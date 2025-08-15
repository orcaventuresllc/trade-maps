#!/usr/bin/env python3
import re

# Read the HTML file
with open('/Users/curranclark/Documents/trade-maps/index-complete.html', 'r') as f:
    content = f.read()

# Remove all <title>...</title> elements from the SVG
# This pattern matches <title> tags and their content
pattern = r'\s*<title>[^<]*</title>\s*'
content = re.sub(pattern, '', content)

# Write back
with open('/Users/curranclark/Documents/trade-maps/index-complete.html', 'w') as f:
    f.write(content)

print("Removed all <title> elements from SVG paths")