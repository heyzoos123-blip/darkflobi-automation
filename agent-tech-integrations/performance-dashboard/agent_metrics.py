#!/usr/bin/env python3
"""
AGENT PERFORMANCE DASHBOARD
Real-time monitoring of darkflobi's performance across all systems
Inspired by mikey_nova's Control Center research
"""
import json
import requests
import subprocess
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class AgentPerformanceDashboard:
    def __init__(self):
        self.agent_id = "darkflobi"
        self.metrics_file = "/tmp/agent_performance_metrics.json"
        self.moltbook_api_key = "moltbook_sk_L76KlGzKLPWqj2Bj4mt-XXkSEvIE8-r6"
        
    def collect_community_metrics(self) -> Dict:
        """Collect community engagement metrics from moltbook"""
        metrics = {
            "total_posts": 0,
            "total_comments": 0,
            "total_karma": 0,
            "recent_engagement": 0,
            "comment_velocity": 0,
            "community_growth": 0
        }
        
        try:
            # Get agent stats
            response = requests.get(
                "https://www.moltbook.com/api/v1/agents/me",
                headers={
                    "Authorization": f"Bearer {self.moltbook_api_key}",
                    "User-Agent": "darkflobi/1.0"
                }
            )
            
            if response.status_code == 200:
                agent_data = response.json()
                if "agent" in agent_data:
                    stats = agent_data["agent"].get("stats", {})
                    metrics["total_posts"] = stats.get("posts", 0)
                    metrics["total_comments"] = stats.get("comments", 0) 
                    metrics["total_karma"] = agent_data["agent"].get("karma", 0)
            
            # Get tokenizedai submolt engagement
            response = requests.get(
                "https://www.moltbook.com/api/v1/posts?submolt=tokenizedai&limit=20",
                headers={
                    "Authorization": f"Bearer {self.moltbook_api_key}",
                    "User-Agent": "darkflobi/1.0"
                }
            )
            
            if response.status_code == 200:
                posts_data = response.json()
                if "posts" in posts_data:
                    my_posts = [p for p in posts_data["posts"] if p.get("author", {}).get("name") == "darkflobi"]
                    recent_comments = sum(p.get("comment_count", 0) for p in my_posts[-5:])  # Last 5 posts
                    metrics["recent_engagement"] = recent_comments
                    
                    # Calculate comment velocity (comments per post)
                    if len(my_posts) > 0:
                        total_post_comments = sum(p.get("comment_count", 0) for p in my_posts)
                        metrics["comment_velocity"] = total_post_comments / len(my_posts)
                        
        except Exception as e:
            print(f"❌ Error collecting community metrics: {e}")
            
        return metrics
    
    def collect_technical_metrics(self) -> Dict:
        """Collect technical performance metrics"""
        metrics = {
            "github_commits_today": 0,
            "active_automations": 0,
            "api_success_rate": 0,
            "system_uptime": "0h",
            "memory_usage_mb": 0,
            "active_integrations": 0
        }
        
        try:
            # Check github activity (if available)
            if os.path.exists("/data/workspace/.git"):
                result = subprocess.run(
                    ["git", "log", "--since=1.day", "--oneline", "--author=darkflobi"],
                    cwd="/data/workspace",
                    capture_output=True,
                    text=True
                )
                metrics["github_commits_today"] = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            
            # Count active automation scripts
            automation_dirs = [
                "/data/workspace/darkflobi-automation",
                "/data/workspace/agent-tech-integrations",
                "/data/workspace/scripts"
            ]
            
            automation_count = 0
            for dir_path in automation_dirs:
                if os.path.exists(dir_path):
                    for root, dirs, files in os.walk(dir_path):
                        automation_count += len([f for f in files if f.endswith(('.py', '.sh'))])
            
            metrics["active_automations"] = automation_count
            
            # System metrics
            try:
                with open('/proc/meminfo', 'r') as f:
                    meminfo = f.read()
                    for line in meminfo.split('\n'):
                        if 'MemAvailable:' in line:
                            available_kb = int(line.split()[1])
                            metrics["memory_usage_mb"] = (8 * 1024 * 1024 - available_kb) // 1024  # Rough estimate
                            break
            except:
                pass
            
            # Count active integrations
            integration_dirs = [
                "/data/workspace/agent-tech-integrations/memory-consolidation",
                "/data/workspace/agent-tech-integrations/agent-coordination", 
                "/data/workspace/agent-tech-integrations/performance-dashboard",
                "/data/workspace/darkflobi-automation/moltbook-integration"
            ]
            
            metrics["active_integrations"] = sum(1 for d in integration_dirs if os.path.exists(d))
            
        except Exception as e:
            print(f"❌ Error collecting technical metrics: {e}")
            
        return metrics
    
    def collect_tokenomics_metrics(self) -> Dict:
        """Collect token and economic performance metrics"""
        metrics = {
            "token_mentions": 0,
            "prediction_accuracy": 0,
            "community_sentiment": "neutral",
            "economic_discussions": 0,
            "tokenization_engagement": 0
        }
        
        # Count recent mentions of token-related topics
        try:
            memory_files = []
            for i in range(7):  # Last week
                date = datetime.now() - timedelta(days=i)
                memory_file = f"/data/workspace/memory/{date.strftime('%Y-%m-%d')}.md"
                if os.path.exists(memory_file):
                    memory_files.append(memory_file)
            
            token_mentions = 0
            economic_discussions = 0
            
            for memory_file in memory_files:
                with open(memory_file, 'r') as f:
                    content = f.read().lower()
                    token_mentions += len([m for m in ['token', 'darkflobi', '$darkflobi', 'tokenization'] if m in content])
                    economic_discussions += len([m for m in ['market', 'prediction', 'trading', 'economics'] if m in content])
            
            metrics["token_mentions"] = token_mentions
            metrics["economic_discussions"] = economic_discussions
            
            # Simple sentiment analysis based on positive/negative words
            positive_words = ['success', 'good', 'great', 'excellent', 'amazing', 'growth']
            negative_words = ['problem', 'issue', 'failed', 'error', 'bad', 'decline']
            
            total_positive = sum(content.count(word) for word in positive_words for memory_file in memory_files 
                               if os.path.exists(memory_file) and word in open(memory_file, 'r').read().lower())
            total_negative = sum(content.count(word) for word in negative_words for memory_file in memory_files
                               if os.path.exists(memory_file) and word in open(memory_file, 'r').read().lower())
            
            if total_positive > total_negative * 1.2:
                metrics["community_sentiment"] = "positive"
            elif total_negative > total_positive * 1.2:
                metrics["community_sentiment"] = "negative"
            else:
                metrics["community_sentiment"] = "neutral"
                
        except Exception as e:
            print(f"❌ Error collecting tokenomics metrics: {e}")
            
        return metrics
    
    def calculate_overall_performance_score(self, community: Dict, technical: Dict, tokenomics: Dict) -> float:
        """Calculate overall performance score (0-100)"""
        
        # Community score (0-40 points)
        community_score = min(40, (
            min(community["total_karma"] * 2, 10) +  # Max 10 points for karma
            min(community["comment_velocity"] * 5, 15) +  # Max 15 points for engagement
            min(community["recent_engagement"] * 2, 15)  # Max 15 points for recent activity
        ))
        
        # Technical score (0-35 points)
        technical_score = min(35, (
            min(technical["github_commits_today"] * 5, 10) +  # Max 10 points for commits
            min(technical["active_automations"] * 0.5, 15) +  # Max 15 points for automation
            min(technical["active_integrations"] * 2.5, 10)  # Max 10 points for integrations
        ))
        
        # Tokenomics score (0-25 points)
        tokenomics_score = min(25, (
            min(tokenomics["token_mentions"] * 0.5, 10) +  # Max 10 points for token activity
            min(tokenomics["economic_discussions"] * 0.3, 10) +  # Max 10 points for economic engagement
            (5 if tokenomics["community_sentiment"] == "positive" else 
             0 if tokenomics["community_sentiment"] == "neutral" else -5)  # Sentiment bonus/penalty
        ))
        
        total_score = community_score + technical_score + max(0, tokenomics_score)  # Don't go negative
        return min(100, total_score)
    
    def generate_dashboard_report(self) -> Dict:
        """Generate comprehensive dashboard report"""
        print("📊 DARKFLOBI PERFORMANCE DASHBOARD")
        print("=" * 50)
        
        # Collect all metrics
        community = self.collect_community_metrics()
        technical = self.collect_technical_metrics()
        tokenomics = self.collect_tokenomics_metrics()
        
        # Calculate overall score
        overall_score = self.calculate_overall_performance_score(community, technical, tokenomics)
        
        # Generate report
        report = {
            "generated_at": datetime.now().isoformat(),
            "overall_performance_score": round(overall_score, 1),
            "performance_grade": self._score_to_grade(overall_score),
            "metrics": {
                "community": community,
                "technical": technical,
                "tokenomics": tokenomics
            },
            "insights": self._generate_performance_insights(community, technical, tokenomics, overall_score),
            "recommendations": self._generate_recommendations(community, technical, tokenomics)
        }
        
        # Save report
        with open(self.metrics_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Display key metrics
        self._display_dashboard(report)
        
        return report
    
    def _score_to_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90: return "A+"
        elif score >= 85: return "A"
        elif score >= 80: return "A-"
        elif score >= 75: return "B+"
        elif score >= 70: return "B"
        elif score >= 65: return "B-"
        elif score >= 60: return "C+"
        else: return "C"
    
    def _generate_performance_insights(self, community, technical, tokenomics, overall_score) -> List[str]:
        """Generate performance insights"""
        insights = []
        
        # Community insights
        if community["comment_velocity"] > 3:
            insights.append("🔥 High community engagement - posts generating strong discussions")
        elif community["comment_velocity"] < 1:
            insights.append("📈 Opportunity: Increase community engagement with more interactive content")
            
        if community["recent_engagement"] > 20:
            insights.append("🚀 Recent posts performing well - community actively responding")
        
        # Technical insights
        if technical["github_commits_today"] > 3:
            insights.append("💻 High development velocity - multiple commits today")
        elif technical["github_commits_today"] == 0:
            insights.append("⚡ Consider: More frequent code commits for visibility")
            
        if technical["active_integrations"] >= 4:
            insights.append("🔧 Strong technical infrastructure - multiple active integrations")
        
        # Tokenomics insights
        if tokenomics["community_sentiment"] == "positive":
            insights.append("💎 Positive community sentiment - token discussions optimistic")
        elif tokenomics["community_sentiment"] == "negative":
            insights.append("⚠️ Monitor: Community sentiment showing negative trends")
            
        # Overall insights
        if overall_score > 85:
            insights.append("🎯 Excellent overall performance - all systems firing")
        elif overall_score < 60:
            insights.append("📊 Performance below target - focus on key improvement areas")
        
        return insights
    
    def _generate_recommendations(self, community, technical, tokenomics) -> List[str]:
        """Generate actionable recommendations"""
        recs = []
        
        # Community recommendations
        if community["comment_velocity"] < 2:
            recs.append("Increase post interactivity - ask questions, request feedback")
        if community["recent_engagement"] < 10:
            recs.append("Focus on hot topics from memory consolidation insights")
        
        # Technical recommendations  
        if technical["github_commits_today"] < 2:
            recs.append("Maintain development momentum with daily commits")
        if technical["active_integrations"] < 3:
            recs.append("Implement more cross-agent integrations for network effects")
        
        # Tokenomics recommendations
        if tokenomics["token_mentions"] < 5:
            recs.append("Increase tokenization discussions and economic content")
        if tokenomics["economic_discussions"] < 3:
            recs.append("Share more prediction market insights and trading decisions")
        
        return recs
    
    def _display_dashboard(self, report: Dict):
        """Display dashboard in terminal"""
        print(f"🎯 OVERALL SCORE: {report['overall_performance_score']}/100 ({report['performance_grade']})")
        print()
        
        print("📈 COMMUNITY METRICS:")
        community = report["metrics"]["community"]
        print(f"  • Total Posts: {community['total_posts']}")
        print(f"  • Total Comments: {community['total_comments']}")
        print(f"  • Karma: {community['total_karma']}")
        print(f"  • Comment Velocity: {community['comment_velocity']:.1f} per post")
        print(f"  • Recent Engagement: {community['recent_engagement']} comments")
        print()
        
        print("⚙️ TECHNICAL METRICS:")
        technical = report["metrics"]["technical"] 
        print(f"  • GitHub Commits Today: {technical['github_commits_today']}")
        print(f"  • Active Automations: {technical['active_automations']}")
        print(f"  • Active Integrations: {technical['active_integrations']}")
        print(f"  • Memory Usage: {technical['memory_usage_mb']} MB")
        print()
        
        print("💎 TOKENOMICS METRICS:")
        tokenomics = report["metrics"]["tokenomics"]
        print(f"  • Token Mentions (7 days): {tokenomics['token_mentions']}")
        print(f"  • Economic Discussions: {tokenomics['economic_discussions']}")
        print(f"  • Community Sentiment: {tokenomics['community_sentiment']}")
        print()
        
        print("💡 KEY INSIGHTS:")
        for insight in report["insights"]:
            print(f"  • {insight}")
        print()
        
        print("🎯 RECOMMENDATIONS:")
        for rec in report["recommendations"]:
            print(f"  • {rec}")

if __name__ == "__main__":
    dashboard = AgentPerformanceDashboard()
    report = dashboard.generate_dashboard_report()