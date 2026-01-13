<?php
/**
 * Insurance Maps Template
 * Renders the interactive map with data from database
 *
 * Variables available:
 * - $trade: Trade name
 * - $map_data: Formatted data for JavaScript (glPremiumRanges, stateData)
 * - $raw_data: Raw database rows for SEO table
 * - $show_table: Boolean to show/hide SEO table
 * - $state_names: Array of state code => state name
 */

// Pass data to JavaScript
?>
<script>
window.insuranceMapData = <?php echo json_encode($map_data); ?>;
</script>

<div id="insurance-map-container">
    <div class="map-header">
        <h2><?php echo esc_html(ucfirst($trade)); ?> Insurance Cost Metrics by State</h2>
        <p class="map-subtitle">Explore insurance costs and savings opportunities across the United States</p>
    </div>

    <div class="metric-toggles">
        <button class="metric-btn active" data-metric="glPremium">GL Premium % of Revenue</button>
        <button class="metric-btn" data-metric="glSavings">GL Savings %</button>
        <button class="metric-btn" data-metric="glCompetitiveness">GL Carrier Competitiveness</button>
        <button class="metric-btn" data-metric="wcRate">WC Rate per $100</button>
    </div>

    <div class="wc-sub-buttons" id="wc-sub-buttons" style="display:none;">
        <button class="wc-sub-btn active" data-wc-code="5437">Class 5437 (Interior)</button>
        <button class="wc-sub-btn" data-wc-code="5645">Class 5645 (Framing)</button>
    </div>

    <div class="legend-container">
        <span class="legend-label">Legend:</span>
        <span class="legend-min">Low</span>
        <div class="legend-gradient"></div>
        <span class="legend-max">High</span>
    </div>

    <!-- Mobile Dropdown (hidden on desktop) -->
    <div class="mobile-selector">
        <label for="state-dropdown">Select a state:</label>
        <select id="state-dropdown">
            <option value="">Choose a state...</option>
            <!-- Options will be populated by JavaScript -->
        </select>
    </div>

    <div class="map-content-container">
        <div class="map-wrapper">
            <div id="map-svg-container">
                <!-- SVG will be copied here by JavaScript -->
            </div>

            <!-- Tooltip for hover functionality -->
            <div id="map-tooltip" style="position: absolute; display: none; background: white; border: 1px solid #ddd; border-radius: 8px; padding: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 1000; pointer-events: none; min-width: 200px;">
                <div class="state-name" style="font-weight: 600; color: #1a1a1a; margin-bottom: 4px;"></div>
                <div class="metric-label" style="font-size: 12px; color: #666; margin-bottom: 2px;"></div>
                <div class="metric-value" style="font-size: 24px; font-weight: 700; color: #2563eb;"></div>
            </div>
        </div>

        <div class="info-card">
            <div class="state-name">Select a State</div>
            <div class="metric-value">--</div>
            <div class="metric-description">Click on a state to view insurance metrics</div>
            <a href="#" class="cta-link" style="display: none;">
                View insurance details →
            </a>
        </div>
    </div>
</div>

<!-- Hidden SVG source -->
<?php include INSURANCE_MAPS_PATH . 'templates/svg-map.html'; ?>

<?php if ($show_table && !empty($raw_data)): ?>
<!-- SEO Data Table -->
<div class="insurance-data-table-section">
    <h3><?php echo esc_html(ucfirst($trade)); ?> Insurance Cost Data by State</h3>
    <table class="insurance-data-table">
        <thead>
            <tr>
                <th>State</th>
                <th>GL Premium Range</th>
                <th>GL Savings %</th>
                <th>GL Competitiveness</th>
                <th>WC Rate (Class 5437)</th>
                <th>WC Rate (Class 5645)</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($raw_data as $row): ?>
            <tr>
                <td><?php echo esc_html($state_names[$row['state_code']]); ?></td>
                <td><?php echo esc_html($row['gl_premium_low'] . '% - ' . $row['gl_premium_high'] . '%'); ?></td>
                <td><?php echo esc_html($row['gl_savings']); ?>%</td>
                <td><?php echo esc_html($row['gl_competitiveness']); ?></td>
                <td>$<?php echo esc_html($row['wc_rate_5437']); ?></td>
                <td>$<?php echo esc_html($row['wc_rate_5645']); ?></td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
</div>

<!-- Schema.org Structured Data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "<?php echo esc_js(ucfirst($trade)); ?> Insurance Cost Metrics by US State",
  "description": "Comprehensive insurance cost data for <?php echo esc_js($trade); ?> professionals across all 50 US states, including General Liability premiums, savings potential, carrier competitiveness, and Workers Compensation rates.",
  "creator": {
    "@type": "Organization",
    "name": "Contractor Nerd"
  },
  "temporalCoverage": "<?php echo date('Y'); ?>",
  "spatialCoverage": {
    "@type": "Place",
    "geo": {
      "@type": "GeoCoordinates",
      "name": "United States"
    }
  }
}
</script>
<?php endif; ?>
