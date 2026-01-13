<?php
/**
 * Insurance Maps Admin Interface
 * Creates admin menu and page for managing insurance cost data
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Add admin menu
add_action('admin_menu', 'insurance_maps_add_admin_menu');
function insurance_maps_add_admin_menu() {
    add_menu_page(
        'Insurance Maps',           // Page title
        'Insurance Maps',           // Menu title
        'manage_options',           // Capability
        'insurance-maps',           // Menu slug
        'insurance_maps_admin_page', // Callback function
        'dashicons-location-alt',   // Icon
        30                          // Position
    );
}

// Render admin page
function insurance_maps_admin_page() {
    $data_manager = new Insurance_Maps_Data_Manager();
    $trades = $data_manager->get_available_trades();

    ?>
    <div class="wrap">
        <h1>Insurance Cost Maps</h1>
        <p>Manage insurance cost data for interactive US maps. Upload CSV files for each trade and use shortcodes to display maps on your pages.</p>

        <!-- Upload Section -->
        <div class="card" style="max-width: 800px; margin: 20px 0;">
            <h2>Upload CSV Data</h2>
            <form method="post" enctype="multipart/form-data" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                <input type="hidden" name="action" value="insurance_maps_upload_csv">
                <?php wp_nonce_field('insurance_maps_upload', 'insurance_maps_nonce'); ?>

                <table class="form-table">
                    <tr>
                        <th scope="row"><label for="trade">Trade</label></th>
                        <td>
                            <input type="text" name="trade" id="trade" class="regular-text" required
                                   placeholder="e.g., carpenter, electrician, plumber" pattern="[a-z]+" title="Lowercase letters only, no spaces">
                            <p class="description">Enter the trade name (lowercase, no spaces). Examples: carpenter, electrician, plumber, hvac, gc, landscaping, painter</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row"><label for="csv_file">CSV File</label></th>
                        <td>
                            <input type="file" name="csv_file" id="csv_file" accept=".csv" required>
                            <p class="description">
                                <strong>Required columns:</strong> State, GL_Premium_Low, GL_Premium_High, GL_Savings, GL_Competitiveness, WC_Rate_5437, WC_Rate_5645<br>
                                <strong>Note:</strong> Uploading a CSV for an existing trade will replace all data for that trade.
                            </p>
                        </td>
                    </tr>
                </table>

                <?php submit_button('Upload CSV'); ?>
            </form>
        </div>

        <!-- Existing Trades -->
        <div class="card" style="max-width: 800px;">
            <h2>Existing Trade Maps</h2>
            <?php if (empty($trades)): ?>
                <p>No trade data uploaded yet. Upload a CSV file above to get started.</p>
            <?php else: ?>
                <table class="wp-list-table widefat fixed striped">
                    <thead>
                        <tr>
                            <th style="width: 20%;">Trade</th>
                            <th style="width: 15%;">States</th>
                            <th style="width: 45%;">Shortcode</th>
                            <th style="width: 20%;">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($trades as $trade):
                            $state_count = $data_manager->get_trade_state_count($trade);
                        ?>
                            <tr>
                                <td><strong><?php echo esc_html(ucfirst($trade)); ?></strong></td>
                                <td><?php echo esc_html($state_count); ?>/50</td>
                                <td>
                                    <code style="background: #f0f0f1; padding: 3px 8px; border-radius: 3px;">[insurance_map trade="<?php echo esc_attr($trade); ?>"]</code>
                                    <button type="button" class="button button-small copy-shortcode"
                                            data-shortcode='[insurance_map trade="<?php echo esc_attr($trade); ?>"]'
                                            style="margin-left: 10px;">
                                        Copy
                                    </button>
                                </td>
                                <td>
                                    <a href="<?php echo esc_url(wp_nonce_url(
                                        admin_url('admin-post.php?action=insurance_maps_export_csv&trade=' . urlencode($trade)),
                                        'export_trade_' . $trade
                                    )); ?>"
                                       class="button button-small"
                                       title="Download current data as CSV">
                                        <span class="dashicons dashicons-download" style="font-size: 14px; vertical-align: middle; margin-top: -2px;"></span>
                                        Download CSV
                                    </a>
                                    <a href="<?php echo esc_url(wp_nonce_url(
                                        admin_url('admin-post.php?action=insurance_maps_delete&trade=' . urlencode($trade)),
                                        'delete_trade_' . $trade
                                    )); ?>"
                                       class="button button-small"
                                       onclick="return confirm('Delete all data for <?php echo esc_js($trade); ?>? This cannot be undone.');">
                                        Delete
                                    </a>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            <?php endif; ?>
        </div>

        <!-- Usage Instructions -->
        <div class="card" style="max-width: 800px; margin-top: 20px;">
            <h2>How to Use</h2>
            <ol style="line-height: 1.8;">
                <li><strong>Prepare Your Data:</strong> Create a CSV file with insurance data for all 50 US states using the format below</li>
                <li><strong>Upload CSV:</strong> Use the form above to upload data for each trade (carpenter, electrician, etc.)</li>
                <li><strong>Copy Shortcode:</strong> Click the "Copy" button next to the trade you want to display</li>
                <li><strong>Add to Page:</strong> Paste the shortcode into any WordPress page or post</li>
                <li><strong>Publish:</strong> Save and publish your page to display the interactive map</li>
                <li><strong>Update Data:</strong> Upload a new CSV with the same trade name to replace existing data</li>
            </ol>

            <h3 style="margin-top: 30px;">CSV Format Template</h3>
            <p>Your CSV file must have exactly these column headers in this order:</p>
            <pre style="background: #f5f5f5; padding: 15px; overflow-x: auto; border: 1px solid #ddd; border-radius: 4px;">State,GL_Premium_Low,GL_Premium_High,GL_Savings,GL_Competitiveness,WC_Rate_5437,WC_Rate_5645
AL,1.2,2.3,32.3,90,6.14,14.07
AK,0.8,1.6,22.6,0,6.16,9.78
AZ,0.9,2.1,50.6,30,4.05,8.51
...
(50 states total)</pre>

            <h4>Column Descriptions:</h4>
            <ul style="line-height: 1.8;">
                <li><strong>State:</strong> Two-letter state code (AL, AK, AZ, etc.)</li>
                <li><strong>GL_Premium_Low:</strong> General Liability premium low end percentage (e.g., 1.2)</li>
                <li><strong>GL_Premium_High:</strong> General Liability premium high end percentage (e.g., 2.3)</li>
                <li><strong>GL_Savings:</strong> General Liability savings percentage (e.g., 32.3)</li>
                <li><strong>GL_Competitiveness:</strong> Carrier competitiveness score 0-100 (e.g., 90)</li>
                <li><strong>WC_Rate_5437:</strong> Workers Comp rate for class 5437 (e.g., 6.14)</li>
                <li><strong>WC_Rate_5645:</strong> Workers Comp rate for class 5645 (e.g., 14.07)</li>
            </ul>

            <h3 style="margin-top: 30px;">Shortcode Options</h3>
            <ul style="line-height: 1.8;">
                <li><code>[insurance_map trade="carpenter"]</code> - Display map with SEO data table</li>
                <li><code>[insurance_map trade="electrician" show_table="no"]</code> - Hide the data table (map only)</li>
            </ul>
        </div>

        <!-- Help Section -->
        <div class="card" style="max-width: 800px; margin-top: 20px; background: #e7f5fe; border-left: 4px solid #2271b1;">
            <h2>Need Help?</h2>
            <p><strong>Common Issues:</strong></p>
            <ul style="line-height: 1.8;">
                <li>If upload fails, check that your CSV has exactly 7 columns with the correct headers</li>
                <li>Trade names must be lowercase with no spaces (use hyphens if needed: general-contractor)</li>
                <li>Make sure you have data for all 50 states for best results</li>
                <li>If the map doesn't display, check that you've activated the plugin</li>
            </ul>
            <p><strong>Plugin Version:</strong> <?php echo esc_html(INSURANCE_MAPS_VERSION); ?></p>
        </div>
    </div>

    <script>
    jQuery(document).ready(function($) {
        $('.copy-shortcode').on('click', function() {
            var shortcode = $(this).data('shortcode');

            // Modern clipboard API
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(shortcode).then(function() {
                    alert('Shortcode copied to clipboard!');
                }).catch(function() {
                    alert('Failed to copy. Please copy manually: ' + shortcode);
                });
            } else {
                // Fallback for older browsers
                var temp = $('<textarea>');
                $('body').append(temp);
                temp.val(shortcode).select();
                try {
                    document.execCommand('copy');
                    alert('Shortcode copied to clipboard!');
                } catch (err) {
                    alert('Failed to copy. Please copy manually: ' + shortcode);
                }
                temp.remove();
            }
        });
    });
    </script>
    <?php
}
