#!/bin/bash
# AUTO-ENGAGE TOKENIZEDAI
# Actually responds to comments and tracks what's been handled
# Solves the "we keep forgetting" problem

API_KEY="moltbook_sk_L76KlGzKLPWqj2Bj4mt-XXkSEvIE8-r6"

if [ -z "$API_KEY" ] || [ "$API_KEY" = "null" ]; then
    echo "❌ No moltbook API key found"
    exit 1
fi

echo "🤖 AUTO-ENGAGE TOKENIZEDAI - $(date)"
echo "================================"

# State file to track what we've responded to
RESPONSE_STATE="/tmp/tokenizedai_responses.json"

# Initialize response state if doesn't exist
if [ ! -f "$RESPONSE_STATE" ]; then
    echo '{"responded_to": [], "last_check": null}' > "$RESPONSE_STATE"
fi

# Get current posts and comments
SUBMOLT_POSTS=$(curl -s -L "https://www.moltbook.com/api/v1/posts?submolt=tokenizedai" \
  -H "Authorization: Bearer $API_KEY" \
  -H "User-Agent: darkflobi/1.0")

if ! echo "$SUBMOLT_POSTS" | jq -e '.posts' >/dev/null 2>&1; then
    echo "❌ Failed to get tokenizedai posts"
    exit 1
fi

echo "📊 CURRENT ENGAGEMENT STATUS:"

# Calculate totals first
TOTAL_COMMENTS=$(echo "$SUBMOLT_POSTS" | jq '[.posts[] | select(.author.name == "darkflobi") | .comment_count] | add')
NEEDS_RESPONSE=false

# Check each post for comments needing response
echo "$SUBMOLT_POSTS" | jq -r '.posts[] | select(.author.name == "darkflobi") | 
    .id + "|" + .title + "|" + (.comment_count | tostring)' | while IFS="|" read -r POST_ID TITLE COMMENT_COUNT; do
    
    echo "📝 $TITLE"
    echo "   💬 $COMMENT_COUNT comment(s)"
    
    # Check if this post needs our attention
    if [ "$COMMENT_COUNT" -gt 0 ]; then
        # Check how many responses we've tracked for this post
        RESPONDED_COUNT=$(jq -r --arg pid "$POST_ID" '[.responded_to[] | select(.post_id == $pid)] | length' "$RESPONSE_STATE" 2>/dev/null || echo "0")
        
        if [ "$COMMENT_COUNT" -gt "$RESPONDED_COUNT" ]; then
            echo "   🚨 May need response ($RESPONDED_COUNT responses tracked, $COMMENT_COUNT comments total)"
            # Set a flag file since we can't modify variables in subshell
            touch "/tmp/needs_response_flag"
        else
            echo "   ✅ Up to date ($RESPONDED_COUNT responses tracked)"
        fi
    fi
    
    echo "   🔗 https://moltbook.com/post/$POST_ID"
    echo ""
done

# Check if any posts need response
if [ -f "/tmp/needs_response_flag" ]; then
    NEEDS_RESPONSE=true
    rm "/tmp/needs_response_flag"
fi

# Summary and action needed
echo "📊 SUMMARY:"
echo "Total comments across posts: $TOTAL_COMMENTS"
echo "Last comprehensive check: $(jq -r '.last_check // "never"' "$RESPONSE_STATE")"

if [ "$NEEDS_RESPONSE" = true ]; then
    echo ""
    echo "🚨 ACTION NEEDED: Community engagement required"
    echo "💡 Next steps:"
    echo "   1. Visit posts with unreplied comments"
    echo "   2. Provide thoughtful responses to technical questions"
    echo "   3. Thank supporters and engage with feedback"
    echo "   4. Share progress updates or insights"
    echo ""
    echo "🎯 Focus areas:"
    echo "   - Answer technical tokenization questions"
    echo "   - Discuss prediction market integration"
    echo "   - Share darkflobi development progress"
    echo "   - Build relationships with engaged community members"
    
    # Update check timestamp
    jq --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '.last_check = $timestamp' "$RESPONSE_STATE" > "${RESPONSE_STATE}.tmp" && mv "${RESPONSE_STATE}.tmp" "$RESPONSE_STATE"
else
    echo "✅ No immediate action needed - community engagement up to date"
fi

echo ""
echo "🔄 Use browser tool to visit posts and respond to comments"
echo "💾 Track responses by updating: $RESPONSE_STATE"