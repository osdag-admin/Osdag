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
import shutil
import tempfile

# NEW: Conditional import for customization dialog
try:
    from .ui_report_customization_popup import show_customization_dialog
    CUSTOMIZATION_DIALOG_AVAILABLE = True
except ImportError:
    show_customization_dialog = None
    CUSTOMIZATION_DIALOG_AVAILABLE = False

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
        """
        MAIN FUNCTION: Process user inputs and generate customizable report.

        WORKFLOW:
        1. Collect user inputs from dialog form
        2. Create temporary directory for LaTeX file processing
        3. Show loading animation while generating LaTeX
        4. Launch customization dialog for section selection
        5. Clean up temporary files when done

        CHANGES MADE:
        - REMOVED: File save dialog (user no longer prompted for location)
        - ADDED: Automatic temporary directory creation
        - ADDED: Automatic cleanup after customization dialog closes

        Args:
            main: Main application object containing design data

        """
        # Get all user inputs from the dialog form
        input_summary = self.getPopUpInputs()

        # CREATE TEMPORARY WORKSPACE - No user prompt needed
        temp_dir = tempfile.mkdtemp(prefix='osdag_report_')
        filename = os.path.join(temp_dir, "report.tex")

        print(f"INFO: Using temporary location for LaTeX file: {filename}")

        # LOADING ANIMATION SETUP (unchanged from original)
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
        self.thread_2.finished.connect(lambda: self.tex_file_message(filename, main, input_summary))

    def create_pdf_file(self, filename, main, input_summary):
        """
        Generate LaTeX file (not PDF) for customization.

        This method creates the initial LaTeX file that will be customized
        in the next step.
        """
        fname_no_ext = filename.split(".")[0]
        input_summary['filename'] = fname_no_ext
        input_summary['does_design_exist'] = self.design_exist
        input_summary['logger_messages'] = self.loggermsg
        # Generate LaTeX file instead of PDF
        main.save_design(main, input_summary)

    def tex_file_message(self, filename, main, input_summary):
        """
        INTEGRATION POINT: Launch customization dialog after LaTeX generation.

        This function is called after the LaTeX file is successfully generated.
        It launches our custom report customization dialog and handles cleanup.

        CHANGES MADE:
        - REPLACED: Old section selection dialog with new customization interface
        - ADDED: Automatic temp directory cleanup after dialog closes
        - ADDED: Better error handling and user feedback

        Args:
            filename (str): Path to generated LaTeX file
            main: Main application object
            input_summary (dict): User inputs from dialog
        """
        fname_no_ext = filename.split(".")[0]

        # VERIFY LaTeX file was created successfully
        if not os.path.isfile(str(fname_no_ext + ".tex")):
            self.Dialog.reject()
            QMessageBox.critical(self.Dialog, 'Error',
                                'Error generating initial LaTeX file. Please check the console for details.')
            return

        # CHECK FOR NON-CAD MODULES that should bypass customization
        module_name = getattr(main, 'module', '')
        non_cad_modules = ['Butt Joint Bolted Connection', 'KEY_DISP_BUTTJOINTBOLTED']

        if any(name in str(module_name) for name in non_cad_modules):
            # BYPASS customization for non-CAD modules - use old workflow with PDF save
            print(f"INFO: Bypassing customization for non-CAD module: {module_name}")

            # Prompt user for PDF save location
            file_type = "PDF (*.pdf)"
            pdf_filename, _ = QFileDialog.getSaveFileName(
                self.Dialog, "Save PDF Report As", '', file_type, None,
                QtWidgets.QFileDialog.DontUseNativeDialog
            )

            if pdf_filename == '':
                # User cancelled - clean up and return
                temp_dir = os.path.dirname(fname_no_ext)
                if temp_dir and os.path.exists(temp_dir):
                    try:
                        shutil.rmtree(temp_dir, ignore_errors=True)
                        print(f"INFO: Cleaned up temp directory: {temp_dir}")
                    except Exception as e:
                        print(f"WARNING: Could not clean up temp directory {temp_dir}: {e}")
                self.Dialog.reject()
                return

            # Generate PDF directly using pdflatex
            try:
                import subprocess
                latex_dir = os.path.dirname(fname_no_ext)
                latex_file = fname_no_ext + ".tex"

                print(f"INFO: Generating PDF from {latex_file}")

                # Use only the filename (not full path) since we're setting cwd=latex_dir
                latex_filename = os.path.basename(latex_file)

                # Run pdflatex to generate PDF in the temp directory
                result = subprocess.run([
                    'pdflatex', '-interaction=nonstopmode',
                    latex_filename
                ], cwd=latex_dir, capture_output=True, text=True, timeout=60)

                # Look for PDF in the working directory (not using full path)
                pdf_filename_only = os.path.splitext(latex_filename)[0] + ".pdf"
                temp_pdf = os.path.join(latex_dir, pdf_filename_only)

                if os.path.exists(temp_pdf):
                    # Ensure the destination filename has .pdf extension
                    if not pdf_filename.lower().endswith('.pdf'):
                        pdf_filename += '.pdf'

                    # Copy the generated PDF to user's chosen location
                    shutil.copy2(temp_pdf, pdf_filename)
                    print(f"INFO: PDF copied to {pdf_filename}")

                    # Clean up temp directory
                    if latex_dir and os.path.exists(latex_dir):
                        shutil.rmtree(latex_dir, ignore_errors=True)
                        print(f"INFO: Cleaned up temp directory: {latex_dir}")

                    self.Dialog.accept()
                    QMessageBox.information(self.Dialog, 'Information',
                                          f'PDF report saved successfully to:\n{pdf_filename}')
                else:
                    # Check for errors in pdflatex output
                    if result.stderr:
                        print(f"ERROR: pdflatex stderr: {result.stderr}")
                    if result.stdout:
                        print(f"INFO: pdflatex stdout: {result.stdout}")

                    self.Dialog.reject()
                    QMessageBox.critical(self.Dialog, 'Error',
                                       'Failed to generate PDF. Please check if LaTeX is installed and the LaTeX file is valid.')

            except subprocess.TimeoutExpired:
                self.Dialog.reject()
                QMessageBox.critical(self.Dialog, 'Error',
                                   'PDF generation timed out. The LaTeX file may have errors.')
            except FileNotFoundError:
                self.Dialog.reject()
                QMessageBox.critical(self.Dialog, 'Error',
                                   'LaTeX (pdflatex) not found. Please install a LaTeX distribution like MiKTeX or TeX Live.')
            except Exception as e:
                self.Dialog.reject()
                QMessageBox.critical(self.Dialog, 'Error',
                                   f'Error generating PDF: {str(e)}')
            return

        # LAUNCH CUSTOMIZATION DIALOG if available
        if CUSTOMIZATION_DIALOG_AVAILABLE:
            # Prepare data for customization dialog
            main.report_input = getattr(main, 'report_input', {})
            main.report_input['filename'] = fname_no_ext
            main.report_input['temp_dir'] = os.path.dirname(fname_no_ext)  # Store for cleanup

            # Open the customization dialog
            show_customization_dialog(main, parent=self.Dialog)

            # AUTOMATIC CLEANUP of temporary files
            temp_dir = main.report_input.get('temp_dir')
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    print(f"INFO: Cleaned up temp directory: {temp_dir}")
                except Exception as e:
                    print(f"WARNING: Could not clean up temp directory {temp_dir}: {e}")

            self.Dialog.accept()
        else:
            # FALLBACK: Show message if customization not available
            self.Dialog.accept()
            QMessageBox.information(self.Dialog, 'Information',
                                    f'LaTeX file generated successfully at {fname_no_ext}.tex. Report customization not available.')

    def pdf_file_message(self, filename):
        fname_no_ext = filename.split(".")[0]
        # if os.path.isfile(str(filename)) and not os.path.isfile(fname_no_ext+'.log'):
        if os.path.isfile(str(filename.replace(".pdf", "") + ".pdf")) and not os.path.isfile(fname_no_ext + '.log'):
            self.Dialog.accept()
            QMessageBox.information(QMessageBox(), 'Information', 'Design report saved!')
        elif not os.path.isfile(str(filename.replace(".pdf", "") + ".pdf")) and not os.path.isfile(
                fname_no_ext + '.log'):
            self.Dialog.reject()
            QMessageBox.critical(QMessageBox(), 'Error',
                                 'Latex Creation Error. Please run <latex> in command prompt to check if latex is installed.')
        else:
            logfile = open(fname_no_ext + '.log', 'r')
            # TODO: This logic can be improved so that log is not read twice.
            logs = logfile.read()
            logfile.close()
            self.Dialog.reject()
            if (r'! I can\'t write on file' in logs):
                QMessageBox.critical(QMessageBox(), 'Error',
                                     'Please make sure no PDF is open with same name and try again.')
            else:
                missing_package = None
                log_lines = logs.split('\n')
                for line in log_lines:
                    if '! LaTeX Error: File' in line:
                        missing_package = line
                if missing_package != None:
                    QMessageBox.critical(QMessageBox(), 'Error', missing_package + ' Please install missing package')
                else:
                    QMessageBox.critical(QMessageBox(), 'Error',
                                         'Latex Creation Error. Please send us the log file created in the same folder choosen for the Design Report.')

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
