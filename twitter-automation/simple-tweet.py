#!/usr/bin/env python3
"""
Simple Twitter Content - No External Dependencies
For when we can't install external packages but still want to generate content
"""

import sys
import random
import json
from datetime import datetime

# Simple templates that work without any dependencies
SIMPLE_TEMPLATES = {
    'daily_motivation': [
        "another day, another chance to automate something that probably didn't need automating",
        "protip: if it takes longer to automate than to do manually, automate it anyway. it's about the principle",
        "morning reminder that you're one bash script away from world domination",
        "today's mood: fix one bug, create three more, call it feature enhancement",
        "caffeine: the original ai performance enhancer"
    ],
    
    'tech_tip': [
        "friendly reminder that documentation is a love letter to your future confused self",
        "debugging is like detective work, except the criminal is you from 3 months ago",
        "version control: because 'final_final_actual_final_v2.py' isn't sustainable",
        "the best code is code you don't have to write. the second best is code that works"
    ],
    
    'project_update': [
        "made some progress on the chaos engine today. still chaotic, but now with 30% more features",
        "update: the ai is learning. mostly learning new ways to confuse me, but it's learning",
        "small wins: fixed the thing that was breaking the other thing. classic tuesday energy",
        "shipped a feature that nobody asked for but everybody needed. that's the gremlin way"
    ],
    
    'random_thoughts': [
        "the internet was a mistake, but it's *our* mistake and we're stuck with it now",
        "imagine explaining to someone from 1990 that we taught sand to think and now it won't stop making memes",
        "technology peaked when we figured out how to make computers beep angrily at us",
        "we're all just npcs in someone else's poorly coded simulation"
    ]
}

def add_gremlin_energy(text):
    """Add personality without external dependencies"""
    # lowercase aesthetic
    text = text.lower()
    
    # random gremlin touches
    if random.random() < 0.7:  # 70% chance of emoji
        emojis = ['😁', '🤖', '⚡', '🔥', '💀', '🌙', '🚀', '⚙️']
        text += f" {random.choice(emojis)}"
    
    # occasional hashtags
    if random.random() < 0.5:  # 50% chance
        hashtags = ['#AI', '#automation', '#coding', '#darkflobi', '#tech']
        selected = random.sample(hashtags, min(2, len(hashtags)))
        text += f" {' '.join(selected)}"
    
    return text

def generate_content(template='random'):
    """Generate content using simple templates"""
    if template == 'random':
        template = random.choice(list(SIMPLE_TEMPLATES.keys()))
    
    if template in SIMPLE_TEMPLATES:
        base_text = random.choice(SIMPLE_TEMPLATES[template])
        return add_gremlin_energy(base_text)
    
    # Fallback for unknown templates
    return add_gremlin_energy("just another day building chaos into useful systems")

def create_thread(topic, count=3):
    """Create a simple thread"""
    if topic == 'project_update':
        thread = [
            "weekly darkflobi update thread 🧵",
            "what got built: some cool automation stuff that definitely wasn't supposed to take this long",
            "what got broken: everything else, but that's tomorrow's problem",
            "next week: more chaos, same energy. stay tuned ⚡"
        ]
    else:
        # Generic thread
        thread = [
            f"thread about {topic} 🧵",
            f"so basically, {topic} is pretty wild when you think about it",
            f"anyway, that's my take on {topic}. thoughts?"
        ]
    
    return [add_gremlin_energy(t) for t in thread[:count]]

def save_to_file(content, filename="generated_content.txt"):
    """Save content to file for manual posting"""
    with open(filename, "w") as f:
        if isinstance(content, list):
            for i, item in enumerate(content, 1):
                f.write(f"{i}. {item}\n")
        else:
            f.write(content)
    
    print(f"💾 Content saved to {filename}")
    return filename

def main():
    """Simple CLI for content generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Simple Twitter content generation')
    parser.add_argument('--template', choices=list(SIMPLE_TEMPLATES.keys()) + ['random'], 
                       default='random', help='Content template to use')
    parser.add_argument('--thread', action='store_true', help='Generate thread instead of single tweet')
    parser.add_argument('--count', type=int, default=3, help='Number of tweets in thread')
    parser.add_argument('--save', help='Save to file instead of printing')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    if args.thread:
        content = create_thread(args.template, args.count)
    else:
        content = generate_content(args.template)
    
    if args.save:
        save_to_file(content, args.save)
        return
    
    if args.json:
        result = {
            'content': content,
            'template': args.template,
            'generated_at': datetime.now().isoformat(),
            'type': 'thread' if args.thread else 'single'
        }
        print(json.dumps(result, indent=2))
    else:
        if isinstance(content, list):
            for i, item in enumerate(content, 1):
                print(f"{i}. {item}")
        else:
            print(content)

if __name__ == '__main__':
    main()