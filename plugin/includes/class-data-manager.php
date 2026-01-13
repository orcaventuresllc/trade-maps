<?php
/**
 * Insurance Maps Data Manager
 * Handles all database operations for insurance cost data
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class Insurance_Maps_Data_Manager {
    private $table_name;

    public function __construct() {
        global $wpdb;
        $this->table_name = $wpdb->prefix . 'insurance_map_data';
    }

    /**
     * Validate CSV row data
     *
     * @param array $row CSV row data
     * @return bool|WP_Error True if valid, WP_Error otherwise
     */
    private function validate_csv_row($row, $line_number) {
        // Check we have 7 columns
        if (count($row) !== 7) {
            return new WP_Error('invalid_columns', sprintf('Line %d: Expected 7 columns, found %d', $line_number, count($row)));
        }

        // Validate state code (2 uppercase letters)
        $state_code = strtoupper(trim($row[0]));
        if (!preg_match('/^[A-Z]{2}$/', $state_code)) {
            return new WP_Error('invalid_state', sprintf('Line %d: Invalid state code "%s"', $line_number, $row[0]));
        }

        // Validate numeric values are actually numeric
        for ($i = 1; $i <= 6; $i++) {
            if (!is_numeric($row[$i])) {
                return new WP_Error('invalid_number', sprintf('Line %d: Column %d must be numeric', $line_number, $i + 1));
            }
        }

        // Validate GL Premium ranges (0-100%)
        $gl_low = floatval($row[1]);
        $gl_high = floatval($row[2]);
        if ($gl_low < 0 || $gl_low > 100 || $gl_high < 0 || $gl_high > 100) {
            return new WP_Error('invalid_range', sprintf('Line %d: GL Premium values must be between 0 and 100', $line_number));
        }

        if ($gl_low > $gl_high) {
            return new WP_Error('invalid_range', sprintf('Line %d: GL Premium Low cannot be greater than High', $line_number));
        }

        // Validate GL Savings (0-100%)
        $gl_savings = floatval($row[3]);
        if ($gl_savings < 0 || $gl_savings > 100) {
            return new WP_Error('invalid_range', sprintf('Line %d: GL Savings must be between 0 and 100', $line_number));
        }

        // Validate GL Competitiveness (0-100)
        $gl_comp = intval($row[4]);
        if ($gl_comp < 0 || $gl_comp > 100) {
            return new WP_Error('invalid_range', sprintf('Line %d: GL Competitiveness must be between 0 and 100', $line_number));
        }

        // Validate WC Rates (0-1000) - reasonable upper limit
        $wc_5437 = floatval($row[5]);
        $wc_5645 = floatval($row[6]);
        if ($wc_5437 < 0 || $wc_5437 > 1000 || $wc_5645 < 0 || $wc_5645 > 1000) {
            return new WP_Error('invalid_range', sprintf('Line %d: WC Rates must be between 0 and 1000', $line_number));
        }

        return true;
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
        $line_number = 2; // Start at 2 (header is line 1)

        // Begin transaction for performance
        $wpdb->query('START TRANSACTION');

        try {
            while (($row = fgetcsv($file)) !== false) {
                // Skip empty rows
                if (empty($row[0])) {
                    $line_number++;
                    continue;
                }

                // Validate row data
                $validation = $this->validate_csv_row($row, $line_number);
                if (is_wp_error($validation)) {
                    $wpdb->query('ROLLBACK');
                    fclose($file);
                    return $validation;
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
                $line_number++;
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

    /**
     * Export trade data to CSV format
     * Generates downloadable CSV file from database
     *
     * @param string $trade Trade name
     * @return string|WP_Error CSV content or error
     */
    public function export_trade_to_csv($trade) {
        $data = $this->get_trade_data($trade);

        if (empty($data)) {
            return new WP_Error('no_data', 'No data available for this trade');
        }

        // Create CSV in memory (php://temp is more efficient than php://output for this)
        $output = fopen('php://temp', 'r+');

        // Write header row (must match import format exactly)
        fputcsv($output, array('State', 'GL_Premium_Low', 'GL_Premium_High', 'GL_Savings', 'GL_Competitiveness', 'WC_Rate_5437', 'WC_Rate_5645'));

        // Write data rows
        foreach ($data as $row) {
            fputcsv($output, array(
                $row['state_code'],
                $row['gl_premium_low'],
                $row['gl_premium_high'],
                $row['gl_savings'],
                $row['gl_competitiveness'],
                $row['wc_rate_5437'],
                $row['wc_rate_5645']
            ));
        }

        // Get CSV content
        rewind($output);
        $csv = stream_get_contents($output);
        fclose($output);

        return $csv;
    }
}
