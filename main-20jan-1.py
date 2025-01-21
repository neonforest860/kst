# main.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from components.sidebar import NavigationSidebar, DesignSidebar
from components.canvas import Canvas
from components.settings_panel import SettingsPanel
from utils.styles import load_styles, load_dark_theme, load_light_theme

class HomeView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Konect Traffic Studio")
        title.setStyleSheet("""
            QLabel {
                font-size: 48px;
                color: white;
                font-weight: bold;
            }
        """)
        layout.addWidget(title)

class KonectTrafficStudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konect Traffic Studio v1.1")
        self.dark_mode = True
        self.setStyleSheet(load_dark_theme())
        self.setMinimumSize(1200, 800)
        
        # Create stacked widget for different views
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create views
        self.home_view = HomeView()
        self.canvas = Canvas()
        self.settings_panel = SettingsPanel(self)
        
        # Add views to stacked widget
        self.stacked_widget.addWidget(self.home_view)  # index 0
        self.stacked_widget.addWidget(self.canvas)     # index 1
        self.stacked_widget.addWidget(self.settings_panel)  # index 2
        
        # Add main navigation sidebar
        self.nav_sidebar = NavigationSidebar(self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.nav_sidebar)
        
        # Create design sidebar (initially hidden)
        self.design_sidebar = DesignSidebar()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.design_sidebar)
        self.design_sidebar.hide()
        
        # Create menu bar
        self.create_menu_bar()
        
    # def create_menu_bar(self):        20jan-1
    #     menubar = self.menuBar()
        
    #     # File menu
    #     file_menu = menubar.addMenu("File")
        
    #     save_action = file_menu.addAction("Save")
    #     save_action.setShortcut("Ctrl+S")
    #     save_action.triggered.connect(self.canvas.save_schema)
        
    #     load_action = file_menu.addAction("Load")
    #     load_action.setShortcut("Ctrl+O")
    #     load_action.triggered.connect(self.canvas.load_schema)
        
    #     # Edit menu
    #     edit_menu = menubar.addMenu("Edit")
        
    #     undo_action = edit_menu.addAction("Undo")
    #     undo_action.setShortcut("Ctrl+Z")
    #     undo_action.triggered.connect(self.canvas.undo)
        
    #     redo_action = edit_menu.addAction("Redo")
    #     redo_action.setShortcut("Ctrl+Shift+Z")
    #     redo_action.triggered.connect(self.canvas.redo)
        
    #     # View menu
    #     view_menu = menubar.addMenu("View")
        
    #     toggle_grid_action = view_menu.addAction("Toggle Grid")
    #     toggle_grid_action.setShortcut("Ctrl+G")
    #     toggle_grid_action.triggered.connect(self.canvas.toggle_snap_to_grid)

    def switch_to_home(self):
        self.stacked_widget.setCurrentWidget(self.home_view)
        self.design_sidebar.hide()

    def switch_to_design(self):
        self.stacked_widget.setCurrentWidget(self.canvas)
        self.design_sidebar.show()

    def switch_to_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings_panel)
        self.design_sidebar.hide()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet(load_dark_theme())
        else:
            self.setStyleSheet(load_light_theme())
        self.nav_sidebar.update_theme(self.dark_mode)
        self.design_sidebar.update_theme(self.dark_mode)
        self.canvas.set_theme(self.dark_mode)  # Add this line

    def create_menu_bar(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #f0f0f0;
                color: black;
            }
            QMenuBar::item:selected {
                background-color: #0078d7;
                color: white;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu("&File")  # Add & for keyboard navigation
        
        save_action = file_menu.addAction("&Save")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_schema)
        
        load_action = file_menu.addAction("&Load")
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.load_schema)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        undo_action = edit_menu.addAction("&Undo")
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.central_widget.undo)
        
        redo_action = edit_menu.addAction("&Redo")
        # Add both Ctrl+Shift+Z and Ctrl+Y shortcuts
        redo_action.setShortcuts(["Ctrl+Shift+Z", "Ctrl+Y"])
        redo_action.triggered.connect(self.central_widget.redo)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        toggle_grid_action = view_menu.addAction("Toggle &Grid Snap")
        toggle_grid_action.setShortcut("Ctrl+G")
        toggle_grid_action.triggered.connect(self.central_widget.toggle_snap_to_grid)
        
        toggle_connection_mode = view_menu.addAction("Toggle &Connection Mode")
        toggle_connection_mode.setShortcut("Ctrl+L")
        toggle_connection_mode.triggered.connect(self.toggle_connection_mode)
        
        # Theme menu
        theme_menu = menubar.addMenu("&Theme")
        
        light_theme_action = theme_menu.addAction("&Light Mode")
        light_theme_action.triggered.connect(self.set_light_theme)
        
        dark_theme_action = theme_menu.addAction("&Dark Mode")
        dark_theme_action.triggered.connect(self.set_dark_theme)

def main():
    app = QApplication(sys.argv)
    window = KonectTrafficStudio()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()