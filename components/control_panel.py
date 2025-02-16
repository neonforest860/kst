from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLineEdit, QLabel, QListWidget, QComboBox, QTableWidget,
                           QTableWidgetItem, QHeaderView, QGroupBox)
from PyQt6.QtCore import Qt

class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.dark_mode = True
        self.apply_theme()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Top section: Plan Creation and Control
        top_group = QGroupBox("Plan Control")
        top_layout = QVBoxLayout()
        
        # Plan creation controls
        input_layout = QHBoxLayout()
        self.plan_name = QLineEdit()
        self.plan_name.setPlaceholderText("Enter plan name")
        self.create_plan_btn = QPushButton("Create Plan")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["USB", "Software"])
        
        input_layout.addWidget(QLabel("Plan Name:"))
        input_layout.addWidget(self.plan_name)
        input_layout.addWidget(self.create_plan_btn)
        input_layout.addWidget(QLabel("Mode:"))
        input_layout.addWidget(self.mode_combo)
        
        # Button controls
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.clear_btn = QPushButton("Clear")
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.clear_btn)
        
        # Inventory list
        inventory_layout = QVBoxLayout()
        inventory_layout.addWidget(QLabel("Inventory:"))
        self.inventory_list = QListWidget()
        inventory_layout.addWidget(self.inventory_list)
        
        top_layout.addLayout(input_layout)
        top_layout.addLayout(button_layout)
        top_layout.addLayout(inventory_layout)
        top_group.setLayout(top_layout)
        main_layout.addWidget(top_group)
        
        # Phase Signal Group Table
        signal_group = QGroupBox("Phase Signal Group")
        signal_layout = QVBoxLayout()
        self.phase_table = QTableWidget()
        self.phase_table.setColumnCount(8)  # Assuming 8 phases
        self.phase_table.setHorizontalHeaderLabels([f"Phase {i+1}" for i in range(8)])
        self.phase_table.clicked.connect(self.on_phase_table_click)
        signal_layout.addWidget(self.phase_table)
        signal_group.setLayout(signal_layout)
        main_layout.addWidget(signal_group)
        
        # Timing Table
        timing_group = QGroupBox("Timing Schedule")
        timing_layout = QVBoxLayout()
        self.timing_table = QTableWidget()
        days = ["شنبه", "یکشنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنج شنبه", "جمعه"]
        hours = [f"{i:02d}:00" for i in range(24)]
        
        self.timing_table.setRowCount(len(days))
        self.timing_table.setColumnCount(len(hours))
        self.timing_table.setHorizontalHeaderLabels(hours)
        self.timing_table.setVerticalHeaderLabels(days)
        
        # Set column widths to make the table more compact
        for i in range(len(hours)):
            self.timing_table.setColumnWidth(i, 60)  # Set each column to 60 pixels
            
        # Set row heights
        for i in range(len(days)):
            self.timing_table.setRowHeight(i, 40)  # Set each row to 40 pixels
        
        # Enable text alignment for header labels
        header = self.timing_table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_vertical = self.timing_table.verticalHeader()
        header_vertical.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.timing_table.clicked.connect(self.on_timing_table_click)
        
        timing_layout.addWidget(self.timing_table)
        timing_group.setLayout(timing_layout)
        main_layout.addWidget(timing_group)
        
        # Connect signals
        self.create_plan_btn.clicked.connect(self.create_plan)
        self.save_btn.clicked.connect(self.save_plan)
        self.clear_btn.clicked.connect(self.clear_fields)

    def create_plan(self):
        plan_name = self.plan_name.text()
        if plan_name:
            self.inventory_list.addItem(plan_name)
            self.plan_name.clear()

    def save_plan(self):
        # Implementation for saving plan configuration
        pass

    def clear_fields(self):
        self.plan_name.clear()
        self.phase_table.clearContents()
        self.timing_table.clearContents()

    def on_phase_table_click(self, index):
        current_item = self.phase_table.item(index.row(), index.column())
        if current_item and current_item.text() == "X":
            self.phase_table.setItem(index.row(), index.column(), QTableWidgetItem(""))
        else:
            self.phase_table.setItem(index.row(), index.column(), QTableWidgetItem("X"))

    def on_timing_table_click(self, index):
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QCursor
        
        menu = QMenu(self)
        pretime_action = menu.addAction("Pretime")
        actuated_action = menu.addAction("Actuated")
        fix_action = menu.addAction("Fix")
        
        def on_pretime():
            # Show plan selection dialog
            self.timing_table.setItem(index.row(), index.column(), 
                                    QTableWidgetItem("PT"))
            
        def on_actuated():
            self.timing_table.setItem(index.row(), index.column(), 
                                    QTableWidgetItem("AC"))
            
        def on_fix():
            self.timing_table.setItem(index.row(), index.column(), 
                                    QTableWidgetItem("FX"))
        
        pretime_action.triggered.connect(on_pretime)
        actuated_action.triggered.connect(on_actuated)
        fix_action.triggered.connect(on_fix)
        
        # Use cursor position instead of index position
        menu.exec(QCursor.pos())

    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget {
                    background-color: #1a1a1a;
                    color: white;
                }
                QGroupBox {
                    border: 1px solid #3a3a3a;
                    margin-top: 0.5em;
                    padding-top: 0.5em;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px 0 3px;
                }
                QPushButton {
                    background-color: #2a2a2a;
                    border: 1px solid #3a3a3a;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                }
                QLineEdit {
                    background-color: #2a2a2a;
                    border: 1px solid #3a3a3a;
                    padding: 5px;
                }
                QTableWidget {
                    background-color: #2a2a2a;
                    border: 1px solid #3a3a3a;
                    gridline-color: #3a3a3a;
                }
                QTableWidget::item {
                    padding: 5px;
                    border: none;
                    text-align: center;
                }
                QTableWidget::item:selected {
                    background-color: #3a3a3a;
                }
                QHeaderView::section {
                    background-color: #2a2a2a;
                    color: white;
                    padding: 5px;
                    border: 1px solid #3a3a3a;
                }
                QHeaderView::section:vertical {
                    min-width: 80px;
                }
                QListWidget {
                    background-color: #2a2a2a;
                    border: 1px solid #3a3a3a;
                }
                QComboBox {
                    background-color: #2a2a2a;
                    border: 1px solid #3a3a3a;
                    padding: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f0f0f0;
                    color: black;
                }
                QGroupBox {
                    border: 1px solid #d0d0d0;
                    margin-top: 0.5em;
                    padding-top: 0.5em;
                }
                QPushButton {
                    background-color: white;
                    border: 1px solid #d0d0d0;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QLineEdit {
                    background-color: white;
                    border: 1px solid #d0d0d0;
                    padding: 5px;
                }
                QTableWidget {
                    background-color: white;
                    border: 1px solid #d0d0d0;
                }
                QListWidget {
                    background-color: white;
                    border: 1px solid #d0d0d0;
                }
                QComboBox {
                    background-color: white;
                    border: 1px solid #d0d0d0;
                    padding: 5px;
                }
            """)