from pcbnew import *
import os

class SimplePlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "PcbPlotVisualiser"
        self.category = ""
        self.description = "Outputs simple"
        self.show_toolbar_button = False
       # self.icon_file_name = os.path.join(os.path.dirname(__file__), 'simple_plugin.png') # Optional, defaults to ""

    def Run(self):
        # The entry function of the plugin that is executed on user action
        print("Hello World")
