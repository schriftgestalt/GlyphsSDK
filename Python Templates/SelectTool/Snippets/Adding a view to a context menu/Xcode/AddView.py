# encoding: utf-8

from GlyphsApp.plugins import *

class ____PluginClassName____(SelectTool):

	# The reference to the dialog
	sliderMenuView = objc.IBOutlet()
	
	def settings(self):
		self.name = 'My Select Tool'

		# Load .nib file from package (without .extension)
		self.loadNib("SliderView", self.__file__())

		# Define the menu
		self.generalContextMenus = [
			{"view": self.sliderMenuView}
		]

	# Prints the slider’s value
	@objc.IBAction
	def slider_(self, sender):
		print('Slider value:', sender.floatValue())

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__