#!/usr/bin/env python3

import re

print("Creating WordPress version with hidden SVG approach...")

# Read the carpenter copy.html to get the real SVG
with open('carpenter copy.html', 'r') as f:
    carpenter_content = f.read()

# Extract the real SVG
svg_match = re.search(r'<svg.*?</svg>', carpenter_content, re.DOTALL)
if not svg_match:
    print("ERROR: Could not find SVG in carpenter copy.html")
    exit(1)

real_svg = svg_match.group(0)

# Remove all inline event handlers
real_svg = re.sub(r'\s+onclick="[^"]*"', '', real_svg)
real_svg = re.sub(r'\s+onmouseover="[^"]*"', '', real_svg)
real_svg = re.sub(r'\s+onmouseout="[^"]*"', '', real_svg)

state_count = real_svg.count('id="state-')
print(f"Extracted SVG with {state_count} states")

# Create the HTML with hidden SVG
html_content = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>WordPress Hidden SVG Version</title>
</head>
<body>

<!-- ================================================== -->
<!-- COPY EVERYTHING BELOW THIS LINE INTO WORDPRESS -->
<!-- ================================================== -->

<style>
#insurance-map-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.map-header {
    text-align: center;
    margin-bottom: 30px;
}

.map-header h2 {
    font-size: 28px;
    font-weight: 600;
    color: #1a1a1a;
}

.metric-toggles {
    display: flex;
    gap: 10px;
    justify-content: center;
    margin-bottom: 30px;
    flex-wrap: wrap;
}

.metric-btn {
    padding: 10px 20px;
    border: 2px solid #ddd;
    background: white;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s;
}

.metric-btn:hover {
    background: #f5f5f5;
}

.metric-btn.active {
    background: #2563eb;
    color: white;
    border-color: #2563eb;
}

.map-wrapper {
    background: #f9fafb;
    border-radius: 12px;
    padding: 20px;
    min-height: 400px;
}

/* State path styles */
.state-path {
    stroke: #fff;
    stroke-width: 0.5;
    cursor: pointer;
    transition: all 0.2s;
    fill: #e5e7eb;
}

.state-path:hover {
    stroke: #333;
    stroke-width: 1.5;
}

.state-path.selected {
    stroke: #dc2626 !important;
    stroke-width: 2 !important;
    fill: #fca5a5 !important;
}

/* Heat colors */
.heat-0 { fill: #fee2e2; }
.heat-1 { fill: #fecaca; }
.heat-2 { fill: #fca5a5; }
.heat-3 { fill: #f87171; }
.heat-4 { fill: #ef4444; }
.heat-5 { fill: #dc2626; }
.heat-6 { fill: #b91c1c; }
.heat-7 { fill: #991b1b; }

.info-card {
    margin-top: 20px;
    padding: 20px;
    background: white;
    border-radius: 8px;
    text-align: center;
}

.state-name {
    font-size: 24px;
    font-weight: 600;
    color: #2563eb;
    margin-bottom: 10px;
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
    color: #1a1a1a;
}

/* Hide the source SVG */
#hidden-svg-source {
    display: none !important;
    visibility: hidden !important;
    position: absolute !important;
    left: -9999px !important;
}
</style>

<div id="insurance-map-container">
    <div class="map-header">
        <h2>Carpenter Insurance Cost Metrics by State</h2>
    </div>
    
    <div class="metric-toggles">
        <button class="metric-btn active" data-metric="glPremium">GL Premium %</button>
        <button class="metric-btn" data-metric="glSavings">GL Savings %</button>
        <button class="metric-btn" data-metric="wcRate">WC Rate</button>
    </div>
    
    <div class="map-wrapper">
        <div id="map-svg-container">
            <!-- SVG will be copied here by JavaScript -->
        </div>
    </div>
    
    <div class="info-card">
        <div class="state-name">Select a State</div>
        <div class="metric-value">--</div>
    </div>
</div>

<!-- Hidden SVG source - WordPress won't strip this -->
<div id="hidden-svg-source">
''' + real_svg + '''
</div>

<script>
// Pure ES5 JavaScript - WordPress Safe
(function() {
    'use strict';
    
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
    };
    
    var currentMetric = 'glPremium';
    var selectedState = null;
    
    // Update colors
    function updateColors() {
        console.log('Updating colors for metric:', currentMetric);
        
        var data = stateData[currentMetric];
        if (!data) return;
        
        // Get all state elements
        var states = document.querySelectorAll('.state-path');
        
        // Calculate min/max
        var values = [];
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                values.push(data[key]);
            }
        }
        
        if (values.length === 0) return;
        
        var min = Math.min.apply(null, values);
        var max = Math.max.apply(null, values);
        
        // Update each state
        for (var i = 0; i < states.length; i++) {
            var state = states[i];
            var stateCode = state.id.replace('state-', '');
            var value = data[stateCode];
            
            // Remove old heat classes
            for (var j = 0; j <= 7; j++) {
                state.classList.remove('heat-' + j);
            }
            
            // Add new heat class
            if (value !== undefined) {
                var normalized = (value - min) / (max - min);
                var heat = Math.floor(normalized * 8);
                heat = Math.min(7, Math.max(0, heat));
                state.classList.add('heat-' + heat);
            }
        }
    }
    
    // Handle state click
    function handleStateClick(event) {
        var target = event.target;
        
        // Check if it's a state path
        if (!target.classList || !target.classList.contains('state-path')) {
            return;
        }
        
        var stateCode = target.id.replace('state-', '');
        console.log('State clicked:', stateCode);
        
        // Remove previous selection
        var allStates = document.querySelectorAll('.state-path');
        for (var i = 0; i < allStates.length; i++) {
            allStates[i].classList.remove('selected');
        }
        
        // Toggle selection
        if (selectedState === stateCode) {
            selectedState = null;
            updateInfo(null);
        } else {
            target.classList.add('selected');
            selectedState = stateCode;
            updateInfo(stateCode);
        }
    }
    
    // Update info display
    function updateInfo(stateCode) {
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
    }
    
    // Handle metric button click
    function handleMetricClick(event) {
        var target = event.target;
        
        if (!target.classList || !target.classList.contains('metric-btn')) {
            return;
        }
        
        var metric = target.getAttribute('data-metric');
        console.log('Metric clicked:', metric);
        
        // Update active button
        var buttons = document.querySelectorAll('.metric-btn');
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].classList.remove('active');
        }
        target.classList.add('active');
        
        // Update metric and colors
        currentMetric = metric;
        updateColors();
        
        // Update info if state selected
        if (selectedState) {
            updateInfo(selectedState);
        }
    }
    
    // Initialize everything
    function init() {
        console.log('Initializing map...');
        
        try {
            // Get the hidden SVG
            var hiddenSvg = document.querySelector('#hidden-svg-source svg');
            var container = document.getElementById('map-svg-container');
            
            if (!hiddenSvg) {
                console.error('Hidden SVG not found!');
                return;
            }
            
            if (!container) {
                console.error('Map container not found!');
                return;
            }
            
            // Clone the SVG and insert it into the visible container
            var svgClone = hiddenSvg.cloneNode(true);
            container.appendChild(svgClone);
            console.log('SVG copied to container');
            
            // Add click listener to map container (event delegation)
            container.addEventListener('click', handleStateClick);
            console.log('Added state click listener');
            
            // Add click listener to buttons container (event delegation)
            var buttonContainer = document.querySelector('.metric-toggles');
            if (buttonContainer) {
                buttonContainer.addEventListener('click', handleMetricClick);
                console.log('Added metric click listener');
            }
            
            // Initial color update
            updateColors();
            
            console.log('Initialization complete!');
            
        } catch (error) {
            console.error('Initialization error:', error);
        }
    }
    
    // Wait for DOM to be ready
    function domReady() {
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            // Small delay for WordPress
            setTimeout(init, 100);
        } else {
            document.addEventListener('DOMContentLoaded', init);
        }
    }
    
    // Start
    domReady();
    
})();
</script>

<!-- ================================================== -->
<!-- COPY EVERYTHING ABOVE THIS LINE INTO WORDPRESS -->
<!-- ================================================== -->

</body>
</html>'''

# Save the file
with open('wordpress-hidden-svg.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\n✅ Created wordpress-hidden-svg.html")
print("\nThis version:")
print("- Stores the complete SVG in a hidden div")
print("- JavaScript copies it to the visible container")
print("- No string escaping issues")
print("- Pure ES5 JavaScript")
print("\nCopy everything between the marked lines into WordPress!")