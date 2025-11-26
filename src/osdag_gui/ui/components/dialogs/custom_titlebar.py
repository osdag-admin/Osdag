from PySide6.QtWidgets import QWidget, QLabel, QToolButton, QHBoxLayout, QSizePolicy, QVBoxLayout
from PySide6.QtCore import Qt, QPoint, QEvent
from PySide6.QtGui import QMouseEvent, QFont

class CustomTitleBar(QWidget):
    def __init__(self, max_res_btn: bool = False, min_res_btn:bool = False, parent=None):
        super().__init__(parent)
        # Ensures automatic deletion when closed
        self.setAttribute(Qt.WA_DeleteOnClose, True)
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

        # Minimize button (optional)
        self.btn_minimize = None
        if min_res_btn:
            self.btn_minimize = QToolButton(self)
            self.btn_minimize.setObjectName("MinimizeButton")
            self.btn_minimize.setToolTip("Minimize")
            self.btn_minimize.setText("–")
            self.btn_minimize.setFixedSize(46, 32)
            self.btn_minimize.clicked.connect(self._minimize_parent)

        # Maximize/Restore button (optional)
        self.btn_max_restore = None
        if max_res_btn:
            self.btn_max_restore = QToolButton(self)
            self.btn_max_restore.setObjectName("MaxRestoreButton")
            self.btn_max_restore.setToolTip("Maximize")
            self.btn_max_restore.setText("□")
            self.btn_max_restore.setFixedSize(46, 32)
            self.btn_max_restore.clicked.connect(self._toggle_max_restore)

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
        if self.btn_minimize is not None:
            row_layout.addWidget(self.btn_minimize, 0)
        if self.btn_max_restore is not None:
            row_layout.addWidget(self.btn_max_restore, 0)
        row_layout.addWidget(self.btn_close, 0)
        outer_layout.addWidget(row_widget)

        self.bottom_line = QWidget(self)
        self.bottom_line.setObjectName("BottomLine")
        self.bottom_line.setFixedHeight(1)
        outer_layout.addWidget(self.bottom_line)

        # Keep the maximize/restore button state in sync with the window state
        if self.btn_max_restore is not None and self.parent() is not None:
            self.parent().installEventFilter(self)
            self._update_max_restore_icon()

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

    def _toggle_max_restore(self):
        """Toggle between maximizing and restoring the parent window."""
        window = self.parent()
        if not window:
            return
        if window.isMaximized():
            window.showNormal()
        else:
            window.showMaximized()
        self._update_max_restore_icon()

    def _update_max_restore_icon(self):
        """Update the icon/text and tooltip of the maximize/restore button based on window state."""
        if self.btn_max_restore is None:
            return
        window = self.parent()
        if not window:
            return
        if window.isMaximized():
            self.btn_max_restore.setText("❐")  # Restore
            self.btn_max_restore.setToolTip("Restore")
        else:
            self.btn_max_restore.setText("□")  # Maximize
            self.btn_max_restore.setToolTip("Maximize")

    def eventFilter(self, obj, event):
        # Update button when window state changes (e.g., via system controls or double-click)
        if obj is self.parent() and event.type() == QEvent.WindowStateChange:
            self._update_max_restore_icon()
        return super().eventFilter(obj, event)

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
            # Keep button state in sync
            if self.btn_max_restore is not None:
                self._update_max_restore_icon()
            event.accept()
        else:
            super().mouseDoubleClickEvent(event)
