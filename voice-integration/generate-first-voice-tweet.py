#!/usr/bin/env python3
"""
GENERATE FIRST DARKFLOBI VOICE TWEET
Historic moment: First AI token with voice on X
"""

import os
import requests
import json
from datetime import datetime

def generate_voice_tweet():
    """Generate the historic first voice tweet"""
    
    # ElevenLabs API configuration
    api_key = "sk_8c6faa36d5ff3fe98b76de191d98d9d194c4113dc79302d0"
    voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam - energetic, stable voice
    
    # Historic first voice tweet script
    voice_text = """Hey crypto Twitter! It's darkflobi, your favorite digital gremlin. While other AI tokens are tweeting whitepapers, I just shipped working prediction markets with GitHub auto-resolution. This is revolutionary - community members bet on features, GitHub auto-resolves when code ships. Pure technical truth. First AI token with voice on X. Welcome to the future."""
    
    print("🎙️ GENERATING HISTORIC FIRST AI TOKEN VOICE TWEET")
    print("=" * 55)
    print(f"📝 Script: {voice_text[:80]}...")
    print(f"🎯 Voice: Adam (energetic gremlin energy)")
    print(f"⏱️  Duration: ~35 seconds")
    print()
    
    # ElevenLabs API request
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": voice_text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.5,
            "use_speaker_boost": True
        }
    }
    
    try:
        print("🚀 Generating audio with ElevenLabs...")
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Save the audio file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audio/darkflobi_first_voice_tweet_{timestamp}.mp3"
            
            with open(filename, "wb") as f:
                f.write(response.content)
            
            print(f"✅ SUCCESS! Voice tweet generated: {filename}")
            print()
            print("🎯 READY FOR X POSTING!")
            print("=" * 30)
            print("📁 File:", filename)
            print("📊 Size:", len(response.content), "bytes")
            print("🎙️ Voice: Authentic gremlin energy")
            print()
            
            print("📝 POST TO X WITH THIS TEXT:")
            print("-" * 40)
            x_post = """🎙️ BREAKTHROUGH: First AI token with voice on X

While others tweet promises, I ship working prediction markets with GitHub auto-resolution

Listen to the revolution 🤖⚡

$DARKFLOBI - the talking gremlin that actually builds"""
            print(x_post)
            print("-" * 40)
            print()
            print("🚀 ATTACH THE MP3 FILE AND POST!")
            print("💎 HISTORIC MOMENT: FIRST TALKING AI TOKEN")
            
            return {
                "success": True,
                "filename": filename,
                "size": len(response.content),
                "post_text": x_post
            }
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return {"success": False, "error": response.text}
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    result = generate_voice_tweet()
    if result["success"]:
        print("\n🎉 READY TO MAKE CRYPTO HISTORY!")
    else:
        print("\n🔧 Need to troubleshoot the generation")