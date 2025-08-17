#!/usr/bin/env python3

import re

print("Creating exact WordPress match version...")

# Read carpenter copy.html to get the exact styles and layout
with open('carpenter copy.html', 'r') as f:
    carpenter_content = f.read()

# Extract the exact SVG
svg_match = re.search(r'<svg.*?</svg>', carpenter_content, re.DOTALL)
if not svg_match:
    print("ERROR: Could not find SVG")
    exit(1)

real_svg = svg_match.group(0)

# Remove inline event handlers
real_svg = re.sub(r'\s+onclick="[^"]*"', '', real_svg)
real_svg = re.sub(r'\s+onmouseover="[^"]*"', '', real_svg)
real_svg = re.sub(r'\s+onmouseout="[^"]*"', '', real_svg)

state_count = real_svg.count('id="state-')
print(f"Extracted SVG with {state_count} states")

# Create the exact match HTML
html_content = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>WordPress Exact Match - Carpenter Insurance Map</title>
</head>
<body>

<!-- ================================================== -->
<!-- COPY EVERYTHING BELOW THIS LINE INTO WORDPRESS -->
<!-- ================================================== -->

<style>
/* Container Styles */
#insurance-map-container {
    max-width: 1160px;
    margin: 0 auto;
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    color: #333;
}

/* Header Styles */
.map-header {
    text-align: center;
    margin-bottom: 30px;
}

.map-header h2 {
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 10px;
    color: #1a1a1a;
}

.map-subtitle {
    font-size: 16px;
    color: #666;
    margin: 0;
}

/* Toggle Button Styles */
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
    font-weight: 500;
    transition: all 0.3s ease;
    color: #555;
}

.metric-btn:hover {
    background: #f5f5f5;
    border-color: #999;
}

.metric-btn.active {
    background: #2563eb;
    color: white;
    border-color: #2563eb;
}

/* WC Sub-buttons */
.wc-sub-buttons {
    display: none;
    gap: 10px;
    justify-content: center;
    margin-top: -20px;
    margin-bottom: 20px;
}

.wc-sub-buttons.show {
    display: flex;
}

.wc-sub-btn {
    padding: 8px 16px;
    border: 2px solid #ddd;
    background: white;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.3s ease;
    color: #555;
}

.wc-sub-btn:hover {
    background: #f5f5f5;
    border-color: #999;
}

.wc-sub-btn.active {
    background: #10b981;
    color: white;
    border-color: #10b981;
}

/* Main content layout */
.map-content-container {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
}

/* Map Wrapper */
.map-wrapper {
    position: relative;
    background: #f9fafb;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    flex: 1;
}

#us-map-svg {
    width: 100%;
    height: auto;
    display: block;
}

#us-map-svg svg {
    width: 100%;
    height: auto;
    display: block;
}

/* State Styles */
.state-path {
    stroke: #fff;
    stroke-width: 0.5;
    cursor: pointer;
    transition: all 0.2s ease;
    pointer-events: all !important;
}

.state-path:hover {
    stroke: #333;
    stroke-width: 1.5;
    filter: brightness(0.9);
}

.state-path.selected {
    stroke: #f73333;
    stroke-width: 2;
    fill: #ffcccc !important;
}

/* CORRECT BLUE HEAT MAP COLORS FROM ORIGINAL */
.heat-0 { fill: #e5f3ff; }
.heat-1 { fill: #b3d9ff; }
.heat-2 { fill: #80bfff; }
.heat-3 { fill: #4da6ff; }
.heat-4 { fill: #1a8cff; }
.heat-5 { fill: #0066cc; }
.heat-6 { fill: #004c99; }
.heat-7 { fill: #003366; }

/* Info Panel */
.info-panel {
    width: 320px;
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.info-panel h3 {
    font-size: 14px;
    font-weight: 500;
    color: #666;
    margin: 0 0 16px 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.state-info {
    text-align: center;
    padding: 20px 0;
}

.state-name {
    font-size: 28px;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 48px;
    font-weight: 700;
    color: #2563eb;
    margin-bottom: 8px;
}

.metric-label {
    font-size: 14px;
    color: #666;
    margin-bottom: 16px;
}

.metric-description {
    font-size: 13px;
    color: #999;
    line-height: 1.5;
}

/* Legend */
.legend-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    margin-bottom: 20px;
}

.legend-label {
    font-size: 14px;
    font-weight: 500;
    color: #666;
}

.legend-gradient {
    width: 200px;
    height: 12px;
    background: linear-gradient(to right, #e5f3ff, #003366);
    border-radius: 6px;
}

.legend-min, .legend-max {
    font-size: 12px;
    color: #888;
}

/* Hide the source SVG */
#hidden-svg-source {
    display: none !important;
    visibility: hidden !important;
    position: absolute !important;
    left: -9999px !important;
}

/* Responsive */
@media (max-width: 768px) {
    .map-content-container {
        flex-direction: column;
    }
    
    .info-panel {
        width: 100%;
    }
}
</style>

<div id="insurance-map-container">
    <div class="map-header">
        <h2>Carpenter Insurance Cost Metrics by State</h2>
        <p class="map-subtitle">Explore insurance costs and savings opportunities across the United States</p>
    </div>
    
    <div class="metric-toggles">
        <button class="metric-btn active" data-metric="glPremiumPct">GL Premium % of Revenue</button>
        <button class="metric-btn" data-metric="glSavingsPct">GL Savings %</button>
        <button class="metric-btn" data-metric="glCompetitiveness">GL Carrier Competitiveness</button>
        <button class="metric-btn" data-metric="wcRate">WC Rate per $100</button>
    </div>
    
    <div class="wc-sub-buttons" id="wc-sub-buttons">
        <button class="wc-sub-btn active" data-wc-code="5437">Class 5437 (Carpentry-framing)</button>
        <button class="wc-sub-btn" data-wc-code="5645">Class 5645 (Carpentry-interior)</button>
    </div>
    
    <div class="legend-container">
        <span class="legend-label">Legend:</span>
        <span class="legend-min">Low</span>
        <div class="legend-gradient"></div>
        <span class="legend-max">High</span>
    </div>
    
    <div class="map-content-container">
        <div class="map-wrapper">
            <div id="us-map-svg">
                <!-- SVG will be copied here by JavaScript -->
            </div>
        </div>
        
        <div class="info-panel">
            <h3>State Information</h3>
            <div class="state-info">
                <div class="state-name">Select a State</div>
                <div class="metric-value">--</div>
                <div class="metric-label">Click on a state</div>
                <div class="metric-description">View detailed insurance metrics by selecting any state on the map</div>
            </div>
        </div>
    </div>
</div>

<!-- Hidden SVG source -->
<div id="hidden-svg-source">
''' + real_svg + '''
</div>

<script>
// Pure ES5 JavaScript - WordPress Safe
(function() {
    'use strict';
    
    // Complete state data (matching original)
    var stateData = {
        glPremiumPct: {
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
        glSavingsPct: {
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
        glCompetitiveness: {
            AL: 90, AK: 0, AZ: 20, AR: 50, CA: 10,
            CO: 40, CT: 30, DE: 50, FL: 20, GA: 100,
            HI: 0, ID: 50, IL: 40, IN: 50, IA: 10,
            KS: 40, KY: 20, LA: 10, ME: 20, MD: 80,
            MA: 50, MI: 50, MN: 80, MS: 50, MO: 50,
            MT: 20, NE: 20, NV: 10, NH: 20, NJ: 80,
            NM: 50, NY: 0, NC: 40, ND: 30, OH: 80,
            OK: 70, OR: 70, PA: 70, RI: 40, SC: 90,
            SD: 50, TN: 100, TX: 90, UT: 80, VT: 10,
            VA: 100, WA: 20, WV: 30, WI: 70, WY: 30
        },
        wcRate5437: {
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
        },
        wcRate5645: {
            AL: 14.07, AK: 9.78, AZ: 10.17, AR: 6.33, CA: 8.46,
            CO: 7.40, CT: 17.17, DE: 9.06, FL: 12.61, GA: 43.42,
            HI: 10.60, ID: 12.93, IL: 19.23, IN: 5.56, IA: 9.65,
            KS: 10.53, KY: 9.81, LA: 17.76, ME: 10.58, MD: 7.23,
            MA: 6.93, MI: 10.27, MN: 11.44, MS: 9.19, MO: 12.48,
            MT: 9.85, NE: 9.15, NV: 7.89, NH: 9.54, NJ: 17.09,
            NM: 12.78, NY: 11.47, NC: 16.73, ND: 3.51, OH: 4.59,
            OK: 13.80, OR: 6.70, PA: 9.50, RI: 9.03, SC: 21.48,
            SD: 10.29, TN: 12.84, TX: 4.39, UT: 9.90, VT: 11.50,
            VA: 9.73, WA: 8.20, WV: 5.72, WI: 13.07, WY: 4.31
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
    
    var metricConfig = {
        glPremiumPct: {
            label: 'GL Premium as % of Revenue',
            format: function(val) { return val + '%'; },
            description: 'General Liability insurance premium as a percentage of contractor revenue'
        },
        glSavingsPct: {
            label: 'GL Savings as % of Premium', 
            format: function(val) { return val + '%'; },
            description: 'Potential savings on General Liability insurance premiums'
        },
        glCompetitiveness: {
            label: 'GL Carrier Competitiveness',
            format: function(val) { return val + 'th percentile'; },
            description: 'Market competitiveness ranking based on number of carrier quotes'
        },
        wcRate5437: {
            label: 'WC Rate per $100 (Class 5437)',
            format: function(val) { return '$' + val.toFixed(2); },
            description: 'Workers\' Comp rate for Class Code 5437 (Carpentry-framing)'
        },
        wcRate5645: {
            label: 'WC Rate per $100 (Class 5645)',
            format: function(val) { return '$' + val.toFixed(2); },
            description: 'Workers\' Comp rate for Class Code 5645 (Carpentry-interior)'
        }
    };
    
    var currentMetric = 'glPremiumPct';
    var currentWCCode = '5437';
    var selectedState = null;
    
    // Update colors
    function updateColors() {
        console.log('Updating colors for metric:', currentMetric);
        
        var metricKey = currentMetric === 'wcRate' ? 'wcRate' + currentWCCode : currentMetric;
        var data = stateData[metricKey];
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
        var labelEl = document.querySelector('.metric-label');
        var descEl = document.querySelector('.metric-description');
        
        if (!nameEl || !valueEl) return;
        
        if (stateCode) {
            var stateName = stateNames[stateCode] || stateCode;
            nameEl.textContent = stateName;
            
            var metricKey = currentMetric === 'wcRate' ? 'wcRate' + currentWCCode : currentMetric;
            var config = metricConfig[metricKey];
            var value = stateData[metricKey][stateCode];
            
            if (value !== undefined && config) {
                valueEl.textContent = config.format(value);
                labelEl.textContent = config.label;
                descEl.textContent = config.description;
            } else {
                valueEl.textContent = '--';
            }
        } else {
            nameEl.textContent = 'Select a State';
            valueEl.textContent = '--';
            labelEl.textContent = 'Click on a state';
            descEl.textContent = 'View detailed insurance metrics by selecting any state on the map';
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
        
        // Show/hide WC sub-buttons
        var wcButtons = document.getElementById('wc-sub-buttons');
        if (metric === 'wcRate') {
            wcButtons.classList.add('show');
            currentMetric = 'wcRate';
        } else {
            wcButtons.classList.remove('show');
            currentMetric = metric;
        }
        
        // Update colors and info
        updateColors();
        if (selectedState) {
            updateInfo(selectedState);
        }
    }
    
    // Handle WC code button click
    function handleWCClick(event) {
        var target = event.target;
        
        if (!target.classList || !target.classList.contains('wc-sub-btn')) {
            return;
        }
        
        var code = target.getAttribute('data-wc-code');
        console.log('WC code clicked:', code);
        
        // Update active button
        var buttons = document.querySelectorAll('.wc-sub-btn');
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].classList.remove('active');
        }
        target.classList.add('active');
        
        currentWCCode = code;
        updateColors();
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
            var container = document.getElementById('us-map-svg');
            
            if (!hiddenSvg || !container) {
                console.error('SVG or container not found');
                return;
            }
            
            // Clone and insert SVG
            var svgClone = hiddenSvg.cloneNode(true);
            container.appendChild(svgClone);
            
            // Add event listeners using delegation
            container.addEventListener('click', handleStateClick);
            
            var buttonContainer = document.querySelector('.metric-toggles');
            if (buttonContainer) {
                buttonContainer.addEventListener('click', handleMetricClick);
            }
            
            var wcContainer = document.getElementById('wc-sub-buttons');
            if (wcContainer) {
                wcContainer.addEventListener('click', handleWCClick);
            }
            
            // Initial color update
            updateColors();
            
            console.log('Map initialized successfully!');
            
        } catch (error) {
            console.error('Initialization error:', error);
        }
    }
    
    // Wait for DOM
    function domReady() {
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            setTimeout(init, 100);
        } else {
            document.addEventListener('DOMContentLoaded', init);
        }
    }
    
    domReady();
})();
</script>

<!-- ================================================== -->
<!-- COPY EVERYTHING ABOVE THIS LINE INTO WORDPRESS -->
<!-- ================================================== -->

</body>
</html>'''

# Save the file
with open('wordpress-exact-match.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\n✅ Created wordpress-exact-match.html")
print("\nThis version exactly matches the original with:")
print("- Blue gradient heat map colors (#e5f3ff to #003366)")
print("- Complete UI with subtitle and legend")
print("- Side panel layout for state information")
print("- WC sub-buttons that appear when WC Rate is selected")
print("- All 50 states with complete data")
print("\nCopy everything between the marked lines into WordPress!")