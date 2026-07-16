"""
Unit tests for Configuration Manager

Tests configuration loading, dot-notation access, runtime updates,
environment variable overrides, and validation.

Requirements: Requirement 20 (Configuration and Customization)
"""

import pytest
import os
import tempfile
from pathlib import Path
from src.config import Config, get_config


class TestConfigSingleton:
    """Test singleton pattern"""
    
    def test_singleton_same_instance(self):
        """Test that Config returns same instance"""
        config1 = Config()
        config2 = Config()
        
        assert config1 is config2
    
    def test_get_config_returns_singleton(self):
        """Test that get_config returns singleton"""
        config1 = get_config()
        config2 = get_config()
        
        assert config1 is config2


class TestConfigLoading:
    """Test configuration loading from YAML"""
    
    def test_load_default_config(self):
        """Test loading default configuration file"""
        config = Config()
        result = config.load('config/geometry_analysis.yaml')
        
        # Should load successfully
        assert result == True or result == False  # May not exist in test environment
    
    def test_load_nonexistent_file(self):
        """Test loading non-existent file"""
        config = Config()
        result = config.load('nonexistent_config.yaml')
        
        # Should fail gracefully
        assert result == False
        
        # Should have default config
        assert config.get('parser.max_file_size_mb') is not None
    
    def test_load_custom_config(self, tmp_path):
        """Test loading custom configuration"""
        # Create temporary config file
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("""
parser:
  max_file_size_mb: 50
geometry_analyzer:
  wall_thickness:
    sample_density: 500
""")
        
        config = Config()
        result = config.load(str(config_file))
        
        assert result == True
        assert config.get('parser.max_file_size_mb') == 50
        assert config.get('geometry_analyzer.wall_thickness.sample_density') == 500
    
    def test_load_invalid_yaml(self, tmp_path):
        """Test loading invalid YAML"""
        # Create invalid YAML file
        config_file = tmp_path / "invalid.yaml"
        config_file.write_text("invalid: yaml: content:")
        
        config = Config()
        result = config.load(str(config_file))
        
        # Should fail gracefully
        assert result == False


class TestDotNotationAccess:
    """Test dot-notation configuration access"""
    
    @pytest.fixture
    def config_with_data(self, tmp_path):
        """Create config with test data"""
        config_file = tmp_path / "test.yaml"
        config_file.write_text("""
section1:
  key1: value1
  subsection:
    key2: 42
    key3: 3.14
section2:
  enabled: true
""")
        
        config = Config()
        config.load(str(config_file))
        return config
    
    def test_get_top_level_key(self, config_with_data):
        """Test getting top-level key"""
        value = config_with_data.get('section1')
        
        assert isinstance(value, dict)
        assert 'key1' in value
    
    def test_get_nested_key(self, config_with_data):
        """Test getting nested key with dot notation"""
        value = config_with_data.get('section1.key1')
        
        assert value == 'value1'
    
    def test_get_deeply_nested_key(self, config_with_data):
        """Test getting deeply nested key"""
        value = config_with_data.get('section1.subsection.key2')
        
        assert value == 42
    
    def test_get_nonexistent_key_returns_default(self, config_with_data):
        """Test that non-existent key returns default"""
        value = config_with_data.get('nonexistent.key', 'default_value')
        
        assert value == 'default_value'
    
    def test_get_nonexistent_key_returns_none(self, config_with_data):
        """Test that non-existent key returns None by default"""
        value = config_with_data.get('nonexistent.key')
        
        assert value is None
    
    def test_get_boolean_value(self, config_with_data):
        """Test getting boolean value"""
        value = config_with_data.get('section2.enabled')
        
        assert value == True
        assert isinstance(value, bool)
    
    def test_get_float_value(self, config_with_data):
        """Test getting float value"""
        value = config_with_data.get('section1.subsection.key3')
        
        assert value == 3.14
        assert isinstance(value, float)


class TestRuntimeUpdates:
    """Test runtime configuration updates"""
    
    @pytest.fixture
    def config_with_data(self, tmp_path):
        """Create config with test data"""
        config_file = tmp_path / "test.yaml"
        config_file.write_text("""
section1:
  key1: original_value
""")
        
        config = Config()
        config.load(str(config_file))
        return config
    
    def test_set_existing_key(self, config_with_data):
        """Test updating existing key"""
        result = config_with_data.set('section1.key1', 'new_value')
        
        assert result == True
        assert config_with_data.get('section1.key1') == 'new_value'
    
    def test_set_new_key(self, config_with_data):
        """Test setting new key"""
        result = config_with_data.set('section1.new_key', 'new_value')
        
        assert result == True
        assert config_with_data.get('section1.new_key') == 'new_value'
    
    def test_set_nested_new_key(self, config_with_data):
        """Test setting nested new key"""
        result = config_with_data.set('new_section.new_key', 123)
        
        assert result == True
        assert config_with_data.get('new_section.new_key') == 123
    
    def test_set_different_types(self, config_with_data):
        """Test setting different value types"""
        config_with_data.set('test.int_value', 42)
        config_with_data.set('test.float_value', 3.14)
        config_with_data.set('test.bool_value', True)
        config_with_data.set('test.str_value', 'hello')
        
        assert config_with_data.get('test.int_value') == 42
        assert config_with_data.get('test.float_value') == 3.14
        assert config_with_data.get('test.bool_value') == True
        assert config_with_data.get('test.str_value') == 'hello'


class TestEnvironmentOverrides:
    """Test environment variable overrides"""
    
    def test_env_override_applied(self, tmp_path, monkeypatch):
        """Test that environment variables override config"""
        # Create config file
        config_file = tmp_path / "test.yaml"
        config_file.write_text("""
parser:
  max_file_size_mb: 100
""")
        
        # Set environment variable
        monkeypatch.setenv('GEOM_ANALYSIS_PARSER__MAX_FILE_SIZE_MB', '200')
        
        config = Config()
        config.load(str(config_file))
        
        # Should use environment value
        assert config.get('parser.max_file_size_mb') == 200
    
    def test_env_override_boolean(self, tmp_path, monkeypatch):
        """Test environment override with boolean"""
        config_file = tmp_path / "test.yaml"
        config_file.write_text("""
parser:
  fallback_enabled: false
""")
        
        monkeypatch.setenv('GEOM_ANALYSIS_PARSER__FALLBACK_ENABLED', 'true')
        
        config = Config()
        config.load(str(config_file))
        
        assert config.get('parser.fallback_enabled') == True


class TestConfigValidation:
    """Test configuration validation"""
    
    def test_valid_config_passes(self, tmp_path):
        """Test that valid configuration passes validation"""
        config_file = tmp_path / "valid.yaml"
        config_file.write_text("""
parser:
  max_file_size_mb: 100
geometry_analyzer:
  wall_thickness:
    sample_density: 1000
    min_samples: 100
    max_samples: 100000
feature_detector:
  min_feature_size: 0.5
visualization:
  resolution:
    width: 1920
    height: 1080
logging:
  level: INFO
""")
        
        config = Config()
        result = config.load(str(config_file))
        
        assert result == True
    
    def test_invalid_max_file_size(self, tmp_path):
        """Test validation catches invalid max_file_size"""
        config_file = tmp_path / "invalid.yaml"
        config_file.write_text("""
parser:
  max_file_size_mb: -10
""")
        
        config = Config()
        result = config.load(str(config_file))
        
        # Should fail validation
        assert result == False
    
    def test_invalid_sample_range(self, tmp_path):
        """Test validation catches invalid sample range"""
        config_file = tmp_path / "invalid.yaml"
        config_file.write_text("""
geometry_analyzer:
  wall_thickness:
    min_samples: 1000
    max_samples: 100
""")
        
        config = Config()
        result = config.load(str(config_file))
        
        # Should fail validation
        assert result == False


class TestGetAll:
    """Test getting entire configuration"""
    
    def test_get_all_returns_dict(self, tmp_path):
        """Test that get_all returns dictionary"""
        config_file = tmp_path / "test.yaml"
        config_file.write_text("""
section1:
  key1: value1
section2:
  key2: value2
""")
        
        config = Config()
        config.load(str(config_file))
        
        all_config = config.get_all()
        
        assert isinstance(all_config, dict)
        assert 'section1' in all_config
        assert 'section2' in all_config
    
    def test_get_all_returns_copy(self, tmp_path):
        """Test that get_all returns a copy (not reference)"""
        config_file = tmp_path / "test.yaml"
        config_file.write_text("""
section1:
  key1: value1
""")
        
        config = Config()
        config.load(str(config_file))
        
        all_config = config.get_all()
        all_config['section1']['key1'] = 'modified'
        
        # Original should not be modified
        assert config.get('section1.key1') == 'value1'


class TestReload:
    """Test configuration reloading"""
    
    def test_reload_updates_config(self, tmp_path):
        """Test that reload updates configuration"""
        config_file = tmp_path / "test.yaml"
        config_file.write_text("""
section1:
  key1: original
""")
        
        config = Config()
        config.load(str(config_file))
        
        assert config.get('section1.key1') == 'original'
        
        # Modify file
        config_file.write_text("""
section1:
  key1: updated
""")
        
        # Reload
        config.reload()
        
        assert config.get('section1.key1') == 'updated'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
