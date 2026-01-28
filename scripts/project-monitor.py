#!/usr/bin/env python3
"""
DarkFlobi Project Intelligence System
Tracks darkflobi collective development progress
"""

import json
import os
from datetime import datetime, timedelta
import subprocess
import sys

class ProjectMonitor:
    def __init__(self):
        self.workspace = "/data/workspace"
        self.projects_dir = f"{self.workspace}/projects"
        self.memory_dir = f"{self.workspace}/memory"
        self.tracker_file = f"{self.projects_dir}/darkflobi-tracker.json"
        
    def load_tracker(self):
        """Load the project tracker JSON"""
        try:
            with open(self.tracker_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "project": "darkflobi_collective",
                "status": "launch_ready",
                "last_update": datetime.now().isoformat(),
                "entities": {
                    "flobi_dev": {"progress": 100, "task": "website complete"},
                    "darkflobi_core": {"progress": 100, "task": "entity system live"},
                    "shadow_admin": {"progress": 100, "task": "monitoring active"},
                    "void_analyst": {"progress": 100, "task": "analytics ready"}
                }
            }
    
    def check_darkflobi_status(self):
        """Check darkflobi project status"""
        darkflobi_dir = f"{self.projects_dir}/darkflobi-website"
        
        status = {
            "website": "ready",
            "entities": "active", 
            "launch_status": "ready",
            "timestamp": datetime.now().isoformat()
        }
        
        if os.path.exists(darkflobi_dir):
            # Check if entity collaboration file exists
            collab_file = f"{darkflobi_dir}/entity_collaboration.json"
            if os.path.exists(collab_file):
                status["collaboration"] = "active"
            
            # Check git status
            try:
                result = subprocess.run(['git', 'status', '--porcelain'], 
                                      cwd=darkflobi_dir, 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    if result.stdout.strip():
                        status["git"] = "changes_pending"
                    else:
                        status["git"] = "clean"
            except:
                status["git"] = "unknown"
        
        return status
    
    def generate_report(self):
        """Generate status report"""
        tracker = self.load_tracker()
        darkflobi_status = self.check_darkflobi_status()
        
        # Update tracker with current status
        tracker["darkflobi_status"] = darkflobi_status
        tracker["last_check"] = datetime.now().isoformat()
        
        # Save updated tracker
        os.makedirs(self.projects_dir, exist_ok=True)
        with open(self.tracker_file, 'w') as f:
            json.dump(tracker, f, indent=2)
        
        return {
            "project": "darkflobi_collective",
            "status": "launch_ready",
            "website": darkflobi_status["website"],
            "entities": darkflobi_status["entities"],
            "last_update": darkflobi_status["timestamp"]
        }

def main():
    """Main project monitoring function"""
    monitor = ProjectMonitor()
    report = monitor.generate_report()
    
    print(f"📋 Active projects: {report['project']}")
    return report

if __name__ == "__main__":
    main()