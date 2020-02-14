from PyQt5.QtWidgets import QMainWindow, QDialog,QMessageBox, QFileDialog, QApplication
from gui.ui_template import Ui_ModuleWindow
from PyQt5.QtCore import pyqtSlot,pyqtSignal, QObject
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice






class Cadcontroller(QMainWindow):
    closed = pyqtSignal()
    def __init__(self, Ui_ModuleWindow):
        super(Cadcontroller,self).__init__()
        QMainWindow.__init__(self)
        self.ui = Ui_ModuleWindow()
        self.ui.setupUi(self)
        self.ui.btn3D.clicked.connect(lambda: self.call_3DModel("gradient_bg"))
        self.ui.chkBxBeam.clicked.connect(lambda: self.call_3DBeam("gradient_bg"))
        self.ui.chkBxCol.clicked.connect(lambda: self.call_3DColumn("gradient_bg"))
        self.ui.chkBxFinplate.clicked.connect(lambda: self.call_3DFinplate("gradient_bg"))

    def call_3DModel(self, bgcolor):
        '''

        This routine responsible for displaying 3D Cad model
        :param flag: boolean
        :return:
        '''
        if self.ui.btn3D.isChecked:
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(Qt.Unchecked)
        self.commLogicObj.display_3DModel("Model", bgcolor)


    def call_3DBeam(self, bgcolor):
        '''
        Creating and displaying 3D Beam
        '''
        self.ui.chkBxBeam.setChecked(Qt.Checked)
        if self.ui.chkBxBeam.isChecked():
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.commLogicObj.display_3DModel("Beam", bgcolor)


    def call_3DColumn(self, bgcolor):
        '''
        '''
        self.ui.chkBxCol.setChecked(Qt.Checked)
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.commLogicObj.display_3DModel("Column", bgcolor)


    def call_3DFinplate(self, bgcolor):
        '''
        Displaying FinPlate in 3D
        '''
        self.ui.chkBxFinplate.setChecked(Qt.Checked)
        if self.ui.chkBxFinplate.isChecked():
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
            self.ui.btn3D.setChecked(Qt.Unchecked)

        self.commLogicObj.display_3DModel("Plate", bgcolor)

    def unchecked_allChkBox(self):
            '''
            This routine is responsible for unchecking all checkboxes in GUI
            '''

            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(Qt.Unchecked)

    # def create2Dcad(self):
    #         ''' Returns the 3D model of finplate depending upon component
    #         '''
    #
    #
    #         if self.commLogicObj.component == "Beam":
    #             final_model = self.commLogicObj.connectivityObj.get_beamModel()
    #
    #         elif self.commLogicObj.component == "Column":
    #             final_model = self.commLogicObj.connectivityObj.columnModel
    #
    #         elif self.commLogicObj.component == "Plate":
    #             cadlist = [self.commLogicObj.connectivityObj.weldModelLeft,
    #                        self.commLogicObj.connectivityObj.weldModelRight,
    #                        self.commLogicObj.connectivityObj.plateModel] + self.commLogicObj.connectivityObj.nut_bolt_array.get_models()
    #             final_model = cadlist[0]
    #             for model in cadlist[1:]:
    #                 final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()
    #         else:
    #             cadlist = self.commLogicObj.connectivityObj.get_models()
    #             final_model = cadlist[0]
    #             for model in cadlist[1:]:
    #                 final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()
    #
    #         return final_model
    #
    #
    # def save3DcadImages(self):
    #     status = self.resultObj['Bolt']['status']
    #     if status is True:
    #         if self.fuse_model is None:
    #             self.fuse_model = self.create2Dcad()
    #         shape = self.fuse_model
    #
    #         files_types = "IGS (*.igs);;STEP (*.stp);;STL (*.stl);;BREP(*.brep)"
    #
    #         fileName, _ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.igs"),
    #                                                   files_types)
    #         fName = str(fileName)
    #
    #         flag = True
    #         if fName == '':
    #             flag = False
    #             return flag
    #         else:
    #             file_extension = fName.split(".")[-1]
    #
    #             if file_extension == 'igs':
    #                 IGESControl.IGESControl_Controller().Init()
    #                 iges_writer = IGESControl.IGESControl_Writer()
    #                 iges_writer.AddShape(shape)
    #                 iges_writer.Write(fName)
    #
    #             elif file_extension == 'brep':
    #
    #                 BRepTools.breptools.Write(shape, fName)
    #
    #             elif file_extension == 'stp':
    #                 # initialize the STEP exporter
    #                 step_writer = STEPControl_Writer()
    #                 Interface_Static_SetCVal("write.step.schema", "AP203")
    #
    #                 # transfer shapes and write file
    #                 step_writer.Transfer(shape, STEPControl_AsIs)
    #                 status = step_writer.Write(fName)
    #
    #                 assert (status == IFSelect_RetDone)
    #
    #             else:
    #                 stl_writer = StlAPI_Writer()
    #                 stl_writer.SetASCIIMode(True)
    #                 stl_writer.Write(shape, fName)
    #
    #             self.fuse_model = None
    #
    #             QMessageBox.about(self, 'Information', "File saved")
    #     else:
    #         self.ui.actionSave_3D_model.setEnabled(False)
    #         QMessageBox.about(self, 'Information', 'Design Unsafe: 3D Model cannot be saved')