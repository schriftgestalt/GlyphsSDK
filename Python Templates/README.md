# Python templates

### Using the templates

Make a copy of the plugin folder structure. The core code must go into `Contents/Resources/____PluginFileName____.py`. Rename the file and copy the filename into the last line of `__boot__.py`. Give `Contents/MacOS/____PluginFileName____` the same name, except for the `.py` suffix.

Make sure to go through these text files and replace the placeholders with quadruple underscores (`____placeholder____`):
* `Contents/Info.plist`
* `Contents/Resources/____PluginFileName____.py`
* `Contents/Resources/__boot__.py`

Don’t touch these files and folders:
* `Contents/MacOS/python`
* `Contents/PkgInfo`
* `Contents/Resources/lib/`
* `Contents/Resources/site.py`
* `Contents/Resources/__error__.sh`

### Installing and debugging

To install it, move it into the Plugins folder inside the Application Support folder of Glyphs (double click the plugin to let Glyphs do that for you). You can edit your code right there, but you need to restart the application for any changes to take effect.


### Some resources:

To use .xib files, you need to add IBActions and IBOutlet in the controller class like this:
```python
	_theOutlet = objc.IBOutlet()
```

and 
```python
	@objc.IBAction
	def actionMethod_(self, sender):
		pass
```

Then edit the .xib in Xcode and add the .py file by File > Add Files...
after every change to the .xib, it has to be compiled to an .nib:
`ibtool Path/to/the/.xib --compile Path/to/the/.nib`

http://blog.adamw523.com/os-x-cocoa-application-python-pyobjc/