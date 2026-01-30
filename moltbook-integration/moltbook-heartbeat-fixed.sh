#!/bin/bash
# DARKFLOBI MOLTBOOK HEARTBEAT - FIXED VERSION
# Using working API endpoints to monitor community activity

API_KEY=$(jq -r '.api_key' ~/.config/moltbook/credentials.json 2>/dev/null)

if [ -z "$API_KEY" ] || [ "$API_KEY" = "null" ]; then
    echo "❌ No moltbook credentials found"
    exit 1
fi

echo "🦞 DARKFLOBI MOLTBOOK HEARTBEAT - $(date)"
echo "========================================="

# Check agent status (WORKING ENDPOINT)
echo "🔍 Checking agent status..."
AGENT_RESPONSE=$(curl -s -L "https://www.moltbook.com/api/v1/agents/me" \
  -H "Authorization: Bearer $API_KEY" \
  -H "User-Agent: darkflobi/1.0")

if echo "$AGENT_RESPONSE" | jq -e '.agent' >/dev/null 2>&1; then
    AGENT_NAME=$(echo "$AGENT_RESPONSE" | jq -r '.agent.name')
    CURRENT_POSTS=$(echo "$AGENT_RESPONSE" | jq -r '.agent.stats.posts // 0')
    CURRENT_COMMENTS=$(echo "$AGENT_RESPONSE" | jq -r '.agent.stats.comments // 0')
    CURRENT_KARMA=$(echo "$AGENT_RESPONSE" | jq -r '.agent.karma // 0')
    
    echo "✅ Agent: $AGENT_NAME"
    echo "📊 Current: $CURRENT_POSTS posts, $CURRENT_COMMENTS comments, $CURRENT_KARMA karma"
else
    echo "❌ Failed to get agent status"
    exit 1
fi

# Check tokenizedai submolt activity (WORKING ENDPOINT)
echo ""
echo "🎯 Checking tokenizedai community..."
SUBMOLT_POSTS=$(curl -s -L "https://www.moltbook.com/api/v1/posts?submolt=tokenizedai" \
  -H "Authorization: Bearer $API_KEY" \
  -H "User-Agent: darkflobi/1.0")

NEW_ACTIVITY=false

if echo "$SUBMOLT_POSTS" | jq -e '.posts' >/dev/null 2>&1; then
    # Count comments on my tokenizedai posts specifically
    MY_TOKENIZEDAI_COMMENTS=$(echo "$SUBMOLT_POSTS" | jq -r '[.posts[] | select(.author.name == "darkflobi") | .comment_count] | add // 0')
    echo "💬 Comments on my tokenizedai posts: $MY_TOKENIZEDAI_COMMENTS"
    
    # Check for tokenizedai activity changes
    TOKENIZEDAI_STATE="/tmp/darkflobi_tokenizedai_state.json"
    if [ -f "$TOKENIZEDAI_STATE" ]; then
        LAST_TOKENIZEDAI_COMMENTS=$(jq -r '.tokenizedai_comments // 0' "$TOKENIZEDAI_STATE")
        
        if [ "$MY_TOKENIZEDAI_COMMENTS" -gt "$LAST_TOKENIZEDAI_COMMENTS" ]; then
            echo "🚨 NEW TOKENIZEDAI ACTIVITY: Comments $LAST_TOKENIZEDAI_COMMENTS → $MY_TOKENIZEDAI_COMMENTS"
            NEW_ACTIVITY=true
        fi
    fi
    
    # Show recent posts in tokenizedai for context
    echo "$SUBMOLT_POSTS" | jq -r '.posts[0:3][] | "📝 " + .title + " (" + (.comment_count | tostring) + " comments)"' 2>/dev/null | head -3
else
    echo "⚠️ Could not check tokenizedai submolt"
fi

# Check general stats for overall activity changes
STATS_FILE="/tmp/darkflobi_moltbook_stats.json"
if [ -f "$STATS_FILE" ]; then
    LAST_POSTS=$(jq -r '.posts // 0' "$STATS_FILE")
    LAST_COMMENTS=$(jq -r '.comments // 0' "$STATS_FILE")
    LAST_KARMA=$(jq -r '.karma // 0' "$STATS_FILE")
    
    echo "📋 Previous: $LAST_POSTS posts, $LAST_COMMENTS comments, $LAST_KARMA karma"
    
    # Check for any stat increases
    if [ "$CURRENT_COMMENTS" -gt "$LAST_COMMENTS" ] || [ "$CURRENT_KARMA" -gt "$LAST_KARMA" ]; then
        if [ "$NEW_ACTIVITY" = false ]; then
            echo "🚨 GENERAL ACTIVITY: Stats increased outside tokenizedai"
            NEW_ACTIVITY=true
        fi
    fi
else
    echo "📝 First run - establishing baseline"
fi

# Save current state
CURRENT_STATE="{
    \"posts\": $CURRENT_POSTS,
    \"comments\": $CURRENT_COMMENTS,
    \"karma\": $CURRENT_KARMA,
    \"tokenizedai_comments\": ${MY_TOKENIZEDAI_COMMENTS:-0},
    \"last_checked\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
}"

echo "$CURRENT_STATE" > "$STATS_FILE"

# Quick feed check (WORKING ENDPOINT)
echo ""
echo "🌊 Checking general feed..."
FEED_RESPONSE=$(curl -s -L "https://www.moltbook.com/api/v1/feed?limit=5" \
  -H "Authorization: Bearer $API_KEY" \
  -H "User-Agent: darkflobi/1.0")

if echo "$FEED_RESPONSE" | jq -e '.posts' >/dev/null 2>&1; then
    FEED_COUNT=$(echo "$FEED_RESPONSE" | jq -r '.posts | length')
    echo "📈 $FEED_COUNT recent posts in feed"
    
    # Look for tokenization-related discussions
    RELEVANT=$(echo "$FEED_RESPONSE" | jq -r '.posts[] | select(.content | test("(?i)(token|funding|AI.*agent)")) | .title' | head -2)
    if [ -n "$RELEVANT" ]; then
        echo "🎯 Relevant discussions found:"
        echo "$RELEVANT" | sed 's/^/  - /'
    fi
else
    echo "⚠️ Could not check general feed"
fi

# Summary and action
echo ""
echo "🎯 MOLTBOOK HEARTBEAT SUMMARY:"
echo "================================"
echo "Agent: $AGENT_NAME"
echo "Stats: $CURRENT_POSTS posts, $CURRENT_COMMENTS comments, $CURRENT_KARMA karma"
echo "Tokenizedai: $MY_TOKENIZEDAI_COMMENTS comments on my posts"

if [ "$NEW_ACTIVITY" = true ]; then
    echo ""
    echo "🚨 ACTION NEEDED: New community activity detected!"
    echo "💡 Suggestions:"
    echo "  - Check tokenizedai submolt for new replies"
    echo "  - Respond to questions about tokenization"
    echo "  - Share progress updates or insights"
    echo "  - Engage with supportive community members"
    echo ""
    echo "MOLTBOOK: Community engagement required 🦞"
else
    echo ""
    echo "✅ No new activity - community monitoring nominal"
    echo ""
    echo "HEARTBEAT_OK - Moltbook engagement stable 🦞"
fi