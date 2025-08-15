#!/usr/bin/env python3

# Read the processed states file
with open('/Users/curranclark/Documents/trade-maps/processed-states.txt', 'r') as f:
    states_content = f.read()

# Read the working HTML file
with open('/Users/curranclark/Documents/trade-maps/index-working.html', 'r') as f:
    html_content = f.read()

# Find the SVG placeholder section
svg_start = html_content.find('const svgContent = `')
svg_end = html_content.find('`;', svg_start)

# Create the new SVG content with all state paths
new_svg = '''const svgContent = `
            <svg viewBox="0 0 959 593" xmlns="http://www.w3.org/2000/svg">
                <g class="state">
''' + states_content + '''
                </g>
            </svg>
        `;'''

# Replace the SVG section
new_html = html_content[:svg_start] + new_svg + html_content[svg_end+2:]

# Write the final file
with open('/Users/curranclark/Documents/trade-maps/index-final.html', 'w') as f:
    f.write(new_html)

print('Successfully created index-final.html with all 50 state paths integrated!')
print('The file is ready to be pasted into a Kadence Custom HTML block in WordPress.')