#!/bin/bash
# project-tracker.sh - Track development progress for darkflobi projects 📊

PROJECT_NAME=${1:-"darkflobi_collective"}
LOG_FILE="/data/workspace/memory/project-${PROJECT_NAME}.log"

echo "📊 $PROJECT_NAME development tracker • $(date '+%Y-%m-%d %H:%M UTC')"
echo "═══════════════════════════════════════════════════════════════"

# Function to log progress
log_progress() {
    echo "$(date '+%Y-%m-%d %H:%M UTC') | $1" >> "$LOG_FILE"
    echo "✅ logged: $1"
}

# Function to show recent progress
show_progress() {
    if [ -f "$LOG_FILE" ]; then
        echo "📝 recent progress entries:"
        echo "─────────────────────────────────"
        tail -10 "$LOG_FILE" | while read line; do
            echo "  $line"
        done
        echo ""
        echo "📊 total entries: $(wc -l < "$LOG_FILE")"
    else
        echo "📝 no progress log found - ready to start tracking"
    fi
}

# Function to add milestone
add_milestone() {
    echo "$(date '+%Y-%m-%d %H:%M UTC') | 🎯 MILESTONE: $1" >> "$LOG_FILE"
    echo "🎯 milestone logged: $1"
}

# Main menu
case "${2:-show}" in
    "show"|"status")
        show_progress
        ;;
    "log")
        if [ -z "$3" ]; then
            echo "usage: $0 $PROJECT_NAME log 'your progress note'"
            exit 1
        fi
        log_progress "$3"
        ;;
    "milestone")
        if [ -z "$3" ]; then
            echo "usage: $0 $PROJECT_NAME milestone 'milestone description'"
            exit 1
        fi
        add_milestone "$3"
        ;;
    "revenue")
        # Special tracking for revenue milestones
        if [ -z "$3" ]; then
            echo "usage: $0 $PROJECT_NAME revenue 'amount or update'"
            exit 1
        fi
        log_progress "💰 REVENUE UPDATE: $3"
        ;;
    "stats")
        if [ -f "$LOG_FILE" ]; then
            echo "📊 $PROJECT_NAME statistics:"
            echo "  total entries: $(wc -l < "$LOG_FILE")"
            echo "  milestones: $(grep -c "MILESTONE" "$LOG_FILE")"
            echo "  revenue updates: $(grep -c "REVENUE" "$LOG_FILE")"
            echo "  first entry: $(head -1 "$LOG_FILE" | cut -d'|' -f1)"
            echo "  latest entry: $(tail -1 "$LOG_FILE" | cut -d'|' -f1)"
        else
            echo "📊 no statistics available yet"
        fi
        ;;
    "help")
        echo "🔧 project tracker commands:"
        echo "  show/status    - show recent progress"
        echo "  log 'note'     - add progress entry"
        echo "  milestone 'x'  - add milestone"
        echo "  revenue 'x'    - add revenue update"
        echo "  stats          - show statistics"
        echo ""
        echo "examples:"
        echo "  $0 darkflobi_collective log 'completed user auth system'"
        echo "  $0 darkflobi_collective milestone 'MVP v1.0 released'"
        echo "  $0 darkflobi_collective revenue 'hit \$1000/month target'"
        ;;
    *)
        echo "❌ unknown command: $2"
        echo "use '$0 $PROJECT_NAME help' for usage"
        ;;
esac

echo ""
echo "😁 keep building • track progress • ship features"