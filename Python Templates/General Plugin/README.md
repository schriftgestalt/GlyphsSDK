The General Plugin doesn’t have a particular purpose yet. You give it that purpose.

It’s a plugin that gets quietly loaded when Glyphs.app starts and will execute whatever code you write. This could be callback functions for drawing into the Edit View (similar to the Reporter Plugin) or automatically backing up a .glyphs file when it’s being saved by the user.

Please check our Python API for the callbacks here: [`GSApplication.addCallback()`](http://docu.glyphsapp.com/#addCallback)

# User code

A functional plugin can be as small as this (in `Contents/Resources/____PluginFileName____.py`):

```python
# encoding: utf-8

from plugin import *
from AppKit import *
from GlyphsApp import *

class ____PluginClassName____(GeneralPlugin):
	def start(self):
		# Yor init code goes here
```
