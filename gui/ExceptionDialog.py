from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class AbstractDialog(QtWidgets.QDialog):
    """
    Abstract dialog that will be inherited by all dialogs classes.

    Functions overrided:
        mousePressEvent - mouseMoveEvent - mouseReleaseEvent

    Make it movable.
    """

    def __init__(self, parent=None):
        super(AbstractDialog, self).__init__(parent=parent)

        # Need to be added, if not, moving frame from a button crash
        self.left_click = False
        self.offset = self.pos()

        # Make the dialog modal to ONLY its parent
        self.setWindowModality(Qt.WindowModal)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
            self.left_click = True

    def mouseMoveEvent(self, event):
        if self.left_click:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)

    def mouseReleaseEvent(self, event):
        self.left_click = False


    def showEvent(self, event):
        # current_widget = QtWidgets.QApplication.instance().activeWindow()
        # Center the dialog regarding its parent

        return super(AbstractDialog, self).showEvent(event)

class Dialog(AbstractDialog):
    """
    Abstract Dialog.

    Base class for dialogs.
    """

    def __init__(self, width, height, obj_name, titlebar_name, titlebar_icon, parent=None):
        super(Dialog, self).__init__(parent)

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)

        self.setFixedSize(width, height)

        self.setObjectName(obj_name)

        self.layout = QtWidgets.QVBoxLayout()
        self.titlebar = AbstractTitleBar(self, title=titlebar_name, icon=titlebar_icon)
        self.titlebar.setFont(QFont('Helvetica', 9))
        self.dialog_frame = QtWidgets.QFrame(self)

        self.setup_ui()


    def setup_ui(self):
        """
        Setup the UI layout.

        :return:
        """
        # Set margin between frame and borders
        self.layout.setContentsMargins(1, 1, 1, 1)
        # Set margin between elements of layout
        self.layout.setSpacing(0)

        self.layout.insertWidget(0, self.titlebar)
        self.layout.insertWidget(1, self.dialog_frame)

        self.setLayout(self.layout)

class CriticalExceptionDialog(Dialog):
    """
    About dialog.
    """
    def __init__(self, parent=None):
        super(CriticalExceptionDialog, self).__init__(width=670, height=380,
                                                      obj_name=self.__class__.__name__,
                                                      titlebar_name="  Exception", titlebar_icon=None,
                                                      parent=parent)

        self.v_layout = QtWidgets.QVBoxLayout()

        self.dialog_frame.setLayout(self.v_layout)
        #widget = instance.activeWindow()
        #print(widget)
        #blur_effect = QtWidgets.QGraphicsBlurEffect()
        #blur_effect.setBlurHints(QtWidgets.QGraphicsBlurEffect.PerformanceHint)
        #blur_effect.setBlurRadius(3)
        #widget.setGraphicsEffect(blur_effect)
        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setObjectName("TextEditError")
        self.text_edit.setReadOnly(True)

        self.v_layout.addWidget(self.text_edit)

class AbstractTitleBar(QtWidgets.QFrame):
    """
    Abstract TitleBar.

    Used in dialogs.
    """

    def __init__(self, parent=None, title="Dafault", icon=None):
        super(AbstractTitleBar, self).__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName('TitleBar')

        self.setAutoFillBackground(True)
        self.setFixedHeight(35)

        self.close_button = QtWidgets.QToolButton(self)
        self.save_log = QtWidgets.QToolButton(self)
        self.report_issue = QtWidgets.QToolButton(self)
        self.close_button.setFixedSize(32, 32)
        self.save_log.setFixedSize(75,32)
        self.report_issue.setFixedSize(115,32)
        self.report_issue.setText("Report Issue")
        self.save_log.setText("Save")
        self.close_button.setObjectName("close_button")
        self.save_log.setObjectName("save_log")
        self.report_issue.setObjectName("report_issue")
        self.titlebar_text = QtWidgets.QLabel(title, self)
        self.titlebar_icon = QtWidgets.QLabel(self)
        self.titlebar_icon.setPixmap(QPixmap(icon))

        self.horizontal_layout = QtWidgets.QHBoxLayout(self)

        self.horizontal_layout.insertWidget(0, self.titlebar_text)
        self.horizontal_layout.insertWidget(1, self.titlebar_icon)
        self.horizontal_layout.insertStretch(2)

        self.horizontal_layout.insertWidget(-3, self.report_issue)
        self.horizontal_layout.insertWidget(-2, self.save_log)
        self.horizontal_layout.insertWidget(-1, self.close_button)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(0)

        self.close_button.clicked.connect(self.window().close)
