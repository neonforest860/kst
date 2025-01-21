# components/sidebar.py
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, 
                           QPushButton, QLabel, QComboBox)
from PyQt6.QtCore import Qt, QSize, QMimeData, QPoint, QPropertyAnimation
from PyQt6.QtGui import QIcon, QDrag, QPixmap

class CollapsibleSection(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Title button
        self.toggle_button = QPushButton(title)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                text-align: center;
                padding: 5px;
                font-weight: bold;
                background-color: #1a1a1a;
                border: none;
                color: #888888;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                color: white;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_content)
        self.layout.addWidget(self.toggle_button)
        
        # Content widget
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setSpacing(2)
        self.content_layout.setContentsMargins(10, 0, 0, 0)
        self.layout.addWidget(self.content)
        
        self.is_expanded = True

    def toggle_content(self):
        self.is_expanded = not self.is_expanded
        self.content.setVisible(self.is_expanded)

    def addWidget(self, widget):
        self.content_layout.addWidget(widget)
        
    def setText(self, text):
        self.toggle_button.setText(text)

class NavigationButton(QPushButton):
    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(parent)
        self.setText(text)
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))
        
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 10px;
                background-color: #1a1a1a;
                border: none;
                color: white;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)

class DraggableButton(QPushButton):
    def __init__(self, text, icon_path, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(32, 32))
        self.icon_path = icon_path
        self.full_text = text
        
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 5px;
                background-color: #2a2a2a;
                border: none;
                color: white;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)

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

class Sidebar(QDockWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Navigation")
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        
        # Main widget and layout
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

        # Entity Section with new camera types
        self.entity_section = CollapsibleSection("Entity")
        self.layout.addWidget(self.entity_section)
        
        camera_types = ["CCTV", "Redlight", "Firn", "TPE", "Controller"]
        self.camera_buttons = []
        for cam_type in camera_types:
            btn = DraggableButton(cam_type, f"assets/icons/{cam_type.lower()}.png")
            self.camera_buttons.append(btn)
            self.entity_section.addWidget(btn)
        
        # TPE Section
        self.tpe_section = CollapsibleSection("TPE")
        self.layout.addWidget(self.tpe_section)
        self.tpe_combo = QComboBox()
        self.tpe_combo.addItems([f"TPE {i}" for i in range(1, 6)])
        self.tpe_section.addWidget(self.tpe_combo)
        
        # Algorithm Section
        self.algo_section = CollapsibleSection("Algorithm")
        self.layout.addWidget(self.algo_section)
        self.algo_button = DraggableButton("BasiQ", "assets/icons/algorithm.png")
        self.algo_section.addWidget(self.algo_button)
        
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
            self.entity_section.setText("E")
            self.tpe_section.setText("T")
            self.algo_section.setText("A")
            for btn in self.camera_buttons:
                btn.setText("")
            self.tpe_combo.hide()
            self.algo_button.setText("")
        else:
            self.home_btn.setText("Konect Traffic Studio")
            self.design_btn.setText("Design")
            self.settings_btn.setText("Settings")
            self.entity_section.setText("Entity")
            self.tpe_section.setText("TPE")
            self.algo_section.setText("Algorithm")
            for btn, text in zip(self.camera_buttons, ["CCTV", "Redlight", "Firn", "TPE", "Controller"]):
                btn.setText(text)
            self.tpe_combo.show()
            self.algo_button.setText("BasiQ")
        
        self.expanded = not self.expanded