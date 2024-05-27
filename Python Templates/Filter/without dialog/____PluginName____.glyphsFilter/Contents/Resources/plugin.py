# encoding: utf-8

###########################################################################################################
#
#
# Filter without dialog plug-in
#
# Read the docs:
# https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20without%20Dialog
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import Glyphs
from GlyphsApp.plugins import FilterWithoutDialog


class ____PluginClassName____(FilterWithoutDialog):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'My Filter',
			'de': 'Mein Filter',
			'fr': 'Mon filtre',
			'es': 'Mi filtro',
			'pt': 'Meu filtro',
			'jp': '私のフィルター',
			'ko': '내 필터',
			'zh': '我的过滤器',
		})

	@objc.python_method
	def filter(self, layer, inEditView, customParameters):

		# Apply your filter code here
		print(layer, inEditView, customParameters)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
