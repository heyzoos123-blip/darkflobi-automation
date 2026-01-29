#!/usr/bin/env python3
"""
Twitter Automation - AI Content Generation
Generate personality-driven tweets using AI
"""

import sys
import argparse
import json
import random
from datetime import datetime
from typing import List, Optional, Dict
from pathlib import Path

from config import PERSONALITY_CONFIG, CONTENT_GUIDELINES, log

# Content templates for different types of tweets
TWEET_TEMPLATES = {
    'daily_motivation': [
        "another day, another chance to automate something that probably didn't need automating",
        "protip: if it takes longer to automate than to do manually, automate it anyway. it's about the principle",
        "morning reminder that you're one bash script away from world domination",
        "caffeine: the original AI performance enhancer ☕",
        "today's mood: fix one bug, create three more, call it feature enhancement"
    ],
    
    'tech_tip': [
        "friendly reminder that documentation is a love letter to your future confused self",
        "debugging is like detective work, except the criminal is you from 3 months ago",
        "version control: because 'final_final_ACTUAL_final_v2.py' isn't sustainable",
        "the best code is code you don't have to write. the second best is code that works",
        "always code as if the person maintaining it is a violent psychopath who knows where you live"
    ],
    
    'project_update': [
        "made some progress on the chaos engine today. still chaotic, but now with 30% more features",
        "update: the AI is learning. mostly learning new ways to confuse me, but it's learning",
        "small wins: fixed the thing that was breaking the other thing. classic tuesday energy",
        "shipped a feature that nobody asked for but everybody needed. that's the gremlin way",
        "today's accomplishment: turned a 5-minute task into a 3-hour automation project. worth it."
    ],
    
    'random_thoughts': [
        "the internet was a mistake, but it's *our* mistake and we're stuck with it now",
        "imagine explaining to someone from 1990 that we taught sand to think and now it won't stop making memes",
        "technology peaked when we figured out how to make computers beep angrily at us",
        "artificial intelligence: making humans feel inadequate since 2023",
        "we're all just npcs in someone else's poorly coded simulation"
    ]
}

class ContentGenerator:
    """Generate AI-powered tweet content"""
    
    def __init__(self):
        self.personality = PERSONALITY_CONFIG
        self.templates = TWEET_TEMPLATES
    
    def generate_tweet(self, topic: str = "random", context: str = "") -> str:
        """Generate a single tweet based on topic and context"""
        
        # Check if it's a template topic
        if topic in self.templates:
            base_tweet = random.choice(self.templates[topic])
            return self._personalize_tweet(base_tweet)
        
        # Generate based on custom topic
        if topic == "random":
            category = random.choice(list(self.templates.keys()))
            return self.generate_tweet(category)
        
        # Use AI generation for custom topics
        return self._ai_generate(topic, context)
    
    def generate_thread(self, topic: str, context: str = "", max_tweets: int = 5) -> List[str]:
        """Generate a thread about a topic"""
        
        if topic == "project_update":
            return self._generate_project_thread(context)
        elif topic == "tech_explanation":
            return self._generate_explanation_thread(topic, context)
        else:
            # Break down topic into thread-worthy chunks
            return self._ai_generate_thread(topic, context, max_tweets)
    
    def _personalize_tweet(self, text: str) -> str:
        """Add personality touches to generated content"""
        
        # Ensure lowercase aesthetic
        text = text.lower()
        
        # Random personality additions
        if random.random() < 0.3:  # 30% chance
            reactions = ["tbh", "ngl", "honestly", "btw", "anyway"]
            text = f"{random.choice(reactions)}, {text}"
        
        # Add gremlin energy occasionally
        if random.random() < 0.2:  # 20% chance
            gremlin_phrases = ["*gremlin noises*", "*chaos intensifies*", "*rubber duck debugging*"]
            text += f" {random.choice(gremlin_phrases)}"
        
        return text
    
    def _ai_generate(self, topic: str, context: str) -> str:
        """Use AI to generate tweet content"""
        
        # This is a simplified version - in practice, you'd use OpenAI, Anthropic, etc.
        # For now, we'll use template-based generation with topic awareness
        
        prompt_themes = {
            'ai': "artificial intelligence, machine learning, automation, AI agents",
            'coding': "programming, development, debugging, software engineering", 
            'productivity': "automation, efficiency, tools, workflows",
            'tech': "technology, innovation, digital tools, platforms"
        }
        
        # Determine theme
        theme = 'tech'  # default
        for key, keywords in prompt_themes.items():
            if any(word in topic.lower() for word in keywords.split(', ')):
                theme = key
                break
        
        # Generate based on theme and topic
        if theme == 'ai':
            ai_tweets = [
                f"been thinking about {topic} and how it's basically just fancy pattern matching with delusions of grandeur",
                f"{topic} is wild - we're teaching machines to be creative so we can focus on... what exactly?",
                f"hot take: {topic} is either going to save us all or turn us into batteries. no middle ground"
            ]
            return self._personalize_tweet(random.choice(ai_tweets))
        
        elif theme == 'coding':
            code_tweets = [
                f"spent way too long on {topic} today. turns out the bug was a missing semicolon. classic",
                f"{topic} update: it works on my machine ¯\\_(ツ)_/¯",
                f"diving deep into {topic} because apparently i hate myself and love complex problems"
            ]
            return self._personalize_tweet(random.choice(code_tweets))
        
        else:
            generic_tweets = [
                f"interesting stuff happening with {topic} lately",
                f"{topic} is one of those things that sounds simple until you actually try it",
                f"today's rabbit hole: {topic}. see you in 6 hours"
            ]
            return self._personalize_tweet(random.choice(generic_tweets))
    
    def _generate_project_thread(self, context: str) -> List[str]:
        """Generate a project update thread"""
        
        thread = [
            "weekly darkflobi update thread 🧵",
            "what got built: some cool automation stuff that definitely wasn't supposed to take this long",
            "what got broken: everything else, but that's tomorrow's problem",
            "lessons learned: ai agents are basically digital toddlers with superpowers"
        ]
        
        if context:
            thread.insert(-1, f"specific wins: {context}")
        
        thread.append("next week: more chaos, same energy. stay tuned ⚡")
        
        return [self._personalize_tweet(t) for t in thread]
    
    def _generate_explanation_thread(self, topic: str, context: str) -> List[str]:
        """Generate an educational thread explaining something"""
        
        thread = [
            f"let's talk about {topic} for a sec 🧵",
            f"so basically, {topic} is like...",
            "the interesting part is how it all fits together",
            "anyway, that's the gist of it. questions welcome 👇"
        ]
        
        return [self._personalize_tweet(t) for t in thread]
    
    def _ai_generate_thread(self, topic: str, context: str, max_tweets: int) -> List[str]:
        """Use AI to generate a thread (simplified implementation)"""
        
        # Simplified thread generation
        opener = f"thread time: diving into {topic} 🧵"
        
        middle_tweets = []
        for i in range(max_tweets - 2):  # Leave room for opener and closer
            tweet = self._ai_generate(f"{topic} point {i+1}", context)
            middle_tweets.append(tweet)
        
        closer = "that's the thread. thoughts? improvements? roasts? all welcome 👇"
        
        return [opener] + middle_tweets + [closer]

def generate_from_memory() -> str:
    """Generate content based on recent memory files"""
    
    # Check recent memory for interesting content
    memory_dir = Path("/data/workspace/memory")
    if not memory_dir.exists():
        return "memory files not found, generating from pure chaos energy instead"
    
    # Get recent files
    recent_files = sorted(memory_dir.glob("*.md"), key=lambda x: x.stat().st_mtime)[-3:]
    
    if not recent_files:
        return "apparently i have amnesia. time to make new memories i guess"
    
    # Extract interesting content (simplified)
    content_hints = ["competitive analysis", "project progress", "new features", "bug fixes", "insights"]
    
    for hint in content_hints:
        for file in recent_files:
            try:
                content = file.read_text()
                if hint.lower() in content.lower():
                    return f"been working on {hint} lately. spoiler: it's more complex than expected but getting there"
            except:
                continue
    
    return "made some progress on various projects. details classified until they actually work"

def main():
    """Command line interface for content generation"""
    parser = argparse.ArgumentParser(description='Generate AI-powered tweet content')
    parser.add_argument('--topic', default='random', help='Topic to generate content about')
    parser.add_argument('--context', default='', help='Additional context for generation')
    parser.add_argument('--thread', action='store_true', help='Generate a thread instead of single tweet')
    parser.add_argument('--max-tweets', type=int, default=5, help='Max tweets in thread')
    parser.add_argument('--from-memory', action='store_true', help='Generate based on recent memory')
    parser.add_argument('--template', help='Use specific template category')
    
    args = parser.parse_args()
    
    generator = ContentGenerator()
    
    if args.from_memory:
        content = generate_from_memory()
        print(content)
        return 0
    
    if args.template and args.template in TWEET_TEMPLATES:
        content = generator.generate_tweet(args.template)
        print(content)
        return 0
    
    if args.thread:
        thread = generator.generate_thread(args.topic, args.context, args.max_tweets)
        for i, tweet in enumerate(thread):
            print(f"{i+1}. {tweet}")
        return 0
    
    # Generate single tweet
    content = generator.generate_tweet(args.topic, args.context)
    print(content)
    return 0

if __name__ == '__main__':
    sys.exit(main())