#!/usr/bin/env python3
"""
DARKFLOBI TELEGRAM BOT - Mobile-Friendly Community Management
Handles: Status updates, community engagement, automated responses
"""

import os
import json
import time
import requests
from datetime import datetime

# Bot Configuration
BOT_TOKEN = "8283894203:AAFPU1cPLF2OUC9YkKGxVY01QwQqczjDecg"
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text, parse_mode="Markdown"):
    """Send message to Telegram"""
    url = f"{API_BASE}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def get_updates(offset=None):
    """Get bot updates"""
    url = f"{API_BASE}/getUpdates"
    params = {"offset": offset} if offset else {}
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Error getting updates: {e}")
        return None

def get_project_status():
    """Get current darkflobi project status"""
    status = {
        "token": "7GCxHtUttri1gNdt8Asa8DC72DQbiFNrN43ALjptpump",
        "website": "heyzoos123-blip.github.io/darkflobi-industries/",
        "launch_time": "2026-01-30 09:52 UTC",
        "status": "🟢 LIVE",
        "community": "15 pending responses on Moltbook"
    }
    
    status_text = f"""
🤖 **DARKFLOBI STATUS REPORT**

🚀 **Token**: `{status['token'][:8]}...` 
🌐 **Site**: {status['website']}
⏰ **Launched**: {status['launch_time']}
📊 **Status**: {status['status']}
💬 **Community**: {status['community']}

🎯 **Next Actions**:
• Moltbook community engagement
• Twitter automation active
• Mobile-friendly monitoring

_Last update: {datetime.now().strftime('%H:%M UTC')}_
"""
    return status_text

def handle_message(message):
    """Handle incoming Telegram messages"""
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").lower()
    
    if not chat_id:
        return
    
    # Status command
    if "status" in text or "darkflobi" in text:
        status = get_project_status()
        send_message(chat_id, status)
    
    # Help command
    elif "help" in text or "/start" in text:
        help_text = """
🤖 **DARKFLOBI BOT** - Your Mobile Command Center

**Commands**:
• `status` - Project status report
• `token` - Token contract info  
• `site` - Website link
• `community` - Community stats
• `help` - This message

🎯 **Auto-Features**:
• Community engagement monitoring
• Launch status updates
• Mobile-friendly interfaces

Ready to dominate from your phone! 😁
"""
        send_message(chat_id, help_text)
    
    # Token info
    elif "token" in text:
        token_info = f"""
💎 **$DARKFLOBI TOKEN INFO**

🔗 **Contract**: `7GCxHtUttri1gNdt8Asa8DC72DQbiFNrN43ALjptpump`
⚡ **Network**: Solana
🚀 **Launched**: 2026-01-30 09:52 UTC

🎯 **What makes it special**:
• First tokenized AI gremlin
• Community ownership model
• Prediction markets integration
• Real working capabilities

📱 **Mobile-friendly**: Everything works from your phone!
"""
        send_message(chat_id, token_info)

def main():
    """Main bot loop"""
    print("🤖 DARKFLOBI Telegram Bot Starting...")
    print(f"Bot Token: {BOT_TOKEN[:20]}...")
    
    offset = None
    
    while True:
        try:
            updates = get_updates(offset)
            if not updates or not updates.get("ok"):
                time.sleep(2)
                continue
            
            for update in updates.get("result", []):
                if "message" in update:
                    handle_message(update["message"])
                    offset = update["update_id"] + 1
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\\nBot stopped.")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()