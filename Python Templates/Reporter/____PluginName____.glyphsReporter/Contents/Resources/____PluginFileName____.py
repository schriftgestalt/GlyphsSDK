# encoding: utf-8


from plugin import *
from AppKit import *



class ____PluginClassName____(ReporterPlugin):

	def settings(self):
		self.menuName = 'My Plugin'
		
	def drawForeground(self, layer):
		NSColor.blueColor().set()
		NSBezierPath.fillRect_(layer.bounds)
		self.drawTextAtPoint(layer.parent.name, NSPoint(0, 0))

	def drawBackgroundForInactiveLayers(self, layer):
		NSColor.redColor().set()
		if layer.paths:
			layer.bezierPath().fill()
		if layer.components:
			for component in layer.components:
				component.bezierPath().fill()

	def drawPreview(self, layer):
		NSColor.blueColor().set()
		layer.bezierPath().fill()
	
	def contextmenuEntries(event):
		'''
		return a list of tuples
		(Text, Method Name, target, index)
		The index in the menu. It might be -1, then the item will be added to the end of the menu.
		'''
		return [("Do Something", "doSomething", self, 0)]
	
	def doSomething(self):
		pass