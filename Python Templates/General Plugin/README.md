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
