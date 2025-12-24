"""
Custom 3D CAD Viewer with stable hover highlighting for models and ViewCube.
"""
from PySide6.QtCore import QTimer, QTime, Qt
from PySide6.QtWidgets import QToolTip, QApplication

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

        # ViewCube interaction state
        self.view_cube = None
        self.view_cube_active = False
        self.is_interacting_with_cube = False
        self.mouse_press_pos = None
        self.mouse_press_time = 0

    # ------------------------------------------------------------------
    # Mouse Move Event (FIXED)
    # ------------------------------------------------------------------
    def mouseMoveEvent(self, event):
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

                # ------------------------------------------------------
                # VIEW CUBE HOVER (STABLE – NO FLICKER)
                # ------------------------------------------------------
                if self.view_cube and detected == self.view_cube:
                    if not self.view_cube_active:
                        self.context.SetAutomaticHilight(True)
                        self.view_cube_active = True
                    return

                # ------------------------------------------------------
                # LEFT VIEW CUBE → CLEANUP
                # ------------------------------------------------------
                if self.view_cube_active:
                    self.context.SetAutomaticHilight(False)
                    self.view_cube_active = False
                    try:
                        self.context.Unhilight(self.view_cube, True)
                    except:
                        pass

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
                if self.view_cube_active:
                    self.context.SetAutomaticHilight(False)
                    self.view_cube_active = False
                    try:
                        self.context.Unhilight(self.view_cube, True)
                    except:
                        pass

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

        if self.view_cube_active:
            self.context.SetAutomaticHilight(False)
            self.view_cube_active = False
            try:
                self.context.Unhilight(self.view_cube, True)
            except:
                pass

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
        """
        import gc
        
        # Reset view cube state
        if hasattr(self, 'view_cube') and self.view_cube:
            try:
                # Try to remove from context if possible
                if self.context:
                    try:
                        self.context.Remove(self.view_cube, False)
                    except Exception:
                        pass  # May already be removed by EraseAll
            except Exception:
                pass
            self.view_cube = None
        
        # Reset View Cube interaction state
        self.view_cube_active = False
        self.is_interacting_with_cube = False
        
        # Clear highlighted objects list
        if self.current_highlighted_ais_list and self.context:
            for obj in self.current_highlighted_ais_list:
                try:
                    self.context.Unhilight(obj, False)
                except Exception:
                    pass
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
        
        # Force garbage collection to clean up OCC shapes
        gc.collect()

    # ------------------------------------------------------------------
    # View Cube Display
    # ------------------------------------------------------------------

    def display_view_cube(self):
        import gc

        try:
            # Force garbage collection before OCC operations to prevent heap corruption
            gc.collect()
            
            # Remove existing view cube if it exists using safe method
            if hasattr(self, 'view_cube') and self.view_cube:
                try:
                    self.context.Remove(self.view_cube, False)
                except Exception as remove_error:
                    # Object may have been displayed in a different context or already removed
                    # Just log and continue - we'll create a fresh one
                    print(f"Note: Could not remove old ViewCube (may already be removed): {remove_error}")
                self.view_cube = None
            
            self.view_cube = AIS_ViewCube()
            self.view_cube.SetSize(45)
            self.view_cube.SetFontHeight(12)
            self.view_cube.SetAxesLabels("", "", "")
            self.view_cube.SetDrawAxes(False)
            
            # Make corner and edge pieces larger for better interaction
            self.view_cube.SetBoxFacetExtension(12)

            # Configure Highlight Attributes
            highlight_drawer = Prs3d_Drawer()
            highlight_drawer.SetColor(Quantity_Color(Quantity_NOC_CYAN))
            self.view_cube.SetHilightAttributes(highlight_drawer)
            
            # Style
            drawer = self.view_cube.Attributes()
            drawer.SetDatumAspect(Prs3d_DatumAspect())
            
            # Colors
            color_white = Quantity_Color(Quantity_NOC_WHITE)
            color_gray = Quantity_Color(Quantity_NOC_GRAY50)
            color_black = Quantity_Color(Quantity_NOC_BLACK)
            
            self.view_cube.SetColor(color_white)
            self.view_cube.SetBoxColor(color_gray)
            self.view_cube.SetTextColor(color_black)
            
            # Display
            self.context.Display(self.view_cube, False)
            
            try:
                from OCC.Core.Graphic3d import Graphic3d_TransformPers, Graphic3d_TMF_TriedronPers, Graphic3d_Vec2i
                from OCC.Core.Aspect import Aspect_TOTP_RIGHT_UPPER
                
                # Create transform persistence anchored to top-right corner
                offset = Graphic3d_Vec2i(60, 70)
                transform_pers = Graphic3d_TransformPers(Graphic3d_TMF_TriedronPers, Aspect_TOTP_RIGHT_UPPER, offset)
                self.view_cube.SetTransformPersistence(transform_pers)
            except Exception as e:
                # Fallback to old method if Graphic3d classes not available
                print(f"Using fallback positioning: {e}")
                try:
                    # Try 2D persistence as fallback
                    from OCC.Core.Graphic3d import Graphic3d_TransformPers, Graphic3d_TMF_2d
                    from OCC.Core.gp import gp_Pnt2d
                    # Try explicit coordinates if corner persistence fails
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

    # ------------------------------------------------------------------
    # Mouse Press
    # ------------------------------------------------------------------
    def mousePressEvent(self, event):
        if not self.context or not self.view:
            super().mousePressEvent(event)
            return

        pixel_ratio = self.devicePixelRatioF()
        x = int(event.position().x() * pixel_ratio)
        y = int(event.position().y() * pixel_ratio)

        self.context.MoveTo(x, y, self.view, True)

        if self.context.HasDetected():
            if self.context.DetectedInteractive() == self.view_cube:
                self.is_interacting_with_cube = True
                self.mouse_press_pos = event.position()
                self.mouse_press_time = QTime.currentTime().msecsSinceStartOfDay()

        super().mousePressEvent(event)

    # ------------------------------------------------------------------
    # Mouse Release
    # ------------------------------------------------------------------
    def mouseReleaseEvent(self, event):
        if self.is_interacting_with_cube:
            current_time = QTime.currentTime().msecsSinceStartOfDay()
            dt = current_time - self.mouse_press_time
            dist = (event.position() - self.mouse_press_pos).manhattanLength()

            if dt < 500 and dist < 10:
                super().mouseReleaseEvent(event)
            else:
                self.context.MoveTo(-1, -1, self.view, True)
                super().mouseReleaseEvent(event)

            self.is_interacting_with_cube = False
            self.mouse_press_pos = None
            return

        # restore holding cursor so cursor can update
        self.unsetCursor()
        QApplication.restoreOverrideCursor()
        self.releaseMouse()
        super().mouseReleaseEvent(event)
