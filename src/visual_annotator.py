"""
Visual Annotation Generator for DFM Analysis
Creates annotated images showing problem areas in CAD geometry
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Arrow
import numpy as np
from typing import Dict, List, Tuple
import os
import tempfile


class VisualAnnotator:
    """Generate annotated images for DFM analysis"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.images = []
    
    def create_hole_annotation(self, geometry: Dict, holes: List[Dict], 
                              failed_holes: List[Dict], rule_name: str) -> str:
        """
        Create annotated image showing problematic holes
        
        Args:
            geometry: Geometry information with dimensions
            holes: List of all holes
            failed_holes: List of holes that failed the rule
            rule_name: Name of the rule being visualized
            
        Returns:
            Path to generated image
        """
        if not holes:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Get part dimensions
        dims = geometry.get('dimensions', {})
        width = dims.get('x', 100)
        height = dims.get('y', 100)
        
        # Draw part outline
        part_rect = Rectangle((0, 0), width, height, 
                              fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(part_rect)
        
        # Draw all holes (green = pass, red = fail)
        for hole in holes:
            center = hole.get('center', {})
            x = center.get('x', 0)
            y = center.get('y', 0)
            diameter = hole.get('diameter', 5)
            radius = diameter / 2
            
            # Check if this hole failed
            is_failed = any(
                abs(fh.get('center', {}).get('x', -999) - x) < 0.1 and
                abs(fh.get('center', {}).get('y', -999) - y) < 0.1
                for fh in failed_holes
            )
            
            color = 'red' if is_failed else 'green'
            alpha = 0.7 if is_failed else 0.3
            
            circle = Circle((x, y), radius, 
                          fill=True, facecolor=color, 
                          edgecolor=color, alpha=alpha, linewidth=2)
            ax.add_patch(circle)
            
            # Add label for failed holes
            if is_failed:
                ax.annotate(f'Ø{diameter:.1f}mm', 
                          xy=(x, y), xytext=(x + radius + 5, y + radius + 5),
                          fontsize=9, color='red', weight='bold',
                          bbox=dict(boxstyle='round,pad=0.3', 
                                  facecolor='white', edgecolor='red'))
        
        # Set axis properties
        ax.set_xlim(-10, width + 10)
        ax.set_ylim(-10, height + 10)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('X (mm)', fontsize=10)
        ax.set_ylabel('Y (mm)', fontsize=10)
        
        # Add title
        title = f'{rule_name}\n'
        title += f'Red = Failed ({len(failed_holes)}), Green = Passed ({len(holes) - len(failed_holes)})'
        ax.set_title(title, fontsize=12, weight='bold', pad=15)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='red', alpha=0.7, label='Failed'),
            Patch(facecolor='green', alpha=0.3, label='Passed'),
            Patch(facecolor='none', edgecolor='black', linewidth=2, label='Part Outline')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=9)
        
        # Save image
        filename = os.path.join(self.temp_dir, f'annotation_{rule_name.replace(" ", "_")}.png')
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        
        self.images.append(filename)
        return filename
    
    def create_thickness_annotation(self, geometry: Dict, min_thickness: float,
                                   threshold: float, rule_name: str) -> str:
        """
        Create annotated image showing wall thickness issues
        
        Args:
            geometry: Geometry information
            min_thickness: Measured minimum thickness
            threshold: Threshold value for the rule
            rule_name: Name of the rule
            
        Returns:
            Path to generated image
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create bar chart comparing thickness
        categories = ['Measured\nThickness', 'Minimum\nRequired', 'Recommended']
        values = [min_thickness, threshold, threshold * 1.5]
        colors = ['red' if min_thickness < threshold else 'green', 'orange', 'green']
        
        bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.2f}mm',
                   ha='center', va='bottom', fontsize=12, weight='bold')
        
        # Add threshold line
        ax.axhline(y=threshold, color='red', linestyle='--', linewidth=2, 
                  label=f'Minimum Threshold: {threshold:.2f}mm')
        
        # Styling
        ax.set_ylabel('Thickness (mm)', fontsize=12, weight='bold')
        ax.set_title(rule_name, fontsize=14, weight='bold', pad=15)
        ax.legend(fontsize=10)
        ax.grid(True, axis='y', alpha=0.3)
        
        # Add status text
        status = 'PASS ✓' if min_thickness >= threshold else 'FAIL ✗'
        status_color = 'green' if min_thickness >= threshold else 'red'
        ax.text(0.5, 0.95, status, transform=ax.transAxes,
               fontsize=16, weight='bold', color=status_color,
               ha='center', va='top',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                        edgecolor=status_color, linewidth=2))
        
        # Save image
        filename = os.path.join(self.temp_dir, f'annotation_{rule_name.replace(" ", "_")}.png')
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        
        self.images.append(filename)
        return filename
    
    def create_spacing_annotation(self, geometry: Dict, holes: List[Dict],
                                  violations: List[Tuple], min_spacing: float,
                                  rule_name: str) -> str:
        """
        Create annotated image showing hole spacing violations
        
        Args:
            geometry: Geometry information
            holes: List of all holes
            violations: List of (hole1_idx, hole2_idx, distance) tuples
            min_spacing: Minimum required spacing
            rule_name: Name of the rule
            
        Returns:
            Path to generated image
        """
        if not holes or not violations:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Get part dimensions
        dims = geometry.get('dimensions', {})
        width = dims.get('x', 100)
        height = dims.get('y', 100)
        
        # Draw part outline
        part_rect = Rectangle((0, 0), width, height,
                              fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(part_rect)
        
        # Draw all holes
        for i, hole in enumerate(holes):
            center = hole.get('center', {})
            x = center.get('x', 0)
            y = center.get('y', 0)
            diameter = hole.get('diameter', 5)
            radius = diameter / 2
            
            # Check if this hole is involved in a violation
            is_violated = any(i in (v[0], v[1]) for v in violations)
            
            color = 'red' if is_violated else 'green'
            alpha = 0.7 if is_violated else 0.3
            
            circle = Circle((x, y), radius,
                          fill=True, facecolor=color,
                          edgecolor=color, alpha=alpha, linewidth=2)
            ax.add_patch(circle)
        
        # Draw lines between violated hole pairs
        for hole1_idx, hole2_idx, distance in violations:
            if hole1_idx < len(holes) and hole2_idx < len(holes):
                h1 = holes[hole1_idx]
                h2 = holes[hole2_idx]
                
                x1 = h1.get('center', {}).get('x', 0)
                y1 = h1.get('center', {}).get('y', 0)
                x2 = h2.get('center', {}).get('x', 0)
                y2 = h2.get('center', {}).get('y', 0)
                
                # Draw line
                ax.plot([x1, x2], [y1, y2], 'r--', linewidth=2, alpha=0.7)
                
                # Add distance label
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                ax.annotate(f'{distance:.2f}mm\n(min: {min_spacing:.2f}mm)',
                          xy=(mid_x, mid_y),
                          fontsize=9, color='red', weight='bold',
                          ha='center',
                          bbox=dict(boxstyle='round,pad=0.3',
                                  facecolor='yellow', edgecolor='red', alpha=0.8))
        
        # Set axis properties
        ax.set_xlim(-10, width + 10)
        ax.set_ylim(-10, height + 10)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('X (mm)', fontsize=10)
        ax.set_ylabel('Y (mm)', fontsize=10)
        
        # Add title
        title = f'{rule_name}\n'
        title += f'{len(violations)} spacing violation(s) detected'
        ax.set_title(title, fontsize=12, weight='bold', pad=15)
        
        # Add legend
        from matplotlib.patches import Patch, Line2D
        legend_elements = [
            Patch(facecolor='red', alpha=0.7, label='Violated Holes'),
            Patch(facecolor='green', alpha=0.3, label='OK Holes'),
            Line2D([0], [0], color='red', linestyle='--', linewidth=2, label='Too Close'),
            Patch(facecolor='none', edgecolor='black', linewidth=2, label='Part Outline')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=9)
        
        # Save image
        filename = os.path.join(self.temp_dir, f'annotation_{rule_name.replace(" ", "_")}.png')
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        
        self.images.append(filename)
        return filename
    
    def create_summary_chart(self, analysis_results: Dict) -> str:
        """
        Create summary chart showing pass/fail/warning counts
        
        Args:
            analysis_results: Complete analysis results
            
        Returns:
            Path to generated image
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Pie chart of rule statuses
        all_rules = analysis_results.get('all_rules', [])
        if all_rules:
            status_counts = {}
            for rule in all_rules:
                status = rule.get('status', 'INFO')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            labels = list(status_counts.keys())
            sizes = list(status_counts.values())
            colors = [self._get_status_color_mpl(s) for s in labels]
            explode = [0.1 if s == 'FAIL' else 0 for s in labels]
            
            ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', startangle=90, textprops={'fontsize': 11, 'weight': 'bold'})
            ax1.set_title('Rule Status Distribution', fontsize=12, weight='bold')
        
        # Bar chart of score
        score = analysis_results.get('score', 0)
        categories = ['Current\nScore', 'Target\nScore']
        values = [score, 90]
        colors = [self._get_score_color_mpl(score), 'green']
        
        bars = ax2.bar(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        
        # Add value labels
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.0f}',
                    ha='center', va='bottom', fontsize=14, weight='bold')
        
        ax2.set_ylim(0, 100)
        ax2.set_ylabel('Score', fontsize=12, weight='bold')
        ax2.set_title('Manufacturability Score', fontsize=12, weight='bold')
        ax2.grid(True, axis='y', alpha=0.3)
        
        # Add threshold lines
        ax2.axhline(y=90, color='green', linestyle='--', linewidth=1, alpha=0.5, label='Excellent (90+)')
        ax2.axhline(y=75, color='blue', linestyle='--', linewidth=1, alpha=0.5, label='Good (75+)')
        ax2.axhline(y=60, color='orange', linestyle='--', linewidth=1, alpha=0.5, label='Acceptable (60+)')
        ax2.legend(fontsize=8, loc='lower right')
        
        # Save image
        filename = os.path.join(self.temp_dir, 'summary_chart.png')
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        
        self.images.append(filename)
        return filename
    
    def _get_status_color_mpl(self, status: str) -> str:
        """Get matplotlib color for status"""
        colors = {
            'PASS': '#00AA00',
            'FAIL': '#CC0000',
            'WARNING': '#FF8C00',
            'INFO': '#0066CC'
        }
        return colors.get(status, '#000000')
    
    def _get_score_color_mpl(self, score: float) -> str:
        """Get matplotlib color for score"""
        if score >= 90:
            return '#00AA00'  # Green
        elif score >= 75:
            return '#0066CC'  # Blue
        elif score >= 60:
            return '#FF8C00'  # Orange
        else:
            return '#CC0000'  # Red
    
    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def __del__(self):
        """Cleanup on deletion"""
        self.cleanup()
