## Dialogs in contextual menus with Xcode

Create a dialog in Xcode like you’ve read about [here](https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates). An *IBOutlet* needs to be created at the root of the plug-in class for it (and more for more controls that you want to access from Python), and our class needs an *IBAction* method to receive input from the dialog.

You will find the .xib/.nib files of this example [here](https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Sample%20dialogs) as `SliderView`. Place them in the `Resources` folder in the plug-in package, where the main `plugin.py` is located.


```python
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
```
