"""
Test STEP file loading to see mesh quality
"""
import os

step_file = r"C:\Users\aleatala\AppData\Local\Temp\420-21634.STEP"

if not os.path.exists(step_file):
    print(f"File not found: {step_file}")
    exit(1)

print(f"Testing STEP file: {step_file}")
print(f"File size: {os.path.getsize(step_file):,} bytes")

# Try trimesh
print("\n" + "="*70)
print("METHOD 1: Trimesh")
print("="*70)
try:
    import trimesh
    mesh = trimesh.load(step_file)
    
    if isinstance(mesh, trimesh.Scene):
        print(f"Loaded as Scene with {len(mesh.geometry)} geometries")
        # Combine all geometries
        mesh = trimesh.util.concatenate([geom for geom in mesh.geometry.values()])
    
    print(f"✓ Loaded successfully!")
    print(f"  Vertices: {len(mesh.vertices):,}")
    print(f"  Faces: {len(mesh.faces):,}")
    print(f"  Bounds: {mesh.bounds}")
    print(f"  Is watertight: {mesh.is_watertight}")
    
    if len(mesh.faces) > 100:
        print(f"\n✅ HIGH QUALITY MESH - Can render with full detail!")
    else:
        print(f"\n⚠️ LOW QUALITY MESH - Only {len(mesh.faces)} faces")
        
except Exception as e:
    print(f"✗ Trimesh failed: {e}")

# Try EnhancedSTEPParser
print("\n" + "="*70)
print("METHOD 2: EnhancedSTEPParser")
print("="*70)
try:
    from src.enhanced_step_parser import EnhancedSTEPParser
    
    parser = EnhancedSTEPParser(step_file)
    success = parser.load()
    
    if success and parser.mesh:
        print(f"✓ Loaded successfully!")
        print(f"  Vertices: {len(parser.mesh.vertices):,}")
        print(f"  Faces: {len(parser.mesh.faces):,}")
        print(f"  Parse method: {parser.parse_result.get('method', 'unknown')}")
        
        if len(parser.mesh.faces) > 100:
            print(f"\n✅ HIGH QUALITY MESH - Can render with full detail!")
        else:
            print(f"\n⚠️ LOW QUALITY MESH - Only {len(parser.mesh.faces)} faces")
            print(f"   This is likely a convex hull, not the actual geometry")
    else:
        print(f"✗ Failed to load")
        
except Exception as e:
    print(f"✗ EnhancedSTEPParser failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print("For CAD-quality renderings like Image 2, we need:")
print("1. Full detailed mesh (1000+ faces)")
print("2. Proper STEP file parsing (not convex hull)")
print("3. If trimesh loads more faces, use that instead")
