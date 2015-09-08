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

##### Plugin update mechanism

Glyphs provides automatic update checks and notifications (not automatic installation) for installed plugins and will notify users in the user interface when a new version is available. It will once per day (or upon click in the preferences) check a URL that must contain a xml file very similar (or even identical) to this here Info.plist. This online xml file must contain at least the two fields `CFBundleVersion` and `productPageURL`. `CFBundleVersion` is checked against the installed plugin's version on the user's computer, and when a newer version is detected, the user may click to be directed to the URL given in `productPageURL` in the browser where he can download the new plugin.

In `UpdateFeedURL`, replace `____OnlineUrlToThisPlist____` with a deep link to this .plist file. This file can be your GitHub repository, or elsewhere. In `productPageURL`, replace `____ProductPageURL____` with a web page URL for the plugin. This can be your GitHub repository page or elsewhere. Finally, in `productReleaseNotes`, you may provide a short description of your latest changes, e.g., ‘New option X’. This will be displayed when the user checks for updates in the app preferences, and will motivate your users to keep your plugins up to date.

###### Dynamic version information

If you operate your own software distribution system, like an online shop, you can have your server output this Info.plist with dynamic information about the latest version of the plugin, instead of keeping the online Info.plist manually up to date. Please make sure that the file is delivered in the `application/xml` MIME-type.

Glyphs will add the URL parameters `glyphsUniqueID` (an anonymous ID identifiying unique Glyphs installations on people's computer's) and `glyphsVersion` (the Build number of that Glyphs installation) to the update check call (planned but not yet implemented: `pluginVersion` describing the version of your plugin installed within the user's Glyphs installation). You can use this information to keep anonymous track of the number of plugin installations out there and their version information and level of adoption.

Automagically (or, as it should), the interface language of Glyphs makes its way into the update check call via the HTTP headers. Therefore, you may choose to provide the `productReleaseNotes` in various languages.

A live example of all of this can be found for Yanone’s Speed Punk, with `productReleaseNotes` provided in English and German (if you click the following link here in your browser, your browser will send the preferred languages via the HTTP headers): https://yanone.de/buy/?page=versionInformation&product=speedpunkglyphs&format=GlyphsInfoPlist


#### Edit the boot file

In the last line of `Contents/Resources/__boot__.py`, the file name (`____PluginFileName____`), this time *with* the `.py` extension, must be mentioned.

#### Rename the MacOS executable

Rename `Contents/MacOS/____PluginFileName____`. Make sure it is exactly in sync with the `CFBundleExecutable` value in Info.plist, and with the name of the core Python file (except for the .py suffix). See below.

#### Rename and edit the core Python file

`Contents/Resources/____PluginFileName____.py` is where your actual code goes. Rename the file, and open it. You will find extensive step-by-step instructions in the comments. Have fun.

### Installing and debugging

To install a plugin, move it into the Plugins folder inside the Application Support folder of Glyphs (double click the plugin to let Glyphs do that for you). You can edit your code right there, but you need to restart the application for any changes to take effect.

Tip: right-click the Glyphs.app Dock icon, force quit it, and restart immediately with a click on the Dock icon. This will also immediately re-open any windows (you had open before the force quit) to their last state.

## Interface Builder: Adding GUI elements

The interaction between your Python script and a graphical user interface (GUI) requires the use of Interface Builder, which is part of Apple’s XCode software development environment. The work with Interface Builder can be a bit daunting, but we’ve written a step-by-step walkthrough here for you that will get you going quickly. After your first completed GUI interaction, using it will become as natural as all the rest.

Your Python code communicates with the UI through:
- **IBOutlets** *(.py->GUI)*: Make UI elements available to your Python code. Then your code can change these elements (like the caption of a text field)
- **IBActions** *(GUI->.py)*: Call methods in the Python code from actions in the UI (like the click of a button)

The two sample plugins here that use a UI, `File format` and `Filter with dialog`, are small functional plugins that make use of both IBOutlets and IBActions.

##### 1. IBOutlets: Make UI elements available to Python 

At the root of the plugin class, you define variables that will be linked to UI elements. In this example, we want to attach the `NSView` object (the *Custom View* window pane from Interface Builder) to the variable `settings_view`. (Glyphs then accesses the NSView object found in this variable through the function `exportSettingsView()`.

```python
class CSVFileExport (NSObject, GlyphsFileFormatProtocol):
	settings_view = objc.IBOutlet()
```

##### 2. IBActions: Let UI elements trigger Python functions

Functions to be triggered from the UI get defined by a `@objc.IBAction` just before the function definition.
The function names need to end with an underscore, e.g. `setValue_()`.

```python
	@objc.IBAction
	def setExportUnicode_(self, sender):
		self.exportUnicode = sender.intValue()
		self.updateFeedBackTextField()
```

##### 3. Interface Builder

![](_Readme_Images/IB_Overview.png)

- Open the .xib file in XCode, and add and arrange interface elements
- Add this .py file via *File > Add Files...* for Xcode to recognize all IBOutlets and IBActions
- In the left sidebar, choose *Placeholders > File's Owner*, in the right sidebar, open the *Identity inspector* (3rd icon), and put the name of this controller class in the *Custom Class > Class* field
- The first **IBOutlet**, the main window pane: Ctrl-drag from the *File's Owner* to the window pane (called *Custom View*) either in the graphical arrangement or in the list on the left, then choose `settings_view` from the pop-up list, to establish the connection between the Python variable and the main NSView object

![](_Readme_Images/IB_DragConnection.png)

- Other **IBOutlets**: Ctrl-drag from the *File's Owner* to a UI element (e.g. text field), and choose which outlet shall be linked to the UI element
- **IBActions**: Ctrl-drag from a UI element (e.g. button) to the *File’s Owner* in the left sidebar, and choose the function that the UI element is supposed to trigger
- In the left-side objects side bar choose *Custom View*, and in the right-side pane choose *Attributes inspector* (4th icon), and deactivate *Translate Mask Into Constraints*. Don't ask, just do it.

All the back and forth relations between the UI and your Python code can be reviewed in the *Connection inspector* (6th icon on the right).

![](_Readme_Images/IB_Connections.png)


##### 4. Compile .xib to .nib

As a last step, you need to compile the .xib file to a .nib file with this *Terminal* command: `ibtool xxx.xib --compile xxx.nib`.
Please note: Every time the .xib is changed, it has to be **recompiled** to a .nib. 

##### 5. Troubleshooting and debugging

Check *Console.app* for error messages to see if everything went right.
You can also output your own debug code to *Console.app* using the plugin's own `self.logToConsole()` function.

##### Further reading

For a quick introduction to using Interface Builder with the PyObjC bridge, read http://blog.adamw523.com/os-x-cocoa-application-python-pyobjc/

For the complete reference for the UI elements, see Apple's AppKit Framework Reference: https://developer.apple.com/library/mac/documentation/Cocoa/Reference/ApplicationKit/ObjC_classic/index.html
