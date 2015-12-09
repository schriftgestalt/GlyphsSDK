# encoding: utf-8


from plugins import *
from AppKit import *



class ____PluginClassName____(ReporterPlugin):

	def loadPlugin(self):
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
