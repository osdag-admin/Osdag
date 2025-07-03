import sys
import os

from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QGridLayout,
    QLabel, QMainWindow, QSizePolicy, QFrame
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, Signal, QSize, QEvent, QRect, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QIcon, QPainter
from PySide6.QtSvg import QSvgRenderer


class SvgCard(QFrame):
    cardSelected = Signal(str)
    cardDeselected = Signal()

    def __init__(self, title, svg_path, parent=None):
        super().__init__(parent)
        self.setObjectName("SvgCard")
        self.title = title
        self.is_selected = False

        self.setFixedSize(160, 160) 

        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 8, 0, 0)

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 13px;")

        self.svg_widget = QSvgWidget(svg_path)
        self.svg_widget.setFixedSize(90, 80)

        self.open_label = QLabel("Open")
        self.open_label.setAlignment(Qt.AlignCenter)
        self.open_label.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.open_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) 

        self.open_label.setFixedHeight(30)
        self.open_label.setStyleSheet("""
            QLabel {
                background-color: white; 
                color: black; 
                font-weight: bold; 
                border-top: 2px solid #7ba525; 
                border-bottom-left-radius: 12px; 
                border-bottom-right-radius: 12px;
                padding: 0px;
                margin: 0px;
            }
            QLabel:hover {
                color: #90AF13;
            }
        """)
        # Connect the click event for the QLabel
        self.open_label.mousePressEvent = self.open_label_clicked # Override mousePressEvent for QLabel


        self.open_label_wrapper = QWidget(self)
        open_label_wrapper_layout = QVBoxLayout(self.open_label_wrapper)
        open_label_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        open_label_wrapper_layout.setSpacing(0)
        open_label_wrapper_layout.addWidget(self.open_label)

        self.open_label_wrapper.setMaximumHeight(0)
        self.open_label_wrapper.setMinimumHeight(0)
        self.open_label_wrapper.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        layout.addWidget(self.title_label)
        layout.addWidget(self.svg_widget, alignment=Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(self.open_label_wrapper)

        self.open_button_animation = QPropertyAnimation(self.open_label_wrapper, b"maximumHeight")
        self.open_button_animation.setDuration(250)
        self.open_button_animation.setEasingCurve(QEasingCurve.OutQuad)

        self.setStyleSheet(self.default_style())
        self.installEventFilter(self)

    def default_style(self):
        return """
        QFrame#SvgCard {
            border-radius: 12px;
            background-color: rgba(255, 255, 255, 200);
            border: 2px solid transparent;
        }
        """

    def hover_style(self):
        return """
        QFrame#SvgCard {
            background-color: rgba(144, 175, 19, 100);
            border: 2px solid #90AF13;
            border-radius: 12px;
        }
        """

    def selected_style(self):
        return """
        QFrame#SvgCard {
            background-color: rgba(144, 175, 19, 100);
            border: 2px solid #90AF13;
            border-radius: 12px;
        }
        """

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            if not self.is_selected:
                self.setStyleSheet(self.hover_style())
            target_height = self.open_label.sizeHint().height()
            self.open_button_animation.setStartValue(self.open_label_wrapper.height())
            self.open_button_animation.setEndValue(target_height)
            self.open_button_animation.start()
            self.open_label_wrapper.setMinimumHeight(0)
        elif event.type() == QEvent.Leave:
            if not self.is_selected:
                self.setStyleSheet(self.default_style())
            self.open_button_animation.setStartValue(self.open_label_wrapper.height())
            self.open_button_animation.setEndValue(0)
            self.open_button_animation.start()
        return super().eventFilter(obj, event)

    # Removed the mousePressEvent for the QFrame itself.
    # The selection logic will now be triggered only by the open_label_clicked method.
    def open_label_clicked(self, event):
        """Custom mousePressEvent for the open_label."""
        if event.button() == Qt.LeftButton:
            self.cardSelected.emit(self.title)
        # Call the base class method to ensure standard QLabel behavior (e.g., event propagation)
        super(type(self.open_label), self.open_label).mousePressEvent(event) 

    def mouseDoubleClickEvent(self, event):
        # This will still deselect if the card background is double-clicked
        self.cardDeselected.emit()

    def set_selected(self, selected):
        self.is_selected = selected
        if selected:
            self.setStyleSheet(self.selected_style())
            self.open_button_animation.stop()
            self.open_label_wrapper.setMaximumHeight(self.open_label.sizeHint().height())
            self.open_label_wrapper.setMinimumHeight(self.open_label.sizeHint().height())
        else:
            self.setStyleSheet(self.default_style())
            self.open_button_animation.stop()
            self.open_label_wrapper.setMaximumHeight(0)
            self.open_label_wrapper.setMinimumHeight(0)


class SvgCardContainer(QWidget):
    def __init__(self, card_data):
        super().__init__()
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)

        self.selected_card = None
        self.selected_card_name = ""

        self.card_data = card_data

        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(4, 1)
        
        self.layout.setRowStretch(0, 1)
        num_rows = (len(self.card_data) + 2) // 3
        self.layout.setRowStretch(num_rows + 1, 1)

        if len(self.card_data) <= 0:
            label = QLabel("Module Under Development")
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            label.setStyleSheet("""
                QLabel{
                    color: #000000;
                    font-size: 16px;
                    font-family: 'Calibri';
                }
            """)
            self.layout.addWidget(label, 1, 1, 1, 3)

        for idx, (title, svg_path) in enumerate(self.card_data):
            card = SvgCard(title, svg_path)
            card.cardSelected.connect(self.handle_card_selected)
            card.cardDeselected.connect(self.deselect_card)
            row, col = divmod(idx, 3)
            self.layout.addWidget(card, row + 1, col + 1)

    def handle_card_selected(self, card_title):
        for i in range(self.layout.count()):
            widget_item = self.layout.itemAt(i)
            if widget_item:
                widget = widget_item.widget()
                if isinstance(widget, SvgCard):
                    widget.set_selected(widget.title == card_title)
                    if widget.title == card_title:
                        self.selected_card = widget
                        self.selected_card_name = widget.title

    def get_selected_card_name(self):
        return self.selected_card_name

    def deselect_card(self):
        for i in range(self.layout.count()):
            widget_item = self.layout.itemAt(i)
            if widget_item:
                widget = widget_item.widget()
                if isinstance(widget, SvgCard):
                    widget.set_selected(False)
        self.selected_card = None
        self.selected_card_name = ""
