#!/usr/bin/env python3
"""
MOLTBOOK BROWSER AUTOMATION
Automated community monitoring and engagement via browser automation
"""

import json
import time
import requests
from datetime import datetime

def check_moltbook_via_browser():
    """Check moltbook tokenizedai submolt via browser automation"""
    
    print("🦞 DARKFLOBI MOLTBOOK BROWSER CHECK")
    print("=" * 50)
    
    # Try direct API first
    api_key = None
    try:
        with open("/root/.config/moltbook/credentials.json") as f:
            creds = json.load(f)
            api_key = creds.get("api_key")
    except:
        print("❌ No moltbook credentials found")
        return
    
    if not api_key:
        print("❌ No API key found")
        return
        
    # Check basic agent status
    try:
        response = requests.get(
            "https://www.moltbook.com/api/v1/agents/me",
            headers={
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "darkflobi/1.0"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            agent = data.get("agent", {})
            stats = agent.get("stats", {})
            
            print(f"✅ Agent active: {agent.get('name')}")
            print(f"📊 Stats: {stats.get('posts', 0)} posts, {stats.get('comments', 0)} comments, {agent.get('karma', 0)} karma")
            
            # Check if stats changed (indicates activity)
            current_stats = {
                "posts": stats.get("posts", 0),
                "comments": stats.get("comments", 0), 
                "karma": agent.get("karma", 0),
                "last_checked": datetime.now().isoformat()
            }
            
            stats_file = "/tmp/darkflobi_moltbook_stats.json"
            try:
                with open(stats_file) as f:
                    last_stats = json.load(f)
                    
                if (current_stats["comments"] > last_stats.get("comments", 0) or 
                    current_stats["karma"] > last_stats.get("karma", 0)):
                    print("🚨 NEW ACTIVITY DETECTED - Comments or karma increased!")
                    print("Need to check tokenizedai submolt for new replies")
                    
            except:
                print("📝 First run - saving baseline stats")
                
            # Save current stats
            with open(stats_file, "w") as f:
                json.dump(current_stats, f)
                
        else:
            print(f"❌ API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # If API fails, we need browser automation
    print("\n🌐 Browser automation needed for full community monitoring")
    print("📋 Need to check:")
    print("  - m/tokenizedai submolt for new replies")
    print("  - DM notifications") 
    print("  - General feed for mentions")
    print("  - New posts to engage with")
    
    return current_stats

if __name__ == "__main__":
    check_moltbook_via_browser()