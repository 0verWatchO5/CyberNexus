"""
Report Generator - Generates formatted reports from scan results
"""

import json
from datetime import datetime
import os
from rich.console import Console
from colorama import Fore, Style

console = Console()

class ReportGenerator:
    def __init__(self):
        pass
    
    def generate_report(self, results, output_file, format='json'):
        """Generate a report in the specified format"""
        try:
            if format == 'json':
                return self._generate_json_report(results, output_file)
            elif format == 'html':
                return self._generate_html_report(results, output_file)
            elif format == 'txt':
                return self._generate_text_report(results, output_file)
            else:
                console.print(f"[bold red]Unsupported report format: {format}[/bold red]")
                return False
        except Exception as e:
            console.print(f"[bold red]Error generating report: {str(e)}[/bold red]")
            return False
    
    def _generate_json_report(self, results, output_file):
        """Generate a JSON report"""
        try:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            return True
        except Exception as e:
            console.print(f"[bold red]Error generating JSON report: {str(e)}[/bold red]")
            return False
    
    def _generate_html_report(self, results, output_file):
        """Generate an HTML report"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            metadata = results.get('metadata', {})
            scan_results = results.get('results', {})
            
            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberNexus Scan Report - {timestamp}</title>
    <style>
        :root {{
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --accent-color: #e74c3c;
            --success-color: #2ecc71;
            --warning-color: #f39c12;
            --light-color: #ecf0f1;
            --dark-color: #34495e;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: #333;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        
        header {{
            background-color: var(--primary-color);
            color: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
        }}
        
        header h1 {{
            margin: 0;
            font-size: 2.2em;
        }}
        
        header p {{
            margin: 5px 0 0;
            opacity: 0.8;
        }}
        
        .logo {{
            font-weight: bold;
            font-size: 1.2em;
            margin-bottom: 10px;
            color: var(--secondary-color);
        }}
        
        .summary {{
            background-color: var(--light-color);
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .summary h2 {{
            margin-top: 0;
            color: var(--primary-color);
            border-bottom: 2px solid var(--secondary-color);
            padding-bottom: 10px;
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .summary-item {{
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            text-align: center;
        }}
        
        .summary-item h3 {{
            margin-top: 0;
            color: var(--dark-color);
        }}
        
        .summary-item p {{
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .summary-item.high p {{
            color: var(--accent-color);
        }}
        
        .summary-item.medium p {{
            color: var(--warning-color);
        }}
        
        .summary-item.low p {{
            color: var(--secondary-color);
        }}
        
        .summary-item.total p {{
            color: var(--dark-color);
        }}
        
        .scan-type {{
            margin-bottom: 40px;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .scan-type h2 {{
            color: var(--primary-color);
            border-bottom: 2px solid var(--secondary-color);
            padding-bottom: 10px;
            margin-top: 0;
        }}
        
        .vulnerability {{
            background-color: #fff;
            border-left: 4px solid var(--accent-color);
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .vulnerability.info {{
            border-left-color: var(--secondary-color);
        }}
        
        .vulnerability.warning {{
            border-left-color: var(--warning-color);
        }}
        
        .vulnerability.success {{
            border-left-color: var(--success-color);
        }}
        
        .vulnerability pre {{
            background-color: #f8f9fa;
            padding: 10px;
            overflow-x: auto;
            border-radius: 3px;
            margin: 10px 0;
        }}
        
        footer {{
            margin-top: 30px;
            text-align: center;
            font-size: 0.9em;
            color: #7f8c8d;
            padding: 20px;
            background-color: var(--primary-color);
            color: white;
            border-radius: 5px;
        }}
        
        .metadata {{
            background-color: var(--light-color);
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        
        .metadata table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .metadata table td {{
            padding: 8px;
        }}
        
        .metadata table td:first-child {{
            font-weight: bold;
            width: 200px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">CyberNexus</div>
            <h1>Security Scan Report</h1>
            <p>Generated on: {timestamp}</p>
        </header>
        
        <div class="metadata">
            <h2>Scan Metadata</h2>
            <table>
                <tr>
                    <td>Target:</td>
                    <td>{metadata.get('target', 'Unknown')}</td>
                </tr>
                <tr>
                    <td>Scan Time:</td>
                    <td>{metadata.get('timestamp', timestamp)}</td>
                </tr>
                <tr>
                    <td>Scanner Version:</td>
                    <td>CyberNexus 1.0</td>
                </tr>
            </table>
        </div>
        
        <div class="summary">
            <h2>Scan Summary</h2>
            <div class="summary-grid">
                <div class="summary-item total">
                    <h3>Total Issues</h3>
                    <p>{metadata.get('summary', {}).get('total_issues', 0)}</p>
                </div>
                <div class="summary-item high">
                    <h3>High Severity</h3>
                    <p>{metadata.get('summary', {}).get('high_severity', 0)}</p>
                </div>
                <div class="summary-item medium">
                    <h3>Medium Severity</h3>
                    <p>{metadata.get('summary', {}).get('medium_severity', 0)}</p>
                </div>
                <div class="summary-item low">
                    <h3>Low Severity</h3>
                    <p>{metadata.get('summary', {}).get('low_severity', 0)}</p>
                </div>
            </div>
        </div>
"""
            
            # Add results for each scan type
            for scan_type, scan_results in scan_results.items():
                html += f"""
        <div class="scan-type">
            <h2>{scan_type.upper()} Scan Results</h2>
"""
                
                if isinstance(scan_results, list):
                    for issue in scan_results:
                        # Determine if it's an info message or a vulnerability
                        css_class = "vulnerability"
                        if "No" in issue or "not" in issue or "Note:" in issue:
                            css_class += " info"
                        elif "warning" in issue.lower() or "potential" in issue.lower():
                            css_class += " warning"
                        elif "vulnerable" in issue.lower() or "found" in issue.lower():
                            css_class += ""  # Default is vulnerability (red)
                        else:
                            css_class += " info"
                        
                        html += f"""
            <div class="{css_class}">
                <p>{issue}</p>
            </div>
"""
                elif isinstance(scan_results, dict):
                    # Handle vulnerable flag specially
                    if "vulnerable" in scan_results:
                        if scan_results["vulnerable"]:
                            html += f"""
            <div class="vulnerability">
                <h3>Vulnerable: Yes</h3>
            </div>
"""
                        else:
                            html += f"""
            <div class="vulnerability success">
                <h3>Vulnerable: No</h3>
            </div>
"""
                    
                    # Handle other key-value pairs
                    for key, value in scan_results.items():
                        if key != "vulnerable" and key != "details":
                            html += f"""
            <div class="vulnerability info">
                <h3>{key}</h3>
                <p>{value}</p>
            </div>
"""
                    
                    # Handle details list
                    if "details" in scan_results and isinstance(scan_results["details"], list):
                        for detail in scan_results["details"]:
                            css_class = "vulnerability"
                            if "error" in detail.lower() or "vulnerable" in detail.lower():
                                css_class += ""  # Default is vulnerability (red)
                            elif "warning" in detail.lower() or "potential" in detail.lower():
                                css_class += " warning"
                            elif "recommendation" in detail.lower() or "protected" in detail.lower():
                                css_class += " success"
                            else:
                                css_class += " info"
                            
                            html += f"""
            <div class="{css_class}">
                <p>{detail}</p>
            </div>
"""
                else:
                    html += f"""
            <div class="vulnerability info">
                <p>{scan_results}</p>
            </div>
"""
                
                html += """
        </div>
"""
            
            html += """
        <footer>
            <p>CyberNexus - Advanced Web Security Scanner</p>
            <p>Developed for security professionals and penetration testers</p>
        </footer>
    </div>
</body>
</html>
"""
            
            with open(output_file, 'w') as f:
                f.write(html)
            
            return True
            
        except Exception as e:
            console.print(f"[bold red]Error generating HTML report: {str(e)}[/bold red]")
            return False
    
    def _generate_text_report(self, results, output_file):
        """Generate a plain text report"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            metadata = results.get('metadata', {})
            scan_results = results.get('results', {})
            
            text = f"CyberNexus Security Scan Report\n"
            text += f"===============================\n\n"
            text += f"Generated on: {timestamp}\n"
            text += f"Target: {metadata.get('target', 'Unknown')}\n"
            text += f"Scanner Version: CyberNexus 1.0\n\n"
            
            text += f"Scan Summary\n"
            text += f"------------\n"
            text += f"Total Issues: {metadata.get('summary', {}).get('total_issues', 0)}\n"
            text += f"High Severity: {metadata.get('summary', {}).get('high_severity', 0)}\n"
            text += f"Medium Severity: {metadata.get('summary', {}).get('medium_severity', 0)}\n"
            text += f"Low Severity: {metadata.get('summary', {}).get('low_severity', 0)}\n\n"
            
            # Add results for each scan type
            for scan_type, scan_results in scan_results.items():
                text += f"{scan_type.upper()} Scan Results\n"
                text += f"{'-' * len(scan_type + ' Scan Results')}\n"
                
                if isinstance(scan_results, list):
                    for issue in scan_results:
                        text += f"- {issue}\n"
                elif isinstance(scan_results, dict):
                    if "vulnerable" in scan_results:
                        text += f"Vulnerable: {'Yes' if scan_results['vulnerable'] else 'No'}\n"
                    
                    for key, value in scan_results.items():
                        if key != "vulnerable" and key != "details":
                            text += f"{key}: {value}\n"
                    
                    if "details" in scan_results and isinstance(scan_results["details"], list):
                        text += f"\nDetails:\n"
                        for detail in scan_results["details"]:
                            text += f"- {detail}\n"
                else:
                    text += f"{scan_results}\n"
                
                text += f"\n"
            
            with open(output_file, 'w') as f:
                f.write(text)
            
            return True
            
        except Exception as e:
            console.print(f"[bold red]Error generating text report: {str(e)}[/bold red]")
            return False