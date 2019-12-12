from PyQt5 import QtCore, QtWidgets

class TwoListSelection(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TwoListSelection, self).__init__(parent)
        self.setup_layout()

    def setup_layout(self):
        lay = QtWidgets.QHBoxLayout(self)
        self.mInput = QtWidgets.QListWidget()
        self.mOuput = QtWidgets.QListWidget()

        self.mButtonToSelected = QtWidgets.QPushButton(">>")
        self.mBtnMoveToAvailable= QtWidgets.QPushButton(">")
        self.mBtnMoveToSelected= QtWidgets.QPushButton("<")
        self.mButtonToAvailable = QtWidgets.QPushButton("<<")

        vlay = QtWidgets.QVBoxLayout()
        vlay.addStretch()
        vlay.addWidget(self.mButtonToSelected)
        vlay.addWidget(self.mBtnMoveToAvailable)
        vlay.addWidget(self.mBtnMoveToSelected)
        vlay.addWidget(self.mButtonToAvailable)
        vlay.addStretch()

        #self.mBtnUp = QtWidgets.QPushButton("Up")
        #self.mBtnDown = QtWidgets.QPushButton("Down")

        """vlay2 = QtWidgets.QVBoxLayout()
        vlay2.addStretch()
        #vlay2.addWidget(self.mBtnUp)
        #vlay2.addWidget(self.mBtnDown)
        vlay2.addStretch()"""

        lay.addWidget(self.mInput)
        lay.addLayout(vlay)
        lay.addWidget(self.mOuput)
        #lay.addLayout(vlay2)

        self.update_buttons_status()
        self.connections()

    @QtCore.pyqtSlot()
    def update_buttons_status(self):
        #self.mBtnUp.setDisabled(not bool(self.mOuput.selectedItems()) or self.mOuput.currentRow() == 0)
        #self.mBtnDown.setDisabled(not bool(self.mOuput.selectedItems()) or self.mOuput.currentRow() == (self.mOuput.count() -1))
        self.mBtnMoveToAvailable.setDisabled(not bool(self.mInput.selectedItems()) or self.mOuput.currentRow() == 0)
        self.mBtnMoveToSelected.setDisabled(not bool(self.mOuput.selectedItems()))

    def connections(self):
        self.mInput.itemSelectionChanged.connect(self.update_buttons_status)
        self.mOuput.itemSelectionChanged.connect(self.update_buttons_status)
        self.mBtnMoveToAvailable.clicked.connect(self.on_mBtnMoveToAvailable_clicked)
        self.mBtnMoveToSelected.clicked.connect(self.on_mBtnMoveToSelected_clicked)
        self.mButtonToAvailable.clicked.connect(self.on_mButtonToAvailable_clicked)
        self.mButtonToSelected.clicked.connect(self.on_mButtonToSelected_clicked)
        #self.mBtnUp.clicked.connect(self.on_mBtnUp_clicked)
        #self.mBtnDown.clicked.connect(self.on_mBtnDown_clicked)

    @QtCore.pyqtSlot()
    def on_mBtnMoveToAvailable_clicked(self):
        self.mOuput.addItem(self.mInput.takeItem(self.mInput.currentRow()))

    @QtCore.pyqtSlot()
    def on_mBtnMoveToSelected_clicked(self):
        self.mInput.addItem(self.mOuput.takeItem(self.mOuput.currentRow()))

    @QtCore.pyqtSlot()
    def on_mButtonToAvailable_clicked(self):
        while self.mOuput.count() > 0:
            self.mInput.addItem(self.mOuput.takeItem(0))

    @QtCore.pyqtSlot()
    def on_mButtonToSelected_clicked(self):
        while self.mInput.count() > 0:
            self.mOuput.addItem(self.mInput.takeItem(0))        

    @QtCore.pyqtSlot()
    def on_mBtnUp_clicked(self):
        row = self.mOuput.currentRow()
        currentItem = self.mOuput.takeItem(row)
        self.mOuput.insertItem(row - 1, currentItem)
        self.mOuput.setCurrentRow(row - 1)

    @QtCore.pyqtSlot()
    def on_mBtnDown_clicked(self):
        row = self.mOuput.currentRow()
        currentItem = self.mOuput.takeItem(row)
        self.mOuput.insertItem(row + 1, currentItem)
        self.mOuput.setCurrentRow(row + 1)

    def addAvailableItems(self,items):
        self.mInput.addItems((items))

    def get_left_elements(self):
        r = []
        for i in range(self.mInput.count()):
            it = self.mInput.item(i)
            r.append(it.text())
        print(r)
        return r

    def get_right_elements(self):
        r = []
        for i in range(self.mOuput.count()):
            it = self.mOuput.item(i)
            r.append(it.text())
        return r

if __name__ == '__main__':
    lst = ['1','2']
    import sys
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    list_selection = TwoListSelection()
    #list_selection.addAvailableItems(["item-{}".format(i) for i in range(20)])
    list_selection.addAvailableItems(lst)
    def on_clicked_left():
        print(list_selection.get_left_elements())
    def on_clicked_right():
        print(list_selection.get_right_elements())
    l_button = QtWidgets.QPushButton(
        text="Available:",
        clicked=on_clicked_left
    )
    r_button = QtWidgets.QPushButton(
        text="Selected:",
        clicked=on_clicked_right
    )
    w = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(w)
    hlay = QtWidgets.QHBoxLayout()
    hlay.addWidget(l_button)
    hlay.addWidget(r_button)
    lay.addLayout(hlay)
    lay.addWidget(list_selection)
    w.show()
    sys.exit(app.exec_())
