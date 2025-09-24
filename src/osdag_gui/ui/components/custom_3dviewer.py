from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QToolTip

from osdag_gui.__config__ import CAD_BACKEND

from OCC.Display import backend
backend.load_backend(CAD_BACKEND)

from OCC.Display.qtDisplay import qtViewer3d

class CustomViewer3d(qtViewer3d):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.context = None  # Will be set externally
        self.view = None     # Will be set externally
        self.model_ais_objects = {}  # Dictionary to map AIS objects to model names
        self.model_hover_labels = {}  # Dictionary to map model names to tooltip text
        self.current_hovered_model = None
        self.hover_timer = QTimer(self)
        self.hover_timer.setSingleShot(True)
        self.hover_timer.timeout.connect(self.show_tooltip)
        self.hover_position = None

    def mouseMoveEvent(self, event):
        if not self.context or not self.view or not self.model_ais_objects:
            QToolTip.hideText()
            return

        try:
            # Get device pixel ratio for high-DPI adjustment
            pixel_ratio = self.devicePixelRatioF()

            # Convert coordinates to integers with high-DPI scaling
            x = int(event.position().x() * pixel_ratio)
            y = int(event.position().y() * pixel_ratio)
            # print(f"Mouse position: ({x}, {y})")  # Debug output

            # Call OCC picking system with adjusted coordinates
            self.context.MoveTo(x, y, self.view, True)

            # Check if something is detected
            hovered_model = None
            if self.context.HasDetected():
                detected = self.context.DetectedInteractive()
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

            self.hover_position = event.globalPosition().toPoint()
            if hovered_model != self.current_hovered_model:
                self.current_hovered_model = hovered_model
                self.hover_timer.start(100)  # Reduced delay to 100ms for faster response
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
        QToolTip.hideText()
        super().leaveEvent(event)