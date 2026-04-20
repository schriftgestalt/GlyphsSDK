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
from GlyphsApp import Glyphs, GSFont, GSCallbackHandler, GSGlyphsInfo, GSInstance
from GlyphsApp.plugins import GeneralPlugin
from mekkaKernFlattener import subsetKerning


MekkablueKernTableSubsetterKey = "Mekkablue kern table subsetter"

class KernTableSubsetter(GeneralPlugin):

	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({
			'en': 'Kern Table Subsetter',
		})
		GSCallbackHandler.addCallback_forOperation_(self, "GSFilterFlatKerning")
		try:  # some imaginary future API
			GSGlyphsInfo.addDescription_forParameter_("Apply mekkablue kern table subsetter. This is only applied when the \"Export kern Table\" parameter is set, too", MekkablueKernTableSubsetterKey)
			GSGlyphsInfo.addType_forParameter_forClass_(True, MekkablueKernTableSubsetterKey, GSInstance.__class__)
		except:
			pass

	@objc.python_method
	def start(self):
		pass

	@objc.typedSelector(b'@@:@@o^@')
	def filterFlatKerning_font_error_(self, kerning: list, font: GSFont, error=None):
		"""Do something like show a window """

		instance = font.instances[0]
		parameter = instance.customValueForKey_(MekkablueKernTableSubsetterKey)

		if parameter and int(parameter):  # subset if parameter is set, otherwise return the original list
			kerning = subsetKerning(kerning, font)
		return kerning, None

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
