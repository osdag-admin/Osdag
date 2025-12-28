"""
🚀 FUTURISTIC 3D PSO CONVERGENCE VISUALIZER 🚀

A premium, manim-inspired visualization showing particle swarm optimization
in a single unified 3D space with glowing particles and convergence trails.

Axes:
- X: Total Depth (mm)
- Y: Utilization Ratio
- Z: Weight (kg)

Features:
- Glowing particle effect with color gradient by iteration
- Convergence trails showing particle movement history
- Rotating camera for dynamic view
- Dark futuristic theme with neon accents
- Live stats overlay
- Replay with smooth animation

Uses matplotlib with FigureCanvasQTAgg for stable Qt integration.
"""

from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
from collections import deque

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QProgressBar, QPushButton, QComboBox, QSlider
)
from PySide6.QtGui import QFont

# Matplotlib with Qt backend
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors


# =============================================================================
# Data Store with History for Trails
# =============================================================================

class ParticleDataStore:
    """Storage for particle evaluation history with trail support."""
    
    def __init__(self, max_points: int = 5000):
        self.depths: List[float] = []
        self.urs: List[float] = []
        self.weights: List[float] = []
        self.iterations: List[int] = []
        self.particle_ids: List[int] = []
        self.max_points = max_points
        
        # Track best solution path
        self.best_history: List[Tuple[float, float, float]] = []
        self.best_depth = float('inf')
        self.best_ur = float('inf')
        self.best_weight = float('inf')
        self.current_iteration = 0
        
    def add(self, depth: float, ur: float, weight: float, iteration: int, particle_idx: int):
        self.depths.append(depth)
        self.urs.append(ur)
        self.weights.append(weight)
        self.iterations.append(iteration)
        self.particle_ids.append(particle_idx)
        self.current_iteration = max(self.current_iteration, iteration)
        
        # Track best solution (feasible with lowest weight)
        if ur <= 1.0 and weight < self.best_weight:
            self.best_depth = depth
            self.best_ur = ur
            self.best_weight = weight
            self.best_history.append((depth, ur, weight))
            
        # Limit memory
        if len(self.depths) > self.max_points:
            self.depths = self.depths[-self.max_points:]
            self.urs = self.urs[-self.max_points:]
            self.weights = self.weights[-self.max_points:]
            self.iterations = self.iterations[-self.max_points:]
            self.particle_ids = self.particle_ids[-self.max_points:]
    
    def get_arrays(self, up_to: int = None):
        n = up_to if up_to else len(self.depths)
        return (np.array(self.depths[:n]), 
                np.array(self.urs[:n]), 
                np.array(self.weights[:n]),
                np.array(self.iterations[:n]))
    
    def clear(self):
        self.depths.clear()
        self.urs.clear()
        self.weights.clear()
        self.iterations.clear()
        self.particle_ids.clear()
        self.best_history.clear()
        self.best_depth = float('inf')
        self.best_ur = float('inf')
        self.best_weight = float('inf')
        self.current_iteration = 0
    
    def __len__(self):
        return len(self.depths)


# =============================================================================
# Futuristic 3D Canvas 
# =============================================================================

class Futuristic3DCanvas(FigureCanvas):
    """
    A single unified 3D visualization with futuristic style.
    X = Depth, Y = UR, Z = Weight
    """
    
    def __init__(self, parent=None):
        # Create figure with dark background
        self.fig = Figure(figsize=(10, 8), dpi=100, facecolor='#0a0a0f')
        super().__init__(self.fig)
        
        # 3D axes
        self.ax = self.fig.add_subplot(111, projection='3d', facecolor='#0a0a0f')
        self.fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.02)
        
        # Camera rotation angle (for animation)
        self.camera_angle = 45
        
        # Store plot elements
        self.scatter = None
        self.trail_line = None
        self.best_marker = None
        
        self._setup_dark_theme()
        
    def _setup_dark_theme(self):
        """Apply futuristic dark theme with neon accents."""
        ax = self.ax
        
        # Title with glow effect
        ax.set_title("⚡ PSO CONVERGENCE - 3D PARAMETER SPACE ⚡", 
                    color='#00d4ff', fontsize=14, fontweight='bold', 
                    pad=15, fontfamily='monospace')
        
        # Axis labels with neon colors
        ax.set_xlabel('Depth (mm)', color='#ff6b6b', fontsize=10, labelpad=8)
        ax.set_ylabel('Utilization Ratio', color='#4ecdc4', fontsize=10, labelpad=8)
        ax.set_zlabel('Weight (kg)', color='#95e1d3', fontsize=10, labelpad=8)
        
        # Tick colors
        ax.tick_params(axis='x', colors='#ff6b6b', labelsize=8)
        ax.tick_params(axis='y', colors='#4ecdc4', labelsize=8)
        ax.tick_params(axis='z', colors='#95e1d3', labelsize=8)
        
        # Dark panes with subtle glow
        ax.xaxis.pane.fill = True
        ax.yaxis.pane.fill = True
        ax.zaxis.pane.fill = True
        ax.xaxis.pane.set_facecolor((0.05, 0.05, 0.1, 0.8))
        ax.yaxis.pane.set_facecolor((0.05, 0.05, 0.1, 0.8))
        ax.zaxis.pane.set_facecolor((0.05, 0.05, 0.1, 0.8))
        ax.xaxis.pane.set_edgecolor('#ff6b6b30')
        ax.yaxis.pane.set_edgecolor('#4ecdc430')
        ax.zaxis.pane.set_edgecolor('#95e1d330')
        
        # Grid with glow
        ax.grid(True, alpha=0.2, color='#00d4ff', linestyle='--', linewidth=0.5)
        
        # Initial view angle
        ax.view_init(elev=25, azim=self.camera_angle)
        
    def update_visualization(self, depths, urs, weights, iterations, 
                            best_history=None, animate_camera=False):
        """
        Update the unified 3D visualization with particle cloud and trails.
        """
        ax = self.ax
        ax.cla()
        self._setup_dark_theme()
        
        if len(depths) == 0:
            self.draw_idle()
            return
        
        # Normalize iterations for color mapping (0 to 1)
        max_iter = max(iterations) if len(iterations) > 0 else 1
        colors = iterations / max(max_iter, 1)
        
        # Create custom colormap: dark purple → cyan → white (manim style)
        custom_cmap = mcolors.LinearSegmentedColormap.from_list(
            'convergence', 
            ['#1a0033', '#6b2d5b', '#9b59b6', '#00d4ff', '#ffffff'],
            N=256
        )
        
        # Calculate particle sizes - newer particles are larger
        sizes = 10 + (colors ** 2) * 50  # Exponential growth
        
        # Main particle scatter with glow effect
        scatter = ax.scatter(
            depths, urs, weights,
            c=colors, cmap=custom_cmap,
            s=sizes, alpha=0.8,
            edgecolors='none',
            marker='o'
        )
        
        # Add glow layer (larger, more transparent particles behind)
        ax.scatter(
            depths, urs, weights,
            c=colors, cmap=custom_cmap,
            s=sizes * 2, alpha=0.2,
            edgecolors='none',
            marker='o'
        )
        
        # Draw best solution trail (convergence path)
        if best_history and len(best_history) > 1:
            best_depths = [p[0] for p in best_history]
            best_urs = [p[1] for p in best_history]
            best_weights = [p[2] for p in best_history]
            
            # Trail line with gradient
            ax.plot(best_depths, best_urs, best_weights, 
                   color='#00ff88', linewidth=2, alpha=0.8,
                   linestyle='-', marker='', label='Best Path')
            
            # Mark current best with star
            if len(best_depths) > 0:
                ax.scatter([best_depths[-1]], [best_urs[-1]], [best_weights[-1]],
                          color='#00ff88', s=200, marker='*', 
                          edgecolors='#ffffff', linewidths=2,
                          label='Optimal Solution', zorder=10)
        
        # Draw UR = 1.0 plane (feasibility boundary)
        if len(depths) > 0 and len(weights) > 0:
            d_range = [min(depths), max(depths)]
            w_range = [min(weights), max(weights)]
            D_plane, W_plane = np.meshgrid(
                np.linspace(d_range[0], d_range[1], 10),
                np.linspace(w_range[0], w_range[1], 10)
            )
            UR_plane = np.ones_like(D_plane)
            ax.plot_surface(D_plane, UR_plane, W_plane, 
                           alpha=0.1, color='#ff6b6b',
                           linewidth=0, antialiased=True)
        
        # Animate camera if enabled
        if animate_camera:
            self.camera_angle = (self.camera_angle + 0.5) % 360
            ax.view_init(elev=20 + 10 * np.sin(self.camera_angle * np.pi / 180), 
                        azim=self.camera_angle)
        
        # Set axis limits with padding
        if len(depths) > 0:
            ax.set_xlim([min(depths) * 0.95, max(depths) * 1.05])
        if len(urs) > 0:
            ax.set_ylim([0, max(1.5, max(urs) * 1.1)])
        if len(weights) > 0:
            ax.set_zlim([min(weights) * 0.95, max(weights) * 1.05])
        
        self.draw_idle()


# =============================================================================
# Control Panel
# =============================================================================

class ControlPanel(QFrame):
    """Futuristic control panel with neon styling."""
    
    toggle_clicked = Signal()
    replay_clicked = Signal()
    speed_changed = Signal(float)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            ControlPanel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0a0a0f, stop:0.5 #1a1a2e, stop:1 #0a0a0f);
                border-top: 1px solid #00d4ff40;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a2e, stop:1 #0d0d15);
                color: #00d4ff;
                border: 1px solid #00d4ff60;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
                font-family: 'Consolas', monospace;
            }
            QPushButton:hover {
                background: #00d4ff30;
                border-color: #00d4ff;
                color: #ffffff;
            }
            QPushButton:pressed {
                background: #00d4ff50;
            }
            QComboBox {
                background: #1a1a2e;
                color: #00d4ff;
                border: 1px solid #00d4ff60;
                border-radius: 6px;
                padding: 6px 12px;
                font-family: 'Consolas', monospace;
            }
            QLabel {
                color: #8b949e;
                font-size: 11px;
                font-family: 'Consolas', monospace;
            }
        """)
        
        self.setFixedHeight(55)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 8, 20, 8)
        layout.setSpacing(20)
        
        # Status
        self.status_label = QLabel("⚡ OPTIMIZING...")
        self.status_label.setStyleSheet("color: #00d4ff; font-weight: bold; font-size: 12px;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # Replay
        self.replay_btn = QPushButton("🔄 REPLAY")
        self.replay_btn.clicked.connect(self.replay_clicked.emit)
        self.replay_btn.setEnabled(False)
        layout.addWidget(self.replay_btn)
        
        # Speed
        speed_label = QLabel("SPEED:")
        layout.addWidget(speed_label)
        
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.5x", "1x", "2x", "4x"])
        self.speed_combo.setCurrentIndex(1)
        self.speed_combo.currentTextChanged.connect(
            lambda t: self.speed_changed.emit(float(t.replace('x', '')))
        )
        layout.addWidget(self.speed_combo)
        
        # Toggle
        self.toggle_btn = QPushButton("📊 VIEW CAD →")
        self.toggle_btn.clicked.connect(self.toggle_clicked.emit)
        layout.addWidget(self.toggle_btn)
        
    def set_complete(self):
        self.status_label.setText("✓ OPTIMIZATION COMPLETE")
        self.status_label.setStyleSheet("color: #00ff88; font-weight: bold; font-size: 12px;")
        self.replay_btn.setEnabled(True)
        
    def set_replaying(self, is_replaying: bool):
        if is_replaying:
            self.status_label.setText("🔄 REPLAYING...")
            self.status_label.setStyleSheet("color: #ffd93d; font-weight: bold;")
            self.replay_btn.setText("⏹ STOP")
        else:
            self.set_complete()
            self.replay_btn.setText("🔄 REPLAY")


# =============================================================================
# Stats HUD (Heads-Up Display)
# =============================================================================

class StatsHUD(QFrame):
    """Futuristic HUD overlay with live stats."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            StatsHUD {
                background: rgba(10, 10, 15, 0.9);
                border: 1px solid #00d4ff40;
                border-radius: 10px;
            }
            QLabel { 
                color: #c9d1d9; 
                font-size: 11px; 
                font-family: 'Consolas', monospace;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)
        
        title = QLabel("📡 LIVE STATS")
        title.setStyleSheet("color: #00d4ff; font-weight: bold; font-size: 12px;")
        layout.addWidget(title)
        
        self.iter_label = QLabel("ITER: 0 / 100")
        self.particles_label = QLabel("PARTICLES: 0")
        self.best_depth_label = QLabel("BEST D: -- mm")
        self.best_ur_label = QLabel("BEST UR: --")
        self.best_weight_label = QLabel("BEST W: -- kg")
        
        for lbl in [self.iter_label, self.particles_label, 
                   self.best_depth_label, self.best_ur_label, self.best_weight_label]:
            layout.addWidget(lbl)
        
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #00d4ff40;
                border-radius: 4px;
                background: #0a0a0f;
                height: 6px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:1 #00ff88);
                border-radius: 3px;
            }
        """)
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)
        
        self.setFixedWidth(170)
        
    def update_stats(self, iteration, max_iter, particles, best_d, best_ur, best_w):
        self.iter_label.setText(f"ITER: {iteration} / {max_iter}")
        self.particles_label.setText(f"PARTICLES: {particles}")
        self.best_depth_label.setText(f"BEST D: {best_d:.0f} mm" if best_d < float('inf') else "BEST D: --")
        self.best_ur_label.setText(f"BEST UR: {best_ur:.3f}" if best_ur < float('inf') else "BEST UR: --")
        self.best_weight_label.setText(f"BEST W: {best_w:.0f} kg" if best_w < float('inf') else "BEST W: --")
        self.progress.setValue(int((iteration / max(max_iter, 1)) * 100))


# =============================================================================
# Main Visualization Widget
# =============================================================================

class PSOVisualizerWidget(QWidget):
    """
    Premium futuristic 3D visualization widget.
    Single unified 3D space with Depth × UR × Weight.
    """
    
    switch_to_cad = Signal()
    
    def __init__(self, parent=None, max_iterations: int = 100):
        super().__init__(parent)
        self.max_iterations = max_iterations
        self.data_store = ParticleDataStore()
        self.is_replaying = False
        self.replay_index = 0
        self.replay_speed = 1.0
        
        self._setup_ui()
        self._setup_timers()
        
    def _setup_ui(self):
        self.setStyleSheet("background-color: #0a0a0f;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0a0a0f, stop:0.5 #1a1a2e, stop:1 #0a0a0f);
                border-bottom: 1px solid #00d4ff40;
            }
        """)
        header.setFixedHeight(45)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        title = QLabel("🚀 PLATE GIRDER PSO - UNIFIED 3D CONVERGENCE")
        title.setStyleSheet("""
            color: #00d4ff; 
            font-weight: bold; 
            font-size: 14px;
            font-family: 'Consolas', monospace;
        """)
        header_layout.addWidget(title)
        layout.addWidget(header)
        
        # Canvas
        self.canvas = Futuristic3DCanvas()
        layout.addWidget(self.canvas, stretch=1)
        
        # Control panel
        self.control_panel = ControlPanel()
        self.control_panel.toggle_clicked.connect(self._on_toggle)
        self.control_panel.replay_clicked.connect(self._on_replay)
        self.control_panel.speed_changed.connect(self._on_speed_change)
        layout.addWidget(self.control_panel)
        
        # HUD overlay
        self.hud = StatsHUD(self)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.hud.move(15, 55)
        
    def _setup_timers(self):
        # Live update timer with camera animation
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._flush_updates)
        self.update_timer.start(150)  # Smooth 150ms updates
        self.pending_updates = False
        
        # Replay timer
        self.replay_timer = QTimer()
        self.replay_timer.timeout.connect(self._replay_step)
        
    def add_particle_data(self, depth: float, ur: float, weight: float, 
                         iteration: int, particle_idx: int):
        self.data_store.add(depth, ur, weight, iteration, particle_idx)
        self.pending_updates = True
        
    def _flush_updates(self):
        if not self.pending_updates or self.is_replaying:
            return
            
        self.pending_updates = False
        ds = self.data_store
        depths, urs, weights, iters = ds.get_arrays()
        
        self.canvas.update_visualization(
            depths, urs, weights, iters,
            best_history=ds.best_history,
            animate_camera=True
        )
        
        self.hud.update_stats(
            ds.current_iteration, self.max_iterations,
            len(ds), ds.best_depth, ds.best_ur, ds.best_weight
        )
    
    def set_complete(self):
        self.control_panel.set_complete()
        
    def _on_toggle(self):
        self.switch_to_cad.emit()
        
    def _on_replay(self):
        if self.is_replaying:
            self.is_replaying = False
            self.replay_timer.stop()
            self.control_panel.set_replaying(False)
            # Show final state
            ds = self.data_store
            depths, urs, weights, iters = ds.get_arrays()
            self.canvas.update_visualization(depths, urs, weights, iters, ds.best_history, False)
        else:
            if len(self.data_store) == 0:
                return
            self.is_replaying = True
            self.replay_index = 0
            self.control_panel.set_replaying(True)
            self.replay_timer.start(int(80 / self.replay_speed))
            
    def _on_speed_change(self, speed: float):
        self.replay_speed = speed
        if self.replay_timer.isActive():
            self.replay_timer.setInterval(int(80 / speed))
            
    def _replay_step(self):
        total = len(self.data_store)
        step_size = max(1, total // 100)
        self.replay_index = min(self.replay_index + step_size, total)
        
        ds = self.data_store
        depths, urs, weights, iters = ds.get_arrays(self.replay_index)
        
        # Animate camera during replay
        self.canvas.update_visualization(depths, urs, weights, iters, 
                                        ds.best_history[:len([h for h in ds.best_history 
                                                             if len(depths) > 0 and h[0] <= max(depths)])],
                                        animate_camera=True)
        
        self.hud.update_stats(
            int(iters[-1]) if len(iters) > 0 else 0,
            self.max_iterations, len(iters),
            ds.best_depth, ds.best_ur, ds.best_weight
        )
        
        if self.replay_index >= total:
            self.is_replaying = False
            self.replay_timer.stop()
            self.control_panel.set_replaying(False)
        
    def clear(self):
        self.data_store.clear()
        self.is_replaying = False
        self.replay_timer.stop()
        
    def cleanup(self):
        if hasattr(self, 'update_timer'):
            self.update_timer.stop()
        if hasattr(self, 'replay_timer'):
            self.replay_timer.stop()
        try:
            import matplotlib.pyplot as plt
            plt.close(self.canvas.fig)
        except:
            pass


# Helper
def calculate_weight(area_cm2: float, length_mm: float) -> float:
    return (area_cm2 / 10000) * (length_mm / 1000) * 7850
