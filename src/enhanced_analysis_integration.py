"""
Integration layer for Enhanced 3D Geometry Analysis

This module integrates the Enhanced STEP Parser and Mesh Analyzer
with the existing Flask application.
"""

import logging
from typing import Dict, Any, Optional
from src.enhanced_step_parser import EnhancedSTEPParser
from src.mesh_analyzer import MeshAnalyzer
from src.config import get_config

logger = logging.getLogger(__name__)


def analyze_with_enhanced_parser(filepath: str) -> Dict[str, Any]:
    """
    Analyze CAD file using Enhanced STEP Parser and Mesh Analyzer
    
    Args:
        filepath: Path to STEP file
        
    Returns:
        Dictionary with analysis results
    """
    try:
        # Load configuration
        config = get_config()
        
        # Parse STEP file
        logger.info(f"Parsing file with Enhanced STEP Parser: {filepath}")
        parser = EnhancedSTEPParser(filepath)
        parse_success = parser.load()
        
        if not parse_success:
            return {
                'success': False,
                'error': 'Failed to parse STEP file',
                'parser_used': 'EnhancedSTEPParser',
                'fallback_available': True
            }
        
        # Get geometry summary
        geometry = parser.get_analysis_summary()
        
        # Analyze mesh quality if available
        mesh_quality = None
        if parser.mesh is not None:
            logger.info("Analyzing mesh quality...")
            analyzer = MeshAnalyzer(parser.mesh)
            mesh_quality = analyzer.analyze_quality()
            
            # Get quality report
            quality_report = analyzer.get_quality_report()
        
        # Build comprehensive result
        result = {
            'success': True,
            'parser_used': 'EnhancedSTEPParser',
            'geometry': geometry,
            'mesh_quality': mesh_quality,
            'quality_report': quality_report if mesh_quality else None,
            'parser': parser,  # Keep for later use
            'capabilities': {
                'accurate_measurements': True,
                'feature_detection': False,  # Not yet implemented
                'wall_thickness_measurement': False,  # Not yet implemented
                'visualization': False  # Not yet implemented
            }
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error in enhanced analysis: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e),
            'parser_used': 'EnhancedSTEPParser',
            'fallback_available': True
        }


def get_enhanced_geometry_info(parser: EnhancedSTEPParser) -> Dict[str, Any]:
    """
    Extract detailed geometry information from Enhanced STEP Parser
    
    Args:
        parser: EnhancedSTEPParser instance
        
    Returns:
        Dictionary with detailed geometry info
    """
    try:
        info = {
            'dimensions': parser.parse_result.dimensions if parser.parse_result else {},
            'volume': parser.parse_result.volume if parser.parse_result else 0,
            'surface_area': parser.parse_result.surface_area if parser.parse_result else 0,
            'vertex_count': len(parser.parse_result.vertices) if parser.parse_result else 0,
            'face_count': len(parser.parse_result.faces) if parser.parse_result else 0,
            'is_watertight': parser.mesh.is_watertight if parser.mesh else False,
            'parser_method': 'Enhanced (Multi-method)',
            'accuracy': '±0.01mm'
        }
        
        return info
        
    except Exception as e:
        logger.error(f"Error extracting geometry info: {e}")
        return {}


def format_mesh_quality_for_display(mesh_quality: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format mesh quality metrics for display in UI
    
    Args:
        mesh_quality: Raw mesh quality metrics
        
    Returns:
        Formatted metrics for display
    """
    if not mesh_quality:
        return {}
    
    return {
        'overall_rating': mesh_quality.get('quality_rating', 'Unknown'),
        'is_watertight': '✓ Yes' if mesh_quality.get('is_watertight') else '✗ No',
        'is_manifold': '✓ Yes' if mesh_quality.get('is_manifold') else '✗ No',
        'vertex_count': f"{mesh_quality.get('vertex_count', 0):,}",
        'face_count': f"{mesh_quality.get('face_count', 0):,}",
        'avg_quality': f"{mesh_quality.get('avg_triangle_quality', 0):.3f}",
        'defects': {
            'degenerate_faces': mesh_quality.get('degenerate_faces', 0),
            'non_manifold_edges': mesh_quality.get('non_manifold_edges', 0)
        },
        'volume': f"{mesh_quality.get('volume', 0):.2f} mm³",
        'surface_area': f"{mesh_quality.get('surface_area', 0):.2f} mm²"
    }
