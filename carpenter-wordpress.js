console.log('Insurance map script starting...');

(function() {
    try {
        console.log('Map initialization function executing...');
        
        // Data definitions for carpenter insurance metrics
        window.DATA = {
        glPremiumPct: {
            AL: { min: 2.8, max: 5.0, midpoint: 3.9, range: "2.8% – 5.0%" },
            AK: { min: 3.2, max: 5.8, midpoint: 4.5, range: "3.2% – 5.8%" },
            AZ: { min: 2.5, max: 4.7, midpoint: 3.6, range: "2.5% – 4.7%" },
            AR: { min: 2.7, max: 4.9, midpoint: 3.8, range: "2.7% – 4.9%" },
            CA: { min: 3.1, max: 5.5, midpoint: 4.3, range: "3.1% – 5.5%" },
            CO: { min: 2.4, max: 4.6, midpoint: 3.5, range: "2.4% – 4.6%" },
            CT: { min: 3.0, max: 5.2, midpoint: 4.1, range: "3.0% – 5.2%" },
            DE: { min: 2.6, max: 4.8, midpoint: 3.7, range: "2.6% – 4.8%" },
            FL: { min: 3.3, max: 5.7, midpoint: 4.5, range: "3.3% – 5.7%" },
            GA: { min: 2.8, max: 5.0, midpoint: 3.9, range: "2.8% – 5.0%" },
            HI: { min: 3.5, max: 5.9, midpoint: 4.7, range: "3.5% – 5.9%" },
            ID: { min: 2.3, max: 4.5, midpoint: 3.4, range: "2.3% – 4.5%" },
            IL: { min: 2.9, max: 5.1, midpoint: 4.0, range: "2.9% – 5.1%" },
            IN: { min: 2.6, max: 4.8, midpoint: 3.7, range: "2.6% – 4.8%" },
            IA: { min: 2.4, max: 4.6, midpoint: 3.5, range: "2.4% – 4.6%" },
            KS: { min: 2.6, max: 4.8, midpoint: 3.7, range: "2.6% – 4.8%" },
            KY: { min: 2.8, max: 5.0, midpoint: 3.9, range: "2.8% – 5.0%" },
            LA: { min: 3.0, max: 5.2, midpoint: 4.1, range: "3.0% – 5.2%" },
            ME: { min: 2.6, max: 4.8, midpoint: 3.7, range: "2.6% – 4.8%" },
            MD: { min: 2.8, max: 5.0, midpoint: 3.9, range: "2.8% – 5.0%" },
            MA: { min: 3.0, max: 5.2, midpoint: 4.1, range: "3.0% – 5.2%" },
            MI: { min: 2.8, max: 5.0, midpoint: 3.9, range: "2.8% – 5.0%" },
            MN: { min: 2.6, max: 4.8, midpoint: 3.7, range: "2.6% – 4.8%" },
            MS: { min: 2.9, max: 5.1, midpoint: 4.0, range: "2.9% – 5.1%" },
            MO: { min: 2.6, max: 4.8, midpoint: 3.7, range: "2.6% – 4.8%" },
            MT: { min: 2.4, max: 4.6, midpoint: 3.5, range: "2.4% – 4.6%" },
            NE: { min: 2.4, max: 4.6, midpoint: 3.5, range: "2.4% – 4.6%" },
            NV: { min: 2.9, max: 5.1, midpoint: 4.0, range: "2.9% – 5.1%" },
            NH: { min: 2.6, max: 4.8, midpoint: 3.7, range: "2.6% – 4.8%" },
            NJ: { min: 3.1, max: 5.5, midpoint: 4.3, range: "3.1% – 5.5%" },
            NM: { min: 2.8, max: 5.0, midpoint: 3.9, range: "2.8% – 5.0%" },
            NY: { min: 3.3, max: 5.7, midpoint: 4.5, range: "3.3% – 5.7%" },
            NC: { min: 2.6, max: 4.8, midpoint: 3.7, range: "2.6% – 4.8%" },
            ND: { min: 2.4, max: 4.6, midpoint: 3.5, range: "2.4% – 4.6%" },
            OH: { min: 2.8, max: 5.0, midpoint: 3.9, range: "2.8% – 5.0%" },
            OK: { min: 2.6, max: 4.8, midpoint: 3.7, range: "2.6% – 4.8%" },
            OR: { min: 2.6, max: 4.8, midpoint: 3.7, range: "2.6% – 4.8%" },
            PA: { min: 2.9, max: 5.1, midpoint: 4.0, range: "2.9% – 5.1%" },
            RI: { min: 3.0, max: 5.2, midpoint: 4.1, range: "3.0% – 5.2%" },
            SC: { min: 2.8, max: 5.0, midpoint: 3.9, range: "2.8% – 5.0%" },
            SD: { min: 2.4, max: 4.6, midpoint: 3.5, range: "2.4% – 4.6%" },
            TN: { min: 2.8, max: 5.0, midpoint: 3.9, range: "2.8% – 5.0%" },
            TX: { min: 2.9, max: 5.1, midpoint: 4.0, range: "2.9% – 5.1%" },
            UT: { min: 2.4, max: 4.6, midpoint: 3.5, range: "2.4% – 4.6%" },
            VT: { min: 2.6, max: 4.8, midpoint: 3.7, range: "2.6% – 4.8%" },
            VA: { min: 2.8, max: 5.0, midpoint: 3.9, range: "2.8% – 5.0%" },
            WA: { min: 2.8, max: 5.0, midpoint: 3.9, range: "2.8% – 5.0%" },
            WV: { min: 2.9, max: 5.1, midpoint: 4.0, range: "2.9% – 5.1%" },
            WI: { min: 2.6, max: 4.8, midpoint: 3.7, range: "2.6% – 4.8%" },
            WY: { min: 2.4, max: 4.6, midpoint: 3.5, range: "2.4% – 4.6%" }
        },
        
        glSavingsPct: {
            AL: 18, AK: 22, AZ: 20, AR: 19, CA: 25, CO: 21, CT: 23, DE: 20, FL: 26, GA: 19,
            HI: 24, ID: 18, IL: 22, IN: 20, IA: 19, KS: 20, KY: 19, LA: 21, ME: 20, MD: 21,
            MA: 24, MI: 21, MN: 20, MS: 19, MO: 20, MT: 18, NE: 19, NV: 22, NH: 20, NJ: 25,
            NM: 20, NY: 26, NC: 20, ND: 18, OH: 21, OK: 20, OR: 21, PA: 22, RI: 23, SC: 19,
            SD: 18, TN: 19, TX: 21, UT: 19, VT: 20, VA: 21, WA: 22, WV: 20, WI: 20, WY: 18
        },
        
        glCompetitiveness: {
            AL: 65, AK: 45, AZ: 75, AR: 60, CA: 85, CO: 80, CT: 70, DE: 65, FL: 90, GA: 75,
            HI: 50, ID: 55, IL: 80, IN: 70, IA: 60, KS: 65, KY: 60, LA: 65, ME: 55, MD: 75,
            MA: 80, MI: 75, MN: 70, MS: 55, MO: 70, MT: 50, NE: 60, NV: 70, NH: 65, NJ: 85,
            NM: 60, NY: 85, NC: 75, ND: 50, OH: 80, OK: 65, OR: 75, PA: 80, RI: 70, SC: 70,
            SD: 55, TN: 70, TX: 85, UT: 65, VT: 60, VA: 75, WA: 80, WV: 55, WI: 70, WY: 50
        },
        
        // Workers' Comp Rate per $100 of payroll - Class 5437 (Carpentry-framing)
        wcRate5437: {
            AL: 6.14, AK: 6.16, AZ: 4.05, AR: 3.26, CA: 5.62, CO: 4.74, CT: 7.86,
            DE: 5.00, FL: 6.23, GA: 8.98, HI: 6.03, ID: 6.58, IL: 9.75,
            IN: 2.83, IA: 5.71, KS: 4.55, KY: 3.87, LA: 9.60, ME: 6.61, MD: 5.50,
            MA: 6.75, MI: 5.88, MN: 8.41, MS: 6.50, MO: 5.44, MT: 5.52, NE: 4.31,
            NV: 8.71, NH: 5.30, NJ: 7.79, NM: 5.17, NY: 8.50, NC: 3.96, ND: 5.45,
            OH: 4.56, OK: 6.37, OR: 5.43, PA: 7.07, RI: 6.19, SC: 5.31, SD: 4.99,
            TN: 3.93, TX: 3.55, UT: 4.39, VT: 7.55, VA: 5.46, WA: 4.67, WV: 2.74,
            WI: 10.03, WY: 3.48
        },
        wcRate5645: {
            AL: 14.07, AK: 9.78, AZ: 10.17, AR: 6.33, CA: 8.46, CO: 7.40, CT: 17.17,
            DE: 9.06, FL: 12.61, GA: 43.42, HI: 10.60, ID: 12.93, IL: 19.23,
            IN: 5.56, IA: 9.65, KS: 10.53, KY: 9.81, LA: 17.76, ME: 10.58, MD: 7.23,
            MA: 11.44, MI: 11.01, MN: 13.70, MS: 11.55, MO: 8.69, MT: 8.79, NE: 7.15,
            NV: 12.58, NH: 9.35, NJ: 13.29, NM: 8.99, NY: 13.37, NC: 6.81, ND: 8.44,
            OH: 8.20, OK: 10.79, OR: 8.84, PA: 12.14, RI: 10.12, SC: 8.38, SD: 8.01,
            TN: 6.95, TX: 6.78, UT: 7.50, VT: 11.26, VA: 8.53, WA: 7.98, WV: 5.94,
            WI: 15.76, WY: 6.42
        }
    };
    
    // State names mapping
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
    
    // Metric configurations
    window.METRIC_CONFIG = {
        glPremiumPct: {
            label: "GL Premium as % of Revenue",
            format: function(data) { return data.range; },
            description: "General Liability insurance premium as a percentage of contractor revenue",
            reverseScale: false
        },
        glSavingsPct: {
            label: "GL Savings as % of Premium",
            format: function(val) { return val + '%'; },
            description: "Potential savings on General Liability insurance premiums",
            reverseScale: false
        },
        glCompetitiveness: {
            label: "GL Carrier Competitiveness",
            format: function(val) { return val + 'th percentile'; },
            description: "Market competitiveness ranking based on number of carrier quotes",
            reverseScale: false
        },
        wcRate5437: {
            label: "WC Rate per $100 (Class 5437)",
            format: function(val) { return '$' + val.toFixed(2); },
            description: "Workers' Comp rate for Class Code 5437 (Carpentry-framing)",
            reverseScale: true
        },
        wcRate5645: {
            label: "WC Rate per $100 (Class 5645)",
            format: function(val) { return '$' + val.toFixed(2); },
            description: "Workers' Comp rate for Class Code 5645 (Carpentry-interior)",
            reverseScale: true
        }
    };
    
    // Application State
    window.currentMetric = 'glPremiumPct';
    window.currentWCCode = '5437';
    window.selectedState = null;
    
    // Hawaii multi-element fixes
    function normalizeStateCode(stateCode) {
        // Remove any suffix after dash (e.g., HI-2 -> HI)
        return stateCode.split('-')[0];
    }
    
    function getStateEls(stateCode) {
        // Return all elements for a state including multi-part states like Hawaii
        var normalized = normalizeStateCode(stateCode);
        var elements = document.querySelectorAll('[id^="state-' + normalized + '"]');
        return Array.prototype.slice.call(elements);
    }
    
    // Color calculation functions
    function getHeatmapColor(value, min, max, reverseScale) {
        if (value == null || min == null || max == null) {
            return 'heat-0';
        }
        
        reverseScale = reverseScale || false;
        
        var normalized = (value - min) / (max - min);
        
        if (reverseScale) {
            normalized = 1 - normalized;
        }
        
        var heatLevel = Math.floor(normalized * 8);
        return 'heat-' + Math.min(7, Math.max(0, heatLevel));
    }
    
    window.updateMapColors = function() {
        console.log('Updating map colors for metric:', window.currentMetric);
        var metricData = window.DATA[window.currentMetric];
        var config = window.METRIC_CONFIG[window.currentMetric];
        
        if (!metricData || !config) return;
        
        var values = [];
        for (var state in metricData) {
            if (metricData.hasOwnProperty(state)) {
                var val = window.currentMetric === 'glPremiumPct' ? metricData[state].midpoint : metricData[state];
                values.push(val);
            }
        }
        
        var min = Math.min.apply(Math, values);
        var max = Math.max.apply(Math, values);
        
        for (var state in metricData) {
            if (metricData.hasOwnProperty(state)) {
                // Get all elements for this state (handles Hawaii's multiple islands)
                var stateElements = getStateEls(state);
                
                for (var i = 0; i < stateElements.length; i++) {
                    var element = stateElements[i];
                    
                    // Remove all heat classes
                    for (var j = 0; j <= 7; j++) {
                        element.classList.remove('heat-' + j);
                    }
                    
                    var val = window.currentMetric === 'glPremiumPct' ? metricData[state].midpoint : metricData[state];
                    var colorClass = getHeatmapColor(val, min, max, config.reverseScale);
                    element.classList.add(colorClass);
                }
            }
        }
        
        updateLegend(config);
    };
    
    function updateLegend(config) {
        var legendMin = document.querySelector('.legend-min');
        var legendMax = document.querySelector('.legend-max');
        
        if (!legendMin || !legendMax || !config) return;
        
        if (config.reverseScale) {
            legendMin.textContent = 'Better';
            legendMax.textContent = 'Worse';
        } else {
            legendMin.textContent = 'Low';
            legendMax.textContent = 'High';
        }
    }
    
    window.updateInfoCard = function(stateCode) {
        var stateName = window.STATE_NAMES[stateCode];
        var metricData = stateCode && window.DATA[window.currentMetric] ? window.DATA[window.currentMetric][stateCode] : null;
        var config = window.METRIC_CONFIG[window.currentMetric];
        
        var nameElement = document.querySelector('.info-card .state-name');
        if (nameElement) {
            nameElement.textContent = stateName || 'Select a State';
        }
        
        var valueElement = document.querySelector('.info-card .metric-value');
        if (valueElement) {
            if (metricData && config) {
                var formattedValue = window.currentMetric === 'glPremiumPct' 
                    ? config.format(metricData) 
                    : config.format(metricData);
                valueElement.textContent = formattedValue;
            } else {
                valueElement.textContent = '--';
            }
        }
        
        var descElement = document.querySelector('.info-card .metric-description');
        if (descElement && config) {
            descElement.textContent = stateCode ? config.description : 'Click on a state to view insurance metrics';
        }
        
        var ctaLink = document.querySelector('.info-card .cta-link');
        if (ctaLink) {
            if (stateCode && stateName) {
                ctaLink.href = 'https://app.contractornerd.com/';
                ctaLink.textContent = 'Get Free Quotes for ' + stateName + ' →';
                ctaLink.style.display = 'inline-block';
            } else {
                ctaLink.style.display = 'none';
            }
        }
    };
    
    window.handleMetricToggle = function(metric) {
        var buttons = document.querySelectorAll('.metric-btn');
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].classList.remove('active');
        }
        
        var targetBtn = document.querySelector('[data-metric="' + metric + '"]');
        if (targetBtn) {
            targetBtn.classList.add('active');
        }
        
        var wcSubButtons = document.getElementById('wc-sub-buttons');
        if (metric === 'wcRate') {
            wcSubButtons.classList.add('show');
            window.currentMetric = 'wcRate' + window.currentWCCode;
        } else {
            wcSubButtons.classList.remove('show');
            window.currentMetric = metric;
        }
        
        window.updateMapColors();
        
        if (window.selectedState) {
            window.updateInfoCard(window.selectedState);
        }
    };
    
    window.handleWCCodeToggle = function(code) {
        var buttons = document.querySelectorAll('.wc-sub-btn');
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].classList.remove('active');
        }
        
        var btn = document.querySelector('[data-wc-code="' + code + '"]');
        if (btn) btn.classList.add('active');
        window.currentWCCode = code;
        window.currentMetric = 'wcRate' + code;
        window.updateMapColors();
        if (window.selectedState) window.updateInfoCard(window.selectedState);
    };
    
    function populateDropdown() {
        var dropdown = document.getElementById('state-dropdown');
        if (!dropdown) return;
        
        var stateEntries = [];
        for (var code in window.STATE_NAMES) {
            if (window.STATE_NAMES.hasOwnProperty(code)) {
                stateEntries.push([code, window.STATE_NAMES[code]]);
            }
        }
        
        stateEntries.sort(function(a, b) {
            return a[1].localeCompare(b[1]);
        });
        
        for (var i = 0; i < stateEntries.length; i++) {
            var code = stateEntries[i][0];
            var name = stateEntries[i][1];
            var option = document.createElement('option');
            option.value = code;
            option.textContent = name;
            dropdown.appendChild(option);
        }
    }
    
    function initializeToggles() {
        var buttons = document.querySelectorAll('.metric-btn');
        for (var i = 0; i < buttons.length; i++) {
            var btn = buttons[i];
            btn.addEventListener('click', function() {
                window.handleMetricToggle(this.dataset.metric);
            });
        }
        
        var wcButtons = document.querySelectorAll('.wc-sub-btn');
        for (var j = 0; j < wcButtons.length; j++) {
            var wcBtn = wcButtons[j];
            wcBtn.addEventListener('click', function() {
                window.handleWCCodeToggle(this.dataset.wcCode);
            });
        }
    }
    
    function initializeDropdown() {
        var dropdown = document.getElementById('state-dropdown');
        if (dropdown) {
            dropdown.addEventListener('change', function() {
                if (this.value) {
                    window.selectedState = this.value;
                    window.updateInfoCard(this.value);
                }
            });
        }
    }
    
    window.showTooltip = function(event, stateCode) {
        var normalizedCode = normalizeStateCode(stateCode);
        var tooltip = document.getElementById('map-tooltip');
        var metricData = window.DATA[window.currentMetric] && window.DATA[window.currentMetric][normalizedCode] ? window.DATA[window.currentMetric][normalizedCode] : null;
        var config = window.METRIC_CONFIG[window.currentMetric];
        
        if (metricData && tooltip && config) {
            var formattedValue = window.currentMetric === 'glPremiumPct' 
                ? config.format(metricData) 
                : config.format(metricData);
            
            var stateNameEl = tooltip.querySelector('.state-name');
            var metricLabelEl = tooltip.querySelector('.metric-label');
            var metricValueEl = tooltip.querySelector('.metric-value');
            
            if (stateNameEl) stateNameEl.textContent = window.STATE_NAMES[normalizedCode] || '';
            if (metricLabelEl) metricLabelEl.textContent = config.label || '';
            if (metricValueEl) metricValueEl.textContent = formattedValue || '';
            
            var rect = event.target.getBoundingClientRect();
            var mapWrapper = document.querySelector('.map-wrapper');
            if (!mapWrapper) return;
            
            var wrapperRect = mapWrapper.getBoundingClientRect();
            
            var left = rect.right - wrapperRect.left + 10;
            var top = rect.top - wrapperRect.top + (rect.height / 2) - 40;
            
            var tooltipWidth = 220;
            if (left + tooltipWidth > wrapperRect.width) {
                left = rect.left - wrapperRect.left - tooltipWidth - 10;
            }
            if (top < 10) top = 10;
            
            tooltip.style.left = left + 'px';
            tooltip.style.top = top + 'px';
            tooltip.style.display = 'block';
        }
    };
    
    window.hideTooltip = function() {
        var tooltip = document.getElementById('map-tooltip');
        if (tooltip) {
            tooltip.style.display = 'none';
        }
    };
    
    window.handleStateClick = function(stateCode) {
        var normalizedCode = normalizeStateCode(stateCode);
        
        // Get all elements for this state (handles Hawaii's multiple islands)
        var stateElements = getStateEls(normalizedCode);
        
        if (stateElements.length === 0) return;
        
        var isAlreadySelected = stateElements[0].classList.contains('selected');
        
        // Clear all selections
        var allStates = document.querySelectorAll('.state-path');
        for (var i = 0; i < allStates.length; i++) {
            allStates[i].classList.remove('selected');
        }
        
        if (isAlreadySelected) {
            window.selectedState = null;
            window.updateInfoCard(null);
        } else {
            // Select all elements for this state
            for (var j = 0; j < stateElements.length; j++) {
                stateElements[j].classList.add('selected');
            }
            window.selectedState = normalizedCode;
            window.updateInfoCard(normalizedCode);
        }
        
        window.hideTooltip();
    };
    
    window.handleStateHover = function(event, stateCode) {
        if (window.innerWidth > 768) {
            window.showTooltip(event, stateCode);
        }
    };
    
    window.handleStateLeave = function() {
        window.hideTooltip();
    };
    
    function initializeStateInteractions() {
        console.log('Initializing state interactions...');
        var states = document.querySelectorAll('.state-path');
        
        for (var i = 0; i < states.length; i++) {
            var state = states[i];
            var stateCode = normalizeStateCode(state.id.replace('state-', ''));
            
            state.addEventListener('click', function(code) {
                return function() {
                    window.handleStateClick(code);
                };
            }(stateCode));
            
            state.addEventListener('mouseover', function(code) {
                return function(e) {
                    window.handleStateHover(e, code);
                };
            }(stateCode));
            
            state.addEventListener('mouseout', function() {
                window.handleStateLeave();
            });
            
            state.style.cursor = 'pointer';
            state.style.pointerEvents = 'all';
        }
    }
    
    function initializeMap() {
        if (window.mapInitialized) return;
        window.mapInitialized = true;
        
        console.log('Initializing map with robust pattern...');
        initializeStateInteractions();
        window.updateMapColors();
        populateDropdown();
        initializeToggles();
        initializeDropdown();
        window.updateInfoCard(null);
    }
    
    // WordPress robust initialization with polling - no early returns
    function tryInit() {
        console.log('Trying initialization...');
        if (window.mapInitialized) {
            console.log('Map already initialized');
            return;
        }
        var root = document.getElementById('insurance-map-container');
        if (!root) {
            console.log('Container not found yet');
            return;
        }
        console.log('Container found, initializing map');
        initializeMap();
    }
    
    // Try now if ready, otherwise wait
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', tryInit);
    } else {
        tryInit();
    }
    window.addEventListener('load', tryInit);
    
    // Poll for async content (WordPress often loads blocks later)
    var initPoll = setInterval(function() {
        if (window.mapInitialized) {
            clearInterval(initPoll);
            return;
        }
        tryInit();
    }, 300);
    
    // Stop polling after 5 seconds
    setTimeout(function() { 
        clearInterval(initPoll); 
    }, 5000);
    
    } catch (error) {
        // Log error if console exists
        if (typeof console !== 'undefined' && console.error) {
            console.error('Map initialization error:', error);
        }
    }
})();