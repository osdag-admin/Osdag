"""
PSO Visualizer - 3D Cloud Plot + Cross-Section View
=====================================================
Visualization of Particle Swarm Optimization results with:
- 3D scatter plot: Utilization Ratio vs Weight vs Depth
- Engineering cross-section view with dimension labels
- Global best particle tracking with iteration and particle ID
"""

from typing import List, Dict, Tuple, Optional
import numpy as np
from collections import deque
from threading import RLock

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch, Arc
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('QtAgg')

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QApplication, QFrame,
    QSizePolicy, QFileDialog
)
from PySide6.QtGui import QFont


# ============== COLORS (matching Osdag theme) ==============
SAFE_COLOR = '#4ADE80'      # Green for feasible (UR <= 1)
FAIL_COLOR = '#F87171'      # Red for infeasible (UR > 1)
OPTIMAL_COLOR = '#FFD700'   # Gold for global best
ACCENT_BLUE = '#2563EB'     # Strong blue for cross-section
OSDAG_GREEN = '#2E9F4F'     # Osdag theme green
HEADER_GREEN = '#6B7D20'    # Osdag olive header
SECTION_FILL = '#4A90D9'    # Blue fill for I-beam section
SECTION_EDGE = '#1E3A8A'    # Dark blue edge


# Memory limit constants for 8GB RAM compatibility
MAX_HISTORY_ENTRIES = 10000
MAX_PARTICLES = 100


class DataProcessor:
    """Data processor for particle updates with memory limits."""
    
    def __init__(self):
        self.lock = RLock()
        self._disposed = False
        
        # Ranges for normalization
        self.depth_range = [float('inf'), float('-inf')]
        self.ur_range = [0.0, 2.0]
        self.weight_range = [float('inf'), float('-inf')]
        
        # History
        self.history: List[Dict] = []
        
        # Current visible particles
        self.particles: Dict[int, Dict] = {}
        
        # Variable Metadata
        self.variable_names = []
        self.variable_bounds = {'lb': [], 'ub': []}
        
        # Best Solution Tracking
        self.best_weight = float('inf')
        self.best_pos = None
        self.best_position_vector = None
        self.best_iteration = 0
        self.best_particle_id = 0
        
    def add_particle_data(self, depth: float, ur: float, weight: float,
                          iteration: int, particle_idx: int, position: list = None, 
                          variables: list = None, lb: list = None, ub: list = None):
        """Add new particle data (called from optimization thread)."""
        if self._disposed:
            return
            
        with self.lock:
            # Store variable names and bounds if provided (once)
            if variables and not self.variable_names:
                self.variable_names = variables
            
            if lb and ub and not self.variable_bounds['lb']:
                self.variable_bounds['lb'] = lb
                self.variable_bounds['ub'] = ub

            # Memory limit: cap history
            if len(self.history) < MAX_HISTORY_ENTRIES:
                entry = {
                    'depth': depth, 'ur': ur, 'weight': weight,
                    'iteration': iteration, 'particle_idx': particle_idx
                }
                if position:
                    entry['position'] = position
                self.history.append(entry)
            
            # Update ranges for dynamic scaling
            self.depth_range[0] = min(self.depth_range[0], depth)
            self.depth_range[1] = max(self.depth_range[1], depth)
            self.weight_range[0] = min(self.weight_range[0], weight)
            self.weight_range[1] = max(self.weight_range[1], weight)
            self.ur_range[1] = max(self.ur_range[1], ur)
            
            # Update best tracking (feasible solutions only)
            if weight < self.best_weight and ur <= 1.0:
                self.best_weight = weight
                self.best_pos = (depth, ur, weight)
                self.best_iteration = iteration
                self.best_particle_id = particle_idx
                if position:
                    self.best_position_vector = list(position)
            
            # Update particle trails (keep last 15 points)
            if particle_idx not in self.particles:
                self.particles[particle_idx] = {'trail': deque(maxlen=15)}
            self.particles[particle_idx]['trail'].append((depth, ur, weight))
            self.particles[particle_idx]['current'] = (depth, ur, weight)
            self.particles[particle_idx]['iteration'] = iteration
            if position:
                self.particles[particle_idx]['position'] = position
                
    def get_render_data(self) -> dict:
        """Get current state for rendering."""
        with self.lock:
            d_range = list(self.depth_range)
            w_range = list(self.weight_range)
            ur_range = list(self.ur_range)
            
            # Ensure valid ranges
            if d_range[0] == float('inf'):
                d_range = [0, 2000]
            else:
                padding = max(50, (d_range[1] - d_range[0]) * 0.1)
                d_range[0] = max(0, d_range[0] - padding)
                d_range[1] = d_range[1] + padding
            
            if w_range[0] == float('inf'):
                w_range = [0, 50000]
            else:
                padding = max(1000, (w_range[1] - w_range[0]) * 0.1)
                w_range[0] = max(0, w_range[0] - padding)
                w_range[1] = w_range[1] + padding
            
            return {
                'particles': dict(self.particles),
                'depth_range': d_range,
                'ur_range': ur_range,
                'weight_range': w_range,
                'best_pos': self.best_pos,
                'global_best_position': self.best_position_vector,
                'best_weight': self.best_weight,
                'best_iteration': self.best_iteration,
                'best_particle_id': self.best_particle_id,
                'history': list(self.history),
                'iteration': max((p.get('iteration', 0) for p in self.particles.values()), default=0),
                'variable_names': self.variable_names,
                'variable_bounds': self.variable_bounds
            }
    
    def get_history_length(self) -> int:
        with self.lock:
            return len(self.history)
    
    def clear(self):
        """Reset all data and mark as disposed."""
        self._disposed = True
        with self.lock:
            self.history.clear()
            self.history = []
            self.particles.clear()
            self.particles = {}
            self.best_weight = float('inf')
            self.best_pos = None
            self.best_position_vector = None
            self.depth_range = [float('inf'), float('-inf')]
            self.ur_range = [0.0, 2.0]
            self.weight_range = [float('inf'), float('-inf')]


class MatplotlibCanvas(FigureCanvas):
    """Two-Panel Visualization: 3D Cloud Plot + Cross-Section View."""
    
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(16, 8), dpi=90, facecolor='#ffffff')
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()
        
        # Initialize Layout
        self._setup_layout()
        
    def _setup_layout(self):
        """Create the 2-panel layout: 3D plot + Cross-section."""
        # GridSpec: 1 Row, 2 Columns (60% / 40% split)
        self.gs = self.fig.add_gridspec(1, 5, wspace=0.15, 
                                        left=0.05, right=0.95, top=0.90, bottom=0.10)
        
        # 1. 3D Cloud Scatter Plot (Left - 60%)
        self.ax_3d = self.fig.add_subplot(self.gs[0, :3], projection='3d')
        
        # 2. Cross-Section View (Right - 40%)
        self.ax_sect = self.fig.add_subplot(self.gs[0, 3:])

    def update_plot(self, data: dict):
        """Update both panels with new data."""
        # Clear Axes
        self.ax_3d.cla()
        self.ax_sect.cla()
        
        # 1. 3D Cloud Plot
        self._setup_3d_axes(data)
        self._plot_3d_cloud(data)
        
        # 2. Cross-Section View
        self._setup_section_axes()
        self._plot_cross_section(data)
        
        self.draw_idle()

    def _setup_3d_axes(self, data):
        """Configure 3D axes appearance."""
        ax = self.ax_3d
        
        # Title
        ax.set_title('3D Scatter Plot: Utilization Ratio vs Depth vs Weight', 
                     fontsize=11, fontweight='bold', pad=15)
        
        # Axis labels with units
        ax.set_xlabel('Utilization Ratio', fontsize=10, labelpad=10)
        ax.set_ylabel('Depth (mm)', fontsize=10, labelpad=10)
        ax.set_zlabel('Weight (kg)', fontsize=10, labelpad=10)
        
        # Set axis ranges from data
        ur_range = data.get('ur_range', [0, 2])
        depth_range = data.get('depth_range', [0, 2000])
        weight_range = data.get('weight_range', [0, 50000])
        
        ax.set_xlim(0, max(1.5, ur_range[1]))
        ax.set_ylim(depth_range[0], depth_range[1])
        ax.set_zlim(weight_range[0], weight_range[1])
        
        # Background style (white, clean)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('lightgray')
        ax.yaxis.pane.set_edgecolor('lightgray')
        ax.zaxis.pane.set_edgecolor('lightgray')
        
        # Grid
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # View angle (same as reference)
        ax.view_init(elev=20, azim=225)
        
        # Add UR=1.0 plane reference (feasibility boundary)
        ur_limit = 1.0
        d_vals = np.linspace(depth_range[0], depth_range[1], 2)
        w_vals = np.linspace(weight_range[0], weight_range[1], 2)
        DV, WV = np.meshgrid(d_vals, w_vals)
        UV = np.ones_like(DV) * ur_limit
        ax.plot_surface(UV, DV, WV, alpha=0.1, color='red', linewidth=0)

    def _plot_3d_cloud(self, data):
        """Render 3D scatter cloud plot."""
        ax = self.ax_3d
        history = data.get('history', [])
        
        if not history:
            ax.text2D(0.5, 0.5, "Waiting for data...", 
                     transform=ax.transAxes, ha='center', fontsize=12, color='gray')
            return
        
        # Separate feasible and infeasible points
        feasible_pts = []
        infeasible_pts = []
        
        for entry in history:
            ur = entry.get('ur', 0)
            depth = entry.get('depth', 0)
            weight = entry.get('weight', 0)
            
            if ur <= 1.0:
                feasible_pts.append((ur, depth, weight))
            else:
                infeasible_pts.append((ur, depth, weight))
        
        # Plot infeasible points (red, smaller, faint)
        if infeasible_pts:
            inf_ur, inf_d, inf_w = zip(*infeasible_pts)
            ax.scatter(inf_ur, inf_d, inf_w, 
                      c=FAIL_COLOR, s=20, alpha=0.4, marker='s',
                      label='Utilization > 1')
        
        # Plot feasible points (green)
        if feasible_pts:
            feas_ur, feas_d, feas_w = zip(*feasible_pts)
            ax.scatter(feas_ur, feas_d, feas_w, 
                      c=SAFE_COLOR, s=30, alpha=0.7, marker='o',
                      label='Utilization ≤ 1')
        
        # Plot global best (gold star, prominent)
        best_pos = data.get('best_pos')
        best_weight = data.get('best_weight', float('inf'))
        
        if best_pos and best_weight != float('inf'):
            b_depth, b_ur, b_weight = best_pos
            
            # Large gold star marker
            ax.scatter([b_ur], [b_depth], [b_weight], 
                      c=OPTIMAL_COLOR, s=200, marker='*', 
                      edgecolors='black', linewidth=1,
                      label='Global Best', zorder=10)
            
            # Draw trajectory line from origin to best
            ax.plot([0, b_ur], [b_depth, b_depth], [b_weight, b_weight],
                   color=OPTIMAL_COLOR, linewidth=2, linestyle='-', alpha=0.8)
            
            # Annotation box
            best_vector = data.get('global_best_position')
            names = data.get('variable_names', [])
            best_iter = data.get('best_iteration', 0)
            best_pid = data.get('best_particle_id', 0)
            
            if best_vector and names:
                dims = dict(zip(names, best_vector))
                D = dims.get('D', dims.get('d', 0))
                tw = dims.get('tw', 0)
                bf = dims.get('bf', dims.get('bf_top', 0))
                tf = dims.get('tf', dims.get('tf_top', 0))
                
                annotation_text = (
                    f"Global Best:\n"
                    f"  Iter: {best_iter + 1} | Particle: {best_pid + 1}\n"
                    f"  Depth: {D:.1f} mm\n"
                    f"  Width: {bf:.1f} mm\n"
                    f"  Weight: {b_weight:.1f} kg\n"
                    f"  UR: {b_ur:.3f}"
                )
                
                # Text box annotation (2D overlay)
                ax.text2D(0.02, 0.98, annotation_text, 
                         transform=ax.transAxes, fontsize=9,
                         verticalalignment='top',
                         bbox=dict(boxstyle='round,pad=0.5', 
                                  facecolor='lightyellow', 
                                  edgecolor='gray', alpha=0.9),
                         fontfamily='monospace')
        
        # Legend
        ax.legend(loc='upper right', fontsize=8, framealpha=0.9)

    def _setup_section_axes(self):
        """Configure cross-section view axes."""
        ax = self.ax_sect
        ax.set_title('Best Cross-Section (I-Beam)', fontsize=11, fontweight='bold', pad=10)
        ax.set_aspect('equal')
        ax.axis('off')

    def _plot_cross_section(self, data):
        """Render I-beam cross-section with engineering labels."""
        ax = self.ax_sect
        names = data.get('variable_names', [])
        best_vector = data.get('global_best_position')
        best_iter = data.get('best_iteration', 0)
        best_pid = data.get('best_particle_id', 0)
        best_weight = data.get('best_weight', float('inf'))
        best_pos = data.get('best_pos')
        
        if not best_vector or not names:
            ax.text(0.5, 0.5, "No Feasible Solution Yet\n(Searching...)", 
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=14, color='gray')
            return
        
        # Extract dimensions from best solution
        dims = dict(zip(names, best_vector))
        
        D = dims.get('D', dims.get('d', 1000))
        tw = dims.get('tw', 10)
        
        # Handle symmetric or asymmetric flanges
        if 'bf' in dims and 'tf' in dims:
            bf_top = bf_bot = dims['bf']
            tf_top = tf_bot = dims['tf']
        else:
            bf_top = dims.get('bf_top', 200)
            bf_bot = dims.get('bf_bot', 200)
            tf_top = dims.get('tf_top', 15)
            tf_bot = dims.get('tf_bot', 15)
        
        # Fillet radii (if available, else defaults)
        R1 = dims.get('R1', min(tw, tf_top) * 0.5)
        R2 = dims.get('R2', min(tw, tf_bot) * 0.5)
        
        # Draw I-beam cross-section
        # Scale factor for visibility
        max_dim = max(D, bf_top, bf_bot)
        
        # Bottom flange
        bot_flange = Rectangle((-bf_bot/2, 0), bf_bot, tf_bot,
                               facecolor=SECTION_FILL, edgecolor=SECTION_EDGE, linewidth=2)
        ax.add_patch(bot_flange)
        
        # Web
        web_height = D - tf_top - tf_bot
        web = Rectangle((-tw/2, tf_bot), tw, web_height,
                        facecolor=SECTION_FILL, edgecolor=SECTION_EDGE, linewidth=2)
        ax.add_patch(web)
        
        # Top flange
        top_flange = Rectangle((-bf_top/2, D - tf_top), bf_top, tf_top,
                               facecolor=SECTION_FILL, edgecolor=SECTION_EDGE, linewidth=2)
        ax.add_patch(top_flange)
        
        # Set view limits
        margin = max_dim * 0.4
        ax.set_xlim(-max(bf_top, bf_bot)/2 - margin, max(bf_top, bf_bot)/2 + margin)
        ax.set_ylim(-margin * 0.5, D + margin * 0.5)
        
        # ===== DIMENSION LABELS =====
        label_offset = max_dim * 0.08
        arrow_props = dict(arrowstyle='<->', color='black', lw=1.5)
        
        # Y-Y Axis (vertical, through center)
        ax.annotate('', xy=(0, -margin * 0.3), xytext=(0, D + margin * 0.2),
                   arrowprops=dict(arrowstyle='-', color='red', lw=1.5, linestyle='--'))
        ax.text(label_offset * 0.5, D + margin * 0.3, 'Y', fontsize=12, fontweight='bold', color='red')
        ax.text(label_offset * 0.5, -margin * 0.4, 'Y', fontsize=12, fontweight='bold', color='red')
        
        # Z-Z Axis (horizontal, through mid-height)
        mid_y = D / 2
        ax.annotate('', xy=(-max(bf_top, bf_bot)/2 - margin * 0.2, mid_y), 
                   xytext=(max(bf_top, bf_bot)/2 + margin * 0.2, mid_y),
                   arrowprops=dict(arrowstyle='-', color='red', lw=1.5, linestyle='--'))
        ax.text(max(bf_top, bf_bot)/2 + margin * 0.3, mid_y, 'Z', fontsize=12, fontweight='bold', color='red')
        ax.text(-max(bf_top, bf_bot)/2 - margin * 0.4, mid_y, 'Z', fontsize=12, fontweight='bold', color='red')
        
        # D (Total Depth) - right side
        x_d = max(bf_top, bf_bot)/2 + label_offset * 2
        ax.annotate('', xy=(x_d, 0), xytext=(x_d, D),
                   arrowprops=arrow_props)
        ax.text(x_d + label_offset, D/2, f'D\n{D:.0f}', fontsize=10, ha='left', va='center', fontweight='bold')
        
        # B (Flange Width) - bottom
        y_b = -label_offset * 2
        ax.annotate('', xy=(-bf_bot/2, y_b), xytext=(bf_bot/2, y_b),
                   arrowprops=arrow_props)
        ax.text(0, y_b - label_offset, f'B = {bf_bot:.0f}', fontsize=10, ha='center', va='top', fontweight='bold')
        
        # t (Web Thickness) - at mid-height
        y_t = D / 2
        ax.annotate('', xy=(-tw/2, y_t + label_offset * 0.5), xytext=(tw/2, y_t + label_offset * 0.5),
                   arrowprops=dict(arrowstyle='<->', color='blue', lw=1))
        ax.text(tw/2 + label_offset * 0.5, y_t + label_offset, f't={tw:.1f}', fontsize=9, ha='left', color='blue')
        
        # tf (Flange Thickness) - top flange, left side
        x_tf = -bf_top/2 - label_offset
        ax.annotate('', xy=(x_tf, D - tf_top), xytext=(x_tf, D),
                   arrowprops=dict(arrowstyle='<->', color='green', lw=1))
        ax.text(x_tf - label_offset, D - tf_top/2, f'tf={tf_top:.1f}', fontsize=9, ha='right', color='green', va='center')
        
        # R1, R2 fillet indicators (small arcs at web-flange junctions)
        # Top-right fillet
        arc1 = Arc((tw/2, D - tf_top), R1*2, R1*2, angle=0, theta1=0, theta2=90, color='purple', lw=1)
        ax.add_patch(arc1)
        ax.text(tw/2 + R1 + label_offset * 0.3, D - tf_top - R1, f'R1', fontsize=8, color='purple')
        
        # Bottom-right fillet
        arc2 = Arc((tw/2, tf_bot), R2*2, R2*2, angle=0, theta1=270, theta2=360, color='purple', lw=1)
        ax.add_patch(arc2)
        ax.text(tw/2 + R2 + label_offset * 0.3, tf_bot + R2, f'R2', fontsize=8, color='purple')
        
        # ===== GLOBAL BEST INFO BOX =====
        if best_pos:
            b_depth, b_ur, b_weight = best_pos
            info_text = (
                f"GLOBAL BEST SOLUTION\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"Iteration: {best_iter + 1}\n"
                f"Particle ID: {best_pid + 1}\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"Weight: {b_weight:.1f} kg\n"
                f"Utilization: {b_ur:.4f}"
            )
            
            # Position info box at top-left
            ax.text(0.02, 0.98, info_text, 
                   transform=ax.transAxes, fontsize=10,
                   verticalalignment='top', ha='left',
                   bbox=dict(boxstyle='round,pad=0.6', 
                            facecolor='#f0f9ff', 
                            edgecolor=HEADER_GREEN, 
                            linewidth=2, alpha=0.95),
                   fontfamily='monospace', fontweight='bold')

    def cleanup(self):
        """Clean up matplotlib resources."""
        try:
            plt.close(self.fig)
        except Exception:
            pass


class PSOVisualizerWidget(QWidget):
    """Main PSO Visualizer Widget with 3D Cloud Plot + Cross-Section."""
    switch_to_cad = Signal()
    
    def __init__(self, parent=None, max_iterations=100):
        super().__init__(parent)
        print("DEBUG: Loading PSO Visualizer V3 (3D Cloud + Cross-Section)")
        self.setWindowFlags(self.windowFlags() | Qt.Dialog)
        self.max_iter = max_iterations
        self.is_complete = False
        
        # Data processor
        self.data_processor = DataProcessor()
        
        # Batch buffer for performance
        self.batch_buffer = {'d': [], 'u': [], 'w': [], 'i': [], 'p': [], 
                            'pos': [], 'vars': [], 'lb': [], 'ub': []}
        
        # Setup UI
        self.setup_ui()
        
        # Render timer (update canvas from data)
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self._update_canvas)
        self.render_timer.start(150)  # ~7 FPS for smooth performance
        
    def setup_ui(self):
        """Setup the UI components."""
        self.setStyleSheet("""
            QWidget { 
                background-color: white; 
                font-family: 'Segoe UI', 'SF Pro Display', sans-serif; 
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # ===== HEADER =====
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {HEADER_GREEN};
                border-bottom: 2px solid #556619;
            }}
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        # Title
        title = QLabel("PSO OPTIMIZATION SPACE")
        title.setStyleSheet("""
            color: white; 
            font-size: 14px; 
            font-weight: bold;
            letter-spacing: 1px;
        """)
        
        # Iteration label
        self.lbl_iter = QLabel("ITERATION: 0")
        self.lbl_iter.setStyleSheet("""
            color: rgba(255,255,255,0.9); 
            font-size: 13px; 
            font-weight: bold;
        """)
        
        # Best weight label
        self.lbl_best = QLabel("BEST: --- kg")
        self.lbl_best.setStyleSheet("""
            color: #FFD700; 
            font-size: 13px; 
            font-weight: bold;
        """)
        
        # Best particle info
        self.lbl_particle = QLabel("PARTICLE: ---")
        self.lbl_particle.setStyleSheet("""
            color: rgba(255,255,255,0.8); 
            font-size: 12px;
        """)
        
        # Close button
        close_btn = QPushButton("CLOSE")
        close_btn.clicked.connect(self.switch_to_cad.emit)
        close_btn.setStyleSheet("""
            QPushButton { 
                background-color: #90AF13; 
                color: white; 
                border: 0px;
                border-radius: 5px; 
                padding: 6px 14px; 
                font-weight: bold; 
            }
            QPushButton:hover { background-color: #a0c020; }
            QPushButton:pressed { background-color: #7a9a12; }
        """)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.lbl_iter)
        header_layout.addSpacing(25)
        header_layout.addWidget(self.lbl_best)
        header_layout.addSpacing(15)
        header_layout.addWidget(self.lbl_particle)
        header_layout.addSpacing(25)
        header_layout.addWidget(close_btn)
        
        layout.addWidget(header)
        
        # ===== MAIN CONTENT: Matplotlib Canvas =====
        self.canvas = MatplotlibCanvas(self)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.canvas, 1)
        
        # ===== BOTTOM TOOLBAR (Simplified) =====
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(40)
        bottom_bar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-top: 1px solid #ddd;
            }
        """)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(15, 5, 15, 5)
        bottom_layout.setSpacing(15)
        
        # Status label
        self.lbl_status = QLabel("Optimizing...")
        self.lbl_status.setStyleSheet("color: #666; font-size: 11px;")
        
        # Save button
        btn_style = """
            QPushButton { 
                background-color: #f0f0f0; 
                color: #333; 
                border: 1px solid #ccc;
                border-radius: 3px; 
                padding: 4px 12px;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #e0e0e0; }
            QPushButton:pressed { background-color: #d0d0d0; }
            QPushButton:disabled { background-color: #f8f8f8; color: #aaa; }
        """
        
        self.btn_save = QPushButton("💾 Save Plot")
        self.btn_save.setStyleSheet(btn_style)
        self.btn_save.clicked.connect(self.save_plot)
        self.btn_save.setEnabled(False)
        
        # Legend
        legend_text = QLabel(
            "<span style='color: #FFD700;'>★</span> Best  "
            "<span style='color: #4ADE80;'>●</span> Feasible  "
            "<span style='color: #F87171;'>■</span> Infeasible"
        )
        legend_text.setStyleSheet("color: #333; font-size: 11px;")
        
        bottom_layout.addWidget(self.lbl_status)
        bottom_layout.addStretch()
        bottom_layout.addWidget(legend_text)
        bottom_layout.addSpacing(20)
        bottom_layout.addWidget(self.btn_save)
        
        layout.addWidget(bottom_bar)
    
    def add_particle_data(self, depth: float, ur: float, weight: float,
                          iteration: int, particle_idx: int, position: list = None, 
                          variables: list = None, lb: list = None, ub: list = None):
        """Add particle data (called from optimization)."""
        if self.is_complete:
            return
        
        # Buffer for batch processing
        self.batch_buffer['d'].append(depth)
        self.batch_buffer['u'].append(ur)
        self.batch_buffer['w'].append(weight)
        self.batch_buffer['i'].append(iteration)
        self.batch_buffer['p'].append(particle_idx)
        self.batch_buffer['pos'].append(position)
        self.batch_buffer['vars'].append(variables)
        self.batch_buffer['lb'].append(lb)
        self.batch_buffer['ub'].append(ub)
        
        # Flush when buffer is full
        if len(self.batch_buffer['d']) >= 20:
            self._flush_buffer()
    
    def _flush_buffer(self):
        """Process buffered data."""
        if not self.batch_buffer['d']:
            return
        
        for i in range(len(self.batch_buffer['d'])):
            self.data_processor.add_particle_data(
                self.batch_buffer['d'][i],
                self.batch_buffer['u'][i],
                self.batch_buffer['w'][i],
                self.batch_buffer['i'][i],
                self.batch_buffer['p'][i],
                self.batch_buffer['pos'][i],
                self.batch_buffer['vars'][i],
                self.batch_buffer['lb'][i],
                self.batch_buffer['ub'][i]
            )
        
        self.batch_buffer = {'d': [], 'u': [], 'w': [], 'i': [], 'p': [], 
                            'pos': [], 'vars': [], 'lb': [], 'ub': []}
    
    def _update_canvas(self):
        """Update canvas with latest data."""
        data = self.data_processor.get_render_data()
        if data:
            self.canvas.update_plot(data)
            
            # Update header labels
            self.lbl_iter.setText(f"ITERATION: {data['iteration'] + 1}")
            
            if data['best_weight'] != float('inf'):
                self.lbl_best.setText(f"BEST: {data['best_weight']:.0f} kg")
                self.lbl_particle.setText(
                    f"PARTICLE: {data['best_particle_id'] + 1} @ Iter {data['best_iteration'] + 1}"
                )
    
    def save_plot(self):
        """Save the current visualization as PNG."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Plot", "pso_visualization.png", 
            "PNG Files (*.png);;All Files (*)"
        )
        
        if not file_path:
            return
        
        self.btn_save.setText("Saving...")
        self.btn_save.setEnabled(False)
        QApplication.processEvents()
        
        try:
            self.canvas.fig.savefig(file_path, dpi=150, bbox_inches='tight', facecolor='white')
            self.btn_save.setText("✓ Saved!")
        except Exception as e:
            print(f"[WARNING] Failed to save: {e}")
            self.btn_save.setText("❌ Failed")
        finally:
            QTimer.singleShot(2000, lambda: self.btn_save.setText("💾 Save Plot"))
            QTimer.singleShot(2000, lambda: self.btn_save.setEnabled(True))
    
    def set_complete(self):
        """Mark optimization as complete."""
        self._flush_buffer()
        self.is_complete = True
        
        # Final update
        data = self.data_processor.get_render_data()
        if data:
            best_iter = data.get('best_iteration', 0)
            best_pid = data.get('best_particle_id', 0)
            self.lbl_iter.setText(f"COMPLETE: {data['iteration'] + 1} iterations")
            self.lbl_status.setText(
                f"Optimization Complete | Best found at Iteration {best_iter + 1}, Particle {best_pid + 1}"
            )
        
        # Enable save button
        self.btn_save.setEnabled(True)
    
    def cleanup(self):
        """Clean up resources safely."""
        try:
            if hasattr(self, 'render_timer') and self.render_timer:
                self.render_timer.stop()
        except Exception:
            pass
        
        try:
            if hasattr(self, 'canvas') and self.canvas:
                self.canvas.cleanup()
        except Exception as e:
            print(f"[WARNING] Canvas cleanup error: {e}")
        
        try:
            if hasattr(self, 'data_processor') and self.data_processor:
                self.data_processor.clear()
        except Exception as e:
            print(f"[WARNING] Data processor cleanup error: {e}")
        
        try:
            if hasattr(self, 'batch_buffer'):
                self.batch_buffer = {'d': [], 'u': [], 'w': [], 'i': [], 'p': []}
        except Exception:
            pass
        
        self.is_complete = True
