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
        
        # Summary Section
        summary = self.data.get('summary', {})
        html_content += f"""
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
        
        # Network Flow Diagram
        html += self._generate_flow_diagram(vpc)
        
        # Group subnets by type
        public_subnets = [s for s in vpc.get('subnets', []) if s.get('subnet_type') == 'Public']
        private_subnets = [s for s in vpc.get('subnets', []) if s.get('subnet_type') == 'Private']
        
        # Find NACL associations for each subnet
        nacl_map = self._build_nacl_map(vpc)
        
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
    
    def _generate_subnet_card(self, subnet: Dict, nacl_map: Dict, subnet_type: str) -> str:
        """Generate individual subnet card with ACL info"""
        subnet_id = subnet['subnet_id']
        subnet_name = subnet.get('name', 'N/A')
        
        html = f"""
            <div class="subnet-card {subnet_type}">
                <h4>{subnet_name}</h4>
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
                    html += f"""
                        <div class="acl-rule {action_class}">
                            #{rule['rule_number']}: {rule['action'].upper()} {rule['protocol']} from {rule['cidr']} port {port_info}
                        </div>
"""
            
            html += """
                        <div style="font-weight: 600; margin-top: 10px; margin-bottom: 5px;">Outbound Rules:</div>
"""
            
            for rule in nacl_info['outbound_rules']:
                if rule['rule_number'] < 32767:
                    action_class = rule['action']
                    port_info = rule.get('port_range', 'All')
                    html += f"""
                        <div class="acl-rule {action_class}">
                            #{rule['rule_number']}: {rule['action'].upper()} {rule['protocol']} to {rule['cidr']} port {port_info}
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
