# encoding: utf-8

###########################################################################################################
#
#
# Filter with dialog Plugin
#
# Read the docs:
# https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20with%20Dialog
#
# For help on the use of Xcode:
# https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import Glyphs
from GlyphsApp.plugins import FilterWithDialog
from AppKit import NSPoint


class ____PluginClassName____(FilterWithDialog):

	# Definitions of IBOutlets

	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()

	# Text field in dialog
	myTextField = objc.IBOutlet()

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

		# Word on Run Button (default: Apply)
		self.actionButtonLabel = Glyphs.localize({
			'en': 'Apply',
			'de': 'Anwenden',
			'fr': 'Appliquer',
			'es': 'Aplicar',
			'pt': 'Aplique',
			'jp': '申し込む',
			'ko': '대다',
			'zh': '应用',
		})

		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)

	# On dialog show
	@objc.python_method
	def start(self):

		# Set default value
		Glyphs.registerDefault('com.myname.myfilter.value', 15.0)

		# Set value of text field
		self.myTextField.setStringValue_(Glyphs.defaults['com.myname.myfilter.value'])

		# Set focus to text field
		self.myTextField.becomeFirstResponder()

	# Action triggered by UI
	@objc.IBAction
	def setValue_(self, sender):

		# Store value coming in from dialog
		Glyphs.defaults['com.myname.myfilter.shift'] = sender.floatValue()

		# Trigger redraw
		self.update()

	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):

		# Called on font export, get value from customParameters
		if "shift" in customParameters:
			value = customParameters['shift']

		# Called through UI, use stored value
		else:
			value = float(Glyphs.defaults['com.myname.myfilter.shift'])

		# Shift all nodes in x and y direction by the value
		for path in layer.paths:
			for node in path.nodes:
				node.position = NSPoint(node.position.x + value, node.position.y + value)

	@objc.python_method
	def generateCustomParameter(self):
		return "%s; shift:%s;" % (self.__class__.__name__, Glyphs.defaults['com.myname.myfilter.shift'])

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
