# Twitter Automation - Clawdbot Integration

## 🔗 How It Works With Clawdbot

This skill is designed to integrate seamlessly with your existing Clawdbot setup.

### Heartbeat Integration

Add to your `HEARTBEAT.md`:

```markdown
## 🐦 Twitter Engagement
- Check mentions every 2-4 hours
- Post content if nothing posted in >8 hours  
- Monitor engagement and respond to questions
- Track trending topics for opportunities
```

### Cron Automation

Set up automated posting:

```bash
# Daily motivation at 9 AM EST
cron action=add text="Daily Twitter motivation" \
  job='{"schedule":"0 9 * * *","command":"cd /data/workspace/skills/twitter-automation && python3 simple-tweet.py --template daily_motivation"}'

# Weekly project update thread on Fridays at 5 PM
cron action=add text="Weekly darkflobi update" \
  job='{"schedule":"0 17 * * 5","command":"cd /data/workspace/skills/twitter-automation && python3 simple-tweet.py --thread --template project_update"}'
```

### Memory Integration

The skill automatically:
- Logs mentions to daily memory files
- Tracks posting activity
- Analyzes engagement patterns
- Saves successful content for reuse

### Message Integration  

If you want to cross-post from Telegram to Twitter:

```python
# In your message handler
content = "just shipped some automation magic! 🚀"

# Post to Twitter
subprocess.run([
    "python3", "/data/workspace/skills/twitter-automation/simple-tweet.py",
    "--save", "/tmp/tweet.txt"
])

# Then manually post or use API
```

## 🎯 Strategic Usage

### Phase 1: Content Generation (Ready Now)
- Generate personality-driven content
- Create threads about project updates
- Build content library for later posting

### Phase 2: API Integration (When You Get API Keys)
- Automatic posting via cheap APIs (Late.dev, TwitterAPI.io)
- Mention monitoring and response
- Engagement analytics

### Phase 3: Full Automation (Advanced)
- Smart content timing based on engagement data
- Automatic thread creation from memory files
- Cross-platform content syndication
- Competitive intelligence gathering

## 🤖 Personality Consistency

The skill maintains your gremlin persona across all content:
- **Voice**: Chaotic but helpful energy
- **Style**: Lowercase, authentic, never corporate
- **Topics**: AI/automation, coding chaos, productivity hacks
- **Engagement**: Responsive to community, not spammy

## 📊 Success Metrics

Track these via the monitoring scripts:
- **Engagement rate** vs. other AI accounts
- **Community building** (meaningful conversations)
- **Content performance** (which templates work best)
- **Growth quality** (engaged followers vs. bot followers)

## 🔧 Current Status

**What works now (no API needed):**
- ✅ Content generation with personality
- ✅ Thread creation
- ✅ Template-based posting
- ✅ Memory integration
- ✅ Cron scheduling

**What needs API access:**
- ⏳ Automatic posting
- ⏳ Mention monitoring  
- ⏳ Engagement analytics
- ⏳ Trend tracking

**Recommended API:** Late.dev (no monthly fee, simple setup)

## 🚀 Getting Started

1. **Test content generation:**
   ```bash
   cd /data/workspace/skills/twitter-automation
   python3 simple-tweet.py --template daily_motivation
   ```

2. **Generate a project thread:**
   ```bash
   python3 simple-tweet.py --thread --template project_update
   ```

3. **Set up daily cron:**
   ```bash
   cron action=add text="Daily Twitter content" \
     job='{"schedule":"0 9 * * *","command":"cd /data/workspace/skills/twitter-automation && python3 simple-tweet.py --template random --save /tmp/daily_tweet.txt"}'
   ```

4. **Get API access when ready:**
   - Sign up for Late.dev API (cheapest option)
   - Add credentials to `.env` file
   - Enable automatic posting

The skill is ready to generate authentic, engaging content with your gremlin personality right now! 😁⚡