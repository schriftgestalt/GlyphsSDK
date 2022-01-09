# encoding: utf-8

###########################################################################################################
#
#
#	Palette Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class ____PluginClassName____ (PalettePlugin):
	
	dialog = objc.IBOutlet()
	textField = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({
			'en': 'My Palette',
			'de': 'Meine Palette',
			'fr': 'Ma palette',
			'es': 'Mi panel',
			'pt': 'Meu painel',
			})
		
		# Load .nib dialog (without .extension)
		self.loadNib('IBdialog', __file__)

	@objc.python_method
	def start(self):
		# Adding a callback for the 'GSUpdateInterface' event
		Glyphs.addCallback(self.update, UPDATEINTERFACE)

	@objc.python_method	
	def __del__(self):
		Glyphs.removeCallback(self.update)

	@objc.python_method
	def update(self, sender):
		
		text = []
		# Extract font from sender
		currentTab = sender.object()
		# We’re in the Edit View
		if isinstance(currentTab, GSEditViewController):
			# Check whether glyph is being edited
			layer = currentTab.activeLayer()
			if layer is not None:
				text.append('Selected nodes: %s' % len(layer.selection))
				if layer.selection:
					text.append('Selection bounds: %sx%s' % (int(layer.selectionBounds.size.width), int(layer.selectionBounds.size.height)))

		# We’re in the Font view
		else:
			try:
				text.append('Selected glyphs: %s' % len(currentTab.selectedLayers))
			except:
				pass

		# Send text to dialog to display
		self.textField.setStringValue_('\n'.join(text))

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
