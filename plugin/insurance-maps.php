<?php
/**
 * Plugin Name: Insurance Cost Maps
 * Plugin URI: https://github.com/orcaventuresllc/trade-maps
 * Description: Interactive US maps displaying insurance cost metrics by trade and state. Upload CSV files to manage data and use shortcodes to display maps.
 * Version: 1.1.2
 * Author: Orca Ventures LLC
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: insurance-maps
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('INSURANCE_MAPS_VERSION', '1.1.2');
define('INSURANCE_MAPS_PATH', plugin_dir_path(__FILE__));
define('INSURANCE_MAPS_URL', plugin_dir_url(__FILE__));

// Load dependencies
require_once INSURANCE_MAPS_PATH . 'includes/class-data-manager.php';
require_once INSURANCE_MAPS_PATH . 'includes/class-shortcode.php';

// Admin interface (only load in admin)
if (is_admin()) {
    require_once INSURANCE_MAPS_PATH . 'admin/admin-page.php';
    require_once INSURANCE_MAPS_PATH . 'admin/csv-uploader.php';
}

/**
 * Activation hook - create database table
 */
register_activation_hook(__FILE__, 'insurance_maps_activate');
function insurance_maps_activate() {
    global $wpdb;
    $table_name = $wpdb->prefix . 'insurance_map_data';

    $charset_collate = $wpdb->get_charset_collate();

    // Updated schema with flexible WC columns
    $sql = "CREATE TABLE $table_name (
        id mediumint(9) NOT NULL AUTO_INCREMENT,
        trade varchar(50) NOT NULL,
        state_code varchar(2) NOT NULL,
        gl_premium_low decimal(4,2) NOT NULL,
        gl_premium_high decimal(4,2) NOT NULL,
        gl_savings decimal(5,2) NOT NULL,
        gl_competitiveness int NOT NULL,
        wc_class_1 varchar(10) DEFAULT NULL,
        wc_rate_1 decimal(5,2) DEFAULT NULL,
        wc_label_1 varchar(50) DEFAULT NULL,
        wc_class_2 varchar(10) DEFAULT NULL,
        wc_rate_2 decimal(5,2) DEFAULT NULL,
        wc_label_2 varchar(50) DEFAULT NULL,
        updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY  (id),
        UNIQUE KEY trade_state (trade, state_code)
    ) $charset_collate;";

    require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
    dbDelta($sql);

    // Set version
    update_option('insurance_maps_version', INSURANCE_MAPS_VERSION);
}

/**
 * Check and migrate database schema on plugin load
 * Handles upgrades from v1.0 to v1.1 (adds WC class columns)
 */
add_action('plugins_loaded', 'insurance_maps_check_schema');
function insurance_maps_check_schema() {
    global $wpdb;
    $table_name = $wpdb->prefix . 'insurance_map_data';

    // Check if table exists first
    if ($wpdb->get_var("SHOW TABLES LIKE '$table_name'") !== $table_name) {
        return; // Table doesn't exist yet, will be created on activation
    }

    // Get current columns
    $columns = $wpdb->get_col("DESCRIBE {$table_name}", 0);

    // Check if migration needed (old columns exist but new ones don't)
    $needs_migration = in_array('wc_rate_5437', $columns) && !in_array('wc_class_1', $columns);

    if ($needs_migration) {
        // Add new WC class columns
        $wpdb->query("ALTER TABLE {$table_name}
            ADD COLUMN wc_class_1 varchar(10) DEFAULT NULL AFTER gl_competitiveness,
            ADD COLUMN wc_label_1 varchar(50) DEFAULT NULL AFTER wc_class_1,
            ADD COLUMN wc_class_2 varchar(10) DEFAULT NULL AFTER wc_label_1,
            ADD COLUMN wc_label_2 varchar(50) DEFAULT NULL AFTER wc_class_2");

        // Rename old columns to new generic names
        $wpdb->query("ALTER TABLE {$table_name}
            CHANGE COLUMN wc_rate_5437 wc_rate_1 decimal(5,2) DEFAULT NULL,
            CHANGE COLUMN wc_rate_5645 wc_rate_2 decimal(5,2) DEFAULT NULL");

        // Set default class codes for existing data (carpenter format)
        $wpdb->query("UPDATE {$table_name}
            SET wc_class_1 = '5437', wc_label_1 = 'Interior',
                wc_class_2 = '5645', wc_label_2 = 'Framing'
            WHERE wc_class_1 IS NULL");

        // Update version
        update_option('insurance_maps_version', INSURANCE_MAPS_VERSION);
    }
}

/**
 * Initialize shortcode
 */
add_action('init', 'insurance_maps_init_shortcode');
function insurance_maps_init_shortcode() {
    new Insurance_Maps_Shortcode();
}

/**
 * Enqueue assets on frontend
 */
add_action('wp_enqueue_scripts', 'insurance_maps_enqueue_assets');
function insurance_maps_enqueue_assets() {
    // Only enqueue if shortcode is present on the page
    global $post;
    if (is_a($post, 'WP_Post') && has_shortcode($post->post_content, 'insurance_map')) {
        wp_enqueue_style(
            'insurance-maps-styles',
            INSURANCE_MAPS_URL . 'assets/css/map-styles.css',
            array(),
            INSURANCE_MAPS_VERSION
        );

        wp_enqueue_script(
            'insurance-maps-interactive',
            INSURANCE_MAPS_URL . 'assets/js/map-interactive.js',
            array(),
            INSURANCE_MAPS_VERSION,
            true
        );
    }
}

/**
 * Add security headers to admin pages
 */
add_action('admin_init', 'insurance_maps_security_headers');
function insurance_maps_security_headers() {
    if (is_admin() && isset($_GET['page']) && $_GET['page'] === 'insurance-maps') {
        header('X-Content-Type-Options: nosniff');
        header('X-Frame-Options: SAMEORIGIN');
        header('X-XSS-Protection: 1; mode=block');
    }
}
