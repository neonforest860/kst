# main.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from components.sidebar import Sidebar
from components.canvas import Canvas
from utils.styles import load_styles

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Designer")
        self.setStyleSheet(load_styles())
        self.setMinimumSize(1200, 800)
        
        # Set main central widget
        self.central_widget = Canvas()
        self.setCentralWidget(self.central_widget)
        
        # Add sidebar
        self.sidebar = Sidebar()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

# components/__init__.py
# This file can be empty or contain package initialization code

# components/sidebar.py
from PyQt6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QSize
from PyQt6.QtGui import QIcon

class Sidebar(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | 
                            Qt.DockWidgetArea.RightDockWidgetArea)
        
        # Create widget for sidebar content
        self.content = QWidget()
        self.setWidget(self.content)
        
        # Setup layout
        self.layout = QVBoxLayout(self.content)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        
        # Add buttons
        self.buttons = []
        self.add_button("Camera", "assets/icons/camera.png")
        self.add_button("TMS", "assets/icons/tms.png")
        self.add_button("Algorithm", "assets/icons/algorithm.png")
        
        # Set fixed width
        self.setFixedWidth(60)
        self.expanded = False

    def add_button(self, text, icon_path):
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(32, 32))
        button.setToolTip(text)
        button.setFixedSize(50, 50)
        self.buttons.append((button, text))
        self.layout.addWidget(button)
        button.clicked.connect(self.toggle_sidebar)
        
    def toggle_sidebar(self):
        width = 200 if not self.expanded else 60
        animation = QPropertyAnimation(self, b"minimumWidth")
        animation.setDuration(200)
        animation.setStartValue(self.width())
        animation.setEndValue(width)
        animation.start()
        
        self.expanded = not self.expanded
        for button, text in self.buttons:
            if self.expanded:
                button.setText(text)
            else:
                button.setText("")

# components/canvas.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.nodes = []
        self.connections = []
        self.dragging = False
        self.current_node = None
        self.setMouseTracking(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        pos = event.pos()
        text = event.mimeData().text()
        self.nodes.append({
            "pos": pos,
            "type": text,
            "size": QPoint(50, 50)
        })
        self.update()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            for node in self.nodes:
                if self.node_contains(node["pos"], event.pos()):
                    self.dragging = True
                    self.current_node = node
                    break
                    
    def mouseReleaseEvent(self, event):
        if self.dragging:
            self.dragging = False
            self.current_node = None
            
    def mouseMoveEvent(self, event):
        if self.dragging and self.current_node:
            self.current_node["pos"] = event.pos()
            self.update()
            
    def node_contains(self, node_pos, point):
        return abs(node_pos.x() - point.x()) < 25 and abs(node_pos.y() - point.y()) < 25
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw grid
        self.draw_grid(painter)
        
        # Draw connections
        pen = QPen(QColor("#00ffff"), 2)
        painter.setPen(pen)
        for conn in self.connections:
            painter.drawLine(conn[0], conn[1])
            
        # Draw nodes
        for node in self.nodes:
            self.draw_node(painter, node)
            
    def draw_grid(self, painter):
        pen = QPen(QColor("#333333"), 1)
        painter.setPen(pen)
        
        # Draw vertical lines
        for x in range(0, self.width(), 50):
            painter.drawLine(x, 0, x, self.height())
            
        # Draw horizontal lines
        for y in range(0, self.height(), 50):
            painter.drawLine(0, y, self.width(), y)
            
    def draw_node(self, painter, node):
        # Draw node background
        painter.fillRect(
            node["pos"].x() - 25,
            node["pos"].y() - 25,
            50, 50,
            QColor("#2a2a2a")
        )
        
        # Draw node border with neon effect
        painter.setPen(QPen(QColor("#00ffff"), 2))
        painter.drawRect(
            node["pos"].x() - 25,
            node["pos"].y() - 25,
            50, 50
        )

# utils/__init__.py
# This file can be empty or contain package initialization code

# utils/styles.py
def load_styles():
    return """
        QMainWindow {
            background-color: #1a1a1a;
        }
        
        QDockWidget {
            background-color: #2a2a2a;
            border: none;
            color: white;
        }
        
        QPushButton {
            background-color: #2a2a2a;
            border: 2px solid #00ff00;
            border-radius: 5px;
            color: white;
            padding: 5px;
        }
        
        QPushButton:hover {
            background-color: #3a3a3a;
            border-color: #00ff99;
        }
        
        QLabel {
            color: white;
        }
        
        QWidget#Canvas {
            background-color: #1a1a1a;
        }
    """