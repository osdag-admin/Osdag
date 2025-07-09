from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PySide6.QtCore import Qt
from PySide6.QtCore import QDateTime

class LogDock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_visible = True
        self.init_ui()
        self.adjust_size()

    def init_ui(self):
        # Create layout for the log dock
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 0)
        layout.setSpacing(0)

        # Create a top strip for "Log Window"
        self.log_window_title = QLabel("Log Window")
        self.log_window_title.setStyleSheet("""
            QLabel {
                background-color: #F2F2F2;
                color: #000000;
                padding: 3px;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        self.log_window_title.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.log_window_title)

        # Create log display area
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: #F8F8F8;
                border: 1px solid #D0D0D0;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                padding: 5px;
                color: #000000;
            }
            QScrollBar:vertical {
                background: #E0E0E0; /* Light grey for the scrollbar track */
                width: 8px;
                margin: 0px 0px 0px 3px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical {
                background: #A0A0A0; /* Medium grey for the scrollbar handle */
                min-height: 30px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: #707070; /* Darker grey on hover for the handle */
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px; /* Hides the up/down arrows */
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none; /* Hides the area between handle and arrows */
            }
        """)
        layout.addWidget(self.log_display)

        # Add demo log text matching the image format
        self.append_log(f"[{QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')}] Log initialized", "info")
        demo_log_messages = [
            ("Info: In the case of reverse loading, the slenderness value shall be less than 180 [Ref. Table 3, IS 800:2007].", "info"),
            ("Info: To reduce the quantity of bolts, define a list of diameter, plate thickness and/or member size higher than the one currently defined.", "info"),
            ("Error: Overall bolted tension member design is safe.", "error"),
            ("Info: ====== End Of Design ======", "info")
        ]
        for message, level in demo_log_messages:
            self.append_log(message, level)

        self.setLayout(layout)
        self.show()  # Show initially to display demo text

    def append_log(self, message, log_level="info"):
        """Append a message to the log display with specified color."""
        if log_level == "error":
            color = "#FF0000"  # Red for errors
        elif log_level == "info":
            color = "#000000"  # Black for info
        elif log_level == "success":
            color = "#008000"  # Green for success

        formatted_message = f"<span style=\"color: {color};\">{message}</span>"
        self.log_display.append(formatted_message)
        self.log_display.ensureCursorVisible()

    def toggle_log_dock(self):
        """Toggle the visibility of the log dock."""
        self.is_visible = not self.is_visible
        if self.is_visible:
            self.show()
            self.adjust_size()
            self.move(0, self.parent().height() - self.height())
        else:
            self.hide()

    def adjust_size(self):
        """Adjust the size of the log dock based on input and output dock states."""
        parent = self.parent()
        if not parent:
            return

        # Get the current tab's input and output dock states
        current_tab_index = parent.tab_bar.currentIndex()
        if current_tab_index < 0 or current_tab_index >= len(parent.tab_widget_content):
            return

        input_active = parent.tab_widget_content[current_tab_index][3]
        output_active = parent.tab_widget_content[current_tab_index][4]

        # Calculate available width
        parent_width = parent.width()
        input_dock_width = parent.tab_widget_content[current_tab_index][1].width() if input_active else 0
        output_dock_width = parent.tab_widget_content[current_tab_index][2].width() if output_active else 0
        available_width = parent_width - input_dock_width - output_dock_width

        # Set log dock size
        default_height = 150  # Fixed height for log dock
        self.setFixedSize(available_width, default_height)

        # Update position if visible
        if self.is_visible:
            self.move(0, parent.height() - default_height)