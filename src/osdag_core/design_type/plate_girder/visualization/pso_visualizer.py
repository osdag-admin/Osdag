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
    QSizePolicy, QFileDialog, QDialog
)
from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from PySide6.QtGui import QFont

# Import safe_processEvents for thread-safe UI updates during CAD operations
try:
    from osdag_gui.OS_safety_protocols import safe_processEvents
except ImportError:
    # Fallback to direct call if not available
    def safe_processEvents():
        QApplication.processEvents()


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
                    entry['position'] = list(position)  # Store a copy
                self.history.append(entry)
            
            # Update ranges for dynamic scaling
            self.depth_range[0] = min(self.depth_range[0], depth)
            self.depth_range[1] = max(self.depth_range[1], depth)
            self.weight_range[0] = min(self.weight_range[0], weight)
            self.weight_range[1] = max(self.weight_range[1], weight)
            self.ur_range[1] = max(self.ur_range[1], ur)
            
            # Update best tracking (feasible solutions only)
            # CRITICAL: Update ALL best fields atomically when a new best is found
            if weight < self.best_weight and ur <= 1.0:
                self.best_weight = weight
                self.best_pos = (depth, ur, weight)
                self.best_iteration = iteration
                self.best_particle_id = particle_idx
                # Always update position vector when best changes
                if position:
                    self.best_position_vector = list(position)
                else:
                    # Position not passed - try to find from current entry or keep existing
                    # This shouldn't happen in normal flow, but guard against it
                    pass
            
            # Update particle trails (keep last 15 points)
            if particle_idx not in self.particles:
                self.particles[particle_idx] = {'trail': deque(maxlen=15)}
            self.particles[particle_idx]['trail'].append((depth, ur, weight))
            self.particles[particle_idx]['current'] = (depth, ur, weight)
            self.particles[particle_idx]['iteration'] = iteration
            if position:
                self.particles[particle_idx]['position'] = list(position)
                
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
        # Larger figure for better visualization
        self.fig = Figure(figsize=(12, 6.5), dpi=90, facecolor='#ffffff')
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(400, 300)
        self.updateGeometry()
        
        # Initialize Layout
        self._setup_layout()
        
    def _setup_layout(self):
        """Create the 2-panel layout: 3D plot + Cross-section with tables at bottom."""
        # GridSpec: Optimized layout with better margins
        # Increased bottom margin for info table
        self.gs = self.fig.add_gridspec(1, 5, wspace=0.12, 
                                        left=0.06, right=0.96, top=0.90, bottom=0.18)
        
        # 1. 3D Cloud Scatter Plot (Left - 60%)
        self.ax_3d = self.fig.add_subplot(self.gs[0, :3], projection='3d')
        
        # 2. Cross-Section View (Right - 40%)
        self.ax_sect = self.fig.add_subplot(self.gs[0, 3:])

    def update_plot(self, data: dict):
        """Update both panels with new data."""
        # Clear Axes
        self.ax_3d.cla()
        self.ax_sect.cla()
        
        # Clear any previous figure texts (tables)
        for txt in self.fig.texts:
            txt.remove()
        
        # 1. 3D Cloud Plot
        self._setup_3d_axes(data)
        self._plot_3d_cloud(data)
        
        # 2. Cross-Section View
        self._setup_section_axes()
        self._plot_cross_section(data)
        
        # 3. Add tables at bottom
        self._add_bottom_tables(data)
        
        self.draw_idle()

    def _setup_3d_axes(self, data):
        """Configure 3D axes appearance."""
        ax = self.ax_3d
        
        # Title (larger for better visibility)
        ax.set_title('3D Scatter: Utilization Ratio vs Depth vs Weight', 
                     fontsize=11, fontweight='bold', pad=10)
        
        # Axis labels with units (larger)
        ax.set_xlabel('Utilization Ratio', fontsize=10, labelpad=6)
        ax.set_ylabel('Depth (mm)', fontsize=10, labelpad=6)
        ax.set_zlabel('Weight (kg)', fontsize=10, labelpad=6)
        
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
        
        # Plot infeasible points (red hollow circles) - more transparent
        if infeasible_pts:
            inf_ur, inf_d, inf_w = zip(*infeasible_pts)
            ax.scatter(inf_ur, inf_d, inf_w, 
                      facecolors='none', edgecolors=FAIL_COLOR, s=25, alpha=0.4, 
                      marker='o', linewidths=1.0, depthshade=False,
                      label='Utilization > 1')
        
        # Plot feasible points (olive green hollow circles) - more transparent
        if feasible_pts:
            feas_ur, feas_d, feas_w = zip(*feasible_pts)
            ax.scatter(feas_ur, feas_d, feas_w, 
                      facecolors='none', edgecolors='#6B8E23', s=30, alpha=0.5, 
                      marker='o', linewidths=1.0, depthshade=False,
                      label='Utilization ≤ 1')
        
        # Plot global best (gold star, prominent - rendered as solid with no depth shading)
        best_pos = data.get('best_pos')
        best_weight = data.get('best_weight', float('inf'))
        
        if best_pos and best_weight != float('inf'):
            b_depth, b_ur, b_weight = best_pos
            
            # Large gold star marker - solid fill, no depth shading for consistent visibility
            # depthshade=False ensures it maintains full opacity regardless of position
            ax.scatter([b_ur], [b_depth], [b_weight], 
                      c=OPTIMAL_COLOR, s=350, marker='*', 
                      edgecolors='#8B4513', linewidths=1.5,
                      label='Global Best', depthshade=False)
            
            # Draw trajectory line from origin to best
            ax.plot([0, b_ur], [b_depth, b_depth], [b_weight, b_weight],
                   color=OPTIMAL_COLOR, linewidth=2, linestyle='-', alpha=0.8)
            
            # Annotation box
            best_vector = data.get('global_best_position')
            names = data.get('variable_names', [])
            best_iter = data.get('best_iteration', 0)
            best_pid = data.get('best_particle_id', 0)
            
        # Legend (larger for better visibility)
        ax.legend(loc='upper right', fontsize=9, framealpha=0.9)

    def _setup_section_axes(self):
        """Configure cross-section view axes."""
        ax = self.ax_sect
        ax.set_title('Best Cross-Section (I-Beam)', fontsize=11, fontweight='bold', pad=8)
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
        
        # Set view limits - increased bottom margin for B label visibility
        margin = max_dim * 0.4
        ax.set_xlim(-max(bf_top, bf_bot)/2 - margin, max(bf_top, bf_bot)/2 + margin)
        ax.set_ylim(-margin * 0.7, D + margin * 0.5)
        
        # ===== CLEAN DIMENSION LABELS =====
        label_offset = max_dim * 0.06
        arrow_props = dict(arrowstyle='<->', color='#333', lw=1.2)
        
        # Y-Y Axis (vertical, through center) - subtle dashed line
        ax.plot([0, 0], [-margin * 0.2, D + margin * 0.15], 
               color='#C41E3A', lw=1.2, linestyle='--', alpha=0.7)
        ax.text(label_offset * 0.4, D + margin * 0.2, 'Y', fontsize=10, fontweight='bold', color='#C41E3A')
        ax.text(label_offset * 0.4, -margin * 0.28, 'Y', fontsize=10, fontweight='bold', color='#C41E3A')
        
        # Z-Z Axis (horizontal, through mid-height) - subtle dashed line
        mid_y = D / 2
        half_w = max(bf_top, bf_bot) / 2
        ax.plot([-half_w - margin * 0.15, half_w + margin * 0.15], [mid_y, mid_y],
               color='#C41E3A', lw=1.2, linestyle='--', alpha=0.7)
        ax.text(half_w + margin * 0.2, mid_y, 'Z', fontsize=10, fontweight='bold', color='#C41E3A')
        ax.text(-half_w - margin * 0.25, mid_y, 'Z', fontsize=10, fontweight='bold', color='#C41E3A')
        
        # D (Total Depth) - right side, clean arrow
        x_d = half_w + label_offset * 2.5
        ax.annotate('', xy=(x_d, 0), xytext=(x_d, D), arrowprops=arrow_props)
        ax.text(x_d + label_offset * 0.8, D/2, f'D={D:.0f}', fontsize=9, ha='left', va='center', fontweight='bold')
        
        # B (Flange Width) - bottom, clean arrow
        y_b = -label_offset * 2.5
        ax.annotate('', xy=(-bf_bot/2, y_b), xytext=(bf_bot/2, y_b), arrowprops=arrow_props)
        ax.text(0, y_b - label_offset * 1.2, f'B={bf_bot:.0f}', fontsize=9, ha='center', va='top', fontweight='bold')
        
        # ===== DIMENSION TABLE (below B label, under the I-beam) =====
        table_y = -margin * 0.70  # Lower position, under B label
        table_text = f"tw={tw:.1f}  │  tf={tf_top:.1f}  │  R1={R1:.1f}  │  R2={R2:.1f}"
        ax.text(0, table_y, table_text, fontsize=8, ha='center', va='top', 
               color='#555', fontfamily='monospace',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='#f8f8f8', edgecolor='#ddd', alpha=0.9))
        
        # Cross-section info is now shown in bottom table instead of floating box

    def _add_bottom_tables(self, data):
        """Add tabular information at the bottom of the figure."""
        best_pos = data.get('best_pos')
        best_weight = data.get('best_weight', float('inf'))
        best_iter = data.get('best_iteration', 0)
        best_pid = data.get('best_particle_id', 0)
        best_vector = data.get('global_best_position')
        names = data.get('variable_names', [])
        
        # Extract dimensions for display
        if best_vector and names:
            dims = dict(zip(names, best_vector))
            D = dims.get('D', dims.get('d', 0))
            tw = dims.get('tw', 0)
            bf = dims.get('bf', dims.get('bf_top', 0))
            tf = dims.get('tf', dims.get('tf_top', 0))
        else:
            D = tw = bf = tf = 0
        
        # Get UR
        b_ur = best_pos[1] if best_pos else 0
        
        # === SINGLE COMBINED TABLE (larger font for better readability) ===
        table_text = (
            f"Global Best │ Iter: {best_iter + 1} │ Particle: {best_pid + 1} │ "
            f"Weight: {best_weight:.1f} kg │ D: {D:.0f} mm │ B: {bf:.0f} mm │ "
            f"tw: {tw:.1f} mm │ tf: {tf:.1f} mm │"
        )
        self.fig.text(0.50, 0.07, table_text, 
                     fontsize=10, ha='center', va='top',
                     fontfamily='monospace', fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.4', 
                              facecolor='#fffef0', edgecolor='#bbb', alpha=0.95))

    def cleanup(self):
        """Clean up matplotlib resources."""
        try:
            plt.close(self.fig)
        except Exception:
            pass


class PSOVisualizerWidget(QDialog):
    """Main PSO Visualizer Widget with 3D Cloud Plot + Cross-Section.
    
    Displayed as a fixed-size popup window (not dockable).
    Uses CustomTitleBar to match Osdag style.
    """
    switch_to_cad = Signal()
    closed = Signal()  # Emitted when the popup is closed
    
    def __init__(self, parent=None, max_iterations=100):
        super().__init__(parent)
        print("DEBUG: Loading PSO Visualizer V6 (Custom QDialog)")
        
        # Window flags: Frameless to use CustomTitleBar
        self.setWindowFlags(
            Qt.Dialog | 
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        # Fixed size popup - prevents resizing issues (larger for aesthetics)
        self.setFixedSize(1100, 700)
        
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
        self.render_timer.start(80)  # ~12 FPS for smoother real-time updates
        
    def setup_ui(self):
        """Setup the UI components."""
        self.setStyleSheet("""
            QDialog { 
                background-color: white; 
                font-family: 'Segoe UI', 'SF Pro Display', sans-serif; 
                border: 1px solid #ccc;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)  # Thin border margin
        layout.setSpacing(0)
        
        # ===== HEADER: Custom Title Bar =====
        # Matches "Additional Inputs" style
        self.titleBar = CustomTitleBar(max_res_btn=False, min_res_btn=False, parent=self)
        self.titleBar.setTitle("PSO Optimization Visualization")
        
        # Customize title bar colors to match PSO theme (optional, staying with default Osdag style is safer)
        # But we need to add the info labels (Iter, Best, Particle) below the title bar or inside it?
        # The CustomTitleBar occupies the top. We'll put the info panel BELOW it.
        
        layout.addWidget(self.titleBar)
        
        # ===== INFO PANEL (was part of header) =====
        info_panel = QFrame()
        info_panel.setFixedHeight(34)
        info_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {HEADER_GREEN};
                border-bottom: 2px solid #556619;
            }}
        """)
        info_layout = QHBoxLayout(info_panel)
        info_layout.setContentsMargins(15, 0, 15, 0)
        
        # Info labels (Iter, Best, Particle)
        
        # Iteration label
        self.lbl_iter = QLabel("ITERATION: 0")
        self.lbl_iter.setStyleSheet("""
            color: rgba(255,255,255,0.95); 
            font-size: 12px; 
            font-weight: bold;
        """)
        
        # Best weight label
        self.lbl_best = QLabel("BEST: --- kg")
        self.lbl_best.setStyleSheet("""
            color: #FFD700; 
            font-size: 12px; 
            font-weight: bold;
        """)
        
        # Best particle info
        self.lbl_particle = QLabel("PARTICLE: ---")
        self.lbl_particle.setStyleSheet("""
            color: rgba(255,255,255,0.85); 
            font-size: 11px;
        """)
        
        info_layout.addWidget(self.lbl_iter)
        info_layout.addSpacing(20)
        info_layout.addWidget(self.lbl_best)
        info_layout.addSpacing(15)
        info_layout.addWidget(self.lbl_particle)
        info_layout.addStretch()
        
        layout.addWidget(info_panel)
        
        # ===== MAIN CONTENT: Matplotlib Canvas =====
        self.canvas = MatplotlibCanvas(self)
        # Canvas uses Preferred policy set in MatplotlibCanvas.__init__
        # This prevents the matplotlib figure from demanding excessive space
        layout.addWidget(self.canvas, 1)
        
        # ===== BOTTOM TOOLBAR (Compact) =====
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(28)  # Compact footer
        bottom_bar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-top: 1px solid #ddd;
            }
        """)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(8, 2, 8, 2)
        bottom_layout.setSpacing(15)
        
        # Status label
        self.lbl_status = QLabel("Optimizing...")
        self.lbl_status.setStyleSheet("color: #666; font-size: 10px;")
        
        # Save button
        btn_style = """
            QPushButton { 
                background-color: #f0f0f0; 
                color: #333; 
                border: 1px solid #ccc;
                border-radius: 3px; 
                padding: 2px 8px;
                font-size: 10px;
            }
            QPushButton:hover { background-color: #e0e0e0; }
            QPushButton:pressed { background-color: #d0d0d0; }
            QPushButton:disabled { background-color: #f8f8f8; color: #aaa; }
        """
        
        self.btn_save = QPushButton("💾 Save Plot")
        self.btn_save.setStyleSheet(btn_style)
        self.btn_save.clicked.connect(self.save_plot)
        self.btn_save.setEnabled(False)
        
        # Legend - updated to match hollow circle markers
        legend_text = QLabel(
            "<span style='color: #FFD700;'>★</span> Best  "
            "<span style='color: #6B8E23;'>◯</span> Feasible  "
            "<span style='color: #F87171;'>◯</span> Infeasible"
        )
        legend_text.setStyleSheet("color: #333; font-size: 9px;")
        
        bottom_layout.addWidget(self.lbl_status)
        bottom_layout.addStretch()
        bottom_layout.addWidget(legend_text)
        bottom_layout.addSpacing(10)
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
        """Update canvas with latest data (uses draw_idle for background updates)."""
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
    
    def _update_canvas_immediate(self):
        """Force immediate canvas update (synchronous redraw for real-time per-iteration updates).
        
        Uses draw() instead of draw_idle() to guarantee the canvas redraws synchronously.
        This ensures the global best cross-section updates visibly each iteration.
        """
        data = self.data_processor.get_render_data()
        if data:
            # Clear and rebuild plots
            self.canvas.ax_3d.cla()
            self.canvas.ax_sect.cla()
            
            # Clear any previous figure texts (tables)
            for txt in self.canvas.fig.texts:
                txt.remove()
            
            # Rebuild all plots
            self.canvas._setup_3d_axes(data)
            self.canvas._plot_3d_cloud(data)
            self.canvas._setup_section_axes()
            self.canvas._plot_cross_section(data)
            self.canvas._add_bottom_tables(data)
            
            # Force synchronous redraw (not deferred)
            self.canvas.draw()
            self.canvas.flush_events()
            
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
        safe_processEvents()  # Use safe version to prevent AIS context race conditions
        
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
        
        # CRITICAL: Force final canvas update with latest data
        data = self.data_processor.get_render_data()
        if data:
            # Update the canvas with final data
            self.canvas.update_plot(data)
            
            # Update header labels
            best_iter = data.get('best_iteration', 0)
            best_pid = data.get('best_particle_id', 0)
            self.lbl_iter.setText(f"COMPLETE: {data['iteration'] + 1} iterations")
            self.lbl_best.setText(f"BEST: {data['best_weight']:.0f} kg")
            self.lbl_particle.setText(f"PARTICLE: {best_pid + 1} @ Iter {best_iter + 1}")
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

    def closeEvent(self, event):
        """Handle window close button click."""
        self.closed.emit()
        self.switch_to_cad.emit()
        event.accept()
