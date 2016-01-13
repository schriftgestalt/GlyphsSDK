Welcome to Glyphs.app’s plug-in documentation. 

This documentation here covers only a few details of the whole process. If you are new to the subject, we recommend to start by [reading our tutorial](https://glyphsapp.com/tutorials/plugins), where you will later be asked to return here.

## Palette Plug-in

The palette plug-in will show up as a dialog in Glyphs.app’s sidebar on the right edge of the application window. 

You may use it to display information about the glyphs or add controls to change them.
For displaying information, you would typically use callbacks that tie in with events being fired in Glyphs.app, such as the `GSUpdateInterface` event, which gets fired each time anything is being redrawn in the user interface. This can happen quite often, so be careful as to how complicated your code becomes.

![](../_Readme_Images/palette.png)


# User code

A functional plug-in can be as small as this (in `Contents/Resources/plugin.py`):

```python
# encoding: utf-8

from GlyphsPlugins import *

class ____PluginClassName____ (PalettePlugin):

	# The Interface Builder dialog
	dialog = objc.IBOutlet()

	# A text field to display information in that dialog
	textField = objc.IBOutlet()
	
	def settings(self):
		self.name = 'My Palette'
	
	def start(self):

		# Adding a callback for the 'GSUpdateInterface' event
		s = objc.selector( self.update, signature="v@:" )
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSUpdateInterface", None )

	def update( self, sender ):

		# Your code goes here...

	def quit(self):
		
		# Delete callbacks when Glyphs quits, otherwise it'll crash :( 
		NSNotificationCenter.defaultCenter().removeObserver_(self)
```

From there you can add the following methods:

#### settings()

In this method you set all attributes that describe the plug-in, such as its name etc.


```python
	def settings(self):

		# The name as it will appear in the sidebar
		# You may use a simple string or Glyphs.localize() for localizations (see http://docu.glyphsapp.com#localize)
		self.name = 'My Palette'
		# or:
		self.name = Glyphs.localize({'en': 'My Palette', 'de': 'Mein Palette'})

		# The name of the Interface Builder file containing the UI dialog, without file extension
		self.dialogName = 'IBDialog'
```

#### start()

This method gets called when the plug-in gets initialized upon Glyphs.app start.
You put all your initialization code here.
In our example, this would be adding the callbacks.

An observer needs a method to execute. In our example, we’ve used a method named `update()`, but you can name your methods otherwise.

```python
	def start(self):

		# Adding a callback for the 'GSUpdateInterface' event
		s = objc.selector( self.update, signature="v@:" )
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSUpdateInterface", None )
```

#### update()

In our example, this method gets called through the callbacks you may have added upon `start()`.

We’ve named this method `update()`, but you can name your methods otherwise.

```python
	def update(self):

		# Your code goes here...
```

#### quit()

This method gets called when Glyphs.app is being quitted.
You need to unload all callbacks here because Glyphs.app will otherwise crash.

```python
	def quit(self):

		# Unload callback
		NSNotificationCenter.defaultCenter().removeObserver_(self)
```
