# Trade Maps - Contractor Insurance Metrics Map

## Project Overview
Interactive US map for WordPress (Kadence Theme) displaying contractor insurance metrics using vanilla JavaScript and inline SVG. No external dependencies or frameworks.

## Key Requirements
- **Technology Stack**: Vanilla JS + Inline SVG (no React, Vue, or other frameworks)
- **Platform**: WordPress with Kadence Theme + Blocks Pro
- **Deployment**: Single Kadence Custom HTML block containing all code
- **Mobile Support**: Dropdown fallback for screens < 768px
- **Browser Support**: Modern browsers (Chrome, Safari, Firefox, Edge, iOS, Android)

## Four Insurance Metrics
1. **GL Premium as % Revenue** - Range format (e.g., "2.5% – 4.8%"), use midpoint for heatmap
2. **GL Savings as % of Premium** - Single percentage (higher = better)
3. **GL Carrier Competitiveness** - Percentile (higher = better)
4. **WC Rate per $100** - Dollar amount (lower = better, reverse heatmap)

## Core Features
- Interactive US map with all 50 states + D.C.
- Heatmap coloring based on selected metric
- Desktop: Hover tooltips + click to update info card
- Mobile: Dropdown menu replacing map
- Metric toggle buttons for instant switching
- State info card showing details and CTA link

## Data Structure
```javascript
const DATA = {
  glPremiumPct: {
    CA: { midpoint: 3.65, range: "2.5% – 4.8%" },
    // ... all states
  },
  glSavingsPct: { CA: 18, /* ... */ },
  glCompetitiveness: { CA: 92, /* ... */ },
  wcRate: { CA: 4.50, /* ... */ }
};
```

## Implementation Notes
- States identified by USPS codes (CA, TX, etc.)
- SVG paths use `id` or `data-code` attributes
- All styling inline via `<style>` tags
- All JavaScript inline via `<script>` tags
- No external dependencies or CDN links
- Heatmap: darker = higher values (except WC Rate which is reversed)

## File Structure
- Single HTML file containing all code
- Pasteable into Kadence Custom HTML block
- Self-contained with no external assets

## Testing Checklist
- [ ] All 50 states + D.C. have data
- [ ] Four metric toggles work correctly
- [ ] Heatmap colors update per metric
- [ ] Desktop hover/click interactions work
- [ ] Mobile dropdown functions properly
- [ ] No console errors
- [ ] Works across all target browsers

## Important Constraints
- NO external libraries (jQuery, D3.js, etc.)
- NO paid licenses or proprietary code
- MUST be completely self-contained
- MUST work within WordPress/Kadence environment
- File size should be minimal (~5-10KB JS)

## Development Commands
No build process required - this is vanilla JavaScript that runs directly in the browser.

## Contact & Questions
This is a WordPress plugin/block for displaying contractor insurance metrics across US states.