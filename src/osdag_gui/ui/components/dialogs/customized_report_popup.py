"""
OSDAG Report Customization Dialog

PURPOSE:
This module provides a user-friendly interface for customizing engineering design reports.
Users can select which sections to include in their final PDF report.

WORKFLOW:
1. Parse existing LaTeX report file
2. Display sections/subsections in a tree view with checkboxes
3. Allow users to select which content to include
4. Filter LaTeX content based on selection
5. Compile customized PDF
6. Allow saving the final customized report

MAIN FEATURES:
- Tree-based section selection (no PDF preview for performance)
- Manual compile control (auto-compile disabled by default)
- Temporary file handling for clean workspace
- External PDF viewer integration
- Smart LaTeX filtering that preserves document structure

AUTHOR: Srinivas Raghav V C
"""

import os
import re
import tempfile
import subprocess
import shutil
import sys

# ==============================================================================
# Qt ENVIRONMENT SETUP - Fix platform plugin issues on different systems
# ==============================================================================

def setup_qt_environment():
    """
    Configure Qt environment to prevent platform plugin errors.

    This is especially important in conda environments where Qt plugins
    may not be in the expected location.
    """
    try:
        import PySide6
        pyside6_path = os.path.dirname(PySide6.__file__)

        # Common Qt plugin locations to search
        plugin_paths = [
            os.path.join(pyside6_path, 'Qt5', 'plugins'),
            os.path.join(pyside6_path, 'Qt', 'plugins'),
            os.path.join(pyside6_path, 'plugins'),
            os.path.join(pyside6_path, '..', 'qt5', 'plugins'),
        ]

        # Find and set the first valid plugin path
        for plugin_path in plugin_paths:
            if os.path.exists(plugin_path):
                os.environ['QT_PLUGIN_PATH'] = plugin_path
                if not os.environ.get('QT_QPA_PLATFORM_PLUGIN_PATH'):
                    print(f"INFO: Set QT_PLUGIN_PATH to {plugin_path}")
                break

    except Exception as e:
        print(f"WARNING: Could not setup Qt environment: {e}")


# ==============================================================================
# IMPORTS - PySide6 widgets and core functionality
# ==============================================================================

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QWidget,QSizeGrip,
                           QTreeWidget, QTreeWidgetItem, QPushButton, QLabel,
                           QCheckBox, QFileDialog)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

# ==============================================================================
# OSDAG IMPORTS - Try to import LaTeX generator
# ==============================================================================

try:
    from osdag_core.design_report.reportGenerator_latex import CreateLatex
    CREATELATEX_AVAILABLE = True
    print("INFO: CreateLatex successfully imported")
except ImportError:
    CreateLatex = None
    CREATELATEX_AVAILABLE = False
    print("WARNING: CreateLatex not available")
    CREATELATEX_AVAILABLE = False


# ==============================================================================
# CLASS: LaTeXParser - Extracts sections from LaTeX documents
# ==============================================================================

class LaTeXParser:
    """
    Parses LaTeX files to extract document structure.

    This class finds all \section{} and \subsection{} commands in a LaTeX
    document and organizes them into a hierarchical structure.

    Returns:
        dict: {section_name: [list_of_subsections]}
    """

    def parse_sections(self, latex_content):
        """
        Extract sections and subsections from LaTeX content.

        Args:
            latex_content (str): Raw LaTeX document content

        Returns:
            dict: Hierarchical structure of sections and subsections
        """
        sections = {}
        current_section = None

        # Process each line to find LaTeX section commands
        for line in latex_content.split('\n'):
            # Look for \section{Section Name} patterns
            section_match = re.search(r'\\section\{([^}]+)\}', line)
            if section_match:
                current_section = section_match.group(1).strip()
                sections[current_section] = []  # Initialize subsection list

            # Look for \subsection{Subsection Name} patterns
            subsection_match = re.search(r'\\subsection\{([^}]+)\}', line)
            if subsection_match and current_section:
                subsection = subsection_match.group(1).strip()
                sections[current_section].append(subsection)

        return sections


# ==============================================================================
# CLASS: SectionTreeWidget - Interactive tree for selecting report sections
# ==============================================================================

class SectionTreeWidget(QTreeWidget):
    """
    Custom tree widget for selecting report sections and subsections.

    Features:
    - Hierarchical display of sections and subsections
    - Checkbox selection with parent-child relationships
    - Automatic state updates (checking parent checks all children)
    - Signal emission for real-time updates
    """

    # Custom signal emitted when selection changes
    selectionChanged = Signal()

    def __init__(self):
        """Initialize the tree widget with proper configuration."""
        super().__init__()
        self.setHeaderLabel("Report Sections")
        # Add a border to the tree widget for better visual separation
        self.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #a6a6a6;
                border-radius: 6px;
                background-color: #f6f6f6;
            }
            QTreeWidget::item {
                padding: 2px 0px;
            }
        """)
        # Connect item changes to our handler
        self.itemChanged.connect(self.on_item_changed)

    def build_from_sections(self, sections):
        """
        Populate tree widget from parsed LaTeX sections.

        Args:
            sections (dict): {section_name: [subsection_list]}
        """
        self.clear()

        # Validate input format
        if not isinstance(sections, dict):
            print(f"ERROR: Expected dict, got {type(sections)}: {sections}")
            return

        # Create tree items for each section
        for section_name, subsections in sections.items():
            # Create main section item with checkbox
            section_item = QTreeWidgetItem(self, [section_name])
            section_item.setFlags(section_item.flags() | Qt.ItemIsUserCheckable)
            section_item.setCheckState(0, Qt.Checked)  # Default: all selected

            # Add subsection items under the section
            if isinstance(subsections, (list, tuple)):
                for subsection in subsections:
                    sub_item = QTreeWidgetItem(section_item, [str(subsection)])
                    sub_item.setFlags(sub_item.flags() | Qt.ItemIsUserCheckable)
                    sub_item.setCheckState(0, Qt.Checked)  # Default: all selected
            else:
                print(f"WARNING: Subsections not iterable for {section_name}: {type(subsections)}")

        # Expand all items to show the full tree structure
        self.expandAll()

    def on_item_changed(self, item, column):
        """Handle checkbox changes"""
        if column == 0:
            # Temporarily block signals to prevent recursion
            self.blockSignals(True)

            state = item.checkState(0)
            # Update children
            for i in range(item.childCount()):
                item.child(i).setCheckState(0, state)

            # Update parent state based on children
            self.update_parent_state(item)

            # Re-enable signals and emit
            self.blockSignals(False)
            self.selectionChanged.emit()

    def update_parent_state(self, item):
        """Update parent checkbox state based on children"""
        parent = item.parent()
        if parent is None:
            return

        total_children = parent.childCount()
        checked_children = sum(1 for i in range(total_children)
                             if parent.child(i).checkState(0) == Qt.Checked)

        if checked_children == total_children:
            parent.setCheckState(0, Qt.Checked)
        elif checked_children == 0:
            parent.setCheckState(0, Qt.Unchecked)
        else:
            parent.setCheckState(0, Qt.PartiallyChecked)

    def get_selected_sections(self):
        """Return list of selected sections"""
        selected = []

        for i in range(self.topLevelItemCount()):
            section_item = self.topLevelItem(i)
            section_name = section_item.text(0)

            if section_item.checkState(0) == Qt.Checked:
                # Entire section selected
                selected.append(section_name)
            else:
                # Check individual subsections
                for j in range(section_item.childCount()):
                    sub_item = section_item.child(j)
                    if sub_item.checkState(0) == Qt.Checked:
                        selected.append(f"{section_name}/{sub_item.text(0)}")

        return selected


class LaTeXFilter:
    """Filter LaTeX content based on selection - 100 lines max"""

    def filter_content(self, latex_content, selected_sections):
        """Remove unselected sections from LaTeX"""
        lines = latex_content.split('\n')
        filtered_lines = []
        current_section = None
        current_subsection = None
        include_content = True  # Start with True for document preamble
        section_started = False

        for line in lines:
            # Check for new section
            section_match = re.search(r'\\section\{([^}]+)\}', line)
            if section_match:
                current_section = section_match.group(1).strip()
                current_subsection = None
                section_started = True
                # Include section if it's selected OR if any of its subsections are selected
                include_content = (current_section in selected_sections or
                                 any(sel.startswith(f"{current_section}/") for sel in selected_sections))

            # Check for subsection
            subsection_match = re.search(r'\\subsection\{([^}]+)\}', line)
            if subsection_match and current_section:
                current_subsection = subsection_match.group(1).strip()
                subsection_key = f"{current_section}/{current_subsection}"
                # Include subsection only if specifically selected OR parent section is fully selected
                include_content = (current_section in selected_sections or
                                 subsection_key in selected_sections)

            # Always include document structure and preamble
            if (include_content or
                not section_started or  # Include everything before first section
                line.startswith('\\documentclass') or
                line.startswith('\\usepackage') or
                line.startswith('\\title') or
                line.startswith('\\author') or
                line.startswith('\\date') or
                line.startswith('\\begin{document}') or
                line.startswith('\\maketitle') or
                line.startswith('\\end{document}')):
                filtered_lines.append(line)

        return '\n'.join(filtered_lines)

from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_gui.ui.components.dialogs.custom_messagebox import CustomMessageBox, MessageBoxType

class ReportCustomizationDialog(QDialog):
    """Main dialog - 200 lines max"""

    def __init__(self, main_obj, parent=None, existing_tex_file=None):
        super().__init__(parent)
        self.main_obj = main_obj
        self.existing_tex_file = existing_tex_file
        self.latex_content = None
        self.temp_dir = None
        self.setModal(True)
        self.resize(1000, 700)        # Initialize components
        self.parser = LaTeXParser()
        self.filter = LaTeXFilter()
        self.latest_pdf = None
        self.setWindowIcon(QIcon(":/images/osdag_logo.png"))

        self.init_ui()
        self.load_existing_or_generate_report()

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
        """) 
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)
        self.title_bar = CustomTitleBar()
        self.title_bar.setTitle("Customize and Save Design Report")
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

    def init_ui(self):
        """Create simple UI layout"""
        self.setupWrapper()

        layout = QVBoxLayout()

        # Title
        title = QLabel("Customize Report Sections")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Main content - only section tree (no PDF preview)
        self.section_tree = SectionTreeWidget()
        # Do not auto-compile on selection changes
        layout.addWidget(self.section_tree)

        # Controls
        controls = QHBoxLayout()

        # Removed auto-compile and manual compile controls per UX update

        # Open PDF button (compiles into temp dir each time before opening)
        open_btn = QPushButton("Open PDF")
        open_btn.clicked.connect(self.compile_and_open_pdf)
        controls.addWidget(open_btn)

        controls.addStretch()

        # Save and close buttons
        save_btn = QPushButton("Save PDF")
        save_btn.clicked.connect(self.compile_and_save_pdf)
        controls.addWidget(save_btn)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        controls.addWidget(close_btn)

        layout.addLayout(controls)
        # ------Part-of-wrapper-Setup--------
        self.content_widget.setLayout(layout)

    def load_existing_or_generate_report(self):
        """Load existing LaTeX or generate initial LaTeX report"""
        try:
            # Create temp directory
            self.temp_dir = tempfile.mkdtemp(prefix='osdag_report_')

            # DEBUG: Log what we have available
            module_name = getattr(self.main_obj, 'module', 'Unknown')
            print(f"DEBUG: Module = {module_name}")
            print(f"DEBUG: Existing tex file = {self.existing_tex_file}")
            print(f"DEBUG: Existing tex file exists = {self.existing_tex_file and os.path.exists(self.existing_tex_file) if self.existing_tex_file else False}")
            print(f"DEBUG: Has report_input = {hasattr(self.main_obj, 'report_input')}")
            print(f"DEBUG: Has report_check = {hasattr(self.main_obj, 'report_check')}")

            if self.existing_tex_file and os.path.exists(self.existing_tex_file):
                # Load existing LaTeX file
                with open(self.existing_tex_file, 'r', encoding='utf-8') as f:
                    self.latex_content = f.read()
                print(f"SUCCESS: Loaded existing LaTeX file ({len(self.latex_content)} characters)")
                self.parse_and_compile()
            elif CreateLatex:
                # Use real CreateLatex
                self.generate_with_createlatex()
            else:
                # No LaTeX available
                CustomMessageBox(
                    title="Error",
                    text="No LaTeX content available for customization",
                    dialogType=MessageBoxType.Critical
                ).exec()

        except Exception as e:
            print(f"ERROR in load_existing_or_generate_report: {e}")
            CustomMessageBox(
                title="Error",
                text=f"Failed to load/generate report: {e}",
                dialogType=MessageBoxType.Critical
            ).exec()

    def generate_with_createlatex(self):
        """Generate report using actual CreateLatex - simplified version"""
        try:
            # Check if this is a module without CAD support (like butt_joint_bolted)
            module_name = getattr(self.main_obj, 'module', '')
            non_cad_modules = ['Butt Joint Bolted', 'KEY_DISP_BUTTJOINTBOLTED']

            if any(name in str(module_name) for name in non_cad_modules):
                # For non-CAD modules, try to use existing LaTeX if already generated
                print(f"INFO: Handling non-CAD module: {module_name}")

                # First, check if we already have the LaTeX file passed from main workflow
                if self.existing_tex_file and os.path.exists(self.existing_tex_file):
                    print(f"INFO: Using existing LaTeX file for non-CAD module: {self.existing_tex_file}")
                    with open(self.existing_tex_file, 'r', encoding='utf-8') as f:
                        self.latex_content = f.read()
                    self.parse_and_compile()
                    return
                else:
                    raise Exception("Non-CAD module without existing LaTeX file")

            # For CAD-enabled modules - this would need proper implementation
            raise Exception("CAD module LaTeX generation not implemented in customization dialog")

        except Exception as e:
            print(f"ERROR: Failed to generate LaTeX: {e}")
            CustomMessageBox(
                title="Error",
                text=f"Failed to generate report: {e}",
                dialogType=MessageBoxType.Critical
            ).exec()

    def parse_and_compile(self):
        """Parse sections and compile initial PDF"""
        # Parse sections and build tree
        sections = self.parser.parse_sections(self.latex_content)

        if sections:
            self.section_tree.build_from_sections(sections)
            print(f"SUCCESS: Parsed {len(sections)} sections from LaTeX")
            # Compile initial PDF
            self.compile_pdf()
        else:
            CustomMessageBox(
                title="Warning",
                text="No sections found in LaTeX content",
                dialogType=MessageBoxType.Warning
            ).exec()


    def compile_pdf(self):
        """Compile filtered LaTeX to PDF in a fixed temp dir (overwritten each time)."""
        if not self.latex_content:
            return None
        try:
            import shutil

            # Get selected sections
            selected = self.section_tree.get_selected_sections()
            print(f"INFO: Compiling PDF with sections: {selected}")

            # Filter LaTeX content
            filtered_latex = self.filter.filter_content(self.latex_content, selected)

            # Use fixed temp directory to overwrite each time
            safe_temp_dir = os.path.join(tempfile.gettempdir(), "osdag_pdf_compile")
            if os.path.exists(safe_temp_dir):
                shutil.rmtree(safe_temp_dir, ignore_errors=True)
            os.makedirs(safe_temp_dir, exist_ok=True)

            # Write filtered LaTeX to fixed directory
            safe_latex_file = os.path.join(safe_temp_dir, "filtered_report.tex")
            with open(safe_latex_file, 'w', encoding='utf-8') as f:
                f.write(filtered_latex)

            pdf_file = safe_latex_file.replace('.tex', '.pdf')

            # Remove old PDF if exists
            if os.path.exists(pdf_file):
                os.remove(pdf_file)

            print(f"Running pdflatex in fixed dir: {safe_temp_dir}")

            # Run pdflatex
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'filtered_report.tex'],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=safe_temp_dir
            )

            print(f"INFO: pdflatex return code: {result.returncode}")

            if result.returncode == 0 and os.path.exists(pdf_file):
                print(f"SUCCESS: PDF generated: {pdf_file}")
                self.latest_pdf = pdf_file
                return pdf_file
            else:
                error_msg = "PDF compilation warning"
                if result.stderr:
                    error_msg += f"\n\nErrors:\n{result.stderr[:500]}"
                if result.stdout:
                    error_msg += f"\n\nOutput:\n{result.stdout[:500]}"
                print(f"ERROR: {error_msg}")
        except subprocess.TimeoutExpired:
            error_msg = "PDF compilation timed out (>30s)\n\nThis might be due to:\n• LaTeX not installed\n• Missing packages\n• Complex LaTeX content"
            print(f"TIMEOUT: {error_msg}")
            CustomMessageBox(
                title="Compilation Timeout",
                text=error_msg,
                dialogType=MessageBoxType.Warning
            ).exec()
        except FileNotFoundError:
            error_msg = "pdflatex not found\n\nInstall LaTeX distribution:\n• Windows: MiKTeX or TeX Live\n• Linux: texlive-full\n• macOS: MacTeX"
            print(f"ERROR: {error_msg}")
            CustomMessageBox(
                title="LaTeX Not Found",
                text=error_msg,
                dialogType=MessageBoxType.Warning
            ).exec()
        except Exception as e:
            error_msg = f"Compilation failed: {e}"
            print(f"ERROR: {error_msg}")
            CustomMessageBox(
                title="Error",
                text=error_msg,
                dialogType=MessageBoxType.Critical
            ).exec()
        return None

    def compile_and_open_pdf(self):
        """Compile into fixed temp dir and open the PDF."""
        pdf = self.compile_pdf()
        if not pdf:
            return
        self.open_latest_pdf()

    def open_latest_pdf(self):
        """Open the latest generated PDF in external viewer"""
        if self.latest_pdf and os.path.exists(self.latest_pdf):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(self.latest_pdf)
                elif sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', self.latest_pdf])
                else:  # Linux
                    subprocess.run(['xdg-open', self.latest_pdf])
                print(f"SUCCESS: Opened PDF: {self.latest_pdf}")
            except Exception as e:
                print(f"ERROR: Failed to open PDF: {e}")
                CustomMessageBox(
                    title="Error",
                    text=f"Failed to open PDF:\n{e}",
                    dialogType=MessageBoxType.Warning
                ).exec()
        else:
            CustomMessageBox(
                title="No PDF",
                text="No PDF generated yet. Please compile first.",
                dialogType=MessageBoxType.Information
            ).exec()

    def compile_and_save_pdf(self):
        """Compile into fixed temp dir and then save the PDF to a chosen location."""
        pdf = self.compile_pdf()
        if not pdf:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Customized Report", "Osdag_Custom_Report.pdf", "PDF files (*.pdf)"
        )

        if filename:
            shutil.copy2(pdf, filename)
            CustomMessageBox(
                title="Success",
                text=f"PDF saved to:\n{filename}",
                dialogType=MessageBoxType.Success
            ).exec()
            self.accept()

    def closeEvent(self, event):
        """Clean up temp files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        event.accept()


def show_customization_dialog(main_obj, parent=None):
    """Main entry point - simple function"""
    # Look for existing .tex file from main_obj
    existing_tex_file = None
    if hasattr(main_obj, 'report_input') and isinstance(main_obj.report_input, dict):
        filename = main_obj.report_input.get('filename')
        if filename:
            tex_path = f"{filename}.tex"
            if os.path.exists(tex_path):
                existing_tex_file = tex_path

    dialog = ReportCustomizationDialog(main_obj, parent, existing_tex_file)
    return dialog.exec()
