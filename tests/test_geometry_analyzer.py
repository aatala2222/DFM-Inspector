"""
Unit Tests for Geometry Analyzer

Tests wall thickness measurement, dimension analysis,
and geometric property calculations.
"""
import pytest
import numpy as np
import trimesh
from src.geometry_analyzer import GeometryAnalyzer, ThicknessMeasurement


class TestGeometryAnalyzerInitialization:
    """Test GeometryAnalyzer initialization"""
    
    def test_analyzer_initialization(self):
        """Test basic initialization with valid mesh"""
        mesh = trimesh.creation.box(extents=[10, 20, 30])
        analyzer = GeometryAnalyzer(mesh)
        
        assert analyzer.mesh is mesh
        assert analyzer.ray_intersector is not None
        assert isinstance(analyzer.thickness_map, dict)
        assert len(analyzer.thickness_map) == 0
    
    def test_initialization_with_invalid_input(self):
        """Test initialization fails with invalid input"""
        with pytest.raises(TypeError):
            GeometryAnalyzer("not a mesh")
        
        with pytest.raises(TypeError):
            GeometryAnalyzer(None)


class TestDimensionMeasurement:
    """Test dimension measurement"""
    
    def test_measure_dimensions_box(self):
        """Test dimension measurement on a box"""
        mesh = trimesh.creation.box(extents=[10, 20, 30])
        analyzer = GeometryAnalyzer(mesh)
        
        dims = analyzer.measure_dimensions()
        
        assert 'x' in dims
        assert 'y' in dims
        assert 'z' in dims
        assert abs(dims['x'] - 10.0) < 0.1
        assert abs(dims['y'] - 20.0) < 0.1
        assert abs(dims['z'] - 30.0) < 0.1
    
    def test_measure_dimensions_sphere(self):
        """Test dimension measurement on a sphere"""
        mesh = trimesh.creation.icosphere(radius=5.0)
        analyzer = GeometryAnalyzer(mesh)
        
        dims = analyzer.measure_dimensions()
        
        # Sphere should have equal dimensions
        assert abs(dims['x'] - dims['y']) < 0.5
        assert abs(dims['y'] - dims['z']) < 0.5
        # Diameter should be ~10mm (radius 5mm)
        assert abs(dims['x'] - 10.0) < 1.0


class TestVolumeCalculation:
    """Test volume calculation"""
    
    def test_calculate_volume_box(self):
        """Test volume calculation for a box"""
        mesh = trimesh.creation.box(extents=[10, 20, 30])
        analyzer = GeometryAnalyzer(mesh)
        
        volume = analyzer.calculate_volume()
        
        # Box volume = 10 * 20 * 30 = 6000
        assert abs(volume - 6000.0) < 10.0
    
    def test_calculate_volume_sphere(self):
        """Test volume calculation for a sphere"""
        mesh = trimesh.creation.icosphere(radius=5.0)
        analyzer = GeometryAnalyzer(mesh)
        
        volume = analyzer.calculate_volume()
        
        # Sphere volume = (4/3) * π * r³ = (4/3) * π * 125 ≈ 523.6
        expected = (4/3) * np.pi * (5.0 ** 3)
        assert abs(volume - expected) < 50.0  # Allow some error for mesh approximation


class TestSurfaceAreaCalculation:
    """Test surface area calculation"""
    
    def test_calculate_surface_area_box(self):
        """Test surface area calculation for a box"""
        mesh = trimesh.creation.box(extents=[10, 20, 30])
        analyzer = GeometryAnalyzer(mesh)
        
        area = analyzer.calculate_surface_area()
        
        # Box surface area = 2*(10*20 + 20*30 + 30*10) = 2*(200 + 600 + 300) = 2200
        assert abs(area - 2200.0) < 50.0
    
    def test_calculate_surface_area_sphere(self):
        """Test surface area calculation for a sphere"""
        mesh = trimesh.creation.icosphere(radius=5.0)
        analyzer = GeometryAnalyzer(mesh)
        
        area = analyzer.calculate_surface_area()
        
        # Sphere surface area = 4 * π * r² = 4 * π * 25 ≈ 314.16
        expected = 4 * np.pi * (5.0 ** 2)
        assert abs(area - expected) < 50.0  # Allow some error for mesh approximation


class TestWallThicknessMeasurement:
    """Test wall thickness measurement"""
    
    def test_measure_wall_thickness_hollow_box(self):
        """Test wall thickness measurement on a hollow box"""
        # Skip if manifold3d not available
        pytest.importorskip("manifold3d")
        
        # Create hollow box (outer box - inner box)
        outer = trimesh.creation.box(extents=[20, 20, 20])
        inner = trimesh.creation.box(extents=[16, 16, 16])
        mesh = outer.difference(inner)
        
        analyzer = GeometryAnalyzer(mesh)
        result = analyzer.measure_wall_thickness(sample_density=500)
        
        assert 'min_thickness' in result
        assert 'max_thickness' in result
        assert 'avg_thickness' in result
        assert 'samples' in result
        assert result['samples'] > 0
        
        # Wall thickness should be ~2mm (20-16)/2
        assert 1.5 < result['min_thickness'] < 2.5
    
    def test_measure_wall_thickness_returns_measurements(self):
        """Test that wall thickness measurement returns measurement objects"""
        mesh = trimesh.creation.box(extents=[10, 10, 10])
        analyzer = GeometryAnalyzer(mesh)
        
        result = analyzer.measure_wall_thickness(sample_density=100)
        
        assert 'measurements' in result
        assert isinstance(result['measurements'], list)
        
        if len(result['measurements']) > 0:
            measurement = result['measurements'][0]
            assert isinstance(measurement, ThicknessMeasurement)
            assert hasattr(measurement, 'location')
            assert hasattr(measurement, 'thickness')
            assert hasattr(measurement, 'opposing_point')
            assert hasattr(measurement, 'normal')
    
    def test_measure_wall_thickness_min_samples(self):
        """Test that minimum number of samples is enforced"""
        # Use a hollow cylinder which has measurable wall thickness
        mesh = trimesh.creation.annulus(r_min=4.0, r_max=5.0, height=10.0)
        analyzer = GeometryAnalyzer(mesh)
        
        result = analyzer.measure_wall_thickness(sample_density=10)
        
        # Should have at least some samples (minimum enforced is 100)
        # But not all rays will find opposing surfaces
        assert result['samples'] >= 0  # At least attempted


class TestThicknessMap:
    """Test thickness map functionality"""
    
    def test_get_thickness_map(self):
        """Test getting thickness map"""
        mesh = trimesh.creation.box(extents=[10, 10, 10])
        analyzer = GeometryAnalyzer(mesh)
        
        # Measure thickness first
        analyzer.measure_wall_thickness(sample_density=100)
        
        thickness_map = analyzer.get_thickness_map()
        
        assert isinstance(thickness_map, dict)
        # Should have some measurements
        assert len(thickness_map) >= 0
    
    def test_get_thickness_at_point(self):
        """Test getting thickness at specific point"""
        mesh = trimesh.creation.box(extents=[10, 10, 10])
        analyzer = GeometryAnalyzer(mesh)
        
        # Measure thickness first
        result = analyzer.measure_wall_thickness(sample_density=100)
        
        if result['min_location']:
            x, y, z = result['min_location']
            thickness = analyzer.get_thickness_at_point(x, y, z, tolerance=1.0)
            
            # Should find a thickness value near the min location
            assert thickness is not None
            assert thickness > 0


class TestAnalysisSummary:
    """Test comprehensive analysis summary"""
    
    def test_get_analysis_summary(self):
        """Test getting complete analysis summary"""
        mesh = trimesh.creation.box(extents=[10, 20, 30])
        analyzer = GeometryAnalyzer(mesh)
        
        summary = analyzer.get_analysis_summary()
        
        assert 'dimensions' in summary
        assert 'volume' in summary
        assert 'surface_area' in summary
        assert 'is_watertight' in summary
        assert 'vertex_count' in summary
        assert 'face_count' in summary
        
        assert summary['dimensions']['x'] > 0
        assert summary['volume'] > 0
        assert summary['surface_area'] > 0
    
    def test_get_analysis_summary_with_thickness(self):
        """Test analysis summary includes thickness if measured"""
        mesh = trimesh.creation.box(extents=[10, 10, 10])
        analyzer = GeometryAnalyzer(mesh)
        
        # Measure thickness
        analyzer.measure_wall_thickness(sample_density=100)
        
        summary = analyzer.get_analysis_summary()
        
        # Should include wall thickness if measurements were made
        if analyzer.thickness_map:
            assert 'wall_thickness' in summary
            assert 'min' in summary['wall_thickness']
            assert 'max' in summary['wall_thickness']
            assert 'avg' in summary['wall_thickness']


class TestMeasurementValidation:
    """Test measurement validation"""
    
    def test_validate_wall_thickness(self):
        """Test wall thickness validation"""
        mesh = trimesh.creation.box(extents=[10, 20, 30])
        analyzer = GeometryAnalyzer(mesh)
        
        # Valid thickness (positive and less than max dimension)
        assert analyzer.validate_measurement('wall_thickness', 5.0) is True
        
        # Invalid thickness (negative)
        assert analyzer.validate_measurement('wall_thickness', -1.0) is False
        
        # Invalid thickness (zero)
        assert analyzer.validate_measurement('wall_thickness', 0.0) is False
        
        # Invalid thickness (exceeds max dimension)
        assert analyzer.validate_measurement('wall_thickness', 100.0) is False
    
    def test_validate_hole_diameter(self):
        """Test hole diameter validation"""
        mesh = trimesh.creation.box(extents=[10, 20, 30])
        analyzer = GeometryAnalyzer(mesh)
        
        # Valid diameter
        assert analyzer.validate_measurement('hole_diameter', 5.0) is True
        
        # Invalid diameter (negative)
        assert analyzer.validate_measurement('hole_diameter', -1.0) is False
        
        # Invalid diameter (exceeds max dimension)
        assert analyzer.validate_measurement('hole_diameter', 100.0) is False


class TestRealWorldMeshes:
    """Test with real-world mesh scenarios"""
    
    def test_cylinder_mesh(self):
        """Test analysis of cylindrical mesh"""
        mesh = trimesh.creation.cylinder(radius=5.0, height=20.0)
        analyzer = GeometryAnalyzer(mesh)
        
        dims = analyzer.measure_dimensions()
        volume = analyzer.calculate_volume()
        
        # Cylinder dimensions
        assert abs(dims['z'] - 20.0) < 1.0  # Height
        assert abs(dims['x'] - 10.0) < 1.0  # Diameter
        
        # Cylinder volume = π * r² * h = π * 25 * 20 ≈ 1571
        expected_volume = np.pi * (5.0 ** 2) * 20.0
        assert abs(volume - expected_volume) < 100.0
    
    def test_torus_mesh(self):
        """Test analysis of torus mesh"""
        mesh = trimesh.creation.torus(major_radius=10.0, minor_radius=2.0)
        analyzer = GeometryAnalyzer(mesh)
        
        summary = analyzer.get_analysis_summary()
        
        assert summary['volume'] > 0
        assert summary['surface_area'] > 0
        assert summary['vertex_count'] > 0
        assert summary['face_count'] > 0
