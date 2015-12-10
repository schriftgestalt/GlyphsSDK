## File Format Plugin

At the moment, this plugin provides font export functionality through the Export dialog.
Planned for the future are Save and Open functionalities.

This sample plugin is functional and exports glyph names, unicodes and glyph width into a simple CSV file.
It makes use of a GUI through Interface Builder. See the description one level up (https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates) on how to use it.

![](_Readme_Images/exportdialog.png)

# User code

A functional plugin can be as small as this (in `Contents/Resources/____PluginFileName____.py`):

```python
# encoding: utf-8

from plugin import *
from AppKit import *

class ____PluginClassName____(FileFormatPlugin):
	
	dialog = objc.IBOutlet()

	def settings(self):
		self.name = 'My CSV Export'
		self.dialog = '____PluginFileName____Dialog'
		self.icon = 'ExportIcon'

	def export(self, font):

		# Code that writes a file goes here...

		# Return values
		return (True, 'The export of the file was successful.')
```

The methods in detail:

#### settings()

In this method you set all attributes that describe the plugin, such as its name and icon etc.


```python
	def settings(self):

		# The name as it will appear in the Export dialog
		self.name = 'My CSV Export'

		# The file name of the Interface Builder .nib file (the dialog) without file extension
		self.dialog = '____PluginFileName____Dialog'

		# The file name of the icon file without file extension
		self.icon = 'ExportIcon'

		# The position of the icon in the Export dialog toolbar
		self.toolbarPosition = 100
```

#### loadPlugin()

This method gets called when the plugin gets initialized upon Glyphs.app start.
You put all your initialization code here.

```python
	def loadPlugin(self):

		# Your init code goes here...
```

#### export()

Use this method to write the file after the 'Next' button has been clicked in the Export dialog.

The `font` argument in the method will contain the `GSFont` object we’re dealing with.

Return value:
This function must return a tuple containing:
- `True`/`False` (Boolean describing the success of the file writing)
- Message (A text message describing the success/failure of the file writing)

```python
	def export(self, font):

		# Your file writing code goes here

		if exportSuccessful == True:
			return (True, 'The export was successful.')
		
		else:
			return (False, 'The export failed.')
```


# Other useful methods

#### saveFileDialog()

Dialog to choose export destination.

Optional arguments:
- `title` (a string for the title of the file dialog)
- `proposedFilename` (a string describing a possible file name)
- `fileTypes` (a list (not a tuple!) of acceptable file name extensions)

```python
	def export(self, font):
	
		# Ask for export destination and write the file:
		title = "Choose export destination"
		proposedFilename = font.familyName
		fileTypes = ['csv']

		# Call dialog
		filepath = self.saveFileDialog(title, proposedFilename, fileTypes)
		
		# Your file writing code goes here...
```
