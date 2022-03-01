# encoding: utf-8

###########################################################################################################
#
#
#	General Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
import traceback


class PluginWithWindow(GeneralPlugin):

	"""
	A GeneralPlugin has no windowcontroller.
	The panel plugin does have it (as there is an instance of the
	plugin per window).
	The GeneralPlugin needs to get to the windows by
	[NSApp mainWindow], [NSApp currentFontDocument] or [NSApp orderedDocuments].
	"""

	windowName = "com.Glyphs.PluginWithWindowWindow"
	window = objc.IBOutlet()
	fontNameLabel = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({
			'en': 'Plugin with Window',
			'de': 'Plug-in mit Fenster',
			'fr': 'Extension avec fenêtre',
			'es': 'Plugin con ventana',
			})
		self.loadNib("MyPluginWindow", __file__) # Load .nib file next to plugin.py
		self.window.setTitle_(self.name)
		self.window.setFrameAutosaveName_(self.windowName)
		self.fontNameLabel.setStringValue_("No Font Open")

	@objc.python_method
	def start(self):
		newMenuItem = NSMenuItem(self.name, self.showWindow_)
		Glyphs.menu[WINDOW_MENU].append(newMenuItem)

	def showWindow_(self, sender):
		self.window.makeKeyAndOrderFront_(self) # Show the window
		
		Glyphs.addCallback(self.update, DOCUMENTACTIVATED) # Add a callback for the 'GSUpdateInterface' event

		self.update(None) # Update once when window is shown

	@objc.python_method
	def update(self, sender):
		try:
			thisFont = Glyphs.currentDocument.font
			if thisFont:
				self.fontNameLabel.setStringValue_(thisFont.familyName) # Update the font name label
		except:
			print(traceback.format_exc())

	@objc.python_method	
	def __del__(self):
		Glyphs.removeCallback(self.update) # Remove the callback

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__

	def windowShouldClose_(self, window):
		Glyphs.removeCallback(self.update) # Remove callbacks when the window is closed
		return True
		