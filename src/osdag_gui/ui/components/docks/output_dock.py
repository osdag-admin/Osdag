"""
Output dock widget for Osdag GUI.
Displays output fields and report generation for connection design.
"""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QSizePolicy, QGroupBox,
    QFormLayout, QLineEdit, QScrollArea,
    QFileDialog
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve

from osdag_core.texlive.Design_wrapper import init_display as init_display_off_screen

from osdag_gui.ui.components.dialogs.custom_messagebox import CustomMessageBox, MessageBoxType
from osdag_gui.ui.components.custom_buttons import DockCustomButton
from osdag_gui.ui.components.dialogs.design_report import DesignReportDialog
from osdag_gui.ui.components.dialogs.spacing_dialog import SpacingDialog

from osdag_gui.data.database.database_config import *
from osdag_core.Common import *
import osdag_gui.resources.resources_rc

# Importing Core Files
from osdag_core.design_type.connection.fin_plate_connection import FinPlateConnection
from osdag_core.design_type.connection.cleat_angle_connection import CleatAngleConnection
from osdag_core.design_type.connection.end_plate_connection import EndPlateConnection
from osdag_core.design_type.connection.beam_cover_plate_weld import BeamCoverPlateWeld
from osdag_core.design_type.connection.beam_cover_plate import BeamCoverPlate
from osdag_core.design_type.compression_member.compression_column import ColumnDesign

# Spacing Detail
from osdag_gui.ui.components.output_details.b2bCoverPlateWelded import B2BCoverPlateWeldedDetails
from osdag_gui.ui.components.output_details.b2bCoverPlate import B2BCoverPlateDetails
from osdag_gui.ui.components.output_details.b2bCoverPlateCapacity import B2BCoverPlateCapacityDetails
from osdag_gui.ui.components.output_details.b2cEndPlate import B2CEndPlateDetails
from osdag_gui.ui.components.output_details.b2bEndPlateSketch import B2BEndPlateSketch
from osdag_gui.ui.components.output_details.basePlate import BasePlateDetails
from osdag_gui.ui.components.output_details.basePlateHollow import BasePlateHollowDetails
from osdag_gui.ui.components.output_details.c2cEndPlate import C2CEndPlateDetails
from osdag_gui.ui.components.output_details.finPlateCapacity import FinPlateCapacityDetails #CapacityDetailsWindow
from osdag_gui.ui.components.output_details.endPlate import EndPlateDetails
from osdag_gui.ui.components.output_details.boltPattern import BoltPatternGenerator
from osdag_gui.ui.components.output_details.seatedAngleSpacing import SeatedAngleDetails
from osdag_gui.ui.components.output_details.cleatAngle import CleatAngleDetails
from osdag_gui.ui.components.output_details.tensionBoltedSpacing import TensionBoltedDetails

from osdag_gui.__config__ import CAD_BACKEND
from osdag_gui.OS_safety_protocols import get_cleanup_coordinator

class DummyCADWidget:
    """
    A lightweight mock of the CAD widget for off-screen rendering.
    Allows us to capture and clean up OCC objects generated purely for
    reports without polluting the main application's CAD widget state.
    """
    def __init__(self):
        self.model_ais_objects = {}
        self.model_hover_labels = {}
        
    def cleanup_for_new_model(self):
        # Allow cleanup coordinator to clear references
        self.model_ais_objects = {}
        self.model_hover_labels = {}

class OutputDock(QWidget):
    def __init__(self, backend:object, parent):
        super().__init__(parent)
        # NOTE: Do NOT use WA_DeleteOnClose - it causes heap corruption (use-after-free)
        # when processEvents() is called during OpenGL rendering. Parent manages lifecycle.
        self.parent = parent
        # Already an Object created in template_page.py
        self.backend = backend
        self.output_widget = None

        # Tracks the visibility state of output sections (titles) and their associated fields
        # Tisplays sections that have meaningful content
        self.output_title_fields = {}

        self.setObjectName("output_dock")
        self.dock_width = 360

        # Ensure OutputDock expands in splitter
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Animation setup
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(100)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.finished.connect(self._on_animation_finished)
        self._animation_callback = None

        output_layout = QHBoxLayout(self)
        output_layout.setContentsMargins(0,0,0,0)
        output_layout.setSpacing(0)

        self.toggle_strip = QWidget()
        self.toggle_strip.setObjectName("toggle_strip")
        self.toggle_strip.setFixedWidth(6)  # Always visible
        toggle_layout = QVBoxLayout(self.toggle_strip)

        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(0)
        toggle_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        self.toggle_btn = QPushButton("❯")  # Show state initially
        self.toggle_btn.setFixedSize(6, 60)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.setObjectName("toggle_strip_button")
        self.toggle_btn.setToolTip("Show panel")

        self.toggle_btn.clicked.connect(self.toggle_output_dock)
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.toggle_btn)
        toggle_layout.addStretch()
        output_layout.addWidget(self.toggle_strip)

        # --- Right content (everything except toggle strip) ---
        right_content = QWidget()
        right_content.setObjectName("outputs-rightpanel")
        self.output_widget = right_content
        right_layout = QVBoxLayout(right_content)
        right_layout.setContentsMargins(5,5,5,5)
        right_layout.setSpacing(4)

        # Top button
        top_button_layout = QHBoxLayout()
        output_dock_btn = QPushButton("Output Dock")
        output_dock_btn.setObjectName("outputs_button")
        output_dock_btn.setCursor(Qt.CursorShape.ArrowCursor)
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
        scroll_area.setObjectName("outputs_vscrollarea")

        # Group container
        group_container = QWidget()
        group_container.setObjectName("outputs_container")
        group_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        group_container_layout = QVBoxLayout(group_container)
        group_container_layout.setSpacing(0)
        group_container_layout.setContentsMargins(5,5,5,5)

        # Bring the data instance from `design_type` folder
        field_list = self.backend.output_values(False)
        # To equalize the label length
        # So that they are of equal size
        # field_list = self.equalize_label_length(field_list)

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
                cur_box_form = QFormLayout()
                cur_box_form.setHorizontalSpacing(5)
                cur_box_form.setVerticalSpacing(10)
                cur_box_form.setContentsMargins(10, 10, 10, 10)
                cur_box_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                cur_box_form.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

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
                
                right = QLineEdit()
                right.setObjectName(field[0])
                right.setFixedWidth(150)
                # Add size policy
                right.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                right.setReadOnly(True)
                # To Right Align
                layout = QHBoxLayout()
                layout.setSpacing(0)
                layout.setContentsMargins(0,0,0,0)
                layout.setAlignment(Qt.AlignmentFlag.AlignRight)
                layout.addWidget(right)
                cur_box_form.addRow(left, layout)
                fields += 1
                self.output_title_fields[current_key][1] = fields
            
            elif type == TYPE_OUT_BUTTON:
                left = QLabel(label)
                left.setObjectName(field[0] + "_label")
                
                right = QPushButton(label.strip())
                right.setFixedWidth(150)
                # Add size policy
                right.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                right.setCursor(Qt.CursorShape.PointingHandCursor)
                spacing_button_list.append(field)
                right.setObjectName(field[0])
                right.setDisabled(True)
                # To Right Align
                layout = QHBoxLayout()
                layout.setSpacing(0)
                layout.setContentsMargins(0,0,0,0)
                layout.setAlignment(Qt.AlignmentFlag.AlignRight)
                layout.addWidget(right)
                cur_box_form.addRow(left, layout)
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
                buttonQPush = self.output_widget.findChild(QPushButton, tupple[0])

                if button:
                    self.output_button_connect(spacing_button_list, button)
                if buttonQPush and buttonQPush is not button:
                    self.output_button_connect(spacing_button_list, buttonQPush)

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
        h_scroll_area.setObjectName("outputs_hscrollarea")
        h_scroll_area.setWidgetResizable(True)
        h_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        h_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        h_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        h_scroll_area.setWidget(right_content)

        output_layout.addWidget(h_scroll_area)

    # ----------------------------------Save-Design-Report-Start------------------------------------------------------
    
    def open_summary_popup(self, main):
        """Open the unified report dialog instead of separate popups"""
        # print("Testing Unified Report Dialog")
        print(self.backend.logger.logs)
        # print('main.module_name', main.module_name())
        
        if not main.design_button_status:
            CustomMessageBox(
                title="Warning",
                text="No design created!",
                dialogType=MessageBoxType.Warning
            ).exec()
            return
        
        # Generate 3D images only if design exists
        if main.design_status:
            try:
                # print("[INFO] Start!")
                off_display, _, _, _ = init_display_off_screen(backend_str=CAD_BACKEND)
                # print(' [INFO] off_display', off_display)
                
                # Check if commLogicObj exists and is properly initialized
                if hasattr(self.parent, 'commLogicObj') and self.parent.commLogicObj is not None:
                    # Store original display settings
                    original_display = self.parent.commLogicObj.display
                    original_component = getattr(self.parent.commLogicObj, 'component', None)
                    original_cad_widget = getattr(self.parent.commLogicObj, 'cad_widget', None)
                    
                    # Create a dummy widget to capture off-screen objects
                    # This prevents polluting the main CAD widget with temporary report objects
                    dummy_widget = DummyCADWidget()
                    
                    try:
                        # Set up for image generation with ISOLATION
                        self.parent.commLogicObj.display = off_display
                        self.parent.commLogicObj.cad_widget = dummy_widget
                        
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
                        
                    finally:
                        # CRITICAL: Clean up the dummy widget's objects
                        # This ensures the off-screen objects are properly deregistered/erased
                        get_cleanup_coordinator().cleanup_for_new_design(dummy_widget, off_display)
                        
                        # Restore original display settings
                        self.parent.commLogicObj.display = original_display
                        if original_cad_widget is not None:
                            self.parent.commLogicObj.cad_widget = original_cad_widget
                        if original_component is not None:
                            self.parent.commLogicObj.component = original_component
                        
                    # print("[INFO] 3D images generated successfully")
                else:
                    # print("[INFO] commLogicObj not available - skipping 3D image generation")
                    # Create default/placeholder images directory
                    image_folder_path = "./ResourceFiles/images"
                    if not os.path.exists(image_folder_path):
                        os.makedirs(image_folder_path)
                    
            except Exception as e:
                print(f"[ERROR] Error generating 3D images: {str(e)}")
                # Ensure images directory exists even if image generation fails
                image_folder_path = "./ResourceFiles/images"
                if not os.path.exists(image_folder_path):
                    os.makedirs(image_folder_path)
            
        # Open Unified report popup dialog
        self.design_report_dialog = DesignReportDialog(
            backend=main,
            module_window=self,
            design_exist=main.design_status,
            loggermsg=self.parent.textEdit.toPlainText()
        )
        
        # Execute the dialog
        self.design_report_dialog.exec()

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
                    original_cad_widget = getattr(self.parent.commLogicObj, 'cad_widget', None)

                    # Create a dummy widget to capture off-screen objects
                    dummy_widget = DummyCADWidget()
                    
                    try:
                        # Set up for image generation with ISOLATION
                        self.parent.commLogicObj.display = off_display
                        self.parent.commLogicObj.cad_widget = dummy_widget
                        
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
                        
                    finally:
                        # CRITICAL: Clean up the dummy widget's objects
                        get_cleanup_coordinator().cleanup_for_new_design(dummy_widget, off_display)

                        # Restore original display settings
                        self.parent.commLogicObj.display = original_display
                        if original_cad_widget is not None:
                            self.parent.commLogicObj.cad_widget = original_cad_widget
                        if original_component is not None:
                            self.parent.commLogicObj.component = original_component
                        
                    print("[INFO] 3D images generated successfully")
                else:
                    print("[INFO] commLogicObj not available - skipping 3D image generation")
                    # Create default/placeholder images directory
                    image_folder_path = "./ResourceFiles/images"
                    if not os.path.exists(image_folder_path):
                        os.makedirs(image_folder_path)
                    
            except Exception as e:
                print(f"[ERROR] Error generating 3D images: {str(e)}")
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
            print(f"[ERROR] Error copying .tex file to {target_dir}: {e}")

        # Copy all PNG files
        for img_path in imgs:
            # Only copy if img_path is a file and ends with .png (case-insensitive)
            if isinstance(img_path, str) and img_path.lower().endswith(".png") and os.path.isfile(img_path):
                try:
                    shutil.copy(img_path, os.path.join(target_dir, os.path.basename(img_path)))
                except Exception as e:
                    # print(f"[ERROR] Error copying PNG file {img_path} to {target_dir}: {e}")
                    pass
            else:
                # print(f"[WARNING] Skipping invalid PNG path: {img_path}")
                pass

        return id    
    
    #----------------------create-tex-to-save-project-END----------------------------------------

    # ----------------------------------Save-Outputs-START------------------------------------------------------
    def save_output_to_csv(self, main, file_name):
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
            default_dir = os.path.join(get_documents_folder(), f"{file_name}.csv")
            fileName, _ = QFileDialog.getSaveFileName(
                self.parent,
                f"Save {file_name}",
                default_dir,
                f"{file_name}(*.csv)",
                options=QFileDialog.Option.DontUseNativeDialog
            )
            if fileName:
                bigdata.to_csv(fileName, index=False, header=None)
                CustomMessageBox(
                    title="Success",
                    text="Saved successfully.",
                    dialogType=MessageBoxType.Success
                ).exec()

    # ----------------------------------Save-Outputs-END------------------------------------------------------

    def run_spacing_script(self,cols,rows,generator_class=BoltPatternGenerator , main=None):
        print("[INFO] Creating spacing window...")
        self.spacing_window = generator_class(self.backend,cols=cols,rows=rows,main=main)
        self.spacing_window.setWindowTitle("Spacing Viewer")
        self.spacing_window.raise_()
        self.spacing_window.activateWindow()
        self.spacing_window.show()
    
    def run_capacity_details(self,cols,rows,generator_class=FinPlateCapacityDetails , main=None):
        print("[INFO] Creating capacity details window...")
        # print("++++++++++++++++++++++++++++++DEBUG++++++++++++++++++++++++++++++")
        # print(generator_class)
        # print("++++++++++++++++++++++++++++++DEBUG++++++++++++++++++++++++++++++")
        self.capacity_window = generator_class(self.backend,cols=cols,rows=rows,main=main)
        self.capacity_window.setWindowTitle("Capacity Details")
        self.capacity_window.raise_()
        self.capacity_window.activateWindow()
        self.capacity_window.show()   

    def output_button_connect(self, spacing_button_list, button):
        button.clicked.connect(lambda: self.spacing_dialog(self.backend, spacing_button_list, button))

    def spacing_dialog(self, main, button_list, button):
        for op in button_list:
            tup = op[3]
            title = tup[0]
            fn = tup[1]
            if op[0] == button.objectName():
                if op[0]==KEY_OUT_SPACING or op[0]==KEY_OUT_SPTING_SPACING:
                    # print(main)
                    flag_legacyspacing = False 
                    if main.module_name()==KEY_DISP_FINPLATE:
                        if hasattr(self.backend, 'spting_leg') and \
                            hasattr(self.backend.spting_leg, 'bolt_line') and \
                            hasattr(self.backend.spting_leg, 'bolts_one_line'):
                                self.run_spacing_script(self.backend.spting_leg.bolts_one_line,self.backend.spting_leg.bolt_line,
                                                        main=main)
                        else:
                                self.run_spacing_script(rows=self.backend.plate.bolts_one_line,cols=self.backend.plate.bolt_line,
                                                        main=main)
                    elif main.module_name()==KEY_DISP_CLEATANGLE and op[0]==KEY_OUT_SPACING:
                        self.run_spacing_script(0,0,CleatAngleDetails,(main,0))
                    elif op[0] != KEY_OUT_SPACING and main.module_name()==KEY_DISP_CLEATANGLE:
                        self.run_spacing_script(0,0,CleatAngleDetails,(main,1))
                    elif main.module_name()==KEY_DISP_ENDPLATE:
                        self.run_spacing_script(0,0,EndPlateDetails,main)
                    elif main.module_name()==KEY_DISP_TENSION_BOLTED:
                        self.run_spacing_script(0,0,TensionBoltedDetails, main)
                    elif main.module_name()==KEY_DISP_STRUT_BOLTED_END_GUSSET:
                        self.run_spacing_script(rows=self.backend.plate.bolt_line,cols=self.backend.plate.bolts_one_line,
                                                main=main)
                    elif main.module_name()==KEY_DISP_LAPJOINTBOLTED:
                        self.run_spacing_script(rows=self.backend.rows, cols=self.backend.cols, main=main)
                    else :
                        flag_legacyspacing = True

                    if not flag_legacyspacing:
                        return            
                
                elif ((op[0]=='button1' or op[0]=='button2') and op[3][0]==KEY_OUT_DISP_BOLT_IR_DETAILS and main.module_name()==KEY_DISP_FINPLATE) :
                    if main.module_name()==KEY_DISP_FINPLATE:
                                if hasattr(self.backend, 'spting_leg') and \
                                    hasattr(self.backend.spting_leg, 'bolt_line') and \
                                    hasattr(self.backend.spting_leg, 'bolts_one_line'):
                                        self.run_capacity_details(self.backend.spting_leg.bolts_one_line,self.backend.spting_leg.bolt_line,
                                                                main=main)
                                else:
                                        self.run_capacity_details(rows=self.backend.plate.bolts_one_line,cols=self.backend.plate.bolt_line,
                                                                main=main)
                    break    

                elif op[0].startswith('SeatedAngle') or op[0].startswith('TopAngle'):
                            if op[0]==KEY_OUT_SEATED_ANGLE_BOLT_COL:
                                val=3
                            elif op[0]==KEY_OUT_SEATED_ANGLE_BOLT_BEAM:
                                val=4
                            elif op[0]==KEY_OUT_TOP_ANGLE_BOLT_COL:
                                val=1
                            else:
                                val=2
                            self.run_spacing_script(None,val,SeatedAngleDetails,main)
                            return
                elif op[0]==KEY_OUT_DISP_BP_DETAILING_SKETCH and op[1]==KEY_OUT_DISP_BP_DETAILING:
                            # print(f"[INFO] rows: {self.backend.bolt_row} , cols : {self.backend.bolt_column} , {self.backend.bolt_row_web}")
                            self.run_spacing_script(0,0,B2CEndPlateDetails,main)
                            return
               
                # Stiffener Sketch
                elif op[0] == KEY_OUT_STIFFENER_SKETCH and main.module_name() == KEY_DISP_BCENDPLATE:
                    self.run_capacity_details(cols=1, rows=1, generator_class=B2CEndPlateDetails, main=main)
                    return

                elif op[0]==KEY_OUT_BP_TYPICAL_DETAILING:
                    if main.connectivity == 'Moment Base Plate' or main.connectivity=='Welded Column Base':
                        self.run_spacing_script(0,0,BasePlateDetails,main)
                    else:
                        self.run_spacing_script(0,0,BasePlateHollowDetails,main)
                    return
                elif op[0]==KEY_WEB_SPACING:
                    self.run_capacity_details(0,0,B2BCoverPlateDetails,(main,True, KEY_OUT_SPACING))
                    return
                elif op[0]==KEY_FLANGE_SPACING:
                    self.run_capacity_details(0,0,B2BCoverPlateDetails,(main,False, KEY_OUT_SPACING))
                    return
                elif op[0]==KEY_WEB_WELD_DETAILS and main.module_name()==KEY_DISP_BEAMCOVERPLATEWELD:
                    self.run_spacing_script(0,0,B2BCoverPlateWeldedDetails,(main,True))
                    return
                elif op[0]==KEY_FLANGE_WELD_DETAILS and main.module_name()==KEY_DISP_BEAMCOVERPLATEWELD:
                    self.run_spacing_script(0,0,B2BCoverPlateWeldedDetails,(main,False))
                    return   

                #im working here
                elif op[0]==KEY_WEB_CAPACITY and main.module_name()==KEY_DISP_BEAMCOVERPLATE:  
                    self.run_capacity_details(0,0,B2BCoverPlateCapacityDetails,(main,True,"capacity"))
                    return
                
                #im working here
                elif op[0]==KEY_FLANGE_CAPACITY and main.module_name()==KEY_DISP_BEAMCOVERPLATE:
                    self.run_capacity_details(0,0,B2BCoverPlateCapacityDetails,(main,False,"capacity"))
                    return
                
                #im working here
                elif op[0]==KEY_OUT_STIFFENER_SKETCH and op[1]==KEY_OUT_DISP_STIFFENER_SKETCH:
                    self.run_spacing_script(0,0,B2BEndPlateSketch,main)
                    return

                elif op[0]==KEY_BOLT_WEB_SPACING or op[0]==KEY_BOLT_FLANGE_SPACING:
                    if op[0]==KEY_BOLT_WEB_SPACING:
                        self.run_spacing_script(0,0,C2CEndPlateDetails,(main,0))
                    else:
                        self.run_spacing_script(0,0,C2CEndPlateDetails,(main,1))
                    break
        #--------------------------Legacy-dialog----------------------------------------------------------------
                dialog = SpacingDialog(main, title, fn)
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
        # Checking hasattr is only meant to prevent errors
        if self.parent:
            if self.width() == 0:
                if hasattr(self.parent, 'update_docking_icons'):
                    self.parent.update_docking_icons(output_is_active=False)
            elif self.width() > 0:
                # Update Output Dock
                if hasattr(self.parent, 'update_docking_icons'):
                    self.parent.update_docking_icons(output_is_active=True)

    # Functions for Design
    # This function Updates the visibility of output titles based on Input Dock Selections
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
                    # print(f"\n[INFO] {option[0]} Is Visible")
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
        # print(f"[INFO] Output_Visibilty key={key} \n titles={titles} \n visible_fields={visible_fields}")
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

    def clear_output_fields(self):
        """Clear all output fields and reset buttons."""
        for output_field in self.output_widget.findChildren(QLineEdit):
            output_field.clear()
        
        for output_field in self.output_widget.findChildren(QPushButton):
            if output_field.objectName() == "dock_custom_button":
                continue
            output_field.setEnabled(False)

#----------------Standalone-Test-Code--------------------------------

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
