"""
SELF-EXPLANATORY SCIENTIFIC VISUALIZATION
Features:
- "Reference Plane" at UR=1.0 (Separates Safe vs Unsafe)
- Explicit Text Annotations within 3D Space
- Readable Axis Ticks & Labels
- Heatmap Coloring with Legend
"""

from typing import List, Dict
import numpy as np
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QApplication, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QFont, QColor

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# THEME PALETTE
BG_COLOR = "#0F172A"   # Slate 900
ACCENT_COLOR = "#38BDF8"  # Sky Blue
GRID_COLOR = "#334155"    # Slate 700
SAFE_COLOR = "#4ade80"    # Green
FAIL_COLOR = "#f87171"    # Red

class ParticleDataStore:
    def __init__(self, max_points: int = 2000):
        self.trails: Dict[int, dict] = {}
        self.best_particle_id = -1
        self.best_weight = float('inf')
        self.worst_weight = 0.0
        self.best_pos = None # (depth, ur, weight)

    def add_batch(self, depths, urs, weights, iterations, particle_ids):
        # Update range for normalization
        if weights:
            self.worst_weight = max(self.worst_weight, max(weights))
        
        for i in range(len(depths)):
            pid = particle_ids[i]
            w = weights[i]
            
            if pid not in self.trails:
                self.trails[pid] = {'x': [], 'y': [], 'z': []}
            
            self.trails[pid]['x'].append(depths[i])
            self.trails[pid]['y'].append(urs[i])
            self.trails[pid]['z'].append(w)
            
            if len(self.trails[pid]['x']) > 20: 
                self.trails[pid]['x'].pop(0)
                self.trails[pid]['y'].pop(0)
                self.trails[pid]['z'].pop(0)
                
            if w < self.best_weight and urs[i] <= 1.0:
                self.best_weight = w
                self.best_particle_id = pid
                self.best_pos = (depths[i], urs[i], w)

    def clear(self):
        self.trails.clear()
        self.best_particle_id = -1
        self.best_weight = float('inf')
        self.best_pos = None


class ExplanatoryCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(10, 8), dpi=100, facecolor=BG_COLOR)
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111, projection='3d', facecolor=BG_COLOR)
        self.fig.subplots_adjust(left=0.0, right=0.95, top=0.95, bottom=0.05)
        
        self.camera_angle = 35
        self.elevation = 25
        self.cmap = cm.get_cmap('viridis_r') 
        self._setup_theme()
        
    def _setup_theme(self):
        ax = self.ax
        ax.set_facecolor(BG_COLOR)
        
        # Transparent Panes
        ax.xaxis.set_pane_color((0, 0, 0, 0))
        ax.yaxis.set_pane_color((0, 0, 0, 0))
        ax.zaxis.set_pane_color((0, 0, 0, 0))
        
        # Grid
        grid_style = {"color": GRID_COLOR, "linewidth": 0.5, "linestyle": "--"}
        ax.xaxis._axinfo["grid"].update(grid_style)
        ax.yaxis._axinfo["grid"].update(grid_style)
        ax.zaxis._axinfo["grid"].update(grid_style)
        
        # Spines (Colored)
        ax.xaxis.line.set_color(GRID_COLOR)
        ax.yaxis.line.set_color(GRID_COLOR)
        ax.zaxis.line.set_color(GRID_COLOR)
        
        # Labels
        lbl_style = {'fontsize': 9, 'color': '#94a3b8', 'fontweight': 'bold'}
        ax.set_xlabel('Depth (mm)', fontdict=lbl_style, labelpad=5)
        ax.set_ylabel('Utilization Ratio', fontdict=lbl_style, labelpad=5)
        ax.set_zlabel('Weight (kg)', fontdict=lbl_style, labelpad=5)
        
        # Ticks (Visible Numbers!)
        ax.tick_params(axis='x', colors='#64748b', labelsize=8)
        ax.tick_params(axis='y', colors='#64748b', labelsize=8)
        ax.tick_params(axis='z', colors='#64748b', labelsize=8)

        ax.view_init(elev=self.elevation, azim=self.camera_angle)

    def update_plot(self, trails, best_pos, best_w, worst_w):
        ax = self.ax
        ax.clear()
        self._setup_theme()
        
        norm = mcolors.Normalize(vmin=best_w*0.9, vmax=max(worst_w, best_w*1.5))

        # 1. DRAW REFERENCE PLANE "THE LIMIT" (UR = 1.0)
        # We draw a semi-transparent plane at Y=1.0 to show the failure boundary
        x_lim = ax.get_xlim()
        z_lim = ax.get_zlim()
        if x_lim[1] > 10: # Only draw if we have data scaling
            y_ref = np.array([1.0, 1.0])
            x_ref, z_ref = np.meshgrid(np.linspace(x_lim[0], x_lim[1], 2), np.linspace(z_lim[0], z_lim[1], 2))
            
            # Draw Plane
            ax.plot_surface(x_ref, np.ones_like(x_ref), z_ref, alpha=0.1, color=FAIL_COLOR)
            
            # Plane Edge Line
            ax.plot([x_lim[0], x_lim[1]], [1.0, 1.0], [z_lim[0], z_lim[0]], color=FAIL_COLOR, linewidth=1.5, linestyle='--')
            
            # Text Annotation for Plane
            ax.text(x_lim[0], 1.05, z_lim[0], "FAILURE LIMIT (UR=1.0)", color=FAIL_COLOR, fontsize=8)


        # 2. DRAW PARTICLES
        for pid, data in trails.items():
            if not data['x']: continue
            x, y, z = data['x'], data['y'], data['z']
            
            color = self.cmap(norm(z[-1]))
            # If failed (UR > 1), tint 'Red'
            if y[-1] > 1.0: 
                color = FAIL_COLOR
            
            if len(x) > 1:
                ax.plot(x, y, z, color=color, alpha=0.5, linewidth=1.0)
            ax.scatter([x[-1]], [y[-1]], [z[-1]], color=color, s=20, alpha=0.9)

        # 3. HIGHLIGHT OPTIMAL
        if best_pos:
            bx, by, bz = best_pos
            ax.scatter([bx], [by], [bz], color='#ffffff', s=160, marker='*', edgecolors='gold', linewidth=1.5)
            # Label the Optimal Point clearly
            ax.text(bx, by, bz, f" OPTIMAL\n {bz:.0f} kg", color='white', fontsize=8)
            
            # Draw line to axes to show coordinates
            # To Depth Axis
            ax.plot([bx, bx], [by, ax.get_ylim()[0]], [bz, bz], color='gray', linestyle=':', alpha=0.5)
            # To Weight Axis
            ax.plot([bx, bx], [by, by], [bz, ax.get_zlim()[0]], color='gold', linestyle='--', alpha=0.8)

        self.camera_angle += 0.2
        ax.view_init(elev=self.elevation, azim=self.camera_angle)
        self.draw()


class PSOVisualizerWidget(QWidget):
    switch_to_cad = Signal() 

    def __init__(self, parent=None, max_iterations=100):
        super().__init__(parent)
        self.data_store = ParticleDataStore()
        self.max_iter = max_iterations
        self.is_complete = False
        self.batch_buffer = {'d':[], 'u':[], 'w':[], 'i':[], 'p':[]}
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet(f"background-color: {BG_COLOR}; font-family: 'Segoe UI', sans-serif;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # --- HEADER ---
        header = QHBoxLayout()
        header.setContentsMargins(15, 10, 15, 0)
        
        title_box = QVBoxLayout()
        title = QLabel("DESIGN OPTIMIZATION SPACE")
        title.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        sub_title = QLabel("Seeking minimum weight (Vertical Axis) within safe limits (UR < 1.0)")
        sub_title.setStyleSheet("color: #94a3b8; font-size: 10px;")
        title_box.addWidget(title)
        title_box.addWidget(sub_title)
        
        close_btn = QPushButton("CLOSE DASHBOARD")
        close_btn.clicked.connect(self.switch_to_cad.emit)
        close_btn.setStyleSheet("""
            QPushButton { background-color: #334155; color: white; border-radius: 4px; padding: 6px 12px; font-weight: bold; }
            QPushButton:hover { background-color: #475569; }
        """)
        
        header.addLayout(title_box)
        header.addStretch()
        header.addWidget(close_btn)
        layout.addLayout(header)

        # --- BODY ---
        body = QHBoxLayout()
        
        self.canvas = ExplanatoryCanvas(self)
        
        # Legend Panel
        legend = QFrame()
        legend.setFixedWidth(200)
        legend.setStyleSheet("background-color: rgba(30, 41, 59, 0.5); border-left: 1px solid #334155;")
        l_layout = QVBoxLayout(legend)
        l_layout.setContentsMargins(20, 20, 20, 20)
        
        def add_leg_item(color, text, details=""):
            w = QWidget()
            h = QHBoxLayout(w)
            h.setContentsMargins(0,0,0,0)
            dot = QLabel("⬤")
            dot.setStyleSheet(f"color: {color}; font-size: 16px;")
            v = QVBoxLayout()
            t = QLabel(text)
            t.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
            d = QLabel(details)
            d.setStyleSheet("color: #94a3b8; font-size: 10px;")
            v.addWidget(t)
            v.addWidget(d)
            h.addWidget(dot)
            h.addLayout(v)
            l_layout.addWidget(w)
            l_layout.addSpacing(10)

        add_leg_item("#FDE047", "OPTIMAL", "Lowest Weight, Safe")
        add_leg_item("#4ADE80", "SAFE DESIGN", "Heavier, but passes checks")
        add_leg_item("#F87171", "UNSAFE / FAILED", "Utilization Ratio > 1.0")
        
        l_layout.addStretch()
        
        # Live Stats
        self.lbl_iter = QLabel("GENERATION: 0")
        self.lbl_iter.setStyleSheet("color: #38BDF8; font-weight: bold;")
        self.lbl_best = QLabel("BEST: --- kg")
        self.lbl_best.setStyleSheet("color: white; font-size: 18px; font-weight: 900;")
        
        l_layout.addWidget(self.lbl_iter)
        l_layout.addWidget(self.lbl_best)
        l_layout.addSpacing(20)
        
        body.addWidget(self.canvas, 1)
        body.addWidget(legend)
        
        layout.addLayout(body)

    def add_particle_data(self, depth, ur, weight, iteration, particle_idx):
        if self.is_complete: return
        self.batch_buffer['d'].append(depth)
        self.batch_buffer['u'].append(ur)
        self.batch_buffer['w'].append(weight)
        self.batch_buffer['i'].append(iteration)
        self.batch_buffer['p'].append(particle_idx)
        
        if len(self.batch_buffer['d']) >= 30:
            self._flush_buffer()

    def _flush_buffer(self):
        if not self.batch_buffer['d']: return
        self.data_store.add_batch(
            self.batch_buffer['d'], self.batch_buffer['u'], 
            self.batch_buffer['w'], self.batch_buffer['i'], 
            self.batch_buffer['p']
        )
        it = self.batch_buffer['i'][-1]
        self.batch_buffer = {'d':[], 'u':[], 'w':[], 'i':[], 'p':[]}
        
        QApplication.processEvents()
        self.canvas.update_plot(self.data_store.trails, self.data_store.best_pos, self.data_store.best_weight, self.data_store.worst_weight)
        
        self.lbl_iter.setText(f"GENERATION: {it}")
        if self.data_store.best_weight != float('inf'):
            self.lbl_best.setText(f"BEST: {self.data_store.best_weight:.0f} kg")

    def set_complete(self):
        self._flush_buffer()
        self.is_complete = True
        self.lbl_iter.setText("OPTIMIZATION COMPLETE")
        QTimer.singleShot(2000, self.switch_to_cad.emit)
        
    def cleanup(self):
        self.data_store.clear()
        try: self.canvas.fig.clf()
        except: pass
