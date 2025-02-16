from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QFormLayout, QGroupBox,
                           QMessageBox, QSpinBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt
import requests

class BasiQDialog(QDialog):
    def __init__(self, node_data=None, parent=None):
        super().__init__(parent)
        self.node_data = node_data or {}
        self.token = None
        self.setWindowTitle("BasiQ Configuration")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
        self.setup_ui()
        self.apply_theme()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Algorithm Settings group
        algo_group = QGroupBox("Algorithm Settings")
        algo_layout = QFormLayout()
        
        # Initialize fields with empty values or existing values
        self.algo_name = QLineEdit(self.node_data.get("algorithm_name", ""))
        self.comp_threshold = QDoubleSpinBox()
        self.comp_threshold.setRange(0, 1)
        self.comp_threshold.setSingleStep(0.1)
        self.comp_threshold.setValue(float(self.node_data.get("computation_threshold", 0.0)))
        
        self.f_adj = QDoubleSpinBox()
        self.f_adj.setRange(0, 1)
        self.f_adj.setSingleStep(0.1)
        self.f_adj.setValue(float(self.node_data.get("f_adj", 0.0)))
        
        self.set_setting_threshold = QDoubleSpinBox()
        self.set_setting_threshold.setRange(0, 1)
        self.set_setting_threshold.setSingleStep(0.05)
        self.set_setting_threshold.setValue(float(self.node_data.get("set_setting_threshold", 0.0)))
        
        self.saturation_flow = QSpinBox()
        self.saturation_flow.setRange(0, 5000)
        self.saturation_flow.setValue(int(self.node_data.get("saturation_flow_rate", 0)))
        
        self.startup_loss = QSpinBox()
        self.startup_loss.setRange(0, 10)
        self.startup_loss.setValue(int(self.node_data.get("startup_loss_time", 0)))
        
        algo_layout.addRow("Algorithm Name:", self.algo_name)
        algo_layout.addRow("Computation Threshold:", self.comp_threshold)
        algo_layout.addRow("F Adjustment:", self.f_adj)
        algo_layout.addRow("Setting Threshold:", self.set_setting_threshold)
        algo_layout.addRow("Saturation Flow Rate:", self.saturation_flow)
        algo_layout.addRow("Startup Loss Time:", self.startup_loss)
        
        algo_group.setLayout(algo_layout)
        layout.addWidget(algo_group)
        
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

    def get_config(self):
        try:
            # Find connected controller
            canvas = self.parent()
            controller_node = None
            basiq_pos = None
            
            for node in canvas.nodes:
                if node["type"] == "BasiQ":
                    basiq_pos = node["pos"]
                    break
            
            if basiq_pos:
                for conn in canvas.connections:
                    start, end = conn
                    other_pos = end if start == basiq_pos else start
                    for node in canvas.nodes:
                        if node["pos"] == other_pos and node["type"] == "Controller":
                            controller_node = node
                            break
            
            if not controller_node or "characteristics" not in controller_node:
                raise Exception("No connected controller found or controller not configured")
            
            # Get token from controller
            url = f"http://{controller_node['characteristics']['ip']}:{controller_node['characteristics']['port']}/auth/login"
            headers = {'Content-Type': 'application/json'}
            data = {
                "username": controller_node['characteristics']['username'],
                "password": controller_node['characteristics']['password']
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            token = response.json()["access_token"]
            
            # Get configuration
            url = f"http://{controller_node['characteristics']['ip']}:{controller_node['characteristics']['port']}/getconfig"
            headers = {"Authorization": f"Bearer {token}"}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            config = response.json()
            
            # Update UI with received configuration
            self.algo_name.setText(config.get("algorithm_name", ""))
            self.comp_threshold.setValue(float(config.get("computation_threshold", 0.0)))
            self.f_adj.setValue(float(config.get("f_adj", 0.0)))
            self.set_setting_threshold.setValue(float(config.get("set_setting_threshold", 0.0)))
            self.saturation_flow.setValue(int(config.get("saturation_flow_rate", 0)))
            self.startup_loss.setValue(int(config.get("startup_loss_time", 0)))
            
            QMessageBox.information(self, "Success", "Configuration retrieved successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def set_config(self):
        try:
            # Find connected controller
            canvas = self.parent()
            controller_node = None
            basiq_pos = None
            
            for node in canvas.nodes:
                if node["type"] == "BasiQ":
                    basiq_pos = node["pos"]
                    break
            
            if basiq_pos:
                for conn in canvas.connections:
                    start, end = conn
                    other_pos = end if start == basiq_pos else start
                    for node in canvas.nodes:
                        if node["pos"] == other_pos and node["type"] == "Controller":
                            controller_node = node
                            break
            
            if not controller_node or "characteristics" not in controller_node:
                raise Exception("No connected controller found or controller not configured")
            
            # Get token from controller
            url = f"http://{controller_node['characteristics']['ip']}:{controller_node['characteristics']['port']}/auth/login"
            headers = {'Content-Type': 'application/json'}
            data = {
                "username": controller_node['characteristics']['username'],
                "password": controller_node['characteristics']['password']
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            token = response.json()["access_token"]
            
            # Prepare configuration data
            config = {
                "algorithm_name": self.algo_name.text(),
                "computation_threshold": self.comp_threshold.value(),
                "f_adj": self.f_adj.value(),
                "set_setting_threshold": self.set_setting_threshold.value(),
                "saturation_flow_rate": self.saturation_flow.value(),
                "startup_loss_time": self.startup_loss.value()
            }
            
            # Send configuration
            url = f"http://{controller_node['characteristics']['ip']}:{controller_node['characteristics']['port']}/setconfig"
            headers = {
                "Authorization": f"Bearer {token}",
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
        return {
            "algorithm_name": self.algo_name.text(),
            "computation_threshold": self.comp_threshold.value(),
            "f_adj": self.f_adj.value(),
            "set_setting_threshold": self.set_setting_threshold.value(),
            "saturation_flow_rate": self.saturation_flow.value(),
            "startup_loss_time": self.startup_loss.value()
        }
        
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
                QLineEdit, QSpinBox, QDoubleSpinBox {
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
                QLineEdit, QSpinBox, QDoubleSpinBox {
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