# DFM Inspector — Deployment Guide

This guide walks you through deploying the DFM Inspector Flask app to AWS so
other Amazon employees can reach it via a URL.

The recommended target is **AWS App Runner** because it takes a container
image, gives you an HTTPS endpoint, scales to zero when idle, and minimizes
networking and load-balancer plumbing. ECS Fargate is a reasonable
alternative if you need finer control over networking or want to put it
behind an internal ALB.

If your team has an existing deployment pattern (Apollo, a shared ECS
cluster, an internal hosting platform), use theirs instead. The container
this guide produces is platform-agnostic.

## Prerequisites

- AWS CLI v2 installed and configured (`aws sts get-caller-identity` should
  return a real role).
- Docker installed locally.
- Permissions in your target AWS account for ECR, App Runner (or ECS),
  CloudWatch Logs, and IAM.
- The app builds and runs locally — see "Local smoke test" below.

If you do not have those permissions in your team's account, talk to whoever
manages the account before continuing.

## 1. Local smoke test

Build and run the container locally first. This catches dependency or import
errors before you spend time on the deploy.

```powershell
docker build -t dfm-inspector .
docker run --rm -p 5000:5000 dfm-inspector
```

In another shell:

```powershell
curl http://localhost:5000/health
# Expected: {"status":"ok"}

# Open http://localhost:5000 in a browser and try uploading a STEP file.
```

If that doesn't work, fix it before deploying. Common issues are missing
system libs (matplotlib needs libfontconfig1, trimesh's `rtree` needs
libspatialindex), which the Dockerfile already addresses.

## 2. Push the image to ECR

Replace `<account-id>` and `<region>` with values for your target account.
Pick the region your team usually uses; `us-west-2` is a common default.

```powershell
$ACCOUNT_ID = "<account-id>"
$REGION     = "us-west-2"
$REPO       = "dfm-inspector"

# Create the ECR repo (one-time).
aws ecr create-repository --repository-name $REPO --region $REGION

# Authenticate Docker to ECR.
aws ecr get-login-password --region $REGION `
  | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"

# Tag and push.
docker tag dfm-inspector:latest "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/${REPO}:latest"
docker push "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/${REPO}:latest"
```

After this step, the image is reachable from App Runner / ECS in the same
account.

## 3. Deploy on AWS App Runner (recommended)

App Runner is the lowest-friction option for a small Flask service.

```powershell
aws apprunner create-service `
  --service-name "dfm-inspector" `
  --source-configuration "{\"ImageRepository\":{\"ImageIdentifier\":\"$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/dfm-inspector:latest\",\"ImageRepositoryType\":\"ECR\",\"ImageConfiguration\":{\"Port\":\"5000\"}},\"AutoDeploymentsEnabled\":true,\"AuthenticationConfiguration\":{\"AccessRoleArn\":\"arn:aws:iam::${ACCOUNT_ID}:role/service-role/AppRunnerECRAccessRole\"}}" `
  --instance-configuration "{\"Cpu\":\"1 vCPU\",\"Memory\":\"2 GB\"}" `
  --health-check-configuration "{\"Protocol\":\"HTTP\",\"Path\":\"/health\",\"Interval\":20,\"Timeout\":10,\"HealthyThreshold\":2,\"UnhealthyThreshold\":5}" `
  --region $REGION
```

App Runner takes about 3-5 minutes to build, deploy, and become reachable.
The output of `create-service` includes a `ServiceUrl` like
`https://abc123.us-west-2.awsapprunner.com` — that is your live URL.

If `create-service` fails with `AppRunnerECRAccessRole does not exist`, run
this once to create it:

```powershell
aws iam create-role `
  --role-name AppRunnerECRAccessRole `
  --assume-role-policy-document '{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"build.apprunner.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}'

aws iam attach-role-policy `
  --role-name AppRunnerECRAccessRole `
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess
```

## 4. Auth — restrict access to Amazon employees

By default the App Runner URL is public (anyone with the URL can reach it).
For an internal Amazon tool that is **not acceptable**.

The right answer for an Amazon-internal tool is a Midway-protected URL via
your team's existing internal hosting pattern (Apollo, internal ALB, etc).
App Runner does not natively support Midway, so two options:

1. **Switch deployment target to ECS Fargate behind an internal ALB**.
   The internal ALB can be configured for Midway via your team's standard
   pattern. This is more setup but is the production-correct answer.

2. **Use App Runner with a temporary IP allowlist** (e.g., your office
   subnet) while you arrange a proper internal hosting solution. Useful for
   demos or short-lived sharing.

Until auth is in place, do not share the URL widely. Treat anything you put
on a public App Runner URL as world-readable.

## 5. Cost notes

App Runner with `1 vCPU / 2 GB` and scale-to-zero (default for low traffic):

- **Idle**: roughly $0/month — App Runner does not bill while paused.
- **Light usage** (a few uploads per day): single-digit dollars/month.
- **Continuous usage**: roughly $40-60/month.

ECS Fargate with a single small task running 24/7: roughly $20-30/month.

Set up a CloudWatch billing alarm if you are bill-sensitive.

## 6. Logs and debugging

App Runner streams stdout/stderr to CloudWatch Logs at
`/aws/apprunner/<service-name>/...`. Tail with:

```powershell
aws logs tail /aws/apprunner/dfm-inspector/application --follow --region $REGION
```

Errors during STEP analysis show up as Python tracebacks. Failures during
container startup show up at the top of the log stream.

## 7. Rolling back

App Runner keeps the previous deployment. To roll back, pause the service:

```powershell
aws apprunner pause-service --service-arn <service-arn> --region $REGION
```

Then push a previous image tag and resume.

For a clean rollback, tag your images with git SHAs (e.g.
`dfm-inspector:c277e07`) instead of `latest`, and update the service to
point at the previous tag.

## 8. Tearing it down

When you're done with the deployment:

```powershell
aws apprunner delete-service --service-arn <service-arn> --region $REGION
aws ecr delete-repository --repository-name dfm-inspector --force --region $REGION
```

This stops all charges. Verify in the AWS billing console afterwards that
no surprise resources are still running.

## Known limitations

These are real concerns the current code carries into production. None of
them block a demo deployment but each should be addressed before "anyone
internal can use it" usage:

- **No auth.** Anyone with the URL can use the service. See section 4.
- **Upload storage is ephemeral.** `tempfile.gettempdir()` is wiped when the
  container restarts. For multi-user persistence, swap to S3.
- **In-process LRU parser cache.** Per-replica only; if App Runner spawns
  multiple instances, cache hit rates degrade. Acceptable for this app.
- **No metrics or alarms.** CloudWatch will capture logs, but custom metrics
  (analyses/sec, error rates) require app-side instrumentation.
- **Synchronous analysis.** Long-running STEP analyses block the worker.
  The 300s gunicorn timeout in the Dockerfile mitigates worst-case but
  large parts may need a background-job pattern long-term.
