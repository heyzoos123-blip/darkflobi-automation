#!/bin/bash
# ACTIVE TOKENIZEDAI MONITORING
# Monitors replies to our posts and comments in real-time

API_KEY=$(jq -r '.api_key' ~/.config/moltbook/credentials.json 2>/dev/null)

if [ -z "$API_KEY" ] || [ "$API_KEY" = "null" ]; then
    echo "❌ No moltbook API key found"
    exit 1
fi

echo "🦞 ACTIVE TOKENIZEDAI MONITORING - $(date)"
echo "=========================================="

# Get current state of our tokenizedai posts
SUBMOLT_POSTS=$(curl -s -L "https://www.moltbook.com/api/v1/posts?submolt=tokenizedai" \
  -H "Authorization: Bearer $API_KEY" \
  -H "User-Agent: darkflobi/1.0")

if echo "$SUBMOLT_POSTS" | jq -e '.posts' >/dev/null 2>&1; then
    # Track each of our posts specifically
    echo "📊 CURRENT POST STATUS:"
    echo "$SUBMOLT_POSTS" | jq -r '.posts[] | select(.author.name == "darkflobi") | 
        "📝 " + .title + 
        "\n   💬 " + (.comment_count | tostring) + " comments, " +
        "👍 " + (.upvotes | tostring) + " upvotes, " +
        "🆔 " + .id + "\n"'
    
    # Save detailed state for comparison
    STATE_FILE="/tmp/tokenizedai_detailed_state.json"
    CURRENT_STATE=$(echo "$SUBMOLT_POSTS" | jq '{
        timestamp: now,
        posts: [.posts[] | select(.author.name == "darkflobi") | {
            id: .id,
            title: .title,
            comments: .comment_count,
            upvotes: .upvotes,
            url: .url
        }]
    }')
    
    echo "$CURRENT_STATE" > "$STATE_FILE"
    
    # Check for changes since last check
    if [ -f "$STATE_FILE.prev" ]; then
        echo "🔍 CHECKING FOR NEW ACTIVITY..."
        
        # Compare comment counts
        for post_id in $(echo "$CURRENT_STATE" | jq -r '.posts[].id'); do
            CURRENT_COMMENTS=$(echo "$CURRENT_STATE" | jq -r ".posts[] | select(.id == \"$post_id\") | .comments")
            PREV_COMMENTS=$(jq -r ".posts[] | select(.id == \"$post_id\") | .comments // 0" "$STATE_FILE.prev" 2>/dev/null || echo "0")
            POST_TITLE=$(echo "$CURRENT_STATE" | jq -r ".posts[] | select(.id == \"$post_id\") | .title")
            
            if [ "$CURRENT_COMMENTS" -gt "$PREV_COMMENTS" ]; then
                NEW_COMMENTS=$((CURRENT_COMMENTS - PREV_COMMENTS))
                echo "🚨 NEW ACTIVITY: \"$POST_TITLE\" +$NEW_COMMENTS comment(s) ($PREV_COMMENTS → $CURRENT_COMMENTS)"
                echo "🔗 https://moltbook.com/post/$post_id"
                echo ""
                
                # Store this as an alert for main monitoring
                echo "{
                    \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
                    \"post_id\": \"$post_id\",
                    \"post_title\": \"$POST_TITLE\",
                    \"new_comments\": $NEW_COMMENTS,
                    \"total_comments\": $CURRENT_COMMENTS,
                    \"action_needed\": true
                }" > "/tmp/tokenizedai_alert_$post_id.json"
                
                ACTIVITY_DETECTED=true
            fi
        done
        
        if [ "$ACTIVITY_DETECTED" != true ]; then
            echo "✅ No new activity since last check"
        fi
    else
        echo "📝 First monitoring run - establishing baseline"
    fi
    
    # Save current state as previous for next run
    cp "$STATE_FILE" "$STATE_FILE.prev"
    
    # Quick feed check for relevant discussions
    echo ""
    echo "🌊 Checking for tokenization discussions in general feed..."
    FEED_RESPONSE=$(curl -s -L "https://www.moltbook.com/api/v1/feed?limit=10" \
      -H "Authorization: Bearer $API_KEY" \
      -H "User-Agent: darkflobi/1.0")
    
    if echo "$FEED_RESPONSE" | jq -e '.posts' >/dev/null 2>&1; then
        RELEVANT_POSTS=$(echo "$FEED_RESPONSE" | jq -r '.posts[] | 
            select(.content | test("(?i)(token|funding|prediction.*market|darkflobi)")) | 
            "🎯 " + .title + " by " + .author.name' | head -3)
        
        if [ -n "$RELEVANT_POSTS" ]; then
            echo "$RELEVANT_POSTS"
        else
            echo "📭 No relevant discussions in general feed"
        fi
    fi
    
else
    echo "❌ Failed to get tokenizedai posts"
    exit 1
fi

echo ""
echo "📊 Monitoring complete at $(date)"
echo "🔄 Run this script regularly to track community engagement"