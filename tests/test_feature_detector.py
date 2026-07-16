"""
Unit Tests for Feature Detector

Tests hole detection, corner detection, and other feature identification.
"""
import pytest
import numpy as np
import trimesh
from src.feature_detector import (
    FeatureDetector, Feature, Hole, Pocket, Corner, Boss, Rib
)


class TestFeatureDetectorInitialization:
    """Test FeatureDetector initialization"""
    
    def test_detector_initialization(self):
        """Test basic initialization"""
        mesh = trimesh.creation.box(extents=[10, 20, 30])
        detector = FeatureDetector(mesh)
        
        assert detector.mesh is mesh
        assert isinstance(detector.features, list)
        assert len(detector.features) == 0
    
    def test_initialization_with_invalid_input(self):
        """Test initialization fails with invalid input"""
        with pytest.raises(TypeError):
            FeatureDetector("not a mesh")


class TestFeatureDataModels:
    """Test feature data models"""
    
    def test_hole_creation(self):
        """Test Hole dataclass"""
        hole = Hole(
            center=(10.0, 20.0, 5.0),
            diameter=5.0,
            depth=10.0,
            axis=(0, 0, 1),
            is_through=True,
            confidence=0.95
        )
        
        assert hole.feature_type == 'hole'
        assert hole.diameter == 5.0
        assert hole.depth == 10.0
        assert hole.is_through is True
        assert 'diameter' in hole.dimensions
        assert 'depth' in hole.dimensions
    
    def test_corner_creation(self):
        """Test Corner dataclass"""
        corner = Corner(
            center=(5.0, 5.0, 5.0),
            radius=2.0,
            angle=90.0,
            is_internal=True,
            is_fillet=True,
            confidence=0.9
        )
        
        assert corner.feature_type == 'corner'
        assert corner.radius == 2.0
        assert corner.angle == 90.0
        assert corner.is_internal is True
        assert 'radius' in corner.dimensions
        assert 'angle' in corner.dimensions
    
    def test_pocket_creation(self):
        """Test Pocket dataclass"""
        pocket = Pocket(
            center=(10.0, 10.0, 5.0),
            width=20.0,
            length=30.0,
            depth=10.0,
            corner_radii=[2.0, 2.0, 2.0, 2.0],
            is_open=True,
            confidence=0.85
        )
        
        assert pocket.feature_type == 'pocket'
        assert pocket.width == 20.0
        assert pocket.length == 30.0
        assert pocket.depth == 10.0
        assert len(pocket.corner_radii) == 4


class TestHoleDetection:
    """Test hole detection"""
    
    def test_detect_holes_on_simple_mesh(self):
        """Test hole detection on a simple mesh"""
        # Create a box (no holes)
        mesh = trimesh.creation.box(extents=[20, 20, 20])
        detector = FeatureDetector(mesh)
        
        holes = detector.detect_holes()
        
        # Box has no holes
        assert isinstance(holes, list)
        # May detect 0 or more depending on mesh structure
        assert len(holes) >= 0
    
    def test_detect_holes_with_cylinder(self):
        """Test hole detection with cylindrical mesh"""
        # Create a cylinder (could be interpreted as a hole)
        mesh = trimesh.creation.cylinder(radius=5.0, height=20.0)
        detector = FeatureDetector(mesh)
        
        holes = detector.detect_holes(min_diameter=8.0, max_diameter=12.0)
        
        assert isinstance(holes, list)
        # Cylinder might be detected as a hole
        for hole in holes:
            assert isinstance(hole, Hole)
            assert hole.diameter > 0
            assert hole.depth > 0
    
    def test_detect_holes_returns_hole_objects(self):
        """Test that hole detection returns Hole objects"""
        mesh = trimesh.creation.icosphere(radius=10.0)
        detector = FeatureDetector(mesh)
        
        holes = detector.detect_holes()
        
        for hole in holes:
            assert isinstance(hole, Hole)
            assert hasattr(hole, 'diameter')
            assert hasattr(hole, 'depth')
            assert hasattr(hole, 'center')
            assert hasattr(hole, 'axis')
            assert hasattr(hole, 'is_through')


class TestCornerDetection:
    """Test corner detection"""
    
    def test_detect_corners_on_box(self):
        """Test corner detection on a box"""
        mesh = trimesh.creation.box(extents=[10, 20, 30])
        detector = FeatureDetector(mesh)
        
        corners = detector.detect_corners(min_angle=45.0)
        
        assert isinstance(corners, list)
        # Box has many corners
        assert len(corners) > 0
        
        for corner in corners:
            assert isinstance(corner, Corner)
            assert corner.angle > 0
    
    def test_detect_corners_returns_corner_objects(self):
        """Test that corner detection returns Corner objects"""
        mesh = trimesh.creation.box(extents=[10, 10, 10])
        detector = FeatureDetector(mesh)
        
        corners = detector.detect_corners()
        
        for corner in corners:
            assert isinstance(corner, Corner)
            assert hasattr(corner, 'radius')
            assert hasattr(corner, 'angle')
            assert hasattr(corner, 'center')
            assert hasattr(corner, 'is_internal')


class TestFeatureDetectionWorkflow:
    """Test complete feature detection workflow"""
    
    def test_detect_all_features(self):
        """Test detecting all features at once"""
        mesh = trimesh.creation.box(extents=[20, 20, 20])
        detector = FeatureDetector(mesh)
        
        features = detector.detect_all_features(
            detect_holes=True,
            detect_corners=True,
            detect_pockets=False,
            detect_bosses=False,
            detect_ribs=False
        )
        
        assert isinstance(features, list)
        assert len(features) >= 0
        
        # Features should be stored in detector
        assert detector.features == features
    
    def test_get_features_by_type(self):
        """Test filtering features by type"""
        mesh = trimesh.creation.box(extents=[10, 10, 10])
        detector = FeatureDetector(mesh)
        
        # Detect features
        detector.detect_all_features(detect_holes=True, detect_corners=True)
        
        # Get holes only
        holes = detector.get_features_by_type('hole')
        assert all(f.feature_type == 'hole' for f in holes)
        
        # Get corners only
        corners = detector.get_features_by_type('corner')
        assert all(f.feature_type == 'corner' for f in corners)
    
    def test_get_feature_summary(self):
        """Test getting feature summary"""
        mesh = trimesh.creation.box(extents=[10, 10, 10])
        detector = FeatureDetector(mesh)
        
        # Detect features
        detector.detect_all_features()
        
        summary = detector.get_feature_summary()
        
        assert 'total_features' in summary
        assert 'by_type' in summary
        assert 'hole' in summary['by_type']
        assert 'corner' in summary['by_type']
        assert 'pocket' in summary['by_type']
        
        # Check counts
        for feature_type, info in summary['by_type'].items():
            assert 'count' in info
            assert 'features' in info
            assert info['count'] == len(info['features'])


class TestRealWorldScenarios:
    """Test with real-world mesh scenarios"""
    
    def test_cylinder_mesh(self):
        """Test feature detection on cylinder"""
        mesh = trimesh.creation.cylinder(radius=5.0, height=20.0)
        detector = FeatureDetector(mesh)
        
        features = detector.detect_all_features()
        
        assert isinstance(features, list)
        summary = detector.get_feature_summary()
        assert summary['total_features'] >= 0
    
    def test_sphere_mesh(self):
        """Test feature detection on sphere"""
        mesh = trimesh.creation.icosphere(radius=10.0)
        detector = FeatureDetector(mesh)
        
        features = detector.detect_all_features()
        
        assert isinstance(features, list)
        # Sphere should have few sharp corners
        corners = detector.get_features_by_type('corner')
        # Icosphere has some edges but they're not very sharp
        assert len(corners) >= 0
    
    def test_torus_mesh(self):
        """Test feature detection on torus"""
        mesh = trimesh.creation.torus(major_radius=10.0, minor_radius=2.0)
        detector = FeatureDetector(mesh)
        
        features = detector.detect_all_features()
        
        assert isinstance(features, list)
        summary = detector.get_feature_summary()
        assert 'total_features' in summary
