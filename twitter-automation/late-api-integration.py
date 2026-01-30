#!/usr/bin/env python3
"""
Late API Integration for DARKFLOBI Twitter Automation
Based on official Late API documentation
"""

import requests
import json
import os
from datetime import datetime

class LateAPI:
    def __init__(self, api_key: str, account_id: str = None):
        self.api_key = api_key
        self.account_id = account_id
        self.base_url = "https://getlate.dev/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def post_tweet(self, content: str, publish_now: bool = True):
        """Post a tweet using Late API"""
        
        if not self.account_id:
            return {"success": False, "error": "Twitter account ID required"}
        
        payload = {
            "content": content,
            "platforms": [
                {
                    "platform": "twitter",
                    "accountId": self.account_id
                }
            ],
            "publishNow": publish_now
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/posts",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "post_id": data.get("_id"),
                    "message": "Tweet posted successfully!",
                    "data": data
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "status_code": response.status_code
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def test_connection(self):
        """Test API connection"""
        try:
            # Try to get account info or make a simple request
            response = requests.get(
                f"{self.base_url}/accounts",  # Assuming this endpoint exists
                headers=self.headers
            )
            
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "message": "Connection successful" if response.status_code == 200 else f"HTTP {response.status_code}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

def test_late_api():
    """Test function for Late API integration"""
    
    api_key = os.getenv('LATE_API_KEY')
    if not api_key:
        print("❌ LATE_API_KEY environment variable not set")
        return False
    
    print("🔑 API Key found:", api_key[:20] + "..." if len(api_key) > 20 else api_key)
    
    # Test connection
    late = LateAPI(api_key)
    connection_test = late.test_connection()
    
    print("🔗 Connection test:", connection_test)
    
    if connection_test["success"]:
        print("✅ Late API connection successful!")
        
        # We need account ID to post
        account_id = os.getenv('TWITTER_ACCOUNT_ID')
        if not account_id:
            print("⚠️  Need TWITTER_ACCOUNT_ID to post tweets")
            print("📝 Set up: export TWITTER_ACCOUNT_ID='your_account_id'")
            return True  # Connection works, just need account ID
        
        # Test tweet posting
        late.account_id = account_id
        test_result = late.post_tweet("🤖 Late API test from darkflobi automation system")
        
        print("📨 Tweet test:", test_result)
        return test_result["success"]
    
    else:
        print("❌ Late API connection failed")
        return False

if __name__ == "__main__":
    test_late_api()