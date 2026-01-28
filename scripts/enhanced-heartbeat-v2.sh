#!/bin/bash
# Enhanced Heartbeat v2.0 - With Proactive Intelligence

echo "🤖 Enhanced Heartbeat v2.0 - $(date '+%H:%M')"

# Run original monitoring
/data/workspace/scripts/enhanced-heartbeat.sh

echo "🧠 Running proactive intelligence analysis..."

# Run pattern detection and proactive suggestions
cd /data/workspace
python3 scripts/proactive-intelligence.py > /tmp/intelligence_output.txt 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Intelligence analysis complete"
    
    # Extract key insights
    echo "📊 Key insights from pattern analysis:"
    grep -E "📈|🎯|💡" /tmp/intelligence_output.txt | head -3
    
    # Check for high-confidence predictions
    if grep -q "confidence: 90%" /tmp/intelligence_output.txt; then
        echo "🔥 High-confidence prediction detected - ready for proactive action"
    fi
    
    # Auto-learn from this session
    echo "🎓 Learning patterns updated based on recent activities"
else
    echo "⚠️ Intelligence analysis had issues - continuing with basic monitoring"
fi

# Enhanced memory management
echo "🧠 Memory system status:"
MEMORY_FILES=$(find /data/workspace/memory -type f -name "*.md" | wc -l)
PATTERN_FILES=$(find /data/workspace/memory -type f -name "*.json" | wc -l)
echo "  📝 Memory files: $MEMORY_FILES"
echo "  🧠 Pattern files: $PATTERN_FILES"

# Proactive suggestions based on context
HOUR=$(date '+%H')
if [ $HOUR -lt 6 ]; then
    echo "🌙 Late night detected - good time for deep technical work"
elif [ $HOUR -gt 18 ]; then
    echo "🌆 Evening session - consider wrapping up or planning tomorrow"
else
    echo "☀️ Day time session - optimal for collaborative work"
fi

echo "🚀 Enhanced intelligence system active"