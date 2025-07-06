from PySide6.QtWidgets import QPushButton, QMenu
from PySide6.QtGui import QPainter, QPen, QColor, QPolygon, QAction
from PySide6.QtCore import Qt, QPoint, Signal

class AdditionalInputsButton(QPushButton):
    menu_item_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__("Additional Inputs", parent)
        self.pinned = False
        self.arrow_up = False

        # Dropdown menu
        self.menu = QMenu(self)
        self.apply_menu_style(self.menu)
        self.add_menu_actions()

        # Styling
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(30)
        self.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 5px;
                border: 1px solid #90AF13;
                padding-left: 14px;
                padding-right: 60px;
                text-align: left;
            }
        """)
        self.subMenu = False
        self.clicked.connect(self.on_main_clicked)

    def apply_menu_style(self, menu):
        menu.setStyleSheet("""
            QMenu {
                margin-top: 2px;
                background-color: white;
                border: 1px solid #90AF13;
            }
            QMenu::item {
                padding: 5px 14px;
                color: black;
            }
            QMenu::item:selected {
                background-color: #90AF13;
                color: black;
            }
        """)

    def add_menu_actions(self):
        assumptions = QAction("Assumptions", self)
        preferences = QAction("Preferences", self)
        assumptions.triggered.connect(lambda: self.menu_item_clicked.emit("Assumptions"))
        preferences.triggered.connect(lambda: self.menu_item_clicked.emit("Preferences"))
        self.menu.addAction(assumptions)
        self.menu.addAction(preferences)
        self.menu.aboutToHide.connect(self.on_menu_closed)

    def on_main_clicked(self):
        if self.subMenu:
            self.subMenu = False
            self.menu.hide()
            self.pinned = False
            self.arrow_up = False
            self.update()
        else:    
            self.subMenu = True
            self.show_menu()
            self.pinned = True
            self.arrow_up = True
            self.update()

    def show_menu(self):
        self.menu.setMinimumWidth(self.width())
        anchor_pos = self.mapToGlobal(self.rect().bottomLeft())
        self.menu.move(anchor_pos)
        self.menu.show()
        self.arrow_up = True
        self.update()

    def on_menu_closed(self):
        self.subMenu = False
        self.pinned = False
        self.arrow_up = False
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        circle_radius = 9
        margin_right = 14
        center_x = self.width() - margin_right - circle_radius
        center_y = self.height() // 2
        circle_center = QPoint(center_x, center_y)
        painter.setBrush(QColor("white"))
        painter.setPen(QPen(QColor("Black"), 1))
        painter.drawEllipse(circle_center, circle_radius, circle_radius)
        arrow_size = circle_radius // 2
        if self.arrow_up:
            points = [
                QPoint(center_x - arrow_size, center_y + arrow_size // 2),
                QPoint(center_x + arrow_size, center_y + arrow_size // 2),
                QPoint(center_x, center_y - arrow_size // 2),
            ]
        else:
            points = [
                QPoint(center_x - arrow_size, center_y - arrow_size // 2),
                QPoint(center_x + arrow_size, center_y - arrow_size // 2),
                QPoint(center_x, center_y + arrow_size // 2),
            ]
        painter.setBrush(QColor("black"))
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(QPolygon(points))
        painter.end()

