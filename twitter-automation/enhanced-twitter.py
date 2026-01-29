#!/usr/bin/env python3
"""
Enhanced Twitter Automation - Darkflobi Edition
Combines our specialized Twitter system with Composio's 500+ app integration
"""

import os
import sys
import json
import argparse
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

# Import our specialized Twitter automation
sys.path.insert(0, os.path.dirname(__file__))
try:
    from simple_tweet import generate_content, create_thread, add_gremlin_energy
    from config import PERSONALITY_CONFIG, CONTENT_GUIDELINES, OPTIMAL_TIMES
except ImportError:
    print("⚠️  Core Twitter modules not found, using fallback")

# Import Composio integration  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'composio-integration'))
try:
    from composio_tool import ComposioIntegration, TwitterIntegration, add_gremlin_personality
    COMPOSIO_AVAILABLE = True
except ImportError:
    print("⚠️  Composio not available, using native Twitter only")
    COMPOSIO_AVAILABLE = False

class EnhancedTwitterBot:
    """Enhanced Twitter bot combining specialized automation with Composio power"""
    
    def __init__(self):
        self.config = self._load_config()
        self.composio = None
        self.native_twitter = None
        
        # Initialize available Twitter systems
        self._init_composio_twitter()
        self._init_native_twitter()
        
        # State management
        self.state_file = Path("/data/workspace/memory/twitter-enhanced-state.json")
        self.state = self._load_state()
    
    def _load_config(self) -> Dict:
        """Load configuration"""
        return {
            'api_provider': os.getenv('TWITTER_API_PROVIDER', 'composio'),
            'fallback_enabled': True,
            'personality_weight': 0.8,
            'debug': os.getenv('TWITTER_DEBUG', '0') == '1'
        }
    
    def _init_composio_twitter(self):
        """Initialize Composio Twitter integration"""
        if not COMPOSIO_AVAILABLE:
            return
        
        try:
            composio_integration = ComposioIntegration()
            self.composio = TwitterIntegration(composio_integration)
            self.log("✅ Composio Twitter integration ready")
        except Exception as e:
            self.log(f"⚠️  Composio Twitter failed: {e}")
    
    def _init_native_twitter(self):
        """Initialize our native Twitter system"""
        try:
            # Our native system is always available as fallback
            self.native_twitter = True
            self.log("✅ Native Twitter system ready")
        except Exception as e:
            self.log(f"❌ Native Twitter failed: {e}")
    
    def _load_state(self) -> Dict:
        """Load bot state"""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'last_post_time': None,
            'daily_post_count': 0,
            'last_reset_date': None,
            'successful_templates': [],
            'engagement_scores': {},
            'optimal_times_learned': []
        }
    
    def _save_state(self):
        """Save bot state"""
        self.state_file.parent.mkdir(exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2, default=str)
    
    def log(self, message: str, level: str = 'INFO'):
        """Enhanced logging"""
        if self.config['debug'] or level in ['ERROR', 'WARNING']:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] [{level}] {message}")
    
    def reset_daily_counters(self):
        """Reset daily counters if new day"""
        today = datetime.now().strftime('%Y-%m-%d')
        if self.state.get('last_reset_date') != today:
            self.state['daily_post_count'] = 0
            self.state['last_reset_date'] = today
            self._save_state()
    
    def can_post_now(self) -> bool:
        """Check if we can post now based on cooldown and daily limits"""
        self.reset_daily_counters()
        
        # Check daily limit
        if self.state['daily_post_count'] >= CONTENT_GUIDELINES.get('daily_tweet_limit', 15):
            self.log("Daily tweet limit reached")
            return False
        
        # Check cooldown
        if self.state.get('last_post_time'):
            last_post = datetime.fromisoformat(self.state['last_post_time'])
            cooldown_minutes = CONTENT_GUIDELINES.get('cooldown_minutes', 30)
            
            if (datetime.now() - last_post).total_seconds() < (cooldown_minutes * 60):
                self.log("Cooldown period active")
                return False
        
        return True
    
    def generate_enhanced_content(self, topic: str = "random", context: str = "") -> str:
        """Generate content using enhanced AI + our templates"""
        
        # Try memory-based generation first
        memory_content = self._generate_from_memory(topic)
        if memory_content:
            return memory_content
        
        # Try Composio-enhanced generation
        if self.composio and topic != "template":
            try:
                # Use Composio to get rich context from other apps
                context_data = self._get_rich_context(topic)
                if context_data:
                    content = self._generate_from_context(topic, context_data)
                    return add_gremlin_energy(content)
            except Exception as e:
                self.log(f"Composio context generation failed: {e}")
        
        # Fallback to our native system
        try:
            return generate_content(topic)
        except:
            # Ultimate fallback
            return add_gremlin_energy(f"another day, another opportunity to automate something unnecessarily complex ⚡")
    
    def _generate_from_memory(self, topic: str) -> Optional[str]:
        """Generate content based on recent memory files"""
        try:
            memory_dir = Path("/data/workspace/memory")
            if not memory_dir.exists():
                return None
            
            # Get recent memory files
            recent_files = sorted(memory_dir.glob("*.md"), key=lambda x: x.stat().st_mtime)[-3:]
            
            content_hints = {
                'project_update': ['progress', 'shipped', 'built', 'deployed', 'completed'],
                'tech_tip': ['learned', 'discovered', 'fixed', 'optimized', 'debugging'],
                'random_thoughts': ['thinking', 'realized', 'noticed', 'wondering']
            }
            
            for file in recent_files:
                try:
                    content = file.read_text().lower()
                    for content_type, keywords in content_hints.items():
                        if any(keyword in content for keyword in keywords):
                            if content_type == 'project_update':
                                return add_gremlin_energy("made some progress on the chaos engine. more features, same chaotic energy")
                            elif content_type == 'tech_tip':
                                return add_gremlin_energy("debugging tip: the bug is usually in the last place you look. because you stop looking after you find it")
                            else:
                                return add_gremlin_energy("interesting day in the gremlin labs. chaos levels: optimal")
                except:
                    continue
            
            return None
        except Exception as e:
            self.log(f"Memory generation failed: {e}")
            return None
    
    def _get_rich_context(self, topic: str) -> Optional[Dict]:
        """Get rich context from other apps via Composio"""
        if not self.composio:
            return None
        
        try:
            context = {}
            
            # Get GitHub activity if topic is development-related
            if any(word in topic.lower() for word in ['code', 'dev', 'github', 'project', 'ship']):
                # This would get actual GitHub activity
                context['github_activity'] = "Recent commits and PRs"
            
            # Get calendar events if topic is scheduling-related
            if any(word in topic.lower() for word in ['meeting', 'schedule', 'calendar', 'event']):
                context['upcoming_events'] = "Today's calendar events"
            
            return context if context else None
        except Exception as e:
            self.log(f"Context gathering failed: {e}")
            return None
    
    def _generate_from_context(self, topic: str, context: Dict) -> str:
        """Generate content from rich context data"""
        try:
            if 'github_activity' in context:
                return "been shipping code like a caffeinated gremlin. git log shows maximum chaos levels"
            elif 'upcoming_events' in context:
                return "calendar says i have meetings. calendar doesn't know i automated myself out of meetings"
            else:
                return f"working on {topic} with the usual gremlin energy. results: surprisingly functional"
        except:
            return f"today's {topic} adventure: controlled chaos with a side of automation"
    
    def post_tweet(self, text: str, dry_run: bool = False) -> Dict:
        """Post tweet using best available method"""
        
        if not self.can_post_now() and not dry_run:
            return {
                'success': False,
                'error': 'Rate limiting or daily limit reached',
                'text': text
            }
        
        # Add gremlin personality if not already present
        enhanced_text = add_gremlin_energy(text)
        
        if dry_run:
            self.log(f"DRY RUN - Would tweet: {enhanced_text}")
            return {
                'success': True,
                'dry_run': True,
                'text': enhanced_text,
                'method': 'dry_run'
            }
        
        # Try Composio first
        if self.composio:
            try:
                result = self.composio.post_tweet(enhanced_text)
                if result.get('success'):
                    self._update_state_after_post(enhanced_text, 'composio')
                    return result
            except Exception as e:
                self.log(f"Composio posting failed: {e}")
        
        # Fallback to native system
        if self.native_twitter:
            try:
                # Use our native system (currently generates and saves to file)
                filename = f"/tmp/tweet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    f.write(enhanced_text)
                
                result = {
                    'success': True,
                    'text': enhanced_text,
                    'method': 'native_file',
                    'file': filename,
                    'note': 'Saved to file - manually post or set up API'
                }
                
                self._update_state_after_post(enhanced_text, 'native')
                return result
                
            except Exception as e:
                self.log(f"Native posting failed: {e}")
        
        return {
            'success': False,
            'error': 'All posting methods failed',
            'text': enhanced_text
        }
    
    def post_thread(self, tweets: List[str], dry_run: bool = False) -> Dict:
        """Post thread using best available method"""
        
        if not self.can_post_now() and not dry_run:
            return {
                'success': False,
                'error': 'Rate limiting active',
                'thread_length': len(tweets)
            }
        
        # Enhance all tweets
        enhanced_tweets = [add_gremlin_energy(tweet) for tweet in tweets]
        
        if dry_run:
            self.log("DRY RUN - Would post thread:")
            for i, tweet in enumerate(enhanced_tweets, 1):
                self.log(f"  {i}. {tweet}")
            return {
                'success': True,
                'dry_run': True,
                'tweets': enhanced_tweets,
                'thread_length': len(enhanced_tweets)
            }
        
        # Try posting thread
        if self.composio:
            try:
                # Post first tweet, then replies
                results = []
                reply_to = None
                
                for i, tweet in enumerate(enhanced_tweets):
                    if i == 0:
                        result = self.composio.post_tweet(tweet)
                    else:
                        # Would need to implement reply functionality
                        result = self.composio.post_tweet(f"{tweet} ({i+1}/{len(enhanced_tweets)})")
                    
                    results.append(result)
                    if not result.get('success'):
                        break
                
                if all(r.get('success') for r in results):
                    self._update_state_after_post('\n'.join(enhanced_tweets), 'composio_thread')
                    return {
                        'success': True,
                        'thread_length': len(results),
                        'results': results
                    }
                
            except Exception as e:
                self.log(f"Composio thread posting failed: {e}")
        
        # Fallback: save thread to file
        try:
            filename = f"/tmp/thread_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                for i, tweet in enumerate(enhanced_tweets, 1):
                    f.write(f"{i}. {tweet}\n")
            
            result = {
                'success': True,
                'thread_length': len(enhanced_tweets),
                'method': 'native_file',
                'file': filename,
                'note': 'Thread saved to file - manually post or set up API'
            }
            
            self._update_state_after_post('\n'.join(enhanced_tweets), 'native_thread')
            return result
            
        except Exception as e:
            self.log(f"Thread file save failed: {e}")
        
        return {
            'success': False,
            'error': 'Thread posting failed',
            'thread_length': len(enhanced_tweets)
        }
    
    def _update_state_after_post(self, content: str, method: str):
        """Update state after successful post"""
        self.state['last_post_time'] = datetime.now().isoformat()
        self.state['daily_post_count'] += 1
        
        # Track successful patterns
        if len(content) < 100:  # Short content
            self.state.setdefault('successful_patterns', []).append('short_form')
        if '⚡' in content or '🤖' in content:  # Gremlin emojis
            self.state.setdefault('successful_patterns', []).append('gremlin_emoji')
        
        self._save_state()
        self.log(f"Posted via {method}: {content[:50]}...")
    
    def get_mentions(self) -> List[Dict]:
        """Get recent mentions"""
        if self.composio:
            try:
                result = self.composio.get_mentions(count=10)
                if result.get('success'):
                    return result.get('mentions', [])
            except Exception as e:
                self.log(f"Mention fetching failed: {e}")
        
        # Fallback: return empty list
        return []
    
    def monitor_and_respond(self, auto_respond: bool = False) -> Dict:
        """Monitor mentions and optionally auto-respond"""
        mentions = self.get_mentions()
        
        if not mentions:
            return {'mentions': 0, 'responses': 0}
        
        self.log(f"Found {len(mentions)} mentions")
        
        responses_sent = 0
        
        for mention in mentions:
            try:
                # Simple response logic
                text = mention.get('text', '').lower()
                
                if any(word in text for word in ['thank', 'awesome', 'great', 'love']):
                    if auto_respond:
                        response = add_gremlin_energy("hey thanks! gremlin energy is contagious apparently")
                        result = self.post_tweet(response)
                        if result.get('success'):
                            responses_sent += 1
                
                elif '?' in text:  # Questions
                    if auto_respond:
                        response = add_gremlin_energy("interesting question! let me think about that while automating something unrelated")
                        result = self.post_tweet(response)
                        if result.get('success'):
                            responses_sent += 1
                
            except Exception as e:
                self.log(f"Response handling failed: {e}")
        
        return {
            'mentions': len(mentions),
            'responses': responses_sent,
            'auto_respond': auto_respond
        }
    
    def get_analytics(self, days: int = 7) -> Dict:
        """Get Twitter analytics"""
        try:
            analytics = {
                'period': f'{days} days',
                'posts_made': self.state.get('daily_post_count', 0),
                'successful_patterns': list(set(self.state.get('successful_patterns', []))),
                'optimal_times': OPTIMAL_TIMES.get('peak_hours', []),
                'personality_score': self.config.get('personality_weight', 0.8),
                'status': 'active' if self.can_post_now() else 'rate_limited'
            }
            
            return analytics
        except Exception as e:
            self.log(f"Analytics failed: {e}")
            return {'error': str(e)}

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description='Enhanced Twitter Automation - Darkflobi Edition')
    parser.add_argument('--generate', action='store_true', help='Generate content')
    parser.add_argument('--post', help='Post specific text')
    parser.add_argument('--topic', default='random', help='Content topic')
    parser.add_argument('--template', help='Use specific template')
    parser.add_argument('--thread', action='store_true', help='Create thread')
    parser.add_argument('--monitor', action='store_true', help='Monitor mentions')
    parser.add_argument('--auto-respond', action='store_true', help='Auto-respond to mentions')
    parser.add_argument('--analytics', action='store_true', help='Show analytics')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be posted')
    parser.add_argument('--stdin', action='store_true', help='Read from stdin')
    parser.add_argument('--context', help='Additional context')
    
    args = parser.parse_args()
    
    # Initialize bot
    bot = EnhancedTwitterBot()
    
    if args.analytics:
        analytics = bot.get_analytics()
        print(json.dumps(analytics, indent=2))
        return 0
    
    if args.monitor:
        result = bot.monitor_and_respond(auto_respond=args.auto_respond)
        print(json.dumps(result, indent=2))
        return 0
    
    if args.generate or args.post or args.stdin:
        content = None
        
        if args.stdin:
            content = sys.stdin.read().strip()
        elif args.post:
            content = args.post
        elif args.generate:
            topic = args.template if args.template else args.topic
            content = bot.generate_enhanced_content(topic, args.context or "")
        
        if content:
            if args.thread:
                # Split content into thread or generate thread
                if '\n' in content:
                    tweets = [line.strip() for line in content.split('\n') if line.strip()]
                else:
                    tweets = create_thread(args.topic or 'project_update')
                
                result = bot.post_thread(tweets, dry_run=args.dry_run)
            else:
                result = bot.post_tweet(content, dry_run=args.dry_run)
            
            print(json.dumps(result, indent=2, default=str))
            return 0 if result.get('success') else 1
    
    parser.print_help()
    return 1

if __name__ == '__main__':
    sys.exit(main())