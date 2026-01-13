# Contributing to Insurance Cost Maps Plugin

Thank you for your interest in contributing! This document provides guidelines for contributing to the Insurance Cost Maps WordPress plugin.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Code Standards](#code-standards)
5. [Security Requirements](#security-requirements)
6. [Testing Requirements](#testing-requirements)
7. [Submission Guidelines](#submission-guidelines)

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other contributors

## Getting Started

### Prerequisites
- WordPress 5.0+ (local installation)
- PHP 7.0+
- MySQL 5.6+
- Git
- Code editor (VS Code, PHPStorm, etc.)

### Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR-USERNAME/trade-maps.git
cd trade-maps
```

### Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number
```

## Development Setup

### Local WordPress Environment

**Option 1: Local by Flywheel** (Recommended)
```bash
# Install Local by Flywheel
# Create new site
# Copy plugin folder to wp-content/plugins/
```

**Option 2: Docker**
```bash
docker-compose up -d
# Copy plugin to wordpress/wp-content/plugins/
```

**Option 3: MAMP/XAMPP**
```bash
# Install MAMP/XAMPP
# Set up WordPress
# Copy plugin to wp-content/plugins/
```

### Enable Debug Mode
```php
// In wp-config.php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
define('SCRIPT_DEBUG', true);
```

### Install Plugin
1. Copy `/plugin/` directory to `/wp-content/plugins/insurance-maps/`
2. Activate plugin in WordPress admin
3. Upload sample CSV files from `/sample-data/`
4. Test shortcode on a page

## Code Standards

### WordPress Coding Standards

Follow [WordPress Coding Standards](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/):

```php
// ✅ Good
function my_function() {
    if ( condition ) {
        do_something();
    }
}

// ❌ Bad
function my_function(){
  if(condition){
    do_something();
  }
}
```

### PHP Standards

- **PHP Version**: Compatible with PHP 7.0+
- **Type Hints**: Use when possible (PHP 7.0+)
- **Error Handling**: Use WP_Error for error returns
- **Naming**:
  - Classes: `Insurance_Maps_Class_Name`
  - Functions: `insurance_maps_function_name`
  - Variables: `$descriptive_name`

### JavaScript Standards

- **ES5 Only**: No ES6+ features
  - No `const` or `let` (use `var`)
  - No arrow functions (use `function`)
  - No template literals (use string concatenation)
  - No classes (use constructor functions)

```javascript
// ✅ Good (ES5)
var myVar = 'value';
function myFunction() {
    return 'result';
}

// ❌ Bad (ES6+)
const myVar = 'value';
const myFunction = () => 'result';
```

### CSS Standards

- **No Preprocessors**: Plain CSS only
- **Namespacing**: Prefix classes with `insurance-map-` or use unique container IDs
- **Mobile-First**: Use min-width media queries where appropriate
- **Browser Prefixes**: Include vendor prefixes for compatibility

### Documentation Standards

- **PHPDoc**: All functions must have PHPDoc comments
- **Inline Comments**: Explain complex logic
- **README**: Update README.md for new features
- **Changelog**: Update CHANGELOG.md with all changes

## Security Requirements

### CRITICAL: Security Checklist

All code must pass these security checks:

#### Input Validation
- [ ] All `$_GET`/`$_POST` variables sanitized
- [ ] All file uploads validated (extension, MIME type, size)
- [ ] All numeric inputs validated within acceptable ranges
- [ ] All text inputs sanitized with `sanitize_text_field()`
- [ ] All URLs sanitized with `esc_url()`

#### Output Escaping
- [ ] All HTML content escaped with `esc_html()`
- [ ] All HTML attributes escaped with `esc_attr()`
- [ ] All JavaScript strings escaped with `esc_js()`
- [ ] All URLs escaped with `esc_url()`
- [ ] No raw `echo` of user input

#### Database Security
- [ ] All queries use `$wpdb->prepare()`
- [ ] No SQL string concatenation
- [ ] All table names use `$wpdb->prefix`
- [ ] Numeric values cast to appropriate types
- [ ] Transactions used for bulk operations

#### Access Control
- [ ] All admin functions check `current_user_can('manage_options')`
- [ ] All admin actions verify nonces
- [ ] All PHP files have ABSPATH checks
- [ ] No hardcoded credentials

#### File Security
- [ ] No eval() or similar dangerous functions
- [ ] No user input in file paths
- [ ] All file operations validated
- [ ] Uploaded files stored securely

### Security Testing

Before submitting, test for:
- SQL injection attempts
- XSS attempts (script tags in CSV data)
- CSRF attacks (submitting without nonce)
- Path traversal attempts
- File upload exploits

## Testing Requirements

### Required Tests

All contributions must pass:

1. **Functional Tests**
   - Plugin activates without errors
   - Admin interface loads correctly
   - CSV upload works
   - Data displays correctly
   - Shortcode renders map
   - All interactive features work

2. **Browser Tests**
   - Chrome (latest)
   - Safari (latest)
   - Firefox (latest)
   - Edge (latest)
   - Mobile browsers

3. **WordPress Compatibility**
   - Test with latest WordPress version
   - Test with Kadence theme
   - Test with default theme
   - Test with Gutenberg editor
   - Test with Classic editor

4. **Security Tests**
   - Upload invalid files
   - Try SQL injection
   - Try XSS attacks
   - Test without nonces
   - Test as non-admin user

5. **Performance Tests**
   - Page load time < 3 seconds
   - No excessive database queries
   - No JavaScript errors

### Testing Locally

```bash
# Run WordPress with debug enabled
# Check wp-content/debug.log for errors

# Test CSV upload
# Upload sample-data/carpenter.csv
# Verify 50 states imported

# Test shortcode
# Add [insurance_map trade="carpenter"] to a page
# Verify map displays

# Test all metrics
# Click each metric button
# Verify heat map updates

# Test state selection
# Click different states
# Verify info panel updates
```

## Submission Guidelines

### Pull Request Process

1. **Update your fork**
   ```bash
   git checkout master
   git pull upstream master
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow code standards
   - Add security measures
   - Test thoroughly
   - Update documentation

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to GitHub repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out PR template
   - Submit for review

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Security improvement
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tested locally
- [ ] No errors in debug.log
- [ ] Cross-browser tested
- [ ] Security tested
- [ ] Mobile tested

## Checklist
- [ ] Code follows WordPress Coding Standards
- [ ] All security requirements met
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or clearly documented)

## Screenshots
(If applicable)
```

### Commit Message Format

```
Type: Brief description (50 chars or less)

More detailed explanation if needed. Wrap at 72 characters.
Explain what and why, not how.

- Bullet points are okay
- Use present tense ("Add feature" not "Added feature")

Fixes #123
```

**Types**: `Add`, `Update`, `Fix`, `Remove`, `Refactor`, `Security`, `Docs`

## Development Workflow

### Adding a New Feature

1. Discuss feature in GitHub issue first
2. Get approval before starting
3. Create feature branch
4. Implement feature
5. Add tests
6. Update documentation
7. Submit pull request

### Fixing a Bug

1. Create issue describing bug
2. Create bugfix branch
3. Write test that reproduces bug
4. Fix the bug
5. Verify test passes
6. Submit pull request

### Security Fixes

1. **DO NOT** create public issue for security vulnerabilities
2. Email security contact privately
3. Work with maintainer on fix
4. Coordinated disclosure after fix is released

## Code Review Process

All contributions will be reviewed for:

1. **Code Quality**
   - Follows WordPress Coding Standards
   - Clean, readable code
   - Proper documentation
   - No unnecessary complexity

2. **Security**
   - All security requirements met
   - No vulnerabilities introduced
   - Input validated, output escaped
   - Capability checks in place

3. **Functionality**
   - Feature works as described
   - No regressions
   - Edge cases handled
   - Error handling implemented

4. **Testing**
   - Adequate test coverage
   - All tests pass
   - Browser compatibility verified
   - No console errors

5. **Documentation**
   - Code is documented
   - README updated if needed
   - CHANGELOG updated
   - User-facing changes explained

## Questions?

- Open a GitHub issue for questions
- Tag maintainers for help
- Check existing issues/PRs first

## License

By contributing, you agree that your contributions will be licensed under the GPL v2 or later license.

## Attribution

Contributors will be recognized in:
- README.md contributors section
- Git commit history
- Release notes

Thank you for contributing!
