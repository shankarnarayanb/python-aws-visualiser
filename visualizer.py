#!/usr/bin/env python3
"""
Improved AWS Network Visualization Tool

This version creates cleaner, more readable diagrams with better layout and formatting.
Uses HTML reports and simplified diagrams to avoid overlapping text.

Usage:
    python improved_visualizer.py network_discovery.json
    python improved_visualizer.py network_discovery.json --format html

Requirements:
    pip install jinja2
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class ImprovedNetworkVisualizer:
    """Create clean, readable network documentation"""
    
    def __init__(self, discovery_file: str):
        """
        Initialize visualizer with discovery data
        
        Args:
            discovery_file: Path to JSON file from network discovery
        """
        self.discovery_file = discovery_file
        self.data = self._load_data()
        self.output_dir = "network_reports"
        
        # Create output directory
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
        """Create comprehensive HTML report with all network information"""
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
            max-width: 1400px;
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
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
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
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
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
        
        .badge.inactive {{
            background: #ffebee;
            color: #c62828;
        }}
        
        .badge.available {{
            background: #e0f2f1;
            color: #00695c;
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
        
        .subnet-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .subnet-card {{
            border: 1px solid #ddd;
            border-radius: 6px;
            padding: 15px;
            background: white;
        }}
        
        .subnet-card.public {{
            border-left: 4px solid #2193b0;
        }}
        
        .subnet-card.private {{
            border-left: 4px solid #764ba2;
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
        
        .route-entry.vpn {{
            border-left: 3px solid #f46b45;
        }}
        
        .route-entry.local {{
            border-left: 3px solid #999;
        }}
        
        .nacl-rules {{
            margin: 15px 0;
        }}
        
        .rule {{
            padding: 10px;
            margin: 8px 0;
            background: #f8f9fa;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }}
        
        .rule.allow {{
            border-left: 4px solid #2e7d32;
        }}
        
        .rule.deny {{
            border-left: 4px solid #c62828;
        }}
        
        .crowdstrike-highlight {{
            background: #fff3cd;
            border: 2px solid #ffc107;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }}
        
        .info-box {{
            background: #e3f2fd;
            border-left: 4px solid #1976d2;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        .warning-box {{
            background: #fff3e0;
            border-left: 4px solid #f57c00;
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
        
        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
            }}
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
        
        <table>
            <tr>
                <th>Component</th>
                <th>Count</th>
            </tr>
            <tr>
                <td>Internet Gateways</td>
                <td>{summary.get('internet_gateways', 0)}</td>
            </tr>
            <tr>
                <td>VPN Connections</td>
                <td>{summary.get('vpn_connections', 0)}</td>
            </tr>
            <tr>
                <td>VPC Peering Connections</td>
                <td>{summary.get('vpc_peering_connections', 0)}</td>
            </tr>
            <tr>
                <td>Transit Gateways</td>
                <td>{summary.get('transit_gateways', 0)}</td>
            </tr>
            <tr>
                <td>VPC Endpoints</td>
                <td>{summary.get('vpc_endpoints', 0)}</td>
            </tr>
        </table>
"""
        
        # VPC Details
        for vpc in self.data.get('vpcs', []):
            html_content += self._generate_vpc_section(vpc)
        
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
    
    def _generate_vpc_section(self, vpc: Dict) -> str:
        """Generate HTML section for a VPC"""
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
        
        # Internet Gateway
        if vpc.get('internet_gateway'):
            igw = vpc['internet_gateway']
            html += f"""
            <div class="info-box">
                <strong>🌐 Internet Gateway:</strong> {igw['igw_id']} 
                <span class="badge active">{igw['state']}</span>
            </div>
"""
        
        # VPN Gateway
        if vpc.get('vpn_gateway'):
            vgw = vpc['vpn_gateway']
            html += f"""
            <div class="info-box">
                <strong>🔒 VPN Gateway:</strong> {vgw['vgw_id']} 
                <span class="badge {vgw['state']}">{vgw['state']}</span>
            </div>
"""
        
        # NAT Gateways
        if vpc.get('nat_gateways'):
            html += f"""
            <div class="info-box">
                <strong>🔄 NAT Gateways:</strong> {len(vpc['nat_gateways'])}
                <ul>
"""
            for nat in vpc['nat_gateways']:
                html += f"<li>{nat['nat_gateway_id']} in {nat.get('subnet_id', 'N/A')} - {nat['state']}</li>"
            html += "</ul></div>"
        
        # Subnets
        html += "<h3>📍 Subnets</h3><div class='subnet-grid'>"
        
        for subnet in vpc.get('subnets', []):
            subnet_type = subnet.get('subnet_type', 'Unknown')
            class_name = subnet_type.lower()
            
            html += f"""
            <div class="subnet-card {class_name}">
                <h4>{subnet.get('name', 'N/A')}</h4>
                <div><span class="badge {class_name}">{subnet_type}</span></div>
                <div class="code" style="margin: 10px 0;">{subnet['subnet_id']}</div>
                <div><strong>CIDR:</strong> {subnet['cidr_block']}</div>
                <div><strong>AZ:</strong> {subnet['availability_zone']}</div>
                <div><strong>Available IPs:</strong> {subnet['available_ip_count']}</div>
            </div>
"""
        
        html += "</div>"
        
        # Route Tables
        html += "<h3>🗺️ Route Tables</h3>"
        
        for rt in vpc.get('route_tables', []):
            rt_name = rt.get('name', 'N/A')
            rt_id = rt['route_table_id']
            is_main = rt['is_main']
            associated_subnets = rt.get('associated_subnets', [])
            
            html += f"""
            <div class="route-table">
                <h4>{rt_name} {'(Main)' if is_main else ''}</h4>
                <div class="code">{rt_id}</div>
                <div><strong>Associated Subnets:</strong> {len(associated_subnets)}</div>
"""
            
            if associated_subnets:
                html += "<ul>"
                for subnet_id in associated_subnets:
                    # Find subnet name
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
        
        # Network ACLs
        html += "<h3>🛡️ Network ACLs</h3>"
        
        for nacl in vpc.get('nacls', []):
            nacl_name = nacl.get('name', 'N/A')
            nacl_id = nacl['nacl_id']
            is_default = nacl['is_default']
            associated_subnets = nacl.get('associated_subnets', [])
            
            html += f"""
            <div class="route-table">
                <h4>{nacl_name} {'(Default)' if is_default else ''}</h4>
                <div class="code">{nacl_id}</div>
                <div><strong>Associated Subnets:</strong> {len(associated_subnets)}</div>
"""
            
            # Check for potential CrowdStrike IPs
            crowdstrike_found = False
            for rule in nacl.get('inbound_rules', []) + nacl.get('outbound_rules', []):
                cidr = rule.get('cidr', '')
                # Common CrowdStrike IP ranges (52.x.x.x, 34.x.x.x, etc.)
                if cidr and (cidr.startswith('52.') or cidr.startswith('34.') or 
                           cidr.startswith('35.') or cidr.startswith('54.')):
                    crowdstrike_found = True
                    break
            
            if crowdstrike_found:
                html += """
                <div class="crowdstrike-highlight">
                    ⚠️ <strong>Potential CrowdStrike Rules Detected</strong>
                </div>
"""
            
            # Inbound Rules
            html += "<div class='nacl-rules'><strong>Inbound Rules:</strong>"
            for rule in nacl.get('inbound_rules', [])[:10]:  # Show first 10
                if rule['rule_number'] < 32767:  # Skip default deny
                    action_class = rule['action']
                    html += f"""
                    <div class="rule {action_class}">
                        #{rule['rule_number']}: <strong>{rule['action'].upper()}</strong> 
                        {rule['protocol']} from {rule['cidr']} 
                        port {rule.get('port_range', 'All')}
                    </div>
"""
            html += "</div>"
            
            # Outbound Rules
            html += "<div class='nacl-rules'><strong>Outbound Rules:</strong>"
            for rule in nacl.get('outbound_rules', [])[:10]:  # Show first 10
                if rule['rule_number'] < 32767:  # Skip default deny
                    action_class = rule['action']
                    html += f"""
                    <div class="rule {action_class}">
                        #{rule['rule_number']}: <strong>{rule['action'].upper()}</strong> 
                        {rule['protocol']} to {rule['cidr']} 
                        port {rule.get('port_range', 'All')}
                    </div>
"""
            html += "</div></div>"
        
        html += "</div>"  # Close vpc-section
        
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
    
    def create_text_report(self):
        """Create clean text-based report"""
        region = self.data.get('region', 'unknown')
        filename = f"{self.output_dir}/network_report_{region}.txt"
        
        with open(filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write(f"AWS NETWORK INFRASTRUCTURE REPORT - {region.upper()}\n")
            f.write("="*80 + "\n\n")
            
            # Summary
            summary = self.data.get('summary', {})
            f.write("SUMMARY\n")
            f.write("-"*80 + "\n")
            f.write(f"Total VPCs:               {summary.get('total_vpcs', 0)}\n")
            f.write(f"Total Subnets:            {summary.get('total_subnets', 0)}\n")
            f.write(f"  - Public:               {summary.get('public_subnets', 0)}\n")
            f.write(f"  - Private:              {summary.get('private_subnets', 0)}\n")
            f.write(f"Internet Gateways:        {summary.get('internet_gateways', 0)}\n")
            f.write(f"NAT Gateways:             {summary.get('nat_gateways', 0)}\n")
            f.write(f"VPN Connections:          {summary.get('vpn_connections', 0)}\n")
            f.write(f"VPC Peering:              {summary.get('vpc_peering_connections', 0)}\n")
            f.write(f"Transit Gateways:         {summary.get('transit_gateways', 0)}\n")
            f.write(f"VPC Endpoints:            {summary.get('vpc_endpoints', 0)}\n")
            f.write("\n")
            
            # VPC Details
            for vpc in self.data.get('vpcs', []):
                self._write_vpc_text(f, vpc)
            
            # Connectivity
            self._write_connectivity_text(f)
        
        print(f"✅ Text report created: {filename}")
        return filename
    
    def _write_vpc_text(self, f, vpc: Dict):
        """Write VPC details to text file"""
        f.write("="*80 + "\n")
        f.write(f"VPC: {vpc.get('name', 'N/A')}\n")
        f.write("="*80 + "\n")
        f.write(f"VPC ID:        {vpc['vpc_id']}\n")
        f.write(f"CIDR Block:    {vpc['cidr_block']}\n")
        f.write(f"Default VPC:   {'Yes' if vpc.get('is_default') else 'No'}\n")
        
        if vpc.get('internet_gateway'):
            igw = vpc['internet_gateway']
            f.write(f"Internet GW:   {igw['igw_id']} ({igw['state']})\n")
        
        if vpc.get('vpn_gateway'):
            vgw = vpc['vpn_gateway']
            f.write(f"VPN Gateway:   {vgw['vgw_id']} ({vgw['state']})\n")
        
        if vpc.get('nat_gateways'):
            f.write(f"NAT Gateways:  {len(vpc['nat_gateways'])}\n")
        
        f.write("\n")
        
        # Subnets
        f.write("SUBNETS\n")
        f.write("-"*80 + "\n")
        for subnet in vpc.get('subnets', []):
            f.write(f"  {subnet.get('name', 'N/A'):30} [{subnet['subnet_type']:7}]\n")
            f.write(f"    ID:               {subnet['subnet_id']}\n")
            f.write(f"    CIDR:             {subnet['cidr_block']}\n")
            f.write(f"    Availability Zone: {subnet['availability_zone']}\n")
            f.write(f"    Available IPs:    {subnet['available_ip_count']}\n")
            f.write("\n")
        
        # Route Tables (abbreviated)
        f.write("ROUTE TABLES\n")
        f.write("-"*80 + "\n")
        for rt in vpc.get('route_tables', []):
            f.write(f"  {rt.get('name', 'N/A'):30} {'[MAIN]' if rt['is_main'] else ''}\n")
            f.write(f"    ID: {rt['route_table_id']}\n")
            f.write(f"    Associated Subnets: {len(rt.get('associated_subnets', []))}\n")
            f.write("    Key Routes:\n")
            for route in rt.get('routes', []):
                if route['target_type'] != 'local':
                    f.write(f"      {route['destination']:20} -> {route['target']:25} ({route['target_type']})\n")
            f.write("\n")
        
        # Network ACLs (with CrowdStrike detection)
        f.write("NETWORK ACLs\n")
        f.write("-"*80 + "\n")
        for nacl in vpc.get('nacls', []):
            f.write(f"  {nacl.get('name', 'N/A'):30} {'[DEFAULT]' if nacl['is_default'] else ''}\n")
            f.write(f"    ID: {nacl['nacl_id']}\n")
            f.write(f"    Associated Subnets: {len(nacl.get('associated_subnets', []))}\n")
            
            # Check for CrowdStrike IPs
            crowdstrike_rules = []
            for rule in nacl.get('inbound_rules', []) + nacl.get('outbound_rules', []):
                cidr = rule.get('cidr', '')
                if cidr and (cidr.startswith('52.') or cidr.startswith('34.') or 
                           cidr.startswith('35.') or cidr.startswith('54.')):
                    crowdstrike_rules.append(rule)
            
            if crowdstrike_rules:
                f.write("    *** POTENTIAL CROWDSTRIKE RULES DETECTED ***\n")
            
            f.write("    Inbound Rules (first 5):\n")
            for rule in nacl.get('inbound_rules', [])[:5]:
                if rule['rule_number'] < 32767:
                    f.write(f"      #{rule['rule_number']:5} {rule['action']:6} {rule['protocol']:8} "
                           f"from {rule['cidr']:20} port {rule.get('port_range', 'All')}\n")
            
            f.write("    Outbound Rules (first 5):\n")
            for rule in nacl.get('outbound_rules', [])[:5]:
                if rule['rule_number'] < 32767:
                    f.write(f"      #{rule['rule_number']:5} {rule['action']:6} {rule['protocol']:8} "
                           f"to {rule['cidr']:20} port {rule.get('port_range', 'All')}\n")
            f.write("\n")
        
        f.write("\n")
    
    def _write_connectivity_text(self, f):
        """Write connectivity details to text file"""
        f.write("="*80 + "\n")
        f.write("NETWORK CONNECTIVITY\n")
        f.write("="*80 + "\n\n")
        
        connectivity = self.data.get('connectivity', {})
        
        # VPC Peering
        peering = connectivity.get('vpc_peering', [])
        if peering:
            f.write("VPC PEERING CONNECTIONS\n")
            f.write("-"*80 + "\n")
            for peer in peering:
                f.write(f"  {peer.get('name', 'N/A')}\n")
                f.write(f"    Peering ID:  {peer['peering_id']}\n")
                f.write(f"    Status:      {peer['status']}\n")
                f.write(f"    Requester:   {peer['requester']['vpc_id']} ({peer['requester']['cidr']})\n")
                f.write(f"    Accepter:    {peer['accepter']['vpc_id']} ({peer['accepter']['cidr']})\n")
                f.write("\n")
        
        # VPN Connections
        vpn_connections = connectivity.get('vpn_connections', [])
        if vpn_connections:
            f.write("VPN CONNECTIONS\n")
            f.write("-"*80 + "\n")
            for vpn in vpn_connections:
                f.write(f"  {vpn.get('name', 'N/A')}\n")
                f.write(f"    VPN ID:      {vpn['vpn_id']}\n")
                f.write(f"    State:       {vpn['state']}\n")
                f.write(f"    Type:        {vpn['type']}\n")
                f.write(f"    Customer GW: {vpn.get('customer_gateway_ip', 'N/A')}\n")
                f.write("\n")
        
        # Transit Gateways
        tgws = connectivity.get('transit_gateways', [])
        if tgws:
            f.write("TRANSIT GATEWAYS\n")
            f.write("-"*80 + "\n")
            for tgw in tgws:
                f.write(f"  {tgw.get('name', 'N/A')}\n")
                f.write(f"    TGW ID:      {tgw['tgw_id']}\n")
                f.write(f"    State:       {tgw['state']}\n")
                f.write(f"    Attachments: {len(tgw.get('attachments', []))}\n")
                for att in tgw.get('attachments', []):
                    f.write(f"      - {att['resource_type']:10} {att['resource_id']:30} ({att['state']})\n")
                f.write("\n")
        
        # VPC Endpoints
        endpoints = connectivity.get('vpc_endpoints', [])
        if endpoints:
            f.write("VPC ENDPOINTS\n")
            f.write("-"*80 + "\n")
            for ep in endpoints:
                f.write(f"    {ep['endpoint_id']:30} {ep['service_name']:50} ({ep['state']})\n")
            f.write("\n")
    
    def create_markdown_report(self):
        """Create Markdown report for documentation"""
        region = self.data.get('region', 'unknown')
        timestamp = self.data.get('timestamp', '')
        filename = f"{self.output_dir}/network_report_{region}.md"
        
        with open(filename, 'w') as f:
            f.write(f"# AWS Network Infrastructure Report - {region}\n\n")
            f.write(f"**Generated:** {timestamp}\n\n")
            f.write("---\n\n")
            
            # Summary
            summary = self.data.get('summary', {})
            f.write("## Summary\n\n")
            f.write("| Component | Count |\n")
            f.write("|-----------|-------|\n")
            f.write(f"| VPCs | {summary.get('total_vpcs', 0)} |\n")
            f.write(f"| Total Subnets | {summary.get('total_subnets', 0)} |\n")
            f.write(f"| - Public Subnets | {summary.get('public_subnets', 0)} |\n")
            f.write(f"| - Private Subnets | {summary.get('private_subnets', 0)} |\n")
            f.write(f"| Internet Gateways | {summary.get('internet_gateways', 0)} |\n")
            f.write(f"| NAT Gateways | {summary.get('nat_gateways', 0)} |\n")
            f.write(f"| VPN Connections | {summary.get('vpn_connections', 0)} |\n")
            f.write(f"| VPC Peering | {summary.get('vpc_peering_connections', 0)} |\n")
            f.write(f"| Transit Gateways | {summary.get('transit_gateways', 0)} |\n")
            f.write(f"| VPC Endpoints | {summary.get('vpc_endpoints', 0)} |\n")
            f.write("\n---\n\n")
            
            # VPC Details
            for vpc in self.data.get('vpcs', []):
                self._write_vpc_markdown(f, vpc)
            
            # Connectivity
            self._write_connectivity_markdown(f)
        
        print(f"✅ Markdown report created: {filename}")
        return filename
    
    def _write_vpc_markdown(self, f, vpc: Dict):
        """Write VPC details to markdown file"""
        vpc_name = vpc.get('name', 'N/A')
        vpc_id = vpc['vpc_id']
        vpc_cidr = vpc['cidr_block']
        
        f.write(f"## VPC: {vpc_name}\n\n")
        f.write(f"**VPC ID:** `{vpc_id}`  \n")
        f.write(f"**CIDR Block:** `{vpc_cidr}`  \n")
        f.write(f"**Default VPC:** {'Yes' if vpc.get('is_default') else 'No'}  \n")
        
        if vpc.get('internet_gateway'):
            igw = vpc['internet_gateway']
            f.write(f"**Internet Gateway:** `{igw['igw_id']}` ({igw['state']})  \n")
        
        if vpc.get('vpn_gateway'):
            vgw = vpc['vpn_gateway']
            f.write(f"**VPN Gateway:** `{vgw['vgw_id']}` ({vgw['state']})  \n")
        
        if vpc.get('nat_gateways'):
            f.write(f"**NAT Gateways:** {len(vpc['nat_gateways'])}  \n")
        
        f.write("\n")
        
        # Subnets
        f.write("### Subnets\n\n")
        f.write("| Name | ID | Type | CIDR | AZ | Available IPs |\n")
        f.write("|------|----|----- |------|----|--------------|\n")
        
        for subnet in vpc.get('subnets', []):
            f.write(f"| {subnet.get('name', 'N/A')} | `{subnet['subnet_id']}` | "
                   f"**{subnet['subnet_type']}** | `{subnet['cidr_block']}` | "
                   f"{subnet['availability_zone']} | {subnet['available_ip_count']} |\n")
        
        f.write("\n")
        
        # Route Tables
        f.write("### Route Tables\n\n")
        
        for rt in vpc.get('route_tables', []):
            rt_name = rt.get('name', 'N/A')
            rt_id = rt['route_table_id']
            is_main = rt['is_main']
            
            f.write(f"#### {rt_name} {'(Main)' if is_main else ''}\n\n")
            f.write(f"**Route Table ID:** `{rt_id}`  \n")
            f.write(f"**Associated Subnets:** {len(rt.get('associated_subnets', []))}  \n\n")
            
            f.write("**Routes:**\n\n")
            f.write("| Destination | Target | Type |\n")
            f.write("|-------------|--------|------|\n")
            
            for route in rt.get('routes', []):
                f.write(f"| `{route['destination']}` | `{route['target']}` | {route['target_type']} |\n")
            
            f.write("\n")
        
        # Network ACLs
        f.write("### Network ACLs\n\n")
        
        for nacl in vpc.get('nacls', []):
            nacl_name = nacl.get('name', 'N/A')
            nacl_id = nacl['nacl_id']
            is_default = nacl['is_default']
            
            f.write(f"#### {nacl_name} {'(Default)' if is_default else ''}\n\n")
            f.write(f"**NACL ID:** `{nacl_id}`  \n")
            f.write(f"**Associated Subnets:** {len(nacl.get('associated_subnets', []))}  \n\n")
            
            # Check for CrowdStrike
            crowdstrike_found = False
            for rule in nacl.get('inbound_rules', []) + nacl.get('outbound_rules', []):
                cidr = rule.get('cidr', '')
                if cidr and (cidr.startswith('52.') or cidr.startswith('34.') or 
                           cidr.startswith('35.') or cidr.startswith('54.')):
                    crowdstrike_found = True
                    break
            
            if crowdstrike_found:
                f.write("> ⚠️ **Potential CrowdStrike Rules Detected**\n\n")
            
            f.write("**Inbound Rules:**\n\n")
            f.write("| Rule # | Action | Protocol | CIDR | Port |\n")
            f.write("|--------|--------|----------|------|------|\n")
            
            for rule in nacl.get('inbound_rules', [])[:10]:
                if rule['rule_number'] < 32767:
                    f.write(f"| {rule['rule_number']} | {rule['action']} | {rule['protocol']} | "
                           f"`{rule['cidr']}` | {rule.get('port_range', 'All')} |\n")
            
            f.write("\n**Outbound Rules:**\n\n")
            f.write("| Rule # | Action | Protocol | CIDR | Port |\n")
            f.write("|--------|--------|----------|------|------|\n")
            
            for rule in nacl.get('outbound_rules', [])[:10]:
                if rule['rule_number'] < 32767:
                    f.write(f"| {rule['rule_number']} | {rule['action']} | {rule['protocol']} | "
                           f"`{rule['cidr']}` | {rule.get('port_range', 'All')} |\n")
            
            f.write("\n")
        
        f.write("---\n\n")
    
    def _write_connectivity_markdown(self, f):
        """Write connectivity details to markdown file"""
        f.write("## Network Connectivity\n\n")
        
        connectivity = self.data.get('connectivity', {})
        
        # VPC Peering
        peering = connectivity.get('vpc_peering', [])
        if peering:
            f.write("### VPC Peering Connections\n\n")
            f.write("| Name | Peering ID | Requester VPC | Accepter VPC | Status |\n")
            f.write("|------|------------|---------------|--------------|--------|\n")
            
            for peer in peering:
                f.write(f"| {peer.get('name', 'N/A')} | `{peer['peering_id']}` | "
                       f"`{peer['requester']['vpc_id']}` ({peer['requester']['cidr']}) | "
                       f"`{peer['accepter']['vpc_id']}` ({peer['accepter']['cidr']}) | "
                       f"{peer['status']} |\n")
            
            f.write("\n")
        
        # VPN Connections
        vpn_connections = connectivity.get('vpn_connections', [])
        if vpn_connections:
            f.write("### VPN Connections\n\n")
            f.write("| Name | VPN ID | State | Type | Customer Gateway IP |\n")
            f.write("|------|--------|-------|------|--------------------|\n")
            
            for vpn in vpn_connections:
                f.write(f"| {vpn.get('name', 'N/A')} | `{vpn['vpn_id']}` | "
                       f"{vpn['state']} | {vpn['type']} | "
                       f"{vpn.get('customer_gateway_ip', 'N/A')} |\n")
            
            f.write("\n")
        
        # Transit Gateways
        tgws = connectivity.get('transit_gateways', [])
        if tgws:
            f.write("### Transit Gateways\n\n")
            
            for tgw in tgws:
                f.write(f"#### {tgw.get('name', 'N/A')}\n\n")
                f.write(f"**TGW ID:** `{tgw['tgw_id']}`  \n")
                f.write(f"**State:** {tgw['state']}  \n")
                f.write(f"**Attachments:** {len(tgw.get('attachments', []))}  \n\n")
                
                if tgw.get('attachments'):
                    f.write("| Resource Type | Resource ID | State |\n")
                    f.write("|---------------|-------------|-------|\n")
                    
                    for att in tgw['attachments']:
                        f.write(f"| {att['resource_type']} | `{att['resource_id']}` | {att['state']} |\n")
                    
                    f.write("\n")
        
        # VPC Endpoints
        endpoints = connectivity.get('vpc_endpoints', [])
        if endpoints:
            f.write("### VPC Endpoints\n\n")
            f.write("| Endpoint ID | Service | VPC | Type | State |\n")
            f.write("|-------------|---------|-----|------|-------|\n")
            
            for ep in endpoints:
                f.write(f"| `{ep['endpoint_id']}` | {ep['service_name']} | "
                       f"`{ep['vpc_id']}` | {ep['endpoint_type']} | {ep['state']} |\n")
            
            f.write("\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Improved AWS Network Visualization - Clean, readable reports'
    )
    parser.add_argument(
        'discovery_file',
        help='Path to JSON file from network discovery tool'
    )
    parser.add_argument(
        '--format',
        choices=['html', 'text', 'markdown', 'all'],
        default='html',
        help='Output format (default: html)'
    )
    
    args = parser.parse_args()
    
    try:
        visualizer = ImprovedNetworkVisualizer(args.discovery_file)
        
        print("\n" + "="*80)
        print("Creating Network Documentation")
        print("="*80 + "\n")
        
        if args.format == 'html' or args.format == 'all':
            visualizer.create_html_report()
        
        if args.format == 'text' or args.format == 'all':
            visualizer.create_text_report()
        
        if args.format == 'markdown' or args.format == 'all':
            visualizer.create_markdown_report()
        
        print(f"\n✅ Reports saved in: {visualizer.output_dir}/")
        print("\n" + "="*80)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
