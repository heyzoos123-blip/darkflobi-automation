#!/usr/bin/env python3
"""
Twitter Automation - Configuration Manager
Handles API credentials and settings for different Twitter/X services
"""

import os
from typing import Dict, Optional

# Try to load dotenv if available, fallback to just os.getenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # No problem, we'll just use environment variables directly
    pass

class TwitterConfig:
    """Manages Twitter/X API configurations"""
    
    def __init__(self):
        self.api_provider = os.getenv('TWITTER_API_PROVIDER', 'late')  # late, official, twitterapi
        self.debug = os.getenv('TWITTER_DEBUG', '0') == '1'
        
    def get_credentials(self) -> Dict[str, str]:
        """Get API credentials based on selected provider"""
        
        if self.api_provider == 'official':
            return {
                'api_key': os.getenv('TWITTER_API_KEY'),
                'api_secret': os.getenv('TWITTER_API_SECRET'), 
                'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
                'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
                'bearer_token': os.getenv('TWITTER_BEARER_TOKEN')
            }
            
        elif self.api_provider == 'late':
            return {
                'api_key': os.getenv('LATE_API_KEY'),
                'base_url': 'https://api.getlate.dev/v1'
            }
            
        elif self.api_provider == 'twitterapi':
            return {
                'api_key': os.getenv('TWITTERAPI_IO_KEY'),
                'base_url': 'https://api.twitterapi.io/v1'
            }
        
        else:
            raise ValueError(f"Unknown API provider: {self.api_provider}")
    
    def validate_credentials(self) -> bool:
        """Check if required credentials are available"""
        creds = self.get_credentials()
        
        if self.api_provider == 'official':
            required = ['api_key', 'api_secret', 'access_token', 'access_token_secret']
            return all(creds.get(key) for key in required)
            
        else:
            return bool(creds.get('api_key'))

# Personality and content settings
PERSONALITY_CONFIG = {
    'voice': 'chaotic gremlin',
    'tone': 'helpful but not corporate', 
    'style': 'lowercase energy',
    'emoji_frequency': 0.7,  # 70% of tweets get emoji
    'hashtag_limit': 3,      # max hashtags per tweet
    'preferred_hashtags': [
        '#AI', '#automation', '#coding', '#productivity', 
        '#tech', '#OpenSource', '#Python', '#darkflobi'
    ],
    'avoid_hashtags': [
        '#blockchain', '#crypto', '#NFT', '#sponsored'  # keep it authentic
    ]
}

CONTENT_GUIDELINES = {
    'max_length': 280,           # Twitter character limit
    'thread_max_tweets': 10,     # reasonable thread length
    'min_engagement_words': 5,   # avoid too-short tweets
    'cooldown_minutes': 30,      # min time between posts
    'daily_tweet_limit': 15,     # avoid spam appearance
}

# Timing optimization
OPTIMAL_TIMES = {
    'timezone': 'America/New_York',  # flobi's timezone
    'peak_hours': [9, 12, 15, 18, 21],  # EST peak engagement times
    'avoid_hours': [1, 2, 3, 4, 5, 6],  # late night quiet hours
    'weekend_shift': -2,  # post 2 hours later on weekends
}

def log(message: str, level: str = 'INFO'):
    """Simple logging with debug support"""
    if TwitterConfig().debug or level in ['ERROR', 'WARNING']:
        print(f"[{level}] {message}")

def get_config() -> TwitterConfig:
    """Get configured Twitter client"""
    return TwitterConfig()