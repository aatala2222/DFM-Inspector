"""
Basic tests for DFM Inspector
"""
import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import DFMInspector
from rules.manufacturing_rules import ManufacturingRules


class TestManufacturingRules(unittest.TestCase):
    """Test manufacturing rules"""
    
    def test_get_injection_molding_rules(self):
        """Test getting injection molding rules"""
        rules = ManufacturingRules.get_rules_by_process('injection_molding')
        self.assertGreater(len(rules), 0)
        self.assertEqual(rules[0].category, 'Wall Thickness')
    
    def test_get_cnc_rules(self):
        """Test getting CNC machining rules"""
        rules = ManufacturingRules.get_rules_by_process('cnc_machining')
        self.assertGreater(len(rules), 0)
    
    def test_get_robotics_rules(self):
        """Test getting robotics-specific rules"""
        rules = ManufacturingRules.get_rules_by_process('robotics')
        self.assertGreater(len(rules), 0)
    
    def test_get_rule_by_name(self):
        """Test getting specific rule by name"""
        rule = ManufacturingRules.get_rule_by_name('min_wall_thickness')
        self.assertIsNotNone(rule)
        self.assertEqual(rule.name, 'min_wall_thickness')
        self.assertEqual(rule.threshold, 1.5)
    
    def test_get_all_rules(self):
        """Test getting all rules"""
        rules = ManufacturingRules.get_all_rules()
        self.assertGreater(len(rules), 5)


class TestDFMInspector(unittest.TestCase):
    """Test DFM Inspector"""
    
    def test_inspector_initialization(self):
        """Test inspector can be initialized"""
        inspector = DFMInspector('config/inspection_rules.yaml')
        self.assertIsNotNone(inspector.rules)
        self.assertIn('wall_thickness', inspector.rules)
    
    def test_rules_loaded(self):
        """Test rules are loaded correctly"""
        inspector = DFMInspector('config/inspection_rules.yaml')
        self.assertEqual(inspector.rules['wall_thickness']['min_thickness'], 1.5)
        self.assertEqual(inspector.rules['draft_angles']['min_draft_smooth'], 1.0)
    
    def test_calculate_score(self):
        """Test score calculation"""
        inspector = DFMInspector('config/inspection_rules.yaml')
        
        # Test with no issues
        results = {'issues': [], 'warnings': [], 'passed': [1, 2, 3]}
        score = inspector._calculate_score(results)
        self.assertGreater(score, 0)
        
        # Test with issues
        results = {'issues': [1, 2], 'warnings': [1], 'passed': [1]}
        score = inspector._calculate_score(results)
        self.assertLess(score, 100)


if __name__ == '__main__':
    unittest.main()
