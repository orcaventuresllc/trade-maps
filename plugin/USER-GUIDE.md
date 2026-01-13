# Insurance Maps Plugin - User Guide

Complete guide for using the Insurance Cost Maps WordPress plugin.

## Table of Contents
1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Uploading Data](#uploading-data)
4. [Using Shortcodes](#using-shortcodes)
5. [Updating Data](#updating-data)
6. [Customization](#customization)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

---

## Installation

### Automatic Installation (Recommended)

1. Log in to your WordPress admin dashboard
2. Navigate to **Plugins → Add New**
3. Click **Upload Plugin** button at the top
4. Click **Choose File** and select `insurance-maps-v1.0.0.zip`
5. Click **Install Now**
6. Click **Activate Plugin**
7. You should see "Insurance Maps" in your admin menu

### Manual Installation

1. Download `insurance-maps-v1.0.0.zip`
2. Unzip the file on your computer
3. Connect to your site via FTP
4. Upload the `insurance-maps` folder to `/wp-content/plugins/`
5. Go to WordPress admin → Plugins
6. Find "Insurance Cost Maps" and click **Activate**

### Verification

After activation, verify the plugin is working:
- Check for "Insurance Maps" in the left admin menu
- Go to **Insurance Maps** page
- You should see the upload form and instructions
- Check that no errors appear

---

## Getting Started

### Quick Start (5 Minutes)

1. **Upload Sample Data**
   - Go to **Insurance Maps** in admin menu
   - Enter trade name: `carpenter`
   - Upload `carpenter.csv` from sample-data folder
   - Click **Upload CSV**

2. **Copy Shortcode**
   - After upload, find "carpenter" in the list
   - Click **Copy** button next to the shortcode
   - You'll see: `[insurance_map trade="carpenter"]`

3. **Add to Page**
   - Create or edit a WordPress page
   - Paste the shortcode where you want the map
   - Click **Preview** to see the map
   - Click **Publish** when ready

That's it! Your interactive map is live.

---

## Uploading Data

### Preparing Your CSV File

#### Required Format

Your CSV file must have **exactly 7 columns** in this order:

```csv
State,GL_Premium_Low,GL_Premium_High,GL_Savings,GL_Competitiveness,WC_Rate_5437,WC_Rate_5645
AL,1.2,2.3,32.3,90,6.14,14.07
AK,0.8,1.6,22.6,0,6.16,9.78
...
```

#### Column Descriptions

| Column | Description | Valid Range | Example |
|--------|-------------|-------------|---------|
| **State** | Two-letter state code | AL-WY | CA |
| **GL_Premium_Low** | GL premium low end % | 0-100 | 1.6 |
| **GL_Premium_High** | GL premium high end % | 0-100 | 3.0 |
| **GL_Savings** | GL savings percentage | 0-100 | 18.2 |
| **GL_Competitiveness** | Competitiveness score | 0-100 | 10 |
| **WC_Rate_5437** | WC rate for class 5437 | 0-1000 | 5.62 |
| **WC_Rate_5645** | WC rate for class 5645 | 0-1000 | 8.46 |

#### Creating Your CSV

**Using Google Sheets:**
1. Create a new Google Sheet
2. Add headers in row 1 (exactly as shown above)
3. Add data for all 50 states (rows 2-51)
4. Go to **File → Download → Comma Separated Values (.csv)**
5. Save the file

**Using Excel:**
1. Create new Excel file
2. Add headers in row 1
3. Add data for all 50 states
4. Go to **File → Save As**
5. Choose **CSV (Comma delimited)** format
6. Save the file

#### Important Notes

- Include all 50 states for best results
- State codes must be UPPERCASE (AL, not al)
- Use decimal points for numbers (1.5, not 1,5)
- Don't include extra columns
- Don't skip the header row
- File must be UTF-8 encoded

### Uploading to WordPress

1. **Navigate to Upload Page**
   - Go to WordPress admin
   - Click **Insurance Maps** in left menu

2. **Enter Trade Name**
   - Type the trade name (lowercase, no spaces)
   - Examples: `carpenter`, `electrician`, `plumber`, `hvac`
   - Note: This will be used in the shortcode

3. **Choose CSV File**
   - Click **Choose File** button
   - Select your CSV file
   - Verify the filename shows

4. **Upload**
   - Click **Upload CSV** button
   - Wait for success message
   - You'll see "Successfully imported X states!"

5. **Verify Upload**
   - Check the trade appears in the list below
   - Verify state count shows "50/50"
   - Copy the shortcode for use

### Upload Limits

- **File Size**: Maximum 5MB per file
- **Rate Limit**: 10 uploads per hour per user
- **File Type**: CSV only (.csv extension)
- **Format**: Must match required column structure

---

## Using Shortcodes

### Basic Usage

To display an insurance cost map on any page or post:

```
[insurance_map trade="carpenter"]
```

This displays:
- Interactive US map
- Metric toggle buttons
- Info panel with state details
- SEO-friendly data table

### Shortcode Parameters

#### trade (required)
Specifies which trade's data to display.

```
[insurance_map trade="carpenter"]
[insurance_map trade="electrician"]
[insurance_map trade="plumber"]
```

#### show_table (optional)
Controls whether the SEO data table appears below the map.

```
[insurance_map trade="carpenter" show_table="yes"]    (default)
[insurance_map trade="carpenter" show_table="no"]     (hide table)
```

### Where to Use Shortcodes

Shortcodes work in:
- WordPress pages
- WordPress posts
- Text widgets
- Custom post types
- Gutenberg shortcode block
- Classic editor

### Multiple Maps on One Page

You can add multiple shortcodes to display different trades:

```
[insurance_map trade="carpenter"]

[insurance_map trade="electrician"]

[insurance_map trade="plumber"]
```

Each map is independent and displays its own data.

---

## Updating Data

### When to Update

Update your data when:
- Insurance rates change
- You get new market data
- Competitiveness scores update
- Workers comp rates change

### How to Update

1. **Edit Your Data**
   - Open your original Google Sheet or Excel file
   - Update the values for any states/metrics
   - Keep the same column structure
   - Keep the same trade name

2. **Export to CSV**
   - Export your updated data to CSV
   - Use the same filename (optional)

3. **Re-Upload**
   - Go to **Insurance Maps** admin page
   - Enter the **same trade name** as before
   - Upload the new CSV file
   - Click **Upload CSV**

4. **Automatic Update**
   - The old data is replaced automatically
   - All pages using that shortcode update immediately
   - No need to edit any pages
   - Changes are live instantly

### Important Notes

- Uploading with the same trade name **replaces all existing data** for that trade
- Other trades are not affected
- Shortcodes don't need to be updated
- No cache clearing needed (usually)

---

## Customization

### Changing Map Colors

The heat map uses a blue gradient by default. To change colors:

1. Go to `/wp-content/plugins/insurance-maps/assets/css/map-styles.css`
2. Find the `.heat-0` through `.heat-7` classes
3. Change the `fill` colors:

```css
.heat-0 { fill: #e5f3ff; }  /* Lightest */
.heat-1 { fill: #b3d9ff; }
.heat-2 { fill: #80bfff; }
.heat-3 { fill: #4da6ff; }
.heat-4 { fill: #1a8cff; }
.heat-5 { fill: #0066cc; }
.heat-6 { fill: #004c99; }
.heat-7 { fill: #003366; }  /* Darkest */
```

### Changing CTA Button URL

The CTA button currently links to `https://app.contractornerd.com/`

To change this:

1. Edit `/wp-content/plugins/insurance-maps/assets/js/map-interactive.js`
2. Find line with `ctaEl.href = 'https://app.contractornerd.com/'`
3. Change to your URL
4. Save and clear browser cache

### Changing Button Colors

Active buttons are blue (#2563eb) by default. To change:

1. Edit `/wp-content/plugins/insurance-maps/assets/css/map-styles.css`
2. Find `.metric-btn.active` class
3. Change `background` and `border-color` properties

### Adding New Metrics

To add additional metrics beyond the current 4:

1. Update database schema to add new columns
2. Update CSV format and upload handler
3. Update JavaScript to handle new metric
4. Update template to display new button

(This is an advanced customization - consider creating a GitHub issue for guidance)

---

## Troubleshooting

### Map Not Displaying

**Problem**: Shortcode shows but map doesn't appear

**Solutions**:
1. Check that you uploaded CSV data for that trade
2. Verify the trade name in shortcode matches upload
3. Check browser console for JavaScript errors (F12)
4. Ensure plugin is activated
5. Clear browser cache (Cmd/Ctrl + Shift + R)
6. Check WordPress error logs

**How to Check**:
```
WordPress Admin → Insurance Maps
Look for your trade in the list
Verify state count shows "50/50" or at least some number
```

### CSV Upload Fails

**Problem**: Error message after trying to upload

**Common Errors and Solutions**:

| Error | Solution |
|-------|----------|
| "Invalid CSV format" | Check column headers match exactly |
| "Invalid file type" | Ensure file has .csv extension |
| "File too large" | Reduce file size (remove extra data) |
| "Invalid state code" | State codes must be 2 uppercase letters |
| "Invalid range" | Check numbers are within valid ranges |
| "Rate limit exceeded" | Wait 1 hour before uploading again |

**Validation Checklist**:
- [ ] File extension is `.csv`
- [ ] Headers match exactly (case-sensitive)
- [ ] All 50 states included
- [ ] State codes are uppercase (AL, not al)
- [ ] Numbers use decimal points (1.5 not 1,5)
- [ ] GL Premium Low < High
- [ ] All values within valid ranges

### Wrong Data Showing

**Problem**: Map shows data from different trade

**Solution**:
1. Check the shortcode trade name
2. Verify you uploaded data for that trade
3. Try deleting and re-uploading the CSV
4. Clear WordPress object cache if using caching plugin

### Styling Issues

**Problem**: Map looks broken or poorly styled

**Solutions**:
1. Check for theme CSS conflicts
2. Try adding shortcode to a page without other content
3. Check browser console for CSS errors
4. Disable other plugins temporarily to test for conflicts
5. Try with a default WordPress theme

### Mobile Issues

**Problem**: Map doesn't work on mobile

**Solution**:
This is expected behavior. On mobile (< 768px width):
- Map is hidden
- Dropdown selector appears instead
- Select states from dropdown
- This is intentional for better mobile UX

### Data Not Updating

**Problem**: Uploaded new CSV but page shows old data

**Solutions**:
1. Hard refresh the page (Cmd/Ctrl + Shift + R)
2. Clear WordPress cache (if using caching plugin)
3. Clear browser cache
4. Check that upload showed success message
5. Verify in admin that new data is listed
6. Check WordPress error logs

### Performance Issues

**Problem**: Page loads slowly

**Solutions**:
1. Check for other slow plugins/themes
2. Use a caching plugin (WP Super Cache, W3 Total Cache)
3. Optimize your images on the page
4. Consider using a CDN
5. Check your hosting performance

---

## FAQ

### General Questions

**Q: How many trades can I create?**
A: Unlimited. Create as many trades as you need.

**Q: Can I use the same data for multiple trades?**
A: Yes, upload the same CSV with different trade names.

**Q: Can I delete a trade?**
A: Yes, click the Delete button next to the trade in the admin list.

**Q: Will deleting a trade break my pages?**
A: Pages with that shortcode will show an error message asking to upload data.

**Q: Can I export data back to CSV?**
A: Not currently. Keep your original CSV files for records.

**Q: How do I backup my data?**
A: Backup your WordPress database (includes the plugin's data table).

### Data Questions

**Q: What if I don't have data for all 50 states?**
A: Upload what you have. States without data won't appear in the heat map.

**Q: Can I use different metrics than the defaults?**
A: Not currently. The plugin uses fixed metrics (GL Premium, GL Savings, etc.).

**Q: What do the competitiveness scores mean?**
A: Higher scores (closer to 100) mean more carrier competition in that state.

**Q: Why are there two WC rates?**
A: Class 5437 and 5645 are different work categories (e.g., interior vs framing for carpenters).

**Q: Can I hide certain metrics?**
A: Not currently. All 4 metrics always display.

### Technical Questions

**Q: Does this work with my theme?**
A: Yes, should work with any WordPress theme. Tested with Kadence.

**Q: Does this work with page builders?**
A: Yes, works with Gutenberg, Classic Editor, and most page builders that support shortcodes.

**Q: Will this slow down my site?**
A: No. CSS/JS only load on pages with the shortcode. Database queries are optimized.

**Q: Is the data crawlable by search engines?**
A: Yes! The plugin includes an HTML table and Schema.org markup for SEO.

**Q: Can I use this on multiple sites?**
A: Yes, install the plugin on each site and upload data separately.

**Q: Does this work with caching plugins?**
A: Yes, compatible with WP Super Cache, W3 Total Cache, etc.

### Security Questions

**Q: Is this plugin secure?**
A: Yes. Includes SQL injection protection, XSS prevention, CSRF protection, and more. See SECURITY.md for details.

**Q: Who can upload CSV files?**
A: Only WordPress administrators (users with `manage_options` capability).

**Q: Are there any upload limits?**
A: Yes, maximum 5MB per file and 10 uploads per hour per user.

**Q: Is my data safe?**
A: Data is stored in your WordPress database. Use standard WordPress security best practices.

---

## Tips & Tricks

### Organizing Your Data

**Use Google Sheets for Easy Management:**
1. Create one Google Sheet
2. Use separate tabs for each trade
3. All tabs have the same column structure
4. Export each tab as CSV when ready
5. Upload to WordPress

**Maintain a Master Spreadsheet:**
- Keep one source of truth for all insurance data
- Add a "Last Updated" column for tracking
- Use data validation in Google Sheets to prevent errors
- Add notes about data sources

### Efficient Workflow

**For Regular Updates:**
1. Update all trades in Google Sheets
2. Export all CSVs at once
3. Upload each CSV via WordPress admin (takes 2-3 minutes total)
4. All pages update automatically
5. Done!

**For Design Changes:**
- Edit template file once
- Changes apply to all trades instantly
- No need to re-upload data
- No need to update pages

### SEO Optimization

The plugin includes SEO features:

1. **HTML Data Table**
   - Visible below the map by default
   - Contains all state data in crawlable format
   - Can be hidden with `show_table="no"` if desired

2. **Schema.org Markup**
   - Automatically added to every map
   - Helps Google understand your data
   - May appear in rich results
   - Validate at: https://validator.schema.org/

3. **Best Practices**
   - Keep table visible for best SEO (default)
   - Add descriptive text above/below map
   - Use proper page titles and meta descriptions
   - Link between related trade pages

### Performance Tips

1. **Use Caching**
   - Install a caching plugin (WP Super Cache recommended)
   - Set to cache pages with shortcodes
   - Clear cache after uploading new data

2. **Optimize Loading**
   - Plugin only loads CSS/JS on pages with shortcode
   - No performance impact on other pages
   - Map assets are lightweight (~50KB total)

3. **Database**
   - Plugin uses efficient queries
   - Data is indexed for fast retrieval
   - No impact on other WordPress operations

---

## Keyboard Shortcuts

When viewing a map page:

- **Tab**: Navigate between metric buttons
- **Enter/Space**: Activate focused button
- **Arrow Keys**: Navigate states (when focused on map)
- **Escape**: Deselect current state

---

## Browser Support

The plugin works in:
- ✅ Chrome (latest)
- ✅ Safari (latest)
- ✅ Firefox (latest)
- ✅ Edge (latest)
- ✅ Mobile Safari (iOS)
- ✅ Chrome Mobile (Android)
- ⚠️ IE11 (basic support, may need polyfills)

---

## Getting Help

### Before Asking for Help

1. Check this user guide
2. Review [Troubleshooting](#troubleshooting) section
3. Check [FAQ](#faq)
4. Look at the CSV template in admin
5. Check WordPress error logs

### Where to Get Help

1. **Plugin Documentation**
   - Read README.md
   - Review INSTALL.md
   - Check SECURITY.md

2. **WordPress Community**
   - WordPress.org support forums
   - WordPress Facebook groups
   - WordPress Slack community

3. **GitHub Issues**
   - Open an issue at: https://github.com/orcaventuresllc/trade-maps/issues
   - Include:
     - WordPress version
     - PHP version
     - Plugin version
     - Error messages
     - Steps to reproduce

### What to Include in Support Requests

- WordPress version
- PHP version
- Theme name and version
- List of active plugins
- Error messages (full text)
- Screenshots of the issue
- Steps you've already tried

---

## Uninstalling

### Deactivate Plugin

1. Go to **Plugins** in WordPress admin
2. Find "Insurance Cost Maps"
3. Click **Deactivate**
4. Plugin stops working but data remains in database

### Delete Plugin

1. Deactivate the plugin first
2. Click **Delete** next to the plugin
3. Confirm deletion
4. Plugin files are removed

**Note**: Deleting the plugin does NOT remove the database table or data. This is intentional to prevent accidental data loss.

### Remove Data Completely

If you want to remove all plugin data:

1. Deactivate and delete the plugin
2. Run this SQL query in phpMyAdmin or similar:
   ```sql
   DROP TABLE IF EXISTS wp_insurance_map_data;
   ```
3. Replace `wp_` with your actual database prefix if different

**Warning**: This permanently deletes all uploaded insurance data. Cannot be undone.

---

## Appendix: State Codes Reference

| Code | State | Code | State |
|------|-------|------|-------|
| AL | Alabama | MT | Montana |
| AK | Alaska | NE | Nebraska |
| AZ | Arizona | NV | Nevada |
| AR | Arkansas | NH | New Hampshire |
| CA | California | NJ | New Jersey |
| CO | Colorado | NM | New Mexico |
| CT | Connecticut | NY | New York |
| DE | Delaware | NC | North Carolina |
| FL | Florida | ND | North Dakota |
| GA | Georgia | OH | Ohio |
| HI | Hawaii | OK | Oklahoma |
| ID | Idaho | OR | Oregon |
| IL | Illinois | PA | Pennsylvania |
| IN | Indiana | RI | Rhode Island |
| IA | Iowa | SC | South Carolina |
| KS | Kansas | SD | South Dakota |
| KY | Kentucky | TN | Tennessee |
| LA | Louisiana | TX | Texas |
| ME | Maine | UT | Utah |
| MD | Maryland | VT | Vermont |
| MA | Massachusetts | VA | Virginia |
| MI | Michigan | WA | Washington |
| MN | Minnesota | WV | West Virginia |
| MS | Mississippi | WI | Wisconsin |
| MO | Missouri | WY | Wyoming |

---

## Version

This user guide is for Insurance Cost Maps plugin version 1.0.0.

Last updated: January 13, 2026
