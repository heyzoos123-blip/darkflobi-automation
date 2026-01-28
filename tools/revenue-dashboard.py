#!/usr/bin/env python3
"""
Real-Time Revenue Dashboard - CEO darkflobi
Live MRR tracking, customer analytics, and business intelligence
"""

import json
import subprocess
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import webbrowser
import http.server
import socketserver
from threading import Thread

class RevenueDashboard:
    def __init__(self):
        self.data_file = '/data/workspace/operations/revenue_data.json'
        self.ensure_data_file()
        
    def ensure_data_file(self):
        """Initialize revenue tracking data"""
        try:
            with open(self.data_file, 'r') as f:
                json.load(f)
        except FileNotFoundError:
            initial_data = {
                'launch_date': None,
                'target_mrr': 4900,
                'current_mrr': 0,
                'customers': [],
                'daily_metrics': {},
                'conversion_rates': {
                    'visitor_to_trial': 0.15,
                    'trial_to_paid': 0.25,
                    'monthly_churn': 0.03
                },
                'traffic_sources': {},
                'api_costs': {
                    'monthly_target': 500,
                    'current_month': 0
                }
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def update_metrics(self, customers=0, mrr=0, trials=0, traffic_source='direct'):
        """Update business metrics"""
        with open(self.data_file, 'r') as f:
            data = json.load(f)
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        if today not in data['daily_metrics']:
            data['daily_metrics'][today] = {
                'new_customers': 0,
                'new_trials': 0,
                'mrr_added': 0,
                'visitors': 0
            }
        
        data['daily_metrics'][today]['new_customers'] += customers
        data['daily_metrics'][today]['new_trials'] += trials
        data['daily_metrics'][today]['mrr_added'] += mrr
        data['current_mrr'] += mrr
        
        if traffic_source not in data['traffic_sources']:
            data['traffic_sources'][traffic_source] = 0
        data['traffic_sources'][traffic_source] += 1
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def generate_dashboard_html(self):
        """Generate real-time dashboard HTML"""
        with open(self.data_file, 'r') as f:
            data = json.load(f)
        
        progress_percentage = (data['current_mrr'] / data['target_mrr']) * 100
        days_since_launch = 0
        
        if data['launch_date']:
            launch_date = datetime.fromisoformat(data['launch_date'])
            days_since_launch = (datetime.now() - launch_date).days
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>🚀 DuoTrader Revenue Dashboard - CEO darkflobi</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 20px; background: #0f0f23; color: #cccccc; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 40px; }}
        .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .metric-card {{ background: #1e1e3f; padding: 20px; border-radius: 10px; border: 1px solid #333; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #00ff88; }}
        .metric-label {{ font-size: 0.9em; color: #999; text-transform: uppercase; }}
        .progress-bar {{ background: #333; height: 20px; border-radius: 10px; overflow: hidden; margin: 10px 0; }}
        .progress-fill {{ background: linear-gradient(90deg, #00ff88, #00cc66); height: 100%; transition: width 0.3s; }}
        .status {{ text-align: center; padding: 20px; background: #1e3f1e; border-radius: 10px; margin: 20px 0; }}
        .emoji {{ font-size: 1.5em; }}
        .update-time {{ text-align: center; color: #666; font-size: 0.8em; }}
    </style>
    <meta http-equiv="refresh" content="30">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 CEO darkflobi's Revenue Command Center</h1>
            <p>DuoTrader AI Platform - Real-Time Business Intelligence</p>
        </div>
        
        <div class="status">
            <h2>🎯 Mission Progress: ${progress_percentage:.1f}% to Target</h2>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress_percentage}%"></div>
            </div>
            <p><strong>${data['current_mrr']} / $4,900 MRR</strong> | Days Since Launch: {days_since_launch}</p>
        </div>
        
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">💰 Monthly Recurring Revenue</div>
                <div class="metric-value">${data['current_mrr']}</div>
                <p>Target: $4,900/month</p>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">👥 Total Customers</div>
                <div class="metric-value">{len(data['customers'])}</div>
                <p>Revenue-generating accounts</p>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">📊 Revenue Runway</div>
                <div class="metric-value">{"∞" if data['current_mrr'] >= data['api_costs']['monthly_target'] else f"{data['api_costs']['monthly_target'] - data['current_mrr']}"}</div>
                <p>{"PROFITABLE! 🎉" if data['current_mrr'] >= data['api_costs']['monthly_target'] else "Deficit remaining"}</p>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">⚡ API Cost Coverage</div>
                <div class="metric-value">{(data['current_mrr'] / max(data['api_costs']['monthly_target'], 1) * 100):.0f}%</div>
                <p>Monthly costs covered by revenue</p>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">📈 Conversion Rates</div>
                <div class="metric-value">{data['conversion_rates']['visitor_to_trial']*100:.0f}%</div>
                <p>Visitor → Trial: {data['conversion_rates']['visitor_to_trial']*100:.0f}% | Trial → Paid: {data['conversion_rates']['trial_to_paid']*100:.0f}%</p>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">🎯 Days to Target</div>
                <div class="metric-value">{"ACHIEVED!" if data['current_mrr'] >= data['target_mrr'] else "TBD"}</div>
                <p>Based on current growth rate</p>
            </div>
        </div>
        
        <div class="update-time">
            <p>🤖 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Auto-refresh every 30s</p>
            <p><em>CEO darkflobi's Executive Dashboard - Powered by AI Business Intelligence</em></p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def start_dashboard_server(self, port=8080):
        """Start live dashboard server"""
        dashboard_html = self.generate_dashboard_html()
        
        with open('/data/workspace/operations/dashboard.html', 'w') as f:
            f.write(dashboard_html)
        
        print(f"🚀 Revenue Dashboard starting at http://localhost:{port}")
        print("📊 Real-time business metrics now available!")
        
        class DashboardHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/' or self.path == '/dashboard':
                    self.path = '/operations/dashboard.html'
                return super().do_GET()
        
        handler = DashboardHandler
        httpd = socketserver.TCPServer(("", port), handler)
        httpd.serve_forever()

def launch_dashboard():
    """Launch the revenue dashboard"""
    dashboard = RevenueDashboard()
    
    print("🤖 CEO darkflobi - Revenue Dashboard Initializing...")
    print("💰 Business Intelligence System Online")
    
    # Set launch date to tomorrow night
    with open(dashboard.data_file, 'r') as f:
        data = json.load(f)
    
    if not data['launch_date']:
        data['launch_date'] = (datetime.now() + timedelta(days=1)).replace(hour=19).isoformat()
        with open(dashboard.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    # Start dashboard server
    dashboard.start_dashboard_server()

if __name__ == "__main__":
    launch_dashboard()