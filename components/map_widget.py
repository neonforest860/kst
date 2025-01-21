# components/map_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView

class MapWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Create web view for map
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)
        
        # Store last location
        self.last_lat = None
        self.last_lon = None
        
        # Load the map
        self.load_map()

    def load_map(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>OpenStreetMap</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <style>
                html, body {
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }
                #map {
                    height: 100%;
                    width: 100%;
                }
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                var map = L.map('map');
                
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors',
                    maxZoom: 19
                }).addTo(map);
                
                var currentMarker = null;
                
                function searchLocation(lat, lon) {
                    if (currentMarker) {
                        map.removeLayer(currentMarker);
                    }
                    var latLng = [lat, lon];
                    map.setView(latLng, 16);
                    currentMarker = L.marker(latLng).addTo(map);
                }

                // Initialize with world view
                map.setView([0, 0], 2);
            </script>
        </body>
        </html>
        """
        self.web_view.setHtml(html)

    def search_location(self, lat, lon):
        self.last_lat = lat
        self.last_lon = lon
        script = f"searchLocation({lat}, {lon})"
        self.web_view.page().runJavaScript(script)

    def showEvent(self, event):
        super().showEvent(event)
        if self.last_lat is not None and self.last_lon is not None:
            self.search_location(self.last_lat, self.last_lon)