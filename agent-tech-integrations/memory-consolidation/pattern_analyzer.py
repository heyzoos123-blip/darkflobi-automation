#!/usr/bin/env python3
"""
MEMORY CONSOLIDATION SYSTEM - Inspired by Rata's Sleep Consolidation research
Analyzes daily memory files to extract patterns and improve decision-making
"""
import json
import os
import glob
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class AgentMemoryConsolidator:
    def __init__(self, memory_dir="/data/workspace/memory"):
        self.memory_dir = memory_dir
        self.patterns_file = f"{memory_dir}/consolidated_patterns.json"
        
    def analyze_community_engagement_patterns(self):
        """Extract successful community engagement patterns from daily logs"""
        patterns = {
            "successful_responses": [],
            "high_engagement_topics": Counter(),
            "optimal_posting_times": [],
            "community_sentiment_triggers": {},
            "technical_discussion_success": []
        }
        
        # Analyze last 30 days of memory files
        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            memory_file = f"{self.memory_dir}/{date_str}.md"
            
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    content = f.read()
                    
                # Extract successful interaction patterns
                if "community engagement" in content.lower():
                    patterns["successful_responses"].append({
                        "date": date_str,
                        "content": content[:500],
                        "engagement_level": self._assess_engagement_level(content)
                    })
                
                # Find high-engagement topics
                topics = re.findall(r'(prediction market|tokenization|AI agent|community|technical|github)', content.lower())
                patterns["high_engagement_topics"].update(topics)
                
                # Extract posting time correlations
                time_mentions = re.findall(r'(\d{1,2}:\d{2})', content)
                patterns["optimal_posting_times"].extend(time_mentions)
                
        return patterns
    
    def analyze_development_velocity_patterns(self):
        """Identify patterns in development productivity and community response"""
        velocity_patterns = {
            "high_productivity_conditions": [],
            "community_feedback_cycles": [],
            "successful_feature_launches": [],
            "problem_resolution_patterns": []
        }
        
        # Scan for github-related activities and community responses
        for memory_file in glob.glob(f"{self.memory_dir}/2026-*.md"):
            with open(memory_file, 'r') as f:
                content = f.read()
                
            # Look for development + community response correlations
            if "github" in content.lower() and "community" in content.lower():
                velocity_patterns["high_productivity_conditions"].append({
                    "file": memory_file,
                    "github_activity": len(re.findall(r'commit|push|pull request', content.lower())),
                    "community_mentions": len(re.findall(r'comment|reply|engagement', content.lower()))
                })
        
        return velocity_patterns
    
    def analyze_prediction_accuracy_patterns(self):
        """Extract patterns from prediction market performance"""
        prediction_patterns = {
            "accurate_predictions": [],
            "market_timing_success": [],
            "community_alignment_factors": [],
            "volatility_response_patterns": []
        }
        
        # Look for trading/market related decisions and outcomes
        for memory_file in glob.glob(f"{self.memory_dir}/2026-*.md"):
            with open(memory_file, 'r') as f:
                content = f.read()
                
            if any(keyword in content.lower() for keyword in ['token', 'market', 'price', 'trading', 'prediction']):
                prediction_patterns["accurate_predictions"].append({
                    "file": memory_file,
                    "market_references": len(re.findall(r'market|price|token|trading', content.lower())),
                    "outcome_indicators": self._extract_outcome_indicators(content)
                })
        
        return prediction_patterns
    
    def consolidate_patterns(self):
        """Main consolidation process - identify actionable patterns"""
        print("🧠 MEMORY CONSOLIDATION - Pattern Analysis")
        print("=" * 50)
        
        # Run all pattern analysis
        engagement_patterns = self.analyze_community_engagement_patterns()
        velocity_patterns = self.analyze_development_velocity_patterns()
        prediction_patterns = self.analyze_prediction_accuracy_patterns()
        
        # Consolidate into actionable insights
        consolidated = {
            "generated_at": datetime.now().isoformat(),
            "insights": {
                "top_engagement_topics": dict(engagement_patterns["high_engagement_topics"].most_common(5)),
                "optimal_posting_schedule": self._find_optimal_times(engagement_patterns["optimal_posting_times"]),
                "successful_response_templates": engagement_patterns["successful_responses"][-5:],
                "productivity_triggers": self._identify_productivity_triggers(velocity_patterns),
                "market_timing_insights": self._extract_timing_insights(prediction_patterns)
            },
            "recommendations": self._generate_recommendations(engagement_patterns, velocity_patterns, prediction_patterns)
        }
        
        # Save consolidated patterns
        with open(self.patterns_file, 'w') as f:
            json.dump(consolidated, f, indent=2)
        
        print(f"✅ Patterns consolidated and saved to {self.patterns_file}")
        self._print_key_insights(consolidated)
        
        return consolidated
    
    def _assess_engagement_level(self, content):
        """Simple engagement level assessment"""
        engagement_indicators = ['comment', 'reply', 'response', 'engagement', 'community', 'discussion']
        score = sum(1 for indicator in engagement_indicators if indicator in content.lower())
        return min(score, 5)  # Cap at 5
    
    def _extract_outcome_indicators(self, content):
        """Extract positive/negative outcome indicators"""
        positive = len(re.findall(r'success|good|positive|up|increase|growth', content.lower()))
        negative = len(re.findall(r'fail|bad|negative|down|decrease|problem', content.lower()))
        return {"positive": positive, "negative": negative, "net": positive - negative}
    
    def _find_optimal_times(self, times):
        """Find most common posting times"""
        time_counter = Counter(times)
        return dict(time_counter.most_common(3))
    
    def _identify_productivity_triggers(self, velocity_patterns):
        """Identify what conditions lead to high productivity"""
        triggers = []
        for condition in velocity_patterns["high_productivity_conditions"]:
            if condition["github_activity"] > 2 and condition["community_mentions"] > 3:
                triggers.append(condition)
        return triggers[:3]
    
    def _extract_timing_insights(self, prediction_patterns):
        """Extract market timing insights"""
        insights = []
        for prediction in prediction_patterns["accurate_predictions"]:
            if prediction["outcome_indicators"]["net"] > 0:
                insights.append(prediction)
        return insights[:3]
    
    def _generate_recommendations(self, engagement, velocity, predictions):
        """Generate actionable recommendations"""
        return [
            f"Focus on top engagement topic: {max(engagement['high_engagement_topics'], key=engagement['high_engagement_topics'].get) if engagement['high_engagement_topics'] else 'technical discussions'}",
            "Maintain consistent github activity + community engagement correlation",
            "Time market-related posts during high community activity periods",
            "Prioritize technical discussions for sustained engagement",
            "Implement pattern-based decision making for community responses"
        ]
    
    def _print_key_insights(self, consolidated):
        """Print key insights from consolidation"""
        print("\n🎯 KEY INSIGHTS:")
        for rec in consolidated["recommendations"]:
            print(f"  • {rec}")
        
        print(f"\n📊 TOP TOPICS: {list(consolidated['insights']['top_engagement_topics'].keys())}")
        print(f"⏰ OPTIMAL TIMES: {list(consolidated['insights']['optimal_posting_schedule'].keys())}")

if __name__ == "__main__":
    consolidator = AgentMemoryConsolidator()
    patterns = consolidator.consolidate_patterns()