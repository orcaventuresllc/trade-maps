// Chunk 5: Interactive Features, SVG Map, and Mobile Support
// This code should be added to the main script section

// Tooltip functionality
function showTooltip(event, stateCode) {
    const tooltip = document.getElementById('map-tooltip');
    const metricData = DATA[currentMetric][stateCode];
    const config = METRIC_CONFIG[currentMetric];
    
    if (metricData) {
        const formattedValue = currentMetric === 'glPremiumPct' 
            ? config.format(metricData) 
            : config.format(metricData);
        
        tooltip.querySelector('.tooltip-content').textContent = 
            `${STATE_NAMES[stateCode]}: ${formattedValue}`;
        
        // Position tooltip
        const rect = event.target.getBoundingClientRect();
        const containerRect = document.getElementById('insurance-map-container').getBoundingClientRect();
        
        tooltip.style.left = (rect.left - containerRect.left + rect.width/2) + 'px';
        tooltip.style.top = (rect.top - containerRect.top - 40) + 'px';
        tooltip.style.display = 'block';
    }
}

function hideTooltip() {
    document.getElementById('map-tooltip').style.display = 'none';
}

// Initialize state interactions
function initializeStateInteractions() {
    // Add event listeners to all state paths
    document.querySelectorAll('.state-path').forEach(state => {
        // Extract state code from ID
        const stateCode = state.id.replace('state-', '');
        
        // Hover events (desktop only)
        state.addEventListener('mouseenter', function(e) {
            if (window.innerWidth > 768) {
                showTooltip(e, stateCode);
            }
        });
        
        state.addEventListener('mouseleave', function() {
            hideTooltip();
        });
        
        // Click event
        state.addEventListener('click', function() {
            // Remove previous selection
            document.querySelectorAll('.state-path').forEach(s => {
                s.classList.remove('selected');
            });
            
            // Add selection to clicked state
            this.classList.add('selected');
            selectedState = stateCode;
            
            // Update info card
            updateInfoCard(stateCode);
            
            // Hide tooltip
            hideTooltip();
        });
    });
}

// Create simplified SVG map
function createSVGMap() {
    // This is a simplified SVG - in production, you'd use the full SVG file
    // For now, creating a placeholder with a few states for demonstration
    const svgHTML = `
        <svg viewBox="0 0 959 593" xmlns="http://www.w3.org/2000/svg">
            <style>
                .state-path { 
                    stroke: #fff; 
                    stroke-width: 0.5; 
                    cursor: pointer; 
                    transition: all 0.2s ease;
                }
            </style>
            <g>
                <!-- Simplified state paths - in production, use full paths from Blank_US_Map_(states_only).svg -->
                <!-- California -->
                <path id="state-CA" class="state-path heat-0" d="M 69.4,365.6 L 93.4,382.4 L 93.4,265 L 69.4,265 Z" />
                <!-- Texas -->
                <path id="state-TX" class="state-path heat-0" d="M 400,400 L 500,400 L 500,320 L 400,320 Z" />
                <!-- Florida -->
                <path id="state-FL" class="state-path heat-0" d="M 700,450 L 780,450 L 780,400 L 700,400 Z" />
                <!-- New York -->
                <path id="state-NY" class="state-path heat-0" d="M 800,150 L 850,150 L 850,200 L 800,200 Z" />
                <!-- Add more states as needed -->
            </g>
        </svg>
    `;
    
    document.getElementById('us-map-svg').innerHTML = svgHTML;
}

// Initialize everything when DOM is ready
function initializeMap() {
    // Create the SVG map
    createSVGMap();
    
    // Initialize all functionality
    populateDropdown();
    initializeToggles();
    initializeDropdown();
    initializeStateInteractions();
    
    // Apply initial colors
    updateMapColors();
    
    // Set initial info card state
    updateInfoCard(null);
}

// Wait for DOM to be ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeMap);
} else {
    initializeMap();
}

// IMPORTANT NOTE:
// To use the full US map, replace the createSVGMap() function with code that:
// 1. Loads the content from Blank_US_Map_(states_only).svg
// 2. Processes each <path> element to add:
//    - id="state-XX" where XX is the state code (extracted from class attribute)
//    - class="state-path heat-0"
// 3. Removes unnecessary styling from the original SVG
// 4. Inserts the processed SVG into the #us-map-svg container