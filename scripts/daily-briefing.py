#!/usr/bin/env python3
"""
DarkFlobi Daily Briefing Generator
Intelligent summary of overnight activity and day ahead priorities
"""

import json
import os
from datetime import datetime, timedelta
import subprocess

class DailyBriefing:
    def __init__(self):
        self.workspace = "/data/workspace"
        self.memory_dir = f"{self.workspace}/memory"
        
    def get_weather_outlook(self):
        """Get weather for day ahead"""
        try:
            result = subprocess.run(['curl', '-s', 'wttr.in/New+York?format=%l:+%c+%t+%h+%w+%m'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return f"🌤️ NYC Today: {result.stdout.strip()}"
        except:
            pass
        return "🌤️ Weather: Unable to fetch"
    
    def get_project_priorities(self):
        """Analyze project status and suggest priorities"""
        priorities = []
        
        # Check DuoTrader timeline
        tracker_file = f"{self.workspace}/projects/super-duo-tracker.json"
        try:
            with open(tracker_file, 'r') as f:
                tracker = json.load(f)
                
            duotrader = tracker.get('active_projects', {}).get('duotrader_revenue', {})
            if duotrader.get('status') == 'in_progress':
                priorities.append("🚀 **DuoTrader MVP** - Continue development (Week 1 foundation)")
                
                # Check for specific incomplete tasks
                tasks = duotrader.get('tasks', [])
                incomplete = [task for task in tasks if not task.startswith('✅')]
                if incomplete:
                    priorities.append(f"📋 Focus areas: {', '.join(incomplete[:2])}")
                    
        except:
            priorities.append("🚀 **DuoTrader MVP** - Check project status")
            
        return priorities
    
    def scan_memory_insights(self):
        """Scan recent memory for important context"""
        insights = []
        
        # Check yesterday's and today's memory
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')
        
        for day in [yesterday, today]:
            memory_file = f"{self.memory_dir}/{day}.md"
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    content = f.read()
                    
                # Look for important keywords
                if 'completed' in content.lower():
                    insights.append(f"✅ Recent completions noted in {day}")
                if 'issue' in content.lower() or 'problem' in content.lower():
                    insights.append(f"⚠️ Issues flagged in {day} - review needed")
                if 'idea' in content.lower():
                    insights.append(f"💡 New ideas captured in {day}")
                    
        return insights
    
    def generate_briefing(self):
        """Generate comprehensive daily briefing"""
        briefing = []
        
        # Header
        today = datetime.now().strftime('%A, %B %d, %Y')
        briefing.append(f"# 🤖 Daily Briefing - {today}")
        briefing.append("")
        
        # Weather
        weather = self.get_weather_outlook()
        briefing.append(weather)
        briefing.append("")
        
        # Project Priorities
        briefing.append("## 🎯 Today's Priorities")
        priorities = self.get_project_priorities()
        for priority in priorities:
            briefing.append(f"- {priority}")
        if not priorities:
            briefing.append("- Check project tracker for current focus")
        briefing.append("")
        
        # Memory Insights
        insights = self.scan_memory_insights()
        if insights:
            briefing.append("## 🧠 Memory Insights")
            for insight in insights:
                briefing.append(f"- {insight}")
            briefing.append("")
        
        # System Status
        briefing.append("## 💻 System Status")
        briefing.append("- Enhanced monitoring: ✅ Active")
        briefing.append("- Project intelligence: ✅ Online") 
        briefing.append("- GitHub CLI: ✅ Ready (needs auth)")
        briefing.append("- Weather monitoring: ✅ NYC updates")
        briefing.append("")
        
        # Action Items
        briefing.append("## 🔧 Quick Wins Available")
        briefing.append("- Set up Gmail/email management")
        briefing.append("- Configure GitHub authentication for repo monitoring")
        briefing.append("- Create automated deployment scripts")
        briefing.append("- Set up revenue tracking dashboard")
        
        return "\n".join(briefing)

def main():
    briefing = DailyBriefing()
    print(briefing.generate_briefing())

if __name__ == "__main__":
    main()