# -*- coding: utf-8 -*-

__all__ = ["GlyphView"]


import traceback
from vanilla import Group
from AppKit import NSView, NSColor, NSRectFill
from GlyphsApp import Glyphs


class GlyphView_view(NSView):
	
	def drawRect_(self, rect):
		try:
			bounds = self.bounds()
			if self._backgroundColor != None:
				self._backgroundColor.set()
				NSRectFill(bounds)
			self._layer.drawInFrame_(bounds)
		except:
			print traceback.format_exc()

class GlyphView(Group):
	
	'''
	A vanilla object that displays a GSLayer
	
	from vanilla import *
	from GlyphsApp.UI import *
	class GlyphViewDemo(object):
		def __init__(self):
			self.w = Window((150, 150))
			l = Font.selectedLayers[0]
			self.w.group = GlyphView((10, 10, -10, -10), layer = l)
			self.w.open()

	GlyphViewDemo()
	
	'''
	
	version = "1.0"
	nsViewClass = GlyphView_view
	
	def __init__(self, posSize, layer = None, backgroundColor = None):
		self._setupView(self.nsViewClass, posSize)
		self.layer = layer
		if backgroundColor != None:
			self.backgroundColor = backgroundColor
		else:
			self.backgroundColor = NSColor.whiteColor()
	
	def _get_layer(self):
		return self.view._layer
	def _set_layer(self, layer):
		self._nsObject._layer = layer
		self._nsObject.setNeedsDisplay_(True)
	layer = property(_get_layer, _set_layer)
	
	def _get_backgroundColor(self):
		return self.view._backgroundColor
	def _set_backgroundColor(self, backgroundColor):
		self._nsObject._backgroundColor = backgroundColor
		self._nsObject.setNeedsDisplay_(True)
	backgroundColor = property(_get_backgroundColor, _set_backgroundColor)
