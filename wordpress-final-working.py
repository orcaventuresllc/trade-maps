#!/usr/bin/env python3

import re

print("Creating final WordPress version with real SVG...")

# Read the working ES5 test version
with open('wordpress-es5-safe.html', 'r') as f:
    es5_content = f.read()

# Read the carpenter copy.html to get the real SVG
with open('carpenter copy.html', 'r') as f:
    carpenter_content = f.read()

# Extract the real SVG from carpenter copy.html
svg_match = re.search(r'<svg.*?</svg>', carpenter_content, re.DOTALL)
if not svg_match:
    print("ERROR: Could not find SVG in carpenter copy.html")
    exit(1)

real_svg = svg_match.group(0)

# Remove all inline event handlers from the SVG
real_svg = re.sub(r'\s+onclick="[^"]*"', '', real_svg)
real_svg = re.sub(r'\s+onmouseover="[^"]*"', '', real_svg)
real_svg = re.sub(r'\s+onmouseout="[^"]*"', '', real_svg)

state_count = real_svg.count('id="state-')
print(f"Extracted SVG with {state_count} states")

# Extract the complete state data from carpenter copy.html
# Find the DATA object
data_pattern = r'window\.DATA\s*=\s*\{(.*?)\};'
data_match = re.search(data_pattern, carpenter_content, re.DOTALL)

if data_match:
    data_content = data_match.group(1)
    print("Extracted complete state data")
else:
    print("Warning: Could not extract full state data, using defaults")
    data_content = ""

# Now replace the test SVG with the real one in our ES5 version
# Find and replace the createTestSVG function
test_svg_pattern = r'function createTestSVG\(\) \{.*?return svg;\s*\}'

def create_real_svg_function(svg):
    # Escape the SVG for JavaScript string
    svg_escaped = svg.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
    
    return f"""function createRealSVG() {{
        debug('Injecting real US map SVG...');
        return '{svg_escaped}';
    }}"""

es5_content = re.sub(test_svg_pattern, create_real_svg_function(real_svg), es5_content, flags=re.DOTALL)

# Replace createTestSVG() call with createRealSVG()
es5_content = es5_content.replace('createTestSVG()', 'createRealSVG()')

# Update the simple state data with complete data for all 50 states
complete_data = """
    // Complete state data for all 50 states
    var stateData = {
        glPremium: {
            AL: 0.95, AK: 0.65, AZ: 1.0, AR: 0.85, CA: 1.0,
            CO: 0.55, CT: 0.85, DE: 0.95, FL: 0.85, GA: 1.25,
            HI: 2.6, ID: 0.9, IL: 0.85, IN: 0.6, IA: 0.85,
            KS: 0.8, KY: 0.65, LA: 1.2, ME: 0.75, MD: 1.05,
            MA: 0.8, MI: 0.8, MN: 1.3, MS: 1.2, MO: 1.9,
            MT: 0.85, NE: 1.6, NV: 0.6, NH: 0.9, NJ: 0.6,
            NM: 0.75, NY: 0.75, NC: 1.6, ND: 0.75, OH: 1.15,
            OK: 1.3, OR: 1.1, PA: 1.4, RI: 1.25, SC: 0.9,
            SD: 0.85, TN: 0.85, TX: 0.8, UT: 1.0, VT: 0.7,
            VA: 0.5, WA: 0.75, WV: 1.0, WI: 0.8, WY: 0.8
        },
        glSavings: {
            AL: 27.7, AK: 35.9, AZ: 58.1, AR: 46.0, CA: 35.8,
            CO: 55.6, CT: 46.9, DE: 32.0, FL: 29.5, GA: 47.3,
            HI: 22.6, ID: 17.0, IL: 46.9, IN: 41.4, IA: 36.2,
            KS: 44.4, KY: 65.2, LA: 69.7, ME: 45.5, MD: 33.9,
            MA: 27.9, MI: 43.2, MN: 41.7, MS: 23.8, MO: 29.0,
            MT: 42.2, NE: 29.3, NV: 60.0, NH: 17.6, NJ: 42.9,
            NM: 57.8, NY: 28.9, NC: 13.0, ND: 43.9, OH: 47.8,
            OK: 62.7, OR: 46.8, PA: 37.9, RI: 60.6, SC: 53.4,
            SD: 54.2, TN: 22.7, TX: 21.2, UT: 35.8, VT: 34.4,
            VA: 37.0, WA: 61.5, WV: 54.0, WI: 51.0, WY: 17.9
        },
        wcRate: {
            AL: 6.14, AK: 6.16, AZ: 4.05, AR: 3.26, CA: 5.62,
            CO: 4.74, CT: 7.86, DE: 5.00, FL: 6.23, GA: 8.98,
            HI: 6.03, ID: 6.58, IL: 9.75, IN: 2.83, IA: 5.71,
            KS: 4.55, KY: 3.87, LA: 9.60, ME: 6.61, MD: 5.50,
            MA: 4.19, MI: 5.66, MN: 11.75, MS: 6.14, MO: 5.96,
            MT: 6.91, NE: 4.91, NV: 4.80, NH: 6.79, NJ: 11.44,
            NM: 5.93, NY: 9.50, NC: 5.48, ND: 3.73, OH: 3.32,
            OK: 6.37, OR: 2.50, PA: 7.06, RI: 8.14, SC: 8.26,
            SD: 5.71, TN: 3.93, TX: 3.55, UT: 4.39, VT: 7.55,
            VA: 5.46, WA: 4.67, WV: 2.74, WI: 10.03, WY: 3.48
        }
    };
    
    // State names for display
    var stateNames = {
        AL: 'Alabama', AK: 'Alaska', AZ: 'Arizona', AR: 'Arkansas', CA: 'California',
        CO: 'Colorado', CT: 'Connecticut', DE: 'Delaware', FL: 'Florida', GA: 'Georgia',
        HI: 'Hawaii', ID: 'Idaho', IL: 'Illinois', IN: 'Indiana', IA: 'Iowa',
        KS: 'Kansas', KY: 'Kentucky', LA: 'Louisiana', ME: 'Maine', MD: 'Maryland',
        MA: 'Massachusetts', MI: 'Michigan', MN: 'Minnesota', MS: 'Mississippi',
        MO: 'Missouri', MT: 'Montana', NE: 'Nebraska', NV: 'Nevada',
        NH: 'New Hampshire', NJ: 'New Jersey', NM: 'New Mexico', NY: 'New York',
        NC: 'North Carolina', ND: 'North Dakota', OH: 'Ohio', OK: 'Oklahoma',
        OR: 'Oregon', PA: 'Pennsylvania', RI: 'Rhode Island', SC: 'South Carolina',
        SD: 'South Dakota', TN: 'Tennessee', TX: 'Texas', UT: 'Utah', VT: 'Vermont',
        VA: 'Virginia', WA: 'Washington', WV: 'West Virginia', WI: 'Wisconsin', WY: 'Wyoming'
    };"""

# Replace the simple state data
simple_data_pattern = r'// Simple state data.*?var currentMetric = \'glPremium\';'
es5_content = re.sub(simple_data_pattern, complete_data + '\n\n    var currentMetric = \'glPremium\';', es5_content, flags=re.DOTALL)

# Update the updateInfo function to show state names
info_update = """function updateInfo(stateCode) {
        var nameEl = document.querySelector('.state-name');
        var valueEl = document.querySelector('.metric-value');
        
        if (!nameEl || !valueEl) return;
        
        if (stateCode) {
            var stateName = stateNames[stateCode] || stateCode;
            nameEl.textContent = stateName;
            var value = stateData[currentMetric][stateCode];
            if (value !== undefined) {
                if (currentMetric === 'glPremium') {
                    valueEl.textContent = value + '%';
                } else if (currentMetric === 'glSavings') {
                    valueEl.textContent = value + '%';
                } else if (currentMetric === 'wcRate') {
                    valueEl.textContent = '$' + value.toFixed(2);
                }
            } else {
                valueEl.textContent = '--';
            }
        } else {
            nameEl.textContent = 'Select a State';
            valueEl.textContent = '--';
        }
    }"""

# Replace the updateInfo function
info_pattern = r'function updateInfo\(stateCode\) \{.*?\n    \}'
es5_content = re.sub(info_pattern, info_update, es5_content, flags=re.DOTALL)

# Save the final version
with open('wordpress-final-working.html', 'w') as f:
    f.write(es5_content)

print("\n✅ Created wordpress-final-working.html")
print("\nThis version has:")
print("- The complete real US map SVG")
print("- All 50 states with real data")
print("- ES5-only JavaScript that works in WordPress")
print("- Debug console for troubleshooting")
print("\nCopy the entire contents into WordPress!")