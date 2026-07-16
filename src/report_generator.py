"""
Generate DFM inspection reports
"""
from typing import Dict
from datetime import datetime
import json


class ReportGenerator:
    """Generate inspection reports in various formats"""
    
    def __init__(self):
        self.template = None
    
    def generate_text_report(self, results: Dict) -> str:
        """Generate plain text report"""
        report = []
        report.append("=" * 80)
        report.append("DFM INSPECTION REPORT")
        report.append("=" * 80)
        report.append(f"File: {results['file']}")
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        summary = results['summary']
        report.append("SUMMARY")
        report.append("-" * 80)
        report.append(f"Manufacturability Score: {summary['manufacturability_score']}/100")
        report.append(f"Total Issues: {summary['total_issues']}")
        report.append(f"Total Warnings: {summary['total_warnings']}")
        report.append(f"Passed Checks: {summary['total_passed']}")
        report.append("")
        
        # Issues
        if results['issues']:
            report.append("ISSUES (CRITICAL)")
            report.append("-" * 80)
            for i, issue in enumerate(results['issues'], 1):
                report.append(f"{i}. [{issue['category']}] {issue['message']}")
                if 'location' in issue:
                    report.append(f"   Location: {issue['location']}")
                if 'recommendation' in issue:
                    report.append(f"   Recommendation: {issue['recommendation']}")
                report.append("")
        
        # Warnings
        if results['warnings']:
            report.append("WARNINGS")
            report.append("-" * 80)
            for i, warning in enumerate(results['warnings'], 1):
                report.append(f"{i}. [{warning['category']}] {warning['message']}")
                if 'recommendation' in warning:
                    report.append(f"   Recommendation: {warning['recommendation']}")
                report.append("")
        
        # Passed checks
        if results['passed']:
            report.append("PASSED CHECKS")
            report.append("-" * 80)
            for check in results['passed']:
                report.append(f"✓ {check['category']}: {check['details']}")
            report.append("")
        
        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def generate_json_report(self, results: Dict) -> str:
        """Generate JSON report"""
        report_data = {
            'metadata': {
                'file': results['file'],
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            },
            'summary': results['summary'],
            'issues': results['issues'],
            'warnings': results['warnings'],
            'passed': results['passed']
        }
        
        return json.dumps(report_data, indent=2)
    
    def generate_html_report(self, results: Dict) -> str:
        """Generate HTML report"""
        score = results['summary']['manufacturability_score']
        
        # Determine score color
        if score >= 80:
            score_color = '#28a745'
        elif score >= 60:
            score_color = '#ffc107'
        else:
            score_color = '#dc3545'
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>DFM Inspection Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .summary-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }}
        .summary-card h3 {{ margin: 0; color: #666; font-size: 14px; }}
        .summary-card .value {{ font-size: 32px; font-weight: bold; margin: 10px 0; }}
        .score {{ color: {score_color}; }}
        .issue {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 10px 0; }}
        .issue.critical {{ background: #f8d7da; border-left-color: #dc3545; }}
        .passed {{ background: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 10px 0; }}
        .category {{ font-weight: bold; color: #007bff; }}
        .recommendation {{ margin-top: 10px; font-style: italic; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>DFM Inspection Report</h1>
        <p><strong>File:</strong> {results['file']}</p>
        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Manufacturability Score</h3>
                <div class="value score">{score:.1f}/100</div>
            </div>
            <div class="summary-card">
                <h3>Issues</h3>
                <div class="value" style="color: #dc3545;">{results['summary']['total_issues']}</div>
            </div>
            <div class="summary-card">
                <h3>Warnings</h3>
                <div class="value" style="color: #ffc107;">{results['summary']['total_warnings']}</div>
            </div>
            <div class="summary-card">
                <h3>Passed</h3>
                <div class="value" style="color: #28a745;">{results['summary']['total_passed']}</div>
            </div>
        </div>
"""
        
        # Add issues
        if results['issues']:
            html += "<h2>Issues</h2>"
            for issue in results['issues']:
                html += f"""
        <div class="issue critical">
            <span class="category">{issue['category']}</span>: {issue['message']}
            {f'<div class="recommendation">💡 {issue["recommendation"]}</div>' if 'recommendation' in issue else ''}
        </div>
"""
        
        # Add warnings
        if results['warnings']:
            html += "<h2>Warnings</h2>"
            for warning in results['warnings']:
                html += f"""
        <div class="issue">
            <span class="category">{warning['category']}</span>: {warning['message']}
            {f'<div class="recommendation">💡 {warning["recommendation"]}</div>' if 'recommendation' in warning else ''}
        </div>
"""
        
        # Add passed checks
        if results['passed']:
            html += "<h2>Passed Checks</h2>"
            for check in results['passed']:
                html += f"""
        <div class="passed">
            ✓ <span class="category">{check['category']}</span>: {check['details']}
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        return html
    
    def save_report(self, results: Dict, output_path: str, format: str = 'html'):
        """Save report to file"""
        if format == 'text':
            content = self.generate_text_report(results)
        elif format == 'json':
            content = self.generate_json_report(results)
        elif format == 'html':
            content = self.generate_html_report(results)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        return output_path
