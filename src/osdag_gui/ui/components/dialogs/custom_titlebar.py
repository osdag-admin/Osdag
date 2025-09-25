from PySide6.QtWidgets import QWidget, QLabel, QToolButton, QHBoxLayout, QSizePolicy, QVBoxLayout
from PySide6.QtCore import Qt, QPoint, QEvent
from PySide6.QtGui import QMouseEvent, QPixmap, QFont

class CustomTitleBar(QWidget):
    def __init__(self):
        super().__init__()
        self._drag_pos = QPoint()
        self.setObjectName("CustomTitleBar")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(32)  # Set consistent height
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Add Osdag logo icon to the title bar
        from PySide6.QtSvgWidgets import QSvgWidget
        self.logo_label = QSvgWidget(":/vectors/Osdag_logo.svg", self)
        self.logo_label.setObjectName("LogoLabel")
        self.logo_label.setFixedSize(20, 20)

        # Title label
        self.title_label = QLabel("Osdag", self)
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        
        # Set font for title
        title_font = QFont()
        title_font.setPointSize(9)
        title_font.setWeight(QFont.Weight.Medium)
        self.title_label.setFont(title_font)

        # Minimize button
        self.btn_minimize = QToolButton(self)
        self.btn_minimize.setObjectName("MinimizeButton")
        self.btn_minimize.setToolTip("Minimize")
        self.btn_minimize.setText("–")
        self.btn_minimize.setFixedSize(46, 32)
        self.btn_minimize.clicked.connect(self._minimize_parent)

        # Close button
        self.btn_close = QToolButton(self)
        self.btn_close.setObjectName("CloseButton")
        self.btn_close.setToolTip("Close")
        self.btn_close.setText("✕")  # Better multiplication symbol
        self.btn_close.setFixedSize(46, 32)
        self.btn_close.clicked.connect(self._close_parent)

        # Title bar layout
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        row_widget = QWidget(self)
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(8, 0, 0, 0)
        row_layout.setSpacing(8)
        row_layout.addWidget(self.logo_label, 0)
        row_layout.addWidget(self.title_label, 1)
        row_layout.addWidget(self.btn_minimize, 0)
        row_layout.addWidget(self.btn_close, 0)
        outer_layout.addWidget(row_widget)

        self.bottom_line = QWidget(self)
        self.bottom_line.setObjectName("BottomLine")
        self.bottom_line.setFixedHeight(1)
        outer_layout.addWidget(self.bottom_line)

        # Improved stylesheet
        self.setStyleSheet("""
            QWidget#CustomTitleBar { 
                background-color: #f4f4f4;
            }
            QWidget#BottomLine {
                background-color: #90af13;
            }
            
            QLabel#TitleLabel {
                color: #000000;
                padding: 0px;
                background: transparent;
            }
            
            QLabel#LogoLabel {
                background: transparent;
                color: #ffffff;
                font-size: 14px;
            }
            
            QToolButton#MinimizeButton {
                background-color: transparent;
                color: #000000;
                border: none;
                font-size: 16px;
                border-radius: 0px;
            }
            
            QToolButton#MinimizeButton:hover {
                background-color: #f1f1f1;
            }

            QToolButton#MinimizeButton:pressed {
                background-color: #a6a6a6;
            }
            
            QToolButton#CloseButton {
                background-color: transparent;
                color: #000000;
                border: none;
                font-size: 16px;
                border-radius: 0px;
            }
            
            QToolButton#CloseButton:hover {
                background-color: #e74c3c;
                color: #ffffff;
            }
            
            QToolButton#CloseButton:pressed {
                background-color: #c0392b;
            }
        """)

    def setTitle(self, title):
        """Set the title displayed in the title bar."""
        self.title_label.setText(title)

    def _close_parent(self):
        """Close the parent widget."""
        if self.parent():
            self.parent().close()

    def _minimize_parent(self):
        """Minimize the parent widget."""
        if self.parent():
            self.parent().showMinimized()

    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for dragging."""
        if event.button() == Qt.LeftButton:
            if self.parent() and self.parent().isWindow():
                self._drag_pos = event.globalPosition().toPoint() - self.parent().frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move for dragging."""
        if (event.buttons() & Qt.LeftButton and 
            not self._drag_pos.isNull() and 
            self.parent() and 
            self.parent().isWindow()):
            self.parent().move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Reset drag position on mouse release."""
        if event.button() == Qt.LeftButton:
            self._drag_pos = QPoint()
            event.accept()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """Handle double-click to maximize/restore window."""
        if event.button() == Qt.LeftButton and self.parent() and self.parent().isWindow():
            if self.parent().isMaximized():
                self.parent().showNormal()
            else:
                self.parent().showMaximized()
            event.accept()
        else:
            super().mouseDoubleClickEvent(event)
