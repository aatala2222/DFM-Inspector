"""
Visualization module for DFM inspection results
"""
import matplotlib.pyplot as plt
from typing import Dict, List
import numpy as np

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


class DFMVisualizer:
    """Visualize DFM inspection results and highlight issues"""
    
    def __init__(self):
        self.fig = None
    
    def visualize_mesh(self, mesh, issues: List[Dict] = None):
        """Visualize 3D mesh with issue highlights"""
        if not PLOTLY_AVAILABLE:
            print("Plotly not available. Install with: pip install plotly")
            return
        
        vertices = mesh.vertices
        faces = mesh.faces
        
        # Create 3D mesh plot
        fig = go.Figure(data=[
            go.Mesh3d(
                x=vertices[:, 0],
                y=vertices[:, 1],
                z=vertices[:, 2],
                i=faces[:, 0],
                j=faces[:, 1],
                k=faces[:, 2],
                opacity=0.7,
                color='lightblue',
                name='Model'
            )
        ])
        
        # Add issue markers if provided
        if issues:
            self._add_issue_markers(fig, issues)
        
        fig.update_layout(
            title='DFM Inspection - 3D Model View',
            scene=dict(
                xaxis_title='X (mm)',
                yaxis_title='Y (mm)',
                zaxis_title='Z (mm)',
                aspectmode='data'
            ),
            width=1000,
            height=800
        )
        
        self.fig = fig
        return fig
    
    def _add_issue_markers(self, fig, issues: List[Dict]):
        """Add markers for detected issues"""
        # Placeholder for issue location markers
        pass
    
    def plot_inspection_summary(self, results: Dict):
        """Create summary charts for inspection results"""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # Issue distribution pie chart
        categories = {}
        for issue in results['issues']:
            cat = issue.get('category', 'Other')
            categories[cat] = categories.get(cat, 0) + 1
        
        if categories:
            axes[0].pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
            axes[0].set_title('Issues by Category')
        else:
            axes[0].text(0.5, 0.5, 'No Issues Found', ha='center', va='center')
            axes[0].set_title('Issues by Category')
        
        # Score gauge
        score = results['summary']['manufacturability_score']
        self._plot_score_gauge(axes[1], score)
        
        plt.tight_layout()
        return fig
    
    def _plot_score_gauge(self, ax, score: float):
        """Plot manufacturability score as a gauge"""
        # Color based on score
        if score >= 80:
            color = 'green'
        elif score >= 60:
            color = 'orange'
        else:
            color = 'red'
        
        # Create gauge
        theta = np.linspace(0, np.pi, 100)
        r = np.ones_like(theta)
        
        ax.plot(theta, r, 'k-', linewidth=2)
        
        # Fill based on score
        score_theta = np.linspace(0, np.pi * (score / 100), 50)
        ax.fill_between(score_theta, 0, 1, alpha=0.3, color=color)
        
        # Add score text
        ax.text(np.pi/2, 0.5, f'{score:.1f}', 
                ha='center', va='center', fontsize=24, fontweight='bold')
        ax.text(np.pi/2, 0.2, 'Manufacturability Score',
                ha='center', va='center', fontsize=10)
        
        ax.set_xlim(0, np.pi)
        ax.set_ylim(0, 1.2)
        ax.axis('off')
        ax.set_title('Overall Score')
    
    def show(self):
        """Display the visualization"""
        if self.fig:
            self.fig.show()
        plt.show()
    
    def save(self, filepath: str):
        """Save visualization to file"""
        if self.fig:
            self.fig.write_html(filepath)
        plt.savefig(filepath.replace('.html', '.png'))
