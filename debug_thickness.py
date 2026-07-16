import numpy as np
from src.cadquery_feature_extractor import extract_features_from_step
import cadquery as cq
from OCP.TopAbs import TopAbs_FACE
from OCP.TopExp import TopExp_Explorer
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.TopoDS import TopoDS

filepath = 'C:/Users/aleatala/AppData/Local/Temp/sheet_metal_test.STEP'
shape = cq.importers.importStep(filepath)
solid = shape.val()
scale = 1000.0

# Collect planar faces
planar_faces = []
exp = TopExp_Explorer(solid.wrapped, TopAbs_FACE)
while exp.More():
    face = TopoDS.Face_s(exp.Current())
    adaptor = BRepAdaptor_Surface(face)
    if adaptor.GetType() == GeomAbs_Plane:
        plane = adaptor.Plane()
        normal = plane.Axis().Direction()
        fprops = GProp_GProps()
        BRepGProp.SurfaceProperties_s(face, fprops)
        area = fprops.Mass() * (scale**2)
        com = fprops.CentreOfMass()
        planar_faces.append({
            'normal': {'x': round(normal.X(),6), 'y': round(normal.Y(),6), 'z': round(normal.Z(),6)},
            'area': round(area, 3),
            'center': {'x': com.X()*scale, 'y': com.Y()*scale, 'z': com.Z()*scale}
        })
    exp.Next()

print(f"Total planar faces: {len(planar_faces)}")

# Find all anti-parallel pairs and their distances
pairs = []
for i, f1 in enumerate(planar_faces):
    n1 = np.array([f1['normal']['x'], f1['normal']['y'], f1['normal']['z']])
    for f2 in planar_faces[i+1:]:
        n2 = np.array([f2['normal']['x'], f2['normal']['y'], f2['normal']['z']])
        dot = np.dot(n1, n2)
        if dot < -0.99:
            c1 = np.array([f1['center']['x'], f1['center']['y'], f1['center']['z']])
            c2 = np.array([f2['center']['x'], f2['center']['y'], f2['center']['z']])
            dist = abs(np.dot(c2 - c1, n1))
            if 0.3 < dist < 10.0:
                pairs.append((dist, min(f1['area'], f2['area']), f1['area'], f2['area']))

pairs.sort(key=lambda x: x[0])
print(f"\nAnti-parallel face pairs (thickness candidates):")
for dist, min_area, a1, a2 in pairs:
    print(f"  dist={dist:.3f}mm, areas={a1:.1f} & {a2:.1f} mm2")
