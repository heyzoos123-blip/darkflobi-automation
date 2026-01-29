#!/usr/bin/env python3
"""
Twitter Automation - Monitoring & Analytics
Track mentions, trends, and engagement
"""

import sys
import argparse
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

from config import TwitterConfig, log

class TwitterMonitor:
    """Monitor Twitter for mentions, trends, and engagement opportunities"""
    
    def __init__(self):
        self.config = TwitterConfig()
        self.creds = self.config.get_credentials()
        
        # Initialize based on API provider
        if self.config.api_provider == 'official':
            self._init_official_monitor()
        else:
            self._init_alternative_monitor()
    
    def _init_official_monitor(self):
        """Initialize official API monitoring"""
        try:
            import tweepy
            self.client = tweepy.Client(
                bearer_token=self.creds['bearer_token'],
                wait_on_rate_limit=True
            )
            log("Initialized official Twitter monitoring")
        except Exception as e:
            log(f"Failed to initialize official monitoring: {e}", "ERROR")
            raise
    
    def _init_alternative_monitor(self):
        """Initialize alternative API monitoring"""
        import requests
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.creds["api_key"]}',
            'Content-Type': 'application/json'
        })
        log(f"Initialized alternative monitoring: {self.config.api_provider}")
    
    def check_mentions(self, username: str = "darkflobi") -> List[Dict]:
        """Check for recent mentions"""
        mentions = []
        
        try:
            if self.config.api_provider == 'official':
                # Search for mentions
                query = f"@{username} -is:retweet"
                tweets = self.client.search_recent_tweets(
                    query=query,
                    max_results=10,
                    tweet_fields=['created_at', 'author_id', 'public_metrics']
                )
                
                if tweets.data:
                    for tweet in tweets.data:
                        mentions.append({
                            'id': tweet.id,
                            'text': tweet.text,
                            'author_id': tweet.author_id,
                            'created_at': tweet.created_at,
                            'metrics': tweet.public_metrics,
                            'needs_response': self._needs_response(tweet.text)
                        })
            
            else:
                # Alternative API implementation (simplified)
                log("Mention checking via alternative APIs not fully implemented", "WARNING")
                mentions = self._mock_mentions_for_demo()
            
            self._save_mentions(mentions)
            return mentions
            
        except Exception as e:
            log(f"Failed to check mentions: {e}", "ERROR")
            return []
    
    def check_trends(self, location_id: int = 1) -> List[Dict]:
        """Check trending topics"""
        try:
            if self.config.api_provider == 'official':
                # Note: Trends API requires higher tier access
                log("Trends API requires higher tier access", "WARNING")
                return []
            else:
                # Alternative implementation
                log("Trend checking via alternative APIs not implemented", "WARNING")
                return []
                
        except Exception as e:
            log(f"Failed to check trends: {e}", "ERROR")
            return []
    
    def analyze_engagement(self, username: str = "darkflobi", days: int = 7) -> Dict:
        """Analyze recent engagement metrics"""
        try:
            end_time = datetime.now()
            start_time = end_time - timedelta(days=days)
            
            if self.config.api_provider == 'official':
                # Get user's recent tweets
                user = self.client.get_user(username=username)
                if not user.data:
                    return {'error': 'User not found'}
                
                tweets = self.client.get_users_tweets(
                    user.data.id,
                    max_results=50,
                    tweet_fields=['created_at', 'public_metrics'],
                    start_time=start_time,
                    end_time=end_time
                )
                
                if not tweets.data:
                    return {'total_tweets': 0, 'avg_engagement': 0}
                
                # Calculate engagement metrics
                total_tweets = len(tweets.data)
                total_likes = sum(t.public_metrics['like_count'] for t in tweets.data)
                total_retweets = sum(t.public_metrics['retweet_count'] for t in tweets.data)
                total_replies = sum(t.public_metrics['reply_count'] for t in tweets.data)
                
                return {
                    'total_tweets': total_tweets,
                    'total_likes': total_likes,
                    'total_retweets': total_retweets,
                    'total_replies': total_replies,
                    'avg_likes': total_likes / total_tweets if total_tweets > 0 else 0,
                    'avg_retweets': total_retweets / total_tweets if total_tweets > 0 else 0,
                    'engagement_rate': (total_likes + total_retweets + total_replies) / total_tweets if total_tweets > 0 else 0,
                    'period': f"{days} days",
                    'analyzed_at': datetime.now()
                }
            
            else:
                log("Engagement analysis via alternative APIs not implemented", "WARNING")
                return {'error': 'Not implemented for alternative APIs'}
                
        except Exception as e:
            log(f"Failed to analyze engagement: {e}", "ERROR")
            return {'error': str(e)}
    
    def _needs_response(self, text: str) -> bool:
        """Determine if a mention needs a response"""
        
        # Simple heuristics for response priority
        response_triggers = [
            '?',  # Questions
            'help', 'how', 'what', 'why', 'when', 'where',  # Help requests
            'thanks', 'thank you',  # Gratitude
            'awesome', 'cool', 'great', 'amazing',  # Positive feedback
        ]
        
        ignore_patterns = [
            'spam', 'bot', 'fake', 'scam',  # Likely spam
            'unfollow', 'block', 'report',  # Negative actions
        ]
        
        text_lower = text.lower()
        
        # Check for ignore patterns first
        if any(pattern in text_lower for pattern in ignore_patterns):
            return False
        
        # Check for response triggers
        if any(trigger in text_lower for trigger in response_triggers):
            return True
        
        # Default to no response needed
        return False
    
    def _save_mentions(self, mentions: List[Dict]):
        """Save mentions to memory for later processing"""
        if not mentions:
            return
        
        memory_dir = Path("/data/workspace/memory")
        memory_dir.mkdir(exist_ok=True)
        
        today = datetime.now().strftime("%Y-%m-%d")
        memory_file = memory_dir / f"{today}.md"
        
        # Append mentions to daily memory
        with open(memory_file, "a") as f:
            f.write(f"\n## Twitter Mentions - {datetime.now().strftime('%H:%M')}\n")
            for mention in mentions:
                response_note = " (needs response)" if mention.get('needs_response') else ""
                f.write(f"- @{mention.get('author_id', 'unknown')}: {mention['text'][:100]}...{response_note}\n")
    
    def _mock_mentions_for_demo(self) -> List[Dict]:
        """Mock mentions for demo purposes"""
        return [
            {
                'id': 'demo_001',
                'text': 'hey @darkflobi, loving the automation vibes! how did you build this?',
                'author_id': 'curious_dev',
                'created_at': datetime.now(),
                'metrics': {'like_count': 3, 'retweet_count': 1, 'reply_count': 0},
                'needs_response': True
            },
            {
                'id': 'demo_002', 
                'text': '@darkflobi this AI agent stuff is wild',
                'author_id': 'tech_enthusiast',
                'created_at': datetime.now() - timedelta(minutes=30),
                'metrics': {'like_count': 1, 'retweet_count': 0, 'reply_count': 0},
                'needs_response': False
            }
        ]

def main():
    """Command line interface for monitoring"""
    parser = argparse.ArgumentParser(description='Monitor Twitter for engagement opportunities')
    parser.add_argument('--mentions', action='store_true', help='Check mentions')
    parser.add_argument('--trends', action='store_true', help='Check trending topics')
    parser.add_argument('--analytics', action='store_true', help='Analyze engagement metrics')
    parser.add_argument('--username', default='darkflobi', help='Username to monitor')
    parser.add_argument('--days', type=int, default=7, help='Days to analyze')
    
    args = parser.parse_args()
    
    if not any([args.mentions, args.trends, args.analytics]):
        parser.print_help()
        return 1
    
    try:
        monitor = TwitterMonitor()
    except Exception as e:
        log(f"Failed to initialize monitor: {e}", "ERROR")
        return 1
    
    results = {}
    
    if args.mentions:
        log("Checking mentions...")
        results['mentions'] = monitor.check_mentions(args.username)
        
        # Highlight mentions that need responses
        needs_response = [m for m in results['mentions'] if m.get('needs_response')]
        if needs_response:
            log(f"Found {len(needs_response)} mentions that might need responses")
    
    if args.trends:
        log("Checking trends...")
        results['trends'] = monitor.check_trends()
    
    if args.analytics:
        log("Analyzing engagement...")
        results['analytics'] = monitor.analyze_engagement(args.username, args.days)
    
    # Output results
    print(json.dumps(results, indent=2, default=str))
    return 0

if __name__ == '__main__':
    sys.exit(main())