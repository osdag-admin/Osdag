"""
Custom 3D CAD Viewer with stable hover highlighting for models and ViewCube.
"""
from PySide6.QtCore import QEvent, QPoint, QTimer, QTime, Qt
from PySide6.QtWidgets import QToolTip, QApplication

from osdag_gui.__config__ import CAD_BACKEND

from OCC.Display import backend
backend.load_backend(CAD_BACKEND)

from OCC.Display.qtDisplay import qtViewer3d
from osdag_gui.ui.components.navicube_overlay import NaviCubeOverlay
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


class CustomViewer3d(qtViewer3d):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.context = None
        self.view = None

        self.model_ais_objects = {}
        self.model_hover_labels = {}

        self.current_hovered_model = None
        self.current_highlighted_ais_list = []

        self.hover_timer = QTimer(self)
        self.hover_timer.setSingleShot(True)
        self.hover_timer.timeout.connect(self.show_tooltip)
        self.hover_position = None

        # Host the overlay as a sibling widget instead of a child of the
        # OCC/OpenGL canvas. This avoids corrupted transparent repaints on Linux.
        overlay_parent = parent if parent is not None else self
        self.navicube = NaviCubeOverlay(self, overlay_parent)
        self.navicube.viewOrientationRequested.connect(self._on_navicube_clicked)
        self.navicube.hide()
        self._overlay_anchor = overlay_parent
        if self._overlay_anchor is not None and self._overlay_anchor is not self:
            self._overlay_anchor.installEventFilter(self)

        # ---------------- Navigation state ----------------
        self.active_nav_mode = None      # NavMode.ROTATE / PAN 
        self.is_dragging_nav = False
        self.last_mouse_pos = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._position_navicube()

    def moveEvent(self, event):
        super().moveEvent(event)
        self._position_navicube()

    def showEvent(self, event):
        super().showEvent(event)
        self._position_navicube()

    def hideEvent(self, event):
        if hasattr(self, "navicube") and self.navicube:
            self.navicube.hide()
        super().hideEvent(event)

    def _position_navicube(self):
        if not hasattr(self, "navicube") or not self.navicube:
            return

        host = self.navicube.parentWidget()
        if host is None:
            return

        padding = 10
        local_pos = QPoint(
            max(0, self.width() - self.navicube.width() - padding),
            padding,
        )

        if host is self:
            target_pos = local_pos
        elif self.navicube.isWindow():
            target_pos = self.mapToGlobal(local_pos)
        else:
            global_pos = self.mapToGlobal(local_pos)
            target_pos = host.mapFromGlobal(global_pos)

        self.navicube.move(target_pos)
        if self.navicube.isVisible():
            self.navicube.raise_()

    def eventFilter(self, watched, event):
        if watched is getattr(self, "_overlay_anchor", None):
            if event.type() in (
                QEvent.Move,
                QEvent.Resize,
                QEvent.Show,
                QEvent.WindowStateChange,
            ):
                self._position_navicube()
                if hasattr(self, "navicube") and self.navicube and self.navicube.isVisible():
                    self.navicube.raise_()
        return super().eventFilter(watched, event)

    def _on_navicube_clicked(self, px, py, pz, ux, uy, uz):
        """
        Receives camera orientation on every animation tick (~60fps).

        The navicube now only emits animated camera states. We avoid any
        extra end-of-animation correction here because that was the source
        of the visible settle/jiggle after face clicks.
        """
        if not self.view:
            return

        # Guard: OCC raises V3d_BadValue if projection vector is zero
        if abs(px) < 1e-6 and abs(py) < 1e-6 and abs(pz) < 1e-6:
            return

        self.view.SetProj(px, py, pz)
        self.view.SetUp(ux, uy, uz)
        self.view.Redraw()


    # ------------------------------------------------------------------
    # Mouse Move Event (FIXED)
    # ------------------------------------------------------------------
    def mouseMoveEvent(self, event):

        # ---------------- NAVIGATION MOVE ----------------
        if self.is_dragging_nav and self.active_nav_mode:
            pixel_ratio = self.devicePixelRatioF()

            x = int(event.position().x() * pixel_ratio)
            y = int(event.position().y() * pixel_ratio)

            last_x = int(self.last_mouse_pos.x() * pixel_ratio)
            last_y = int(self.last_mouse_pos.y() * pixel_ratio)

            dx = x - last_x
            dy = y - last_y

            if self.active_nav_mode == NavMode.ROTATE:
                self.view.Rotation(x, y)

            elif self.active_nav_mode == NavMode.PAN:
                self.view.Pan(dx, -dy)

            self.last_mouse_pos = event.position()
            event.accept()
            return

        if not self.context or not self.view:
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

                # ------------------------------------------------------
                # STANDARD MODEL HIGHLIGHTING
                # ------------------------------------------------------
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
                    for obj in self.current_highlighted_ais_list:
                        try:
                            self.context.Unhilight(obj, False)
                        except:
                            pass

                    self.current_highlighted_ais_list = objects_to_highlight

                    for obj in self.current_highlighted_ais_list:
                        try:
                            self.context.HilightWithColor(
                                obj, self.context.HighlightStyle(), False
                            )
                        except:
                            pass

                    self.view.Redraw()

            else:
                # Nothing detected → cleanup
                if self.current_highlighted_ais_list:
                    for obj in self.current_highlighted_ais_list:
                        try:
                            self.context.Unhilight(obj, False)
                        except:
                            pass
                    self.current_highlighted_ais_list = []
                    self.view.Redraw()

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

    # ------------------------------------------------------------------
    # Tooltip
    # ------------------------------------------------------------------
    def show_tooltip(self):
        if (
            self.current_hovered_model
            and self.current_hovered_model in self.model_hover_labels
            and self.hover_position
        ):
            QToolTip.showText(
                self.hover_position,
                self.model_hover_labels[self.current_hovered_model],
                self,
            )

    # ------------------------------------------------------------------
    # Leave Event
    # ------------------------------------------------------------------
    def leaveEvent(self, event):
        self.hover_timer.stop()
        self.current_hovered_model = None

        if self.current_highlighted_ais_list:
            for obj in self.current_highlighted_ais_list:
                try:
                    self.context.Unhilight(obj, False)
                except:
                    pass
            self.current_highlighted_ais_list = []
            self.view.Redraw()

        QToolTip.hideText()

        # restore holding cursor so cursor can update
        self.unsetCursor()
        QApplication.restoreOverrideCursor()
        self.releaseMouse()
        super().leaveEvent(event)

    def cleanup_for_new_model(self):
        """
        Clean up all internal state before displaying a new model.
        This prevents memory corruption from stale OCC object references.
        
        Uses IsDisplayed/IsHilighted checks for OS-independent safety:
        - Windows requires explicit Remove before EraseAll for AIS_ViewCube
        - Linux crashes with double-free if Remove is called on already-freed objects
        - Checking first avoids both issues.
        """
        
        # Clear highlighted objects list - use IsHilighted check for OS-independent safety
        if self.current_highlighted_ais_list and self.context:
            for obj in self.current_highlighted_ais_list:
                try:
                    # Only unhilight if confirmed still highlighted
                    if self.context.IsHilighted(obj):
                        self.context.Unhilight(obj, False)
                except Exception:
                    pass  # Object may already be unhighlighted or invalid
            self.current_highlighted_ais_list = []
        elif self.current_highlighted_ais_list:
            # Context not available, just clear the list
            self.current_highlighted_ais_list = []
        
        self.current_highlighted_owner = None
        self.current_hovered_model = None
        
        # Clear the model AIS objects dictionary
        self.model_ais_objects.clear()
        
        # Clear hover labels
        self.model_hover_labels.clear()
        
        # NOTE: Do NOT call gc.collect() here!
        # The gdb backtrace shows the crash happens during GC when trying to clean up
        # Shiboken MetaObjectBuilder objects. Let Python handle GC naturally.

    # ------------------------------------------------------------------
    # View Cube Display
    # ------------------------------------------------------------------

    def display_view_cube(self):
        """Displays the custom Qt Navicube overlay after CAD Init."""
        if hasattr(self, "navicube") and self.navicube:
            self._position_navicube()
            self.navicube.request_sync()
            self.navicube.show()
            self.navicube.raise_()
            self.navicube.update()

    # ------------------------------------------------------------------
    # Mouse Press
    # ------------------------------------------------------------------
    def mousePressEvent(self, event):
        if not self.context or not self.view:
            super().mousePressEvent(event)
            return

        if event.button() == Qt.LeftButton and self.active_nav_mode:
            if hasattr(self, "navicube") and self.navicube:
                self.navicube.set_interaction_sync_active(True)

        pixel_ratio = self.devicePixelRatioF()
        x = int(event.position().x() * pixel_ratio)
        y = int(event.position().y() * pixel_ratio)

        self.context.MoveTo(x, y, self.view, True)

        # ---------------- NAVIGATION START ----------------
        if (
            event.button() == Qt.LeftButton
            and self.active_nav_mode
            and self._can_start_navigation()
        ):
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

    # ------------------------------------------------------------------
    # Mouse Release
    # ------------------------------------------------------------------
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.active_nav_mode:
            if hasattr(self, "navicube") and self.navicube:
                self.navicube.set_interaction_sync_active(False)

        # ---------------- NAVIGATION END ----------------
        if self.is_dragging_nav and event.button() == Qt.LeftButton:
            self.is_dragging_nav = False
            self.last_mouse_pos = None
            event.accept()
            return

        # restore holding cursor so cursor can update
        self.unsetCursor()
        QApplication.restoreOverrideCursor()
        self.releaseMouse()
        super().mouseReleaseEvent(event)

    def set_navigation_mode(self, mode):
        """
        mode: NavMode.ROTATE | NavMode.PAN | None
        """
        self.active_nav_mode = mode

    def _can_start_navigation(self):
        if not self.context.HasDetected():
            return False
        return True



class NavMode:
    ROTATE = "ROTATE"
    PAN = "PAN"
