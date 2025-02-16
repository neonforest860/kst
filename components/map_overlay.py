# components/map_overlay.py
import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebEngineCore import QWebEnginePage
except ImportError:
    print("PyQt6-WebEngine is required. Please install it using:")
    print("pip install PyQt6-WebEngine")
    sys.exit(1)

class MapOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Debug print
        print("Initializing MapOverlay")
        self.setup_ui()

    def setup_ui(self):
        print("Setting up UI")  # Debug print
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(0)

        # Title bar
        title_bar = QWidget()
        title_bar.setFixedHeight(30)
        title_bar.setStyleSheet("background-color: #2a2a2a; border-top-left-radius: 5px; border-top-right-radius: 5px;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(5, 0, 5, 0)

        # Close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.clicked.connect(self.hide)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ff0000;
            }
        """)
        title_layout.addStretch()
        title_layout.addWidget(close_btn)

        layout.addWidget(title_bar)

        # Web view for map
        print("Creating WebEngineView")  # Debug print
        self.web_view = QWebEngineView()
        self.web_view.setMinimumSize(400, 300)
        layout.addWidget(self.web_view)

        # Set up the map
        print("Loading map HTML")  # Debug print
        self.load_map()

        # Style the widget
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                border: 1px solid #555555;
                border-radius: 5px;
            }
        """)
        self.setMinimumSize(400, 300)

    def load_map(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <style>
                body { margin: 0; padding: 0; }
                #map { 
                    position: absolute;
                    top: 0;
                    bottom: 0;
                    width: 100%;
                    height: 100%;
                    background: transparent;
                }
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                console.log('Initializing map');
                var map = L.map('map').setView([0, 0], 2);
                
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: '© OpenStreetMap contributors'
                }).addTo(map);
                
                var marker = null;
                
                function searchLocation(lat, lon) {
                    console.log('Searching:', lat, lon);
                    if (marker) {
                        map.removeLayer(marker);
                    }
                    marker = L.marker([lat, lon]).addTo(map);
                    map.setView([lat, lon], 15);
                }
                
                // Force map to update its size
                setTimeout(function() {
                    map.invalidateSize();
                    console.log('Map size updated');
                }, 100);
            </script>
        </body>
        </html>
        """
        print("Setting HTML content")  # Debug print
        self.web_view.setHtml(html)
        print("HTML content set")  # Debug print

    def search(self, lat, lon):
        print(f"Searching for: {lat}, {lon}")  # Debug print
        script = f"searchLocation({lat}, {lon});"
        self.web_view.page().runJavaScript(script, lambda result: print("Search completed"))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def showEvent(self, event):
        super().showEvent(event)
        # Force map to update when shown
        self.web_view.page().runJavaScript("if (typeof map !== 'undefined') { map.invalidateSize(); }")