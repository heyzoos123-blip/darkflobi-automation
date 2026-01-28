#!/bin/bash
# darkflobi-status.sh - Quick system status with personality 😁

echo "$(cat /data/workspace/darkflobi-terminal-logo.txt | head -6)"
echo ""
echo "🤖 darkflobi system status • $(date '+%H:%M UTC')"
echo "═════════════════════════════════════════════"

# System basics
echo "💻 system:"
echo "  disk: $(df -h /data | tail -1 | awk '{print $5}') used"
echo "  memory: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100}') used" 
echo ""

# Project status
echo "📊 projects:"
if [ -d "/data/workspace" ]; then
    echo "  workspace: active"
    echo "  memory files: $(find /data/workspace/memory -name "*.md" 2>/dev/null | wc -l)"
    echo "  scripts: $(find /data/workspace/scripts -name "*.sh" 2>/dev/null | wc -l)"
else
    echo "  workspace: not found"
fi
echo ""

# Recent activity (last 24h)
echo "📝 recent activity:"
if [ -f "/data/workspace/memory/$(date +%Y-%m-%d).md" ]; then
    echo "  today's log: active"
    lines=$(wc -l < "/data/workspace/memory/$(date +%Y-%m-%d).md")
    echo "  entries: $lines lines"
else
    echo "  today's log: not started"
fi
echo ""

# Weather (if available)
echo "🌤️ nyc weather:"
if command -v curl >/dev/null 2>&1; then
    curl -s "https://wttr.in/New+York?format=%l:+%c+%t+%h+→%w" 2>/dev/null || echo "  weather data unavailable"
else
    echo "  curl not available"
fi
echo ""

echo "───────────────────────────────────────────"
echo "😁 build mode: ACTIVE • hype level: ZERO"
echo "   $(whoami) ready to continue building"