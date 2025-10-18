"""
Theme Manager for Osdag GUI.
Handles theme switching and persistence.
"""
from PySide6.QtCore import QSettings, QObject, Signal
from PySide6.QtCore import QFile, QTextStream


class ThemeManager(QObject):
    """Manages application themes (light/dark mode)."""
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.settings = QSettings("Osdag", "Osdag-Desktop")
        self.current_theme = self.settings.value("theme", "light")
        self.themes = {
            "light": ":/themes/lightstyle.qss",
            "dark": ":/themes/darkstyle.qss"
        }
    
    def load_theme(self, theme_name):
        """Load and apply theme stylesheet."""
        if theme_name not in self.themes:
            print(f"Theme '{theme_name}' not found. Available: {list(self.themes.keys())}")
            return False
        
        theme_file = self.themes[theme_name]
        file = QFile(theme_file)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            file.close()
            self.app.setStyleSheet(stylesheet)
            self.current_theme = theme_name
            self.settings.setValue("theme", theme_name)
            print(f"Theme changed to: {theme_name}")
            return True
        else:
            print(f"Failed to open theme file: {theme_file}")
            return False
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.load_theme(new_theme)
    
    def get_current_theme(self):
        """Get the name of the current theme."""
        return self.current_theme

    def is_light(self):
        if self.current_theme == 'light':
            return True
        else:
            return False