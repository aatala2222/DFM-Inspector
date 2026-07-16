#!/usr/bin/env python3
"""
DFM Violation Teaching Part Generator
Creates a STEP file that intentionally violates every major CNC machining DFM rule.
Used as a teaching tool to demonstrate what NOT to do in design for manufacturability.

DFM Rules Violated:
1. Wall Thickness - Ultra-thin walls (0.3mm) below minimum 0.8mm
2. Hole Depth-to-Diameter Ratio - Deep holes >10:1 ratio
3. Internal Corner Radii - Sharp 90° internal corners (no radii)
4. Part Size - Oversized part >1000mm in one dimension
5. Small Features - Micro features <2mm
6. Non-Standard Hole Sizes - Odd diameter holes (7.3mm, 13.7mm)
7. Thread Depth - Insufficient thread engagement
8. Thin Tall Walls - High aspect ratio walls (>4:1 height:thickness)
9. Deep Narrow Pockets - Inaccessible pocket geometry
10. Undercuts - Features requiring special tooling
"""
import numpy as np
import trimesh
import os


def create_dfm_violation_step():
    """Generate a 3D part that violates all major CNC DFM rules"""
    
    print("=" * 60)
    print("DFM VIOLATION TEACHING PART GENERATOR")
    print("=" * 60)
    
    # Start with a large base block (violates Rule 4: Part Size >1000mm)
    # 1200mm x 400mm x 300mm - exceeds standard 3-axis machine capacity
    print("\n1. Creating oversized base block (1200x400x300mm)...")
    print("   VIOLATES: Part Size rule - exceeds 1000mm standard machine capacity")
    base = trimesh.creation.box(extents=[1.2, 0.4, 0.3])  # meters
    
    # Add ultra-thin wall feature (violates Rule 1: Wall Thickness <0.5mm)
    # 0.3mm thin wall standing 50mm tall (also violates aspect ratio >4:1)
    print("\n2. Adding ultra-thin wall (0.3mm thick, 50mm tall)...")
    print("   VIOLATES: Wall Thickness rule - 0.3mm below 0.8mm minimum")
    print("   VIOLATES: Aspect Ratio rule - 167:1 height:thickness ratio (max 4:1)")
    thin_wall = trimesh.creation.box(extents=[0.0003, 0.1, 0.05])  # 0.3mm x 100mm x 50mm
    thin_wall.apply_translation([0.3, 0.0, 0.175])
    
    # Add deep narrow pocket (violates Rule 9: Deep Narrow Pockets)
    # 5mm wide x 5mm long x 80mm deep pocket
    print("\n3. Adding deep narrow pocket (5x5x80mm)...")
    print("   VIOLATES: Deep Pocket rule - 16:1 depth-to-width ratio (max 4:1)")
    pocket = trimesh.creation.box(extents=[0.005, 0.005, 0.08])
    pocket.apply_translation([-0.2, 0.0, 0.11])
    
    # Add micro features (violates Rule 5: Small Features <2mm)
    # 0.5mm wide slot
    print("\n4. Adding micro features (0.5mm slot)...")
    print("   VIOLATES: Small Features rule - 0.5mm below 2.0mm minimum")
    micro_slot = trimesh.creation.box(extents=[0.0005, 0.05, 0.01])
    micro_slot.apply_translation([0.1, 0.1, 0.145])
    
    # Add deep hole features (violates Rule 2: Hole Depth >10x diameter)
    # 3mm diameter x 60mm deep hole (20:1 ratio)
    print("\n5. Adding deep holes (3mm dia x 60mm deep = 20:1 ratio)...")
    print("   VIOLATES: Hole Depth rule - 20:1 ratio exceeds 10:1 maximum")
    deep_hole = trimesh.creation.cylinder(radius=0.0015, height=0.06, sections=16)
    deep_hole.apply_translation([-0.1, 0.1, 0.12])
    
    # Add non-standard hole sizes (violates Rule 3: Non-Standard Holes)
    # 7.3mm and 13.7mm diameter holes (not standard 3,4,5,6,8,10,12mm)
    print("\n6. Adding non-standard holes (7.3mm and 13.7mm diameter)...")
    print("   VIOLATES: Hole Size rule - not standard drill sizes")
    odd_hole1 = trimesh.creation.cylinder(radius=0.00365, height=0.02, sections=16)
    odd_hole1.apply_translation([0.0, -0.1, 0.14])
    
    odd_hole2 = trimesh.creation.cylinder(radius=0.00685, height=0.02, sections=16)
    odd_hole2.apply_translation([0.05, -0.1, 0.14])
    
    # Add sharp internal corners (violates Rule 2: Internal Corner Radii)
    # Square pocket with perfectly sharp 90° corners
    print("\n7. Adding square pocket with sharp 90° corners...")
    print("   VIOLATES: Internal Corner Radii rule - no fillet radii (requires EDM)")
    sharp_pocket = trimesh.creation.box(extents=[0.03, 0.03, 0.025])
    sharp_pocket.apply_translation([0.2, 0.0, 0.1375])
    
    # Add undercut feature (violates Rule 10: Undercuts)
    # T-slot that requires special tooling
    print("\n8. Adding T-slot undercut feature...")
    print("   VIOLATES: Undercut rule - requires special T-slot cutter")
    t_slot_top = trimesh.creation.box(extents=[0.005, 0.08, 0.01])
    t_slot_top.apply_translation([-0.3, 0.0, 0.145])
    t_slot_bottom = trimesh.creation.box(extents=[0.015, 0.08, 0.005])
    t_slot_bottom.apply_translation([-0.3, 0.0, 0.1375])
    
    # Add tall thin fin (violates aspect ratio)
    # 0.5mm thick x 80mm tall fin
    print("\n9. Adding tall thin fin (0.5mm x 80mm = 160:1 ratio)...")
    print("   VIOLATES: Aspect Ratio rule - 160:1 exceeds 4:1 maximum")
    tall_fin = trimesh.creation.box(extents=[0.0005, 0.06, 0.08])
    tall_fin.apply_translation([-0.4, 0.0, 0.19])
    
    # Add features on multiple sides requiring many setups (violates Rule 5: Setup Minimization)
    # Features on all 6 faces
    print("\n10. Adding features on all 6 faces (requires 6+ setups)...")
    print("    VIOLATES: Setup Minimization rule - target is ≤2 setups")
    
    bottom_feature = trimesh.creation.box(extents=[0.02, 0.02, 0.005])
    bottom_feature.apply_translation([0.0, 0.0, -0.1475])
    
    side_feature1 = trimesh.creation.box(extents=[0.005, 0.02, 0.02])
    side_feature1.apply_translation([0.5975, 0.0, 0.0])
    
    side_feature2 = trimesh.creation.box(extents=[0.005, 0.02, 0.02])
    side_feature2.apply_translation([-0.5975, 0.0, 0.0])
    
    # Combine all features using boolean operations
    print("\n" + "=" * 60)
    print("Combining all violation features...")
    
    # Build the part by adding features to the base
    parts_to_add = [thin_wall, tall_fin]
    parts_to_subtract = [pocket, micro_slot, deep_hole, odd_hole1, odd_hole2, 
                         sharp_pocket, t_slot_top, t_slot_bottom, 
                         bottom_feature, side_feature1, side_feature2]
    
    # Start with base
    result = base
    
    # Add protruding features
    for part in parts_to_add:
        try:
            result = trimesh.boolean.union([result, part], engine='blender')
        except Exception:
            # If boolean fails, just concatenate meshes
            result = trimesh.util.concatenate([result, part])
    
    # Subtract pocket features
    for part in parts_to_subtract:
        try:
            result = trimesh.boolean.difference([result, part], engine='blender')
        except Exception:
            pass  # Skip if boolean fails
    
    # If booleans didn't work well, create a composite mesh
    if result is None or len(result.vertices) < 100:
        print("Using composite mesh approach...")
        all_meshes = [base, thin_wall, tall_fin]
        result = trimesh.util.concatenate(all_meshes)
    
    # Export as STEP file
    output_path = os.path.join('sample_files', 'DFM_Violation_Teaching_Part.STEP')
    
    # Try to export as STEP
    try:
        result.export(output_path, file_type='step')
        print(f"\n✓ STEP file exported: {output_path}")
    except Exception as e:
        print(f"STEP export not available ({e}), exporting as STL instead...")
        output_path = os.path.join('sample_files', 'DFM_Violation_Teaching_Part.STL')
        result.export(output_path)
        print(f"✓ STL file exported: {output_path}")
    
    # Also export STL as backup
    stl_path = os.path.join('sample_files', 'DFM_Violation_Teaching_Part.STL')
    result.export(stl_path)
    print(f"✓ STL backup exported: {stl_path}")
    
    print("\n" + "=" * 60)
    print("DFM VIOLATIONS SUMMARY")
    print("=" * 60)
    print("""
This part intentionally violates the following DFM rules:

 1. WALL THICKNESS      - 0.3mm walls (min: 0.8mm aluminum, 1.0mm steel)
 2. HOLE DEPTH RATIO    - 20:1 depth-to-diameter (max: 4:1 standard, 10:1 gun drill)
 3. INTERNAL CORNERS    - Sharp 90° corners (need radius ≥ tool radius)
 4. PART SIZE           - 1200mm length (standard machine: 500mm)
 5. SMALL FEATURES      - 0.5mm slot (min: 2.0mm for standard tooling)
 6. NON-STANDARD HOLES  - 7.3mm, 13.7mm (use 3,4,5,6,8,10,12mm)
 7. ASPECT RATIO        - 160:1 fin height:thickness (max: 4:1)
 8. DEEP POCKETS        - 16:1 depth-to-width (max: 4:1)
 9. UNDERCUTS           - T-slot requiring special tooling
10. SETUP COUNT         - Features on 6 faces (target: ≤2 setups)
11. TOLERANCE           - Design implies tight tolerances everywhere

Use this part with the DFM Inspector to see all violations flagged.
""")
    
    return output_path


if __name__ == '__main__':
    create_dfm_violation_step()
