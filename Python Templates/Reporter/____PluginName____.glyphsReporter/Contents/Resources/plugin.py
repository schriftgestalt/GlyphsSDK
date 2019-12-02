# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class ____PluginClassName____(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({'en': u'My Plugin', 'de': u'Mein Plugin'})
		self.generalContextMenus = [
			{'name': Glyphs.localize({'en': u'Do something', 'de': u'Tu etwas'}), 'action': self.doSomething},
		]
	
	@objc.python_method
	def foreground(self, layer):
		NSColor.blueColor().set()
		NSBezierPath.fillRect_(layer.bounds)
		self.drawTextAtPoint(layer.parent.name, NSPoint(0, 0))
	
	@objc.python_method
	def inactiveLayer(self, layer):
		NSColor.redColor().set()
		if layer.paths:
			layer.bezierPath.fill()
		if layer.components:
			for component in layer.components:
				component.bezierPath.fill()
	
	@objc.python_method
	def preview(self, layer):
		NSColor.blueColor().set()
		if layer.paths:
			layer.bezierPath.fill()
		if layer.components:
			for component in layer.components:
				component.bezierPath.fill()
	
	@objc.python_method
	def doSomething(self):
		print('Just did something')
	
	@objc.python_method
	def conditionalContextMenus(self):

		# Empty list of context menu items
		contextMenus = []

		# Execute only if layers are actually selected
		if Glyphs.font.selectedLayers:
			layer = Glyphs.font.selectedLayers[0]
			
			# Exactly one object is selected and it’s an anchor
			if len(layer.selection) == 1 and type(layer.selection[0]) == GSAnchor:
					
				# Add context menu item
				contextMenus.append({'name': Glyphs.localize({'en': u'Do something else', 'de': u'Tu etwas anderes'}), 'action': self.doSomethingElse})

		# Return list of context menu items
		return contextMenus
	
	@objc.python_method
	def doSomethingElse(self):
		print('Just did something else')
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
