from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QFormLayout, QGroupBox,
                           QMessageBox, QWidget)
from PyQt6.QtCore import Qt
import requests

class ControllerDialog(QDialog):
    def __init__(self, node_data=None, parent=None):
        super().__init__(parent)
        self.node_data = node_data or {}
        self.token = None
        self.setWindowTitle("Controller Configuration")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
        self.setup_ui()
        self.apply_theme()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Connection group
        conn_group = QGroupBox("Connection Settings")
        conn_layout = QFormLayout()
        self.ip_edit = QLineEdit(self.node_data.get("ip", ""))
        self.port_edit = QLineEdit(self.node_data.get("port", ""))
        self.user_edit = QLineEdit(self.node_data.get("username", ""))
        self.pass_edit = QLineEdit(self.node_data.get("password", ""))
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        
        conn_layout.addRow("IP Address:", self.ip_edit)
        conn_layout.addRow("Port:", self.port_edit)
        conn_layout.addRow("Username:", self.user_edit)
        conn_layout.addRow("Password:", self.pass_edit)
        conn_group.setLayout(conn_layout)
        layout.addWidget(conn_group)
        
        # Phase Camera Mapping group
        self.mapping_group = QGroupBox("Phase Camera Mapping")
        self.mapping_layout = QFormLayout()
        
        # Initial mapping entry
        self.camera_mappings = []
        self.add_camera_mapping()
        
        # Add button
        add_btn = QPushButton("+")
        add_btn.clicked.connect(self.add_camera_mapping)
        add_btn.setFixedWidth(30)
        self.mapping_layout.addRow("", add_btn)
        
        self.mapping_group.setLayout(self.mapping_layout)
        layout.addWidget(self.mapping_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.get_config_btn = QPushButton("Get Config")
        self.set_config_btn = QPushButton("Set Config")
        self.cancel_btn = QPushButton("Cancel")
        
        self.get_config_btn.clicked.connect(self.get_config)
        self.set_config_btn.clicked.connect(self.set_config)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.get_config_btn)
        button_layout.addWidget(self.set_config_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

    def apply_theme(self):
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

    def add_camera_mapping(self):
        mapping_container = QWidget()
        mapping_layout = QHBoxLayout(mapping_container)
        mapping_layout.setContentsMargins(0, 0, 0, 0)
        
        phase_edit = QLineEdit()
        cameras_edit = QLineEdit()
        remove_btn = QPushButton("-")
        remove_btn.setFixedWidth(30)
        remove_btn.clicked.connect(lambda: self.remove_camera_mapping(mapping_container))
        
        mapping_layout.addWidget(phase_edit)
        mapping_layout.addWidget(cameras_edit)
        mapping_layout.addWidget(remove_btn)
        
        self.camera_mappings.append((mapping_container, phase_edit, cameras_edit))
        self.mapping_layout.insertRow(len(self.camera_mappings) - 1, "Phase:", mapping_container)

    def remove_camera_mapping(self, container):
        for i, (widget, _, _) in enumerate(self.camera_mappings):
            if widget == container:
                self.camera_mappings.pop(i)
                self.mapping_layout.removeRow(i)
                break

    def get_token(self):
        try:
            url = f"http://{self.ip_edit.text()}:{self.port_edit.text()}/auth/login"
            headers = {'Content-Type': 'application/json'}
            data = {
                "username": self.user_edit.text(),
                "password": self.pass_edit.text()
            }
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["access_token"]
        except Exception as e:
            raise Exception(f"Failed to get token: {str(e)}")

    def get_config(self):
        try:
            # Get token first
            self.token = self.get_token()
            
            # Get configuration
            url = f"http://{self.ip_edit.text()}:{self.port_edit.text()}/get-config"
            headers = {"Authorization": f"Bearer {self.token}"}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            config = response.json()
            
            # Clear existing mappings
            while self.camera_mappings:
                self.remove_camera_mapping(self.camera_mappings[0][0])
            
            # Add mappings from config
            phase_camera_mapping = config.get("phase_camera_mapping", {})
            for phase, cameras in phase_camera_mapping.items():
                self.add_camera_mapping()
                mapping = self.camera_mappings[-1]
                mapping[1].setText(str(phase))
                mapping[2].setText(",".join(map(str, cameras)))
            
            QMessageBox.information(self, "Success", "Configuration retrieved successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def set_config(self):
        try:
            # Get token first
            self.token = self.get_token()
            
            # Prepare configuration data
            config = {
                "phase_camera_mapping": {}
            }
            
            # Add phase camera mapping from UI
            for _, phase_edit, cameras_edit in self.camera_mappings:
                phase = phase_edit.text().strip()
                cameras_text = cameras_edit.text().strip()
                if phase and cameras_text:
                    cameras = [int(cam.strip()) for cam in cameras_text.split(",") if cam.strip()]
                    config["phase_camera_mapping"][phase] = cameras
            
            # Send configuration
            url = f"http://{self.ip_edit.text()}:{self.port_edit.text()}/set-config"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, headers=headers, json=config)
            response.raise_for_status()
            
            QMessageBox.information(self, "Success", "Configuration set successfully")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def get_data(self):
        """Return the current configuration as a dictionary"""
        data = {
            "ip": self.ip_edit.text(),
            "port": self.port_edit.text(),
            "username": self.user_edit.text(),
            "password": self.pass_edit.text(),
            "phase_camera_mapping": {}
        }
        
        # Add phase camera mapping
        for _, phase_edit, cameras_edit in self.camera_mappings:
            phase = phase_edit.text().strip()
            cameras_text = cameras_edit.text().strip()
            if phase and cameras_text:
                cameras = [int(cam.strip()) for cam in cameras_text.split(",") if cam.strip()]
                data["phase_camera_mapping"][phase] = cameras
        
        return data