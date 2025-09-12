from PySide6.QtWidgets import (QPushButton, QLabel, QDialog, QGridLayout, QLineEdit, QHBoxLayout, QTextEdit, QFrame, QDialogButtonBox,QFileDialog,
                               QMainWindow, QApplication, QSizePolicy, QFormLayout, QLayout, QProgressBar,
                               QWidget, QVBoxLayout, QSizeGrip)
from PySide6.QtCore import (QRect, QMetaObject, QCoreApplication, QSize, QThread, Signal)
from PySide6.QtGui import Qt, QGuiApplication, QCursor
from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_gui.ui.components.dialogs.custom_messagebox import CustomMessageBox, MessageBoxType
from osdag_gui.ui.components.dialogs.loading_popup import ModernLoadingDialog, DelayThread

import time,os,yaml

import shutil
import tempfile

# NEW: Conditional import for customization dialog
try:
    from osdag_gui.ui.components.dialogs.customized_report_popup import show_customization_dialog
    CUSTOMIZATION_DIALOG_AVAILABLE = True
except ImportError:
    show_customization_dialog = None
    CUSTOMIZATION_DIALOG_AVAILABLE = False

# Dialog to capture company details before save design report
class DesignSummaryPopup(QDialog):
    saveInputFinished = Signal()
    def __init__(self, design_exist, loggermsg, parent=None):
        self.parent = parent
        super().__init__(parent=parent)
        self.design_exist = design_exist
        self.loggermsg = loggermsg

    # It is a general function that can set the dialog look similar and in osdag theme with custom Title bar.
    def setupWrapper(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setStyleSheet("""
            QDialog{ 
                background-color: white;
                border: 1px solid #90af13;
            }
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold; 
                border-radius: 5px;
                border: 1px solid black;
                padding: 5px 14px;
                text-align: center;
                font-family: "Calibri";
            }
            QPushButton:hover {
                background-color: #90AF13;
                border: 1px solid #90AF13;
                color: white;
            }
            QPushButton:pressed {
                color: black;
                background-color: white;
                border: 1px solid black;
            }
            QLineEdit,QTextEdit {
                padding: 2px 7px;
                border: 1px solid #A6A6A6;
                border-radius: 4px;
                background-color: white;
                color: #000000;
                font-weight: normal;
            }
        """) 
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)
        self.title_bar = CustomTitleBar()
        main_layout.addWidget(self.title_bar)
        self.content_widget = QWidget(self)
        main_layout.addWidget(self.content_widget, 1)
        size_grip = QSizeGrip(self)
        size_grip.setFixedSize(16, 16)
        overlay = QHBoxLayout()
        overlay.setContentsMargins(0, 0, 4, 4)
        overlay.addStretch(1)
        overlay.addWidget(size_grip, 0, Qt.AlignBottom | Qt.AlignRight)
        main_layout.addLayout(overlay)

    # root is the top level of parent, that is the QMainWindow
    def setupUi(self, main=None, module_window=None):
        self.setupWrapper()

        self.module_window = module_window
        self.folder = module_window.parent.folder
        self.setObjectName("Dialog")
        self.resize(int(600), int(550))

        # Adopt visual style from parent main window if provided
        if self.module_window is not None:
            try:
                self.setPalette(self.module_window.palette())
                self.setFont(self.module_window.font())
                if self.module_window.styleSheet():
                    self.setStyleSheet(self.module_window.styleSheet())
                if self.module_window.windowTitle():
                    self.setWindowTitle(self.module_window.windowTitle())
                try:
                    self.setWindowIcon(self.module_window.windowIcon())
                except Exception:
                    pass
            except Exception:
                pass

        self.setInputMethodHints(Qt.ImhNone)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_companyName = QLabel(self)
        self.lbl_companyName.setObjectName("lbl_companyName")
        self.gridLayout.addWidget(self.lbl_companyName, 0, 0, 1, 1)
        self.lineEdit_companyName = QLineEdit(self)
        self.lineEdit_companyName.setCursor(QCursor(Qt.ArrowCursor))
        self.lineEdit_companyName.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_companyName.setObjectName("lineEdit_companyName")
        self.gridLayout.addWidget(self.lineEdit_companyName, 0, 1, 1, 1)
        self.lbl_comapnyLogo = QLabel(self)
        self.lbl_comapnyLogo.setObjectName("lbl_comapnyLogo")
        self.gridLayout.addWidget(self.lbl_comapnyLogo, 1, 0, 1, 1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_browse = QPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_browse.sizePolicy().hasHeightForWidth())
        self.btn_browse.setSizePolicy(sizePolicy)
        self.btn_browse.setFocusPolicy(Qt.TabFocus)
        self.btn_browse.setObjectName("btn_browse")

        self.btn_browse.clicked.connect(lambda: self.getLogoFilePath(self.lbl_browse))

        self.horizontalLayout.addWidget(self.btn_browse)
        self.lbl_browse = QLabel(self)
        self.lbl_browse.setMouseTracking(True)
        self.lbl_browse.setAcceptDrops(True)
        self.lbl_browse.setText("")
        self.lbl_browse.setObjectName("lbl_browse")
        self.horizontalLayout.addWidget(self.lbl_browse)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.lbl_groupName = QLabel(self)
        self.lbl_groupName.setObjectName("lbl_groupName")
        self.gridLayout.addWidget(self.lbl_groupName, 2, 0, 1, 1)
        self.lineEdit_groupName = QLineEdit(self)
        self.lineEdit_groupName.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_groupName.setCursorPosition(0)
        self.lineEdit_groupName.setObjectName("lineEdit_groupName")
        self.gridLayout.addWidget(self.lineEdit_groupName, 2, 1, 1, 1)
        self.lbl_designer = QLabel(self)
        self.lbl_designer.setObjectName("lbl_designer")
        self.gridLayout.addWidget(self.lbl_designer, 3, 0, 1, 1)
        self.lineEdit_designer = QLineEdit(self)
        self.lineEdit_designer.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_designer.setObjectName("lineEdit_designer")
        self.gridLayout.addWidget(self.lineEdit_designer, 3, 1, 1, 1)
        self.formLayout = QFormLayout()
        self.formLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.formLayout.setObjectName("formLayout")
        self.btn_useProfile = QPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_useProfile.sizePolicy().hasHeightForWidth())
        self.btn_useProfile.setSizePolicy(sizePolicy)
        self.btn_useProfile.setFocusPolicy(Qt.TabFocus)
        self.btn_useProfile.setObjectName("btn_useProfile")

        self.btn_useProfile.clicked.connect(self.useUserProfile)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.btn_useProfile)
        self.btn_saveProfile = QPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_saveProfile.sizePolicy().hasHeightForWidth())
        self.btn_saveProfile.setSizePolicy(sizePolicy)
        self.btn_saveProfile.setFocusPolicy(Qt.TabFocus)
        self.btn_saveProfile.setObjectName("btn_saveProfile")

        self.btn_saveProfile.clicked.connect(self.saveUserProfile)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.btn_saveProfile)
        self.gridLayout.addLayout(self.formLayout, 4, 1, 1, 1)
        self.lbl_projectTitle = QLabel(self)
        self.lbl_projectTitle.setObjectName("lbl_projectTitle")
        self.gridLayout.addWidget(self.lbl_projectTitle, 5, 0, 1, 1)
        self.lineEdit_projectTitle = QLineEdit(self)
        self.lineEdit_projectTitle.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_projectTitle.setObjectName("lineEdit_projectTitle")
        self.gridLayout.addWidget(self.lineEdit_projectTitle, 5, 1, 1, 1)
        self.lbl_subtitle = QLabel(self)
        self.lbl_subtitle.setObjectName("lbl_subtitle")
        self.gridLayout.addWidget(self.lbl_subtitle, 6, 0, 1, 1)
        self.lineEdit_subtitle = QLineEdit(self)
        self.lineEdit_subtitle.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_subtitle.setText("")
        self.lineEdit_subtitle.setObjectName("lineEdit_subtitle")
        self.gridLayout.addWidget(self.lineEdit_subtitle, 6, 1, 1, 1)
        self.lbl_jobNumber = QLabel(self)
        self.lbl_jobNumber.setObjectName("lbl_jobNumber")
        self.gridLayout.addWidget(self.lbl_jobNumber, 7, 0, 1, 1)
        self.lineEdit_jobNumber = QLineEdit(self)
        self.lineEdit_jobNumber.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_jobNumber.setObjectName("lineEdit_jobNumber")
        self.gridLayout.addWidget(self.lineEdit_jobNumber, 7, 1, 1, 1)
        self.lbl_client = QLabel(self)
        self.lbl_client.setObjectName("lbl_client")
        self.gridLayout.addWidget(self.lbl_client, 8, 0, 1, 1)
        self.lineEdit_client = QLineEdit(self)
        self.lineEdit_client.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_client.setObjectName("lineEdit_client")
        self.gridLayout.addWidget(self.lineEdit_client, 8, 1, 1, 1)
        self.lbl_addComment = QLabel(self)
        self.lbl_addComment.setObjectName("lbl_addComment")
        self.gridLayout.addWidget(self.lbl_addComment, 9, 0, 1, 1)
        self.txt_additionalComments = QTextEdit(self)
        self.txt_additionalComments.setFocusPolicy(Qt.StrongFocus)
        self.txt_additionalComments.setStyleSheet("  QTextCursor textCursor;\n"
                                                  "  textCursor.setPosistion(0, QTextCursor::MoveAnchor); \n"
                                                  "  textedit->setTextCursor( textCursor );")
        self.txt_additionalComments.setInputMethodHints(Qt.ImhNone)
        self.txt_additionalComments.setFrameShape(QFrame.WinPanel)
        self.txt_additionalComments.setFrameShadow(QFrame.Sunken)
        self.txt_additionalComments.setTabChangesFocus(False)
        self.txt_additionalComments.setReadOnly(False)
        self.txt_additionalComments.setObjectName("txt_additionalComments")
        self.gridLayout.addWidget(self.txt_additionalComments, 9, 1, 1, 1)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 10, 1, 1, 1)

        self.retranslateUi()

        # self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.accepted.connect(lambda: self.save_inputSummary(main))
        self.buttonBox.rejected.connect(self.reject)
        self.btn_browse.clicked.connect(self.lbl_browse.clear)
        QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.lineEdit_companyName, self.btn_browse)
        self.setTabOrder(self.btn_browse, self.lineEdit_groupName)
        self.setTabOrder(self.lineEdit_groupName, self.lineEdit_designer)
        self.setTabOrder(self.lineEdit_designer, self.btn_useProfile)
        self.setTabOrder(self.btn_useProfile, self.btn_saveProfile)
        self.setTabOrder(self.btn_saveProfile, self.lineEdit_projectTitle)
        self.setTabOrder(self.lineEdit_projectTitle, self.lineEdit_subtitle)
        self.setTabOrder(self.lineEdit_subtitle, self.lineEdit_jobNumber)
        self.setTabOrder(self.lineEdit_jobNumber, self.lineEdit_client)
        self.setTabOrder(self.lineEdit_client, self.txt_additionalComments)
        self.setTabOrder(self.txt_additionalComments, self.buttonBox)

        # ------Part-of-wrapper-Setup--------
        # Add this widget to content
        self.content_widget.setLayout(self.gridLayout)

    # def start_thread(self, main):
    #     self.thread_1 = DelayThread()
    #     self.thread_2 = DelayThread()
    
    #     self.loading = ModernLoadingDialog()
    #     self.setEnabled(False)
    #     self.loading.show()
    #     self.thread_1.start()
    #     self.thread_1.finished.connect(lambda: self.save_inputSummary(main))

    # def finished_loading(self):
    #     self.thread_2.start()
    #     self.thread_2.finished.connect(self.loading_close)

    # def loading_close(self):
    #     self.loading.close()
    #     self.setEnabled(True)

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

        self.create_pdf_file(filename, main, input_summary)
        self.tex_file_message(filename, main, input_summary)

        # call loading finished
        if self.finished_loading:
            self.finished_loading()

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
        main.save_design(input_summary)

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
            self.reject()
            CustomMessageBox(
                title="Error",
                text="Error generating initial LaTeX file. Please check the console for details.",
                dialogType=MessageBoxType.Critical
            ).exec()
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
                self, "Save PDF Report As", '', file_type, None,
                QFileDialog.DontUseNativeDialog
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
                self.reject()
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

                    self.accept()
                    CustomMessageBox(
                        title="Success",
                        text=f'PDF report saved successfully to:\n{pdf_filename}',
                        dialogType=MessageBoxType.Success
                    ).exec()
                else:
                    # Check for errors in pdflatex output
                    if result.stderr:
                        print(f"ERROR: pdflatex stderr: {result.stderr}")
                    if result.stdout:
                        print(f"INFO: pdflatex stdout: {result.stdout}")

                    self.reject()
                    CustomMessageBox(
                        title="Error",
                        text='Failed to generate PDF. Please check if LaTeX is installed and the LaTeX file is valid.',
                        dialogType=MessageBoxType.Critical
                    ).exec()

            except subprocess.TimeoutExpired:
                self.reject()
                CustomMessageBox(
                    title="Error",
                    text='PDF generation timed out. The LaTeX file may have errors.',
                    dialogType=MessageBoxType.Critical
                ).exec()
            except FileNotFoundError:
                self.reject()
                CustomMessageBox(
                    title="Error",
                    text='LaTeX (pdflatex) not found. Please install a LaTeX distribution like MiKTeX or TeX Live.',
                    dialogType=MessageBoxType.Critical
                ).exec()
            except Exception as e:
                self.reject()
                CustomMessageBox(
                    title="Error",
                    text=f'Error generating PDF: {str(e)}',
                    dialogType=MessageBoxType.Critical
                ).exec()
            return

        # LAUNCH CUSTOMIZATION DIALOG if available
        if CUSTOMIZATION_DIALOG_AVAILABLE:
            # Prepare data for customization dialog
            main.report_input = getattr(main, 'report_input', {})
            main.report_input['filename'] = fname_no_ext
            main.report_input['temp_dir'] = os.path.dirname(fname_no_ext)  # Store for cleanup

            # Open the customization dialog
            show_customization_dialog(main, parent=self.parent)

            # AUTOMATIC CLEANUP of temporary files
            temp_dir = main.report_input.get('temp_dir')
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    print(f"INFO: Cleaned up temp directory: {temp_dir}")
                except Exception as e:
                    print(f"WARNING: Could not clean up temp directory {temp_dir}: {e}")

            self.accept()
        else:
            # FALLBACK: Show message if customization not available
            self.accept()
            CustomMessageBox(
                title="Success",
                text=f'LaTeX file generated successfully at {fname_no_ext}.tex. Report customization not available.',
                dialogType=MessageBoxType.Success
            ).exec()

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
    
    def saveUserProfile(self):
        inputData = self.getPopUpInputs()
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Files',
                                                  os.path.join(str(self.folder), "Profile"), '*.txt')
        if filename == '':
            return False
        else:
            infile = open(filename, 'w')
            yaml.dump(inputData, infile)
            infile.close()

    def useUserProfile(self):

        filename, _ = QFileDialog.getOpenFileName(self, 'Open Files',
                                                  os.path.join(str(self.folder), "Profile"),
                                                  '*.txt')
        if os.path.isfile(filename):
            outfile = open(filename, 'r')
            reportsummary = yaml.safe_load(outfile)
            self.summary_popup.lineEdit_companyName.setText(reportsummary["ProfileSummary"]['CompanyName'])
            self.summary_popup.lbl_browse.setText(reportsummary["ProfileSummary"]['CompanyLogo'])
            self.summary_popup.lineEdit_groupName.setText(reportsummary["ProfileSummary"]['Group/TeamName'])
            self.summary_popup.lineEdit_designer.setText(reportsummary["ProfileSummary"]['Designer'])

    def getLogoFilePath(self, lblwidget):

        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", os.path.join(str(' '), ''), "InputFiles(*.png *.svg *.jpg)")
        if filename == '':
            return False
        else:
            lblwidget.setText(str(filename))
        return str(filename)

    def retranslateUi(self):
        _translate = QCoreApplication.translate

        # ------Part-of-wrapper-Setup--------
        # Set title
        self.title_bar.setTitle(_translate("Dialog", "Design Report Summary"))

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
