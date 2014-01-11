# Python templates

### Using the templates

Make a copy of the plugin folder structure. Make sure to go through these text files and replace the placeholders with quadruple underscores (`____placeholder____`):
* `Contents/Info.plist`
* `Contents/Resources/____PluginFileName____.py`
* `Contents/Resources/__boot__.py`

Don’t touch these files and folders:
* `Contents/MacOS/python`
* `Contents/PkgInfo`
* `Contents/Resources/lib/`
* `Contents/Resources/site.py`
* `Contents/Resources/__error__.sh`

Open `Info.plist` and customize the entries there. Set the version number in `CFBundleVersion` and `CFBundleShortVersionString`, put your name and the year in `NSHumanReadableCopyright`, and `CFBundleIdentifier` should be a reverse domain name without spaces. Re-use `____Developer____` for other projects.

Replace `____PluginFileName____` in `CFBundleExecutable` and `CFBundleVersion` with the name of the file name of `Contents/Resources/____PluginFileName____.py`, ignoring the `.py` extension. We recommend to use a camel-cased file name without spaces. The file and these two entries in `Contents/Info.plist` must carry the exact same name. Additionally, the name, including the `.py` extension must be reflected in the last line of `__boot__.py`.

In `Contents/Info.plist`, replace `____PluginClassName____` with the name of the principal Python class in `Contents/Resources/____PluginFileName____.py`. No spaces, we recommend camel case. These two entries and the name of the class in `____PluginFileName____.py` must be exactly the same.

`Contents/Resources/____PluginFileName____.py` is also where your code goes. Follow the instructions in the comments of the file.


### Installing and debugging

To install it, move it into the Plugins folder inside the Application Support folder of Glyphs (double click the plugin to let Glyphs do that for you). You can edit your code right there, but you need to restart the application for any changes to take effect.


### Some resources:

To use .xib files, you need to add IBActions and IBOutlet in the controller class like this:
```python
	_theOutlet = objc.IBOutlet()
```

... and:
```python
	@objc.IBAction
	def actionMethod_(self, sender):
		pass
```

Then edit the .xib in Xcode and add the .py file by File > Add Files...
after every change to the .xib, it has to be compiled to an .nib:
`ibtool Path/to/the/.xib --compile Path/to/the/.nib`

http://blog.adamw523.com/os-x-cocoa-application-python-pyobjc/
