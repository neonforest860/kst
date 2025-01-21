# custom_widgets.py
from PyQt6 import QtDesigner
from components.canvas import Canvas

# This allows the Canvas widget to be promoted in Designer
class CanvasPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    def __init__(self):
        super().__init__()
        self.initialized = False

    def initialize(self, core):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return Canvas(parent)

    def name(self):
        return "Canvas"

    def group(self):
        return "Custom Widgets"

    def icon(self):
        return QtGui.QIcon()

    def toolTip(self):
        return "Network Designer Canvas Widget"

    def whatsThis(self):
        return "A canvas widget for network design"

    def isContainer(self):
        return False

    def domXml(self):
        return '<widget class="Canvas" name="canvas">\n' \
               ' <property name="toolTip" >\n' \
               '  <string>Network Designer Canvas</string>\n' \
               ' </property>\n' \
               '</widget>\n'

    def includeFile(self):
        return "custom_widgets"