### Warning

We’re currently in the process of restructuring the whole Python implementation of our plug-ins. Although we’re pretty far with it, please note that until we have released a stable 2.3 version, the plug-in skeletons might still see minor changes that could break a plug-in of yours currently under development from this code base here.

Please refrain from finishing up and publishing plug-ins based on this code until we have announced the final version 2.3 and monitor code changes to this repository.

January 27th 2016

___

Welcome to Glyphs.app’s plug-in documentation. 

This documentation here covers only a few details of the whole process. If you are new to the subject, we recommend to start by [reading our tutorial](https://glyphsapp.com/tutorials/plugins), where you will later be asked to return here.

## General Plug-in

The General Plug-in doesn’t have a particular purpose yet. You give it that purpose.

It’s a plug-in that gets quietly loaded when Glyphs.app starts and will execute whatever code you write. This could be callback functions for drawing into the Edit View (similar to the Reporter Plugin) or automatically backing up a .glyphs file when it’s being saved by the user.

The main difference between this General Plugin and a Python script executed via Glyphs.app’s *Script* menu or via the *Macro* window (where you could also add callbacks) is that the plug-in gets loaded automatically on startup whereas the two other methods require further user interaction.

Please check our Python API for the callbacks here: [`GSApplication.addCallback()`](http://docu.glyphsapp.com/#addCallback)

# User code

A functional plug-in can be as small as this (in `Contents/Resources/plugin.py`):

```python
# encoding: utf-8

from GlyphsPlugins import *

class ____PluginClassName____(GeneralPlugin):
	def start(self):
		# Your init code goes here
```

From there you can add the following methods:

#### settings()

In this method you set all attributes that describe the plug-in, such as its name etc.


```python
	def settings(self):

		# The name of the plug-in (here mainly used for error messages)
		# You may use a simple string or Glyphs.localize() for localizations (see http://docu.glyphsapp.com#localize)
		self.name = 'My General Plugin'
		# or:
		self.name = Glyphs.localize({'en': u'My General Plugin', 'de': u'Mein allgemeines Plugin'})

		# A keyboard shortcut for adctivating/deactivating the plug-in (together with Command+Shift)
		self.keyboardShortcut = 'p'
```

#### start()

This method gets called when the plug-in gets initialized upon Glyphs.app start.
You put all your initialization code here.

```python
	def start(self):

		# Your plugin code goes here...
```
