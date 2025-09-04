#!/usr/bin/env python3
"""
Create a simple app icon for Android File Transfer
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    # Create a 512x512 image with a blue background
    size = 512
    img = Image.new('RGBA', (size, size), (59, 130, 246, 255))  # Blue background
    draw = ImageDraw.Draw(img)
    
    # Draw a phone icon
    phone_width = 200
    phone_height = 300
    phone_x = (size - phone_width) // 2
    phone_y = (size - phone_height) // 2
    
    # Phone body
    draw.rounded_rectangle(
        [phone_x, phone_y, phone_x + phone_width, phone_y + phone_height],
        radius=30,
        fill=(255, 255, 255, 255),
        outline=(0, 0, 0, 255),
        width=4
    )
    
    # Phone screen
    screen_margin = 20
    draw.rounded_rectangle(
        [phone_x + screen_margin, phone_y + screen_margin + 40, 
         phone_x + phone_width - screen_margin, phone_y + phone_height - screen_margin],
        radius=20,
        fill=(59, 130, 246, 255)
    )
    
    # Screen content - simple grid
    grid_size = 40
    for i in range(3):
        for j in range(2):
            x = phone_x + screen_margin + 20 + j * (grid_size + 10)
            y = phone_y + screen_margin + 60 + i * (grid_size + 10)
            draw.rectangle([x, y, x + grid_size, y + grid_size], fill=(255, 255, 255, 200))
    
    # Arrow pointing up (transfer)
    arrow_x = phone_x + phone_width + 20
    arrow_y = phone_y + phone_height // 2
    arrow_points = [
        (arrow_x, arrow_y - 20),
        (arrow_x + 20, arrow_y),
        (arrow_x + 15, arrow_y + 5),
        (arrow_x + 15, arrow_y + 15),
        (arrow_x + 5, arrow_y + 15),
        (arrow_x + 5, arrow_y + 5)
    ]
    draw.polygon(arrow_points, fill=(255, 255, 255, 255))
    
    # Computer icon
    comp_width = 120
    comp_height = 80
    comp_x = arrow_x + 40
    comp_y = arrow_y - comp_height // 2
    
    # Computer body
    draw.rectangle([comp_x, comp_y, comp_x + comp_width, comp_y + comp_height], 
                   fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=3)
    
    # Computer screen
    draw.rectangle([comp_x + 10, comp_y + 10, comp_x + comp_width - 10, comp_y + comp_height - 10], 
                   fill=(59, 130, 246, 255))
    
    # Save the icon
    icon_path = "AndroidFileTransfer.app/Contents/Resources/icon.png"
    img.save(icon_path)
    
    # Create different sizes for the app bundle
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for s in sizes:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(f"AndroidFileTransfer.app/Contents/Resources/icon_{s}x{s}.png")
    
    print(f"App icon created: {icon_path}")
    return icon_path

if __name__ == "__main__":
    try:
        create_app_icon()
    except ImportError:
        print("PIL (Pillow) not available. Creating a simple text-based icon instead.")
        # Fallback: create a simple text file
        with open("AndroidFileTransfer.app/Contents/Resources/icon.png", "w") as f:
            f.write("# Simple icon placeholder")
