# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogBox_march23.ui'
#
# Created: Fri Apr  1 05:21:38 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore
from PyQt5.QtWidgets import  QDialog, QLabel,QLineEdit, QApplication
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_Capacitydetals(object):
    def setupUi(self, Capacitydetals):
        Capacitydetals.setObjectName(_fromUtf8("Capacitydetals"))
        Capacitydetals.resize(395, 403)
        self.lbl_shear = QLabel(Capacitydetals)
        self.lbl_shear.setGeometry(QtCore.QRect(10, 30, 131, 17))
        self.lbl_shear.setObjectName(_fromUtf8("lbl_shear"))
        self.label_2 = QLabel(Capacitydetals)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 151, 21))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lbl_bearing = QLabel(Capacitydetals)
        self.lbl_bearing.setGeometry(QtCore.QRect(10, 60, 151, 21))
        self.lbl_bearing.setObjectName(_fromUtf8("lbl_bearing"))
        self.lbl_capacity = QLabel(Capacitydetals)
        self.lbl_capacity.setGeometry(QtCore.QRect(10, 90, 141, 20))
        self.lbl_capacity.setObjectName(_fromUtf8("lbl_capacity"))
        self.lbl_boltGrp = QLabel(Capacitydetals)
        self.lbl_boltGrp.setGeometry(QtCore.QRect(10, 120, 171, 17))
        self.lbl_boltGrp.setObjectName(_fromUtf8("lbl_boltGrp"))
        self.lbl_col = QLabel(Capacitydetals)
        self.lbl_col.setGeometry(QtCore.QRect(10, 10, 171, 17))
        self.lbl_col.setObjectName(_fromUtf8("lbl_col"))
        self.lbl_beam = QLabel(Capacitydetals)
        self.lbl_beam.setGeometry(QtCore.QRect(11, 150, 171, 17))
        self.lbl_beam.setObjectName(_fromUtf8("lbl_beam"))
        self.lbl_cleat = QLabel(Capacitydetals)
        self.lbl_cleat.setGeometry(QtCore.QRect(10, 290, 91, 17))
        self.lbl_cleat.setObjectName(_fromUtf8("lbl_cleat"))
        self.lbl_shear_b = QLabel(Capacitydetals)
        self.lbl_shear_b.setGeometry(QtCore.QRect(10, 170, 131, 17))
        self.lbl_shear_b.setObjectName(_fromUtf8("lbl_shear_b"))
        self.lbl_bearing_b = QLabel(Capacitydetals)
        self.lbl_bearing_b.setGeometry(QtCore.QRect(10, 200, 151, 21))
        self.lbl_bearing_b.setObjectName(_fromUtf8("lbl_bearing_b"))
        self.lbl_capacity_b = QLabel(Capacitydetals)
        self.lbl_capacity_b.setGeometry(QtCore.QRect(10, 230, 141, 17))
        self.lbl_capacity_b.setObjectName(_fromUtf8("lbl_capacity_b"))
        self.lbl_boltGrp_b = QLabel(Capacitydetals)
        self.lbl_boltGrp_b.setGeometry(QtCore.QRect(10, 260, 171, 17))
        self.lbl_boltGrp_b.setObjectName(_fromUtf8("lbl_boltGrp_b"))
        self.lbl_mDemand = QLabel(Capacitydetals)
        self.lbl_mDemand.setGeometry(QtCore.QRect(10, 310, 171, 20))
        self.lbl_mDemand.setObjectName(_fromUtf8("lbl_mDemand"))
        self.lbl_mCapacity = QLabel(Capacitydetals)
        self.lbl_mCapacity.setGeometry(QtCore.QRect(10, 340, 171, 17))
        self.lbl_mCapacity.setObjectName(_fromUtf8("lbl_mCapacity"))
        self.shear = QLineEdit(Capacitydetals)
        self.shear.setGeometry(QtCore.QRect(240, 30, 130, 27))
        self.shear.setObjectName(_fromUtf8("shear"))
        self.shear.setReadOnly(True)
        
        self.bearing = QLineEdit(Capacitydetals)
        self.bearing.setGeometry(QtCore.QRect(240, 60, 130, 27))
        self.bearing.setObjectName(_fromUtf8("bearing"))
        self.bearing.setReadOnly(True)
        
        self.capacity = QLineEdit(Capacitydetals)
        self.capacity.setGeometry(QtCore.QRect(240, 90, 130, 27))
        self.capacity.setObjectName(_fromUtf8("capacity"))
        self.capacity.setReadOnly(True)
        
        self.boltGrp = QLineEdit(Capacitydetals)
        self.boltGrp.setGeometry(QtCore.QRect(240, 120, 130, 27))
        self.boltGrp.setObjectName(_fromUtf8("boltGrp"))
        self.boltGrp.setReadOnly(True)
        
        self.bearing_b = QLineEdit(Capacitydetals)
        self.bearing_b.setGeometry(QtCore.QRect(240, 200, 130, 27))
        self.bearing_b.setObjectName(_fromUtf8("bearing_b"))
        self.bearing_b.setReadOnly(True)
        
        self.capacity_b = QLineEdit(Capacitydetals)
        self.capacity_b.setGeometry(QtCore.QRect(239, 230, 130, 27))
        self.capacity_b.setObjectName(_fromUtf8("capacity_b"))
        self.capacity_b.setReadOnly(True)
        
        self.boltGrp_b = QLineEdit(Capacitydetals)
        self.boltGrp_b.setGeometry(QtCore.QRect(239, 260, 130, 27))
        self.boltGrp_b.setObjectName(_fromUtf8("boltGrp_b"))
        self.boltGrp_b.setReadOnly(True)
        
        self.mDemand = QLineEdit(Capacitydetals)
        self.mDemand.setGeometry(QtCore.QRect(241, 310, 130, 27))
        self.mDemand.setObjectName(_fromUtf8("mDemand"))
        self.mDemand.setReadOnly(True)
        
        self.mCapacity = QLineEdit(Capacitydetals)
        self.mCapacity.setGeometry(QtCore.QRect(241, 340, 130, 27))
        self.mCapacity.setObjectName(_fromUtf8("mCapacity"))
        self.mCapacity.setReadOnly(True)
        
        self.shear_b = QLineEdit(Capacitydetals)
        self.shear_b.setGeometry(QtCore.QRect(240, 170, 130, 27))
        self.shear_b.setObjectName(_fromUtf8("shear_b"))
        self.shear_b.setReadOnly(True)

        self.retranslateUi(Capacitydetals)
        QtCore.QMetaObject.connectSlotsByName(Capacitydetals)

    def retranslateUi(self, Capacitydetals):
        Capacitydetals.setWindowTitle(_translate("Capacitydetals", "Dialog", None))
        self.lbl_shear.setText(_translate("Capacitydetals", "Shear capacity (kN)", None))
        self.lbl_bearing.setText(_translate("Capacitydetals", "Bearing capacity (kN)", None))
        self.lbl_capacity.setText(_translate("Capacitydetals", "Capacity of bolt (kN)", None))
        self.lbl_boltGrp.setText(_translate("Capacitydetals", "Bolt group capacity (kN)", None))
        self.lbl_col.setText(_translate("Capacitydetals", "<html><head/><body><p><span style=\" font-weight:600;\">Supporting member</span></p></body></html>", None))
        self.lbl_beam.setText(_translate("Capacitydetals", "<html><head/><body><p><span style=\" font-weight:600;\">Supported member</span></p></body></html>", None))
        self.lbl_cleat.setText(_translate("Capacitydetals", "<html><head/><body><p><span style=\" font-weight:600;\">Cleat Angle</span></p></body></html>", None))
        self.lbl_shear_b.setText(_translate("Capacitydetals", "Shear capacity (kN)", None))
        self.lbl_bearing_b.setText(_translate("Capacitydetals", "Bearing capacity (kN)", None))
        self.lbl_capacity_b.setText(_translate("Capacitydetals", "Capacity of bolt (kN)", None))
        self.lbl_boltGrp_b.setText(_translate("Capacitydetals", "Bolt group capacity (kN)", None))
        self.lbl_mDemand.setText(_translate("Capacitydetals", "Moment demand (kNm)", None))
        self.lbl_mCapacity.setText(_translate("Capacitydetals", "Moment capacity (kNm)", None))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Capacitydetals()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
