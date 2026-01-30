#!/bin/bash
# Test Late API connection using curl

echo "🔑 Testing Late API Connection..."

if [ -z "$LATE_API_KEY" ]; then
    echo "❌ LATE_API_KEY not set"
    echo "Usage: LATE_API_KEY='your_key' TWITTER_ACCOUNT_ID='your_id' ./test-late-api.sh"
    exit 1
fi

if [ -z "$TWITTER_ACCOUNT_ID" ]; then
    echo "❌ TWITTER_ACCOUNT_ID not set"
    echo "Usage: LATE_API_KEY='your_key' TWITTER_ACCOUNT_ID='your_id' ./test-late-api.sh"
    exit 1
fi

echo "📡 Testing connection..."

# Test with a simple tweet
curl -X POST https://getlate.dev/api/v1/posts \
  -H "Authorization: Bearer $LATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "🤖 Late API test from darkflobi automation - voice development continues!",
    "platforms": [
      {"platform": "twitter", "accountId": "'$TWITTER_ACCOUNT_ID'"}
    ],
    "publishNow": true
  }' \
  -v

echo ""
echo "✅ If you see a 200 response above, the API is working!"