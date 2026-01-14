#!/usr/bin/env python3
"""
Extract insurance data from HTML files and generate CSV files
Creates sample CSV files for each trade with flexible WC class codes
Version 1.1 - Updated for flexible WC class format
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

def extract_wc_config(html_content):
    """Extract WC class codes and labels from HTML"""
    wc_config = {
        'class1': None,
        'label1': None,
        'class2': None,
        'label2': None
    }

    # Look for WC button definitions
    # Pattern: <button ... data-wc-code="5437">Class 5437 (Interior)</button>
    button_pattern = r'<button[^>]*data-wc-code="(\d+)"[^>]*>Class\s+(\d+)(?:\s*\(([^)]+)\))?</button>'
    matches = re.findall(button_pattern, html_content)

    if matches:
        if len(matches) >= 1:
            wc_config['class1'] = matches[0][1]
            wc_config['label1'] = matches[0][2] if matches[0][2] else ''

        if len(matches) >= 2:
            wc_config['class2'] = matches[1][1]
            wc_config['label2'] = matches[1][2] if matches[1][2] else ''

    # Fallback: Look for single WC Rate button label
    # Pattern 1: <button ... data-metric="wcRate">WC Rate - 5190</button>
    # Pattern 2: <button ... data-metric="wcRate">WC Rate - 9102 (Lawncare)</button>
    single_pattern = r'data-metric="wcRate">WC Rate - (\d+)(?:\s*\(([^)]+)\))?</button>'
    single_match = re.search(single_pattern, html_content)

    if single_match and not wc_config['class1']:
        wc_config['class1'] = single_match.group(1)
        wc_config['label1'] = single_match.group(2) if single_match.group(2) else ''

    return wc_config

def extract_wc_data(html_content, wc_config):
    """Extract WC rate data for specific class codes"""
    wc_data = {'rate1': {}, 'rate2': {}}

    # Extract state data section
    state_data_match = re.search(r'var stateData = \{(.+?)\s*\};', html_content, re.DOTALL)
    if not state_data_match:
        return wc_data

    state_data_text = state_data_match.group(1)

    # For trades with two WC classes (like carpenter)
    if wc_config['class1'] and wc_config['class2']:
        # Look for wcRate5437, wcRate5645 pattern
        wc1_pattern = f"wcRate{wc_config['class1']}:\\s*\\{{([^}}]+)\\}}"
        wc2_pattern = f"wcRate{wc_config['class2']}:\\s*\\{{([^}}]+)\\}}"

        wc1_match = re.search(wc1_pattern, state_data_text)
        if wc1_match:
            for match in re.finditer(r'(\w+):\s*([\d.]+)', wc1_match.group(1)):
                wc_data['rate1'][match.group(1)] = float(match.group(2))

        wc2_match = re.search(wc2_pattern, state_data_text)
        if wc2_match:
            for match in re.finditer(r'(\w+):\s*([\d.]+)', wc2_match.group(1)):
                wc_data['rate2'][match.group(1)] = float(match.group(2))

    # For trades with single WC class
    elif wc_config['class1']:
        # Look for generic wcRate: { ... } pattern
        wc_pattern = r"wcRate:\s*\{([^}]+)\}"
        wc_match = re.search(wc_pattern, state_data_text)

        if wc_match:
            for match in re.finditer(r'(\w+):\s*([\d.]+)', wc_match.group(1)):
                wc_data['rate1'][match.group(1)] = float(match.group(2))

    return wc_data

def extract_data_from_html(html_file):
    """Extract insurance data from HTML file"""
    with open(html_file, 'r') as f:
        content = f.read()

    # Extract WC configuration
    wc_config = extract_wc_config(content)
    print(f"  WC Config: Class 1={wc_config['class1']} ({wc_config['label1']}), Class 2={wc_config['class2']} ({wc_config['label2']})")

    # Extract WC data
    wc_data = extract_wc_data(content, wc_config)

    # Extract glPremiumRanges
    gl_ranges_match = re.search(r'var glPremiumRanges = \{([^}]+)\}', content)
    if not gl_ranges_match:
        print(f"  Error: Could not find glPremiumRanges")
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
        print(f"  Error: Could not find stateData")
        return None

    state_data_text = state_data_match.group(1)

    # Extract each metric
    data = {}

    # GL Premium (average values - not used in CSV, we use ranges)
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

    # Combine all data
    for state in gl_ranges:
        if state not in data:
            data[state] = {}
        data[state]['glPremiumLow'] = gl_ranges[state][0]
        data[state]['glPremiumHigh'] = gl_ranges[state][1]
        data[state]['wcClass1'] = wc_config['class1'] or ''
        data[state]['wcRate1'] = wc_data['rate1'].get(state, 0)
        data[state]['wcLabel1'] = wc_config['label1'] or ''
        data[state]['wcClass2'] = wc_config['class2'] or ''
        data[state]['wcRate2'] = wc_data['rate2'].get(state, 0)
        data[state]['wcLabel2'] = wc_config['label2'] or ''

    return data

def write_csv(data, output_file, wc_config):
    """Write data to CSV file with new 11-column format"""
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)

        # Write header (new 11-column format)
        writer.writerow(['State', 'GL_Premium_Low', 'GL_Premium_High', 'GL_Savings',
                        'GL_Competitiveness', 'WC_Class_1', 'WC_Rate_1', 'WC_Label_1',
                        'WC_Class_2', 'WC_Rate_2', 'WC_Label_2'])

        # Write data for all 50 states
        for state in STATE_CODES:
            if state in data:
                row = [
                    state,
                    data[state].get('glPremiumLow', 0),
                    data[state].get('glPremiumHigh', 0),
                    data[state].get('glSavings', 0),
                    data[state].get('glCompetitiveness', 0),
                    data[state].get('wcClass1', ''),
                    data[state].get('wcRate1', 0),
                    data[state].get('wcLabel1', ''),
                    data[state].get('wcClass2', ''),
                    data[state].get('wcRate2', 0),
                    data[state].get('wcLabel2', '')
                ]
                writer.writerow(row)
            else:
                print(f"  Warning: No data found for state {state}")

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

    print("Extracting insurance data from HTML files (v1.1 format with flexible WC classes)...\n")

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
            # Get WC config for display
            with open(html_path, 'r') as f:
                content = f.read()
            wc_config = extract_wc_config(content)

            # Write CSV
            csv_file = output_dir / f"{trade_name}.csv"
            write_csv(data, csv_file, wc_config)
        else:
            print(f"✗ Failed to extract data from {html_file}")

        print()

    print(f"\n✅ Done! CSV files created in {output_dir}/ with flexible WC class format")
    print(f"\nNew CSV format (11 columns):")
    print("  - Columns 1-5: State, GL data (same as before)")
    print("  - Columns 6-8: WC_Class_1, WC_Rate_1, WC_Label_1")
    print("  - Columns 9-11: WC_Class_2, WC_Rate_2, WC_Label_2")
    print(f"\nYou can now upload these CSV files via WordPress admin:")
    print("  Dashboard → Insurance Maps → Upload CSV")

if __name__ == '__main__':
    main()
