# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'summary_popup.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog, QDialogButtonBox
from PyQt5.QtWidgets import QMessageBox, qApp
from PyQt5 import QtCore, QtGui, QtWidgets
import configparser
import os
import re
import time
import pickle
# from .ui_summary_popup import Ui_Dialog1
from ..design_report.reportGenerator import save_html
from ..design_report.reportGenerator_latex import CreateLatex
# from ..design_type.connection.fin_plate_connection import sa
from ..get_DPI_scale import scale


class DummyThread(QtCore.QThread):
    finished = QtCore.pyqtSignal()

    def __init__(self, sec, parent):
        self.sec = sec
        super().__init__(parent=parent)

    def run(self):
        time.sleep(self.sec)
        self.finished.emit()


class Ui_Dialog1(object):

    def __init__(self, design_exist, loggermsg):
        self.design_exist = design_exist
        self.loggermsg = loggermsg

    def setupUi(self, Dialog, main, module_window):
        self.Dialog = Dialog
        self.module_window = module_window
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(int(scale * 600), int(scale * 550))
        self.Dialog.setInputMethodHints(QtCore.Qt.ImhNone)
        self.gridLayout = QtWidgets.QGridLayout(self.Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_companyName = QtWidgets.QLabel(self.Dialog)
        self.lbl_companyName.setObjectName("lbl_companyName")
        self.gridLayout.addWidget(self.lbl_companyName, 0, 0, 1, 1)
        self.lineEdit_companyName = QtWidgets.QLineEdit(self.Dialog)
        self.lineEdit_companyName.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lineEdit_companyName.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit_companyName.setObjectName("lineEdit_companyName")
        self.gridLayout.addWidget(self.lineEdit_companyName, 0, 1, 1, 1)
        self.lbl_comapnyLogo = QtWidgets.QLabel(self.Dialog)
        self.lbl_comapnyLogo.setObjectName("lbl_comapnyLogo")
        self.gridLayout.addWidget(self.lbl_comapnyLogo, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_browse = QtWidgets.QPushButton(self.Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_browse.sizePolicy().hasHeightForWidth())
        self.btn_browse.setSizePolicy(sizePolicy)
        self.btn_browse.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btn_browse.setObjectName("btn_browse")
        self.horizontalLayout.addWidget(self.btn_browse)
        self.lbl_browse = QtWidgets.QLabel(self.Dialog)
        self.lbl_browse.setMouseTracking(True)
        self.lbl_browse.setAcceptDrops(True)
        self.lbl_browse.setText("")
        self.lbl_browse.setObjectName("lbl_browse")
        self.horizontalLayout.addWidget(self.lbl_browse)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.lbl_groupName = QtWidgets.QLabel(self.Dialog)
        self.lbl_groupName.setObjectName("lbl_groupName")
        self.gridLayout.addWidget(self.lbl_groupName, 2, 0, 1, 1)
        self.lineEdit_groupName = QtWidgets.QLineEdit(self.Dialog)
        self.lineEdit_groupName.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit_groupName.setCursorPosition(0)
        self.lineEdit_groupName.setObjectName("lineEdit_groupName")
        self.gridLayout.addWidget(self.lineEdit_groupName, 2, 1, 1, 1)
        self.lbl_designer = QtWidgets.QLabel(self.Dialog)
        self.lbl_designer.setObjectName("lbl_designer")
        self.gridLayout.addWidget(self.lbl_designer, 3, 0, 1, 1)
        self.lineEdit_designer = QtWidgets.QLineEdit(self.Dialog)
        self.lineEdit_designer.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit_designer.setObjectName("lineEdit_designer")
        self.gridLayout.addWidget(self.lineEdit_designer, 3, 1, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.formLayout.setObjectName("formLayout")
        self.btn_useProfile = QtWidgets.QPushButton(self.Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_useProfile.sizePolicy().hasHeightForWidth())
        self.btn_useProfile.setSizePolicy(sizePolicy)
        self.btn_useProfile.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btn_useProfile.setObjectName("btn_useProfile")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.btn_useProfile)
        self.btn_saveProfile = QtWidgets.QPushButton(self.Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_saveProfile.sizePolicy().hasHeightForWidth())
        self.btn_saveProfile.setSizePolicy(sizePolicy)
        self.btn_saveProfile.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btn_saveProfile.setObjectName("btn_saveProfile")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.btn_saveProfile)
        self.gridLayout.addLayout(self.formLayout, 4, 1, 1, 1)
        self.lbl_projectTitle = QtWidgets.QLabel(self.Dialog)
        self.lbl_projectTitle.setObjectName("lbl_projectTitle")
        self.gridLayout.addWidget(self.lbl_projectTitle, 5, 0, 1, 1)
        self.lineEdit_projectTitle = QtWidgets.QLineEdit(self.Dialog)
        self.lineEdit_projectTitle.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit_projectTitle.setObjectName("lineEdit_projectTitle")
        self.gridLayout.addWidget(self.lineEdit_projectTitle, 5, 1, 1, 1)
        self.lbl_subtitle = QtWidgets.QLabel(self.Dialog)
        self.lbl_subtitle.setObjectName("lbl_subtitle")
        self.gridLayout.addWidget(self.lbl_subtitle, 6, 0, 1, 1)
        self.lineEdit_subtitle = QtWidgets.QLineEdit(self.Dialog)
        self.lineEdit_subtitle.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit_subtitle.setText("")
        self.lineEdit_subtitle.setObjectName("lineEdit_subtitle")
        self.gridLayout.addWidget(self.lineEdit_subtitle, 6, 1, 1, 1)
        self.lbl_jobNumber = QtWidgets.QLabel(self.Dialog)
        self.lbl_jobNumber.setObjectName("lbl_jobNumber")
        self.gridLayout.addWidget(self.lbl_jobNumber, 7, 0, 1, 1)
        self.lineEdit_jobNumber = QtWidgets.QLineEdit(self.Dialog)
        self.lineEdit_jobNumber.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit_jobNumber.setObjectName("lineEdit_jobNumber")
        self.gridLayout.addWidget(self.lineEdit_jobNumber, 7, 1, 1, 1)
        self.lbl_client = QtWidgets.QLabel(self.Dialog)
        self.lbl_client.setObjectName("lbl_client")
        self.gridLayout.addWidget(self.lbl_client, 8, 0, 1, 1)
        self.lineEdit_client = QtWidgets.QLineEdit(self.Dialog)
        self.lineEdit_client.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit_client.setObjectName("lineEdit_client")
        self.gridLayout.addWidget(self.lineEdit_client, 8, 1, 1, 1)
        self.lbl_addComment = QtWidgets.QLabel(self.Dialog)
        self.lbl_addComment.setObjectName("lbl_addComment")
        self.gridLayout.addWidget(self.lbl_addComment, 9, 0, 1, 1)
        self.txt_additionalComments = QtWidgets.QTextEdit(self.Dialog)
        self.txt_additionalComments.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.txt_additionalComments.setStyleSheet("  QTextCursor textCursor;\n"
                                                  "  textCursor.setPosistion(0, QTextCursor::MoveAnchor); \n"
                                                  "  textedit->setTextCursor( textCursor );")
        self.txt_additionalComments.setInputMethodHints(QtCore.Qt.ImhNone)
        self.txt_additionalComments.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.txt_additionalComments.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.txt_additionalComments.setTabChangesFocus(False)
        self.txt_additionalComments.setReadOnly(False)
        self.txt_additionalComments.setObjectName("txt_additionalComments")
        self.gridLayout.addWidget(self.txt_additionalComments, 9, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 10, 1, 1, 1)

        self.retranslateUi()

        # self.buttonBox.accepted.connect(self.Dialog.accept)
        self.buttonBox.accepted.connect(lambda: self.save_inputSummary(main))
        self.buttonBox.rejected.connect(self.Dialog.reject)
        self.btn_browse.clicked.connect(self.lbl_browse.clear)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)
        self.Dialog.setTabOrder(self.lineEdit_companyName, self.btn_browse)
        self.Dialog.setTabOrder(self.btn_browse, self.lineEdit_groupName)
        self.Dialog.setTabOrder(self.lineEdit_groupName, self.lineEdit_designer)
        self.Dialog.setTabOrder(self.lineEdit_designer, self.btn_useProfile)
        self.Dialog.setTabOrder(self.btn_useProfile, self.btn_saveProfile)
        self.Dialog.setTabOrder(self.btn_saveProfile, self.lineEdit_projectTitle)
        self.Dialog.setTabOrder(self.lineEdit_projectTitle, self.lineEdit_subtitle)
        self.Dialog.setTabOrder(self.lineEdit_subtitle, self.lineEdit_jobNumber)
        self.Dialog.setTabOrder(self.lineEdit_jobNumber, self.lineEdit_client)
        self.Dialog.setTabOrder(self.lineEdit_client, self.txt_additionalComments)
        self.Dialog.setTabOrder(self.txt_additionalComments, self.buttonBox)

    def save_inputSummary(self, main):
        input_summary = self.getPopUpInputs()  # getting all inputs entered by user in PopUp dialog box.
        file_type = "PDF (*.pdf)"
        # filename, _ = QFileDialog.getSaveFileName(QFileDialog(), "Save File As", os.path.join(str(' '), "untitled.pdf"),
        #                                           file_type)
        filename, _ = QFileDialog.getSaveFileName(self.Dialog, "Save File As", '', file_type, None, QtWidgets.QFileDialog.DontUseNativeDialog)
        # filename, _ = QFileDialog.getSaveFileName(self.Dialog, "Save File As", '', file_type)
        '''
        Uncomment the third QFileDialog function if you want to use NativeDialog which will be both system and OS dependent hence
        it would be impossible to assign any modal to QFileDialog once it's opened, therefore it'll look like system is hanged.
        But if you want to control the behaviour of QFileDialog according to your need then use the second function(QFileDialog provided by Qt which is faster than NativeDialog).

        Same is the case when we'll select 'Load Input' option. We can't control the behaviour of QFileDialog because it's native and hence
        OS and system dependent.
        '''

        if filename == '':
            return
        # else:
        #     self.create_pdf_file(filename,main, input_summary)
        #     self.pdf_file_message(filename)

        loading_widget = QDialog(self.module_window)
        window_width = self.module_window.width() // 2
        window_height = self.module_window.height() // 10
        loading_widget.setFixedSize(window_width, int(1.5 * window_height))
        loading_widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.progress_bar = QtWidgets.QProgressBar(loading_widget)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setGeometry(QtCore.QRect(0, 0, window_width, window_height // 2))
        loading_label = QtWidgets.QLabel(loading_widget)
        loading_label.setGeometry(QtCore.QRect(0, window_height // 2, window_width, window_height))
        loading_label.setFixedSize(window_width, window_height)
        loading_label.setAlignment(QtCore.Qt.AlignCenter)
        loading_label.setText("<p style='font-weight:500'>Please Wait...</p>")
        self.thread_1 = DummyThread(0.00001, self.module_window)
        self.thread_1.start()
        self.thread_2 = DummyThread(0.00001, self.module_window)
        self.thread_1.finished.connect(lambda: loading_widget.exec())
        self.thread_1.finished.connect(lambda: self.progress_bar.setValue(20))
        self.thread_1.finished.connect(lambda: self.thread_2.start())
        self.thread_2.finished.connect(lambda: self.create_pdf_file(filename, main, input_summary))
        self.thread_2.finished.connect(lambda: loading_widget.close())
        self.thread_2.finished.connect(lambda: self.progress_bar.setValue(90))
        self.thread_2.finished.connect(lambda: self.pdf_file_message(filename))

    def create_pdf_file(self, filename, main, input_summary):
        fname_no_ext = filename.split(".")[0]
        input_summary['filename'] = fname_no_ext
        input_summary['does_design_exist'] = self.design_exist
        input_summary['logger_messages'] = self.loggermsg
        # self.progress_bar.setValue(30)
        main.save_design(main, input_summary)
        # self.progress_bar.setValue(80)

    def pdf_file_message(self, filename):
        """Handle PDF generation completion and display appropriate message"""
        try:
            # **FIX**: Determine the correct UI object reference
            ui_ref = None
            if hasattr(self, 'ui') and self.ui:
                ui_ref = self.ui
            elif hasattr(self, 'lblmessage'):
                ui_ref = self  # self is the UI object directly
            else:
                print("Could not find UI reference")
                return

            # **FIX**: Handle encoding issues when reading log file
            logfile_path = filename + '.log'
            logs = ""
            
            if os.path.exists(logfile_path):
                # Try multiple encoding strategies to handle LaTeX log files
                encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                
                for encoding in encodings_to_try:
                    try:
                        with open(logfile_path, 'r', encoding=encoding) as logfile:
                            logs = logfile.read()
                        print(f"Successfully read log file with {encoding} encoding")
                        break
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error reading with {encoding}: {e}")
                        continue
                else:
                    # If all encodings fail, try with error handling
                    try:
                        with open(logfile_path, 'r', encoding='utf-8', errors='ignore') as logfile:
                            logs = logfile.read()
                        print("Read log file with UTF-8 and ignored decode errors")
                    except Exception as e:
                        print(f"Final fallback failed: {e}")
                        logs = "Could not read log file due to encoding issues"
            else:
                logs = "Log file not found"
                print(f"Log file not found: {logfile_path}")

            # Check for LaTeX errors in the log content
            has_latex_error = False
            has_fatal_error = False
            
            if logs:
                # Check for various types of LaTeX errors
                error_indicators = [
                    "LaTeX Error:",
                    "! LaTeX Error:",
                    "Fatal error occurred",
                    "Emergency stop",
                    "! ==> Fatal error occurred",
                    "Runaway argument",
                    "! Undefined control sequence",
                    "! Missing $ inserted",
                    "! File ended while scanning"
                ]
                
                for error in error_indicators:
                    if error in logs:
                        has_latex_error = True
                        if "Fatal" in error or "Emergency stop" in error:
                            has_fatal_error = True
                        break

            # Check if PDF was actually generated regardless of log errors
            pdf_file_path = filename + '.pdf'
            pdf_exists = os.path.exists(pdf_file_path)
            
            # Determine the appropriate message
            if pdf_exists:
                if has_fatal_error:
                    message = "<font color='orange'>PDF generated with warnings. Please check the output.</font>"
                elif has_latex_error:
                    message = "<font color='orange'>PDF generated successfully with some LaTeX warnings.</font>"
                else:
                    message = "<font color='green'>PDF generated successfully.</font>"
            else:
                # PDF not generated
                if has_latex_error or has_fatal_error:
                    message = "<font color='red'>ERROR: LaTeX file processing failed. PDF not generated.</font>"
                else:
                    message = "<font color='red'>ERROR: PDF generation failed for unknown reason.</font>"

            # **FIX**: Set message using the correct UI reference
            if hasattr(ui_ref, 'lblmessage'):
                ui_ref.lblmessage.setText(message)
            elif hasattr(ui_ref, 'label') and hasattr(ui_ref.label, 'setText'):
                ui_ref.label.setText(message)
            else:
                print(f"Message would be: {message}")

            # **FIX**: Enable/disable buttons using correct UI reference
            if pdf_exists:
                # Enable view buttons if they exist
                for btn_name in ['btn_viewPDF', 'pushButton_3', 'pushButton_view']:
                    if hasattr(ui_ref, btn_name):
                        getattr(ui_ref, btn_name).setEnabled(True)
            else:
                # Disable view buttons
                for btn_name in ['btn_viewPDF', 'pushButton_3', 'pushButton_view']:
                    if hasattr(ui_ref, btn_name):
                        getattr(ui_ref, btn_name).setEnabled(False)

            # Update progress bar if it exists
            for progress_name in ['progressBar', 'progress']:
                if hasattr(ui_ref, progress_name):
                    getattr(ui_ref, progress_name).setValue(100)
                    break

            # Enable close buttons
            for btn_name in ['btn_close', 'buttonBox']:
                if hasattr(ui_ref, btn_name):
                    getattr(ui_ref, btn_name).setEnabled(True)

            print(f"PDF exists: {pdf_exists}")
            print(f"Has LaTeX error: {has_latex_error}")
            print(f"Has fatal error: {has_fatal_error}")

        except Exception as e:
            print(f"Error in pdf_file_message: {e}")
            import traceback
            traceback.print_exc()
            
            # Fallback message
            pdf_file_path = filename + '.pdf'
            if os.path.exists(pdf_file_path):
                message = "<font color='green'>PDF generated successfully.</font>"
            else:
                message = "<font color='red'>ERROR: Could not determine PDF generation status.</font>"
            
            # Try to set message with fallback approach
            try:
                if hasattr(self, 'lblmessage'):
                    self.lblmessage.setText(message)
                elif hasattr(self, 'ui') and hasattr(self.ui, 'lblmessage'):
                    self.ui.lblmessage.setText(message)
                else:
                    print(f"Fallback message: {message}")
            except:
                print(f"Could not set UI message: {message}")

    def call_designreport(self, main, fileName, report_summary, folder):
        self.alist = main.report_input
        self.column_details = main.report_supporting
        self.beam_details = main.report_supported
        self.result = main.report_result
        self.Design_Check = main.report_check
        # save_html(main.report_result, main.report_input, main.report_check, main.report_supporting,main.report_supported, report_summary,fileName, folder)
        # CreateLatex.\
        #     save_latex(CreateLatex(),main.report_result, main.report_input, main.report_check, main.report_supporting,
        #           main.report_supported, report_summary, fileName, folder)

    def getPopUpInputs(self):
        input_summary = {}
        input_summary["ProfileSummary"] = {}
        input_summary["ProfileSummary"]["CompanyName"] = str(self.lineEdit_companyName.text())
        input_summary["ProfileSummary"]["CompanyLogo"] = str(self.lbl_browse.text())
        input_summary["ProfileSummary"]["Group/TeamName"] = str(self.lineEdit_groupName.text())
        input_summary["ProfileSummary"]["Designer"] = str(self.lineEdit_designer.text())

        input_summary["ProjectTitle"] = str(self.lineEdit_projectTitle.text())
        input_summary["Subtitle"] = str(self.lineEdit_subtitle.text())
        input_summary["JobNumber"] = str(self.lineEdit_jobNumber.text())
        input_summary["AdditionalComments"] = str(self.txt_additionalComments.toPlainText())
        input_summary["Client"] = str(self.lineEdit_client.text())

        return input_summary

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Design Report Summary"))
        self.lbl_companyName.setText(_translate("Dialog", "Company Name :"))
        self.lbl_comapnyLogo.setText(_translate("Dialog", "Company Logo :"))
        self.btn_browse.setText(_translate("Dialog", "Browse..."))
        self.lbl_groupName.setText(_translate("Dialog", "Group/Team Name :"))
        self.lbl_designer.setText(_translate("Dialog", "Designer :"))
        self.btn_useProfile.setText(_translate("Dialog", "Use Profile"))
        self.btn_saveProfile.setText(_translate("Dialog", "Save Profile"))
        self.lbl_projectTitle.setText(_translate("Dialog", "Project Title :"))
        self.lbl_subtitle.setText(_translate("Dialog", "Subtitle :"))
        self.lineEdit_subtitle.setPlaceholderText(_translate("Dialog", "(Optional)"))
        self.lbl_jobNumber.setText(_translate("Dialog", "Job Number :"))
        self.lbl_client.setText(_translate("Dialog", "Client :"))
        self.lbl_addComment.setText(_translate("Dialog", "Additional Comments :"))
        self.txt_additionalComments.setHtml(_translate("Dialog",
                                                       "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                       "p, li { white-space: pre-wrap; }\n"
                                                       "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.5pt; font-weight:400; font-style:normal;\">\n"
                                                       "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:11pt;\"><br /></p></body></html>"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog1()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())