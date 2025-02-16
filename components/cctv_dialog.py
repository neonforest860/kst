from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QFormLayout, QGroupBox)
from PyQt6.QtCore import Qt

class CCTVDialog(QDialog):
    def __init__(self, node_data=None, parent=None):
        super().__init__(parent)
        self.node_data = node_data or {}
        self.setWindowTitle("CCTV Configuration")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
        self.setup_ui()
        self.apply_theme()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Location group
        location_group = QGroupBox("Location")
        location_layout = QFormLayout()
        self.lat_edit = QLineEdit(self.node_data.get("latitude", ""))
        self.lon_edit = QLineEdit(self.node_data.get("longitude", ""))
        self.name_edit = QLineEdit(self.node_data.get("name", ""))
        location_layout.addRow("Latitude:", self.lat_edit)
        location_layout.addRow("Longitude:", self.lon_edit)
        location_layout.addRow("Name:", self.name_edit)
        location_group.setLayout(location_layout)
        
        # Network group
        network_group = QGroupBox("Network")
        network_layout = QFormLayout()
        self.ip_edit = QLineEdit(self.node_data.get("ip", ""))
        self.port_edit = QLineEdit(self.node_data.get("port", ""))
        self.user_edit = QLineEdit(self.node_data.get("username", ""))
        self.pass_edit = QLineEdit(self.node_data.get("password", ""))
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        network_layout.addRow("IP Address:", self.ip_edit)
        network_layout.addRow("OnVif Port:", self.port_edit)
        network_layout.addRow("Username:", self.user_edit)
        network_layout.addRow("Password:", self.pass_edit)
        network_group.setLayout(network_layout)
        
        # IDs group
        ids_group = QGroupBox("Identification")
        ids_layout = QFormLayout()
        self.camera_id_edit = QLineEdit(self.node_data.get("camera_id", ""))
        self.street_id_edit = QLineEdit(self.node_data.get("street_id", ""))
        ids_layout.addRow("Camera ID:", self.camera_id_edit)
        ids_layout.addRow("Street ID:", self.street_id_edit)
        ids_group.setLayout(ids_layout)
        
        # Add groups to main layout
        layout.addWidget(location_group)
        layout.addWidget(network_group)
        layout.addWidget(ids_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save & Config")
        self.test_btn = QPushButton("Test")
        self.cancel_btn = QPushButton("Cancel")
        self.save_btn.clicked.connect(self.accept)
        self.test_btn.clicked.connect(self.test_connection)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.test_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

    def apply_theme(self):
        # Get theme from parent window
        is_dark = self.parent().dark_mode if hasattr(self.parent(), 'dark_mode') else True
        
        if is_dark:
            self.setStyleSheet("""
                QDialog {
                    background-color: #1a1a1a;
                    color: white;
                }
                QGroupBox {
                    background-color: #2a2a2a;
                    color: white;
                    border: 1px solid #3a3a3a;
                    margin-top: 0.5em;
                }
                QGroupBox::title {
                    color: white;
                }
                QLineEdit {
                    background-color: #2a2a2a;
                    color: white;
                    border: 1px solid #3a3a3a;
                    padding: 5px;
                }
                QLabel {
                    color: white;
                }
                QPushButton {
                    background-color: #2a2a2a;
                    color: white;
                    border: 1px solid #3a3a3a;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background-color: #f0f0f0;
                    color: black;
                }
                QGroupBox {
                    background-color: white;
                    color: black;
                    border: 1px solid #d0d0d0;
                    margin-top: 0.5em;
                }
                QGroupBox::title {
                    color: black;
                }
                QLineEdit {
                    background-color: white;
                    color: black;
                    border: 1px solid #d0d0d0;
                    padding: 5px;
                }
                QLabel {
                    color: black;
                }
                QPushButton {
                    background-color: white;
                    color: black;
                    border: 1px solid #d0d0d0;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
    
    def test_connection(self):
        # Implement connection testing logic here
        pass
        
    def get_data(self):
        return {
            "latitude": self.lat_edit.text(),
            "longitude": self.lon_edit.text(),
            "name": self.name_edit.text(),
            "ip": self.ip_edit.text(),
            "port": self.port_edit.text(),
            "username": self.user_edit.text(),
            "password": self.pass_edit.text(),
            "camera_id": self.camera_id_edit.text(),
            "street_id": self.street_id_edit.text()
        }