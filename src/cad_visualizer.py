"""
3D CAD Visualization with DFM Annotations
Renders actual STEP file geometry and highlights non-compliant features
Professional CAD-quality rendering with smooth shading and lighting
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as mcolors
from matplotlib import cm
import numpy as np
import tempfile
import os
from typing import Dict, List, Tuple

try:
    from OCP.STEPControl import STEPControl_Reader
    from OCP.IFSelect import IFSelect_RetDone
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.BRep import BRep_Tool
    from OCP.TopLoc import TopLoc_Location
    from OCP.gp import gp_Pnt
    OCP_AVAILABLE = True
except ImportError:
    OCP_AVAILABLE = False
    print("Warning: OCP not available. 3D visualization disabled.")

try:
    import trimesh
    TRIMESH_AVAILABLE = True
except ImportError:
    TRIMESH_AVAILABLE = False
    print("Warning: trimesh not available. Using fallback visualization.")


class CADVisualizer:
    """Render 3D CAD models with highlighted DFM issues"""
    
    def __init__(self, step_file_path: str = None, parser=None):
        """
        Initialize CAD visualizer
        
        Args:
            step_file_path: Path to STEP file (optional if parser provided)
            parser: Pre-loaded parser instance (EnhancedSTEPParser or SimpleCADParser)
        """
        self.step_file = step_file_path
        self.temp_dir = tempfile.mkdtemp()
        self.mesh = None
        self.vertices = None
        self.faces = None
        self.parser = parser
        
        # If parser provided, use its mesh directly
        if parser and hasattr(parser, 'mesh') and parser.mesh is not None:
            print("✓ Using mesh from provided parser")
            self.mesh = parser.mesh
            self.vertices = parser.mesh.vertices
            self.faces = parser.mesh.faces
            print(f"✓ Loaded from parser: {len(self.vertices)} vertices, {len(self.faces)} faces")
        elif step_file_path:
            self._load_geometry()
        else:
            print("⚠ No STEP file or parser provided")
    
    def _load_geometry(self):
        """Load STEP file geometry"""
        if not os.path.exists(self.step_file):
            print(f"STEP file not found: {self.step_file}")
            return
        
        try:
            if TRIMESH_AVAILABLE:
                # Use trimesh for easier mesh handling
                self.mesh = trimesh.load(self.step_file)
                if isinstance(self.mesh, trimesh.Scene):
                    # If it's a scene, combine all geometries
                    self.mesh = trimesh.util.concatenate(
                        [geom for geom in self.mesh.geometry.values()]
                    )
                self.vertices = self.mesh.vertices
                self.faces = self.mesh.faces
                print(f"✓ Loaded mesh: {len(self.vertices)} vertices, {len(self.faces)} faces")
            
            elif OCP_AVAILABLE:
                # Fallback to OCP
                self._load_with_ocp()
            
            else:
                print("No 3D loading library available")
                
        except Exception as e:
            print(f"Error loading geometry: {e}")
            import traceback
            traceback.print_exc()
    
    def _load_with_ocp(self):
        """Load geometry using OpenCascade"""
        reader = STEPControl_Reader()
        status = reader.ReadFile(self.step_file)
        
        if status != IFSelect_RetDone:
            print("Error reading STEP file")
            return
        
        reader.TransferRoots()
        shape = reader.OneShape()
        
        # Mesh the shape
        mesh = BRepMesh_IncrementalMesh(shape, 0.1, False, 0.5, True)
        mesh.Perform()
        
        # Extract vertices and faces
        vertices_list = []
        faces_list = []
        vertex_map = {}
        
        explorer = TopExp_Explorer(shape, TopAbs_FACE)
        while explorer.More():
            face = explorer.Current()
            location = TopLoc_Location()
            triangulation = BRep_Tool.Triangulation_s(face, location)
            
            if triangulation:
                # Get vertices
                for i in range(1, triangulation.NbNodes() + 1):
                    pnt = triangulation.Node(i)
                    vertex_map[len(vertices_list)] = (pnt.X(), pnt.Y(), pnt.Z())
                    vertices_list.append([pnt.X(), pnt.Y(), pnt.Z()])
                
                # Get faces
                for i in range(1, triangulation.NbTriangles() + 1):
                    triangle = triangulation.Triangle(i)
                    n1, n2, n3 = triangle.Get()
                    faces_list.append([n1-1, n2-1, n3-1])
            
            explorer.Next()
        
        self.vertices = np.array(vertices_list)
        self.faces = np.array(faces_list)
        print(f"✓ Loaded with OCP: {len(self.vertices)} vertices, {len(self.faces)} faces")
    
    def render_with_highlighted_holes(self, holes: List[Dict], 
                                      failed_holes: List[Dict],
                                      rule_name: str,
                                      view_angle: Tuple[float, float] = (30, 45)) -> str:
        """
        Render 3D model with highlighted problematic holes - CAD quality
        
        Args:
            holes: All holes in the part
            failed_holes: Holes that failed the rule
            rule_name: Name of the rule being visualized
            view_angle: (elevation, azimuth) for camera angle
            
        Returns:
            Path to generated image
        """
        if self.vertices is None or self.faces is None:
            print("No geometry loaded")
            return None
        
        # Create figure with white background for CAD appearance
        fig = plt.figure(figsize=(14, 11), facecolor='white')
        ax = fig.add_subplot(111, projection='3d', facecolor='white')
        
        # Render the main part with CAD-style smooth shading
        # Use light blue-gray color similar to CAD software
        poly = Poly3DCollection(
            self.vertices[self.faces],
            alpha=0.95,
            facecolor='#B8C5D6',  # Light blue-gray CAD color
            edgecolor='#4A5A6A',  # Darker edge color
            linewidths=0.3,
            antialiased=True,
            shade=True  # Enable smooth shading
        )
        ax.add_collection3d(poly)
        
        # Highlight failed holes in bright red
        for hole in failed_holes:
            center = hole.get('center', {})
            x, y, z = center.get('x', 0), center.get('y', 0), center.get('z', 0)
            diameter = hole.get('diameter', 5)
            radius = diameter / 2
            
            # Draw cylinder for hole with smooth shading
            theta = np.linspace(0, 2*np.pi, 40)  # More segments for smoothness
            z_cyl = np.linspace(z - 2, z + 2, 20)
            theta_grid, z_grid = np.meshgrid(theta, z_cyl)
            x_cyl = x + radius * np.cos(theta_grid)
            y_cyl = y + radius * np.sin(theta_grid)
            
            # Bright red for failed features
            ax.plot_surface(x_cyl, y_cyl, z_grid, 
                          color='#FF3333', alpha=0.9, 
                          shade=True, antialiased=True,
                          label=f'Failed: Ø{diameter:.1f}mm')
            
            # Add arrow pointing to hole
            arrow_length = max(5, diameter * 2)
            ax.quiver(x, y, z + arrow_length, 0, 0, -arrow_length*0.6,
                     color='#FF0000', arrow_length_ratio=0.25, linewidth=2.5)
            
            # Add text label with background box
            ax.text(x, y, z + arrow_length + 2, f'Ø{diameter:.1f}mm\nFAILED',
                   color='#CC0000', fontsize=11, weight='bold',
                   ha='center', va='bottom',
                   bbox=dict(boxstyle='round,pad=0.6', 
                           facecolor='white', edgecolor='#FF0000', linewidth=2))
        
        # Highlight passed holes in subtle green
        passed_holes = [h for h in holes if h not in failed_holes]
        for hole in passed_holes[:8]:  # Show up to 8 passed holes
            center = hole.get('center', {})
            x, y, z = center.get('x', 0), center.get('y', 0), center.get('z', 0)
            diameter = hole.get('diameter', 5)
            radius = diameter / 2
            
            # Draw smaller indicator with subtle green
            theta = np.linspace(0, 2*np.pi, 30)
            z_cyl = np.linspace(z - 1, z + 1, 10)
            theta_grid, z_grid = np.meshgrid(theta, z_cyl)
            x_cyl = x + radius * np.cos(theta_grid)
            y_cyl = y + radius * np.sin(theta_grid)
            
            ax.plot_surface(x_cyl, y_cyl, z_grid,
                          color='#66BB66', alpha=0.4, shade=True, antialiased=True)
        
        # Set axis properties for CAD appearance
        self._set_axis_properties_cad_style(ax, view_angle)
        
        # Add professional title
        title = f'{rule_name}\n'
        title += f'{len(failed_holes)} Failed Feature(s) | {len(passed_holes)} Passed'
        ax.set_title(title, fontsize=15, weight='bold', pad=25, color='#2C3E50')
        
        # Add legend with CAD styling
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#FF3333', alpha=0.9, edgecolor='#CC0000', linewidth=1.5,
                  label=f'Failed Holes ({len(failed_holes)})'),
            Patch(facecolor='#66BB66', alpha=0.4, edgecolor='#44AA44', linewidth=1.5,
                  label=f'Passed Holes ({len(passed_holes)})'),
            Patch(facecolor='#B8C5D6', alpha=0.95, edgecolor='#4A5A6A', linewidth=1.5,
                  label='Part Geometry')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=11, 
                 framealpha=0.95, edgecolor='#CCCCCC')
        
        # Save image with high quality
        filename = os.path.join(self.temp_dir, f'3d_{rule_name.replace(" ", "_")}.png')
        plt.tight_layout()
        plt.savefig(filename, dpi=200, bbox_inches='tight', facecolor='white', 
                   edgecolor='none', pad_inches=0.2)
        plt.close()
        
        return filename
    
    def render_with_highlighted_features(self, feature_locations: List[Tuple[float, float, float]],
                                        feature_type: str,
                                        rule_name: str,
                                        view_angle: Tuple[float, float] = (30, 45)) -> str:
        """
        Render 3D model with highlighted features (walls, edges, etc.)
        
        Args:
            feature_locations: List of (x, y, z) coordinates to highlight
            feature_type: Type of feature ('wall', 'edge', 'corner', etc.)
            rule_name: Name of the rule
            view_angle: Camera angle
            
        Returns:
            Path to generated image
        """
        if self.vertices is None or self.faces is None:
            return None
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Render main part
        poly = Poly3DCollection(
            self.vertices[self.faces],
            alpha=0.3,
            facecolor='lightgray',
            edgecolor='darkgray',
            linewidths=0.1
        )
        ax.add_collection3d(poly)
        
        # Highlight problem areas
        for i, (x, y, z) in enumerate(feature_locations):
            # Draw sphere at problem location
            u = np.linspace(0, 2 * np.pi, 20)
            v = np.linspace(0, np.pi, 20)
            radius = 2
            x_sphere = x + radius * np.outer(np.cos(u), np.sin(v))
            y_sphere = y + radius * np.outer(np.sin(u), np.sin(v))
            z_sphere = z + radius * np.outer(np.ones(np.size(u)), np.cos(v))
            
            ax.plot_surface(x_sphere, y_sphere, z_sphere,
                          color='red', alpha=0.7)
            
            # Add arrow
            ax.quiver(x, y, z + 5, 0, 0, -3,
                     color='red', arrow_length_ratio=0.3, linewidth=2)
            
            # Add label
            ax.text(x, y, z + 6, f'{feature_type.upper()}\n#{i+1}',
                   color='red', fontsize=10, weight='bold',
                   bbox=dict(boxstyle='round,pad=0.5',
                           facecolor='white', edgecolor='red'))
        
        # Set axis properties
        self._set_axis_properties(ax, view_angle)
        
        # Add title
        title = f'{rule_name}\n3D View: {len(feature_locations)} Problem Area(s) Highlighted'
        ax.set_title(title, fontsize=14, weight='bold', pad=20)
        
        # Save image
        filename = os.path.join(self.temp_dir, f'3d_{rule_name.replace(" ", "_")}.png')
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def render_multiple_views(self, holes: List[Dict],
                             failed_holes: List[Dict],
                             rule_name: str) -> str:
        """
        Render multiple views (front, top, side) with highlighted issues - CAD quality
        
        Args:
            holes: All holes
            failed_holes: Failed holes
            rule_name: Rule name
            
        Returns:
            Path to generated image
        """
        if self.vertices is None or self.faces is None:
            return None
        
        fig = plt.figure(figsize=(18, 6), facecolor='white')
        
        views = [
            (0, 0, 'Front View'),      # Front
            (90, 0, 'Top View'),       # Top
            (0, 90, 'Side View')       # Side
        ]
        
        for idx, (elev, azim, title) in enumerate(views, 1):
            ax = fig.add_subplot(1, 3, idx, projection='3d', facecolor='white')
            
            # Render part with CAD styling
            poly = Poly3DCollection(
                self.vertices[self.faces],
                alpha=0.95,
                facecolor='#B8C5D6',
                edgecolor='#4A5A6A',
                linewidths=0.3,
                antialiased=True,
                shade=True
            )
            ax.add_collection3d(poly)
            
            # Highlight failed holes with bright markers
            for hole in failed_holes:
                center = hole.get('center', {})
                x, y, z = center.get('x', 0), center.get('y', 0), center.get('z', 0)
                diameter = hole.get('diameter', 5)
                
                # Draw prominent marker
                ax.scatter([x], [y], [z], c='#FF3333', s=diameter*30, 
                          marker='o', alpha=0.95, edgecolors='#CC0000', linewidths=2.5,
                          depthshade=True)
            
            # Set view angle
            ax.view_init(elev=elev, azim=azim)
            ax.set_title(title, fontsize=13, weight='bold', pad=15, color='#2C3E50')
            
            # Set axis properties with CAD styling
            self._set_axis_properties_cad_style(ax, (elev, azim))
        
        # Overall title
        fig.suptitle(f'{rule_name} - Multiple Views\n{len(failed_holes)} Failed Features Highlighted in Red',
                    fontsize=15, weight='bold', color='#2C3E50', y=0.98)
        
        # Save image with high quality
        filename = os.path.join(self.temp_dir, f'3d_multiview_{rule_name.replace(" ", "_")}.png')
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(filename, dpi=200, bbox_inches='tight', facecolor='white',
                   edgecolor='none', pad_inches=0.2)
        plt.close()
        
        return filename
    
    def _set_axis_properties(self, ax, view_angle):
        """Set consistent axis properties"""
        if self.vertices is not None:
            # Set equal aspect ratio
            max_range = np.array([
                self.vertices[:, 0].max() - self.vertices[:, 0].min(),
                self.vertices[:, 1].max() - self.vertices[:, 1].min(),
                self.vertices[:, 2].max() - self.vertices[:, 2].min()
            ]).max() / 2.0
            
            mid_x = (self.vertices[:, 0].max() + self.vertices[:, 0].min()) * 0.5
            mid_y = (self.vertices[:, 1].max() + self.vertices[:, 1].min()) * 0.5
            mid_z = (self.vertices[:, 2].max() + self.vertices[:, 2].min()) * 0.5
            
            ax.set_xlim(mid_x - max_range, mid_x + max_range)
            ax.set_ylim(mid_y - max_range, mid_y + max_range)
            ax.set_zlim(mid_z - max_range, mid_z + max_range)
        
        # Set view angle
        ax.view_init(elev=view_angle[0], azim=view_angle[1])
        
        # Labels
        ax.set_xlabel('X (mm)', fontsize=10)
        ax.set_ylabel('Y (mm)', fontsize=10)
        ax.set_zlabel('Z (mm)', fontsize=10)
        
        # Grid
        ax.grid(True, alpha=0.3)
    
    def _set_axis_properties_cad_style(self, ax, view_angle):
        """Set CAD-style axis properties with professional appearance"""
        if self.vertices is not None:
            # Set equal aspect ratio
            max_range = np.array([
                self.vertices[:, 0].max() - self.vertices[:, 0].min(),
                self.vertices[:, 1].max() - self.vertices[:, 1].min(),
                self.vertices[:, 2].max() - self.vertices[:, 2].min()
            ]).max() / 2.0
            
            mid_x = (self.vertices[:, 0].max() + self.vertices[:, 0].min()) * 0.5
            mid_y = (self.vertices[:, 1].max() + self.vertices[:, 1].min()) * 0.5
            mid_z = (self.vertices[:, 2].max() + self.vertices[:, 2].min()) * 0.5
            
            ax.set_xlim(mid_x - max_range, mid_x + max_range)
            ax.set_ylim(mid_y - max_range, mid_y + max_range)
            ax.set_zlim(mid_z - max_range, mid_z + max_range)
        
        # Set view angle
        ax.view_init(elev=view_angle[0], azim=view_angle[1])
        
        # CAD-style axis labels
        ax.set_xlabel('X (mm)', fontsize=11, weight='bold', color='#2C3E50')
        ax.set_ylabel('Y (mm)', fontsize=11, weight='bold', color='#2C3E50')
        ax.set_zlabel('Z (mm)', fontsize=11, weight='bold', color='#2C3E50')
        
        # Clean grid
        ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5, color='#CCCCCC')
        
        # Set pane colors to white for clean CAD appearance
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        
        # Set pane edge colors
        ax.xaxis.pane.set_edgecolor('#DDDDDD')
        ax.yaxis.pane.set_edgecolor('#DDDDDD')
        ax.zaxis.pane.set_edgecolor('#DDDDDD')
        
        # Tick parameters
        ax.tick_params(axis='both', which='major', labelsize=9, colors='#555555')
    
    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def render_with_violations(self, violations: List[Dict], 
                               rule_name: str = "DFM Violations",
                               view_angle: Tuple[float, float] = (30, 45)) -> str:
        """
        Render 3D model with color-coded violation highlighting
        
        Args:
            violations: List of violation dictionaries with 'location', 'severity', 'feature_type'
            rule_name: Name of the rule or analysis
            view_angle: Camera angle (elevation, azimuth)
            
        Returns:
            Path to generated image
        """
        if self.vertices is None or self.faces is None:
            print("No geometry loaded")
            return None
        
        # Create figure with white background
        fig = plt.figure(figsize=(14, 11), facecolor='white')
        ax = fig.add_subplot(111, projection='3d', facecolor='white')
        
        # Render main part with CAD styling
        poly = Poly3DCollection(
            self.vertices[self.faces],
            alpha=0.95,
            facecolor='#B8C5D6',
            edgecolor='#4A5A6A',
            linewidths=0.3,
            antialiased=True,
            shade=True
        )
        ax.add_collection3d(poly)
        
        # Color mapping for severity
        severity_colors = {
            'critical': '#FF3333',  # Bright red
            'warning': '#FFA500',   # Orange
            'suggestion': '#FFFF00' # Yellow
        }
        
        # Group violations by severity
        violations_by_severity = {'critical': [], 'warning': [], 'suggestion': []}
        for v in violations:
            severity = v.get('severity', 'warning')
            violations_by_severity[severity].append(v)
        
        # Render violations with color coding
        for severity, color in severity_colors.items():
            for violation in violations_by_severity[severity]:
                location = violation.get('location')
                if not location:
                    continue
                
                # Handle both tuple and dict formats
                if isinstance(location, (list, tuple)):
                    x, y, z = location[0], location[1], location[2]
                else:
                    x, y, z = location.get('x', 0), location.get('y', 0), location.get('z', 0)
                
                feature_type = violation.get('feature_type', 'unknown')
                measured = violation.get('measured_value', 0)
                required = violation.get('required_value', 0)
                
                # Draw sphere at violation location
                u = np.linspace(0, 2 * np.pi, 30)
                v = np.linspace(0, np.pi, 30)
                radius = 2.5 if severity == 'critical' else 2.0
                x_sphere = x + radius * np.outer(np.cos(u), np.sin(v))
                y_sphere = y + radius * np.outer(np.sin(u), np.sin(v))
                z_sphere = z + radius * np.outer(np.ones(np.size(u)), np.cos(v))
                
                ax.plot_surface(x_sphere, y_sphere, z_sphere,
                              color=color, alpha=0.9, shade=True, antialiased=True)
                
                # Add arrow pointing to violation
                arrow_length = 8 if severity == 'critical' else 6
                ax.quiver(x, y, z + arrow_length, 0, 0, -arrow_length*0.6,
                         color=color, arrow_length_ratio=0.25, linewidth=2.5)
                
                # Add label
                label_text = f'{feature_type.upper()}\n{measured:.2f}mm'
                ax.text(x, y, z + arrow_length + 2, label_text,
                       color=color, fontsize=10, weight='bold',
                       ha='center', va='bottom',
                       bbox=dict(boxstyle='round,pad=0.6',
                               facecolor='white', edgecolor=color, linewidth=2))
        
        # Set axis properties
        self._set_axis_properties_cad_style(ax, view_angle)
        
        # Add title with violation counts
        critical_count = len(violations_by_severity['critical'])
        warning_count = len(violations_by_severity['warning'])
        suggestion_count = len(violations_by_severity['suggestion'])
        
        title = f'{rule_name}\n'
        title += f'{critical_count} Critical | {warning_count} Warnings | {suggestion_count} Suggestions'
        ax.set_title(title, fontsize=15, weight='bold', pad=25, color='#2C3E50')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#FF3333', alpha=0.9, edgecolor='#CC0000', linewidth=1.5,
                  label=f'Critical ({critical_count})'),
            Patch(facecolor='#FFA500', alpha=0.9, edgecolor='#CC8400', linewidth=1.5,
                  label=f'Warnings ({warning_count})'),
            Patch(facecolor='#FFFF00', alpha=0.9, edgecolor='#CCCC00', linewidth=1.5,
                  label=f'Suggestions ({suggestion_count})'),
            Patch(facecolor='#B8C5D6', alpha=0.95, edgecolor='#4A5A6A', linewidth=1.5,
                  label='Part Geometry')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=11,
                 framealpha=0.95, edgecolor='#CCCCCC')
        
        # Save image
        filename = os.path.join(self.temp_dir, f'3d_violations_{rule_name.replace(" ", "_")}.png')
        plt.tight_layout()
        plt.savefig(filename, dpi=200, bbox_inches='tight', facecolor='white',
                   edgecolor='none', pad_inches=0.2)
        plt.close()
        
        return filename
    
    def render_violations_multiview(self, violations: List[Dict],
                                    rule_name: str = "DFM Violations") -> str:
        """
        Render multiple views with violation highlighting
        
        Args:
            violations: List of violations
            rule_name: Rule name
            
        Returns:
            Path to generated image
        """
        if self.vertices is None or self.faces is None:
            return None
        
        fig = plt.figure(figsize=(18, 6), facecolor='white')
        
        views = [
            (0, 0, 'Front View'),
            (90, 0, 'Top View'),
            (0, 90, 'Side View')
        ]
        
        severity_colors = {
            'critical': '#FF3333',
            'warning': '#FFA500',
            'suggestion': '#FFFF00'
        }
        
        for idx, (elev, azim, title) in enumerate(views, 1):
            ax = fig.add_subplot(1, 3, idx, projection='3d', facecolor='white')
            
            # Render part
            poly = Poly3DCollection(
                self.vertices[self.faces],
                alpha=0.95,
                facecolor='#B8C5D6',
                edgecolor='#4A5A6A',
                linewidths=0.3,
                antialiased=True,
                shade=True
            )
            ax.add_collection3d(poly)
            
            # Render violations
            for violation in violations:
                location = violation.get('location')
                if not location:
                    continue
                
                if isinstance(location, (list, tuple)):
                    x, y, z = location[0], location[1], location[2]
                else:
                    x, y, z = location.get('x', 0), location.get('y', 0), location.get('z', 0)
                
                severity = violation.get('severity', 'warning')
                color = severity_colors.get(severity, '#FFA500')
                
                # Draw marker
                marker_size = 100 if severity == 'critical' else 70
                ax.scatter([x], [y], [z], c=color, s=marker_size,
                          marker='o', alpha=0.95, edgecolors='#000000', linewidths=2,
                          depthshade=True)
            
            # Set view
            ax.view_init(elev=elev, azim=azim)
            ax.set_title(title, fontsize=13, weight='bold', pad=15, color='#2C3E50')
            self._set_axis_properties_cad_style(ax, (elev, azim))
        
        # Overall title
        critical_count = len([v for v in violations if v.get('severity') == 'critical'])
        warning_count = len([v for v in violations if v.get('severity') == 'warning'])
        
        fig.suptitle(f'{rule_name} - Multiple Views\n{critical_count} Critical | {warning_count} Warnings',
                    fontsize=15, weight='bold', color='#2C3E50', y=0.98)
        
        # Save
        filename = os.path.join(self.temp_dir, f'3d_multiview_violations_{rule_name.replace(" ", "_")}.png')
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(filename, dpi=200, bbox_inches='tight', facecolor='white',
                   edgecolor='none', pad_inches=0.2)
        plt.close()
        
        return filename
    
    def __del__(self):
        """Cleanup on deletion"""
        self.cleanup()
