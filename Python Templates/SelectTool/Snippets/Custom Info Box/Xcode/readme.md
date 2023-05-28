## Custom Info Box with Xcode

If you must continuously display a dialog with your plug-in and it need not contain many controls, consider using an inspector (the little gray info boxes at the bottom of the Edit View).

The inspector view, if present, needs to be hard-wired to the variable `inspectorDialogView`.

![](../_Readme_Images/inspectorview.png)

### Xcode

Create a dialog in Xcode like you’ve read about [here](https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates). An *IBOutlet* needs to be created at the root of the plug-in class for it (and more for more controls that you want to access from Python), and our class needs an *IBAction* method to receive input from the dialog.

If you want the dialog to blend in with the same gray background, the View needs to be of the `GSInspectorView` class (Identity inspector in Xcode)

You will find the .xib/.nib files of this example [here](https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Sample%20dialogs) as `InspectorView`. Place them in the `Resources` folder in the plug-in package, where the main `plugin.py` is located.

###You need to select a node to see the info view!!

```python
# encoding: utf-8

import objc
from GlyphsApp import Glyphs, GSNode, Message
from GlyphsApp.plugins import SelectTool

class MySelectTool(SelectTool):
	
	inspectorDialogView = objc.IBOutlet()
	button = objc.IBOutlet()

	def settings(self):
		self.name = Glyphs.localize({'en': 'My Select Tool', 'de': 'Mein Auswahlwerkzeug'})

		# Load .nib file from package (without .extension)
		self.loadNib("InspectorView", self.__file__())

	# Return a GSInspectorView (not a Group) when needed
	def view(self):
		# This this is just sample code. Change that to your own conditions
		layer = self.editViewController().graphicView().activeLayer()
		if layer is not None and len(layer.selection) == 1 and isinstance(layer.selection[0], GSNode):
			return self.inspectorDialogView
		return None

	@objc.IBAction
	def buttonCallback_(self, sender):
		Message("Action", "You have clicked the button")

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	
```
