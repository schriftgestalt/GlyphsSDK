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


from GlyphsApp.plugins import *

class SmileyPalette (PalettePlugin):
	_theView = objc.IBOutlet()
	_theImageView = objc.IBOutlet()

	def settings(self):
		"""
		Do all initializing here.
		"""
		try:
			self.controller = None
			self.loadNib('SmileyPaletteView', __file__)
			Glyphs.addCallback(self.update, UPDATEINTERFACE)
		except Exception as e:
			self.logError(traceback.format_exc())
	
	def start(self):
		# Adding a callback for the 'GSUpdateInterface' event
		Glyphs.addCallback(self.update, UPDATEINTERFACE)
	
	def __del__(self):
		# remove the callback
		Glyphs.removeCallback(self.update)
	
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
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__