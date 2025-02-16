# components/location_completer.py
from PyQt6.QtWidgets import QCompleter, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QTimer
import requests

class LocationCompleter(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setFocusProxy(parent)
        self.setMouseTracking(True)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.suggest_locations)
        self.current_text = ""
        
        # Style the suggestion list
        self.setStyleSheet("""
            QListWidget {
                border: 1px solid #555;
                background-color: #2a2a2a;
                color: white;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #3a3a3a;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
        """)
        
        self.itemClicked.connect(self.item_selected)

    def suggest_locations(self):
        if len(self.current_text) < 3:
            self.hide()
            return
            
        try:
            headers = {'User-Agent': 'KonectTrafficStudio/1.0'}
            response = requests.get(
                f"https://nominatim.openstreetmap.org/search?format=json&q={self.current_text}&limit=5",
                headers=headers
            )
            data = response.json()
            
            self.clear()
            if data:
                for place in data:
                    item = QListWidgetItem(place['display_name'])
                    item.setData(Qt.ItemDataRole.UserRole, {
                        'lat': float(place['lat']),
                        'lon': float(place['lon'])
                    })
                    self.addItem(item)
                
                # Position and show the list
                parent = self.parent()
                if parent:
                    pos = parent.mapToGlobal(parent.rect().bottomLeft())
                    self.setGeometry(pos.x(), pos.y(), 
                                   parent.width(), 
                                   min(200, self.sizeHintForRow(0) * self.count() + 10))
                    self.show()
            else:
                self.hide()
                
        except Exception as e:
            print(f"Error fetching suggestions: {e}")
            self.hide()

    def update_suggestions(self, text):
        self.current_text = text
        self.timer.start(300)  # Delay to avoid too many requests

    def item_selected(self, item):
        data = item.data(Qt.ItemDataRole.UserRole)
        if self.parent() and hasattr(self.parent(), 'location_selected'):
            self.parent().location_selected(item.text(), data)
        self.hide()

    def update_theme(self, dark_mode):
        if dark_mode:
            self.setStyleSheet("""
                QListWidget {
                    border: 1px solid #555;
                    background-color: #2a2a2a;
                    color: white;
                }
                QListWidget::item {
                    padding: 5px;
                }
                QListWidget::item:selected {
                    background-color: #3a3a3a;
                }
                QListWidget::item:hover {
                    background-color: #404040;
                }
            """)
        else:
            self.setStyleSheet("""
                QListWidget {
                    border: 1px solid #ccc;
                    background-color: white;
                    color: black;
                }
                QListWidget::item {
                    padding: 5px;
                }
                QListWidget::item:selected {
                    background-color: #e0e0e0;
                }
                QListWidget::item:hover {
                    background-color: #f0f0f0;
                }
            """)