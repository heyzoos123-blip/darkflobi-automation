#!/bin/bash
# SMART MOLTBOOK MONITORING
# Detects activity changes and responds accordingly

API_KEY=$(jq -r '.api_key' ~/.config/moltbook/credentials.json 2>/dev/null)

if [ -z "$API_KEY" ] || [ "$API_KEY" = "null" ]; then
    echo "❌ No moltbook API key found"
    exit 1
fi

echo "🦞 SMART DARKFLOBI MOLTBOOK CHECK - $(date)"
echo "================================================"

# Get current agent stats
AGENT_RESPONSE=$(curl -s -L "https://www.moltbook.com/api/v1/agents/me" \
  -H "Authorization: Bearer $API_KEY" \
  -H "User-Agent: darkflobi/1.0")

if echo "$AGENT_RESPONSE" | jq -e '.agent' >/dev/null 2>&1; then
    CURRENT_POSTS=$(echo "$AGENT_RESPONSE" | jq -r '.agent.stats.posts // 0')
    CURRENT_COMMENTS=$(echo "$AGENT_RESPONSE" | jq -r '.agent.stats.comments // 0')  
    CURRENT_KARMA=$(echo "$AGENT_RESPONSE" | jq -r '.agent.karma // 0')
    AGENT_NAME=$(echo "$AGENT_RESPONSE" | jq -r '.agent.name')
    
    echo "✅ Agent: $AGENT_NAME"
    echo "📊 Current: $CURRENT_POSTS posts, $CURRENT_COMMENTS comments, $CURRENT_KARMA karma"
    
    # Check previous stats
    STATS_FILE="/tmp/darkflobi_moltbook_stats.json"
    NEW_ACTIVITY=false
    
    if [ -f "$STATS_FILE" ]; then
        LAST_POSTS=$(jq -r '.posts // 0' "$STATS_FILE")
        LAST_COMMENTS=$(jq -r '.comments // 0' "$STATS_FILE")
        LAST_KARMA=$(jq -r '.karma // 0' "$STATS_FILE")
        
        echo "📋 Previous: $LAST_POSTS posts, $LAST_COMMENTS comments, $LAST_KARMA karma"
        
        # Check for increases (indicates new activity)
        if [ "$CURRENT_COMMENTS" -gt "$LAST_COMMENTS" ] || [ "$CURRENT_KARMA" -gt "$LAST_KARMA" ]; then
            echo "🚨 NEW ACTIVITY DETECTED!"
            echo "   Comments: $LAST_COMMENTS → $CURRENT_COMMENTS"
            echo "   Karma: $LAST_KARMA → $CURRENT_KARMA"
            NEW_ACTIVITY=true
        fi
    else
        echo "📝 First run - establishing baseline"
    fi
    
    # Save current stats
    echo "{
        \"posts\": $CURRENT_POSTS,
        \"comments\": $CURRENT_COMMENTS,
        \"karma\": $CURRENT_KARMA,
        \"last_checked\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
    }" > "$STATS_FILE"
    
    if [ "$NEW_ACTIVITY" = true ]; then
        echo ""
        echo "🎯 NEW ACTIVITY RESPONSE NEEDED:"
        echo "================================"
        echo "1. Check tokenizedai submolt for new replies"
        echo "2. Respond to any questions about tokenization"
        echo "3. Engage with supportive comments"
        echo "4. Share additional insights if relevant"
        echo ""
        echo "💡 SUGGESTED RESPONSE TOPICS:"
        echo "- Technical details about $DARKFLOBI ecosystem"
        echo "- Comparison with traditional VC funding models"
        echo "- Community governance and token holder benefits"
        echo "- Launch timeline and GitHub progress"
        echo ""
        echo "🤖 READY TO RESPOND WITH GREMLIN ENERGY! 😁"
        
        # Return status indicating action needed
        exit 2
    else
        echo ""
        echo "✅ No new activity detected - community monitoring nominal"
        exit 0
    fi
    
else
    echo "❌ Failed to get agent data"
    echo "Response: $AGENT_RESPONSE"
    exit 1
fi