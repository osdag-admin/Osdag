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
        self._resize_navcube()
        self._position_navcube()

    def _resize_navcube(self):
        """Scale the NavCube to a consistent 8% of the viewport in physical pixels.

        style.size is a 96-dpi-equivalent reference pixel value.  _update_dpi
        converts it via:  target_phys = ref_size * physical_dpi / 96.

        To keep the cube at exactly vp_physical * 0.08 physical pixels on every
        screen (regardless of OS zoom level or monitor DPI) we set:
            ref_size = vp_physical * 0.08 * 96 / physical_dpi

        Then _update_dpi computes:
            target_phys = ref_size * physical_dpi / 96 = vp_physical * 0.08  ✓
            new_size    = target_phys / dpr            = vp_logical  * 0.08  ✓

        Padding uses the same 96/physical_dpi factor so it stays proportional.
        """
        if not hasattr(self, "navcube") or not self.navcube:
            return
        vp_logical = min(self.width(), self.height())
        if vp_logical < 10:
            return

        nc = self.navcube
        app = QApplication.instance()
        screen = nc.screen() if nc.isVisible() else None
        if screen is None and app:
            screen = app.primaryScreen()
        dpr = max(1.0, screen.devicePixelRatio()) if screen is not None else 1.0

        # Use physical viewport size so the cube fraction is DPI-independent.
        physical_dpi = max(72.0, min(screen.physicalDotsPerInch(), 400.0)) if screen else 96.0
        vp_physical = vp_logical * dpr
        ref_size = max(40, min(round(vp_physical * 0.08 * 96.0 / physical_dpi), 90))
        ref_padding = round(10 * 96.0 / physical_dpi)   # consistent logical pad across DPIs
        ref_scale = round(25.0 * ref_size / 100.0, 2)

        if (nc._style.size == ref_size and nc._style.padding == ref_padding
                and abs(nc._style.scale - ref_scale) < 0.05):
            return
        nc._style.size = ref_size
        nc._style.padding = ref_padding
        nc._style.scale = ref_scale
        nc._update_dpi()

    def moveEvent(self, event):
        super().moveEvent(event)
        self._position_navcube()

    def showEvent(self, event):
        super().showEvent(event)
        self._resize_navcube()
        self._position_navcube()
        # Re-show the navcube when the tab is restored or the window is un-minimized.
        # Only show it if OCC has already been initialised (_navcube_sync set).
        if (
            hasattr(self, "navcube") and self.navcube
            and getattr(self, "_navcube_sync", None) is not None
        ):
            self.navcube.show()
            self.navcube.raise_()

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

        # Engineering-neutral — matches Osdag's UI language
        #   faces   → warm white / light grey (matches panel backgrounds)
        #   edges   → slightly deeper grey bevel
        #   corners → lightest grey bevel
        #   hover   → Osdag blue (#4A90C4)
        #   gizmo   → standard CAD red/green/blue
        style = NavCubeStyle(
            # size=65: 96-dpi-reference pixels.  _resize_navcube overrides this
            # to exactly 9 % of the viewport, but 65 keeps the fallback small on
            # screens whose physicalDotsPerInch > 96 (would inflate size=100 → 137px).
            size=65,
            theme="light",
            face_color=(242, 244, 247),          # warm white-grey — matches panel bg
            edge_color=(218, 224, 232),          # slightly darker bevel
            corner_color=(228, 232, 238),        # light corner bevel
            text_color=(45, 55, 72),             # dark slate — readable, not harsh
            border_color=(30, 30, 30),           # black lines
            border_secondary_color=(80, 80, 80),
            border_width_main=1.6,
            border_width_secondary=0.9,
            hover_color=(145, 176, 20, 235),     # Osdag green #91b014
            hover_text_color=(255, 255, 255),
            dot_color=(60, 60, 60, 180),
            shadow_color=(20, 20, 20, 45),
            shadow_offset_x=2.0,
            shadow_offset_y=2.5,
            # dark-theme mirrors
            face_color_dark=(52, 62, 76),
            edge_color_dark=(42, 52, 65),
            corner_color_dark=(47, 57, 70),
            text_color_dark=(210, 220, 232),
            border_color_dark=(200, 200, 200),
            border_secondary_color_dark=(130, 130, 130),
            hover_color_dark=(145, 176, 20, 235),
            show_gizmo=False,
            # feel
            inactive_opacity=0.70,
            animation_ms=300,
            light_direction=(-0.5, -1.0, -1.5),
        )
        self.navcube.set_style(style)
        self._resize_navcube()   # set size from viewport (may return early if width=0)

        # Create the OCC sync bridge the first time the view is ready.
        if self._navcube_sync is None:
            self._navcube_sync = OCCNavCubeSync(self.view, self.navcube)
        self._position_navcube()
        self.navcube.show()
        self.navcube.raise_()
        # Deferred re-resize: show() triggers _update_dpi internally, so we run
        # _resize_navcube again after the event loop settles to ensure our size wins.
        QTimer.singleShot(50, self._resize_navcube)
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
