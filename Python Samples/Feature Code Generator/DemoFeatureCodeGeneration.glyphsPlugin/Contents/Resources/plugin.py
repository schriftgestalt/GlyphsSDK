import objc
from AppKit import NSObject
from GlyphsApp import GSCallbackHandler, GSFeaturePrefix, GSClass, GSFeature, GSFont
from GlyphsApp.plugins import GeneralPlugin

GSFeatureCodeGeneratorProtocol = objc.protocolNamed("GSFeatureCodeGeneratorProtocol")

class DemoFeatureCode(GeneralPlugin):
	@objc.python_method
	def settings(self):
		pass

	@objc.python_method
	def start(self):
		GSCallbackHandler.addFeatureCodeGenerator_(DemoFeatureCodeGenerator)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__

class DemoFeatureCodeGenerator(NSObject):
	__pyobjc_protocols__ = [GSFeatureCodeGeneratorProtocol]

	@classmethod
	def title(cls):
		return "Demo Feature Code Generation"

	@classmethod
	def canGenerateFeatureCodeForPrefixWithName_(cls, prefixName: str):
		return prefixName in ["Header"]

	@classmethod
	def featureCodeForPrefix_font_error_(cls, prefix: GSFeaturePrefix, font: GSFont, error):
		if prefix.name == "Header":
			prefix.code = "sub main by mail;\n"
		return True, None

	@classmethod
	def canGenerateFeatureCodeForClassWithName_(cls, className: str):
		return False

	@classmethod
	def featureCodeForClass_font_error_(cls, aClass: GSClass, font: GSFont, error):
		return True, None

	@classmethod
	def canGenerateFeatureCodeForFeatureWithTag_(cls, featureTag: str):
		return True

	@classmethod
	def featureCodeForFeature_font_error_(cls, feature: GSFeature, font: GSFont, error):
		return True, None
