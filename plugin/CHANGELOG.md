# Changelog

All notable changes to the Insurance Cost Maps plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-13

### Added
- **Flexible WC Class Code System**: Support for 1 or 2 Workers Compensation classes per trade
- Dynamic WC button labels showing actual class codes (e.g., "Class 5190", "Class 5437 (Interior)")
- WC class code and label storage in database
- Trade-specific WC class codes:
  - Carpenter: 5437 (Interior) & 5645 (Framing)
  - Electrician: 5190
  - Plumber: 5183
  - HVAC: 5537
  - General Contractor: 5645
  - Landscaping: 9102 (Lawncare)
  - Painter: 5474
- CSV export/download feature in admin interface
- Download button for each trade to export current data as CSV
- **Collapsible data table**: Table collapsed by default, expands on click
- SEO-friendly accordion using HTML5 `<details>` element

### Changed
- **CSV Format**: Expanded from 7 to 11 columns to support flexible WC classes
  - Old: `State,GL_Premium_Low,GL_Premium_High,GL_Savings,GL_Competitiveness,WC_Rate_5437,WC_Rate_5645`
  - New: `State,GL_Premium_Low,GL_Premium_High,GL_Savings,GL_Competitiveness,WC_Class_1,WC_Rate_1,WC_Label_1,WC_Class_2,WC_Rate_2,WC_Label_2`
- Database schema updated with new WC class columns
- WC buttons now generated dynamically based on uploaded data
- SEO table headers now show actual WC class codes
- JavaScript updated to use generic wcRate1/wcRate2 keys

### Fixed
- WC data now correctly populated for all trades (was showing zeros for non-carpenter trades)
- Each trade now displays its correct WC class code(s)
- Sample CSV files regenerated with accurate WC data for each trade
- **Brand colors applied**: Table now uses brand teal (#416E72) instead of blue
- Table hover color updated to brand light teal (#D9F0EE)
- Alternating row colors updated to brand beige (#F3F3F0)

### UI/UX Improvements
- Data table now collapsible (collapsed by default) for cleaner page layout
- Toggle text changes: "Show State-by-State Data" → "Hide Data"
- Smooth expand/collapse animation
- Table remains crawlable by search engines when collapsed
- Keyboard accessible (Tab to toggle, Enter to expand/collapse)

### Brand Styling Applied
- **Fonts**: Added Google Fonts (Saira Extra Condensed, Poppins, Inter)
- **Active buttons**: Gold (#F0CC4C) instead of blue
- **Heat map**: Teal gradient (#D9F0EE to #416E72) matching brand
- **Selected state**: Gold highlight (#F0CC4C border, #FFE898 fill)
- **CTA button**: Brand gold (#F0CC4C, hover #E0B004)
- **WC sub-buttons**: Dark (#181815) when active
- **Text colors**: Brand grays (#181815, #353433, #8F8D85)
- **Backgrounds**: Brand beige (#F3F3F0, #E3E3DB)
- **Borders**: Brand gray (#B5B4AE)
- All colors now match ContractorNerd brand guidelines

### Developer Features
- Added debug logging to JavaScript for troubleshooting
- Console messages show data loading status
- Error message displayed if no CSV data uploaded
- Helpful debugging for administrators

### Migration
- Automatic database migration on plugin load (v1.0 → v1.1)
- Old column names renamed: `wc_rate_5437` → `wc_rate_1`, `wc_rate_5645` → `wc_rate_2`
- Existing data migrated with default carpenter class codes (5437/5645)
- Users should re-upload CSVs in new 11-column format for full functionality

### Backward Compatibility
- Plugin automatically migrates old database structure
- Old CSV format data will be migrated but won't show custom class codes
- New CSV format required to display trade-specific class codes

## [1.0.0] - 2026-01-13

### Added
- Initial plugin release
- WordPress admin interface for CSV data management
- CSV upload functionality with drag-and-drop support
- Interactive US maps for all 50 states
- Database-driven architecture (wp_insurance_map_data table)
- Shortcode system: `[insurance_map trade="carpenter"]`
- Support for multiple trades (carpenter, electrician, plumber, hvac, gc, landscaping, painter)
- Four insurance metrics:
  - GL Premium % of Revenue (with range display)
  - GL Savings %
  - GL Carrier Competitiveness
  - WC Rate per $100 (with Class 5437/5645 sub-categories)
- Heat map visualization with blue gradient (8 levels)
- Mobile responsive design with dropdown selector
- Side-by-side layout (map + info panel)
- CTA button with dynamic state-specific links
- Admin features:
  - Upload CSV files
  - View all existing trades
  - One-click shortcode copying
  - Delete trade data
  - State count display (X/50)
  - Built-in help and CSV template

### SEO Features
- Crawlable HTML data tables for each trade
- Schema.org structured data (JSON-LD Dataset markup)
- Semantic HTML structure
- Proper heading hierarchy
- Alt text and aria labels

### Security
- SQL injection protection via `$wpdb->prepare()` prepared statements
- XSS prevention via comprehensive output escaping
- CSRF protection via WordPress nonces
- File upload validation:
  - Extension validation (.csv only)
  - MIME type validation (text/csv, text/plain, application/csv)
  - File size limits (5MB maximum)
  - Filename sanitization
- CSV content validation:
  - State code validation (2 uppercase letters)
  - Numeric range validation
  - Column count validation
  - Data integrity checks
- Access control:
  - Capability checks (`manage_options` required)
  - Direct file access prevention (ABSPATH checks)
  - Admin-only functionality
- Rate limiting: 10 uploads per hour per user
- Security headers:
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: SAMEORIGIN
  - X-XSS-Protection: 1; mode=block

### Technical
- ES5 JavaScript for maximum compatibility (no arrow functions, const/let, template literals)
- WordPress KSES compatible (no inline event handlers)
- Event delegation for all interactive elements
- Hidden SVG source cloned to container (WordPress safe)
- Database transactions for bulk imports
- Unique constraints prevent duplicate data
- Auto-update timestamps
- Conditional asset loading (only on pages with shortcode)

### Documentation
- Comprehensive README.md with usage instructions
- SECURITY.md with security policy and best practices
- INSTALL.md with step-by-step installation guide
- USER-GUIDE.md with complete user documentation
- CONTRIBUTING.md with development guidelines
- Inline code documentation
- CSV template examples
- Admin page help sections

### Browser Support
- Chrome (latest)
- Safari (latest)
- Firefox (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)
- IE11 (with polyfills)

### WordPress Compatibility
- WordPress 5.0+
- PHP 7.0+
- MySQL 5.6+
- Kadence theme tested
- Gutenberg block editor compatible
- Classic editor compatible

## [Unreleased]

### Planned Features
- Bulk CSV upload for multiple trades
- Export data back to CSV
- Admin settings page for customization
- Map color scheme options
- Custom CTA URL per trade
- Historical data comparison
- Gutenberg block (in addition to shortcode)
- REST API endpoints

## Migration from HTML Files

### Legacy Approach (August 2025)
- Used 8 separate HTML files (final-*.html)
- Data hard-coded in JavaScript
- Manual copy-paste into WordPress
- ~7,200 lines of duplicate code
- Required editing 8 files for any change

### Plugin Approach (January 2026)
- Single WordPress plugin
- CSV data management
- Database-driven
- No code duplication
- Update via CSV upload only

### Migration Path
1. Install plugin
2. Extract data using `extract-csv-data.py`
3. Upload CSV files via admin
4. Replace HTML in pages with shortcodes
5. Archive old HTML files

## Version History

- **1.0.0** (2026-01-13): Initial release with full feature set

---

## Notes

- **Breaking Changes**: None (initial release)
- **Deprecations**: None
- **Security Fixes**: None (initial secure release)
- **Bug Fixes**: None (initial release)

For detailed commit history, see: https://github.com/orcaventuresllc/trade-maps/commits/master
