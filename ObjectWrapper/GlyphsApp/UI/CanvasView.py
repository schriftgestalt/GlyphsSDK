# -*- coding: utf-8 -*-

from __future__ import print_function

__all__ = ["CanvasView"]

import traceback
from vanilla import Group
from AppKit import NSView, NSRectFill, NSColor


class CanvasView_view(NSView):
	
	def drawRect_(self, rect):
		try:
			if self._backgroundColor is not None:
				self._backgroundColor.set()
				NSRectFill(rect)
			if self._delegate != None:
				self._delegate.draw(self)
		except:
			print(traceback.format_exc())
	def mouseDown_(self, event):
		try:
			if self._delegate != None and hasattr(self._delegate, "mouseDown"):
				self._delegate.mouseDown(event)
		except:
			print(traceback.format_exc())
	def mouseDragged_(self, event):
		try:
			if self._delegate != None and hasattr(self._delegate, "mouseDragged"):
				self._delegate.mouseDragged(event)
		except:
			print(traceback.format_exc())
	def mouseUp_(self, event):
		try:
			if self._delegate != None and hasattr(self._delegate, "mouseUp"):
				self._delegate.mouseUp(event)
		except:
			print(traceback.format_exc())

class CanvasView(Group):
	
	'''
	A vanilla object that can be used to draw anything.
	
	from AppKit import *
	from vanilla import *
	from GlyphsApp.UI import *
	class CanvasViewDemo(object):
		def __init__(self):
			self.w = Window((150, 150))
			self.w.group = CanvasView((10, 10, -10, -10), self)
			self.w.open()
	
		def draw(self, view):
			bounds = view.bounds()
			NSColor.greenColor().set()
			NSRectFill(bounds)

	CanvasViewDemo()
	
	'''
	
	version = "1.0"
	nsViewClass = CanvasView_view
	
	def __init__(self, posSize, delegate, backgroundColor=None):
		self._setupView(self.nsViewClass, posSize)
		self.delegate = delegate
		self._nsObject._backgroundColor = backgroundColor
	
	def _get_delegate(self):
		return self.view._delegate
	def _set_delegate(self, delegate):
		self._nsObject._delegate = delegate
		self._nsObject.setNeedsDisplay_(True)
	delegate = property(_get_delegate, _set_delegate)
	
	def update(self):
		self._nsObject.setNeedsDisplay_(True)
