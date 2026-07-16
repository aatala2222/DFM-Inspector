"""
Enhanced DFM Workflow - Complete Analysis Pipeline

Orchestrates the complete analysis workflow:
1. Parse STEP file
2. Analyze geometry (wall thickness)
3. Detect features (holes, corners, pockets)
4. Check DFM rules
5. Generate violations with 3D coordinates
6. Prepare for visualization
"""
import logging
from typing import Dict, Optional
from src.enhanced_step_parser import EnhancedSTEPParser
from src.mesh_analyzer import MeshAnalyzer
from src.geometry_analyzer import GeometryAnalyzer
from src.feature_detector import FeatureDetector
from src.dfm_feature_integration import DFMFeatureIntegration

logger = logging.getLogger(__name__)


class EnhancedDFMWorkflow:
    """
    Complete DFM analysis workflow with feature detection
    
    Provides end-to-end analysis from STEP file to DFM violations
    with 3D coordinates for visualization.
    """
    
    def __init__(self, filepath: str, process: str, material: str):
        """
        Initialize enhanced DFM workflow
        
        Args:
            filepath: Path to STEP file
            process: Manufacturing process
            material: Material name
        """
        self.filepath = filepath
        self.process = process
        self.material = material
        
        # Components
        self.parser = None
        self.mesh_analyzer = None
        self.geometry_analyzer = None
        self.feature_detector = None
        self.dfm_integration = None
        
        # Results
        self.results = {}
        
        logger.info(f"Initialized Enhanced DFM Workflow")
        logger.info(f"  File: {filepath}")
        logger.info(f"  Process: {process}")
        logger.info(f"  Material: {material}")
    
    def run_complete_analysis(self, 
                             detect_features: bool = True,
                             measure_thickness: bool = True,
                             sample_density: int = 1000) -> Dict:
        """
        Run complete DFM analysis workflow
        
        Args:
            detect_features: Enable feature detection
            measure_thickness: Enable wall thickness measurement
            sample_density: Sampling density for thickness measurement
            
        Returns:
            Complete analysis results with violations
        """
        logger.info("=" * 70)
        logger.info("ENHANCED DFM ANALYSIS WORKFLOW")
        logger.info("=" * 70)
        
        try:
            # Step 1: Parse STEP file
            logger.info("\n[1/6] Parsing STEP file...")
            self.parser = EnhancedSTEPParser(self.filepath)
            parse_success = self.parser.load()
            
            if not parse_success:
                return self._error_result("Failed to parse STEP file")
            
            logger.info(f"✓ Parsed successfully")
            
            # Step 2: Analyze mesh quality
            logger.info("\n[2/6] Analyzing mesh quality...")
            if self.parser.mesh:
                self.mesh_analyzer = MeshAnalyzer(self.parser.mesh)
                mesh_quality = self.mesh_analyzer.analyze_quality()
                logger.info(f"✓ Mesh quality: {mesh_quality.get('quality_rating')}")
            else:
                mesh_quality = {}
                logger.warning("⚠ No mesh available for quality analysis")
            
            # Step 3: Measure geometry (wall thickness)
            logger.info("\n[3/6] Measuring geometry...")
            thickness_result = None
            if measure_thickness and self.parser.mesh:
                self.geometry_analyzer = GeometryAnalyzer(self.parser.mesh)
                thickness_result = self.geometry_analyzer.measure_wall_thickness(
                    sample_density=sample_density
                )
                logger.info(f"✓ Wall thickness measured: {thickness_result['samples']} samples")
                logger.info(f"  Min thickness: {thickness_result['min_thickness']:.3f}mm at {thickness_result['min_location']}")
            else:
                logger.info("⏭ Skipping wall thickness measurement")
            
            # Step 4: Detect features
            logger.info("\n[4/6] Detecting features...")
            holes = []
            corners = []
            pockets = []
            
            if detect_features and self.parser.mesh:
                self.feature_detector = FeatureDetector(self.parser.mesh)
                features = self.feature_detector.detect_all_features(
                    detect_holes=True,
                    detect_corners=True,
                    detect_pockets=False,  # Simplified for now
                    detect_bosses=False,
                    detect_ribs=False
                )
                
                holes = self.feature_detector.get_features_by_type('hole')
                corners = self.feature_detector.get_features_by_type('corner')
                pockets = self.feature_detector.get_features_by_type('pocket')
                
                logger.info(f"✓ Features detected:")
                logger.info(f"  Holes: {len(holes)}")
                logger.info(f"  Corners: {len(corners)}")
                logger.info(f"  Pockets: {len(pockets)}")
            else:
                logger.info("⏭ Skipping feature detection")
            
            # Step 5: Check DFM rules
            logger.info("\n[5/6] Checking DFM rules...")
            self.dfm_integration = DFMFeatureIntegration(self.process, self.material)
            
            violation_summary = self.dfm_integration.analyze_all_features(
                geometry_analyzer=self.geometry_analyzer,
                holes=holes,
                corners=corners,
                pockets=pockets
            )
            
            logger.info(f"✓ DFM analysis complete:")
            logger.info(f"  Total violations: {violation_summary['total_violations']}")
            logger.info(f"  Critical: {violation_summary['by_severity']['critical']}")
            logger.info(f"  Warnings: {violation_summary['by_severity']['warning']}")
            
            # Step 6: Prepare results
            logger.info("\n[6/6] Preparing results...")
            
            # Get geometry summary
            geometry_summary = self.parser.get_analysis_summary()
            
            # Add thickness info if available
            if thickness_result:
                geometry_summary['wall_thickness'] = {
                    'min': thickness_result['min_thickness'],
                    'max': thickness_result['max_thickness'],
                    'avg': thickness_result['avg_thickness'],
                    'min_location': thickness_result['min_location'],
                    'samples': thickness_result['samples']
                }
            
            # Build complete results
            self.results = {
                'success': True,
                'process': self.process,
                'material': self.material,
                'geometry': geometry_summary,
                'mesh_quality': mesh_quality,
                'features': {
                    'holes': [self._feature_to_dict(h) for h in holes],
                    'corners': [self._feature_to_dict(c) for c in corners],
                    'pockets': [self._feature_to_dict(p) for p in pockets],
                    'total': len(holes) + len(corners) + len(pockets)
                },
                'violations': violation_summary,
                'visualization_data': self.dfm_integration.get_violations_for_visualization(),
                'parser': self.parser,  # Keep for visualization
                'components': {
                    'geometry_analyzer': self.geometry_analyzer,
                    'feature_detector': self.feature_detector,
                    'dfm_integration': self.dfm_integration
                }
            }
            
            logger.info("✓ Results prepared")
            logger.info("=" * 70)
            logger.info("✅ ENHANCED DFM ANALYSIS COMPLETE")
            logger.info("=" * 70)
            
            return self.results
            
        except Exception as e:
            logger.error(f"Error in enhanced DFM workflow: {e}")
            import traceback
            traceback.print_exc()
            return self._error_result(str(e))
    
    def _feature_to_dict(self, feature) -> Dict:
        """Convert feature to dictionary"""
        return {
            'type': feature.feature_type,
            'center': feature.center,
            'dimensions': feature.dimensions,
            'confidence': feature.confidence
        }
    
    def _error_result(self, error_message: str) -> Dict:
        """Generate error result"""
        return {
            'success': False,
            'error': error_message,
            'process': self.process,
            'material': self.material
        }
    
    def get_violations_by_severity(self, severity: str) -> list:
        """Get violations filtered by severity"""
        if not self.dfm_integration:
            return []
        
        return [v for v in self.dfm_integration.violations if v.severity == severity]
    
    def get_critical_violations(self) -> list:
        """Get critical violations only"""
        return self.get_violations_by_severity('critical')
    
    def get_warning_violations(self) -> list:
        """Get warning violations only"""
        return self.get_violations_by_severity('warning')
