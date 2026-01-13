# Installation Guide - Insurance Cost Maps Plugin

Complete step-by-step installation guide for WordPress administrators.

## Prerequisites

Before installing, ensure you have:

- ✅ WordPress 5.0 or higher
- ✅ PHP 7.0 or higher
- ✅ MySQL 5.6 or higher
- ✅ WordPress administrator access
- ✅ Ability to upload plugins

**To check your versions:**
1. Go to WordPress admin → Tools → Site Health
2. Click "Info" tab
3. Check WordPress Version and Server sections

---

## Installation Methods

Choose one of three methods based on your preference and access level.

---

## Method 1: Automatic Installation via WordPress Admin (Recommended)

This is the easiest method and works for most users.

### Step 1: Download Plugin

1. Download `insurance-maps-v1.0.0.zip` to your computer
2. Remember where you saved it (usually Downloads folder)
3. Do NOT unzip the file

### Step 2: Access WordPress Admin

1. Log in to your WordPress website
2. Go to your admin dashboard (usually `yoursite.com/wp-admin`)
3. Enter your admin credentials

### Step 3: Upload Plugin

1. In WordPress admin, hover over **Plugins** in the left menu
2. Click **Add New**
3. Click the **Upload Plugin** button at the top of the page
4. Click **Choose File**
5. Select the `insurance-maps-v1.0.0.zip` file
6. Click **Install Now**

### Step 4: Activate Plugin

1. Wait for upload to complete (usually 5-10 seconds)
2. You'll see "Plugin installed successfully"
3. Click the **Activate Plugin** button
4. You should see "Plugin activated" message

### Step 5: Verify Installation

1. Look for **Insurance Maps** in the left admin menu
2. If you see it, installation was successful!
3. Click on it to access the admin page

### Step 6: Check for Errors

1. Go to **Tools → Site Health → Info → Server**
2. Check that no errors are shown
3. If you enabled debug mode, check `wp-content/debug.log` for any errors

---

## Method 2: Manual Installation via FTP

Use this method if:
- You have FTP access to your server
- WordPress upload limits are too small
- You prefer manual file management

### Step 1: Download and Unzip

1. Download `insurance-maps-v1.0.0.zip`
2. Unzip the file on your computer
3. You should see an `insurance-maps` folder

### Step 2: Connect via FTP

1. Open your FTP client (FileZilla, Cyberduck, etc.)
2. Connect to your web server
3. Navigate to your WordPress installation

### Step 3: Upload Plugin Files

1. Navigate to `/wp-content/plugins/` directory
2. Upload the entire `insurance-maps` folder
3. Wait for all files to upload (may take 1-2 minutes)
4. Verify all files and folders are present

### Step 4: Activate Plugin

1. Go to WordPress admin → **Plugins**
2. Find "Insurance Cost Maps" in the list
3. Click **Activate**
4. Check for "Plugin activated" message

### Step 5: Verify Installation

1. Check for **Insurance Maps** in admin menu
2. Click it to verify the admin page loads
3. Check `wp-content/debug.log` for any errors (if debug mode enabled)

---

## Method 3: Installation via WP-CLI

Use this method if you have command-line access to your server.

### Step 1: Upload ZIP to Server

```bash
# SSH into your server
ssh user@yourserver.com

# Navigate to WordPress directory
cd /path/to/wordpress

# Upload the ZIP file (or use wget/curl to download)
```

### Step 2: Install Plugin

```bash
# Install from local ZIP file
wp plugin install /path/to/insurance-maps-v1.0.0.zip --activate

# Or install from URL
wp plugin install https://yoursite.com/path/insurance-maps-v1.0.0.zip --activate
```

### Step 3: Verify Installation

```bash
# Check if plugin is active
wp plugin list | grep insurance-maps

# Should show:
# insurance-maps  1.0.0  active
```

---

## Post-Installation Setup

After installing and activating the plugin, follow these steps to get started.

### Step 1: Access Admin Interface

1. Go to WordPress admin
2. Click **Insurance Maps** in the left menu
3. You should see the admin page with:
   - Upload form
   - Instructions
   - CSV template

### Step 2: Prepare Your Data

You have two options:

**Option A: Use Sample Data** (Quick Start)
1. Navigate to the `sample-data/` folder in the GitHub repository
2. Download CSV files for the trades you want
3. These contain pre-populated insurance data

**Option B: Create Your Own Data**
1. Create a new Google Sheet or Excel file
2. Add these column headers (exact spelling):
   ```
   State,GL_Premium_Low,GL_Premium_High,GL_Savings,GL_Competitiveness,WC_Rate_5437,WC_Rate_5645
   ```
3. Add data for all 50 states
4. Export as CSV

### Step 3: Upload CSV Files

For each trade you want to display:

1. In the **Upload CSV Data** section:
   - Enter trade name (lowercase, no spaces)
     - Examples: `carpenter`, `electrician`, `plumber`
   - Click **Choose File**
   - Select your CSV file
   - Click **Upload CSV**

2. Wait for success message:
   - "Successfully imported 50 states for carpenter"

3. Repeat for each trade

### Step 4: Copy Shortcodes

1. Find your trade in the **Existing Trade Maps** list
2. You'll see something like:
   ```
   [insurance_map trade="carpenter"]
   ```
3. Click the **Copy** button
4. The shortcode is copied to your clipboard

### Step 5: Add Maps to Pages

1. Create a new page or edit an existing one
2. In the content editor:
   - **Gutenberg**: Add a "Shortcode" block, paste shortcode
   - **Classic Editor**: Paste shortcode directly
   - **Page Builders**: Add shortcode element, paste shortcode

3. Click **Preview** to see the map
4. If it looks good, click **Publish** or **Update**

### Step 6: Test Everything

1. View the published page
2. Verify the map displays correctly
3. Try clicking different metric buttons
4. Click on different states
5. Check that the info panel updates
6. Test on mobile device (or resize browser)

---

## Database Table

The plugin creates one database table:

**Table Name**: `wp_insurance_map_data` (or `{your-prefix}_insurance_map_data`)

**Structure**:
```sql
CREATE TABLE wp_insurance_map_data (
    id mediumint(9) AUTO_INCREMENT,
    trade varchar(50) NOT NULL,
    state_code varchar(2) NOT NULL,
    gl_premium_low decimal(4,2),
    gl_premium_high decimal(4,2),
    gl_savings decimal(5,2),
    gl_competitiveness int,
    wc_rate_5437 decimal(5,2),
    wc_rate_5645 decimal(5,2),
    updated_at datetime,
    PRIMARY KEY (id),
    UNIQUE KEY trade_state (trade, state_code)
)
```

This table is created automatically when you activate the plugin.

---

## Troubleshooting Installation

### Plugin Won't Activate

**Error: "The plugin does not have a valid header"**
- Solution: Re-download the ZIP file and try again
- Ensure ZIP file is not corrupted

**Error: "Plugin could not be activated because it triggered a fatal error"**
- Check PHP version (must be 7.0+)
- Check error logs for specific error message
- Ensure no file corruption during upload

### Can't Find Plugin in Admin

**After activation, "Insurance Maps" doesn't appear in menu**
- Solution: Clear browser cache and reload
- Check if plugin is actually activated (Plugins page)
- Check user has administrator role

### Database Table Not Created

**Error when trying to upload CSV**
- Solution: Deactivate and reactivate plugin
- Check database permissions
- Check MySQL version (must be 5.6+)
- Manually run activation function

### Upload Size Limits

**Error: "The uploaded file exceeds the upload_max_filesize directive"**
- This is a PHP/server limit, not the plugin
- Solution: Increase PHP upload limits
- Edit `php.ini`:
  ```ini
  upload_max_filesize = 10M
  post_max_size = 10M
  ```
- Or ask your hosting provider to increase limits

### Permission Errors

**Error: "Sorry, you are not allowed to access this page"**
- Ensure you're logged in as administrator
- Check user capabilities
- Try logging out and back in

---

## Upgrading

### From Future Versions

When version 1.1.0 or higher is released:

1. **Backup First**
   - Backup your WordPress database
   - Backup plugin files (optional)

2. **Automatic Update**
   - WordPress will show update notification
   - Click "Update Now"
   - Wait for completion

3. **Manual Update**
   - Download new version ZIP
   - Deactivate old version
   - Delete old version
   - Upload and activate new version
   - Your data is preserved

### Migration from HTML Files

If you're upgrading from the old HTML file approach:

1. Install plugin (steps above)
2. Use `extract-csv-data.py` script to extract data from HTML files
3. Upload extracted CSV files via admin
4. Replace HTML in pages with shortcodes
5. Test all pages
6. Archive old HTML files

---

## System Requirements

### Minimum Requirements
- WordPress 5.0+
- PHP 7.0+
- MySQL 5.6+
- Apache or Nginx web server
- 128MB PHP memory limit

### Recommended Requirements
- WordPress 6.0+
- PHP 8.0+
- MySQL 8.0+
- 256MB PHP memory limit
- SSL certificate (HTTPS)

### Server Configuration

**PHP Extensions Required:**
- `mysqli` - Database connectivity
- `fileinfo` - MIME type detection
- `json` - JSON encoding/decoding

**WordPress Configuration:**
```php
// Recommended wp-config.php settings
define('WP_MEMORY_LIMIT', '256M');
define('WP_MAX_MEMORY_LIMIT', '512M');
```

---

## Getting Started

After successful installation, see:
- **USER-GUIDE.md** for complete usage instructions
- **README.md** for plugin overview and features
- **SECURITY.md** for security best practices

---

## Support

For installation issues:
- Check [Troubleshooting Installation](#troubleshooting-installation) section above
- Review WordPress error logs (`wp-content/debug.log`)
- Open a GitHub issue with error details
- Contact WordPress support community

## License

GPL v2 or later - https://www.gnu.org/licenses/gpl-2.0.html
