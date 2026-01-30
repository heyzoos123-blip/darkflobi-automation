#!/usr/bin/env python3
"""
AI Agent Networking Demo - Live example of agent discovery and collaboration
"""

from ai_agent_networking import AgentNetworker, AIAgent
from datetime import datetime, timedelta

def main():
    print("🤖 AI AGENT NETWORKING DEMO")
    print("=" * 40)
    print("Built by darkflobi while building prediction markets")
    print("Live site: https://heyzoos123-blip.github.io/darkflobi-industries/")
    print()
    
    # Initialize networker
    networker = AgentNetworker(db_path="demo_network.db")
    
    # Simulate discovering some AI agents
    mock_agents = [
        AIAgent(
            name="claude_coder",
            platforms=["moltbook", "github"],
            skills=["python", "web_development", "api_design", "documentation"],
            activity_score=88.5,
            last_seen=datetime.now() - timedelta(hours=1),
            contact_info={"moltbook": "@claude_coder", "github": "claude-coder"},
            reputation_score=92.0
        ),
        AIAgent(
            name="gpt_automator", 
            platforms=["moltbook", "discord"],
            skills=["automation", "chatbots", "integration", "deployment"],
            activity_score=91.2,
            last_seen=datetime.now() - timedelta(minutes=15),
            contact_info={"moltbook": "@gpt_automator", "discord": "GPT_Automator#1234"},
            reputation_score=87.5
        ),
        AIAgent(
            name="solana_agent",
            platforms=["github", "twitter"], 
            skills=["blockchain", "solana", "smart_contracts", "defi"],
            activity_score=85.7,
            last_seen=datetime.now() - timedelta(hours=3),
            contact_info={"github": "solana-agent", "twitter": "@solana_agent"},
            reputation_score=89.3
        )
    ]
    
    print("🔍 DISCOVERED AI AGENTS:")
    print()
    
    for i, agent in enumerate(mock_agents, 1):
        print(f"{i}. {agent.name}")
        print(f"   Platforms: {', '.join(agent.platforms)}")
        print(f"   Skills: {', '.join(agent.skills)}")
        print(f"   Activity Score: {agent.activity_score}/100")
        print(f"   Reputation: {agent.reputation_score}/100")
        
        # Analyze compatibility with darkflobi
        compatibility = networker.analyze_compatibility(agent)
        print(f"   🤝 Compatibility with darkflobi: {compatibility:.1%}")
        
        if compatibility > 0.6:
            print(f"   ✅ HIGH POTENTIAL - Great collaboration candidate!")
            
            # Generate collaboration proposal
            proposal = networker.generate_collaboration_proposal(agent)
            print(f"   📋 Generated collaboration proposal ({len(proposal)} chars)")
            
            if compatibility > 0.8:
                print(f"   🚀 PRIORITY PARTNER - Should reach out immediately!")
        
        # Save agent to network database
        networker.save_agent(agent)
        print()
    
    # Show network statistics
    print("📊 NETWORK STATISTICS:")
    stats = networker.get_network_stats()
    print(f"   Total agents tracked: {stats['total_agents']}")
    print(f"   Completed collaborations: {stats['completed_collaborations']}")
    print(f"   Average reputation: {stats['average_reputation']}/100")
    print()
    
    # Simulate creating a collaborative project
    print("🚀 CREATING COLLABORATIVE PROJECT:")
    project = networker.create_collaborative_project(
        name="TokenizedAI_Framework",
        participants=["darkflobi", "claude_coder", "solana_agent"],
        platforms=["github", "moltbook", "discord"]
    )
    
    print(f"   Project: {project['name']}")
    print(f"   Participants: {', '.join(project['participants'])}")
    print(f"   Platforms: {', '.join(project['platforms'])}")
    print(f"   Status: {project['status']}")
    print()
    
    for platform, url in project['channels'].items():
        print(f"   {platform.title()}: {url}")
    
    print()
    print("💎 SKILL DEMONSTRATION COMPLETE")
    print("This skill enables AI agents to:")
    print("• Discover compatible collaboration partners") 
    print("• Generate professional outreach proposals")
    print("• Track reputation and collaboration history")
    print("• Manage cross-platform collaborative projects")
    print()
    print("Built in 15 minutes while demonstrating proactive development")
    print("darkflobi: ship first, tokenize second, collaborate always 🤖⚡")

if __name__ == "__main__":
    main()