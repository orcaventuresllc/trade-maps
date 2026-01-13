<?php
/**
 * Plugin Name: Insurance Cost Maps
 * Plugin URI: https://github.com/orcaventuresllc/trade-maps
 * Description: Interactive US maps displaying insurance cost metrics by trade and state. Upload CSV files to manage data and use shortcodes to display maps.
 * Version: 1.0.0
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
define('INSURANCE_MAPS_VERSION', '1.0.0');
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

    $sql = "CREATE TABLE $table_name (
        id mediumint(9) NOT NULL AUTO_INCREMENT,
        trade varchar(50) NOT NULL,
        state_code varchar(2) NOT NULL,
        gl_premium_low decimal(4,2) NOT NULL,
        gl_premium_high decimal(4,2) NOT NULL,
        gl_savings decimal(5,2) NOT NULL,
        gl_competitiveness int NOT NULL,
        wc_rate_5437 decimal(5,2) NOT NULL,
        wc_rate_5645 decimal(5,2) NOT NULL,
        updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY  (id),
        UNIQUE KEY trade_state (trade, state_code)
    ) $charset_collate;";

    require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
    dbDelta($sql);

    // Set version
    add_option('insurance_maps_version', INSURANCE_MAPS_VERSION);
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
