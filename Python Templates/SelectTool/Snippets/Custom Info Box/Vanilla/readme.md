## Custom Info Box with vanilla

We need to create a so called [Group](https://vanilla.robotools.dev/en/latest/objects/Group.html) that contains a set of objects. Of this group, we can get hold of the wrapped `NSView` object to display in Glyphs. Note that due to Vanilla internals, we have to create a window first, although that window isn’t getting any attention anymore later on, and it must contain a `Group()` of the same size. Note that stretching the `Group` to the far corners of the windows using `(0, 0, -0, -0)` may not work, so explicitly define its size identical to the containing window.

The `NSView` object that we hand over to Glyphs to display needs to be of the `GSInspectorView` class. In order to achieve this using Vanilla, we need to create a patched Vanilla-style `Group` class and tell it to use a `GSInspectorView` object instead of the regular `NSView`. `GSInspectorView` is already a descendant of `NSView`, so Vanilla can very well use that instead.


```python
# encoding: utf-8

from GlyphsApp.plugins import *
from vanilla import Window, Group, Button

# Our own patched Vanilla Group class
GSInspectorView = objc.lookUpClass("GSInspectorView")
class InspectorGroup(Group):
	nsViewClass = GSInspectorView

class ____PluginClassName____(SelectTool):

	def settings(self):
		self.name = 'My Select Tool'

		# Create Vanilla window and group with controls
		self.infoBoxWindow = Window((viewWidth, viewHeight))
		# Using InspectorGroup() here instead of Group()
		self.infoBoxWindow.group = InspectorGroup("auto")
		self.infoBoxWindow.group.button = Button("auto", "Move", callback=self.buttonCallback_)
		rules = [
			"H:|-8-[button]-8-|",
			"V:|-10-[button]-10-|",
		]
		self.infoBoxWindow.group.addAutoPosSizeRules(rules)
		self.infoBoxView = self.infoBoxWindow.group.getNSView()
		self.inspectorDialogView = True
	
	# Return a GSInspectorView (not a Group) when needed
	def view(self):
		# This this is just sample code. Change that to your own conditions
		layer = self.editViewController().graphicView().activeLayer()
		if layer is not None and len(layer.selection) == 1 and isinstance(layer.selection[0], GSNode):
			return self.infoBoxView
		return None

	# Prints the slider’s value
	def buttonCallback_(self, sender):
		print('Button:', sender.get())
```
