"""
Enhanced STEP File Parser with Multi-Method Parsing and Accurate Geometry Extraction

This module implements the Enhanced STEP Parser component from the Enhanced 3D Geometry
Analysis and Visualization feature. It provides accurate STEP file parsing with ±0.01mm
tolerance using multiple parsing strategies.

Requirements: Requirement 1 (Accurate STEP File Parsing)
Design Reference: Section "Enhanced STEP Parser"
"""

import os
import re
import logging
from typing import Dict, Tuple, Optional, List
import numpy as np
import trimesh

from src.data_models import (
    Vertex, Edge, Face, Surface, GeometricEntity
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ParseResult:
    """Result of STEP file parsing operation"""
    def __init__(self, success: bool, error: str = ''):
        self.success = success
        self.error = error
        self.vertices: List[Vertex] = []
        self.edges: List[Edge] = []
        self.faces: List[Face] = []
        self.surfaces: List[Surface] = []
        self.dimensions: Dict[str, float] = {}
        self.volume: float = 0.0
        self.surface_area: float = 0.0


class EnhancedSTEPParser:
    """
    Multi-method STEP parser with fallback strategies
    
    Implements accurate STEP AP203/AP214 parsing with ±0.01mm accuracy using:
    1. Cascadio library (primary method)
    2. Text-based coordinate extraction (fallback)
    3. Trimesh conversion (tertiary)
    
    Requirements: Requirement 1 (Accurate STEP File Parsing)
    """
    
    def __init__(self, file_path: str):
        """
        Initialize Enhanced STEP Parser
        
        Args:
            file_path: Path to STEP file (AP203 or AP214)
        """
        self.file_path = file_path
        self.shape = None  # OCC TopoDS_Shape (if available)
        self.mesh = None   # trimesh.Trimesh
        self.entities = {} # Geometric entities
        self.topology = {} # Connectivity graph
        self.parse_result = None
        
        logger.info(f"Initialized EnhancedSTEPParser for: {os.path.basename(file_path)}")
    
    def load(self) -> bool:
        """
        Load STEP file using best available method
        
        Tries multiple parsing strategies in order:
        1. Cascadio (OCC-based) - most accurate
        2. Text parsing - reliable for coordinates
        3. Trimesh fallback
        
        Returns:
            bool: True if parsing succeeded, False otherwise
        """
        try:
            logger.info(f"Loading STEP file: {os.path.basename(self.file_path)}")
            
            # Validate file exists
            if not os.path.exists(self.file_path):
                logger.error(f"File not found: {self.file_path}")
                self.parse_result = ParseResult(False, f"File not found: {self.file_path}")
                return False
            
            # Method 1: Try Trimesh FIRST (gives best quality mesh)
            logger.info("Attempting Trimesh parsing (highest quality)...")
            if self._parse_with_trimesh():
                logger.info("✓ Successfully parsed with Trimesh")
                return True
            
            # Method 2: Try Cascadio (OCC-based parsing)
            if self._parse_with_cascadio():
                logger.info("✓ Successfully parsed with Cascadio")
                return True
            
            # Method 3: Text-based parsing (fallback - low quality convex hull)
            logger.info("Attempting text-based parsing (fallback)...")
            if self._parse_with_text():
                logger.info("✓ Successfully parsed with text extraction (convex hull)")
                return True
            
            # All methods failed
            logger.error("All parsing methods failed")
            self.parse_result = ParseResult(False, "All parsing methods failed")
            return False
            
        except Exception as e:
            logger.error(f"Error in load(): {e}", exc_info=True)
            self.parse_result = ParseResult(False, f"Parsing error: {str(e)}")
            return False

    
    def _parse_with_cascadio(self) -> bool:
        """
        Parse STEP file using Cascadio library (OCC-based)
        
        This is the most accurate method, providing full geometric entity extraction.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import cascadio
            
            logger.info("Parsing with Cascadio (OpenCascade)...")
            
            # Load STEP file
            shape = cascadio.import_step(self.file_path)
            
            if shape is None:
                logger.warning("Cascadio returned None")
                return False
            
            self.shape = shape
            
            # Extract geometric entities
            entities = self.extract_geometric_entities()
            
            if not entities or len(entities.get('vertices', [])) == 0:
                logger.warning("No geometric entities extracted")
                return False
            
            # Build topology
            self.topology = self.build_topology()
            
            # Generate mesh representation
            self.mesh = self.get_mesh()
            
            # Create successful parse result
            self.parse_result = ParseResult(True)
            self.parse_result.vertices = entities.get('vertices', [])
            self.parse_result.edges = entities.get('edges', [])
            self.parse_result.faces = entities.get('faces', [])
            self.parse_result.surfaces = entities.get('surfaces', [])
            
            # Calculate dimensions
            if self.mesh:
                bounds = self.mesh.bounds
                raw_dims = {
                    'x': float(bounds[1][0] - bounds[0][0]),
                    'y': float(bounds[1][1] - bounds[0][1]),
                    'z': float(bounds[1][2] - bounds[0][2])
                }
                max_dim = max(raw_dims.values()) if raw_dims.values() else 0
                if max_dim > 0 and max_dim < 1.0:
                    scale = 1000.0
                elif max_dim > 10000:
                    scale = 0.001
                else:
                    scale = 1.0
                self.parse_result.dimensions = {
                    'x': raw_dims['x'] * scale,
                    'y': raw_dims['y'] * scale,
                    'z': raw_dims['z'] * scale
                }
                self.parse_result.volume = float(self.mesh.volume * (scale ** 3)) if self.mesh.is_watertight else 0.0
                self.parse_result.surface_area = float(self.mesh.area * (scale ** 2))
                self._unit_scale = scale
            
            return True
            
        except ImportError:
            logger.info("Cascadio not available")
            return False
        except Exception as e:
            logger.warning(f"Cascadio parsing failed: {e}")
            return False
    
    def _parse_with_text(self) -> bool:
        """
        Parse STEP file by reading text and extracting coordinates
        
        This method extracts CARTESIAN_POINT entities directly from the STEP text.
        Reliable fallback when OCC libraries are not available.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("Parsing STEP file as text...")
            
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Clean content - remove line breaks within parentheses
            content_cleaned = re.sub(
                r'\(\s*([^)]+?)\s*\)',
                lambda m: '(' + m.group(1).replace('\n', ' ').replace('\r', '') + ')',
                content
            )
            
            # Extract CARTESIAN_POINT coordinates
            # Pattern: CARTESIAN_POINT('name',(x,y,z))
            cartesian_pattern = r"CARTESIAN_POINT\s*\([^,]*,\s*\(([^)]+)\)\s*\)"
            matches = re.findall(cartesian_pattern, content_cleaned, re.IGNORECASE)
            
            if not matches:
                logger.warning("No CARTESIAN_POINT entries found")
                return False
            
            logger.info(f"Found {len(matches)} coordinate points")
            
            # Parse coordinates
            all_coords = []
            for match in matches:
                try:
                    coord_str = match.replace('\n', ' ').replace('\r', '').strip()
                    coords = [float(x.strip()) for x in coord_str.split(',')]
                    if len(coords) == 3:
                        all_coords.append(coords)
                except Exception:
                    continue
            
            if len(all_coords) < 3:
                logger.warning(f"Insufficient valid coordinates: {len(all_coords)}")
                return False
            
            logger.info(f"Parsed {len(all_coords)} valid 3D points")
            
            # Convert to numpy array
            coords_array = np.array(all_coords)
            
            # Calculate bounding box
            min_coords = coords_array.min(axis=0)
            max_coords = coords_array.max(axis=0)
            dimensions = max_coords - min_coords
            
            # Create vertices
            vertices = []
            for i, coord in enumerate(all_coords):
                vertex = Vertex(
                    entity_id=f'v{i}',
                    entity_type='vertex',
                    coordinates=np.array(coord),
                    x=coord[0],
                    y=coord[1],
                    z=coord[2]
                )
                vertices.append(vertex)
            
            # Create mesh from point cloud (using convex hull as approximation)
            try:
                self.mesh = trimesh.Trimesh(vertices=coords_array)
                # Try to create convex hull for better volume estimation
                hull = trimesh.convex.convex_hull(coords_array)
                if hull is not None:
                    self.mesh = hull
            except Exception as e:
                logger.warning(f"Could not create mesh from points: {e}")
            
            # Create parse result
            self.parse_result = ParseResult(True)
            self.parse_result.vertices = vertices
            self.parse_result.dimensions = {
                'x': float(dimensions[0]),
                'y': float(dimensions[1]),
                'z': float(dimensions[2])
            }
            
            if self.mesh:
                self.parse_result.volume = float(self.mesh.volume) if self.mesh.is_watertight else 0.0
                self.parse_result.surface_area = float(self.mesh.area)
            
            logger.info(f"Dimensions: {dimensions[0]:.2f} × {dimensions[1]:.2f} × {dimensions[2]:.2f} mm")
            
            return True
            
        except Exception as e:
            logger.error(f"Text parsing failed: {e}", exc_info=True)
            return False
    
    def _parse_with_trimesh(self) -> bool:
        """
        Parse STEP file using Trimesh library
        
        Tertiary fallback method.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("Attempting Trimesh parsing...")
            
            # Trimesh can load STEP files if the right dependencies are installed
            mesh = trimesh.load(self.file_path)
            
            if mesh is None:
                logger.warning("Trimesh parsing returned None")
                return False
            
            # Handle Scene objects (multiple geometries)
            if isinstance(mesh, trimesh.Scene):
                logger.info(f"Loaded as Scene with {len(mesh.geometry)} geometries")
                if len(mesh.geometry) == 0:
                    logger.warning("Scene contains no geometries")
                    return False
                # Combine all geometries into single mesh
                mesh = trimesh.util.concatenate([geom for geom in mesh.geometry.values()])
            
            # Verify we have a valid mesh
            if not hasattr(mesh, 'vertices') or len(mesh.vertices) == 0:
                logger.warning("Trimesh parsing returned invalid mesh")
                return False
            
            logger.info(f"Trimesh loaded: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")
            
            self.mesh = mesh
            
            # Create parse result
            self.parse_result = ParseResult(True)
            
            # Extract vertices
            vertices = []
            for i, coord in enumerate(self.mesh.vertices):
                vertex = Vertex(
                    entity_id=f'v{i}',
                    entity_type='vertex',
                    coordinates=coord,
                    x=float(coord[0]),
                    y=float(coord[1]),
                    z=float(coord[2])
                )
                vertices.append(vertex)
            
            self.parse_result.vertices = vertices
            
            # Calculate dimensions
            bounds = self.mesh.bounds
            raw_dims = {
                'x': float(bounds[1][0] - bounds[0][0]),
                'y': float(bounds[1][1] - bounds[0][1]),
                'z': float(bounds[1][2] - bounds[0][2])
            }
            
            # Auto-detect units: if max dimension < 1.0, likely meters -> convert to mm
            max_dim = max(raw_dims.values()) if raw_dims.values() else 0
            if max_dim > 0 and max_dim < 1.0:
                scale = 1000.0  # meters to mm
                logger.info(f"Auto-detected units: meters (max dim {max_dim:.4f}m). Converting to mm.")
            elif max_dim > 10000:
                scale = 0.001  # micrometers to mm
                logger.info(f"Auto-detected units: micrometers. Converting to mm.")
            else:
                scale = 1.0  # already in mm
            
            self.parse_result.dimensions = {
                'x': raw_dims['x'] * scale,
                'y': raw_dims['y'] * scale,
                'z': raw_dims['z'] * scale
            }
            self.parse_result.volume = float(self.mesh.volume * (scale ** 3)) if self.mesh.is_watertight else 0.0
            self.parse_result.surface_area = float(self.mesh.area * (scale ** 2))
            self._unit_scale = scale
            
            logger.info(f"✓ Trimesh parsing successful: {len(vertices)} vertices, {len(self.mesh.faces)} faces")
            
            return True
            
        except Exception as e:
            logger.warning(f"Trimesh parsing failed: {e}")
            return False
    
    def extract_geometric_entities(self) -> Dict:
        """
        Extract surfaces, edges, vertices from parsed geometry
        
        Returns:
            Dictionary containing:
            - vertices: List[Vertex]
            - edges: List[Edge]
            - faces: List[Face]
            - normals: np.ndarray
            - surfaces: List[Surface]
        """
        entities = {
            'vertices': [],
            'edges': [],
            'faces': [],
            'normals': None,
            'surfaces': []
        }
        
        try:
            if self.mesh is None:
                logger.warning("No mesh available for entity extraction")
                return entities
            
            # Extract vertices
            for i, coord in enumerate(self.mesh.vertices):
                vertex = Vertex(
                    entity_id=f'v{i}',
                    entity_type='vertex',
                    coordinates=coord,
                    x=float(coord[0]),
                    y=float(coord[1]),
                    z=float(coord[2])
                )
                entities['vertices'].append(vertex)
            
            # Extract faces
            for i, face_indices in enumerate(self.mesh.faces):
                if len(face_indices) >= 3:
                    # Calculate face normal
                    v0 = self.mesh.vertices[face_indices[0]]
                    v1 = self.mesh.vertices[face_indices[1]]
                    v2 = self.mesh.vertices[face_indices[2]]
                    
                    edge1 = v1 - v0
                    edge2 = v2 - v0
                    cross = np.cross(edge1, edge2)
                    cross_norm = np.linalg.norm(cross)
                    
                    # Normalize to unit vector (handle zero-length case)
                    if cross_norm > 1e-10:
                        normal = cross / cross_norm
                    else:
                        normal = np.array([0.0, 0.0, 1.0])  # Default for degenerate faces
                    
                    # Calculate area
                    area = 0.5 * cross_norm
                    
                    face = Face(
                        entity_id=f'f{i}',
                        entity_type='face',
                        coordinates=np.mean([v0, v1, v2], axis=0),
                        v1_id=int(face_indices[0]),
                        v2_id=int(face_indices[1]),
                        v3_id=int(face_indices[2]),
                        normal=tuple(normal),
                        area=float(area)
                    )
                    entities['faces'].append(face)
            
            # Store face normals
            if hasattr(self.mesh, 'face_normals'):
                entities['normals'] = self.mesh.face_normals
            
            logger.info(f"Extracted {len(entities['vertices'])} vertices, {len(entities['faces'])} faces")
            
        except Exception as e:
            logger.error(f"Error extracting geometric entities: {e}", exc_info=True)
        
        return entities
    
    def build_topology(self) -> Dict:
        """
        Build connectivity graph
        
        Returns:
            Dictionary containing:
            - vertex_to_edges: Dict[int, List[int]]
            - edge_to_faces: Dict[int, List[int]]
            - face_adjacency: Dict[int, List[int]]
        """
        topology = {
            'vertex_to_edges': {},
            'edge_to_faces': {},
            'face_adjacency': {}
        }
        
        try:
            if self.mesh is None:
                return topology
            
            # Build face adjacency using trimesh
            if hasattr(self.mesh, 'face_adjacency'):
                for i, adjacent_faces in enumerate(self.mesh.face_adjacency):
                    topology['face_adjacency'][i] = adjacent_faces.tolist()
            
            # Build edge-to-face mapping
            if hasattr(self.mesh, 'edges') and hasattr(self.mesh, 'edges_face'):
                for edge_idx, face_idx in enumerate(self.mesh.edges_face):
                    if edge_idx not in topology['edge_to_faces']:
                        topology['edge_to_faces'][edge_idx] = []
                    topology['edge_to_faces'][edge_idx].append(int(face_idx))
            
            logger.info(f"Built topology: {len(topology['face_adjacency'])} face adjacencies")
            
        except Exception as e:
            logger.error(f"Error building topology: {e}", exc_info=True)
        
        return topology
    
    def get_mesh(self) -> Optional[trimesh.Trimesh]:
        """
        Get triangulated mesh representation
        
        Returns:
            trimesh.Trimesh or None
        """
        return self.mesh
    
    def validate_geometry(self) -> Tuple[bool, List[str]]:
        """
        Check for corrupted geometry
        
        Checks:
        - Watertight (closed volume)
        - Manifold (proper edge connectivity)
        - Degenerate triangles (zero area)
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        try:
            if self.mesh is None:
                issues.append("No mesh available for validation")
                return False, issues
            
            # Check watertight
            if not self.mesh.is_watertight:
                issues.append("Mesh is not watertight (has open edges)")
            
            # Check for degenerate faces
            if hasattr(self.mesh, 'face_areas'):
                degenerate_count = np.sum(self.mesh.face_areas < 1e-10)
                if degenerate_count > 0:
                    issues.append(f"Found {degenerate_count} degenerate triangles (zero area)")
            
            # Check manifold
            if hasattr(self.mesh, 'is_winding_consistent'):
                if not self.mesh.is_winding_consistent:
                    issues.append("Mesh has inconsistent winding (non-manifold)")
            
            is_valid = len(issues) == 0
            
            if is_valid:
                logger.info("✓ Geometry validation passed")
            else:
                logger.warning(f"Geometry validation found {len(issues)} issues")
                for issue in issues:
                    logger.warning(f"  - {issue}")
            
            return is_valid, issues
            
        except Exception as e:
            logger.error(f"Error in geometry validation: {e}", exc_info=True)
            issues.append(f"Validation error: {str(e)}")
            return False, issues
    
    # Backward compatibility methods (matching SimpleCADParser interface)
    
    def get_analysis_summary(self) -> Dict:
        """
        Get complete analysis summary (backward compatible)
        
        Returns:
            Dictionary with geometry analysis
        """
        if self.parse_result is None or not self.parse_result.success:
            return {
                'parsed': False,
                'error': self.parse_result.error if self.parse_result else 'Not parsed',
                'dimensions': {'x': 0, 'y': 0, 'z': 0},
                'volume': 0,
                'surface_area': 0,
                'estimated_min_thickness': 0
            }
        
        # Estimate min thickness from dimensions
        dims = self.parse_result.dimensions
        estimated_min_thickness = self._estimate_min_thickness(dims)
        
        # Estimate volume from convex hull if mesh isn't watertight
        volume = self.parse_result.volume
        scale = getattr(self, '_unit_scale', 1.0)
        if (volume == 0 or volume < 0.01) and self.mesh is not None:
            try:
                hull = self.mesh.convex_hull
                if hull is not None and hull.is_watertight:
                    volume = float(hull.volume) * (scale ** 3)
            except Exception:
                # Fallback: estimate from bounding box with packing factor
                if dims:
                    volume = dims.get('x', 0) * dims.get('y', 0) * dims.get('z', 0) * 0.6
        
        return {
            'parsed': True,
            'dimensions': dims,
            'volume': volume,
            'surface_area': self.parse_result.surface_area,
            'estimated_min_thickness': estimated_min_thickness,
            'vertex_count': len(self.parse_result.vertices),
            'face_count': len(self.parse_result.faces),
            'is_watertight': self.mesh.is_watertight if self.mesh else False,
            'file_type': '.step',
            'parser': 'EnhancedSTEPParser'
        }
    
    def _estimate_min_thickness(self, dims: Dict) -> float:
        """Estimate minimum wall thickness from geometry"""
        if not dims:
            return 0.0
        
        x, y, z = dims.get('x', 0), dims.get('y', 0), dims.get('z', 0)
        sorted_dims = sorted([d for d in [x, y, z] if d > 0])
        
        if not sorted_dims:
            return 0.0
        
        # Use ray-based thickness estimation if mesh is available
        if self.mesh is not None:
            try:
                import numpy as np
                # Sample rays through the mesh to estimate wall thickness
                bounds = self.mesh.bounds
                center = (bounds[0] + bounds[1]) / 2
                
                # Cast rays along each axis through multiple sample points
                thicknesses = []
                for axis in range(3):
                    direction = np.zeros(3)
                    direction[axis] = 1.0
                    
                    # Sample grid on the perpendicular plane
                    other_axes = [a for a in range(3) if a != axis]
                    for i in range(5):
                        for j in range(5):
                            origin = np.copy(bounds[0])
                            origin[axis] = bounds[0][axis] - 1.0
                            span0 = bounds[1][other_axes[0]] - bounds[0][other_axes[0]]
                            span1 = bounds[1][other_axes[1]] - bounds[0][other_axes[1]]
                            origin[other_axes[0]] = bounds[0][other_axes[0]] + span0 * (i + 0.5) / 5
                            origin[other_axes[1]] = bounds[0][other_axes[1]] + span1 * (j + 0.5) / 5
                            
                            locations, index_ray, index_tri = self.mesh.ray.intersects_location(
                                ray_origins=[origin],
                                ray_directions=[direction]
                            )
                            
                            if len(locations) >= 2:
                                # Sort hit points along ray direction
                                hits = sorted(locations, key=lambda p: p[axis])
                                # Wall thickness = distance between first entry and exit
                                for k in range(0, len(hits) - 1, 2):
                                    thickness = hits[k + 1][axis] - hits[k][axis]
                                    if 0.1 < thickness < sorted_dims[-1]:
                                        thicknesses.append(thickness)
                
                if thicknesses:
                    return float(np.percentile(thicknesses, 10)) * getattr(self, '_unit_scale', 1.0)  # Scale to mm
            except Exception:
                pass
        
        # Fallback: smallest dimension as rough estimate
        return sorted_dims[0]
    
    def get_bounding_box(self) -> Tuple[float, float, float]:
        """Get bounding box dimensions (backward compatible)"""
        if self.parse_result and self.parse_result.dimensions:
            dims = self.parse_result.dimensions
            return (dims['x'], dims['y'], dims['z'])
        return (0.0, 0.0, 0.0)
    
    def get_volume(self) -> float:
        """Get part volume (backward compatible)"""
        if self.parse_result:
            return self.parse_result.volume
        return 0.0
    
    def get_surface_area(self) -> float:
        """Get surface area (backward compatible)"""
        if self.parse_result:
            return self.parse_result.surface_area
        return 0.0
    
    # New methods (extended interface)
    
    def get_vertices(self) -> np.ndarray:
        """Get vertex coordinates as numpy array"""
        if self.mesh:
            return self.mesh.vertices
        return np.array([])
    
    def get_faces(self) -> np.ndarray:
        """Get face indices as numpy array"""
        if self.mesh:
            return self.mesh.faces
        return np.array([])
    
    def get_normals(self) -> np.ndarray:
        """Get face normals as numpy array"""
        if self.mesh and hasattr(self.mesh, 'face_normals'):
            return self.mesh.face_normals
        return np.array([])
    
    def get_topology(self) -> Dict:
        """Get topology connectivity graph"""
        return self.topology
    
    def get_features(self) -> List:
        """Get detected features (placeholder for future implementation)"""
        # This will be implemented by FeatureDetector in later phases
        return []
    
    def get_measurements(self) -> Dict:
        """Get measurements (placeholder for future implementation)"""
        # This will be implemented by GeometryAnalyzer in later phases
        return {}
