# -*- coding: utf-8 -*-

__all__ = ["GlyphPreview"]

import traceback
from typing import Tuple, cast

from AppKit import NSColor, NSGraphicsContext, NSRectFill, NSView
from Foundation import NSAffineTransform
from vanilla.vanillaBase import VanillaBaseObject

from GlyphsApp import GSLayer


class GSGlyphPreviewView(NSView):

	_transformation: NSAffineTransform | None = None
	_layer: GSLayer

	@property
	def layer(self):
		return self._layer

	@layer.setter
	def layer(self, layer):
		assert isinstance(layer, GSLayer)
		self._layer = layer

	def setDelegate_(self, delegate):
		self._delegate = delegate

	def drawRect_(self, rect):
		frame = self.bounds()
		NSColor.whiteColor().set()
		NSRectFill(frame)
		try:
			if self._transformation:
				NSGraphicsContext.saveGraphicsState()
				self._transformation.concat()
			if self._layer is not None:
				self._layer.drawInFrame_(frame)
		except:
			print(traceback.format_exc())
		finally:
			if self._transformation:
				NSGraphicsContext.restoreGraphicsState()

	def mouseDown_(self, event):
		try:
			if event.clickCount() == 2:
				if self._delegate.mouseDoubleDownCallBack:
					self._delegate.mouseDoubleDownCallBack(self)
				return
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

	GlyphPreview objects handle GSLayer

		from vanilla import FloatingWindow
		from GlyphsApp.UI import GlyphPreview
		class GlyphPreviewDemo(object):
			def __init__(self):
				self.title = "Glyph Preview"
				self.w = FloatingWindow((200, 200), self.title)
				layer = Glyphs.font.selectedLayers[0]
				self.w.Preview = GlyphPreview((0, 0, 0, 0), layer=layer)
				self.w.Preview.mouseDoubleDownCallBack = self.mouseDoubleDown
				self.w.open()
			def mouseDoubleDown(self, sender):
				print("Mouse Double Down")

		GlyphPreviewDemo()

	**posSize** Tuple of form *(left, top, width, height)* representing the position and size of the color well.

	**layer** A *GSLayer*. If *None* is given, the view will be empty.
	"""

	nsGlyphPreviewClass = GSGlyphPreviewView

	def __init__(self, posSize: Tuple, layer: GSLayer | None = None) -> None:
		self.mouseDownCallBack = None
		self.mouseDoubleDownCallBack = None
		self.mouseUpCallBack = None
		self._setupView(self.nsGlyphPreviewClass, posSize)
		view: GSGlyphPreviewView = cast(GSGlyphPreviewView, self._nsObject)
		view.setDelegate_(self)
		view.layer = layer

	@property
	def layer(self) -> GSLayer:
		view: GSGlyphPreviewView = cast(GSGlyphPreviewView, self._nsObject)
		return view.layer

	@layer.setter
	def layer(self, value: GSLayer) -> None:
		view: GSGlyphPreviewView = cast(GSGlyphPreviewView, self._nsObject)
		view.layer = value
		self._nsObject.setNeedsDisplay_(True)

	@property
	def transformation(self) -> NSAffineTransform | None:
		view: GSGlyphPreviewView = cast(GSGlyphPreviewView, self._nsObject)
		return view._transformation

	@transformation.setter
	def transformation(self, value: NSAffineTransform) -> None:
		assert isinstance(value, NSAffineTransform)
		view: GSGlyphPreviewView = cast(GSGlyphPreviewView, self._nsObject)
		view._transformation = value
		self._nsObject.setNeedsDisplay_(True)
