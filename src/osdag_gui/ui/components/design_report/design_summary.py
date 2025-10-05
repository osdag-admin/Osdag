
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QGridLayout, QLineEdit, QTextEdit,
    QFileDialog
)
from PySide6.QtCore import Qt
import os
import yaml

class DesignSummaryWidget(QWidget):
    """Widget for Design Summary input (first page)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        layout = QGridLayout()
        layout.setObjectName("gridLayout")
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Company Name
        self.lbl_companyName = QLabel("Company Name :")
        self.lbl_companyName.setObjectName("lbl_companyName")
        self.lineEdit_companyName = QLineEdit()
        self.lineEdit_companyName.setObjectName("lineEdit_companyName")
        self.lineEdit_companyName.setFocusPolicy(Qt.StrongFocus)
        layout.addWidget(self.lbl_companyName, 0, 0, 1, 1)
        layout.addWidget(self.lineEdit_companyName, 0, 1, 1, 1)
        
        # Company Logo
        self.lbl_comapnyLogo = QLabel("Company Logo :")
        self.lbl_comapnyLogo.setObjectName("lbl_comapnyLogo")

        logo_layout = QHBoxLayout()
        logo_layout.setObjectName("horizontalLayout")
        self.btn_browse = QPushButton("Browse")
        self.btn_browse.setObjectName("btn_browse")
        self.btn_browse.setFixedWidth(100)
        self.btn_browse.clicked.connect(self.browse_logo)

        self.lbl_browse = QLabel("")
        self.lbl_browse.setObjectName("lbl_browse")
        logo_layout.addWidget(self.btn_browse)
        logo_layout.addWidget(self.lbl_browse)
        logo_layout.addStretch()
        layout.addWidget(self.lbl_comapnyLogo, 1, 0, 1, 1)
        layout.addLayout(logo_layout, 1, 1, 1, 1)
        
        # Group Name
        self.lbl_groupName = QLabel("Group/Team Name :")
        self.lbl_groupName.setObjectName("lbl_groupName")
        self.lineEdit_groupName = QLineEdit()
        self.lineEdit_groupName.setObjectName("lineEdit_groupName")
        layout.addWidget(self.lbl_groupName, 2, 0, 1, 1)
        layout.addWidget(self.lineEdit_groupName, 2, 1, 1, 1)
        
        # Designer
        self.lbl_designer = QLabel("Designer :")
        self.lbl_designer.setObjectName("lbl_designer")
        self.lineEdit_designer = QLineEdit()
        self.lineEdit_designer.setObjectName("lineEdit_designer")
        layout.addWidget(self.lbl_designer, 3, 0, 1, 1)
        layout.addWidget(self.lineEdit_designer, 3, 1, 1, 1)
        
        # Profile buttons
        profile_layout = QHBoxLayout()
        self.btn_useProfile = QPushButton("Use Profile")
        self.btn_useProfile.setObjectName("btn_useProfile")

        self.btn_saveProfile = QPushButton("Save Profile")
        self.btn_saveProfile.setObjectName("btn_saveProfile")

        self.btn_useProfile.setFixedWidth(100)
        self.btn_saveProfile.setFixedWidth(100)
        self.btn_useProfile.clicked.connect(self.use_profile)
        self.btn_saveProfile.clicked.connect(self.save_profile)
        profile_layout.addWidget(self.btn_useProfile)
        profile_layout.addWidget(self.btn_saveProfile)
        profile_layout.addStretch()
        layout.addWidget(QLabel(""), 4, 0, 1, 1)  # Empty label for alignment
        layout.addLayout(profile_layout, 4, 1, 1, 1)
        
        # Project Title
        self.lbl_projectTitle = QLabel("Project Title :")
        self.lbl_projectTitle.setObjectName("lbl_projectTitle")

        self.lineEdit_projectTitle = QLineEdit()
        self.lineEdit_projectTitle.setObjectName("lineEdit_projectTitle")

        layout.addWidget(self.lbl_projectTitle, 5, 0, 1, 1)
        layout.addWidget(self.lineEdit_projectTitle, 5, 1, 1, 1)
        
        # Subtitle
        self.lbl_subtitle = QLabel("Subtitle :")
        self.lbl_subtitle.setObjectName("lbl_subtitle")

        self.lineEdit_subtitle = QLineEdit()
        self.lineEdit_subtitle.setObjectName("lineEdit_subtitle")

        self.lineEdit_subtitle.setPlaceholderText("(Optional)")
        layout.addWidget(self.lbl_subtitle, 6, 0, 1, 1)
        layout.addWidget(self.lineEdit_subtitle, 6, 1, 1, 1)
        
        # Job Number
        self.lbl_jobNumber = QLabel("Job Number :")
        self.lbl_jobNumber.setObjectName("lbl_jobNumber")

        self.lineEdit_jobNumber = QLineEdit()
        self.lineEdit_jobNumber.setObjectName("lineEdit_jobNumber")

        layout.addWidget(self.lbl_jobNumber, 7, 0, 1, 1)
        layout.addWidget(self.lineEdit_jobNumber, 7, 1, 1, 1)
        
        # Client
        self.lbl_client = QLabel("Client :")
        self.lbl_client.setObjectName("lbl_client")

        self.lineEdit_client = QLineEdit()
        self.lineEdit_client.setObjectName("lineEdit_client")

        layout.addWidget(self.lbl_client, 8, 0, 1, 1)
        layout.addWidget(self.lineEdit_client, 8, 1, 1, 1)
        
        # Additional Comments
        self.lbl_addComment = QLabel("Additional Comments :")
        self.lbl_addComment.setObjectName("lbl_addComment")

        self.txt_additionalComments = QTextEdit()
        self.txt_additionalComments.setObjectName("txt_additionalComments")

        self.txt_additionalComments.setMaximumHeight(100)
        layout.addWidget(self.lbl_addComment, 9, 0, 1, 1)
        layout.addWidget(self.txt_additionalComments, 9, 1, 1, 1)
        
        layout.addItem(QVBoxLayout(), 10, 0, 1, 2)  # Spacer
        self.setLayout(layout)
    
    def browse_logo(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.svg)"
        )
        if filename:
            self.lbl_browse.setText(filename)
    
    def use_profile(self):
        if hasattr(self.parent, 'folder'):
            folder = self.parent.folder
        else:
            folder = ""
            
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open Profile', 
            os.path.join(str(folder), "Profile"),
            '*.txt'
        )
        if os.path.isfile(filename):
            with open(filename, 'r') as outfile:
                reportsummary = yaml.safe_load(outfile)
                self.lineEdit_companyName.setText(reportsummary["ProfileSummary"]['CompanyName'])
                self.lbl_browse.setText(reportsummary["ProfileSummary"]['CompanyLogo'])
                self.lineEdit_groupName.setText(reportsummary["ProfileSummary"]['Group/TeamName'])
                self.lineEdit_designer.setText(reportsummary["ProfileSummary"]['Designer'])
    
    def save_profile(self):
        input_data = self.get_inputs()
        
        if hasattr(self.parent, 'folder'):
            folder = self.parent.folder
        else:
            folder = ""
            
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Save Profile',
            os.path.join(str(folder), "Profile"), 
            '*.txt'
        )
        if filename:
            with open(filename, 'w') as infile:
                yaml.dump(input_data, infile)
    
    def get_inputs(self):
        """Get all inputs from the summary widget"""
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
