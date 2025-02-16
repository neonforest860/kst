from PyQt6.QtWidgets import QWidget, QMenu, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt, QPoint, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QPixmap, QIcon
import json
from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, QPoint, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWebEngineWidgets import QWebEngineView
import platform
import subprocess
import requests


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.theme = "dark"
        self.setObjectName("Canvas")
        self.setAcceptDrops(True)
        self.nodes = []
        self.connections = []
        self.dragging = False
        self.current_node = None
        self.connecting = False
        self.connection_start = None
        self.setMouseTracking(True)
        self.grid_size = 50
        self.snap_to_grid = True
        self.dark_mode = True
        
        # Undo/Redo stacks
        self.undo_stack = []
        self.redo_stack = []

        # Initialize map view
        self.map_widget = None
        self.map_mode = False


    def set_theme(self, theme):
        self.theme = theme
        self.update()


        
        # self.api_key = "YOUR_GOOGLE_MAPS_API_KEY"  # Replace with your API key

    def draw_arrow(self, painter, start, end):
        """
        Draw an arrow head at the end of a line
        """
        # Set up arrow parameters
        arrow_size = 10

        # Calculate direction vector
        dx = end.x() - start.x()
        dy = end.y() - start.y()
        length = (dx * dx + dy * dy) ** 0.5
        
        if length == 0:
            return

        # Normalize direction vector
        dx /= length
        dy /= length

        # Calculate arrow points
        arrow_point1_x = end.x() - arrow_size * (dx * 0.866 + dy * 0.5)
        arrow_point1_y = end.y() - arrow_size * (-dx * 0.5 + dy * 0.866)
        arrow_point2_x = end.x() - arrow_size * (dx * 0.866 - dy * 0.5)
        arrow_point2_y = end.y() - arrow_size * (dx * 0.5 + dy * 0.866)

        # Draw the arrow head
        points = [
            end,
            QPoint(int(arrow_point1_x), int(arrow_point1_y)),
            QPoint(int(arrow_point2_x), int(arrow_point2_y))
        ]

        # Fill the arrow head with the same color as the line
        painter.setBrush(painter.pen().color())
        painter.drawPolygon(points)

    def draw_connection(self, painter, connection, temporary=False):
        """
        Draw a connection line with an arrow
        """
        # Extract start and end points
        if isinstance(connection, tuple):
            start, end = connection
        else:
            start, end = connection["start"], connection["end"]

        # Get color based on theme and connection type
        if self.theme == "light":
            color = QColor("#0078d7")  # Blue for light theme
        else:
            color = QColor("#00ffff")  # Cyan for dark theme

        # Set up the pen
        pen = QPen(color, 2)
        painter.setPen(pen)

        # Draw the main line
        painter.drawLine(start, end)

        # Draw arrow head if not a temporary connection
        if not temporary:
            self.draw_arrow(painter, start, end)



    # def save_schema(self):
    #     filename, _ = QFileDialog.getSaveFileName(self, "Save Schema", "", "JSON Files (*.json)")
    #     if filename:
    #         data = {
    #             'nodes': [],
    #             'connections': []
    #         }
            
    #         # Save nodes
    #         for node in self.nodes:
    #             node_data = {
    #                 'type': node['type'],
    #                 'pos': {'x': node['pos'].x(), 'y': node['pos'].y()},
    #                 'name': node.get('name', node['type'])
    #             }
    #             data['nodes'].append(node_data)
            
    #         # Save connections
    #         for conn in self.connections:
    #             if isinstance(conn, dict):
    #                 conn_data = {
    #                     'start': {'x': conn['start'].x(), 'y': conn['start'].y()},
    #                     'end': {'x': conn['end'].x(), 'y': conn['end'].y()}
    #                 }
    #                 data['connections'].append(conn_data)
            
    #         with open(filename, 'w') as f:
    #             json.dump(data, f, indent=4)

    # def load_schema(self):
    #     filename, _ = QFileDialog.getOpenFileName(self, "Load Schema", "", "JSON Files (*.json)")
    #     if filename:
    #         with open(filename, 'r') as f:
    #             data = json.load(f)
            
    #         # Clear current schema
    #         self.nodes.clear()
    #         self.connections.clear()
            
    #         # Load nodes
    #         for node_data in data['nodes']:
    #             node = {
    #                 'type': node_data['type'],
    #                 'pos': QPoint(node_data['pos']['x'], node_data['pos']['y'])
    #             }
    #             if 'name' in node_data:
    #                 node['name'] = node_data['name']
    #             self.nodes.append(node)
            
    #         # Load connections
    #         for conn_data in data['connections']:
    #             conn = {
    #                 'start': QPoint(conn_data['start']['x'], conn_data['start']['y']),
    #                 'end': QPoint(conn_data['end']['x'], conn_data['end']['y'])
    #             }
    #             self.connections.append(conn)
            
    #         self.update()

    # In canvas.py, add/update these methods

    # def save_schema(self, filename):
    #     """Save the current schema to a .kst file"""
    #     data = {
    #         'nodes': [],
    #         'connections': [],
    #         'version': '1.0'  # Adding version for future compatibility
    #     }
        
    #     # Save nodes with all their properties
    #     for node in self.nodes:
    #         node_data = {
    #             'type': node['type'],
    #             'pos': {'x': node['pos'].x(), 'y': node['pos'].y()},
    #             'name': node.get('name', node['type']),
    #             'size': {'width': node['size'].x(), 'height': node['size'].y()}
    #         }
    #         data['nodes'].append(node_data)
        
    #     # Save connections
    #     for conn in self.connections:
    #         if isinstance(conn, tuple):
    #             start, end = conn
    #             conn_data = {
    #                 'start': {'x': start.x(), 'y': start.y()},
    #                 'end': {'x': end.x(), 'y': end.y()}
    #             }
    #             data['connections'].append(conn_data)
        
    #     try:
    #         with open(filename, 'w') as f:
    #             json.dump(data, f, indent=4)
    #         return True
    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
    #         return False

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


    # def load_schema(self, filename):
    #     """Load a schema from a .kst file"""
    #     try:
    #         with open(filename, 'r') as f:
    #             data = json.load(f)
            
    #         # Clear current schema
    #         self.nodes.clear()
    #         self.connections.clear()
            
    #         # Load nodes
    #         for node_data in data['nodes']:
    #             node = {
    #                 'type': node_data['type'],
    #                 'pos': QPoint(node_data['pos']['x'], node_data['pos']['y']),
    #                 'size': QPoint(
    #                     node_data.get('size', {}).get('width', 50),
    #                     node_data.get('size', {}).get('height', 50)
    #                 ),
    #                 'icon': QIcon(f"assets/icons/{node_data['type'].lower()}.png")
    #             }
    #             if 'name' in node_data:
    #                 node['name'] = node_data['name']
    #             self.nodes.append(node)
            
    #         # Load connections
    #         for conn_data in data['connections']:
    #             conn = (
    #                 QPoint(conn_data['start']['x'], conn_data['start']['y']),
    #                 QPoint(conn_data['end']['x'], conn_data['end']['y'])
    #             )
    #             self.connections.append(conn)
            
    #         self.update()
    #         return True
    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")
    #         return False

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
        """Save the canvas as an image"""
        try:
            # Create a pixmap of the canvas
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.GlobalColor.transparent)
            
            # Create painter for the pixmap
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Draw the canvas content
            self.render(painter)
            painter.end()
            
            # Save the pixmap
            pixmap.save(filename)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save image: {str(e)}")
            return False

    # Add your existing Canvas methods here...
    # Rest of the Canvas class methods...

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
        
        from PyQt6.QtGui import QIcon
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

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
    #     # Draw grid
    #     self.draw_grid(painter)
        
    #     # Draw connections
    #     for conn in self.connections:
    #         self.draw_connection(painter, conn)
            
    #     # Draw temporary connection line
    #     if self.connecting and self.connection_start:
    #         pos = self.mapFromGlobal(self.cursor().pos())
    #         pen = QPen(QColor("#ffffff"), 2)
    #         painter.setPen(pen)
    #         painter.drawLine(self.connection_start["pos"], pos)
            
    #     # Draw nodes
    #     for node in self.nodes:
    #         self.draw_node(painter, node)

    def draw_grid(self, painter):
        pen = QPen(QColor("#333333"), 1)
        painter.setPen(pen)
        
        # Draw vertical lines
        for x in range(0, self.width(), self.grid_size):
            painter.drawLine(x, 0, x, self.height())
            
        # Draw horizontal lines
        for y in range(0, self.height(), self.grid_size):
            painter.drawLine(0, y, self.width(), y)

    # def draw_node(self, painter, node):
    #     x = node["pos"].x() - 25
    #     y = node["pos"].y() - 25
    #     width = 50
    #     height = 50
        
    #     # Draw background
    #     painter.fillRect(x, y, width, height, QColor("#2a2a2a"))
        
    #     # Draw icon
    #     if "icon" in node:
    #         icon_rect = QRectF(x + 5, y + 5, width - 10, height - 10)
    #         node["icon"].paint(painter, icon_rect.toRect())
        
    #     # Draw border - white in dark mode, black in light mode
    #     border_color = QColor("#ffffff") if self.dark_mode else QColor("#000000")
    #     pen = QPen(border_color, 2)
    #     painter.setPen(pen)
    #     painter.drawRect(x, y, width, height)
        
    #     # Draw label - white in dark mode, black in light mode
    #     text_color = QColor("#ffffff") if self.dark_mode else QColor("#000000")
    #     painter.setPen(text_color)
    #     text_rect = QRectF(x, y + height + 5, width, 20)
    #     painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, node.get("name", node["type"]))

    # def draw_connection(self, painter, connection):
    #     if isinstance(connection, dict):
    #         start = connection["start"]
    #         end = connection["end"]
    #     else:
    #         start, end = connection
        
    #     pen = QPen(QColor("#ffffff"), 2)
    #     painter.setPen(pen)
    #     painter.drawLine(start, end)

    # def draw_connection(self, painter, connection):
    #     if isinstance(connection, dict):
    #         start = connection["start"]
    #         end = connection["end"]
    #     else:
    #         start, end = connection
        
    #     # Use cyan in light mode, white in dark mode
    #     color = QColor("#ffffff") if self.dark_mode else QColor("#000000")
    #     pen = QPen(color, 2)
    #     painter.setPen(pen)
    #     painter.drawLine(start, end)

    def set_theme(self, dark_mode):
        self.dark_mode = dark_mode
        self.update()

    # def mousePressEvent(self, event):             #20jan-1
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         clicked_node = None
    #         for node in self.nodes:
    #             if self.node_contains(node["pos"], event.pos()):
    #                 clicked_node = node
    #                 break

    #         if clicked_node:
    #             if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
    #                 self.connecting = True
    #                 self.connection_start = clicked_node
    #             else:
    #                 self.dragging = True
    #                 self.current_node = clicked_node
    #             self.update()

    # def mouseMoveEvent(self, event):
    #     if self.dragging and self.current_node:
    #         pos = event.pos()
    #         if self.snap_to_grid:
    #             pos = self.snap_to_grid_pos(pos)
    #         self.current_node["pos"] = pos
    #         self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            clicked_node = None
            clicked_dot = False
            
            for node in self.nodes:
                if self.is_dot_clicked(node, event.pos()):
                    clicked_node = node
                    clicked_dot = True
                    break
                elif self.node_contains(node["pos"], event.pos()):
                    clicked_node = node
                    break

            if clicked_node:
                if clicked_dot or event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                    self.connecting = True
                    self.connection_start = clicked_node
                    self.update()  # Force redraw to show connection state
                else:
                    self.dragging = True
                    self.current_node = clicked_node

    def mouseMoveEvent(self, event):
        if self.dragging and self.current_node:
            # Calculate new position
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
            # Update to redraw the temporary connection line
            self.update()

    # def mouseReleaseEvent(self, event):    #20jan-1
    #     if self.connecting and self.connection_start:
    #         for node in self.nodes:
    #             if node != self.connection_start and self.node_contains(node["pos"], event.pos()):
    #                 new_connection = {
    #                     "start": self.connection_start["pos"],
    #                     "end": node["pos"],
    #                     "source_node": self.connection_start,
    #                     "target_node": node
    #                 }
    #                 self.connections.append(new_connection)
            
    #         self.connecting = False
    #         self.connection_start = None
            
    #     elif self.dragging and self.current_node:
    #         self.dragging = False
    #         self.current_node = None
            
    #     self.update()

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
                if node != self.connection_start and (self.node_contains(node["pos"], event.pos()) or self.is_dot_clicked(node, event.pos())):
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


    def node_contains(self, node_pos, point):
        return abs(node_pos.x() - point.x()) < 25 and abs(node_pos.y() - point.y()) < 25

    def add_to_undo_stack(self, action):
        self.undo_stack.append(action)
        self.redo_stack.clear()

    # def undo(self):       #20jan-1
    #     if self.undo_stack:
    #         action = self.undo_stack.pop()
    #         self.redo_stack.append(action)
            
    #         if action['type'] == 'add_node':
    #             self.nodes.remove(action['node'])
    #         elif action['type'] == 'delete_node':
    #             self.nodes.append(action['node'])
    #         elif action['type'] == 'move_node':
    #             node = action['node']
    #             old_pos = node['pos']
    #             node['pos'] = action['old_pos']
    #             action['old_pos'] = old_pos
            
    #         self.update()

    # def undo(self):       20jan-2
    #     if len(self.undo_stack) > 0:
    #         action = self.undo_stack.pop()
    #         self.redo_stack.append(action)
                
    #         if action['type'] == 'add_node':
    #             self.nodes.remove(action['node'])
    #         elif action['type'] == 'delete_node':
    #             self.nodes.append(action['node'])
    #         elif action['type'] == 'move_node':
    #             node = action['node']
    #             current_pos = node['pos']
    #             node['pos'] = action['old_pos']
    #             action['old_pos'] = current_pos
    #             # Update connected lines
    #             for i, conn in enumerate(self.connections):
    #                 start, end = conn
    #                 if start == current_pos:
    #                     self.connections[i] = (node['pos'], end)
    #                 elif end == current_pos:
    #                     self.connections[i] = (start, node['pos'])
    #         elif action['type'] == 'add_connection':
    #             if action['connection'] in self.connections:
    #                 self.connections.remove(action['connection'])
    #         elif action['type'] == 'delete_connection':
    #             self.connections.append(action['connection'])
                
    #     self.update()

    # def redo(self):       20jan-1
    #     if self.redo_stack:
    #         action = self.redo_stack.pop()
    #         self.undo_stack.append(action)
            
    #         if action['type'] == 'add_node':
    #             self.nodes.append(action['node'])
    #         elif action['type'] == 'delete_node':
    #             self.nodes.remove(action['node'])
    #         elif action['type'] == 'move_node':
    #             node = action['node']
    #             old_pos = node['pos']
    #             node['pos'] = action['old_pos']
    #             action['old_pos'] = old_pos
            
    #         self.update()

    # def redo(self):       20jan-2
    #     if len(self.redo_stack) > 0:
    #         action = self.redo_stack.pop()
    #         self.undo_stack.append(action)
                
    #         if action['type'] == 'add_node':
    #             self.nodes.append(action['node'])
    #         elif action['type'] == 'delete_node':
    #             self.nodes.remove(action['node'])
    #         elif action['type'] == 'move_node':
    #             node = action['node']
    #             current_pos = node['pos']
    #             node['pos'] = action['old_pos']
    #             action['old_pos'] = current_pos
    #             # Update connected lines
    #             for i, conn in enumerate(self.connections):
    #                 start, end = conn
    #                 if start == current_pos:
    #                     self.connections[i] = (node['pos'], end)
    #                 elif end == current_pos:
    #                     self.connections[i] = (start, node['pos'])
    #         elif action['type'] == 'add_connection':
    #             self.connections.append(action['connection'])
    #         elif action['type'] == 'delete_connection':
    #             if action['connection'] in self.connections:
    #                 self.connections.remove(action['connection'])

    #     self.update()

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
                # Update connected lines
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
                # Update connected lines
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

    def toggle_snap_to_grid(self):
        self.snap_to_grid = not self.snap_to_grid
        if self.snap_to_grid:
            for node in self.nodes:
                node["pos"] = self.snap_to_grid_pos(node["pos"])
        self.update()

    def snap_to_grid_pos(self, pos):
        if self.snap_to_grid:
            x = round(pos.x() / self.grid_size) * self.grid_size
            y = round(pos.y() / self.grid_size) * self.grid_size
            return QPoint(x, y)
        return pos

    # def contextMenuEvent(self, event):
    #     menu = QMenu(self)
    #     clicked_pos = event.pos()
    #     clicked_node = None
    #     clicked_connection = None

    #     # Check for clicked node
    #     for node in self.nodes:
    #         if self.node_contains(node["pos"], clicked_pos):
    #             clicked_node = node
    #             break

    #     # Check for clicked connection
    #     for conn in self.connections:
    #         if self.connection_contains(conn, clicked_pos):
    #             clicked_connection = conn
    #             break

    #     if clicked_node:
    #         rename_action = menu.addAction("Rename")
    #         rename_action.triggered.connect(lambda: self.rename_node(clicked_node))
            
    #         delete_action = menu.addAction("Delete")
    #         delete_action.triggered.connect(lambda: self.delete_node(clicked_node))

    #     elif clicked_connection:
    #         delete_conn_action = menu.addAction("Delete Connection")
    #         delete_conn_action.triggered.connect(lambda: self.delete_connection(clicked_connection))

    #     if menu.actions():
    #         menu.exec(event.globalPos())

    def rename_node(self, node):
        from PyQt6.QtWidgets import QInputDialog
        old_name = node.get("name", node["type"])
        new_name, ok = QInputDialog.getText(self, "Rename Node", 
                                          "Enter new name:", 
                                          text=old_name)
        if ok and new_name:
            node["name"] = new_name
            self.update()

    # def delete_node(self, node):      20jan-1
    #     # Store the node for undo
    #     self.add_to_undo_stack({
    #         'type': 'delete_node',
    #         'node': node.copy()  # Make a copy for undo
    #     })

    #     # Remove all connections to/from this node
    #     to_remove = []
    #     for conn in self.connections:
    #         if conn["source_node"] == node or conn["target_node"] == node:
    #             to_remove.append(conn)
    #             # Store each connection removal for undo
    #             self.add_to_undo_stack({
    #                 'type': 'delete_connection',
    #                 'connection': conn.copy()
    #             })

    #     # Remove the connections
    #     for conn in to_remove:
    #         self.connections.remove(conn)

    #     # Remove the node
    #     self.nodes.remove(node)
    #     self.update()

    def delete_node(self, node):
        """Delete a node and its connections"""
        self.add_to_undo_stack({
            'type': 'delete_node',
            'node': node.copy()  # Store copy of node for undo
        })
        
        # Remove all connections to/from this node
        connections_to_remove = []
        for conn in self.connections:
            start, end = conn
            if start == node["pos"] or end == node["pos"]:
                connections_to_remove.append(conn)
                # Add connection to undo stack
                self.add_to_undo_stack({
                    'type': 'delete_connection',
                    'connection': conn  # Store connection for undo
                })
        
        # Remove the connections
        for conn in connections_to_remove:
            self.connections.remove(conn)
        
        # Remove the node
        self.nodes.remove(node)
        self.update()

    def delete_connection(self, connection):
        """Delete a connection"""
        # For undo/redo, store a copy of the connection tuple
        self.add_to_undo_stack({
            'type': 'delete_connection',
            'connection': connection  # Since it's a tuple, we can store it directly
        })
        
        self.connections.remove(connection)
        self.update()

    # def connection_contains(self, connection, pos):
    #     # Get start and end points
    #     if isinstance(connection, dict):
    #         start = connection["start"]
    #         end = connection["end"]
    #     else:
    #         start, end = connection

    #     # Calculate distance from point to line
    #     line_len = ((end.x() - start.x())**2 + (end.y() - start.y())**2)**0.5
    #     if line_len == 0:
    #         return False

    #     # Calculate distance from point to line using cross product
    #     dist = abs((end.x() - start.x()) * (start.y() - pos.y()) - 
    #               (start.x() - pos.x()) * (end.y() - start.y())) / line_len

    #     # Return true if distance is less than 5 pixels
    #     return dist < 5
    

    def connection_contains(self, connection, pos):
        """Check if position is near a connection line"""
        # Get start and end points
        if isinstance(connection, tuple):
            start, end = connection
        else:
            start, end = connection["start"], connection["end"]

        # Calculate distance from point to line
        line_len = ((end.x() - start.x())**2 + (end.y() - start.y())**2)**0.5
        if line_len == 0:
            return False

        # Calculate distance from point to line using cross product
        dist = abs((end.x() - start.x()) * (start.y() - pos.y()) - 
                (start.x() - pos.x()) * (end.y() - start.y())) / line_len

        # Return true if distance is less than 5 pixels
        return dist < 5

    # def show_map_overlay(self):
    #     if not self.map_overlay:
    #         from components.map_overlay import MapOverlay
    #         self.map_overlay = MapOverlay(self, self.api_key)
    #         # Set initial size and position
    #         self.map_overlay.resize(400, 300)
    #         self.map_overlay.move(50, 50)
    #     self.map_overlay.show()

    # def hide_map_overlay(self):
    #     if self.map_overlay:
    #         self.map_overlay.hide()

    # def search_location(self, query):
    #     if self.map_overlay:
    #         self.map_overlay.search(query)

    def show_map_overlay(self):
        print("show_map_overlay called")  # Debug print
        if self.map_overlay is None:
            from components.map_overlay import MapOverlay
            print("Creating new MapOverlay")  # Debug print
            self.map_overlay = MapOverlay(self)
            self.map_overlay.resize(600, 400)
            # Center the map overlay
            center_point = self.rect().center()
            self.map_overlay.move(
                center_point.x() - self.map_overlay.width() // 2,
                center_point.y() - self.map_overlay.height() // 2
            )
            print("MapOverlay created and positioned")  # Debug print
        
        print("Showing MapOverlay")  # Debug print
        self.map_overlay.show()
        self.map_overlay.raise_()
        print("MapOverlay shown and raised")  # Debug print


    def toggle_map_view(self):
        if not self.map_mode:
            if self.map_widget is None:
                # Create map widget first time it's needed
                layout = QVBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                self.map_widget = MapWidget()
                layout.addWidget(self.map_widget)
                self.setLayout(layout)
            self.map_widget.show()
            # Hide grid
            self.update()  # Force redraw
        else:
            if self.map_widget:
                self.map_widget.hide()
            # Show grid
            self.update()  # Force redraw
        self.map_mode = not self.map_mode

    # def search_location(self, lat, lon):
    #     if not self.map_widget:
    #         # Create map if it doesn't exist
    #         layout = QVBoxLayout()
    #         layout.setContentsMargins(0, 0, 0, 0)
    #         self.map_widget = MapWidget()
    #         layout.addWidget(self.map_widget)
    #         self.setLayout(layout)
        
    #     self.map_widget.search_location(lat, lon)
    #     if not self.map_mode:
    #         self.toggle_map_view()

    # def paintEvent(self, event):     #20jan-1
    #     if not self.map_mode:
    #         painter = QPainter(self)
    #         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
    #         # Draw grid
    #         self.draw_grid(painter)
            
    #         # Draw connections
    #         for conn in self.connections:
    #             self.draw_connection(painter, conn)
                
    #         # Draw temporary connection line
    #         if self.connecting and self.connection_start:
    #             pos = self.mapFromGlobal(self.cursor().pos())
    #             pen = QPen(QColor("#ffffff") if self.dark_mode else QColor("#000000"), 2)
    #             painter.setPen(pen)
    #             painter.drawLine(self.connection_start["pos"], pos)
                
    #         # Draw nodes
    #         for node in self.nodes:
    #             self.draw_node(painter, node)

    # def paintEvent(self, event):        #20jan-2
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
    #     # Draw grid
    #     self.draw_grid(painter)
        
    #     # Draw connections
    #     pen = QPen(QColor("#00ffff"), 2)
    #     painter.setPen(pen)
    #     for conn in self.connections:
    #         self.draw_connection(painter, conn)
            
    #     # Draw temporary connection line
    #     if self.connecting and self.connection_start:
    #         start_pos = QPoint(
    #             self.connection_start["dot_pos"].x(),  # Start from dot position
    #             self.connection_start["dot_pos"].y()
    #         )
    #         pos = self.mapFromGlobal(self.cursor().pos())
    #         painter.drawLine(start_pos, pos)
        
    #     # Draw nodes
    #     for node in self.nodes:
    #         self.draw_node(painter, node)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw grid
        self.draw_grid(painter)
        
        # Draw connections
        pen = QPen(QColor("#00ffff"), 2)
        painter.setPen(pen)
        for conn in self.connections:
            self.draw_connection(painter, conn)
        
        # Draw temporary connection line
        if self.connecting and self.connection_start:
            start_pos = QPoint(
                self.connection_start["dot_pos"].x(),
                self.connection_start["dot_pos"].y()
            )
            pos = self.mapFromGlobal(self.cursor().pos())
            painter.drawLine(start_pos, pos)
        
        # Draw nodes
        for node in self.nodes:
            self.draw_node(painter, node)

    # def draw_node(self, painter, node):   #20jan-1
    #     x = node["pos"].x() - 25
    #     y = node["pos"].y() - 25
    #     width = 50
    #     height = 50
        
    #     # Draw background
    #     painter.fillRect(x, y, width, height, QColor("#2a2a2a"))
        
    #     # Draw icon
    #     if "icon" in node:
    #         icon_rect = QRectF(x + 5, y + 5, width - 10, height - 10)
    #         node["icon"].paint(painter, icon_rect.toRect())
        
    #     # Draw border - white in dark mode, black in light mode
    #     border_color = QColor("#ffffff") if self.dark_mode else QColor("#000000")
    #     pen = QPen(border_color, 2)
    #     painter.setPen(pen)
    #     painter.drawRect(x, y, width, height)
        
    #     # Draw label - white in dark mode, black in light mode
    #     text_color = QColor("#ffffff") if self.dark_mode else QColor("#000000")
    #     painter.setPen(text_color)
    #     text_rect = QRectF(x, y + height + 5, width, 20)
    #     painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, node.get("name", node["type"]))

    # def draw_node(self, painter, node): #20jan-2 
    #     x = node["pos"].x() - 25
    #     y = node["pos"].y() - 25
    #     width = 50
    #     height = 50
        
    #     # Draw node background (keep it dark even when selected)
    #     background_color = QColor("#2a2a2a")
    #     painter.fillRect(x, y, width, height, background_color)
        
    #     # Draw icon (draw this AFTER background to ensure visibility)
    #     if "icon" in node:
    #         icon_rect = QRectF(x + 5, y + 5, width - 10, height - 10)
    #         node["icon"].paint(painter, icon_rect.toRect())
        
    #     # Draw neon border (cyan if it's the connection start node)
    #     border_color = QColor("#00ffff") if self.connection_start == node else QColor("#ffffff")
    #     pen = QPen(border_color, 2)
    #     painter.setPen(pen)
    #     painter.drawRect(x, y, width, height)
        
    #     # Draw connection dot
    #     dot_radius = 6
    #     dot_x = x + width + 15
    #     dot_y = y + height/2
    #     painter.setBrush(QColor("#00ffff"))
    #     painter.drawEllipse(QPoint(int(dot_x), int(dot_y)), dot_radius, dot_radius)
        
    #     # Store dot position in node data for hit testing
    #     node["dot_pos"] = QPoint(int(dot_x), int(dot_y))
        
    #     # Draw node type text
    #     painter.setPen(QColor("white"))
    #     text_rect = QRectF(x, y + height + 5, width, 20)
    #     painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, node.get("name", node["type"]))

    # def draw_node(self, painter, node):       20jan-3
    #     x = node["pos"].x() - 25
    #     y = node["pos"].y() - 25
    #     width = 50
    #     height = 50
        
    #     # Draw node background
    #     background_color = QColor("#2a2a2a")  # Dark background
    #     painter.fillRect(x, y, width, height, background_color)
        
    #     # Draw icon BEFORE border to ensure visibility
    #     if "icon" in node:
    #         icon_rect = QRectF(x + 5, y + 5, width - 10, height - 10)
    #         node["icon"].paint(painter, icon_rect.toRect())
        
    #     # Draw neon border only (don't fill)
    #     if self.connecting and self.connection_start == node:
    #         border_color = QColor("#00ffff")  # Cyan for selected
    #     else:
    #         border_color = QColor("#ffffff")  # White for normal
        
    #     pen = QPen(border_color, 2)
    #     painter.setPen(pen)
    #     painter.setBrush(Qt.BrushStyle.NoBrush)  # Important: No fill
    #     painter.drawRect(x, y, width, height)
        
    #     # Draw connection dot
    #     dot_radius = 6
    #     dot_x = x + width + 15
    #     dot_y = y + height/2
    #     painter.setBrush(QColor("#00ffff"))
    #     painter.drawEllipse(QPoint(int(dot_x), int(dot_y)), dot_radius, dot_radius)
        
    #     # Store dot position in node data for hit testing
    #     node["dot_pos"] = QPoint(int(dot_x), int(dot_y))
        
    #     # Draw node type text
    #     painter.setPen(QColor("white"))
    #     text_rect = QRectF(x, y + height + 5, width, 20)
    #     painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, node.get("name", node["type"]))

    def draw_node(self, painter, node):
        x = node["pos"].x() - 25
        y = node["pos"].y() - 25
        width = 50
        height = 50
        
        # Theme-aware colors
        if self.theme == "light":
            background_color = QColor("#ffffff")
            border_color = QColor("#000000") if self.connection_start != node else QColor("#0078d7")
            text_color = QColor("#000000")
            dot_color = QColor("#0078d7")
        else:
            background_color = QColor("#2a2a2a")
            border_color = QColor("#ffffff") if self.connection_start != node else QColor("#00ffff")
            text_color = QColor("#ffffff")
            dot_color = QColor("#00ffff")
        
        # Draw node background
        painter.fillRect(x, y, width, height, background_color)
        
        # Draw icon
        if "icon" in node:
            icon_rect = QRectF(x + 5, y + 5, width - 10, height - 10)
            node["icon"].paint(painter, icon_rect.toRect())
        
        # Draw border
        pen = QPen(border_color, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(x, y, width, height)
        
        # Draw connection dot
        dot_radius = 6
        dot_x = x + width + 15
        dot_y = y + height/2
        painter.setBrush(dot_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(int(dot_x), int(dot_y)), dot_radius, dot_radius)
        
        # Store dot position
        node["dot_pos"] = QPoint(int(dot_x), int(dot_y))
        
        # Draw node type text
        painter.setPen(text_color)
        text_rect = QRectF(x, y + height + 5, width, 20)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, node.get("name", node["type"]))


    # def contextMenuEvent(self, event):
    #     menu = QMenu(self)
    #     clicked_pos = event.pos()
    #     clicked_node = None

    #     # Check for clicked node
    #     for node in self.nodes:
    #         if self.node_contains(node["pos"], clicked_pos):
    #             clicked_node = node
    #             break

    #     if clicked_node:
    #         rename_action = menu.addAction("Rename")
    #         rename_action.triggered.connect(lambda: self.rename_node(clicked_node))
            
    #         delete_action = menu.addAction("Delete")
    #         delete_action.triggered.connect(lambda: self.delete_node(clicked_node))
            
    #         terminal_action = menu.addAction("Open Terminal")
    #         terminal_action.triggered.connect(lambda: self.open_terminal())

    #     if menu.actions():
    #         menu.exec(event.globalPos())

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        clicked_pos = event.pos()
        clicked_node = None
        clicked_connection = None

        # Check for clicked node
        for node in self.nodes:
            if self.node_contains(node["pos"], clicked_pos):
                clicked_node = node
                break

        # Check for clicked connection
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
            terminal_action.triggered.connect(lambda: self.open_terminal())

        elif clicked_connection:
            delete_conn_action = menu.addAction("Delete Connection")
            delete_conn_action.triggered.connect(lambda: self.delete_connection(clicked_connection))

        if menu.actions():
            menu.exec(event.globalPos())

    def open_terminal(self):
        system = platform.system().lower()
        try:
            if system == 'windows':
                subprocess.Popen(['cmd.exe'])
            elif system == 'linux':
                # Try different terminal emulators
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

    def mouseDoubleClickEvent(self, event):
        for node in self.nodes:
            if self.node_contains(node["pos"], event.pos()):
                if node["type"] == "CCTV":
                    self.show_cctv_dialog(node)
                elif node["type"] == "TPE":
                    self.show_tpe_dialog(node)
                #icons carachter
                break        
    
    def show_cctv_dialog(self, node):
        from components.cctv_dialog import CCTVDialog
        dialog = CCTVDialog(node.get("characteristics", {}), self)
        if dialog.exec():
            node["characteristics"] = dialog.get_data()
            self.update()

    # def show_tpe_dialog(self, node):
    #     from components.tpe_dialog import TPEDialog
    #     dialog = TPEDialog(node.get("characteristics", {}), self, self)
    #     if dialog.exec():
    #         node["characteristics"] = dialog.get_data()
    #         self.update()

    def show_tpe_dialog(self, node):
        from components.tpe_dialog import TPEDialog
        dialog = TPEDialog(node_data=node.get("characteristics", {}), 
                        canvas=self, 
                        parent=self)
        if dialog.exec():
            node["characteristics"] = dialog.get_data()
            self.update()


    def get_icon(self, icon_type):
        """Helper method to get icon for a node type"""
        return QIcon(f"assets/icons/{icon_type.lower()}.png")


    def is_dot_clicked(self, node, pos):
        if "dot_pos" in node:
            dot_radius = 6
            dx = node["dot_pos"].x() - pos.x()
            dy = node["dot_pos"].y() - pos.y()
            return (dx * dx + dy * dy) <= (dot_radius * dot_radius)
        return False


    # def draw_connection(self, painter, connection):       20jan-1
    #     if isinstance(connection, dict):
    #         start = connection["start"]
    #         end = connection["end"]
    #     else:
    #         start, end = connection
        
    #     # Line color - white in dark mode, black in light mode
    #     line_color = QColor("#ffffff") if self.dark_mode else QColor("#000000")
    #     pen = QPen(line_color, 2)
    #     painter.setPen(pen)
    #     painter.drawLine(start, end)

    # In canvas.py, update the draw_connection method

    def draw_connection(self, painter, connection, temporary=False):
        # Extract start and end points
        if isinstance(connection, tuple):
            start, end = connection
        else:
            start, end = connection["start"], connection["end"]

        # Set color based on theme
        if hasattr(self, 'theme') and self.theme == "light":
            color = QColor("#000000")  # Black for light theme
        else:
            color = QColor("#00ffff")  # Cyan for dark theme

        pen = QPen(color, 2)
        painter.setPen(pen)
        
        # Draw the main line
        painter.drawLine(start, end)
        
        # Draw arrow if not temporary
        if not temporary:
            self.draw_arrow(painter, start, end)

    # def draw_node(self, painter, node):
    #     x = node["pos"].x() - 25
    #     y = node["pos"].y() - 25
    #     width = 50
    #     height = 50
        
    #     # Draw node background
    #     background_color = QColor("#ffffff") if hasattr(self, 'theme') and self.theme == "light" else QColor("#2a2a2a")
    #     painter.fillRect(x, y, width, height, background_color)
        
    #     # Draw icon
    #     if "icon" in node:
    #         icon_rect = QRectF(x + 5, y + 5, width - 10, height - 10)
    #         node["icon"].paint(painter, icon_rect.toRect())
        
    #     # Draw border
    #     if self.connection_start == node:
    #         border_color = QColor("#000000") if hasattr(self, 'theme') and self.theme == "light" else QColor("#00ffff")
    #     else:
    #         border_color = QColor("#000000") if hasattr(self, 'theme') and self.theme == "light" else QColor("#ffffff")
        
    #     pen = QPen(border_color, 2)
    #     painter.setPen(pen)
    #     painter.drawRect(x, y, width, height)
        
    #     # Draw connection dot
    #     dot_radius = 6
    #     dot_x = x + width + 15
    #     dot_y = y + height/2
    #     painter.setBrush(QColor("#000000") if hasattr(self, 'theme') and self.theme == "light" else QColor("#00ffff"))
    #     painter.drawEllipse(QPoint(int(dot_x), int(dot_y)), dot_radius, dot_radius)
        
    #     # Store dot position
    #     node["dot_pos"] = QPoint(int(dot_x), int(dot_y))
        
    #     # Draw node text
    #     painter.setPen(QColor("black") if hasattr(self, 'theme') and self.theme == "light" else QColor("white"))
    #     text_rect = QRectF(x, y + height + 5, width, 20)
    #     painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, node.get("name", node["type"]))
    #     def update_theme(self, dark_mode):
    #         self.dark_mode = dark_mode
    #         self.update()  # Redraw with new theme

    def search_location(self, lat, lon):
        print(f"Canvas search_location called with {lat}, {lon}")  # Debug print
        if self.map_overlay is None or not self.map_overlay.isVisible():
            self.show_map_overlay()
        self.map_overlay.search(lat, lon)
        print("Search request sent to MapOverlay")  # Debug print

    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #     # If map overlay exists and is visible, resize it
    #     if self.show_map_overlay is not None and self.show_map_overlay.isVisible():
    #         self.show_map_overlay.resize(self.width() // 2, self.height() // 2)
    #         self.show_map_overlay.move(
    #             (self.width() - self.map_overlay.width()) // 2,
    #             (self.height() - self.map_overlay.height()) // 2
            # )