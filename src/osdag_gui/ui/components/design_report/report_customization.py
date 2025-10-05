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
- Temporary file handling for clean workspace
- External PDF viewer integration
- Smart LaTeX filtering that preserves document structure

AUTHOR: Srinivas Raghav V C
"""
import re

# ==============================================================================
# OSDAG IMPORTS - Try to import LaTeX generator
# ==============================================================================

try:
    from osdag_core.design_report.reportGenerator_latex import CreateLatex
    from osdag_core.Common import PDFLATEX
    CREATELATEX_AVAILABLE = True
    print("INFO: CreateLatex successfully imported")
except ImportError:
    CreateLatex = None
    CREATELATEX_AVAILABLE = False
    print("WARNING: CreateLatex not available")
    CREATELATEX_AVAILABLE = False

# ==============================================================================
# IMPORTS - PySide6 widgets and core functionality
# ==============================================================================

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QWidget,QSizeGrip,
                           QTreeWidget, QTreeWidgetItem, QPushButton, QLabel,
                           QCheckBox, QFileDialog)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon


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
                border: 1px solid #90AF13;
                border-radius: 6px;
                background-color: #ffffff;
                show-decoration-selected: 1;
            }

            QTreeWidget::item {
                padding: 4px 6px;
                background-color: #f9f9f9;
                border-bottom: 1px solid #e0e0e0;
            }

            QTreeWidget::item:selected {
                background-color: #d9e9c7;
                color: #000000;
            }

            QTreeWidget::item:hover {
                background-color: #eef5e6;
            }

            QTreeWidget::indicator {
                width: 14px;
                height: 14px;
            }

            QTreeWidget::indicator:unchecked {
                border: 1px solid #555555;
                background: #ffffff;
            }

            QTreeWidget::indicator:checked {
                border: 1px solid #555555;
                background: #90AF13;
                image: none;
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


class CustomizationWidget(QWidget):
    """Widget for Report Customization (second page)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.latex_content = None
        self.latest_pdf = None
        self.init_ui()
        
        self.parser = LaTeXParser()
        self.filter = LaTeXFilter()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Customize Report Sections")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        self.section_tree = SectionTreeWidget()
        
        self.section_tree.setMinimumHeight(300)
        layout.addWidget(self.section_tree)
        
        # Action buttons
        action_layout = QHBoxLayout()
        self.btn_open_pdf = QPushButton("Open PDF")
        self.btn_open_pdf.clicked.connect(self.open_pdf)
        
        action_layout.addWidget(self.btn_open_pdf)
        action_layout.addStretch()
        
        layout.addLayout(action_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def load_latex_content(self, latex_content):
        """Load LaTeX content and parse sections"""
        self.latex_content = latex_content
        if CREATELATEX_AVAILABLE and self.parser:
            sections = self.parser.parse_sections(latex_content)
            if hasattr(self.section_tree, 'build_from_sections'):
                self.section_tree.build_from_sections(sections)
    
    def open_pdf(self):
        """Compile and open PDF"""
        if hasattr(self.parent, 'compile_and_open_pdf'):
            self.parent.compile_and_open_pdf()
