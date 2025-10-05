"""
Report Dialog - Combines Design Summary and Report Customization
"""

from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QStackedWidget, QLabel, QGridLayout, QLineEdit, QTextEdit,
    QFormLayout, QSizeGrip, QTreeWidget, QTreeWidgetItem,
    QFileDialog, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QCoreApplication
from PySide6.QtGui import QIcon, QCursor

from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_gui.ui.components.dialogs.custom_messagebox import CustomMessageBox, MessageBoxType

from osdag_gui.ui.components.design_report.design_summary import DesignSummaryWidget
from osdag_gui.ui.components.design_report.report_customization import CustomizationWidget

import os, sys
import tempfile
import shutil
import subprocess

try:
    from osdag_core.Common import PDFLATEX
except ImportError:
    # using systems pdflatex
    PDFLATEX = 'pdflatex'

class DesignReportDialog(QDialog):
    """Main dialog containing both widgets with navigation"""
    
    def __init__(self, backend, module_window, design_exist, loggermsg, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.module_window = module_window
        self.design_exist = design_exist
        self.loggermsg = loggermsg
        self.latex_content = None
        self.temp_dir = None
        self.latest_pdf = None
        
        # Get folder from module_window
        if module_window and hasattr(module_window, 'parent'):
            self.folder = module_window.parent.folder
        else:
            self.folder = ""
        
        self.setWindowIcon(QIcon(":/images/osdag_logo.png"))
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI with stacked widget"""
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.resize(550, 500)
        
        # Apply styling
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
            QLineEdit, QTextEdit {
                padding: 2px 7px;
                border: 1px solid #A6A6A6;
                border-radius: 4px;
                background-color: white;
                color: #000000;
                font-weight: normal;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)
        
        # Title bar
        self.title_bar = CustomTitleBar()
        self.title_bar.setTitle("Design Report")
        main_layout.addWidget(self.title_bar)
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        
        # Create pages
        self.summary_widget = DesignSummaryWidget(self)
        self.customization_widget = CustomizationWidget(self)
        
        self.stacked_widget.addWidget(self.summary_widget)
        self.stacked_widget.addWidget(self.customization_widget)
        
        content_layout.addWidget(self.stacked_widget)
        
        # Navigation buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(20, 10, 20, 20)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_next = QPushButton("Next")
        self.btn_back = QPushButton("Back")
        self.btn_finish = QPushButton("Finish")
        
        # Initially hide back and finish
        self.btn_back.hide()
        self.btn_finish.hide()
        
        # Connect buttons
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_next.clicked.connect(self.go_next)
        self.btn_back.clicked.connect(self.go_back)
        self.btn_finish.clicked.connect(self.finish_and_close)
        
        button_layout.addStretch()
        button_layout.addWidget(self.btn_back)
        button_layout.addWidget(self.btn_next)
        button_layout.addWidget(self.btn_finish)
        button_layout.addWidget(self.btn_cancel)
        
        content_layout.addLayout(button_layout)
        
        main_layout.addWidget(content_widget)
        
        # Size grip
        size_grip = QSizeGrip(self)
        size_grip.setFixedSize(16, 16)
        overlay = QHBoxLayout()
        overlay.setContentsMargins(0, 0, 4, 4)
        overlay.addStretch(1)
        overlay.addWidget(size_grip, 0, Qt.AlignBottom | Qt.AlignRight)
        main_layout.addLayout(overlay)
        
    def go_next(self):
        """Navigate to customization page"""
        # Get inputs from summary widget
        input_summary = self.summary_widget.get_inputs()
        
        # Create temp directory
        self.temp_dir = tempfile.mkdtemp(prefix='osdag_report_')
        filename = os.path.join(self.temp_dir, "report.tex")

        print(f"INFO: Temp dir initialized, {self.temp_dir}")

        # Generate LaTeX file
        self.generate_latex_file(filename, input_summary)
        
        # Verify LaTeX was created
        if not os.path.exists(filename):
            print(f"ERROR: {filename} Tex file not created.")
            CustomMessageBox(
                title="Error",
                text="Failed to generate LaTeX file",
                dialogType=MessageBoxType.Critical
            ).exec()
            return
        
        with open(filename, 'r', encoding='utf-8') as f:
            self.latex_content = f.read()

        # Load LaTeX content into customization widget
        self.customization_widget.load_latex_content(self.latex_content)
        
        # Switch to customization page
        self.stacked_widget.setCurrentIndex(1)
        self.title_bar.setTitle("Customize Report")
        
        # Update button visibility
        self.btn_next.hide()
        self.btn_back.show()
        self.btn_finish.show()
        
    def go_back(self):
        """Go back to summary page"""
        self.stacked_widget.setCurrentIndex(0)
        self.title_bar.setTitle("Design Report")
        
        # Update button visibility
        self.btn_next.show()
        self.btn_back.hide()
        self.btn_finish.hide()
    
    def generate_latex_file(self, filename, input_summary):
        """Generate LaTeX file using backend"""
        fname_no_ext = filename.split(".")[0]
        input_summary['filename'] = fname_no_ext
        input_summary['does_design_exist'] = self.design_exist
        input_summary['logger_messages'] = self.loggermsg
        
        # Call backend's save_design method
        self.backend.save_design(input_summary)
    
    def compile_pdf(self):
        """Compile filtered LaTeX to PDF"""
        if not self.latex_content:
            return None
            
        try:
            # Get selected sections
            selected = self.customization_widget.section_tree.get_selected_sections()
            
            # Filter content
            if hasattr(self.customization_widget, 'filter'):
                filtered_latex = self.customization_widget.filter.filter_content(
                    self.latex_content, selected
                )
            else:
                filtered_latex = self.latex_content
            
            # Use temp directory for compilation
            safe_temp_dir = os.path.join(tempfile.gettempdir(), "osdag_pdf_compile")
            if os.path.exists(safe_temp_dir):
                shutil.rmtree(safe_temp_dir, ignore_errors=True)
            os.makedirs(safe_temp_dir, exist_ok=True)
            
            # Write filtered LaTeX
            latex_file = os.path.join(safe_temp_dir, "filtered_report.tex")
            with open(latex_file, 'w', encoding='utf-8') as f:
                f.write(filtered_latex)
            
            pdf_file = latex_file.replace('.tex', '.pdf')
            
            # Run pdflatex
            result = subprocess.run(
                [PDFLATEX, '-interaction=nonstopmode', 'filtered_report.tex'],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=safe_temp_dir
            )

            if result.returncode != 0:
                print(f"ERROR: Return Code {result.returncode}")
            else:
                print(f"INFO: Compilation Successful, Return Code {result.returncode}")

            if os.path.exists(pdf_file):
                self.latest_pdf = pdf_file
                print(f"INFO: PDF Generated.")
                return pdf_file 
            

        except subprocess.TimeoutExpired:
            CustomMessageBox(
                title="Error",
                text='PDF generation timed out.',
                dialogType=MessageBoxType.Critical
            ).exec()

        except Exception as e:
            CustomMessageBox(
                title="Error",
                text=f"Failed to compile PDF: {e}",
                dialogType=MessageBoxType.Critical
            ).exec()
        
        return None
    
    def compile_and_open_pdf(self):
        """Compile filtered LaTeX and open PDF"""
        pdf_path = self.compile_pdf()
        if pdf_path and os.path.exists(pdf_path):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(pdf_path)
                elif sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', pdf_path])
                else:  # Linux
                    subprocess.run(['xdg-open', pdf_path])
            except Exception as e:
                CustomMessageBox(
                    title="Error",
                    text=f"Failed to open PDF: {e}",
                    dialogType=MessageBoxType.Warning
                ).exec()
        else:
            CustomMessageBox(
                title="No PDF",
                text="No PDF generated yet. Please compile first.",
                dialogType=MessageBoxType.Information
            ).exec()
    
    def compile_and_save_pdf(self):
        """Save the customized PDF"""
        pdf_path = self.compile_pdf()
        if not pdf_path:
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Customized Report", 
            "Osdag_Custom_Report.pdf", 
            "PDF files (*.pdf)"
        )
        
        if filename:
            shutil.copy2(pdf_path, filename)
            CustomMessageBox(
                title="Success",
                text=f"PDF saved successfully to:\n{filename}",
                dialogType=MessageBoxType.Success
            ).exec()
            self.accept()
    
    def finish_and_close(self):
        """Handle finish button - save PDF and close"""
        self.compile_and_save_pdf()
    
    def closeEvent(self, event):
        """Clean up temp files on close"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            except:
                pass
        
        # Also clean up compile directory
        safe_temp_dir = os.path.join(tempfile.gettempdir(), "osdag_pdf_compile")
        if os.path.exists(safe_temp_dir):
            try:
                shutil.rmtree(safe_temp_dir, ignore_errors=True)
            except:
                pass
        
        event.accept()
