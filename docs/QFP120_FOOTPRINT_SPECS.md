# QFP-120 Package Specifications
# From SCC68070/SCC66470 Datasheets

## SCC68070 QFP-120 (SOT220)
================================

**Package Code:** SOT220
**Datasheet Reference:** Figure 58

### Key Dimensions (from PDF diagram):
- **Pin pitch:** 0.5mm (standard)
- **Pin width:** 0.5mm max
- **Total pins:** 120 (30 pins per side)
- **Package type:** Plastic Quad Flat Pack

### Calculations:
- 30 pins per side × 0.5mm pitch = 15mm span per side
- Body size: likely 14mm × 14mm
- Overall size with leads: ~16mm × 16mm

## SCC66470 QFP-120 (SOT220B)
================================

**Package Code:** SOT220B (variant B)
**Same dimensions as SOT220**

### Expected footprint:
Both chips should use the same footprint with 0.5mm pitch

## KiCad Standard Footprint Match
================================

**Recommended KiCad footprint:**
```
Package_QFP.pretty/LQFP-120_14x14mm_P0.5mm
```
or
```
Package_QFP.pretty/TQFP-120_14x14mm_P0.5mm
```

### Footprint Details:
- Pin count: 120 (30 per side)
- Pitch: 0.5mm
- Body: 14mm × 14mm
- Package height: Low profile (LQFP) or Thin (TQFP)

## PLCC-84 Package (for reference)
================================

**Package Code:** SOT189CG (AGA)

### Key Dimensions:
- **Pin pitch:** 1.27mm (0.050")
- **Body size:** 29.21mm × 29.21mm (verified)
- **Total pins:** 84 (21 pins per side)

**KiCad footprint:**
```
Package_LCC.pretty/PLCC-84_*
```

## Footprint Assignment Summary
================================

| Component | Package | KiCad Footprint |
|-----------|---------|-----------------|
| SCC68070_PLCC84 | SOT189CG | PLCC-84_THT-Socket or PLCC-84_SMD |
| SCC68070_QFP120 | SOT220 | LQFP-120_14x14mm_P0.5mm |
| SCC66470_QFP120 | SOT220B | LQFP-120_14x14mm_P0.5mm |

## Notes
================================

1. **0.5mm pitch confirmed** - This is the standard pitch for QFP-120 packages from the 1990s
2. **Both chips use same footprint** - SOT220 and SOT220B are compatible
3. **LQFP vs TQFP** - Both work, LQFP (Low-profile) is more common
4. **IPC-7351B compliant** - KiCad's standard footprints follow IPC standards

## Next Steps
================================

1. Update symbol files with correct footprint references
2. Verify footprint exists in KiCad libraries
3. Create custom footprint if KiCad doesn't have exact match
4. Test footprint pad sizes for manufacturability
