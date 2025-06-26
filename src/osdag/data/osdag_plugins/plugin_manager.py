import os
import importlib.util
import sys
from typing import Dict, Any, Optional
from importlib.metadata import entry_points
from dataclasses import dataclass
import subprocess
import shutil
import stat
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

@dataclass
class PluginInfo:
    #storing plugin metadata
    name: str
    version: str
    description: str
    author: str
    module: Any
    location: Optional[str] = None

class PluginManager:
    def __init__(self, main_win=None):
        self.plugins: Dict[str, PluginInfo] = {}
        self.main_win = main_win
        
    def _get_main_window(self):
        """ To get the main window instance if not provided during initialization"""
        #checks if main_win was provided during initialization,
        if self.main_win is not None:
            return self.main_win
            
        # Otherwise, uses from active Qt application
        try:
            from PyQt5.QtWidgets import QApplication
            from osdag.osdagMainPage import OsdagMainWindow
            
            for widget in QApplication.instance().topLevelWidgets():
                if isinstance(widget, OsdagMainWindow):
                    self.main_win = widget
                    return self.main_win
        except Exception as e:
            print(f"Error finding main window: {str(e)}")
            
        return None

    def load_plugins(self):
        """Load plugins from entry points and local directory."""
        print("Starting plugin loading process...")
        self.plugins.clear()  
        self._load_from_entry_points()
        
        print("Checking local directory for additional plugins...")
        self._load_from_directory()
        
        if self.plugins:
            print("Loaded plugins:")
            for name, info in self.plugins.items():
                print(f"- {name} (v{info.version})")
        else:
            print("No plugins were loaded.")

    def _load_from_entry_points(self):
        try:
            print("Searching for entry points in group 'osdag.plugins'...")
            
            # using pkg_resources 
            try:
                import pkg_resources
                entry_points = list(pkg_resources.iter_entry_points(group='osdag.plugins'))
                print(f"Found {len(entry_points)} entry points using pkg_resources")
                
                for entry_point in entry_points:
                    print(f"Attempting to load plugin from entry point: {entry_point.name}")
                    try:
                        plugin_class = entry_point.load()
                        print(f"Loaded class {plugin_class.__name__} from entry point")
                        plugin_instance = plugin_class()
                        
                        if hasattr(plugin_instance, 'register'):
                            plugin_info = PluginInfo(
                                name=getattr(plugin_instance, 'name', entry_point.name),
                                version=getattr(plugin_instance, 'version', '0.1.0'),
                                description=getattr(plugin_instance, 'description', ''),
                                author=getattr(plugin_instance, 'author', 'Unknown'),
                                module=plugin_instance
                            )
                            self.plugins[entry_point.name] = plugin_info
                            print(f"Successfully loaded plugin from entry point: {entry_point.name} v{plugin_info.version}")
                        else:
                            print(f"Plugin {entry_point.name} does not have register() function.")
                    except Exception as e:
                        print(f"Error loading plugin {entry_point.name}: {str(e)}")
                
                if self.plugins:
                    return
            except ImportError:
                print("pkg_resources not available, falling back to importlib.metadata")
            except Exception as e:
                print(f"Error using pkg_resources: {str(e)}")
                
            # Fallback to importlib.metadata
            try:
                from importlib.metadata import entry_points as get_entry_points
                all_entry_points = get_entry_points()
                
                # to handle different return types from entry_points()
                if isinstance(all_entry_points, dict):
                    # for handling dict
                    osdag_plugins = all_entry_points.get('osdag.plugins', [])
                else:
                    # to handle return object with select method
                    try:
                        osdag_plugins = all_entry_points.select(group='osdag.plugins')
                    except AttributeError:
                        # to handle list 
                        osdag_plugins = []
                        for ep in all_entry_points:
                            try:
                                if hasattr(ep, 'group') and ep.group == 'osdag.plugins':
                                    osdag_plugins.append(ep)
                            except Exception:
                                pass  
                print(f"Found {len(osdag_plugins)} entry points using importlib.metadata")
                
                for plugin_entry in osdag_plugins:
                    print(f"Attempting to load plugin from entry point: {plugin_entry.name}")
                    try:
                        self._load_plugin_from_entry(plugin_entry)
                    except Exception as e:
                        print(f"Error loading plugin {plugin_entry.name}: {str(e)}")
            except Exception as e:
                print(f"Error using importlib.metadata: {str(e)}")
        except Exception as e:
            print(f"Error discovering plugins via entry points: {str(e)}")

    def _load_from_directory(self):
        plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')
        print(f"Searching for plugins in directory: {plugin_dir}")
        
        if not os.path.exists(plugin_dir):
            print(f"Plugin directory not found: {plugin_dir}")
            return

        # Directories to ignore
        ignore_dirs = {'__pycache__', '.egg-info'}
        
        for plugin_name in os.listdir(plugin_dir):
            if plugin_name in ignore_dirs or plugin_name.endswith('.egg-info'):
                continue
                
            plugin_path = os.path.join(plugin_dir, plugin_name)
            if not os.path.isdir(plugin_path):
                continue
                
            print(f"Found potential plugin directory: {plugin_name}")
            
            # Check for specific plugin subdirectories
            for subdir in os.listdir(plugin_path):
                if subdir in ignore_dirs or subdir.endswith('.egg-info'):
                    continue
                    
                subdir_path = os.path.join(plugin_path, subdir)
                if not os.path.isdir(subdir_path):
                    continue
                    
                # Check if subdirectory has __init__.py
                init_file = os.path.join(subdir_path, '__init__.py')
                if os.path.exists(init_file):
                    print(f"Found plugin with __init__.py: {plugin_name}/{subdir}")
                    try:
                        self._try_load_plugin_from_directory(plugin_name, subdir_path)
                    except Exception as e:
                        print(f"Error loading plugin from {plugin_name}/{subdir}: {str(e)}")

    def _try_load_plugin_from_directory(self, plugin_name: str, plugin_path: str) -> bool:
        """Try to load a plugin from a directory. Returns True if successful."""
        init_path = os.path.join(plugin_path, '__init__.py')
        if not os.path.exists(init_path):
            print(f"No __init__.py found in {plugin_path}")
            return False

        try:
            print(f"Attempting to load plugin from: {plugin_path}")
            spec = importlib.util.spec_from_file_location(plugin_name, init_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[plugin_name] = module
                spec.loader.exec_module(module)
                
                plugin_class = None
                if hasattr(module, 'plugin_class'):
                    plugin_class = getattr(module, 'plugin_class')
                else:
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and hasattr(attr, 'register'):
                            plugin_class = attr
                            break
                
                if plugin_class:
                    try:
                        plugin_instance = plugin_class()
                        plugin_instance.is_active = False
                        
                        # validation to ensure this is a proper plugin
                        if not hasattr(plugin_instance, 'register') or not callable(plugin_instance.register):
                            print(f"Skipping invalid plugin {plugin_name}: missing register() method")
                            return False
                    except Exception as e:
                        print(f"Error initializing plugin {plugin_name}: {str(e)}")
                        return False
                    
                    if hasattr(plugin_instance, 'register'):
                        # Get the root plugin directory (parent of the current path)
                        root_plugin_dir = os.path.dirname(plugin_path)
                        plugin_info = PluginInfo(
                            name=getattr(plugin_instance, 'name', plugin_name),
                            version=getattr(plugin_instance, 'version', '0.1.0'),
                            description=getattr(plugin_instance, 'description', ''),
                            author=getattr(plugin_instance, 'author', 'Unknown'),
                            module=plugin_instance,
                            location=root_plugin_dir  # Store the root plugin directory
                        )
                        self.plugins[plugin_name] = plugin_info
                        # Storing main window reference in the plugin instance
                        # Uses _get_main_window to find main window if not provided
                        plugin_instance.main_win = self._get_main_window()
                        print(f"Successfully loaded plugin from directory: {plugin_name} v{plugin_info.version}")
                        return True
                    else:
                        print(f"Plugin class in {plugin_name} does not have register() method")
                else:
                    print(f"No valid plugin class found in {plugin_name}")
            else:
                print(f"Could not load specification for plugin: {plugin_name}")
        except Exception as e:
            print(f"Error loading plugin {plugin_name}: {str(e)}")
            print(f"Full plugin path: {plugin_path}")
        return False

    def _load_plugin_from_entry(self, plugin_entry):
        try:
            plugin_class = plugin_entry.load()
            print(f"Loaded class {plugin_class.__name__} from entry point")
            plugin_instance = plugin_class()
            
            if hasattr(plugin_instance, 'register'):
                plugin_info = PluginInfo(
                    name=getattr(plugin_instance, 'name', plugin_entry.name),
                    version=getattr(plugin_instance, 'version', '0.1.0'),
                    description=getattr(plugin_instance, 'description', ''),
                    author=getattr(plugin_instance, 'author', 'Unknown'),
                    module=plugin_instance
                )
                self.plugins[plugin_entry.name] = plugin_info
                # Storing main window reference in the plugin instance
                # Uses _get_main_window to find main window if not provided
                plugin_instance.main_win = self._get_main_window()
                print(f"Successfully loaded plugin from entry point: {plugin_entry.name} v{plugin_info.version}")
                return True
            else:
                print(f"Plugin {plugin_entry.name} does not have register() function.")
                return False
        except Exception as e:
            print(f"Error loading plugin {plugin_entry.name}: {str(e)}")
            return False

    def get_plugin_info(self, plugin_name: str) -> PluginInfo:
        return self.plugins.get(plugin_name)

    def _show_delete_confirmation(self, plugin_name: str):
        """confirmation dialog before deleting a plugin."""
        reply = QMessageBox.question(
            None,
            'Delete Plugin',
            f'Are you sure you want to delete the plugin "{plugin_name}"?',
            QMessageBox.Yes | QMessageBox.Cancel,
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Yes:
            self._delete_plugin(plugin_name)

    def _delete_plugin(self, plugin_name: str):
        """Deletes a plugin and its directory."""
        plugin_info = self.get_plugin_info(plugin_name)
        if not plugin_info:
            print(f"Plugin {plugin_name} not found")
            return False

        try:
            # Uninstall using pip
            result = subprocess.run(
                ['pip', 'uninstall', '-y', plugin_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"Successfully uninstalled {plugin_name}")
                
                # Remove plugin directory
                if plugin_info.location and os.path.exists(plugin_info.location):
                    try:
                        def handle_remove_readonly(func, path, exc):
                            if not os.access(path, os.W_OK):
                                os.chmod(path, stat.S_IWRITE)
                                func(path)
                            else:
                                raise
                        
                        plugin_dir = os.path.join(plugin_info.location)
                        if os.path.exists(plugin_dir):
                            shutil.rmtree(plugin_dir, ignore_errors=False, onerror=handle_remove_readonly)
                            print(f"Successfully removed plugin directory: {plugin_dir}")
                        
                    except Exception as e:
                        print(f"Error removing plugin directory: {e}")
                        return False
                
                # Remove from plugin list
                if plugin_name in self.plugins:
                    del self.plugins[plugin_name]
                    
                return True
            else:
                print(f"Failed to uninstall plugin: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error deleting plugin: {str(e)}")
            return False
