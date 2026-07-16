"""
DFM Inspector - Design for Manufacturability inspection tool
"""
from .cad_parser import CADParser
from .dfm_inspector import DFMInspector
from .report_generator import ReportGenerator
from .visualization import DFMVisualizer

__version__ = '1.0.0'
__all__ = ['CADParser', 'DFMInspector', 'ReportGenerator', 'DFMVisualizer']
