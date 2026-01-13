# Insurance Cost Maps WordPress Plugin

Interactive US maps displaying insurance cost metrics by trade and state. Easy CSV upload, shortcode-based embedding, and SEO-friendly with structured data.

## Features

- **Interactive US Maps**: Clickable heat maps for all 50 states
- **CSV Data Management**: Upload insurance cost data via WordPress admin
- **Multiple Metrics**: GL Premium, GL Savings, GL Competitiveness, WC Rates
- **Shortcode System**: Easy embedding with `[insurance_map trade="carpenter"]`
- **SEO Optimized**: HTML tables + Schema.org structured data
- **Responsive Design**: Works on desktop and mobile devices
- **WordPress Safe**: ES5 JavaScript, no inline event handlers

## Installation

### 1. Upload Plugin

**Option A: Via WordPress Admin**
1. Go to Plugins → Add New → Upload Plugin
2. Choose `insurance-maps.zip`
3. Click "Install Now"
4. Click "Activate"

**Option B: Via FTP**
1. Upload the `insurance-maps` folder to `/wp-content/plugins/`
2. Go to Plugins in WordPress admin
3. Activate "Insurance Cost Maps"

### 2. Upload Initial Data

1. Go to **Insurance Maps** in WordPress admin sidebar
2. For each trade (carpenter, electrician, etc.):
   - Enter trade name (lowercase, no spaces)
   - Choose CSV file from `../sample-data/` directory
   - Click "Upload CSV"
3. Copy the shortcode shown in the list

### 3. Add to Pages

1. Edit or create a WordPress page
2. Add the shortcode: `[insurance_map trade="carpenter"]`
3. Publish the page
4. View to see the interactive map

## Usage

### Shortcode Options

```
[insurance_map trade="carpenter"]
```

Basic usage with SEO data table

```
[insurance_map trade="electrician" show_table="no"]
```

Hide the SEO data table (map only)

### Available Trades

The plugin works with any trade name you upload. Sample data provided for:
- carpenter
- electrician
- plumber
- hvac
- gc (general contractor)
- landscaping
- painter

### Updating Data

1. Edit your data in Google Sheets or Excel
2. Export as CSV with these columns:
   ```
   State,GL_Premium_Low,GL_Premium_High,GL_Savings,GL_Competitiveness,WC_Rate_5437,WC_Rate_5645
   ```
3. Go to Insurance Maps admin page
4. Upload the CSV with the same trade name
5. Data updates automatically on all pages using that shortcode

## CSV Format

### Required Columns (in this order)

1. **State**: Two-letter state code (AL, AK, AZ, etc.)
2. **GL_Premium_Low**: General Liability premium low end % (e.g., 1.2)
3. **GL_Premium_High**: General Liability premium high end % (e.g., 2.3)
4. **GL_Savings**: General Liability savings % (e.g., 32.3)
5. **GL_Competitiveness**: Carrier competitiveness score 0-100 (e.g., 90)
6. **WC_Rate_5437**: Workers Comp rate for class 5437 (e.g., 6.14)
7. **WC_Rate_5645**: Workers Comp rate for class 5645 (e.g., 14.07)

### Example CSV

```csv
State,GL_Premium_Low,GL_Premium_High,GL_Savings,GL_Competitiveness,WC_Rate_5437,WC_Rate_5645
AL,1.2,2.3,32.3,90,6.14,14.07
AK,0.8,1.6,22.6,0,6.16,9.78
AZ,0.9,2.1,50.6,30,4.05,10.17
...
```

**Important**: Include all 50 states for best results.

## File Structure

```
insurance-maps/
├── insurance-maps.php          # Main plugin file
├── admin/
│   ├── admin-page.php          # Admin interface
│   └── csv-uploader.php        # Upload handler
├── includes/
│   ├── class-data-manager.php  # Database operations
│   └── class-shortcode.php     # Shortcode handler
├── templates/
│   ├── map-template.php        # Map template
│   └── svg-map.html            # SVG paths
├── assets/
│   ├── css/
│   │   └── map-styles.css      # Styles
│   └── js/
│       └── map-interactive.js  # JavaScript
└── README.md                   # This file
```

## Database

The plugin creates one table:

```sql
wp_insurance_map_data
- id (primary key)
- trade (varchar)
- state_code (varchar)
- gl_premium_low, gl_premium_high
- gl_savings, gl_competitiveness
- wc_rate_5437, wc_rate_5645
- updated_at (datetime)
```

Unique constraint on (trade, state_code) ensures no duplicates.

## Troubleshooting

### Map not displaying
- Check that you've uploaded CSV data for the trade
- Verify the shortcode has correct trade name
- Check browser console for JavaScript errors
- Ensure plugin is activated

### CSV upload fails
- Verify CSV has exactly 7 columns with correct headers
- Trade name must be lowercase letters only (no spaces)
- File must be valid CSV format
- Check file size (max 5MB)

### Data not updating
- Clear WordPress cache if using caching plugin
- Hard refresh the page (Cmd/Ctrl + Shift + R)
- Verify CSV was uploaded successfully (check admin notice)

### Styling conflicts
- Check for theme CSS conflicts
- Plugin uses namespaced classes (insurance-map-*)
- CSS is loaded only on pages with shortcode

## SEO Features

### HTML Data Table
Automatically includes a crawlable HTML table with all state data. Search engines can index this structured content.

### Schema.org Markup
Adds JSON-LD structured data:
```json
{
  "@type": "Dataset",
  "name": "Carpenter Insurance Cost Metrics by US State",
  ...
}
```

Validate at: https://validator.schema.org/

## Development

### Requirements
- WordPress 5.0+
- PHP 7.0+
- MySQL 5.6+

### ES5 Compatibility
All JavaScript uses ES5 syntax for maximum compatibility:
- No arrow functions
- No const/let (uses var)
- No template literals
- Event delegation (no inline handlers)

### WordPress KSES Safe
- No inline onclick/onmouseover attributes
- All events via addEventListener
- Content properly escaped (esc_html, esc_attr, esc_js)

## Support

For issues or questions:
1. Check the admin page "How to Use" section
2. Review this README
3. Check WordPress error logs
4. Open an issue on GitHub

## License

GPL v2 or later

## Credits

- Built for contractor insurance cost visualization
- SVG US map with accurate state boundaries
- Interactive heat map visualization
- Responsive design for all devices

## Version History

### 1.0.0
- Initial release
- CSV upload functionality
- Interactive maps for all trades
- SEO optimization
- Mobile responsive
- WordPress safe (ES5, KSES compatible)
