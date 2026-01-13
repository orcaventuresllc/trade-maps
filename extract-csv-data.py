#!/usr/bin/env python3
"""
Extract insurance data from HTML files and generate CSV files
Creates sample CSV files for each trade to use with WordPress plugin
"""

import re
import csv
from pathlib import Path

# State codes for all 50 states
STATE_CODES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

def extract_data_from_html(html_file):
    """Extract insurance data from HTML file"""
    with open(html_file, 'r') as f:
        content = f.read()

    # Extract glPremiumRanges
    gl_ranges_match = re.search(r'var glPremiumRanges = \{([^}]+)\}', content)
    if not gl_ranges_match:
        print(f"Error: Could not find glPremiumRanges in {html_file}")
        return None

    gl_ranges_text = gl_ranges_match.group(1)
    gl_ranges = {}
    for match in re.finditer(r'(\w+):\s*"([\d.]+)%\s*-\s*([\d.]+)%"', gl_ranges_text):
        state = match.group(1)
        low = float(match.group(2))
        high = float(match.group(3))
        gl_ranges[state] = (low, high)

    # Extract stateData
    state_data_match = re.search(r'var stateData = \{(.+?)\s*\};', content, re.DOTALL)
    if not state_data_match:
        print(f"Error: Could not find stateData in {html_file}")
        return None

    state_data_text = state_data_match.group(1)

    # Extract each metric
    data = {}

    # GL Premium (average values)
    gl_premium_match = re.search(r'glPremium:\s*\{([^}]+)\}', state_data_text)
    if gl_premium_match:
        for match in re.finditer(r'(\w+):\s*([\d.]+)', gl_premium_match.group(1)):
            state = match.group(1)
            if state not in data:
                data[state] = {}
            data[state]['glPremium'] = float(match.group(2))

    # GL Savings
    gl_savings_match = re.search(r'glSavings:\s*\{([^}]+)\}', state_data_text)
    if gl_savings_match:
        for match in re.finditer(r'(\w+):\s*([\d.]+)', gl_savings_match.group(1)):
            state = match.group(1)
            if state not in data:
                data[state] = {}
            data[state]['glSavings'] = float(match.group(2))

    # GL Competitiveness
    gl_comp_match = re.search(r'glCompetitiveness:\s*\{([^}]+)\}', state_data_text)
    if gl_comp_match:
        for match in re.finditer(r'(\w+):\s*(\d+)', gl_comp_match.group(1)):
            state = match.group(1)
            if state not in data:
                data[state] = {}
            data[state]['glCompetitiveness'] = int(match.group(2))

    # WC Rate 5437
    wc_5437_match = re.search(r'wcRate5437:\s*\{([^}]+)\}', state_data_text)
    if wc_5437_match:
        for match in re.finditer(r'(\w+):\s*([\d.]+)', wc_5437_match.group(1)):
            state = match.group(1)
            if state not in data:
                data[state] = {}
            data[state]['wcRate5437'] = float(match.group(2))

    # WC Rate 5645
    wc_5645_match = re.search(r'wcRate5645:\s*\{([^}]+)\}', state_data_text)
    if wc_5645_match:
        for match in re.finditer(r'(\w+):\s*([\d.]+)', wc_5645_match.group(1)):
            state = match.group(1)
            if state not in data:
                data[state] = {}
            data[state]['wcRate5645'] = float(match.group(2))

    # Combine ranges with data
    for state in gl_ranges:
        if state in data:
            data[state]['glPremiumLow'] = gl_ranges[state][0]
            data[state]['glPremiumHigh'] = gl_ranges[state][1]

    return data

def write_csv(data, output_file):
    """Write data to CSV file"""
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)

        # Write header
        writer.writerow(['State', 'GL_Premium_Low', 'GL_Premium_High', 'GL_Savings',
                        'GL_Competitiveness', 'WC_Rate_5437', 'WC_Rate_5645'])

        # Write data for all 50 states
        for state in STATE_CODES:
            if state in data:
                row = [
                    state,
                    data[state].get('glPremiumLow', 0),
                    data[state].get('glPremiumHigh', 0),
                    data[state].get('glSavings', 0),
                    data[state].get('glCompetitiveness', 0),
                    data[state].get('wcRate5437', 0),
                    data[state].get('wcRate5645', 0)
                ]
                writer.writerow(row)
            else:
                print(f"Warning: No data found for state {state}")

    print(f"✓ Created: {output_file}")

def main():
    """Main extraction process"""
    # Map of HTML files to trade names
    trades = {
        'final-carpenter.html': 'carpenter',
        'final-electrician.html': 'electrician',
        'final-plumber.html': 'plumber',
        'final-hvac.html': 'hvac',
        'final-gc.html': 'gc',
        'final-landscaping.html': 'landscaping',
        'final-painter.html': 'painter'
    }

    # Create output directory
    output_dir = Path('sample-data')
    output_dir.mkdir(exist_ok=True)

    print("Extracting insurance data from HTML files...\n")

    # Process each trade
    for html_file, trade_name in trades.items():
        html_path = Path(html_file)

        if not html_path.exists():
            print(f"⚠ Skipping {html_file} (file not found)")
            continue

        print(f"Processing {trade_name}...")

        # Extract data
        data = extract_data_from_html(html_path)

        if data:
            # Write CSV
            csv_file = output_dir / f"{trade_name}.csv"
            write_csv(data, csv_file)
        else:
            print(f"✗ Failed to extract data from {html_file}")

        print()

    print(f"\n✅ Done! CSV files created in {output_dir}/")
    print(f"\nYou can now upload these CSV files via WordPress admin:")
    print("  Dashboard → Insurance Maps → Upload CSV")

if __name__ == '__main__':
    main()
