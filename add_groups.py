#!/usr/bin/env python3
"""
Add GROUP column to pin table files
"""

def get_group(signal, pin_type):
    """Determine pin group based on signal name and type"""
    if pin_type == 'PWR':
        if 'VDD' in signal or 'VCC' in signal:
            return 'POWER'
        else:
            return 'GROUND'
    elif pin_type == 'NC' or signal == 'RESERVED':
        return 'NC'
    # Check EXACT matches first to avoid false positives!
    elif signal in ['SDA', 'SCL']:
        return 'I2C'  # I²C serial bus
    elif signal in ['TXD', 'RXD', 'RTS', 'CTS', 'XCKI']:
        return 'UART'  # UART serial interface
    # Now check bus patterns
    elif signal.startswith('A') and len(signal) > 1 and signal[1].isdigit():
        return 'ADDRESS'
    elif signal.startswith('D') and len(signal) > 1 and signal[1].isdigit():
        return 'DATA'
    elif signal.startswith('MD') and len(signal) > 2 and signal[2].isdigit():
        return 'MEM_DATA'  # Memory Data bus (MD0-MD15) for VRAM
    elif signal.startswith('MA') and len(signal) > 2 and signal[2].isdigit():
        return 'MEM_ADDR'  # Memory Address for video RAM
    elif signal.startswith('V') and len(signal) > 1 and signal[1].isdigit():
        return 'VIDEO'  # Video output bits V0-V7
    # Memory control
    elif any(x in signal for x in ['RAS', 'CAS', 'WE', 'OE', 'W/R']):
        return 'MEM_CTRL'
    # Video sync - check AFTER SDA/SCL!
    elif signal in ['VSYNC', 'HSYNC', 'CSYNC', 'BLANK', 'DA']:
        return 'VIDEO_SYNC'
    # Chip selects
    elif signal.startswith('CS') or signal == 'WRP':
        return 'CHIP_SEL'
    # Interrupts
    elif any(x in signal for x in ['INT', 'IRQ', 'IACK', 'NMI']):
        return 'INTERRUPT'
    elif signal.startswith('IN') and len(signal) > 2 and signal[2].isdigit():
        return 'INTERRUPT'  # IN2, IN4, IN5
    # DMA
    elif any(x in signal for x in ['REQ', 'DONE', 'DTC', 'BR', 'BG', 'BGACK']):
        return 'DMA'
    elif signal.startswith('ACK') and len(signal) > 3:
        return 'DMA'  # ACK1, ACK2
    # Clock
    elif any(x in signal for x in ['CLK', 'XTAL', 'CKOUT', 'XT/']):
        return 'CLOCK'
    # System
    elif any(x in signal for x in ['RESET', 'HALT', 'BERR', 'AV', 'RSTOUT', 'M/S', 'TST']):
        return 'SYSTEM'
    elif any(x in signal for x in ['AS', 'DS', 'UDS', 'LDS', 'DTACK', 'FC', 'R/W', 'RDY']):
        return 'BUS_CTRL'
    elif any(x in signal for x in ['T1', 'T2']):
        return 'TIMER'
    elif signal == 'IPA':
        return 'VIDEO'
    else:
        return 'CONTROL'

def process_file(input_file, output_file):
    """Add GROUP column to pin table"""
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    with open(output_file, 'w') as f:
        for line in lines:
            # Skip comments
            if line.startswith('#'):
                f.write(line)
                continue
            
            # Header line
            if line.startswith('PIN |'):
                # Check if GROUP already exists
                if 'GROUP' in line:
                    f.write(line)
                else:
                    # Add GROUP column
                    line = line.replace('| FUNCTION', '| GROUP      | FUNCTION')
                    f.write(line)
                continue
            
            # Separator line
            if '---' in line:
                # Rebuild separator line properly
                f.write('----|-------------|------|-----|-------|------------|--------------------------------------------------\n')
                continue
            
            # Data line - parse and add group
            if '|' in line and line.strip():
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 7:
                    # Already has GROUP column
                    f.write(line)
                elif len(parts) >= 6:
                    pin_num = parts[0]
                    signal = parts[1]
                    pin_type = parts[2]
                    polarity = parts[3]
                    drive = parts[4]
                    function = parts[5]
                    
                    # Determine group
                    group = get_group(signal, pin_type)
                    
                    # Write line with GROUP
                    f.write(f"{pin_num:<4}| {signal:<12}| {pin_type:<5}| {polarity:<4}| {drive:<6}| {group:<11}| {function}\n")
                else:
                    f.write(line)
            else:
                f.write(line)

if __name__ == '__main__':
    import sys
    files = [
        'pin_extraction/SCC68070_PLCC84_complete.txt',
        'pin_extraction/SCC68070_QFP120_complete.txt',
        'pin_extraction/SCC66470_QFP120_complete.txt'
    ]
    
    for file in files:
        print(f"Processing {file}...")
        process_file(file, file + '.tmp')
        import shutil
        shutil.move(file + '.tmp', file)
        print(f"  Done!")
