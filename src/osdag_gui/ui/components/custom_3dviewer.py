"""
Custom 3D CAD Viewer with stable hover highlighting for models and Python-based ViewCube.
"""
from PySide6.QtCore import QTimer, QTime, Qt, QPoint
from PySide6.QtWidgets import QToolTip, QApplication
from typing import Dict, List, Optional, Any
from osdag_gui.__config__ import CAD_BACKEND

from OCC.Display import backend
backend.load_backend(CAD_BACKEND)

from OCC.Display.qtDisplay import qtViewer3d
from OCC.Core.AIS import AIS_ViewCube
from OCC.Core.Prs3d import Prs3d_DatumAspect, Prs3d_Drawer
from OCC.Core.Quantity import (
    Quantity_Color,
    Quantity_NOC_WHITE,
    Quantity_NOC_GRAY50,
    Quantity_NOC_BLACK,
    Quantity_NOC_CYAN,
)
from OCC.Core.V3d import V3d_Zpos
from OCC.Core.Aspect import Aspect_GT_Rectangular, Aspect_GDM_Lines

from osdag_gui.ui.components.view_cube_widget import ViewCubeWidget


class CustomViewer3d(qtViewer3d):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.context = None
        self.view = None

        self.model_ais_objects: Dict[str, List[Any]] = {}
        self.model_hover_labels: Dict[str, str] = {}

        self.current_hovered_model: Optional[str] = None
        self.current_highlighted_ais_list: List[Any] = []

        self.hover_timer = QTimer(self)
        self.hover_timer.setSingleShot(True)
        self.hover_timer.timeout.connect(self.show_tooltip)
        self.hover_position: Optional[QPoint] = None

        # OCC ViewCube state (disabled)
        self.view_cube = None
        self.view_cube_active = False
        self.is_interacting_with_cube = False
        self.mouse_press_pos = None
        self.mouse_press_time = 0

        self.python_view_cube_widget: Optional[ViewCubeWidget] = None
        self._view_cube_enabled = True

        self.active_nav_mode: Optional[str] = None
        self.is_dragging_nav = False
        self.last_mouse_pos: Optional[QPoint] = None

        QTimer.singleShot(100, self._init_python_view_cube)

    def _init_python_view_cube(self) -> None:
        try:
            if self._view_cube_enabled:
                self.python_view_cube_widget = ViewCubeWidget(
                    parent=self,
                    cube_size=100,
                    position="top_right",  
                    margin=70
                )
                self.python_view_cube_widget.view_changed.connect(
                    self._on_view_cube_changed
                )
                self.python_view_cube_widget.show()
                print("Python View Cube initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Python View Cube: {e}")

    def _on_view_cube_changed(self, view_name: str) -> None:
        if not self.view:
            return
        
        try:
            from osdag_gui.ui.components.view_cube import ChamferedViewCube
            
            if view_name in ChamferedViewCube.VIEWS:
                view_info = ChamferedViewCube.VIEWS[view_name]
                direction = view_info.direction
                camera_distance = 500
                
                self.view.SetProj(
                    direction.X() * camera_distance,
                    direction.Y() * camera_distance,
                    direction.Z() * camera_distance,
                    0, 0, 0
                )
                
                self.view.Redraw()
                print(f"View changed to: {view_name}")
                
        except Exception as e:
            print(f"Error changing view: {e}")

    # ------------------------------------------------------------------
    # Mouse Event Handling
    # ------------------------------------------------------------------
    def mouseMoveEvent(self, event):
        if self.python_view_cube_widget and self.python_view_cube_widget.isVisible():
            global_pos = event.globalPosition().toPoint()
            local_pos = self.python_view_cube_widget.mapFromGlobal(global_pos)
            
            if self.python_view_cube_widget.rect().contains(local_pos):
                self.python_view_cube_widget.mouseMoveEvent(event)
                
                if self.current_highlighted_ais_list:
                    self._clear_highlights()
                if self.view_cube_active:
                    self._reset_view_cube_state()
                
                event.accept()
                return

        # ---------------- NAVIGATION MOVE ----------------
        if self.is_dragging_nav and self.active_nav_mode and self.view:
            pixel_ratio = self.devicePixelRatioF()
            x = int(event.position().x() * pixel_ratio)
            y = int(event.position().y() * pixel_ratio)
            last_x = int(self.last_mouse_pos.x() * pixel_ratio) if self.last_mouse_pos else x
            last_y = int(self.last_mouse_pos.y() * pixel_ratio) if self.last_mouse_pos else y
            dx = x - last_x
            dy = y - last_y

            if self.active_nav_mode == NavMode.ROTATE:
                self.view.Rotation(x, y)
            elif self.active_nav_mode == NavMode.PAN:
                self.view.Pan(dx, -dy)

            self.last_mouse_pos = event.position()
            event.accept()
            return

        # ---------------- HOVER HIGHLIGHTING ----------------
        if not self.context or not self.view:
            super().mouseMoveEvent(event)
            return

        if self.is_interacting_with_cube:
            super().mouseMoveEvent(event)
            return

        try:
            pixel_ratio = self.devicePixelRatioF()
            x = int(event.position().x() * pixel_ratio)
            y = int(event.position().y() * pixel_ratio)

            self.context.MoveTo(x, y, self.view, True)

            hovered_model = None

            if self.context.HasDetected():
                detected = self.context.DetectedInteractive()

                if self.view_cube and detected == self.view_cube:
                    if not self.view_cube_active:
                        self.context.SetAutomaticHilight(True)
                        self.view_cube_active = True
                    return

                if self.view_cube_active:
                    self._reset_view_cube_state()

                for model_name, ais_list in self.model_ais_objects.items():
                    for ais in ais_list:
                        if detected == ais:
                            hovered_model = model_name
                            break
                    if hovered_model:
                        break

                objects_to_highlight = []

                if hovered_model in ("Bolt", "Nut"):
                    objects_to_highlight.extend(self.model_ais_objects.get("Bolt", []))
                    objects_to_highlight.extend(self.model_ais_objects.get("Nut", []))
                elif detected:
                    objects_to_highlight.append(detected)

                if set(objects_to_highlight) != set(self.current_highlighted_ais_list):
                    self._update_highlights(objects_to_highlight)

            else:
                if self.view_cube_active:
                    self._reset_view_cube_state()
                if self.current_highlighted_ais_list:
                    self._clear_highlights()

            self.hover_position = event.globalPosition().toPoint()
            if hovered_model != self.current_hovered_model:
                self.current_hovered_model = hovered_model
                self.hover_timer.start(100)
            elif hovered_model is None:
                QToolTip.hideText()

        except Exception as e:
            print(f"mouseMoveEvent error: {e}")
            QToolTip.hideText()

        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if self.python_view_cube_widget and self.python_view_cube_widget.isVisible():
            global_pos = event.globalPosition().toPoint()
            local_pos = self.python_view_cube_widget.mapFromGlobal(global_pos)
            
            if self.python_view_cube_widget.rect().contains(local_pos):
                self.python_view_cube_widget.mousePressEvent(event)
                event.accept()
                return

        if not self.context or not self.view:
            super().mousePressEvent(event)
            return

        pixel_ratio = self.devicePixelRatioF()
        x = int(event.position().x() * pixel_ratio)
        y = int(event.position().y() * pixel_ratio)

        self.context.MoveTo(x, y, self.view, True)

        if self.context.HasDetected():
            if self.view_cube and self.context.DetectedInteractive() == self.view_cube:
                self.is_interacting_with_cube = True
                self.mouse_press_pos = event.position()
                self.mouse_press_time = QTime.currentTime().msecsSinceStartOfDay()

        if (event.button() == Qt.LeftButton and 
            self.active_nav_mode and 
            not self.is_interacting_with_cube and 
            self._can_start_navigation()):
            
            self.is_dragging_nav = True
            self.last_mouse_pos = event.position()
            pixel_ratio = self.devicePixelRatioF()
            x = int(event.position().x() * pixel_ratio)
            y = int(event.position().y() * pixel_ratio)

            if self.active_nav_mode == NavMode.ROTATE:
                self.view.StartRotation(x, y)

            event.accept()
            return

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.python_view_cube_widget and self.python_view_cube_widget.isVisible():
            global_pos = event.globalPosition().toPoint()
            local_pos = self.python_view_cube_widget.mapFromGlobal(global_pos)
            
            if self.python_view_cube_widget.rect().contains(local_pos):
                self.python_view_cube_widget.mouseReleaseEvent(event)
                event.accept()
                return

        if self.is_dragging_nav and event.button() == Qt.LeftButton:
            self.is_dragging_nav = False
            self.last_mouse_pos = None
            event.accept()
            return

        if self.is_interacting_with_cube:
            current_time = QTime.currentTime().msecsSinceStartOfDay()
            dt = current_time - self.mouse_press_time
            dist = (event.position() - self.mouse_press_pos).manhattanLength() if self.mouse_press_pos else 0

            if dt < 500 and dist < 10:
                super().mouseReleaseEvent(event)
            else:
                self.context.MoveTo(-1, -1, self.view, True)
                super().mouseReleaseEvent(event)

            self.is_interacting_with_cube = False
            self.mouse_press_pos = None
            return

        self.unsetCursor()
        QApplication.restoreOverrideCursor()
        self.releaseMouse()
        super().mouseReleaseEvent(event)

    def leaveEvent(self, event):
        self.hover_timer.stop()
        self.current_hovered_model = None

        if self.view_cube_active:
            self._reset_view_cube_state()
        if self.current_highlighted_ais_list:
            self._clear_highlights()

        QToolTip.hideText()
        self.unsetCursor()
        QApplication.restoreOverrideCursor()
        self.releaseMouse()
        super().leaveEvent(event)

    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------
    def _clear_highlights(self) -> None:
        for obj in self.current_highlighted_ais_list:
            try:
                self.context.Unhilight(obj, False)
            except Exception:
                pass
        self.current_highlighted_ais_list = []
        if self.view:
            self.view.Redraw()

    def _update_highlights(self, objects_to_highlight: List[Any]) -> None:
        for obj in self.current_highlighted_ais_list:
            try:
                self.context.Unhilight(obj, False)
            except Exception:
                pass

        self.current_highlighted_ais_list = objects_to_highlight

        for obj in self.current_highlighted_ais_list:
            try:
                self.context.HilightWithColor(
                    obj, self.context.HighlightStyle(), False
                )
            except Exception:
                pass

        if self.view:
            self.view.Redraw()

    def _reset_view_cube_state(self) -> None:
        self.context.SetAutomaticHilight(False)
        self.view_cube_active = False
        try:
            self.context.Unhilight(self.view_cube, True)
        except Exception:
            pass

    def show_tooltip(self) -> None:
        if (self.current_hovered_model and 
            self.current_hovered_model in self.model_hover_labels and 
            self.hover_position):
            QToolTip.showText(
                self.hover_position,
                self.model_hover_labels[self.current_hovered_model],
                self,
            )

    def _can_start_navigation(self) -> bool:
        if not self.context or not self.context.HasDetected():
            return True
        if self.context.DetectedInteractive() == self.view_cube:
            return False
        return True

    # ------------------------------------------------------------------
    # View Cube Control
    # ------------------------------------------------------------------
    def display_view_cube(self) -> None:
        if self.python_view_cube_widget:
            self.python_view_cube_widget.show()

    def hide_view_cube(self) -> None:
        if self.python_view_cube_widget:
            self.python_view_cube_widget.hide()

    def set_view_cube_enabled(self, enabled: bool) -> None:
        self._view_cube_enabled = enabled
        if enabled:
            self.display_view_cube()
        else:
            self.hide_view_cube()

    # ------------------------------------------------------------------
    # Model Management
    # ------------------------------------------------------------------
    def cleanup_for_new_model(self) -> None:
        if hasattr(self, 'view_cube') and self.view_cube and self.context:
            try:
                if self.context.IsDisplayed(self.view_cube):
                    self.context.Remove(self.view_cube, False)
            except Exception:
                pass
            finally:
                self.view_cube = None
        elif hasattr(self, 'view_cube'):
            self.view_cube = None
        
        self.view_cube_active = False
        self.is_interacting_with_cube = False
        
        if self.current_highlighted_ais_list and self.context:
            for obj in self.current_highlighted_ais_list:
                try:
                    if self.context.IsHilighted(obj):
                        self.context.Unhilight(obj, False)
                except Exception:
                    pass
            self.current_highlighted_ais_list = []
        elif self.current_highlighted_ais_list:
            self.current_highlighted_ais_list = []
        
        self.current_hovered_model = None
        self.model_ais_objects.clear()
        self.model_hover_labels.clear()

    # ------------------------------------------------------------------
    # Navigation Control
    # ------------------------------------------------------------------
    def set_navigation_mode(self, mode: Optional[str]) -> None:
        self.active_nav_mode = mode

    # ------------------------------------------------------------------
    # OCC View Cube (Disabled - kept for reference)
    # ------------------------------------------------------------------
    def _display_occ_view_cube(self) -> None:
        try:
            if hasattr(self, 'view_cube') and self.view_cube:
                try:
                    self.context.Remove(self.view_cube, False)
                except Exception:
                    pass
                self.view_cube = None
            
            self.view_cube = AIS_ViewCube()
            self.view_cube.SetSize(45)
            self.view_cube.SetFontHeight(12)
            self.view_cube.SetAxesLabels("", "", "")
            self.view_cube.SetDrawAxes(False)
            self.view_cube.SetBoxFacetExtension(12)

            highlight_drawer = Prs3d_Drawer()
            highlight_drawer.SetColor(Quantity_Color(Quantity_NOC_CYAN))
            self.view_cube.SetHilightAttributes(highlight_drawer)
            
            drawer = self.view_cube.Attributes()
            drawer.SetDatumAspect(Prs3d_DatumAspect())
            
            color_white = Quantity_Color(Quantity_NOC_WHITE)
            color_gray = Quantity_Color(Quantity_NOC_GRAY50)
            color_black = Quantity_Color(Quantity_NOC_BLACK)
            
            self.view_cube.SetColor(color_white)
            self.view_cube.SetBoxColor(color_gray)
            self.view_cube.SetTextColor(color_black)
            
            self.context.Display(self.view_cube, False)
            
            try:
                from OCC.Core.Graphic3d import Graphic3d_TransformPers, Graphic3d_TMF_TriedronPers, Graphic3d_Vec2i
                from OCC.Core.Aspect import Aspect_TOTP_RIGHT_UPPER
                
                offset = Graphic3d_Vec2i(60, 70)
                transform_pers = Graphic3d_TransformPers(Graphic3d_TMF_TriedronPers, Aspect_TOTP_RIGHT_UPPER, offset)
                self.view_cube.SetTransformPersistence(transform_pers)
            except Exception as e:
                print(f"Using fallback positioning: {e}")
                try:
                    from OCC.Core.Graphic3d import Graphic3d_TransformPers, Graphic3d_TMF_2d
                    from OCC.Core.gp import gp_Pnt2d
                    offset = gp_Pnt2d(850, 40) 
                    transform_pers = Graphic3d_TransformPers(Graphic3d_TMF_2d, offset)
                    self.view_cube.SetTransformPersistence(transform_pers)
                except:
                    self.view_cube.SetTransformPersistence(
                        V3d_Zpos, 
                        Aspect_GT_Rectangular, 
                        Aspect_GDM_Lines
                    )
            
            self.view.Redraw()
        except Exception as e:
            print(f"Error displaying View Cube: {e}")


class NavMode:
    ROTATE = "ROTATE"
    PAN = "PAN"