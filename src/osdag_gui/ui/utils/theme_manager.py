"""
Theme Manager for Osdag GUI.
Handles theme switching and persistence.
"""
from PySide6.QtCore import QSettings, QObject, Signal
from PySide6.QtCore import QFile, QTextStream
from PySide6.QtGui import QPalette, QColor


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
        self.theme_cache = {}
        self._preload_themes()
    
    def _preload_themes(self):
        """Read and cache theme stylesheets."""
        for name, path in self.themes.items():
            file = QFile(path)
            if file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(file)
                self.theme_cache[name] = stream.readAll()
                file.close()
            else:
                print(f"Failed to preload theme: {name} from {path}")
                pass

    def load_theme(self, theme_name):
        """Load and apply theme stylesheet."""
        if theme_name not in self.themes:
            # print(f"Theme '{theme_name}' not found. Available: {list(self.themes.keys())}")
            return False
        
        stylesheet = self.theme_cache.get(theme_name)
        if stylesheet:
            self.app.setStyleSheet(stylesheet)
            self.set_palette(theme_name)
            self.current_theme = theme_name
            self.settings.setValue("theme", theme_name)
            # print(f"Theme changed to: {theme_name}")
            return True
        else:
            # print(f"Theme content not found in cache for: {theme_name}")
            return False
    
    def set_palette(self, theme_name):
        """Set the application palette to match the theme."""
        palette = QPalette()
        if theme_name == "light":
            palette.setColor(QPalette.Window, QColor("#f4f4f4"))
            palette.setColor(QPalette.WindowText, QColor("#000000"))
            palette.setColor(QPalette.Base, QColor("#ffffff"))
            palette.setColor(QPalette.AlternateBase, QColor("#f4f4f4"))
            palette.setColor(QPalette.ToolTipBase, QColor("#ffffff"))
            palette.setColor(QPalette.ToolTipText, QColor("#000000"))
            palette.setColor(QPalette.Text, QColor("#000000"))
            palette.setColor(QPalette.Button, QColor("#f4f4f4"))
            palette.setColor(QPalette.ButtonText, QColor("#000000"))
            palette.setColor(QPalette.BrightText, QColor("#ff0000"))
            palette.setColor(QPalette.Link, QColor("#2a82da"))
            palette.setColor(QPalette.Highlight, QColor("#90AF13"))
            palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        else:
            palette.setColor(QPalette.Window, QColor("#282828"))
            palette.setColor(QPalette.WindowText, QColor("#D0D0D0"))
            palette.setColor(QPalette.Base, QColor("#333333"))
            palette.setColor(QPalette.AlternateBase, QColor("#282828"))
            palette.setColor(QPalette.ToolTipBase, QColor("#2B2B2B"))
            palette.setColor(QPalette.ToolTipText, QColor("#D0D0D0"))
            palette.setColor(QPalette.Text, QColor("#D0D0D0"))
            palette.setColor(QPalette.Button, QColor("#353535"))
            palette.setColor(QPalette.ButtonText, QColor("#D0D0D0"))
            palette.setColor(QPalette.BrightText, QColor("#ff0000"))
            palette.setColor(QPalette.Link, QColor("#2a82da"))
            palette.setColor(QPalette.Highlight, QColor("#6B7D20"))
            palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        
        self.app.setPalette(palette)

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