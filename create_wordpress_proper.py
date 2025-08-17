#!/usr/bin/env python3

import re

print("Creating proper WordPress-compatible version...")

# Read the working carpenter copy.html
with open('carpenter copy.html', 'r') as f:
    content = f.read()

# Step 1: Remove ONLY the inline event handlers (keep modern JS)
print("1. Removing inline event handlers...")
content = re.sub(r'\s+onclick="[^"]*"', '', content)
content = re.sub(r'\s+onmouseover="[^"]*"', '', content)
content = re.sub(r'\s+onmouseout="[^"]*"', '', content)

# Step 2: Find the script section and modify it
script_start = content.find('<script>')
script_end = content.find('</script>')

if script_start != -1 and script_end != -1:
    original_script = content[script_start:script_end]
    
    # Add WordPress-specific event delegation right before the closing of the main function
    wordpress_additions = """
    
    // ===== WORDPRESS COMPATIBILITY LAYER =====
    console.log('WordPress: Adding event delegation...');
    
    // Remove any existing inline handlers (in case WordPress partially processes them)
    document.querySelectorAll('[onclick]').forEach(el => el.removeAttribute('onclick'));
    document.querySelectorAll('[onmouseover]').forEach(el => el.removeAttribute('onmouseover'));
    document.querySelectorAll('[onmouseout]').forEach(el => el.removeAttribute('onmouseout'));
    
    // Use event delegation for all interactions
    const mapContainer = document.getElementById('us-map-svg');
    if (mapContainer) {
        // Delegate click events
        mapContainer.addEventListener('click', function(e) {
            let target = e.target;
            
            // Handle state path clicks
            if (target.classList.contains('state-path')) {
                const stateCode = target.id.replace('state-', '');
                if (window.handleStateClick) {
                    window.handleStateClick(stateCode);
                }
            }
        });
        
        // Delegate mouseover events  
        mapContainer.addEventListener('mouseover', function(e) {
            let target = e.target;
            
            if (target.classList.contains('state-path')) {
                const stateCode = target.id.replace('state-', '');
                if (window.handleStateHover) {
                    window.handleStateHover(stateCode);
                }
            }
        });
        
        // Delegate mouseout events
        mapContainer.addEventListener('mouseout', function(e) {
            let target = e.target;
            
            if (target.classList.contains('state-path')) {
                if (window.handleStateMouseOut) {
                    window.handleStateMouseOut();
                }
            }
        });
    }
    
    // Delegate metric button clicks
    const metricContainer = document.querySelector('.metric-toggles');
    if (metricContainer) {
        metricContainer.addEventListener('click', function(e) {
            const btn = e.target.closest('.metric-btn');
            if (btn) {
                const metric = btn.getAttribute('data-metric');
                if (window.handleMetricToggle) {
                    window.handleMetricToggle(metric);
                }
            }
        });
    }
    
    // Delegate WC sub-button clicks
    const wcContainer = document.querySelector('.wc-sub-buttons');
    if (wcContainer) {
        wcContainer.addEventListener('click', function(e) {
            const btn = e.target.closest('.wc-sub-btn');
            if (btn) {
                const code = btn.getAttribute('data-wc-code');
                if (window.handleWCCodeToggle) {
                    window.handleWCCodeToggle(code);
                }
            }
        });
    }
    
    // Handle Kadence tabs/accordions - reinitialize when map becomes visible
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && entry.intersectionRatio > 0) {
                    console.log('WordPress: Map became visible, updating colors...');
                    if (window.updateMapColors) {
                        window.updateMapColors();
                    }
                    // Only need to initialize once
                    observer.disconnect();
                }
            });
        }, { threshold: 0.1 });
        
        const mapElement = document.getElementById('insurance-map-container');
        if (mapElement) {
            observer.observe(mapElement);
        }
    }
    
    console.log('WordPress: Event delegation complete!');
    // ===== END WORDPRESS COMPATIBILITY LAYER =====
"""
    
    # Insert the WordPress additions before the last closing braces
    # Find the pattern that indicates the end of the main initialization
    last_brace_pattern = r'(\s*console\.log\([^)]*\);\s*)(}\)\(\);)'
    
    if re.search(last_brace_pattern, original_script):
        modified_script = re.sub(
            last_brace_pattern,
            r'\1' + wordpress_additions + r'\n\2',
            original_script
        )
    else:
        # Fallback: insert before the last })();
        last_close = original_script.rfind('})();')
        if last_close != -1:
            modified_script = (
                original_script[:last_close] + 
                wordpress_additions + '\n' +
                original_script[last_close:]
            )
        else:
            modified_script = original_script + wordpress_additions
    
    # Replace the script section
    content = content[:script_start] + modified_script + '</script>' + content[script_end + 9:]

# Step 3: Add CSS to ensure proper container height for Kadence
css_addition = """
<style>
/* WordPress/Kadence Compatibility Styles */
#insurance-map-container {
    min-height: 600px; /* Ensure container has height even in tabs */
}

#us-map-svg {
    width: 100%;
    height: auto;
    min-height: 400px; /* Prevent collapse in hidden tabs */
}

/* Ensure map is visible even in Kadence tabs/accordions */
.kt-tabs-content-wrap #insurance-map-container,
.kt-accordion-panel #insurance-map-container {
    display: block !important;
    visibility: visible !important;
}
</style>
"""

# Add the CSS right before the main container div
container_pattern = r'(<div id="insurance-map-container")'
content = re.sub(container_pattern, css_addition + r'\n\1', content)

# Save the result
with open('wordpress-proper.html', 'w') as f:
    f.write(content)

print("\n✅ Created wordpress-proper.html")
print("\nThis version:")
print("✓ Removes inline event handlers (WordPress strips these)")
print("✓ Keeps modern JavaScript (no unnecessary ES5 conversion)")  
print("✓ Uses event delegation for all interactions")
print("✓ Handles Kadence tabs/accordions with IntersectionObserver")
print("✓ Ensures proper container height")
print("✓ Preserves the complete working SVG map")
print("\nCopy the entire contents into a WordPress Custom HTML block.")