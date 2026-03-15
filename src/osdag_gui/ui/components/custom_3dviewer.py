"""
Custom 3D CAD Viewer with stable hover highlighting for models and ViewCube.
"""
import math
from PySide6.QtCore import QEvent, QPoint, QTimer, QTime, Qt
from PySide6.QtWidgets import QToolTip, QApplication

from osdag_gui.__config__ import CAD_BACKEND

from OCC.Display import backend
backend.load_backend(CAD_BACKEND)

from OCC.Display.qtDisplay import qtViewer3d
from navcube import NavCubeOverlay, NavCubeStyle
from navcube.connectors.occ import OCCNavCubeSync
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
        self.current_highlighted_owner = None

        self.hover_timer = QTimer(self)
        self.hover_timer.setSingleShot(True)
        self.hover_timer.timeout.connect(self.show_tooltip)
        self.hover_position = None

        # Host the overlay as a sibling widget instead of a child of the
        # OCC/OpenGL canvas. This avoids corrupted transparent repaints on Linux.
        overlay_parent = parent if parent is not None else self
        self.navcube = NavCubeOverlay(overlay_parent)   # zero OCC dependency
        self.navcube.hide()
        self._overlay_anchor = overlay_parent
        self._navcube_sync: OCCNavCubeSync | None = None  # created once view is ready
        if self._overlay_anchor is not None and self._overlay_anchor is not self:
            self._overlay_anchor.installEventFilter(self)
        self.destroyed.connect(self._teardown_navcube)

        # ---------------- Navigation state ----------------
        self.active_nav_mode = None      # NavMode.ROTATE / PAN 
        self.is_dragging_nav = False
        self.last_mouse_pos = None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._position_navcube()

    def moveEvent(self, event):
        super().moveEvent(event)
        self._position_navcube()

    def showEvent(self, event):
        super().showEvent(event)
        self._position_navcube()

    def hideEvent(self, event):
        if hasattr(self, "navcube") and self.navcube:
            self.navcube.hide()
        super().hideEvent(event)

    def _position_navcube(self):
        if not hasattr(self, "navcube") or not self.navcube:
            return

        host = self.navcube.parentWidget()
        if host is None:
            return

        padding = 10
        local_pos = QPoint(
            max(0, self.width() - self.navcube.width() - padding),
            padding,
        )

        if host is self:
            target_pos = local_pos
        elif self.navcube.isWindow():
            target_pos = self.mapToGlobal(local_pos)
        else:
            global_pos = self.mapToGlobal(local_pos)
            target_pos = host.mapFromGlobal(global_pos)

        self.navcube.move(target_pos)
        if self.navcube.isVisible():
            self.navcube.raise_()

    def eventFilter(self, watched, event):
        if watched is getattr(self, "_overlay_anchor", None):
            if event.type() in (
                QEvent.Move,
                QEvent.Resize,
                QEvent.Show,
                QEvent.WindowStateChange,
            ):
                self._position_navcube()
                if hasattr(self, "navcube") and self.navcube and self.navcube.isVisible():
                    self.navcube.raise_()
        return super().eventFilter(watched, event)

    # ------------------------------------------------------------------
    # Mouse Move Event
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
    # NaviCube teardown
    # ------------------------------------------------------------------

    def _teardown_navcube(self):
        """
        Called via self.destroyed signal when this viewer's C++ object is
        being deleted.  Tears down the OCC sync helper (stops its poll timer,
        disconnects signals) then makes the navicube widget inert.
        The widget itself is parented to the tab and is deleted by Qt; we
        just ensure no OCC calls happen after this point.
        """
        try:
            sync = getattr(self, "_navcube_sync", None)
            if sync is not None:
                sync.teardown()
                self._navcube_sync = None
        except Exception:
            pass
        try:
            nc = getattr(self, "navcube", None)
            if nc is not None:
                nc._tmr.stop()   # stop navicube's own animation timer
                nc.hide()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # View Cube Display
    # ------------------------------------------------------------------

    def display_view_cube(self):
        """Displays the custom Qt NaviCube overlay after CAD init."""
        if not (hasattr(self, "navcube") and self.navcube and self.view):
            return

        # Refined pastel tri-tone — jewel-depth pastels on light grey viewport
        #   faces   → richer periwinkle (more saturated, less washed)
        #   edges   → deep rose-pink bevel
        #   corners → fresh mint bevel
        style = NavCubeStyle(
            theme="light",
            face_color=(205, 215, 252),          # richer periwinkle — more blue saturation
            edge_color=(252, 186, 208),          # deeper rose-pink bevel
            corner_color=(182, 238, 210),        # fresh mint bevel
            text_color=(28, 26, 68),             # deep indigo — sharper than near-black
            border_color=( 82,  78, 138),        # soft violet frame
            border_secondary_color=(145, 142, 178),
            border_width_main=1.8,
            border_width_secondary=1.0,
            hover_color=(218,  62, 112, 250),    # rich raspberry — decisive, not soft
            hover_text_color=(255, 255, 255),
            dot_color=(182, 178, 228, 218),
            shadow_color=( 45,  25,  88,  55),   # violet-tinted shadow — pulls from face family
            shadow_offset_x=2.2,
            shadow_offset_y=2.8,
            # dark-theme mirrors
            face_color_dark=(118, 108, 168),
            edge_color_dark=(178, 105, 132),
            corner_color_dark=( 92, 152, 122),
            text_color_dark=(242, 240, 255),
            border_color_dark=( 22,  18,  38),
            border_secondary_color_dark=( 44,  40,  62),
            hover_color_dark=(205,  55, 105, 250),
            # gizmo axes harmonized with the face palette
            show_gizmo=True,
            gizmo_x_color=(228,  78, 108),       # rose-red  — echoes edge bevel
            gizmo_y_color=( 75, 198, 138),       # mint      — echoes corner bevel
            gizmo_z_color=( 85, 132, 238),       # periwinkle— echoes face
            # feel
            inactive_opacity=0.65,
            animation_ms=350,
            light_direction=(-0.6, -1.2, -1.6),  # slightly steeper — more face contrast
        )
        self.navcube.set_style(style)

        # Create the OCC sync bridge the first time the view is ready.
        if self._navcube_sync is None:
            self._navcube_sync = OCCNavCubeSync(self.view, self.navcube)
        self._position_navcube()
        self.navcube.show()
        self.navcube.raise_()
        QTimer.singleShot(0, self.navcube._update_dpi)
        self.navcube.update()

    # ------------------------------------------------------------------
    # Mouse Press
    # ------------------------------------------------------------------
    def mousePressEvent(self, event):
        if not self.context or not self.view:
            super().mousePressEvent(event)
            return

        if self._navcube_sync is not None:
            self._navcube_sync.set_interaction_active(True)

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
        if self._navcube_sync is not None:
            self._navcube_sync.set_interaction_active(False)

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
