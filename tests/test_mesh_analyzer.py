"""
Unit tests for Mesh Analyzer

Tests mesh quality analysis, defect detection, and automatic repair.
Requirements: Requirement 19 (Mesh Quality Analysis)
"""

import pytest
import numpy as np
import trimesh
from src.mesh_analyzer import MeshAnalyzer


class TestMeshAnalyzerInitialization:
    """Test MeshAnalyzer initialization"""
    
    def test_analyzer_initialization(self):
        """Test analyzer initializes correctly"""
        # Create simple mesh
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        faces = np.array([
            [0, 1, 2],
            [0, 1, 3],
            [0, 2, 3],
            [1, 2, 3]
        ])
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        analyzer = MeshAnalyzer(mesh)
        
        assert analyzer.mesh is not None
        assert len(analyzer.quality_metrics) == 0
        assert len(analyzer.defects) == 0


class TestWatertightCheck:
    """Test watertight checking"""
    
    def test_watertight_mesh(self):
        """Test watertight mesh detection"""
        # Create closed tetrahedron (watertight)
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        faces = np.array([
            [0, 1, 2],
            [0, 1, 3],
            [0, 2, 3],
            [1, 2, 3]
        ])
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        analyzer = MeshAnalyzer(mesh)
        is_watertight = analyzer.check_watertight()
        
        assert is_watertight == True
    
    def test_non_watertight_mesh(self):
        """Test non-watertight mesh detection"""
        # Create single triangle (not watertight)
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0]
        ])
        faces = np.array([[0, 1, 2]])
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        analyzer = MeshAnalyzer(mesh)
        is_watertight = analyzer.check_watertight()
        
        assert is_watertight == False


class TestDegenerateTriangleDetection:
    """Test degenerate triangle detection"""
    
    def test_no_degenerate_triangles(self):
        """Test mesh with no degenerate triangles"""
        # Create valid tetrahedron
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        faces = np.array([
            [0, 1, 2],
            [0, 1, 3],
            [0, 2, 3],
            [1, 2, 3]
        ])
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        analyzer = MeshAnalyzer(mesh)
        degenerate = analyzer.detect_degenerate_triangles()
        
        assert len(degenerate) == 0
    
    def test_degenerate_triangle_detection(self):
        """Test detection of degenerate triangles"""
        # Create mesh with one degenerate triangle (all vertices at same point)
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0]  # Duplicate of first vertex
        ])
        faces = np.array([
            [0, 1, 2],  # Valid triangle
            [0, 1, 3]   # Degenerate (v0 == v3)
        ])
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        analyzer = MeshAnalyzer(mesh)
        degenerate = analyzer.detect_degenerate_triangles()
        
        # Should detect at least one degenerate triangle
        assert len(degenerate) >= 1


class TestNonManifoldEdgeDetection:
    """Test non-manifold edge detection"""
    
    def test_manifold_mesh(self):
        """Test manifold mesh (no non-manifold edges)"""
        # Create valid tetrahedron
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        faces = np.array([
            [0, 1, 2],
            [0, 1, 3],
            [0, 2, 3],
            [1, 2, 3]
        ])
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        analyzer = MeshAnalyzer(mesh)
        non_manifold = analyzer.detect_non_manifold_edges()
        
        assert len(non_manifold) == 0
    
    def test_non_manifold_edges(self):
        """Test detection of non-manifold edges"""
        # Create mesh with open edge (non-manifold)
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0]
        ])
        faces = np.array([[0, 1, 2]])
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        analyzer = MeshAnalyzer(mesh)
        non_manifold = analyzer.detect_non_manifold_edges()
        
        # Single triangle has 3 open edges (each shared by only 1 face)
        assert len(non_manifold) == 3


class TestTriangleQualityCalculation:
    """Test triangle quality metric calculation"""
    
    def test_equilateral_triangle_quality(self):
        """Test quality of equilateral triangle (should be 1.0)"""
        # Create equilateral triangle
        side = 1.0
        height = side * np.sqrt(3) / 2
        vertices = np.array([
            [0, 0, 0],
            [side, 0, 0],
            [side/2, height, 0]
        ])
        faces = np.array([[0, 1, 2]])
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        analyzer = MeshAnalyzer(mesh)
        qualities = analyzer.calculate_triangle_quality()
        
        assert len(qualities) == 1
        # Equilateral triangle should have quality close to 1.0
        assert qualities[0] > 0.99
    
    def test_degenerate_triangle_quality(self):
        """Test quality of degenerate triangle (should be 0.0)"""
        # Create degenerate triangle (all vertices collinear)
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0]  # Collinear with first two
        ])
        faces = np.array([[0, 1, 2]])
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        analyzer = MeshAnalyzer(mesh)
        qualities = analyzer.calculate_triangle_quality()
        
        assert len(qualities) == 1
        # Degenerate triangle should have quality close to 0.0
        assert qualities[0] < 0.01
    
    def test_quality_range(self):
        """Test that quality values are in valid range [0, 1]"""
        # Create random mesh
        mesh = trimesh.creation.icosphere(subdivisions=2)
        
        analyzer = MeshAnalyzer(mesh)
        qualities = analyzer.calculate_triangle_quality()
        
        # All qualities should be in [0, 1]
        assert np.all(qualities >= 0.0)
        assert np.all(qualities <= 1.0)


class TestQualityAnalysis:
    """Test comprehensive quality analysis"""
    
    def test_analyze_quality_returns_dict(self):
        """Test that analyze_quality returns dictionary"""
        mesh = trimesh.creation.icosphere(subdivisions=2)
        
        analyzer = MeshAnalyzer(mesh)
        metrics = analyzer.analyze_quality()
        
        assert isinstance(metrics, dict)
    
    def test_analyze_quality_has_required_keys(self):
        """Test that quality metrics contain required keys"""
        mesh = trimesh.creation.icosphere(subdivisions=2)
        
        analyzer = MeshAnalyzer(mesh)
        metrics = analyzer.analyze_quality()
        
        required_keys = [
            'is_watertight', 'is_manifold', 'degenerate_faces',
            'non_manifold_edges', 'avg_triangle_quality', 'min_triangle_quality',
            'vertex_count', 'face_count', 'volume', 'surface_area',
            'quality_rating'
        ]
        
        for key in required_keys:
            assert key in metrics, f"Missing key: {key}"
    
    def test_analyze_quality_icosphere(self):
        """Test quality analysis on perfect icosphere"""
        mesh = trimesh.creation.icosphere(subdivisions=2)
        
        analyzer = MeshAnalyzer(mesh)
        metrics = analyzer.analyze_quality()
        
        # Icosphere should be high quality
        assert metrics['is_watertight'] == True
        assert metrics['is_manifold'] == True
        assert metrics['degenerate_faces'] == 0
        assert metrics['non_manifold_edges'] == 0
        assert metrics['avg_triangle_quality'] > 0.7
        assert metrics['quality_rating'] in ['Excellent', 'Good']
    
    def test_analyze_quality_counts(self):
        """Test that vertex and face counts are correct"""
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        faces = np.array([
            [0, 1, 2],
            [0, 1, 3],
            [0, 2, 3],
            [1, 2, 3]
        ])
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        analyzer = MeshAnalyzer(mesh)
        metrics = analyzer.analyze_quality()
        
        assert metrics['vertex_count'] == 4
        assert metrics['face_count'] == 4


class TestMeshRepair:
    """Test automatic mesh repair"""
    
    def test_repair_returns_tuple(self):
        """Test that repair_mesh returns tuple"""
        mesh = trimesh.creation.icosphere(subdivisions=2)
        
        analyzer = MeshAnalyzer(mesh)
        result = analyzer.repair_mesh()
        
        assert isinstance(result, tuple)
        assert len(result) == 2
        
        repaired_mesh, repairs = result
        assert isinstance(repaired_mesh, trimesh.Trimesh)
        assert isinstance(repairs, list)
    
    def test_repair_perfect_mesh(self):
        """Test repair on perfect mesh (no repairs needed)"""
        mesh = trimesh.creation.icosphere(subdivisions=2)
        
        analyzer = MeshAnalyzer(mesh)
        repaired_mesh, repairs = analyzer.repair_mesh()
        
        # Perfect mesh should need minimal or no repairs
        assert repaired_mesh is not None
        assert isinstance(repairs, list)
    
    def test_repair_removes_degenerate_triangles(self):
        """Test that repair removes degenerate triangles"""
        # Create mesh with degenerate triangle
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0]  # Duplicate
        ])
        faces = np.array([
            [0, 1, 2],  # Valid
            [0, 1, 3]   # Degenerate
        ])
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        analyzer = MeshAnalyzer(mesh)
        repaired_mesh, repairs = analyzer.repair_mesh()
        
        # Should have performed some repairs
        assert len(repairs) > 0
        
        # Check if degenerate removal was mentioned
        repair_text = ' '.join(repairs).lower()
        assert 'degenerate' in repair_text or 'triangle' in repair_text


class TestQualityReport:
    """Test quality report generation"""
    
    def test_get_quality_report_returns_string(self):
        """Test that get_quality_report returns string"""
        mesh = trimesh.creation.icosphere(subdivisions=2)
        
        analyzer = MeshAnalyzer(mesh)
        report = analyzer.get_quality_report()
        
        assert isinstance(report, str)
        assert len(report) > 0
    
    def test_quality_report_contains_metrics(self):
        """Test that quality report contains key metrics"""
        mesh = trimesh.creation.icosphere(subdivisions=2)
        
        analyzer = MeshAnalyzer(mesh)
        report = analyzer.get_quality_report()
        
        # Check for key terms
        assert 'MESH QUALITY REPORT' in report
        assert 'Vertices' in report
        assert 'Faces' in report
        assert 'Watertight' in report
        assert 'Quality Rating' in report or 'Overall Rating' in report
    
    def test_quality_report_auto_analyzes(self):
        """Test that get_quality_report runs analysis if not done"""
        mesh = trimesh.creation.icosphere(subdivisions=2)
        
        analyzer = MeshAnalyzer(mesh)
        # Don't call analyze_quality first
        report = analyzer.get_quality_report()
        
        # Should still generate report
        assert isinstance(report, str)
        assert len(report) > 0
        
        # Metrics should be populated
        assert len(analyzer.quality_metrics) > 0


class TestRealWorldMeshes:
    """Test with real-world mesh scenarios"""
    
    def test_box_mesh(self):
        """Test analysis of box mesh"""
        mesh = trimesh.creation.box(extents=[10, 10, 10])
        
        analyzer = MeshAnalyzer(mesh)
        metrics = analyzer.analyze_quality()
        
        assert metrics['is_watertight'] == True
        assert metrics['vertex_count'] > 0
        assert metrics['face_count'] > 0
        assert metrics['volume'] > 0
        assert metrics['surface_area'] > 0
    
    def test_cylinder_mesh(self):
        """Test analysis of cylinder mesh"""
        mesh = trimesh.creation.cylinder(radius=5, height=10)
        
        analyzer = MeshAnalyzer(mesh)
        metrics = analyzer.analyze_quality()
        
        assert metrics['is_watertight'] == True
        assert metrics['volume'] > 0
    
    def test_sphere_mesh(self):
        """Test analysis of sphere mesh"""
        mesh = trimesh.creation.icosphere(subdivisions=3, radius=5)
        
        analyzer = MeshAnalyzer(mesh)
        metrics = analyzer.analyze_quality()
        
        assert metrics['is_watertight'] == True
        assert metrics['is_manifold'] == True
        assert metrics['degenerate_faces'] == 0
        assert metrics['quality_rating'] in ['Excellent', 'Good']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
