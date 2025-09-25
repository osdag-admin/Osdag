"""
Output dock widget for Osdag GUI.
Displays output fields and report generation for connection design.
"""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QSizePolicy, QGroupBox, QFrame, QDialog,
    QFormLayout, QLineEdit, QScrollArea, QTableWidget, QGridLayout,
    QFileDialog
)
from PySide6.QtGui import QPalette, QColor, QPixmap, QIcon, QPainter
from PySide6.QtCore import Qt, QPropertyAnimation, QSize, QPoint, QEasingCurve, QCoreApplication

from osdag_core.texlive.Design_wrapper import init_display as init_display_off_screen

from osdag_gui.ui.components.dialogs.custom_messagebox import CustomMessageBox, MessageBoxType
from osdag_gui.ui.components.custom_buttons import DockCustomButton
from osdag_gui.ui.components.dialogs.design_summary_popup import DesignSummaryPopup
from osdag_gui.data.database.database_config import *
from osdag_core.Common import *
import osdag_gui.resources.resources_rc

from osdag_gui.__config__ import CAD_BACKEND

import yaml

def style_line_edit():
    return """
        QLineEdit {
            padding: 2px 7px;
            border: 1px solid #070707;
            border-radius: 4px;
            background-color: white;
            color: #000000;
            font-weight: normal;
            min-width: 100px;
            max-width: 120px;
        }
    """

def style_small_button():
    return """
        QPushButton {
            padding: 2px 7px;
            background-color: #888;
            color: white;
            border-radius: 4px;
            min-width: 100px;
            max-width: 120px;
            font-size: 12px;
        }
        QPushButton:disabled {
            background-color: #cccccc;
            color: #888888;
        }
    """

def style_main_buttons():
    return """
        QPushButton {
            background-color: #94b816;
            color: white;
            font-weight: bold;
            border-radius: 4px;
            padding: 6px 18px;
        }
        QPushButton:hover {
            background-color: #7a9a12;
        }
        QPushButton:pressed {
            background-color: #5f7a0e;
        }
    """

class OutputDock(QWidget):
    def __init__(self, backend:object, parent):
        super().__init__(parent)
        self.parent = parent
        # Already an Object created in template_page.py
        self.backend = backend
        self.output_widget = None

        # Tracks the visibility state of output sections (titles) and their associated fields
        # Tisplays sections that have meaningful content
        self.output_title_fields = {}

        self.setStyleSheet("background-color: #FFF;")
        self.dock_width = 360
        self.panel_visible = False # Initially hidden
        self.setMinimumWidth(0)
        self.setMaximumWidth(16777215)

        # Ensure OutputDock expands in splitter
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Animation setup
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(800)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.finished.connect(self._on_animation_finished)
        self._animation_callback = None

        output_layout = QHBoxLayout(self)
        output_layout.setContentsMargins(0,0,0,0)
        output_layout.setSpacing(0)

        self.toggle_strip = QWidget()
        self.toggle_strip.setStyleSheet("background-color: #94b816;")
        self.toggle_strip.setFixedWidth(6)  # Always visible
        toggle_layout = QVBoxLayout(self.toggle_strip)
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(0)
        toggle_layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.toggle_btn = QPushButton("❯")  # Show state initially
        self.toggle_btn.setFixedSize(6, 60)
        self.toggle_btn.setToolTip("Show panel")
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c8408;
                color: white;
                font-size: 12px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #5e7407;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_output_dock)
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.toggle_btn)
        toggle_layout.addStretch()
        output_layout.addWidget(self.toggle_strip)

        # # Hide the dock initially
        # self.setMinimumWidth(0)
        # self.setMaximumWidth(0)

        # Show the dock initially for testing
        self.setMinimumWidth(self.dock_width)
        self.setMaximumWidth(self.dock_width)

        # --- Right content (everything except toggle strip) ---
        right_content = QWidget()
        self.output_widget = right_content
        right_layout = QVBoxLayout(right_content)
        right_layout.setContentsMargins(5,5,5,5)
        right_layout.setSpacing(4)

        # Top button
        top_button_layout = QHBoxLayout()
        output_dock_btn = QPushButton("Output Dock")
        output_dock_btn.setStyleSheet(style_main_buttons())
        output_dock_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        top_button_layout.addWidget(output_dock_btn)
        top_button_layout.addStretch()
        right_layout.addLayout(top_button_layout)

        # Vertical scroll area for group boxes (vertical only)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #EFEFEC;
                background-color: transparent;
                padding: 3px;
            }
            QScrollBar:vertical {
                background: #E0E0E0;
                width: 8px;
                margin: 0px 0px 0px 3px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical {
                background: #A0A0A0;
                min-height: 30px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: #707070;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        # Group container
        group_container = QWidget()
        group_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        group_container_layout = QVBoxLayout(group_container)

        # Bring the data instance from `design_type` folder
        field_list = self.backend.output_values(False)
        # To equalize the label length
        # So that they are of equal size
        field_list = self.equalize_label_length(field_list)

        # Track any group is active or not
        track_group = False
        index = 0
        current_key = None
        key = None
        fields = 0
        title_repeat = 1
        spacing_button_list = []
        for field in field_list:
            index += 1
            label = field[1]
            type = field[2]
            if type == TYPE_MODULE:
                # No use of module title will see.
                continue
            elif type == TYPE_TITLE:
                key = label
                if track_group:
                    current_group.setLayout(cur_box_form)
                    group_container_layout.addWidget(current_group)
                    track_group = False

                # Initialized the group box for current title
                current_group = QGroupBox(label)
                current_group.setObjectName(label)
                track_group = True
                current_group.setStyleSheet("""
                    QGroupBox {
                        border: 1px solid #90AF13;
                        border-radius: 4px;
                        margin-top: 0.8em;
                        font-weight: bold;
                    }
                    QGroupBox::title {
                        subcontrol-origin: content;
                        subcontrol-position: top left;
                        left: 10px;
                        padding: 0 4px;
                        margin-top: -15px;
                        background-color: white;
                    }
                """)
                cur_box_form = QFormLayout()
                cur_box_form.setHorizontalSpacing(5)
                cur_box_form.setVerticalSpacing(10)
                cur_box_form.setContentsMargins(10, 10, 10, 10)
                cur_box_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
                cur_box_form.setAlignment(Qt.AlignmentFlag.AlignRight)

                if key:
                    fields = 0
                    current_key = key
                    if key in self.output_title_fields.keys():
                        self.output_title_fields.update({key+str(title_repeat): [current_group, fields]})
                        title_repeat +=1
                    else:
                        self.output_title_fields.update({key: [current_group, fields]})

            elif type == TYPE_TEXTBOX:
                left = QLabel(label)
                left.setObjectName(field[0] + "_label")
                # left.setStyleSheet("font-family: 'Consolas', 'Courier New', monospace;")
                
                right = QLineEdit()
                right.setStyleSheet(style_line_edit())
                right.setObjectName(field[0])
                right.setReadOnly(True)
                cur_box_form.addRow(left, right)
                fields += 1
                self.output_title_fields[current_key][1] = fields
            
            elif type == TYPE_OUT_BUTTON:
                left = QLabel(label)
                left.setObjectName(field[0] + "_label")
                print("@",label,"@")
                # left.setStyleSheet("font-family: 'Consolas', 'Courier New', monospace;")
                
                right = QPushButton(label.strip())
                spacing_button_list.append(field)
                right.setObjectName(field[0])
                right.setStyleSheet(style_small_button())
                right.setDisabled(True)
                cur_box_form.addRow(left, right)
                fields += 1
                self.output_title_fields[current_key][1] = fields

            if index == len(field_list):
                # Last Data tupple
                # Must add group_box with form
                current_group.setLayout(cur_box_form)
                group_container_layout.addWidget(current_group)

        group_container_layout.addStretch()
        scroll_area.setWidget(group_container)
        right_layout.addWidget(scroll_area)

        if spacing_button_list:
            for tupple in spacing_button_list:
                button = self.output_widget.findChild(QWidget, tupple[0])
                self.output_button_connect(spacing_button_list, button)

        btn_button_layout = QHBoxLayout()
        btn_button_layout.setContentsMargins(0, 20, 0, 0)
        btn_button_layout.addStretch(2)

        design_report_btn = DockCustomButton("Generate Design Report", ":/vectors/design_report.svg")
        design_report_btn.clicked.connect(lambda: self.open_summary_popup(self.backend))
        btn_button_layout.addWidget(design_report_btn)
        btn_button_layout.addStretch(1)    

        save_output_csv_btn = DockCustomButton("  Save Outputs (csv)  ", ":/vectors/design_report.svg")
        save_output_csv_btn.clicked.connect(lambda: self.save_output_to_csv(self.backend))
        btn_button_layout.addWidget(save_output_csv_btn)
        btn_button_layout.addStretch(2)

        right_layout.addLayout(btn_button_layout)

        # --- Horizontal scroll area for all right content ---
        h_scroll_area = QScrollArea()
        h_scroll_area.setWidgetResizable(True)
        h_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        h_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        h_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        h_scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:horizontal {
                background: #E0E0E0;
                height: 8px;
                margin: 3px 0px 0px 0px;
                border-radius: 2px;
            }
            QScrollBar::handle:horizontal {
                background: #A0A0A0;
                min-width: 30px;
                border-radius: 2px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #707070;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)
        h_scroll_area.setWidget(right_content)

        output_layout.addWidget(h_scroll_area)

    # ----------------------------------Save-Design-Report-Start------------------------------------------------------
    
    def open_summary_popup(self, main):
        print("Testing Custom Logger!!")
        print(self.backend.logger.logs)
        print('main.module_name', main.module_name())
        if not main.design_button_status:
            CustomMessageBox(
                title="Warning",
                text="No design created!",
                dialogType=MessageBoxType.Warning
            ).exec()
            return
        
        # Generate 3D images only if design exists and we can create the logic object
        if main.design_status:
            try:
                print("Start!")
                off_display, _, _, _ = init_display_off_screen(backend_str=CAD_BACKEND)
                print('off_display', off_display)
                
                # Check if commLogicObj exists and is properly initialized
                if hasattr(self.parent, 'commLogicObj') and self.parent.commLogicObj is not None:
                    # Store original display settings
                    original_display = self.parent.commLogicObj.display
                    original_component = getattr(self.parent.commLogicObj, 'component', None)
                    
                    # Set up for image generation
                    self.parent.commLogicObj.display = off_display
                    self.parent.commLogicObj.display_3DModel("Model", "gradient_bg")

                    image_folder_path = "./ResourceFiles/images"
                    if not os.path.exists(image_folder_path):
                        os.makedirs(image_folder_path)

                    off_display.set_bg_gradient_color([255,255,255],[255,255,255])
                    off_display.ExportToImage(os.path.join(image_folder_path, '3d.png'))
                    off_display.View_Front()
                    off_display.FitAll()
                    off_display.ExportToImage(os.path.join(image_folder_path, 'front.png'))
                    off_display.View_Top()
                    off_display.FitAll()
                    off_display.ExportToImage(os.path.join(image_folder_path, 'top.png'))
                    off_display.View_Right()
                    off_display.FitAll()
                    off_display.ExportToImage(os.path.join(image_folder_path, 'side.png'))
                    
                    # Restore original display settings
                    self.parent.commLogicObj.display = original_display
                    if original_component is not None:
                        self.parent.commLogicObj.component = original_component
                        
                    print("3D images generated successfully")
                else:
                    print("commLogicObj not available - skipping 3D image generation")
                    # Create default/placeholder images directory
                    image_folder_path = "./ResourceFiles/images"
                    if not os.path.exists(image_folder_path):
                        os.makedirs(image_folder_path)
                    
            except Exception as e:
                print(f"Error generating 3D images: {str(e)}")
                # Ensure images directory exists even if image generation fails
                image_folder_path = "./ResourceFiles/images"
                if not os.path.exists(image_folder_path):
                    os.makedirs(image_folder_path)

        # Open the summary popup dialog
        self.summary_popup = DesignSummaryPopup(main.design_status, loggermsg=self.parent.textEdit.toPlainText())
        self.summary_popup.setupUi(main, self)
        
        # Connect the generate report button to actual report generation
        if hasattr(self.summary_popup, 'btn_CreateDesignReport'):
            self.summary_popup.btn_CreateDesignReport.clicked.connect(lambda: self.generate_design_report(main, self.summary_popup))
        elif hasattr(self.summary_popup, 'buttonBox'):
            # If using QDialogButtonBox, connect to accepted signal
            self.summary_popup.buttonBox.accepted.connect(lambda: self.generate_design_report(main, self.summary_popup))

        self.summary_popup.exec()

    # ----------------------------------Save-Design-Report-END------------------------------------------------------

    #----------------------create-tex-to-save-project-START--------------------------------------

    def generate_tex(self):
        # Generate 3D images only if design exists and we can create the logic object
        if self.backend.design_status:
            try:
                cad_pngs = []
                off_display, _, _, _ = init_display_off_screen(backend_str=CAD_BACKEND)
                
                # Check if commLogicObj exists and is properly initialized
                if hasattr(self.parent, 'commLogicObj') and self.parent.commLogicObj is not None:
                    # Store original display settings
                    original_display = self.parent.commLogicObj.display
                    original_component = getattr(self.parent.commLogicObj, 'component', None)
                    
                    # Set up for image generation
                    self.parent.commLogicObj.display = off_display
                    self.parent.commLogicObj.display_3DModel("Model", "gradient_bg")

                    image_folder_path = "./ResourceFiles/images"
                    if not os.path.exists(image_folder_path):
                        os.makedirs(image_folder_path)

                    off_display.set_bg_gradient_color([255,255,255],[255,255,255])
                    off_display.ExportToImage(os.path.join(image_folder_path, '3d.png'))
                    cad_pngs.append(os.path.join(image_folder_path, '3d.png'))
                    off_display.View_Front()
                    off_display.FitAll()
                    off_display.ExportToImage(os.path.join(image_folder_path, 'front.png'))
                    cad_pngs.append(os.path.join(image_folder_path, 'front.png'))
                    off_display.View_Top()
                    off_display.FitAll()
                    off_display.ExportToImage(os.path.join(image_folder_path, 'top.png'))
                    cad_pngs.append(os.path.join(image_folder_path, 'top.png'))
                    off_display.View_Right()
                    off_display.FitAll()
                    off_display.ExportToImage(os.path.join(image_folder_path, 'side.png'))
                    cad_pngs.append(os.path.join(image_folder_path, 'side.png'))
                    
                    # Restore original display settings
                    self.parent.commLogicObj.display = original_display
                    if original_component is not None:
                        self.parent.commLogicObj.component = original_component
                        
                    print("3D images generated successfully")
                else:
                    print("commLogicObj not available - skipping 3D image generation")
                    # Create default/placeholder images directory
                    image_folder_path = "./ResourceFiles/images"
                    if not os.path.exists(image_folder_path):
                        os.makedirs(image_folder_path)
                    
            except Exception as e:
                print(f"Error generating 3D images: {str(e)}")
                # Ensure images directory exists even if image generation fails
                image_folder_path = "./ResourceFiles/images"
                if not os.path.exists(image_folder_path):
                    os.makedirs(image_folder_path)

        # Init input summary
        input_summary = {}
        input_summary["ProfileSummary"] = {}
        input_summary["ProfileSummary"]["CompanyName"] = ''
        input_summary["ProfileSummary"]["CompanyLogo"] = ''
        input_summary["ProfileSummary"]["Group/TeamName"] = ''
        input_summary["ProfileSummary"]["Designer"] = ''

        input_summary["ProjectTitle"] = ''
        input_summary["Subtitle"] = ''
        input_summary["JobNumber"] = ''
        input_summary["AdditionalComments"] = ''
        input_summary["Client"] = ''

        import tempfile
        # CREATE TEMPORARY WORKSPACE - No user prompt needed
        temp_dir = tempfile.mkdtemp(prefix='osdag_report_')
        filename = os.path.join(temp_dir, "report.tex")

        fname_no_ext = filename.split(".")[0]
        input_summary['filename'] = fname_no_ext
        input_summary['does_design_exist'] = self.backend.design_status
        input_summary['logger_messages'] = self.parent.textEdit.toPlainText()
        # Generate LaTeX file instead of PDF
        self.backend.save_design(input_summary)
        
        return cad_pngs, filename

    # called from template_page
    def save_to_database(self, record: dict):
        imgs, tex_path = self.generate_tex()
        import os
        report_path = "osdag_gui.data.reports"
        # Ensure the 'reports' directory exists
        if not os.path.exists("./osdag_gui/data/reports"):
            os.makedirs("./osdag_gui/data/reports")
        record[REPORT_FILE_PATH] = report_path

        id = insert_recent_project(record)

        # tex_path should always be a string
        if isinstance(tex_path, list):
            tex_path = tex_path[0] if tex_path else None

        # imgs should always be a list of valid files
        if isinstance(imgs, str):
            imgs = [imgs] if os.path.isfile(imgs) else []
        elif isinstance(imgs, list):
            imgs = [img for img in imgs if isinstance(img, str) and os.path.isfile(img)]
        else:
            imgs = []

        # Copy the .tex file and PNGs to the report_path directory, suffixed with the record id
        import shutil

        import pathlib

        # Construct the target directory path using an absolute path
        # Place reports in a real directory, not a Python module path
        base_report_dir = os.path.join(os.getcwd(), "osdag_gui", "data", "reports")
        target_dir = os.path.join(base_report_dir, f"file_{id}")
        pathlib.Path(target_dir).mkdir(parents=True, exist_ok=True)

        # Copy the .tex file
        try:
            shutil.copy(tex_path, os.path.join(target_dir, os.path.basename(tex_path)))
        except Exception as e:
            print(f"Error copying .tex file to {target_dir}: {e}")

        # Copy all PNG files
        for img_path in imgs:
            # Only copy if img_path is a file and ends with .png (case-insensitive)
            if isinstance(img_path, str) and img_path.lower().endswith(".png") and os.path.isfile(img_path):
                try:
                    shutil.copy(img_path, os.path.join(target_dir, os.path.basename(img_path)))
                except Exception as e:
                    print(f"Error copying PNG file {img_path} to {target_dir}: {e}")
            else:
                print(f"Skipping invalid PNG path: {img_path}")

        return id    
    
    #----------------------create-tex-to-save-project-END----------------------------------------

    def getPopUpInputs(self):
        """Enhanced method to collect all popup inputs"""
        input_summary = {}
        input_summary["ProfileSummary"] = {}
        
        # Profile information
        input_summary["ProfileSummary"]["CompanyName"] = str(self.summary_popup.lineEdit_companyName.text()) if hasattr(self.summary_popup, 'lineEdit_companyName') else "Company Name"
        input_summary["ProfileSummary"]["CompanyLogo"] = str(self.summary_popup.lbl_browse.text()) if hasattr(self.summary_popup, 'lbl_browse') else ""
        input_summary["ProfileSummary"]["Group/TeamName"] = str(self.summary_popup.lineEdit_groupName.text()) if hasattr(self.summary_popup, 'lineEdit_groupName') else "Design Team"
        input_summary["ProfileSummary"]["Designer"] = str(self.summary_popup.lineEdit_designer.text()) if hasattr(self.summary_popup, 'lineEdit_designer') else "Designer"

        # Project information - **CRITICAL**: These are required by reportGenerator
        input_summary["ProjectTitle"] = str(self.summary_popup.lineEdit_projectTitle.text()) if hasattr(self.summary_popup, 'lineEdit_projectTitle') else "Welded Butt Joint Design"
        input_summary["Subtitle"] = str(self.summary_popup.lineEdit_subtitle.text()) if hasattr(self.summary_popup, 'lineEdit_subtitle') else "Design Report"
        input_summary["JobNumber"] = str(self.summary_popup.lineEdit_jobNumber.text()) if hasattr(self.summary_popup, 'lineEdit_jobNumber') else "JOB-001"
        input_summary["Client"] = str(self.summary_popup.lineEdit_client.text()) if hasattr(self.summary_popup, 'lineEdit_client') else "Client"
        
        # Additional comments
        if hasattr(self.summary_popup, 'txt_additionalComments'):
            input_summary["AdditionalComments"] = str(self.summary_popup.txt_additionalComments.toPlainText())
        else:
            input_summary["AdditionalComments"] = "Design completed successfully"
        
        # File and folder settings
        if hasattr(self.summary_popup, 'lineEdit_fileName'):
            input_summary["filename"] = str(self.summary_popup.lineEdit_fileName.text())
        if hasattr(self.summary_popup, 'lineEdit_folder'):
            input_summary["folder"] = str(self.summary_popup.lineEdit_folder.text())

        return input_summary
    #----------------------create-tex-to-save-project-END----------------------------------------

    # ----------------------------------Save-Outputs-START------------------------------------------------------
    def save_output_to_csv(self, main):
        status = main.design_status
        if(not status):
            CustomMessageBox(
                title="Warning",
                text="No Design is Created yet.",
                dialogType=MessageBoxType.Warning
            ).exec()
            return
           
        out_list = main.output_values(status)
        to_Save = {}
        flag = 0
        for option in out_list:
            if option[0] is not None and option[2] == TYPE_TEXTBOX:
                to_Save[option[0]] = option[3]
                if str(option[3]):
                    flag = 1
            if option[2] == TYPE_OUT_BUTTON:
                tup = option[3]
                fn = tup[1]
                for item in fn(status):
                    lable = item[0]
                    value = item[3]
                    if lable!=None and value!=None:
                        to_Save[lable] = value

        import pandas as pd
        df = pd.DataFrame(self.parent.design_inputs.items())
        df1 = pd.DataFrame(to_Save.items())
        bigdata = pd.concat([df, df1], axis=1)
        if not flag:
            CustomMessageBox(
                title="Information",
                text="Nothing to Save.",
                dialogType=MessageBoxType.Information
            ).exec()
        else:
            fileName, _ = QFileDialog.getSaveFileName(self,
                                                        "Save Output", os.path.join(self.parent.folder, "untitled.csv"),
                                                        "Input Files(*.csv)")
            if fileName:
                bigdata.to_csv(fileName, index=False, header=None)
                CustomMessageBox(
                    title="Success",
                    text="Saved successfully.",
                    dialogType=MessageBoxType.Success
                ).exec()

    # ----------------------------------Save-Outputs-END------------------------------------------------------

    def output_button_connect(self, spacing_button_list, button):
        button.clicked.connect(lambda: self.spacing_dialog(self.backend, spacing_button_list, button))

    def spacing_dialog(self, main, button_list, button):
        dialog = QDialog()
        dialog.setObjectName("Dialog")
        layout1 = QVBoxLayout(dialog)

        note_widget = QWidget(dialog)
        note_layout = QVBoxLayout(note_widget)
        layout1.addWidget(note_widget)

        tabel_widget = QWidget(dialog)
        table_layout = QVBoxLayout(tabel_widget)
        layout1.addWidget(tabel_widget)

        scroll = QScrollArea(dialog)
        layout1.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.horizontalScrollBar().setVisible(False)
        scroll_content = QWidget(scroll)
        outer_grid_layout = QGridLayout(scroll_content)
        inner_grid_widget = QWidget(scroll_content)
        image_widget = QWidget(scroll_content)
        image_layout = QVBoxLayout(image_widget)
        image_layout.setAlignment(Qt.AlignCenter)
        image_widget.setLayout(image_layout)
        inner_grid_layout = QGridLayout(inner_grid_widget)
        inner_grid_widget.setLayout(inner_grid_layout)
        scroll_content.setLayout(outer_grid_layout)
        scroll.setWidget(scroll_content)

        dialog_width = 260
        dialog_height = 300
        max_image_width = 0
        max_label_width = 0
        max_image_height = 0

        section = 0
        no_note = True

        for op in button_list:

            if op[0] == button.objectName():
                tup = op[3]
                title = tup[0]
                fn = tup[1]
                dialog.setWindowTitle(title)
                j = 1
                _translate = QCoreApplication.translate
                for option in fn(main.design_status):
                    option_type = option[2]
                    lable = option[1]
                    value = option[3]
                    if option_type in [TYPE_TEXTBOX, TYPE_COMBOBOX]:
                        l = QLabel(inner_grid_widget)

                        l.setObjectName(option[0] + "_label")
                        l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))
                        inner_grid_layout.addWidget(l, j, 1, 1, 1)
                        l.setFixedSize(l.sizeHint().width(), l.sizeHint().height())
                        max_label_width = max(l.sizeHint().width(), max_label_width)
                        l.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))

                    if option_type == TYPE_SECTION:
                        if section != 0:
                            outer_grid_layout.addWidget(inner_grid_widget, j, 1, 1, 1)
                            outer_grid_layout.addWidget(image_widget, j, 2, 1, 1)
                            hl1 = QFrame()
                            hl1.setFrameShape(QFrame.HLine)
                            j += 1
                            outer_grid_layout.addWidget(hl1, j, 1, 1, 2)

                        inner_grid_widget = QWidget(scroll_content)
                        image_widget = QWidget(scroll_content)
                        image_layout = QVBoxLayout(image_widget)
                        image_layout.setAlignment(Qt.AlignCenter)
                        image_widget.setLayout(image_layout)
                        inner_grid_layout = QGridLayout(inner_grid_widget)
                        inner_grid_widget.setLayout(inner_grid_layout)

                        if value is not None and value != "":
                            im = QLabel(image_widget)
                            im.setFixedSize(int(value[1]), int(value[2]))
                            pmap = QPixmap(value[0])
                            im.setScaledContents(1)
                            im.setStyleSheet("background-color: white;")
                            im.setPixmap(pmap)
                            image_layout.addWidget(im)
                            caption = QLabel(image_widget)
                            caption.setAlignment(Qt.AlignCenter)
                            caption.setText(value[3])
                            caption.setFixedSize(int(value[1]), caption.sizeHint().height())
                            image_layout.addWidget(caption)
                            max_image_width = max(max_image_width, value[1])
                            max_image_height = max(max_image_height, value[2])
                        j += 1
                        q = QLabel(scroll_content)
                        q.setObjectName("_title")
                        q.setText(lable)
                        q.setFixedSize(q.sizeHint().width(), q.sizeHint().height())
                        q.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
                        outer_grid_layout.addWidget(q, j, 1, 1, 2)
                        section += 1

                    if option_type == TYPE_TEXTBOX:
                        r = QLineEdit(inner_grid_widget)
                        r.setFixedSize(100, 27)
                        r.setObjectName(option[0])
                        r.setText(str(value))
                        inner_grid_layout.addWidget(r, j, 2, 1, 1)

                    if option_type == TYPE_TABLE_OU:
                        tb = QTableWidget(tabel_widget)
                        #tb.setAlignment(Qt.AlignCenter)
                        #tb.setScaledContents(True)
                        table_layout.addWidget(tb)

                    if option_type == TYPE_IMAGE:
                        im = QLabel(image_widget)
                        im.setScaledContents(True)
                        im.setFixedSize(int(value[1]), int(value[2]))
                        pmap = QPixmap(value[0])
                        im.setStyleSheet("background-color: white;")
                        im.setPixmap(pmap)
                        image_layout.addWidget(im)
                        caption = QLabel(image_widget)
                        caption.setAlignment(Qt.AlignCenter)
                        caption.setText(value[3])
                        caption.setFixedSize(int(value[1]), 12)
                        image_layout.addWidget(caption)
                        max_image_width = max(max_image_width, value[1])
                        max_image_height = max(max_image_height, value[2])

                    if option_type == TYPE_NOTE:
                        note = QLabel(note_widget)
                        note.setText("Note: "+str(value))
                        note.setFixedSize(note.sizeHint().width(), note.sizeHint().height())
                        note_layout.addWidget(note)
                        no_note = False

                    j = j + 1

                if inner_grid_layout.count() > 0:
                    outer_grid_layout.addWidget(inner_grid_widget, j, 1, 1, 1)
                if image_layout.count() > 0:
                    outer_grid_layout.addWidget(image_widget, j, 2, 1, 1)

                dialog_width += max_label_width
                dialog_width += max_image_width
                dialog_height = max(dialog_height, max_image_height+125)
                if not no_note:
                    dialog_height += 40
                dialog.resize(int(dialog_width), int(dialog_height))
                dialog.setMinimumSize(int(dialog_width), int(dialog_height))

                if no_note:
                    layout1.removeWidget(note_widget)

                dialog.exec()

    # To equalize the size of label strings
    def equalize_label_length(self, list):
        # Calculate maximum size
        max_len = 0
        for t in list:
            if t[2] not in [TYPE_TITLE]:
                if len(t[1]) > max_len:
                    max_len = len(t[1])
        
        # Create a new list with equal string length
        return_list = [] 
        for t in list:
            if t[2] not in [TYPE_TITLE]:
                new_tupple = (t[0], t[1].ljust(max_len)) + t[2:]
            else:
                new_tupple = t
            return_list.append(new_tupple)

        return return_list

    def toggle_output_dock(self):
        parent = self.parent
        if hasattr(parent, 'toggle_animate'):
            is_collapsing = self.width() > 0
            parent.toggle_animate(show=not is_collapsing, dock='output')
        
        self.toggle_btn.setText("❮" if is_collapsing else "❯")
        self.toggle_btn.setToolTip("Show panel" if is_collapsing else "Hide panel")

    def _on_animation_finished(self):
        # Callback logic can go here if needed after animation completes
        # For now, we don't have a specific callback for the width animation
        pass

    def is_panel_visible(self):
        return self.panel_visible

    def set_results(self, result_dict):
        layout = self.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for key, value in result_dict.items():
            label = QLabel(f"{key}: {value}")
            layout.addWidget(label)
        self.current_result = result_dict      

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Checking hasattr is only meant to prevent errors,
        # while standalone testing of this widget
        if self.parent and hasattr(self.parent, 'parent') and self.parent.parent:
            if self.width() == 0:
                if hasattr(self.parent.parent, 'update_docking_icons'):
                    self.parent.parent.update_docking_icons(output_is_active=False)
                if hasattr(self.parent, 'update_input_label_state'):
                    self.parent.update_output_label_state(True)
            elif self.width() > 0:
                if hasattr(self.parent.parent, 'update_docking_icons'):
                    self.parent.parent.update_docking_icons(output_is_active=True)
                if hasattr(self.parent, 'update_input_label_state'):
                    self.parent.update_output_label_state(False)

    # Functions for Design
    def output_title_change(self, main):
        status = main.design_status
        out_list = main.output_values(status)
        key = None
        no_field_titles = []
        titles = []
        title_repeat = 1
        visible_fields = 0
        for option in out_list:
            if option[2] == TYPE_TITLE:
                if key:
                    title_repeat = self.output_title_visiblity(visible_fields, key, titles, title_repeat)
                    titles.append(key)

                key = option[1]
                if self.output_title_fields[key][1] == 0:
                    no_field_titles.append(key)
                if key in no_field_titles:
                    visible_fields = 1
                else:
                    visible_fields = 0

            if option[2] == TYPE_TEXTBOX:
                if self.output_widget.findChild(QWidget, option[0]).isVisible():
                    visible_fields += 1

            elif option[2] == TYPE_OUT_BUTTON:
                if self.output_widget.findChild(QWidget, option[0]).isVisible():
                    visible_fields += 1

        self.output_title_visiblity(visible_fields, key, titles, title_repeat)

        no_field_title = ""
        for title in self.output_title_fields.keys():
            if title in no_field_titles:
                no_field_title = title
            elif self.output_title_fields[title][0].isVisible():
                if no_field_title in no_field_titles:
                    no_field_titles.remove(no_field_title)

        for no_field_title in no_field_titles:
            self.output_title_fields[no_field_title][0].setVisible(False)

    def output_title_visiblity(self, visible_fields, key, titles, title_repeat):
        print(f"key={key} \n titles={titles} ")
        if visible_fields == 0:
            if key in titles:
                self.output_title_fields[key + str(title_repeat)][0].setVisible(False)
                title_repeat += 1
            else:
                self.output_title_fields[key][0].setVisible(False)
        else:
            if key in titles:
                self.output_title_fields[key + str(title_repeat)][0].setVisible(True)
                title_repeat += 1
            else:
                self.output_title_fields[key][0].setVisible(True)

        return title_repeat


#----------------Standalone-Test-Code--------------------------------
from osdag_core.design_type.connection.fin_plate_connection import FinPlateConnection

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("border: none")

        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.main_h_layout = QHBoxLayout(self.central_widget)
        self.main_h_layout.addStretch(40)

        self.main_h_layout.addWidget(OutputDock(backend=FinPlateConnection ,parent=self),15)
        self.setWindowState(Qt.WindowMaximized)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec()) 

