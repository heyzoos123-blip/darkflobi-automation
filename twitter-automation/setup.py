#!/usr/bin/env python3
"""
Twitter Automation - Setup Script
Easy installation and configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_template():
    """Create environment variable template"""
    env_template = """# Twitter/X Automation Configuration
# Copy this to .env and fill in your actual credentials

# API Provider: 'official', 'late', or 'twitterapi'
TWITTER_API_PROVIDER=late

# Official Twitter API (requires $100+/month)
# Get from: https://developer.x.com/
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here

# Late.dev API (cheaper alternative)
# Get from: https://getlate.dev/
LATE_API_KEY=your_late_api_key_here

# TwitterAPI.io (96% cheaper alternative)
# Get from: https://twitterapi.io/
TWITTERAPI_IO_KEY=your_twitterapi_key_here

# Debug mode (set to 1 for verbose logging)
TWITTER_DEBUG=0
"""
    
    env_file = Path(".env.template")
    with open(env_file, "w") as f:
        f.write(env_template)
    
    print(f"📝 Created {env_file}")
    print("   Copy this to .env and add your API credentials")
    return True

def setup_scripts():
    """Make scripts executable"""
    scripts = ["tweet.py", "generate.py", "monitor.py"]
    
    for script in scripts:
        script_path = Path(script)
        if script_path.exists():
            # Make executable
            os.chmod(script_path, 0o755)
            print(f"✅ Made {script} executable")
    
    return True

def create_example_usage():
    """Create example usage guide"""
    examples = """# Twitter Automation - Quick Examples

## Setup
1. Copy .env.template to .env
2. Add your API credentials to .env
3. Run: python setup.py

## Basic Usage

### Post a tweet
python tweet.py "just shipped some automation magic! 🚀"

### Generate AI content
python generate.py --topic "AI agents"
python generate.py --template daily_motivation

### Create a thread
python generate.py --thread --topic "project update" --max-tweets 4

### Post generated content
python generate.py --topic "coding" | python tweet.py --stdin

### Check mentions
python monitor.py --mentions

### Analyze engagement
python monitor.py --analytics --days 7

## Automation Examples

### Daily motivation tweet (cron)
0 9 * * * cd /path/to/twitter-automation && python generate.py --template daily_motivation | python tweet.py --stdin

### Weekly project update thread
0 17 * * 5 cd /path/to/twitter-automation && python generate.py --thread --topic project_update | python tweet.py --thread --stdin

### Monitor mentions every hour
0 * * * * cd /path/to/twitter-automation && python monitor.py --mentions

## Integration with Clawdbot

### Add to HEARTBEAT.md
```
## Twitter Check
- Monitor mentions and respond to questions
- Post daily content if nothing posted in >8 hours
- Track engagement and optimize timing
```

### Cron job via Clawdbot
cron action=add text="Daily Twitter engagement" job='{"schedule":"0 9,15,21 * * *","command":"cd /data/workspace/skills/twitter-automation && python monitor.py --mentions && python generate.py --from-memory | python tweet.py --stdin"}'
"""
    
    with open("EXAMPLES.md", "w") as f:
        f.write(examples)
    
    print("📚 Created EXAMPLES.md with usage examples")
    return True

def test_setup():
    """Test if setup works"""
    print("🧪 Testing setup...")
    
    # Test imports
    try:
        from config import TwitterConfig
        print("✅ Config module loads correctly")
    except Exception as e:
        print(f"❌ Config module failed: {e}")
        return False
    
    # Test content generation (offline)
    try:
        from generate import ContentGenerator
        gen = ContentGenerator()
        tweet = gen.generate_tweet("test")
        print(f"✅ Content generation works: {tweet[:50]}...")
    except Exception as e:
        print(f"❌ Content generation failed: {e}")
        return False
    
    print("✅ Basic setup test passed")
    print("⚠️  Note: Full functionality requires API credentials in .env")
    return True

def main():
    """Run setup process"""
    print("🚀 Setting up Twitter Automation for darkflobi...")
    print()
    
    success = True
    
    # Install dependencies
    if not install_dependencies():
        success = False
    
    # Create configuration template
    if not create_env_template():
        success = False
    
    # Setup scripts
    if not setup_scripts():
        success = False
    
    # Create examples
    if not create_example_usage():
        success = False
    
    # Test basic functionality
    if not test_setup():
        success = False
    
    print()
    if success:
        print("🎉 Setup completed successfully!")
        print()
        print("Next steps:")
        print("1. Copy .env.template to .env")
        print("2. Add your Twitter API credentials to .env")
        print("3. Test with: python tweet.py 'hello world!' --dry-run")
        print("4. Check EXAMPLES.md for more usage examples")
        print()
        print("For cheap API access, consider:")
        print("- Late.dev: https://getlate.dev/ (no monthly fee)")
        print("- TwitterAPI.io: https://twitterapi.io/ (96% cheaper)")
        print()
        print("Ready to dominate Twitter with gremlin energy! 😁⚡")
    else:
        print("❌ Setup encountered some issues. Check the errors above.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())