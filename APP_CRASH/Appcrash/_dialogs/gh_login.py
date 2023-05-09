from PyQt5 import QtCore, QtWidgets

from .._forms import dlg_github_login_ui

GH_MARK_NORMAL = ':/rc/GitHub-Mark.png'
GH_MARK_LIGHT = ':/rc/GitHub-Mark-Light.png'


class DlgGitHubLogin(QtWidgets.QDialog):
    HTML = '<html><head/><body><p align="center"><img src="%s"/></p>' \
        '<p align="center">Sign in to GitHub</p></body></html>'

    def __init__(self, parent, username, remember, password, remember_token, token):
        super(DlgGitHubLogin, self).__init__(parent)
        self.ui = dlg_github_login_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.username = username
        self.remember = remember
        self.password = password
        self.remember_token = remember_token
        self.token = token
        self.is_basic = True
        mark = GH_MARK_NORMAL
        if self.palette().base().color().lightness() < 128:
            mark = GH_MARK_LIGHT
        html = self.HTML % mark
        self.ui.label_6.hide()
        self.ui.label_7.hide()
        self.ui.label_8.hide()
        self.ui.label_9.hide()
        self.ui.hl1.hide()
        self.ui.lbl_html.setText(html)
        self.ui.bt_sign_in.clicked.connect(self.accept)
        self.ui.le_username.textChanged.connect(self.update_btn_state)
        self.ui.le_password.textChanged.connect(self.update_btn_state)
        if self.is_basic:
            if self.username=='' and self.password=='':
                self.ui.bt_sign_in.setDisabled(True)
        else:
            if not self.token:
                self.ui.bt_sign_in.setDisabled(True)

        self.ui.le_username.setText(self.username)
        self.ui.le_password.setText(self.password)
        self.ui.cb_remember.setChecked(self.remember)
        #self.ui.label_8.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,QtWidgets.QSizePolicy.Maximum))
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
        self.ui.le_password.installEventFilter(self)
        self.ui.le_username.installEventFilter(self)
        self.ui.label_4.installEventFilter(self)

    def eventFilter(self, obj, event):
        interesting_objects = [self.ui.le_password, self.ui.le_username]
        if obj in interesting_objects and event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return and event.modifiers() & QtCore.Qt.ControlModifier and \
                    self.ui.bt_sign_in.isEnabled():
                self.accept()
                return True
        if obj == self.ui.label_4:
            if event.type()==QtCore.QEvent.Enter:
                self.ui.label_4.setStyleSheet("color:Green;font-size:10pt;font-family:consolas;")
                self.adjustSize()
            elif event.type()==QtCore.QEvent.Leave:
                self.ui.label_4.setStyleSheet("font-size:9pt;font-family:consolas;")
                self.adjustSize()
            elif event.type()==QtCore.QEvent.MouseButtonPress:
                if event.button()==QtCore.Qt.LeftButton:
                    text = self.ui.label_4.text()
                    if text == 'Sign in using Personal Access Token':
                        self.remove_widget()
                    else:
                        self.add_Widget()
                    self.adjustSize()
                    return True
        return False

    def remove_widget(self):
        #self.ui.verticalLayout.removeWidget(self.ui.le_password)
        #self.ui.le_password.deleteLater()
        #self.ui.le_password = None

        #self.ui.verticalLayout.removeWidget(self.ui.label_3)
        #self.ui.label_3.deleteLater()
        #self.ui.label_3 = None
        self.ui.label_6.show()
        self.ui.label_7.show()
        self.ui.label_8.show()
        self.ui.label_9.show()
        self.ui.hl1.show()
        self.is_basic = False
        self.ui.le_username.setText(self.token)
        if self.ui.le_username.text():
            self.ui.bt_sign_in.setEnabled(1)
        self.ui.le_password.hide()
        self.ui.label_3.hide()
        self.ui.label_2.setText("Token:")
        self.ui.label_4.setText("Basic Authentication")
        self.ui.le_username.textChanged.connect(self.change_btn_state)
        self.ui.cb_remember.setChecked(self.remember_token)
        self.adjustSize()

    def add_Widget(self):
        self.ui.label_6.hide()
        self.ui.label_7.hide()
        self.ui.label_8.hide()
        self.ui.label_9.hide()
        self.ui.hl1.hide()
        self.is_basic = True
        if self.username and self.password:
            self.ui.bt_sign_in.setEnabled(1)
        else:
            self.ui.bt_sign_in.setEnabled(0)
        self.ui.le_password.setText(self.password)
        self.ui.le_username.setText(self.username)
        self.ui.le_password.show()
        self.ui.label_3.show()
        self.ui.label_2.setText("Username:")
        self.ui.le_username.textChanged.connect(self.update_btn_state)
        self.ui.label_4.setText("Sign in using Personal Access Token")
        self.ui.cb_remember.setChecked(self.remember)
        self.adjustSize()

    def change_btn_state(self):
        if self.ui.le_username.text():
            self.ui.bt_sign_in.setEnabled(1)
        else:
            self.ui.bt_sign_in.setEnabled(0)

    def update_btn_state(self):
        if self.ui.le_username.text()!='' and self.ui.le_password.text()!='':
            self.ui.bt_sign_in.setEnabled(1)
        else:
            self.ui.bt_sign_in.setEnabled(0)

    @classmethod
    def login(cls, parent, username, remember, password, remember_token, token):  # pragma: no cover
        dlg = DlgGitHubLogin(parent, username, remember, password, remember_token, token)
        if dlg.exec_() == dlg.Accepted:
            return dlg.ui.le_username.text(), dlg.ui.le_password.text(), \
                dlg.ui.cb_remember.isChecked(),dlg.is_basic, dlg.ui.cb_remember.isChecked(), dlg.ui.le_username.text()
        return None, None, None, None, None, None
