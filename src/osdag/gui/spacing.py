import sys
import ezdxf
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, QGraphicsView,
                             QGraphicsScene, QCheckBox, QFileDialog)
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF
import tempfile
import os

from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf import recover
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import matplotlib.pyplot as plt

ezdxf.addons.drawing.properties.MODEL_SPACE_BG_COLOR = "#FFFFFF"

class BoltPatternGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.display = None
        
    def initUI(self):
        self.setWindowTitle('Bolt Pattern Generator')
        self.setGeometry(100, 100, 800, 500)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left panel for inputs
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Input fields
        self.inputs = {}
        
        # Pitch Distance
        pitch_layout = QHBoxLayout()
        pitch_label = QLabel('Pitch Distance (mm)')
        self.inputs['pitch'] = QLineEdit('65')
        pitch_layout.addWidget(pitch_label)
        pitch_layout.addWidget(self.inputs['pitch'])
        left_layout.addLayout(pitch_layout)
        
        # End Distance
        end_layout = QHBoxLayout()
        end_label = QLabel('End Distance (mm)')
        self.inputs['end'] = QLineEdit('15')
        end_layout.addWidget(end_label)
        end_layout.addWidget(self.inputs['end'])
        left_layout.addLayout(end_layout)
        
        # Gauge Distance 1
        gauge1_layout = QHBoxLayout()
        gauge1_label = QLabel('Gauge Distance 1 (mm)')
        self.inputs['gauge1'] = QLineEdit('25.0')
        gauge1_layout.addWidget(gauge1_label)
        gauge1_layout.addWidget(self.inputs['gauge1'])
        left_layout.addLayout(gauge1_layout)
        
        # Gauge Distance 2
        gauge2_layout = QHBoxLayout()
        gauge2_label = QLabel('Gauge Distance 2 (mm)')
        self.inputs['gauge2'] = QLineEdit('20.0')
        gauge2_layout.addWidget(gauge2_label)
        gauge2_layout.addWidget(self.inputs['gauge2'])
        left_layout.addLayout(gauge2_layout)
        
        # Edge Distance
        edge_layout = QHBoxLayout()
        edge_label = QLabel('Edge Distance (mm)')
        self.inputs['edge'] = QLineEdit('25.0')
        edge_layout.addWidget(edge_label)
        edge_layout.addWidget(self.inputs['edge'])
        left_layout.addLayout(edge_layout)
        
        # Hole Diameter (additional parameter)
        hole_layout = QHBoxLayout()
        hole_label = QLabel('Hole Diameter (mm)')
        self.inputs['hole'] = QLineEdit('10.0')
        hole_layout.addWidget(hole_label)
        hole_layout.addWidget(self.inputs['hole'])
        left_layout.addLayout(hole_layout)

        
        # Update button
        update_button = QPushButton('Update Drawing')
        update_button.clicked.connect(self.update_drawing)
        left_layout.addWidget(update_button)
        
        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        
        # Right panel for the drawing
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        right_layout.addWidget(self.view)
        right_panel.setLayout(right_layout)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 3)
        
        # Set main widget
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Initial drawing
        self.update_drawing()
    
    def get_parameters(self):
        params = {}
        for key, widget in self.inputs.items():
            try:
                value = float(widget.text())
                # Ensure positive values for critical parameters
                if key in ['pitch', 'end', 'gauge1', 'gauge2', 'edge', 'hole', 'thickness'] and value <= 0:
                    value = 1.0  # Default to a small positive value
                params[key] = value
            except ValueError:
                params[key] = 1.0  # Default value if conversion fails
        return params
    
    def update_drawing(self):
        params = self.get_parameters()
        
        # Create a new DXF document
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        
        # Get parameters
        pitch = params['pitch']
        end = params['end']
        gauge1 = params['gauge1']
        gauge2 = params['gauge2']
        edge = params['edge']
        hole_diameter = params['hole']
        
        # Calculate dimensions
        width = gauge1 + gauge2 + edge
        height = 2 * end + 2 * pitch
        
        # Draw the rectangle
        msp.add_lwpolyline([(0, 0), (width, 0), (width, height), (0, height), (0, 0)], close=True)
        
        # Draw the holes
        # Top row
        msp.add_circle((gauge1, end), hole_diameter/2)
        msp.add_circle((gauge1 + gauge2, end), hole_diameter/2)
        
        # Middle row
        msp.add_circle((gauge1, end + pitch), hole_diameter/2)
        msp.add_circle((gauge1 + gauge2, end + pitch), hole_diameter/2)
        
        # Bottom row
        msp.add_circle((gauge1, end + 2 * pitch), hole_diameter/2)
        msp.add_circle((gauge1 + gauge2, end + 2 * pitch), hole_diameter/2)
        
        # Add dimensions
        self.add_dimensions_to_dxf(msp, params)
        
        # Save to a temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.dxf', delete=False)
        temp_file.close()
        doc.saveas(temp_file.name)
        
        # Safe loading procedure
        try:
            doc, auditor = recover.readfile(temp_file.name)
        except IOError:
            print(f'Not a DXF file or a generic I/O error with temporary file {temp_file.name}.')
            os.unlink(temp_file.name)
            return
        except ezdxf.DXFStructureError:
            print(f'Invalid or corrupted DXF file {temp_file.name}.')
            os.unlink(temp_file.name)
            return

        # Check for severe errors
        if not auditor.has_errors:
            # Convert to raster image
            try:
                fig = plt.figure(figsize=(10, 8))
                ax = fig.add_axes([0, 0, 1, 1])
                # Create drawing from DXF document
                ctx = RenderContext(doc)
                ctx.set_current_layout(msp)
                out = MatplotlibBackend(ax)
                Frontend(ctx, out).draw_layout(doc.modelspace(), finalize=True)
                
                # Adjust limits to focus on the drawing
                ax.set_xlim(-60, width + 80)
                ax.set_ylim(-60, height + 20)
                
                # Save to temporary image file
                temp_img = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                temp_img.close()
                fig.savefig(temp_img.name, dpi=300)
                plt.close(fig)
                
                # Display in Qt
                pixmap = QPixmap(temp_img.name)
                self.scene.clear()
                self.scene.addPixmap(pixmap)
                self.view.fitInView(QRectF(pixmap.rect()), Qt.KeepAspectRatio)
                
                # Remove temporary files
                os.unlink(temp_img.name)
                os.unlink(temp_file.name)
                
            except ImportError:
                print("Matplotlib or ezdxf.addons.drawing not available for rendering")
        else:
            print(f"Severe errors detected in DXF file: {auditor.errors}")
            os.unlink(temp_file.name)

    def add_dimensions_to_dxf(self, msp, params):
        # Extract parameters
        pitch = params['pitch']
        end = params['end']
        gauge1 = params['gauge1']
        gauge2 = params['gauge2']
        edge = params['edge']
        
        # Calculate dimensions
        width = gauge1 + gauge2 + edge
        height = 2 * end + 2 * pitch
        
        # Create dimension style override
        dim_style = {
            'dimtsz': 0,       # Set tick size to 0 to enable arrows
            'dimasz': 2.5,      # Arrow size
            'dimblk': 'OPEN30', # Correct arrow block name (no underscore)
            'dimtxt': 5.0,      # Text height
            'dimgap': 1.0       # Gap between dimension line and text
        }
        
        # Pitch dimension (vertical)
        pitch_dim = msp.add_linear_dim(
            base=(width + 20, end + pitch/2),
            p1=(width + 10, end + pitch),
            p2=(width + 10, end),
            angle=90,
            dimstyle='STANDARD',
            override=dim_style
        )
        pitch_dim.render()
        
        # End dimension (vertical)
        end_dim = msp.add_linear_dim(
            base=(width + 20, end/2),
            p1=(width + 10, 0),
            p2=(width + 10, end),
            angle=90,
            dimstyle='STANDARD',
            override=dim_style
        )
        end_dim.render()
        
        # Gauge1 dimension (horizontal)
        gauge1_dim = msp.add_linear_dim(
            base=(gauge1/2, -20),
            p1=(0, -10),
            p2=(gauge1, -10),
            angle=0,
            dimstyle='STANDARD',
            override=dim_style
        )
        gauge1_dim.render()
        
        # Gauge2 dimension (horizontal)
        gauge2_dim = msp.add_linear_dim(
            base=(gauge1 + gauge2/2, -20),
            p1=(gauge1, -10),
            p2=(gauge1 + gauge2, -10),
            angle=0,
            dimstyle='STANDARD',
            override=dim_style
        )
        gauge2_dim.render()
        
        # Edge dimension (horizontal)
        edge_dim = msp.add_linear_dim(
            base=(gauge1 + gauge2 + edge/2, -20),
            p1=(gauge1 + gauge2, -10),
            p2=(width, -10),
            angle=0,
            dimstyle='STANDARD',
            override=dim_style
        )
        edge_dim.render()
        
        # You can remove the separate text entities if you want the dimension to display its measurement automatically


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BoltPatternGenerator()
    window.show()
    sys.exit(app.exec_())