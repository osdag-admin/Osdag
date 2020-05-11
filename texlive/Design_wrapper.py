

import logging
import os
import sys

from OCC import VERSION
from OCC.Display.backend import load_backend, get_qt_modules

log = logging.getLogger(__name__)


def check_callable(_callable):
    assert callable(_callable), 'the function supplied is not callable'


def init_display(backend_str=None, size=(1024, 768)):
   
    if os.getenv("PYTHONOCC_SHUNT_GUI") == "1":
        # define a dumb class and an empty method
        from OCC.Display import OCCViewer

        def do_nothing(*kargs, **kwargs):
            """ A method that does nothing
            """
            pass

        def call_function(s, func):
            """ A function that calls another function.
            Helpfull to bypass add_function_to_menu. s should be a string
            """
            check_callable(func)
            print(s, func.__name__)
            func()

        class BlindViewer(OCCViewer.Viewer3d):
            def __init__(self, *kargs):
                self._window_handle = 0
                self._inited = False
                self._local_context_opened = False
                self.Context_handle = Dumb()
                self.Viewer_handle = Dumb()
                self.View_handle = Dumb()
                self.Context = Dumb()
                self.Viewer = Dumb()
                self.View = Dumb()
                self.selected_shapes = []
                self._select_callbacks = []
                self._struc_mgr = Dumb()

            def GetContext(self):
                return Dumb()

            def DisplayMessage(self, *kargs):
                pass

        class Dumb(object):
            """ A class the does nothing whatever the method
            or property is called
            """
            def __getattr__(self, name):
                if name in ['Context']:
                    return Dumb()
                elif name in ['GetContext', 'GetObject']:
                    return Dumb
                else:
                    return do_nothing
        
        return BlindViewer(), do_nothing, do_nothing, call_function
    used_backend = load_backend(backend_str)
    
    if used_backend == 'wx':
        import wx
        from wxDisplay import wxViewer3d

        class AppFrame(wx.Frame):

            def __init__(self, parent):
                wx.Frame.__init__(self, parent, -1, "pythonOCC-%s 3d viewer ('wx' backend)" % VERSION,
                                  style=wx.DEFAULT_FRAME_STYLE, size=size)
                self.canva = wxViewer3d(self)
                self.menuBar = wx.MenuBar()
                self._menus = {}
                self._menu_methods = {}

            def add_menu(self, menu_name):
                _menu = wx.Menu()
                self.menuBar.Append(_menu, "&" + menu_name)
                self.SetMenuBar(self.menuBar)
                self._menus[menu_name] = _menu

            def add_function_to_menu(self, menu_name, _callable):
                
                _id = wx.NewId()
                check_callable(_callable)
                try:
                    self._menus[menu_name].Append(_id,
                                                  _callable.__name__.replace('_', ' ').lower())
                except KeyError:
                    raise ValueError('the menu item %s does not exist' % menu_name)
                self.Bind(wx.EVT_MENU, _callable, id=_id)

        app = wx.App(False)
        win = AppFrame(None)
        win.Show(True)
        wx.SafeYield()
        win.canva.InitDriver()
        app.SetTopWindow(win)
        display = win.canva._display

        def add_menu(*args, **kwargs):
            win.add_menu(*args, **kwargs)

        def add_function_to_menu(*args, **kwargs):
            win.add_function_to_menu(*args, **kwargs)

        def start_display():
            app.MainLoop()

   
    elif 'qt' in used_backend:
        from OCC.Display.qtDisplay import qtViewer3d
        QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

        class MainWindow(QtWidgets.QMainWindow):

            def __init__(self, *args):
                QtWidgets.QMainWindow.__init__(self, *args)
                self.canva = qtViewer3d(self)
                self.setWindowTitle("pythonOCC-%s 3d viewer ('%s' backend)" % (VERSION, used_backend))
                self.resize(size[0], size[1])
                self.setCentralWidget(self.canva)
                if sys.platform != 'darwin':
                    self.menu_bar = self.menuBar()
                else:
                    self.menu_bar = QtWidgets.QMenuBar()
                self._menus = {}
                self._menu_methods = {}
                self.centerOnScreen()

            def centerOnScreen(self):
                '''Centers the window on the screen.'''
                resolution = QtWidgets.QDesktopWidget().screenGeometry()
                self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                          (resolution.height() / 2) - (self.frameSize().height() / 2))

            def add_menu(self, menu_name):
                _menu = self.menu_bar.addMenu("&" + menu_name)
                self._menus[menu_name] = _menu

            def add_function_to_menu(self, menu_name, _callable):
                check_callable(_callable)
                try:
                    _action = QtWidgets.QAction(_callable.__name__.replace('_', ' ').lower(), self)
                    _action.setMenuRole(QtWidgets.QAction.NoRole)
                    _action.triggered.connect(_callable)

                    self._menus[menu_name].addAction(_action)
                except KeyError:
                    raise ValueError('the menu item %s does not exist' % menu_name)

        app = QtWidgets.QApplication.instance()  
        if not app:  
            app = QtWidgets.QApplication(sys.argv)
        win = MainWindow()
        win.showMinimized()
        win.close()
        win.canva.InitDriver()
        win.canva.qApp = app
        display = win.canva._display
        if sys.platform != "linux2":
            display.EnableAntiAliasing()
        display.set_bg_gradient_color([23, 1, 32], [23, 1, 32])
        display.display_triedron()

        def add_menu(*args, **kwargs):
            win.add_menu(*args, **kwargs)

        def add_function_to_menu(*args, **kwargs):
            win.add_function_to_menu(*args, **kwargs)

        def start_display():
            win.raise_() 
            app.exec_()
    return display, start_display, add_menu, add_function_to_menu
