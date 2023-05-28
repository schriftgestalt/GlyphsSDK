# encoding: utf-8

import objc
from GlyphsApp import Glyphs, GSNode, Message
from GlyphsApp.plugins import SelectTool

class MySelectTool(SelectTool):
	
	inspectorDialogView = objc.IBOutlet()
	button = objc.IBOutlet()

	def settings(self):
		self.name = Glyphs.localize({'en': 'My Select Tool', 'de': 'Mein Auswahlwerkzeug'})

		# Load .nib file from package (without .extension)
		self.loadNib("InspectorView", self.__file__())

	# Return a GSInspectorView (not a Group) when needed
	def view(self):
		# This this is just sample code. Change that to your own conditions
		layer = self.editViewController().graphicView().activeLayer()
		if layer is not None and len(layer.selection) == 1 and isinstance(layer.selection[0], GSNode):
			return self.inspectorDialogView
		return None

	@objc.IBAction
	def buttonCallback_(self, sender):
		Message("Action", "You have clicked the button")

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__