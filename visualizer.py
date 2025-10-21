#!/usr/bin/env python3
"""
Enhanced AWS Network Visualization Tool

Creates interactive network diagrams with visual flow and grouped subnet cards.

Usage:
    python enhanced_visualizer.py network_discovery.json

Requirements:
    pip install jinja2
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class EnhancedNetworkVisualizer:
    """Create interactive network documentation with flow diagrams"""
    
    def __init__(self, discovery_file: str):
        """Initialize visualizer with discovery data"""
        self.discovery_file = discovery_file
        self.data = self._load_data()
        self.output_dir = "network_reports"
        Path(self.output_dir).mkdir(exist_ok=True)
    
    def _load_data(self) -> Dict:
        """Load discovery data from JSON file"""
        try:
            with open(self.discovery_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"ERROR: File not found: {self.discovery_file}")
            exit(1)
        except json.JSONDecodeError:
            print(f"ERROR: Invalid JSON in file: {self.discovery_file}")
            exit(1)
    
    def create_html_report(self):
        """Create comprehensive HTML report with flow diagram"""
        region = self.data.get('region', 'unknown')
        timestamp = self.data.get('timestamp', '')
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS Network Report - {region}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #232f3e;
            border-bottom: 3px solid #ff9900;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        
        h2 {{
            color: #232f3e;
            margin-top: 40px;
            margin-bottom: 20px;
            padding: 10px;
            background: #f8f9fa;
            border-left: 4px solid #ff9900;
        }}
        
        h3 {{
            color: #232f3e;
            margin-top: 25px;
            margin-bottom: 15px;
        }}
        
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .card.green {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }}
        
        .card.blue {{
            background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
        }}
        
        .card.orange {{
            background: linear-gradient(135deg, #f46b45 0%, #eea849 100%);
        }}
        
        .card h3 {{
            margin: 0 0 10px 0;
            color: white;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .card .number {{
            font-size: 48px;
            font-weight: bold;
        }}
        
        .flow-diagram {{
            background: #f8f9fa;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            padding: 30px;
            margin: 30px 0;
            min-height: 400px;
            overflow-x: auto;
        }}
        
        .flow-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 30px;
        }}
        
        .flow-row {{
            display: flex;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        
        .flow-item {{
            background: white;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            padding: 15px 20px;
            min-width: 150px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            position: relative;
        }}
        
        .flow-item.internet {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: bold;
        }}
        
        .flow-item.igw {{
            background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
            color: white;
            font-weight: bold;
        }}
        
        .flow-item.nat {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            font-weight: bold;
        }}
        
        .flow-item.vpc {{
            background: linear-gradient(135deg, #f46b45 0%, #eea849 100%);
            color: white;
            font-weight: bold;
            font-size: 18px;
        }}
        
        .flow-arrow {{
            font-size: 24px;
            color: #6c757d;
        }}
        
        .vpc-section {{
            margin: 40px 0;
            padding: 20px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            background: #fafafa;
        }}
        
        .vpc-header {{
            background: #232f3e;
            color: white;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
        }}
        
        .vpc-header h3 {{
            margin: 0;
            color: white;
        }}
        
        .subnet-group {{
            margin: 30px 0;
        }}
        
        .subnet-group-header {{
            background: #495057;
            color: white;
            padding: 12px 20px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 18px;
            font-weight: bold;
        }}
        
        .subnet-group-header.public {{
            background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
        }}
        
        .subnet-group-header.private {{
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }}
        
        .subnet-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}
        
        .subnet-card {{
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .subnet-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .subnet-card.public {{
            border-left: 6px solid #2193b0;
        }}
        
        .subnet-card.private {{
            border-left: 6px solid #764ba2;
        }}
        
        .subnet-card h4 {{
            margin-bottom: 15px;
            color: #232f3e;
            font-size: 16px;
        }}
        
        .subnet-info {{
            margin: 10px 0;
        }}
        
        .subnet-info-row {{
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            padding: 8px;
            background: #f8f9fa;
            border-radius: 4px;
            font-size: 13px;
        }}
        
        .subnet-info-label {{
            font-weight: 600;
            color: #495057;
        }}
        
        .subnet-info-value {{
            font-family: 'Courier New', monospace;
            color: #212529;
        }}
        
        .subnet-acl {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #dee2e6;
        }}
        
        .subnet-acl-header {{
            font-weight: 600;
            color: #495057;
            margin-bottom: 10px;
            font-size: 14px;
        }}
        
        .acl-summary {{
            background: #e9ecef;
            padding: 10px;
            border-radius: 4px;
            font-size: 12px;
        }}
        
        .acl-rule {{
            padding: 6px;
            margin: 4px 0;
            background: white;
            border-left: 3px solid #6c757d;
            border-radius: 3px;
            font-size: 11px;
            font-family: 'Courier New', monospace;
        }}
        
        .acl-rule.allow {{
            border-left-color: #28a745;
        }}
        
        .acl-rule.deny {{
            border-left-color: #dc3545;
        }}
        
        .acl-rule-explanation {{
            margin-top: 4px;
            font-size: 10px;
            color: #495057;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.4;
        }}
        
        .security-risk {{
            background: #fff3cd;
            border: 2px solid #ffc107;
            padding: 12px;
            border-radius: 6px;
            margin: 15px 0;
        }}
        
        .security-risk.high {{
            background: #f8d7da;
            border-color: #dc3545;
        }}
        
        .security-risk.critical {{
            background: #721c24;
            border-color: #491217;
            color: white;
        }}
        
        .security-risk-header {{
            font-weight: 700;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .security-risk-list {{
            font-size: 13px;
            margin: 8px 0;
            padding-left: 20px;
        }}
        
        .security-risk-list li {{
            margin: 6px 0;
        }}
        
        .security-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            margin-left: 10px;
        }}
        
        .security-badge.critical {{
            background: #dc3545;
            color: white;
        }}
        
        .security-badge.high {{
            background: #fd7e14;
            color: white;
        }}
        
        .security-badge.medium {{
            background: #ffc107;
            color: #000;
        }}
        
        .security-badge.low {{
            background: #28a745;
            color: white;
        }}
        
        .security-badge.secure {{
            background: #28a745;
            color: white;
        }}
        
        .acl-rule.security-risk {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            border: 2px solid #ffc107;
        }}
        
        .acl-rule.security-risk.high {{
            background: #f8d7da;
            border-left: 4px solid #dc3545;
            border-color: #dc3545;
        }}
        
        .acl-rule.security-risk.critical {{
            background: #f8d7da;
            border-left: 4px solid #721c24;
            border-color: #721c24;
        }}
        
        .subnet-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}
        
        .subnet-card h4 {{
            margin: 0;
        }}
        
        .info-box ul {{
            margin: 8px 0;
            padding-left: 20px;
        }}
        
        .info-box li {{
            margin: 4px 0;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .badge.public {{
            background: #e3f2fd;
            color: #1565c0;
        }}
        
        .badge.private {{
            background: #f3e5f5;
            color: #6a1b9a;
        }}
        
        .badge.active {{
            background: #e8f5e9;
            color: #2e7d32;
        }}
        
        .route-table {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 6px;
            padding: 15px;
            margin: 15px 0;
        }}
        
        .route-entry {{
            padding: 8px;
            margin: 5px 0;
            background: #f8f9fa;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }}
        
        .route-entry.igw {{
            border-left: 3px solid #2193b0;
        }}
        
        .route-entry.nat {{
            border-left: 3px solid #11998e;
        }}
        
        .route-entry.local {{
            border-left: 3px solid #999;
        }}
        
        .info-box {{
            background: #e3f2fd;
            border-left: 4px solid #1976d2;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        .code {{
            font-family: 'Courier New', monospace;
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 13px;
        }}
        
        .meta-info {{
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        th {{
            background: #232f3e;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 AWS Network Infrastructure Report</h1>
        <div class="meta-info">
            <strong>Region:</strong> {region} | 
            <strong>Generated:</strong> {timestamp}
        </div>
"""
        
        # Add interpretation guide
        html_content += """
        <div class="info-box" style="margin: 20px 0;">
            <h3 style="margin-top: 0;">📖 Quick Reference Guide</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin-top: 15px;">
                <div>
                    <strong>Security Risk Levels:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; font-size: 13px;">
                        <li>🚨 <strong>CRITICAL:</strong> Immediate action required (SSH/RDP/DB exposed)</li>
                        <li>⚠️ <strong>HIGH:</strong> Serious security concern (SMB, FTP exposed)</li>
                        <li>⚡ <strong>MEDIUM:</strong> Should be reviewed (overly permissive)</li>
                        <li>ℹ️ <strong>LOW:</strong> Minor concern (HTTP vs HTTPS)</li>
                        <li>✅ <strong>SECURE:</strong> No issues detected</li>
                    </ul>
                </div>
                <div>
                    <strong>Common IP Ranges:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; font-size: 13px;">
                        <li><code>0.0.0.0/0</code> = The entire Internet</li>
                        <li><code>10.x.x.x</code> = Internal VPC network</li>
                        <li><code>172.16-31.x.x</code> = Private network (RFC 1918)</li>
                        <li><code>x.x.x.x/32</code> = Single specific IP address</li>
                    </ul>
                </div>
                <div>
                    <strong>Common Ports:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; font-size: 13px;">
                        <li><code>22</code> = SSH (Server access)</li>
                        <li><code>80</code> = HTTP (Web traffic)</li>
                        <li><code>443</code> = HTTPS (Secure web)</li>
                        <li><code>3306</code> = MySQL Database</li>
                        <li><code>5432</code> = PostgreSQL Database</li>
                        <li><code>1521</code> = Oracle Database</li>
                        <li><code>3389</code> = RDP (Remote Desktop)</li>
                        <li><code>32768-65535</code> = Ephemeral (return traffic)</li>
                    </ul>
                </div>
                <div>
                    <strong>Security Best Practices:</strong>
                    <ul style="margin: 8px 0; padding-left: 20px; font-size: 13px;">
                        <li>🚨 Never expose SSH/RDP to <code>0.0.0.0/0</code></li>
                        <li>🔒 Database ports should only allow internal traffic</li>
                        <li>✅ Use security groups for instance-level control</li>
                        <li>✅ Public subnets should restrict inbound access</li>
                        <li>✅ Use HTTPS (443) instead of HTTP (80) when possible</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <h2>📊 Summary</h2>
        <div class="summary-cards">
            <div class="card">
                <h3>VPCs</h3>
                <div class="number">{summary.get('total_vpcs', 0)}</div>
            </div>
            <div class="card green">
                <h3>Public Subnets</h3>
                <div class="number">{summary.get('public_subnets', 0)}</div>
            </div>
            <div class="card blue">
                <h3>Private Subnets</h3>
                <div class="number">{summary.get('private_subnets', 0)}</div>
            </div>
            <div class="card orange">
                <h3>NAT Gateways</h3>
                <div class="number">{summary.get('nat_gateways', 0)}</div>
            </div>
        </div>
"""
        
        # VPC Details with Flow Diagrams
        for vpc in self.data.get('vpcs', []):
            html_content += self._generate_vpc_section_with_flow(vpc)
        
        # Connectivity Section
        html_content += self._generate_connectivity_section()
        
        html_content += """
    </div>
</body>
</html>
"""
        
        # Save HTML file
        filename = f"{self.output_dir}/network_report_{region}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(filename, 'w') as f:
            f.write(html_content)
        
        print(f"✅ HTML report created: {filename}")
        return filename
    
    def _generate_vpc_security_summary(self, vpc: Dict, nacl_map: Dict) -> str:
        """Generate security summary for entire VPC"""
        all_risks = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        # Analyze all subnets
        for subnet in vpc.get('subnets', []):
            subnet_id = subnet['subnet_id']
            if subnet_id in nacl_map:
                security_score = self._calculate_subnet_security_score(nacl_map[subnet_id])
                
                for level in ['critical', 'high', 'medium', 'low']:
                    for risk_item in security_score['risks'][level]:
                        all_risks[level].append({
                            'subnet_name': subnet.get('name', 'N/A'),
                            'subnet_id': subnet_id,
                            'rule_number': risk_item['rule_number'],
                            'reason': risk_item['reason']
                        })
        
        total_issues = sum(len(all_risks[level]) for level in all_risks)
        
        if total_issues == 0:
            return """
                <div class="info-box" style="background: #d4edda; border-left-color: #28a745;">
                    <strong>✅ No Security Issues Detected</strong>
                    <p style="margin: 8px 0 0 0;">All Network ACL rules appear to follow security best practices.</p>
                </div>
"""
        
        # Determine overall severity
        if len(all_risks['critical']) > 0:
            severity = 'critical'
            severity_text = 'CRITICAL SECURITY ISSUES'
            icon = '🚨'
        elif len(all_risks['high']) > 0:
            severity = 'high'
            severity_text = 'HIGH SECURITY RISKS'
            icon = '⚠️'
        elif len(all_risks['medium']) > 0:
            severity = 'medium'
            severity_text = 'MEDIUM SECURITY CONCERNS'
            icon = '⚡'
        else:
            severity = 'low'
            severity_text = 'LOW SECURITY NOTES'
            icon = 'ℹ️'
        
        html = f"""
            <div class="security-risk {severity}" style="margin: 20px 0;">
                <div class="security-risk-header" style="font-size: 16px;">
                    {icon} {severity_text} - {total_issues} Issue(s) Found
                </div>
                <p style="margin: 8px 0;">Review and remediate the following security issues:</p>
"""
        
        for level in ['critical', 'high', 'medium', 'low']:
            if len(all_risks[level]) > 0:
                level_icon = {'critical': '🚨', 'high': '⚠️', 'medium': '⚡', 'low': 'ℹ️'}[level]
                html += f"""
                <div style="margin-top: 15px;">
                    <strong style="text-transform: uppercase;">{level_icon} {level} ({len(all_risks[level])})</strong>
                    <ul class="security-risk-list">
"""
                for risk in all_risks[level]:
                    html += f"""
                        <li><strong>{risk['subnet_name']}</strong> - Rule #{risk['rule_number']}: {risk['reason']}</li>
"""
                html += """
                    </ul>
                </div>
"""
        
        html += """
            </div>
"""
        
        return html
    
    def _generate_vpc_section_with_flow(self, vpc: Dict) -> str:
        """Generate VPC section with flow diagram and grouped subnets"""
        vpc_id = vpc['vpc_id']
        vpc_name = vpc.get('name', 'N/A')
        vpc_cidr = vpc['cidr_block']
        
        html = f"""
        <div class="vpc-section">
            <div class="vpc-header">
                <h3>{vpc_name}</h3>
                <div><strong>VPC ID:</strong> {vpc_id}</div>
                <div><strong>CIDR:</strong> {vpc_cidr}</div>
            </div>
"""
        
        # Build NACL map first for security analysis
        nacl_map = self._build_nacl_map(vpc)
        
        # Add VPC-level security summary
        html += self._generate_vpc_security_summary(vpc, nacl_map)
        
        # Network Flow Diagram
        html += self._generate_flow_diagram(vpc)
        
        # Group subnets by type
        public_subnets = [s for s in vpc.get('subnets', []) if s.get('subnet_type') == 'Public']
        private_subnets = [s for s in vpc.get('subnets', []) if s.get('subnet_type') == 'Private']
        
        # Public Subnets Group
        if public_subnets:
            html += """
            <div class="subnet-group">
                <div class="subnet-group-header public">
                    🌐 Public Subnets
                </div>
                <div class="subnet-grid">
"""
            for subnet in public_subnets:
                html += self._generate_subnet_card(subnet, nacl_map, 'public')
            
            html += "</div></div>"
        
        # Private Subnets Group
        if private_subnets:
            html += """
            <div class="subnet-group">
                <div class="subnet-group-header private">
                    🔒 Private Subnets
                </div>
                <div class="subnet-grid">
"""
            for subnet in private_subnets:
                html += self._generate_subnet_card(subnet, nacl_map, 'private')
            
            html += "</div></div>"
        
        # Route Tables
        html += "<h3>🗺️ Route Tables</h3>"
        for rt in vpc.get('route_tables', []):
            html += self._generate_route_table(rt, vpc)
        
        html += "</div>"
        
        return html
    
    def _generate_flow_diagram(self, vpc: Dict) -> str:
        """Generate network flow visualization"""
        has_igw = vpc.get('internet_gateway') is not None
        nat_gateways = vpc.get('nat_gateways', [])
        has_vpn = vpc.get('vpn_gateway') is not None
        
        html = """
        <h3>📊 Network Flow</h3>
        <div class="flow-diagram">
            <div class="flow-container">
"""
        
        # Internet level
        if has_igw or has_vpn:
            html += """
                <div class="flow-row">
                    <div class="flow-item internet">🌐 Internet</div>
"""
            if has_vpn:
                html += """
                    <div class="flow-item internet">🔒 On-Premises</div>
"""
            html += "</div>"
            
            html += """
                <div class="flow-arrow">↓</div>
"""
        
        # Gateway level
        html += '<div class="flow-row">'
        
        if has_igw:
            igw = vpc['internet_gateway']
            html += f"""
                <div class="flow-item igw">
                    Internet Gateway<br>
                    <small>{igw['igw_id']}</small>
                </div>
"""
        
        if has_vpn:
            vgw = vpc['vpn_gateway']
            html += f"""
                <div class="flow-item igw">
                    VPN Gateway<br>
                    <small>{vgw['vgw_id']}</small>
                </div>
"""
        
        html += '</div>'
        
        html += """
            <div class="flow-arrow">↓</div>
"""
        
        # VPC level
        html += f"""
            <div class="flow-row">
                <div class="flow-item vpc">
                    VPC: {vpc.get('name', 'N/A')}<br>
                    <small>{vpc['cidr_block']}</small>
                </div>
            </div>
"""
        
        html += """
            <div class="flow-arrow">↓</div>
"""
        
        # Subnets level
        public_count = len([s for s in vpc.get('subnets', []) if s.get('subnet_type') == 'Public'])
        private_count = len([s for s in vpc.get('subnets', []) if s.get('subnet_type') == 'Private'])
        
        html += '<div class="flow-row">'
        
        if public_count > 0:
            html += f"""
                <div class="flow-item" style="background: #e3f2fd; border-color: #2193b0; font-weight: bold;">
                    {public_count} Public Subnet{'s' if public_count > 1 else ''}<br>
                    <small>Direct Internet Access</small>
                </div>
"""
        
        if len(nat_gateways) > 0:
            html += f"""
                <div class="flow-item nat">
                    {len(nat_gateways)} NAT Gateway{'s' if len(nat_gateways) > 1 else ''}<br>
                    <small>Outbound Only</small>
                </div>
"""
        
        html += '</div>'
        
        if private_count > 0:
            html += """
                <div class="flow-arrow">↓</div>
                <div class="flow-row">
                    <div class="flow-item" style="background: #f3e5f5; border-color: #764ba2; font-weight: bold;">
"""
            html += f"""
                        {private_count} Private Subnet{'s' if private_count > 1 else ''}<br>
                        <small>No Direct Internet Access</small>
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
"""
        
        return html
    
    def _build_nacl_map(self, vpc: Dict) -> Dict:
        """Build mapping of subnet to NACL"""
        nacl_map = {}
        
        for nacl in vpc.get('nacls', []):
            nacl_id = nacl['nacl_id']
            nacl_name = nacl.get('name', 'N/A')
            
            for subnet_id in nacl.get('associated_subnets', []):
                nacl_map[subnet_id] = {
                    'nacl_id': nacl_id,
                    'nacl_name': nacl_name,
                    'is_default': nacl.get('is_default', False),
                    'inbound_rules': nacl.get('inbound_rules', [])[:5],
                    'outbound_rules': nacl.get('outbound_rules', [])[:5]
                }
        
        return nacl_map
    
    def _analyze_security_risk(self, rule: Dict, direction: str) -> Dict:
        """Analyze security risk level of a rule"""
        action = rule['action']
        protocol = rule['protocol']
        cidr = rule['cidr']
        port_range = rule.get('port_range', 'All')
        
        risk = {
            'level': 'none',
            'reason': ''
        }
        
        # Only analyze ALLOW rules for inbound from internet
        if action == 'allow' and direction == 'inbound' and cidr == '0.0.0.0/0':
            # Critical risks - Administrative and Database access
            if port_range == '22':
                risk = {
                    'level': 'critical',
                    'reason': '🚨 CRITICAL: SSH port 22 open to entire Internet! This allows anyone to attempt SSH access. Restrict to specific IPs.'
                }
            elif port_range == '3389':
                risk = {
                    'level': 'critical',
                    'reason': '🚨 CRITICAL: RDP port 3389 open to entire Internet! This allows anyone to attempt remote desktop access. Restrict to specific IPs.'
                }
            elif port_range == '3306':
                risk = {
                    'level': 'critical',
                    'reason': '🚨 CRITICAL: MySQL port 3306 exposed to Internet! Database should not be publicly accessible. Use private subnets.'
                }
            elif port_range == '5432':
                risk = {
                    'level': 'critical',
                    'reason': '🚨 CRITICAL: PostgreSQL port 5432 exposed to Internet! Database should not be publicly accessible. Use private subnets.'
                }
            elif port_range == '1521':
                risk = {
                    'level': 'critical',
                    'reason': '🚨 CRITICAL: Oracle port 1521 exposed to Internet! Database should not be publicly accessible. Use private subnets.'
                }
            elif port_range == '27017':
                risk = {
                    'level': 'critical',
                    'reason': '🚨 CRITICAL: MongoDB port 27017 exposed to Internet! Database should not be publicly accessible. Use private subnets.'
                }
            elif port_range == '6379':
                risk = {
                    'level': 'critical',
                    'reason': '🚨 CRITICAL: Redis port 6379 exposed to Internet! Cache/database should not be publicly accessible. Use private subnets.'
                }
            elif port_range == '5984':
                risk = {
                    'level': 'critical',
                    'reason': '🚨 CRITICAL: CouchDB port 5984 exposed to Internet! Database should not be publicly accessible.'
                }
            elif port_range == '9200' or port_range == '9300':
                risk = {
                    'level': 'critical',
                    'reason': '🚨 CRITICAL: Elasticsearch exposed to Internet! Search engine should not be publicly accessible.'
                }
            # Critical - All ports open
            elif port_range == '0-65535' or port_range == 'All':
                risk = {
                    'level': 'critical',
                    'reason': '🚨 CRITICAL: ALL ports open to Internet! This is extremely permissive and insecure. Restrict to specific required ports.'
                }
            # High risks - Insecure protocols and ransomware targets
            elif port_range == '23':
                risk = {
                    'level': 'critical',
                    'reason': '🚨 CRITICAL: Telnet port 23 open to Internet! Telnet is unencrypted and insecure. Use SSH instead.'
                }
            elif port_range == '445' or port_range == '139':
                risk = {
                    'level': 'high',
                    'reason': '⚠️ HIGH: SMB/NetBIOS port exposed to Internet. Common ransomware and malware target. Block immediately.'
                }
            elif port_range == '21':
                risk = {
                    'level': 'high',
                    'reason': '⚠️ HIGH: FTP port 21 open to Internet. FTP is unencrypted. Use SFTP/FTPS instead.'
                }
            elif port_range == '25':
                risk = {
                    'level': 'high',
                    'reason': '⚠️ HIGH: SMTP port 25 exposed to Internet. Common spam relay vector. Should be restricted.'
                }
            elif port_range == '53':
                risk = {
                    'level': 'high',
                    'reason': '⚠️ HIGH: DNS port 53 open to Internet. Can be used for DNS amplification attacks.'
                }
            elif port_range == '135' or port_range == '137' or port_range == '138':
                risk = {
                    'level': 'high',
                    'reason': '⚠️ HIGH: Windows RPC/NetBIOS ports exposed. Common attack vector. Block from Internet.'
                }
            # Medium risks - Admin interfaces and development ports
            elif port_range == '8080' or port_range == '8000':
                risk = {
                    'level': 'medium',
                    'reason': '⚠️ MEDIUM: Development/admin port exposed to Internet. Should typically be restricted to internal access.'
                }
            elif port_range == '8443' or port_range == '8888':
                risk = {
                    'level': 'medium',
                    'reason': '⚠️ MEDIUM: Alternative HTTPS/admin port exposed. Verify if intentional and restrict if possible.'
                }
            elif port_range == '9090' or port_range == '9091':
                risk = {
                    'level': 'medium',
                    'reason': '⚠️ MEDIUM: Management/monitoring port exposed. Should be restricted to authorized networks.'
                }
            elif port_range == '5000':
                risk = {
                    'level': 'medium',
                    'reason': '⚠️ MEDIUM: Common development port exposed. Review if public access is required.'
                }
            # Low risks - HTTP
            elif port_range == '80':
                risk = {
                    'level': 'low',
                    'reason': 'ℹ️ Standard HTTP port open. Consider using HTTPS (443) for encrypted traffic.'
                }
            # Acceptable - HTTPS
            elif port_range == '443':
                risk = {
                    'level': 'none',
                    'reason': '✅ Standard HTTPS port for web traffic. This is acceptable.'
                }
        
        # Check for overly permissive rules from private networks
        elif action == 'allow' and direction == 'inbound':
            if port_range == '0-65535' or port_range == 'All':
                risk = {
                    'level': 'medium',
                    'reason': '⚡ MEDIUM: All ports open. Consider restricting to specific required ports for better security.'
                }
        
        return risk
    
    def _calculate_subnet_security_score(self, nacl_info: Dict) -> Dict:
        """Calculate overall security score for a subnet based on its ACL"""
        risks = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        for rule in nacl_info.get('inbound_rules', []):
            if rule['rule_number'] < 32767:
                risk = self._analyze_security_risk(rule, 'inbound')
                if risk['level'] in ['critical', 'high', 'medium', 'low']:
                    risks[risk['level']].append({
                        'rule_number': rule['rule_number'],
                        'reason': risk['reason'],
                        'rule': rule
                    })
        
        # Determine overall risk level
        if len(risks['critical']) > 0:
            overall = 'critical'
        elif len(risks['high']) > 0:
            overall = 'high'
        elif len(risks['medium']) > 0:
            overall = 'medium'
        elif len(risks['low']) > 0:
            overall = 'low'
        else:
            overall = 'secure'
        
        return {
            'overall': overall,
            'risks': risks,
            'total_issues': len(risks['critical']) + len(risks['high']) + len(risks['medium']) + len(risks['low'])
        }
    
    def _interpret_cidr(self, cidr: str) -> str:
        """Provide human-readable interpretation of CIDR blocks"""
        if cidr == '0.0.0.0/0':
            return '🌐 Internet (all IPv4 addresses)'
        elif cidr.startswith('10.'):
            return '🏢 Internal VPC network'
        elif cidr.startswith('172.16.') or cidr.startswith('172.17.'):
            return '🏢 Internal network (RFC 1918)'
        elif cidr.startswith('192.168.'):
            return '🏠 Private network (RFC 1918)'
        elif '/32' in cidr:
            return '🖥️ Single IP address'
        elif '/28' in cidr:
            return '📦 Small subnet (16 IPs)'
        elif '/24' in cidr:
            return '📦 Standard subnet (256 IPs)'
        elif '/22' in cidr:
            return '📦 Medium subnet (1024 IPs)'
        elif '/16' in cidr:
            return '📦 Large subnet (65k IPs)'
        return '📍 Specific network'
    
    def _interpret_port(self, port_range: str, protocol: str) -> str:
        """Provide human-readable interpretation of port ranges"""
        if port_range == 'All':
            return '🔓 All ports/protocols'
        elif port_range == '22':
            return '🔐 SSH (Secure Shell)'
        elif port_range == '80':
            return '🌐 HTTP (Web)'
        elif port_range == '443':
            return '🔒 HTTPS (Secure Web)'
        elif port_range == '3389':
            return '🖥️ RDP (Remote Desktop)'
        elif port_range == '3306':
            return '🗄️ MySQL Database'
        elif port_range == '5432':
            return '🗄️ PostgreSQL Database'
        elif port_range == '1521':
            return '🗄️ Oracle Database'
        elif port_range == '8080':
            return '🌐 Alternative HTTP'
        elif port_range == '8443':
            return '🔒 Alternative HTTPS'
        elif port_range == '8000':
            return '🔧 Development server'
        elif port_range == '0-65535':
            return '🔓 All TCP/UDP ports'
        elif port_range == '32768-65535':
            return '🔄 Ephemeral ports (return traffic)'
        elif '-' in port_range:
            return f'📊 Port range {port_range}'
        else:
            return f'🔌 Port {port_range}'
    
    def _generate_rule_explanation(self, rule: Dict, direction: str) -> str:
        """Generate a human-readable explanation of what the rule does"""
        action = rule['action']
        protocol = rule['protocol']
        cidr = rule['cidr']
        port_range = rule.get('port_range', 'All')
        
        cidr_explain = self._interpret_cidr(cidr)
        port_explain = self._interpret_port(port_range, protocol)
        
        if direction == 'inbound':
            if action == 'allow':
                if cidr == '0.0.0.0/0' and port_range == '0-65535':
                    return '⚠️ Allows ALL traffic from Internet (very permissive)'
                elif cidr == '0.0.0.0/0' and port_range == '22':
                    return '⚠️ SSH accessible from Internet (security concern)'
                elif cidr == '0.0.0.0/0' and port_range == '443':
                    return '✅ HTTPS accessible from Internet (standard for web)'
                elif cidr == '0.0.0.0/0' and port_range == '80':
                    return '✅ HTTP accessible from Internet (standard for web)'
                elif port_range == '32768-65535':
                    return '✅ Allows return traffic (ephemeral ports)'
                elif cidr.startswith('10.') or cidr.startswith('172.'):
                    return f'✅ Allows {port_explain} from internal network'
                else:
                    return f'{cidr_explain} → {port_explain}'
            else:
                return f'🚫 Blocks {port_explain} from {cidr_explain}'
        else:  # outbound
            if action == 'allow':
                if cidr == '0.0.0.0/0' and port_range == 'All':
                    return '✅ Allows ALL outbound traffic (standard)'
                elif cidr == '0.0.0.0/0' and port_range == '443':
                    return '✅ Can make HTTPS requests to Internet'
                elif port_range == '32768-65535':
                    return '✅ Allows response traffic (ephemeral ports)'
                else:
                    return f'{port_explain} → {cidr_explain}'
            else:
                return f'🚫 Blocks outbound to {cidr_explain}'
    
    def _generate_subnet_card(self, subnet: Dict, nacl_map: Dict, subnet_type: str) -> str:
        """Generate individual subnet card with ACL info and security analysis"""
        subnet_id = subnet['subnet_id']
        subnet_name = subnet.get('name', 'N/A')
        
        # Calculate security score if ACL info available
        security_score = None
        if subnet_id in nacl_map:
            security_score = self._calculate_subnet_security_score(nacl_map[subnet_id])
        
        html = f"""
            <div class="subnet-card {subnet_type}">
                <div class="subnet-card-header">
                    <h4>{subnet_name}</h4>
"""
        
        # Add security badge
        if security_score:
            badge_text = security_score['overall'].upper()
            badge_icon = {
                'critical': '🚨',
                'high': '⚠️',
                'medium': '⚡',
                'low': 'ℹ️',
                'secure': '✅'
            }.get(security_score['overall'], '❓')
            
            html += f"""
                    <span class="security-badge {security_score['overall']}" title="{security_score['total_issues']} security issue(s) found">
                        {badge_icon} {badge_text}
                    </span>
"""
        
        html += f"""
                </div>
                <div class="subnet-info">
                    <div class="subnet-info-row">
                        <span class="subnet-info-label">Subnet ID:</span>
                        <span class="subnet-info-value">{subnet_id}</span>
                    </div>
                    <div class="subnet-info-row">
                        <span class="subnet-info-label">CIDR Block:</span>
                        <span class="subnet-info-value">{subnet['cidr_block']}</span>
                    </div>
                    <div class="subnet-info-row">
                        <span class="subnet-info-label">Availability Zone:</span>
                        <span class="subnet-info-value">{subnet['availability_zone']}</span>
                    </div>
                    <div class="subnet-info-row">
                        <span class="subnet-info-label">Available IPs:</span>
                        <span class="subnet-info-value">{subnet['available_ip_count']}</span>
                    </div>
                </div>
"""
        
        # Add security risk summary if there are issues
        if security_score and security_score['total_issues'] > 0:
            risk_class = security_score['overall']
            html += f"""
                <div class="security-risk {risk_class}">
                    <div class="security-risk-header">
                        🛡️ Security Issues Detected ({security_score['total_issues']})
                    </div>
                    <ul class="security-risk-list">
"""
            
            for level in ['critical', 'high', 'medium', 'low']:
                for risk_item in security_score['risks'][level]:
                    html += f"""
                        <li><strong>Rule #{risk_item['rule_number']}:</strong> {risk_item['reason']}</li>
"""
            
            html += """
                    </ul>
                </div>
"""
        
        # Add NACL information
        if subnet_id in nacl_map:
            nacl_info = nacl_map[subnet_id]
            default_text = ' (Default)' if nacl_info['is_default'] else ''
            
            html += f"""
                <div class="subnet-acl">
                    <div class="subnet-acl-header">🛡️ Network ACL: {nacl_info['nacl_name']}{default_text}</div>
                    <div class="acl-summary">
                        <div style="font-weight: 600; margin-bottom: 5px;">Inbound Rules:</div>
"""
            
            for rule in nacl_info['inbound_rules']:
                if rule['rule_number'] < 32767:
                    action_class = rule['action']
                    port_info = rule.get('port_range', 'All')
                    explanation = self._generate_rule_explanation(rule, 'inbound')
                    
                    # Check if this rule has security risk
                    risk = self._analyze_security_risk(rule, 'inbound')
                    risk_class = f"security-risk {risk['level']}" if risk['level'] != 'none' else ''
                    
                    html += f"""
                        <div class="acl-rule {action_class} {risk_class}" title="{explanation}">
                            #{rule['rule_number']}: {rule['action'].upper()} {rule['protocol']} from {rule['cidr']} port {port_info}
                            <div class="acl-rule-explanation">
                                {explanation}
                            </div>
                        </div>
"""
            
            html += """
                        <div style="font-weight: 600; margin-top: 10px; margin-bottom: 5px;">Outbound Rules:</div>
"""
            
            for rule in nacl_info['outbound_rules']:
                if rule['rule_number'] < 32767:
                    action_class = rule['action']
                    port_info = rule.get('port_range', 'All')
                    explanation = self._generate_rule_explanation(rule, 'outbound')
                    
                    html += f"""
                        <div class="acl-rule {action_class}" title="{explanation}">
                            #{rule['rule_number']}: {rule['action'].upper()} {rule['protocol']} to {rule['cidr']} port {port_info}
                            <div class="acl-rule-explanation">
                                {explanation}
                            </div>
                        </div>
"""
            
            html += """
                    </div>
                </div>
"""
        
        html += "</div>"
        
        return html
    
    def _generate_route_table(self, rt: Dict, vpc: Dict) -> str:
        """Generate route table section"""
        rt_name = rt.get('name', 'N/A')
        rt_id = rt['route_table_id']
        is_main = rt['is_main']
        associated_subnets = rt.get('associated_subnets', [])
        
        html = f"""
        <div class="route-table">
            <h4>{rt_name} {'(Main)' if is_main else ''}</h4>
            <div class="code">{rt_id}</div>
            <div><strong>Associated Subnets:</strong> {len(associated_subnets)}</div>
"""
        
        if associated_subnets:
            html += "<ul>"
            for subnet_id in associated_subnets:
                subnet_name = 'N/A'
                for subnet in vpc.get('subnets', []):
                    if subnet['subnet_id'] == subnet_id:
                        subnet_name = subnet.get('name', 'N/A')
                        break
                html += f"<li>{subnet_name} ({subnet_id})</li>"
            html += "</ul>"
        
        html += "<div style='margin-top: 15px;'><strong>Routes:</strong></div>"
        
        for route in rt.get('routes', []):
            target_type = route['target_type']
            destination = route['destination']
            target = route['target']
            
            html += f"""
            <div class="route-entry {target_type}">
                <strong>{destination}</strong> → {target} ({target_type})
            </div>
"""
        
        html += "</div>"
        
        return html
    
    def _generate_connectivity_section(self) -> str:
        """Generate connectivity section"""
        html = "<h2>🔗 Network Connectivity</h2>"
        
        connectivity = self.data.get('connectivity', {})
        
        # VPC Peering
        peering = connectivity.get('vpc_peering', [])
        if peering:
            html += "<h3>VPC Peering Connections</h3><table>"
            html += "<tr><th>Peering ID</th><th>Name</th><th>Requester</th><th>Accepter</th><th>Status</th></tr>"
            
            for peer in peering:
                status_class = 'active' if peer['status'] == 'active' else 'inactive'
                html += f"""
                <tr>
                    <td class="code">{peer['peering_id']}</td>
                    <td>{peer.get('name', 'N/A')}</td>
                    <td>{peer['requester']['vpc_id']}<br>({peer['requester']['cidr']})</td>
                    <td>{peer['accepter']['vpc_id']}<br>({peer['accepter']['cidr']})</td>
                    <td><span class="badge {status_class}">{peer['status']}</span></td>
                </tr>
"""
            html += "</table>"
        
        # VPN Connections
        vpn_connections = connectivity.get('vpn_connections', [])
        if vpn_connections:
            html += "<h3>VPN Connections</h3><table>"
            html += "<tr><th>VPN ID</th><th>Name</th><th>State</th><th>Type</th><th>Customer Gateway IP</th></tr>"
            
            for vpn in vpn_connections:
                state_class = 'active' if vpn['state'] == 'available' else 'inactive'
                html += f"""
                <tr>
                    <td class="code">{vpn['vpn_id']}</td>
                    <td>{vpn.get('name', 'N/A')}</td>
                    <td><span class="badge {state_class}">{vpn['state']}</span></td>
                    <td>{vpn['type']}</td>
                    <td>{vpn.get('customer_gateway_ip', 'N/A')}</td>
                </tr>
"""
            html += "</table>"
        
        # Transit Gateways
        tgws = connectivity.get('transit_gateways', [])
        if tgws:
            html += "<h3>Transit Gateways</h3>"
            
            for tgw in tgws:
                html += f"""
                <div class="route-table">
                    <h4>{tgw.get('name', 'N/A')}</h4>
                    <div class="code">{tgw['tgw_id']}</div>
                    <div><strong>State:</strong> <span class="badge {tgw['state']}">{tgw['state']}</span></div>
                    <div><strong>Attachments:</strong> {len(tgw.get('attachments', []))}</div>
"""
                
                if tgw.get('attachments'):
                    html += "<table style='margin-top: 15px;'>"
                    html += "<tr><th>Resource Type</th><th>Resource ID</th><th>State</th></tr>"
                    
                    for att in tgw['attachments']:
                        html += f"""
                        <tr>
                            <td>{att['resource_type']}</td>
                            <td class="code">{att['resource_id']}</td>
                            <td><span class="badge {att['state']}">{att['state']}</span></td>
                        </tr>
"""
                    html += "</table>"
                
                html += "</div>"
        
        # VPC Endpoints
        endpoints = connectivity.get('vpc_endpoints', [])
        if endpoints:
            html += "<h3>VPC Endpoints</h3><table>"
            html += "<tr><th>Endpoint ID</th><th>Service</th><th>VPC</th><th>Type</th><th>State</th></tr>"
            
            for ep in endpoints:
                html += f"""
                <tr>
                    <td class="code">{ep['endpoint_id']}</td>
                    <td>{ep['service_name']}</td>
                    <td class="code">{ep['vpc_id']}</td>
                    <td>{ep['endpoint_type']}</td>
                    <td><span class="badge {ep['state']}">{ep['state']}</span></td>
                </tr>
"""
            html += "</table>"
        
        return html


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Enhanced AWS Network Visualization with Flow Diagrams'
    )
    parser.add_argument(
        'discovery_file',
        help='Path to JSON file from network discovery tool'
    )
    
    args = parser.parse_args()
    
    try:
        visualizer = EnhancedNetworkVisualizer(args.discovery_file)
        
        print("\n" + "="*80)
        print("Creating Enhanced Network Documentation")
        print("="*80 + "\n")
        
        visualizer.create_html_report()
        
        print(f"\n✅ Report saved in: {visualizer.output_dir}/")
        print("\n" + "="*80)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
