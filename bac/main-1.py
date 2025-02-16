# main.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt
from components.sidebar import Sidebar
from components.canvas import Canvas
from components.settings_panel import SettingsPanel
from utils.styles import load_styles, load_dark_theme, load_light_theme

class KonectTrafficStudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konect Traffic Studio v1.1")
        self.setStyleSheet(load_styles())
        self.setMinimumSize(1200, 800)
        
        # Create stacked widget for different views
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create canvas for design view
        self.canvas = Canvas()
        self.stacked_widget.addWidget(self.canvas)
        
        # Create settings panel
        self.settings_panel = SettingsPanel()
        self.stacked_widget.addWidget(self.settings_panel)
        
        # Add main sidebar
        self.sidebar = Sidebar(self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Set dark mode as default
        self.dark_mode = True

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        save_action = file_menu.addAction("Save")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.canvas.save_schema)
        
        load_action = file_menu.addAction("Load")
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.canvas.load_schema)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        undo_action = edit_menu.addAction("Undo")
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.canvas.undo)
        
        redo_action = edit_menu.addAction("Redo")
        redo_action.setShortcut("Ctrl+Shift+Z")
        redo_action.triggered.connect(self.canvas.redo)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        toggle_grid_action = view_menu.addAction("Toggle Grid")
        toggle_grid_action.setShortcut("Ctrl+G")
        toggle_grid_action.triggered.connect(self.canvas.toggle_snap_to_grid)

    def switch_to_design(self):
        self.stacked_widget.setCurrentWidget(self.canvas)

    def switch_to_home(self):
        # You can create a home widget if needed
        pass

    def switch_to_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings_panel)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet(load_dark_theme())
        else:
            self.setStyleSheet(load_light_theme())

def main():
    app = QApplication(sys.argv)
    window = KonectTrafficStudio()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()