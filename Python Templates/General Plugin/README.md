The General Plugin doesn’t have a particular purpose yet. You give it that purpose.

It’s a plugin that gets quietly loaded when Glyphs.app starts and will execute whatever code you write. This could be callback functions for drawing into the Edit View (similar to the Reporter Plugin) or automatically backing up a .glyphs file when it’s being saved by the user.

The main difference between this General Plugin and a Python script executed via Glyphs.app’s *Script* menu or via the *Macro* window (where you could also add callbacks) is that the plugin gets loaded automatically on startup whereas the two other methods require further user interaction.

Please check our Python API for the callbacks here: [`GSApplication.addCallback()`](http://docu.glyphsapp.com/#addCallback)

# User code

A functional plugin can be as small as this (in `Contents/Resources/plugin.py`):

```python
# encoding: utf-8

from GlyphsPlugins import *

class ____PluginClassName____(GeneralPlugin):
	def start(self):
		# Yor init code goes here
```
