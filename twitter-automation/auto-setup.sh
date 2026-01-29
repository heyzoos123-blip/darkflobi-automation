#!/bin/bash
# Twitter Automation - Auto Setup Script
# Run this after adding API credentials to .env

echo "🚀 Setting up Twitter automation for darkflobi..."

cd "$(dirname "$0")"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ No .env file found. Copy .env.template to .env and add your API credentials first."
    exit 1
fi

# Test API connection
echo "🔌 Testing API connection..."
python3 tweet.py "twitter automation test - if you see this, everything works! 😁 #test" --dry-run

if [ $? -eq 0 ]; then
    echo "✅ API connection test passed"
else
    echo "❌ API connection failed. Check your .env credentials."
    exit 1
fi

# Generate sample content
echo "📝 Generating sample content..."
mkdir -p samples
python3 simple-tweet.py --template daily_motivation --save samples/daily_motivation.txt
python3 simple-tweet.py --template tech_tip --save samples/tech_tip.txt
python3 simple-tweet.py --thread --template project_update > samples/project_thread.txt
echo "✅ Sample content saved to samples/ directory"

# Set up automation via Clawdbot (commented out - user will do this manually)
echo "⏰ To set up automated posting, run these Clawdbot commands:"
echo ""
echo "# Daily motivation at 9 AM EST:"
echo "cron action=add text='Daily Twitter content' job='{\"schedule\":\"0 9 * * *\",\"command\":\"cd $(pwd) && python3 simple-tweet.py --template random | python3 tweet.py --stdin\"}'"
echo ""
echo "# Weekly project thread on Fridays:"
echo "cron action=add text='Weekly darkflobi update' job='{\"schedule\":\"0 17 * * 5\",\"command\":\"cd $(pwd) && python3 simple-tweet.py --thread --template project_update | python3 tweet.py --thread --stdin\"}'"
echo ""

# Update heartbeat integration
echo "🧠 Adding Twitter monitoring to heartbeat system..."
if [ -f "/data/workspace/HEARTBEAT.md" ]; then
    if ! grep -q "Twitter Check" /data/workspace/HEARTBEAT.md; then
        cat >> /data/workspace/HEARTBEAT.md << 'EOF'

## 🐦 Twitter Check
- Monitor mentions and respond to questions  
- Post content if nothing posted in >8 hours
- Track engagement and optimize timing
EOF
        echo "✅ Added Twitter monitoring to HEARTBEAT.md"
    else
        echo "✅ Twitter monitoring already in HEARTBEAT.md"
    fi
fi

echo ""
echo "🎉 Setup complete! Your Twitter automation is ready."
echo ""
echo "Next steps:"
echo "1. Review samples/ directory for generated content"
echo "2. Test with: python3 tweet.py 'hello twitter! 😁' --dry-run"
echo "3. When ready, remove --dry-run to post for real"
echo "4. Set up the cron jobs shown above for automation"
echo ""
echo "You're ready to dominate Twitter with authentic gremlin energy! ⚡"