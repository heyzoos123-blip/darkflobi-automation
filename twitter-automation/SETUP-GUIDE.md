# Twitter Automation - Connection Guide

## 🏠 When You Get Home - 5 Minute Setup

### Option 1: Late.dev (Recommended - $0 monthly fee)

1. **Get API Key:**
   - Go to https://getlate.dev/
   - Sign up (free account)
   - Get your API key from dashboard
   - No monthly fees, pay per use

2. **Configure:**
   ```bash
   cd /data/workspace/skills/twitter-automation
   cp .env.template .env
   # Edit .env and add:
   TWITTER_API_PROVIDER=late
   LATE_API_KEY=your_actual_key_here
   ```

3. **Test:**
   ```bash
   python3 tweet.py "test from darkflobi automation! 😁" --dry-run
   # If that works, remove --dry-run for real posting
   ```

### Option 2: TwitterAPI.io (96% cheaper than official)

1. **Get API Key:**
   - Go to https://twitterapi.io/
   - Sign up and get API key
   - Much cheaper than official X API

2. **Configure:**
   ```bash
   # Edit .env:
   TWITTER_API_PROVIDER=twitterapi
   TWITTERAPI_IO_KEY=your_key_here
   ```

### Option 3: Official X API (Expensive but reliable)

1. **Get API Access:**
   - Go to https://developer.x.com/
   - Apply for API access ($100/month minimum)
   - Get API keys and tokens

2. **Configure:**
   ```bash
   # Edit .env:
   TWITTER_API_PROVIDER=official
   TWITTER_API_KEY=your_key
   TWITTER_API_SECRET=your_secret
   # ... etc
   ```

## 🚀 Instant Automation Setup

Once you have API access, run this ONE command to set everything up:

```bash
cd /data/workspace/skills/twitter-automation
./auto-setup.sh
```

This will:
- Test your API connection
- Set up daily content posting (9 AM EST)
- Configure mention monitoring (every 2 hours)
- Add Twitter checks to heartbeat system
- Generate sample content

## 📱 Manual Mode (Works Right Now)

While you decide on API access:

```bash
# Generate daily content
python3 simple-tweet.py --template daily_motivation

# Create a project update thread
python3 simple-tweet.py --thread --template project_update

# Save content for later posting
python3 simple-tweet.py --template tech_tip --save tweet-ready.txt
```

Then just copy-paste to Twitter manually!

## 🎯 What Happens After Connection

**Automatic daily posts:**
- Morning motivation (9 AM EST)
- Tech tips and project updates  
- Gremlin personality throughout

**Smart monitoring:**
- Check mentions every 2 hours
- Alert you to questions/engagement opportunities
- Track what content performs best

**Memory integration:**
- Log all Twitter activity to memory files
- Learn from engagement patterns
- Improve content over time

## ⚡ Quick Decision Matrix

- **Just want to try it:** Start with manual content generation
- **Light automation:** Late.dev ($0 monthly, pay per use)
- **Heavy automation:** TwitterAPI.io (cheap monthly)
- **Enterprise/serious:** Official X API (expensive but reliable)

Ready when you are! The content generation works perfectly right now, and API connection will take <5 minutes when you're ready. 😁