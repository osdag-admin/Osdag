import math
import numpy as np
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QPointF, Signal, QRectF
from PySide6.QtGui import QPainter, QColor, QPolygonF, QFont, QPen, QBrush, QTransform, QCursor

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: return v
    return v / norm

class NaviCubeOverlay(QWidget):
    """
    A premium, crash-free 3D ViewCube overlay using pure Qt 2D rendering.
    Generates a true 26-face chamfered cube using Painter's algorithm.
    """
    viewOrientationRequested = Signal(float, float, float, float, float, float)

    def __init__(self, cad_widget, parent=None):
        super().__init__(parent)
        self.cad_widget = cad_widget
        self.setFixedSize(140, 140)
        self.setMouseTracking(True)
        self.hovered_id = None
        
        # Dimensions for the chamfered cube
        self.r = 1.0   # Outer radius
        self.c = 0.70  # Inner flat face radius (controls chamfer size)
        
        self._build_geometry()

    def _build_geometry(self):
        r, c = self.r, self.c
        self.V = {
            'Z_TR_C': (c, c, r), 'Z_TL_C': (-c, c, r), 'Z_BL_C': (-c, -c, r), 'Z_BR_C': (c, -c, r),
            'Z_TR_B': (c, c, -r), 'Z_TL_B': (-c, c, -r), 'Z_BL_B': (-c, -c, -r), 'Z_BR_B': (c, -c, -r),
            
            'Y_TR_B': (c, r, c), 'Y_TL_B': (-c, r, c), 'Y_BL_B': (-c, r, -c), 'Y_BR_B': (c, r, -c),
            'Y_TR_F': (c, -r, c), 'Y_TL_F': (-c, -r, c), 'Y_BL_F': (-c, -r, -c), 'Y_BR_F': (c, -r, -c),
            
            'X_TR_R': (r, c, c), 'X_TL_R': (r, c, -c), 'X_BL_R': (r, -c, -c), 'X_BR_R': (r, -c, c),
            'X_TR_L': (-r, c, c), 'X_TL_L': (-r, c, -c), 'X_BL_L': (-r, -c, -c), 'X_BR_L': (-r, -c, c),
        }
        
        # Group vertices into faces and assign normals
        groups = {
            # 6 Main Faces
            'TOP': (['Z_BR_C', 'Z_TR_C', 'Z_TL_C', 'Z_BL_C'], (0,0,1)),
            'BOTTOM': (['Z_TR_B', 'Z_BR_B', 'Z_BL_B', 'Z_TL_B'], (0,0,-1)),
            'FRONT': (['Y_BR_F', 'Y_TR_F', 'Y_TL_F', 'Y_BL_F'], (0,-1,0)),
            'BACK': (['Y_TR_B', 'Y_BR_B', 'Y_BL_B', 'Y_TL_B'], (0,1,0)),
            'RIGHT': (['X_BR_R', 'X_TR_R', 'X_TL_R', 'X_BL_R'], (1,0,0)),
            'LEFT': (['X_BL_L', 'X_TL_L', 'X_TR_L', 'X_BR_L'], (-1,0,0)),
            
            # 12 Edge Faces
            'TOP_FRONT': (['Z_BR_C', 'Z_BL_C', 'Y_TL_F', 'Y_TR_F'], (0,-1,1)),
            'TOP_BACK': (['Z_TL_C', 'Z_TR_C', 'Y_TR_B', 'Y_TL_B'], (0,1,1)),
            'TOP_RIGHT': (['Z_TR_C', 'Z_BR_C', 'X_BR_R', 'X_TR_R'], (1,0,1)),
            'TOP_LEFT': (['Z_BL_C', 'Z_TL_C', 'X_TR_L', 'X_BR_L'], (-1,0,1)),
            
            'BOTTOM_FRONT': (['Z_BL_B', 'Z_BR_B', 'Y_BR_F', 'Y_BL_F'], (0,-1,-1)),
            'BOTTOM_BACK': (['Z_TR_B', 'Z_TL_B', 'Y_TL_B', 'Y_BR_B'], (0,1,-1)),
            'BOTTOM_RIGHT': (['Z_BR_B', 'Z_TR_B', 'X_TL_R', 'X_BL_R'], (1,0,-1)),
            'BOTTOM_LEFT': (['Z_TL_B', 'Z_BL_B', 'X_BL_L', 'X_TL_L'], (-1,0,-1)),
            
            'FRONT_RIGHT': (['Y_TR_F', 'Y_BR_F', 'X_BL_R', 'X_BR_R'], (1,-1,0)),
            'FRONT_LEFT': (['Y_BL_F', 'Y_TL_F', 'X_BR_L', 'X_BL_L'], (-1,-1,0)),
            'BACK_RIGHT': (['Y_BR_B', 'Y_TR_B', 'X_TR_R', 'X_TL_R'], (1,1,0)),
            'BACK_LEFT': (['Y_TL_B', 'Y_BL_B', 'X_TL_L', 'X_TR_L'], (-1,1,0)),
            
            # 8 Corner Faces
            'TOP_FRONT_RIGHT': (['Z_BR_C', 'Y_TR_F', 'X_BR_R'], (1,-1,1)),
            'TOP_FRONT_LEFT': (['Z_BL_C', 'X_BR_L', 'Y_TL_F'], (-1,-1,1)),
            'TOP_BACK_RIGHT': (['Z_TR_C', 'X_TR_R', 'Y_TR_B'], (1,1,1)),
            'TOP_BACK_LEFT': (['Z_TL_C', 'Y_TL_B', 'X_TR_L'], (-1,1,1)),
            
            'BOTTOM_FRONT_RIGHT': (['Z_BR_B', 'X_BL_R', 'Y_BR_F'], (1,-1,-1)),
            'BOTTOM_FRONT_LEFT': (['Z_BL_B', 'Y_BL_F', 'X_BL_L'], (-1,-1,-1)),
            'BOTTOM_BACK_RIGHT': (['Z_TR_B', 'Y_BR_B', 'X_TL_R'], (1,1,-1)),
            'BOTTOM_BACK_LEFT': (['Z_TL_B', 'X_TL_L', 'Y_BL_B'], (-1,1,-1)),
        }
        
        self.faces = {}
        for name, (v_keys, normal) in groups.items():
            pts = [np.array(self.V[k]) for k in v_keys]
            n = normalize(np.array(normal))
            
            # Auto-sort vertices counter-clockwise around the normal
            center = np.mean(pts, axis=0)
            u = pts[0] - center
            u = normalize(u)
            v = np.cross(n, u)
            
            def angle(p):
                d = p - center
                return math.atan2(np.dot(d, v), np.dot(d, u))
                
            sorted_pts = sorted(pts, key=angle)
            
            self.faces[name] = {
                'pts': sorted_pts,
                'normal': n,
                'center': center,
                'text': name if name in ['TOP', 'BOTTOM', 'FRONT', 'BACK', 'RIGHT', 'LEFT'] else None,
                'type': 'face' if len(v_keys) == 4 and np.abs(n).sum() == 1 else ('edge' if len(v_keys)==4 else 'corner')
            }
            
            # Text alignment helpers for main faces
            if self.faces[name]['text']:
                if name == 'TOP': self.faces[name]['up'] = np.array([0, 1, 0])
                elif name == 'BOTTOM': self.faces[name]['up'] = np.array([0, 1, 0])
                else: self.faces[name]['up'] = np.array([0, 0, 1])

    def _get_camera_matrix(self):
        # Default iso view
        D = normalize(np.array([1, -1, -1]))
        U = normalize(np.array([0, 0, 1]))
        R = np.cross(D, U)
        
        if not self.cad_widget or not hasattr(self.cad_widget, 'view') or not self.cad_widget.view:
            return D, U, R
            
        try:
            cam = self.cad_widget.view.Camera()
            cdir = cam.Direction()
            cup = cam.Up()
            
            D = normalize(np.array([cdir.X(), cdir.Y(), cdir.Z()]))
            U = normalize(np.array([cup.X(), cup.Y(), cup.Z()]))
            R = normalize(np.cross(D, U))
        except:
            pass
            
        return D, U, R

    def _project(self, P, R, U, scale, cx, cy):
        # Project 3D point onto 2D screen using camera Right and Up vectors
        x = np.dot(P, R) * scale
        y = -np.dot(P, U) * scale
        return QPointF(cx + x, cy + y)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Match Osdag theme
        is_light = True
        try:
            is_light = QApplication.instance().theme_manager.is_light()
        except: pass

        c_bg = QColor(240, 240, 240, 120) if is_light else QColor(40, 40, 40, 120)
        c_face_base = QColor(245, 245, 245, 255) if is_light else QColor(90, 90, 90, 255)
        c_text = QColor(70, 70, 70) if is_light else QColor(220, 220, 220)
        c_border = QColor(130, 130, 130) if is_light else QColor(50, 50, 50)
        c_hover = QColor(0, 160, 255, 180)
        
        cx, cy = self.width() / 2, self.height() / 2
        S = 32.0 # Master Scale
        
        # 1. Compass background ring
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(c_bg))
        painter.drawEllipse(QPointF(cx, cy), S*2.4, S*2.4)
        
        D, U, R = self._get_camera_matrix()
        
        # 2. Collect visible faces and calculate their depth
        visible_faces = []
        for name, f in self.faces.items():
            # A face is visible if its normal is pointing towards the camera (dot < 0)
            # We use 0.2 to allow seeing edges just on the horizon
            if np.dot(f['normal'], D) < 0.2:
                depth = np.dot(f['center'], D)
                visible_faces.append((depth, name, f))
                
        # 3. Sort by depth for Painter's Algorithm (Draw deepest faces first)
        visible_faces.sort(key=lambda x: x[0], reverse=True)
        
        font = QFont("Segoe UI", 9, QFont.Bold)
        
        # 4. Render Faces
        for depth, name, f in visible_faces:
            pts_2d = [self._project(p, R, U, S, cx, cy) for p in f['pts']]
            poly = QPolygonF(pts_2d)
            
            # Dynamic Shading (Light from Top-Left-Front)
            light = normalize(np.array([-1, -1, -1]))
            shade = np.dot(f['normal'], light) * 0.15 + 0.85
            
            r, g, b = c_face_base.red() * shade, c_face_base.green() * shade, c_face_base.blue() * shade
            r = min(255, max(0, int(r)))
            g = min(255, max(0, int(g)))
            b = min(255, max(0, int(b)))
            
            face_color = QColor(r, g, b)
            
            # Highlight hovered region
            if self.hovered_id == name:
                painter.setBrush(QBrush(c_hover))
            else:
                painter.setBrush(QBrush(face_color))
                
            # Make edges/corners slightly darker for depth contrast
            if f['type'] != 'face' and self.hovered_id != name:
                painter.setBrush(QBrush(face_color.darker(108)))
                
            painter.setPen(QPen(c_border, 1.2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawPolygon(poly)
            
            # Render 3D Perspective Text
            if f['text']:
                N = f['normal']
                up_vec = f['up']
                right_vec = np.cross(up_vec, N)
                
                # Compute 4 corners of text plane in 3D
                tc = f['center']
                tw = self.c * 0.75 # Text area size
                p_tl = tc - right_vec * tw + up_vec * tw
                p_tr = tc + right_vec * tw + up_vec * tw
                p_br = tc + right_vec * tw - up_vec * tw
                p_bl = tc - right_vec * tw - up_vec * tw
                
                quad_3d = [p_tl, p_tr, p_br, p_bl]
                quad_2d = [self._project(p, R, U, S, cx, cy) for p in quad_3d]
                
                dst = QPolygonF(quad_2d)
                src = QPolygonF([QPointF(0,0), QPointF(100,0), QPointF(100,100), QPointF(0,100)])
                
                transform = QTransform()
                # quadToQuad creates a perfect perspective projection matrix
                if QTransform.quadToQuad(src, dst, transform):
                    painter.save()
                    painter.setTransform(transform)
                    painter.setFont(font)
                    painter.setPen(QPen(c_text))
                    painter.drawText(QRectF(0, 0, 100, 100), Qt.AlignCenter, f['text'])
                    painter.restore()

    def mouseMoveEvent(self, event):
        pos = event.position()
        D, U, R = self._get_camera_matrix()
        cx, cy = self.width() / 2, self.height() / 2
        S = 32.0
        
        visible_faces = []
        for name, f in self.faces.items():
            if np.dot(f['normal'], D) < 0.2:
                depth = np.dot(f['center'], D)
                visible_faces.append((depth, name, f))
                
        # Sort shallowest first (Front-to-Back for accurate hit testing)
        visible_faces.sort(key=lambda x: x[0])
        
        new_hover = None
        for depth, name, f in visible_faces:
            pts_2d = [self._project(p, R, U, S, cx, cy) for p in f['pts']]
            poly = QPolygonF(pts_2d)
            if poly.containsPoint(pos, Qt.OddEvenFill):
                new_hover = name
                break
                
        if new_hover != self.hovered_id:
            self.hovered_id = new_hover
            self.update()
            
        if self.hovered_id:
            self.setCursor(QCursor(Qt.PointingHandCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

    def mousePressEvent(self, event):
        if self.hovered_id and event.button() == Qt.LeftButton:
            f = self.faces[self.hovered_id]
            proj = f['normal']
            
            # Determine Up vector for the camera
            up = np.array([0, 0, 1]) # Default Z is up
            if abs(proj[2]) > 0.99:  # If looking directly from Top or Bottom
                up = np.array([0, 1, 0]) # Y becomes up
                
            self.viewOrientationRequested.emit(proj[0], proj[1], proj[2], up[0], up[1], up[2])
            event.accept()
        else:
            super().mousePressEvent(event)

    def leaveEvent(self, event):
        self.hovered_id = None
        self.update()
        super().leaveEvent(event)
