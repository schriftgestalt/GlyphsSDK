from __future__ import print_function

__all__ = ["GlyphView"]

import traceback

from AppKit import NSColor, NSRectFill, NSView
from vanilla import Group

from GlyphsApp import GSLayer


class GlyphView_view(NSView):
	_layer: GSLayer | None
	_backgroundColor: NSColor | None
	_foregroundColor: NSColor | None

	def drawRect_(self, rect):
		try:
			bounds = self.bounds()
			if self._backgroundColor is not None:
				self._backgroundColor.set()
				NSRectFill(bounds)
			if self._layer is not None:
				self._layer.drawInFrame_metrics_color_dark_(bounds, self._layer.glyphMetrics(), self._foregroundColor or NSColor.blackColor(), False)
		except:
			print(traceback.format_exc())


class GlyphView(Group):
	'''
	A vanilla object that displays a GSLayer

	from vanilla import Window
	from GlyphsApp.UI import GlyphView
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
	_nsObject: GlyphView_view

	def __init__(self, posSize, layer=None, backgroundColor=None, foregroundColor=NSColor.textColor()):
		self._setupView(self.nsViewClass, posSize)
		self.layer = layer
		self.backgroundColor = backgroundColor if backgroundColor is not None else NSColor.textBackgroundColor()
		self.foregroundColor = foregroundColor if foregroundColor is not None else NSColor.textColor()

	def _get_layer(self):
		return self._nsObject._layer

	def _set_layer(self, layer):
		self._nsObject._layer = layer
		self._nsObject.setNeedsDisplay_(True)

	layer = property(_get_layer, _set_layer)

	def _get_backgroundColor(self):
		return self._nsObject._backgroundColor

	def _set_backgroundColor(self, backgroundColor):
		self._nsObject._backgroundColor = backgroundColor
		self._nsObject.setNeedsDisplay_(True)

	backgroundColor = property(_get_backgroundColor, _set_backgroundColor)

	def _get_foregroundColor(self):
		return self._nsObject._foregroundColor

	def _set_foregroundColor(self, foregroundColor):
		self._nsObject._foregroundColor = foregroundColor
		self._nsObject.setNeedsDisplay_(True)

	foregroundColor = property(_get_foregroundColor, _set_foregroundColor)
