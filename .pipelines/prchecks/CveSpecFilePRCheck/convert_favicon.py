#!/usr/bin/env python3
"""
Temporary script to convert radar_web_logo.png to SVG favicon.
This creates an optimized SVG that embeds the PNG as base64 at a small size.
"""

import base64
import os
from PIL import Image

def png_to_svg_favicon(input_png, output_svg, favicon_size=32):
    """
    Convert PNG to SVG favicon by:
    1. Resizing PNG to favicon_size x favicon_size
    2. Embedding resized PNG as base64 in SVG
    """
    print(f"Converting {input_png} to {output_svg}...")
    
    # Load and resize the PNG
    img = Image.open(input_png)
    print(f"Original size: {img.size}")
    
    # Resize to favicon size maintaining aspect ratio
    img.thumbnail((favicon_size, favicon_size), Image.Resampling.LANCZOS)
    print(f"Resized to: {img.size}")
    
    # Save resized PNG to temp file
    temp_png = "temp_favicon.png"
    img.save(temp_png, optimize=True)
    
    # Read resized PNG and convert to base64
    with open(temp_png, 'rb') as f:
        png_data = base64.b64encode(f.read()).decode('utf-8')
    
    # Create SVG with embedded PNG
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{favicon_size}" height="{favicon_size}" viewBox="0 0 {favicon_size} {favicon_size}">
  <image width="{favicon_size}" height="{favicon_size}" xlink:href="data:image/png;base64,{png_data}"/>
</svg>'''
    
    # Write SVG
    with open(output_svg, 'w') as f:
        f.write(svg_content)
    
    # Cleanup
    os.remove(temp_png)
    
    # Show file sizes
    original_size = os.path.getsize(input_png)
    svg_size = os.path.getsize(output_svg)
    print(f"\nOriginal PNG: {original_size:,} bytes ({original_size/1024:.1f} KB)")
    print(f"SVG favicon: {svg_size:,} bytes ({svg_size/1024:.1f} KB)")
    print(f"Reduction: {100 * (1 - svg_size/original_size):.1f}%")
    print(f"\nSVG favicon created: {output_svg}")

def create_optimized_png_favicon(input_png, output_png, favicon_size=32):
    """
    Create optimized PNG favicon by resizing to small dimensions.
    """
    print(f"\nCreating optimized PNG favicon...")
    
    img = Image.open(input_png)
    img.thumbnail((favicon_size, favicon_size), Image.Resampling.LANCZOS)
    img.save(output_png, optimize=True, format='PNG')
    
    original_size = os.path.getsize(input_png)
    png_size = os.path.getsize(output_png)
    print(f"Original PNG: {original_size:,} bytes ({original_size/1024:.1f} KB)")
    print(f"Optimized PNG: {png_size:,} bytes ({png_size/1024:.1f} KB)")
    print(f"Reduction: {100 * (1 - png_size/original_size):.1f}%")
    print(f"\nPNG favicon created: {output_png}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, 'assets')
    
    input_png = os.path.join(assets_dir, 'radar_web_logo.png')
    output_svg = os.path.join(assets_dir, 'radar_favicon.svg')
    output_png = os.path.join(assets_dir, 'radar_favicon.png')
    
    if not os.path.exists(input_png):
        print(f"Error: {input_png} not found!")
        exit(1)
    
    # Create both SVG and PNG versions
    print("=" * 60)
    print("FAVICON CONVERSION")
    print("=" * 60)
    
    png_to_svg_favicon(input_png, output_svg, favicon_size=32)
    print()
    create_optimized_png_favicon(input_png, output_png, favicon_size=32)
    
    print("\n" + "=" * 60)
    print("Done! You can now use either:")
    print(f"  - SVG: {output_svg}")
    print(f"  - PNG: {output_png}")
    print("=" * 60)
