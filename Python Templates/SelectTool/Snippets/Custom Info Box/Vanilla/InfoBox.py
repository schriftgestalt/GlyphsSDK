# encoding: utf-8

from GlyphsApp.plugins import *
from vanilla import Window, Group, Button

# Our own patched Vanilla Group class
GSInspectorView = objc.lookUpClass("GSInspectorView")
class InspectorGroup(Group):
	nsViewClass = GSInspectorView

class MySelectTool(SelectTool):

	def settings(self):
		self.name = 'My Select Tool'

		# Create Vanilla window and group with controls
		self.infoBoxWindow = Window((viewWidth, viewHeight))
		# Using InspectorGroup() here instead of Group()
		self.infoBoxWindow.group = InspectorGroup("auto")
		self.infoBoxWindow.group.button = Button("auto", "Move", callback=self.buttonCallback_)
		rules = [
			"H:|-8-[button]-8-|",
			"V:|-10-[button]-10-|",
		]
		self.infoBoxWindow.group.addAutoPosSizeRules(rules)
		self.infoBoxView = self.infoBoxWindow.group.getNSView()
		self.inspectorDialogView = True
	
	# Return a GSInspectorView (not a Group) when needed
	def view(self):
		# This this is just sample code. Change that to your own conditions
		layer = self.editViewController().graphicView().activeLayer()
		if layer is not None and len(layer.selection) == 1 and isinstance(layer.selection[0], GSNode):
			return self.infoBoxView
		return None

	# Prints the slider’s value
	def buttonCallback_(self, sender):
		print('Button:', sender.get())