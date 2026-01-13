<?php
/**
 * Insurance Maps Data Manager
 * Handles all database operations for insurance cost data
 */

class Insurance_Maps_Data_Manager {
    private $table_name;

    public function __construct() {
        global $wpdb;
        $this->table_name = $wpdb->prefix . 'insurance_map_data';
    }

    /**
     * Import data from CSV file
     *
     * @param string $file_path Path to CSV file
     * @param string $trade Trade name (carpenter, electrician, etc.)
     * @return int|WP_Error Number of records imported or error
     */
    public function import_csv($file_path, $trade) {
        global $wpdb;

        if (!file_exists($file_path)) {
            return new WP_Error('file_not_found', 'CSV file not found');
        }

        $file = fopen($file_path, 'r');
        if ($file === false) {
            return new WP_Error('file_open_error', 'Could not open CSV file');
        }

        // Read and validate header row
        $header = fgetcsv($file);
        $expected_headers = array('State', 'GL_Premium_Low', 'GL_Premium_High', 'GL_Savings', 'GL_Competitiveness', 'WC_Rate_5437', 'WC_Rate_5645');

        if ($header !== $expected_headers) {
            fclose($file);
            return new WP_Error('invalid_format', 'Invalid CSV format. Expected headers: ' . implode(', ', $expected_headers));
        }

        $imported = 0;

        // Begin transaction for performance
        $wpdb->query('START TRANSACTION');

        try {
            while (($row = fgetcsv($file)) !== false) {
                // Skip empty rows
                if (empty($row[0])) {
                    continue;
                }

                $data = array(
                    'trade' => sanitize_text_field($trade),
                    'state_code' => sanitize_text_field(strtoupper($row[0])),
                    'gl_premium_low' => floatval($row[1]),
                    'gl_premium_high' => floatval($row[2]),
                    'gl_savings' => floatval($row[3]),
                    'gl_competitiveness' => intval($row[4]),
                    'wc_rate_5437' => floatval($row[5]),
                    'wc_rate_5645' => floatval($row[6])
                );

                // Insert or update (upsert)
                $wpdb->replace($this->table_name, $data);
                $imported++;
            }

            $wpdb->query('COMMIT');
        } catch (Exception $e) {
            $wpdb->query('ROLLBACK');
            fclose($file);
            return new WP_Error('import_error', 'Error importing data: ' . $e->getMessage());
        }

        fclose($file);

        return $imported;
    }

    /**
     * Get all data for a specific trade
     *
     * @param string $trade Trade name
     * @return array Array of database rows
     */
    public function get_trade_data($trade) {
        global $wpdb;

        return $wpdb->get_results(
            $wpdb->prepare(
                "SELECT * FROM {$this->table_name} WHERE trade = %s ORDER BY state_code ASC",
                $trade
            ),
            ARRAY_A
        );
    }

    /**
     * Get data formatted for JavaScript
     * Converts database format to the format expected by map-interactive.js
     *
     * @param string $trade Trade name
     * @return array Formatted data array with glPremiumRanges and stateData
     */
    public function get_trade_data_for_js($trade) {
        $data = $this->get_trade_data($trade);

        $formatted = array(
            'glPremiumRanges' => array(),
            'stateData' => array(
                'glPremium' => array(),
                'glSavings' => array(),
                'glCompetitiveness' => array(),
                'wcRate5437' => array(),
                'wcRate5645' => array()
            )
        );

        foreach ($data as $row) {
            $state = $row['state_code'];

            // Format range display (e.g., "1.2% - 2.3%")
            $formatted['glPremiumRanges'][$state] =
                $row['gl_premium_low'] . '% - ' . $row['gl_premium_high'] . '%';

            // Calculate average for heat map
            $formatted['stateData']['glPremium'][$state] =
                ($row['gl_premium_low'] + $row['gl_premium_high']) / 2;

            $formatted['stateData']['glSavings'][$state] = floatval($row['gl_savings']);
            $formatted['stateData']['glCompetitiveness'][$state] = intval($row['gl_competitiveness']);
            $formatted['stateData']['wcRate5437'][$state] = floatval($row['wc_rate_5437']);
            $formatted['stateData']['wcRate5645'][$state] = floatval($row['wc_rate_5645']);
        }

        return $formatted;
    }

    /**
     * Get list of available trades
     *
     * @return array Array of trade names
     */
    public function get_available_trades() {
        global $wpdb;

        return $wpdb->get_col(
            "SELECT DISTINCT trade FROM {$this->table_name} ORDER BY trade ASC"
        );
    }

    /**
     * Get count of states for a trade
     *
     * @param string $trade Trade name
     * @return int Number of states with data
     */
    public function get_trade_state_count($trade) {
        global $wpdb;

        return (int) $wpdb->get_var(
            $wpdb->prepare(
                "SELECT COUNT(*) FROM {$this->table_name} WHERE trade = %s",
                $trade
            )
        );
    }

    /**
     * Delete all data for a trade
     *
     * @param string $trade Trade name
     * @return int|false Number of rows deleted or false on error
     */
    public function delete_trade_data($trade) {
        global $wpdb;

        return $wpdb->delete(
            $this->table_name,
            array('trade' => $trade),
            array('%s')
        );
    }

    /**
     * Check if trade has data
     *
     * @param string $trade Trade name
     * @return bool True if trade has data
     */
    public function trade_has_data($trade) {
        return $this->get_trade_state_count($trade) > 0;
    }
}
