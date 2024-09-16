# encoding: utf-8

###########################################################################################################
#
#
# General Plugin
#
# Read the docs:
# https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import Glyphs, EDIT_MENU
from GlyphsApp.plugins import GeneralPlugin
from AppKit import NSMenuItem


class ____PluginClassName____(GeneralPlugin):

	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({
			'en': 'My General Plug-in',
			'de': 'Mein allgemeines Plug-in',
			'fr': 'Ma extension générale',
			'es': 'Mi plugin general',
			'pt': 'Meu plug-in geral',
		})

	@objc.python_method
	def start(self):
		if Glyphs.versionNumber >= 3.3:
			newMenuItem = NSMenuItem(self.name, callback=self.showWindow_, target=self)
		else:
			newMenuItem = NSMenuItem(self.name, self.showWindow_)
		Glyphs.menu[EDIT_MENU].append(newMenuItem)

	def showWindow_(self, sender):
		"""Do something like show a window """
		print("show Windows")

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
