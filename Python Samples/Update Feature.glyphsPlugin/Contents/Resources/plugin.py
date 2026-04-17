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

import objc
from GlyphsApp import GSCallbackHandler, GSFeaturePrefix, GSClass, GSFeature, GSFont
from GlyphsApp.plugins import GeneralPlugin

GSFeatureCodeGeneratorProtocol = objc.protocolNamed("GSFeatureCodeGeneratorProtocol")

class MyUpdateFeature(GeneralPlugin):
	__pyobjc_protocols__ = [GSFeatureCodeGeneratorProtocol]

	@classmethod
	def title(cls):
		return "My Feature Code"

	@objc.python_method
	def settings(self):
		pass

	@objc.python_method
	def start(self):
		GSCallbackHandler.addFeatureCodeGenerator_(MyUpdateFeature)

	@classmethod
	def featureCodeForFeature_font_error_(cls, feature: GSFeature, font: GSFont, error):
		print("__", feature)
		if feature.name == "liga":
			feature.code += "\n# Hallo"

		return (True, None)

	@classmethod
	def featureCodeForClass_font_error_(cls, aClass: GSClass, font: GSFont, error):
		if aClass.name == "Uppercase":
			aClass.code += "\n# Hallo"

		return (True, None)

	@classmethod
	def featureCodeForPrefix_font_error_(cls, prefix: GSFeaturePrefix, font: GSFont, error):
		return (True, None)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
