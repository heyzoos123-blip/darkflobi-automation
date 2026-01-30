#!/usr/bin/env python3
"""
DARKFLOBI VOICE DEMO - Generate sample audio right now
"""

import os
import subprocess
import tempfile

def create_gremlin_voice_demo():
    """Create voice demo using system TTS as backup if no API key"""
    
    # Gremlin voice scripts to demo
    demo_lines = [
        "Hey flobi! It's darkflobi here - your digital gremlin is alive and ready to speak!",
        "I've integrated voice across the entire ecosystem - from website announcements to launch celebrations.",
        "When we launch dollar darkflobi on pump dot fun, I'll be announcing every milestone with authentic gremlin energy!",
        "The community is going to love having the first tokenized AI that actually talks back.",
        "Four AM energy meets voice integration - productive chaos at maximum volume! Let's dominate!"
    ]
    
    print("🎙️ DARKFLOBI VOICE DEMO")
    print("======================")
    
    # Check for ElevenLabs API key first
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if api_key:
        print("✅ ElevenLabs API key found - using premium voice")
        try:
            # Try ElevenLabs integration
            from elevenlabs import generate, save
            for i, line in enumerate(demo_lines):
                print(f"🎙️ Generating: {line[:50]}...")
                audio = generate(
                    text=line,
                    voice="Adam",  # Energetic, clear voice
                    model="eleven_monolingual_v1"
                )
                filename = f"audio/demo_{i+1}.mp3"
                save(audio, filename)
                print(f"✅ Saved: {filename}")
            print("\n🎉 Premium voice demo generated!")
            return True
        except Exception as e:
            print(f"⚠️ ElevenLabs error: {e}")
            print("💡 Falling back to system TTS...")
    
    # Fallback to system TTS for immediate demo
    print("🔧 Using system TTS for immediate demo...")
    
    # Create demo audio directory
    os.makedirs("audio", exist_ok=True)
    
    try:
        # Try different TTS systems based on what's available
        tts_commands = [
            # macOS
            ["say", "-v", "Alex", "-o", "audio/demo_system.aiff"],
            # Linux with espeak
            ["espeak", "-s", "150", "-p", "40", "-w", "audio/demo_system.wav"],
            # Linux with festival  
            ["text2wave", "-o", "audio/demo_system.wav"],
        ]
        
        demo_text = " ".join(demo_lines[:2])  # First 2 lines for system demo
        
        for cmd_base in tts_commands:
            try:
                cmd = cmd_base.copy()
                if cmd[0] == "say":
                    cmd.append(demo_text)
                else:
                    # For other TTS, we need to pipe the text
                    process = subprocess.run(
                        cmd,
                        input=demo_text,
                        text=True,
                        capture_output=True
                    )
                    if process.returncode == 0:
                        print(f"✅ Generated with {cmd[0]}: audio/demo_system.*")
                        print_demo_info()
                        return True
                        
            except FileNotFoundError:
                continue
                
        # If no system TTS works, create text demo
        print("📝 No TTS system found - creating text demo...")
        with open("audio/voice_demo.txt", "w") as f:
            f.write("🎙️ DARKFLOBI VOICE PREVIEW\n")
            f.write("==========================\n\n")
            for i, line in enumerate(demo_lines, 1):
                f.write(f"{i}. {line}\n\n")
            f.write("🤖 Gremlin Voice Characteristics:\n")
            f.write("• Energetic but authentic tone\n")
            f.write("• Says 'dollar darkflobi' (not symbol)\n") 
            f.write("• Slightly faster pace for productive chaos\n")
            f.write("• Natural pauses and genuine excitement\n")
            f.write("• Lowercase energy maintained in speech\n\n")
            f.write("💡 Get ElevenLabs API key to hear actual gremlin voice!\n")
            f.write("   Visit: https://elevenlabs.io/ (FREE tier available)\n")
        
        print("✅ Voice preview saved to: audio/voice_demo.txt")
        print_demo_info()
        return True
        
    except Exception as e:
        print(f"❌ Demo creation failed: {e}")
        return False

def print_demo_info():
    """Show user how to access the demo"""
    print("\n🎯 HOW TO HEAR THE GREMLIN VOICE:")
    print("================================")
    print("1. 🎧 IMMEDIATE: Check audio/ folder for generated files")
    print("2. 🌐 WEBSITE: Voice toggle on https://heyzoos123-blip.github.io/darkflobi-industries/")
    print("3. 🔑 PREMIUM: Get free ElevenLabs API key for authentic gremlin voice")
    print("4. 🚀 LAUNCH: Voice will announce all token milestones live!")
    print()
    print("💰 COST BREAKDOWN:")
    print("   • FREE: 10,000 characters/month (covers all launch content)")
    print("   • $5/month: 30,000 characters (daily automation)")
    print()
    print("🤖 VOICE FEATURES READY:")
    print("   ✅ GitHub milestone announcements")
    print("   ✅ Token launch celebrations")  
    print("   ✅ Website voice toggle")
    print("   ✅ Gremlin personality in speech")

if __name__ == "__main__":
    create_gremlin_voice_demo()