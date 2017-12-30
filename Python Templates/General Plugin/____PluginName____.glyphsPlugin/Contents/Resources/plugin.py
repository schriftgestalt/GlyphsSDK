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

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class ____PluginClassName____(GeneralPlugin):
	def settings(self):
		self.name = Glyphs.localize({'en': u'My General Plugin', 'de': u'Mein allgemeines Plugin'})
	
	def start(self):
		try: 
			# new API in Glyphs 2.3.1-910
			newMenuItem = NSMenuItem(self.name, self.showWindow)
			Glyphs.menu[EDIT_MENU].append(newMenuItem)
		except:
			mainMenu = Glyphs.mainMenu()
			s = objc.selector(self.showWindow,signature='v@:@')
			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name, s, "")
			newMenuItem.setTarget_(self)
			mainMenu.itemWithTag_(5).submenu().addItem_(newMenuItem)
	
	def showWindow(self, sender):
		""" Do something like show a window"""
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	