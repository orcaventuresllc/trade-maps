#!/usr/bin/env python3

# Read the processed states file
with open('/Users/curranclark/Documents/trade-maps/processed-states.txt', 'r') as f:
    states_svg = f.read()

# Read the working HTML file
with open('/Users/curranclark/Documents/trade-maps/index-working.html', 'r') as f:
    html_lines = f.readlines()

# Find where to insert the SVG (replace the placeholder div)
output_lines = []
skip_section = False

for i, line in enumerate(html_lines):
    # Skip the loadSVGMap function entirely
    if 'function loadSVGMap()' in line:
        skip_section = True
        continue
    
    if skip_section and line.strip() == '}':
        skip_section = False
        continue
        
    if skip_section:
        continue
    
    # Replace the SVG placeholder div with actual SVG
    if '<div id="us-map-svg">' in line:
        output_lines.append('            <div id="us-map-svg">\n')
        output_lines.append('                <svg viewBox="0 0 959 593" xmlns="http://www.w3.org/2000/svg">\n')
        output_lines.append('                    <g class="state">\n')
        # Add all state paths
        for svg_line in states_svg.split('\n'):
            if svg_line.strip():
                output_lines.append('                        ' + svg_line + '\n')
        output_lines.append('                    </g>\n')
        output_lines.append('                </svg>\n')
        # Skip the next two lines (placeholder comment and closing div)
        continue
    
    # Skip the placeholder comment
    if '<!-- Placeholder - will be populated by JavaScript -->' in line:
        continue
        
    # Remove the loadSVGMap() call from initializeMap
    if 'loadSVGMap();' in line:
        continue
        
    output_lines.append(line)

# Write the final file
with open('/Users/curranclark/Documents/trade-maps/index-complete.html', 'w') as f:
    f.writelines(output_lines)

print('Successfully created index-complete.html with direct SVG embedding!')
print('The map should now display correctly with all 50 states visible.')