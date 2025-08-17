# WordPress Interactive US Map - Carpenter Insurance Cost Metrics

## Project Overview
Interactive US map for WordPress (Kadence Theme) displaying carpenter insurance metrics using vanilla JavaScript and inline SVG. Successfully deployed and working in WordPress production environment.

## ✅ Current Status: FULLY FUNCTIONAL
The map is working correctly in WordPress with all features operational as of August 16, 2025.

## Key Features Implemented
- **Interactive US Map**: All 50 states with real boundaries (not placeholder shapes)
- **Four Insurance Metrics**:
  1. GL Premium % of Revenue - Displays as ranges (e.g., "0.7% - 2.1%")
  2. GL Savings % - Single percentage values
  3. GL Carrier Competitiveness - Percentile rankings
  4. WC Rate per $100 - Dollar amounts with two sub-categories (Class 5437/5645)
- **Heat Map Visualization**: Blue gradient (#e5f3ff to #003366)
- **Side-by-side Layout**: Map on left (flex: 1), info panel on right (320px fixed)
- **CTA Button**: Two-line format "Get Free Quotes for\n[State] →"

## Technical Implementation

### WordPress Compatibility Solutions
- **Event Delegation**: All events use addEventListener on parent containers
- **No Inline Handlers**: WordPress KSES strips onclick/onmouseover attributes
- **ES5 JavaScript Only**: No arrow functions, const/let, or template literals
- **No Console Statements**: Removed all console.log/error to prevent breaking
- **Hidden SVG Approach**: SVG stored in hidden div, cloned to visible container

### File Structure
```
wordpress-final-fixed.html - Main working file
├── Styles (inline <style>)
├── HTML structure
├── Hidden SVG source
└── JavaScript (ES5, IIFE pattern)
```

### Data Structure
```javascript
// Numeric values for heat map calculations
var stateData = {
    glPremium: { CA: 1.0, TX: 0.8, ... },
    glSavings: { CA: 35.8, TX: 21.2, ... },
    // ...
};

// Separate display ranges for GL Premium
var glPremiumRanges = {
    CA: "0.5% - 1.5%",
    TX: "0.5% - 1.1%",
    // ...
};
```

## Known Issues & Solutions

| Issue | Solution |
|-------|----------|
| Map not displaying | Remove all console statements |
| Buttons not clickable | Use event delegation |
| Data not updating | Use specific selectors `.info-card .state-name` |
| Button text invisible on hover | Add explicit `color: #333` to hover state |
| Wrong layout | Add flex container wrapper |

## Implementation in WordPress

1. Copy everything between the HTML comment markers:
   ```html
   <!-- ================================================== -->
   <!-- COPY EVERYTHING BELOW THIS LINE INTO WORDPRESS -->
   <!-- ================================================== -->
   ```

2. Paste into WordPress Kadence Custom HTML block
3. Map initializes automatically on page load

## Styling Specifications
- **Container**: max-width: 1160px
- **Buttons**: Blue (#2563eb) when active, white background default
- **Info Panel**: 320px width, white background, blue text
- **Heat Map**: 8 levels of blue gradient
- **Hover States**: Properly defined text colors

## Recent Fixes (August 16, 2025)
1. Fixed map display by removing console statements
2. Corrected button hover text visibility
3. Implemented side-by-side layout with proper flex container
4. Added GL Premium range display
5. Fixed data update selectors to avoid tooltip conflicts
6. Updated CTA button to two-line format
7. Ensured WordPress KSES compatibility

## Testing Checklist
- [x] All 50 states have data and display correctly
- [x] Four metric toggles work and update heat map
- [x] State selection updates info panel
- [x] CTA button displays and links properly
- [x] No console errors in production
- [x] Works in WordPress/Kadence environment
- [x] Button hover states maintain visibility
- [x] GL Premium shows ranges, not single values

## Future Enhancements (Currently Disabled)
- Hover tooltips (implemented but commented out due to conflicts)
- Mobile dropdown support (structure exists but not active)

## Important Notes
- Always test locally before deploying to WordPress
- Avoid using console statements in any capacity
- Maintain ES5 compatibility for WordPress
- Use event delegation for all interactive elements
- Keep selectors specific to avoid conflicts

## File Size
- Approximately 45KB unminified (including SVG paths)
- Self-contained with no external dependencies

## Browser Support
- Chrome ✓
- Safari ✓
- Firefox ✓
- Edge ✓
- Mobile browsers ✓