# encoding: utf-8

###########################################################################################################
#
#
# Reporter Plugin
#
# Read the docs:
# https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################


from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import Glyphs, GSLayer, GSGlyphsInfo
from GlyphsApp.plugins import ReporterPlugin
from Cocoa import NSBezierPath, NSRect


class GSDrawInFontViewExample(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Draw In Font View Example',
		})

	def drawFontViewBackgroundForLayer_inFrame_(self, layer: GSLayer, frame: NSRect):
		glyph = layer.parent
		color = GSGlyphsInfo.labelColors()[len(glyph.name) % len(GSGlyphsInfo.labelColors())]
		color = color.colorWithAlphaComponent_(0.4)
		color.set()

		frame.origin.y -= 20
		frame.size.height += 20
		NSBezierPath.fillRect_(frame)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
