## Adding a view to a context menu with vanilla

As in the sidebar example, we need to create a so called [Group](https://vanilla.robotools.dev/en/latest/objects/Group.html) that contains a set of objects. Of this group, we can get hold of the wrapped `NSView` object to display in Glyphs. Note that due to Vanilla internals, we have to create a window first, although that window isn’t getting any attention anymore later on, and it must contain a `Group()` of the same size. Note that stretching the `Group` to the far corners of the windows using `(0, 0, -0, -0)` may not work, so explicitly define its size identical to the containing window.

Then we use that in self.generalContextMenus

```python
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
```
