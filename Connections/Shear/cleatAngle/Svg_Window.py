'''
Created on Oct 20, 2016

@author: USER
'''
from PyQt4 import QtSvg, QtGui
import sys
import shutil


class SvgWindow(object):

    def call_svgwindow(self, filename, view, folder):
        # app = QtGui.QApplication(sys.argv)
        self.svgWidget = QtSvg.QSvgWidget(filename)
    #             svgWidget.setGeometry(50, 50, 759, 668)
        self.svgWidget.setFixedSize(900, 800)
        self.btn_save = QtGui.QPushButton('Save as PNG', self.svgWidget)
        self.btn_save.setToolTip('Saves 2D Image as PNG')
        self.btn_save.resize(self.btn_save.sizeHint())
        self.btn_save.setFixedHeight(40)
        self.btn_save.setFixedWidth(110)
        self.btn_save.move(760, 700)
        myfont = QtGui.QFont()
        myfont.setBold(True)
        myfont.setPointSize(9)
        self.btn_save.setFont(myfont)
        self.svgWidget.setWindowTitle('2D View')
        self.svgWidget.show()
        print filename, 'filenameeeee'
        print view, 'viewwwwwww'
        self.folder = folder
        self.btn_save.clicked.connect(lambda: self.save_2d_image_names(view))
        # sys.exit(app.exec_())

    def save_2d_image_names(self, view):
        #         view = self.go_to_open_svg(view)
        # self.btn_save.clicked.connect(view)

        if view == "Front":
            png_image_path = self.folder + "/images_html/cleatFront.png"
            shutil.copyfile(png_image_path, str(QtGui.QFileDialog.getSaveFileName(None, "Save File As", self.folder + "/", "PNG (*.png)")))
        elif view == "Side":
            png_image_path = self.folder + "/images_html/cleatSide.png"
            shutil.copyfile(png_image_path, str(QtGui.QFileDialog.getSaveFileName(None, "Save File As", self.folder + "/", "PNG (*.png)")))
        else:
            png_image_path = self.folder + "/images_html/cleatTop.png"
            shutil.copyfile(png_image_path, str(QtGui.QFileDialog.getSaveFileName(None, "Save File As", self.folder + "/", "PNG (*.png)")))

        QtGui.QMessageBox.about(None, 'Information', "Image Saved")


def main():
    app = QtGui.QApplication(sys.argv)
    ex = SvgWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
