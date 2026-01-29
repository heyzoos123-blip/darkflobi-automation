#!/usr/bin/env python3
"""
Twitter Automation - Tweet Posting
Core functionality for posting tweets with multiple API support
"""

import sys
import argparse
import json
import time
import requests
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from pathlib import Path

# Import our config
from config import TwitterConfig, PERSONALITY_CONFIG, CONTENT_GUIDELINES, log

try:
    import tweepy
    TWEEPY_AVAILABLE = True
except ImportError:
    TWEEPY_AVAILABLE = False
    log("Tweepy not available, using alternative APIs only", "WARNING")

class TwitterClient:
    """Unified Twitter client supporting multiple APIs"""
    
    def __init__(self):
        self.config = TwitterConfig()
        self.creds = self.config.get_credentials()
        self.last_tweet_time = None
        
        # Initialize API client based on provider
        if self.config.api_provider == 'official' and TWEEPY_AVAILABLE:
            self._init_official_api()
        else:
            self._init_alternative_api()
    
    def _init_official_api(self):
        """Initialize official Twitter API v2 client"""
        try:
            self.client = tweepy.Client(
                bearer_token=self.creds['bearer_token'],
                consumer_key=self.creds['api_key'],
                consumer_secret=self.creds['api_secret'],
                access_token=self.creds['access_token'],
                access_token_secret=self.creds['access_token_secret'],
                wait_on_rate_limit=True
            )
            log("Initialized official Twitter API client")
        except Exception as e:
            log(f"Failed to initialize official API: {e}", "ERROR")
            raise
    
    def _init_alternative_api(self):
        """Initialize alternative API client"""
        self.base_url = self.creds.get('base_url')
        self.headers = {
            'Authorization': f'Bearer {self.creds["api_key"]}',
            'Content-Type': 'application/json'
        }
        log(f"Initialized alternative API: {self.config.api_provider}")
    
    def _respect_cooldown(self):
        """Ensure we don't tweet too frequently"""
        if self.last_tweet_time:
            elapsed = (datetime.now() - self.last_tweet_time).total_seconds() / 60
            cooldown = CONTENT_GUIDELINES['cooldown_minutes']
            
            if elapsed < cooldown:
                wait_time = (cooldown - elapsed) * 60
                log(f"Cooldown active, waiting {wait_time:.1f} seconds")
                time.sleep(wait_time)
    
    def post_tweet(self, text: str, media_path: Optional[str] = None, 
                   reply_to: Optional[str] = None, dry_run: bool = False) -> Dict:
        """Post a single tweet"""
        
        if dry_run:
            log(f"DRY RUN - Would tweet: {text}")
            return {'success': True, 'dry_run': True, 'text': text}
        
        # Respect cooldown
        self._respect_cooldown()
        
        # Validate tweet length
        if len(text) > CONTENT_GUIDELINES['max_length']:
            log(f"Tweet too long ({len(text)} chars), truncating", "WARNING")
            text = text[:277] + "..."
        
        try:
            if self.config.api_provider == 'official':
                return self._post_official(text, media_path, reply_to)
            else:
                return self._post_alternative(text, media_path, reply_to)
                
        except Exception as e:
            log(f"Failed to post tweet: {e}", "ERROR")
            return {'success': False, 'error': str(e)}
    
    def _post_official(self, text: str, media_path: Optional[str], 
                      reply_to: Optional[str]) -> Dict:
        """Post using official Twitter API"""
        try:
            # Handle media upload if provided
            media_ids = []
            if media_path and Path(media_path).exists():
                # Note: This requires tweepy v1.1 API for media upload
                api_v1 = tweepy.API(tweepy.OAuth1UserHandler(
                    self.creds['api_key'], self.creds['api_secret'],
                    self.creds['access_token'], self.creds['access_token_secret']
                ))
                media = api_v1.media_upload(media_path)
                media_ids = [media.media_id]
            
            # Post tweet
            response = self.client.create_tweet(
                text=text,
                media_ids=media_ids if media_ids else None,
                in_reply_to_tweet_id=reply_to
            )
            
            self.last_tweet_time = datetime.now()
            log(f"Tweet posted successfully: {response.data['id']}")
            
            return {
                'success': True,
                'tweet_id': response.data['id'],
                'text': text,
                'timestamp': self.last_tweet_time
            }
            
        except Exception as e:
            log(f"Official API error: {e}", "ERROR")
            return {'success': False, 'error': str(e)}
    
    def _post_alternative(self, text: str, media_path: Optional[str], 
                         reply_to: Optional[str]) -> Dict:
        """Post using alternative API"""
        try:
            payload = {
                'text': text,
                'reply_to': reply_to
            }
            
            # Handle media (implementation depends on specific API)
            if media_path and Path(media_path).exists():
                log("Media upload not yet implemented for alternative APIs", "WARNING")
            
            response = requests.post(
                f"{self.base_url}/tweet",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                self.last_tweet_time = datetime.now()
                result = response.json()
                log(f"Tweet posted successfully via {self.config.api_provider}")
                
                return {
                    'success': True,
                    'tweet_id': result.get('id', 'unknown'),
                    'text': text,
                    'timestamp': self.last_tweet_time
                }
            else:
                error_msg = f"API error {response.status_code}: {response.text}"
                log(error_msg, "ERROR")
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            log(f"Alternative API error: {e}", "ERROR")
            return {'success': False, 'error': str(e)}
    
    def post_thread(self, tweets: List[str], dry_run: bool = False) -> Dict:
        """Post a thread of tweets"""
        if len(tweets) > CONTENT_GUIDELINES['thread_max_tweets']:
            log(f"Thread too long ({len(tweets)} tweets), limiting", "WARNING")
            tweets = tweets[:CONTENT_GUIDELINES['thread_max_tweets']]
        
        results = []
        reply_to = None
        
        for i, tweet in enumerate(tweets):
            log(f"Posting thread tweet {i+1}/{len(tweets)}")
            
            result = self.post_tweet(tweet, reply_to=reply_to, dry_run=dry_run)
            results.append(result)
            
            if result['success'] and not dry_run:
                reply_to = result['tweet_id']
                # Small delay between thread tweets
                time.sleep(2)
            elif not result['success']:
                log(f"Thread failed at tweet {i+1}", "ERROR")
                break
        
        return {
            'success': all(r['success'] for r in results),
            'thread_length': len(results),
            'results': results
        }

def add_personality(text: str) -> str:
    """Add personality touches to tweet content"""
    import random
    
    # Convert to lowercase (our aesthetic)
    text = text.lower()
    
    # Add emoji occasionally  
    if random.random() < PERSONALITY_CONFIG['emoji_frequency']:
        gremlin_emojis = ['😁', '🤖', '⚡', '🔥', '💀', '🌙', '🚀', '⚙️']
        text += f" {random.choice(gremlin_emojis)}"
    
    # Add hashtags if there's room
    remaining_chars = CONTENT_GUIDELINES['max_length'] - len(text)
    hashtags = random.sample(
        PERSONALITY_CONFIG['preferred_hashtags'], 
        min(PERSONALITY_CONFIG['hashtag_limit'], 2)
    )
    
    hashtag_text = " ".join(hashtags)
    if len(hashtag_text) < remaining_chars - 1:
        text += f" {hashtag_text}"
    
    return text

def main():
    """Command line interface for tweet posting"""
    parser = argparse.ArgumentParser(description='Post tweets with personality')
    parser.add_argument('text', nargs='?', help='Tweet text (or read from stdin)')
    parser.add_argument('--image', help='Path to image file')
    parser.add_argument('--reply-to', help='Tweet ID to reply to')
    parser.add_argument('--thread', nargs='+', help='Post as thread')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be posted')
    parser.add_argument('--no-personality', action='store_true', help='Skip personality additions')
    parser.add_argument('--stdin', action='store_true', help='Read from stdin')
    
    args = parser.parse_args()
    
    # Get tweet content
    if args.stdin:
        text = sys.stdin.read().strip()
    elif args.thread:
        text = args.thread
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        return 1
    
    # Initialize client
    try:
        client = TwitterClient()
    except Exception as e:
        log(f"Failed to initialize Twitter client: {e}", "ERROR")
        return 1
    
    # Add personality unless disabled
    if isinstance(text, str) and not args.no_personality:
        text = add_personality(text)
    
    # Post tweet or thread
    if isinstance(text, list) or args.thread:
        tweets = text if isinstance(text, list) else args.thread
        if not args.no_personality:
            tweets = [add_personality(t) for t in tweets]
        result = client.post_thread(tweets, dry_run=args.dry_run)
    else:
        result = client.post_tweet(text, args.image, args.reply_to, args.dry_run)
    
    # Output result
    print(json.dumps(result, indent=2, default=str))
    return 0 if result['success'] else 1

if __name__ == '__main__':
    sys.exit(main())