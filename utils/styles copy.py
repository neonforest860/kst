# utils/styles.py

def load_styles():
    return load_dark_theme()  # Default to dark theme

def load_dark_theme():
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
            border: none;
            color: white;
            padding: 5px;
        }
        
        QPushButton:hover {
            background-color: #3a3a3a;
        }
        
        QLabel {
            color: white;
        }
        
        QComboBox {
            background-color: #2a2a2a;
            border: none;
            color: white;
            padding: 5px;
        }
        
        QComboBox:hover {
            background-color: #3a3a3a;
        }
        
        QLineEdit {
            background-color: #2a2a2a;
            border: none;
            color: white;
            padding: 5px;
        }
    """

def load_light_theme():
    return """
        QMainWindow {
            background-color: #f0f0f0;
        }
        
        QDockWidget {
            background-color: #ffffff;
            border: none;
            color: black;
        }
        
        QPushButton {
            background-color: #ffffff;
            border: 1px solid #dddddd;
            color: black;
            padding: 5px;
        }
        
        QPushButton:hover {
            background-color: #f5f5f5;
        }
        
        QLabel {
            color: black;
        }
        
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #dddddd;
            color: black;
            padding: 5px;
        }
        
        QComboBox:hover {
            background-color: #f5f5f5;
        }
        
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #dddddd;
            color: black;
            padding: 5px;
        }
    """