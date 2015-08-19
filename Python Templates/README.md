# Python templates

### Using the templates

Copy the template plugin into your Plugins folder, which is located at ~/Library/Application Support/Glyphs/Plugins (see ‘Installing and debugging’ below). And open it in your favorite text editor. It should display the internal folder structure of the plugin.

Make sure to go through the following files and replace all placeholders that have quadruple underscores (like `____placeholder____`):
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

For simplicity’s sake, and if it makes sense for your project, you can keep `____PluginClassName____`, `____PluginFileName____`, and `____PluginName____` the same throughout the whole project.

#### Edit Info.plist

Open `Contents/Info.plist` and customize the entries there. If you want to make sure your plugin works with the update mechanism built into Glyphs, always update the version numbers: Put a version number in dotted format into `CFBundleShortVersionString` (e.g, 1.2.3), and a release number into `CFBundleVersion` (a simple incremental number, e.g., 12).

You will probably re-use `____Developer____` for other projects, so put your name or twitter handle there. Put your name and year in `NSHumanReadableCopyright`. Glyphs will try to parse your name between the copyright and the year number, and display it in the Plugins section of the app preferences. `CFBundleIdentifier` should be a reverse domain name without spaces (e.g., com.myCompany.pluginName). In case you are making a filter with a custom parameter: `NSPrincipalClass` will be the filter trigger for the parameter value (i.e., the identifier before the first semicolon).

Still in `Contents/Info.plist`, replace `____PluginClassName____` with the name of the principal Python class in `Contents/Resources/____PluginFileName____.py`. No spaces, we recommend camelCase. These two entries and the name of the class in `____PluginFileName____.py` must be exactly the same.

Again, in `Contents/Info.plist`, replace `____PluginFileName____` in `CFBundleExecutable` and `CFBundleVersion` with the actual file name of `Contents/Resources/____PluginFileName____.py`, ignoring the `.py` extension. Rename `Contents/MacOS/____PluginFileName____` to the same file name, again ignoring the `.py` extension. The files and these two entries in `Contents/Info.plist` must carry the exact same name. We recommend to use a camel-cased file name without spaces.

### Plugin update mechanism

In `UpdateFeedURL`, replace `____OnlineUrlToThisPlist____` with a deep link to this .plist file. On GitHub, navigate to the file, and use its Raw link. And then, in `productPageURL`, replace `____ProductPageURL____` with a web page URL for the plugin. This can be your GitHub repository page. Finally, in `productReleaseNotes`, don’t forget to replace `____LatestReleaseNotes____` with a short description of your latest changes, e.g., ‘New option X’. This will be displayed when the user checks for updates in the app preferences, and will motivate your users to keep your plugins up to date.

#### Edit the boot file

In the last line of `Contents/Resources/__boot__.py`, the file name (`____PluginFileName____`), this time *with* the `.py` extension, must be mentioned.

#### Rename the MacOS executable

Rename `Contents/MacOS/____PluginFileName____`. Make sure it is exactly in sync with the `CFBundleExecutable` value in Info.plist, and with the name of the core Python file (except for the .py suffix). See below.

#### Rename and edit the core Python file

`Contents/Resources/____PluginFileName____.py` is where your actual code goes. Rename the file, and open it. You will find extensive step-by-step instructions in the comments. Have fun.

### Installing and debugging

To install a plugin, move it into the Plugins folder inside the Application Support folder of Glyphs (double click the plugin to let Glyphs do that for you). You can edit your code right there, but you need to restart the application for any changes to take effect.

Tip: right-click the Glyphs.app Dock icon, force quit it, and restart immediately with a click on the Dock icon. This will also immediately re-open any windows (you had open before the force quit) to their last state.

### Adding GUI elements

For GUI elements, you will need to work with Interface Builder (IB). For this, you edit `.xib` files in XCode, and compile them to `.nib` files. To use `.xib` files, you need to add IBActions and IBOutlets in the principal controller class of your `____PluginFileName____.py`, like this:
```python
	_theOutlet = objc.IBOutlet()
```

... and start the respective UI action method (e.g., an action triggered by a button) with `@objc.IBAction`:
```python
	@objc.IBAction
	def buttonPressed_( self, sender ):
		print "The button was pressed!"
```

Then, still in Xcode, add the .py file with *File > Add Files...*. When you are done, and every time the `.xib` file is changed, it has to be compiled to a `.nib` file. Do so with this Terminal command:
`ibtool xxx.xib --compile xxx.nib`.

If this looks confusing at first, do not worry. You will find detailed step-by-step instructions in the comments of the .py file. And for a quick introduction to using Interface Builder with the PyObjC bridge, read:
http://blog.adamw523.com/os-x-cocoa-application-python-pyobjc/
