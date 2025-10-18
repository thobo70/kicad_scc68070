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
    group: str  # ADDRESS, DATA, POWER, GROUND, BUS_CTRL, DMA, INTERRUPT, etc.
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
            
            # Parse pin table line - now with GROUP column
            match = re.match(r'\s*(\d+)\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(\S+)\s*\|\s*(.+)', line)
            if match:
                pin_num, signal, pin_type, polarity, drive, group, description = match.groups()
                
                pins.append(Pin(
                    number=pin_num.strip(),
                    name=signal.strip(),
                    type=pin_type.strip(),
                    polarity=polarity.strip(),
                    drive=drive.strip(),
                    group=group.strip(),
                    description=description.strip()
                ))
    
    return pins


def generate_kicad_symbol(component_name: str, pins: List[Pin], footprint_filter: str = "*") -> str:
    """Generate KiCad 6.x symbol file content"""
    
def generate_kicad_symbol(component_name: str, pins: List[Pin], footprint_filter: str = "*") -> str:
    """Generate KiCad 6.x symbol file content"""
    
    # Group pins using the GROUP field from pin tables (data-driven, not hardcoded!)
    pin_groups = {}
    for pin in pins:
        group = pin.group
        if group not in pin_groups:
            pin_groups[group] = []
        pin_groups[group].append(pin)
    
    # Extract groups (using .get() so missing groups don't cause errors)
    address_pins = pin_groups.get('ADDRESS', [])
    data_pins = pin_groups.get('DATA', [])
    power_pins = pin_groups.get('POWER', [])
    ground_pins = pin_groups.get('GROUND', [])
    bus_control = pin_groups.get('BUS_CTRL', [])
    interrupts = pin_groups.get('INTERRUPT', [])
    dma_pins = pin_groups.get('DMA', [])
    i2c_pins = pin_groups.get('I2C', [])
    uart_pins = pin_groups.get('UART', [])
    clock_pins = pin_groups.get('CLOCK', [])
    system_pins = pin_groups.get('SYSTEM', [])
    timer_pins = pin_groups.get('TIMER', [])
    
    # Video chip specific groups
    mem_data_pins = pin_groups.get('MEM_DATA', [])  # Memory data bus MD0-MD15
    mem_addr_pins = pin_groups.get('MEM_ADDR', [])  # Memory address MA0-MA9
    mem_ctrl_pins = pin_groups.get('MEM_CTRL', [])  # RAS, CAS, WE, OE
    video_pins = pin_groups.get('VIDEO', [])        # V0-V7 video output
    video_sync_pins = pin_groups.get('VIDEO_SYNC', [])  # VSYNC, HSYNC, etc.
    chip_sel_pins = pin_groups.get('CHIP_SEL', [])  # CS, WRP
    
    control_pins = pin_groups.get('CONTROL', [])
    
    # Sort buses by number
    def extract_bus_number(pin):
        match = re.search(r'\d+', pin.name)
        return int(match.group()) if match else 999
    
    address_pins.sort(key=extract_bus_number)
    data_pins.sort(key=extract_bus_number)
    power_pins.sort(key=lambda p: int(p.number))
    ground_pins.sort(key=lambda p: int(p.number))
    
    # Assign pins to sides with logical grouping (from GROUP field)
    # Left: Address bus, memory address, bus control, interrupts
    # Right: Data bus, memory data bus, DMA, I2C, UART, timers, chip selects
    # Top: Power, clock, video sync
    # Bottom: Ground, system control, memory control
    left_pins = address_pins + mem_addr_pins + bus_control + interrupts
    right_pins = data_pins + mem_data_pins + dma_pins + i2c_pins + uart_pins + timer_pins + chip_sel_pins + control_pins
    top_pins = power_pins + clock_pins + video_sync_pins
    bottom_pins = ground_pins + system_pins + mem_ctrl_pins + video_pins
    
    # Helper function to calculate size with group gaps
    def calculate_size_with_gaps(pins_list, gap_between_groups=2.54):
        if not pins_list:
            return 0
        group_changes = 0
        prev_group = None
        for pin in pins_list:
            if prev_group is not None and pin.group != prev_group:
                group_changes += 1
            prev_group = pin.group
        return len(pins_list) * pin_spacing + group_changes * gap_between_groups
    
    # Calculate symbol box size with gaps between groups
    pin_spacing = 2.54  # 2.54mm spacing between pins
    group_gap = 2.54    # 2.54mm gap between different groups
    
    left_height = calculate_size_with_gaps(left_pins, group_gap)
    right_height = calculate_size_with_gaps(right_pins, group_gap)
    top_width = calculate_size_with_gaps(top_pins, group_gap) if top_pins else 10.16
    bottom_width = calculate_size_with_gaps(bottom_pins, group_gap) if bottom_pins else 10.16
    
    # Symbol dimensions
    height = max(left_height, right_height) + 10.16  # Add padding
    width = max(top_width, bottom_width, 50.8)  # Minimum 50.8mm width
    
    # Start building symbol
    # Pin names will be shown outside the box with proper offset
    # Reference at top (above the box), Value at bottom (below the box)
    symbol = f'''(kicad_symbol_lib (version 20211014) (generator kicad_symbol_generator)
  (symbol "{component_name}" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)
    (property "Reference" "U" (id 0) (at 0 {height/2 + 2.54:.2f} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "{component_name}" (id 1) (at 0 {-height/2 - 2.54:.2f} 0)
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
      (rectangle (start {-width/2:.2f} {height/2:.2f}) (end {width/2:.2f} {-height/2:.2f})
        (stroke (width 0.254) (type default) (color 0 0 0 0))
        (fill (type background))
      )
    )
'''
    
    # Add pins
    symbol += f'    (symbol "{component_name}_1_1"\n'
    
    # Helper function to place pins with group gaps
    def place_pins_with_gaps(pins_list, x_pos, angle, gap_between_groups=2.54):
        """Place pins with gaps between different groups"""
        if not pins_list:
            return
        
        # Calculate total height including gaps
        group_changes = 0
        prev_group = None
        for pin in pins_list:
            if prev_group is not None and pin.group != prev_group:
                group_changes += 1
            prev_group = pin.group
        
        total_height = (len(pins_list) - 1) * pin_spacing + group_changes * gap_between_groups
        start_y = total_height / 2
        
        current_y = start_y
        prev_group = None
        for pin in pins_list:
            # Add gap if group changed
            if prev_group is not None and pin.group != prev_group:
                current_y -= gap_between_groups
            
            symbol_line = f'      (pin {pin.to_kicad_type()} line (at {x_pos:.2f} {current_y:.2f} {angle}) (length 5.08)\n'
            symbol_line += f'        (name "{pin.get_display_name()}" (effects (font (size 1.016 1.016))))\n'
            symbol_line += f'        (number "{pin.number}" (effects (font (size 1.016 1.016))))\n'
            symbol_line += f'      )\n'
            
            nonlocal symbol
            symbol += symbol_line
            
            current_y -= pin_spacing
            prev_group = pin.group
    
    # Left side pins (address bus first, then control)
    place_pins_with_gaps(left_pins, -width/2 - 5.08, 0)
    
    # Right side pins (data bus first, then control)
    place_pins_with_gaps(right_pins, width/2 + 5.08, 180)
    
    # Helper function for horizontal pins (top/bottom) with group gaps
    def place_horizontal_pins_with_gaps(pins_list, y_pos, angle, gap_between_groups=2.54):
        """Place horizontal pins with gaps between different groups"""
        if not pins_list:
            return
        
        # Calculate total width including gaps
        group_changes = 0
        prev_group = None
        for pin in pins_list:
            if prev_group is not None and pin.group != prev_group:
                group_changes += 1
            prev_group = pin.group
        
        total_width = (len(pins_list) - 1) * pin_spacing + group_changes * gap_between_groups
        start_x = -total_width / 2
        
        current_x = start_x
        prev_group = None
        for pin in pins_list:
            # Add gap if group changed
            if prev_group is not None and pin.group != prev_group:
                current_x += gap_between_groups
            
            symbol_line = f'      (pin {pin.to_kicad_type()} line (at {current_x:.2f} {y_pos:.2f} {angle}) (length 5.08)\n'
            symbol_line += f'        (name "{pin.get_display_name()}" (effects (font (size 1.016 1.016))))\n'
            symbol_line += f'        (number "{pin.number}" (effects (font (size 1.016 1.016))))\n'
            symbol_line += f'      )\n'
            
            nonlocal symbol
            symbol += symbol_line
            
            current_x += pin_spacing
            prev_group = pin.group
    
    # Top pins (power supplies)
    place_horizontal_pins_with_gaps(top_pins, height/2 + 5.08, 270)
    
    # Bottom pins (ground, NC/RESERVED)
    place_horizontal_pins_with_gaps(bottom_pins, -height/2 - 5.08, 90)
    
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
