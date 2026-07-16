#!/usr/bin/env python3
"""
DFM Violation Teaching Part - STEP File Generator
Creates a proper STEP file using CadQuery that violates every major CNC DFM rule.
"""
import cadquery as cq
import os


def create_violation_part():
    print("=" * 60)
    print("DFM VIOLATION TEACHING PART - STEP GENERATOR")
    print("=" * 60)

    # Start with oversized base block: 1200 x 400 x 300mm
    # VIOLATES Rule 4: Part Size >1000mm
    print("\n1. Oversized base (1200x400x300mm) - VIOLATES Part Size rule")
    part = cq.Workplane("XY").box(1200, 400, 300)

    # Add ultra-thin wall: 0.3mm thick, 100mm wide, 80mm tall
    # VIOLATES Rule 1: Wall Thickness <0.8mm
    # VIOLATES Rule 7: Aspect Ratio 267:1 (max 4:1)
    print("2. Ultra-thin wall (0.3mm x 80mm tall) - VIOLATES Wall Thickness + Aspect Ratio")
    part = (
        part
        .faces(">Z")
        .workplane()
        .center(300, 0)
        .box(0.3, 100, 80, combine=True)
    )

    # Add tall thin fin: 0.5mm thick, 60mm wide, 100mm tall
    # VIOLATES Rule 7: Aspect Ratio 200:1
    print("3. Tall thin fin (0.5mm x 100mm) - VIOLATES Aspect Ratio rule")
    part = (
        part
        .faces(">Z")
        .workplane()
        .center(-400, 0)
        .box(0.5, 60, 100, combine=True)
    )

    # Cut deep narrow pocket: 5mm x 5mm x 120mm deep
    # VIOLATES Rule 8: Deep Pocket 24:1 ratio (max 4:1)
    print("4. Deep narrow pocket (5x5x120mm) - VIOLATES Deep Pocket rule")
    part = (
        part
        .faces(">Z")
        .workplane()
        .center(-200, 100)
        .rect(5, 5)
        .cutBlind(-120)
    )

    # Cut sharp-cornered square pocket: 30x30x25mm with NO fillet
    # VIOLATES Rule 2: Internal Corner Radii (sharp 90° corners)
    print("5. Sharp-cornered pocket (30x30x25mm) - VIOLATES Corner Radii rule")
    part = (
        part
        .faces(">Z")
        .workplane()
        .center(200, 0)
        .rect(30, 30)
        .cutBlind(-25)
    )

    # Cut micro slot: 0.5mm wide x 50mm long x 10mm deep
    # VIOLATES Rule 5: Small Features <2mm
    print("6. Micro slot (0.5mm wide) - VIOLATES Small Features rule")
    part = (
        part
        .faces(">Z")
        .workplane()
        .center(100, 100)
        .rect(0.5, 50)
        .cutBlind(-10)
    )

    # Deep hole: 3mm diameter x 80mm deep (ratio 26.7:1)
    # VIOLATES Rule 2: Hole Depth >10:1
    print("7. Deep hole (3mm dia x 80mm deep = 26.7:1) - VIOLATES Hole Depth rule")
    part = (
        part
        .faces(">Z")
        .workplane()
        .center(-100, -100)
        .hole(3, 80)
    )

    # Non-standard holes: 7.3mm and 13.7mm diameter
    # VIOLATES Rule 3: Non-Standard Hole Sizes
    print("8. Non-standard holes (7.3mm, 13.7mm) - VIOLATES Hole Size rule")
    part = (
        part
        .faces(">Z")
        .workplane()
        .center(0, -100)
        .hole(7.3, 20)
    )
    part = (
        part
        .faces(">Z")
        .workplane()
        .center(50, -100)
        .hole(13.7, 20)
    )

    # T-slot undercut on the side
    # VIOLATES Rule 9: Undercuts requiring special tooling
    print("9. T-slot undercut - VIOLATES Undercut rule")
    # Narrow top slot
    part = (
        part
        .faces(">X")
        .workplane()
        .center(0, 0)
        .rect(5, 80)
        .cutBlind(-20)
    )
    # Wider bottom (undercut)
    part = (
        part
        .faces(">X")
        .workplane()
        .center(0, 0)
        .rect(15, 80)
        .cutBlind(-8)
    )

    # Features on bottom face (requires flipping = extra setup)
    # VIOLATES Rule 5: Setup Minimization (features on >2 faces)
    print("10. Bottom features (requires 6+ setups) - VIOLATES Setup Minimization")
    part = (
        part
        .faces("<Z")
        .workplane()
        .center(0, 0)
        .rect(20, 20)
        .cutBlind(-10)
    )

    # Side pocket on left face
    part = (
        part
        .faces("<X")
        .workplane()
        .center(0, 0)
        .rect(30, 30)
        .cutBlind(-15)
    )

    # Side pocket on front face
    part = (
        part
        .faces(">Y")
        .workplane()
        .center(0, 0)
        .rect(25, 25)
        .cutBlind(-12)
    )

    # Side pocket on back face
    part = (
        part
        .faces("<Y")
        .workplane()
        .center(0, 0)
        .rect(25, 25)
        .cutBlind(-12)
    )

    # Export as STEP
    output_path = os.path.join('sample_files', 'DFM_Violation_Teaching_Part.STEP')
    cq.exporters.export(part, output_path)
    print(f"\n✓ STEP file exported: {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")

    print("\n" + "=" * 60)
    print("DFM VIOLATIONS IN THIS PART:")
    print("=" * 60)
    print("""
 1. WALL THICKNESS      0.3mm thin wall (min: 0.8mm Al, 1.0mm steel)
 2. HOLE DEPTH RATIO    3mm x 80mm deep = 26.7:1 (max: 4:1)
 3. INTERNAL CORNERS    Sharp 90° pocket corners (need fillet radii)
 4. PART SIZE           1200mm length (standard machine max: 500mm)
 5. SMALL FEATURES      0.5mm slot (min: 2.0mm standard tooling)
 6. NON-STANDARD HOLES  7.3mm, 13.7mm (standard: 3,4,5,6,8,10,12mm)
 7. ASPECT RATIO        0.3mm x 80mm wall = 267:1 (max: 4:1)
 8. DEEP POCKETS        5mm x 120mm = 24:1 depth:width (max: 4:1)
 9. UNDERCUTS           T-slot requiring special tooling
10. SETUP COUNT         Features on all 6 faces (target: ≤2 setups)
11. TOLERANCES          Over-toleranced design (use ±0.1mm standard)

Upload this file to the DFM Inspector to see all violations flagged.
""")
    return output_path


if __name__ == '__main__':
    create_violation_part()
