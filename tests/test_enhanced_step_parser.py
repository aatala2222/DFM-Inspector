"""
Unit tests for Enhanced STEP Parser

Tests parsing accuracy, fallback strategies, and geometry extraction.
Requirements: Requirement 1 (Accurate STEP File Parsing)
"""

import pytest
import os
import numpy as np
from src.enhanced_step_parser import EnhancedSTEPParser, ParseResult


class TestParseResult:
    """Test ParseResult dataclass"""
    
    def test_parse_result_success(self):
        """Test successful parse result"""
        result = ParseResult(success=True)
        assert result.success == True
        assert result.error == ''
        assert len(result.vertices) == 0
    
    def test_parse_result_failure(self):
        """Test failed parse result"""
        result = ParseResult(success=False, error='File not found')
        assert result.success == False
        assert result.error == 'File not found'


class TestEnhancedSTEPParserInitialization:
    """Test parser initialization"""
    
    def test_parser_initialization(self):
        """Test parser initializes correctly"""
        parser = EnhancedSTEPParser('test.step')
        assert parser.file_path == 'test.step'
        assert parser.shape is None
        assert parser.mesh is None
        assert parser.parse_result is None
    
    def test_parser_with_nonexistent_file(self):
        """Test parser with non-existent file"""
        parser = EnhancedSTEPParser('nonexistent.step')
        result = parser.load()
        assert result == False
        assert parser.parse_result is not None
        assert parser.parse_result.success == False
        assert 'not found' in parser.parse_result.error.lower()


class TestSTEPFileParsing:
    """Test STEP file parsing with real files"""
    
    @pytest.fixture
    def sample_step_files(self):
        """Get list of available sample STEP files"""
        sample_dir = 'sample_files'
        if not os.path.exists(sample_dir):
            pytest.skip("Sample files directory not found")
        
        step_files = [
            os.path.join(sample_dir, f) 
            for f in os.listdir(sample_dir) 
            if f.endswith('.STEP') or f.endswith('.step')
        ]
        
        if not step_files:
            pytest.skip("No STEP files found in sample_files directory")
        
        return step_files
    
    def test_parse_real_step_file(self, sample_step_files):
        """Test parsing real STEP files"""
        for step_file in sample_step_files:
            parser = EnhancedSTEPParser(step_file)
            result = parser.load()
            
            # Parser should succeed with at least one method
            assert result == True, f"Failed to parse {os.path.basename(step_file)}"
            assert parser.parse_result is not None
            assert parser.parse_result.success == True
            
            # Should have extracted some geometry
            assert len(parser.parse_result.vertices) > 0, \
                f"No vertices extracted from {os.path.basename(step_file)}"
    
    def test_parse_dimensions(self, sample_step_files):
        """Test dimension extraction from STEP files"""
        for step_file in sample_step_files:
            parser = EnhancedSTEPParser(step_file)
            parser.load()
            
            if parser.parse_result and parser.parse_result.success:
                dims = parser.parse_result.dimensions
                
                # Dimensions should be positive
                assert dims['x'] > 0, f"Invalid X dimension in {os.path.basename(step_file)}"
                assert dims['y'] > 0, f"Invalid Y dimension in {os.path.basename(step_file)}"
                assert dims['z'] > 0, f"Invalid Z dimension in {os.path.basename(step_file)}"
                
                print(f"\n{os.path.basename(step_file)}: "
                      f"{dims['x']:.2f} × {dims['y']:.2f} × {dims['z']:.2f} mm")
    
    def test_parse_volume_and_area(self, sample_step_files):
        """Test volume and surface area calculation"""
        for step_file in sample_step_files:
            parser = EnhancedSTEPParser(step_file)
            parser.load()
            
            if parser.parse_result and parser.parse_result.success:
                # Volume might be 0 if not watertight
                assert parser.parse_result.volume >= 0
                
                # Surface area should be positive
                assert parser.parse_result.surface_area > 0, \
                    f"Invalid surface area in {os.path.basename(step_file)}"


class TestGeometricEntityExtraction:
    """Test geometric entity extraction"""
    
    @pytest.fixture
    def parsed_step_file(self):
        """Get a parsed STEP file for testing"""
        sample_dir = 'sample_files'
        if not os.path.exists(sample_dir):
            pytest.skip("Sample files directory not found")
        
        step_files = [
            os.path.join(sample_dir, f) 
            for f in os.listdir(sample_dir) 
            if f.endswith('.STEP') or f.endswith('.step')
        ]
        
        if not step_files:
            pytest.skip("No STEP files found")
        
        parser = EnhancedSTEPParser(step_files[0])
        if not parser.load():
            pytest.skip("Failed to parse STEP file")
        
        return parser
    
    def test_extract_vertices(self, parsed_step_file):
        """Test vertex extraction"""
        entities = parsed_step_file.extract_geometric_entities()
        
        assert 'vertices' in entities
        assert len(entities['vertices']) > 0
        
        # Check vertex structure
        vertex = entities['vertices'][0]
        assert hasattr(vertex, 'x')
        assert hasattr(vertex, 'y')
        assert hasattr(vertex, 'z')
        assert hasattr(vertex, 'coordinates')
    
    def test_extract_faces(self, parsed_step_file):
        """Test face extraction"""
        entities = parsed_step_file.extract_geometric_entities()
        
        assert 'faces' in entities
        assert len(entities['faces']) > 0
        
        # Check face structure
        face = entities['faces'][0]
        assert hasattr(face, 'v1_id')
        assert hasattr(face, 'v2_id')
        assert hasattr(face, 'v3_id')
        assert hasattr(face, 'normal')
        assert hasattr(face, 'area')
        
        # Face area should be positive
        assert face.area > 0
    
    def test_face_normals(self, parsed_step_file):
        """Test face normal calculation"""
        entities = parsed_step_file.extract_geometric_entities()
        
        for face in entities['faces']:
            normal = np.array(face.normal)
            
            # Normal should be unit vector (length ≈ 1)
            length = np.linalg.norm(normal)
            assert abs(length - 1.0) < 0.01, f"Normal not unit vector: {length}"


class TestTopologyBuilding:
    """Test topology connectivity graph building"""
    
    @pytest.fixture
    def parsed_step_file(self):
        """Get a parsed STEP file for testing"""
        sample_dir = 'sample_files'
        if not os.path.exists(sample_dir):
            pytest.skip("Sample files directory not found")
        
        step_files = [
            os.path.join(sample_dir, f) 
            for f in os.listdir(sample_dir) 
            if f.endswith('.STEP') or f.endswith('.step')
        ]
        
        if not step_files:
            pytest.skip("No STEP files found")
        
        parser = EnhancedSTEPParser(step_files[0])
        if not parser.load():
            pytest.skip("Failed to parse STEP file")
        
        return parser
    
    def test_build_topology(self, parsed_step_file):
        """Test topology building"""
        topology = parsed_step_file.build_topology()
        
        assert isinstance(topology, dict)
        assert 'vertex_to_edges' in topology
        assert 'edge_to_faces' in topology
        assert 'face_adjacency' in topology


class TestMeshGeneration:
    """Test mesh generation"""
    
    @pytest.fixture
    def parsed_step_file(self):
        """Get a parsed STEP file for testing"""
        sample_dir = 'sample_files'
        if not os.path.exists(sample_dir):
            pytest.skip("Sample files directory not found")
        
        step_files = [
            os.path.join(sample_dir, f) 
            for f in os.listdir(sample_dir) 
            if f.endswith('.STEP') or f.endswith('.step')
        ]
        
        if not step_files:
            pytest.skip("No STEP files found")
        
        parser = EnhancedSTEPParser(step_files[0])
        if not parser.load():
            pytest.skip("Failed to parse STEP file")
        
        return parser
    
    def test_get_mesh(self, parsed_step_file):
        """Test mesh retrieval"""
        mesh = parsed_step_file.get_mesh()
        
        assert mesh is not None
        assert hasattr(mesh, 'vertices')
        assert hasattr(mesh, 'faces')
        assert len(mesh.vertices) > 0
        assert len(mesh.faces) > 0
    
    def test_mesh_properties(self, parsed_step_file):
        """Test mesh properties"""
        mesh = parsed_step_file.get_mesh()
        
        # Check mesh has required properties
        assert hasattr(mesh, 'bounds')
        assert hasattr(mesh, 'area')
        
        # Bounds should be valid
        bounds = mesh.bounds
        assert bounds.shape == (2, 3)
        assert np.all(bounds[1] >= bounds[0])  # max >= min


class TestGeometryValidation:
    """Test geometry validation"""
    
    @pytest.fixture
    def parsed_step_file(self):
        """Get a parsed STEP file for testing"""
        sample_dir = 'sample_files'
        if not os.path.exists(sample_dir):
            pytest.skip("Sample files directory not found")
        
        step_files = [
            os.path.join(sample_dir, f) 
            for f in os.listdir(sample_dir) 
            if f.endswith('.STEP') or f.endswith('.step')
        ]
        
        if not step_files:
            pytest.skip("No STEP files found")
        
        parser = EnhancedSTEPParser(step_files[0])
        if not parser.load():
            pytest.skip("Failed to parse STEP file")
        
        return parser
    
    def test_validate_geometry(self, parsed_step_file):
        """Test geometry validation"""
        is_valid, issues = parsed_step_file.validate_geometry()
        
        # Should return boolean and list
        assert isinstance(is_valid, bool)
        assert isinstance(issues, list)
        
        # If invalid, should have issues
        if not is_valid:
            assert len(issues) > 0
            print(f"\nGeometry issues found: {issues}")


class TestBackwardCompatibility:
    """Test backward compatibility with SimpleCADParser interface"""
    
    @pytest.fixture
    def parsed_step_file(self):
        """Get a parsed STEP file for testing"""
        sample_dir = 'sample_files'
        if not os.path.exists(sample_dir):
            pytest.skip("Sample files directory not found")
        
        step_files = [
            os.path.join(sample_dir, f) 
            for f in os.listdir(sample_dir) 
            if f.endswith('.STEP') or f.endswith('.step')
        ]
        
        if not step_files:
            pytest.skip("No STEP files found")
        
        parser = EnhancedSTEPParser(step_files[0])
        if not parser.load():
            pytest.skip("Failed to parse STEP file")
        
        return parser
    
    def test_get_analysis_summary(self, parsed_step_file):
        """Test get_analysis_summary method"""
        summary = parsed_step_file.get_analysis_summary()
        
        assert isinstance(summary, dict)
        assert 'parsed' in summary
        assert 'dimensions' in summary
        assert 'volume' in summary
        assert 'surface_area' in summary
        
        if summary['parsed']:
            assert summary['dimensions']['x'] > 0
            assert summary['dimensions']['y'] > 0
            assert summary['dimensions']['z'] > 0
    
    def test_get_bounding_box(self, parsed_step_file):
        """Test get_bounding_box method"""
        bbox = parsed_step_file.get_bounding_box()
        
        assert isinstance(bbox, tuple)
        assert len(bbox) == 3
        assert all(dim > 0 for dim in bbox)
    
    def test_get_volume(self, parsed_step_file):
        """Test get_volume method"""
        volume = parsed_step_file.get_volume()
        
        assert isinstance(volume, float)
        assert volume >= 0
    
    def test_get_surface_area(self, parsed_step_file):
        """Test get_surface_area method"""
        area = parsed_step_file.get_surface_area()
        
        assert isinstance(area, float)
        assert area > 0


class TestExtendedInterface:
    """Test new extended interface methods"""
    
    @pytest.fixture
    def parsed_step_file(self):
        """Get a parsed STEP file for testing"""
        sample_dir = 'sample_files'
        if not os.path.exists(sample_dir):
            pytest.skip("Sample files directory not found")
        
        step_files = [
            os.path.join(sample_dir, f) 
            for f in os.listdir(sample_dir) 
            if f.endswith('.STEP') or f.endswith('.step')
        ]
        
        if not step_files:
            pytest.skip("No STEP files found")
        
        parser = EnhancedSTEPParser(step_files[0])
        if not parser.load():
            pytest.skip("Failed to parse STEP file")
        
        return parser
    
    def test_get_vertices(self, parsed_step_file):
        """Test get_vertices method"""
        vertices = parsed_step_file.get_vertices()
        
        assert isinstance(vertices, np.ndarray)
        assert len(vertices) > 0
        assert vertices.shape[1] == 3  # 3D coordinates
    
    def test_get_faces(self, parsed_step_file):
        """Test get_faces method"""
        faces = parsed_step_file.get_faces()
        
        assert isinstance(faces, np.ndarray)
        assert len(faces) > 0
        assert faces.shape[1] == 3  # Triangle faces
    
    def test_get_normals(self, parsed_step_file):
        """Test get_normals method"""
        normals = parsed_step_file.get_normals()
        
        assert isinstance(normals, np.ndarray)
        if len(normals) > 0:
            assert normals.shape[1] == 3  # 3D normal vectors
    
    def test_get_topology(self, parsed_step_file):
        """Test get_topology method"""
        topology = parsed_step_file.get_topology()
        
        assert isinstance(topology, dict)


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_file_path(self):
        """Test with invalid file path"""
        parser = EnhancedSTEPParser('/invalid/path/file.step')
        result = parser.load()
        
        assert result == False
        assert parser.parse_result.success == False
        assert 'not found' in parser.parse_result.error.lower()
    
    def test_empty_file_path(self):
        """Test with empty file path"""
        parser = EnhancedSTEPParser('')
        result = parser.load()
        
        assert result == False
    
    def test_non_step_file(self, tmp_path):
        """Test with non-STEP file"""
        # Create a text file
        test_file = tmp_path / "test.txt"
        test_file.write_text("This is not a STEP file")
        
        parser = EnhancedSTEPParser(str(test_file))
        result = parser.load()
        
        # Should fail gracefully
        assert result == False
        assert parser.parse_result.success == False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
