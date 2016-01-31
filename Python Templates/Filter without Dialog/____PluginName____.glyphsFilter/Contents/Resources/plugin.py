# encoding: utf-8

###########################################################################################################
#
#
#	Filter without dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20without%20Dialog
#
#
###########################################################################################################


from GlyphsApp.plugins import *

class ____PluginClassName____(FilterWithoutDialog):
	
	def settings(self):
		self.menuName = Glyphs.localize({'en': u'My Filter', 'de': u'Mein Filter'})
		self.keyboardShortcut = None # With Cmd+Shift

	def filter(self, layer, inEditView, customParameters):
		
		# Apply your filter code here
		
		print layer, inEditView, customParameters
