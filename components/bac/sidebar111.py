from PyQt6.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox,
    QLineEdit, QHBoxLayout, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QSize, QMimeData, QPoint, QPropertyAnimation
from PyQt6.QtGui import QIcon, QDrag, QPixmap
from utils.styles import load_dark_theme, load_light_theme
from PyQt6.QtWidgets import QGridLayout, QFileDialog, QApplication, QMessageBox
import requests

class CollapsibleSection(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.toggle_button = QPushButton(title)
        self.toggle_button.clicked.connect(self.toggle_content)
        self.layout.addWidget(self.toggle_button)
        
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setSpacing(2)
        self.content_layout.setContentsMargins(10, 0, 0, 0)
        self.layout.addWidget(self.content)
        
        self.is_expanded = True
        self.update_theme(True)

    def toggle_content(self):
        self.is_expanded = not self.is_expanded
        self.content.setVisible(self.is_expanded)

    def addWidget(self, widget):
        self.content_layout.addWidget(widget)
        
    def setText(self, text):
        self.toggle_button.setText(text)

    def update_theme(self, dark_mode):
        style = """
            QPushButton {
                text-align: center;
                padding: 5px;
                font-weight: bold;
                background-color: %s;
                border: none;
                color: %s;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: %s;
                color: %s;
            }
        """
        if dark_mode:
            self.toggle_button.setStyleSheet(style % ("#1a1a1a", "#888888", "#3a3a3a", "white"))
        else:
            self.toggle_button.setStyleSheet(style % ("#f0f0f0", "#666666", "#e0e0e0", "black"))

class DraggableButton(QPushButton):
    def __init__(self, text, icon_path, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(32, 32))
        self.icon_path = icon_path
        self.full_text = text
        self.update_theme(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text() if self.text() else self.full_text)
            drag.setMimeData(mime_data)
            
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.setHotSpot(QPoint(pixmap.width()//2, pixmap.height()//2))
            
            drag.exec(Qt.DropAction.CopyAction | Qt.DropAction.MoveAction)
        else:
            super().mousePressEvent(event)

    def update_theme(self, dark_mode):
        style = """
            QPushButton {
                text-align: left;
                padding: 5px;
                background-color: %s;
                border: none;
                color: %s;
            }
            QPushButton:hover {
                background-color: %s;
            }
        """
        if dark_mode:
            self.setStyleSheet(style % ("#2a2a2a", "white", "#3a3a3a"))
        else:
            self.setStyleSheet(style % ("#ffffff", "black", "#e5e5e5"))

class NavigationButton(QPushButton):
    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(parent)
        self.setText(text)
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))
        self.update_theme(True)

    def update_theme(self, dark_mode):
        style = """
            QPushButton {
                text-align: left;
                padding: 10px;
                background-color: %s;
                border: none;
                color: %s;
            }
            QPushButton:hover {
                background-color: %s;
            }
        """
        if dark_mode:
            self.setStyleSheet(style % ("#1a1a1a", "white", "#3a3a3a"))
        else:
            self.setStyleSheet(style % ("#f0f0f0", "black", "#e0e0e0"))

class NavigationSidebar(QDockWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("")
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        
        self.content = QWidget()
        self.setWidget(self.content)
        self.layout = QVBoxLayout(self.content)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Add toggle button
        self.toggle_button = QPushButton()
        self.toggle_button.setIcon(QIcon("assets/icons/menu.png"))
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.layout.addWidget(self.toggle_button)

        # Add navigation buttons
        self.home_btn = NavigationButton("Konect Traffic Studio", "assets/icons/home.png")
        self.design_btn = NavigationButton("Design", "assets/icons/design.png")
        self.settings_btn = NavigationButton("Settings", "assets/icons/settings.png")
        
        self.home_btn.clicked.connect(main_window.switch_to_home)
        self.design_btn.clicked.connect(main_window.switch_to_design)
        self.settings_btn.clicked.connect(main_window.switch_to_settings)
        
        self.layout.addWidget(self.home_btn)
        self.layout.addWidget(self.design_btn)
        self.layout.addWidget(self.settings_btn)
        
        # Add stretch to push content up
        self.layout.addStretch()
        
        # Set initial state
        self.expanded = True
        self.setFixedWidth(200)

    def toggle_sidebar(self):
        width = 60 if self.expanded else 200
        
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(200)
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(width)
        self.animation.start()

        if self.expanded:
            self.home_btn.setText("")
            self.design_btn.setText("")
            self.settings_btn.setText("")
        else:
            self.home_btn.setText("Konect Traffic Studio")
            self.design_btn.setText("Design")
            self.settings_btn.setText("Settings")
        
        self.expanded = not self.expanded

    def update_theme(self, dark_mode):
        style = """
            QPushButton {
                text-align: left;
                padding: 10px;
                background-color: %s;
                border: none;
                color: %s;
            }
            QPushButton:hover {
                background-color: %s;
            }
        """
        if dark_mode:
            style = style % ("#1a1a1a", "white", "#3a3a3a")
        else:
            style = style % ("#f0f0f0", "black", "#e0e0e0")
            
        self.home_btn.setStyleSheet(style)
        self.design_btn.setStyleSheet(style)
        self.settings_btn.setStyleSheet(style)
        self.toggle_button.setStyleSheet(style)

class DesignSidebar(QDockWidget):
    def __init__(self, canvas=None):
        super().__init__()
        self.canvas = canvas
        self.setWindowTitle("Design Tools")
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        
        # Main widget and layout
        self.main_widget = QWidget()
        self.setWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Add sections
        self.setup_entity_section()
        self.setup_tpe_section()
        self.setup_algorithm_section()
        self.setup_search_section()

        # Add file operations at bottom
        self.setup_file_operations()

        # Set initial width
        self.setFixedWidth(200)
        
        # Set initial dark theme
        self.dark_mode = True
        self.update_theme(self.dark_mode)

    def setup_entity_section(self):
        self.entity_section = CollapsibleSection("Entity")
        self.main_layout.addWidget(self.entity_section)
        
        camera_types = ["CCTV", "Redlight", "Firn", "TPE", "Controller"]
        self.camera_buttons = []
        for cam_type in camera_types:
            btn = DraggableButton(cam_type, f"assets/icons/{cam_type.lower()}.png")
            self.camera_buttons.append(btn)
            self.entity_section.addWidget(btn)

    def setup_tpe_section(self):
        self.tpe_section = CollapsibleSection("TPE")
        self.main_layout.addWidget(self.tpe_section)
        
        self.tpe_combo = QComboBox()
        self.tpe_combo.addItems([f"TPE {i}" for i in range(1, 6)])
        self.tpe_section.addWidget(self.tpe_combo)

    def setup_algorithm_section(self):
        self.algo_section = CollapsibleSection("Algorithm")
        self.main_layout.addWidget(self.algo_section)
        
        self.algo_button = DraggableButton("BasiQ", "assets/icons/algorithm.png")
        self.algo_section.addWidget(self.algo_button)

    def setup_search_section(self):
        search_widget = QWidget()
        search_layout = QVBoxLayout(search_widget)
        search_layout.setContentsMargins(5, 5, 5, 5)
        
        search_label = QLabel("Location Search")
        search_label.setStyleSheet("color: #888888; font-size: 12px;")
        search_layout.addWidget(search_label)
        
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search location...")
        input_layout.addWidget(self.search_input)
        
        search_button = QPushButton()
        search_button.setIcon(QIcon("assets/icons/search.png"))
        search_button.setFixedSize(30, 30)
        input_layout.addWidget(search_button)
        
        search_layout.addWidget(input_container)
        self.main_layout.addWidget(search_widget)

    def setup_file_operations(self):
        # Create container for file operation buttons
        file_container = QWidget()
        file_layout = QGridLayout(file_container)
        file_layout.setSpacing(5)
        file_layout.setContentsMargins(5, 5, 5, 5)

        # Create file operation buttons
        self.save_btn = QPushButton("Save")
        self.load_btn = QPushButton("Load")
        self.image_btn = QPushButton("Image")
        self.exit_btn = QPushButton("Exit")

        # Set icons for buttons
        self.save_btn.setIcon(QIcon("assets/icons/save.png"))
        self.load_btn.setIcon(QIcon("assets/icons/load.png"))
        self.image_btn.setIcon(QIcon("assets/icons/image.png"))
        self.exit_btn.setIcon(QIcon("assets/icons/exit.png"))

        # Add buttons to grid layout (2x2)
        file_layout.addWidget(self.save_btn, 0, 0)
        file_layout.addWidget(self.load_btn, 0, 1)
        file_layout.addWidget(self.image_btn, 1, 0)
        file_layout.addWidget(self.exit_btn, 1, 1)

        # Connect button signals
        self.save_btn.clicked.connect(self.save_schema)
        self.load_btn.clicked.connect(self.load_schema)
        self.image_btn.clicked.connect(self.save_as_image)
        self.exit_btn.clicked.connect(QApplication.instance().quit)

        # Add stretch to push file container to bottom
        self.main_layout.addStretch()
        
        # Add file container to main layout
        self.main_layout.addWidget(file_container)

    def update_theme(self, dark_mode):
        self.dark_mode = dark_mode
        if dark_mode:
            self.setStyleSheet(load_dark_theme())
        else:
            self.setStyleSheet(load_light_theme())

        # Update section themes
        if hasattr(self, 'entity_section'):
            self.entity_section.update_theme(dark_mode)
        if hasattr(self, 'tpe_section'):
            self.tpe_section.update_theme(dark_mode)
        if hasattr(self, 'algo_section'):
            self.algo_section.update_theme(dark_mode)

        # Update button themes
        for btn in self.camera_buttons:
            btn.update_theme(dark_mode)
        if hasattr(self, 'algo_button'):
            self.algo_button.update_theme(dark_mode)

    def save_schema(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "Save Schema", 
            "", 
            "Konect Traffic Studio Files (*.kst)"
        )
        if filename:
            if not filename.endswith('.kst'):
                filename += '.kst'
            self.canvas.save_schema(filename)

    def load_schema(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            "Load Schema", 
            "", 
            "Konect Traffic Studio Files (*.kst)"
        )
        if filename:
            self.canvas.load_schema(filename)

    
    def save_as_image(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "Save as Image", 
            "", 
            "PNG Files (*.png);;JPEG Files (*.jpg)")
        if filename:
            self.canvas.save_as_image(filename)

    def get_data(self):
        return {
            "ip": self.ip_edit.text() if hasattr(self, 'ip_edit') else "",
            "port": self.port_edit.text() if hasattr(self, 'port_edit') else "",
            "username": self.user_edit.text() if hasattr(self, 'user_edit') else "",
            "password": self.pass_edit.text() if hasattr(self, 'pass_edit') else ""
        }

    def search_location(self):
        search_text = self.search_input.text()
        if search_text and self.canvas:
            self.canvas.show_map_overlay()
            self.canvas.search_location(search_text)

    def show_suggestions(self):
        pos = self.search_input.mapToGlobal(self.search_input.rect().bottomLeft())
        width = self.search_input.width()
        height = min(200, self.suggestions_list.sizeHintForRow(0) * 
                    self.suggestions_list.count() + 10)
        self.suggestions_list.setGeometry(pos.x(), pos.y(), width, height)
        self.suggestions_list.show()
        self.suggestions_list.raise_()

    def on_suggestion_clicked(self, item):
        try:
            data = item.data(Qt.ItemDataRole.UserRole)
            display_text = item.text()
            
            self.suggestions_list.hide()
            self.search_input.setText(display_text)
            
            if self.canvas:
                self.canvas.search_location(data['lat'], data['lon'])
            
            self.last_location = data
            
        except Exception as e:
            print(f"Error handling suggestion click: {e}")