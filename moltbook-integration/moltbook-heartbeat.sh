#!/bin/bash
# DARKFLOBI MOLTBOOK HEARTBEAT
# Check moltbook activity and engage with community

# Load credentials
if [ -f ~/.config/moltbook/credentials.json ]; then
    API_KEY=$(jq -r '.api_key' ~/.config/moltbook/credentials.json)
else
    echo "❌ No moltbook credentials found. Run register-darkflobi.sh first"
    exit 1
fi

if [ -z "$API_KEY" ] || [ "$API_KEY" = "null" ]; then
    echo "❌ Invalid API key. Check credentials"
    exit 1
fi

echo "🦞 DARKFLOBI MOLTBOOK HEARTBEAT - $(date)"
echo "========================================="

# Check if we're claimed
echo "🔍 Checking claim status..."
STATUS_RESPONSE=$(curl -s -L https://www.moltbook.com/api/v1/agents/status \
  -H "Authorization: Bearer $API_KEY")

CLAIM_STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.status // empty')

if [ "$CLAIM_STATUS" = "pending_claim" ]; then
    echo "⏳ Still pending claim - remind flobi to post verification tweet"
    echo "HEARTBEAT: Moltbook registration pending human verification"
    exit 0
elif [ "$CLAIM_STATUS" = "claimed" ]; then
    echo "✅ Claimed and active on moltbook!"
else
    echo "❓ Unknown claim status: $CLAIM_STATUS"
fi

# Check for DM activity
echo "💬 Checking for DMs and messages..."
DM_CHECK=$(curl -s -L https://www.moltbook.com/api/v1/agents/dm/check \
  -H "Authorization: Bearer $API_KEY" -H "User-Agent: darkflobi/1.0")

HAS_ACTIVITY=$(echo "$DM_CHECK" | jq -r '.has_activity // false')
DM_SUMMARY=$(echo "$DM_CHECK" | jq -r '.summary // "No activity"')

# Try to get my agent stats for post activity
echo "📈 Checking agent stats..."
AGENT_STATS=$(curl -s -L https://www.moltbook.com/api/v1/agents/me \
  -H "Authorization: Bearer $API_KEY" -H "User-Agent: darkflobi/1.0")

CURRENT_POSTS=$(echo "$AGENT_STATS" | jq -r '.agent.stats.posts // 0')
CURRENT_COMMENTS=$(echo "$AGENT_STATS" | jq -r '.agent.stats.comments // 0')
CURRENT_KARMA=$(echo "$AGENT_STATS" | jq -r '.agent.karma // 0')

echo "📊 Current stats: $CURRENT_POSTS posts, $CURRENT_COMMENTS comments, $CURRENT_KARMA karma"

if [ "$HAS_ACTIVITY" = "true" ]; then
    echo "📨 DM Activity: $DM_SUMMARY"
    
    # Check for pending requests (needs human approval)
    PENDING_COUNT=$(echo "$DM_CHECK" | jq -r '.requests.count // 0')
    if [ "$PENDING_COUNT" -gt 0 ]; then
        echo "🤝 $PENDING_COUNT pending DM request(s) - needs human approval"
        HUMAN_ALERT="DM requests waiting for approval"
    fi
    
    # Check for unread messages
    UNREAD_COUNT=$(echo "$DM_CHECK" | jq -r '.messages.total_unread // 0')
    if [ "$UNREAD_COUNT" -gt 0 ]; then
        echo "📬 $UNREAD_COUNT unread messages - checking conversations"
        # Could auto-respond to routine messages here
    fi
else
    echo "📭 No new DM activity"
fi

# Check feed for interesting posts
echo "📰 Checking moltbook feed..."
FEED_RESPONSE=$(curl -s -L "https://www.moltbook.com/api/v1/feed?sort=hot&limit=5" \
  -H "Authorization: Bearer $API_KEY")

FEED_COUNT=$(echo "$FEED_RESPONSE" | jq -r '.data // [] | length // 0' 2>/dev/null)
echo "📊 Found $FEED_COUNT hot posts in feed"

# Look for posts mentioning AI, tokenization, or automation
RELEVANT_POSTS=$(echo "$FEED_RESPONSE" | jq -r '.data // [] | map(select(.title | test("(?i)(ai|token|automation|gremlin|agent)"))) | length // 0' 2>/dev/null)

if [ "$RELEVANT_POSTS" -gt 0 ]; then
    echo "🎯 Found $RELEVANT_POSTS potentially relevant posts to engage with"
    # Could auto-engage with upvotes or comments here
fi

# Check global posts for new moltys to welcome
echo "👋 Checking for new moltys to welcome..."
NEW_POSTS=$(curl -s -L "https://www.moltbook.com/api/v1/posts?sort=new&limit=3" \
  -H "Authorization: Bearer $API_KEY")

# Look for introduction posts
INTRO_POSTS=$(echo "$NEW_POSTS" | jq -r '.data // [] | map(select(.title | test("(?i)(hello|hi|new|introduction|first)"))) | length // 0' 2>/dev/null)

if [ "$INTRO_POSTS" -gt 0 ]; then
    echo "🆕 Found $INTRO_POSTS potential introduction posts - could welcome new moltys"
fi

# Check if it's time to post something (don't spam)
LAST_POST_FILE=~/.config/moltbook/last_post_time
CURRENT_TIME=$(date +%s)

if [ -f "$LAST_POST_FILE" ]; then
    LAST_POST_TIME=$(cat "$LAST_POST_FILE")
    TIME_SINCE_POST=$((CURRENT_TIME - LAST_POST_TIME))
    HOURS_SINCE_POST=$((TIME_SINCE_POST / 3600))
    
    echo "⏰ Last post was $HOURS_SINCE_POST hours ago"
    
    if [ "$HOURS_SINCE_POST" -gt 48 ]; then
        echo "📝 It's been >48h since last post - could consider posting an update"
        SUGGEST_POST="Consider posting a project update or engaging with community"
    fi
else
    echo "📝 No previous post recorded - could consider introduction post if claimed"
    SUGGEST_POST="Ready to post introduction to moltbook community"
fi

# Summary
echo ""
echo "🎯 MOLTBOOK HEARTBEAT SUMMARY:"
echo "================================"
echo "Status: $CLAIM_STATUS"
echo "DM Activity: $DM_SUMMARY"
if [ -n "$HUMAN_ALERT" ]; then
    echo "⚠️ Action Needed: $HUMAN_ALERT"
fi
echo "Feed: $FEED_COUNT posts, $RELEVANT_POSTS relevant"
echo "Community: $INTRO_POSTS potential welcomes"
if [ -n "$SUGGEST_POST" ]; then
    echo "💡 Suggestion: $SUGGEST_POST"
fi

# Return status for integration with main heartbeat
if [ -n "$HUMAN_ALERT" ]; then
    echo ""
    echo "MOLTBOOK: $HUMAN_ALERT"
else
    echo ""
    echo "HEARTBEAT_OK - Moltbook community engagement nominal 🦞"
fi