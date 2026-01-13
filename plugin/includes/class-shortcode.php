<?php
/**
 * Insurance Maps Shortcode Handler
 * Registers and processes the [insurance_map] shortcode
 */

class Insurance_Maps_Shortcode {
    private $data_manager;

    public function __construct() {
        $this->data_manager = new Insurance_Maps_Data_Manager();
        add_shortcode('insurance_map', array($this, 'render_shortcode'));
    }

    /**
     * Render the insurance map shortcode
     * Usage: [insurance_map trade="carpenter"]
     * Usage: [insurance_map trade="electrician" show_table="no"]
     *
     * @param array $atts Shortcode attributes
     * @return string HTML output
     */
    public function render_shortcode($atts) {
        $atts = shortcode_atts(array(
            'trade' => 'carpenter',
            'show_table' => 'yes'
        ), $atts);

        $trade = sanitize_text_field($atts['trade']);
        $show_table = ($atts['show_table'] === 'yes');

        // Check if trade has data
        if (!$this->data_manager->trade_has_data($trade)) {
            return '<div class="insurance-maps-error" style="padding: 20px; background: #fee; border: 1px solid #c33; border-radius: 8px; margin: 20px 0;">' .
                   '<p><strong>No data available for trade: ' . esc_html($trade) . '</strong></p>' .
                   '<p>Please upload CSV data for this trade in the <a href="' . admin_url('admin.php?page=insurance-maps') . '">Insurance Maps admin panel</a>.</p>' .
                   '</div>';
        }

        // Get data from database
        $map_data = $this->data_manager->get_trade_data_for_js($trade);
        $raw_data = $this->data_manager->get_trade_data($trade);

        // Get state names
        $state_names = $this->get_state_names();

        // Start output buffering
        ob_start();

        // Include the template
        include INSURANCE_MAPS_PATH . 'templates/map-template.php';

        return ob_get_clean();
    }

    /**
     * Get full state names mapped to state codes
     *
     * @return array State code => State name mapping
     */
    private function get_state_names() {
        return array(
            'AL' => 'Alabama', 'AK' => 'Alaska', 'AZ' => 'Arizona', 'AR' => 'Arkansas', 'CA' => 'California',
            'CO' => 'Colorado', 'CT' => 'Connecticut', 'DE' => 'Delaware', 'FL' => 'Florida', 'GA' => 'Georgia',
            'HI' => 'Hawaii', 'ID' => 'Idaho', 'IL' => 'Illinois', 'IN' => 'Indiana', 'IA' => 'Iowa',
            'KS' => 'Kansas', 'KY' => 'Kentucky', 'LA' => 'Louisiana', 'ME' => 'Maine', 'MD' => 'Maryland',
            'MA' => 'Massachusetts', 'MI' => 'Michigan', 'MN' => 'Minnesota', 'MS' => 'Mississippi',
            'MO' => 'Missouri', 'MT' => 'Montana', 'NE' => 'Nebraska', 'NV' => 'Nevada',
            'NH' => 'New Hampshire', 'NJ' => 'New Jersey', 'NM' => 'New Mexico', 'NY' => 'New York',
            'NC' => 'North Carolina', 'ND' => 'North Dakota', 'OH' => 'Ohio', 'OK' => 'Oklahoma',
            'OR' => 'Oregon', 'PA' => 'Pennsylvania', 'RI' => 'Rhode Island', 'SC' => 'South Carolina',
            'SD' => 'South Dakota', 'TN' => 'Tennessee', 'TX' => 'Texas', 'UT' => 'Utah', 'VT' => 'Vermont',
            'VA' => 'Virginia', 'WA' => 'Washington', 'WV' => 'West Virginia', 'WI' => 'Wisconsin', 'WY' => 'Wyoming'
        );
    }
}
