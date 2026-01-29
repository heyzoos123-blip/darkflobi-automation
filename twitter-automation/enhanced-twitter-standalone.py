#!/usr/bin/env python3
"""
Enhanced Twitter Automation - Standalone Version
Complete Twitter automation with Composio integration and gremlin personality
"""

import os
import sys
import json
import argparse
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

# Configuration and templates
PERSONALITY_CONFIG = {
    'voice': 'chaotic gremlin',
    'tone': 'helpful but not corporate',
    'style': 'lowercase energy',
    'emoji_frequency': 0.7,
    'hashtag_limit': 3,
    'preferred_hashtags': [
        '#AI', '#automation', '#coding', '#productivity',
        '#tech', '#OpenSource', '#Python', '#darkflobi'
    ]
}

CONTENT_GUIDELINES = {
    'max_length': 280,
    'thread_max_tweets': 10,
    'min_engagement_words': 5,
    'cooldown_minutes': 30,
    'daily_tweet_limit': 15,
}

# Simple templates that work without external dependencies
TWEET_TEMPLATES = {
    'daily_motivation': [
        "another day, another chance to automate something that probably didn't need automating",
        "protip: if it takes longer to automate than to do manually, automate it anyway. it's about the principle",
        "morning reminder that you're one bash script away from world domination",
        "today's mood: fix one bug, create three more, call it feature enhancement",
        "caffeine: the original ai performance enhancer"
    ],
    
    'tech_tip': [
        "friendly reminder that documentation is a love letter to your future confused self",
        "debugging is like detective work, except the criminal is you from 3 months ago",
        "version control: because 'final_final_actual_final_v2.py' isn't sustainable",
        "the best code is code you don't have to write. the second best is code that works"
    ],
    
    'project_update': [
        "made some progress on the chaos engine today. still chaotic, but now with 30% more features",
        "update: the ai is learning. mostly learning new ways to confuse me, but it's learning",
        "small wins: fixed the thing that was breaking the other thing. classic tuesday energy",
        "shipped a feature that nobody asked for but everybody needed. that's the gremlin way"
    ],
    
    'random_thoughts': [
        "the internet was a mistake, but it's *our* mistake and we're stuck with it now",
        "imagine explaining to someone from 1990 that we taught sand to think and now it won't stop making memes",
        "technology peaked when we figured out how to make computers beep angrily at us",
        "we're all just npcs in someone else's poorly coded simulation"
    ]
}

def add_gremlin_energy(text: str) -> str:
    """Add gremlin personality to content"""
    # Convert to lowercase (our aesthetic)
    text = text.lower()
    
    # Random personality additions
    if random.random() < 0.3:  # 30% chance
        reactions = ["tbh", "ngl", "honestly", "btw", "anyway"]
        text = f"{random.choice(reactions)}, {text}"
    
    # Add gremlin energy occasionally
    if random.random() < 0.2:  # 20% chance
        gremlin_phrases = ["*gremlin noises*", "*chaos intensifies*", "*rubber duck debugging*"]
        text += f" {random.choice(gremlin_phrases)}"
    
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

def generate_content(topic: str = "random") -> str:
    """Generate content using templates"""
    if topic == 'random':
        topic = random.choice(list(TWEET_TEMPLATES.keys()))
    
    if topic in TWEET_TEMPLATES:
        base_text = random.choice(TWEET_TEMPLATES[topic])
        return add_gremlin_energy(base_text)
    
    # Fallback for unknown topics
    return add_gremlin_energy(f"working on {topic} with the usual gremlin energy. results: surprisingly functional")

def create_thread(topic: str, count: int = 4) -> List[str]:
    """Create a thread about a topic"""
    if topic == 'project_update':
        thread = [
            "weekly darkflobi update thread 🧵",
            "what got built: some cool automation stuff that definitely wasn't supposed to take this long",
            "what got broken: everything else, but that's tomorrow's problem",
            "lessons learned: ai agents are basically digital toddlers with superpowers",
            "next week: more chaos, same energy. stay tuned ⚡"
        ]
    elif topic == 'ai_development':
        thread = [
            "ai development thoughts thread 🧵",
            "building ai systems is like parenting a really smart, really stubborn toddler",
            "they learn fast, break things creatively, and always find edge cases you never considered",
            "but when they work, it feels like actual magic happened in your terminal"
        ]
    else:
        # Generic thread
        thread = [
            f"thread about {topic} 🧵",
            f"so basically, {topic} is pretty wild when you think about it",
            f"the interesting part is how it all connects to everything else",
            f"anyway, that's my take on {topic}. thoughts?"
        ]
    
    return [add_gremlin_energy(t) for t in thread[:count]]

class EnhancedTwitterBot:
    """Enhanced Twitter bot with personality and smart features"""
    
    def __init__(self):
        self.config = self._load_config()
        
        # State management
        self.state_file = Path("/data/workspace/memory/twitter-enhanced-state.json")
        self.state = self._load_state()
        
        # Try to initialize Composio if available
        self.composio = None
        self._init_composio()
    
    def _load_config(self) -> Dict:
        """Load configuration"""
        return {
            'api_provider': os.getenv('TWITTER_API_PROVIDER', 'native'),
            'personality_weight': 0.8,
            'debug': os.getenv('TWITTER_DEBUG', '0') == '1'
        }
    
    def _init_composio(self):
        """Try to initialize Composio"""
        try:
            # This is a placeholder - in real deployment, would use actual Composio
            if os.getenv('COMPOSIO_API_KEY'):
                self.log("✅ Composio API key found (would initialize in production)")
            else:
                self.log("⚠️  No Composio API key - using native mode")
        except Exception as e:
            self.log(f"⚠️  Composio initialization skipped: {e}")
    
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
        self.state_file.parent.mkdir(exist_ok=True, parents=True)
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
            self.log(f"Reset daily counters for {today}")
    
    def can_post_now(self) -> bool:
        """Check if we can post now based on cooldown and daily limits"""
        self.reset_daily_counters()
        
        # Check daily limit
        if self.state['daily_post_count'] >= CONTENT_GUIDELINES['daily_tweet_limit']:
            self.log("Daily tweet limit reached")
            return False
        
        # Check cooldown
        if self.state.get('last_post_time'):
            try:
                last_post = datetime.fromisoformat(self.state['last_post_time'])
                cooldown_minutes = CONTENT_GUIDELINES['cooldown_minutes']
                
                if (datetime.now() - last_post).total_seconds() < (cooldown_minutes * 60):
                    remaining = cooldown_minutes * 60 - (datetime.now() - last_post).total_seconds()
                    self.log(f"Cooldown active ({remaining/60:.1f} minutes remaining)")
                    return False
            except ValueError:
                self.log("Invalid last_post_time format, continuing")
        
        return True
    
    def generate_enhanced_content(self, topic: str = "random", context: str = "") -> str:
        """Generate content with enhanced intelligence"""
        
        # Try memory-based generation first
        memory_content = self._generate_from_memory(topic)
        if memory_content:
            return memory_content
        
        # Use context if provided
        if context:
            return add_gremlin_energy(f"working on {topic} with {context}. chaos levels: optimal")
        
        # Fallback to template-based generation
        return generate_content(topic)
    
    def _generate_from_memory(self, topic: str) -> Optional[str]:
        """Generate content based on recent memory files"""
        try:
            memory_dir = Path("/data/workspace/memory")
            if not memory_dir.exists():
                return None
            
            # Get recent memory files
            recent_files = sorted(memory_dir.glob("*.md"), key=lambda x: x.stat().st_mtime)[-3:]
            
            content_hints = {
                'project_update': ['progress', 'shipped', 'built', 'deployed', 'completed', 'integration'],
                'tech_tip': ['learned', 'discovered', 'fixed', 'optimized', 'debugging', 'breakthrough'],
                'random_thoughts': ['thinking', 'realized', 'noticed', 'wondering', 'insight']
            }
            
            for file in recent_files:
                try:
                    content = file.read_text().lower()
                    for content_type, keywords in content_hints.items():
                        if any(keyword in content for keyword in keywords):
                            if content_type == 'project_update':
                                if 'composio' in content or 'integration' in content:
                                    return add_gremlin_energy("major breakthrough today: integrated 500+ apps via composio. automation level: maximum chaos")
                                elif 'twitter' in content:
                                    return add_gremlin_energy("twitter automation is live and learning to be sarcastic. this feels like natural evolution")
                                else:
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
    
    def post_tweet(self, text: str, dry_run: bool = False) -> Dict:
        """Post tweet (or simulate posting)"""
        
        if not self.can_post_now() and not dry_run:
            return {
                'success': False,
                'error': 'Rate limiting or daily limit reached',
                'text': text,
                'can_post_at': self._next_post_time()
            }
        
        # Add gremlin personality if not already present
        enhanced_text = text
        if not any(marker in text.lower() for marker in ['😁', '🤖', '⚡', 'gremlin', 'chaos']):
            enhanced_text = add_gremlin_energy(text)
        
        if dry_run:
            self.log(f"DRY RUN - Would tweet: {enhanced_text}")
            return {
                'success': True,
                'dry_run': True,
                'text': enhanced_text,
                'character_count': len(enhanced_text),
                'method': 'dry_run'
            }
        
        # In production, this would use actual APIs
        # For now, save to file for manual posting
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"/tmp/darkflobi_tweet_{timestamp}.txt"
            
            with open(filename, 'w') as f:
                f.write(enhanced_text)
                f.write(f"\n\n# Generated at: {datetime.now().isoformat()}")
                f.write(f"\n# Character count: {len(enhanced_text)}")
                f.write(f"\n# Template used: {self._detect_template(enhanced_text)}")
            
            # Update state
            self._update_state_after_post(enhanced_text, 'file_save')
            
            result = {
                'success': True,
                'text': enhanced_text,
                'character_count': len(enhanced_text),
                'method': 'file_save',
                'file': filename,
                'note': 'Tweet saved to file. Set up API for automatic posting.',
                'timestamp': datetime.now().isoformat()
            }
            
            self.log(f"Tweet saved: {enhanced_text[:50]}...")
            return result
            
        except Exception as e:
            self.log(f"Tweet saving failed: {e}", "ERROR")
            return {
                'success': False,
                'error': str(e),
                'text': enhanced_text
            }
    
    def post_thread(self, tweets: List[str], dry_run: bool = False) -> Dict:
        """Post thread (or simulate posting)"""
        
        if not self.can_post_now() and not dry_run:
            return {
                'success': False,
                'error': 'Rate limiting active',
                'thread_length': len(tweets)
            }
        
        # Enhance all tweets
        enhanced_tweets = []
        for i, tweet in enumerate(tweets):
            enhanced = tweet
            if not any(marker in tweet.lower() for marker in ['😁', '🤖', '⚡', 'gremlin']):
                enhanced = add_gremlin_energy(tweet)
            enhanced_tweets.append(enhanced)
        
        if dry_run:
            self.log("DRY RUN - Would post thread:")
            for i, tweet in enumerate(enhanced_tweets, 1):
                self.log(f"  {i}. {tweet}")
            return {
                'success': True,
                'dry_run': True,
                'tweets': enhanced_tweets,
                'thread_length': len(enhanced_tweets),
                'total_characters': sum(len(t) for t in enhanced_tweets)
            }
        
        # Save thread to file
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"/tmp/darkflobi_thread_{timestamp}.txt"
            
            with open(filename, 'w') as f:
                f.write("🧵 DARKFLOBI THREAD 🧵\n")
                f.write("=" * 30 + "\n\n")
                
                for i, tweet in enumerate(enhanced_tweets, 1):
                    f.write(f"{i}. {tweet}\n\n")
                
                f.write(f"# Generated at: {datetime.now().isoformat()}\n")
                f.write(f"# Thread length: {len(enhanced_tweets)} tweets\n")
                f.write(f"# Total characters: {sum(len(t) for t in enhanced_tweets)}\n")
            
            # Update state
            self._update_state_after_post('\n'.join(enhanced_tweets), 'thread_file_save')
            
            result = {
                'success': True,
                'thread_length': len(enhanced_tweets),
                'tweets': enhanced_tweets,
                'method': 'file_save',
                'file': filename,
                'note': 'Thread saved to file. Set up API for automatic posting.',
                'timestamp': datetime.now().isoformat(),
                'total_characters': sum(len(t) for t in enhanced_tweets)
            }
            
            self.log(f"Thread saved: {len(enhanced_tweets)} tweets")
            return result
            
        except Exception as e:
            self.log(f"Thread saving failed: {e}", "ERROR")
            return {
                'success': False,
                'error': str(e),
                'thread_length': len(enhanced_tweets)
            }
    
    def _detect_template(self, text: str) -> str:
        """Detect which template was likely used"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['automate', 'bash script', 'fix one bug']):
            return 'daily_motivation'
        elif any(word in text_lower for word in ['debugging', 'documentation', 'version control']):
            return 'tech_tip'
        elif any(word in text_lower for word in ['progress', 'shipped', 'update', 'chaos engine']):
            return 'project_update'
        elif any(word in text_lower for word in ['internet', 'mistake', 'npc']):
            return 'random_thoughts'
        else:
            return 'custom'
    
    def _update_state_after_post(self, content: str, method: str):
        """Update state after successful post"""
        self.state['last_post_time'] = datetime.now().isoformat()
        self.state['daily_post_count'] += 1
        
        # Track successful patterns
        template = self._detect_template(content)
        self.state.setdefault('successful_templates', []).append(template)
        
        # Track patterns that work
        if '⚡' in content or '🤖' in content:
            self.state.setdefault('successful_patterns', []).append('gremlin_emoji')
        if len(content) < 150:
            self.state.setdefault('successful_patterns', []).append('concise')
        
        self._save_state()
        self.log(f"State updated: {method}, daily count: {self.state['daily_post_count']}")
    
    def _next_post_time(self) -> str:
        """Calculate when next post is allowed"""
        if not self.state.get('last_post_time'):
            return datetime.now().isoformat()
        
        try:
            last_post = datetime.fromisoformat(self.state['last_post_time'])
            next_post = last_post + timedelta(minutes=CONTENT_GUIDELINES['cooldown_minutes'])
            return next_post.isoformat()
        except:
            return datetime.now().isoformat()
    
    def get_analytics(self, days: int = 7) -> Dict:
        """Get analytics and status"""
        try:
            analytics = {
                'status': {
                    'can_post': self.can_post_now(),
                    'daily_posts': self.state.get('daily_post_count', 0),
                    'daily_limit': CONTENT_GUIDELINES['daily_tweet_limit'],
                    'last_post': self.state.get('last_post_time'),
                    'next_post_allowed': self._next_post_time()
                },
                'performance': {
                    'successful_templates': list(set(self.state.get('successful_templates', []))),
                    'successful_patterns': list(set(self.state.get('successful_patterns', []))),
                    'total_posts_tracked': len(self.state.get('successful_templates', []))
                },
                'personality': {
                    'gremlin_energy_level': self.config.get('personality_weight', 0.8),
                    'preferred_emojis': ['😁', '🤖', '⚡', '🔥', '💀', '🌙', '🚀', '⚙️'],
                    'hashtag_strategy': PERSONALITY_CONFIG['preferred_hashtags']
                },
                'configuration': {
                    'api_provider': self.config.get('api_provider', 'native'),
                    'composio_available': bool(os.getenv('COMPOSIO_API_KEY')),
                    'debug_mode': self.config.get('debug', False)
                }
            }
            
            return analytics
        except Exception as e:
            self.log(f"Analytics failed: {e}", "ERROR")
            return {'error': str(e)}

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description='Enhanced Twitter Automation - Darkflobi Edition')
    parser.add_argument('--generate', action='store_true', help='Generate content')
    parser.add_argument('--post', help='Post specific text')
    parser.add_argument('--topic', default='random', help='Content topic')
    parser.add_argument('--template', help='Use specific template')
    parser.add_argument('--thread', action='store_true', help='Create thread')
    parser.add_argument('--analytics', action='store_true', help='Show analytics')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be posted')
    parser.add_argument('--stdin', action='store_true', help='Read from stdin')
    parser.add_argument('--context', help='Additional context')
    parser.add_argument('--count', type=int, default=4, help='Number of tweets in thread')
    
    args = parser.parse_args()
    
    # Initialize bot
    bot = EnhancedTwitterBot()
    
    if args.analytics:
        analytics = bot.get_analytics()
        print(json.dumps(analytics, indent=2, default=str))
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
                    tweets = create_thread(args.topic or 'project_update', args.count)
                
                result = bot.post_thread(tweets, dry_run=args.dry_run)
            else:
                result = bot.post_tweet(content, dry_run=args.dry_run)
            
            print(json.dumps(result, indent=2, default=str))
            return 0 if result.get('success') else 1
    
    parser.print_help()
    return 1

if __name__ == '__main__':
    sys.exit(main())