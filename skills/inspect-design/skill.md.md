# Inspect Design

## Description
Inspects a design file against DFM rules and process specifications to identify manufacturability issues.

## Trigger
Use this skill when the user asks to inspect, review, check, or validate a design for manufacturability.

## Steps
1. Ask the user for the design file or part number if not provided.
2. Load relevant DFM rules from context.
3. Analyze the design against each applicable rule.
4. Categorize findings by severity: Critical, Major, Minor.
5. Present results in a table with columns: Finding, Rule Violated, Severity, Recommendation.

## Example Prompts
- "Inspect this design for DFM issues"
- "Check if this part is manufacturable"
- "Review my design against process specs"