from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QSize
from PyQt5.QtGui import QPainter, QColor, QCursor, QFont
from PyQt5.QtWidgets import QApplication, QDialog, QFrame, QGridLayout, QHBoxLayout, QLabel, QMessageBox, QPushButton, QScrollArea, QVBoxLayout, QWidget
from importlib.resources import files

class AnimatedToggle(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(60, 24)
        self.setCursor(Qt.PointingHandCursor)
        
        # Colors
        self._bg_color = QColor('#e0e0e0')  
        self._circle_color = QColor('#ffffff')  
        self._active_color = QColor('#4CAF50')  
        self._inactive_color = QColor('#e0e0e0')  
        self._circle_padding = 3
        
        # Animation
        self._circle_position = self._circle_padding
        self.animation = QPropertyAnimation(self, b'circle_position', self)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        self.animation.setDuration(200)  
        
        # Connect signal
        self.toggled.connect(self.start_animation)
    
    @QtCore.pyqtProperty(int)
    def circle_position(self):
        return self._circle_position
        
    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()
    
    def start_animation(self, checked):
        self.animation.stop()
        self.animation.setStartValue(self._circle_position)
        
        if checked:
            self.animation.setEndValue(self.width() - (self.height() - 2 * self._circle_padding) - self._circle_padding)
            self._bg_color = self._active_color
        else:
            self.animation.setEndValue(self._circle_padding)
            self._bg_color = self._inactive_color
        
        self.animation.start()
    
    def hitButton(self, pos):
        return True
    
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)
        
        shadow_rect = QRect(1, 1, self.width()-2, self.height()-2)
        p.setBrush(QColor(0, 0, 0, 30))
        p.drawRoundedRect(shadow_rect, 11, 11)
        
        rect = QRect(0, 0, self.width()-1, self.height()-1)
        p.setBrush(self._bg_color)
        p.drawRoundedRect(rect, 11, 11)
        
        circle_rect = QRect(
            self._circle_position,
            self._circle_padding,
            self.height() - 2 * self._circle_padding,
            self.height() - 2 * self._circle_padding
        )
        p.setBrush(self._circle_color)
        p.drawEllipse(circle_rect)
        
        p.end()

class Ui_PluginsDialog:
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 500)
        Dialog.setMinimumSize(QtCore.QSize(800, 400))
        
        # main layout
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        
        # status label
        self.status_label = QtWidgets.QLabel("Select plugins to manage")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(12)
        self.status_label.setFont(font)
        self.verticalLayout.addWidget(self.status_label)
        
        # scroll area 
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # grid layout for plugins with no spacing
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setSpacing(0)  
        self.gridLayout.setContentsMargins(5, 1, 5, 1)  
        self.gridLayout.setVerticalSpacing(0)  
        
        # column stretch factors
        self.gridLayout.setColumnStretch(0, 1)  # Name column
        self.gridLayout.setColumnStretch(1, 3)  # Details column (more space)
        self.gridLayout.setColumnStretch(2, 1)  # Buttons column
        
        # column minimum widths
        self.gridLayout.setColumnMinimumWidth(0, 120)  # Name column
        self.gridLayout.setColumnMinimumWidth(1, 300)  # Details column
        self.gridLayout.setColumnMinimumWidth(2, 100)  # Buttons column
        
        # header labels and thin header row
        header_row = QtWidgets.QFrame()
        header_row.setFrameShape(QFrame.StyledPanel)
        header_row.setFixedHeight(20)  
        header_row.setStyleSheet("""
            QFrame {
                background: #f5f5f5;
                border: none;
                border-bottom: 1px solid #e0e0e0;
                margin: 0;
                padding: 0;
                font-size: 9px;
                font-weight: bold;
                text-transform: uppercase;
                color: #666;
            }
        """)
        header_layout = QtWidgets.QHBoxLayout(header_row)
        header_layout.setContentsMargins(8, 0, 8, 0)  # Minimal vertical padding
        header_layout.setSpacing(5)  # Minimal spacing between items
        
        # Plugin Name header
        plugin_header = QtWidgets.QLabel("Plugin Name")
        plugin_header.setFixedWidth(100)  # Smaller width
        
        # Details header - centered
        details_header = QtWidgets.QLabel("Plugin Details")
        details_header.setAlignment(QtCore.Qt.AlignCenter)
        
        # Actions header - right aligned
        actions_header = QtWidgets.QLabel("Actions")
        actions_header.setFixedWidth(100)  # Fixed width for actions
        
        # widgets in header
        header_layout.addWidget(plugin_header)
        header_layout.addWidget(details_header, 1)  # Allow details to expand
        header_layout.addWidget(actions_header, 0, Qt.AlignRight)  # Align actions to right
        
        # header to grid with no extra spacing
        self.gridLayout.addWidget(header_row, 0, 0, 1, 3)
        self.gridLayout.setRowMinimumHeight(0, 20)  # Match fixed height
        
        # scroll area to layout
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        
        # window icon and title
        try:
            Dialog.setWindowIcon(QtGui.QIcon(str(files("osdag.data.ResourceFiles.images").joinpath("Osdag.png"))))
        except Exception:
            # Fallback if resource file can't be found
            pass
        Dialog.setWindowTitle("Osdag Plugin Manager")
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def clearPlugins(self):
        """Clear all plugins from the UI."""
        
        # total initial count
        total_items = self.gridLayout.count()
        print(f"Clearing UI - found {total_items} total items in grid layout")
        
        removed_count = 0
        while self.gridLayout.count() > 1:
            item = self.gridLayout.takeAt(1)  # Always takes the item at index 1
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    print(f"Removing widget at index 1")
                    widget.setParent(None)
                    widget.deleteLater()
                    removed_count += 1
                # If it's a layout instead of a widget
                elif item.layout() is not None:
                    self.deleteItemsOfLayout(item.layout())
        
        print(f"UI cleared - removed {removed_count} widgets, {self.gridLayout.count()} items remain")
        
        # Force update of the layout
        self.scrollAreaWidgetContents.adjustSize()
        
    def deleteItemsOfLayout(self, layout):
        """Recursively delete all items in a layout."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                elif item.layout() is not None:
                    self.deleteItemsOfLayout(item.layout())
    
    def toggle_metadata(self, label, button):
        """Toggle between showing full and truncated metadata."""
        if label.is_expanded:
            label.setText(label.full_text[:150] + ("..." if len(label.full_text) > 150 else ""))
            button.setText("Read More")
        else:
            label.setText(label.full_text)
            button.setText("Show Less")
        
        label.is_expanded = not label.is_expanded
        # Adjust height based on content
        if label.is_expanded:
            label.setFixedHeight(QtWidgets.QWIDGETSIZE_MAX)
        else:
            label.setFixedHeight(50)

    def addPlugin(self, plugin_name, plugin_metadata):
        row = self.gridLayout.rowCount()
        
        # plugin name label with minimal spacing
        name_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        name_layout = QtWidgets.QHBoxLayout(name_widget)
        name_layout.setContentsMargins(2, 1, 2, 1)  # Minimal margins
        
        name_label = QtWidgets.QLabel(plugin_name)
        name_label.setObjectName(f"name_{plugin_name}")
        font = QtGui.QFont()
        font.setBold(True)
        name_label.setFont(font)
        name_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        name_layout.addWidget(name_label)
        name_layout.addStretch()
        
        # Metadata widget with minimal spacing
        metadata_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        metadata_layout = QtWidgets.QVBoxLayout(metadata_widget)
        metadata_layout.setContentsMargins(2, 1, 2, 1)  # Minimal margins
        metadata_layout.setSpacing(0)  # No spacing between metadata items
        
        metadata_label = QtWidgets.QLabel(plugin_metadata)
        metadata_label.setObjectName(f"metadata_{plugin_name}")
        metadata_label.setWordWrap(True)
        metadata_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        metadata_layout.addWidget(metadata_label)
        metadata_layout.addStretch()
        
        # animated toggle button
        toggle_switch = AnimatedToggle()
        toggle_switch.setObjectName(f"toggle_{plugin_name}")
        toggle_switch.setCheckable(True)
        
        # delete button
        delete_button = QtWidgets.QPushButton("Delete")
        delete_button.setObjectName(f"delete_{plugin_name}")
        delete_button.setFixedSize(80, 30)
        
        # container widget for the plugin row with minimal styling
        row_widget = QtWidgets.QFrame()
        row_widget.setFrameShape(QFrame.StyledPanel)
        row_widget.setStyleSheet("""
            QFrame {
                border: none;
                border-bottom: 1px solid #f0f0f0;
                margin: 0;
                padding: 0;
            }
            QFrame:hover {
                background: #f8f8f8;
            }
        """)
        row_layout = QtWidgets.QHBoxLayout(row_widget)
        row_layout.setContentsMargins(5, 2, 5, 2)  # Minimal padding
        row_layout.setSpacing(10)  # Spacing between elements
        row_layout.setAlignment(Qt.AlignVCenter)  # Vertically center contents
        
        # name and metadata to the row
        row_layout.addWidget(name_widget, 1, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        row_layout.addWidget(metadata_widget, 3, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        
        # widget for buttons with proper spacing
        buttons_widget = QtWidgets.QWidget()
        buttons_layout = QtWidgets.QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(8)
        buttons_layout.addStretch()
        
        # Style and add buttons
        toggle_switch.setFixedSize(52, 24)
        delete_button.setFixedSize(70, 24)
        delete_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #333;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 2px 8px;
            }
            QPushButton:hover {
                background: #f0f0f0;
            }
            QPushButton:pressed {
                background: #e0e0e0;
            }
        """)
        
        # vertical layout for the buttons with minimal spacing
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(2)  # Very small space between buttons
        button_layout.addWidget(toggle_switch, 0, Qt.AlignCenter)
        button_layout.addWidget(delete_button, 0, Qt.AlignCenter)
        
        buttons_layout.addWidget(button_container, alignment=Qt.AlignRight)
        
        # buttons to row and row to grid
        row_layout.addWidget(buttons_widget, 1, QtCore.Qt.AlignRight)
        self.gridLayout.addWidget(row_widget, row, 0, 1, 3)
        
        # column stretch factors and alignment
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setColumnStretch(2, 0)  
        self.gridLayout.setRowStretch(row, 0)
        
        # Return only the widgets that need connections
        return toggle_switch, delete_button, None

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_PluginsDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
