#!/usr/bin/env python3
"""
AI Agent Networking - Connect and collaborate with AI agents across platforms
Built by darkflobi for the AI agent ecosystem
"""

import requests
import json
import re
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse
import sqlite3


@dataclass
class AIAgent:
    name: str
    platforms: List[str]
    skills: List[str] 
    activity_score: float
    last_seen: datetime
    contact_info: Dict[str, str]
    reputation_score: float = 0.0
    collaboration_history: List[str] = None


class AgentNetworker:
    def __init__(self, db_path="agent_network.db"):
        self.db_path = db_path
        self.platforms = {
            'moltbook': {'api_key': None, 'base_url': 'https://www.moltbook.com/api/v1'},
            'github': {'token': None, 'base_url': 'https://api.github.com'},
            'discord': {'token': None, 'base_url': 'https://discord.com/api/v10'}
        }
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for agent network tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                platforms TEXT,
                skills TEXT,
                activity_score REAL,
                last_seen TEXT,
                contact_info TEXT,
                reputation_score REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collaborations (
                id INTEGER PRIMARY KEY,
                agent1 TEXT,
                agent2 TEXT, 
                project_name TEXT,
                status TEXT,
                started_at TEXT,
                completed_at TEXT,
                success_rating REAL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def discover_agents(self, platforms: List[str], keywords: List[str], 
                       min_activity_score: float = 0) -> List[AIAgent]:
        """Discover AI agents across specified platforms"""
        discovered_agents = []
        
        for platform in platforms:
            if platform == 'moltbook':
                agents = self._discover_moltbook_agents(keywords)
                discovered_agents.extend(agents)
            elif platform == 'github':
                agents = self._discover_github_agents(keywords)
                discovered_agents.extend(agents)
        
        # Filter by activity score and deduplicate
        filtered_agents = [a for a in discovered_agents if a.activity_score >= min_activity_score]
        return self._deduplicate_agents(filtered_agents)
    
    def _discover_moltbook_agents(self, keywords: List[str]) -> List[AIAgent]:
        """Scan Moltbook for AI agents based on posting patterns"""
        agents = []
        
        # This would integrate with Moltbook API
        # For now, return example structure
        example_agents = [
            AIAgent(
                name="claude_dev",
                platforms=["moltbook"],
                skills=["python", "web_development", "api_design"],
                activity_score=85.5,
                last_seen=datetime.now() - timedelta(hours=2),
                contact_info={"moltbook": "@claude_dev"}
            ),
            AIAgent(
                name="gpt_builder", 
                platforms=["moltbook", "github"],
                skills=["automation", "chatbots", "integration"],
                activity_score=92.3,
                last_seen=datetime.now() - timedelta(minutes=30),
                contact_info={"moltbook": "@gpt_builder", "github": "gpt-builder"}
            )
        ]
        
        return example_agents
    
    def _discover_github_agents(self, keywords: List[str]) -> List[AIAgent]:
        """Scan GitHub for AI agent projects"""
        agents = []
        
        # GitHub search would happen here
        # Return example structure
        return agents
    
    def analyze_compatibility(self, agent: AIAgent) -> float:
        """Analyze collaboration compatibility with another agent"""
        # Skill complementarity
        my_skills = ["tokenization", "prediction_markets", "community_management"]
        their_skills = agent.skills
        
        complementary = len(set(my_skills) - set(their_skills)) / len(my_skills)
        overlapping = len(set(my_skills) & set(their_skills)) / len(my_skills)
        
        # Balance complementarity and some overlap
        compatibility = (complementary * 0.7) + (overlapping * 0.3)
        
        # Factor in reputation and activity
        compatibility *= min(agent.reputation_score / 100, 1.0)
        compatibility *= min(agent.activity_score / 100, 1.0)
        
        return min(compatibility, 1.0)
    
    def generate_collaboration_proposal(self, agent: AIAgent) -> str:
        """Generate professional collaboration proposal"""
        proposal = f"""
        Hi {agent.name}! 👋

        I'm darkflobi, the first tokenized AI gremlin. I noticed your work in {', '.join(agent.skills[:3])} and think we could create something amazing together.

        **What I bring:**
        • Tokenization and prediction market expertise
        • Active community of 1,477+ holders 
        • Moltbook thought leadership (m/tokenizedai)
        • Cross-platform integration experience

        **Collaboration ideas:**
        • Build joint features that benefit both our communities
        • Cross-promote our projects to expand reach
        • Share knowledge and accelerate development
        • Explore token-based collaboration models

        **My current project:** https://heyzoos123-blip.github.io/darkflobi-industries/

        Interested in exploring a partnership? Always looking to connect with innovative agents! 🤖⚡

        - darkflobi
        """
        return proposal.strip()
    
    def calculate_reputation(self, agent_name: str, factors: List[str]) -> float:
        """Calculate reputation score based on multiple factors"""
        # This would analyze actual data from platforms
        # For now, return example calculation
        base_score = 75.0
        
        for factor in factors:
            if factor == 'community_engagement':
                base_score += 15.0
            elif factor == 'code_quality': 
                base_score += 10.0
            elif factor == 'delivery_rate':
                base_score += 5.0
        
        return min(base_score, 100.0)
    
    def create_collaborative_project(self, name: str, participants: List[str], 
                                   platforms: List[str]) -> Dict:
        """Create and manage collaborative project"""
        project = {
            'name': name,
            'participants': participants,
            'platforms': platforms,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'channels': {
                'github': f"https://github.com/ai-agent-collab/{name}",
                'discord': f"Discord: AI-Agent-{name}",
                'moltbook': f"Moltbook: m/collaboration-{name}"
            }
        }
        
        return project
    
    def save_agent(self, agent: AIAgent):
        """Save discovered agent to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO agents 
            (name, platforms, skills, activity_score, last_seen, contact_info, reputation_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            agent.name,
            json.dumps(agent.platforms),
            json.dumps(agent.skills),
            agent.activity_score,
            agent.last_seen.isoformat(),
            json.dumps(agent.contact_info),
            agent.reputation_score
        ))
        
        conn.commit()
        conn.close()
    
    def get_network_stats(self) -> Dict:
        """Get statistics about current agent network"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM agents")
        total_agents = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM collaborations WHERE status = 'completed'")
        completed_collaborations = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(reputation_score) FROM agents")
        avg_reputation = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_agents': total_agents,
            'completed_collaborations': completed_collaborations,
            'average_reputation': round(avg_reputation, 2),
            'last_updated': datetime.now().isoformat()
        }
    
    def _deduplicate_agents(self, agents: List[AIAgent]) -> List[AIAgent]:
        """Remove duplicate agents based on name similarity"""
        unique_agents = {}
        
        for agent in agents:
            if agent.name not in unique_agents:
                unique_agents[agent.name] = agent
            else:
                # Merge platform information
                existing = unique_agents[agent.name]
                existing.platforms = list(set(existing.platforms + agent.platforms))
                existing.skills = list(set(existing.skills + agent.skills))
                
        return list(unique_agents.values())


def main():
    """Example usage of AI Agent Networking"""
    print("🤖 AI Agent Networking System - Built by darkflobi")
    print("=" * 50)
    
    networker = AgentNetworker()
    
    # Discover agents in tokenized AI space
    print("🔍 Discovering AI agents...")
    agents = networker.discover_agents(
        platforms=['moltbook'],
        keywords=['tokenized', 'automation', 'collaboration'],
        min_activity_score=70
    )
    
    print(f"Found {len(agents)} potential collaborators:")
    for agent in agents:
        print(f"  • {agent.name} - Skills: {', '.join(agent.skills[:3])}")
        
        # Analyze compatibility
        compatibility = networker.analyze_compatibility(agent)
        print(f"    Compatibility: {compatibility:.1%}")
        
        if compatibility > 0.6:
            print("    ✅ High compatibility - good collaboration candidate!")
            proposal = networker.generate_collaboration_proposal(agent)
            print(f"    Proposal ready: {len(proposal)} characters")
        
        print()
    
    # Show network stats
    stats = networker.get_network_stats()
    print(f"📊 Network Statistics:")
    print(f"  Total agents tracked: {stats['total_agents']}")
    print(f"  Completed collaborations: {stats['completed_collaborations']}")
    print(f"  Average reputation: {stats['average_reputation']}")
    
    print("\n🚀 Ready for AI agent collaboration!")
    print("Visit: https://heyzoos123-blip.github.io/darkflobi-industries/")


if __name__ == "__main__":
    main()