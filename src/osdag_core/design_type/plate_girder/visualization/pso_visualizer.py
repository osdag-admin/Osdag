"""
OpenGL 3D PSO Visualizer
========================
Beautiful 3D visualization of Particle Swarm Optimization using OpenGL.

Features:
- White background with clean aesthetics
- Threaded data processing for smooth performance  
- Dynamic axis scaling to prevent convergence crowding
- Replay functionality after optimization completes
- Glowing particles with gradient trails
- Mouse-controlled camera rotation
- Meaningful axis labels and tick marks
"""

from typing import List, Dict, Tuple, Optional
import numpy as np
import math
from collections import deque
from threading import Lock

from PySide6.QtCore import Qt, Signal, QTimer, QThread, QObject, QPoint
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QApplication, QFrame, QSlider,
    QSizePolicy
)
from PySide6.QtGui import QFont, QColor, QPainter, QPen, QBrush, QLinearGradient, QMouseEvent
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtOpenGL import QOpenGLFramebufferObject

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    OPENGL_AVAILABLE = True
except ImportError:
    OPENGL_AVAILABLE = False
    print("[WARNING] PyOpenGL not available, falling back to Qt painting")


# ============== COLORS (matching Osdag theme) ==============
WHITE_BG = (1.0, 1.0, 1.0, 1.0)
GRID_COLOR = (0.9, 0.9, 0.9, 1.0)
AXIS_COLOR = (0.3, 0.3, 0.3, 1.0)
LABEL_COLOR = (0.2, 0.2, 0.2, 1.0)
SAFE_COLOR = (0.29, 0.87, 0.50)      # Green #4ADE80
FAIL_COLOR = (0.97, 0.44, 0.44)      # Red #F87171
OPTIMAL_COLOR = (1.0, 0.84, 0.0)     # Gold
ACCENT_BLUE = (0.22, 0.74, 0.97)     # Sky Blue #38BDF8
OSDAG_GREEN = (0.18, 0.62, 0.31)     # Osdag theme green #2E9F4F


# Memory limit constants for 8GB RAM compatibility
MAX_HISTORY_ENTRIES = 10000  # ~1MB max for history buffer
MAX_PARTICLES = 100  # Max particles to track


class DataProcessor(QObject):
    """Threaded data processor for particle updates with memory limits."""
    data_ready = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.lock = Lock()
        self.history: List[Dict] = []
        self.current_frame = 0
        self.best_weight = float('inf')
        self.best_pos = None
        self.is_replaying = False
        self._disposed = False  # Track disposal state
        
        # Axis ranges (for dynamic scaling)
        self.depth_range = [float('inf'), float('-inf')]
        self.ur_range = [0.0, 2.0]
        self.weight_range = [float('inf'), float('-inf')]
        
        # Current visible particles
        self.particles: Dict[int, Dict] = {}
        
    def add_particle_data(self, depth: float, ur: float, weight: float, 
                          iteration: int, particle_idx: int):
        """Add new particle data (called from optimization thread)."""
        if self._disposed:
            return
            
        with self.lock:
            # Memory limit: cap history to prevent OOM on 8GB systems
            if len(self.history) < MAX_HISTORY_ENTRIES:
                self.history.append({
                    'depth': depth, 'ur': ur, 'weight': weight,
                    'iteration': iteration, 'particle_idx': particle_idx
                })
            
            # Update ranges for dynamic scaling
            self.depth_range[0] = min(self.depth_range[0], depth)
            self.depth_range[1] = max(self.depth_range[1], depth)
            self.weight_range[0] = min(self.weight_range[0], weight)
            self.weight_range[1] = max(self.weight_range[1], weight)
            self.ur_range[1] = max(self.ur_range[1], ur)
            
            # Update best
            if weight < self.best_weight and ur <= 1.0:
                self.best_weight = weight
                self.best_pos = (depth, ur, weight)
            
            # Update particle trails (keep last 15 points)
            if particle_idx not in self.particles:
                self.particles[particle_idx] = {'trail': deque(maxlen=15)}
            self.particles[particle_idx]['trail'].append((depth, ur, weight))
            self.particles[particle_idx]['current'] = (depth, ur, weight)
            self.particles[particle_idx]['iteration'] = iteration
            
    def get_render_data(self) -> dict:
        """Get current state for rendering."""
        with self.lock:
            # Add some padding to ranges
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
                'best_weight': self.best_weight,
                'iteration': max((p.get('iteration', 0) for p in self.particles.values()), default=0)
            }
    
    def get_history_frame(self, frame_idx: int) -> Optional[dict]:
        """Get data up to a specific frame for replay."""
        with self.lock:
            if frame_idx >= len(self.history):
                return None
            
            # Rebuild particles from history up to frame
            particles = {}
            best_w = float('inf')
            best_p = None
            
            for i in range(frame_idx + 1):
                h = self.history[i]
                pid = h['particle_idx']
                if pid not in particles:
                    particles[pid] = {'trail': deque(maxlen=15)}
                particles[pid]['trail'].append((h['depth'], h['ur'], h['weight']))
                particles[pid]['current'] = (h['depth'], h['ur'], h['weight'])
                particles[pid]['iteration'] = h['iteration']
                
                if h['weight'] < best_w and h['ur'] <= 1.0:
                    best_w = h['weight']
                    best_p = (h['depth'], h['ur'], h['weight'])
            
            return {
                'particles': particles,
                'depth_range': list(self.depth_range),
                'ur_range': list(self.ur_range),
                'weight_range': list(self.weight_range),
                'best_pos': best_p,
                'best_weight': best_w,
                'iteration': self.history[frame_idx]['iteration']
            }
    
    def get_history_length(self) -> int:
        with self.lock:
            return len(self.history)
    
    def clear(self):
        """Reset all data and mark as disposed."""
        self._disposed = True
        with self.lock:
            self.history.clear()
            self.history = []  # Release memory
            self.particles.clear()
            self.particles = {}  # Release memory
            self.best_weight = float('inf')
            self.best_pos = None
            self.depth_range = [float('inf'), float('-inf')]
            self.ur_range = [0.0, 2.0]
            self.weight_range = [float('inf'), float('-inf')]


class OpenGL3DCanvas(QOpenGLWidget):
    """OpenGL widget for 3D particle visualization with mouse rotation."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 300)
        
        # Camera (fixed initial view)
        self.camera_angle = 225.0  # Nice isometric view
        self.camera_elevation = 25.0
        self.camera_distance = 4.5
        
        # Mouse interaction
        self.last_mouse_pos = QPoint()
        self.is_dragging = False
        
        # Render data
        self.render_data = None
        self.lock = Lock()
        
        # Animation timer (for smooth rendering, not rotation)
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update)
        self.anim_timer.start(33)  # ~30 FPS
        
    def set_render_data(self, data: dict):
        """Thread-safe update of render data."""
        with self.lock:
            self.render_data = data
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for starting rotation."""
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.last_mouse_pos = event.position().toPoint()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release."""
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse drag for camera rotation."""
        if self.is_dragging:
            current_pos = event.position().toPoint()
            dx = current_pos.x() - self.last_mouse_pos.x()
            dy = current_pos.y() - self.last_mouse_pos.y()
            
            # Update camera angles
            self.camera_angle += dx * 0.5
            self.camera_elevation = max(-89, min(89, self.camera_elevation - dy * 0.3))
            
            self.last_mouse_pos = current_pos
            self.update()
    
    def wheelEvent(self, event):
        """Handle mouse wheel for zoom."""
        delta = event.angleDelta().y()
        self.camera_distance = max(2.0, min(10.0, self.camera_distance - delta * 0.002))
        self.update()
    
    def initializeGL(self):
        """Initialize OpenGL context."""
        if not OPENGL_AVAILABLE:
            return
            
        glClearColor(*WHITE_BG)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POINT_SMOOTH)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        
    def resizeGL(self, w, h):
        """Handle resize."""
        if not OPENGL_AVAILABLE:
            return
        glViewport(0, 0, w, h)
        
    def paintGL(self):
        """Render the 3D scene."""
        if not OPENGL_AVAILABLE:
            self._paint_fallback()
            return
            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Setup projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = self.width() / max(self.height(), 1)
        gluPerspective(45, aspect, 0.1, 100.0)
        
        # Setup camera
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Camera position from spherical coordinates
        rad_angle = math.radians(self.camera_angle)
        rad_elev = math.radians(self.camera_elevation)
        cam_x = self.camera_distance * math.cos(rad_elev) * math.sin(rad_angle)
        cam_y = self.camera_distance * math.sin(rad_elev)
        cam_z = self.camera_distance * math.cos(rad_elev) * math.cos(rad_angle)
        
        gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)
        
        with self.lock:
            data = self.render_data
        
        if data is None:
            self._draw_empty_axes()
            return
        
        # Get ranges for normalization
        d_range = data['depth_range']
        w_range = data['weight_range']
        ur_range = data['ur_range']
        
        # Calculate normalized ranges (map to -1 to 1)
        def normalize(v, r):
            if r[1] - r[0] < 0.001:
                return 0
            return 2.0 * (v - r[0]) / (r[1] - r[0]) - 1.0
        
        # Draw axes and grid with labels
        self._draw_axes_with_labels(d_range, w_range, ur_range)
        
        # Draw UR=1.0 reference plane
        self._draw_ur_plane(d_range, w_range, ur_range)
        
        # Draw particles
        particles = data['particles']
        best_pos = data['best_pos']
        best_w = data['best_weight']
        worst_w = w_range[1] if w_range[1] > w_range[0] else best_w * 2
        
        for pid, pdata in particles.items():
            trail = list(pdata['trail'])
            if not trail:
                continue
            
            current = pdata['current']
            cur_ur = current[1]
            cur_w = current[2]
            
            # Color based on UR and weight
            if cur_ur > 1.0:
                color = FAIL_COLOR
            else:
                # Gradient from green (low weight) to blue (high weight)
                t = (cur_w - best_w) / max(worst_w - best_w, 1) if worst_w > best_w else 0
                t = max(0, min(1, t))
                color = (
                    SAFE_COLOR[0] * (1-t) + ACCENT_BLUE[0] * t,
                    SAFE_COLOR[1] * (1-t) + ACCENT_BLUE[1] * t,
                    SAFE_COLOR[2] * (1-t) + ACCENT_BLUE[2] * t
                )
            
            # Draw trail with fading alpha
            if len(trail) > 1:
                glLineWidth(2.0)
                glBegin(GL_LINE_STRIP)
                for i, (d, u, w) in enumerate(trail):
                    alpha = 0.2 + 0.6 * (i / len(trail))
                    glColor4f(color[0], color[1], color[2], alpha)
                    nx = normalize(d, d_range)
                    ny = normalize(w, w_range)
                    nz = normalize(u, ur_range)
                    glVertex3f(nx, ny, nz)
                glEnd()
            
            # Draw current point
            d, u, w = current
            nx = normalize(d, d_range)
            ny = normalize(w, w_range)
            nz = normalize(u, ur_range)
            
            glPointSize(8.0)
            glBegin(GL_POINTS)
            glColor4f(color[0], color[1], color[2], 0.9)
            glVertex3f(nx, ny, nz)
            glEnd()
            
            # Glow effect
            glPointSize(14.0)
            glBegin(GL_POINTS)
            glColor4f(color[0], color[1], color[2], 0.3)
            glVertex3f(nx, ny, nz)
            glEnd()
        
        # Draw optimal point
        if best_pos:
            d, u, w = best_pos
            nx = normalize(d, d_range)
            ny = normalize(w, w_range)
            nz = normalize(u, ur_range)
            
            # Star marker
            glPointSize(20.0)
            glBegin(GL_POINTS)
            glColor4f(*OPTIMAL_COLOR, 1.0)
            glVertex3f(nx, ny, nz)
            glEnd()
            
            # Outer glow
            glPointSize(30.0)
            glBegin(GL_POINTS)
            glColor4f(*OPTIMAL_COLOR, 0.3)
            glVertex3f(nx, ny, nz)
            glEnd()
            
            # Drop line to floor
            glLineWidth(1.0)
            glBegin(GL_LINES)
            glColor4f(*OPTIMAL_COLOR, 0.5)
            glVertex3f(nx, ny, nz)
            glVertex3f(nx, -1.0, nz)
            glEnd()
    
    def _draw_empty_axes(self):
        """Draw axes when no data."""
        glColor4f(*AXIS_COLOR)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0, 1.0)
        glEnd()
    
    def _draw_axes_with_labels(self, d_range, w_range, ur_range):
        """Draw 3D axes with grid and tick marks."""
        # Main axis lines (thicker)
        glColor4f(*AXIS_COLOR)
        glLineWidth(2.5)
        glBegin(GL_LINES)
        # X axis (Depth)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(1.2, -1.0, -1.0)
        # Y axis (Weight)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, 1.2, -1.0)
        # Z axis (UR)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0, 1.2)
        glEnd()
        
        # Grid on floor (XZ plane at Y=-1)
        glColor4f(*GRID_COLOR)
        glLineWidth(1.0)
        glBegin(GL_LINES)
        for i in range(11):
            t = -1.0 + i * 0.2
            # Parallel to X
            glVertex3f(-1.0, -1.0, t)
            glVertex3f(1.0, -1.0, t)
            # Parallel to Z
            glVertex3f(t, -1.0, -1.0)
            glVertex3f(t, -1.0, 1.0)
        glEnd()
        
        # Grid on back wall (XY plane at Z=-1)
        glBegin(GL_LINES)
        for i in range(11):
            t = -1.0 + i * 0.2
            # Parallel to X
            glVertex3f(-1.0, t, -1.0)
            glVertex3f(1.0, t, -1.0)
            # Parallel to Y
            glVertex3f(t, -1.0, -1.0)
            glVertex3f(t, 1.0, -1.0)
        glEnd()
        
        # Tick marks on axes
        glColor4f(*AXIS_COLOR)
        glLineWidth(1.5)
        tick_size = 0.05
        
        # X-axis ticks (5 ticks)
        glBegin(GL_LINES)
        for i in range(6):
            t = -1.0 + i * 0.4
            glVertex3f(t, -1.0, -1.0)
            glVertex3f(t, -1.0 - tick_size, -1.0)
        glEnd()
        
        # Y-axis ticks
        glBegin(GL_LINES)
        for i in range(6):
            t = -1.0 + i * 0.4
            glVertex3f(-1.0, t, -1.0)
            glVertex3f(-1.0 - tick_size, t, -1.0)
        glEnd()
        
        # Z-axis ticks
        glBegin(GL_LINES)
        for i in range(6):
            t = -1.0 + i * 0.4
            glVertex3f(-1.0, -1.0, t)
            glVertex3f(-1.0, -1.0 - tick_size, t)
        glEnd()
    
    def _draw_ur_plane(self, d_range, w_range, ur_range):
        """Draw semi-transparent plane at UR=1.0."""
        # Normalize UR=1.0
        if ur_range[1] - ur_range[0] < 0.001:
            nz = 0
        else:
            nz = 2.0 * (1.0 - ur_range[0]) / (ur_range[1] - ur_range[0]) - 1.0
        
        if nz < -1.0 or nz > 1.0:
            return  # UR=1.0 is outside visible range
        
        # Draw transparent red plane
        glColor4f(*FAIL_COLOR, 0.12)
        glBegin(GL_QUADS)
        glVertex3f(-1.0, -1.0, nz)
        glVertex3f(1.0, -1.0, nz)
        glVertex3f(1.0, 1.0, nz)
        glVertex3f(-1.0, 1.0, nz)
        glEnd()
        
        # Plane border
        glColor4f(*FAIL_COLOR, 0.6)
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        glVertex3f(-1.0, -1.0, nz)
        glVertex3f(1.0, -1.0, nz)
        glVertex3f(1.0, 1.0, nz)
        glVertex3f(-1.0, 1.0, nz)
        glEnd()
    
    def _paint_fallback(self):
        """Fallback QPainter rendering if OpenGL unavailable."""
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255, 255, 255))
        painter.setPen(QColor(100, 100, 100))
        painter.drawText(self.rect(), Qt.AlignCenter, 
                        "OpenGL not available\nInstall PyOpenGL")
        painter.end()
    
    def cleanup(self):
        """Stop animation timer."""
        self.anim_timer.stop()


class PSOVisualizerWidget(QWidget):
    """Main PSO Visualizer Widget with OpenGL 3D rendering."""
    switch_to_cad = Signal()
    
    def __init__(self, parent=None, max_iterations=100):
        super().__init__(parent)
        self.max_iter = max_iterations
        self.is_complete = False
        self.is_replaying = False
        
        # Data processor (handles threading)
        self.data_processor = DataProcessor()
        
        # Batch buffer for performance
        self.batch_buffer = {'d':[], 'u':[], 'w':[], 'i':[], 'p':[]}
        
        # Replay timer
        self.replay_timer = QTimer(self)
        self.replay_timer.timeout.connect(self._replay_tick)
        self.replay_frame = 0
        self.replay_speed = 5  # frames per tick
        
        # Render timer (update GL from data)
        self.render_timer = QTimer(self)
        self.render_timer.timeout.connect(self._update_canvas)
        self.render_timer.start(50)  # 20 FPS for data updates
        
        self.setup_ui()
    
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
        
        # ===== HEADER (matching Osdag olive green theme) =====
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet("""
            QFrame {
                background-color: #6B7D20;
                border-bottom: 2px solid #556619;
            }
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
        
        # Close button (matching Osdag button style)
        close_btn = QPushButton("CLOSE")
        close_btn.clicked.connect(self.switch_to_cad.emit)
        close_btn.setStyleSheet("""
            QPushButton { 
                background-color: #282828; 
                color: #D0D0D0; 
                border: 1px solid #D0D0D0;
                border-radius: 5px; 
                padding: 6px 14px; 
                font-weight: bold; 
            }
            QPushButton:hover { 
                background-color: #90AF13; 
                border: 1px solid #90AF13;
                color: white;
            }
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
        
        # OpenGL Canvas
        self.canvas = OpenGL3DCanvas(self)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Side Panel (info and controls)
        side_panel = QFrame()
        side_panel.setFixedWidth(200)
        side_panel.setStyleSheet("""
            QFrame {
                background-color: #FAFAFA;
                border-left: 1px solid #E0E0E0;
            }
        """)
        side_layout = QVBoxLayout(side_panel)
        side_layout.setContentsMargins(12, 15, 12, 15)
        side_layout.setSpacing(12)
        
        # Axes info section
        axes_title = QLabel("AXES")
        axes_title.setStyleSheet("color: #666; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
        side_layout.addWidget(axes_title)
        
        axes_frame = QFrame()
        axes_frame.setStyleSheet("background: white; border: 1px solid #E0E0E0; border-radius: 4px; padding: 8px;")
        axes_inner = QVBoxLayout(axes_frame)
        axes_inner.setContentsMargins(8, 8, 8, 8)
        axes_inner.setSpacing(4)
        
        for axis_info in [("X", "Depth (mm)", "#E74C3C"), ("Y", "Weight (kg)", "#27AE60"), ("Z", "Utilization Ratio", "#3498DB")]:
            row = QHBoxLayout()
            axis_lbl = QLabel(axis_info[0])
            axis_lbl.setStyleSheet(f"color: {axis_info[2]}; font-weight: bold; font-size: 12px;")
            axis_lbl.setFixedWidth(20)
            desc_lbl = QLabel(axis_info[1])
            desc_lbl.setStyleSheet("color: #333; font-size: 11px;")
            row.addWidget(axis_lbl)
            row.addWidget(desc_lbl)
            row.addStretch()
            axes_inner.addLayout(row)
        
        side_layout.addWidget(axes_frame)
        
        # Legend section
        legend_title = QLabel("LEGEND")
        legend_title.setStyleSheet("color: #666; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
        side_layout.addWidget(legend_title)
        
        # Legend items
        def add_legend(color: str, label: str):
            item = QHBoxLayout()
            item.setSpacing(8)
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 14px;")
            dot.setFixedWidth(18)
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #333; font-size: 11px;")
            item.addWidget(dot)
            item.addWidget(lbl)
            item.addStretch()
            side_layout.addLayout(item)
        
        add_legend("#FFD700", "Optimal (Best)")
        add_legend("#4ADE80", "Feasible (UR ≤ 1)")
        add_legend("#F87171", "Infeasible (UR > 1)")
        
        side_layout.addSpacing(10)
        
        # Control hint
        hint_lbl = QLabel("🖱 Drag to rotate\n🖱 Scroll to zoom")
        hint_lbl.setStyleSheet("color: #888; font-size: 10px;")
        side_layout.addWidget(hint_lbl)
        
        side_layout.addStretch()
        
        # Replay controls (hidden until complete)
        self.replay_frame_widget = QFrame()
        self.replay_frame_widget.setVisible(False)
        replay_layout = QVBoxLayout(self.replay_frame_widget)
        replay_layout.setContentsMargins(0, 0, 0, 0)
        replay_layout.setSpacing(8)
        
        replay_title = QLabel("REPLAY")
        replay_title.setStyleSheet("color: #666; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
        replay_layout.addWidget(replay_title)
        
        self.replay_btn = QPushButton("▶ REPLAY")
        self.replay_btn.clicked.connect(self.start_replay)
        self.replay_btn.setStyleSheet("""
            QPushButton { 
                background-color: #6B7D20; 
                color: white; 
                border-radius: 5px; 
                padding: 8px; 
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover { background-color: #90AF13; }
        """)
        replay_layout.addWidget(self.replay_btn)
        
        # Speed slider
        speed_row = QHBoxLayout()
        speed_label = QLabel("Speed:")
        speed_label.setStyleSheet("color: #666; font-size: 10px;")
        speed_row.addWidget(speed_label)
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 20)
        self.speed_slider.setValue(5)
        self.speed_slider.valueChanged.connect(lambda v: setattr(self, 'replay_speed', v))
        self.speed_slider.setStyleSheet("""
            QSlider::groove:horizontal { height: 4px; background: #ddd; border-radius: 2px; }
            QSlider::handle:horizontal { width: 12px; height: 12px; background: #6B7D20; border-radius: 6px; margin: -4px 0; }
        """)
        speed_row.addWidget(self.speed_slider)
        replay_layout.addLayout(speed_row)
        
        side_layout.addWidget(self.replay_frame_widget)
        
        content.addWidget(self.canvas, 1)
        content.addWidget(side_panel)
        
        layout.addLayout(content)
    
    def add_particle_data(self, depth: float, ur: float, weight: float, 
                          iteration: int, particle_idx: int):
        """Add particle data (called from optimization)."""
        if self.is_complete and not self.is_replaying:
            return
        
        # Buffer for batch processing
        self.batch_buffer['d'].append(depth)
        self.batch_buffer['u'].append(ur)
        self.batch_buffer['w'].append(weight)
        self.batch_buffer['i'].append(iteration)
        self.batch_buffer['p'].append(particle_idx)
        
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
                self.batch_buffer['p'][i]
            )
        
        self.batch_buffer = {'d':[], 'u':[], 'w':[], 'i':[], 'p':[]}
    
    def _update_canvas(self):
        """Update canvas with latest data."""
        if self.is_replaying:
            return
        
        data = self.data_processor.get_render_data()
        self.canvas.set_render_data(data)
        
        # Update labels
        if data:
            self.lbl_iter.setText(f"ITERATION: {data['iteration']}")
            if data['best_weight'] != float('inf'):
                self.lbl_best.setText(f"BEST: {data['best_weight']:.0f} kg")
    
    def start_replay(self):
        """Start replaying the optimization."""
        if self.data_processor.get_history_length() == 0:
            return
        
        self.is_replaying = True
        self.replay_frame = 0
        self.replay_btn.setText("⏸ PAUSE")
        self.replay_btn.clicked.disconnect()
        self.replay_btn.clicked.connect(self.pause_replay)
        self.replay_timer.start(50)
    
    def pause_replay(self):
        """Pause replay."""
        self.replay_timer.stop()
        self.replay_btn.setText("▶ RESUME")
        self.replay_btn.clicked.disconnect()
        self.replay_btn.clicked.connect(self.start_replay)
    
    def _replay_tick(self):
        """Advance replay by one tick."""
        history_len = self.data_processor.get_history_length()
        
        self.replay_frame += self.replay_speed
        if self.replay_frame >= history_len:
            self.replay_frame = history_len - 1
            self.replay_timer.stop()
            self.is_replaying = False
            self.replay_btn.setText("▶ REPLAY")
            self.replay_btn.clicked.disconnect()
            self.replay_btn.clicked.connect(self.start_replay)
            # Show final state
            data = self.data_processor.get_render_data()
            self.canvas.set_render_data(data)
            return
        
        data = self.data_processor.get_history_frame(self.replay_frame)
        if data:
            self.canvas.set_render_data(data)
            self.lbl_iter.setText(f"ITERATION: {data['iteration']}")
            if data['best_weight'] != float('inf'):
                self.lbl_best.setText(f"BEST: {data['best_weight']:.0f} kg")
    
    def set_complete(self):
        """Mark optimization as complete."""
        self._flush_buffer()
        self.is_complete = True
        self.lbl_iter.setText("OPTIMIZATION COMPLETE")
        
        # Show replay controls
        self.replay_frame_widget.setVisible(True)
        
        # DO NOT auto-switch to CAD - let user stay on graph and switch manually
    
    def cleanup(self):
        """Clean up resources safely to prevent segfaults and memory leaks."""
        # Stop timers first to prevent any further callbacks
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
        
        # Clean up OpenGL canvas (must be done carefully)
        try:
            if hasattr(self, 'canvas') and self.canvas:
                self.canvas.cleanup()
        except Exception as e:
            print(f"[WARNING] Canvas cleanup error: {e}")
        
        # Clear data processor
        try:
            if hasattr(self, 'data_processor') and self.data_processor:
                self.data_processor.clear()
        except Exception as e:
            print(f"[WARNING] Data processor cleanup error: {e}")
        
        # Clear batch buffer
        try:
            if hasattr(self, 'batch_buffer'):
                self.batch_buffer = {'d':[], 'u':[], 'w':[], 'i':[], 'p':[]}
        except Exception:
            pass
        
        # Mark as complete to prevent further updates
        self.is_complete = True

