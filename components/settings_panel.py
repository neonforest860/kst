# components/settings_panel.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                           QFormLayout, QLineEdit, QComboBox, QFileDialog)
from PyQt6.QtCore import Qt

class SettingsPanel(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Theme Settings
        theme_label = QLabel("Theme Settings")
        theme_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark Mode", "Light Mode"])
        self.theme_combo.currentTextChanged.connect(self.theme_changed)
        self.layout.addWidget(self.theme_combo)

        # Icon Settings
        icon_label = QLabel("Icon Management")
        icon_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(icon_label)

        add_icon_btn = QPushButton("Add New Icon")
        add_icon_btn.clicked.connect(self.add_icon)
        self.layout.addWidget(add_icon_btn)

        # Algorithm Settings
        algo_label = QLabel("Algorithm Management")
        algo_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(algo_label)

        add_algo_btn = QPushButton("Add New Algorithm")
        add_algo_btn.clicked.connect(self.add_algorithm)
        self.layout.addWidget(add_algo_btn)

        # Add stretch to push everything to the top
        self.layout.addStretch()

    def theme_changed(self, text):
        if text == "Light Mode" and self.main_window.dark_mode:
            self.main_window.toggle_theme()
        elif text == "Dark Mode" and not self.main_window.dark_mode:
            self.main_window.toggle_theme()

    def add_icon(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Icon", "", 
                                                 "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            # Handle icon addition
            pass

    def add_algorithm(self):
        # Add dialog for new algorithm
        pass