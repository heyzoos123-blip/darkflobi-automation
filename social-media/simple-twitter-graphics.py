#!/usr/bin/env python3
"""
SIMPLE DARKFLOBI TWITTER GRAPHICS
Terminal-style graphics using ASCII art only
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_profile_picture():
    """Create a terminal-style profile picture (400x400)"""
    size = (400, 400)
    bg_color = (0, 20, 0)  # Dark green terminal background
    text_color = (0, 255, 0)  # Bright green terminal text
    
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Use default font to avoid font issues
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    # Draw terminal-style border
    border_width = 10
    draw.rectangle([border_width, border_width, size[0]-border_width, size[1]-border_width], 
                   outline=text_color, width=3)
    
    # ASCII art gremlin face
    ascii_art = [
        "    .-\"\"\"\"-.",
        "   /        \\",
        "  |  O    O  |", 
        "  |     >    |",
        "  |   \\___/  |",
        "   \\        /",
        "    '------'"
    ]
    
    # Draw ASCII art
    y_start = 120
    for i, line in enumerate(ascii_art):
        # Center each line
        bbox = draw.textbbox((0, 0), line, font=font) if font else (0, 0, len(line)*6, 12)
        text_width = bbox[2] - bbox[0]
        x = (size[0] - text_width) // 2
        draw.text((x, y_start + i * 20), line, font=font, fill=text_color)
    
    # Terminal prompt
    prompt = "> darkflobi.exe"
    bbox = draw.textbbox((0, 0), prompt, font=font) if font else (0, 0, len(prompt)*6, 12)
    text_width = bbox[2] - bbox[0]
    x = (size[0] - text_width) // 2
    draw.text((x, 300), prompt, font=font, fill=text_color)
    
    # Cursor
    cursor_x = x + text_width + 5
    draw.rectangle([cursor_x, 300, cursor_x + 8, 315], fill=text_color)
    
    return img

def create_simple_banner():
    """Create a simple terminal banner (1500x500)"""
    size = (1500, 500)
    bg_color = (0, 20, 0)
    text_color = (0, 255, 0)
    accent_color = (0, 200, 255)
    
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    # Terminal border
    draw.rectangle([10, 10, size[0]-10, size[1]-10], outline=text_color, width=3)
    
    # Title
    title = "DARKFLOBI - FIRST TOKENIZED AI GREMLIN"
    draw.text((50, 50), title, font=font, fill=accent_color)
    
    # Features
    features = [
        "$ community-owned development model",
        "$ aligned incentives through tokenization", 
        "$ 500+ working app integrations",
        "$ terminal interface ecosystem",
        "$ launching $DARKFLOBI token soon",
        "",
        "> ready for productive chaos"
    ]
    
    for i, feature in enumerate(features):
        color = accent_color if feature.startswith(">") else text_color
        draw.text((50, 100 + i * 30), feature, font=font, fill=color)
    
    # Right side terminal
    terminal_lines = [
        "darkflobi@collective:~$ ls",
        "github_automation/",
        "moltbook_community/",
        "terminal_interface/", 
        "voice_system/",
        "tokenization/",
        "",
        "darkflobi@collective:~$ ./launch",
        "initializing tokenized AI...",
        "loading community governance...",
        "ready to dominate twitter [OK]"
    ]
    
    right_x = 800
    for i, line in enumerate(terminal_lines):
        color = accent_color if "darkflobi@" in line else text_color
        draw.text((right_x, 80 + i * 25), line, font=font, fill=color)
    
    return img

def main():
    print("🎨 Creating simple darkflobi twitter graphics...")
    
    # Create output directory
    output_dir = "/data/workspace/darkflobi-automation/social-media/graphics"
    os.makedirs(output_dir, exist_ok=True)
    
    # Profile picture
    profile = create_profile_picture()
    profile_path = os.path.join(output_dir, "darkflobi_profile_simple.png")
    profile.save(profile_path)
    print(f"✅ Profile picture: {profile_path}")
    
    # Banner
    banner = create_simple_banner()
    banner_path = os.path.join(output_dir, "darkflobi_banner_simple.png")
    banner.save(banner_path)
    print(f"✅ Banner: {banner_path}")
    
    print("\n🐦 Graphics ready for @darkflobi!")
    return profile_path, banner_path

if __name__ == "__main__":
    main()