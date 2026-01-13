# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ Yes             |

## Reporting a Vulnerability

If you discover a security vulnerability in this plugin, please report it responsibly:

1. **DO NOT** open a public GitHub issue
2. Email security details to your security contact email
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

We will respond within 48 hours and work with you to address the issue.

## Security Features

### Input Validation & Sanitization

#### File Uploads
- **Extension Validation**: Only `.csv` files accepted
- **MIME Type Validation**: Verifies file is actually CSV format
- **File Size Limit**: Maximum 5MB per upload
- **Filename Sanitization**: Uses WordPress `sanitize_file_name()`
- **Content Validation**: Validates all CSV data before import

#### CSV Data Validation
- **State Codes**: Must be 2 uppercase letters (AL, AK, etc.)
- **Numeric Ranges**: All values validated within acceptable ranges
  - GL Premium: 0-100%
  - GL Savings: 0-100%
  - GL Competitiveness: 0-100
  - WC Rates: 0-1000
- **Data Integrity**: Low values cannot exceed high values
- **Column Count**: Must have exactly 7 columns

#### User Input
- **Trade Names**: Validated with regex `/^[a-z]+$/` (lowercase letters only)
- **Text Fields**: Sanitized with `sanitize_text_field()`
- **URLs**: Sanitized with `esc_url()`

### SQL Injection Protection

- **Prepared Statements**: All database queries use `$wpdb->prepare()`
- **No String Concatenation**: No SQL queries built with user input
- **Type Casting**: All numeric values cast to appropriate types
- **Replace Method**: Uses `$wpdb->replace()` with array format (safe)
- **Delete Method**: Uses `$wpdb->delete()` with array format and type hints

### Cross-Site Scripting (XSS) Prevention

- **Output Escaping**: All dynamic content properly escaped
  - `esc_html()` for HTML content
  - `esc_attr()` for HTML attributes
  - `esc_js()` for JavaScript strings
  - `esc_url()` for URLs
- **No Raw Output**: No `echo` of user input without escaping
- **Admin Interface**: All user-generated content escaped

### Cross-Site Request Forgery (CSRF) Protection

- **Nonces**: All form submissions require valid nonces
  - Upload form: `wp_nonce_field('insurance_maps_upload', 'insurance_maps_nonce')`
  - Delete action: Dynamic nonces per trade
- **Nonce Verification**: All actions verify nonces before processing
  - `check_admin_referer()` for form submissions
  - `wp_nonce_url()` for URL-based actions

### Access Control

- **Capability Checks**: All admin functions require `manage_options` capability
- **Direct Access Prevention**: All PHP files check for `ABSPATH` constant
- **Admin-Only Files**: Admin files only load when `is_admin()` is true
- **No Unauthorized Access**: Non-admin users cannot access admin functions

### Rate Limiting

- **Upload Limits**: Maximum 10 CSV uploads per hour per user
- **Transient-Based**: Uses WordPress transients for tracking
- **User-Specific**: Limits apply per user ID
- **Automatic Reset**: Limits reset after 1 hour

### Security Headers

The following security headers are sent on admin pages:

- **X-Content-Type-Options: nosniff** - Prevents MIME sniffing
- **X-Frame-Options: SAMEORIGIN** - Prevents clickjacking
- **X-XSS-Protection: 1; mode=block** - Enables XSS filter

### Database Security

- **Table Prefix**: Uses `$wpdb->prefix` for multi-site compatibility
- **Character Encoding**: Uses `$wpdb->get_charset_collate()`
- **Transactions**: Bulk imports use transactions for integrity
- **Unique Constraints**: Prevents duplicate data (trade + state_code)
- **Auto-Update Timestamp**: Tracks when data was last modified

## Security Best Practices for Users

### WordPress Security
1. **Keep WordPress Updated**: Always use the latest version
2. **Strong Passwords**: Use strong, unique passwords for admin accounts
3. **Limit Admin Access**: Only give admin access to trusted users
4. **Regular Backups**: Backup your database regularly
5. **SSL/HTTPS**: Use SSL certificate for encrypted connections
6. **Security Plugins**: Consider using security plugins (Wordfence, Sucuri, etc.)

### Plugin Security
1. **Update Plugin**: Keep this plugin updated to latest version
2. **Monitor Uploads**: Review uploaded CSV files for accuracy
3. **Limit Admin Users**: Only admins can upload CSV files
4. **Check Error Logs**: Monitor WordPress error logs for suspicious activity
5. **Database Backups**: Backup before bulk data imports

### CSV File Security
1. **Trusted Sources**: Only upload CSV files from trusted sources
2. **Validate Data**: Review CSV data before uploading
3. **No Sensitive Data**: Don't include sensitive/personal information in CSV files
4. **Virus Scan**: Scan CSV files before uploading (if from external sources)

## Known Limitations

### Not Implemented
- File upload virus scanning (use server-level antivirus)
- Two-factor authentication (use WordPress 2FA plugins)
- Audit logging (use WordPress activity log plugins)
- IP-based rate limiting (use server-level firewall)

### Why These Are Acceptable
- This plugin has minimal attack surface (admin-only functionality)
- WordPress core provides authentication and session management
- Other plugins/server tools better suited for logging and 2FA
- Rate limiting prevents brute force attacks on upload

## Security Audit Results

### Automated Scans
- No known vulnerabilities in WordPress core functions used
- No external dependencies (no supply chain risks)
- ES5 JavaScript (no modern JS vulnerabilities)

### Manual Review
- All OWASP Top 10 vulnerabilities addressed
- WordPress Coding Standards followed
- Capability checks properly implemented
- Input validation comprehensive
- Output escaping complete

## Changelog

### Version 1.0.0 (2026-01-13)
- Initial release with security features:
  - SQL injection protection
  - XSS prevention
  - CSRF protection
  - File upload validation
  - Rate limiting
  - Security headers
  - CSV content validation

## Security Contact

For security issues, please contact:
- Email: [Your security email]
- Response time: Within 48 hours
- Disclosure: Coordinated disclosure preferred

## Attribution

Security best practices based on:
- WordPress Plugin Security Guidelines
- OWASP Top 10 Web Application Security Risks
- WordPress Coding Standards
- PHP Security Best Practices
