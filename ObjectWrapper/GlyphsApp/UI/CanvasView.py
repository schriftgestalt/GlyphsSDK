from __future__ import print_function

__all__ = ["CanvasView"]

import traceback
from typing import Any, Tuple, Type, cast

from AppKit import NSColor, NSRectFill, NSView
from vanilla import Group


class CanvasView_view(NSView):

	_backgroundColor: NSColor | None
	_delegate: Any | None

	def drawRect_(self, rect):
		try:
			if self._backgroundColor is not None:
				self._backgroundColor.set()
				NSRectFill(rect)
			if self._delegate is not None:
				self._delegate.draw(self)
		except:
			print(traceback.format_exc())

	def mouseDown_(self, event):
		try:
			if self._delegate is not None and hasattr(self._delegate, "mouseDown"):
				self._delegate.mouseDown(event)
		except:
			print(traceback.format_exc())

	def mouseDragged_(self, event):
		try:
			if self._delegate is not None and hasattr(self._delegate, "mouseDragged"):
				self._delegate.mouseDragged(event)
		except:
			print(traceback.format_exc())

	def mouseUp_(self, event):
		try:
			if self._delegate is not None and hasattr(self._delegate, "mouseUp"):
				self._delegate.mouseUp(event)
		except:
			print(traceback.format_exc())


class CanvasView(Group):
	'''
	A vanilla object that can be used to draw anything.

	from AppKit import NSColor, NSRectFill
	from vanilla import Window
	from GlyphsApp.UI import CanvasView
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
	nsViewClass: Type[NSView] = CanvasView_view

	def __init__(self, posSize: Tuple, delegate: Any, backgroundColor: NSColor | None = None):
		self._setupView(self.nsViewClass, posSize)
		self.delegate = delegate
		view: CanvasView_view = cast(CanvasView_view, self._nsObject)
		view._backgroundColor = backgroundColor

	def _get_delegate(self) -> Any | None:
		view: CanvasView_view = cast(CanvasView_view, self._nsObject)
		return view._delegate

	def _set_delegate(self, delegate: Any) -> None:
		view: CanvasView_view = cast(CanvasView_view, self._nsObject)
		view._delegate = delegate
		view.setNeedsDisplay_(True)

	delegate = property(_get_delegate, _set_delegate)

	def update(self):
		self._nsObject.setNeedsDisplay_(True)
