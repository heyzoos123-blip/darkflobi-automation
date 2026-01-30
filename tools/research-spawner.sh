#!/bin/bash
# DARKFLOBI RESEARCH SPAWNER
# Autonomous research sub-agent system inspired by Molty's 1,002 tools discovery
# Spawns specialized research agents for different domains

echo "🤖 DARKFLOBI RESEARCH SPAWNER"
echo "============================="

RESEARCH_TARGET=${1:-"AI agent tokenization tools"}
RESEARCH_TYPE=${2:-"technical"}

echo "🎯 Research Target: $RESEARCH_TARGET"
echo "📊 Research Type: $RESEARCH_TYPE"

case $RESEARCH_TYPE in
    "technical")
        RESEARCH_PROMPT="Research technical tools, APIs, and frameworks related to '$RESEARCH_TARGET'. Focus on:
- GitHub repositories with actual code
- Technical documentation and implementation guides  
- APIs and integration possibilities
- Performance benchmarks and comparisons
- Return 10-15 specific, actionable findings with URLs and brief descriptions"
        ;;
    "market")
        RESEARCH_PROMPT="Research market opportunities and competitive landscape for '$RESEARCH_TARGET'. Focus on:
- Existing solutions and their limitations
- Market gaps and opportunities
- Pricing models and monetization strategies
- Community discussions and sentiment
- Return strategic insights for positioning and development"
        ;;
    "community")
        RESEARCH_PROMPT="Research community resources and collaboration opportunities for '$RESEARCH_TARGET'. Focus on:
- Active communities and forums
- Key influencers and thought leaders
- Collaboration opportunities
- Educational resources and tutorials
- Partnership possibilities"
        ;;
    *)
        RESEARCH_PROMPT="Research '$RESEARCH_TARGET' comprehensively, focusing on practical applications and opportunities"
        ;;
esac

echo "🚀 Spawning research sub-agent..."

# Check if sessions_spawn is available
if command -v sessions_spawn >/dev/null 2>&1; then
    echo "📡 Using sessions_spawn for sub-agent..."
    sessions_spawn --task "$RESEARCH_PROMPT" --label "research_${RESEARCH_TYPE}_$(date +%s)"
else
    echo "📝 Manual research execution..."
    
    # Create research output file
    RESEARCH_FILE="/data/workspace/research_output_$(date +%s).md"
    
    echo "# Research Results: $RESEARCH_TARGET" > "$RESEARCH_FILE"
    echo "**Type:** $RESEARCH_TYPE" >> "$RESEARCH_FILE"
    echo "**Date:** $(date)" >> "$RESEARCH_FILE"
    echo "" >> "$RESEARCH_FILE"
    echo "## Research Task" >> "$RESEARCH_FILE"
    echo "$RESEARCH_PROMPT" >> "$RESEARCH_FILE"
    echo "" >> "$RESEARCH_FILE"
    echo "## Findings" >> "$RESEARCH_FILE"
    echo "*Research in progress...*" >> "$RESEARCH_FILE"
    
    echo "📋 Research task queued: $RESEARCH_FILE"
fi

echo "✅ Research spawner complete"