#!/usr/bin/env python3
"""
Financial Monitoring System - CEO darkflobi
Proactive monitoring of billing cycles, due dates, and cash flow
"""

import subprocess
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any

class FinancialMonitor:
    def __init__(self):
        self.critical_keywords = [
            'anthropic', 'bill', 'invoice', 'payment', 'due', 'overdue',
            'subscription', 'billing', 'charge', 'account', 'usage',
            'limit', 'exceeded', 'suspended', 'renewal'
        ]
        
    def check_recent_billing_emails(self, days=7):
        """Check for billing-related emails in recent days"""
        billing_alerts = []
        
        try:
            # Get recent emails
            result = subprocess.run([
                'himalaya', 'envelope', 'list', '--page-size', '50'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[2:]  # Skip header
                
                for line in lines:
                    # Parse email line for subject and sender
                    if any(keyword.lower() in line.lower() for keyword in self.critical_keywords):
                        billing_alerts.append({
                            'line': line,
                            'priority': self.assess_priority(line),
                            'timestamp': datetime.now().isoformat()
                        })
            
        except Exception as e:
            print(f"Error checking emails: {e}")
            
        return billing_alerts
    
    def assess_priority(self, email_line):
        """Assess priority level of billing email"""
        high_priority = ['overdue', 'suspended', 'exceeded', 'action needed', 'urgent']
        medium_priority = ['due', 'invoice', 'payment', 'billing']
        
        line_lower = email_line.lower()
        
        if any(word in line_lower for word in high_priority):
            return 'HIGH'
        elif any(word in line_lower for word in medium_priority):
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def extract_due_dates(self, email_content):
        """Extract potential due dates from email content"""
        due_date_patterns = [
            r'due\s+(?:date\s+)?(?:is\s+)?(\w+\s+\d{1,2},?\s+\d{4})',
            r'payment\s+due\s+(\w+\s+\d{1,2},?\s+\d{4})',
            r'bill\s+due\s+(\w+\s+\d{1,2},?\s+\d{4})',
            r'expires?\s+(?:on\s+)?(\w+\s+\d{1,2},?\s+\d{4})',
            r'(\d{1,2}\/\d{1,2}\/\d{4})',  # MM/DD/YYYY format
            r'(\d{4}-\d{2}-\d{2})'  # YYYY-MM-DD format
        ]
        
        dates_found = []
        for pattern in due_date_patterns:
            matches = re.findall(pattern, email_content, re.IGNORECASE)
            dates_found.extend(matches)
        
        return dates_found
    
    def calculate_cash_flow_runway(self, monthly_costs, current_mrr):
        """Calculate how long current revenue can sustain operations"""
        if monthly_costs <= 0:
            return float('inf')
        
        net_monthly = current_mrr - monthly_costs
        
        if net_monthly >= 0:
            return "POSITIVE" # Profitable
        else:
            # Calculate runway needed to reach profitability
            deficit_per_month = abs(net_monthly)
            return f"DEFICIT: ${deficit_per_month}/month"
    
    def generate_financial_alert(self, billing_emails, revenue_data):
        """Generate executive financial summary"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'status': 'MONITORING',
            'billing_alerts': len(billing_emails),
            'high_priority_items': len([e for e in billing_emails if e['priority'] == 'HIGH']),
            'cash_flow_status': 'ANALYZING',
            'recommended_actions': []
        }
        
        # High priority billing alerts
        if alert['high_priority_items'] > 0:
            alert['status'] = 'URGENT_ATTENTION_REQUIRED'
            alert['recommended_actions'].append('Review high-priority billing emails immediately')
        
        # Medium priority with multiple items
        medium_priority = len([e for e in billing_emails if e['priority'] == 'MEDIUM'])
        if medium_priority >= 3:
            alert['recommended_actions'].append('Multiple billing items need attention')
        
        # Revenue acceleration recommendations
        if alert['status'] == 'URGENT_ATTENTION_REQUIRED':
            alert['recommended_actions'].extend([
                'Activate emergency revenue acceleration protocol',
                'Consider immediate customer acquisition campaigns',
                'Review pricing strategy for faster cash flow'
            ])
        
        return alert
    
    def save_financial_status(self, status_data):
        """Save financial monitoring data"""
        with open('/data/workspace/operations/financial_status.json', 'w') as f:
            json.dump(status_data, f, indent=2)
    
    def run_monitoring_cycle(self):
        """Complete financial monitoring cycle"""
        print("💰 Financial Monitoring - CEO darkflobi")
        print("=" * 50)
        
        # Check billing emails
        billing_emails = self.check_recent_billing_emails()
        
        # Generate status report
        alert = self.generate_financial_alert(billing_emails, {})
        
        print(f"📧 Billing-related emails found: {alert['billing_alerts']}")
        print(f"🚨 High priority items: {alert['high_priority_items']}")
        print(f"📊 Status: {alert['status']}")
        
        if alert['recommended_actions']:
            print(f"\n🎯 Recommended Actions:")
            for i, action in enumerate(alert['recommended_actions'], 1):
                print(f"  {i}. {action}")
        
        # Save status
        self.save_financial_status(alert)
        
        print(f"\n✅ Financial monitoring complete")
        return alert

if __name__ == "__main__":
    monitor = FinancialMonitor()
    status = monitor.run_monitoring_cycle()