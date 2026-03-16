"""
View Cube Overlay Widget - PySide6-based navigation cube overlay.
Renders the view cube as a 2D overlay that interacts with the 3D viewer.
"""
from typing import Dict, Optional, Tuple
from enum import Enum

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QBrush,
    QPainterPath
)
from PySide6.QtWidgets import QWidget

from osdag_gui.ui.components.view_cube import ChamferedViewCube

class ViewCubeWidget(QWidget):
    """
    A PySide6 widget that renders an interactive view cube overlay.
    
    Features:
    - Chamfered (beveled) cube rendering
    - Hover highlights
    - Click to set view
    - Drag to rotate cube
    - Smooth animations
    """
    
    # Signal emitted when a view is selected
    view_changed = Signal(str)
    
    class State(Enum):
        IDLE = "idle"
        HOVERING = "hovering"
        DRAGGING = "dragging"
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        cube_size: int = 120,
        position: str = "top_right",
        margin: int = 60
    ):
        super().__init__(parent)
        
        self.cube_size = cube_size
        self.position = position
        self.margin = margin
        
        # State
        self._state = self.State.IDLE
        self._hovered_region: Optional[str] = None
        self._is_dragging = False
        self._drag_start_pos = QPoint()
        self._current_rotation = 0.0  # Yaw
        self._current_pitch = 0.0    # Pitch
        
        # Cube data
        self._view_cube = ChamferedViewCube(size=cube_size * 0.4)
        self._region_map: Dict[str, QPainterPath] = {}
        
        # Colors
        self._face_color = QColor(240, 240, 240)
        self._edge_color = QColor(100, 100, 100)
        self._highlight_color = QColor(0, 200, 255, 180)
        self._text_color = QColor(50, 50, 50)
        
        # Labels for faces
        self._face_labels = {
            "front": "F",
            "back": "K", 
            "top": "T",
            "bottom": "Bo",
            "right": "R",
            "left": "L"
        }
        
        self._corner_labels = {
            "front_top_right": "FTR",
            "front_top_left": "FTL",
            "front_bottom_right": "FBR",
            "front_bottom_left": "FBL",
            "back_top_right": "BTR",
            "back_top_left": "BTL", 
            "back_bottom_right": "BBR",
            "back_bottom_left": "BBL"
        }
        
        self._edge_labels = {
            "front_top": "FT",
            "front_bottom": "FB",
            "front_right": "FR",
            "front_left": "FL",
            "back_top": "BT",
            "back_bottom": "BB",
            "back_right": "BR",
            "back_left": "BL",
            "top_right": "TR",
            "top_left": "TL",
            "bottom_right": "BR",
            "bottom_left": "BL"
        }
        
        self._setup_widget()
    
    def _setup_widget(self) -> None:
        """Setup widget properties."""
        # Make widget transparent and always on top
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(
            Qt.Window |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        
        # Set initial size
        self.setFixedSize(self.cube_size + 40, self.cube_size + 40)
        
        # Position the widget
        self._position_widget()
    
    def _position_widget(self) -> None:
        """Position the widget in the specified corner."""
        if not self.parentWidget():
            return
        
        parent_size = self.parentWidget().size()
        
        if self.position == "top_right":
            x = parent_size.width() - self.width() - self.margin
            y = self.margin
        elif self.position == "top_left":
            x = self.margin
            y = self.margin
        elif self.position == "bottom_right":
            x = parent_size.width() - self.width() - self.margin
            y = parent_size.height() - self.height() - self.margin
        elif self.position == "bottom_left":
            x = self.margin
            y = parent_size.height() - self.height() - self.margin
        else:  # default top_right
            x = parent_size.width() - self.width() - self.margin
            y = self.margin
        
        self.move(x, y)
    
    def showEvent(self, event) -> None:
        """Reposition on show."""
        super().showEvent(event)
        self._position_widget()
    
    def resizeEvent(self, event) -> None:
        """Handle parent resize."""
        super().resizeEvent(event)
        self._position_widget()
    
    def paintEvent(self, event) -> None:
        """Paint the view cube."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        
        # Calculate cube center
        center_x = self.width() // 2
        center_y = self.height() // 2
        half = self.cube_size // 2
        
        # Apply rotation transformation
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self._current_rotation)
        painter.rotate(self._current_pitch)
        painter.translate(-center_x, -center_y)
        
        # Draw the chamfered cube (simplified 2D projection)
        self._draw_cube(painter, center_x, center_y, half)
        
        painter.restore()
        
        # Draw view labels
        self._draw_labels(painter, center_x, center_y, half)
    
    def _draw_cube(
        self, 
        painter: QPainter, 
        cx: int, 
        cy: int, 
        half: int
    ) -> None:
        """
        Draw a 2D projection of a chamfered cube.
        Uses a pseudo-3D isometric-like projection.
        """
        # Chamfer size
        chamfer = half // 4
        
        # Define cube vertices (front face)
        # With chamfer, we have additional vertices
        fc = chamfer  # front-chamfer offset
        
        # Face vertices (simplified: draw as 2D projected cube)
        # Front face (square)
        front_points = [
            (cx - half + fc, cy - half + fc),  # top-left
            (cx + half - fc, cy - half + fc),  # top-right
            (cx + half - fc, cy + half - fc),  # bottom-right
            (cx - half + fc, cy + half - fc),  # bottom-left
        ]
        
        # Back face offset
        offset = half // 3
        back_points = [
            (cx - half + fc + offset, cy - half + fc - offset),
            (cx + half - fc + offset, cy - half + fc - offset),
            (cx + half - fc + offset, cy + half - fc - offset),
            (cx - half + fc + offset, cy + half - fc - offset),
        ]
        
        # Colors
        face_brush = QBrush(self._face_color)
        edge_pen = QPen(self._edge_color, 2)
        highlight_brush = QBrush(self._highlight_color)
        
        # Determine which faces to highlight based on rotation
        highlight_front = abs(self._current_pitch) < 30 and abs(self._current_rotation % 360) < 30
        highlight_back = abs(self._current_pitch) < 30 and abs((self._current_rotation % 360) - 180) < 30
        highlight_top = abs(self._current_pitch) > 60
        highlight_right = 30 <= (self._current_rotation % 360) < 150
        highlight_left = 150 <= (self._current_rotation % 360) < 330
        
        # Draw back face
        if not highlight_back:
            painter.setBrush(face_brush)
        else:
            painter.setBrush(highlight_brush)
        painter.setPen(edge_pen)
        self._draw_quad(painter, back_points)
        
        # Draw connecting edges (sides)
        side_points = [
            [back_points[0], front_points[0]],
            [back_points[1], front_points[1]],
            [back_points[2], front_points[2]],
            [back_points[3], front_points[3]],
        ]
        
        for pts in side_points:
            painter.drawLine(pts[0], pts[1])
        
        # Draw front face
        if not highlight_front:
            painter.setBrush(face_brush)
        else:
            painter.setBrush(highlight_brush)
        painter.setPen(edge_pen)
        self._draw_quad(painter, front_points)
        
        # Draw chamfered edges (as lines at corners)
        chamfer_pen = QPen(self._edge_color, 1)
        painter.setPen(chamfer_pen)
        
        # Top chamfers
        if highlight_top:
            painter.setPen(QPen(self._highlight_color, 2))
        
        # Draw horizontal top edge
        painter.drawLine(front_points[0], front_points[1])
        
        # Draw vertical edges with chamfer indication
        for i in [0, 1]:
            painter.drawLine(front_points[i], back_points[i])
        
        # Reset pen
        painter.setPen(edge_pen)
    
    def _draw_quad(
        self, 
        painter: QPainter, 
        points: list
    ) -> None:
        """Draw a quadrilateral from 4 points."""
        path = QPainterPath()
        path.moveTo(points[0][0], points[0][1])
        for i in range(1, 4):
            path.lineTo(points[i][0], points[i][1])
        path.closeSubpath()
        painter.drawPath(path)
    
    def _draw_labels(
        self, 
        painter: QPainter,
        cx: int,
        cy: int,
        half: int
    ) -> None:
        """Draw view labels on the cube faces."""
        font = painter.font()
        font.setPointSize(8)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(self._text_color)
        
        # Draw face labels based on rotation
        label_offset = half + 15
        
        # Front
        if abs(self._current_rotation % 360) < 45:
            painter.drawText(cx - 5, cy + 3, "F")
        
        # Back
        if abs((self._current_rotation % 360) - 180) < 45:
            painter.drawText(cx - 5, cy + 3, "K")
        
        # Top
        if abs(self._current_pitch) > 60:
            painter.drawText(cx - 5, cy + 3, "T")
    
    def mousePressEvent(self, event) -> None:
        """Handle mouse press."""
        if event.button() == Qt.LeftButton:
            self._is_dragging = True
            self._drag_start_pos = event.pos()
            self._state = self.State.DRAGGING
            event.accept()
    
    def mouseMoveEvent(self, event) -> None:
        """Handle mouse move."""
        if self._is_dragging:
            # Update rotation based on drag
            delta = event.pos() - self._drag_start_pos
            
            self._current_rotation += delta.x() * 0.5
            self._current_pitch = max(-90, min(90, 
                self._current_pitch + delta.y() * 0.5
            ))
            
            self._drag_start_pos = event.pos()
            self.update()
            event.accept()
        else:
            # Check for hover
            self._check_hover(event.pos())
    
    def mouseReleaseEvent(self, event) -> None:
        """Handle mouse release."""
        if event.button() == Qt.LeftButton:
            if self._is_dragging:
                # Check if it was a click (minimal drag)
                delta = (event.pos() - self._drag_start_pos).manhattanLength()
                
                if delta < 10:
                    # It was a click - emit view changed
                    view = self._get_view_from_position(event.pos())
                    if view:
                        self.view_changed.emit(view)
                
                self._is_dragging = False
                self._state = self.State.IDLE
                event.accept()
    
    def wheelEvent(self, event) -> None:
        """Handle mouse wheel for quick rotation."""
        delta = event.angleDelta().y()
        self._current_rotation += delta * 0.1
        self.update()
        event.accept()
    
    def _check_hover(self, pos: QPoint) -> None:
        """Check if mouse is hovering over the cube."""
        cx = self.width() // 2
        cy = self.height() // 2
        half = self.cube_size // 2
        
        # Simple bounding box check
        if (abs(pos.x() - cx) < half and abs(pos.y() - cy) < half):
            if self._state != self.State.HOVERING:
                self._state = self.State.HOVERING
                self.setCursor(Qt.PointingHandCursor)
                self.update()
        else:
            if self._state == self.State.HOVERING:
                self._state = self.State.IDLE
                self.unsetCursor()
                self.update()
    
    def _get_view_from_position(self, pos: QPoint) -> Optional[str]:
        """Determine which view was clicked based on position."""
        cx = self.width() // 2
        cy = self.height() // 2
        
        dx = pos.x() - cx
        dy = pos.y() - cy
        
        # Determine quadrant/octant
        half = self.cube_size // 3
        
        # Simplified view determination based on position and rotation
        rotation = self._current_rotation % 360
        pitch = self._current_pitch
        
        # Front view
        if abs(dx) < half and dy < -half//2:
            return "front"
        # Back view
        if abs(dx) < half and dy > half//2:
            return "back"
        # Top view
        if dy < -half:
            return "top"
        # Bottom view  
        if dy > half:
            return "bottom"
        # Right view
        if dx > half:
            return "right"
        # Left view
        if dx < -half:
            return "left"
        
        return "front"  # Default
    
    def set_rotation(self, yaw: float, pitch: float) -> None:
        """Set the cube rotation."""
        self._current_rotation = yaw
        self._current_pitch = pitch
        self.update()
    
    def get_rotation(self) -> Tuple[float, float]:
        """Get current rotation (yaw, pitch)."""
        return (self._current_rotation, self._current_pitch)
    
    def highlight_view(self, view_name: str) -> None:
        """Highlight a specific view."""
        self._hovered_region = view_name
        self.update()
    
    def clear_highlight(self) -> None:
        """Clear highlight."""
        self._hovered_region = None
        self.update()
