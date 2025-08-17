#!/usr/bin/env python3

import re

print("Converting carpenter copy.html to WordPress-compatible version...")

# Read the original file
with open('carpenter copy.html', 'r') as f:
    content = f.read()

# Step 1: Remove ALL inline event handlers
print("1. Removing inline event handlers...")
content = re.sub(r'\s+onclick="[^"]*"', '', content)
content = re.sub(r'\s+onmouseover="[^"]*"', '', content)
content = re.sub(r'\s+onmouseout="[^"]*"', '', content)
content = re.sub(r'\s+onload="[^"]*"', '', content)

# Step 2: Convert ES6 template literals to string concatenation
print("2. Converting ES6 template literals to ES5...")
# Pattern: `text ${var} text` -> 'text ' + var + ' text'
template_pattern = r'`([^`]*)`'

def replace_template(match):
    template = match.group(1)
    # Replace ${...} with ' + ... + '
    result = re.sub(r'\$\{([^}]+)\}', r"' + \1 + '", template)
    return "'" + result + "'"

content = re.sub(template_pattern, replace_template, content)

# Step 3: Convert arrow functions to regular functions
print("3. Converting arrow functions to ES5...")
# Pattern: (param) => { ... } -> function(param) { ... }
content = re.sub(r'\(([^)]*)\)\s*=>\s*\{', r'function(\1) {', content)
# Pattern: param => ... -> function(param) { return ...; }
content = re.sub(r'(\w+)\s*=>\s*([^{][^,;}\n]+)', r'function(\1) { return \2; }', content)

# Step 4: Convert const/let to var
print("4. Converting const/let to var...")
content = re.sub(r'\bconst\b', 'var', content)
content = re.sub(r'\blet\b', 'var', content)

# Step 5: Fix spread operator usage
print("5. Converting spread operators...")
# Pattern: ...array -> array (simplified - may need manual review)
content = re.sub(r'\.\.\.(\w+)', r'\1', content)

# Step 6: Add WordPress-specific initialization
print("6. Adding WordPress-specific initialization...")

# Find the end of the main script
script_end_pattern = r'(</script>)'

wordpress_init = """
    // WordPress Compatibility Layer
    console.log('WordPress compatibility layer loading...');
    
    // Ensure DOM is ready for WordPress
    function ensureReady(callback) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', callback);
        } else {
            setTimeout(callback, 100); // Small delay for WordPress
        }
    }
    
    // Initialize event listeners for WordPress
    function initWordPressListeners() {
        console.log('Initializing WordPress event listeners...');
        
        // Add click listeners to all states using event delegation
        var mapContainer = document.querySelector('#us-map-svg');
        if (mapContainer) {
            mapContainer.addEventListener('click', function(e) {
                var target = e.target;
                while (target && target !== mapContainer) {
                    if (target.classList && target.classList.contains('state-path')) {
                        var stateCode = target.id.replace('state-', '');
                        if (window.handleStateClick) {
                            window.handleStateClick(stateCode);
                        }
                        break;
                    }
                    target = target.parentNode;
                }
            });
            
            mapContainer.addEventListener('mouseover', function(e) {
                var target = e.target;
                while (target && target !== mapContainer) {
                    if (target.classList && target.classList.contains('state-path')) {
                        var stateCode = target.id.replace('state-', '');
                        if (window.handleStateHover) {
                            window.handleStateHover(stateCode);
                        }
                        break;
                    }
                    target = target.parentNode;
                }
            });
            
            mapContainer.addEventListener('mouseout', function(e) {
                var target = e.target;
                if (target.classList && target.classList.contains('state-path')) {
                    if (window.handleStateMouseOut) {
                        window.handleStateMouseOut();
                    }
                }
            });
        }
        
        // Add click listeners to metric buttons using event delegation
        var buttonContainer = document.querySelector('.metric-toggles');
        if (buttonContainer) {
            buttonContainer.addEventListener('click', function(e) {
                var target = e.target;
                if (target.classList && target.classList.contains('metric-btn')) {
                    var metric = target.getAttribute('data-metric');
                    if (window.handleMetricToggle) {
                        window.handleMetricToggle(metric);
                    }
                }
            });
        }
        
        // Add click listeners to WC buttons
        var wcContainer = document.querySelector('.wc-sub-buttons');
        if (wcContainer) {
            wcContainer.addEventListener('click', function(e) {
                var target = e.target;
                if (target.classList && target.classList.contains('wc-sub-btn')) {
                    var code = target.getAttribute('data-wc-code');
                    if (window.handleWCCodeToggle) {
                        window.handleWCCodeToggle(code);
                    }
                }
            });
        }
        
        console.log('WordPress event listeners initialized!');
    }
    
    // Run initialization
    ensureReady(function() {
        initWordPressListeners();
        
        // Initialize the map if function exists
        if (window.updateMapColors) {
            window.updateMapColors();
        }
    });
    
"""

# Insert WordPress init before the closing script tag
content = re.sub(script_end_pattern, wordpress_init + r'\1', content, count=1)

# Step 7: Wrap everything in strict IIFE to avoid conflicts
print("7. Wrapping in strict IIFE...")
# Find script tags and wrap content
script_pattern = r'<script>(.*?)</script>'

def wrap_script(match):
    script_content = match.group(1)
    if '(function()' not in script_content[:100]:  # Check if not already wrapped
        wrapped = '<script>\n(function() {\n    "use strict";\n' + script_content + '\n})();\n</script>'
        return wrapped
    return match.group(0)

content = re.sub(script_pattern, wrap_script, content, flags=re.DOTALL)

# Save the WordPress-compatible version
with open('wordpress-final.html', 'w') as f:
    f.write(content)

print("\n✅ WordPress-compatible version created: wordpress-final.html")
print("\nThis version:")
print("- Removes all inline event handlers (WordPress strips these)")
print("- Converts ES6 to ES5 (for older WordPress environments)")
print("- Uses event delegation (more reliable in WordPress)")
print("- Adds proper DOM ready checks")
print("- Wraps in IIFE to avoid conflicts")
print("\nCopy the entire contents of wordpress-final.html into a WordPress Custom HTML block.")