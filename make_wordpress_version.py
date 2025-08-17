#!/usr/bin/env python3

import re

# Read the working carpenter copy.html
with open('carpenter copy.html', 'r') as f:
    content = f.read()

# Remove all inline event handlers
content = re.sub(r'\s+onclick="[^"]*"', '', content)
content = re.sub(r'\s+onmouseover="[^"]*"', '', content)
content = re.sub(r'\s+onmouseout="[^"]*"', '', content)

# Fix the script to use addEventListener instead of inline handlers
# Find the script section and update it
script_start = content.find('<script>')
script_end = content.find('</script>') + 9

if script_start != -1 and script_end != -1:
    # Keep everything before and after script as is
    before_script = content[:script_start]
    after_script = content[script_end:]
    
    # Add the addEventListener code at the end of the existing script
    additional_js = '''
    // WordPress compatibility - Add event listeners since inline handlers are stripped
    console.log('Adding WordPress event listeners...');
    
    // Add click listeners to all states
    var states = document.querySelectorAll('.state-path');
    for (var i = 0; i < states.length; i++) {
        (function(state) {
            state.addEventListener('click', function() {
                var stateCode = state.id.replace('state-', '');
                if (window.handleStateClick) {
                    window.handleStateClick(stateCode);
                }
            });
            
            state.addEventListener('mouseover', function() {
                var stateCode = state.id.replace('state-', '');
                if (window.handleStateHover) {
                    window.handleStateHover(stateCode);
                }
            });
            
            state.addEventListener('mouseout', function() {
                if (window.handleStateMouseOut) {
                    window.handleStateMouseOut();
                }
            });
        })(states[i]);
    }
    
    // Add click listeners to metric buttons
    var metricButtons = document.querySelectorAll('.metric-btn');
    for (var j = 0; j < metricButtons.length; j++) {
        (function(btn) {
            btn.addEventListener('click', function() {
                var metric = btn.getAttribute('data-metric');
                if (window.handleMetricToggle) {
                    window.handleMetricToggle(metric);
                }
            });
        })(metricButtons[j]);
    }
    
    // Add click listeners to WC sub-buttons
    var wcButtons = document.querySelectorAll('.wc-sub-btn');
    for (var k = 0; k < wcButtons.length; k++) {
        (function(btn) {
            btn.addEventListener('click', function() {
                var code = btn.getAttribute('data-wc-code');
                if (window.handleWCCodeToggle) {
                    window.handleWCCodeToggle(code);
                }
            });
        })(wcButtons[k]);
    }
    
    console.log('WordPress event listeners added successfully!');
'''
    
    # Find the closing of the main IIFE function
    # Look for the last })(); pattern in the original script
    original_script = content[script_start:script_end]
    
    # Find the last occurrence of })();
    last_iife_close = original_script.rfind('})();')
    
    if last_iife_close != -1:
        # Insert the additional JS right before the last })();
        modified_script = (
            original_script[:last_iife_close] + 
            additional_js + 
            '\n' + 
            original_script[last_iife_close:]
        )
    else:
        # If we can't find it, just append
        modified_script = original_script.replace('</script>', additional_js + '\n</script>')
    
    # Reconstruct the full content
    content = before_script + modified_script + after_script

# Save as wordpress-ready.html
with open('wordpress-ready.html', 'w') as f:
    f.write(content)

print("WordPress-ready version created successfully!")
print("The file 'wordpress-ready.html' is ready to be copied into WordPress.")
print("\nInstructions:")
print("1. Open wordpress-ready.html in a text editor")
print("2. Select all content (Ctrl+A or Cmd+A)")
print("3. Copy it (Ctrl+C or Cmd+C)")
print("4. Paste into a WordPress Custom HTML block")
print("5. Save and preview!")