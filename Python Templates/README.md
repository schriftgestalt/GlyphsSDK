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

In `Contents/Info.plist`, replace `____PluginClassName____` with the name of the principal Python class in `Contents/Resources/____PluginFileName____.py`. No spaces, we recommend camelcase. These two entries and the name of the class in `____PluginFileName____.py` must be exactly the same.

`Contents/Resources/____PluginFileName____.py` is also where your code goes. You will find instructions in the comments of the file.


### Installing and debugging

To install it, move it into the Plugins folder inside the Application Support folder of Glyphs (double click the plugin to let Glyphs do that for you). You can edit your code right there, but you need to restart the application for any changes to take effect.

### Adding GUI elements

For GUI elements, you will need to work with Interface Builder (IB). For this, you edit `.xib` files in XCode, and compile them to `.nib` files. To use `.xib` files, you need to add IBActions and IBOutlets in the principal controller class of your `____PluginFileName____.py`, like this:
```python
	_theOutlet = objc.IBOutlet()
```

... and start the respective UI action method (e.g. an action triggered by a button) with `@objc.IBAction`:
```python
	@objc.IBAction
	def actionMethod_(self, sender):
		pass
```

You will find more detailed help in the comments of the .py file. Then, edit the `.xib` in Xcode and add the .py file by *File > Add Files...* When you are done, and every time the `.xib` file is changed, it has to be compiled to a `.nib` file. Do so with this Terminal command:
`ibtool Path/to/the/.xib --compile Path/to/the/.nib`

For a quick walkthrough, read:
http://blog.adamw523.com/os-x-cocoa-application-python-pyobjc/
