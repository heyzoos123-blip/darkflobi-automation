#!/usr/bin/env python3
"""
DARKFLOBI Token Logo Generator
Creates a 512x512 PNG logo for pump.fun deployment
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

def create_darkflobi_logo():
    # Create 512x512 image with dark background
    size = 512
    img = Image.new('RGBA', (size, size), (10, 10, 10, 255))
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = size // 2, size // 2 - 40
    
    # Add subtle tech grid pattern
    grid_color = (26, 26, 26, 100)
    for i in range(0, size, 32):
        draw.line([(i, 0), (i, size)], fill=grid_color, width=1)
        draw.line([(0, i), (size, i)], fill=grid_color, width=1)
    
    # Create glow effect background
    glow_radius = 150
    for r in range(glow_radius, 0, -5):
        alpha = max(0, min(50, int(50 * (glow_radius - r) / glow_radius)))
        glow_color = (0, 255, 136, alpha)
        draw.ellipse([
            center_x - r, center_y - r,
            center_x + r, center_y + r
        ], fill=glow_color)
    
    # Main character background circle
    main_radius = 120
    draw.ellipse([
        center_x - main_radius, center_y - main_radius,
        center_x + main_radius, center_y + main_radius
    ], fill=(26, 26, 26, 255), outline=(0, 255, 136, 255), width=3)
    
    # Gremlin head
    head_width, head_height = 80, 85
    draw.ellipse([
        center_x - head_width, center_y - head_height - 10,
        center_x + head_width, center_y + head_height - 10
    ], fill=(42, 42, 42, 255))
    
    # Gremlin ears (pointed)
    ear_color = (42, 42, 42, 255)
    inner_ear_color = (0, 255, 136, 255)
    
    # Left ear
    draw.polygon([
        (center_x - 65, center_y - 40),
        (center_x - 95, center_y - 80),
        (center_x - 45, center_y - 60)
    ], fill=ear_color)
    draw.polygon([
        (center_x - 60, center_y - 45),
        (center_x - 75, center_y - 65),
        (center_x - 50, center_y - 55)
    ], fill=inner_ear_color)
    
    # Right ear
    draw.polygon([
        (center_x + 65, center_y - 40),
        (center_x + 95, center_y - 80),
        (center_x + 45, center_y - 60)
    ], fill=ear_color)
    draw.polygon([
        (center_x + 60, center_y - 45),
        (center_x + 75, center_y - 65),
        (center_x + 50, center_y - 55)
    ], fill=inner_ear_color)
    
    # Eyes (large, mischievous)
    eye_color = (0, 255, 136, 255)
    pupil_color = (10, 10, 10, 255)
    highlight_color = (255, 255, 255, 255)
    
    # Left eye
    draw.ellipse([
        center_x - 45, center_y - 50,
        center_x - 5, center_y
    ], fill=eye_color)
    draw.ellipse([
        center_x - 33, center_y - 32,
        center_x - 17, center_y - 8
    ], fill=pupil_color)
    draw.ellipse([
        center_x - 25, center_y - 29,
        center_x - 19, center_y - 21
    ], fill=highlight_color)
    
    # Right eye
    draw.ellipse([
        center_x + 5, center_y - 50,
        center_x + 45, center_y
    ], fill=eye_color)
    draw.ellipse([
        center_x + 17, center_y - 32,
        center_x + 33, center_y - 8
    ], fill=pupil_color)
    draw.ellipse([
        center_x + 19, center_y - 29,
        center_x + 25, center_y - 21
    ], fill=highlight_color)
    
    # Grinning mouth
    mouth_color = (0, 255, 136, 255)
    draw.arc([
        center_x - 25, center_y - 5,
        center_x + 25, center_y + 45
    ], start=10, end=170, fill=mouth_color, width=4)
    
    # Teeth for the grin
    tooth_color = (255, 255, 255, 255)
    for i in range(5):
        x = center_x - 20 + (i * 8)
        y = center_y + 20
        draw.rectangle([x, y, x + 4, y + 8], fill=tooth_color)
    
    # Circuit decorations around the character
    circuit_color = (0, 255, 136, 255)
    for i in range(8):
        angle = (i / 8) * 2 * math.pi
        x1 = center_x + math.cos(angle) * 140
        y1 = center_y + math.sin(angle) * 140
        x2 = center_x + math.cos(angle) * 160
        y2 = center_y + math.sin(angle) * 160
        
        draw.line([(x1, y1), (x2, y2)], fill=circuit_color, width=2)
        draw.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=circuit_color)
    
    # Add digital noise effect
    for _ in range(100):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        alpha = random.randint(10, 25)
        draw.point((x, y), fill=(0, 255, 136, alpha))
    
    # Try to load a font, fallback to default if not available
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except:
        try:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        except:
            title_font = None
            subtitle_font = None
    
    # Token name
    if title_font:
        # Get text size for centering
        bbox = draw.textbbox((0, 0), "DARKFLOBI", font=title_font)
        text_width = bbox[2] - bbox[0]
        text_x = (size - text_width) // 2
        
        draw.text((text_x, 380), "DARKFLOBI", fill=(255, 255, 255, 255), font=title_font)
    else:
        draw.text((center_x - 60, 380), "DARKFLOBI", fill=(255, 255, 255, 255))
    
    # Subtitle
    if subtitle_font:
        bbox = draw.textbbox((0, 0), "AI CEO TOKEN", font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        text_x = (size - text_width) // 2
        
        draw.text((text_x, 430), "AI CEO TOKEN", fill=(0, 255, 136, 255), font=subtitle_font)
    else:
        draw.text((center_x - 50, 430), "AI CEO TOKEN", fill=(0, 255, 136, 255))
    
    return img

def main():
    print("🎨 Creating DARKFLOBI logo...")
    
    # Generate the logo
    logo = create_darkflobi_logo()
    
    # Save as PNG
    output_path = "/data/workspace/darkflobi_logo_512x512.png"
    logo.save(output_path, "PNG", optimize=True)
    
    print(f"✅ Logo saved to: {output_path}")
    print(f"📏 Size: 512x512 pixels")
    print(f"📋 Format: PNG with transparency")
    print(f"🚀 Ready for pump.fun deployment!")

if __name__ == "__main__":
    main()