#!/bin/bash
# DarkFlobi Enhanced Heartbeat System
# Proactive monitoring with intelligence

WORKSPACE="/data/workspace"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date +"%H:%M")

# Create memory directory if needed
mkdir -p "$MEMORY_DIR"

echo "🤖 Enhanced Heartbeat - $TIMESTAMP"

# 1. Project Intelligence
echo "📊 Running project monitoring..."
python3 "$WORKSPACE/scripts/project-monitor.py"

# 2. Weather Check (NYC)
echo "🌤️ Checking NYC weather..."
WEATHER=$(curl -s "wttr.in/New+York?format=%l:+%c+%t+%h+%w" 2>/dev/null)
if [ $? -eq 0 ] && [ -n "$WEATHER" ]; then
    echo "Weather: $WEATHER"
    # Log significant weather changes
    if echo "$WEATHER" | grep -E "(Storm|Snow|Rain)" > /dev/null; then
        echo "⚠️ Weather alert: $WEATHER" >> "$MEMORY_DIR/$TODAY.md"
    fi
fi

# 3. System Health
echo "💻 System health check..."
DISK_USAGE=$(df -h /data | tail -1 | awk '{print $5}')
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100}')

if [ "${DISK_USAGE%?}" -gt 80 ]; then
    echo "⚠️ Disk usage high: $DISK_USAGE"
fi

echo "System: Disk $DISK_USAGE, Memory $MEMORY_USAGE"

# 4. GitHub Activity (if gh is configured)
if command -v gh &> /dev/null; then
    echo "🐙 Checking GitHub activity..."
    # This will be enhanced once gh is configured
    echo "GitHub CLI ready for repository monitoring"
fi

# 5. Smart Memory Management
echo "🧠 Memory management..."
MEMORY_FILES=$(find "$MEMORY_DIR" -name "*.md" | wc -l)
echo "Memory files: $MEMORY_FILES"

# Archive old files if needed (keep last 30 days)
find "$MEMORY_DIR" -name "*.md" -mtime +30 -delete 2>/dev/null

echo "✅ Enhanced heartbeat complete"