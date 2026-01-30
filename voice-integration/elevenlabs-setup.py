#!/usr/bin/env python3
"""
DARKFLOBI VOICE - ElevenLabs Integration
Cost-effective voice generation for the gremlin ecosystem
"""

import requests
import json
import os
import hashlib
from pathlib import Path

class DarkflobiVoice:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        self.base_url = "https://api.elevenlabs.io/v1"
        
        # Pre-selected voice for darkflobi (energetic but authentic)
        self.voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam - stable, clear, energetic
        
        # Optimized gremlin voice settings
        self.voice_settings = {
            "stability": 0.75,        # Consistent but slight variation
            "similarity_boost": 0.85, # Clear character voice  
            "style": 0.20,           # Subtle style, authentic energy
            "use_speaker_boost": True # Clarity boost
        }
        
        # Create audio directory
        self.audio_dir = Path("audio")
        self.audio_dir.mkdir(exist_ok=True)
        
    def get_voice_info(self):
        """Get available voices and usage info"""
        if not self.api_key:
            return {"error": "No API key provided"}
            
        try:
            # Get voices
            voices_response = requests.get(
                f"{self.base_url}/voices",
                headers={"xi-api-key": self.api_key}
            )
            
            # Get usage info  
            usage_response = requests.get(
                f"{self.base_url}/user",
                headers={"xi-api-key": self.api_key}
            )
            
            return {
                "voices": voices_response.json() if voices_response.ok else {},
                "usage": usage_response.json() if usage_response.ok else {},
                "selected_voice": self.voice_id
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def estimate_cost(self, text: str):
        """Estimate cost for generating voice from text"""
        char_count = len(text)
        
        # ElevenLabs pricing tiers
        pricing = {
            "free": {"limit": 10000, "cost": 0},
            "starter": {"limit": 30000, "cost": 5},  # $5/month
            "growing": {"limit": 100000, "cost": 22}  # $22/month
        }
        
        estimate = {
            "characters": char_count,
            "free_remaining": max(0, pricing["free"]["limit"] - char_count),
            "tier_recommendation": "free" if char_count <= 10000 else "starter",
            "monthly_cost": 0 if char_count <= 10000 else 5
        }
        
        return estimate
    
    def add_gremlin_personality(self, text: str):
        """Process text for authentic gremlin voice"""
        
        # Pronunciation corrections
        text = text.replace("$DARKFLOBI", "dollar darkflobi")
        text = text.replace("DARKFLOBI", "darkflobi")  # Keep lowercase energy
        text = text.replace("GitHub", "git hub")
        text = text.replace("AI", "A I")  # Clearer pronunciation
        
        # Add natural gremlin pauses  
        text = text.replace("honestly,", "honestly... ")
        text = text.replace("basically,", "basically... ")
        text = text.replace("...", " ... pause ... ")
        
        # Emphasis markers for key gremlin words
        gremlin_words = ["legendary", "chaos", "automation", "gremlin", "epic"]
        for word in gremlin_words:
            text = text.replace(word, f"<emphasis>{word}</emphasis>")
            
        return text
    
    def generate_voice(self, text: str, filename: str = None, preview: bool = False):
        """Generate voice audio from text"""
        
        if not self.api_key:
            if preview:
                print("📝 PREVIEW MODE (No API Key)")
                print(f"🎙️ Would generate: '{text[:100]}...'")
                print(f"💰 Estimated cost: {self.estimate_cost(text)}")
                return {"preview": True, "text": text}
            else:
                return {"error": "ElevenLabs API key required"}
        
        # Process text for gremlin personality
        processed_text = self.add_gremlin_personality(text)
        
        # Generate filename if not provided
        if not filename:
            text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
            filename = f"darkflobi_{text_hash}.mp3"
            
        filepath = self.audio_dir / filename
        
        # Check if already generated (save costs)
        if filepath.exists() and not preview:
            return {"cached": True, "filepath": str(filepath)}
        
        try:
            response = requests.post(
                f"{self.base_url}/text-to-speech/{self.voice_id}",
                json={
                    "text": processed_text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": self.voice_settings
                },
                headers={
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": self.api_key
                }
            )
            
            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(response.content)
                    
                return {
                    "success": True,
                    "filepath": str(filepath),
                    "characters": len(text),
                    "processed_text": processed_text
                }
            else:
                return {
                    "error": f"API error: {response.status_code}",
                    "message": response.text
                }
                
        except Exception as e:
            return {"error": str(e)}

# Pre-generated launch content for cost efficiency
LAUNCH_CONTENT = {
    "website_welcome": "gremlin voice activated. ready for productive chaos announcements.",
    
    "github_milestone_100": "incredible! we just hit 100 git hub stars! the darkflobi ecosystem is growing legendary.",
    
    "token_launch": "legendary launch achieved! dollar darkflobi is now live. the first tokenized A I gremlin with real utility is ready for the world. gremlin energy levels maximum.",
    
    "community_milestone": "amazing! our community just hit another milestone. the gremlin army is growing stronger every day.",
    
    "system_update": "darkflobi automation systems upgraded successfully. productivity levels increasing. chaos levels optimal.",
    
    "daily_update": "daily status report: all systems operational, community growing, gremlin energy at maximum efficiency."
}

def setup_voice_system(api_key: str = None, preview_mode: bool = True):
    """Setup and test the darkflobi voice system"""
    
    print("🤖 DARKFLOBI VOICE SETUP")
    print("=" * 40)
    
    voice = DarkflobiVoice(api_key)
    
    if preview_mode or not api_key:
        print("📝 PREVIEW MODE - No costs incurred")
        print()
        
        total_chars = 0
        for name, text in LAUNCH_CONTENT.items():
            result = voice.generate_voice(text, preview=True)
            print(f"🎙️ {name}: {len(text)} characters")
            total_chars += len(text)
            
        print(f"\n📊 TOTAL USAGE: {total_chars} characters")
        
        estimate = voice.estimate_cost(total_chars)
        print(f"💰 COST ESTIMATE: {estimate}")
        
        if total_chars <= 10000:
            print("✅ Fits in FREE tier!")
        elif total_chars <= 30000:
            print("💵 Requires STARTER tier ($5/month)")
        else:
            print("💵 Requires GROWING tier ($22/month)")
            
    else:
        print("🚀 LIVE MODE - Generating audio files")
        
        # Get account info
        info = voice.get_voice_info()
        if "usage" in info:
            print(f"📊 Account usage: {info['usage']}")
            
        # Generate all launch content
        generated = []
        for name, text in LAUNCH_CONTENT.items():
            print(f"🎙️ Generating: {name}...")
            result = voice.generate_voice(text, f"launch_{name}.mp3")
            
            if result.get("success") or result.get("cached"):
                generated.append(result["filepath"])
                print(f"✅ Generated: {result['filepath']}")
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
                
        print(f"\n🎉 Generated {len(generated)} voice files!")
        
    print("\n🎯 SETUP COMPLETE")
    return voice

if __name__ == "__main__":
    # Test the system
    print("🎙️ Testing darkflobi voice system...")
    
    # Check for API key
    api_key = os.getenv('ELEVENLABS_API_KEY')
    
    if api_key:
        print(f"🔑 API key found: {api_key[:10]}...")
        voice = setup_voice_system(api_key, preview_mode=False)
    else:
        print("💡 No API key found - running preview mode")
        print("💡 Set ELEVENLABS_API_KEY environment variable to generate audio")
        voice = setup_voice_system(preview_mode=True)
        
        print("\n🚀 QUICK SETUP INSTRUCTIONS:")
        print("1. Get free API key: https://elevenlabs.io/")  
        print("2. Set environment variable: export ELEVENLABS_API_KEY='your_key'")
        print("3. Run script again to generate voice files")
        print("4. Free tier gives 10,000 characters/month!")