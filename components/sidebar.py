# components/sidebar.py
from PyQt6.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox,
    QLineEdit, QHBoxLayout, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QSize, QMimeData, QPoint, QPropertyAnimation
from PyQt6.QtGui import QIcon, QDrag, QPixmap
from utils.styles import load_dark_theme, load_light_theme
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
        self.update_theme(True)  # Default to dark theme

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
        self.update_theme(True)  # Default to dark theme

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
        self.update_theme(True)  # Default to dark theme

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

# Continue with NavigationSidebar and DesignSidebar classes...

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
        
        # Add stretch at the bottom
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
    # def __init__(self, canvas=None):
    #     super().__init__()
    #     self.canvas = canvas
    #     self.setWindowTitle("Design Tools")
    #     self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        
    #     # Create main widget and layout
    #     self.main_widget = QWidget()
    #     self.setWidget(self.main_widget)
    #     self.main_layout = QVBoxLayout(self.main_widget)
    #     self.main_layout.setSpacing(0)
    #     self.main_layout.setContentsMargins(0, 0, 0, 0)

    #     # Add sections
    #     self.setup_entity_section()
    #     self.setup_tpe_section()
    #     self.setup_algorithm_section()
    #     self.setup_search_section()

    #     # Set initial width
    #     self.setFixedWidth(200)
    # main.py
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

        # Set initial width
        self.setFixedWidth(200)
        
        # Set initial dark theme
        self.dark_mode = True
        self.update_theme(self.dark_mode)

    def setup_entity_section(self):
        self.entity_section = CollapsibleSection("Entity")
        self.main_layout.addWidget(self.entity_section)
        
        # Camera types
        camera_types = ["CCTV", "Redlight", "Firn", "TPE", "Controller"]
        self.camera_buttons = []
        for cam_type in camera_types:
            btn = DraggableButton(cam_type, f"assets/icons/{cam_type.lower()}.png")
            self.camera_buttons.append(btn)
            self.entity_section.addWidget(btn)

    def setup_tpe_section(self):
        self.tpe_section = CollapsibleSection("TPE")
        self.main_layout.addWidget(self.tpe_section)
        
        # TPE selection combo
        self.tpe_combo = QComboBox()
        self.tpe_combo.addItems([f"TPE {i}" for i in range(1, 6)])
        self.tpe_combo.setStyleSheet("""
            QComboBox {
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
            QComboBox:hover {
                border: 1px solid #666666;
            }
        """)
        self.tpe_section.addWidget(self.tpe_combo)

    def setup_algorithm_section(self):
        self.algo_section = CollapsibleSection("Algorithm")
        self.main_layout.addWidget(self.algo_section)
        
        # Algorithm button
        self.algo_button = DraggableButton("BasiQ", "assets/icons/algorithm.png")
        self.algo_section.addWidget(self.algo_button)

        # Add stretch after sections
        self.main_layout.addStretch()

    def setup_search_section(self):
        # Create search container
        search_widget = QWidget()
        search_layout = QVBoxLayout(search_widget)
        search_layout.setContentsMargins(5, 5, 5, 5)
        
        # Search label
        search_label = QLabel("Location Search")
        search_label.setStyleSheet("color: #888888; font-size: 12px;")
        search_layout.addWidget(search_label)
        
        # Search input and button container
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search location...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #555555;
                border-radius: 3px;
                background: #2a2a2a;
                color: white;
            }
            QLineEdit:focus {
                border: 1px solid #00ffff;
            }
        """)
        
        # Create suggestions list widget
        self.suggestions_list = QListWidget(self)
        self.suggestions_list.setWindowFlags(Qt.WindowType.Popup)
        self.suggestions_list.setStyleSheet("""
            QListWidget {
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #555555;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #3a3a3a;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
        """)
        self.suggestions_list.itemClicked.connect(self.on_suggestion_clicked)
        self.suggestions_list.hide()
        
        input_layout.addWidget(self.search_input)
        
        # Search button
        search_button = QPushButton()
        search_button.setIcon(QIcon("assets/icons/search.png"))
        search_button.setFixedSize(30, 30)
        search_button.clicked.connect(self.search_location)
        search_button.setStyleSheet("""
            QPushButton {
                background: #2a2a2a;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 3px;
            }
            QPushButton:hover {
                background: #3a3a3a;
                border: 1px solid #666666;
            }
        """)
        input_layout.addWidget(search_button)
        
        search_layout.addWidget(input_container)
        self.main_layout.addWidget(search_widget)

    def search_location(self):
        print("Search location called")  # Debug print
        search_text = self.search_input.text()
        if search_text and self.canvas:
            self.canvas.show_map_overlay()
            print("Map overlay shown")  # Debug print
            self.canvas.search_location(search_text)
            print("Location search executed")  # Debug print

    def update_theme(self, dark_mode):
        self.dark_mode = dark_mode
        if dark_mode:
            self.setStyleSheet(load_dark_theme())
        else:
            self.setStyleSheet(load_light_theme())
    
    # def on_search_text_changed(self, text):
    #     if len(text) >= 3:  # Only search if at least 3 characters
    #         import requests
    #         try:
    #             # Use Nominatim API for suggestions
    #             headers = {'User-Agent': 'KonectTrafficStudio/1.0'}
    #             response = requests.get(
    #                 f"https://nominatim.openstreetmap.org/search?format=json&q={text}&limit=5",
    #                 headers=headers
    #             )
    #             data = response.json()
                
    #             # Clear and update suggestions
    #             self.suggestions_list.clear()
    #             for place in data:
    #                 item = QListWidgetItem(place['display_name'])
    #                 item.setData(Qt.ItemDataRole.UserRole, {
    #                     'lat': float(place['lat']),
    #                     'lon': float(place['lon'])
    #                 })
    #                 self.suggestions_list.addItem(item)
                
    #             # Show suggestions if we have any
    #             if self.suggestions_list.count() > 0:
    #                 self.show_suggestions()
    #             else:
    #                 self.suggestions_list.hide()
    #         except Exception as e:
    #             print(f"Error fetching suggestions: {e}")
    #             self.suggestions_list.hide()
    #     else:
    #         self.suggestions_list.hide()

    def show_suggestions(self):
        # Position suggestions list below search input
        pos = self.search_input.mapToGlobal(self.search_input.rect().bottomLeft())
        width = self.search_input.width()
        height = min(200, self.suggestions_list.sizeHintForRow(0) * 
                    self.suggestions_list.count() + 10)
        self.suggestions_list.setGeometry(pos.x(), pos.y(), width, height)
        self.suggestions_list.show()
        self.suggestions_list.raise_()

    def on_suggestion_clicked(self, item):
        # Update search input text
        self.search_input.setText(item.text())
        self.suggestions_list.hide()
        
        # Get coordinates and search
        data = item.data(Qt.ItemDataRole.UserRole)
        if self.canvas and data:
            self.canvas.show_map_overlay()
            self.canvas.search_location(data['lat'], data['lon'])

    def on_suggestion_clicked(self, item):
        # Get coordinates before hiding suggestions
        try:
            data = item.data(Qt.ItemDataRole.UserRole)
            display_text = item.text()
            
            # Hide suggestions
            self.suggestions_list.hide()
            
            # Update search input text
            self.search_input.setText(display_text)
            
            # Search with coordinates
            if self.canvas and data:
                self.canvas.show_map_overlay()
                self.canvas.search_location(data['lat'], data['lon'])
        except Exception as e:
            print(f"Error handling suggestion click: {e}")

    def on_search_text_changed(self, text):
        if len(text) >= 3:  # Only search if at least 3 characters
            import requests
            try:
                # Use Nominatim API for suggestions
                headers = {'User-Agent': 'KonectTrafficStudio/1.0'}
                response = requests.get(
                    f"https://nominatim.openstreetmap.org/search?format=json&q={text}&limit=5",
                    headers=headers
                )
                data = response.json()
                
                # Clear and update suggestions
                self.suggestions_list.clear()
                
                if data:  # Only proceed if we have data
                    for place in data:
                        item = QListWidgetItem(place['display_name'])
                        # Store coordinates in item data
                        coordinates = {
                            'lat': float(place['lat']),
                            'lon': float(place['lon'])
                        }
                        item.setData(Qt.ItemDataRole.UserRole, coordinates)
                        self.suggestions_list.addItem(item)
                    
                    # Show suggestions if we have any
                    if self.suggestions_list.count() > 0:
                        self.show_suggestions()
                    else:
                        self.suggestions_list.hide()
                else:
                    self.suggestions_list.hide()
                    
            except Exception as e:
                print(f"Error fetching suggestions: {e}")
                self.suggestions_list.hide()
        else:
            self.suggestions_list.hide()

#test location new window
    # def setup_search_section(self):
        # Create search container
        search_widget = QWidget()
        search_layout = QVBoxLayout(search_widget)
        search_layout.setContentsMargins(5, 5, 5, 5)
        
        # Search label
        search_label = QLabel("Location Search")
        search_label.setStyleSheet("color: #888888; font-size: 12px;")
        search_layout.addWidget(search_label)
        
        # Search input and buttons container
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search location...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #555555;
                border-radius: 3px;
                background: #2a2a2a;
                color: white;
            }
            QLineEdit:focus {
                border: 1px solid #00ffff;
            }
        """)
        input_layout.addWidget(self.search_input)
        
        # Search button
        search_button = QPushButton()
        search_button.setIcon(QIcon("assets/icons/search.png"))
        search_button.setFixedSize(30, 30)
        search_button.clicked.connect(self.search_location)
        search_button.setStyleSheet("""
            QPushButton {
                background: #2a2a2a;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 3px;
            }
            QPushButton:hover {
                background: #3a3a3a;
                border: 1px solid #666666;
            }
        """)
        input_layout.addWidget(search_button)

        # Map button
        map_button = QPushButton()
        map_button.setIcon(QIcon("assets/icons/map.png"))
        map_button.setFixedSize(30, 30)
        map_button.clicked.connect(self.show_map_window)
        map_button.setStyleSheet("""
            QPushButton {
                background: #2a2a2a;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 3px;
            }
            QPushButton:hover {
                background: #3a3a3a;
                border: 1px solid #666666;
            }
        """)
        input_layout.addWidget(map_button)
        
        search_layout.addWidget(input_container)
        self.main_layout.addWidget(search_widget)

        # Create suggestions list
        self.suggestions_list = QListWidget(self)
        self.suggestions_list.setWindowFlags(Qt.WindowType.Popup)
        self.suggestions_list.setStyleSheet("""
            QListWidget {
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #555555;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #3a3a3a;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
        """)
        self.suggestions_list.itemClicked.connect(self.on_suggestion_clicked)
        self.suggestions_list.hide()

        # Initialize map window
        from components.map_window import MapWindow
        self.map_window = MapWindow()

    # def show_map_window(self):
    #     self.map_window.show()
    #     self.map_window.raise_()

    # def on_suggestion_clicked(self, item):
    #     try:
    #         data = item.data(Qt.ItemDataRole.UserRole)
    #         display_text = item.text()
            
    #         # Hide suggestions
    #         self.suggestions_list.hide()
            
    #         # Update search input text
    #         self.search_input.setText(display_text)
            
    #         # Update map window if visible
    #         if self.map_window.isVisible():
    #             self.map_window.search_location(data['lat'], data['lon'])
    #     except Exception as e:
    #         print(f"Error handling suggestion click: {e}")
    
    #test new window map
    
    # def on_suggestion_clicked(self, item):
    #     try:
    #         data = item.data(Qt.ItemDataRole.UserRole)
    #         display_text = item.text()
            
    #         # Hide suggestions
    #         self.suggestions_list.hide()
            
    #         # Update search input text
    #         self.search_input.setText(display_text)
            
    #         # Update map window
    #         self.map_window.search_location(data['lat'], data['lon'])
            
    #         # Store the last location for future use
    #         self.last_location = data
            
    #     except Exception as e:
    #         print(f"Error handling suggestion click: {e}")

    def show_map_window(self):
        # If we have a last searched location, use it
        if hasattr(self, 'last_location'):
            self.map_window.search_location(
                self.last_location['lat'], 
                self.last_location['lon']
            )
        self.map_window.show()
        self.map_window.raise_()

    # def show_map_window(self):
    #     if self.canvas:
    #         self.canvas.toggle_map_view()

    def on_suggestion_clicked(self, item):
        try:
            data = item.data(Qt.ItemDataRole.UserRole)
            display_text = item.text()
            
            # Hide suggestions
            self.suggestions_list.hide()
            
            # Update search input text
            self.search_input.setText(display_text)
            
            # Update map and show it
            if self.canvas:
                self.canvas.search_location(data['lat'], data['lon'])
            
            # Store the last location
            self.last_location = data
            
        except Exception as e:
            print(f"Error handling suggestion click: {e}")