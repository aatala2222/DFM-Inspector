"""
CadQuery-based Feature Extractor for Sheet Metal DFM Analysis
Uses OpenCascade B-Rep topology to detect holes, bends, and spatial relationships.
Based on 930-00172_R01 Design Guideline, Sheet Metal.
"""
import logging
import math
import numpy as np
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


def extract_features_from_step(filepath: str) -> Dict:
    """
    Extract geometric features from a STEP file using CadQuery/OpenCascade.
    
    Returns dict with:
        - holes: list of detected cylindrical holes with diameter, depth, center
        - bends: list of detected bends with angle, radius, location
        - planar_faces: list of flat faces with normal and area
        - dimensions: bounding box in mm
        - thickness: estimated sheet metal thickness
        - hole_to_bend_distances: proximity analysis
        - hole_to_edge_distances: edge proximity analysis
        - hole_to_hole_distances: spacing analysis
    """
    try:
        import cadquery as cq
        from OCP.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
        from OCP.GeomAbs import (GeomAbs_Cylinder, GeomAbs_Plane, GeomAbs_Cone,
                                  GeomAbs_Torus, GeomAbs_Line, GeomAbs_Circle)
        from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_REVERSED
        from OCP.TopExp import TopExp_Explorer
        from OCP.BRepGProp import BRepGProp
        from OCP.Bnd import Bnd_Box
        from OCP.BRepBndLib import BRepBndLib
        from OCP.gp import gp_Pnt, gp_Vec
        from OCP.BRepTools import BRepTools
    except ImportError as e:
        logger.error(f"CadQuery/OCP not available: {e}")
        return {'error': str(e), 'features_extracted': False}

    logger.info(f"Extracting features from: {filepath}")
    
    try:
        # Load STEP file
        shape = cq.importers.importStep(filepath)
        solid = shape.val()
    except Exception as e:
        logger.error(f"Failed to load STEP file: {e}")
        return {'error': str(e), 'features_extracted': False}

    # Get bounding box
    bbox = Bnd_Box()
    BRepBndLib.Add_s(solid.wrapped, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    
    # Auto-detect units (meters vs mm)
    max_dim = max(xmax - xmin, ymax - ymin, zmax - zmin)
    if max_dim > 0 and max_dim < 1.0:
        scale = 1000.0  # meters to mm
        logger.info(f"Auto-detected units: meters (max dim {max_dim:.4f}m). Converting to mm.")
    else:
        scale = 1.0
    
    dims = {
        'x': (xmax - xmin) * scale,
        'y': (ymax - ymin) * scale,
        'z': (zmax - zmin) * scale
    }
    
    # Get volume and surface area
    from OCP.GProp import GProp_GProps
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(solid.wrapped, props)
    volume = props.Mass() * (scale ** 3)
    
    sprops = GProp_GProps()
    BRepGProp.SurfaceProperties_s(solid.wrapped, sprops)
    surface_area = sprops.Mass() * (scale ** 2)

    # Extract faces
    holes = []
    planar_faces = []
    cylindrical_faces = []
    bend_radii_faces = []
    all_face_data = []
    
    explorer = TopExp_Explorer(solid.wrapped, TopAbs_FACE)
    face_idx = 0
    
    while explorer.More():
        from OCP.TopoDS import TopoDS
        face = TopoDS.Face_s(explorer.Current())
        adaptor = BRepAdaptor_Surface(face)
        surface_type = adaptor.GetType()
        
        # Get face area
        from OCP.GProp import GProp_GProps
        fprops = GProp_GProps()
        BRepGProp.SurfaceProperties_s(face, fprops)
        face_area = fprops.Mass() * (scale ** 2)
        center_of_mass = fprops.CentreOfMass()
        face_center = {
            'x': center_of_mass.X() * scale,
            'y': center_of_mass.Y() * scale,
            'z': center_of_mass.Z() * scale
        }

        if surface_type == GeomAbs_Cylinder:
            cylinder = adaptor.Cylinder()
            radius = cylinder.Radius() * scale
            diameter = radius * 2.0
            axis_dir = cylinder.Axis().Direction()
            axis_loc = cylinder.Location()
            
            center = {
                'x': axis_loc.X() * scale,
                'y': axis_loc.Y() * scale,
                'z': axis_loc.Z() * scale
            }
            direction = {
                'x': axis_dir.X(),
                'y': axis_dir.Y(),
                'z': axis_dir.Z()
            }
            
            # Estimate hole depth from face bounds
            u1, u2, v1, v2 = BRepTools.UVBounds_s(face)
            depth = abs(v2 - v1) * scale
            arc_angle = abs(u2 - u1)  # radians
            
            # Distinguish holes from bend radii:
            # - Holes: arc angle close to 2*pi (full cylinder) or pi (half, for through-holes)
            # - Bend radii: arc angle typically pi/2 (90° bend) or less
            # - Fillets: small arc angles
            is_likely_hole = arc_angle > math.pi * 0.8  # >144° arc = likely a hole
            
            # Also filter by size: bend radii in sheet metal are typically = material thickness
            # Holes are typically larger than the bend radius
            # Skip very large cylinders (likely not holes)
            is_reasonable_hole_size = 0.5 < diameter < 50.0
            
            if is_likely_hole and is_reasonable_hole_size:
                cyl_data = {
                    'diameter': round(diameter, 3),
                    'radius': round(radius, 3),
                    'depth': round(depth, 3),
                    'center': center,
                    'direction': direction,
                    'area': round(face_area, 3),
                    'face_center': face_center,
                    'arc_angle_deg': round(math.degrees(arc_angle), 1),
                    'is_hole': True,
                    'face_idx': face_idx
                }
                cylindrical_faces.append(cyl_data)
            else:
                # This is likely a bend radius or fillet — capture the radius
                arc_deg = math.degrees(arc_angle)
                if 30 < arc_deg < 180 and radius > 0.1:  # Reasonable bend arc
                    bend_radii_faces.append({
                        'radius': round(radius, 3),
                        'arc_angle_deg': round(arc_deg, 1),
                        'center': face_center,
                        'face_idx': face_idx
                    })
                logger.debug(f"Bend radius face: r={radius:.2f}mm, arc={arc_deg:.1f}°")
            
        elif surface_type == GeomAbs_Plane:
            plane = adaptor.Plane()
            normal = plane.Axis().Direction()
            
            planar_faces.append({
                'normal': {
                    'x': round(normal.X(), 6),
                    'y': round(normal.Y(), 6),
                    'z': round(normal.Z(), 6)
                },
                'area': round(face_area, 3),
                'center': face_center,
                'face_idx': face_idx
            })
        
        all_face_data.append({
            'type': _surface_type_name(surface_type),
            'area': round(face_area, 3),
            'center': face_center,
            'face_idx': face_idx
        })
        
        explorer.Next()
        face_idx += 1
    
    # Group cylindrical faces into holes (merge faces with same axis/center)
    holes = _group_cylindrical_faces_into_holes(cylindrical_faces)
    logger.info(f"Detected {len(holes)} holes, {len(planar_faces)} planar faces")
    
    # Detect bends from edge analysis
    bends = _detect_bends(solid, planar_faces, scale)
    logger.info(f"Detected {len(bends)} bends")
    
    # Estimate sheet metal thickness
    thickness = _estimate_thickness(planar_faces, dims)
    logger.info(f"Estimated thickness: {thickness:.2f}mm")
    
    # Calculate hole-to-bend distances
    hole_bend_distances = _calc_hole_to_bend_distances(holes, bends)
    
    # Calculate hole-to-edge distances using actual face edges
    hole_edge_distances = _calc_hole_to_face_edge_distances(solid, holes, scale)
    
    # Calculate hole-to-hole distances
    hole_hole_distances = _calc_hole_to_hole_distances(holes)
    
    # Detect flange lengths
    flange_lengths = _detect_flange_lengths(planar_faces, bends, dims)
    
    result = {
        'features_extracted': True,
        'dimensions': dims,
        'volume': round(volume, 2),
        'surface_area': round(surface_area, 2),
        'estimated_min_thickness': round(thickness, 3),
        'holes': holes,
        'bends': bends,
        'bend_radii': _get_unique_bend_radii(bend_radii_faces),
        'planar_faces_count': len(planar_faces),
        'cylindrical_faces_count': len(cylindrical_faces),
        'total_faces': face_idx,
        'hole_to_bend_distances': hole_bend_distances,
        'hole_to_edge_distances': hole_edge_distances,
        'hole_to_hole_distances': hole_hole_distances,
        'flange_lengths': flange_lengths,
        'parsed': True,
        'parser': 'CadQuery/OpenCascade B-Rep'
    }
    
    logger.info(f"Feature extraction complete: {len(holes)} holes, {len(bends)} bends, bend_radii={result['bend_radii']}, thickness={thickness:.2f}mm")
    return result


def _get_unique_bend_radii(bend_radii_faces: List[Dict]) -> List[float]:
    """Get unique bend radii values from detected cylindrical bend faces"""
    if not bend_radii_faces:
        return []
    radii = set()
    for face in bend_radii_faces:
        r = round(face['radius'], 2)
        radii.add(r)
    return sorted(radii)


def _surface_type_name(surface_type) -> str:
    """Convert OCC surface type enum to string"""
    from OCP.GeomAbs import (GeomAbs_Cylinder, GeomAbs_Plane, GeomAbs_Cone,
                              GeomAbs_Torus, GeomAbs_Sphere, GeomAbs_BSplineSurface)
    names = {
        GeomAbs_Plane: 'Plane',
        GeomAbs_Cylinder: 'Cylinder',
        GeomAbs_Cone: 'Cone',
        GeomAbs_Torus: 'Torus',
        GeomAbs_Sphere: 'Sphere',
        GeomAbs_BSplineSurface: 'BSpline',
    }
    return names.get(surface_type, 'Other')


def _group_cylindrical_faces_into_holes(cylindrical_faces: List[Dict]) -> List[Dict]:
    """Group cylindrical faces that belong to the same hole (same axis, same diameter)"""
    if not cylindrical_faces:
        return []
    
    holes = []
    used = set()
    
    for i, face in enumerate(cylindrical_faces):
        if i in used:
            continue
        
        # Start a new hole group
        group = [face]
        used.add(i)
        
        for j, other in enumerate(cylindrical_faces):
            if j in used:
                continue
            # Same diameter (within 0.1mm) and close centers
            if abs(face['diameter'] - other['diameter']) < 0.1:
                dist = math.sqrt(
                    (face['center']['x'] - other['center']['x'])**2 +
                    (face['center']['y'] - other['center']['y'])**2 +
                    (face['center']['z'] - other['center']['z'])**2
                )
                if dist < face['diameter'] * 2:
                    group.append(other)
                    used.add(j)
        
        # Merge group into single hole
        total_depth = sum(f['depth'] for f in group)
        avg_center = {
            'x': np.mean([f['face_center']['x'] for f in group]),
            'y': np.mean([f['face_center']['y'] for f in group]),
            'z': np.mean([f['face_center']['z'] for f in group])
        }
        
        holes.append({
            'diameter': group[0]['diameter'],
            'radius': group[0]['radius'],
            'depth': round(total_depth, 3),
            'center': avg_center,
            'direction': group[0]['direction'],
            'face_count': len(group)
        })
    
    return holes


def _detect_bends(solid, planar_faces: List[Dict], scale: float) -> List[Dict]:
    """Detect bends by finding pairs of planar faces that meet at an angle"""
    bends = []
    
    if len(planar_faces) < 2:
        return bends
    
    for i, face1 in enumerate(planar_faces):
        n1 = np.array([face1['normal']['x'], face1['normal']['y'], face1['normal']['z']])
        
        for face2 in planar_faces[i+1:]:
            n2 = np.array([face2['normal']['x'], face2['normal']['y'], face2['normal']['z']])
            
            # Calculate angle between normals
            dot = np.clip(np.dot(n1, n2), -1.0, 1.0)
            angle_rad = math.acos(abs(dot))
            angle_deg = math.degrees(angle_rad)
            
            # A bend exists when two planar faces meet at a non-zero, non-180 angle
            # Filter: angle between 10° and 170° (skip parallel and near-parallel faces)
            if 10 < angle_deg < 170:
                # Check if faces are close enough to be a bend (not just random angled faces)
                c1 = np.array([face1['center']['x'], face1['center']['y'], face1['center']['z']])
                c2 = np.array([face2['center']['x'], face2['center']['y'], face2['center']['z']])
                dist = np.linalg.norm(c1 - c2)
                
                # Faces should be relatively close for a bend
                max_dim = max(face1['area']**0.5, face2['area']**0.5, 1.0)
                if dist < max_dim * 3:
                    bend_center = ((c1 + c2) / 2).tolist()
                    
                    bends.append({
                        'angle': round(angle_deg, 1),
                        'bend_angle': round(180 - angle_deg, 1),  # Actual bend angle
                        'center': {
                            'x': round(bend_center[0], 2),
                            'y': round(bend_center[1], 2),
                            'z': round(bend_center[2], 2)
                        },
                        'face1_area': face1['area'],
                        'face2_area': face2['area'],
                        'face_distance': round(dist, 2)
                    })
    
    # Deduplicate bends that are very close together
    unique_bends = []
    for bend in bends:
        is_dup = False
        bc = np.array([bend['center']['x'], bend['center']['y'], bend['center']['z']])
        for existing in unique_bends:
            ec = np.array([existing['center']['x'], existing['center']['y'], existing['center']['z']])
            if np.linalg.norm(bc - ec) < 2.0 and abs(bend['angle'] - existing['angle']) < 5:
                is_dup = True
                break
        if not is_dup:
            unique_bends.append(bend)
    
    return unique_bends


def _estimate_thickness(planar_faces: List[Dict], dims: Dict) -> float:
    """Estimate sheet metal thickness from parallel face pairs.
    
    Strategy: Find anti-parallel face pairs (opposite normals) and measure
    the distance between them. The most common small distance is the sheet thickness.
    Filter out very small distances (bend radii internals) and large distances (part dimensions).
    """
    if len(planar_faces) < 2:
        return min(dims.values()) if dims else 0.0
    
    thicknesses = []
    
    # Standard sheet metal gauges in mm for validation
    standard_gauges = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 1.6, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0]
    
    for i, face1 in enumerate(planar_faces):
        n1 = np.array([face1['normal']['x'], face1['normal']['y'], face1['normal']['z']])
        
        for face2 in planar_faces[i+1:]:
            n2 = np.array([face2['normal']['x'], face2['normal']['y'], face2['normal']['z']])
            
            # Check if faces are anti-parallel (opposite normals) OR parallel (same normal)
            # Both cases can indicate sheet thickness
            dot = np.dot(n1, n2)
            if dot < -0.95 or dot > 0.95:  # Relaxed threshold for bent parts
                # Distance between face centers projected onto normal
                c1 = np.array([face1['center']['x'], face1['center']['y'], face1['center']['z']])
                c2 = np.array([face2['center']['x'], face2['center']['y'], face2['center']['z']])
                dist = abs(np.dot(c2 - c1, n1))
                
                # Filter: must be a reasonable sheet metal thickness (0.3mm to 10mm)
                if 0.3 < dist < 10.0:
                    # Weight by face area — larger faces are more likely to be the main sheet surfaces
                    area_weight = min(face1['area'], face2['area'])
                    thicknesses.append((dist, area_weight))
    
    if thicknesses:
        # Sort by area weight (largest faces first) and take the most common thickness
        thicknesses.sort(key=lambda x: -x[1])
        
        # Group similar thicknesses (within 0.15mm)
        groups = {}
        for dist, weight in thicknesses:
            matched = False
            for key in groups:
                if abs(dist - key) < 0.15:
                    groups[key].append((dist, weight))
                    matched = True
                    break
            if not matched:
                groups[dist] = [(dist, weight)]
        
        # Pick the group with the highest total area weight
        best_group = max(groups.values(), key=lambda g: sum(w for _, w in g))
        avg_thickness = np.mean([d for d, _ in best_group])
        
        # Snap to nearest standard gauge if close (within 0.15mm)
        for gauge in standard_gauges:
            if abs(avg_thickness - gauge) < 0.15:
                return gauge
        
        return round(avg_thickness, 2)
    
    return min(dims.values()) if dims else 0.0


def _calc_hole_to_bend_distances(holes: List[Dict], bends: List[Dict]) -> List[Dict]:
    """Calculate distance from each hole edge to nearest bend line.
    Per 930-00172: A min = 2.0T + R, B min = 3T + R
    """
    distances = []
    
    for hole in holes:
        hc = np.array([hole['center']['x'], hole['center']['y'], hole['center']['z']])
        radius = hole['radius']
        
        for bend in bends:
            bc = np.array([bend['center']['x'], bend['center']['y'], bend['center']['z']])
            
            # Distance from hole center to bend center
            center_dist = np.linalg.norm(hc - bc)
            # Distance from hole edge to bend
            edge_dist = center_dist - radius
            
            distances.append({
                'hole_diameter': hole['diameter'],
                'hole_center': hole['center'],
                'bend_center': bend['center'],
                'bend_angle': bend.get('bend_angle', 90),
                'center_to_center': round(center_dist, 2),
                'hole_edge_to_bend': round(edge_dist, 2)
            })
    
    return distances


def _calc_hole_to_face_edge_distances(solid, holes: List[Dict], scale: float) -> List[Dict]:
    """Calculate distance from each hole edge to nearest part edge using OCC topology.
    Measures actual distance from hole circumference to the nearest linear edge of the solid.
    Per 930-00172: C min = 2T
    """
    distances = []
    
    if not holes:
        return distances
    
    try:
        from OCP.TopAbs import TopAbs_EDGE
        from OCP.TopExp import TopExp_Explorer
        from OCP.BRepAdaptor import BRepAdaptor_Curve
        from OCP.GeomAbs import GeomAbs_Line
        from OCP.TopoDS import TopoDS
        from OCP.BRepExtrema import BRepExtrema_DistShapeShape
        from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
        from OCP.gp import gp_Pnt
        
        # Collect all linear edges (part boundaries, not hole edges or bend radii)
        linear_edges = []
        edge_exp = TopExp_Explorer(solid.wrapped, TopAbs_EDGE)
        while edge_exp.More():
            edge = TopoDS.Edge_s(edge_exp.Current())
            try:
                curve = BRepAdaptor_Curve(edge)
                if curve.GetType() == GeomAbs_Line:
                    linear_edges.append(edge)
            except Exception:
                pass
            edge_exp.Next()
        
        logger.info(f"Found {len(linear_edges)} linear edges for edge distance calculation")
        
        for hole in holes:
            hc = hole['center']
            radius = hole['radius']
            
            # Create a point at the hole center
            hole_point = gp_Pnt(hc['x'] / scale, hc['y'] / scale, hc['z'] / scale)
            hole_vertex = BRepBuilderAPI_MakeVertex(hole_point).Shape()
            
            min_edge_dist = float('inf')
            
            for edge in linear_edges:
                try:
                    dist_calc = BRepExtrema_DistShapeShape(hole_vertex, edge)
                    if dist_calc.IsDone() and dist_calc.NbSolution() > 0:
                        center_to_edge = dist_calc.Value() * scale  # Convert to mm
                        edge_to_edge = center_to_edge - radius  # Subtract hole radius
                        if edge_to_edge > 0.01:  # Skip edges that are part of the hole itself
                            min_edge_dist = min(min_edge_dist, edge_to_edge)
                except Exception:
                    continue
            
            if min_edge_dist == float('inf'):
                min_edge_dist = 0
            
            distances.append({
                'hole_diameter': hole['diameter'],
                'hole_center': hole['center'],
                'min_edge_distance': round(min_edge_dist, 2),
                'all_edge_distances': [round(min_edge_dist, 2)]
            })
            
            logger.info(f"Hole d={hole['diameter']}mm: min edge distance = {min_edge_dist:.2f}mm")
    
    except Exception as e:
        logger.warning(f"Face edge distance calculation failed: {e}")
        # Fallback: return empty (will trigger INFO status in analyzer)
    
    return distances


def _calc_hole_to_hole_distances(holes: List[Dict]) -> List[Dict]:
    """Calculate edge-to-edge distance between all hole pairs.
    Per 930-00172: D min = 1.2T
    """
    distances = []
    
    for i, h1 in enumerate(holes):
        c1 = np.array([h1['center']['x'], h1['center']['y'], h1['center']['z']])
        r1 = h1['radius']
        
        for h2 in holes[i+1:]:
            c2 = np.array([h2['center']['x'], h2['center']['y'], h2['center']['z']])
            r2 = h2['radius']
            
            center_dist = np.linalg.norm(c1 - c2)
            edge_dist = center_dist - r1 - r2
            
            distances.append({
                'hole1_diameter': h1['diameter'],
                'hole2_diameter': h2['diameter'],
                'center_to_center': round(center_dist, 2),
                'edge_to_edge': round(max(edge_dist, 0), 2)
            })
    
    return distances


def _detect_flange_lengths(planar_faces: List[Dict], bends: List[Dict], dims: Dict) -> List[float]:
    """Detect flange lengths by finding planar faces adjacent to bends.
    
    A flange is the flat section between a bend and the nearest edge.
    For each planar face near a bend, estimate the flange length as the
    smaller dimension of the face (perpendicular to the bend line).
    
    Per 930-00172: Minimum flange = 1.33T, Preferred = 4T or 6mm
    """
    flange_lengths = []
    
    if not planar_faces or not bends:
        return flange_lengths
    
    # For each bend, find the adjacent planar faces and estimate their flange length
    for bend in bends:
        bc = np.array([bend['center']['x'], bend['center']['y'], bend['center']['z']])
        
        # Find planar faces close to this bend
        for face in planar_faces:
            fc = np.array([face['center']['x'], face['center']['y'], face['center']['z']])
            dist = np.linalg.norm(fc - bc)
            
            # Face should be close to the bend (within a reasonable distance)
            area = face['area']
            if area < 1.0:  # Skip tiny faces
                continue
            
            # Estimate face dimensions from area
            # For a rectangular face, the shorter dimension is the flange length
            # Approximate: if face is roughly rectangular, shorter side = area / longer side
            # Use sqrt(area) as a rough dimension estimate
            face_dim = math.sqrt(area)
            
            # If face is close to bend and relatively small, it's likely a flange
            if dist < face_dim * 2 and area < max(dims.values()) * max(dims.values()) * 0.5:
                # Estimate flange length: for faces near bends, the shorter dimension
                # is typically the flange length
                # Better estimate: use the distance from bend center to the far edge of the face
                # which approximates the flange length
                flange_est = dist  # Distance from bend to face center ≈ half the flange
                
                # Only add reasonable flange lengths (0.5mm to 100mm)
                if 0.5 < flange_est < 100:
                    flange_lengths.append(round(flange_est, 2))
    
    # Deduplicate similar values (within 0.5mm)
    if flange_lengths:
        unique = []
        flange_lengths.sort()
        for fl in flange_lengths:
            if not unique or abs(fl - unique[-1]) > 0.5:
                unique.append(fl)
        return unique
    
    return flange_lengths
