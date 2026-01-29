#!/usr/bin/env python3
"""
Twitter Automation - Heartbeat Integration
Smart Twitter management during heartbeat cycles
"""

import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from config import log

class TwitterHeartbeat:
    """Manages Twitter activity during heartbeat cycles"""
    
    def __init__(self):
        self.skill_dir = Path(__file__).parent
        self.state_file = Path("/data/workspace/memory/twitter-state.json")
        self.state = self._load_state()
    
    def _load_state(self) -> dict:
        """Load Twitter automation state"""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    return json.load(f)
            except:
                pass
        
        # Default state
        return {
            'last_mention_check': None,
            'last_tweet': None,
            'last_analytics_check': None,
            'mentions_responded': [],
            'tweet_count_today': 0
        }
    
    def _save_state(self):
        """Save current state"""
        self.state_file.parent.mkdir(exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2, default=str)
    
    def should_check_mentions(self) -> bool:
        """Check if it's time to check mentions"""
        if not self.state['last_mention_check']:
            return True
        
        last_check = datetime.fromisoformat(self.state['last_mention_check'])
        return (datetime.now() - last_check).total_seconds() > 3600  # 1 hour
    
    def should_post_content(self) -> bool:
        """Check if we should post new content"""
        if not self.state['last_tweet']:
            return True
        
        last_tweet = datetime.fromisoformat(self.state['last_tweet'])
        hours_since = (datetime.now() - last_tweet).total_seconds() / 3600
        
        # Post if it's been more than 8 hours and less than 15 tweets today
        return hours_since > 8 and self.state['tweet_count_today'] < 15
    
    def check_mentions(self) -> dict:
        """Check and handle mentions"""
        log("Checking Twitter mentions...")
        
        try:
            result = subprocess.run([
                'python', str(self.skill_dir / 'monitor.py'), '--mentions'
            ], capture_output=True, text=True, cwd=self.skill_dir)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                mentions = data.get('mentions', [])
                
                # Count mentions needing response
                needs_response = [m for m in mentions if m.get('needs_response')]
                
                self.state['last_mention_check'] = datetime.now().isoformat()
                self._save_state()
                
                return {
                    'success': True,
                    'total_mentions': len(mentions),
                    'needs_response': len(needs_response),
                    'mentions': needs_response[:3]  # Top 3 for summary
                }
            
        except Exception as e:
            log(f"Failed to check mentions: {e}", "ERROR")
        
        return {'success': False, 'error': 'mention check failed'}
    
    def post_smart_content(self) -> dict:
        """Generate and post contextual content"""
        log("Generating smart Twitter content...")
        
        try:
            # Generate content based on recent activity
            gen_result = subprocess.run([
                'python', str(self.skill_dir / 'generate.py'), '--from-memory'
            ], capture_output=True, text=True, cwd=self.skill_dir)
            
            if gen_result.returncode != 0:
                # Fallback to template
                gen_result = subprocess.run([
                    'python', str(self.skill_dir / 'generate.py'), '--template', 'daily_motivation'
                ], capture_output=True, text=True, cwd=self.skill_dir)
            
            if gen_result.returncode == 0:
                content = gen_result.stdout.strip()
                
                # Post the content
                tweet_result = subprocess.run([
                    'python', str(self.skill_dir / 'tweet.py'), content
                ], capture_output=True, text=True, cwd=self.skill_dir)
                
                if tweet_result.returncode == 0:
                    tweet_data = json.loads(tweet_result.stdout)
                    
                    if tweet_data['success']:
                        self.state['last_tweet'] = datetime.now().isoformat()
                        self.state['tweet_count_today'] += 1
                        self._save_state()
                        
                        return {
                            'success': True,
                            'content': content[:100],
                            'tweet_id': tweet_data.get('tweet_id')
                        }
            
        except Exception as e:
            log(f"Failed to post content: {e}", "ERROR")
        
        return {'success': False, 'error': 'content posting failed'}
    
    def reset_daily_counters(self):
        """Reset daily counters if it's a new day"""
        if self.state.get('last_reset_date') != datetime.now().strftime('%Y-%m-%d'):
            self.state['tweet_count_today'] = 0
            self.state['last_reset_date'] = datetime.now().strftime('%Y-%m-%d')
            self._save_state()

def run_twitter_heartbeat() -> str:
    """Main heartbeat function - returns summary for heartbeat system"""
    
    heartbeat = TwitterHeartbeat()
    heartbeat.reset_daily_counters()
    
    actions_taken = []
    issues_found = []
    
    # Check mentions if it's time
    if heartbeat.should_check_mentions():
        mention_result = heartbeat.check_mentions()
        
        if mention_result['success']:
            if mention_result['needs_response'] > 0:
                actions_taken.append(f"Found {mention_result['needs_response']} mentions needing response")
            
        else:
            issues_found.append("Mention checking failed")
    
    # Post content if appropriate
    if heartbeat.should_post_content():
        content_result = heartbeat.post_smart_content()
        
        if content_result['success']:
            actions_taken.append(f"Posted: {content_result['content']}")
        else:
            issues_found.append("Content posting failed")
    
    # Prepare summary
    if not actions_taken and not issues_found:
        return "HEARTBEAT_OK"  # Nothing to report
    
    summary_parts = []
    
    if actions_taken:
        summary_parts.append("🐦 Twitter activity:")
        summary_parts.extend([f"  - {action}" for action in actions_taken])
    
    if issues_found:
        summary_parts.append("⚠️ Twitter issues:")
        summary_parts.extend([f"  - {issue}" for issue in issues_found])
    
    return "\n".join(summary_parts)

def main():
    """CLI interface for heartbeat integration"""
    summary = run_twitter_heartbeat()
    print(summary)
    return 0 if summary != "HEARTBEAT_OK" else 0

if __name__ == '__main__':
    import sys
    sys.exit(main())