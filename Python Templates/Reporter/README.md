Welcome to Glyphs.app’s plug-in documentation. 

This documentation here covers only a few details of the whole process. If you are new to the subject, we recommend to start by [reading our tutorial](https://glyphsapp.com/tutorials/plugins), where you will later be asked to return here.

## Reporter Plug-in

A reporter plug-in gets activated in the View menu of Glyphs.app and is designed to draw on top and behind the glyphs in the Edit View, as well as change the drawing behaviour of inactive glyphs and the preview panel.

![](README Pictures/showplugin.png)


# User code

A functional plug-in can be as small as this (in `Contents/Resources/plugin.py`):

```python
# encoding: utf-8

from GlyphsPlugins import *

class ____PluginClassName____(ReporterPlugin):
	def settings(self):

		# The name as it will appear in Glyphs’s View menu
		self.menuName = 'My Plugin'

	def drawForeground(self, layer):

		# Draw a blue rectangle on top of the glyph as big as the glyph’s bounding box
		NSColor.blueColor().set()
		NSBezierPath.fillRect_(layer.bounds)
```




From there you can add the following methods:

#### settings()

In this method you set all attributes that describe the plug-in, such as its name and icon etc.


```python
	def settings(self):

		# The name as it will appear in Glyphs’s View menu
		# You may use a simple string or Glyphs.localize() for localizations (see http://docu.glyphsapp.com#localize)
		self.menuName = 'My Plugin'
		# or:
		self.menuName = Glyphs.localize({'en': 'My Plugin', 'de': 'Mein Plugin'})

		# A keyboard shortcut for activating/deactivating the plug-in
		self.keyboardShortcut = 'p'

		# Modifier keys used for the keyboard shortcut
		# Set to any combination of:
		# NSShiftKeyMask | NSControlKeyMask | NSCommandKeyMask | NSAlternateKeyMask
		self.keyboardShortcutModifier = NSCommandKeyMask | NSShiftKeyMask

		# A list of general context menu items described as a list of `name`/`method` pairs.
		# These context menu items will appear at the top of the menu 
		#   if no index is given as the third parameter in each set.
		# Otherwise, -1 will position the menu item at the bottom of the menu, 
		#   all other integers will position them in that position.
		self.generalContextMenus = [
			["Context menu at top", self.doSomething],
			["Context menu at bottom", self.doSomething, -1],
		]
```

#### start()

This method gets called when the plug-in gets initialized upon Glyphs.app start.
You put all your initialization code here.

```python
	def start(self):

		# Your init code goes here...
```

#### drawForeground()

Use this method to draw things on top the glyph outlines in the Edit View.

```python
	def drawForeground(self, layer):

		# Draw a blue rectangle on top of the glyph as big as the glyph’s bounding box
		NSColor.blueColor().set()
		NSBezierPath.fillRect_(layer.bounds)
```

#### drawBackground()

Use this method to draw things behind the glyph outlines in the Edit View.

```python
	def drawBackground(self, layer):

		# Draw a red rectangle on behind the glyph as big as the glyph’s bounding box
		NSColor.redColor().set()
		NSBezierPath.fillRect_(layer.bounds)
```

#### drawBackgroundForInactiveLayers()

Use this method to replace Glyph.app’s default drawing method for drawing inactive glyphs (the glyphs left and right of the active glyph in the Edit View) as well as the glyphs in the Edit View.

If you want to draw the glyphs in the Edit View even different that the inactive glyphs, also implement the `drawPreview()` method as described below.

```python
	def drawBackgroundForInactiveLayers(self, layer):

		# Draw outlines in blue
		if layer.paths:
			NSColor.blueColor().set()
			layer.bezierPath().fill()

		# Draw components in red
		if layer.components:
			NSColor.redColor().set()
			for component in layer.components:
				component.bezierPath().fill()
```

#### drawPreview()

Use this method to replace Glyph.app’s default drawing method for glyphs in the preview panel.

You must implement `drawBackgroundForInactiveLayers()` first and implement `drawPreview()` only as a deviation from `drawBackgroundForInactiveLayers()`.

`drawPreview()` cannot be implemented standalone without `drawBackgroundForInactiveLayers()`.

Please note that due to the live interpolation of the preview panel these layers don’t contain components, but only paths.

```python
	def drawPreview(self, layer):

		# Draw outlines in blue
		if layer.paths:
			NSColor.blueColor().set()
			layer.bezierPath().fill()
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

# Tips on Drawing

Glyphs.app uses the Mac’s own Cocoa methods for drawing. These sometimes behave slightly different from other Python objects, and surely they have different names. 

In order to make use of the Cocoa objects, make sure to include them into your Python plug-in declaring `from AppKit import *` at the top of the plug-in.

Here are a few examples:

```python
	def drawForeground(self, layer):

		# Setting colors:
		# sets RGBA values between 0.0 and 1.0:
		NSColor.colorWithCalibratedRed_green_blue_alpha_( 1.0, 1.0, 1.0, 1.0 ).set()
		
		# predefined colors: blackColor, blueColor, brownColor, clearColor, cyanColor,
		# darkGrayColor, grayColor, greenColor, lightGrayColor, magentaColor, orangeColor,
		# purpleColor, redColor, whiteColor, yellowColor
		NSColor.redColor().set() 


		# Drawing paths:
		myPath = NSBezierPath.alloc().init()  # initialize a path object
		myPath.appendBezierPath_( subpath )   # add subpath
		myPath.fill()   # fill with the current NSColor (see above)
		myPath.stroke() # stroke with the current NSColor (see above)
		
		# All layers, paths, and components have a .bezierPath() method that
		# returns that path as a NSBezierPath object that you can use for drawing:
		# NOTE: This method will be renamed to a .bezierPath attribute very soon!!!
		layer.bezierPath().fill()
		layer.paths[0].bezierPath().fill()
		layer.components[0].bezierPath().fill()
```

For more detailed information make sure to read into the Cocoa documentation:
https://developer.apple.com/library/mac/documentation/Cocoa/Reference/ApplicationKit/Classes/NSBezierPath_Class/Reference/Reference.html
https://developer.apple.com/library/mac/documentation/cocoa/reference/applicationkit/classes/NSColor_Class/Reference/Reference.html

# Other useful methods

#### drawTextAtPoint()

Draw a string of text at a given position.

Mandatory arguments:
- `text` (A string of text)
- `position` (`NSPoint` object of position)

Optional arguments:
- `fontSize` (Size of text in points. Default: 10)
- `align` (Alignment of text. Default: `bottomleft`. Choose from: `topleft`, `topcenter`, `topright`, `left`, `center`, `right`, `bottomleft`, `bottomcenter`, `bottomright`)
- `fontColor` (`NSColor` object. Default: black)

```python
	def drawForeground(self, layer):
		
		# Draw name of glyph at 0,0
		self.drawTextAtPoint(layer.parent.name, NSPoint(0, 0))

```
