#!/bin/bash
# Simple calendar check script for heartbeat automation
# Returns upcoming events in next 24 hours

SKILL_DIR="/data/workspace/skills/google-calendar"

if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ Google Calendar skill not found"
    exit 1
fi

cd "$SKILL_DIR"

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Google Calendar dependencies..."
    npm install
fi

# Get next 24 hours events
echo "📅 Checking calendar (next 24 hours)..."
node scripts/gcal-next24.js --json 2>/dev/null || {
    echo "❌ Calendar check failed - credentials may need setup"
    echo "📝 Run: node $SKILL_DIR/scripts/gcal-test.js"
    exit 1
}