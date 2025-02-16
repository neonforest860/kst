# components/properties_panel.py
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QFormLayout, 
                            QLineEdit, QComboBox, QPushButton, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal

class PropertiesPanel(QDockWidget):
    property_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__("Properties")
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        
        self.widget = QWidget()
        self.setWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)
        self.form = QFormLayout()
        self.layout.addLayout(self.form)
        
        # Node properties
        self.name_edit = QLineEdit()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Camera", "TMS", "Algorithm"])
        self.description_edit = QLineEdit()
        
        self.form.addRow("Name:", self.name_edit)
        self.form.addRow("Type:", self.type_combo)
        self.form.addRow("Description:", self.description_edit)
        
        # Connection properties
        self.connection_type = QComboBox()
        self.connection_type.addItems(["Data", "Control", "Event"])
        self.form.addRow("Connection Type:", self.connection_type)
        
        # Apply button
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.apply_changes)
        self.layout.addWidget(self.apply_btn)
        
        self.current_item = None
        self.hide()

    def show_node_properties(self, node):
        self.current_item = node
        self.name_edit.setText(node.get("name", ""))
        self.type_combo.setCurrentText(node.get("type", ""))
        self.description_edit.setText(node.get("description", ""))
        self.connection_type.hide()
        self.show()

    def show_connection_properties(self, connection):
        self.current_item = connection
        self.connection_type.show()
        self.connection_type.setCurrentText(connection.get("type", "Data"))
        self.name_edit.hide()
        self.type_combo.hide()
        self.description_edit.hide()
        self.show()

    def apply_changes(self):
        if isinstance(self.current_item, dict):
            properties = {
                "name": self.name_edit.text(),
                "type": self.type_combo.currentText(),
                "description": self.description_edit.text()
            }
            self.property_changed.emit(properties)
