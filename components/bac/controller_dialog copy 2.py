from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QFormLayout, QGroupBox,
                           QMessageBox, QWidget, QSpinBox)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon
import requests


# class ControllerDialog(QDialog):
#     def __init__(self, node_data=None, parent=None):
#         super().__init__(parent)
#         self.node_data = node_data or {}
#         self.token = None
#         self.camera_mappings = []
#         self.phase_bounds = []
#         self.setWindowTitle("Controller Configuration")
#         self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
#         self.setup_ui()
#         self.apply_theme()

class ControllerDialog(QDialog):
    def __init__(self, node_data=None, canvas=None, parent=None):
        super().__init__(parent)
        # Ensure node_data is a dictionary
        self.node_data = node_data or {}
        self.canvas = canvas
        self.token = None
        self.phase_bounds = []
        self.camera_mappings = []
        
        # Initialize last_retrieved_config with data from node_data if available
        self.last_retrieved_config = self.node_data.get('last_retrieved_config', {})
        
        self.setWindowTitle("Controller Configuration")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
        self.setup_ui()
        self.load_node_data()
        self.apply_theme()

            

    def load_node_data(self):
        # Load data from node_data into the dialog's fields
        phase_bounds = self.node_data.get("phase_bounds", {})
        for phase, bounds in phase_bounds.items():
            self.add_phase_bound(int(phase), bounds["g_min"], bounds["g_max"])
        
        phase_camera_mapping = self.node_data.get("phase_camera_mapping", {})
        for phase, cameras in phase_camera_mapping.items():
            self.add_camera_mapping(int(phase), cameras)
        
    # def setup_ui(self):
    #     layout = QVBoxLayout(self)
        
    #     # Connection group
    #     conn_group = QGroupBox("Connection Settings")
    #     conn_layout = QFormLayout()
    #     self.ip_edit = QLineEdit(self.node_data.get("ip", ""))
    #     self.port_edit = QLineEdit(self.node_data.get("port", ""))
    #     self.user_edit = QLineEdit(self.node_data.get("username", ""))
    #     self.pass_edit = QLineEdit(self.node_data.get("password", ""))
    #     self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        
    #     conn_layout.addRow("IP Address:", self.ip_edit)
    #     conn_layout.addRow("Port:", self.port_edit)
    #     conn_layout.addRow("Username:", self.user_edit)
    #     conn_layout.addRow("Password:", self.pass_edit)
    #     conn_group.setLayout(conn_layout)
    #     layout.addWidget(conn_group)
        
    #     # Phase Bounds group
    #     self.bounds_group = QGroupBox("Phase Bounds")
    #     self.bounds_layout = QFormLayout()
    #     self.bounds_group.setLayout(self.bounds_layout)
    #     layout.addWidget(self.bounds_group)
        
    #     # Phase Camera Mapping group
    #     self.mapping_group = QGroupBox("Phase Camera Mapping")
    #     self.mapping_layout = QFormLayout()
    #     self.mapping_group.setLayout(self.mapping_layout)
    #     layout.addWidget(self.mapping_group)
        
    #     # Initial entries
    #     self.add_phase_bound()
        
    #     # Add buttons for bounds and mapping
    #     add_bounds_btn = QPushButton("+")
    #     add_bounds_btn.clicked.connect(self.add_phase_bound)
    #     add_bounds_btn.setFixedWidth(30)
    #     self.bounds_layout.addRow("", add_bounds_btn)
        
    #     add_mapping_btn = QPushButton("+")
    #     add_mapping_btn.clicked.connect(self.add_camera_mapping)
    #     add_mapping_btn.setFixedWidth(30)
    #     self.mapping_layout.addRow("", add_mapping_btn)
        
    #     # Buttons
    #     button_layout = QHBoxLayout()
    #     self.get_config_btn = QPushButton("Get Config")
    #     self.set_config_btn = QPushButton("Set Config")
    #     self.cancel_btn = QPushButton("Cancel")
        
    #     self.get_config_btn.clicked.connect(self.get_config)
    #     self.set_config_btn.clicked.connect(self.set_config)
    #     self.cancel_btn.clicked.connect(self.reject)
        
    #     button_layout.addWidget(self.get_config_btn)
    #     button_layout.addWidget(self.set_config_btn)
    #     button_layout.addWidget(self.cancel_btn)
    #     layout.addLayout(button_layout)
        
        # # Buttons
        # button_layout = QHBoxLayout()
        # self.get_config_btn = QPushButton("Get Config")
        # self.set_config_btn = QPushButton("Set Config")
        # self.cancel_btn = QPushButton("Cancel")
        
        # self.get_config_btn.clicked.connect(self.get_config)
        # self.set_config_btn.clicked.connect(self.set_config)
        # self.cancel_btn.clicked.connect(self.reject)
        
        # button_layout.addWidget(self.get_config_btn)
        # button_layout.addWidget(self.set_config_btn)
        # button_layout.addWidget(self.cancel_btn)
        # layout.addLayout(button_layout)

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
        
        # Phase Bounds group
        self.bounds_group = QGroupBox("Phase Bounds")
        self.bounds_layout = QFormLayout()
        self.bounds_group.setLayout(self.bounds_layout)
        layout.addWidget(self.bounds_group)
        
        # Phase Camera Mapping group
        self.mapping_group = QGroupBox("Phase Camera Mapping")
        self.mapping_layout = QFormLayout()
        self.mapping_group.setLayout(self.mapping_layout)
        layout.addWidget(self.mapping_group)
        
        # Initial entries
        self.add_phase_bound()
        
        # Add buttons for bounds and mapping
        add_bounds_btn = QPushButton("+")
        add_bounds_btn.clicked.connect(self.add_phase_bound)
        add_bounds_btn.setFixedWidth(30)
        self.bounds_layout.addRow("", add_bounds_btn)
        
        add_mapping_btn = QPushButton("+")
        add_mapping_btn.clicked.connect(self.add_camera_mapping)
        add_mapping_btn.setFixedWidth(30)
        self.mapping_layout.addRow("", add_mapping_btn)
        
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

        if self.last_retrieved_config:
            self.populate_fields_from_config(self.last_retrieved_config)

        

    def add_phase_bound(self):
        bound_container = QWidget()
        bound_layout = QHBoxLayout(bound_container)
        bound_layout.setContentsMargins(0, 0, 0, 0)
        
        phase_num = len(self.phase_bounds) + 1
        
        min_spin = QSpinBox()
        min_spin.setRange(0, 100)
        min_spin.setValue(1)
        
        max_spin = QSpinBox()
        max_spin.setRange(0, 100)
        max_spin.setValue(100)
        
        remove_btn = QPushButton("-")
        remove_btn.setFixedWidth(30)
        remove_btn.clicked.connect(lambda: self.remove_phase_bound(bound_container))
        
        bound_layout.addWidget(QLabel("Min:"))
        bound_layout.addWidget(min_spin)
        bound_layout.addWidget(QLabel("Max:"))
        bound_layout.addWidget(max_spin)
        bound_layout.addWidget(remove_btn)
        
        self.phase_bounds.append((bound_container, min_spin, max_spin))
        self.bounds_layout.insertRow(len(self.phase_bounds) - 1, f"Phase {phase_num}:", bound_container)
        
        # Add corresponding camera mapping
        self.add_camera_mapping()

    def remove_phase_bound(self, container):
        for i, (widget, _, _) in enumerate(self.phase_bounds):
            if widget == container:
                self.phase_bounds.pop(i)
                self.bounds_layout.removeRow(i)
                # Remove corresponding camera mapping
                if i < len(self.camera_mappings):
                    self.remove_camera_mapping(self.camera_mappings[i][0])
                break

    def add_camera_mapping(self):
        mapping_container = QWidget()
        mapping_layout = QHBoxLayout(mapping_container)
        mapping_layout.setContentsMargins(0, 0, 0, 0)
        
        phase_num = len(self.camera_mappings) + 1
        
        cameras_edit = QLineEdit()
        remove_btn = QPushButton("-")
        remove_btn.setFixedWidth(30)
        remove_btn.clicked.connect(lambda: self.remove_camera_mapping(mapping_container))
        
        mapping_layout.addWidget(cameras_edit)
        mapping_layout.addWidget(remove_btn)
        
        self.camera_mappings.append((mapping_container, cameras_edit))
        self.mapping_layout.insertRow(len(self.camera_mappings) - 1, f"Phase {phase_num}:", mapping_container)

    def remove_camera_mapping(self, container):
        for i, (widget, _) in enumerate(self.camera_mappings):
            if widget == container:
                self.camera_mappings.pop(i)
                self.mapping_layout.removeRow(i)
                # Remove corresponding phase bound
                if i < len(self.phase_bounds):
                    self.remove_phase_bound(self.phase_bounds[i][0])
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

    # def get_config(self):
    #     try:
    #         # Get token first
    #         self.token = self.get_token()
    #         self.last_retrieved_config = {
    #             "ip": self.ip_edit.text(),
    #             "port": self.port_edit.text(),
    #             "username": self.user_edit.text(),
    #             "password": self.pass_edit.text(),
    #             "phase_bounds": config.get("phase_bounds", {}),
    #             "phase_camera_mapping": config.get("phase_camera_mapping", {})
    #         }
            
    #         # Populate fields with the retrieved configuration
    #         self.populate_fields_from_config(self.last_retrieved_config)
            
    #         QMessageBox.information(self, "Success", "Configuration retrieved successfully")
                        
    #         # Get configuration
    #         url = f"http://{self.ip_edit.text()}:{self.port_edit.text()}/get-config"
    #         headers = {"Authorization": f"Bearer {self.token}"}
            
    #         response = requests.get(url, headers=headers)
    #         response.raise_for_status()
    #         config = response.json()
            
    #         # Clear existing bounds and mappings
    #         while self.phase_bounds:
    #             self.remove_phase_bound(self.phase_bounds[0][0])
            
    #         # Add bounds and mappings from config
    #         phase_bounds = config.get("phase_bounds", {})
    #         phase_camera_mapping = config.get("phase_camera_mapping", {})
            
    #         for phase in sorted(phase_bounds.keys(), key=int):
    #             bounds = phase_bounds[phase]
                
    #             # Add phase bound
    #             self.add_phase_bound()
    #             bound = self.phase_bounds[-1]
    #             bound[1].setValue(int(bounds["g_min"]))
    #             bound[2].setValue(int(bounds["g_max"]))
                
    #             # Set camera mapping
    #             cameras = phase_camera_mapping.get(phase, [])
    #             mapping = self.camera_mappings[-1]
    #             mapping[1].setText(",".join(map(str, cameras)))
            
    #         # Add BasiQ icon
    #         self.add_basiq_icon()
            
    #         QMessageBox.information(self, "Success", "Configuration retrieved successfully")
            
    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", str(e))

    def get_config(self):
        try:
            # Get token first
            self.token = self.get_token()
            
            # Get configuration
            url = f"http://{self.ip_edit.text()}:{self.port_edit.text()}/get-config"
            headers = {"Authorization": f"Bearer {self.token}"}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Ensure config is assigned
            config = response.json()
            
            # Clear existing nodes except TPE
            if self.canvas:
                self.canvas.nodes = [node for node in self.canvas.nodes if node["type"] == "TPE"]
                
                # Add cameras
                tpe_pos = next((node["pos"] for node in self.canvas.nodes if node["type"] == "TPE"), None)
                
                if tpe_pos and config.get("status", False):
                    cameras = config.get("data", {}).get("cameras", [])
                    
                    for idx, camera in enumerate(cameras):
                        camera_node = {
                            "type": "CCTV",
                            "pos": self.calculate_camera_position(tpe_pos, idx, len(cameras)),
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
            
            # Store the last retrieved configuration
            self.last_retrieved_config = {
                "ip": self.ip_edit.text(),
                "port": self.port_edit.text(),
                "username": self.user_edit.text(),
                "password": self.pass_edit.text(),
                "phase_bounds": config.get("phase_bounds", {}),
                "phase_camera_mapping": config.get("phase_camera_mapping", {})
            }
            
            # Populate fields with the retrieved configuration
            self.populate_fields_from_config(self.last_retrieved_config)
            
            QMessageBox.information(self, "Success", "Configuration retrieved successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


    def populate_fields_from_config(self, config):
        # Clear existing phase bounds and camera mappings
        while self.phase_bounds:
            self.remove_phase_bound(self.phase_bounds[0][0])
        
        # Repopulate phase bounds and camera mappings
        phase_bounds = config.get("phase_bounds", {})
        phase_camera_mapping = config.get("phase_camera_mapping", {})
        
        # If no bounds or mappings, add an initial empty entry
        if not phase_bounds:
            self.add_phase_bound()
        else:
            for phase in sorted(phase_bounds.keys(), key=int):
                bounds = phase_bounds[phase]
                
                # Add phase bound
                self.add_phase_bound()
                bound = self.phase_bounds[-1]
                bound[1].setValue(int(bounds.get("g_min", 1)))
                bound[2].setValue(int(bounds.get("g_max", 100)))
                
                # Set camera mapping
                cameras = phase_camera_mapping.get(phase, [])
                mapping = self.camera_mappings[-1]
                mapping[1].setText(",".join(map(str, cameras)))

    # def add_basiq_icon(self):
    #     # Get parent canvas
    #     canvas = self.parent()
    #     if not canvas:
    #         return
            
    #     # Find controller node position
    #     controller_pos = None
    #     for node in canvas.nodes:
    #         if node["type"] == "Controller":
    #             controller_pos = node["pos"]
    #             break
                
    #     if not controller_pos:
    #         return
            
    #     # Create BasiQ node
    #     basiq_node = {
    #         "type": "BasiQ",
    #         "pos": canvas.snap_to_grid_pos(controller_pos + QPoint(100, 0)),
    #         "icon": QIcon("assets/icons/basiq.png"),
    #         "size": QPoint(50, 50)
    #     }
        
    #     # Add node and connection
    #     canvas.nodes.append(basiq_node)
    #     canvas.connections.append((basiq_node["pos"], controller_pos))
    #     canvas.update()

    def add_basiq_icon(self):
        # Get parent canvas
        canvas = self.canvas
        if not canvas:
            return
        
        # Find controller node position
        controller_pos = None
        for node in canvas.nodes:
            if node["type"] == "Controller":
                controller_pos = node["pos"]
                break
        
        if not controller_pos:
            return
        
        # Get algorithm settings from config
        url = f"http://{self.ip_edit.text()}:{self.port_edit.text()}/get-config"
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            config = response.json()
            
            # Create BasiQ node with characteristics
            basiq_node = {
                "type": "BasiQ",
                "pos": canvas.snap_to_grid_pos(controller_pos + QPoint(100, 0)),
                "icon": QIcon("assets/icons/basiq.png"),
                "size": QPoint(50, 50),
                "characteristics": {
                    "algorithm_name": config.get("algorithm_name", ""),
                    "computation_threshold": config.get("computation_threshold", ""),
                    "f_adj": config.get("f_adj", ""),
                    "set_setting_threshold": config.get("set_setting_threshold", ""),
                    "saturation_flow_rate": config.get("saturation_flow_rate", ""),
                    "startup_loss_time": config.get("startup_loss_time", "")
                }
            }
            
            # Add node and connection
            canvas.nodes.append(basiq_node)
            canvas.connections.append((basiq_node["pos"], controller_pos))
            canvas.update()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to get algorithm settings: {str(e)}")

    def set_config(self):
        try:
            # Get token first
            self.token = self.get_token()
            
            # Prepare configuration data
            config = {
                "phase_bounds": {},
                "phase_camera_mapping": {}
            }
            
            # Add phase bounds and camera mappings
            for i, ((_, min_spin, max_spin), (_, cameras_edit)) in enumerate(zip(self.phase_bounds, self.camera_mappings)):
                phase = str(i + 1)
                
                # Add phase bounds
                config["phase_bounds"][phase] = {
                    "g_min": min_spin.value(),
                    "g_max": max_spin.value()
                }
                
                # Add phase camera mapping
                cameras_text = cameras_edit.text().strip()
                if cameras_text:
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

    # def get_data(self):
    #     """Return the current configuration as a dictionary"""
    #     data = {
    #         "ip": self.ip_edit.text(),
    #         "port": self.port_edit.text(),
    #         "username": self.user_edit.text(),
    #         "password": self.pass_edit.text(),
    #         "phase_bounds": {},
    #         "phase_camera_mapping": {}
    #     }
        
    #     # Add phase bounds and camera mappings
    #     for i, ((_, min_spin, max_spin), (_, cameras_edit)) in enumerate(zip(self.phase_bounds, self.camera_mappings)):
    #         phase = str(i + 1)
            
    #         # Add phase bounds
    #         data["phase_bounds"][phase] = {
    #             "g_min": min_spin.value(),
    #             "g_max": max_spin.value()
    #         }
            
    #         # Add phase camera mapping
    #         cameras_text = cameras_edit.text().strip()
    #         if cameras_text:
    #             cameras = [int(cam.strip()) for cam in cameras_text.split(",") if cam.strip()]
    #             data["phase_camera_mapping"][phase] = cameras
        
    #     return data
    def get_data(self):
        """Return the current configuration as a dictionary"""
        data = {
            "ip": self.ip_edit.text(),
            "port": self.port_edit.text(),
            "username": self.user_edit.text(),
            "password": self.pass_edit.text(),
            "phase_bounds": {},
            "phase_camera_mapping": {}
        }
        
        # Add phase bounds and camera mappings
        for i, ((_, min_spin, max_spin), (_, cameras_edit)) in enumerate(zip(self.phase_bounds, self.camera_mappings)):
            phase = str(i + 1)
            
            # Add phase bounds
            data["phase_bounds"][phase] = {
                "g_min": min_spin.value(),
                "g_max": max_spin.value()
            }
            
            # Add phase camera mapping
            cameras_text = cameras_edit.text().strip()
            if cameras_text:
                cameras = [int(cam.strip()) for cam in cameras_text.split(",") if cam.strip()]
                data["phase_camera_mapping"][phase] = cameras
        
        # Add last retrieved configuration if it exists
        if hasattr(self, 'last_retrieved_config'):
            data['last_retrieved_config'] = self.last_retrieved_config
        
        return data


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
                QLineEdit, QSpinBox {
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
                QLineEdit, QSpinBox {
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