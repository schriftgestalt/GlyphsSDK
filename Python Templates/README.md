# Python templates

### Using the templates

Make a copy of the plugin folder structure inside your Plugins folder (see ‘Installing and debugging’ below). Make sure to go through these text files and replace the placeholders with quadruple underscores (`____placeholder____`):
* `Contents/Info.plist`
* `Contents/MacOS/____PluginFileName____` (just needs to be renamed)
* `Contents/Resources/____PluginFileName____.py`
* `Contents/Resources/__boot__.py`

Do *not* touch these files and folders:
* `Contents/MacOS/python`
* `Contents/PkgInfo`
* `Contents/Resources/lib/`
* `Contents/Resources/site.py`
* `Contents/Resources/__error__.sh`

Open `Contents/Info.plist` and customize the entries there. Set the version number in `CFBundleVersion` and `CFBundleShortVersionString`, put your name and the year in `NSHumanReadableCopyright`, and `CFBundleIdentifier` should be a reverse domain name without spaces. You can re-use `____Developer____` for other projects. If you are making a filter, it is a good idea to start `NSPrincipalClass` with `GlyphsFilter`, e.g., `GlyphsFilterMoveNodes`.

In `Contents/Info.plist`, replace `____PluginClassName____` with the name of the principal Python class in `Contents/Resources/____PluginFileName____.py`. No spaces, we recommend camelCase. These two entries and the name of the class in `____PluginFileName____.py` must be exactly the same.

Again, in `Contents/Info.plist`, replace `____PluginFileName____` in `CFBundleExecutable` and `CFBundleVersion` with the actual file name of `Contents/Resources/____PluginFileName____.py`, ignoring the `.py` extension. Rename `Contents/MacOS/____PluginFileName____` to the same file name, again ignoring the `.py` extension. The files and these two entries in `Contents/Info.plist` must carry the exact same name. We recommend to use a camel-cased file name without spaces.

In the last line of `Contents/Resources/__boot__.py`, the file name (`____PluginFileName____`), this time *with* the `.py` extension, must be mentioned.

`Contents/Resources/____PluginFileName____.py` is where your code goes. You will find extensive instructions in the comments of the file. Have fun.

### Installing and debugging

To install a plugin, move it into the Plugins folder inside the Application Support folder of Glyphs (double click the plugin to let Glyphs do that for you). You can edit your code right there, but you need to restart the application for any changes to take effect.

Tip: right-click the Glyphs.app Dock icon, force quit it, and restart immediately with a click on the Dock icon. This will also immediately re-open any windows (you had open before the force quit) to their last state.

### Adding GUI elements

For GUI elements, you will need to work with Interface Builder (IB). For this, you edit `.xib` files in XCode, and compile them to `.nib` files. To use `.xib` files, you need to add IBActions and IBOutlets in the principal controller class of your `____PluginFileName____.py`, like this:
```python
	_theOutlet = objc.IBOutlet()
```

... and start the respective UI action method (e.g. an action triggered by a button) with `@objc.IBAction`:
```python
	@objc.IBAction
	def buttonPressed_( self, sender ):
		print "The button was pressed!"
```

Then, still in Xcode, add the .py file with *File > Add Files...*. When you are done, and every time the `.xib` file is changed, it has to be compiled to a `.nib` file. Do so with this Terminal command:
`ibtool xxx.xib --compile xxx.nib`.

If this looks confusing at first, do not worry. You will find detailed step-by-step instructions in the comments of the .py file. And for a quick introduction to using Interface Builder with the PyObjC bridge, read:
http://blog.adamw523.com/os-x-cocoa-application-python-pyobjc/
