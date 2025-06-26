import sys
import os
from PyQt5 import QtWidgets
from osdag.gui.ui_plugins import Ui_PluginsDialog
from osdag.data.osdag_plugins.plugin_manager import PluginManager

class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PluginsDialog()
        self.ui.setupUi(self)
        
        # flag to track if this is the first time the dialog is shown
        self._first_show = True

        print("Initializing plugin manager...")
        self.plugin_manager = PluginManager(main_win=self)  # Pass self as main_win
        self.plugin_manager.load_plugins()  # Initial plugin loading
        self.load_plugins()
        
    def showEvent(self, event):
        """Override showEvent to rescan for plugins whenever the dialog is shown again.
        This ensures newly installed plugins are discovered without requiring a restart.
        Initial plugins are loaded only once in __init__ to avoid duplicates."""
        if not self._first_show:  # Only reload plugins on subsequent shows
            print("Plugin manager dialog reopened - rescanning for new plugins...")
            # clears UI completely
            self.ui.clearPlugins()
            
            # clears existing plugins and rescan
            self.plugin_manager.plugins.clear()
            self.plugin_manager.load_plugins()  # Rescan for plugins
            
            # Reloads UI with fresh plugin data
            self.load_plugins()
            
            # Updates status message to show reload happened
            self.ui.status_label.setText(f"Plugins reloaded successfully - {len(self.plugin_manager.plugins)} found")
        
        # to mark that dialog has been shown once
        self._first_show = False
        
        # Call base class implementation
        super().showEvent(event)

    def load_plugins(self):
        try:
            self.ui.clearPlugins()
            
            plugins = self.plugin_manager.plugins
            
            for plugin_name, plugin_info in plugins.items():
                toggle_switch, delete_btn, _ = self.ui.addPlugin(
                    plugin_name,
                    f"Version: {plugin_info.version}\n"
                    f"Author: {plugin_info.author}\n"
                    f"Description: {plugin_info.description}"
                )
                
                # Connect toggle switch to handle both activate and deactivate
                toggle_switch.toggled.connect(
                    lambda checked, name=plugin_name: (
                        self.activate_plugin(name) if checked 
                        else self.deactivate_plugin(name)
                    )
                )
                delete_btn.clicked.connect(lambda _, name=plugin_name: self.delete_plugin(name))
                
            self.ui.status_label.setText("Plugins loaded successfully")
            
        except Exception as e:
            self.ui.status_label.setText(f"Error loading plugins: {str(e)}")

    def activate_plugin(self, plugin_name):
        try:
            plugin_info = self.plugin_manager.get_plugin_info(plugin_name)
            if plugin_info:
                if not hasattr(plugin_info.module, 'is_active') or not plugin_info.module.is_active:
                    plugin_info.module.register()
                    plugin_info.module.is_active = True
                    self.ui.status_label.setText(f"Plugin '{plugin_info.name}' v{plugin_info.version} activated successfully!")
            else:
                self.ui.status_label.setText(f"Plugin '{plugin_name}' not found")
        except Exception as e:
            self.ui.status_label.setText(f"Error activating {plugin_name}: {str(e)}")
    
    def deactivate_plugin(self, plugin_name):
        try:
            plugin_info = self.plugin_manager.get_plugin_info(plugin_name)
            if plugin_info:
                if hasattr(plugin_info.module, 'deactivate'):
                    if hasattr(plugin_info.module, 'is_active') and plugin_info.module.is_active:
                        plugin_info.module.deactivate()
                        plugin_info.module.is_active = False
                        self.ui.status_label.setText(f"Plugin '{plugin_info.name}' v{plugin_info.version} deactivated successfully!")
                else:
                    self.ui.status_label.setText(f"Plugin '{plugin_info.name}' does not support deactivation")
            else:
                self.ui.status_label.setText(f"Plugin '{plugin_name}' not found")
        except Exception as e:
            self.ui.status_label.setText(f"Error deactivating {plugin_name}: {str(e)}")

    def delete_plugin(self, plugin_name):
        try:
            reply = QtWidgets.QMessageBox.question(
                self,
                'Delete Plugin',
                f'Are you sure you want to delete the plugin "{plugin_name}"?',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                QtWidgets.QMessageBox.Cancel
            )

            if reply == QtWidgets.QMessageBox.Yes:
                self.ui.clearPlugins()
                
                success = self.plugin_manager._delete_plugin(plugin_name)
                
                if success:
                    self.load_plugins()
                    self.ui.status_label.setText(f"Plugin '{plugin_name}' has been successfully deleted.")
                else:
                    self.ui.status_label.setText(f"Failed to delete plugin '{plugin_name}'.")
        except Exception as e:
            self.ui.status_label.setText(f"Error deleting plugin: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
