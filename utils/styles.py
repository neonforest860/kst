# utils/styles.py

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
        
        QDockWidget::title {
            padding: 8px;
            background: #f0f0f0;
            color: black;
        }
        
        QPushButton {
            background-color: #ffffff;
            border: 1px solid #0078d7;
            border-radius: 5px;
            color: black;
            padding: 5px;
        }
        
        QPushButton:hover {
            background-color: #e5f1fb;
            border-color: #429ce3;
        }
        
        QPushButton:pressed {
            background-color: #0078d7;
            color: white;
        }
        
        QLabel {
            color: darkcyan;
        }
        
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #0078d7;
            border-radius: 3px;
            color: black;
            padding: 5px;
        }
        
        QComboBox:hover {
            border-color: #429ce3;
        }
        
        QComboBox::drop-down {
            border: none;
        }
        
        QComboBox::down-arrow {
            image: url(assets/icons/down-arrow.png);
            width: 12px;
            height: 12px;
        }
        
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #0078d7;
            border-radius: 3px;
            color: black;
            padding: 5px;
        }
        
        QLineEdit:hover {
            border-color: #429ce3;
        }
        
        QLineEdit:focus {
            border-color: #0078d7;
            border-width: 2px;
        }
        
        QMenuBar {
            background-color: #f0f0f0;
            color: black;
            border-bottom: 1px solid #d4d4d4;
        }
        
        QMenuBar::item {
            padding: 5px 10px;
            background: transparent;
        }
        
        QMenuBar::item:selected {
            background-color: #0078d7;
            color: white;
        }
        
        QMenu {
            background-color: #ffffff;
            border: 1px solid #d4d4d4;
            padding: 5px 0px;
        }
        
        QMenu::item {
            padding: 5px 30px;
        }
        
        QMenu::item:selected {
            background-color: #0078d7;
            color: white;
        }
        
        QWidget#Canvas {
            background-color: #ffffff;
            border: none;
        }
        
        /* Sidebar specific styles */
        QDockWidget > QWidget {
            background: #ffffff;
        }
        
        /* Node styles */
        .node {
            background-color: #ffffff;
            border: 2px solid #0078d7;
        }
        
        .node:hover {
            border-color: #429ce3;
        }
        
        /* Connection styles */
        .connection-line {
            color: #000000;
        }
        
        /* ScrollBar styles */
        QScrollBar:vertical {
            border: none;
            background: #f0f0f0;
            width: 10px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background: #c1c1c1;
            min-height: 30px;
            border-radius: 5px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #a8a8a8;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        /* Section headers */
        .section-header {
            background-color: #f5f5f5;
            color: black;
            padding: 5px;
            font-weight: bold;
        }
        
        /* Tool tips */
        QToolTip {
            background-color: #ffffff;
            border: 1px solid #d4d4d4;
            color: black;
            padding: 5px;
        }
    """


def load_styles(theme="dark"):
    if theme == "dark":
        return load_dark_theme()
    return load_light_theme()
# # utils/styles.py

# def load_light_theme():
#     return """
#         QMainWindow {
#             background-color: #f0f0f0;
#         }
        
#         QDockWidget {
#             background-color: #ffffff;
#             border: none;
#             color: black;
#         }
        
#         QDockWidget::title {
#             padding: 8px;
#             background: #f0f0f0;
#             color: black;
#         }
        
#         QPushButton {
#             background-color: #ffffff;
#             border: 1px solid #0078d7;
#             border-radius: 5px;
#             color: black;
#             padding: 5px;
#         }
        
#         QPushButton:hover {
#             background-color: #e5f1fb;
#             border-color: #429ce3;
#         }
        
#         QPushButton:pressed {
#             background-color: #0078d7;
#             color: white;
#         }
        
#         QLabel {
#             color: black;
#         }
        
#         QComboBox {
#             background-color: #ffffff;
#             border: 1px solid #0078d7;
#             border-radius: 3px;
#             color: black;
#             padding: 5px;
#         }
        
#         QComboBox:hover {
#             border-color: #429ce3;
#         }
        
#         QComboBox::drop-down {
#             border: none;
#         }
        
#         QComboBox::down-arrow {
#             image: url(assets/icons/down-arrow.png);
#             width: 12px;
#             height: 12px;
#         }
        
#         QLineEdit {
#             background-color: #ffffff;
#             border: 1px solid #0078d7;
#             border-radius: 3px;
#             color: black;
#             padding: 5px;
#         }
        
#         QLineEdit:hover {
#             border-color: #429ce3;
#         }
        
#         QLineEdit:focus {
#             border-color: #0078d7;
#             border-width: 2px;
#         }
        
#         QMenuBar {
#             background-color: #f0f0f0;
#             color: black;
#             border-bottom: 1px solid #d4d4d4;
#         }
        
#         QMenuBar::item {
#             padding: 5px 10px;
#             background: transparent;
#         }
        
#         QMenuBar::item:selected {
#             background-color: #0078d7;
#             color: white;
#         }
        
#         QMenu {
#             background-color: #ffffff;
#             border: 1px solid #d4d4d4;
#             padding: 5px 0px;
#         }
        
#         QMenu::item {
#             padding: 5px 30px;
#         }
        
#         QMenu::item:selected {
#             background-color: #0078d7;
#             color: white;
#         }
        
#         QWidget#Canvas {
#             background-color: #ffffff;
#             border: none;
#         }
        
#         /* Sidebar specific styles */
#         QDockWidget > QWidget {
#             background: #ffffff;
#         }
        
#         /* Node styles */
#         .node {
#             background-color: #ffffff;
#             border: 2px solid #0078d7;
#         }
        
#         .node:hover {
#             border-color: #429ce3;
#         }
        
#         /* Connection styles */
#         .connection-line {
#             color: #0078d7;
#         }
        
#         /* ScrollBar styles */
#         QScrollBar:vertical {
#             border: none;
#             background: #f0f0f0;
#             width: 10px;
#             margin: 0px;
#         }
        
#         QScrollBar::handle:vertical {
#             background: #c1c1c1;
#             min-height: 30px;
#             border-radius: 5px;
#         }
        
#         QScrollBar::handle:vertical:hover {
#             background: #a8a8a8;
#         }
        
#         QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
#             height: 0px;
#         }
        
#         /* Section headers */
#         .section-header {
#             background-color: #f5f5f5;
#             color: black;
#             padding: 5px;
#             font-weight: bold;
#         }
        
#         /* Tool tips */
#         QToolTip {
#             background-color: #ffffff;
#             border: 1px solid #d4d4d4;
#             color: black;
#             padding: 5px;
#         }
#     """

# def load_dark_theme():
#     # Your existing dark theme code remains unchanged
#     return """
#         ... (your existing dark theme code)
#     """

# def load_styles(theme="dark"):
#     if theme == "dark":
#         return load_dark_theme()
#     return load_light_theme()


# # utils/styles.py

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
        
        QComboBox {
            background-color: #2a2a2a;
            border: 1px solid #00ff00;
            border-radius: 3px;
            color: white;
            padding: 5px;
        }
        
        QComboBox:hover {
            border-color: #00ff99;
        }
        
        QLineEdit {
            background-color: #2a2a2a;
            border: 1px solid #00ff00;
            border-radius: 3px;
            color: white;
            padding: 5px;
        }
        
        QLineEdit:hover {
            border-color: #00ff99;
        }
        
        QMenuBar {
            background-color: #2a2a2a;
            color: white;
        }
        
        QMenuBar::item:selected {
            background-color: #3a3a3a;
        }
        
        QMenu {
            background-color: #2a2a2a;
            color: white;
        }
        
        QMenu::item:selected {
            background-color: #3a3a3a;
        }
    """

# def load_light_theme():
#     return """
#         QMainWindow {
#             background-color: #f0f0f0;
#         }
        
#         QDockWidget {
#             background-color: #ffffff;
#             border: none;
#             color: black;
#         }
        
#         QPushButton {
#             background-color: #ffffff;
#             border: 2px solid #0078d7;
#             border-radius: 5px;
#             color: black;
#             padding: 5px;
#         }
        
#         QPushButton:hover {
#             background-color: #e5f1fb;
#             border-color: #429ce3;
#         }
        
#         QLabel {
#             color: black;
#         }
        
#         QComboBox {
#             background-color: #ffffff;
#             border: 1px solid #0078d7;
#             border-radius: 3px;
#             color: black;
#             padding: 5px;
#         }
        
#         QComboBox:hover {
#             border-color: #429ce3;
#         }
        
#         QLineEdit {
#             background-color: #ffffff;
#             border: 1px solid #0078d7;
#             border-radius: 3px;
#             color: black;
#             padding: 5px;
#         }
        
#         QLineEdit:hover {
#             border-color: #429ce3;
#         }
        
#         QMenuBar {
#             background-color: #f0f0f0;
#             color: black;
#         }
        
#         QMenuBar::item:selected {
#             background-color: #0078d7;
#             color: white;
#         }
        
#         QMenu {
#             background-color: #ffffff;
#             color: black;
#         }
        
#         QMenu::item:selected {
#             background-color: #0078d7;
#             color: white;
#         }
#     """

# def load_styles(theme="dark"):
#     if theme == "dark":
#         return load_dark_theme()
#     return load_light_theme()

# # utils/styles.py

# def load_styles():
#     """Default style loading - uses dark theme by default"""
#     return load_dark_theme()

# def load_dark_theme():
#     return """
#         QMainWindow {
#             background-color: #1a1a1a;
#         }
        
#         QDockWidget {
#             background-color: #2a2a2a;
#             border: none;
#             color: white;
#         }
        
#         QPushButton {
#             background-color: #2a2a2a;
#             border: none;
#             color: white;
#             padding: 5px;
#         }
        
#         QPushButton:hover {
#             background-color: #3a3a3a;
#         }
        
#         QLabel {
#             color: white;
#         }
        
#         QComboBox {
#             background-color: #2a2a2a;
#             border: none;
#             color: white;
#             padding: 5px;
#         }
        
#         QComboBox:hover {
#             background-color: #3a3a3a;
#         }
        
#         QLineEdit {
#             background-color: #2a2a2a;
#             border: none;
#             color: white;
#             padding: 5px;
#         }
#     """

# def load_light_theme():
#     return """
#         QMainWindow {
#             background-color: #f0f0f0;
#         }
        
#         QDockWidget {
#             background-color: white;
#             border: none;
#             color: black;
#         }
        
#         QPushButton {
#             background-color: white;
#             border: 1px solid #dddddd;
#             color: black;
#             padding: 5px;
#         }
        
#         QPushButton:hover {
#             background-color: #f5f5f5;
#         }
        
#         QLabel {
#             color: black;
#         }
        
#         QComboBox {
#             background-color: white;
#             border: 1px solid #dddddd;
#             color: black;
#             padding: 5px;
#         }
        
#         QComboBox:hover {
#             background-color: #f5f5f5;
#         }
        
#         QLineEdit {
#             background-color: white;
#             border: 1px solid #dddddd;
#             color: black;
#             padding: 5px;
#         }
#     """

#     def get_light_theme():
#     return """
#         QMainWindow {
#             background-color: #f0f0f0;
#         }
        
#         QDockWidget {
#             background-color: #ffffff;
#             border: none;
#             color: black;
#         }
        
#         QPushButton {
#             background-color: #ffffff;
#             border: 2px solid #0078d7;
#             border-radius: 5px;
#             color: black;
#             padding: 5px;
#         }
        
#         QPushButton:hover {
#             background-color: #e5f1fb;
#             border-color: #429ce3;
#         }
        
#         QLabel {
#             color: black;
#         }
        
#         QComboBox {
#             background-color: #ffffff;
#             border: 1px solid #0078d7;
#             border-radius: 3px;
#             color: black;
#             padding: 5px;
#         }
        
#         QComboBox:hover {
#             border-color: #429ce3;
#         }
        
#         QLineEdit {
#             background-color: #ffffff;
#             border: 1px solid #0078d7;
#             border-radius: 3px;
#             color: black;
#             padding: 5px;
#         }
        
#         QLineEdit:hover {
#             border-color: #429ce3;
#         }
        
#         QWidget#Canvas {
#             background-color: #ffffff;
#         }

#         /* Custom properties for node states */
#         .node {
#             background-color: #ffffff;
#             border: 2px solid #000000;
#         }
        
#         .node-connecting {
#             border: 2px solid #0078d7;
#         }
        
#         .connection-data {
#             color: #0078d7;
#         }
        
#         .connection-control {
#             color: #7b2f93;
#         }
        
#         .connection-event {
#             color: #825b00;
#         }
#     """

# def get_dark_theme():
#     return """
#         /* Your existing dark theme styles */
#     """

# def load_styles(theme="dark"):
#     return get_dark_theme() if theme == "dark" else get_light_theme()