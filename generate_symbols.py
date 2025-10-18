#!/usr/bin/env python3
"""
KiCad Symbol Generator for SCC68070 and SCC66470
Generates .kicad_sym files from pin table text files
"""

import re
from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path


@dataclass
class Pin:
    """Represents a single pin on a component"""
    number: str
    name: str
    type: str  # I, O, I/O, PWR, NC
    polarity: str  # H, L, -
    drive: str  # PP, OD, 3S, -
    description: str
    
    def to_kicad_type(self) -> str:
        """Convert our pin type to KiCad electrical type"""
        type_map = {
            'I': 'input',
            'O': 'output',
            'I/O': 'bidirectional',
            'PWR': 'power_in',
            'NC': 'no_connect'
        }
        
        # Special cases for open-drain
        if self.drive == 'OD':
            if self.type == 'O':
                return 'open_collector'
            elif self.type == 'I/O':
                return 'open_emitter'  # or 'bidirectional' with note
        
        # Special cases for 3-state
        if self.drive == '3S' and self.type == 'O':
            return 'tri_state'
        
        return type_map.get(self.type, 'passive')
    
    def get_display_name(self) -> str:
        """Get pin name with active-LOW overline if needed"""
        if self.polarity == 'L' and self.type != 'PWR' and self.type != 'NC':
            # Add overline for active-LOW signals
            return f"~{{{self.name}}}"
        return self.name


def parse_pin_table(filepath: Path) -> List[Pin]:
    """Parse a pin table text file and return list of Pin objects"""
    pins = []
    
    with open(filepath, 'r') as f:
        for line in f:
            # Skip comments and headers
            if line.startswith('#') or line.startswith('PIN') or '---' in line:
                continue
            
            # Parse pin table line
            match = re.match(r'\s*(\d+)\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(.+)', line)
            if match:
                pin_num, signal, pin_type, polarity, drive, description = match.groups()
                
                pins.append(Pin(
                    number=pin_num.strip(),
                    name=signal.strip(),
                    type=pin_type.strip(),
                    polarity=polarity.strip(),
                    drive=drive.strip(),
                    description=description.strip()
                ))
    
    return pins


def generate_kicad_symbol(component_name: str, pins: List[Pin], footprint_filter: str = "*") -> str:
    """Generate KiCad 6.x symbol file content"""
    
    # Calculate symbol dimensions based on number of pins
    # Place pins on all 4 sides for large pin counts
    left_pins = []
    right_pins = []
    top_pins = []
    bottom_pins = []
    
    # Group pins by function for logical placement
    for pin in pins:
        if pin.type == 'NC' or pin.name == 'RESERVED':
            # NC pins go to bottom
            bottom_pins.append(pin)
        elif pin.type == 'PWR':
            # Power pins go to top/bottom
            if 'VDD' in pin.name or 'VCC' in pin.name:
                top_pins.append(pin)
            else:  # VSS, GND
                bottom_pins.append(pin)
        elif pin.name.startswith('A'):  # Address bus
            left_pins.append(pin)
        elif pin.name.startswith('D'):  # Data bus
            right_pins.append(pin)
        else:  # Control signals
            # Distribute between left and right
            if len(left_pins) <= len(right_pins):
                left_pins.append(pin)
            else:
                right_pins.append(pin)
    
    # Calculate symbol box size
    pin_spacing = 100  # 100 mils = 2.54mm
    max_height = max(len(left_pins), len(right_pins)) * pin_spacing
    max_width = max(len(top_pins), len(bottom_pins)) * pin_spacing
    
    # Minimum symbol size
    width = max(2000, max_width)
    height = max(2000, max_height)
    
    # Start building symbol
    symbol = f'''(kicad_symbol_lib (version 20211014) (generator kicad_symbol_generator)
  (symbol "{component_name}" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
    (property "Reference" "U" (id 0) (at 0 {height//2 + 200} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "{component_name}" (id 1) (at 0 {height//2 + 400} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (id 2) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (id 3) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_keywords" "Philips CD-i microprocessor" (id 4) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_description" "{component_name} - Philips CD-i Component" (id 5) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "ki_fp_filters" "{footprint_filter}" (id 6) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "{component_name}_0_1"
      (rectangle (start -{width//2} {height//2}) (end {width//2} -{height//2})
        (stroke (width 0.254) (type default) (color 0 0 0 0))
        (fill (type background))
      )
    )
'''
    
    # Add pins
    symbol += f'    (symbol "{component_name}_1_1"\n'
    
    # Left side pins (address bus, some control)
    y_pos = height//2 - 200
    for i, pin in enumerate(left_pins):
        if i < len(left_pins):  # Ensure we don't overflow
            y = y_pos - (i * pin_spacing)
            symbol += f'      (pin {pin.to_kicad_type()} line (at -{width//2 - 200} {y} 0) (length 200)\n'
            symbol += f'        (name "{pin.get_display_name()}" (effects (font (size 1.016 1.016))))\n'
            symbol += f'        (number "{pin.number}" (effects (font (size 1.016 1.016))))\n'
            symbol += f'      )\n'
    
    # Right side pins (data bus, some control)
    y_pos = height//2 - 200
    for i, pin in enumerate(right_pins):
        if i < len(right_pins):
            y = y_pos - (i * pin_spacing)
            symbol += f'      (pin {pin.to_kicad_type()} line (at {width//2 + 200} {y} 180) (length 200)\n'
            symbol += f'        (name "{pin.get_display_name()}" (effects (font (size 1.016 1.016))))\n'
            symbol += f'        (number "{pin.number}" (effects (font (size 1.016 1.016))))\n'
            symbol += f'      )\n'
    
    # Top pins (power)
    x_pos = -(len(top_pins) * pin_spacing) // 2
    for i, pin in enumerate(top_pins):
        x = x_pos + (i * pin_spacing)
        symbol += f'      (pin {pin.to_kicad_type()} line (at {x} {height//2 + 200} 270) (length 200)\n'
        symbol += f'        (name "{pin.get_display_name()}" (effects (font (size 1.016 1.016))))\n'
        symbol += f'        (number "{pin.number}" (effects (font (size 1.016 1.016))))\n'
        symbol += f'      )\n'
    
    # Bottom pins (ground, NC)
    x_pos = -(len(bottom_pins) * pin_spacing) // 2
    for i, pin in enumerate(bottom_pins[:20]):  # Limit bottom pins to avoid overcrowding
        x = x_pos + (i * pin_spacing)
        symbol += f'      (pin {pin.to_kicad_type()} line (at {x} -{height//2 + 200} 90) (length 200)\n'
        symbol += f'        (name "{pin.get_display_name()}" (effects (font (size 1.016 1.016))))\n'
        symbol += f'        (number "{pin.number}" (effects (font (size 1.016 1.016))))\n'
        symbol += f'      )\n'
    
    symbol += '    )\n'
    symbol += '  )\n'
    symbol += ')\n'
    
    return symbol


def main():
    """Generate all KiCad symbols"""
    base_path = Path('/home/tom/project/kicad_scc68070')
    pin_path = base_path / 'pin_extraction'
    symbols_path = base_path / 'symbols'
    
    # Ensure symbols directory exists
    symbols_path.mkdir(exist_ok=True)
    
    # Generate symbols
    components = [
        {
            'name': 'SCC68070_PLCC84',
            'pin_file': pin_path / 'SCC68070_PLCC84_complete.txt',
            'footprint_filter': 'PLCC*84*'
        },
        {
            'name': 'SCC68070_QFP120',
            'pin_file': pin_path / 'SCC68070_QFP120_complete.txt',
            'footprint_filter': '*QFP*120* SOT220*'
        },
        {
            'name': 'SCC66470_QFP120',
            'pin_file': pin_path / 'SCC66470_QFP120_complete.txt',
            'footprint_filter': '*QFP*120* SOT220*'
        }
    ]
    
    for comp in components:
        print(f"Generating symbol for {comp['name']}...")
        
        if not comp['pin_file'].exists():
            print(f"  WARNING: Pin file not found: {comp['pin_file']}")
            continue
        
        # Parse pins
        pins = parse_pin_table(comp['pin_file'])
        print(f"  Parsed {len(pins)} pins")
        
        # Generate symbol
        symbol_content = generate_kicad_symbol(
            comp['name'],
            pins,
            comp['footprint_filter']
        )
        
        # Write symbol file
        output_file = symbols_path / f"{comp['name']}.kicad_sym"
        with open(output_file, 'w') as f:
            f.write(symbol_content)
        
        print(f"  Created: {output_file}")
    
    print("\nDone! Symbol files created in symbols/ directory")


if __name__ == '__main__':
    main()
