from typing import cast

from AppKit import NSURLRequest
from Foundation import NSURL
from vanilla.vanillaBase import VanillaBaseObject
from WebKit import WKWebView

__all__ = ["HTMLView"]


class HTMLView(VanillaBaseObject):
	"""
	A view that allows for showing HTML via WKWebView

	from vanilla import FloatingWindow
	from Glyphs.UI import HTMLView
	class HTMLViewDemo(object):
		def __init__(self):
			self.title = "HTML View"
			self.w = FloatingWindow((600, 350), self.title)
			self.w.Preview = HTMLView((0, 0, 0, 0))
			self.w.Preview.setHTMLPath("https://www.glyphsapp.com")
			self.w.open()
	HTMLViewDemo()

	**posSize** Tuple of form *(left, top, width, height)*.
	"""
	nsHTMLViewClass = WKWebView

	def __init__(self, posSize):
		self._setupView(self.nsHTMLViewClass, posSize)
		# you can still set a delegate if needed:
		# self._nsObject.navigationDelegate = self

	def setHTMLPath(self, path):
		if path:
			url = NSURL.URLWithString_(path)
			req = NSURLRequest.requestWithURL_(url)
			webview = cast(WKWebView, self._nsObject)
			webview.loadRequest_(req)
