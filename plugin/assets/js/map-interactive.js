/**
 * Insurance Cost Maps - Interactive JavaScript
 * Handles map interactivity, state selection, and metric toggling
 * ES5 compatible for WordPress
 */

// Pure ES5 JavaScript - WordPress Safe
(function() {
    'use strict';

    // Data will be injected by PHP via insuranceMapData global variable
    // Structure: { glPremiumRanges: {...}, stateData: {...} }

    var glPremiumRanges = window.insuranceMapData ? window.insuranceMapData.glPremiumRanges : {};
    var stateData = window.insuranceMapData ? window.insuranceMapData.stateData : {};

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
    var currentWCCode = '5437';
    var selectedState = null;

    // Update colors
    function updateColors() {
        // Handle WC Rate which has two sub-options
        var metricKey = currentMetric;
        if (currentMetric === 'wcRate') {
            metricKey = 'wcRate' + currentWCCode;
        }

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

    // Show tooltip on hover with error handling
    function showTooltip(event, stateCode) {
        try {
            var tooltip = document.getElementById('map-tooltip');
            if (!tooltip) return;

            var stateName = stateNames[stateCode];
            if (!stateName) return;

            // Get metric data
            var metricKey = currentMetric;
            if (currentMetric === 'wcRate') {
                metricKey = 'wcRate' + currentWCCode;
            }

            var value = stateData[metricKey] ? stateData[metricKey][stateCode] : undefined;

            // Update tooltip content with null checks
            var stateNameEl = tooltip.querySelector('.state-name');
            if (stateNameEl) {
                stateNameEl.textContent = stateName;
            }

            // Set metric label
            var metricLabel = '';
            if (currentMetric === 'glPremium') {
                metricLabel = 'GL Premium % of Revenue';
            } else if (currentMetric === 'glSavings') {
                metricLabel = 'GL Savings %';
            } else if (currentMetric === 'glCompetitiveness') {
                metricLabel = 'GL Carrier Competitiveness';
            } else if (currentMetric === 'wcRate') {
                metricLabel = 'WC Rate per $100';
            }

            var metricLabelEl = tooltip.querySelector('.metric-label');
            if (metricLabelEl) {
                metricLabelEl.textContent = metricLabel;
            }

            // Format value
            var formattedValue = '--';
            if (value !== undefined) {
                if (currentMetric === 'glPremium') {
                    // Show range for GL Premium
                    formattedValue = glPremiumRanges[stateCode] || value + '%';
                } else if (currentMetric === 'glSavings') {
                    formattedValue = value + '%';
                } else if (currentMetric === 'glCompetitiveness') {
                    formattedValue = value + 'th percentile';
                } else if (currentMetric === 'wcRate') {
                    formattedValue = '$' + value.toFixed(2);
                }
            }

            var metricValueEl = tooltip.querySelector('.metric-value');
            if (metricValueEl) {
                metricValueEl.textContent = formattedValue;
            }

            // Position tooltip near cursor
            var wrapper = document.querySelector('.map-wrapper');
            if (!wrapper) return;

            var containerRect = wrapper.getBoundingClientRect();

            // Position relative to cursor position
            var left = event.clientX - containerRect.left + 15;
            var top = event.clientY - containerRect.top - 10;

            // Adjust if would go off screen
            if (left + 220 > containerRect.width) {
                left = event.clientX - containerRect.left - 235;
            }

            if (left < 10) left = 10;
            if (top < 10) top = 10;

            tooltip.style.left = left + 'px';
            tooltip.style.top = top + 'px';
            tooltip.style.display = 'block';
        } catch (e) {
            // Silently fail - don't break the map
        }
    }

    // Hide tooltip with error handling
    function hideTooltip() {
        try {
            var tooltip = document.getElementById('map-tooltip');
            if (tooltip) {
                tooltip.style.display = 'none';
            }
        } catch (e) {
            // Silently fail
        }
    }

    // Handle state hover with error handling
    function handleStateHover(event) {
        try {
            var target = event.target;
            if (!target || !target.classList || !target.classList.contains('state-path')) {
                return;
            }

            var stateCode = target.id ? target.id.replace('state-', '') : '';
            if (stateCode) {
                showTooltip(event, stateCode);
            }
        } catch (e) {
            // Silently fail
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
        var nameEl = document.querySelector('.info-card .state-name');
        var valueEl = document.querySelector('.info-card .metric-value');
        var descEl = document.querySelector('.info-card .metric-description');
        var ctaEl = document.querySelector('.info-card .cta-link');

        if (!nameEl || !valueEl) return;

        if (stateCode) {
            var stateName = stateNames[stateCode] || stateCode;
            nameEl.textContent = stateName;

            // Get the correct data based on metric
            var metricKey = currentMetric;
            if (currentMetric === 'wcRate') {
                metricKey = 'wcRate' + currentWCCode;
            }

            var value = stateData[metricKey][stateCode];
            if (value !== undefined) {
                if (currentMetric === 'glPremium') {
                    valueEl.textContent = glPremiumRanges[stateCode] || value + '%';
                } else if (currentMetric === 'glSavings') {
                    valueEl.textContent = value + '%';
                } else if (currentMetric === 'glCompetitiveness') {
                    valueEl.textContent = value + 'th percentile';
                } else if (currentMetric === 'wcRate') {
                    valueEl.textContent = '$' + value.toFixed(2);
                }
            } else {
                valueEl.textContent = '--';
            }

            // Update description
            if (descEl) {
                if (currentMetric === 'glPremium') {
                    descEl.textContent = 'General Liability insurance premium as a percentage of contractor revenue';
                } else if (currentMetric === 'glSavings') {
                    descEl.textContent = 'Potential savings on General Liability insurance premiums';
                } else if (currentMetric === 'glCompetitiveness') {
                    descEl.textContent = 'Market competitiveness ranking based on number of carrier quotes';
                } else if (currentMetric === 'wcRate') {
                    descEl.textContent = 'Workers Compensation rate per $100 of payroll';
                }
            }

            // Update CTA button
            if (ctaEl) {
                ctaEl.href = 'https://app.contractornerd.com/';
                ctaEl.innerHTML = 'Get Free Quotes for<br>' + stateName + ' →';
                ctaEl.style.display = 'inline-block';
            }
        } else {
            nameEl.textContent = 'Select a State';
            valueEl.textContent = '--';
            if (descEl) {
                descEl.textContent = 'Click on a state to view insurance metrics';
            }
            if (ctaEl) {
                ctaEl.style.display = 'none';
            }
        }
    }

    // Handle metric button click
    function handleMetricClick(event) {
        var target = event.target;

        if (!target.classList || !target.classList.contains('metric-btn')) {
            return;
        }

        var metric = target.getAttribute('data-metric');

        // Update active button
        var buttons = document.querySelectorAll('.metric-btn');
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].classList.remove('active');
        }
        target.classList.add('active');

        // Show/hide WC sub-buttons
        var wcButtons = document.getElementById('wc-sub-buttons');
        if (metric === 'wcRate') {
            wcButtons.style.display = 'flex';
        } else {
            wcButtons.style.display = 'none';
        }

        // Update metric and colors
        currentMetric = metric;
        updateColors();

        // Update info if state selected
        if (selectedState) {
            updateInfo(selectedState);
        }
    }

    // Handle WC sub-button click
    function handleWCClick(event) {
        var target = event.target;

        if (!target.classList || !target.classList.contains('wc-sub-btn')) {
            return;
        }

        var code = target.getAttribute('data-wc-code');

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

    // Populate mobile dropdown with all states
    function populateDropdown() {
        var dropdown = document.getElementById('state-dropdown');
        if (!dropdown) return;

        // Sort states alphabetically
        var sortedStates = [];
        for (var code in stateNames) {
            if (stateNames.hasOwnProperty(code)) {
                sortedStates.push([code, stateNames[code]]);
            }
        }
        sortedStates.sort(function(a, b) {
            return a[1].localeCompare(b[1]);
        });

        // Add each state as an option
        for (var i = 0; i < sortedStates.length; i++) {
            var option = document.createElement('option');
            option.value = sortedStates[i][0];
            option.textContent = sortedStates[i][1];
            dropdown.appendChild(option);
        }
    }

    // Handle mobile dropdown selection
    function handleDropdownChange(event) {
        var stateCode = event.target.value;
        if (stateCode) {
            selectedState = stateCode;
            updateInfo(stateCode);
        }
    }

    // Initialize everything
    function init() {
        try {
            // Check if data is available
            if (!window.insuranceMapData) {
                return;
            }

            // Get the hidden SVG
            var hiddenSvg = document.querySelector('#hidden-svg-source svg');
            var container = document.getElementById('map-svg-container');

            if (!hiddenSvg) {
                return;
            }

            if (!container) {
                return;
            }

            // Clone the SVG and insert it into the visible container
            var svgClone = hiddenSvg.cloneNode(true);
            container.appendChild(svgClone);

            // Add click listener to map container (event delegation)
            container.addEventListener('click', handleStateClick);

            // Add hover listeners for tooltips
            container.addEventListener('mouseover', handleStateHover);
            container.addEventListener('mouseout', hideTooltip);

            // Add click listener to buttons container (event delegation)
            var buttonContainer = document.querySelector('.metric-toggles');
            if (buttonContainer) {
                buttonContainer.addEventListener('click', handleMetricClick);
            }

            // Add click listener to WC sub-buttons
            var wcContainer = document.getElementById('wc-sub-buttons');
            if (wcContainer) {
                wcContainer.addEventListener('click', handleWCClick);
            }

            // Initialize mobile dropdown
            populateDropdown();
            var dropdown = document.getElementById('state-dropdown');
            if (dropdown) {
                dropdown.addEventListener('change', handleDropdownChange);
            }

            // Initial color update
            updateColors();

        } catch (error) {
            // Silent fail
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
