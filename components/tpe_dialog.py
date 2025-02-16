from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QFormLayout, QGroupBox,
                           QMessageBox, QProgressDialog)
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtCore import Qt
import requests
import json
import requests
import math

class TPEDialog(QDialog):
    def __init__(self, node_data=None, canvas=None, parent=None):
        super().__init__(parent)
        self.node_data = node_data or {}  # We initialize as node_data
        self.canvas = canvas
        self.token = None
        self.setWindowTitle("TPE Configuration")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Connection group
        conn_group = QGroupBox("Connection Settings")
        conn_layout = QFormLayout()
        
        # Changed from self.characteristics to self.node_data
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

    def get_token(self):
        try:
            url = f"http://{self.ip_edit.text()}:{self.port_edit.text()}/login"
            data = {
                "username": self.user_edit.text(),
                "password": self.pass_edit.text()
            }
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            
            if result.get("status"):
                return result["data"]["token"]
            else:
                raise Exception(result.get("error", "Unknown error"))
                
        except requests.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error getting token: {str(e)}")

    def get_config(self):
        try:
            # Get token first
            self.token = self.get_token()
            
            # Get cameras
            url = f"http://{self.ip_edit.text()}:{self.port_edit.text()}/cameras"
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            if result.get("status"):
                # Clear existing nodes except TPE
                self.canvas.nodes = [node for node in self.canvas.nodes if node["type"] == "TPE"]
                
                # Add cameras
                tpe_pos = next(node["pos"] for node in self.canvas.nodes if node["type"] == "TPE")
                for idx, camera in enumerate(result["data"]["cameras"]):
                    camera_node = {
                        "type": "CCTV",
                        "pos": self.calculate_camera_position(tpe_pos, idx, len(result["data"]["cameras"])),
                        "icon": self.canvas.get_icon("CCTV"),
                        "name": camera["name"],
                        "characteristics": {
                            "latitude": str(camera["latitude"]),
                            "longitude": str(camera["longitude"]),
                            "camera_id": str(camera["cameraId"]),
                            "street_id": str(camera["streetId"]) if camera["streetId"] else "",
                            "name": camera["name"]
                        }
                    }
                    self.canvas.nodes.append(camera_node)
                    
                    # Add connection to TPE
                    self.canvas.connections.append((tpe_pos, camera_node["pos"]))
                
                self.canvas.update()
                self.accept()
                
            else:
                raise Exception(result.get("error", "Unknown error"))
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def set_config(self):
        try:
            # Get token first
            self.token = self.get_token()
            
            # Prepare camera data
            cameras = []
            tpe_node = next(node for node in self.canvas.nodes if node["type"] == "TPE")
            
            for node in self.canvas.nodes:
                if node["type"] == "CCTV":
                    # Check if connected to TPE
                    is_connected = any(
                        (conn[0] == tpe_node["pos"] and conn[1] == node["pos"]) or
                        (conn[1] == tpe_node["pos"] and conn[0] == node["pos"])
                        for conn in self.canvas.connections
                    )
                    
                    if is_connected:
                        char = node.get("characteristics", {})
                        camera = {
                            "name": char.get("name", ""),
                            "cameraId": int(char.get("camera_id", 0)),
                            "streetId": int(char.get("street_id", 0)) if char.get("street_id") else None,
                            "latitude": float(char.get("latitude", 0)),
                            "longitude": float(char.get("longitude", 0))
                        }
                        cameras.append(camera)
            
            # Send configuration
            url = f"http://{self.ip_edit.text()}:{self.port_edit.text()}/cameras"
            headers = {"Authorization": f"Bearer {self.token}"}
            data = {"cameras": cameras}
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            if result.get("status"):
                QMessageBox.information(self, "Success", "Configuration sent successfully")
                self.accept()
            else:
                raise Exception(result.get("error", "Unknown error"))
                
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def calculate_camera_position(self, tpe_pos, index, total):
        # Calculate position in a circular pattern around TPE
        import math
        radius = 100  # pixels
        angle = (2 * math.pi * index) / total
        x = tpe_pos.x() + radius * math.cos(angle)
        y = tpe_pos.y() + radius * math.sin(angle)
        return QPoint(int(x), int(y))

    def get_data(self):
        return {
            "ip": self.ip_edit.text(),
            "port": self.port_edit.text(),
            "username": self.user_edit.text(),
            "password": self.pass_edit.text()
        }
class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Loading")
        self.setFixedSize(200, 100)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        
        layout = QVBoxLayout(self)
        
        # Create dots container
        self.dots_label = QLabel("Loading")
        self.dots_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.dots_label)
        
        # Initialize dots animation
        self.dot_count = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dots)
        self.timer.start(500)  # Update every 500ms
        
        # Apply theme
        self.apply_theme()

    def update_dots(self):
        self.dot_count = (self.dot_count + 1) % 4
        self.dots_label.setText("Loading" + "." * self.dot_count)

    def apply_theme(self):
        is_dark = self.parent().dark_mode if hasattr(self.parent(), 'dark_mode') else True
        
        if is_dark:
            self.setStyleSheet("""
                QDialog {
                    background-color: #2a2a2a;
                    color: white;
                    border: 1px solid #3a3a3a;
                    border-radius: 10px;
                }
                QLabel {
                    color: white;
                    font-size: 14px;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background-color: white;
                    color: black;
                    border: 1px solid #d0d0d0;
                    border-radius: 10px;
                }
                QLabel {
                    color: black;
                    font-size: 14px;
                }
            """)
            
    # ... (keep existing init and setup_ui methods)

    def get_config(self):
        # Show loading dialog
        loading = LoadingDialog(self)
        loading.show()
        
        try:
            # Get token first
            self.token = self.get_token()
            
            # Get cameras
            url = f"http://{self.ip_edit.text()}:{self.port_edit.text()}/cameras"
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            if result.get("status"):
                # Clear existing nodes except TPE
                self.canvas.nodes = [node for node in self.canvas.nodes if node["type"] == "TPE"]
                
                # Add cameras
                tpe_pos = next(node["pos"] for node in self.canvas.nodes if node["type"] == "TPE")
                for idx, camera in enumerate(result["data"]["cameras"]):
                    camera_node = {
                        "type": "CCTV",
                        "pos": self.calculate_camera_position(tpe_pos, idx, len(result["data"]["cameras"])),
                        "icon": self.canvas.get_icon("CCTV"),
                        "name": camera["name"],
                        "characteristics": {
                            "latitude": str(camera["latitude"]),
                            "longitude": str(camera["longitude"]),
                            "camera_id": str(camera["cameraId"]),
                            "street_id": str(camera["streetId"]) if camera["streetId"] else "",
                            "name": camera["name"]
                        }
                    }
                    self.canvas.nodes.append(camera_node)
                    
                    # Add connection to TPE
                    self.canvas.connections.append((tpe_pos, camera_node["pos"]))
                
                self.canvas.update()
                loading.close()
                self.accept()
                
            else:
                loading.close()
                raise Exception(result.get("error", "Unknown error"))
                
        except Exception as e:
            loading.close()
            QMessageBox.critical(self, "Error", str(e))

    def set_config(self):
        # Show loading dialog
        loading = LoadingDialog(self)
        loading.show()
        
        try:
            # ... (rest of set_config implementation)
            # Remember to close loading dialog in success and error cases
            loading.close()
        except Exception as e:
            loading.close()
            QMessageBox.critical(self, "Error", str(e))