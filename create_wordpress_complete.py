#!/usr/bin/env python3

import re

# Read the carpenter copy.html file for the SVG paths
with open('carpenter copy.html', 'r') as f:
    content = f.read()

# Extract the complete SVG section
svg_match = re.search(r'<svg.*?</svg>', content, re.DOTALL)
if not svg_match:
    print("SVG not found in carpenter copy.html")
    exit(1)
    
svg_content = svg_match.group(0)

# Remove all event handlers from SVG
svg_content = re.sub(r'\s+onclick="[^"]*"', '', svg_content)
svg_content = re.sub(r'\s+onmouseover="[^"]*"', '', svg_content)
svg_content = re.sub(r'\s+onmouseout="[^"]*"', '', svg_content)

# Create the complete WordPress HTML
wordpress_html = '''<style>
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
        fill: #e5e7eb;
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
    
    /* Heat Map Colors */
    .heat-0 { fill: #eff6ff; }
    .heat-1 { fill: #dbeafe; }
    .heat-2 { fill: #bfdbfe; }
    .heat-3 { fill: #93c5fd; }
    .heat-4 { fill: #60a5fa; }
    .heat-5 { fill: #3b82f6; }
    .heat-6 { fill: #2563eb; }
    .heat-7 { fill: #1d4ed8; }
    
    /* Info Card */
    .info-card {
        background: #f8fafc;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        width: 300px;
    }
    
    .info-card h3 {
        margin: 0 0 10px 0;
        color: #1a1a1a;
        font-size: 20px;
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
        margin-bottom: 10px;
    }
    
    .metric-description {
        color: #666;
        font-size: 14px;
        line-height: 1.5;
    }
    
    /* Tooltip */
    #map-tooltip {
        position: absolute;
        background: white;
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        pointer-events: none;
        display: none;
        z-index: 1000;
    }
    
    #map-tooltip .state-name {
        font-weight: 600;
        margin-bottom: 4px;
        font-size: 16px;
    }
    
    #map-tooltip .metric-label {
        font-size: 12px;
        color: #666;
    }
    
    #map-tooltip .metric-value {
        font-size: 18px;
        font-weight: 600;
        color: #2563eb;
    }
    
    /* Legend */
    .legend-container {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .legend-gradient {
        display: inline-block;
        width: 300px;
        height: 20px;
        background: linear-gradient(to right, #eff6ff, #1d4ed8);
        border-radius: 10px;
        margin: 0 10px;
    }
    
    .legend-label {
        font-size: 12px;
        color: #666;
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
        <button class="wc-sub-btn active" data-wc-code="5437">Class 5437 (Framing)</button>
        <button class="wc-sub-btn" data-wc-code="5645">Class 5645 (Interior)</button>
    </div>
    
    <div class="legend-container">
        <span class="legend-label">Low</span>
        <div class="legend-gradient"></div>
        <span class="legend-label">High</span>
    </div>
    
    <div class="map-content-container">
        <div class="map-wrapper">
            <div id="us-map-svg">
                ''' + svg_content + '''
            </div>
            
            <div id="map-tooltip">
                <div class="state-name"></div>
                <div class="metric-label"></div>
                <div class="metric-value"></div>
            </div>
        </div>
        
        <div class="info-card">
            <h3>State Information</h3>
            <div class="state-name">Select a State</div>
            <div class="metric-value">--</div>
            <div class="metric-description">Click on a state to view insurance metrics</div>
        </div>
    </div>
</div>

<script>
console.log('WordPress Insurance Map Script Starting - DOM Ready');

(function() {
    // Data structure with all states
    window.DATA = {
        // GL Premium as % of Revenue (with ranges)
        glPremiumPct: {
            AL: { midpoint: 0.95, range: "0.7% – 1.2%" },
            AK: { midpoint: 0.65, range: "0.4% – 0.9%" },
            AZ: { midpoint: 1.0, range: "0.4% – 1.6%" },
            AR: { midpoint: 0.85, range: "0.4% – 1.3%" },
            CA: { midpoint: 1.0, range: "0.7% – 1.3%" },
            CO: { midpoint: 0.55, range: "0.3% – 0.8%" },
            CT: { midpoint: 0.85, range: "0.4% – 1.3%" },
            DE: { midpoint: 0.95, range: "0.5% – 1.4%" },
            FL: { midpoint: 0.85, range: "0.5% – 1.2%" },
            GA: { midpoint: 1.25, range: "0.6% – 1.9%" },
            HI: { midpoint: 2.6, range: "2.1% – 3.1%" },
            ID: { midpoint: 0.9, range: "0.7% – 1.1%" },
            IL: { midpoint: 0.85, range: "0.4% – 1.3%" },
            IN: { midpoint: 0.6, range: "0.3% – 0.9%" },
            IA: { midpoint: 0.85, range: "0.5% – 1.2%" },
            KS: { midpoint: 0.8, range: "0.3% – 1.3%" },
            KY: { midpoint: 0.65, range: "0.2% – 1.1%" },
            LA: { midpoint: 1.2, range: "0.3% – 2.1%" },
            ME: { midpoint: 0.75, range: "0.4% – 1.1%" },
            MD: { midpoint: 1.05, range: "0.7% – 1.4%" },
            MA: { midpoint: 0.8, range: "0.6% – 1.0%" },
            MI: { midpoint: 0.8, range: "0.5% – 1.1%" },
            MN: { midpoint: 1.3, range: "0.7% – 1.9%" },
            MS: { midpoint: 1.2, range: "0.9% – 1.5%" },
            MO: { midpoint: 1.9, range: "1.4% – 2.4%" },
            MT: { midpoint: 0.85, range: "0.4% – 1.3%" },
            NE: { midpoint: 1.6, range: "1.2% – 2.0%" },
            NV: { midpoint: 0.6, range: "0.3% – 0.9%" },
            NH: { midpoint: 0.9, range: "0.7% – 1.1%" },
            NJ: { midpoint: 0.6, range: "0.3% – 0.9%" },
            NM: { midpoint: 0.75, range: "0.3% – 1.2%" },
            NY: { midpoint: 0.75, range: "0.4% – 1.1%" },
            NC: { midpoint: 1.6, range: "1.3% – 1.9%" },
            ND: { midpoint: 0.75, range: "0.4% – 1.1%" },
            OH: { midpoint: 1.15, range: "0.6% – 1.7%" },
            OK: { midpoint: 1.3, range: "0.5% – 2.1%" },
            OR: { midpoint: 1.1, range: "0.5% – 1.7%" },
            PA: { midpoint: 1.4, range: "0.7% – 2.1%" },
            RI: { midpoint: 1.25, range: "0.6% – 1.9%" },
            SC: { midpoint: 0.9, range: "0.4% – 1.4%" },
            SD: { midpoint: 0.85, range: "0.4% – 1.3%" },
            TN: { midpoint: 0.85, range: "0.6% – 1.1%" },
            TX: { midpoint: 0.8, range: "0.5% – 1.1%" },
            UT: { midpoint: 1.0, range: "0.5% – 1.5%" },
            VT: { midpoint: 0.7, range: "0.4% – 1.0%" },
            VA: { midpoint: 0.5, range: "0.3% – 0.7%" },
            WA: { midpoint: 0.75, range: "0.2% – 1.3%" },
            WV: { midpoint: 1.0, range: "0.4% – 1.6%" },
            WI: { midpoint: 0.8, range: "0.4% – 1.2%" },
            WY: { midpoint: 0.8, range: "0.6% – 1.0%" }
        },
        
        // GL Savings as % of Premium
        glSavingsPct: {
            AL: 27.7, AK: 35.9, AZ: 58.1, AR: 46.0, CA: 35.8, CO: 55.6, CT: 46.9, DE: 32.0,
            FL: 29.5, GA: 47.3, HI: 22.6, ID: 17.0, IL: 46.9, IN: 41.4, IA: 36.2,
            KS: 44.4, KY: 65.2, LA: 69.7, ME: 45.5, MD: 33.9, MA: 27.9, MI: 43.2, MN: 41.7,
            MS: 23.8, MO: 29.0, MT: 42.2, NE: 29.3, NV: 60.0, NH: 17.6, NJ: 42.9, NM: 57.8,
            NY: 28.9, NC: 13.0, ND: 43.9, OH: 47.8, OK: 62.7, OR: 46.8, PA: 37.9, RI: 60.6,
            SC: 53.4, SD: 54.2, TN: 22.7, TX: 21.2, UT: 35.8, VT: 34.4, VA: 37.0, WA: 61.5,
            WV: 54.0, WI: 51.0, WY: 17.9
        },
        
        // GL Carrier Competitiveness (percentile)
        glCompetitiveness: {
            AL: 90, AK: 0, AZ: 20, AR: 50, CA: 10, CO: 40, CT: 30, DE: 50,
            FL: 20, GA: 100, HI: 0, ID: 50, IL: 40, IN: 50, IA: 10,
            KS: 40, KY: 20, LA: 10, ME: 20, MD: 80, MA: 50, MI: 50, MN: 80,
            MS: 50, MO: 50, MT: 20, NE: 20, NV: 10, NH: 20, NJ: 80, NM: 50,
            NY: 0, NC: 40, ND: 30, OH: 80, OK: 70, OR: 70, PA: 70, RI: 40,
            SC: 90, SD: 50, TN: 100, TX: 90, UT: 80, VT: 10, VA: 100, WA: 20,
            WV: 30, WI: 70, WY: 30
        },
        
        // Workers' Comp Rate per $100 of payroll
        wcRate5437: {
            AL: 6.14, AK: 6.16, AZ: 4.05, AR: 3.26, CA: 5.62, CO: 4.74, CT: 7.86,
            DE: 5.00, FL: 6.23, GA: 8.98, HI: 6.03, ID: 6.58, IL: 9.75,
            IN: 2.83, IA: 5.71, KS: 4.55, KY: 3.87, LA: 9.60, ME: 6.61, MD: 5.50,
            MA: 4.19, MI: 5.66, MN: 11.75, MS: 6.14, MO: 5.96, MT: 6.91, NE: 4.91,
            NV: 4.80, NH: 6.79, NJ: 11.44, NM: 5.93, NY: 9.50, NC: 5.48, ND: 3.73,
            OH: 3.32, OK: 6.37, OR: 2.50, PA: 7.06, RI: 8.14, SC: 8.26, SD: 5.71,
            TN: 3.93, TX: 3.55, UT: 4.39, VT: 7.55, VA: 5.46, WA: 4.67, WV: 2.74,
            WI: 10.03, WY: 3.48
        },
        wcRate5645: {
            AL: 14.07, AK: 9.78, AZ: 10.17, AR: 6.33, CA: 8.46, CO: 7.40, CT: 17.17,
            DE: 9.06, FL: 12.61, GA: 43.42, HI: 10.60, ID: 12.93, IL: 19.23,
            IN: 5.56, IA: 9.65, KS: 10.53, KY: 9.81, LA: 17.76, ME: 10.58, MD: 7.23,
            MA: 6.93, MI: 10.27, MN: 11.44, MS: 9.19, MO: 12.48, MT: 9.85, NE: 9.15,
            NV: 7.89, NH: 9.54, NJ: 17.09, NM: 12.78, NY: 11.47, NC: 16.73, ND: 3.51,
            OH: 4.59, OK: 13.80, OR: 6.70, PA: 9.50, RI: 9.03, SC: 21.48, SD: 10.29,
            TN: 12.84, TX: 4.39, UT: 9.90, VT: 11.50, VA: 9.73, WA: 8.20, WV: 5.72,
            WI: 13.07, WY: 4.31
        }
    };
    
    window.STATE_NAMES = {
        AL: "Alabama", AK: "Alaska", AZ: "Arizona", AR: "Arkansas", CA: "California",
        CO: "Colorado", CT: "Connecticut", DE: "Delaware", FL: "Florida", GA: "Georgia",
        HI: "Hawaii", ID: "Idaho", IL: "Illinois", IN: "Indiana", IA: "Iowa",
        KS: "Kansas", KY: "Kentucky", LA: "Louisiana", ME: "Maine", MD: "Maryland",
        MA: "Massachusetts", MI: "Michigan", MN: "Minnesota", MS: "Mississippi",
        MO: "Missouri", MT: "Montana", NE: "Nebraska", NV: "Nevada",
        NH: "New Hampshire", NJ: "New Jersey", NM: "New Mexico", NY: "New York",
        NC: "North Carolina", ND: "North Dakota", OH: "Ohio", OK: "Oklahoma",
        OR: "Oregon", PA: "Pennsylvania", RI: "Rhode Island", SC: "South Carolina",
        SD: "South Dakota", TN: "Tennessee", TX: "Texas", UT: "Utah", VT: "Vermont",
        VA: "Virginia", WA: "Washington", WV: "West Virginia", WI: "Wisconsin", WY: "Wyoming"
    };
    
    window.METRIC_CONFIG = {
        glPremiumPct: {
            label: "GL Premium as % of Revenue",
            format: function(data) { return data.range; }
        },
        glSavingsPct: {
            label: "GL Savings as % of Premium",
            format: function(val) { return val + '%'; }
        },
        glCompetitiveness: {
            label: "GL Carrier Competitiveness",
            format: function(val) { return val + 'th percentile'; }
        },
        wcRate5437: {
            label: "WC Rate per $100 (Class 5437)",
            format: function(val) { return '$' + val.toFixed(2); }
        },
        wcRate5645: {
            label: "WC Rate per $100 (Class 5645)",
            format: function(val) { return '$' + val.toFixed(2); }
        }
    };
    
    // State variables
    var currentMetric = 'glPremiumPct';
    var currentWCCode = '5437';
    var selectedState = null;
    
    // Simple color function
    function getHeatmapColor(value, min, max) {
        var normalized = (value - min) / (max - min);
        var heatLevel = Math.floor(normalized * 8);
        return 'heat-' + Math.min(7, Math.max(0, heatLevel));
    }
    
    // Update map colors
    function updateMapColors() {
        console.log('Updating map colors for metric:', currentMetric);
        
        var metricData = DATA[currentMetric];
        if (!metricData) {
            metricData = DATA['wcRate' + currentWCCode];
        }
        
        if (!metricData) return;
        
        // Calculate min and max
        var values = [];
        for (var state in metricData) {
            var val = currentMetric === 'glPremiumPct' ? metricData[state].midpoint : metricData[state];
            values.push(val);
        }
        
        var min = Math.min.apply(Math, values);
        var max = Math.max.apply(Math, values);
        
        // Update each state
        var states = document.querySelectorAll('.state-path');
        for (var i = 0; i < states.length; i++) {
            var state = states[i];
            var stateCode = state.id.replace('state-', '');
            
            // Remove old heat classes
            for (var j = 0; j <= 7; j++) {
                state.classList.remove('heat-' + j);
            }
            
            // Add new heat class
            if (metricData[stateCode]) {
                var val = currentMetric === 'glPremiumPct' ? metricData[stateCode].midpoint : metricData[stateCode];
                var colorClass = getHeatmapColor(val, min, max);
                state.classList.add(colorClass);
            }
        }
    }
    
    // Handle state click
    function handleStateClick(stateCode) {
        console.log('State clicked:', stateCode);
        
        // Toggle selection
        var allStates = document.querySelectorAll('.state-path');
        for (var i = 0; i < allStates.length; i++) {
            allStates[i].classList.remove('selected');
        }
        
        var stateEl = document.getElementById('state-' + stateCode);
        if (selectedState === stateCode) {
            selectedState = null;
        } else {
            stateEl.classList.add('selected');
            selectedState = stateCode;
        }
        
        updateInfoCard();
    }
    
    // Update info card
    function updateInfoCard() {
        var nameEl = document.querySelector('.info-card .state-name');
        var valueEl = document.querySelector('.info-card .metric-value');
        var descEl = document.querySelector('.info-card .metric-description');
        
        if (selectedState) {
            var stateName = STATE_NAMES[selectedState];
            var metricData = DATA[currentMetric] || DATA['wcRate' + currentWCCode];
            var config = METRIC_CONFIG[currentMetric] || METRIC_CONFIG['wcRate' + currentWCCode];
            
            nameEl.textContent = stateName;
            
            if (metricData && metricData[selectedState]) {
                var data = metricData[selectedState];
                valueEl.textContent = currentMetric === 'glPremiumPct' ? config.format(data) : config.format(data);
                descEl.textContent = config.label;
            }
        } else {
            nameEl.textContent = 'Select a State';
            valueEl.textContent = '--';
            descEl.textContent = 'Click on a state to view insurance metrics';
        }
    }
    
    // Handle metric toggle
    function handleMetricToggle(metric) {
        console.log('Metric toggled:', metric);
        
        // Update buttons
        var buttons = document.querySelectorAll('.metric-btn');
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].classList.remove('active');
        }
        
        var targetBtn = document.querySelector('[data-metric="' + metric + '"]');
        if (targetBtn) {
            targetBtn.classList.add('active');
        }
        
        // Show/hide WC sub-buttons
        var wcButtons = document.getElementById('wc-sub-buttons');
        if (metric === 'wcRate') {
            wcButtons.classList.add('show');
            currentMetric = 'wcRate' + currentWCCode;
        } else {
            wcButtons.classList.remove('show');
            currentMetric = metric;
        }
        
        updateMapColors();
        updateInfoCard();
    }
    
    // Handle WC code toggle
    function handleWCCodeToggle(code) {
        console.log('WC code toggled:', code);
        
        var buttons = document.querySelectorAll('.wc-sub-btn');
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].classList.remove('active');
        }
        
        var targetBtn = document.querySelector('[data-wc-code="' + code + '"]');
        if (targetBtn) {
            targetBtn.classList.add('active');
        }
        
        currentWCCode = code;
        currentMetric = 'wcRate' + code;
        
        updateMapColors();
        updateInfoCard();
    }
    
    // Add event listeners
    console.log('Adding event listeners...');
    
    // State click listeners
    var states = document.querySelectorAll('.state-path');
    for (var i = 0; i < states.length; i++) {
        (function(state) {
            state.addEventListener('click', function() {
                var code = state.id.replace('state-', '');
                handleStateClick(code);
            });
        })(states[i]);
    }
    console.log('Added listeners to ' + states.length + ' states');
    
    // Metric button listeners
    var metricButtons = document.querySelectorAll('.metric-btn');
    for (var j = 0; j < metricButtons.length; j++) {
        (function(btn) {
            btn.addEventListener('click', function() {
                handleMetricToggle(btn.getAttribute('data-metric'));
            });
        })(metricButtons[j]);
    }
    console.log('Added listeners to ' + metricButtons.length + ' metric buttons');
    
    // WC button listeners
    var wcButtons = document.querySelectorAll('.wc-sub-btn');
    for (var k = 0; k < wcButtons.length; k++) {
        (function(btn) {
            btn.addEventListener('click', function() {
                handleWCCodeToggle(btn.getAttribute('data-wc-code'));
            });
        })(wcButtons[k]);
    }
    console.log('Added listeners to ' + wcButtons.length + ' WC buttons');
    
    // Initialize
    console.log('Initializing map...');
    updateMapColors();
    updateInfoCard();
    console.log('Map initialization complete!');
})();
</script>'''

# Save the complete WordPress HTML
with open('wordpress-complete.html', 'w') as f:
    f.write(wordpress_html)

print("Complete WordPress HTML created successfully in wordpress-complete.html")