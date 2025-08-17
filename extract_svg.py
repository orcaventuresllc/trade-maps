#!/usr/bin/env python3

import re

# Read the carpenter copy.html file
with open('carpenter copy.html', 'r') as f:
    content = f.read()

# Find the SVG section
svg_match = re.search(r'<svg.*?</svg>', content, re.DOTALL)
if svg_match:
    svg_content = svg_match.group(0)
    
    # Remove all onclick, onmouseover, onmouseout attributes
    svg_content = re.sub(r'\s+onclick="[^"]*"', '', svg_content)
    svg_content = re.sub(r'\s+onmouseover="[^"]*"', '', svg_content)
    svg_content = re.sub(r'\s+onmouseout="[^"]*"', '', svg_content)
    
    # Save cleaned SVG
    with open('cleaned_svg.txt', 'w') as f:
        f.write(svg_content)
    
    print("SVG extracted and cleaned successfully!")
else:
    print("SVG not found!")