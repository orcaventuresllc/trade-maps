import re

# Read the SVG file
with open('/Users/curranclark/Documents/trade-maps/Blank_US_Map_(states_only).svg', 'r') as f:
    content = f.read()

# Extract all path elements with state classes
pattern = r'<path class="([a-z]{2})"([^>]*)>(.*?)</path>'
matches = re.findall(pattern, content, re.DOTALL)

# Process each state path
for state_code, attributes, inner_content in matches:
    if state_code != 'dc':  # Skip DC
        # Convert to uppercase and format
        state_upper = state_code.upper()
        # Clean up the attributes to get just the path data
        path_match = re.search(r'd="([^"]+)"', attributes)
        if path_match:
            path_data = path_match.group(1)
            # Output the processed path
            print(f'<path id="state-{state_upper}" class="state-path heat-0" d="{path_data}">')
            if inner_content.strip():
                print(inner_content.strip())
            print('</path>')