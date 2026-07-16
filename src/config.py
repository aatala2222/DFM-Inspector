"""
Configuration Manager for Enhanced 3D Geometry Analysis

This module implements a singleton configuration manager that loads settings from
YAML files, supports dot-notation access, runtime updates, and environment variable
overrides.

Requirements: Requirement 20 (Configuration and Customization)
Design Reference: Section "Configuration Design"
"""

import os
import logging
import copy
from typing import Dict, Any, Optional
from pathlib import Path
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Config:
    """
    Singleton configuration manager for geometry analysis
    
    Features:
    - Singleton pattern (one instance per application)
    - YAML configuration loading
    - Dot-notation access (e.g., 'parser.max_file_size_mb')
    - Runtime configuration updates
    - Environment variable overrides
    - Configuration validation
    
    Requirements: Requirement 20 (Configuration and Customization)
    """
    
    _instance: Optional['Config'] = None
    _config: Optional[Dict[str, Any]] = None
    _config_path: Optional[str] = None
    
    def __new__(cls):
        """Implement singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize configuration (only once due to singleton)"""
        if not self._initialized:
            self._config = {}
            self._config_path = None
            self._initialized = True
            logger.debug("Config instance created")
    
    def load(self, config_path: str = "config/geometry_analysis.yaml") -> bool:
        """
        Load configuration from YAML file
        
        Args:
            config_path: Path to YAML configuration file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Resolve path
            if not os.path.isabs(config_path):
                # Try relative to current directory
                if os.path.exists(config_path):
                    full_path = config_path
                else:
                    # Try relative to script directory
                    script_dir = Path(__file__).parent.parent
                    full_path = script_dir / config_path
            else:
                full_path = config_path
            
            # Load YAML
            with open(full_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
            
            self._config_path = str(full_path)
            
            logger.info(f"✓ Configuration loaded from: {full_path}")
            
            # Apply environment variable overrides
            self._apply_env_overrides()
            
            # Validate configuration
            is_valid = self._validate()
            
            if is_valid:
                logger.info("✓ Configuration validated successfully")
            
            return is_valid
            
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            # Load default empty config
            self._config = self._get_default_config()
            return False
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML configuration: {e}")
            self._config = self._get_default_config()
            return False
        except Exception as e:
            logger.error(f"Error loading configuration: {e}", exc_info=True)
            self._config = self._get_default_config()
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key_path: Dot-separated path to configuration value
                     Example: 'geometry_analyzer.wall_thickness.sample_density'
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        if self._config is None:
            logger.warning("Configuration not loaded, loading defaults")
            self.load()
        
        keys = key_path.split('.')
        value = self._config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any) -> bool:
        """
        Set configuration value at runtime using dot notation
        
        Args:
            key_path: Dot-separated path to configuration value
            value: New value to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self._config is None:
                logger.warning("Configuration not loaded, loading defaults")
                self.load()
            
            keys = key_path.split('.')
            config = self._config
            
            # Navigate to parent of target key
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            
            # Set the value
            config[keys[-1]] = value
            
            logger.debug(f"Configuration updated: {key_path} = {value}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting configuration value: {e}")
            return False
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get entire configuration dictionary
        
        Returns:
            Complete configuration dictionary (deep copy)
        """
        if self._config is None:
            logger.warning("Configuration not loaded, loading defaults")
            self.load()
        
        return copy.deepcopy(self._config)
    
    def reload(self) -> bool:
        """
        Reload configuration from file
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self._config_path:
            return self.load(self._config_path)
        else:
            logger.warning("No configuration file path set, cannot reload")
            return False
    
    def _apply_env_overrides(self):
        """
        Apply environment variable overrides.

        Environment variables in the format ``GEOM_ANALYSIS_<DOTTED_PATH>=value``
        override the corresponding dotted configuration key. Section boundaries
        in the dotted path are encoded as a **double underscore** (``__``); a
        single underscore inside a key name is preserved verbatim. This is
        required because real configuration keys (e.g. ``max_file_size_mb``)
        themselves contain single underscores.

        Translation rules:

        1. The variable name MUST start with the ``GEOM_ANALYSIS_`` prefix.
        2. The remainder is lowercased.
        3. Each occurrence of ``__`` (double underscore) becomes ``.`` — this
           is the section separator.
        4. Single underscores are left untouched (they are part of the key
           name itself).

        Worked examples:

        +-----------------------------------------------------------------------+-----------------------------------------------+
        | Env var                                                               | Resolved key                                  |
        +=======================================================================+===============================================+
        | ``GEOM_ANALYSIS_PARSER__MAX_FILE_SIZE_MB=42``                         | ``parser.max_file_size_mb``                   |
        +-----------------------------------------------------------------------+-----------------------------------------------+
        | ``GEOM_ANALYSIS_PARSER__FALLBACK_ENABLED=true``                       | ``parser.fallback_enabled``                   |
        +-----------------------------------------------------------------------+-----------------------------------------------+
        | ``GEOM_ANALYSIS_GEOMETRY_ANALYZER__WALL_THICKNESS__SAMPLE_DENSITY=2000`` | ``geometry_analyzer.wall_thickness.sample_density`` |
        +-----------------------------------------------------------------------+-----------------------------------------------+

        Values are parsed as ``bool`` (``"true"``/``"false"``, case-insensitive)
        first, then ``float`` (if a ``.`` is present), then ``int``, falling
        back to the raw string.
        """
        try:
            prefix = "GEOM_ANALYSIS_"
            
            for env_key, env_value in os.environ.items():
                if env_key.startswith(prefix):
                    # Strip the prefix and lowercase. Only '__' acts as a
                    # section separator; single underscores are preserved as
                    # part of the key name (e.g. 'max_file_size_mb').
                    suffix = env_key[len(prefix):].lower()
                    config_key = suffix.replace('__', '.')
                    
                    # Try to parse value as int, float, or bool
                    try:
                        if env_value.lower() in ('true', 'false'):
                            parsed_value = env_value.lower() == 'true'
                        elif '.' in env_value:
                            parsed_value = float(env_value)
                        else:
                            parsed_value = int(env_value)
                    except ValueError:
                        parsed_value = env_value
                    
                    # Set the value
                    self.set(config_key, parsed_value)
                    logger.debug(f"Applied environment override: {config_key} = {parsed_value}")
        
        except Exception as e:
            logger.warning(f"Error applying environment overrides: {e}")
    
    def _validate(self) -> bool:
        """
        Validate configuration values
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            is_valid = True
            
            # Validate parser settings
            max_file_size = self.get('parser.max_file_size_mb', 100)
            if max_file_size <= 0:
                logger.error("Invalid parser.max_file_size_mb: must be positive")
                is_valid = False
            
            # Validate geometry analyzer settings
            sample_density = self.get('geometry_analyzer.wall_thickness.sample_density', 1000)
            if sample_density <= 0:
                logger.error("Invalid sample_density: must be positive")
                is_valid = False
            
            min_samples = self.get('geometry_analyzer.wall_thickness.min_samples', 100)
            max_samples = self.get('geometry_analyzer.wall_thickness.max_samples', 100000)
            if min_samples > max_samples:
                logger.error("Invalid sample range: min_samples > max_samples")
                is_valid = False
            
            # Validate feature detector settings
            min_feature_size = self.get('feature_detector.min_feature_size', 0.5)
            if min_feature_size <= 0:
                logger.error("Invalid min_feature_size: must be positive")
                is_valid = False
            
            # Validate visualization settings
            width = self.get('visualization.resolution.width', 1920)
            height = self.get('visualization.resolution.height', 1080)
            if width <= 0 or height <= 0:
                logger.error("Invalid resolution: width and height must be positive")
                is_valid = False
            
            # Validate logging level
            log_level = self.get('logging.level', 'INFO')
            valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if log_level not in valid_levels:
                logger.warning(f"Invalid logging level: {log_level}, using INFO")
                self.set('logging.level', 'INFO')
            
            return is_valid
            
        except Exception as e:
            logger.error(f"Error validating configuration: {e}")
            return False
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get minimal default configuration
        
        Returns:
            Default configuration dictionary
        """
        return {
            'parser': {
                'supported_formats': ['AP203', 'AP214'],
                'fallback_enabled': True,
                'max_file_size_mb': 100
            },
            'geometry_analyzer': {
                'wall_thickness': {
                    'sample_density': 1000,
                    'min_samples': 100,
                    'max_samples': 100000,
                    'measurement_tolerance': 0.01
                }
            },
            'feature_detector': {
                'min_feature_size': 0.5
            },
            'mesh_analyzer': {
                'quality': {
                    'min_triangle_quality': 0.3
                },
                'repair': {
                    'auto_repair_enabled': True
                }
            },
            'visualization': {
                'resolution': {
                    'width': 1920,
                    'height': 1080,
                    'dpi': 200
                }
            },
            'performance': {
                'parallel_processing': True,
                'num_workers': -1
            },
            'logging': {
                'level': 'INFO',
                'console': True
            }
        }
    
    def __repr__(self) -> str:
        """String representation"""
        if self._config_path:
            return f"Config(loaded_from='{self._config_path}')"
        else:
            return "Config(not_loaded)"


# Global config instance
_global_config = None

def get_config() -> Config:
    """
    Get global configuration instance
    
    Returns:
        Config: Singleton configuration instance
    """
    global _global_config
    if _global_config is None:
        _global_config = Config()
        # Try to load default configuration
        _global_config.load()
    return _global_config
