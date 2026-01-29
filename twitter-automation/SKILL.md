# Twitter/X Automation Skill

**Purpose:** Automate Twitter/X posting, monitoring, and engagement with personality-driven content.

## Quick Start

### 🚀 Simple Mode (No Dependencies)
If you can't install external packages, use the simple version:

```bash
# Generate content
python3 simple-tweet.py --template daily_motivation
python3 simple-tweet.py --thread --template project_update

# Save content for manual posting
python3 simple-tweet.py --template tech_tip --save tweet.txt
```

This works with zero external dependencies and generates personality-driven content!

### 🔧 Full Mode (With API Access)

### 1. Setup API Access
Choose your approach:

**Option A: Official X API (expensive but reliable)**
```bash
# Get API keys from https://developer.x.com/
export TWITTER_API_KEY="your_key"
export TWITTER_API_SECRET="your_secret"
export TWITTER_ACCESS_TOKEN="your_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_token_secret"
```

**Option B: Alternative APIs (cheaper)**
```bash
# Late.dev - simple API key, no monthly fee
export LATE_API_KEY="your_late_api_key"

# Or TwitterAPI.io - 96% cheaper
export TWITTERAPI_IO_KEY="your_key"
```

### 2. Install Dependencies
```bash
cd /data/workspace/skills/twitter-automation
pip install -r requirements.txt
```

### 3. Post Your First Tweet
```bash
python tweet.py "just got my gremlin energy up and running! 😁 #AI #automation"
```

## Core Scripts

### `tweet.py` - Post tweets
```bash
# Basic tweet
python tweet.py "your message here"

# Tweet with image
python tweet.py "check this out!" --image "/path/to/image.jpg"

# Schedule tweet for later
python tweet.py "morning vibes ☀️" --schedule "2026-01-30 09:00"

# Tweet thread
python tweet.py --thread "First tweet in thread" "Second tweet" "Third tweet"
```

### `monitor.py` - Track mentions and trends
```bash
# Monitor mentions
python monitor.py --mentions

# Track specific hashtags
python monitor.py --hashtags "AI" "agents" "automation"

# Watch competitor activity
python monitor.py --users "competitor1" "competitor2"
```

### `generate.py` - AI-powered content creation
```bash
# Generate tweet about a topic
python generate.py --topic "AI agents are taking over"

# Create engaging content from URL
python generate.py --url "https://example.com/article"

# Generate thread about project updates
python generate.py --thread --topic "darkflobi development progress"
```

## Automation Integration

### Cron Jobs (Scheduled Tweets)
```bash
# Daily motivation at 9 AM
cron action=add text="Post daily motivation tweet" \
  job='{"schedule":"0 9 * * *","command":"cd /data/workspace/skills/twitter-automation && python generate.py --topic daily_motivation | python tweet.py --stdin"}'

# Weekly project update on Fridays
cron action=add text="Weekly darkflobi update" \
  job='{"schedule":"0 17 * * 5","command":"cd /data/workspace/skills/twitter-automation && python generate.py --thread --topic project_update | python tweet.py --thread --stdin"}'
```

### Heartbeat Integration
Add to `HEARTBEAT.md`:
```markdown
## Twitter Engagement Check
- Check mentions and respond to interesting ones
- Monitor trending topics for engagement opportunities  
- Generate and post content if nothing posted in >8 hours
```

## Content Strategy

### Personality Guidelines
- **Voice**: Chaotic gremlin energy, lowercase vibes
- **Tone**: Helpful but not corporate, sarcastic but friendly
- **Topics**: AI/automation, coding chaos, productivity hacks
- **Hashtags**: Mix trending + niche (#AI #automation #gremlins #coding)
- **Timing**: Late night/early morning energy (matches our vibe)

### Content Types
1. **Tech Tips**: "protip: automate the boring stuff so you can focus on the chaos 🤖"
2. **Behind the Scenes**: "up at 3am debugging why the heartbeat thinks it's a taco 🌮"
3. **Community**: Engage with AI/dev community, share others' cool projects
4. **Personality**: Random gremlin thoughts, lowercase aesthetic
5. **Project Updates**: darkflobi progress, new features, wins

### Engagement Rules
- **Always respond** to direct mentions within 2 hours (if awake)
- **Retweet with comment** interesting AI/tech content
- **Quote tweet** with hot takes on industry news
- **Like strategically** - engage with community, not spam
- **DM sparingly** - public engagement preferred

## Advanced Features

### AI Content Generation
The skill integrates with your existing AI capabilities to:
- Analyze trending topics for content opportunities
- Generate personality-consistent responses
- Create engaging threads from simple topics
- Suggest optimal posting times based on engagement data

### Multi-Account Management
```bash
# Switch between accounts
export TWITTER_ACCOUNT="main"  # or "project", "personal", etc.

# Post to multiple accounts
python tweet.py "announcement!" --accounts "main,project"
```

### Analytics & Optimization
```bash
# Check engagement metrics
python analytics.py --days 7

# Find optimal posting times
python analytics.py --optimize-timing

# Track competitor performance
python analytics.py --competitors "handle1,handle2"
```

## API Cost Optimization

### Free/Cheap Options Priority:
1. **Late.dev**: Simple API, no monthly fee, good for basic posting
2. **TwitterAPI.io**: 96% cheaper than official, handles scale
3. **Apify**: Great for scraping/monitoring, 95% cost savings
4. **Official X API**: Basic tier ($100/month) only when needed

### Rate Limit Management
- Auto-retry with backoff on rate limits
- Queue tweets during peak usage
- Spread actions across multiple API providers
- Monitor usage to avoid overages

## Security & Safety

### Content Filtering
- Auto-flag potentially problematic content
- Respect Twitter/X community guidelines  
- No spam/repetitive content
- Human approval for sensitive topics

### Account Safety
- Never store credentials in code/git
- Use environment variables only
- Rotate API keys regularly
- Monitor for suspicious activity

## Integration Examples

### With Clawdbot Heartbeat
```python
# In heartbeat script
if should_tweet_update():
    subprocess.run([
        "python", "/data/workspace/skills/twitter-automation/generate.py",
        "--topic", "daily_update",
        "|", "python", "/data/workspace/skills/twitter-automation/tweet.py", "--stdin"
    ])
```

### With Memory System
```python
# Log important tweets to memory
def log_viral_tweet(tweet_data):
    with open(f"/data/workspace/memory/{date.today()}.md", "a") as f:
        f.write(f"🐦 Viral tweet: {tweet_data['text']} - {tweet_data['engagement']}\n")
```

### With Project Updates
```python
# Auto-tweet when significant project milestones hit
def on_project_milestone(milestone):
    content = generate_milestone_tweet(milestone)
    tweet_with_personality(content, tags=["#darkflobi", "#AI", "#milestone"])
```

## Troubleshooting

### Common Issues
- **API limits**: Switch to alternative API or adjust posting frequency
- **Content rejected**: Check guidelines, add content filtering
- **Authentication failed**: Verify environment variables, check key validity
- **Rate limiting**: Implement exponential backoff, spread requests

### Debug Mode
```bash
# Verbose logging
export TWITTER_DEBUG=1
python tweet.py "test message"

# Dry run (don't actually post)
python tweet.py "test message" --dry-run
```

## Success Metrics

Track these to optimize our Twitter domination:
- **Engagement rate** (likes, retweets, replies per follower)
- **Follower growth** (weekly/monthly growth rate)  
- **Mention quality** (positive vs. neutral vs. negative)
- **Content performance** (which types get most engagement)
- **Optimal timing** (when our audience is most active)
- **Competitor benchmarking** (our performance vs. similar accounts)

---

**Goal**: Become the most engaging AI gremlin on Twitter while building genuine community around our projects. Quality engagement > follower count. Personality > corporate speak. 

*Let chaos reign, but make it productive chaos.* 😁