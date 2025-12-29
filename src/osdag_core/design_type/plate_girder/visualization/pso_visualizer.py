"""
Matplotlib 3D PSO Visualizer
============================
Beautiful 3D visualization of Particle Swarm Optimization using Matplotlib.

Features:
- 3D scatter plot with labeled X, Y, Z axes in empty space
- 2D convergence graph showing global best over iterations
- Threaded data processing for smooth real-time updates
- Replay functionality after optimization completes
- Save animation as GIF
- Proper labels, legends, and color coding
"""

from typing import List, Dict, Tuple, Optional
import numpy as np
from collections import deque
from threading import RLock
import os

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QApplication, QFrame, QSlider,
    QSizePolicy, QFileDialog, QRadioButton
)
from PySide6.QtGui import QFont

# Matplotlib imports with Qt backend
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation


# ============== COLORS (matching Osdag theme) ==============
SAFE_COLOR = '#4ADE80'      # Green for feasible (UR <= 1)
FAIL_COLOR = '#F87171'      # Red for infeasible (UR > 1)
OPTIMAL_COLOR = '#FFD700'   # Gold for global best
ACCENT_BLUE = '#38BDF8'     # Sky Blue
OSDAG_GREEN = '#2E9F4F'     # Osdag theme green
HEADER_GREEN = '#6B7D20'    # Osdag olive header


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
        self.convergence_history: List[Tuple[int, float]] = []
        
        # Current visible particles
        self.particles: Dict[int, Dict] = {}
        
        # Variable Metadata
        self.variable_names = []
        self.variable_bounds = {}
        
        # Best Solution Tracking
        self.best_weight = float('inf')
        self.best_pos = None
        self.best_position_vector = None
        self.variable_bounds = {'lb': [], 'ub': []}
        
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
            
            # Update best and convergence history
            if weight < self.best_weight and ur <= 1.0:
                self.best_weight = weight
                self.best_pos = (depth, ur, weight)
                if position:
                    self.best_position_vector = list(position)
            
            # Always record running best at each iteration (for smooth convergence curve)
            if self.best_weight != float('inf'):
                if (not self.convergence_history or 
                    self.convergence_history[-1][0] != iteration):
                    self.convergence_history.append((iteration, self.best_weight))
            
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
                'convergence': list(self.convergence_history),
                'history': list(self.history),
                'iteration': max((p.get('iteration', 0) for p in self.particles.values()), default=0),
                'variable_names': self.variable_names,
                'variable_bounds': self.variable_bounds
            }
    
    def get_history_frame(self, frame_idx: int) -> Optional[dict]:
        """Get accumulated particle data up to a specific frame for replay."""
        with self.lock:
            if frame_idx >= len(self.history):
                return None
            
            current_iteration = self.history[frame_idx]['iteration']
            particles = {}
            best_w = float('inf')
            best_p = None
            best_position_vector = None
            convergence = []
            
            # Build particles from ALL history up to this frame
            # This shows the evolution of particles across iterations
            for i in range(frame_idx + 1):
                h = self.history[i]
                pid = h['particle_idx']
                
                # Create particle entry if needed
                if pid not in particles:
                    particles[pid] = {'trail': deque(maxlen=10)}
                
                # Add to trail
                particles[pid]['trail'].append((h['depth'], h['ur'], h['weight']))
                particles[pid]['current'] = (h['depth'], h['ur'], h['weight'])
                if 'position' in h:
                    particles[pid]['position'] = h['position']
                particles[pid]['iteration'] = h['iteration']
                
                # Track best
                if h['weight'] < best_w and h['ur'] <= 1.0:
                    best_w = h['weight']
                    best_p = (h['depth'], h['ur'], h['weight'])
                    if 'position' in h:
                        best_position_vector = list(h['position'])
                    if (not convergence or convergence[-1][0] != h['iteration']):
                        convergence.append((h['iteration'], h['weight']))
            
            return {
                'particles': particles,
                'depth_range': list(self.depth_range),
                'ur_range': list(self.ur_range),
                'weight_range': list(self.weight_range),
                'best_pos': best_p,
                'global_best_position': best_position_vector,
                'best_weight': best_w,
                'convergence': convergence,
                'history': list(self.history[:frame_idx+1]),
                'iteration': current_iteration,
                'is_replay': True,
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
            self.convergence_history.clear()
            self.convergence_history = []
            self.particles.clear()
            self.particles = {}
            self.best_weight = float('inf')
            self.best_pos = None
            self.depth_range = [float('inf'), float('-inf')]
            self.ur_range = [0.0, 2.0]
            self.weight_range = [float('inf'), float('-inf')]


class MatplotlibCanvas(FigureCanvas):
    """Scientific Engineering Dashboard for PSO Optimization.
    
    Layout:
    [        Parallel Coordinates Plot (Search History)          ]
    [ Performance Map (Weight vs UR) ] [ Live Cross-Section View ]
    """
    
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(14, 9), dpi=80, facecolor='#ffffff')
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()
        
        # Initialize Layout
        self._setup_layout()
        
    def _setup_layout(self):
        """Create the 3-panel dashboard layout."""
        # GridSpec: 2 Rows. Top row is taller (1.2x).
        self.gs = self.fig.add_gridspec(2, 2, height_ratios=[1.1, 1], hspace=0.30, wspace=0.20, 
                                   left=0.06, right=0.96, top=0.92, bottom=0.08)
        
        # 1. Parallel Coordinates (Top)
        self.ax_parallel = self.fig.add_subplot(self.gs[0, :])
        
        # 2. Performance Map (Bottom Left)
        self.ax_perf = self.fig.add_subplot(self.gs[1, 0])
        
        # 3. Cross Section Preview (Bottom Right)
        self.ax_sect = self.fig.add_subplot(self.gs[1, 1])

    def update_plot(self, data: dict):
        """Update the entire dashboard with new frame data."""
        # Clear Axes
        self.ax_parallel.cla()
        self.ax_perf.cla()
        self.ax_sect.cla()
        self.ax_parallel.set_title("Search Dynamics V3 | Design Variable Convergence", fontsize=10, pad=10)
        
        # 1. Setup Parallel Coordinates
        self._setup_parallel_axes(data)
        self._plot_parallel_coords(data)
        
        # 2. Setup Performance Map
        self._setup_perf_axes(data)
        self._plot_performance(data)
        
        # 3. Setup Section View
        self._setup_section_axes()
        self._plot_best_section(data)
        
        self.draw_idle()

    def _setup_parallel_axes(self, data):
        """Configure Parallel Coordinates Axis."""
        self.ax_parallel.set_title("Search Dynamics | Design Variable Convergence", fontsize=10, fontweight='bold', pad=8)
        self.ax_parallel.set_ylabel("Normalized Range (%)", fontsize=9)
        self.ax_parallel.set_ylim(-2, 102)  # 0-100% with padding
        self.ax_parallel.grid(True, alpha=0.3)
        self.ax_parallel.axhline(y=0, color='k', linestyle='-', linewidth=0.5, alpha=0.3)
        self.ax_parallel.axhline(y=100, color='k', linestyle='-', linewidth=0.5, alpha=0.3)
        
        names = data.get('variable_names', [])
        if names:
            self.ax_parallel.set_xticks(range(len(names)))
            self.ax_parallel.set_xticklabels(names, rotation=15, fontsize=8)
            self.ax_parallel.set_xlim(-0.5, len(names) - 0.5)

    def _setup_perf_axes(self, data):
        """Configure Performance Map Axis."""
        self.ax_perf.set_title("Objective Space: Weight vs Constraints", fontsize=10, fontweight='bold')
        self.ax_perf.set_xlabel("Weight (kg)", fontsize=9)
        self.ax_perf.set_ylabel("Utilization Ratio (UR)", fontsize=9)
        self.ax_perf.grid(True, linestyle='--', alpha=0.5)
        
        # Feasibility Line
        self.ax_perf.axhline(y=1.0, color='r', linestyle='-', linewidth=1.5, alpha=0.6)
        self.ax_perf.text(0.02, 1.02, "Limit (UR=1.0)", transform=self.ax_perf.transAxes, color='red', fontsize=8)

    def _setup_section_axes(self):
        """Configure Section Preview Axis."""
        self.ax_sect.set_title("Best Cross-Section (To Scale)", fontsize=10, fontweight='bold')
        self.ax_sect.set_aspect('equal')
        self.ax_sect.axis('off')

    def _plot_parallel_coords(self, data):
        """Render Parallel Coordinates lines."""
        particles = data.get('particles', {})
        bounds = data.get('variable_bounds', {})
        lbs = bounds.get('lb', [])
        ubs = bounds.get('ub', [])
        
        if not lbs or not ubs:
            # Try to grab from global if available (fallback)
            self.ax_parallel.text(0.5, 0.5, "Waiting for Bounds...", ha='center', transform=self.ax_parallel.transAxes)
            return

        segments = []
        colors = []
        
        # 1. Plot History (Faint Background)
        history = data.get('history', [])
        # Optimization: Limit history rendering to last 500 feasible points to avoid lag if critical
        # But user asked for it, so let's try rendering 1000 sample
        
        hist_segments = []
        hist_colors = []
        
        for entry in history[-2000:]: # Limit to last 2000 for perf
            pos = entry.get('position')
            ur = entry.get('ur', 0)
            
            if pos and len(pos) == len(lbs):
                 norm_pos = []
                 for i, val in enumerate(pos):
                    span = ubs[i] - lbs[i]
                    if span == 0: span = 1
                    norm = (val - lbs[i]) / span * 100
                    norm_pos.append(norm)
                 
                 hist_segments.append(list(enumerate(norm_pos)))
                 hist_colors.append((0.5, 0.5, 0.6, 0.05)) # Neutral Grey-Blue for History

        if hist_segments:
             lc_hist = LineCollection(hist_segments, colors=hist_colors, linewidths=0.5)
             self.ax_parallel.add_collection(lc_hist)

        # 2. Plot Current Swarm (Bold)
        segments = []
        colors = []
        
        for p_data in particles.values():
            pos = p_data.get('position')
            ur = p_data.get('current', (0,0,0))[1]
            
            if pos and len(pos) == len(lbs):
                # Normalize Position
                norm_pos = []
                for i, val in enumerate(pos):
                    span = ubs[i] - lbs[i]
                    if span == 0: span = 1
                    norm = (val - lbs[i]) / span * 100
                    norm_pos.append(norm)
                
                points = list(enumerate(norm_pos))
                segments.append(points)
                
                # Color Code
                if ur <= 1.0:
                    colors.append('blue') # Standard Blue
                else:
                    colors.append('red') # Standard Red
            else:
                 # Debug check
                 pass # Already debugged

        if segments:
            lc = LineCollection(segments, colors=colors, linewidths=2.0) # Thicker lines
            self.ax_parallel.add_collection(lc)

        # 3. Plot Global Best (Persistent Gold Line)
        best_vec = data.get('global_best_position')
        if best_vec and len(best_vec) == len(lbs):
             norm_best = []
             for i, val in enumerate(best_vec):
                span = ubs[i] - lbs[i]
                if span == 0: span = 1
                norm = (val - lbs[i]) / span * 100
                norm_best.append(norm)
             
             # Plot as a distinct dashed line
             self.ax_parallel.plot(range(len(norm_best)), norm_best, color='gold', linewidth=3.0, linestyle='--', label='Global Best')
             # Add dots at vertices
             self.ax_parallel.scatter(range(len(norm_best)), norm_best, color='gold', s=40, zorder=10)

    def _plot_performance(self, data):
        """Render Performance Scatter with History."""
        particles = data.get('particles', {})
        history = data.get('history', [])
        
        # 1. History Points
        h_weights = []
        h_urs = []
        h_colors = []
        
        for entry in history[-3000:]: # Limit to last 3000
            w = entry.get('weight', 0)
            ur = entry.get('ur', 0)
            h_weights.append(w)
            h_urs.append(ur)
            if ur > 1.0: h_colors.append('#FCA5A533') # Fade Red
            else: h_colors.append('#93C5FD44') # Fade Blue (Wait, #93C5FD is blue-300)
            
        if h_weights:
            self.ax_perf.scatter(h_weights, h_urs, c=h_colors, s=10, marker='.', edgecolors='none') # Bigger dots
            
        # 2. Current Swarm
        weights = []
        urs = []
        colors = []
        
        for p_data in particles.values():
            _, ur, w = p_data.get('current', (0,0,0))
            weights.append(w)
            urs.append(ur)
            
            if ur > 1.0:
                colors.append('#DC2626') # Strong Red
            else:
                colors.append('#2563EB') # Strong Blue
        
        if weights:
             self.ax_perf.scatter(weights, urs, c=colors, s=30, alpha=1.0, edgecolors='white', linewidth=0.5)
             
             # Highlight Best (Vertical Line + Star)
             best_w = data.get('best_weight')
             best_p = data.get('best_pos') # (depth, ur, weight)
             
             if best_w and best_w != float('inf'):
                 self.ax_perf.axvline(x=best_w, color='#F59E0B', linestyle='--', alpha=0.8, linewidth=1.5)
                 
                 # Plot the specific Best Point if available
                 if best_p:
                     _, best_ur, _ = best_p
                     self.ax_perf.scatter([best_w], [best_ur], c='gold', s=80, marker='D', edgecolors='black', zorder=20, label='Global Best')
                 
                 # Dynamic Limits
                 all_w = weights + h_weights
                 all_ur = urs + h_urs
                 if all_w:
                     min_w, max_w = min(all_w), max(all_w)
                     margin = (max_w - min_w) * 0.1 if max_w != min_w else 1000
                     self.ax_perf.set_xlim(min_w - margin, max_w + margin)
                     self.ax_perf.set_ylim(0, max(2.0, max(all_ur) if all_ur else 2.0))

    def _plot_best_section(self, data):
        """Render the best cross-section using stored GLOBAL BEST vector."""
        names = data.get('variable_names', [])
        best_vector = data.get('global_best_position')
        
        if best_vector and names:
            dims = dict(zip(names, best_vector))
            D = dims.get('D', 1000)
            tw = dims.get('tw', 8)
            
            if 'bf' in dims and 'tf' in dims:
                 bf_top = bf_bot = dims['bf']
                 tf_top = tf_bot = dims['tf']
            else:
                bf_top = dims.get('bf_top', 200)
                bf_bot = dims.get('bf_bot', 200)
                tf_top = dims.get('tf_top', 12)
                tf_bot = dims.get('tf_bot', 12)
            
            patches = []
            patches.append(Rectangle((-bf_bot/2, 0), bf_bot, tf_bot)) # Bot
            patches.append(Rectangle((-tw/2, tf_bot), tw, D - tf_top - tf_bot)) # Web
            patches.append(Rectangle((-bf_top/2, D - tf_top), bf_top, tf_top)) # Top
            
            pc = PatchCollection(patches, facecolor='#2563EB', edgecolor='#1E3A8A', alpha=0.9)
            self.ax_sect.add_collection(pc)
            
            max_w = max(bf_top, bf_bot)
            self.ax_sect.set_xlim(-max_w - 50, max_w + 50)
            self.ax_sect.set_ylim(-100, D + 150)
            
            self.ax_sect.text(0, D/2, f"D={D:.0f}\ntw={tw:.1f}", ha='center', va='center', fontsize=10, color='white', fontweight='bold')
            self.ax_sect.text(0, -50, f"Bot: {bf_bot:.0f}x{tf_bot:.1f}", ha='center', fontsize=9)
            self.ax_sect.text(0, D + 20, f"Top: {bf_top:.0f}x{tf_top:.1f}", ha='center', fontsize=9)
        else:
             msg = "No Feasible Solution Yet"
             if not names: msg += "\n(Waiting for Metadata)"
             elif not best_vector: msg += "\n(Searching...)"
             self.ax_sect.text(0.5, 0.5, msg, ha='center', transform=self.ax_sect.transAxes)

    def cleanup(self):
        """Clean up matplotlib resources."""
        try:
            plt.close(self.fig)
        except Exception:
            pass
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()
        
        # Create subplots: 3D on left (75% width), 2D convergence on right (25%)
        from matplotlib.gridspec import GridSpec
        gs = GridSpec(1, 4, figure=self.fig)  # 4 columns
        self.ax_3d = self.fig.add_subplot(gs[0, :3], projection='3d')  # First 3 columns
        self.ax_conv = self.fig.add_subplot(gs[0, 3])  # Last column
        
        # Style the 3D axes
        self._setup_3d_axes()
        self._setup_convergence_axes()
        
        self.fig.tight_layout(pad=2.0)
        
        # Data lock
        self.lock = Lock()
        self.render_data = None
        
        # Scatter and line plot references (for efficient updates)
        self._scatter_feasible = None
        self._scatter_infeasible = None
        self._scatter_best = None
        self._conv_line = None
        
    def _setup_3d_axes(self):
        """Configure 3D axes appearance."""
        ax = self.ax_3d
        
        # Set labels
        ax.set_xlabel('X (Depth)', fontsize=10, fontweight='bold', labelpad=10)
        ax.set_ylabel('Y (Weight)', fontsize=10, fontweight='bold', labelpad=10)
        ax.set_zlabel('Z (Feasibility)', fontsize=10, fontweight='bold', labelpad=10)
        
        # Title
        ax.set_title('3D PSO Convergence', fontsize=12, fontweight='bold', pad=15)
        
        # Set background to white (empty space style)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        
        # Make panes transparent
        ax.xaxis.pane.set_edgecolor('lightgray')
        ax.yaxis.pane.set_edgecolor('lightgray')
        ax.zaxis.pane.set_edgecolor('lightgray')
        
        # Grid
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Initial view angle
        ax.view_init(elev=25, azim=225)
        
    def _setup_convergence_axes(self):
        """Configure 2D convergence axes appearance."""
        ax = self.ax_conv
        
        ax.set_xlabel('Iteration', fontsize=11, fontweight='bold')
        ax.set_ylabel('Best Value', fontsize=11, fontweight='bold')
        ax.set_title('Global Best Convergence', fontsize=12, fontweight='bold')
        
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('white')
        
        # Initialize Layout
        self._setup_layout()
        
    def _setup_layout(self):
        """Create the 3-panel dashboard layout."""
        # GridSpec: 2 Rows. Top row is taller (1.2x).
        self.gs = self.fig.add_gridspec(2, 2, height_ratios=[1.1, 1], hspace=0.30, wspace=0.20, 
                                   left=0.06, right=0.96, top=0.92, bottom=0.08)
        
        # 1. Parallel Coordinates (Top)
        self.ax_parallel = self.fig.add_subplot(self.gs[0, :])
        
        # 2. Performance Map (Bottom Left)
        self.ax_perf = self.fig.add_subplot(self.gs[1, 0])
        
        # 3. Cross Section Preview (Bottom Right)
        self.ax_sect = self.fig.add_subplot(self.gs[1, 1])

    def update_plot(self, data: dict):
        """Update the entire dashboard with new frame data."""
        # Clear Axes
        self.ax_parallel.cla()
        self.ax_perf.cla()
        self.ax_sect.cla()
        
        # 1. Setup Parallel Coordinates
        self._setup_parallel_axes(data)
        self._plot_parallel_coords(data)
        
        # 2. Setup Performance Map
        self._setup_perf_axes(data)
        self._plot_performance(data)
        
        # 3. Setup Section View
        self._setup_section_axes()
        self._plot_best_section(data)
        
        self.draw_idle()

    def _setup_parallel_axes(self, data):
        """Configure Parallel Coordinates Axis."""
        self.ax_parallel.set_title("Search Dynamics | Design Variable Convergence", fontsize=10, fontweight='bold', pad=8)
        self.ax_parallel.set_ylabel("Normalized Range (%)", fontsize=9)
        self.ax_parallel.set_ylim(-2, 102)  # 0-100% with padding
        self.ax_parallel.grid(True, alpha=0.3)
        self.ax_parallel.axhline(y=0, color='k', linestyle='-', linewidth=0.5, alpha=0.3)
        self.ax_parallel.axhline(y=100, color='k', linestyle='-', linewidth=0.5, alpha=0.3)
        
        # Set x-ticks from variable names
        names = data.get('variable_names', [])
        if names:
            self.ax_parallel.set_xticks(range(len(names)))
            self.ax_parallel.set_xticklabels(names, rotation=15, fontsize=8)
            self.ax_parallel.set_xlim(-0.5, len(names) - 0.5)

    def _setup_perf_axes(self, data):
        """Configure Performance Map Axis."""
        self.ax_perf.set_title("Objective Space: Weight vs Constraints", fontsize=10, fontweight='bold')
        self.ax_perf.set_xlabel("Weight (kg)", fontsize=9)
        self.ax_perf.set_ylabel("Utilization Ratio (UR)", fontsize=9)
        self.ax_perf.grid(True, linestyle='--', alpha=0.5)
        
        # Feasibility Line
        self.ax_perf.axhline(y=1.0, color='r', linestyle='-', linewidth=1.5, alpha=0.6)
        self.ax_perf.text(0.02, 1.02, "Limit (UR=1.0)", transform=self.ax_perf.transAxes, color='red', fontsize=8)

    def _setup_section_axes(self):
        """Configure Section Preview Axis."""
        self.ax_sect.set_title("Best Cross-Section (To Scale)", fontsize=10, fontweight='bold')
        self.ax_sect.set_aspect('equal')
        self.ax_sect.axis('off')

    def _plot_parallel_coords(self, data):
        """Render Parallel Coordinates lines."""
        particles = data.get('particles', {})
        bounds = data.get('variable_bounds', {})
        lbs = bounds.get('lb', [])
        ubs = bounds.get('ub', [])
        
        if not lbs or not ubs:
            self.ax_parallel.text(0.5, 0.5, "Waiting for Bounds...", ha='center', transform=self.ax_parallel.transAxes)
            return

        segments = []
        colors = []
        
        # Iterate particles
        for p_data in particles.values():
            pos = p_data.get('position')
            ur = p_data.get('current', (0,0,0))[1]
            
            if pos and len(pos) == len(lbs):
                # Normalize Position: (val - min) / (max - min) * 100
                norm_pos = []
                for i, val in enumerate(pos):
                    span = ubs[i] - lbs[i]
                    if span == 0: span = 1  # Avoid division by zero
                    norm = (val - lbs[i]) / span * 100
                    norm_pos.append(norm)
                
                # Create polyline points: (x_idx, y_norm_val)
                points = list(enumerate(norm_pos))
                segments.append(points)
                
                # Color Code
                if ur <= 1.0:
                    colors.append((0.1, 0.7, 0.3, 0.2)) # Green, translucent
                else:
                    colors.append((0.9, 0.1, 0.1, 0.05)) # Red, very faint

        if segments:
            from matplotlib.collections import LineCollection
            lc = LineCollection(segments, colors=colors, linewidths=1.0)
            self.ax_parallel.add_collection(lc)

    def _plot_performance(self, data):
        """Render Performance Scatter."""
        particles = data.get('particles', {})
        weights = []
        urs = []
        colors = []
        
        for p_data in particles.values():
            # Get currentUR/Weight
            _, ur, w = p_data.get('current', (0,0,0))
            weights.append(w)
            urs.append(ur)
            
            # Color map based heavily on Feasibility
            if ur > 1.0:
                colors.append('#F87171') # Red
            else:
                colors.append('#4ADE80') # Green
        
        if weights:
             self.ax_perf.scatter(weights, urs, c=colors, s=20, alpha=0.7, edgecolors='none')
             
             # Highlight Global Best
             best_w = data.get('best_weight')
             if best_w and best_w != float('inf'):
                 # Find matching point (heuristic)
                 self.ax_perf.axvline(x=best_w, color='blue', linestyle='--', alpha=0.4)
                 
                 # Set dynamic limits
                 min_w, max_w = min(weights), max(weights)
                 margin = (max_w - min_w) * 0.1 if max_w != min_w else 100
                 self.ax_perf.set_xlim(min_w - margin, max_w + margin)
                 self.ax_perf.set_ylim(0, max(2.0, max(urs)))

    def _plot_best_section(self, data):
        """Render the best cross-section."""
        particles = data.get('particles', {})
        names = data.get('variable_names', [])
        best_w = data.get('best_weight', float('inf'))
        
        best_vector = None
        
        # Find the vector corresponding to best weight (feasible)
        # Note: DataProcessor tracks 'best_pos' but it is (d, u, w). Use particles to find full vector.
        for p_data in particles.values():
            _, ur, w = p_data.get('current', (0,0,0))
            if w == best_w and ur <= 1.0:
                 best_vector = p_data.get('position')
                 break
        
        if best_vector and names:
            from matplotlib.patches import Rectangle
            from matplotlib.collections import PatchCollection
            # Map values
            dims = dict(zip(names, best_vector))
            
            # Extract Dimensions
            D = dims.get('D', 1000)
            tw = dims.get('tw', 8)
            
            if 'bf' in dims:
                bf_top = bf_bot = dims['bf']
                tf_top = tf_bot = dims['tf']
            else:
                bf_top = dims.get('bf_top', 200)
                bf_bot = dims.get('bf_bot', 200)
                tf_top = dims.get('tf_top', 12)
                tf_bot = dims.get('tf_bot', 12)
            
            # Draw Patches
            patches = []
            
            # Bottom Flange
            patches.append(Rectangle((-bf_bot/2, 0), bf_bot, tf_bot))
            
            # Web
            patches.append(Rectangle((-tw/2, tf_bot), tw, D - tf_top - tf_bot))
            
            # Top Flange
            patches.append(Rectangle((-bf_top/2, D - tf_top), bf_top, tf_top))
            
            pc = PatchCollection(patches, facecolor='#3b82f6', edgecolor='#1e40af', alpha=0.8)
            self.ax_sect.add_collection(pc)
            
            # Set Limits
            max_w = max(bf_top, bf_bot)
            self.ax_sect.set_xlim(-max_w, max_w)
            self.ax_sect.set_ylim(-100, D + 100)
            
            # Annotate
            self.ax_sect.text(0, D/2, f"D={D:.0f}\ntw={tw:.1f}", ha='center', va='center', fontsize=9, color='white', fontweight='bold')
            self.ax_sect.text(0, -50, f"Bot: {bf_bot:.0f}x{tf_bot:.1f}", ha='center', fontsize=8)
            self.ax_sect.text(0, D + 20, f"Top: {bf_top:.0f}x{tf_top:.1f}", ha='center', fontsize=8)
        else:
             self.ax_sect.text(0.5, 0.5, "No Feasible Solution Yet", ha='center', transform=self.ax_sect.transAxes)

    def cleanup(self):
        """Clean up matplotlib resources."""
        try:
            plt.close(self.fig)
        except Exception:
            pass


class PSOVisualizerWidget(QWidget):
    """Main PSO Visualizer Widget with Matplotlib rendering."""
    switch_to_cad = Signal()
    
    def __init__(self, parent=None, max_iterations=100):
        super().__init__(parent)
        print("DEBUG: Loading Updated PSO Visualizer V2 (Blue Theme + Global Best)")
        self.setWindowFlags(self.windowFlags() | Qt.Dialog)
        self.max_iter = max_iterations
        self.is_complete = False
        self.is_replaying = False
        
        # Data processor
        self.data_processor = DataProcessor()
        
        # Batch buffer for performance
        self.batch_buffer = {'d': [], 'u': [], 'w': [], 'i': [], 'p': []}
        
        # Pre-rendered frame cache for smooth replay
        self.cached_frames = []  # List of (iteration, best_w, history_idx) tuples
        self.is_replaying = False
        self.cache_index = 0
        self.cached_data = {}
        self.cache_ready = False
        
        # Interactive Tooltip State
        self.tooltip = None
        self.hover_active = False
        self.current_scatters = {}
        self.current_frame_real_data = {}
        
        # Setup UI
        self.setup_ui()
        
        # Timer for replay
        self.replay_timer = QTimer()
        self.replay_timer.timeout.connect(self._replay_tick)
        self.replay_frame = 0
        self.replay_speed = 5
        
        # Render timer (update canvas from data)
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self._update_canvas)
        self.render_timer.start(100)  # 10 FPS for smooth performance
        
    
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
        header_layout.addSpacing(25)
        header_layout.addWidget(close_btn)
        
        layout.addWidget(header)
        
        # ===== MAIN CONTENT =====
        content = QHBoxLayout()
        content.setContentsMargins(0, 0, 0, 0)
        
        # Matplotlib Canvas
        self.canvas = MatplotlibCanvas(self)
        self.canvas.mpl_connect("motion_notify_event", self._on_hover)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Just the canvas - no side panel!
        content.addWidget(self.canvas, 1)
        
        layout.addLayout(content)
        
        # ===== COMPACT BOTTOM TOOLBAR (Plain white) =====
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(45)
        bottom_bar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-top: 1px solid #ddd;
            }
        """)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(15, 5, 15, 5)
        bottom_layout.setSpacing(8)
        
        # Common button style (light theme)
        btn_style = """
            QPushButton { 
                background-color: #f0f0f0; 
                color: #333; 
                border: 1px solid #ccc;
                border-radius: 3px; 
                padding: 4px 8px;
                font-size: 14px;
                min-width: 28px;
            }
            QPushButton:hover { background-color: #e0e0e0; }
            QPushButton:pressed { background-color: #d0d0d0; }
            QPushButton:disabled { background-color: #f8f8f8; color: #aaa; }
        """
        
        # Step back button |<
        self.btn_step_back = QPushButton("⏮")
        self.btn_step_back.setStyleSheet(btn_style)
        self.btn_step_back.clicked.connect(self._step_back)
        self.btn_step_back.setEnabled(False)
        
        # Previous frame <
        self.btn_prev = QPushButton("◀")
        self.btn_prev.setStyleSheet(btn_style)
        self.btn_prev.clicked.connect(self._prev_frame)
        self.btn_prev.setEnabled(False)
        
        # Play/Pause button
        self.btn_play = QPushButton("▶")
        self.btn_play.setStyleSheet(btn_style.replace("min-width: 28px", "min-width: 35px"))
        self.btn_play.clicked.connect(self._toggle_play)
        self.btn_play.setEnabled(False)
        
        # Next frame >
        self.btn_next = QPushButton("▶")
        self.btn_next.setStyleSheet(btn_style)
        self.btn_next.clicked.connect(self._next_frame)
        self.btn_next.setEnabled(False)
        
        # Step forward >|
        self.btn_step_fwd = QPushButton("⏭")
        self.btn_step_fwd.setStyleSheet(btn_style)
        self.btn_step_fwd.clicked.connect(self._step_forward)
        self.btn_step_fwd.setEnabled(False)
        
        # Loop mode radio buttons
        self.loop_once = QRadioButton("Once")
        self.loop_loop = QRadioButton("Loop")
        self.loop_loop.setChecked(True)
        for rb in [self.loop_once, self.loop_loop]:
            rb.setStyleSheet("color: #333; font-size: 11px;")
        
        # Save GIF button
        self.btn_save = QPushButton("💾 Save")
        self.btn_save.setStyleSheet(btn_style.replace("min-width: 28px", "min-width: 60px"))
        self.btn_save.clicked.connect(self.save_animation)
        self.btn_save.setEnabled(False)
        
        # Frame counter
        self.lbl_frame = QLabel("Frame: 0/0")
        self.lbl_frame.setStyleSheet("color: #666; font-size: 10px;")
        
        # Legend info (compact) - colored icons for clarity
        legend_text = QLabel("<span style='color: #FFD700;'>★</span> Best  <span style='color: #4ADE80;'>●</span> Feasible  <span style='color: #F87171;'>●</span> Infeasible")
        legend_text.setStyleSheet("color: #333; font-size: 10px;")
        
        bottom_layout.addWidget(self.btn_step_back)
        bottom_layout.addWidget(self.btn_prev)
        bottom_layout.addWidget(self.btn_play)
        bottom_layout.addWidget(self.btn_next)
        bottom_layout.addWidget(self.btn_step_fwd)
        bottom_layout.addSpacing(15)
        bottom_layout.addWidget(self.loop_once)
        bottom_layout.addWidget(self.loop_loop)
        bottom_layout.addSpacing(15)
        bottom_layout.addWidget(self.btn_save)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.lbl_frame)
        bottom_layout.addSpacing(20)
        bottom_layout.addWidget(legend_text)
        
        layout.addWidget(bottom_bar)
        
        # Store reference for enabling later
        self.bottom_controls = [self.btn_step_back, self.btn_prev, self.btn_play, 
                                self.btn_next, self.btn_step_fwd, self.btn_save]
    
    def add_particle_data(self, depth: float, ur: float, weight: float,
                          iteration: int, particle_idx: int, position: list = None, 
                          variables: list = None, lb: list = None, ub: list = None):
        """Add particle data (called from optimization)."""
        if self.is_complete and not self.is_replaying:
            return
        
        # Buffer for batch processing
        self.batch_buffer['d'].append(depth)
        self.batch_buffer['u'].append(ur)
        self.batch_buffer['w'].append(weight)
        self.batch_buffer['i'].append(iteration)
        self.batch_buffer['p'].append(particle_idx)
        # Store position/vars only if present (assume parallel lists or just append None)
        # To keep it simple, we will expand the buffer dict
        if 'pos' not in self.batch_buffer: self.batch_buffer['pos'] = []
        if 'vars' not in self.batch_buffer: self.batch_buffer['vars'] = []
        if 'lb' not in self.batch_buffer: self.batch_buffer['lb'] = []
        if 'ub' not in self.batch_buffer: self.batch_buffer['ub'] = []
        
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
        
        self.batch_buffer = {'d': [], 'u': [], 'w': [], 'i': [], 'p': [], 'pos': [], 'vars': [], 'lb': [], 'ub': []}
    
    def _update_canvas(self):
        """Update canvas with latest data."""
        if self.is_replaying:
            return
        
        data = self.data_processor.get_render_data()
        if data:
            self.canvas.update_plot(data)
        
        # Update labels
        if data:
            self.lbl_iter.setText(f"ITERATION: {data['iteration'] + 1}")
            if data['best_weight'] != float('inf'):
                self.lbl_best.setText(f"BEST: {data['best_weight']:.0f} kg")
    
    def _step_back(self):
        """Go to first cached frame."""
        if self.cache_ready and len(self.cached_frames) > 0:
            self.cache_index = 0
            self._show_cached_frame()
        else:
            self.replay_frame = 0
            self._show_frame()
    
    def _prev_frame(self):
        """Go to previous cached frame."""
        if self.cache_ready and len(self.cached_frames) > 0:
            self.cache_index = max(0, self.cache_index - 1)
            self._show_cached_frame()
        else:
            self.replay_frame = max(0, self.replay_frame - 10)
            self._show_frame()
    
    def _toggle_play(self):
        """Toggle play/pause - uses cached frames for smooth playback."""
        if self.is_replaying:
            self.replay_timer.stop()
            self.is_replaying = False
            self.btn_play.setText("▶")
        else:
            if not self.cache_ready or len(self.cached_frames) == 0:
                print("[INFO] Cache not ready, building...")
                self._build_frame_cache()
            self.is_replaying = True
            self.cache_index = 0
            self.btn_play.setText("⏸")
            self.replay_timer.start(200)  # 5 FPS for smooth cached playback
    
    def _next_frame(self):
        """Go to next cached frame."""
        if self.cache_ready and len(self.cached_frames) > 0:
            self.cache_index = min(len(self.cached_frames) - 1, self.cache_index + 1)
            self._show_cached_frame()
        else:
            # Fallback to live rendering
            history_len = self.data_processor.get_history_length()
            self.replay_frame = min(history_len - 1, self.replay_frame + 10)
            self._show_frame()
    
    def _step_forward(self):
        """Go to last cached frame."""
        if self.cache_ready and len(self.cached_frames) > 0:
            self.cache_index = len(self.cached_frames) - 1
            self._show_cached_frame()
        else:
            history_len = self.data_processor.get_history_length()
            self.replay_frame = history_len - 1
            self._show_frame()
    
    def _show_frame(self):
        """Display current frame (live render - slow, used as fallback)."""
        data = self.data_processor.get_history_frame(self.replay_frame)
        if data:
            # Remove is_replay flag to get full mesh
            data['is_replay'] = False
            self.canvas.update_plot(data)
            self.lbl_iter.setText(f"ITERATION: {data['iteration'] + 1}")
            if data['best_weight'] != float('inf'):
                self.lbl_best.setText(f"BEST: {data['best_weight']:.0f} kg")
        history_len = self.data_processor.get_history_length()
        self.lbl_frame.setText(f"Frame: {self.replay_frame}/{history_len}")
    
    def _show_cached_frame(self):
        """Display a pre-computed cached frame - Batched Rendering."""
        if not self.cached_frames or self.cache_index >= len(self.cached_frames):
            return
        
        iteration, best_w, history_idx = self.cached_frames[self.cache_index]
        
        if self.cache_index in self.cached_data:
            data = self.cached_data[self.cache_index]
            self.canvas.update_plot(data)
            
            # Update labels (1-based)
            self.lbl_iter.setText(f"ITERATION: {data['iteration'] + 1}")
            if data['best_weight'] != float('inf'):
                self.lbl_best.setText(f"BEST: {data['best_weight']:.0f} kg")
            self.lbl_frame.setText(f"Frame: {self.cache_index + 1}/{len(self.cached_frames)}")
    
    def _render_batched_scene(self, cache_idx: int):
        """Render Cached Frame to Dashboard."""
        if cache_idx not in self.cached_data:
            return
            
        data = self.cached_data[cache_idx]
        self.canvas.update_plot(data)

    def _on_hover(self, event):
        """Hover interaction handled by interactive backend if needed."""
        pass
    
    def _replay_tick(self):
        """Advance replay using cached iteration frames."""
        if not self.cache_ready or len(self.cached_frames) == 0:
            self.replay_timer.stop()
            self.is_replaying = False
            self.btn_play.setText("▶")
            return
        
        self.cache_index += 1
        
        if self.cache_index >= len(self.cached_frames):
            if self.loop_loop.isChecked():
                self.cache_index = 0
            else:
                self.cache_index = len(self.cached_frames) - 1
                self.replay_timer.stop()
                self.is_replaying = False
                self.btn_play.setText("▶")
        
        self._show_cached_frame()
    
    def _build_frame_cache(self):
        """Build cache for Replay."""
        self.cached_frames = []
        self.cached_data = {}
        history_len = self.data_processor.get_history_length()
        
        print(f"[INFO] Caching {history_len} frames for Dashboard...")
        
        # Optimize: Access history directly to find last index per iteration
        with self.data_processor.lock:
            full_history = self.data_processor.history
            seen_iterations = {}
            for i, h in enumerate(full_history):
                it = h['iteration']
                # Always overwrite to store the LAST index for this iteration
                # This ensures we show the state after ALL particles have moved
                seen_iterations[it] = (it, h['weight'], i)
        
        self.cached_frames = sorted(seen_iterations.values(), key=lambda x: x[0])
        
        # Store raw frames
        for cidx, (iteration, best_w, hidx) in enumerate(self.cached_frames):
            data = self.data_processor.get_history_frame(hidx)
            if data:
                self.cached_data[cidx] = data
            
        self.cache_ready = True
        print(f"[INFO] Built {len(self.cached_frames)} history frames")
    
    def save_animation(self):
        """Save convergence as static image (fast, no animation lag)."""
        history_len = self.data_processor.get_history_length()
        
        # Save as PNG instead of GIF (much faster, no animation processing)
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Convergence Plot", "pso_convergence.png", 
            "PNG Files (*.png);;All Files (*)"
        )
        
        if not file_path:
            return
        
        self.btn_save.setText("Saving...")
        self.btn_save.setEnabled(False)
        QApplication.processEvents()
        
        try:
            # Create a simple static convergence plot (FAST - no animation)
            fig = Figure(figsize=(10, 5), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            # Get final convergence data
            final_data = self.data_processor.get_render_data()
            conv = final_data.get('convergence', [])
            
            if conv:
                iters = [c[0] for c in conv]
                vals = [c[1] for c in conv]
                ax.plot(iters, vals, 'b-', linewidth=2, marker='o', markersize=4)
                ax.fill_between(iters, vals, alpha=0.3)
            
            ax.set_xlabel('Iteration', fontsize=12)
            ax.set_ylabel('Best Weight (kg)', fontsize=12)
            ax.set_title('PSO Convergence', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            # Add best value annotation
            best_w = final_data.get('best_weight', float('inf'))
            if best_w != float('inf'):
                ax.axhline(y=best_w, color='green', linestyle='--', alpha=0.7, 
                          label=f'Best: {best_w:.0f} kg')
                ax.legend(loc='upper right')
            
            fig.tight_layout()
            fig.savefig(file_path, dpi=150, bbox_inches='tight')
            plt.close(fig)
            
            self.btn_save.setText("✓ Saved!")
        except Exception as e:
            print(f"[WARNING] Failed to save: {e}")
            self.btn_save.setText("❌ Failed")
        finally:
            QTimer.singleShot(2000, lambda: self.btn_save.setText("💾 Save"))
            QTimer.singleShot(2000, lambda: self.btn_save.setEnabled(True))
    
    def set_complete(self):
        """Mark optimization as complete and prepare replay cache."""
        self._flush_buffer()
        self.is_complete = True
        self.lbl_iter.setText("OPTIMIZATION COMPLETE")
        
        # Build iteration cache for smooth replay
        self._build_frame_cache()
        
        # Enable bottom toolbar controls
        for ctrl in self.bottom_controls:
            ctrl.setEnabled(True)
        
        # Update frame counter with cached frame count
        self.lbl_frame.setText(f"Frame: {len(self.cached_frames)}/{len(self.cached_frames)}")
    
    def cleanup(self):
        """Clean up resources safely."""
        try:
            if hasattr(self, 'render_timer') and self.render_timer:
                self.render_timer.stop()
        except Exception:
            pass
        
        try:
            if hasattr(self, 'replay_timer') and self.replay_timer:
                self.replay_timer.stop()
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
