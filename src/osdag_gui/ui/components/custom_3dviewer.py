"""
Custom 3D CAD Viewer that has an extra functionality of Hover over Label on Models.
This is custom class is created to implement parent 'qtViewer3d' class and add extra functionality of mouse event. 
"""
from PySide6.QtCore import QTimer, QTime
from PySide6.QtWidgets import QToolTip

from osdag_gui.__config__ import CAD_BACKEND

from OCC.Display import backend
backend.load_backend(CAD_BACKEND)

from OCC.Display.qtDisplay import qtViewer3d
from OCC.Core.AIS import AIS_ViewCube
from OCC.Core.Prs3d import Prs3d_DatumAspect, Prs3d_Drawer
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_WHITE, Quantity_NOC_GRAY50, Quantity_NOC_BLACK, Quantity_NOC_CYAN
from OCC.Core.Aspect import Aspect_TOL_SOLID, Aspect_GDM_Lines, Aspect_GT_Rectangular
from OCC.Core.V3d import V3d_Zpos

class CustomViewer3d(qtViewer3d):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.context = None  # Will be set externally
        self.view = None     # Will be set externally
        self.model_ais_objects = {}  # Dictionary to map AIS objects to model names
        self.model_hover_labels = {}  # Dictionary to map model names to tooltip text
        self.current_hovered_model = None
        self.current_highlighted_ais = None  # Track currently highlighted object
        self.current_highlighted_owner = None  # Track currently highlighted owner (for View Cube parts)
        self.hover_timer = QTimer(self)
        self.hover_timer.setSingleShot(True)
        self.hover_timer.timeout.connect(self.show_tooltip)
        self.hover_position = None
        
        # View Cube Interaction State
        self.is_interacting_with_cube = False
        self.mouse_press_pos = None
        self.mouse_press_time = 0
        self.view_cube_active = False

    def mouseMoveEvent(self, event):
        if not self.context or not self.view:
            super().mouseMoveEvent(event)
            return

        # If we are dragging the view cube (or anything else), let the parent handle rotation
        if self.is_interacting_with_cube:
            super().mouseMoveEvent(event)
            return

        try:
            # Get device pixel ratio for high-DPI adjustment
            pixel_ratio = self.devicePixelRatioF()

            # Convert coordinates to integers with high-DPI scaling
            x = int(event.position().x() * pixel_ratio)
            y = int(event.position().y() * pixel_ratio)

            # Call OCC picking system with adjusted coordinates
            self.context.MoveTo(x, y, self.view, True)

            # Check if something is detected
            hovered_model = None
            if self.context.HasDetected():
                detected = self.context.DetectedInteractive()
                
                # --- VIEW CUBE HIGHLIGHTING LOGIC ---
                if hasattr(self, 'view_cube') and detected == self.view_cube:
                    # Enable Auto Hilight for View Cube to handle part highlighting
                    if not self.view_cube_active:
                        self.context.SetAutomaticHilight(True)
                        self.view_cube_active = True
                        # Re-detect to apply auto-highlight
                        self.context.MoveTo(x, y, self.view, True)
                    
                    # Ensure we redraw to show the highlight
                    self.view.Redraw()
                
                # --- STANDARD MODEL HIGHLIGHTING LOGIC ---
                else:
                    # If we left View Cube, disable Auto Hilight and cleanup
                    if self.view_cube_active:
                        self.context.SetAutomaticHilight(False)
                        self.view_cube_active = False
                        try:
                            self.context.Unhilight(self.view_cube, True)
                        except:
                            pass
                        # Re-detect to update state
                        self.context.MoveTo(x, y, self.view, True)
                        # Update detected after re-move
                        if self.context.HasDetected():
                            detected = self.context.DetectedInteractive()
                        else:
                            detected = None

                    if detected and detected != self.current_highlighted_ais:
                        if self.current_highlighted_ais:
                            self.context.Unhilight(self.current_highlighted_ais, False)
                        
                        self.current_highlighted_ais = detected
                        self.context.HilightWithColor(self.current_highlighted_ais, self.context.HighlightStyle(), False)
                        self.view.Redraw()

                    # Handle Tooltip identification
                    if self.model_ais_objects and detected:
                        for model_name, ais_list in self.model_ais_objects.items():
                            for ais_object in ais_list:
                                try:
                                    if hasattr(detected, 'GetHandle') and hasattr(ais_object, 'GetHandle'):
                                        if detected.GetHandle() == ais_object.GetHandle():
                                            hovered_model = model_name
                                            break
                                    elif detected == ais_object:
                                        hovered_model = model_name
                                        break
                                except:
                                    continue
            else:
                # Unhighlight everything if nothing is detected
                if self.view_cube_active:
                    self.context.SetAutomaticHilight(False)
                    self.view_cube_active = False
                    try:
                        self.context.Unhilight(self.view_cube, True)
                    except:
                        pass
                    self.view.Redraw()

                if self.current_highlighted_owner:
                    # This shouldn't be needed anymore but keeping for safety
                    self.current_highlighted_owner = None
                    
                if self.current_highlighted_ais:
                    self.context.Unhilight(self.current_highlighted_ais, False)
                    self.current_highlighted_ais = None
                    self.view.Redraw()

            self.hover_position = event.globalPosition().toPoint()
            if hovered_model != self.current_hovered_model:
                self.current_hovered_model = hovered_model
                self.hover_timer.start(100)
            elif hovered_model is None:
                QToolTip.hideText()

        except Exception as e:
            print(f"Error in mouseMoveEvent: {e}")
            QToolTip.hideText()

        # Call parent class's mouseMoveEvent to maintain default behavior
        super().mouseMoveEvent(event)

    def show_tooltip(self):
        if self.current_hovered_model and self.current_hovered_model in self.model_hover_labels and self.hover_position:
            QToolTip.showText(
                self.hover_position,
                self.model_hover_labels[self.current_hovered_model],
                self
            )

    def leaveEvent(self, event):
        self.hover_timer.stop()
        self.current_hovered_model = None
        
        # Reset View Cube state if leaving
        if self.view_cube_active:
            self.context.SetAutomaticHilight(False)
            self.view_cube_active = False
            try:
                if hasattr(self, 'view_cube') and self.view_cube:
                    self.context.Unhilight(self.view_cube, True)
            except:
                pass
            self.view.Redraw()
            
        # Also unhighlight when leaving
        if self.current_highlighted_owner:
            try:
                self.context.Unhilight(self.current_highlighted_owner, False)
                self.current_highlighted_owner = None
            except:
                pass
        
        if self.current_highlighted_ais:
            try:
                self.context.Unhilight(self.current_highlighted_ais, False)
                self.current_highlighted_ais = None
                self.view.Redraw()
            except:
                pass
        QToolTip.hideText()
        super().leaveEvent(event)

    def display_view_cube(self):
        try:
            # Remove existing view cube if it exists
            if hasattr(self, 'view_cube') and self.view_cube:
                self.context.Remove(self.view_cube, False)
                self.view_cube = None

            self.view_cube = AIS_ViewCube()
            self.view_cube.SetSize(55)
            self.view_cube.SetFontHeight(12)
            self.view_cube.SetAxesLabels("", "", "")
            self.view_cube.SetDrawAxes(False)
            
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
            
            # Position the View Cube to the left of the 9 view buttons
            try:
                from OCC.Core.Graphic3d import Graphic3d_TransformPers, Graphic3d_TMF_TriedronPers, Graphic3d_Vec2i
                from OCC.Core.Aspect import Aspect_TOTP_RIGHT_UPPER
                
                # Create transform persistence anchored to top-right corner
                offset = Graphic3d_Vec2i(70, 80)
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

    def mousePressEvent(self, event):
        if not self.context or not self.view:
            super().mousePressEvent(event)
            return

        try:
            # Get device pixel ratio for high-DPI adjustment
            pixel_ratio = self.devicePixelRatioF()
            x = int(event.position().x() * pixel_ratio)
            y = int(event.position().y() * pixel_ratio)

            self.context.MoveTo(x, y, self.view, True)
            
            if self.context.HasDetected():
                detected = self.context.DetectedInteractive()
                if hasattr(self, 'view_cube') and detected == self.view_cube:
                    # View Cube pressed
                    self.is_interacting_with_cube = True
                    self.mouse_press_pos = event.position()
                    self.mouse_press_time = QTime.currentTime().msecsSinceStartOfDay()
                    
                    # Don't return here! Pass to parent to allow rotation (drag) to start
                    pass
        except Exception as e:
            print(f"Error in mousePressEvent: {e}")

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.is_interacting_with_cube:
            try:
                current_time = QTime.currentTime().msecsSinceStartOfDay()
                time_diff = current_time - self.mouse_press_time
                
                # Calculate distance moved
                current_pos = event.position()
                dist = (current_pos - self.mouse_press_pos).manhattanLength()
                
                # Thresholds for a "click": < 500ms and < 10 pixels movement
                if time_diff < 500 and dist < 10:
                    # It's a click! 
                    # Let the default behavior handle it (which aligns to the clicked face)
                    super().mouseReleaseEvent(event)
                    return
                else:
                    # It's a drag!
                    # We want to prevent the "snap back" (default selection) behavior.
                    # Hack: Move context to nowhere so nothing is detected when we call super()
                    # This prevents the AIS_ViewCube from processing a "Select" action
                    self.context.MoveTo(-1, -1, self.view, True)
                    super().mouseReleaseEvent(event)
                    return
                
            except Exception as e:
                print(f"Error in mouseReleaseEvent: {e}")
            finally:
                self.is_interacting_with_cube = False
                self.mouse_press_pos = None

        super().mouseReleaseEvent(event)
