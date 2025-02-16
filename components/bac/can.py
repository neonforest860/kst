# canvas.py
from PyQt6.QtWidgets import (QWidget, QMenu, QFileDialog, QMessageBox, 
                           QStackedWidget, QVBoxLayout, QInputDialog)
from PyQt6.QtCore import Qt, QPoint, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QIcon, QPixmap
import json
import platform
import subprocess
import requests
from components.cctv_dialog import CCTVDialog
from components.tpe_dialog import TPEDialog

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.init_canvas()

    def init_canvas(self):
        """Initialize canvas properties"""
        self.setObjectName("Canvas")
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        
        # State variables
        self.theme = "dark"
        self.nodes = []
        self.connections = []
        self.dragging = False
        self.current_node = None
        self.connecting = False
        self.connection_start = None
        self.snap_to_grid = True
        self.dark_mode = True
        self.grid_size = 50
        
        # History for undo/redo
        self.undo_stack = []
        self.redo_stack = []
        
        # Map related
        self.map_widget = None
        self.map_overlay = None
        self.map_mode = False

    def get_theme_colors(self):
        """Get colors based on current theme"""
        if self.theme == "light":
            return {
                "background": QColor("#ffffff"),
                "border": QColor("#000000"),
                "text": QColor("#000000"),
                "dot": QColor("#0078d7"),
                "connection": QColor("#0078d7"),
                "selected_border": QColor("#0078d7"),
                "grid": QColor("#e0e0e0")
            }
        else:
            return {
                "background": QColor("#2a2a2a"),
                "border": QColor("#ffffff"),
                "text": QColor("#ffffff"),
                "dot": QColor("#00ffff"),
                "connection": QColor("#00ffff"),
                "selected_border": QColor("#00ffff"),
                "grid": QColor("#333333")
            }

    def paintEvent(self, event):
        if self.map_mode:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw grid
        self.draw_grid(painter)
        
        # Draw connections
        for conn in self.connections:
            self.draw_connection(painter, conn)
        
        # Draw temporary connection line
        if self.connecting and self.connection_start:
            pos = self.mapFromGlobal(self.cursor().pos())
            start_pos = QPoint(
                self.connection_start["dot_pos"].x(),
                self.connection_start["dot_pos"].y()
            )
            colors = self.get_theme_colors()
            pen = QPen(colors["connection"], 2)
            painter.setPen(pen)
            painter.drawLine(start_pos, pos)
        
        # Draw nodes
        for node in self.nodes:
            self.draw_node(painter, node)

    def draw_grid(self, painter):
        """Draw the background grid"""
        colors = self.get_theme_colors()
        pen = QPen(colors["grid"], 1)
        painter.setPen(pen)
        
        for x in range(0, self.width(), self.grid_size):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), self.grid_size):
            painter.drawLine(0, y, self.width(), y)

    def draw_node(self, painter, node):
        """Draw a single node with icon and label"""
        colors = self.get_theme_colors()
        x = node["pos"].x() - 25
        y = node["pos"].y() - 25
        width = 50
        height = 50
        
        # Draw background
        painter.fillRect(x, y, width, height, colors["background"])
        
        # Draw icon
        if "icon" in node:
            icon_rect = QRectF(x + 5, y + 5, width - 10, height - 10)
            node["icon"].paint(painter, icon_rect.toRect())
        
        # Draw border
        border_color = colors["selected_border"] if node == self.connection_start else colors["border"]
        pen = QPen(border_color, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(x, y, width, height)
        
        # Draw connection dot
        dot_radius = 6
        dot_x = x + width + 15
        dot_y = y + height/2
        painter.setBrush(colors["dot"])
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(int(dot_x), int(dot_y)), dot_radius, dot_radius)
        node["dot_pos"] = QPoint(int(dot_x), int(dot_y))
        
        # Draw node text with proper width
        painter.setPen(colors["text"])
        text = node.get("name", node["type"])
        text_width = 120  # Wider text area
        text_x = x - (text_width - width) / 2
        text_rect = QRectF(text_x, y + height + 5, text_width, 20)
        
        # Use elided text for long names
        metrics = painter.fontMetrics()
        elided_text = metrics.elidedText(text, Qt.TextElideMode.ElideMiddle, int(text_width))
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, elided_text)

    def draw_connection(self, painter, connection, temporary=False):
        """Draw a connection line with arrow"""
        if isinstance(connection, tuple):
            start, end = connection
        else:
            start, end = connection["start"], connection["end"]
        
        colors = self.get_theme_colors()
        pen = QPen(colors["connection"], 2)
        painter.setPen(pen)
        painter.drawLine(start, end)
        
        if not temporary:
            self.draw_arrow(painter, start, end)

    def draw_arrow(self, painter, start, end):
        """Draw arrow head for connections"""
        arrow_size = 10
        dx = end.x() - start.x()
        dy = end.y() - start.y()
        length = (dx * dx + dy * dy) ** 0.5
        
        if length == 0:
            return

        dx, dy = dx/length, dy/length
        
        arrow_point1 = QPoint(
            int(end.x() - arrow_size * (dx * 0.866 + dy * 0.5)),
            int(end.y() - arrow_size * (-dx * 0.5 + dy * 0.866))
        )
        arrow_point2 = QPoint(
            int(end.x() - arrow_size * (dx * 0.866 - dy * 0.5)),
            int(end.y() - arrow_size * (dx * 0.5 + dy * 0.866))
        )

        painter.setBrush(painter.pen().color())
        painter.drawPolygon([end, arrow_point1, arrow_point2])

    # Event Handlers
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            clicked_node = None
            for node in self.nodes:
                if self.is_dot_clicked(node, event.pos()):
                    clicked_node = node
                    self.connecting = True
                    self.connection_start = node
                    break
                elif self.node_contains(node["pos"], event.pos()):
                    clicked_node = node
                    if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                        self.connecting = True
                        self.connection_start = node
                    else:
                        self.dragging = True
                        self.current_node = node
                    break
            self.update()

    def mouseReleaseEvent(self, event):
        if self.dragging and self.current_node:
            self.add_to_undo_stack({
                'type': 'move_node',
                'node': self.current_node,
                'old_pos': QPoint(self.current_node['pos'].x(), self.current_node['pos'].y())
            })
            self.dragging = False
            self.current_node = None
        elif self.connecting and self.connection_start:
            end_node = None
            for node in self.nodes:
                if node != self.connection_start and (
                    self.node_contains(node["pos"], event.pos()) or 
                    self.is_dot_clicked(node, event.pos())
                ):
                    end_node = node
                    break
            
            if end_node:
                new_connection = (self.connection_start["pos"], end_node["pos"])
                self.connections.append(new_connection)
                self.add_to_undo_stack({
                    'type': 'add_connection',
                    'connection': new_connection
                })
            
            self.connecting = False
            self.connection_start = None
            self.update()

    def mouseMoveEvent(self, event):
        if self.dragging and self.current_node:
            pos = event.pos()
            if self.snap_to_grid:
                pos = self.snap_to_grid_pos(pos)
            old_pos = self.current_node["pos"]
            self.current_node["pos"] = pos
            
            # Update connections
            for i, conn in enumerate(self.connections):
                start, end = conn
                if isinstance(start, QPoint) and isinstance(end, QPoint):
                    if start == old_pos:
                        self.connections[i] = (pos, end)
                    elif end == old_pos:
                        self.connections[i] = (start, pos)
            
            self.update()
        elif self.connecting and self.connection_start:
            self.update()

    def mouseDoubleClickEvent(self, event):
        for node in self.nodes:
            if self.node_contains(node["pos"], event.pos()):
                if node["type"] == "CCTV":
                    self.show_cctv_dialog(node)
                elif node["type"] == "TPE":
                    self.show_tpe_dialog(node)
                break

    # Context Menu
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        clicked_pos = event.pos()
        clicked_node = None
        clicked_connection = None

        for node in self.nodes:
            if self.node_contains(node["pos"], clicked_pos):
                clicked_node = node
                break

        for conn in self.connections:
            if self.connection_contains(conn, clicked_pos):
                clicked_connection = conn
                break

        if clicked_node:
            rename_action = menu.addAction("Rename")
            rename_action.triggered.connect(lambda: self.rename_node(clicked_node))
            
            delete_action = menu.addAction("Delete")
            delete_action.triggered.connect(lambda: self.delete_node(clicked_node))
            
            terminal_action = menu.addAction("Open Terminal")
            terminal_action.triggered.connect(self.open_terminal)

        elif clicked_connection:
            delete_conn_action = menu.addAction("Delete Connection")
            delete_conn_action.triggered.connect(lambda: self.delete_connection(clicked_connection))

        if menu.actions():
            menu.exec(event.globalPos())

    # Node Operations
    def rename_node(self, node):
        old_name = node.get("name", node["type"])
        new_name, ok = QInputDialog.getText(self, "Rename Node", 
                                          "Enter new name:", 
                                          text=old_name)
        if ok and new_name:
            node["name"] = new_name
            self.update()

    def delete_node(self, node):
        self.add_to_undo_stack({
            'type': 'delete_node',
            'node': node.copy()
        })
        
        connections_to_remove = []
        for conn in self.connections:
            start, end = conn
            if start == node["pos"] or end == node["pos"]:
                connections_to_remove.append(conn)
                self.add_to_undo_stack({
                    'type': 'delete_connection',
                    'connection': conn
                })
        
        for conn in connections_to_remove:
            self.connections.remove(conn)
        
        self.nodes.remove(node)
        self.update()

    def delete_connection(self, connection):
        self.add_to_undo_stack({
            'type': 'delete_connection',
            'connection': connection
        })
        self.connections.remove(connection)
        self.update()

    # File Operations
    def save_schema(self, filename):
        data = {
            'nodes': [],
            'connections': [],
            'version': '1.0'
        }
        
        for node in self.nodes:
            node_data = {
                'type': node['type'],
                'pos': {'x': node['pos'].x(), 'y': node['pos'].y()},
                'name': node.get('name', node['type']),
                'characteristics': node.get('characteristics', {})
            }
            data['nodes'].append(node_data)
        
        for conn in self.connections:
            if isinstance(conn, tuple):
                start, end = conn
                conn_data = {
                    'start': {'x': start.x(), 'y': start.y()},
                    'end': {'x': end.x(), 'y': end.y()}
                }
                data['connections'].append(conn_data)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_schema(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.nodes.clear()
        self.connections.clear()
        
        for node_data in data['nodes']:
            node = {
                'type': node_data['type'],
                'pos': QPoint(node_data['pos']['x'], node_data['pos']['y']),
                'icon': QIcon(f"assets/icons/{node_data['type'].lower()}.png"),
                'name': node_data.get('name', node_data['type']),
                'characteristics': node_data.get('characteristics', {})
            }
            self.nodes.append(node)
        
        for conn_data in data['connections']:
            conn = (
                QPoint(conn_data['start']['x'], conn_data['start']['y']),
                QPoint(conn_data['end']['x'], conn_data['end']['y'])
            )
            self.connections.append(conn)
        
        self.update()

    def save_as_image(self, filename):
        try:
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.GlobalColor.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.render(painter)
            painter.end()
            
            pixmap.save(filename)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save image: {str(e)}")
            return False

    # Map Overlay Operations
    def show_map_overlay(self):
        print("show_map_overlay called")
        if not hasattr(self, 'map_overlay') or self.map_overlay is None:
            from components.map_overlay import MapOverlay
            print("Creating new MapOverlay")
            self.map_overlay = MapOverlay(self)
            self.map_overlay.resize(600, 400)
            center_point = self.rect().center()
            self.map_overlay.move(
                center_point.x() - self.map_overlay.width() // 2,
                center_point.y() - self.map_overlay.height() // 2
            )
            print("MapOverlay created and positioned")
        
        print("Showing MapOverlay")
        self.map_overlay.show()
        self.map_overlay.raise_()
        print("MapOverlay shown and raised")

    def search_location(self, lat, lon):
        print(f"Canvas search_location called with {lat}, {lon}")
        if self.map_overlay is None or not self.map_overlay.isVisible():
            self.show_map_overlay()
        self.map_overlay.search(lat, lon)
        print("Search request sent to MapOverlay")

    # Dialog Operations
    def show_cctv_dialog(self, node):
        dialog = CCTVDialog(node.get("characteristics", {}), self)
        if dialog.exec():
            node["characteristics"] = dialog.get_data()
            self.update()

    def show_tpe_dialog(self, node):
        dialog = TPEDialog(node_data=node.get("characteristics", {}), 
                          canvas=self, 
                          parent=self)
        if dialog.exec():
            node["characteristics"] = dialog.get_data()
            self.update()

    # Helper Methods
    def node_contains(self, node_pos, point):
        return abs(node_pos.x() - point.x()) < 25 and abs(node_pos.y() - point.y()) < 25

    def is_dot_clicked(self, node, pos):
        if "dot_pos" in node:
            dot_radius = 6
            dx = node["dot_pos"].x() - pos.x()
            dy = node["dot_pos"].y() - pos.y()
            return (dx * dx + dy * dy) <= (dot_radius * dot_radius)
        return False

    def connection_contains(self, connection, pos):
        if isinstance(connection, tuple):
            start, end = connection
        else:
            start, end = connection["start"], connection["end"]

        line_len = ((end.x() - start.x())**2 + (end.y() - start.y())**2)**0.5
        if line_len == 0:
            return False

        dist = abs((end.x() - start.x()) * (start.y() - pos.y()) - 
                  (start.x() - pos.x()) * (end.y() - start.y())) / line_len

        return dist < 5

    def snap_to_grid_pos(self, pos):
        if self.snap_to_grid:
            x = round(pos.x() / self.grid_size) * self.grid_size
            y = round(pos.y() / self.grid_size) * self.grid_size
            return QPoint(x, y)
        return pos

    # Drag and Drop Operations
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        pos = QPoint(int(event.position().x()), int(event.position().y()))
        node_type = event.mimeData().text()
        
        icon_path = f"assets/icons/{node_type.lower()}.png"
        new_node = {
            "pos": self.snap_to_grid_pos(pos) if self.snap_to_grid else pos,
            "type": node_type,
            "icon": QIcon(icon_path),
            "size": QPoint(50, 50)
        }
        
        self.nodes.append(new_node)
        self.add_to_undo_stack({
            'type': 'add_node',
            'node': new_node
        })
        self.update()

    # Undo/Redo Operations
    def undo(self):
        if len(self.undo_stack) > 0:
            action = self.undo_stack.pop()
            self.redo_stack.append(action)
            
            if action['type'] == 'add_node':
                self.nodes.remove(action['node'])
            elif action['type'] == 'delete_node':
                self.nodes.append(action['node'])
            elif action['type'] == 'move_node':
                node = action['node']
                current_pos = node['pos']
                node['pos'] = action['old_pos']
                action['old_pos'] = current_pos
                for i, conn in enumerate(self.connections):
                    start, end = conn
                    if start == current_pos:
                        self.connections[i] = (node['pos'], end)
                    elif end == current_pos:
                        self.connections[i] = (start, node['pos'])
            elif action['type'] == 'add_connection':
                if action['connection'] in self.connections:
                    self.connections.remove(action['connection'])
            elif action['type'] == 'delete_connection':
                self.connections.append(action['connection'])
                
            self.update()

    def redo(self):
        if len(self.redo_stack) > 0:
            action = self.redo_stack.pop()
            self.undo_stack.append(action)
            
            if action['type'] == 'add_node':
                self.nodes.append(action['node'])
            elif action['type'] == 'delete_node':
                self.nodes.remove(action['node'])
            elif action['type'] == 'move_node':
                node = action['node']
                current_pos = node['pos']
                node['pos'] = action['old_pos']
                action['old_pos'] = current_pos
                for i, conn in enumerate(self.connections):
                    start, end = conn
                    if start == current_pos:
                        self.connections[i] = (node['pos'], end)
                    elif end == current_pos:
                        self.connections[i] = (start, node['pos'])
            elif action['type'] == 'add_connection':
                self.connections.append(action['connection'])
            elif action['type'] == 'delete_connection':
                if action['connection'] in self.connections:
                    self.connections.remove(action['connection'])
            
            self.update()

    # Theme Operations
    def set_theme(self, theme):
        self.theme = theme
        self.dark_mode = (theme == "dark")
        self.update()

    def toggle_snap_to_grid(self):
        self.snap_to_grid = not self.snap_to_grid
        if self.snap_to_grid:
            for node in self.nodes:
                node["pos"] = self.snap_to_grid_pos(node["pos"])
        self.update()

    # Terminal Operations
    def open_terminal(self):
        system = platform.system().lower()
        try:
            if system == 'windows':
                subprocess.Popen(['cmd.exe'])
            elif system == 'linux':
                terminals = [
                    'konsole', 'gnome-terminal', 'xfce4-terminal',
                    'alacritty', 'kitty', 'terminator', 'xterm'
                ]
                for term in terminals:
                    try:
                        subprocess.Popen([term])
                        break
                    except FileNotFoundError:
                        continue
            elif system == 'freebsd':
                subprocess.Popen(['xterm'])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to open terminal: {str(e)}")

    def get_icon(self, icon_type):
        return QIcon(f"assets/icons/{icon_type.lower()}.png")