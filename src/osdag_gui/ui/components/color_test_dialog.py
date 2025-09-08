import sys
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QComboBox, QSlider, QSpinBox, 
                               QGroupBox, QGridLayout, QCheckBox, QFrame,
                               QScrollArea, QWidget, QSplitter)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor, QPalette

# Import OpenCASCADE color constants
from OCC.Core.Quantity import (
    Quantity_NOC_WHITE, Quantity_NOC_BLACK, Quantity_NOC_BLUE1, Quantity_NOC_BLUE4,
    Quantity_NOC_CYAN1, Quantity_NOC_RED, Quantity_NOC_GREEN, Quantity_NOC_ORANGE,
    Quantity_NOC_YELLOW, Quantity_NOC_SADDLEBROWN, Quantity_NOC_GRAY, Quantity_NOC_GRAY25,
    Quantity_NOC_BLUE2, Quantity_NOC_BLUE3, Quantity_NOC_RED1, Quantity_NOC_RED2,
    Quantity_NOC_RED3, Quantity_NOC_RED4, Quantity_NOC_GREEN1, Quantity_NOC_GREEN2,
    Quantity_NOC_GREEN3, Quantity_NOC_GREEN4, Quantity_NOC_YELLOW1, Quantity_NOC_YELLOW2,
    Quantity_NOC_YELLOW3, Quantity_NOC_YELLOW4, Quantity_NOC_GRAY1, Quantity_NOC_GRAY2,
    Quantity_NOC_GRAY3, Quantity_NOC_GRAY4, Quantity_NOC_GRAY5, Quantity_NOC_GRAY6,
    Quantity_NOC_GRAY7, Quantity_NOC_GRAY8, Quantity_NOC_GRAY9, Quantity_NOC_MAGENTA1,
    Quantity_NOC_MAGENTA2, Quantity_NOC_MAGENTA3, Quantity_NOC_MAGENTA4, Quantity_NOC_VIOLET,
    Quantity_NOC_ORANGE1, Quantity_NOC_ORANGE2, Quantity_NOC_ORANGE3, Quantity_NOC_ORANGE4,
    Quantity_NOC_PINK1, Quantity_NOC_PINK2, Quantity_NOC_PINK3, Quantity_NOC_PINK4,
    Quantity_NOC_BROWN1, Quantity_NOC_BROWN2, Quantity_NOC_BROWN3, Quantity_NOC_BROWN4,
    Quantity_NOC_GOLD, Quantity_NOC_SILVER, Quantity_NOC_COPPER, Quantity_NOC_BRONZE,
    Quantity_NOC_TURQUOISE, Quantity_NOC_CORAL, Quantity_NOC_SALMON, Quantity_NOC_KHAKI,
    Quantity_NOC_OLIVE, Quantity_NOC_LIME, Quantity_NOC_AQUA, Quantity_NOC_NAVY,
    Quantity_NOC_MAROON, Quantity_NOC_TEAL, Quantity_Color, Quantity_TOC_RGB
)

from OCC.Core.Graphic3d import (
    Graphic3d_NOM_ALUMINIUM, Graphic3d_NOM_STEEL, Graphic3d_NOM_BRASS,
    Graphic3d_NOM_BRONZE, Graphic3d_NOM_COPPER, Graphic3d_NOM_GOLD,
    Graphic3d_NOM_PEWTER, Graphic3d_NOM_PLASTER, Graphic3d_NOM_PLASTIC,
    Graphic3d_NOM_RUBBER, Graphic3d_NOM_SILVER, Graphic3d_NOM_STONE
)


class ColorPreviewWidget(QFrame):
    """Widget to preview color with a colored rectangle"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(2)
        self.setStyleSheet("background-color: white; border: 2px solid black;")
        
    def set_color(self, color):
        """Set the preview color"""
        if isinstance(color, str):
            self.setStyleSheet(f"background-color: {color}; border: 2px solid black;")
        else:
            # Convert Quantity_NOC to RGB
            rgb = self.quantity_color_to_rgb(color)
            self.setStyleSheet(f"background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]}); border: 2px solid black;")
    
    def quantity_color_to_rgb(self, quantity_color):
        """Convert Quantity_NOC to RGB tuple"""
        try:
            color = Quantity_Color(quantity_color)
            r = int(color.Red() * 255)
            g = int(color.Green() * 255)
            b = int(color.Blue() * 255)
            return (r, g, b)
        except:
            return (255, 255, 255)  # Default to white


class ComponentColorControl(QGroupBox):
    """Control group for a single component type"""
    
    colorChanged = Signal(str, object, object, float)  # component_name, color, material, transparency
    
    def __init__(self, component_name, parent=None):
        super().__init__(component_name, parent)
        self.component_name = component_name
        self.current_color = Quantity_NOC_BLUE1
        self.current_material = None
        self.current_transparency = 0.0
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QGridLayout(self)
        
        # Color selection
        layout.addWidget(QLabel("Color:"), 0, 0)
        self.color_combo = QComboBox()
        self.populate_color_combo()
        self.color_combo.currentTextChanged.connect(self.on_color_changed)
        layout.addWidget(self.color_combo, 0, 1)
        
        # Color preview
        self.color_preview = ColorPreviewWidget()
        layout.addWidget(self.color_preview, 0, 2)
        
        # Material selection
        layout.addWidget(QLabel("Material:"), 1, 0)
        self.material_combo = QComboBox()
        self.populate_material_combo()
        self.material_combo.currentTextChanged.connect(self.on_material_changed)
        layout.addWidget(self.material_combo, 1, 1)
        
        # Transparency slider
        layout.addWidget(QLabel("Transparency:"), 2, 0)
        self.transparency_slider = QSlider(Qt.Horizontal)
        self.transparency_slider.setRange(0, 100)
        self.transparency_slider.setValue(0)
        self.transparency_slider.valueChanged.connect(self.on_transparency_changed)
        layout.addWidget(self.transparency_slider, 2, 1)
        
        self.transparency_label = QLabel("0%")
        layout.addWidget(self.transparency_label, 2, 2)
        
        # Enable/Disable checkbox
        self.enable_checkbox = QCheckBox("Enable")
        self.enable_checkbox.setChecked(True)
        self.enable_checkbox.toggled.connect(self.on_enable_toggled)
        layout.addWidget(self.enable_checkbox, 3, 0, 1, 3)
        
        # Set initial color preview
        self.update_color_preview()
        
    def populate_color_combo(self):
        """Populate color combo box with available colors"""
        colors = [
            ("Default Steel", None),
            ("White", Quantity_NOC_WHITE),
            ("Black", Quantity_NOC_BLACK),
            ("Blue1 (Light)", Quantity_NOC_BLUE1),
            ("Blue2", Quantity_NOC_BLUE2),
            ("Blue3", Quantity_NOC_BLUE3),
            ("Blue4 (Dark)", Quantity_NOC_BLUE4),
            ("Cyan1", Quantity_NOC_CYAN1),
            ("Red", Quantity_NOC_RED),
            ("Red1 (Light)", Quantity_NOC_RED1),
            ("Red2", Quantity_NOC_RED2),
            ("Red3", Quantity_NOC_RED3),
            ("Red4 (Dark)", Quantity_NOC_RED4),
            ("Green", Quantity_NOC_GREEN),
            ("Green1 (Light)", Quantity_NOC_GREEN1),
            ("Green2", Quantity_NOC_GREEN2),
            ("Green3", Quantity_NOC_GREEN3),
            ("Green4 (Dark)", Quantity_NOC_GREEN4),
            ("Orange", Quantity_NOC_ORANGE),
            ("Orange1 (Light)", Quantity_NOC_ORANGE1),
            ("Orange2", Quantity_NOC_ORANGE2),
            ("Orange3", Quantity_NOC_ORANGE3),
            ("Orange4 (Dark)", Quantity_NOC_ORANGE4),
            ("Yellow", Quantity_NOC_YELLOW),
            ("Yellow1 (Light)", Quantity_NOC_YELLOW1),
            ("Yellow2", Quantity_NOC_YELLOW2),
            ("Yellow3", Quantity_NOC_YELLOW3),
            ("Yellow4 (Dark)", Quantity_NOC_YELLOW4),
            ("Saddle Brown", Quantity_NOC_SADDLEBROWN),
            ("Brown1 (Light)", Quantity_NOC_BROWN1),
            ("Brown2", Quantity_NOC_BROWN2),
            ("Brown3", Quantity_NOC_BROWN3),
            ("Brown4 (Dark)", Quantity_NOC_BROWN4),
            ("Gray", Quantity_NOC_GRAY),
            ("Gray1 (Light)", Quantity_NOC_GRAY1),
            ("Gray2", Quantity_NOC_GRAY2),
            ("Gray3", Quantity_NOC_GRAY3),
            ("Gray4", Quantity_NOC_GRAY4),
            ("Gray5", Quantity_NOC_GRAY5),
            ("Gray6", Quantity_NOC_GRAY6),
            ("Gray7", Quantity_NOC_GRAY7),
            ("Gray8", Quantity_NOC_GRAY8),
            ("Gray9 (Dark)", Quantity_NOC_GRAY9),
            ("Gray25", Quantity_NOC_GRAY25),
            ("Magenta1 (Light)", Quantity_NOC_MAGENTA1),
            ("Magenta2", Quantity_NOC_MAGENTA2),
            ("Magenta3", Quantity_NOC_MAGENTA3),
            ("Magenta4 (Dark)", Quantity_NOC_MAGENTA4),
            ("Violet", Quantity_NOC_VIOLET),
            ("Pink1 (Light)", Quantity_NOC_PINK1),
            ("Pink2", Quantity_NOC_PINK2),
            ("Pink3", Quantity_NOC_PINK3),
            ("Pink4 (Dark)", Quantity_NOC_PINK4),
            ("Gold", Quantity_NOC_GOLD),
            ("Silver", Quantity_NOC_SILVER),
            ("Copper", Quantity_NOC_COPPER),
            ("Bronze", Quantity_NOC_BRONZE),
            ("Turquoise", Quantity_NOC_TURQUOISE),
            ("Coral", Quantity_NOC_CORAL),
            ("Salmon", Quantity_NOC_SALMON),
            ("Khaki", Quantity_NOC_KHAKI),
            ("Olive", Quantity_NOC_OLIVE),
            ("Lime", Quantity_NOC_LIME),
            ("Aqua", Quantity_NOC_AQUA),
            ("Navy", Quantity_NOC_NAVY),
            ("Maroon", Quantity_NOC_MAROON),
            ("Teal", Quantity_NOC_TEAL),
        ]
        
        for name, color_const in colors:
            self.color_combo.addItem(name, color_const)
    
    def populate_material_combo(self):
        """Populate material combo box"""
        materials = [
            ("None", None),
            ("Aluminum", Graphic3d_NOM_ALUMINIUM),
            ("Steel", Graphic3d_NOM_STEEL),
            ("Brass", Graphic3d_NOM_BRASS),
            ("Bronze", Graphic3d_NOM_BRONZE),
            ("Copper", Graphic3d_NOM_COPPER),
            ("Gold", Graphic3d_NOM_GOLD),
            ("Pewter", Graphic3d_NOM_PEWTER),
            ("Plaster", Graphic3d_NOM_PLASTER),
            ("Plastic", Graphic3d_NOM_PLASTIC),
            ("Rubber", Graphic3d_NOM_RUBBER),
            ("Silver", Graphic3d_NOM_SILVER),
            ("Stone", Graphic3d_NOM_STONE),
        ]
        
        for name, material_const in materials:
            self.material_combo.addItem(name, material_const)
    
    def on_color_changed(self, text):
        """Handle color selection change"""
        color_const = self.color_combo.currentData()
        self.current_color = color_const
        self.update_color_preview()
        self.emit_color_changed()
    
    def on_material_changed(self, text):
        """Handle material selection change"""
        material_const = self.material_combo.currentData()
        self.current_material = material_const
        self.emit_color_changed()
    
    def on_transparency_changed(self, value):
        """Handle transparency slider change"""
        self.current_transparency = value / 100.0
        self.transparency_label.setText(f"{value}%")
        self.emit_color_changed()
    
    def on_enable_toggled(self, checked):
        """Handle enable/disable toggle"""
        self.setEnabled(checked)
        if not checked:
            # Emit with None values to disable component
            self.colorChanged.emit(self.component_name, None, None, 0.0)
        else:
            self.emit_color_changed()
    
    def update_color_preview(self):
        """Update the color preview widget"""
        if self.current_color:
            self.color_preview.set_color(self.current_color)
        else:
            self.color_preview.set_color("lightgray")
    
    def emit_color_changed(self):
        """Emit color change signal"""
        if self.enable_checkbox.isChecked():
            self.colorChanged.emit(self.component_name, self.current_color, 
                                 self.current_material, self.current_transparency)


class ColorTestDialog(QDialog):
    """Main dialog for real-time color testing"""
    
    def __init__(self, display_widget=None, parent=None):
        super().__init__(parent)
        self.display_widget = display_widget
        self.component_controls = {}
        
        self.setWindowTitle("3D Component Color Tester")
        self.setModal(False)
        self.resize(800, 600)
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup the main UI"""
        main_layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Real-time 3D Component Color Testing")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create scroll area for component controls
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Component control groups
        components = [
            "Column",
            "Beam", 
            "Plate",
            "Weld",
            "Bolt",
            "Nut",
            "Angle",
            "Concrete",
            "Grout",
            "Custom1",
            "Custom2"
        ]
        
        for component in components:
            control = ComponentColorControl(component)
            control.colorChanged.connect(self.on_component_color_changed)
            self.component_controls[component] = control
            scroll_layout.addWidget(control)
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.apply_button = QPushButton("Apply Colors")
        self.apply_button.setStyleSheet("""
            QPushButton {
                background-color: #90AF13;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7a9a0f;
            }
            QPushButton:pressed {
                background-color: #5a7a0a;
            }
        """)
        
        self.reset_button = QPushButton("Reset to Defaults")
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #495057;
            }
        """)
        
        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        
        main_layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Ready to test colors")
        self.status_label.setStyleSheet("color: #6c757d; font-style: italic; margin: 5px;")
        main_layout.addWidget(self.status_label)
        
    def setup_connections(self):
        """Setup signal connections"""
        self.apply_button.clicked.connect(self.apply_all_colors)
        self.reset_button.clicked.connect(self.reset_to_defaults)
        self.close_button.clicked.connect(self.accept)
        
    def on_component_color_changed(self, component_name, color, material, transparency):
        """Handle component color change"""
        self.status_label.setText(f"Updated {component_name}: Color={color}, Material={material}, Transparency={transparency:.2f}")
        
        # Auto-apply if display widget is available
        if self.display_widget:
            self.apply_single_component(component_name, color, material, transparency)
    
    def apply_single_component(self, component_name, color, material, transparency):
        """Apply color to a single component"""
        if not self.display_widget:
            return
            
        try:
            # This would need to be implemented based on your specific display system
            # For now, just update the status
            self.status_label.setText(f"Applied {component_name} color changes")
        except Exception as e:
            self.status_label.setText(f"Error applying {component_name}: {str(e)}")
    
    def apply_all_colors(self):
        """Apply all color settings"""
        if not self.display_widget:
            self.status_label.setText("No display widget available")
            return
            
        try:
            applied_count = 0
            for component_name, control in self.component_controls.items():
                if control.enable_checkbox.isChecked():
                    self.apply_single_component(
                        component_name,
                        control.current_color,
                        control.current_material,
                        control.current_transparency
                    )
                    applied_count += 1
            
            self.status_label.setText(f"Applied colors to {applied_count} components")
        except Exception as e:
            self.status_label.setText(f"Error applying colors: {str(e)}")
    
    def reset_to_defaults(self):
        """Reset all controls to default values"""
        defaults = {
            "Column": (None, None, 0.0),  # Default steel
            "Beam": (None, Graphic3d_NOM_ALUMINIUM, 0.0),  # Aluminum material
            "Plate": (Quantity_NOC_BLUE1, None, 0.0),  # Blue plates
            "Weld": (Quantity_NOC_RED, None, 0.0),  # Red welds
            "Bolt": (Quantity_NOC_SADDLEBROWN, None, 0.0),  # Brown bolts
            "Nut": (Quantity_NOC_SADDLEBROWN, None, 0.0),  # Brown nuts
            "Angle": (Quantity_NOC_BLUE1, None, 0.0),  # Blue angles
            "Concrete": (Quantity_NOC_GRAY25, None, 0.5),  # Gray concrete with transparency
            "Grout": (Quantity_NOC_GRAY25, None, 0.5),  # Gray grout with transparency
            "Custom1": (Quantity_NOC_GREEN, None, 0.0),  # Green custom
            "Custom2": (Quantity_NOC_ORANGE, None, 0.0),  # Orange custom
        }
        
        for component_name, control in self.component_controls.items():
            if component_name in defaults:
                color, material, transparency = defaults[component_name]
                
                # Set color
                if color:
                    for i in range(control.color_combo.count()):
                        if control.color_combo.itemData(i) == color:
                            control.color_combo.setCurrentIndex(i)
                            break
                else:
                    control.color_combo.setCurrentIndex(0)  # Default steel
                
                # Set material
                if material:
                    for i in range(control.material_combo.count()):
                        if control.material_combo.itemData(i) == material:
                            control.material_combo.setCurrentIndex(i)
                            break
                else:
                    control.material_combo.setCurrentIndex(0)  # None
                
                # Set transparency
                control.transparency_slider.setValue(int(transparency * 100))
                
                # Enable component
                control.enable_checkbox.setChecked(True)
        
        self.status_label.setText("Reset to default colors")
    
    def get_color_settings(self):
        """Get current color settings as dictionary"""
        settings = {}
        for component_name, control in self.component_controls.items():
            if control.enable_checkbox.isChecked():
                settings[component_name] = {
                    'color': control.current_color,
                    'material': control.current_material,
                    'transparency': control.current_transparency
                }
        return settings
    
    def set_display_widget(self, display_widget):
        """Set the display widget for applying colors"""
        self.display_widget = display_widget


# Demo function to test the dialog
def demo_color_test_dialog():
    """Demo function to show the color test dialog"""
    from PySide6.QtWidgets import QApplication
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    dialog = ColorTestDialog()
    dialog.show()
    
    if app:
        app.exec()


if __name__ == "__main__":
    demo_color_test_dialog()
