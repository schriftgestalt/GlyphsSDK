# encoding: utf-8

###########################################################################################################
#
#
#	Smiley Palette Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Samples/Smiley%20Panel%20Plugin
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
from GlyphsApp import *
from GlyphsApp.plugins import *

class SmileyPalette (PalettePlugin):
	_theView = objc.IBOutlet()
	_theImageView = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		"""
		Do all initializing here.
		"""
		self.controller = None
		self.loadNib('SmileyPaletteView', __file__)

		self.dialog = self._theView
		Glyphs.addCallback(self.update, UPDATEINTERFACE)

	@objc.python_method
	def start(self):
		# Adding a callback for the 'GSUpdateInterface' event
		Glyphs.addCallback(self.update, UPDATEINTERFACE)

	@objc.python_method	
	def __del__(self):
		# remove the callback
		Glyphs.removeCallback(self.update)

	@objc.python_method
	def update(self, sender):
		"""
		Called from the notificationCenter if the info in the current Glyph window has changed.
		This can be called quite a lot, so keep this method fast.
		"""
		try:
			Layer = self.windowController().activeLayer()
			if Layer:
				self._theImageView.setHidden_(False)
			else:
				self._theImageView.setHidden_(True)
		except Exception as e:
			self.logError(traceback.format_exc())

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
