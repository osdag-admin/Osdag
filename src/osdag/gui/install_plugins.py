import os
import sys
import json
import urllib.request
import zipfile
import shutil
import tempfile
import threading
from pathlib import Path

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                            QScrollArea, QWidget, QProgressBar, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, QSize

class PluginItemWidget(QFrame):
    def __init__(self, name, description, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet("QFrame { border: 1px solid #cccccc; border-radius: 5px; padding: 10px; }")
        
        layout = QHBoxLayout(self)
        
        info_layout = QVBoxLayout()
        
        name_label = QLabel(name)
        name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        info_layout.addWidget(name_label)
        
        if description:
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            info_layout.addWidget(desc_label)
        
        layout.addLayout(info_layout, 1)  
        
        self.install_button = QPushButton("Install")
        self.install_button.setFixedWidth(100)
        layout.addWidget(self.install_button)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(100)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        
        self.status_label = QLabel()
        self.status_label.setFixedWidth(100)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)

class InstallPluginsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Install Plugins")
        self.resize(600, 400)
        
        self.repo_url = "https://github.com/aathi-star/available-plugins.git"
        self.api_url = "https://api.github.com/repos/aathi-star/available-plugins/contents"
        
        self.plugins_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                    "data", "osdag_plugins", "plugins")
        
        
        os.makedirs(self.plugins_dir, exist_ok=True)
        
        self.setup_ui()
        
        self.fetch_available_plugins()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        title_label = QLabel("Available Plugins")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        self.status_label = QLabel("Loading available plugins...")
        layout.addWidget(self.status_label)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.plugins_layout = QVBoxLayout(self.scroll_content)
        self.plugins_layout.setAlignment(Qt.AlignTop)
        scroll_area.setWidget(self.scroll_content)
        layout.addWidget(scroll_area)
        
        # Bottom buttons
        buttons_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.fetch_available_plugins)
        buttons_layout.addWidget(self.refresh_button)
        
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.close_button)
        
        layout.addLayout(buttons_layout)
    
    def fetch_available_plugins(self):
        self.clear_plugins()
        self.status_label.setText("Loading available plugins...")
        self.refresh_button.setEnabled(False)
        
        threading.Thread(target=self._fetch_plugins_thread, daemon=True).start()
    
    def _fetch_plugins_thread(self):
        try:
            with urllib.request.urlopen(self.api_url) as response:
                data = json.loads(response.read().decode())
                plugins = [item for item in data if item.get('name', '').endswith('.zip')]
                
                QtCore.QMetaObject.invokeMethod(self, "_update_plugins_ui",
                                            Qt.QueuedConnection,
                                            QtCore.Q_ARG(list, plugins))
        
        except Exception as e:
            QtCore.QMetaObject.invokeMethod(self, "_show_error",
                                         Qt.QueuedConnection,
                                         QtCore.Q_ARG(str, str(e)))
    @QtCore.pyqtSlot(list)
    def _update_plugins_ui(self, plugins):
        if not plugins:
            self.status_label.setText("No plugins available")
            self.refresh_button.setEnabled(True)
            return 
        for plugin in plugins:
            name = plugin.get('name', '').replace('.zip', '')
            description = f"Size: {self._format_size(plugin.get('size', 0))} | Click Install to download"
            download_url = plugin.get('download_url', '')
            
            plugin_widget = PluginItemWidget(name, description)
            plugin_widget.install_button.clicked.connect(
                lambda checked, url=download_url, widget=plugin_widget, name=name: 
                self.install_plugin(url, widget, name)
            )
            
            self.plugins_layout.addWidget(plugin_widget)
        
        self.status_label.setText(f"Found {len(plugins)} available plugins")
        self.refresh_button.setEnabled(True)
    
    @QtCore.pyqtSlot(str)
    def _show_error(self, error_msg):
        self.status_label.setText(f"Error: {error_msg}")
        self.refresh_button.setEnabled(True)
        QMessageBox.critical(self, "Error", f"Failed to fetch plugins: {error_msg}")
    
    def _format_size(self, size_bytes):
        """Format size in bytes to text """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    def clear_plugins(self):
        """Clear all plugins from the layout"""
        while self.plugins_layout.count():
            item = self.plugins_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def install_plugin(self, download_url, widget, plugin_name):
        """Install a plugin from the given URL"""
        # Disable install button
        widget.install_button.setEnabled(False)
        widget.install_button.setVisible(False)
        widget.progress_bar.setVisible(True)
        widget.progress_bar.setValue(0)
        
        # Start thread to download and install the plugin
        threading.Thread(
            target=self._install_plugin_thread, 
            args=(download_url, widget, plugin_name), 
            daemon=True
        ).start()
    
    def _install_plugin_thread(self, download_url, widget, plugin_name):
        temp_dir = None
        try:
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, f"{plugin_name}.zip")
            
            QtCore.QMetaObject.invokeMethod(widget.progress_bar, "setValue",
                                        Qt.QueuedConnection,
                                        QtCore.Q_ARG(int, 10))
            
            with urllib.request.urlopen(download_url) as response, open(zip_path, 'wb') as out_file:
                file_size = int(response.info().get('Content-Length', 0))
                downloaded = 0
                block_size = 8192
                
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    
                    downloaded += len(buffer)
                    out_file.write(buffer)
                    
                    if file_size > 0:
                        progress = int(30 + (downloaded / file_size * 40))
                        QtCore.QMetaObject.invokeMethod(widget.progress_bar, "setValue",
                                                    Qt.QueuedConnection,
                                                    QtCore.Q_ARG(int, progress))
            
            QtCore.QMetaObject.invokeMethod(widget.progress_bar, "setValue",
                                         Qt.QueuedConnection,
                                         QtCore.Q_ARG(int, 70))
            
            plugin_target_dir = os.path.join(self.plugins_dir, plugin_name)
            os.makedirs(plugin_target_dir, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(plugin_target_dir)
            
            QtCore.QMetaObject.invokeMethod(self, "_installation_complete",
                                        Qt.QueuedConnection,
                                        QtCore.Q_ARG(QWidget, widget),
                                        QtCore.Q_ARG(str, plugin_name))
        except Exception as e:
            # Handle installation error
            QtCore.QMetaObject.invokeMethod(self, "_installation_error",
                                        Qt.QueuedConnection,
                                        QtCore.Q_ARG(QWidget, widget),
                                        QtCore.Q_ARG(str, str(e)))
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
    
    @QtCore.pyqtSlot(QWidget, str)
    def _installation_complete(self, widget, plugin_name):
        widget.progress_bar.setValue(100)
        widget.progress_bar.setVisible(False)
        widget.status_label.setVisible(True)
        widget.status_label.setText("Installed")
        widget.status_label.setStyleSheet("color: green; font-weight: bold;")
        
        QMessageBox.information(self, "Installation Complete", 
                              f"Plugin '{plugin_name}' has been successfully installed.\n\n"
                              "Reopen Plugin Manager to use the plugin")
    
    @QtCore.pyqtSlot(QWidget, str)
    def _installation_error(self, widget, error_msg):
        widget.progress_bar.setVisible(False)
        widget.status_label.setVisible(True)
        widget.status_label.setText("Failed")
        widget.status_label.setStyleSheet("color: red; font-weight: bold;")
        
        QMessageBox.critical(self, "Installation Error", 
                           f"Failed to install plugin: {error_msg}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = InstallPluginsDialog()
    dialog.show()
    sys.exit(app.exec_())
