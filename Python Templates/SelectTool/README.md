The Select Tool Plugin creates a replacement for the standard select tool and lets you extend its functionality.
You can add context menus (that appear on the user’s mouse right-click), both general context menus (they always appear) as well as conditional contaxt menus (they only appear under a certain condition defined in your code).

In it’s naked version, the plugin behaves exactly like the built-in select tool.

![](../_Readme_Images/selecttool.png)

# User code

A functional plugin can be as small as this (in `Contents/Resources/____PluginFileName____.py`):

```python
# encoding: utf-8

from plugin import *
from GlyphsApp import *
from AppKit import *

class ____PluginClassName____(SelectTool):
	
	def settings(self):
		self.name = 'My Select Tool'
		self.contextMenus = [
			["Layer info in Macro Window", self.printInfo],
		]

	def printInfo(self):
		"""
		Example for a method triggered by a context menu item.
		Fill in your own method name and code.
		Remove this method if you do not want any extra context menu items.
		"""

		# Execute only if layers are actually selected
		if Glyphs.font.selectedLayers:
			layer = Glyphs.font.selectedLayers[0]
		
			# Do stuff:
			print "Current layer:", layer.parent.name, layer.name
			print "  Number of paths:", len(layer.paths)
			print "  Number of components:", len(layer.components)
			print "  Number of anchors:", len(layer.anchors)
```




From there you can add the following methods:

#### settings()

In this method you set all attributes that describe the plugin, such as its name and icon etc.


```python
	def settings(self):

		# The name as it will appear in Glyphs’s toolbar as a tooltip
		self.name = 'My Select Tool'

		# A keyboard shortcut for adctivating/deactivating the plugin
		self.keyboardShortcut = 'p'

		# Position of the tool icon in the toolbar
		self.toolbarPosition = 100

		# A list of general context menu items described as a list of `name`/`method` pairs.
		# These context menu items will always appear at the bottom of the menu
		# when the user right-clicks into the Edit View.
		self.generalContextMenus = [
			["Layer info in Macro Window", self.printInfo],
		]
```

#### start()

This method gets called when the plugin gets initialized upon Glyphs.app start.
You put all your initialization code here.

```python
	def start(self):

		# Your init code goes here...
```

#### activate()

This method gets called when the tool gets activated through the toolbar.

```python
	def activate(self):

		# Your init code goes here...
```

#### deactivate()

This method gets called when the tool gets deactivated through the toolbar (another tool gets activated).

```python
	def deactivate(self):

		# Your code goes here...
```

#### conditionalContextMenus()

Use this method to create and return a list of conditional context menu items.
These context menu items could be based on the user’s selection of objects in the Edit View and will appear first in the menu.

Return a list of context menu items described as a list of `['name', method]` pairs.

```python
	def conditionalContextMenus(self):

		# Empty list of context menu items
		contextMenus = []

		# Execute only if layers are actually selected
		if Glyphs.font.selectedLayers:
			layer = Glyphs.font.selectedLayers[0]
			
			# Exactly one object is selected and it’s an anchor
			if len(layer.selection) == 1 and type(layer.selection[0]) == GSAnchor:
					
				# Add context menu item
				contextMenus.append(["Randomly move anchor", self.randomlyMoveAnchor])

		# Return list of context menu items
		return contextMenus
```