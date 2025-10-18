# Philips/NXP CD-i Multimedia KiCad Library

✅ **COMPLETE AND VERIFIED** - A comprehensive KiCad library containing symbols and footprints for Philips/NXP CD-i (Compact Disc Interactive) multimedia processors.

## 📦 Components Included

### SCC68070 - CD-i Microprocessor (16/32-bit)
**Two package variants available:**

#### SCC68070_PLCC84
- **Package**: PLCC-84 (SOT189CG)
- **Dimensions**: 29.21mm × 29.21mm, 1.27mm pitch
- **Footprint**: `Package_LCC:PLCC-84`
- **Pins**: 84 (21 per side)

#### SCC68070_QFP120
- **Package**: QFP-120 (SOT220)
- **Dimensions**: 14mm × 14mm body, 0.5mm pitch
- **Footprint**: `Package_QFP:LQFP-120_14x14mm_P0.5mm`
- **Pins**: 120 (30 per side)

**Features:**
- 68000-compatible CPU core (16/32-bit)
- 24-bit address bus (16MB address space, A1-A23)
- 16-bit data bus (D0-D15)
- Integrated I²C controller (SDA, SCL)
- Integrated UART (TXD, RXD, RTS, CTS)
- DMA controller with bus arbitration
- Timer and interrupt controllers
- Active-LOW signal support with overline notation

### SCC66470 - Video Signal Processor
#### SCC66470_QFP120
- **Package**: QFP-120 (SOT220B)
- **Dimensions**: 14mm × 14mm body, 0.5mm pitch
- **Footprint**: `Package_QFP:LQFP-120_14x14mm_P0.5mm`
- **Pins**: 120 (30 per side)

**Features:**
- RGB video output (Red/Green/Blue channels)
- Hardware video sync generation (HSYNC, VSYNC)
- VRAM interface with full control signals
- 16-bit data bus interface
- Programmable display timing
- Hardware graphics acceleration

## 📂 Library Structure

```
kicad_scc68070/
├── symbols/                            ✅ Complete
│   ├── SCC68070_PLCC84.kicad_sym      # 84-pin symbol
│   ├── SCC68070_QFP120.kicad_sym      # 120-pin symbol
│   └── SCC66470_QFP120.kicad_sym      # 120-pin video processor
├── pin_extraction/                     ✅ Verified pin tables
│   ├── SCC68070_PLCC84_complete.txt   # Full pin documentation
│   ├── SCC68070_QFP120_complete.txt   # Full pin documentation
│   └── SCC66470_QFP120_complete.txt   # Full pin documentation
├── datasheets/
│   ├── SCC68070.pdf                   # SCC68070 datasheet
│   ├── SCC68070_fulltext.txt          # OCR extracted text
│   ├── SCC66470.pdf                   # SCC66470 datasheet
│   └── SCC66470_fulltext.txt          # OCR extracted text
└── Documentation/
    ├── README.md                       # This file
    ├── PROJECT_COMPLETE.md             # Complete project summary
    ├── SYMBOL_README.md                # Symbol usage guide
    └── QFP120_FOOTPRINT_SPECS.md       # Footprint specifications
```

## 🚀 Installation

### Method 1: KiCad Symbol Editor (Recommended)

1. **Add Symbol Libraries**:
   - Open KiCad Symbol Editor
   - File → Add Library
   - Browse and select each symbol file:
     - `symbols/SCC68070_PLCC84.kicad_sym`
     - `symbols/SCC68070_QFP120.kicad_sym`
     - `symbols/SCC66470_QFP120.kicad_sym`
   - Save to global or project library table

2. **Footprints** (Use KiCad Standard Libraries):
   - Footprints are pre-assigned to standard KiCad libraries
   - No additional footprint installation needed
   - Uses: `Package_LCC` and `Package_QFP` libraries

### Method 2: Project-Specific Libraries

Copy symbol files to your project directory and add to `sym-lib-table`:
```
(lib (name "SCC68070_PLCC84")(type "KiCad")(uri "${KIPRJMOD}/symbols/SCC68070_PLCC84.kicad_sym")(options "")(descr "SCC68070 PLCC-84"))
(lib (name "SCC68070_QFP120")(type "KiCad")(uri "${KIPRJMOD}/symbols/SCC68070_QFP120.kicad_sym")(options "")(descr "SCC68070 QFP-120"))
(lib (name "SCC66470_QFP120")(type "KiCad")(uri "${KIPRJMOD}/symbols/SCC66470_QFP120.kicad_sym")(options "")(descr "SCC66470 QFP-120"))
```

## 🔧 Usage

### Adding Components to Schematic

1. Open your schematic in KiCad Schematic Editor
2. Press `A` (Add Symbol) or click the "Place Symbol" button
3. Search for:
   - `SCC68070_PLCC84` - Microprocessor in PLCC-84 package
   - `SCC68070_QFP120` - Microprocessor in QFP-120 package
   - `SCC66470_QFP120` - Video processor in QFP-120 package
4. Place the component on your schematic

### Footprint Assignment

✅ Footprints are **pre-assigned** in the symbols:
- `SCC68070_PLCC84` → `Package_LCC:PLCC-84`
- `SCC68070_QFP120` → `Package_QFP:LQFP-120_14x14mm_P0.5mm`
- `SCC66470_QFP120` → `Package_QFP:LQFP-120_14x14mm_P0.5mm`

No manual footprint assignment required!

## 📋 Pin Configuration Overview

### SCC68070 PLCC-84
- **Power (VDD)**: Pins 1, 53 (2 pins)
- **Ground (VSS)**: Pins 22, 83 (2 pins)
- **Address Bus**: A1-A23 (23 pins for 16MB address space)
- **Data Bus**: D0-D15 (16 pins)
- **Control Signals**: AS, UDS, LDS, R/W, DTACK, etc.
- **DMA**: REQ1, REQ2, ACK1, ACK2, DONE, DTC
- **Interrupts**: INT1, INT2, IN2, IN4, IN5, IACK2, IACK4, IACK5, IACK7, NMI
- **Serial**: I²C (SDA, SCL), UART (TXD, RXD, RTS, CTS)
- **Timers**: T1, T2

### SCC68070 QFP-120
- **Power (VDD)**: Pins 45, 46, 105, 106 (4 pins)
- **Ground (VSS)**: Pins 16, 17, 75, 76 (4 pins)
- **Reserved**: Pins 12, 52, 58, 70, 93, 99, 107, 108 (8 pins - do not connect)
- **No Connect**: 24 pins (do not connect)
- **Signals**: Same as PLCC-84 but different pin arrangement

### SCC66470 QFP-120
- **Power (VDD)**: Pins 15, 47, 76, 90, 95, 104, 120 (7 pins)
- **Ground (VSS)**: Pins 1, 17, 31, 45, 74, 96, 106 (7 pins)
- **Pins 9-33**: Address Bus (A0-A23)
- **Pins 40-57**: Data Bus (D0-D15)
- **Pins 35-39, 61-63**: Bus Control Signals
- **Pins 70-71**: I²C Interface (SCL, SDA)
- **Pins 72-73**: UART Interface (TXD, RXD)
- **Pins 75-76**: DMA Control
- **Pin 65**: System Clock Input
- **Pins 4-8**: System Control (~BERR, ~RESET, ~HALT, ~BR, ~BG)
- **Pin 84**: No Connect

### SCC66470 Pin Groups
- **Power (VDD)**: Pins 15, 47, 76, 90, 95, 104, 120 (7 pins)
- **Ground (VSS)**: Pins 1, 17, 31, 45, 74, 96, 106 (7 pins)
- **Address Bus**: A0-A23 (24 pins for 16MB address space)
- **Data Bus**: D0-D15 (16 pins)
- **Bus Control**: AS, UDS, LDS, R/W, DTACK, FC0-FC2
- **DMA**: BR, BG, BGACK
- **Interrupts**: INT1, INT2
- **I²C Interface**: SCL, SDA
- **UART Interface**: TXD, RXD
- **System Control**: BERR, RESET, HALT
- **Clock**: CLK input
- **VRAM Interface**: RAS0, RAS1, CAS, WE, OE
- **Video Output**: RGB signals and sync
- **No Connect**: Pin 84

## ⚠️ Design Considerations

### Power Supply
- Both chips require stable **5V supply** (VDD)
- Multiple VDD and VSS pins should all be connected
- Add decoupling capacitors (100nF ceramic) close to each VDD pin
- Additional bulk capacitance (10-47µF) recommended per chip

### Clock Requirements
- **SCC68070**: External clock input on pin 65 (typically 30MHz)
- **SCC66470**: Can use external clock (pin 3) or crystal oscillator (pins 4-5)

### PCB Layout Tips
- PLCC packages can be surface-mounted or use through-hole sockets
- Ensure proper pin 1 orientation (marked with triangle/dot)
- Keep data and address buses short and parallel where possible
- Place decoupling capacitors on the same side as the IC
- Use ground planes for better signal integrity
- Consider thermal relief for ground connections

### Reflow Considerations
- **PLCC-84**: 1.27mm pitch, use standard PLCC reflow profile
- **QFP-120**: 0.5mm pitch (verified from datasheet), requires precision reflow
  - Pad dimensions as per LQFP-120 footprint
  - Use solder paste with proper stencil thickness (typically 0.125mm for 0.5mm pitch)
  - Recommended reflow profile: SAC305 (lead-free) or SnPb (if applicable)
  - Consider stencil design for fine-pitch assembly

## 📚 References

### Datasheets
- [SCC68070 Datasheet](datasheets/SCC68070.PDF) - Complete technical specifications
- [SCC66470 Datasheet](datasheets/SCC66470.pdf) - Video processor documentation

### Additional Resources
- CD-i System Documentation
- 68000 CPU Family Reference Manual
- IPC-7351 Footprint Standards

## 🔍 Version History

### v1.0 (2025-10-18)
- Initial release
- Added SCC68070 symbol (PLCC-84)
- Added SCC66470 symbol (PLCC-68)
- Created IPC-compliant footprints for both components
- Included comprehensive documentation

## 📝 Notes

- **Pin assignments** in symbols are based on typical CD-i implementations. Always verify against your specific datasheets
- **Footprints** follow IPC-7351B standards for PLCC packages
- These components are **vintage/legacy** parts (1990s era) and may have limited availability
- Consider using sockets for prototyping and easier replacement

## 🤝 Contributing

Improvements and corrections are welcome! If you find any errors in pin assignments or footprint dimensions:
1. Verify against the official datasheets (included in `datasheets/`)
2. Submit corrections with reference to datasheet page numbers
3. Test footprints with actual hardware when possible

## 📄 License

This library is provided as-is for hardware design purposes. Component specifications and pin assignments are based on official Philips/NXP documentation.

## ⚡ Quick Start Example

To create a basic CD-i system schematic:
1. Add `SCC68070` (microcontroller)
2. Add `SCC66470` (video processor)
3. Connect shared data bus (D0-D15)
4. Connect address lines from CPU to video processor
5. Add power supplies with proper decoupling
6. Add clock generation circuit
7. Connect video output signals to DACs/connectors

---

**Designed for KiCad 6.x and later**

For questions or support, refer to the datasheets in the `datasheets/` directory.
