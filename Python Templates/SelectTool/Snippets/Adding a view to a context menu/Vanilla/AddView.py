# encoding: utf-8

from GlyphsApp.plugins import *
from vanilla import Window, Group, TextBox, Slider

class ____PluginClassName____(SelectTool):

	def settings(self):
		self.name = 'My Select Tool'

		# Create Vanilla window and group with controls
		viewWidth = 150
		viewHeight = 40
		self.sliderMenuView = Window((viewWidth, viewHeight))
		# Using PatchedGroup() here instead of Group()
		self.sliderMenuView.group = Group((0, 0, viewWidth, viewHeight))
		self.sliderMenuView.group.text = TextBox((10, 0, -10, -10), self.name)
		self.sliderMenuView.group.slider = Slider((10, 18, -10, 23), callback=self.sliderCallback_)

		# Define the menu
		self.generalContextMenus = [
			{'name': Glyphs.localize({'en': u'Layer info in Macro window', 'de': u'Ebenen-Infos in Makro-Fenster'}), 'action': self.printInfo_},
			{"view": self.sliderMenuView.group.getNSView()},
		]

	# Prints the slider’s value
	def sliderCallback_(self, sender):
		print('Slider value:', sender.get())
		
	def printInfo_(self, sender):
		print("Print Info", sender)