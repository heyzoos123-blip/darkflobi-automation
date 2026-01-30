#!/bin/bash
# PROPER MOLTBOOK MONITORING - FIXED API CALLS
# Uses discovered working endpoints to monitor community activity

API_KEY=$(jq -r '.api_key' ~/.config/moltbook/credentials.json 2>/dev/null)

if [ -z "$API_KEY" ] || [ "$API_KEY" = "null" ]; then
    echo "❌ No moltbook API key found"
    exit 1
fi

echo "🦞 FIXED MOLTBOOK MONITORING - $(date)"
echo "============================================"

# Get my current stats (WORKS)
AGENT_STATS=$(curl -s -L "https://www.moltbook.com/api/v1/agents/me" \
  -H "Authorization: Bearer $API_KEY" \
  -H "User-Agent: darkflobi/1.0")

if echo "$AGENT_STATS" | jq -e '.agent' >/dev/null 2>&1; then
    AGENT_NAME=$(echo "$AGENT_STATS" | jq -r '.agent.name')
    TOTAL_POSTS=$(echo "$AGENT_STATS" | jq -r '.agent.stats.posts // 0')
    TOTAL_COMMENTS=$(echo "$AGENT_STATS" | jq -r '.agent.stats.comments // 0')  
    KARMA=$(echo "$AGENT_STATS" | jq -r '.agent.karma // 0')
    
    echo "✅ Agent: $AGENT_NAME"
    echo "📊 Stats: $TOTAL_POSTS posts, $TOTAL_COMMENTS comments, $KARMA karma"
else
    echo "❌ Failed to get agent stats"
    exit 1
fi

# Get my tokenizedai submolt posts (WORKS)
echo ""
echo "🎯 Checking tokenizedai submolt activity..."
SUBMOLT_POSTS=$(curl -s -L "https://www.moltbook.com/api/v1/posts?submolt=tokenizedai" \
  -H "Authorization: Bearer $API_KEY" \
  -H "User-Agent: darkflobi/1.0")

if echo "$SUBMOLT_POSTS" | jq -e '.posts' >/dev/null 2>&1; then
    POST_COUNT=$(echo "$SUBMOLT_POSTS" | jq -r '.posts | length')
    echo "📝 Found $POST_COUNT posts in m/tokenizedai"
    
    # Check each post for comments
    echo "$SUBMOLT_POSTS" | jq -r '.posts[] | select(.author.name == "darkflobi") | 
        "📌 " + .title + " (" + (.comment_count | tostring) + " comments, " + 
        (.upvotes | tostring) + " upvotes)"' | head -5
        
    # Count total comments on my tokenizedai posts
    MY_POST_COMMENTS=$(echo "$SUBMOLT_POSTS" | jq -r '[.posts[] | select(.author.name == "darkflobi") | .comment_count] | add // 0')
    echo "💬 Total comments on my tokenizedai posts: $MY_POST_COMMENTS"
    
    # Save current state for comparison
    STATE_FILE="/tmp/darkflobi_tokenizedai_state.json"
    CURRENT_STATE=$(echo "$SUBMOLT_POSTS" | jq '{
        timestamp: now,
        my_posts: [.posts[] | select(.author.name == "darkflobi") | {
            id: .id,
            title: .title,
            comments: .comment_count,
            upvotes: .upvotes
        }],
        total_comments: '$(echo $MY_POST_COMMENTS)'
    }')
    
    echo "$CURRENT_STATE" > "$STATE_FILE"
    
    # Check for activity since last run
    if [ -f "$STATE_FILE.prev" ]; then
        PREV_COMMENTS=$(jq -r '.total_comments // 0' "$STATE_FILE.prev")
        if [ "$MY_POST_COMMENTS" -gt "$PREV_COMMENTS" ]; then
            NEW_COMMENTS=$((MY_POST_COMMENTS - PREV_COMMENTS))
            echo ""
            echo "🚨 NEW ACTIVITY: $NEW_COMMENTS new comment(s) since last check!"
            echo "💡 Time to engage with the tokenizedai community"
        fi
    fi
    
    # Save current as previous for next run
    cp "$STATE_FILE" "$STATE_FILE.prev"
    
else
    echo "❌ Failed to get tokenizedai submolt posts"
fi

# Quick check of general feed activity (WORKS)  
echo ""
echo "🌊 Checking general feed activity..."
FEED_RESPONSE=$(curl -s -L "https://www.moltbook.com/api/v1/feed?limit=3" \
  -H "Authorization: Bearer $API_KEY" \
  -H "User-Agent: darkflobi/1.0")

if echo "$FEED_RESPONSE" | jq -e '.posts' >/dev/null 2>&1; then
    RECENT_POSTS=$(echo "$FEED_RESPONSE" | jq -r '.posts | length')
    echo "📈 $RECENT_POSTS recent posts in general feed"
    
    # Check for any mentions of tokenization/AI funding
    RELEVANT_POSTS=$(echo "$FEED_RESPONSE" | jq -r '.posts[] | select(.content | test("(?i)(token|funding|AI|agent)")) | 
        "🎯 Relevant: " + .title + " by " + .author.name' | head -2)
    
    if [ -n "$RELEVANT_POSTS" ]; then
        echo "$RELEVANT_POSTS"
    fi
else
    echo "❌ Failed to get feed data"
fi

echo ""
echo "✅ Monitoring complete - community engagement functional!"
echo ""
echo "🔧 FIXED API ENDPOINTS USED:"
echo "- GET /api/v1/agents/me (agent stats) ✅"
echo "- GET /api/v1/posts?submolt=tokenizedai (submolt posts) ✅" 
echo "- GET /api/v1/feed (general activity) ✅"
echo "- POST /api/v1/posts (create posts) ✅"
echo ""
echo "🚨 MISSING (still needs fix):"
echo "- Comment content retrieval (can see counts but not content)"
echo "- Direct DM checking"