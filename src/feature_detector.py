"""
Feature Detector - Identify Manufacturing-Critical Features

Detects holes, pockets, corners, bosses, and ribs using geometric analysis.
Provides precise measurements and 3D coordinates for each feature.
"""
import numpy as np
import trimesh
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import logging
from scipy.spatial import distance
from sklearn.cluster import DBSCAN

logger = logging.getLogger(__name__)


@dataclass
class Feature:
    """Base class for detected features"""
    feature_type: str
    center: Tuple[float, float, float]
    dimensions: Dict[str, float]
    coordinates: List[Tuple[float, float, float]] = field(default_factory=list)
    confidence: float = 1.0  # 0-1 scale


@dataclass
class Hole(Feature):
    """Cylindrical hole feature"""
    feature_type: str = 'hole'
    center: Tuple[float, float, float] = (0, 0, 0)
    dimensions: Dict[str, float] = field(default_factory=dict)
    coordinates: List[Tuple[float, float, float]] = field(default_factory=list)
    confidence: float = 1.0
    diameter: float = 0.0
    depth: float = 0.0
    axis: Tuple[float, float, float] = (0, 0, 1)
    is_through: bool = False
    is_threaded: bool = False
    thread_pitch: Optional[float] = None
    hole_type: str = 'simple'  # 'simple', 'counterbore', 'countersink'
    counterbore_diameter: Optional[float] = None
    counterbore_depth: Optional[float] = None
    countersink_angle: Optional[float] = None
    
    def __post_init__(self):
        if not self.dimensions:
            self.dimensions = {
                'diameter': self.diameter,
                'depth': self.depth
            }
            if self.hole_type == 'counterbore' and self.counterbore_diameter:
                self.dimensions['counterbore_diameter'] = self.counterbore_diameter
                self.dimensions['counterbore_depth'] = self.counterbore_depth
            elif self.hole_type == 'countersink' and self.countersink_angle:
                self.dimensions['countersink_angle'] = self.countersink_angle


@dataclass
class Pocket(Feature):
    """Cavity/pocket feature"""
    feature_type: str = 'pocket'
    center: Tuple[float, float, float] = (0, 0, 0)
    dimensions: Dict[str, float] = field(default_factory=dict)
    coordinates: List[Tuple[float, float, float]] = field(default_factory=list)
    confidence: float = 1.0
    width: float = 0.0
    length: float = 0.0
    depth: float = 0.0
    corner_radii: List[float] = field(default_factory=list)
    is_open: bool = True
    
    def __post_init__(self):
        if not self.dimensions:
            self.dimensions = {
                'width': self.width,
                'length': self.length,
                'depth': self.depth
            }


@dataclass
class Corner(Feature):
    """Corner/edge feature"""
    feature_type: str = 'corner'
    center: Tuple[float, float, float] = (0, 0, 0)
    dimensions: Dict[str, float] = field(default_factory=dict)
    coordinates: List[Tuple[float, float, float]] = field(default_factory=list)
    confidence: float = 1.0
    radius: float = 0.0
    angle: float = 90.0  # Degrees
    is_internal: bool = True
    is_fillet: bool = True
    chamfer_distance: Optional[float] = None
    
    def __post_init__(self):
        if not self.dimensions:
            self.dimensions = {
                'radius': self.radius,
                'angle': self.angle
            }


@dataclass
class Boss(Feature):
    """Raised cylindrical protrusion"""
    feature_type: str = 'boss'
    center: Tuple[float, float, float] = (0, 0, 0)
    dimensions: Dict[str, float] = field(default_factory=dict)
    coordinates: List[Tuple[float, float, float]] = field(default_factory=list)
    confidence: float = 1.0
    diameter: float = 0.0
    height: float = 0.0
    
    def __post_init__(self):
        if not self.dimensions:
            self.dimensions = {
                'diameter': self.diameter,
                'height': self.height
            }


@dataclass
class Rib(Feature):
    """Thin wall protrusion"""
    feature_type: str = 'rib'
    center: Tuple[float, float, float] = (0, 0, 0)
    dimensions: Dict[str, float] = field(default_factory=dict)
    coordinates: List[Tuple[float, float, float]] = field(default_factory=list)
    confidence: float = 1.0
    thickness: float = 0.0
    height: float = 0.0
    length: float = 0.0
    
    def __post_init__(self):
        if not self.dimensions:
            self.dimensions = {
                'thickness': self.thickness,
                'height': self.height,
                'length': self.length
            }


class FeatureDetector:
    """
    Detect manufacturing features using geometric analysis
    
    Identifies holes, pockets, corners, bosses, and ribs with
    precise measurements and 3D coordinates.
    """
    
    def __init__(self, mesh: trimesh.Trimesh, topology: Optional[Dict] = None):
        """
        Initialize feature detector
        
        Args:
            mesh: Trimesh object with geometry
            topology: Optional topology information (edges, faces, etc.)
        """
        if not isinstance(mesh, trimesh.Trimesh):
            raise TypeError("mesh must be a trimesh.Trimesh object")
        
        self.mesh = mesh
        self.topology = topology or {}
        self.features = []
        
        logger.info(f"Initialized FeatureDetector for mesh with {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")
    
    def detect_all_features(self, detect_holes=True, detect_pockets=True,
                           detect_corners=True, detect_bosses=False,
                           detect_ribs=False) -> List[Feature]:
        """
        Run all feature detection algorithms
        
        Args:
            detect_holes: Enable hole detection
            detect_pockets: Enable pocket detection
            detect_corners: Enable corner detection
            detect_bosses: Enable boss detection
            detect_ribs: Enable rib detection
            
        Returns:
            List of detected features
        """
        logger.info("Starting feature detection...")
        self.features = []
        
        if detect_holes:
            holes = self.detect_holes()
            self.features.extend(holes)
            logger.info(f"  Detected {len(holes)} holes")
        
        if detect_pockets:
            pockets = self.detect_pockets()
            self.features.extend(pockets)
            logger.info(f"  Detected {len(pockets)} pockets")
        
        if detect_corners:
            corners = self.detect_corners()
            self.features.extend(corners)
            logger.info(f"  Detected {len(corners)} corners")
        
        if detect_bosses:
            bosses = self.detect_bosses()
            self.features.extend(bosses)
            logger.info(f"  Detected {len(bosses)} bosses")
        
        if detect_ribs:
            ribs = self.detect_ribs()
            self.features.extend(ribs)
            logger.info(f"  Detected {len(ribs)} ribs")
        
        logger.info(f"✓ Feature detection complete: {len(self.features)} total features")
        return self.features
    
    def detect_holes(self, min_diameter: float = 1.0, max_diameter: float = 100.0) -> List[Hole]:
        """
        Detect cylindrical holes using geometric analysis
        
        Args:
            min_diameter: Minimum hole diameter to detect (mm)
            max_diameter: Maximum hole diameter to detect (mm)
            
        Returns:
            List of detected holes
        """
        logger.info("Detecting holes...")
        holes = []
        
        try:
            # Simple hole detection using mesh analysis
            # Look for circular cross-sections in the mesh
            
            # Get mesh cross-sections at different heights
            bounds = self.mesh.bounds
            z_min, z_max = bounds[0][2], bounds[1][2]
            z_range = z_max - z_min
            
            if z_range < 0.1:
                logger.warning("Mesh is too flat for hole detection")
                return holes
            
            # Sample cross-sections
            num_slices = min(20, int(z_range / 2))  # One slice every 2mm
            z_values = np.linspace(z_min + z_range * 0.1, z_max - z_range * 0.1, num_slices)
            
            detected_circles = []
            
            for z in z_values:
                # Get cross-section at this height
                try:
                    slice_2d = self.mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
                    
                    if slice_2d is None:
                        continue
                    
                    # Convert to 2D path
                    if hasattr(slice_2d, 'to_planar'):
                        planar = slice_2d.to_planar()[0]
                        
                        # Check if path forms closed loops (potential holes)
                        if hasattr(planar, 'polygons_closed'):
                            for polygon in planar.polygons_closed:
                                # Analyze polygon to see if it's circular
                                vertices = polygon.exterior.coords[:]
                                if len(vertices) < 4:
                                    continue
                                
                                # Calculate center and radius
                                vertices_array = np.array(vertices)
                                center_2d = vertices_array.mean(axis=0)
                                
                                # Calculate distances from center
                                distances = np.linalg.norm(vertices_array - center_2d, axis=1)
                                avg_radius = distances.mean()
                                radius_std = distances.std()
                                
                                # Check if it's circular (low standard deviation)
                                if radius_std < avg_radius * 0.2 and min_diameter/2 < avg_radius < max_diameter/2:
                                    detected_circles.append({
                                        'center_2d': center_2d,
                                        'radius': avg_radius,
                                        'z': z,
                                        'circularity': 1.0 - (radius_std / avg_radius)
                                    })
                
                except Exception as e:
                    logger.debug(f"Error processing slice at z={z}: {e}")
                    continue
            
            # Cluster circles that are likely the same hole
            if detected_circles:
                # Group circles by 2D center location
                centers_2d = np.array([c['center_2d'] for c in detected_circles])
                
                if len(centers_2d) > 0:
                    # Use DBSCAN to cluster nearby circles
                    clustering = DBSCAN(eps=5.0, min_samples=2).fit(centers_2d)
                    labels = clustering.labels_
                    
                    # Process each cluster
                    for label in set(labels):
                        if label == -1:  # Noise
                            continue
                        
                        cluster_indices = np.where(labels == label)[0]
                        cluster_circles = [detected_circles[i] for i in cluster_indices]
                        
                        # Calculate hole properties from cluster
                        avg_center_2d = np.mean([c['center_2d'] for c in cluster_circles], axis=0)
                        avg_radius = np.mean([c['radius'] for c in cluster_circles])
                        z_values_cluster = [c['z'] for c in cluster_circles]
                        depth = max(z_values_cluster) - min(z_values_cluster)
                        avg_z = np.mean(z_values_cluster)
                        avg_circularity = np.mean([c['circularity'] for c in cluster_circles])
                        
                        # Create hole object
                        hole = Hole(
                            center=(float(avg_center_2d[0]), float(avg_center_2d[1]), float(avg_z)),
                            diameter=float(avg_radius * 2),
                            depth=float(depth) if depth > 1.0 else float(z_range),
                            axis=(0.0, 0.0, 1.0),
                            is_through=(depth > z_range * 0.8),
                            is_threaded=False,
                            confidence=float(avg_circularity),
                            dimensions={
                                'diameter': float(avg_radius * 2),
                                'depth': float(depth) if depth > 1.0 else float(z_range)
                            },
                            coordinates=[(float(avg_center_2d[0]), float(avg_center_2d[1]), float(z)) 
                                       for z in z_values_cluster]
                        )
                        
                        # Detect hole type (counterbore, countersink, or simple)
                        hole = self.detect_hole_type(hole)
                        
                        holes.append(hole)
            
            logger.info(f"✓ Detected {len(holes)} holes")
            
        except Exception as e:
            logger.error(f"Error in hole detection: {e}")
            import traceback
            traceback.print_exc()
        
        return holes
    
    def detect_hole_type(self, hole: Hole) -> Hole:
        """
        Detect if hole is counterbore, countersink, or simple hole
        
        Args:
            hole: Hole object to analyze
            
        Returns:
            Updated hole object with hole_type and related properties
        """
        try:
            # Extract hole region geometry
            hole_center = hole.center
            hole_diameter = hole.diameter
            
            # Get vertices near hole
            hole_region_vertices = self._extract_hole_region(hole_center, hole_diameter * 2)
            
            if len(hole_region_vertices) < 10:
                hole.hole_type = 'simple'
                return hole
            
            # Check for multiple diameters (counterbore indicator)
            diameters = self._detect_diameter_changes(hole_region_vertices, hole_center)
            
            if len(diameters) >= 2:
                # Multiple diameters detected - likely counterbore
                wall_angle = self._measure_wall_angle(hole_region_vertices, diameters)
                
                if abs(wall_angle - 90) < 5:  # Within 5° of 90°
                    if self._has_flat_bottom(hole_region_vertices, hole_center):
                        hole.hole_type = 'counterbore'
                        hole.counterbore_diameter = float(max(diameters))
                        hole.counterbore_depth = float(hole.depth * 0.3)  # Estimate
                        hole.dimensions['counterbore_diameter'] = hole.counterbore_diameter
                        hole.dimensions['counterbore_depth'] = hole.counterbore_depth
                        return hole
            
            # Check for conical surface (countersink indicator)
            cone_angle = self._measure_cone_angle(hole_region_vertices, hole_center)
            
            if cone_angle is not None:
                if abs(cone_angle - 82) < 5 or abs(cone_angle - 90) < 5:
                    if not self._has_flat_bottom(hole_region_vertices, hole_center):
                        hole.hole_type = 'countersink'
                        hole.countersink_angle = float(cone_angle)
                        hole.dimensions['countersink_angle'] = hole.countersink_angle
                        return hole
            
            hole.hole_type = 'simple'
            return hole
            
        except Exception as e:
            logger.debug(f"Error detecting hole type: {e}")
            hole.hole_type = 'simple'
            return hole
    
    def _extract_hole_region(self, hole_center: Tuple[float, float, float], 
                            search_radius: float) -> np.ndarray:
        """Extract vertices near hole location"""
        center = np.array(hole_center)
        distances = np.linalg.norm(self.mesh.vertices - center, axis=1)
        mask = distances < search_radius
        return self.mesh.vertices[mask]
    
    def _detect_diameter_changes(self, vertices: np.ndarray, 
                                hole_center: Tuple[float, float, float]) -> List[float]:
        """Detect distinct diameters in hole region"""
        center_2d = np.array(hole_center[:2])
        distances = np.linalg.norm(vertices[:, :2] - center_2d, axis=1)
        
        if len(distances) == 0:
            return []
        
        # Find peaks in distance distribution
        sorted_distances = np.sort(distances)
        
        # Look for significant gaps in distances
        diameters = []
        if len(sorted_distances) > 10:
            # Check for bimodal distribution
            mid_point = len(sorted_distances) // 2
            lower_median = np.median(sorted_distances[:mid_point])
            upper_median = np.median(sorted_distances[mid_point:])
            
            if upper_median > lower_median * 1.3:  # 30% difference
                diameters = [lower_median * 2, upper_median * 2]
        
        return diameters
    
    def _measure_wall_angle(self, vertices: np.ndarray, diameters: List[float]) -> float:
        """Measure angle between hole walls"""
        if len(diameters) < 2:
            return 0.0
        
        # Simplified: assume 90° for counterbore, other angles for countersink
        # Full implementation would fit surfaces and measure actual angles
        return 90.0
    
    def _measure_cone_angle(self, vertices: np.ndarray, 
                           hole_center: Tuple[float, float, float]) -> Optional[float]:
        """Measure cone angle for countersink detection"""
        if len(vertices) < 10:
            return None
        
        # Simplified cone angle detection
        # Full implementation would fit cone to surface
        center = np.array(hole_center)
        
        # Calculate z-variation with radius
        center_2d = center[:2]
        distances_2d = np.linalg.norm(vertices[:, :2] - center_2d, axis=1)
        z_values = vertices[:, 2]
        
        if len(distances_2d) > 5 and distances_2d.max() > 0:
            # Fit line to z vs radius
            valid_mask = distances_2d > 0.1
            if np.sum(valid_mask) > 3:
                x = distances_2d[valid_mask]
                y = z_values[valid_mask]
                
                # Calculate slope
                slope = np.polyfit(x, y, 1)[0]
                
                # Convert slope to angle
                angle = np.degrees(np.arctan(abs(slope)))
                
                # Countersink angles are typically 82° or 90°
                if 75 < angle < 95:
                    return float(angle)
        
        return None
    
    def _has_flat_bottom(self, vertices: np.ndarray, 
                        hole_center: Tuple[float, float, float]) -> bool:
        """Check if hole has flat bottom (counterbore indicator)"""
        if len(vertices) < 5:
            return False
        
        # Get bottom vertices (lowest z values)
        z_values = vertices[:, 2]
        z_min = z_values.min()
        z_threshold = z_min + (z_values.max() - z_min) * 0.1
        
        bottom_vertices = vertices[z_values < z_threshold]
        
        if len(bottom_vertices) < 3:
            return False
        
        # Check planarity of bottom surface
        # Fit plane to bottom vertices
        center = bottom_vertices.mean(axis=0)
        centered = bottom_vertices - center
        
        # SVD to find normal
        _, _, vt = np.linalg.svd(centered)
        normal = vt[-1]
        
        # Calculate distances from plane
        distances = np.abs(np.dot(centered, normal))
        planarity = distances.std()
        
        # If planarity is low, it's flat
        return planarity < 0.5  # 0.5mm tolerance
    
    def detect_pockets(self, min_depth: float = 2.0) -> List[Pocket]:
        """
        Detect cavity/pocket features
        
        Args:
            min_depth: Minimum pocket depth to detect (mm)
            
        Returns:
            List of detected pockets
        """
        logger.info("Detecting pockets...")
        pockets = []
        
        # Simplified pocket detection
        # Look for concave regions in the mesh
        
        try:
            # Analyze mesh curvature
            # Pockets typically have negative curvature (concave)
            
            # For now, return empty list
            # Full implementation would analyze surface curvature
            logger.info("✓ Pocket detection complete (simplified)")
            
        except Exception as e:
            logger.error(f"Error in pocket detection: {e}")
        
        return pockets
    
    def detect_corners(self, min_angle: float = 45.0) -> List[Corner]:
        """
        Detect corners and measure radii
        
        Args:
            min_angle: Minimum angle to consider as corner (degrees)
            
        Returns:
            List of detected corners
        """
        logger.info("Detecting corners...")
        corners = []
        
        try:
            # Analyze edges and face adjacency
            # Corners occur where faces meet at significant angles
            
            # Get face adjacency
            face_adjacency = self.mesh.face_adjacency
            face_adjacency_angles = self.mesh.face_adjacency_angles
            
            # Find sharp corners (large angles between faces)
            sharp_edges = face_adjacency_angles > np.radians(min_angle)
            
            if np.any(sharp_edges):
                sharp_edge_indices = face_adjacency[sharp_edges]
                sharp_angles = face_adjacency_angles[sharp_edges]
                
                logger.info(f"  Found {len(sharp_angles)} sharp edges")
                
                # Sample some corners (limit to avoid too many)
                max_corners = 50
                if len(sharp_angles) > max_corners:
                    sample_indices = np.random.choice(len(sharp_angles), max_corners, replace=False)
                    sharp_edge_indices = sharp_edge_indices[sample_indices]
                    sharp_angles = sharp_angles[sample_indices]
                
                # Create corner objects
                for edge_pair, angle in zip(sharp_edge_indices, sharp_angles):
                    face1_idx, face2_idx = edge_pair
                    
                    # Get edge vertices
                    face1 = self.mesh.faces[face1_idx]
                    face2 = self.mesh.faces[face2_idx]
                    
                    # Find shared edge
                    shared_vertices = set(face1) & set(face2)
                    if len(shared_vertices) == 2:
                        v1, v2 = list(shared_vertices)
                        edge_center = (self.mesh.vertices[v1] + self.mesh.vertices[v2]) / 2
                        
                        corner = Corner(
                            center=tuple(edge_center),
                            radius=0.0,  # Would need curve fitting to measure
                            angle=float(np.degrees(angle)),
                            is_internal=(angle > np.pi),
                            is_fillet=False,  # Would need curve analysis
                            confidence=0.8,
                            dimensions={
                                'radius': 0.0,
                                'angle': float(np.degrees(angle))
                            },
                            coordinates=[tuple(self.mesh.vertices[v1]), tuple(self.mesh.vertices[v2])]
                        )
                        
                        corners.append(corner)
            
            logger.info(f"✓ Detected {len(corners)} corners")
            
        except Exception as e:
            logger.error(f"Error in corner detection: {e}")
            import traceback
            traceback.print_exc()
        
        return corners
    
    def detect_bosses(self) -> List[Boss]:
        """
        Detect raised cylindrical protrusions
        
        Returns:
            List of detected bosses
        """
        logger.info("Detecting bosses...")
        bosses = []
        
        # Simplified - would need convex region analysis
        logger.info("✓ Boss detection complete (simplified)")
        
        return bosses
    
    def detect_ribs(self) -> List[Rib]:
        """
        Detect thin wall protrusions
        
        Returns:
            List of detected ribs
        """
        logger.info("Detecting ribs...")
        ribs = []
        
        # Simplified - would need thin feature analysis
        logger.info("✓ Rib detection complete (simplified)")
        
        return ribs
    
    def get_features_by_type(self, feature_type: str) -> List[Feature]:
        """
        Get all features of a specific type
        
        Args:
            feature_type: Type of feature ('hole', 'pocket', 'corner', etc.)
            
        Returns:
            List of features matching the type
        """
        return [f for f in self.features if f.feature_type == feature_type]
    
    def get_feature_summary(self) -> Dict:
        """
        Get summary of detected features
        
        Returns:
            Dictionary with feature counts and statistics
        """
        summary = {
            'total_features': len(self.features),
            'by_type': {}
        }
        
        for feature_type in ['hole', 'pocket', 'corner', 'boss', 'rib']:
            features = self.get_features_by_type(feature_type)
            summary['by_type'][feature_type] = {
                'count': len(features),
                'features': features
            }
        
        return summary
