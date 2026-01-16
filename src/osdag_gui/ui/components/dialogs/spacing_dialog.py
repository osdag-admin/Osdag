from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_core.Common import *

from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QSizePolicy, QFrame, QDialog,
    QLineEdit, QScrollArea, QTableWidget, QGridLayout,
    QSizeGrip
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QCoreApplication

class SpacingDialog(QDialog):
    def __init__(self, main, title, fn):
        super().__init__()
        app = QApplication.instance()
        self.theme = app.theme_manager

        # Center the window on the screen with the same dimensions
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width, height = 900, 500
        x = screen_geometry.x() + (screen_geometry.width() - width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - height) // 2
        self.setGeometry(x, y, width, height)
        self.setObjectName("spacing_dialog")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)
        self.title_bar = CustomTitleBar()
        self.title_bar.setTitle(title)
        main_layout.addWidget(self.title_bar)
        self.content_widget = QWidget(self)
        main_layout.addWidget(self.content_widget, 1)
        size_grip = QSizeGrip(self)
        size_grip.setFixedSize(1, 1)
        overlay = QHBoxLayout()
        overlay.setContentsMargins(0, 0, 4, 4)
        overlay.addStretch(1)
        overlay.addWidget(size_grip, 0, Qt.AlignBottom | Qt.AlignRight)
        main_layout.addLayout(overlay)

        layout1 = QVBoxLayout(self.content_widget)
        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.setSpacing(0)

        note_widget = QWidget()
        note_layout = QVBoxLayout(note_widget)
        layout1.addWidget(note_widget)

        tabel_widget = QWidget()
        table_layout = QVBoxLayout(tabel_widget)
        layout1.addWidget(tabel_widget)

        scroll = QScrollArea()
        layout1.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.horizontalScrollBar().setVisible(False)
        scroll_content = QWidget(scroll)
        scroll_content.setObjectName("scroll_widget")
        outer_grid_layout = QGridLayout(scroll_content)
        inner_grid_widget = QWidget(scroll_content)
        image_widget = QWidget(scroll_content)
        image_layout = QVBoxLayout(image_widget)
        image_layout.setAlignment(Qt.AlignCenter)
        image_widget.setLayout(image_layout)
        inner_grid_layout = QGridLayout(inner_grid_widget)
        inner_grid_widget.setLayout(inner_grid_layout)
        scroll_content.setLayout(outer_grid_layout)
        scroll.setWidget(scroll_content)

        dialog_width = 260
        dialog_height = 300
        max_image_width = 0
        max_label_width = 0
        max_image_height = 0

        section = 0
        no_note = True
        j = 1
        _translate = QCoreApplication.translate
        for option in fn(main.design_status):
            option_type = option[2]
            lable = option[1]
            value = option[3]
            if option_type in [TYPE_TEXTBOX, TYPE_COMBOBOX]:
                l = QLabel(inner_grid_widget)

                l.setObjectName(option[0] + "_label")
                l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))
                inner_grid_layout.addWidget(l, j, 1, 1, 1)
                l.setFixedSize(l.sizeHint().width(), l.sizeHint().height())
                max_label_width = max(l.sizeHint().width(), max_label_width)
                l.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
                
            if option_type == TYPE_SECTION:
                if section != 0:
                    outer_grid_layout.addWidget(inner_grid_widget, j, 1, 1, 1)
                    outer_grid_layout.addWidget(image_widget, j, 2, 1, 1)
                    hl1 = QFrame()
                    hl1.setFrameShape(QFrame.HLine)
                    j += 1
                    outer_grid_layout.addWidget(hl1, j, 1, 1, 2)

                inner_grid_widget = QWidget(scroll_content)
                image_widget = QWidget(scroll_content)
                image_layout = QVBoxLayout(image_widget)
                image_layout.setAlignment(Qt.AlignCenter)
                image_widget.setLayout(image_layout)
                inner_grid_layout = QGridLayout(inner_grid_widget)
                inner_grid_widget.setLayout(inner_grid_layout)

                if value is not None and value != "":
                    im = QLabel(image_widget)
                    im.setFixedSize(int(value[1]), int(value[2]))
                    pmap = QPixmap(value[0])
                    im.setScaledContents(1)
                    im.setStyleSheet("background-color: white;")
                    im.setPixmap(pmap)
                    image_layout.addWidget(im)
                    caption = QLabel(image_widget)
                    caption.setAlignment(Qt.AlignCenter)
                    caption.setText(value[3])
                    caption.setFixedSize(int(value[1]), caption.sizeHint().height())
                    image_layout.addWidget(caption)
                    max_image_width = max(max_image_width, value[1])
                    max_image_height = max(max_image_height, value[2])
                j += 1
                q = QLabel(scroll_content)
                q.setObjectName("_title")
                q.setText(lable)
                q.setFixedSize(q.sizeHint().width(), q.sizeHint().height())
                q.setSizePolicy(
                    QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
                outer_grid_layout.addWidget(q, j, 1, 1, 2)
                section += 1
                
            if option_type == TYPE_TEXTBOX:
                r = QLineEdit(inner_grid_widget)
                r.setDisabled(True)
                r.setFixedSize(100, 27)
                r.setObjectName(option[0])
                r.setText(str(value))
                inner_grid_layout.addWidget(r, j, 2, 1, 1)

            if option_type == TYPE_TABLE_OU:
                tb = QTableWidget(tabel_widget)
                table_layout.addWidget(tb)

            if option_type == TYPE_IMAGE:
                im = QLabel(image_widget)
                im.setScaledContents(True)
                im.setFixedSize(int(value[1]), int(value[2]))
                pmap = QPixmap(value[0])
                im.setStyleSheet("background-color: white;")
                im.setPixmap(pmap)
                image_layout.addWidget(im)
                caption = QLabel(image_widget)
                caption.setAlignment(Qt.AlignCenter)
                caption.setText(value[3])
                caption.setFixedSize(int(value[1]), 12)
                image_layout.addWidget(caption)
                max_image_width = max(max_image_width, value[1])
                max_image_height = max(max_image_height, value[2])

            if option_type == TYPE_NOTE:
                note = QLabel(note_widget)
                note.setText("Note: "+str(value))
                note.setFixedSize(note.sizeHint().width(), note.sizeHint().height())
                note_layout.addWidget(note)
                no_note = False

            j = j + 1

        if inner_grid_layout.count() > 0:
            outer_grid_layout.addWidget(inner_grid_widget, j, 1, 1, 1)
        if image_layout.count() > 0:
            outer_grid_layout.addWidget(image_widget, j, 2, 1, 1)

        dialog_width += max_label_width
        dialog_width += max_image_width
        dialog_height = max(dialog_height, max_image_height+125)
        if not no_note:
            dialog_height += 40
        self.resize(int(dialog_width), int(dialog_height))
        self.setMinimumSize(int(dialog_width), int(dialog_height))
        if no_note:
            layout1.removeWidget(note_widget)