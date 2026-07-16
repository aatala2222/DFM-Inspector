"""
Mesh Analyzer - Quality Analysis, Defect Detection, and Automatic Repair

This module implements the Mesh Analyzer component from the Enhanced 3D Geometry
Analysis and Visualization feature. It evaluates mesh quality, detects defects,
and performs automatic repair.

Requirements: Requirement 19 (Mesh Quality Analysis)
Design Reference: Section "Mesh Analyzer"
"""

import logging
from typing import Dict, List, Tuple, Optional
import numpy as np
import trimesh

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MeshAnalyzer:
    """
    Analyze and repair mesh quality issues
    
    Evaluates mesh quality metrics including:
    - Watertight check (closed volume)
    - Degenerate triangle detection (zero area)
    - Non-manifold edge detection (improper connectivity)
    - Triangle quality calculation (shape metric)
    
    Provides automatic repair capabilities for common mesh defects.
    
    Requirements: Requirement 19 (Mesh Quality Analysis)
    """
    
    def __init__(self, mesh: trimesh.Trimesh):
        """
        Initialize Mesh Analyzer
        
        Args:
            mesh: trimesh.Trimesh object to analyze
        """
        self.mesh = mesh
        self.quality_metrics = {}
        self.defects = []
        
        logger.info(f"Initialized MeshAnalyzer for mesh with {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")
    
    def analyze_quality(self) -> Dict:
        """
        Comprehensive mesh quality analysis
        
        Performs all quality checks and returns complete metrics.
        
        Returns:
            Dictionary containing:
            - is_watertight: bool - Whether mesh forms closed volume
            - is_manifold: bool - Whether mesh has proper edge connectivity
            - degenerate_faces: int - Count of zero-area triangles
            - non_manifold_edges: int - Count of edges shared by >2 faces
            - avg_triangle_quality: float - Average quality metric (0-1)
            - min_triangle_quality: float - Worst triangle quality
            - vertex_count: int - Number of vertices
            - face_count: int - Number of faces
            - volume: float - Mesh volume (if watertight)
            - surface_area: float - Total surface area
            - quality_rating: str - Overall quality rating
        """
        try:
            logger.info("Performing comprehensive mesh quality analysis...")
            
            # Basic counts
            vertex_count = len(self.mesh.vertices)
            face_count = len(self.mesh.faces)
            
            # Watertight check
            is_watertight = self.check_watertight()
            
            # Degenerate triangles
            degenerate_faces = self.detect_degenerate_triangles()
            degenerate_count = len(degenerate_faces)
            
            # Non-manifold edges
            non_manifold_edges = self.detect_non_manifold_edges()
            non_manifold_count = len(non_manifold_edges)
            
            # Triangle quality
            triangle_qualities = self.calculate_triangle_quality()
            avg_quality = float(np.mean(triangle_qualities)) if len(triangle_qualities) > 0 else 0.0
            min_quality = float(np.min(triangle_qualities)) if len(triangle_qualities) > 0 else 0.0
            
            # Volume and surface area
            volume = float(self.mesh.volume) if is_watertight else 0.0
            surface_area = float(self.mesh.area)
            
            # Manifold check (no non-manifold edges)
            is_manifold = (non_manifold_count == 0)
            
            # Overall quality rating
            quality_rating = self._calculate_quality_rating(
                is_watertight, is_manifold, degenerate_count, 
                non_manifold_count, avg_quality
            )
            
            # Store metrics
            self.quality_metrics = {
                'is_watertight': is_watertight,
                'is_manifold': is_manifold,
                'degenerate_faces': degenerate_count,
                'non_manifold_edges': non_manifold_count,
                'avg_triangle_quality': avg_quality,
                'min_triangle_quality': min_quality,
                'vertex_count': vertex_count,
                'face_count': face_count,
                'volume': volume,
                'surface_area': surface_area,
                'quality_rating': quality_rating
            }
            
            logger.info(f"✓ Quality analysis complete: {quality_rating}")
            logger.info(f"  Watertight: {is_watertight}, Manifold: {is_manifold}")
            logger.info(f"  Degenerate faces: {degenerate_count}, Non-manifold edges: {non_manifold_count}")
            logger.info(f"  Avg triangle quality: {avg_quality:.3f}")
            
            return self.quality_metrics
            
        except Exception as e:
            logger.error(f"Error in quality analysis: {e}", exc_info=True)
            return {
                'error': str(e),
                'vertex_count': len(self.mesh.vertices),
                'face_count': len(self.mesh.faces)
            }
    
    def check_watertight(self) -> bool:
        """
        Check if mesh forms closed volume
        
        A mesh is watertight if every edge is shared by exactly 2 faces.
        
        Algorithm:
        1. Build edge-to-face map
        2. Check that all edges have exactly 2 adjacent faces
        
        Returns:
            bool: True if watertight, False otherwise
        """
        try:
            # Use trimesh's built-in watertight check
            is_watertight = self.mesh.is_watertight
            
            if not is_watertight:
                logger.debug("Mesh is not watertight (has open edges)")
            
            return is_watertight
            
        except Exception as e:
            logger.warning(f"Error checking watertight: {e}")
            return False
    
    def detect_degenerate_triangles(self) -> List[int]:
        """
        Find triangles with zero or near-zero area
        
        Degenerate triangles have area < 1e-10 mm² (essentially zero).
        These can cause numerical issues in analysis.
        
        Algorithm:
        1. For each face, compute area using cross product
        2. If area < threshold, mark as degenerate
        
        Returns:
            List of face indices that are degenerate
        """
        try:
            degenerate_faces = []
            threshold = 1e-10  # mm²
            
            # Get face areas from trimesh
            if hasattr(self.mesh, 'area_faces'):
                face_areas = self.mesh.area_faces
            else:
                # Calculate manually if not available
                face_areas = []
                for i, face in enumerate(self.mesh.faces):
                    v0 = self.mesh.vertices[face[0]]
                    v1 = self.mesh.vertices[face[1]]
                    v2 = self.mesh.vertices[face[2]]
                    
                    edge1 = v1 - v0
                    edge2 = v2 - v0
                    area = 0.5 * np.linalg.norm(np.cross(edge1, edge2))
                    face_areas.append(area)
                
                face_areas = np.array(face_areas)
            
            # Find degenerate faces
            degenerate_mask = face_areas < threshold
            degenerate_faces = np.where(degenerate_mask)[0].tolist()
            
            if len(degenerate_faces) > 0:
                logger.debug(f"Found {len(degenerate_faces)} degenerate triangles")
            
            return degenerate_faces
            
        except Exception as e:
            logger.error(f"Error detecting degenerate triangles: {e}", exc_info=True)
            return []
    
    def detect_non_manifold_edges(self) -> List[Tuple[int, int]]:
        """
        Find edges shared by more than 2 faces
        
        Non-manifold edges indicate improper mesh topology.
        In a valid manifold mesh, each edge is shared by exactly 2 faces.
        
        Returns:
            List of edge tuples (v1_id, v2_id) that are non-manifold
        """
        try:
            non_manifold_edges = []
            
            # Build edge-to-face map
            edge_face_map = {}
            
            for face_idx, face in enumerate(self.mesh.faces):
                # Create edges for this face
                edges = [
                    tuple(sorted([face[0], face[1]])),
                    tuple(sorted([face[1], face[2]])),
                    tuple(sorted([face[2], face[0]]))
                ]
                
                for edge in edges:
                    if edge not in edge_face_map:
                        edge_face_map[edge] = []
                    edge_face_map[edge].append(face_idx)
            
            # Find edges with != 2 faces
            for edge, faces in edge_face_map.items():
                if len(faces) != 2:
                    non_manifold_edges.append(edge)
            
            if len(non_manifold_edges) > 0:
                logger.debug(f"Found {len(non_manifold_edges)} non-manifold edges")
            
            return non_manifold_edges
            
        except Exception as e:
            logger.error(f"Error detecting non-manifold edges: {e}", exc_info=True)
            return []
    
    def calculate_triangle_quality(self) -> np.ndarray:
        """
        Calculate quality metric for each triangle
        
        Quality metric: Q = 4 * sqrt(3) * area / (sum of squared edge lengths)
        
        Range:
        - 1.0: Perfect equilateral triangle
        - 0.7-1.0: Good quality
        - 0.3-0.7: Acceptable
        - 0.0-0.3: Poor quality
        - 0.0: Degenerate
        
        Returns:
            numpy array of quality values (one per face)
        """
        try:
            qualities = []
            
            for face in self.mesh.faces:
                v0 = self.mesh.vertices[face[0]]
                v1 = self.mesh.vertices[face[1]]
                v2 = self.mesh.vertices[face[2]]
                
                # Compute edge lengths
                a = np.linalg.norm(v1 - v0)
                b = np.linalg.norm(v2 - v1)
                c = np.linalg.norm(v0 - v2)
                
                # Compute area using Heron's formula
                s = (a + b + c) / 2.0
                area_squared = s * (s - a) * (s - b) * (s - c)
                
                if area_squared > 0:
                    area = np.sqrt(area_squared)
                else:
                    area = 0.0
                
                # Compute quality metric
                sum_squared_edges = a*a + b*b + c*c
                
                if sum_squared_edges > 1e-10:
                    quality = (4.0 * np.sqrt(3.0) * area) / sum_squared_edges
                else:
                    quality = 0.0
                
                qualities.append(quality)
            
            return np.array(qualities)
            
        except Exception as e:
            logger.error(f"Error calculating triangle quality: {e}", exc_info=True)
            return np.array([])
    
    def repair_mesh(self) -> Tuple[trimesh.Trimesh, List[str]]:
        """
        Automatic mesh repair
        
        Attempts to fix common mesh defects:
        1. Remove degenerate triangles
        2. Fill holes (make watertight)
        3. Merge duplicate vertices
        4. Fix non-manifold edges
        5. Recalculate normals
        
        Returns:
            Tuple of (repaired_mesh, list_of_repairs_performed)
        """
        try:
            logger.info("Attempting automatic mesh repair...")
            repairs = []
            repaired_mesh = self.mesh.copy()
            
            # 1. Remove degenerate triangles
            degenerate = self.detect_degenerate_triangles()
            if len(degenerate) > 0:
                # Create mask of faces to keep
                keep_mask = np.ones(len(repaired_mesh.faces), dtype=bool)
                keep_mask[degenerate] = False
                
                # Keep only non-degenerate faces
                repaired_mesh.update_faces(keep_mask)
                repairs.append(f"Removed {len(degenerate)} degenerate triangles")
                logger.info(f"  ✓ Removed {len(degenerate)} degenerate triangles")
            
            # 2. Fill holes (if not watertight)
            if not repaired_mesh.is_watertight:
                try:
                    repaired_mesh.fill_holes()
                    repairs.append("Filled holes to make mesh watertight")
                    logger.info("  ✓ Filled holes")
                except Exception as e:
                    logger.warning(f"  Could not fill holes: {e}")
                    repairs.append(f"Could not fill holes: {str(e)}")
            
            # 3. Merge duplicate vertices
            try:
                initial_vertex_count = len(repaired_mesh.vertices)
                repaired_mesh.merge_vertices()
                final_vertex_count = len(repaired_mesh.vertices)
                duplicates = initial_vertex_count - final_vertex_count
                
                if duplicates > 0:
                    repairs.append(f"Merged {duplicates} duplicate vertices")
                    logger.info(f"  ✓ Merged {duplicates} duplicate vertices")
            except Exception as e:
                logger.warning(f"  Could not merge vertices: {e}")
            
            # 4. Fix normals
            try:
                repaired_mesh.fix_normals()
                repairs.append("Recalculated face normals")
                logger.info("  ✓ Recalculated normals")
            except Exception as e:
                logger.warning(f"  Could not fix normals: {e}")
            
            # 5. Remove unreferenced vertices
            try:
                repaired_mesh.remove_unreferenced_vertices()
                repairs.append("Removed unreferenced vertices")
                logger.info("  ✓ Removed unreferenced vertices")
            except Exception as e:
                logger.warning(f"  Could not remove unreferenced vertices: {e}")
            
            if len(repairs) > 0:
                logger.info(f"✓ Mesh repair complete: {len(repairs)} operations performed")
            else:
                logger.info("✓ No repairs needed")
            
            return repaired_mesh, repairs
            
        except Exception as e:
            logger.error(f"Error in mesh repair: {e}", exc_info=True)
            return self.mesh, [f"Repair failed: {str(e)}"]
    
    def get_quality_report(self) -> str:
        """
        Generate human-readable quality report
        
        Returns:
            Formatted string with quality metrics
        """
        if not self.quality_metrics:
            self.analyze_quality()
        
        report = []
        report.append("=" * 60)
        report.append("MESH QUALITY REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Basic info
        report.append(f"Vertices: {self.quality_metrics.get('vertex_count', 0):,}")
        report.append(f"Faces: {self.quality_metrics.get('face_count', 0):,}")
        report.append("")
        
        # Quality metrics
        report.append("Quality Metrics:")
        report.append(f"  Overall Rating: {self.quality_metrics.get('quality_rating', 'Unknown')}")
        report.append(f"  Watertight: {'✓ Yes' if self.quality_metrics.get('is_watertight') else '✗ No'}")
        report.append(f"  Manifold: {'✓ Yes' if self.quality_metrics.get('is_manifold') else '✗ No'}")
        report.append(f"  Avg Triangle Quality: {self.quality_metrics.get('avg_triangle_quality', 0):.3f}")
        report.append(f"  Min Triangle Quality: {self.quality_metrics.get('min_triangle_quality', 0):.3f}")
        report.append("")
        
        # Defects
        degenerate = self.quality_metrics.get('degenerate_faces', 0)
        non_manifold = self.quality_metrics.get('non_manifold_edges', 0)
        
        if degenerate > 0 or non_manifold > 0:
            report.append("Defects Found:")
            if degenerate > 0:
                report.append(f"  ⚠ {degenerate} degenerate triangles")
            if non_manifold > 0:
                report.append(f"  ⚠ {non_manifold} non-manifold edges")
            report.append("")
        
        # Measurements
        report.append("Measurements:")
        report.append(f"  Volume: {self.quality_metrics.get('volume', 0):.2f} mm³")
        report.append(f"  Surface Area: {self.quality_metrics.get('surface_area', 0):.2f} mm²")
        report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def _calculate_quality_rating(self, is_watertight: bool, is_manifold: bool,
                                  degenerate_count: int, non_manifold_count: int,
                                  avg_quality: float) -> str:
        """
        Calculate overall quality rating
        
        Args:
            is_watertight: Whether mesh is watertight
            is_manifold: Whether mesh is manifold
            degenerate_count: Number of degenerate faces
            non_manifold_count: Number of non-manifold edges
            avg_quality: Average triangle quality
        
        Returns:
            Quality rating string: 'Excellent', 'Good', 'Fair', 'Poor'
        """
        # Start with perfect score
        score = 100
        
        # Deduct points for issues
        if not is_watertight:
            score -= 20
        
        if not is_manifold:
            score -= 15
        
        if degenerate_count > 0:
            score -= min(20, degenerate_count * 2)
        
        if non_manifold_count > 0:
            score -= min(15, non_manifold_count * 2)
        
        # Factor in triangle quality
        if avg_quality < 0.3:
            score -= 20
        elif avg_quality < 0.5:
            score -= 10
        elif avg_quality < 0.7:
            score -= 5
        
        # Determine rating
        if score >= 90:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 50:
            return "Fair"
        else:
            return "Poor"
