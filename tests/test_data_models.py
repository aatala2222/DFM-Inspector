"""
Unit tests for data models

Tests serialization, deserialization, and basic functionality of all data models.
"""

import pytest
import numpy as np
import json
from src.data_models import (
    Vertex, Edge, Face, Surface,
    Measurement, WallThicknessMeasurement,
    Feature, Hole, Pocket, Corner, Boss, Rib,
    Violation, FeatureReport
)


class TestGeometricEntities:
    """Test geometric entity dataclasses"""
    
    def test_vertex_creation(self):
        """Test vertex creation with coordinates"""
        v = Vertex(
            entity_id='v1',
            entity_type='vertex',
            coordinates=np.array([1.0, 2.0, 3.0]),
            x=1.0, y=2.0, z=3.0
        )
        assert v.x == 1.0
        assert v.y == 2.0
        assert v.z == 3.0
        assert np.array_equal(v.coordinates, np.array([1.0, 2.0, 3.0]))
    
    def test_edge_creation(self):
        """Test edge creation"""
        e = Edge(
            entity_id='e1',
            entity_type='edge',
            coordinates=np.array([0.0, 0.0, 0.0]),
            v1_id=0,
            v2_id=1,
            length=5.0
        )
        assert e.v1_id == 0
        assert e.v2_id == 1
        assert e.length == 5.0
    
    def test_face_creation(self):
        """Test face creation"""
        f = Face(
            entity_id='f1',
            entity_type='face',
            coordinates=np.array([0.0, 0.0, 0.0]),
            v1_id=0, v2_id=1, v3_id=2,
            normal=(0.0, 0.0, 1.0),
            area=10.0
        )
        assert f.v1_id == 0
        assert f.v2_id == 1
        assert f.v3_id == 2
        assert f.normal == (0.0, 0.0, 1.0)
        assert f.area == 10.0


class TestMeasurements:
    """Test measurement dataclasses"""
    
    def test_measurement_creation(self):
        """Test basic measurement creation"""
        m = Measurement(
            measurement_type='wall_thickness',
            value=2.5,
            unit='mm',
            location=(10.0, 20.0, 5.0),
            confidence=95.0,
            method='ray_casting'
        )
        assert m.value == 2.5
        assert m.unit == 'mm'
        assert m.confidence == 95.0
    
    def test_wall_thickness_measurement(self):
        """Test wall thickness measurement"""
        wtm = WallThicknessMeasurement(
            measurement_type='wall_thickness',
            value=1.5,
            location=(10.0, 20.0, 5.0),
            sample_point=(10.0, 20.0, 5.0),
            opposing_point=(10.0, 20.0, 6.5),
            normal_direction=(0.0, 0.0, 1.0)
        )
        assert wtm.value == 1.5
        assert wtm.sample_point == (10.0, 20.0, 5.0)
        assert wtm.opposing_point == (10.0, 20.0, 6.5)


class TestFeatures:
    """Test feature dataclasses"""
    
    def test_hole_creation(self):
        """Test hole feature creation"""
        hole = Hole(
            feature_id='hole1',
            feature_type='hole',
            center=(50.0, 50.0, 0.0),
            diameter=5.0,
            depth=10.0,
            axis=(0.0, 0.0, 1.0),
            is_through=True,
            is_threaded=False
        )
        assert hole.diameter == 5.0
        assert hole.depth == 10.0
        assert hole.is_through == True
        assert hole.is_threaded == False
    
    def test_pocket_creation(self):
        """Test pocket feature creation"""
        pocket = Pocket(
            feature_id='pocket1',
            feature_type='pocket',
            center=(25.0, 25.0, 5.0),
            width=10.0,
            length=20.0,
            depth=15.0,
            corner_radii=[1.0, 1.0, 1.0, 1.0],
            is_open=True,
            is_deep=False
        )
        assert pocket.width == 10.0
        assert pocket.length == 20.0
        assert pocket.depth == 15.0
        assert len(pocket.corner_radii) == 4
    
    def test_corner_creation(self):
        """Test corner feature creation"""
        corner = Corner(
            feature_id='corner1',
            feature_type='corner',
            center=(10.0, 10.0, 0.0),
            radius=0.5,
            angle=90.0,
            is_internal=True,
            is_fillet=True
        )
        assert corner.radius == 0.5
        assert corner.angle == 90.0
        assert corner.is_internal == True
        assert corner.is_fillet == True


class TestViolation:
    """Test violation dataclass"""
    
    def test_violation_creation(self):
        """Test violation creation"""
        violation = Violation(
            violation_id='v1',
            rule_name='Minimum Wall Thickness',
            rule_standard='ISO 2768-m',
            measured_value=0.7,
            required_value=0.8,
            severity='critical',
            coordinates=(45.2, 67.8, 12.3),
            message='Wall thickness 0.70mm is below minimum 0.80mm',
            recommendation='Increase wall thickness to at least 0.80mm'
        )
        assert violation.measured_value == 0.7
        assert violation.required_value == 0.8
        assert violation.severity == 'critical'


class TestFeatureReport:
    """Test feature report dataclass and JSON serialization"""
    
    def test_feature_report_creation(self):
        """Test feature report creation"""
        report = FeatureReport(
            part_name='test_part.step',
            walls=[],
            holes=[],
            pockets=[],
            corners=[],
            bosses=[],
            ribs=[]
        )
        assert report.part_name == 'test_part.step'
        assert len(report.holes) == 0
    
    def test_feature_report_with_features(self):
        """Test feature report with actual features"""
        hole = Hole(
            feature_id='hole1',
            feature_type='hole',
            center=(50.0, 50.0, 0.0),
            diameter=5.0,
            depth=10.0,
            axis=(0.0, 0.0, 1.0),
            is_through=True
        )
        
        report = FeatureReport(
            part_name='test_part.step',
            holes=[hole]
        )
        assert len(report.holes) == 1
        assert report.holes[0].diameter == 5.0
    
    def test_json_serialization(self):
        """Test JSON export"""
        hole = Hole(
            feature_id='hole1',
            feature_type='hole',
            center=(50.0, 50.0, 0.0),
            diameter=5.0,
            depth=10.0,
            axis=(0.0, 0.0, 1.0),
            is_through=True
        )
        
        report = FeatureReport(
            part_name='test_part.step',
            holes=[hole]
        )
        
        json_str = report.to_json()
        assert isinstance(json_str, str)
        assert 'test_part.step' in json_str
        assert 'hole1' in json_str
    
    def test_json_round_trip(self):
        """Test JSON export and import (round-trip)"""
        # Create report with features
        hole = Hole(
            feature_id='hole1',
            feature_type='hole',
            center=(50.0, 50.0, 0.0),
            diameter=5.0,
            depth=10.0,
            axis=(0.0, 0.0, 1.0),
            is_through=True
        )
        
        corner = Corner(
            feature_id='corner1',
            feature_type='corner',
            center=(10.0, 10.0, 0.0),
            radius=0.5,
            angle=90.0,
            is_internal=True
        )
        
        original_report = FeatureReport(
            part_name='test_part.step',
            holes=[hole],
            corners=[corner]
        )
        
        # Export to JSON
        json_str = original_report.to_json()
        
        # Import from JSON
        restored_report = FeatureReport.from_json(json_str)
        
        # Verify data preserved
        assert restored_report.part_name == original_report.part_name
        assert len(restored_report.holes) == 1
        assert restored_report.holes[0].diameter == 5.0
        assert len(restored_report.corners) == 1
        assert restored_report.corners[0].radius == 0.5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
