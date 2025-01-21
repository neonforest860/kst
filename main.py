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
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
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
        undo_action.triggered.connect(self.canvas.undo)
        
        redo_action = edit_menu.addAction("&Redo")
        redo_action.setShortcuts(["Ctrl+Shift+Z", "Ctrl+Y"])
        redo_action.triggered.connect(self.canvas.redo)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        toggle_grid_action = view_menu.addAction("Toggle &Grid")
        toggle_grid_action.setShortcut("Ctrl+G")
        toggle_grid_action.triggered.connect(self.canvas.toggle_snap_to_grid)
        
        # Theme menu
        theme_menu = menubar.addMenu("&Theme")
        theme_action = theme_menu.addAction("Toggle &Theme")
        theme_action.triggered.connect(self.toggle_theme)

    def save_schema(self):
        if self.stacked_widget.currentWidget() == self.canvas:
            filename, _ = QFileDialog.getSaveFileName(self, "Save Schema", "", "JSON Files (*.json)")
            if filename:
                self.canvas.save_schema(filename)

    def load_schema(self):
        if self.stacked_widget.currentWidget() == self.canvas:
            filename, _ = QFileDialog.getOpenFileName(self, "Load Schema", "", "JSON Files (*.json)")
            if filename:
                self.canvas.load_schema(filename)

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
        self.canvas.set_theme("dark" if self.dark_mode else "light")

def main():
    app = QApplication(sys.argv)
    window = KonectTrafficStudio()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()