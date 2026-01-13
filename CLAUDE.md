# WordPress Insurance Cost Maps Plugin

## Project Overview
WordPress plugin for displaying interactive US insurance cost maps by trade and state. Features CSV data management, shortcode-based embedding, and SEO optimization with structured data.

## ✅ Current Status: WORDPRESS PLUGIN (v1.0.0)
Plugin architecture implemented January 2026. Replaces previous HTML copy-paste approach with proper WordPress plugin structure.

## Key Features
- **WordPress Plugin**: Professional plugin architecture with admin interface
- **CSV Data Management**: Upload insurance data via WordPress admin (no code editing required)
- **Multiple Trades**: Support for unlimited trades (carpenter, electrician, plumber, hvac, gc, landscaping, painter, etc.)
- **Shortcode System**: Easy embedding with `[insurance_map trade="carpenter"]`
- **Interactive US Map**: All 50 states with real boundaries
- **Four Insurance Metrics**:
  1. GL Premium % of Revenue - Displays as ranges (e.g., "1.2% - 2.3%")
  2. GL Savings % - Single percentage values
  3. GL Carrier Competitiveness - Percentile rankings
  4. WC Rate per $100 - Dollar amounts with two sub-categories (Class 5437/5645)
- **Heat Map Visualization**: Blue gradient (#e5f3ff to #003366)
- **SEO Optimized**: HTML data tables + Schema.org structured data
- **Side-by-side Layout**: Map on left (flex: 1), info panel on right (320px fixed)
- **Mobile Responsive**: Dropdown selector on mobile devices
- **CTA Button**: Two-line format "Get Free Quotes for\n[State] →"

## Architecture

### Plugin Structure
```
wp-content/plugins/insurance-maps/
├── insurance-maps.php              # Main plugin file
├── admin/
│   ├── admin-page.php              # Admin interface with CSV upload
│   └── csv-uploader.php            # CSV processing and validation
├── includes/
│   ├── class-data-manager.php      # Database operations
│   └── class-shortcode.php         # Shortcode handler
├── templates/
│   ├── map-template.php            # Main template (single source)
│   └── svg-map.html                # US map SVG paths
├── assets/
│   ├── css/
│   │   └── map-styles.css          # All styles (extracted from HTML)
│   └── js/
│       └── map-interactive.js      # Interactive functionality (ES5)
└── README.md                       # Plugin documentation
```

### Database Schema
```sql
wp_insurance_map_data
├── id (primary key)
├── trade (varchar)
├── state_code (varchar)
├── gl_premium_low (decimal)
├── gl_premium_high (decimal)
├── gl_savings (decimal)
├── gl_competitiveness (int)
├── wc_rate_5437 (decimal)
├── wc_rate_5645 (decimal)
└── updated_at (datetime)

UNIQUE KEY: (trade, state_code)
```

### Data Flow
```
CSV File → WordPress Admin → Database → Shortcode → Rendered Map
   ↓            ↓               ↓           ↓            ↓
(Upload)   (Validate)       (Store)    (Display)   (SEO Table)
```

## Usage

### Installation
1. Upload `insurance-maps` folder to `/wp-content/plugins/`
2. Activate plugin in WordPress admin
3. Go to "Insurance Maps" in admin sidebar
4. Upload CSV files for each trade
5. Copy shortcode and add to pages

### Uploading Data
1. Prepare CSV with columns:
   ```
   State,GL_Premium_Low,GL_Premium_High,GL_Savings,GL_Competitiveness,WC_Rate_5437,WC_Rate_5645
   ```
2. Navigate to **Insurance Maps** in WordPress admin
3. Enter trade name (lowercase, no spaces)
4. Choose CSV file
5. Click "Upload CSV"
6. Copy the shortcode shown

### Embedding Maps
```
[insurance_map trade="carpenter"]
```

Show map with SEO data table (default):
```
[insurance_map trade="electrician" show_table="yes"]
```

Hide SEO data table (map only):
```
[insurance_map trade="plumber" show_table="no"]
```

### Updating Data
1. Edit data in Google Sheets or Excel
2. Export to CSV with same format
3. Upload via WordPress admin with same trade name
4. Existing data is replaced automatically
5. All pages using that shortcode update immediately

## Technical Implementation

### WordPress Compatibility
- **Event Delegation**: All events use addEventListener on parent containers
- **No Inline Handlers**: WordPress KSES compatible (no onclick/onmouseover attributes)
- **ES5 JavaScript**: No arrow functions, const/let, or template literals
- **Proper Escaping**: esc_html(), esc_attr(), esc_js() throughout
- **Hidden SVG Approach**: SVG stored in hidden div, cloned to visible container

### CSV Format
```csv
State,GL_Premium_Low,GL_Premium_High,GL_Savings,GL_Competitiveness,WC_Rate_5437,WC_Rate_5645
AL,1.2,2.3,32.3,90,6.14,14.07
AK,0.8,1.6,22.6,0,6.16,9.78
AZ,0.9,2.1,50.6,30,4.05,10.17
...
```

**Required**: All 7 columns in exact order
**States**: All 50 states for best results

### Data Structure (JavaScript)
```javascript
// Data passed from PHP to JavaScript
window.insuranceMapData = {
    glPremiumRanges: {
        CA: "1.6% - 3.0%",
        TX: "1.0% - 2.7%",
        ...
    },
    stateData: {
        glPremium: { CA: 2.3, TX: 1.85, ... },
        glSavings: { CA: 18.2, TX: 44.3, ... },
        glCompetitiveness: { CA: 10, TX: 100, ... },
        wcRate5437: { CA: 5.62, TX: 3.55, ... },
        wcRate5645: { CA: 8.46, TX: 4.39, ... }
    }
};
```

## SEO Features

### HTML Data Table
Each map includes a crawlable HTML table with all state data:
```html
<table class="insurance-data-table">
    <thead>
        <tr>
            <th>State</th>
            <th>GL Premium Range</th>
            <th>GL Savings %</th>
            ...
        </tr>
    </thead>
    <tbody>
        <!-- 50 states of data -->
    </tbody>
</table>
```

### Schema.org Structured Data
Automatically adds JSON-LD markup:
```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "Carpenter Insurance Cost Metrics by US State",
  "description": "Comprehensive insurance cost data...",
  "creator": { "@type": "Organization", "name": "Contractor Nerd" },
  "temporalCoverage": "2026",
  "spatialCoverage": { "@type": "Place", "name": "United States" }
}
```

Validate at: https://validator.schema.org/

## Styling Specifications
- **Container**: max-width: 1160px
- **Buttons**: Blue (#2563eb) when active, white background default
- **Info Panel**: 320px width, white background, blue text
- **Heat Map**: 8 levels of blue gradient
- **SEO Table**: Blue header (#2563eb), alternating row colors
- **Mobile**: Dropdown replaces map on screens < 768px

## Benefits Over Old Approach

| Aspect | Old (HTML Files) | New (Plugin) |
|--------|-----------------|--------------|
| **Maintenance** | Edit 8 HTML files | Upload 1 CSV |
| **Code Duplication** | ~7,200 lines | 0 duplication |
| **Design Updates** | Change 8 files | Edit 1 template |
| **Data Updates** | Edit JavaScript | Upload CSV |
| **SEO** | JavaScript only | HTML table + Schema.org |
| **Workflow** | Edit HTML → Copy → Paste | Export CSV → Upload → Done |
| **Portability** | Copy-paste each | Shortcode anywhere |

## Files

### Source Files (Legacy - Reference Only)
- `final-carpenter.html` through `final-painter.html` - Original HTML files
- Used for initial data extraction only
- **Not used in production anymore**

### Plugin Files (Active)
- `/plugin/*` - WordPress plugin (production-ready)
- `/sample-data/*.csv` - Initial data files (extracted from HTML)
- `extract-csv-data.py` - Script to extract CSV from HTML files

### Sample Data Files
- `carpenter.csv` - Carpenter insurance data
- `electrician.csv` - Electrician insurance data
- `plumber.csv` - Plumber insurance data
- `hvac.csv` - HVAC insurance data
- `gc.csv` - General contractor insurance data
- `landscaping.csv` - Landscaping insurance data
- `painter.csv` - Painter insurance data

## Troubleshooting

### Map not displaying
- Check that CSV data uploaded for the trade
- Verify shortcode has correct trade name
- Check WordPress error logs
- Ensure plugin is activated

### CSV upload fails
- Verify exactly 7 columns with correct headers
- Trade name must be lowercase letters only
- File must be valid CSV format (UTF-8 encoding)
- Maximum file size: 5MB

### Data not updating after CSV upload
- Clear WordPress cache if using caching plugin
- Hard refresh the page (Cmd/Ctrl + Shift + R)
- Verify success message appeared after upload
- Check database directly if needed

### Wrong data showing
- Ensure correct trade name in shortcode
- Check that CSV was uploaded for that specific trade
- Verify state codes are uppercase (AL, not al)

## Admin Interface

### Features
- **CSV Upload Form**: Upload data for any trade
- **Trade Management**: View all trades with shortcodes
- **One-Click Copy**: Copy shortcode to clipboard
- **Delete Function**: Remove trade data
- **State Count**: Shows X/50 states for each trade
- **Usage Instructions**: Built-in help and CSV template

### Admin Notices
- Success: Shows number of states imported
- Error: Displays specific error message
- File validation: Checks format before import

## Version History

### v1.0.0 (January 2026)
- Initial plugin release
- Converted from HTML files to WordPress plugin
- CSV upload functionality
- Database-driven architecture
- Admin interface
- Shortcode system
- SEO optimization (tables + Schema.org)
- Mobile responsive design
- WordPress KSES compatible
- ES5 JavaScript for maximum compatibility

### Legacy (August 2025)
- Original HTML file approach
- Manual copy-paste into WordPress
- Data hard-coded in JavaScript
- 8 separate HTML files maintained individually

## Development Notes

### WordPress Best Practices
- Proper nonce validation
- Capability checks (manage_options)
- Prepared SQL statements
- Output escaping (esc_html, esc_attr, esc_js)
- Translation-ready (text domain: insurance-maps)
- Hooks for extensibility

### ES5 Compatibility
All JavaScript is ES5-compatible:
- `var` instead of `const`/`let`
- No arrow functions
- No template literals
- `function` keyword only
- Compatible with IE11+

### Testing
- Test in multiple browsers (Chrome, Safari, Firefox, Edge)
- Test on mobile devices
- Test CSV upload with various formats
- Test shortcode on different page types
- Validate Schema.org markup
- Check WordPress error logs

## Browser Support
- Chrome ✓
- Safari ✓
- Firefox ✓
- Edge ✓
- Mobile browsers ✓
- IE11 (with polyfills)

## Future Enhancements (Potential)

### Could Add
- Bulk CSV upload for multiple trades
- Export data back to CSV
- Map customization options (colors, CTA URL)
- Additional metrics beyond current 4
- Historical data comparison
- Admin analytics dashboard
- REST API endpoints
- Gutenberg block (in addition to shortcode)
- Multi-language support

### Not Planned
- Hover tooltips on desktop (WordPress KSES conflicts)
- Real-time data sync from external APIs
- User-submitted data
- Map editing interface

## Important Notes

### For Developers
- Always test locally before deploying
- Maintain ES5 compatibility for WordPress
- Use event delegation for all interactive elements
- Keep selectors specific to avoid conflicts
- Validate CSV format before processing
- Handle errors gracefully (no breaking)

### For Content Managers
- Trade names must be lowercase (carpenter not Carpenter)
- CSV must have exact column headers
- Include all 50 states for complete maps
- Re-uploading with same trade name replaces data
- Shortcodes can be reused on multiple pages

### Performance
- CSS/JS only load on pages with shortcode
- Database queries use indexes
- Single template shared across all trades
- SVG cloned in JavaScript (not duplicated in HTML)
- Efficient heat map calculation

## Support & Documentation

- **Plugin README**: `/plugin/README.md`
- **Admin Help**: Built into WordPress admin page
- **GitHub**: https://github.com/orcaventuresllc/trade-maps
- **Issues**: Report at GitHub repository

## License
GPL v2 or later
