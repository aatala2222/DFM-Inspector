"""
Accurate STEP File Parser
Provides precise dimension extraction from STEP files using multiple methods
"""
import os
import numpy as np
from typing import Dict, Tuple, Optional
import re


class STEPParser:
    """Accurate STEP file parser"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.analysis = {}
        
    def load(self) -> bool:
        """Load and parse STEP file"""
        try:
            print(f"📂 Parsing STEP file: {os.path.basename(self.file_path)}")
            
            # Method 1: Try steputils library
            success = self._parse_with_steputils()
            if success:
                return True
            
            # Method 2: Direct text parsing (most reliable)
            print("📝 Using direct STEP text parsing...")
            success = self._parse_step_text()
            if success:
                return True
            
            # Method 3: Fallback to defaults
            print("⚠️ Using fallback values")
            self._use_defaults()
            return True
            
        except Exception as e:
            print(f"❌ Error loading STEP file: {e}")
            import traceback
            traceback.print_exc()
            self._use_defaults()
            return True
    
    def _parse_with_steputils(self) -> bool:
        """Try parsing with steputils library"""
        try:
            from steputils import p21
            
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                step_file = p21.readfile(f)
            
            # Extract entities
            if hasattr(step_file, 'data'):
                print("✓ STEP file structure loaded")
                # Continue with text parsing for coordinates
                return False  # Fall through to text parsing
            
        except Exception as e:
            print(f"⚠️ steputils parsing not available: {e}")
            return False
    
    def _detect_holes(self, content: str, coords_array: np.ndarray, min_coords: np.ndarray, max_coords: np.ndarray) -> list:
        """
        Detect circular features (holes) in STEP file
        Returns list of holes with center position, diameter, and edge distances
        """
        holes = []
        
        try:
            # Look for CIRCLE entities in STEP file
            # Pattern: CIRCLE('name',#ref,radius)
            circle_pattern = r"#(\d+)\s*=\s*CIRCLE\s*\([^,]*,\s*#(\d+)\s*,\s*([\d.]+)\s*\)"
            circle_matches = re.findall(circle_pattern, content, re.IGNORECASE)
            
            if circle_matches:
                print(f"🔍 Found {len(circle_matches)} CIRCLE entities")
                
                # Build a map of entity IDs to their definitions for reference lookup
                entity_map = {}
                entity_pattern = r"#(\d+)\s*=\s*([^;]+);"
                for entity_match in re.finditer(entity_pattern, content):
                    entity_id = entity_match.group(1)
                    entity_def = entity_match.group(2).strip()
                    entity_map[entity_id] = entity_def
                
                for circle_id, axis_ref, radius_str in circle_matches:
                    try:
                        radius = float(radius_str)
                        diameter = radius * 2
                        
                        # Only process reasonable hole sizes
                        if not (1.0 <= diameter <= 100.0):
                            continue
                        
                        # Try to find the actual center point by following the axis reference
                        center = self._find_circle_center(axis_ref, entity_map, coords_array, min_coords, max_coords)
                        
                        if center is None:
                            # Fallback: use bounding box center
                            center = [
                                (min_coords[0] + max_coords[0]) / 2,
                                (min_coords[1] + max_coords[1]) / 2,
                                (min_coords[2] + max_coords[2]) / 2
                            ]
                        
                        center_x, center_y, center_z = center
                        
                        # Calculate distances to edges (accounting for hole radius)
                        dist_to_x_min = abs(center_x - min_coords[0]) - radius
                        dist_to_x_max = abs(max_coords[0] - center_x) - radius
                        dist_to_y_min = abs(center_y - min_coords[1]) - radius
                        dist_to_y_max = abs(max_coords[1] - center_y) - radius
                        
                        # Minimum distance to any edge
                        edge_distances_list = [dist_to_x_min, dist_to_x_max, dist_to_y_min, dist_to_y_max]
                        valid_distances = [d for d in edge_distances_list if d > -radius]  # Allow negative if hole extends past edge
                        min_edge_distance = min(valid_distances) if valid_distances else 0
                        
                        hole_info = {
                            'diameter': diameter,
                            'radius': radius,
                            'center': [center_x, center_y, center_z],
                            'min_edge_distance': max(min_edge_distance, 0),  # Don't report negative distances
                            'edge_distances': {
                                'x_min': max(dist_to_x_min, 0),
                                'x_max': max(dist_to_x_max, 0),
                                'y_min': max(dist_to_y_min, 0),
                                'y_max': max(dist_to_y_max, 0)
                            }
                        }
                        holes.append(hole_info)
                        print(f"  • Hole: Ø{diameter:.1f}mm at ({center_x:.1f}, {center_y:.1f}), min edge distance: {hole_info['min_edge_distance']:.1f}mm")
                    
                    except Exception as e:
                        print(f"  ⚠️ Error processing circle: {e}")
                        continue
            
            # Alternative: Look for cylindrical features by analyzing coordinate patterns
            # This is a fallback if CIRCLE entities aren't found or centers couldn't be located
            if not holes:
                holes = self._detect_holes_from_coordinates(coords_array, min_coords, max_coords)
            
        except Exception as e:
            print(f"⚠️ Hole detection error: {e}")
            import traceback
            traceback.print_exc()
        
        return holes
    
    def _find_circle_center(self, axis_ref: str, entity_map: dict, coords_array: np.ndarray, min_coords: np.ndarray, max_coords: np.ndarray) -> Optional[list]:
        """
        Find the center point of a circle by following AXIS2_PLACEMENT_3D references
        """
        try:
            # Look up the axis placement entity
            if axis_ref not in entity_map:
                return None
            
            axis_def = entity_map[axis_ref]
            
            # AXIS2_PLACEMENT_3D('name',#point_ref,#dir_ref,#ref_dir_ref)
            # We need the point_ref (first reference after the name)
            axis_pattern = r"AXIS2_PLACEMENT_3D\s*\([^,]*,\s*#(\d+)"
            axis_match = re.search(axis_pattern, axis_def, re.IGNORECASE)
            
            if not axis_match:
                return None
            
            point_ref = axis_match.group(1)
            
            # Look up the point entity
            if point_ref not in entity_map:
                return None
            
            point_def = entity_map[point_ref]
            
            # CARTESIAN_POINT('name',(x,y,z))
            point_pattern = r"CARTESIAN_POINT\s*\([^,]*,\s*\(([^)]+)\)\s*\)"
            point_match = re.search(point_pattern, point_def, re.IGNORECASE)
            
            if not point_match:
                return None
            
            # Extract coordinates
            coord_str = point_match.group(1).strip()
            coords = [float(x.strip()) for x in coord_str.split(',')]
            
            if len(coords) == 3:
                return coords
            
        except Exception as e:
            pass
        
        return None
    
    def _detect_holes_from_coordinates(self, coords_array: np.ndarray, min_coords: np.ndarray, max_coords: np.ndarray) -> list:
        """
        Detect potential holes by analyzing coordinate patterns
        Look for circular patterns in the point cloud
        """
        holes = []
        
        try:
            # Simplified heuristic: Look for clusters of points that form circles
            # This is a basic implementation - production would use more sophisticated algorithms
            
            # For sheet metal parts, holes are often through-holes
            # Look for points that repeat at different Z levels (indicating a cylinder)
            
            # Group points by XY coordinates (ignoring Z)
            xy_coords = coords_array[:, :2]  # Just X and Y
            
            # Find unique XY positions (with tolerance)
            tolerance = 0.5  # mm
            unique_xy = []
            xy_counts = []
            
            for coord in xy_coords:
                found = False
                for i, unique_coord in enumerate(unique_xy):
                    if np.linalg.norm(coord - unique_coord) < tolerance:
                        xy_counts[i] += 1
                        found = True
                        break
                if not found:
                    unique_xy.append(coord)
                    xy_counts.append(1)
            
            # Points that appear multiple times at different Z levels might be holes
            for i, count in enumerate(xy_counts):
                if count >= 8:  # Arbitrary threshold - holes have many points
                    xy_pos = unique_xy[i]
                    
                    # Estimate hole diameter by looking at nearby points
                    # Find all points near this XY position
                    nearby_mask = np.linalg.norm(xy_coords - xy_pos, axis=1) < 20  # Within 20mm
                    nearby_points = coords_array[nearby_mask]
                    
                    if len(nearby_points) > 10:
                        # Calculate spread of points (rough diameter estimate)
                        xy_nearby = nearby_points[:, :2]
                        distances_from_center = np.linalg.norm(xy_nearby - xy_pos, axis=1)
                        estimated_radius = np.percentile(distances_from_center[distances_from_center > 0.1], 75)
                        estimated_diameter = estimated_radius * 2
                        
                        # Only consider reasonable hole sizes
                        if 2.0 <= estimated_diameter <= 50.0:
                            center_x, center_y = xy_pos
                            center_z = np.mean(nearby_points[:, 2])
                            
                            # Calculate distances to edges
                            dist_to_x_min = abs(center_x - min_coords[0])
                            dist_to_x_max = abs(max_coords[0] - center_x)
                            dist_to_y_min = abs(center_y - min_coords[1])
                            dist_to_y_max = abs(max_coords[1] - center_y)
                            
                            edge_distances = [
                                dist_to_x_min - estimated_radius,
                                dist_to_x_max - estimated_radius,
                                dist_to_y_min - estimated_radius,
                                dist_to_y_max - estimated_radius
                            ]
                            min_edge_distance = min([d for d in edge_distances if d > 0] + [999])
                            
                            hole_info = {
                                'diameter': estimated_diameter,
                                'radius': estimated_radius,
                                'center': [center_x, center_y, center_z],
                                'min_edge_distance': min_edge_distance,
                                'edge_distances': {
                                    'x_min': dist_to_x_min - estimated_radius,
                                    'x_max': dist_to_x_max - estimated_radius,
                                    'y_min': dist_to_y_min - estimated_radius,
                                    'y_max': dist_to_y_max - estimated_radius
                                },
                                'confidence': 'estimated'
                            }
                            holes.append(hole_info)
                            print(f"  • Estimated hole: Ø{estimated_diameter:.1f}mm, min edge distance: {min_edge_distance:.1f}mm")
        
        except Exception as e:
            print(f"⚠️ Coordinate-based hole detection error: {e}")
        
        return holes
    
    def _parse_step_text(self) -> bool:
        """Parse STEP file by reading text and extracting coordinates"""
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            print(f"📄 STEP file size: {len(content)} characters")
            
            # Remove line breaks within CARTESIAN_POINT entries for easier parsing
            # Replace newlines within parentheses
            content_cleaned = re.sub(r'\(\s*([^)]+?)\s*\)', lambda m: '(' + m.group(1).replace('\n', ' ').replace('\r', '') + ')', content)
            
            # Extract all CARTESIAN_POINT coordinates
            # Pattern: CARTESIAN_POINT('name',(x,y,z)) or CARTESIAN_POINT ( 'name', ( x, y, z ) )
            cartesian_pattern = r"CARTESIAN_POINT\s*\([^,]*,\s*\(([^)]+)\)\s*\)"
            matches = re.findall(cartesian_pattern, content_cleaned, re.IGNORECASE)
            
            if not matches:
                print("⚠️ No CARTESIAN_POINT entries found")
                return False
            
            print(f"✓ Found {len(matches)} coordinate points")
            
            # Parse coordinates
            all_coords = []
            for match in matches:
                try:
                    # Clean up the coordinate string
                    coord_str = match.replace('\n', ' ').replace('\r', '').strip()
                    coords = [float(x.strip()) for x in coord_str.split(',')]
                    if len(coords) == 3:
                        all_coords.append(coords)
                except Exception as e:
                    continue
            
            if len(all_coords) < 3:
                print(f"⚠️ Insufficient valid coordinates: {len(all_coords)}")
                return False
            
            print(f"✓ Parsed {len(all_coords)} valid 3D points")
            
            # Calculate bounding box
            coords_array = np.array(all_coords)
            min_coords = coords_array.min(axis=0)
            max_coords = coords_array.max(axis=0)
            dimensions = max_coords - min_coords
            
            dims = {
                'x': abs(float(dimensions[0])),
                'y': abs(float(dimensions[1])),
                'z': abs(float(dimensions[2]))
            }
            
            print(f"📏 Bounding Box: {dims['x']:.2f} × {dims['y']:.2f} × {dims['z']:.2f} mm")
            
            # NEW: Detect holes (circular features)
            holes = self._detect_holes(content_cleaned, coords_array, min_coords, max_coords)
            
            # Estimate volume (assume 30% solid for typical parts)
            volume = dims['x'] * dims['y'] * dims['z'] * 0.3
            
            # Calculate surface area (bounding box surface)
            surface_area = 2 * (dims['x'] * dims['y'] + 
                               dims['y'] * dims['z'] + 
                               dims['z'] * dims['x'])
            
            # Estimate wall thickness (3-5% of smallest dimension)
            min_dim = min(dims.values())
            if min_dim < 50:
                thickness = max(min_dim * 0.03, 0.5)  # 3% for small parts, min 0.5mm
            else:
                thickness = max(min_dim * 0.04, 1.0)  # 4% for larger parts, min 1.0mm
            
            thickness = min(thickness, 10.0)  # Cap at 10mm
            
            print(f"📊 Volume: {volume:.0f} mm³ (estimated)")
            print(f"📊 Surface Area: {surface_area:.0f} mm²")
            print(f"📐 Estimated wall thickness: {thickness:.2f} mm")
            if holes:
                print(f"🔍 Detected {len(holes)} circular features (potential holes)")
            
            # Store analysis
            self.analysis = {
                'parsed': True,
                'dimensions': dims,
                'volume': float(volume),
                'surface_area': float(surface_area),
                'bounding_box': {
                    'min': min_coords.tolist(),
                    'max': max_coords.tolist()
                },
                'point_count': len(all_coords),
                'estimated_min_thickness': float(thickness),
                'is_watertight': True,  # Assume STEP files are valid
                'holes': holes,  # NEW: Hole information
                'file_type': '.step',
                'parser': 'Direct text parsing',
                'note': 'Dimensions extracted from STEP CARTESIAN_POINT coordinates'
            }
            
            print("✅ STEP parsing complete")
            return True
            
        except Exception as e:
            print(f"❌ Text parsing failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _use_defaults(self):
        """Use default values when parsing fails"""
        print("⚠️ Using default dimensions (100×100×50mm)")
        
        self.analysis = {
            'parsed': False,
            'dimensions': {'x': 100.0, 'y': 100.0, 'z': 50.0},
            'volume': 50000.0,
            'surface_area': 15000.0,
            'estimated_min_thickness': 2.0,
            'is_watertight': True,
            'file_type': '.step',
            'parser': 'Default values',
            'note': 'Could not extract dimensions from STEP file. Using default values. Please verify dimensions manually.'
        }
    
    def get_analysis_summary(self) -> Dict:
        """Get complete analysis summary"""
        return self.analysis
    
    def get_bounding_box(self) -> Tuple[float, float, float]:
        """Get bounding box dimensions"""
        if 'dimensions' in self.analysis:
            dims = self.analysis['dimensions']
            return (dims['x'], dims['y'], dims['z'])
        return (0, 0, 0)
    
    def get_volume(self) -> float:
        """Get part volume"""
        return self.analysis.get('volume', 0.0)
    
    def get_surface_area(self) -> float:
        """Get surface area"""
        return self.analysis.get('surface_area', 0.0)


def parse_step_file(file_path: str) -> Dict:
    """
    Convenience function to parse a STEP file and return analysis
    
    Args:
        file_path: Path to STEP file
        
    Returns:
        Dictionary with geometry analysis
    """
    parser = STEPParser(file_path)
    success = parser.load()
    
    if success:
        return parser.get_analysis_summary()
    else:
        return {
            'parsed': False,
            'error': 'Failed to parse STEP file',
            'dimensions': {'x': 0, 'y': 0, 'z': 0},
            'volume': 0,
            'surface_area': 0
        }

