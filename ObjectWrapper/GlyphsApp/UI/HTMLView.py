# -*- coding: utf-8 -*-

from __future__ import print_function

__all__ = ["HTMLView"]

from WebKit import WebView
from vanilla.vanillaBase import VanillaBaseObject

class HTMLView(VanillaBaseObject):
	"""
	A view that allows for showing HTML
	
	from vanilla import *
	from objectsGS import HTMLView
	class HTMLViewDemo(object):
		def __init__(self):
			self.title = "HTML View"
			self.w = FloatingWindow((600, 350), self.title)
			self.w.Preview = HTMLView((0, 0, 0, 0))
			self.w.Preview.setHTMLPath("https://www.glyphsapp.com")
			self.w.open()
	HTMLViewDemo()

	**posSize** Tuple of form *(left, top, width, height)* representing the position and size of the color well.
	"""
	nsHTMLViewClass = WebView
	def __init__(self, posSize):
		self._setupView(self.nsHTMLViewClass, posSize)
		#self._nsObject.setDelegate_(self)
	def setHTMLPath(self, path):
		if (path):
			self._nsObject.setMainFrameURL_(path)