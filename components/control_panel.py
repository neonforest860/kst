from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLineEdit, QLabel, QListWidget, QComboBox, QTableWidget,
                           QTableWidgetItem, QHeaderView, QGroupBox, QStackedWidget,
                           QDialog, QDialogButtonBox, QTimeEdit)
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
        
        # Add toggle button row
        toggle_layout = QHBoxLayout()
        self.view_toggle = QPushButton("⇄")  # Unicode arrow symbol
        self.view_toggle.setFixedWidth(30)
        self.view_toggle.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                padding: 5px;
                font-size: 16px;
            }
        """)
        self.view_toggle.clicked.connect(self.toggle_timing_view)
        toggle_layout.addWidget(self.view_toggle)
        toggle_layout.addStretch()
        timing_layout.addLayout(toggle_layout)
        
        # Container for tables
        self.table_stack = QStackedWidget()
        
        # Time-based table (original)
        self.timing_table = QTableWidget()
        days = ["شنبه", "یکشنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنج شنبه", "جمعه"]
        hours = [f"{i:02d}:00" for i in range(24)]
        
        self.timing_table.setRowCount(len(days))
        self.timing_table.setColumnCount(len(hours))
        self.timing_table.setHorizontalHeaderLabels(hours)
        self.timing_table.setVerticalHeaderLabels(days)
        
        # Set smaller cell sizes
        for i in range(len(hours)):
            self.timing_table.setColumnWidth(i, 40)  # Reduced from 60 to 40
        for i in range(len(days)):
            self.timing_table.setRowHeight(i, 25)  # Reduced from 40 to 25
        
        # Zone-based table
        self.zone_table = QTableWidget()
        self.zone_table.setRowCount(len(days))
        self.zone_table.setColumnCount(1)  # Start with one zone
        self.zone_table.setVerticalHeaderLabels(days)
        self.zone_table.setHorizontalHeaderLabels(["Zone 1"])
        
        # Add "+" button for new zones
        self.add_zone_btn = QPushButton("+")
        self.add_zone_btn.setFixedSize(25, 25)
        self.add_zone_btn.clicked.connect(self.add_new_zone)
        
        # Create zone header widget
        zone_header_widget = QWidget()
        zone_header_layout = QHBoxLayout(zone_header_widget)
        zone_header_layout.setContentsMargins(0, 0, 0, 0)
        zone_header_layout.addWidget(self.add_zone_btn)
        zone_header_layout.addStretch()
        
        # Add tables to stack
        self.table_stack.addWidget(self.timing_table)
        self.table_stack.addWidget(self.zone_table)
        
        timing_layout.addWidget(self.table_stack)
        timing_group.setLayout(timing_layout)
        main_layout.addWidget(timing_group)
        
        # Connect signals
        self.timing_table.clicked.connect(self.on_timing_table_click)
        self.zone_table.clicked.connect(self.on_zone_table_click)
        
        # Connect signals
        self.create_plan_btn.clicked.connect(self.create_plan)
        self.save_btn.clicked.connect(self.save_plan)
        self.clear_btn.clicked.connect(self.clear_fields)

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
        
        menu.exec(QCursor.pos())

    def toggle_timing_view(self):
        current_index = self.table_stack.currentIndex()
        self.table_stack.setCurrentIndex(1 if current_index == 0 else 0)

    def add_new_zone(self):
        current_cols = self.zone_table.columnCount()
        self.zone_table.setColumnCount(current_cols + 1)
        self.zone_table.setHorizontalHeaderItem(
            current_cols,
            QTableWidgetItem(f"Zone {current_cols + 1}")
        )
        self.zone_table.setColumnWidth(current_cols, 100)

    def on_zone_table_click(self, index):
        dialog = QDialog(self)
        dialog.setWindowTitle("Set Zone Time")
        layout = QVBoxLayout(dialog)
        
        # Add time edit widgets
        start_time = QTimeEdit()
        end_time = QTimeEdit()
        start_time.setDisplayFormat("HH:mm")
        end_time.setDisplayFormat("HH:mm")
        
        # Create labels and add widgets
        layout.addWidget(QLabel("Start Time:"))
        layout.addWidget(start_time)
        layout.addWidget(QLabel("End Time:"))
        layout.addWidget(end_time)
        
        # Add buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            time_text = f"{start_time.time().toString('HH:mm')}-\n{end_time.time().toString('HH:mm')}"
            self.zone_table.setItem(index.row(), index.column(), 
                                  QTableWidgetItem(time_text))

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
                QPushButton#view_toggle {
                    border-radius: 15px;
                    background-color: #3a3a3a;
                }
                QPushButton#view_toggle:hover {
                    background-color: #4a4a4a;
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
                    padding: 2px;
                    border: none;
                    text-align: center;
                }
                QTableWidget::item:selected {
                    background-color: #3a3a3a;
                }
                QHeaderView::section {
                    background-color: #2a2a2a;
                    color: white;
                    padding: 2px;
                    border: 1px solid #3a3a3a;
                    font-size: 11px;
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
                QPushButton#view_toggle {
                    border-radius: 15px;
                    background-color: #e0e0e0;
                }
                QPushButton#view_toggle:hover {
                    background-color: #d0d0d0;
                }
                QLineEdit {
                    background-color: white;
                    border: 1px solid #d0d0d0;
                    padding: 5px;
                }
                QTableWidget {
                    background-color: white;
                    border: 1px solid #d0d0d0;
                    gridline-color: #d0d0d0;
                }
                QTableWidget::item {
                    padding: 2px;
                    border: none;
                    text-align: center;
                }
                QTableWidget::item:selected {
                    background-color: #e0e0e0;
                }
                QHeaderView::section {
                    background-color: white;
                    color: black;
                    padding: 2px;
                    border: 1px solid #d0d0d0;
                    font-size: 11px;
                }
                QHeaderView::section:vertical {
                    min-width: 80px;
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