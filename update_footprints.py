#!/usr/bin/env python3
"""Update KiCad symbol files with correct footprint references"""

import re

def update_symbol_footprint(filepath, footprint_value, fp_filter):
    """Update Footprint property and ki_fp_filters in symbol file"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Update Footprint property (currently empty)
    content = re.sub(
        r'(\(property "Footprint" )"" \(id 2\)',
        f'\\1"{footprint_value}" (id 2)',
        content
    )
    
    # Update ki_fp_filters
    content = re.sub(
        r'(\(property "ki_fp_filters" )"[^"]*" \(id 6\)',
        f'\\1"{fp_filter}" (id 6)',
        content
    )
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"Updated: {filepath}")

# Update all symbol files
update_symbol_footprint(
    'symbols/SCC68070_PLCC84.kicad_sym',
    'Package_LCC:PLCC-84',
    'PLCC*84*'
)

update_symbol_footprint(
    'symbols/SCC68070_QFP120.kicad_sym', 
    'Package_QFP:LQFP-120_14x14mm_P0.5mm',
    '*QFP*120*P0.5mm* SOT220*'
)

update_symbol_footprint(
    'symbols/SCC66470_QFP120.kicad_sym',
    'Package_QFP:LQFP-120_14x14mm_P0.5mm', 
    '*QFP*120*P0.5mm* SOT220*'
)

print("\nAll footprint references updated!")
