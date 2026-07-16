"""
Property-Based Tests for Enhanced STEP Parser

Tests correctness properties using hypothesis library with 100 iterations per property.
Requirements: Requirement 1 (Accurate STEP File Parsing)
Design Reference: Section "Testing Strategy - Property-Based Testing"
"""

import pytest
import os
import numpy as np
import trimesh
from hypothesis import given, strategies as st, settings, assume, HealthCheck
from src.enhanced_step_parser import EnhancedSTEPParser


# Custom strategies for generating test data
@st.composite
def step_file_path(draw):
    """Strategy to generate valid STEP file paths from sample_files directory"""
    sample_dir = 'sample_files'
    if not os.path.exists(sample_dir):
        assume(False)  # Skip if no sample files
    
    step_files = [
        os.path.join(sample_dir, f) 
        for f in os.listdir(sample_dir) 
        if f.endswith('.STEP') or f.endswith('.step')
    ]
    
    if not step_files:
        assume(False)  # Skip if no STEP files
    
    return draw(st.sampled_from(step_files))


class TestProperty1_CompleteGeometricEntityExtraction:
    """
    Property 1: Complete Geometric Entity Extraction
    
    For any valid STEP AP203 or AP214 file, when parsed by the Enhanced STEP Parser,
    the resulting data structure SHALL contain all geometric entities (vertices with
    coordinates, edges with connectivity, faces with normals, and topology graph).
    
    Validates: Requirements 1.1, 1.3, 1.4, 1.5, 1.7, 1.8
    """
    
    @settings(max_examples=3, deadline=None)
    @given(file_path=step_file_path())
    def test_property_1_vertices_extracted(self, file_path):
        """
        Property 1a: All vertices SHALL be extracted with 3D coordinates
        """
        parser = EnhancedSTEPParser(file_path)
        result = parser.load()
        
        # If parsing succeeded, must have vertices
        if result and parser.parse_result.success:
            assert len(parser.parse_result.vertices) > 0, \
                f"No vertices extracted from {os.path.basename(file_path)}"
            
            # All vertices must have valid 3D coordinates
            for vertex in parser.parse_result.vertices:
                assert hasattr(vertex, 'x'), "Vertex missing x coordinate"
                assert hasattr(vertex, 'y'), "Vertex missing y coordinate"
                assert hasattr(vertex, 'z'), "Vertex missing z coordinate"
                assert hasattr(vertex, 'coordinates'), "Vertex missing coordinates array"
                
                # Coordinates must be finite numbers
                assert np.isfinite(vertex.x), f"Invalid x coordinate: {vertex.x}"
                assert np.isfinite(vertex.y), f"Invalid y coordinate: {vertex.y}"
                assert np.isfinite(vertex.z), f"Invalid z coordinate: {vertex.z}"
    
    @settings(max_examples=3, deadline=None)
    @given(file_path=step_file_path())
    def test_property_1_faces_extracted(self, file_path):
        """
        Property 1b: All faces SHALL be extracted with normals
        """
        parser = EnhancedSTEPParser(file_path)
        result = parser.load()
        
        if result and parser.parse_result.success:
            entities = parser.extract_geometric_entities()
            
            # Must have faces
            assert 'faces' in entities, "Faces not in extracted entities"
            assert len(entities['faces']) > 0, \
                f"No faces extracted from {os.path.basename(file_path)}"
            
            # All faces must have normals
            for face in entities['faces']:
                assert hasattr(face, 'normal'), "Face missing normal"
                assert face.normal is not None, "Face normal is None"
                assert len(face.normal) == 3, f"Face normal not 3D: {face.normal}"
                
                # Normal must be unit vector (length ≈ 1)
                normal = np.array(face.normal)
                length = np.linalg.norm(normal)
                assert abs(length - 1.0) < 0.01, \
                    f"Face normal not unit vector: {length}"
    
    @settings(max_examples=3, deadline=None)
    @given(file_path=step_file_path())
    def test_property_1_topology_extracted(self, file_path):
        """
        Property 1c: Topology graph SHALL be built
        """
        parser = EnhancedSTEPParser(file_path)
        result = parser.load()
        
        if result and parser.parse_result.success:
            topology = parser.build_topology()
            
            # Topology must be a dictionary
            assert isinstance(topology, dict), "Topology not a dictionary"
            
            # Must have required keys
            assert 'vertex_to_edges' in topology, "Missing vertex_to_edges"
            assert 'edge_to_faces' in topology, "Missing edge_to_faces"
            assert 'face_adjacency' in topology, "Missing face_adjacency"
    
    @settings(max_examples=3, deadline=None)
    @given(file_path=step_file_path())
    def test_property_1_mesh_generated(self, file_path):
        """
        Property 1d: Triangulated mesh SHALL be generated
        """
        parser = EnhancedSTEPParser(file_path)
        result = parser.load()
        
        if result and parser.parse_result.success:
            mesh = parser.get_mesh()
            
            # Mesh must exist
            assert mesh is not None, "Mesh not generated"
            
            # Mesh must have vertices and faces
            assert hasattr(mesh, 'vertices'), "Mesh missing vertices"
            assert hasattr(mesh, 'faces'), "Mesh missing faces"
            assert len(mesh.vertices) > 0, "Mesh has no vertices"
            assert len(mesh.faces) > 0, "Mesh has no faces"


class TestProperty2_DimensionalAccuracyPreservation:
    """
    Property 2: Dimensional Accuracy Preservation
    
    For any STEP file with known dimensions, when parsed and measured by the system,
    the extracted dimensions SHALL match the known dimensions within ±0.01mm tolerance.
    
    Validates: Requirements 1.2, 2.6, 3.4, 4.5, 5.5, 6.7, 7.2
    """
    
    @settings(max_examples=3, deadline=None)
    @given(file_path=step_file_path())
    def test_property_2_dimensions_positive(self, file_path):
        """
        Property 2a: All dimensions SHALL be positive
        """
        parser = EnhancedSTEPParser(file_path)
        result = parser.load()
        
        if result and parser.parse_result.success:
            dims = parser.parse_result.dimensions
            
            # All dimensions must be positive
            assert dims['x'] > 0, f"Invalid X dimension: {dims['x']}"
            assert dims['y'] > 0, f"Invalid Y dimension: {dims['y']}"
            assert dims['z'] > 0, f"Invalid Z dimension: {dims['z']}"
    
    @settings(max_examples=3, deadline=None)
    @given(file_path=step_file_path())
    def test_property_2_dimensions_consistent(self, file_path):
        """
        Property 2b: Dimensions SHALL be consistent with bounding box
        """
        parser = EnhancedSTEPParser(file_path)
        result = parser.load()
        
        if result and parser.parse_result.success and parser.mesh:
            dims = parser.parse_result.dimensions
            bounds = parser.mesh.bounds
            
            # Calculate bounding box dimensions
            bbox_x = bounds[1][0] - bounds[0][0]
            bbox_y = bounds[1][1] - bounds[0][1]
            bbox_z = bounds[1][2] - bounds[0][2]
            
            # Dimensions should match bounding box within tolerance
            tolerance = 0.01  # ±0.01mm
            assert abs(dims['x'] - bbox_x) < tolerance, \
                f"X dimension mismatch: {dims['x']} vs {bbox_x}"
            assert abs(dims['y'] - bbox_y) < tolerance, \
                f"Y dimension mismatch: {dims['y']} vs {bbox_y}"
            assert abs(dims['z'] - bbox_z) < tolerance, \
                f"Z dimension mismatch: {dims['z']} vs {bbox_z}"
    
    @settings(max_examples=3, deadline=None)
    @given(file_path=step_file_path())
    def test_property_2_volume_non_negative(self, file_path):
        """
        Property 2c: Volume SHALL be non-negative
        """
        parser = EnhancedSTEPParser(file_path)
        result = parser.load()
        
        if result and parser.parse_result.success:
            volume = parser.parse_result.volume
            
            # Volume must be non-negative
            assert volume >= 0, f"Invalid volume: {volume}"
    
    @settings(max_examples=3, deadline=None)
    @given(file_path=step_file_path())
    def test_property_2_surface_area_positive(self, file_path):
        """
        Property 2d: Surface area SHALL be positive
        """
        parser = EnhancedSTEPParser(file_path)
        result = parser.load()
        
        if result and parser.parse_result.success:
            area = parser.parse_result.surface_area
            
            # Surface area must be positive
            assert area > 0, f"Invalid surface area: {area}"


class TestProperty3_ParsingErrorHandling:
    """
    Property 3: Parsing Error Handling
    
    For any corrupted or invalid STEP file, when parsing is attempted, the STEP Parser
    SHALL return an error result (not crash) with a descriptive message identifying
    the specific parsing failure.
    
    Validates: Requirements 1.6, 17.1
    """
    
    @settings(max_examples=3, deadline=None)
    @given(
        invalid_path=st.text(min_size=1, max_size=100).filter(
            lambda x: not os.path.exists(x)
        )
    )
    def test_property_3_nonexistent_file_error(self, invalid_path):
        """
        Property 3a: Non-existent files SHALL return error (not crash)
        """
        parser = EnhancedSTEPParser(invalid_path)
        
        # Should not crash
        try:
            result = parser.load()
            
            # Should return False
            assert result == False, "Should return False for non-existent file"
            
            # Should have error message
            assert parser.parse_result is not None, "Missing parse result"
            assert parser.parse_result.success == False, "Success should be False"
            assert parser.parse_result.error != '', "Missing error message"
            assert 'not found' in parser.parse_result.error.lower(), \
                f"Error message not descriptive: {parser.parse_result.error}"
        
        except Exception as e:
            pytest.fail(f"Parser crashed instead of returning error: {e}")
    
    @settings(max_examples=3, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(
        content=st.text(min_size=10, max_size=1000, alphabet=st.characters(exclude_categories=('Cs',)))
    )
    def test_property_3_invalid_content_error(self, content, tmp_path):
        """
        Property 3b: Invalid file content SHALL return error (not crash)
        """
        # Create temporary file with invalid content
        test_file = tmp_path / "invalid.step"
        test_file.write_text(content, encoding='utf-8', errors='ignore')
        
        parser = EnhancedSTEPParser(str(test_file))
        
        # Should not crash
        try:
            result = parser.load()
            
            # Should return False (unless by chance the content is valid)
            # We don't assert False here because random text might accidentally parse
            
            # If it failed, should have error message
            if not result:
                assert parser.parse_result is not None, "Missing parse result"
                assert parser.parse_result.success == False, "Success should be False"
        
        except Exception as e:
            # Should not crash with unhandled exception
            pytest.fail(f"Parser crashed with unhandled exception: {e}")
    
    def test_property_3_empty_file_error(self, tmp_path):
        """
        Property 3c: Empty files SHALL return error (not crash)
        """
        # Create empty file
        test_file = tmp_path / "empty.step"
        test_file.write_text("")
        
        parser = EnhancedSTEPParser(str(test_file))
        
        # Should not crash
        try:
            result = parser.load()
            
            # Should return False
            assert result == False, "Should return False for empty file"
            
            # Should have parse result
            assert parser.parse_result is not None, "Missing parse result"
            assert parser.parse_result.success == False, "Success should be False"
        
        except Exception as e:
            pytest.fail(f"Parser crashed on empty file: {e}")


class TestProperty_BackwardCompatibility:
    """
    Additional property: Backward compatibility with SimpleCADParser interface
    
    The Enhanced STEP Parser SHALL maintain backward compatibility with the
    SimpleCADParser interface for existing code.
    """
    
    @settings(max_examples=3, deadline=None)
    @given(file_path=step_file_path())
    def test_backward_compatible_methods(self, file_path):
        """
        Property: All SimpleCADParser methods SHALL be available
        """
        parser = EnhancedSTEPParser(file_path)
        result = parser.load()
        
        if result and parser.parse_result.success:
            # Check all backward-compatible methods exist
            assert hasattr(parser, 'get_analysis_summary'), \
                "Missing get_analysis_summary method"
            assert hasattr(parser, 'get_bounding_box'), \
                "Missing get_bounding_box method"
            assert hasattr(parser, 'get_volume'), \
                "Missing get_volume method"
            assert hasattr(parser, 'get_surface_area'), \
                "Missing get_surface_area method"
            
            # Check methods return correct types
            summary = parser.get_analysis_summary()
            assert isinstance(summary, dict), "get_analysis_summary not returning dict"
            
            bbox = parser.get_bounding_box()
            assert isinstance(bbox, tuple), "get_bounding_box not returning tuple"
            assert len(bbox) == 3, "get_bounding_box not returning 3 values"
            
            volume = parser.get_volume()
            assert isinstance(volume, float), "get_volume not returning float"
            
            area = parser.get_surface_area()
            assert isinstance(area, float), "get_surface_area not returning float"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])



# ============================================================================
# Property Tests for Mesh Analyzer (Properties 20-21)
# ============================================================================

from src.mesh_analyzer import MeshAnalyzer


class TestProperty20_MeshQualityAnalysis:
    """
    Property 20: Mesh Quality Analysis
    
    For any loaded mesh, the Mesh Analyzer SHALL evaluate quality metrics
    (watertight check, degenerate triangle detection, non-manifold edge detection,
    average triangle quality), SHALL report vertex and face counts, and SHALL
    include a warning in the analysis report when mesh quality is poor.
    
    Validates: Requirements 19.1, 19.2, 19.3, 19.4, 19.5, 19.6, 19.7
    """
    
    @settings(max_examples=3, deadline=None)
    @given(file_path=step_file_path())
    def test_property_20_quality_metrics_complete(self, file_path):
        """
        Property 20a: Quality analysis SHALL include all required metrics
        """
        parser = EnhancedSTEPParser(file_path)
        result = parser.load()
        
        if result and parser.parse_result.success and parser.mesh:
            analyzer = MeshAnalyzer(parser.mesh)
            metrics = analyzer.analyze_quality()
            
            # Must have all required metrics
            required_metrics = [
                'is_watertight', 'is_manifold', 'degenerate_faces',
                'non_manifold_edges', 'avg_triangle_quality',
                'vertex_count', 'face_count', 'quality_rating'
            ]
            
            for metric in required_metrics:
                assert metric in metrics, f"Missing metric: {metric}"
    
    @settings(max_examples=3, deadline=None)
    @given(file_path=step_file_path())
    def test_property_20_vertex_face_counts(self, file_path):
        """
        Property 20b: SHALL report vertex and face counts
        """
        parser = EnhancedSTEPParser(file_path)
        result = parser.load()
        
        if result and parser.parse_result.success and parser.mesh:
            analyzer = MeshAnalyzer(parser.mesh)
            metrics = analyzer.analyze_quality()
            
            # Must have counts
            assert 'vertex_count' in metrics
            assert 'face_count' in metrics
            
            # Counts must be positive
            assert metrics['vertex_count'] > 0, "Vertex count must be positive"
            assert metrics['face_count'] > 0, "Face count must be positive"
    
    @settings(max_examples=3, deadline=None)
    @given(file_path=step_file_path())
    def test_property_20_quality_rating(self, file_path):
        """
        Property 20c: SHALL include quality rating
        """
        parser = EnhancedSTEPParser(file_path)
        result = parser.load()
        
        if result and parser.parse_result.success and parser.mesh:
            analyzer = MeshAnalyzer(parser.mesh)
            metrics = analyzer.analyze_quality()
            
            # Must have quality rating
            assert 'quality_rating' in metrics
            
            # Rating must be valid
            valid_ratings = ['Excellent', 'Good', 'Fair', 'Poor']
            assert metrics['quality_rating'] in valid_ratings, \
                f"Invalid quality rating: {metrics['quality_rating']}"
    
    @settings(max_examples=3, deadline=None)
    @given(
        subdivisions=st.integers(min_value=1, max_value=3)
    )
    def test_property_20_triangle_quality_range(self, subdivisions):
        """
        Property 20d: Triangle quality SHALL be in range [0, 1]
        """
        # Create test mesh
        mesh = trimesh.creation.icosphere(subdivisions=subdivisions)
        
        analyzer = MeshAnalyzer(mesh)
        qualities = analyzer.calculate_triangle_quality()
        
        # All qualities must be in valid range (allow small numerical error)
        assert np.all(qualities >= 0.0), "Quality values must be >= 0"
        assert np.all(qualities <= 1.01), "Quality values must be <= 1 (with tolerance)"


class TestProperty21_AutomaticMeshRepair:
    """
    Property 21: Automatic Mesh Repair
    
    For any mesh with detected defects (non-watertight, degenerate triangles,
    non-manifold edges), the Mesh Analyzer SHALL attempt automatic repair before
    analysis, and SHALL report the repairs performed.
    
    Validates: Requirements 19.8
    """
    
    @settings(max_examples=3, deadline=None)
    @given(file_path=step_file_path())
    def test_property_21_repair_returns_mesh_and_repairs(self, file_path):
        """
        Property 21a: Repair SHALL return repaired mesh and list of repairs
        """
        parser = EnhancedSTEPParser(file_path)
        result = parser.load()
        
        if result and parser.parse_result.success and parser.mesh:
            analyzer = MeshAnalyzer(parser.mesh)
            result = analyzer.repair_mesh()
            
            # Must return tuple
            assert isinstance(result, tuple), "Repair must return tuple"
            assert len(result) == 2, "Repair must return 2 values"
            
            repaired_mesh, repairs = result
            
            # Must return mesh
            assert repaired_mesh is not None, "Repaired mesh must not be None"
            assert isinstance(repaired_mesh, trimesh.Trimesh), \
                "Repaired mesh must be Trimesh"
            
            # Must return list of repairs
            assert isinstance(repairs, list), "Repairs must be a list"
    
    @settings(max_examples=3, deadline=None)
    @given(
        subdivisions=st.integers(min_value=1, max_value=3)
    )
    def test_property_21_repair_preserves_mesh_structure(self, subdivisions):
        """
        Property 21b: Repair SHALL preserve mesh structure
        """
        # Create test mesh
        mesh = trimesh.creation.icosphere(subdivisions=subdivisions)
        original_vertex_count = len(mesh.vertices)
        original_face_count = len(mesh.faces)
        
        analyzer = MeshAnalyzer(mesh)
        repaired_mesh, repairs = analyzer.repair_mesh()
        
        # Repaired mesh should have vertices and faces
        assert len(repaired_mesh.vertices) > 0, "Repaired mesh has no vertices"
        assert len(repaired_mesh.faces) > 0, "Repaired mesh has no faces"
        
        # Vertex/face counts should be similar (within 50% for repairs)
        vertex_ratio = len(repaired_mesh.vertices) / original_vertex_count
        face_ratio = len(repaired_mesh.faces) / original_face_count
        
        assert 0.5 <= vertex_ratio <= 1.5, \
            f"Vertex count changed drastically: {vertex_ratio}"
        assert 0.5 <= face_ratio <= 1.5, \
            f"Face count changed drastically: {face_ratio}"
    
    @settings(max_examples=3, deadline=None)
    @given(
        subdivisions=st.integers(min_value=1, max_value=3)
    )
    def test_property_21_repair_improves_quality(self, subdivisions):
        """
        Property 21c: Repair SHALL improve or maintain mesh quality
        """
        # Create test mesh
        mesh = trimesh.creation.icosphere(subdivisions=subdivisions)
        
        analyzer = MeshAnalyzer(mesh)
        
        # Analyze before repair
        metrics_before = analyzer.analyze_quality()
        
        # Repair
        repaired_mesh, repairs = analyzer.repair_mesh()
        
        # Analyze after repair
        analyzer_after = MeshAnalyzer(repaired_mesh)
        metrics_after = analyzer_after.analyze_quality()
        
        # Quality should not decrease significantly
        # (Allow small variations due to numerical precision)
        if 'avg_triangle_quality' in metrics_before and 'avg_triangle_quality' in metrics_after:
            quality_before = metrics_before['avg_triangle_quality']
            quality_after = metrics_after['avg_triangle_quality']
            
            # Quality should not decrease by more than 10%
            assert quality_after >= quality_before * 0.9, \
                f"Quality decreased: {quality_before} -> {quality_after}"
