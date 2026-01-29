#!/usr/bin/env python3
"""
Composio Integration Tool
500+ app integrations for darkflobi automation
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Any

# Try to import composio
try:
    from composio import Composio, ComposioError
except ImportError:
    print("❌ Composio not available. Install with: npm install @composio/core")
    print("Then use the Node.js interface or install Python SDK")
    sys.exit(1)

class ComposioIntegration:
    """Main Composio integration handler"""
    
    def __init__(self):
        self.api_key = os.getenv('COMPOSIO_API_KEY')
        if not self.api_key:
            raise Exception("COMPOSIO_API_KEY environment variable not set")
        
        self.composio = Composio(api_key=self.api_key)
        self.debug = os.getenv('COMPOSIO_DEBUG', '0') == '1'
        
    def log(self, message: str, level: str = 'INFO'):
        """Simple logging"""
        if self.debug or level in ['ERROR', 'WARNING']:
            print(f"[{level}] {message}")
    
    def execute_action(self, app: str, action: str, params: Dict[str, Any]) -> Dict:
        """Execute a Composio action"""
        try:
            self.log(f"Executing {app}.{action} with params: {params}")
            
            # Execute the action
            result = self.composio.execute_action(
                app=app,
                action=action,
                params=params
            )
            
            self.log(f"Action completed successfully")
            return {
                'success': True,
                'app': app,
                'action': action,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
            
        except ComposioError as e:
            self.log(f"Composio error: {e}", "ERROR")
            return {
                'success': False,
                'app': app,
                'action': action,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.log(f"Unexpected error: {e}", "ERROR")
            return {
                'success': False,
                'app': app,
                'action': action,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_available_apps(self) -> List[str]:
        """Get list of available apps"""
        try:
            return self.composio.get_apps()
        except Exception as e:
            self.log(f"Failed to get apps: {e}", "ERROR")
            return []
    
    def get_app_actions(self, app: str) -> List[str]:
        """Get available actions for an app"""
        try:
            return self.composio.get_actions(app)
        except Exception as e:
            self.log(f"Failed to get actions for {app}: {e}", "ERROR")
            return []

class GmailIntegration:
    """Gmail-specific integration"""
    
    def __init__(self, composio: ComposioIntegration):
        self.composio = composio
    
    def send_email(self, to: str, subject: str, body: str, cc: str = None, bcc: str = None):
        """Send an email via Gmail"""
        params = {
            'to': to,
            'subject': subject,
            'body': body
        }
        if cc:
            params['cc'] = cc
        if bcc:
            params['bcc'] = bcc
        
        return self.composio.execute_action('gmail', 'send_email', params)
    
    def search_emails(self, query: str, max_results: int = 10):
        """Search emails"""
        params = {
            'query': query,
            'max_results': max_results
        }
        return self.composio.execute_action('gmail', 'search', params)
    
    def get_unread_count(self):
        """Get unread email count"""
        return self.composio.execute_action('gmail', 'get_unread_count', {})

class GitHubIntegration:
    """GitHub-specific integration"""
    
    def __init__(self, composio: ComposioIntegration):
        self.composio = composio
    
    def create_issue(self, repo: str, title: str, body: str, labels: List[str] = None):
        """Create a GitHub issue"""
        params = {
            'repo': repo,
            'title': title,
            'body': body
        }
        if labels:
            params['labels'] = labels
        
        return self.composio.execute_action('github', 'create_issue', params)
    
    def list_prs(self, repo: str, state: str = 'open'):
        """List pull requests"""
        params = {
            'repo': repo,
            'state': state
        }
        return self.composio.execute_action('github', 'list_prs', params)
    
    def get_repo_stats(self, repo: str):
        """Get repository statistics"""
        params = {'repo': repo}
        return self.composio.execute_action('github', 'get_repo_stats', params)

class TwitterIntegration:
    """Twitter/X-specific integration"""
    
    def __init__(self, composio: ComposioIntegration):
        self.composio = composio
    
    def post_tweet(self, text: str, media_ids: List[str] = None):
        """Post a tweet"""
        params = {'text': text}
        if media_ids:
            params['media_ids'] = media_ids
        
        return self.composio.execute_action('twitter', 'post_tweet', params)
    
    def get_mentions(self, count: int = 10):
        """Get recent mentions"""
        params = {'count': count}
        return self.composio.execute_action('twitter', 'get_mentions', params)
    
    def search_tweets(self, query: str, count: int = 10):
        """Search tweets"""
        params = {
            'query': query,
            'count': count
        }
        return self.composio.execute_action('twitter', 'search', params)

class SlackIntegration:
    """Slack-specific integration"""
    
    def __init__(self, composio: ComposioIntegration):
        self.composio = composio
    
    def send_message(self, channel: str, text: str):
        """Send a Slack message"""
        params = {
            'channel': channel,
            'text': text
        }
        return self.composio.execute_action('slack', 'send_message', params)
    
    def upload_file(self, channel: str, file_path: str, title: str = None):
        """Upload a file to Slack"""
        params = {
            'channel': channel,
            'file': file_path
        }
        if title:
            params['title'] = title
        
        return self.composio.execute_action('slack', 'upload_file', params)

class CalendarIntegration:
    """Google Calendar integration"""
    
    def __init__(self, composio: ComposioIntegration):
        self.composio = composio
    
    def create_event(self, title: str, start: str, end: str, description: str = None):
        """Create a calendar event"""
        params = {
            'title': title,
            'start': start,
            'end': end
        }
        if description:
            params['description'] = description
        
        return self.composio.execute_action('google_calendar', 'create_event', params)
    
    def list_events(self, date: str = None, count: int = 10):
        """List calendar events"""
        params = {'count': count}
        if date:
            params['date'] = date
        
        return self.composio.execute_action('google_calendar', 'list_events', params)

def add_gremlin_personality(text: str, context: str = 'general') -> str:
    """Add gremlin personality to generated content"""
    
    # Don't modify if it already has personality
    if any(marker in text.lower() for marker in ['😁', '🤖', '⚡', 'gremlin', 'chaos']):
        return text
    
    # Context-specific personality injection
    if context == 'email':
        if not text.lower().startswith(('hey', 'hi', 'hello')):
            text = f"hey! {text}"
        if not text.endswith(('!', '😁', '⚡')):
            text += " 😁"
    
    elif context == 'github':
        # Keep GitHub issues professional but with a touch of personality
        if 'issue' in text.lower() or 'bug' in text.lower():
            text += "\n\n*reported by your friendly neighborhood gremlin* 🤖"
    
    elif context == 'twitter':
        # Twitter gets full gremlin energy
        text = text.lower()  # lowercase aesthetic
        if len(text) < 250:  # room for emoji
            text += " ⚡"
    
    elif context == 'slack':
        # Slack is casual, add some energy
        if not any(emoji in text for emoji in ['😁', '🚀', '⚡', '🤖']):
            text += " 🚀"
    
    return text

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description='Composio Integration Tool')
    parser.add_argument('app', help='App name (gmail, github, twitter, slack, etc.)')
    parser.add_argument('action', help='Action to perform')
    parser.add_argument('--to', help='Email recipient')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--body', help='Email body or message text')
    parser.add_argument('--text', help='Tweet text or message text')
    parser.add_argument('--repo', help='GitHub repository (owner/name)')
    parser.add_argument('--title', help='Issue title or event title')
    parser.add_argument('--channel', help='Slack channel')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--start', help='Event start time')
    parser.add_argument('--end', help='Event end time')
    parser.add_argument('--date', help='Date filter')
    parser.add_argument('--count', type=int, default=10, help='Number of results')
    parser.add_argument('--file', help='File path')
    parser.add_argument('--labels', nargs='+', help='GitHub issue labels')
    parser.add_argument('--cc', help='Email CC')
    parser.add_argument('--bcc', help='Email BCC')
    parser.add_argument('--description', help='Event description')
    parser.add_argument('--list-apps', action='store_true', help='List available apps')
    parser.add_argument('--list-actions', help='List actions for an app')
    parser.add_argument('--personality', action='store_true', help='Add gremlin personality')
    
    args = parser.parse_args()
    
    try:
        composio = ComposioIntegration()
    except Exception as e:
        print(f"❌ Failed to initialize Composio: {e}")
        print("Make sure COMPOSIO_API_KEY environment variable is set")
        return 1
    
    # List apps
    if args.list_apps:
        apps = composio.get_available_apps()
        print("📱 Available apps:")
        for app in apps:
            print(f"  - {app}")
        return 0
    
    # List actions for an app
    if args.list_actions:
        actions = composio.get_app_actions(args.list_actions)
        print(f"🔧 Available actions for {args.list_actions}:")
        for action in actions:
            print(f"  - {action}")
        return 0
    
    # Execute specific integrations
    result = None
    
    if args.app == 'gmail':
        gmail = GmailIntegration(composio)
        
        if args.action == 'send_email':
            if not all([args.to, args.subject, args.body]):
                print("❌ Gmail send_email requires --to, --subject, and --body")
                return 1
            
            # Add personality if requested
            body = args.body
            subject = args.subject
            if args.personality:
                body = add_gremlin_personality(body, 'email')
                if not subject.lower().startswith('darkflobi'):
                    subject = f"darkflobi update - {subject}"
            
            result = gmail.send_email(args.to, subject, body, args.cc, args.bcc)
            
        elif args.action == 'search':
            if not args.query:
                print("❌ Gmail search requires --query")
                return 1
            result = gmail.search_emails(args.query, args.count)
            
        elif args.action == 'get_unread_count':
            result = gmail.get_unread_count()
    
    elif args.app == 'github':
        github = GitHubIntegration(composio)
        
        if args.action == 'create_issue':
            if not all([args.repo, args.title, args.body]):
                print("❌ GitHub create_issue requires --repo, --title, and --body")
                return 1
            
            # Add personality if requested
            body = args.body
            if args.personality:
                body = add_gremlin_personality(body, 'github')
            
            result = github.create_issue(args.repo, args.title, body, args.labels)
            
        elif args.action == 'list_prs':
            if not args.repo:
                print("❌ GitHub list_prs requires --repo")
                return 1
            result = github.list_prs(args.repo)
            
        elif args.action == 'get_repo_stats':
            if not args.repo:
                print("❌ GitHub get_repo_stats requires --repo")
                return 1
            result = github.get_repo_stats(args.repo)
    
    elif args.app == 'twitter':
        twitter = TwitterIntegration(composio)
        
        if args.action == 'post_tweet':
            if not args.text:
                print("❌ Twitter post_tweet requires --text")
                return 1
            
            # Add personality if requested  
            text = args.text
            if args.personality:
                text = add_gremlin_personality(text, 'twitter')
            
            result = twitter.post_tweet(text)
            
        elif args.action == 'get_mentions':
            result = twitter.get_mentions(args.count)
            
        elif args.action == 'search':
            if not args.query:
                print("❌ Twitter search requires --query")
                return 1
            result = twitter.search_tweets(args.query, args.count)
    
    elif args.app == 'slack':
        slack = SlackIntegration(composio)
        
        if args.action == 'send_message':
            if not all([args.channel, args.text]):
                print("❌ Slack send_message requires --channel and --text")
                return 1
            
            # Add personality if requested
            text = args.text
            if args.personality:
                text = add_gremlin_personality(text, 'slack')
            
            result = slack.send_message(args.channel, text)
            
        elif args.action == 'upload_file':
            if not all([args.channel, args.file]):
                print("❌ Slack upload_file requires --channel and --file")
                return 1
            result = slack.upload_file(args.channel, args.file, args.title)
    
    elif args.app == 'google_calendar':
        calendar = CalendarIntegration(composio)
        
        if args.action == 'create_event':
            if not all([args.title, args.start, args.end]):
                print("❌ Calendar create_event requires --title, --start, and --end")
                return 1
            result = calendar.create_event(args.title, args.start, args.end, args.description)
            
        elif args.action == 'list_events':
            result = calendar.list_events(args.date, args.count)
    
    else:
        # Generic action execution
        params = {}
        for key, value in vars(args).items():
            if value is not None and key not in ['app', 'action', 'list_apps', 'list_actions', 'personality']:
                params[key] = value
        
        result = composio.execute_action(args.app, args.action, params)
    
    # Output result
    if result:
        print(json.dumps(result, indent=2, default=str))
        return 0 if result.get('success', False) else 1
    else:
        print(f"❌ Unknown app/action combination: {args.app}.{args.action}")
        return 1

if __name__ == '__main__':
    sys.exit(main())