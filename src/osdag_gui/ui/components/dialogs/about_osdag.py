from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy,
    QWidget, QTextBrowser, QTabWidget, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtSvgWidgets import QSvgWidget
from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
import osdag_gui.resources.resources_rc
from osdag_gui.ui.utils.custom_cursors import pointing_hand_cursor
import markdown, os
from importlib import resources

class CustomTextBrowser(QTextBrowser):
    """Custom TextBrowser that uses the correct pointing hand cursor on links."""
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # Check if hovering over a link
        if self.anchorAt(event.pos()):
            self.viewport().setCursor(pointing_hand_cursor())

class AboutOsdagDialog(QDialog):
    """Modern About dialog for Osdag with tabbed interface."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("About Osdag")
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setModal(True)
        self.setFixedSize(680, 600)
        self.setWindowIcon(QIcon(":/images/osdag_logo.png"))
        self.setObjectName("AboutOsdagDialog")
        
        self._build_ui()
        self._apply_styles()

    def _build_ui(self):
        """Build the main UI layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)

        # Custom title bar
        self.titleBar = CustomTitleBar()
        self.titleBar.setTitle("About Osdag")
        main_layout.addWidget(self.titleBar)

        # Tab widget (no header section now)
        self.tabs = QTabWidget()
        self.tabs.setObjectName("aboutTabs")
        self.tabs.tabBar().setCursor(pointing_hand_cursor())
        main_layout.addWidget(self.tabs, 1)

        # Add tabs
        self.tabs.addTab(self._create_about_tab(), "About")
        self.tabs.addTab(self._create_contributors_tab(), "Contributors")
        self.tabs.addTab(self._create_acknowledgements_tab(), "Acknowledgements")
        self.tabs.addTab(self._create_license_tab(), "License")
        self.tabs.addTab(self._create_privacy_tab(), "Privacy Policy")
        self.tabs.addTab(self._create_caveats_tab(), "Caveats")

        # Footer with buttons
        footer_widget = self._create_footer()
        main_layout.addWidget(footer_widget)

    def _create_footer(self):
        """Create footer section with buttons."""
        footer = QWidget()
        footer.setObjectName("footerWidget")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(15, 10, 15, 15)
        footer_layout.setSpacing(8)
        
        footer_layout.addStretch()

        ok_btn = QPushButton("OK")
        ok_btn.setMinimumWidth(80)
        ok_btn.setDefault(True)
        ok_btn.setCursor(pointing_hand_cursor())
        ok_btn.clicked.connect(self.accept)
        footer_layout.addWidget(ok_btn)
        
        return footer

    def _create_about_tab(self):
        """Create the About tab with logo and system information."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Add logo at the top of About tab
        logo = QSvgWidget(":/vectors/Osdag_light.svg")
        logo.setFixedHeight(106) # calculated wrt original 1316x240
        logo.setFixedWidth(581)
        layout.addWidget(logo, alignment=Qt.AlignLeft)

        # Add some spacing after logo
        layout.addSpacing(10)

        browser = CustomTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setHtml(self._get_about_html())
        
        layout.addWidget(browser)
        return widget
    
    def _create_contributors_tab(self):
        """Create the Credits tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)

        browser = CustomTextBrowser()
        browser.setOpenExternalLinks(True)

        md_text = resources.files("osdag_core.data.doc").joinpath("CONTRIBUTORS.MD").read_text(encoding="utf-8")
        html = markdown.markdown(md_text)

        browser.setHtml(html)
        
        layout.addWidget(browser)
        return widget


    def _create_license_tab(self):
        """Create the License tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)

        browser = CustomTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setHtml("""
<pre>
Osdag is licensed under the terms of the LGPL v3 license, as stated below.

Osdag is a free software: you can redistribute it and/or modify it under the
terms of the GNU Lesser General Public License as published by the Free Software 
Foundation, version 3 of the License.

This programme is distributed in the hope that it will be useful, but WITHOUT 
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more 
details.
                        
You should have received a copy of the GNU Lesser General Public License along 
with this program. If not, see &lt;http://www.gnu.org/licenses/&gt;
                        
Notice of Third Party Software Licenses

Osdag contains open-source software packages from third parties. These are 
available on an "as is" basis and subject to their individual license agreements.
These licenses are available in ‘license-dependencies.txt’. These third party tools 
are subject to their individual licenses as well as the Osdag license.
</pre>

<hr />

<pre>
GNU LESSER GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies of this license document,
but changing it is not allowed.

This version of the GNU Lesser General Public License incorporates the terms and
conditions of version 3 of the GNU General Public License, supplemented by the
additional permissions listed below.

0. Additional Definitions.

    As used herein, "this License" refers to version 3 of the GNU Lesser General Public
    License, and the "GNU GPL" refers to version 3 of the GNU General Public License.

    "The Library" refers to a covered work governed by this License, other than an
    Application or a Combined Work as defined below.

    An "Application" is any work that makes use of an interface provided by the Library,
    but which is not otherwise based on the Library. Defining a subclass of a class
    defined by the Library is deemed a mode of using an interface provided by the Library.

    A "Combined Work" is a work produced by combining or linking an Application with the
    Library. The particular version of the Library with which the Combined Work was made
    is also called the "Linked Version".

    The "Minimal Corresponding Source" for a Combined Work means the Corresponding Source
    for the Combined Work, excluding any source code for portions of the Combined Work
    that, considered in isolation, are based on the Application, and not on the Linked
    Version.

    The "Corresponding Application Code" for a Combined Work means the object code and/or
    source code for the Application, including any data and utility programs needed for
    reproducing the Combined Work from the Application, but excluding the System Libraries
    of the Combined Work.

1. Exception to Section 3 of the GNU GPL.

    You may convey a covered work under sections 3 and 4 of this License without being
    bound by section 3 of the GNU GPL.

2. Conveying Modified Versions.

    If you modify a copy of the Library, and, in your modifications, a facility refers to
    a function or data to be supplied by an Application that uses the facility (other than
    as an argument passed when the facility is invoked), then you may convey a copy of the
    modified version:

    a) under this License, provided that you make a good faith effort to ensure that, in
        the event an Application does not supply the function or data, the facility still
        operates, and performs whatever part of its purpose remains meaningful, or

    b) under the GNU GPL, with none of the additional permissions of this License
        applicable to that copy.

3. Object Code Incorporating Material from Library Header Files.

    The object code form of an Application may incorporate material from a header file
    that is part of the Library. You may convey such object code under terms of your
    choice, provided that, if the incorporated material is not limited to numerical
    parameters, data structure layouts and accessors, or small macros, inline functions
    and templates (ten or fewer lines in length), you do both of the following:

    a) Give prominent notice with each copy of the object code that the Library is used
        in it and that the Library and its use are covered by this License.

    b) Accompany the object code with a copy of the GNU GPL and this license document.

4. Combined Works.

    You may convey a Combined Work under terms of your choice that, taken together,
    effectively do not restrict modification of the portions of the Library contained in
    the Combined Work and reverse engineering for debugging such modifications, if you
    also do each of the following:

    a) Give prominent notice with each copy of the Combined Work that the Library is used
        in it and that the Library and its use are covered by this License.

    b) Accompany the Combined Work with a copy of the GNU GPL and this license document.

    c) For a Combined Work that displays copyright notices during execution, include the
        copyright notice for the Library among these notices, as well as a reference directing
        the user to the copies of the GNU GPL and this license document.

    d) Do one of the following:

        0) Convey the Minimal Corresponding Source under the terms of this License, and the
        Corresponding Application Code in a form suitable for, and under terms that permit,
        the user to recombine or relink the Application with a modified version of the Linked
        Version to produce a modified Combined Work, in the manner specified by section 6 of
        the GNU GPL for conveying Corresponding Source.

        1) Use a suitable shared library mechanism for linking with the Library. A suitable
        mechanism is one that (a) uses at run time a copy of the Library already present on the
        user's computer system, and (b) will operate properly with a modified version of the
        Library that is interface-compatible with the Linked Version.

    e) Provide Installation Information, but only if you would otherwise be required to
    provide such information under section 6 of the GNU GPL, and only to the extent that
    such information is necessary to install and execute a modified version of the
    Combined Work produced by recombining or relinking the Application with a modified
    version of the Linked Version.

5. Combined Libraries.

    You may place library facilities that are a work based on the Library side by side in
    a single library together with other library facilities that are not Applications and
    are not covered by this License, and convey such a combined library under terms of
    your choice, if you do both of the following:

    a) Accompany the combined library with a copy of the same work based on the Library,
        uncombined with any other library facilities, conveyed under the terms of this
        License.

    b) Give prominent notice with the combined library that part of it is a work based on
        the Library, and explaining where to find the accompanying uncombined form of the same
        work.

6. Revised Versions of the GNU Lesser General Public License.

    The Free Software Foundation may publish revised and/or new versions of the GNU Lesser
    General Public License from time to time.

    Each version is given a distinguishing version number. If the Library as you received
    it specifies that a certain numbered version of the GNU Lesser General Public License
    "or any later version" applies to it, you have the option of following the terms and
    conditions either of that published version or of any later version published by the
    Free Software Foundation. If the Library as you received it does not specify a version
    number of the GNU Lesser General Public License, you may choose any version of the GNU
    Lesser General Public License ever published by the Free Software Foundation.

    If the Library as you received it specifies that a proxy can decide whether future
    versions of the GNU Lesser General Public License shall apply, that proxy's public
    statement of acceptance of any version is permanent authorization for you to choose
    that version for the Library.
</pre>
            </section>
        """)
        
        layout.addWidget(browser)
        return widget

    def _create_acknowledgements_tab(self):
        """Create the Acknowledgement tab with organization logos"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)

        browser = CustomTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setHtml("""
        <h2 style="color: #91b014; text-align: left;">Acknowledgements</h2>
        
        <p style="text-align: left; line-height: 1.6; margin-bottom: 30px;">
        Osdag acknowledges the support and contributions of the following organizations:
        </p>

        <div style="margin: 30px 5px; text-align: left;">
            <h3 style="color: #91b014;">
                <a href="https://www.civil.iitb.ac.in/" style="text-decoration: none; color: #91b014;">Department of Civil Engineering, IIT Bombay</a>
            </h3>
            <div style="margin: 15px 0;">
                <img src=":/images/iitb_logo.png" alt="IIT Bombay Civil Engineering Logo"">
            </div>
        </div>
                        
        <div style="margin: 30px 5px; text-align: left;">
            <h3 style="color: #91b014;">
                <a href="https://constructsteel.org/" style="text-decoration: none; color: #91b014;">constructsteel</a>
            </h3>
            <div style="margin: 15px 0;">
                <img src=":/images/constructsteel_logo.png" alt="Constructsteel Logo"">
            </div>
        </div>
                        
        <div style="margin: 30px 5px; text-align: left;">
            <h3 style="color: #91b014;">
                <a href="https://fossee.in/" style="text-decoration: none; color: #91b014;">FOSSEE</a>
            </h3>
            <div style="margin: 15px 0;">
                <img src=":/images/fossee_logo.png" alt="FOSSEE Logo"">
            </div>
        </div>

        <div style="margin: 30px 5px; text-align: left;">
            <h3 style="color: #91b014;">
                <a href="https://insdag.com/" style="text-decoration: none; color: #91b014;">INSDAG</a>
            </h3>
            <div style="margin: 15px 0;">
                <img src=":/images/insdag_logo.png" alt="INSDAG Logo"">
            </div>
        </div>


        <div style="margin: 30px 5px; text-align: left;">
            <h3 style="color: #91b014;">
                <a href="https://steel.gov.in/" style="text-decoration: none; color: #91b014;">Ministry of Steel</a>
            </h3>
            <div style="margin: 15px 0;">
                <img src=":/images/mos_logo.png" alt="Ministry of Steel Logo"">
            </div>
        </div>

        """)
        
        layout.addWidget(browser)
        return widget

    def _create_privacy_tab(self):
        """Create the Privacy Policy tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)

        browser = CustomTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setHtml("""
            <section>
                <h2>Privacy Policy</h2>

                <p>
                    Osdag does not collect, transmit, share or use any personal data.
                </p>

                <p>
                    The Osdag developers’ community does not condone any unauthorised usage of private data, so our software does not gather or send personal data.
                </p>

                <p>
                    The Osdag software does not contain any trackers or advertisements.
                </p>
            </section>
        """)
        
        layout.addWidget(browser)
        return widget

    def _create_caveats_tab(self):
        """Create the Caveats tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)

        browser = CustomTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setHtml("""
            <section>
                <h2>Caveats</h2>

                <p>
                    Osdag can perform the design of various steel structural connections, members and systems.
                    However, Osdag should not be solely relied upon for their complete design.
                    The output from Osdag shall be owned by the individual structural designer, and the designer
                    also remains responsible for the final design submitted to the client, along with associated
                    documents.
                </p>

                <p>
                    It is very important to note that the Osdag design algorithms can be modified by individual
                    users, since it is an open-source software. The Osdag team shall not be liable for any further
                    modification, development, or enhancement, until and unless these have been officially
                    released by the team. We encourage the use of Osdag design reports (unabridged) between the
                    designer and the reviewer for clarity on code compliance and openness.
                </p>

                <p>
                    While running, Osdag uses local persistent storage for logs, configuration files, cache,
                    thumbnails, recently accessed files, and similar other information for faster subsequent
                    runs. These information may contain private data, but stays only on the local storage of
                    the device.
                </p>
            </section>
        """)
        
        layout.addWidget(browser)
        return widget


    def _get_about_html(self):
        """Generate HTML content for About tab."""
        return f"""
        <h3>About Osdag</h3>
        <p align="justify">
        Osdag is a cross-platform, free, and open-source software for the design and detailing of 
        steel structures, following the Indian Standard IS 800:2007. Osdag is primarily built on Python 
        using other FOSS tools, such as, PySide, OpenCascade, PythonOCC, and SQLite. It allows the user 
        to design steel connections, members and systems using a graphical user interface. The interactive 
        GUI provides a 3D visualisation of the designed component and an option to export the CAD model 
        to any drafting or BIM software for the creation of construction/fabrication drawings. The design 
        is typically optimised following industry best practices.
        </p>
        </br>
        <p align="justify">
        Osdag is developed by the Osdag team at IIT Bombay, beginning under the umbrella of FOSSEE. 
        Its development has been supported with funding from the Ministry of Education (MoE), Govt. of India, 
        Ministry of Steel (MoS), Govt. of India, constructsteel, and INSDAG.
        </p>
        </br>
        <p align="justify">
        This program comes with ABSOLUTELY NO WARRANTY. This is a free software, and you are welcome to 
        redistribute it under the conditions of LGPL v3 license. See the ‘LICENSE.txt’ file for details of 
        this license.
        </p>
        </br>
        <p>
        <b>Authors:</b> Osdag Team <a href="https://osdag.fossee.in/team">https://osdag.fossee.in/team</a>
        </p>
        Visit <a href="https://osdag.fossee.in">https://osdag.fossee.in</a> for more information.
        <hr style="margin: 5px 0;">
        </br>
        <p style="margin-top: 10px;">
        Osdag® and the Osdag logo are registered trademarks of Indian Institute of Technology Bombay (IIT Bombay).
        </p>
        """

    def _reset_copy_button(self, original_text):
        """Reset the copy button to its original state."""
        self.copy_btn.setText(original_text)
        self.copy_btn.setEnabled(True)

    def _apply_styles(self):
        """Apply custom stylesheet to the dialog."""
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            
            #footerWidget {
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                background-color: white;
            }
            
            QTabBar::tab {
                background-color: #e9ecef;
                color: #495057;
                padding: 8px 16px;
                margin-right: 2px;
                border: 1px solid #dee2e6;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                color: #91b014;
                font-weight: bold;
            }
            
            QTabBar::tab:hover:!selected {
                background-color: #f1f3f5;
            }
            
            QTextBrowser {
                background-color: white;
                border: none;
                font-size: 9pt;
            }
            
            QPushButton {
                background-color: #91b014;
                color: white;
                border: none;
                padding: 6px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #7A9611;
            }
            
            QPushButton:pressed {
                background-color: #1a3a6e;
            }
            
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)


# # Test the dialog
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     dialog = AboutOsdagDialog()
#     dialog.exec()
#     sys.exit(app.exec())