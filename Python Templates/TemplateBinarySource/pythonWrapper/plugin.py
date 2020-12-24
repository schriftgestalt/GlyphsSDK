# encoding: utf-8
from __future__ import division, print_function, unicode_literals

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

class TestPY(GeneralPlugin):

	@objc.python_method
	def settings(self):
		print("__settings", self.name, __file__)
		self.name = "TéstPy"

	@objc.python_method
	def start(self):
		newMenuItem = NSMenuItem(self.name, self.showWindow_)
		Glyphs.menu[EDIT_MENU].append(newMenuItem)

	def showWindow_(self, sender):
		""" Do something like show a window"""
		print(self.name, __file__)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return(__file__)
