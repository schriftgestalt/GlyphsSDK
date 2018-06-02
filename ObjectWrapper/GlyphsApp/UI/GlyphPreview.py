# -*- coding: utf-8 -*-

from __future__ import print_function

__all__ = ["GlyphView"]

import traceback
from vanilla import Group
from AppKit import NSView, NSColor, NSRectFill
from vanilla.vanillaBase import VanillaBaseObject


class GlyphPreviewView(NSView):
	def setGlyph_(self, glyph):
		self._glyph = glyph
	def setDelegate_(self, delegate):
		self._delegate = delegate
	def drawRect_(self, rect):
		frame = self.frame()
		NSColor.whiteColor().set()
		NSRectFill(frame)
		try:
			if self._glyph is not None:
				if self._glyph.__class__.__name__ in ("NSKVONotifying_GSLayer", "GSLayer"):
					layer = self._glyph
				elif isinstance(self._glyph, RGlyph):
					layer = self._glyph._layer
				if layer:
					layer.drawInFrame_(frame)
		except:
			print(traceback.format_exc())
	def mouseDown_(self, event):
		try:
			if event.clickCount() == 2:
				if self._delegate.mouseDoubleDownCallBack:
					self._delegate.mouseDoubleDownCallBack(self)
				return;
			if self._delegate.mouseDownCallBack:
				self._delegate.mouseDownCallBack(self)
		except:
			print(traceback.format_exc())
	def mouseUp_(self, event):
		try:
			if self._delegate.mouseUpCallBack:
				self._delegate.mouseUpCallBack(self)
		except:
			print(traceback.format_exc())

class GlyphPreview(VanillaBaseObject):

	"""
	A control that allows for showing a glyph

	GlyphPreview objects handle GSLayer or RGlyph
		from vanilla import *
		from objectsGS import GlyphPreview
		class GlyphPreviewDemo(object):
			def __init__(self):
				self.title = "Glyph Preview"
				self.w = FloatingWindow((200, 200), self.title, closable=False)
				glyph = Glyphs.font.selectedLayers[0]
				self.w.Preview = GlyphPreview((0, 0, 0, 0), glyph=glyph)
				self.w.Preview.mouseDoubleDownCallBack = self.mouseDoubleDown
				self.w.open()
			def mouseDoubleDown(self, sender):
				print "Mouse Double Down"
		
		GlyphPreviewDemo()

	**posSize** Tuple of form *(left, top, width, height)* representing the position and size of the color well.

	**glyph** A *GSLayer* or a *RGlyph* object. If *None* is given, the view will be white.
	"""

	nsGlyphPreviewClass = GlyphPreviewView

	def __init__(self, posSize, glyph=None):
		self.mouseDownCallBack = None
		self.mouseDoubleDownCallBack = None
		self.mouseUpCallBack = None
		self._setupView(self.nsGlyphPreviewClass, posSize)
		self._nsObject.setDelegate_(self)
		self._nsObject.setGlyph_(glyph)