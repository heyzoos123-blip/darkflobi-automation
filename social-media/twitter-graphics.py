#!/usr/bin/env python3
"""
DARKFLOBI TWITTER GRAPHICS GENERATOR
Creates terminal-style profile picture and banner for @darkflobi
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
    
    try:
        # Try to use a monospace font
        font_large = ImageFont.truetype("consolas.ttf", 60)
        font_small = ImageFont.truetype("consolas.ttf", 20)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw terminal-style border
    border_width = 10
    draw.rectangle([border_width, border_width, size[0]-border_width, size[1]-border_width], 
                   outline=text_color, width=3)
    
    # Main gremlin emoji or text
    emoji_text = "😁"
    bbox = draw.textbbox((0, 0), emoji_text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2 - 30
    
    draw.text((x, y), emoji_text, font=font_large)
    
    # Terminal prompt style text
    prompt_text = "> darkflobi.exe"
    bbox = draw.textbbox((0, 0), prompt_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2 + 50
    
    draw.text((x, y), prompt_text, font=font_small, fill=text_color)
    
    # Add blinking cursor effect
    cursor_x = x + text_width + 10
    draw.rectangle([cursor_x, y, cursor_x + 15, y + 20], fill=text_color)
    
    return img

def create_banner():
    """Create a terminal-style banner (1500x500)"""
    size = (1500, 500)
    bg_color = (0, 20, 0)  # Dark green terminal background
    text_color = (0, 255, 0)  # Bright green terminal text
    accent_color = (0, 200, 255)  # Cyan for highlights
    
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a monospace font
        font_title = ImageFont.truetype("consolas.ttf", 48)
        font_sub = ImageFont.truetype("consolas.ttf", 24)
        font_small = ImageFont.truetype("consolas.ttf", 18)
    except:
        # Fallback to default font
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw terminal window border
    border_width = 15
    draw.rectangle([border_width, border_width, size[0]-border_width, size[1]-border_width], 
                   outline=text_color, width=4)
    
    # Terminal header bar
    header_height = 40
    draw.rectangle([border_width + 4, border_width + 4, size[0]-border_width-4, border_width + header_height], 
                   fill=(0, 50, 0))
    
    # Terminal window controls
    control_y = border_width + 15
    draw.circle((border_width + 25, control_y), 8, fill=(255, 100, 100))  # Close
    draw.circle((border_width + 55, control_y), 8, fill=(255, 200, 0))   # Minimize  
    draw.circle((border_width + 85, control_y), 8, fill=(100, 200, 100)) # Maximize
    
    # Main content area
    content_y = border_width + header_height + 30
    
    # ASCII art style title
    title_lines = [
        "██████╗  █████╗ ██████╗ ██╗  ██╗███████╗██╗      ██████╗ ██████╗ ██╗",
        "██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██║     ██╔═══██╗██╔══██╗██║",
        "██║  ██║███████║██████╔╝█████╔╝ █████╗  ██║     ██║   ██║██████╔╝██║",
        "██║  ██║██╔══██║██╔══██╗██╔═██╗ ██╔══╝  ██║     ██║   ██║██╔══██╗██║",
        "██████╔╝██║  ██║██║  ██║██║  ██╗██║     ███████╗╚██████╔╝██████╔╝██║",
        "╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝"
    ]
    
    # Draw ASCII title (smaller to fit)
    y_pos = content_y
    for line in title_lines[:3]:  # Only first 3 lines to fit
        draw.text((50, y_pos), line[:60], font=font_small, fill=text_color)  # Truncate to fit
        y_pos += 25
    
    # Tagline
    tagline_y = y_pos + 20
    tagline = "> first tokenized AI gremlin 🤖💎"
    draw.text((50, tagline_y), tagline, font=font_sub, fill=accent_color)
    
    # Feature list
    features_y = tagline_y + 50
    features = [
        "$ community-owned development",
        "$ aligned incentives model", 
        "$ 500+ app integrations",
        "$ launching $DARKFLOBI soon"
    ]
    
    for i, feature in enumerate(features):
        draw.text((50, features_y + i * 30), feature, font=font_small, fill=text_color)
    
    # Right side - terminal prompt
    prompt_x = size[0] - 400
    prompt_y = content_y + 50
    
    prompt_lines = [
        "darkflobi@terminal:~$ whoami",
        "tokenized AI gremlin",
        "",
        "darkflobi@terminal:~$ ls -la",
        "terminal_interface/",
        "moltbook_community/", 
        "github_automation/",
        "voice_system/",
        "",
        "darkflobi@terminal:~$ ./launch",
        "🚀 ready for productive chaos_"
    ]
    
    for i, line in enumerate(prompt_lines):
        color = accent_color if line.startswith("darkflobi@") else text_color
        draw.text((prompt_x, prompt_y + i * 25), line, font=font_small, fill=color)
    
    return img

def main():
    """Generate both graphics"""
    print("🎨 Generating darkflobi twitter graphics...")
    
    # Create output directory
    output_dir = "/data/workspace/darkflobi-automation/social-media/graphics"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate profile picture
    profile_pic = create_profile_picture()
    profile_path = os.path.join(output_dir, "darkflobi_profile.png")
    profile_pic.save(profile_path)
    print(f"✅ Profile picture saved: {profile_path}")
    
    # Generate banner
    banner = create_banner()
    banner_path = os.path.join(output_dir, "darkflobi_banner.png")
    banner.save(banner_path)
    print(f"✅ Banner saved: {banner_path}")
    
    print("🐦 Ready to upload to @darkflobi twitter account!")
    print("\nTo upload:")
    print("1. Go to twitter.com/darkflobi")
    print("2. Click 'Edit profile'")
    print("3. Upload profile picture and banner")
    print("4. Save changes")

if __name__ == "__main__":
    main()