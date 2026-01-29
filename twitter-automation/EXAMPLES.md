# Twitter Automation - Quick Examples

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
