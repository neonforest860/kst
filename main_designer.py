# main_designer.py
import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QApplication
from components.canvas import Canvas
from components.sidebar import Sidebar
from components.properties_panel import PropertiesPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load the UI file
        uic.loadUi('designer/mainwindow.ui', self)
        
        # Promote the canvas widget
        self.canvas = Canvas()
        self.centralWidget().layout().replaceWidget(self.findChild(QtWidgets.QWidget, 'canvas'), self.canvas)
        
        # Add sidebar
        self.sidebar = Sidebar()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar)
        
        # Add properties panel
        self.properties = PropertiesPanel()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties)
        
        # Connect actions
        self.actionSave.triggered.connect(self.canvas.save_schema)
        self.actionLoad.triggered.connect(self.canvas.load_schema)
        self.actionUndo.triggered.connect(self.canvas.undo)
        self.actionRedo.triggered.connect(self.canvas.redo)
        self.actionToggle_Grid.triggered.connect(self.canvas.toggle_snap_to_grid)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())