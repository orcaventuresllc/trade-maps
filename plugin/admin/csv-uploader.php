<?php
/**
 * Insurance Maps CSV Upload Handler
 * Processes CSV file uploads and manages trade data
 */

// Handle CSV upload
add_action('admin_post_insurance_maps_upload_csv', 'insurance_maps_handle_csv_upload');
function insurance_maps_handle_csv_upload() {
    // Security checks
    if (!current_user_can('manage_options')) {
        wp_die('Unauthorized access');
    }

    check_admin_referer('insurance_maps_upload', 'insurance_maps_nonce');

    $trade = sanitize_text_field($_POST['trade']);

    // Validate trade name (lowercase, no spaces)
    if (!preg_match('/^[a-z]+$/', $trade)) {
        wp_redirect(add_query_arg('message', 'invalid_trade_name', wp_get_referer()));
        exit;
    }

    // Handle file upload
    if (!isset($_FILES['csv_file']) || $_FILES['csv_file']['error'] !== UPLOAD_ERR_OK) {
        wp_redirect(add_query_arg('message', 'upload_error', wp_get_referer()));
        exit;
    }

    $file = $_FILES['csv_file'];

    // Validate file type
    $file_ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    if ($file_ext !== 'csv') {
        wp_redirect(add_query_arg('message', 'invalid_file', wp_get_referer()));
        exit;
    }

    // Check file size (max 5MB)
    $max_size = 5 * 1024 * 1024; // 5MB in bytes
    if ($file['size'] > $max_size) {
        wp_redirect(add_query_arg('message', 'file_too_large', wp_get_referer()));
        exit;
    }

    // Import data
    $data_manager = new Insurance_Maps_Data_Manager();
    $result = $data_manager->import_csv($file['tmp_name'], $trade);

    if (is_wp_error($result)) {
        // Get error message and encode it for URL
        $error_message = urlencode($result->get_error_message());
        wp_redirect(add_query_arg(array(
            'message' => 'import_error',
            'error_details' => $error_message
        ), wp_get_referer()));
        exit;
    }

    // Success
    wp_redirect(add_query_arg(array(
        'message' => 'upload_success',
        'imported' => $result,
        'trade' => $trade
    ), wp_get_referer()));
    exit;
}

// Handle delete action
add_action('admin_post_insurance_maps_delete', 'insurance_maps_handle_delete');
function insurance_maps_handle_delete() {
    if (!current_user_can('manage_options')) {
        wp_die('Unauthorized access');
    }

    $trade = sanitize_text_field($_GET['trade']);
    check_admin_referer('delete_trade_' . $trade);

    $data_manager = new Insurance_Maps_Data_Manager();
    $deleted = $data_manager->delete_trade_data($trade);

    if ($deleted === false) {
        wp_redirect(add_query_arg('message', 'delete_error', admin_url('admin.php?page=insurance-maps')));
    } else {
        wp_redirect(add_query_arg(array(
            'message' => 'delete_success',
            'trade' => $trade,
            'count' => $deleted
        ), admin_url('admin.php?page=insurance-maps')));
    }
    exit;
}

// Display admin notices
add_action('admin_notices', 'insurance_maps_admin_notices');
function insurance_maps_admin_notices() {
    if (!isset($_GET['page']) || $_GET['page'] !== 'insurance-maps') {
        return;
    }

    if (!isset($_GET['message'])) {
        return;
    }

    $message = $_GET['message'];
    $class = 'notice notice-success is-dismissible';
    $text = '';

    switch ($message) {
        case 'upload_success':
            $imported = isset($_GET['imported']) ? intval($_GET['imported']) : 0;
            $trade = isset($_GET['trade']) ? sanitize_text_field($_GET['trade']) : 'trade';
            $text = sprintf(
                '<strong>Success!</strong> Imported %d states for <strong>%s</strong>. Use shortcode: <code>[insurance_map trade="%s"]</code>',
                $imported,
                ucfirst($trade),
                $trade
            );
            break;

        case 'delete_success':
            $trade = isset($_GET['trade']) ? sanitize_text_field($_GET['trade']) : 'trade';
            $count = isset($_GET['count']) ? intval($_GET['count']) : 0;
            $text = sprintf(
                '<strong>Deleted!</strong> Removed %d records for <strong>%s</strong>.',
                $count,
                ucfirst($trade)
            );
            break;

        case 'upload_error':
            $class = 'notice notice-error is-dismissible';
            $text = '<strong>Upload Error:</strong> Failed to upload file. Please try again.';
            break;

        case 'invalid_file':
            $class = 'notice notice-error is-dismissible';
            $text = '<strong>Invalid File:</strong> Please upload a CSV file (.csv extension).';
            break;

        case 'file_too_large':
            $class = 'notice notice-error is-dismissible';
            $text = '<strong>File Too Large:</strong> Maximum file size is 5MB.';
            break;

        case 'invalid_trade_name':
            $class = 'notice notice-error is-dismissible';
            $text = '<strong>Invalid Trade Name:</strong> Trade name must be lowercase letters only, no spaces.';
            break;

        case 'import_error':
            $class = 'notice notice-error is-dismissible';
            $error_details = isset($_GET['error_details']) ? urldecode($_GET['error_details']) : 'Unknown error';
            $text = '<strong>Import Error:</strong> ' . esc_html($error_details);
            break;

        case 'delete_error':
            $class = 'notice notice-error is-dismissible';
            $text = '<strong>Delete Error:</strong> Failed to delete trade data. Please try again.';
            break;

        default:
            return;
    }

    if (!empty($text)) {
        printf('<div class="%s"><p>%s</p></div>', esc_attr($class), $text);
    }
}
