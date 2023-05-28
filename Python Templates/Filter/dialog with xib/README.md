Welcome to Glyphs.app’s plug-in documentation! This document covers only some details of the process. If you are new to the subject, we recommend you start with [reading our tutorial](https://glyphsapp.com/tutorials/plugins), which points you back here at the appropriate moment.

## Filter Plug-in with Dialog

The filter plug-in (with dialog) gets called either from the Filter menu, or through Custom Parameters upon font export.

![](../_Readme_Images/filterwithdialog.png)

This is how you call the filter through Custom Parameters:
In the font’s Info dialog, for each *instance* add a `Custom Parameter` called `Filter`. 

The value should contain a semicolon-separated list of the following:
- The plug-in name (by its Python class name, so `____PluginClassName____` in the virgin plug-in)
- `include`: A list of glyphs to exercise the filter on. Only these glyphs will be used.
- `exclude`: A list of glyphs to exclude from the filter. All glyphs of the font except those will be used.
- Any other custom parameter of your choice in the `key:value` format.

If neither of the two `include`/`exclude` statements are provided, the Filter will be applied to all glyphs in the font.

![](../_Readme_Images/filterwithoutdialogcustomparameter.png)


# User code

A functional plug-in can be as small as this (in `Contents/Resources/plugin.py`):

```python
# encoding: utf-8
from __future__ import division, print_function, unicode_literals
from GlyphsApp.plugins import *

class ____PluginClassName____(FilterWithDialog):

	# Definitions of IBOutlets
	
	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()

	# Text field in dialog
	myTextField = objc.IBOutlet()
	
	@objc.python_method
	def settings(self):
		self.menuName = 'My Filter'
		self.loadNib('IBdialog')

	# On dialog show
	@objc.python_method
	def start(self):

		# Set default setting if not present
		if not Glyphs.defaults['com.myname.myfilter.value']:
			Glyphs.defaults['com.myname.myfilter.value'] = 15.0

		# Set value of text field
		self.myTextField.setFloatValue_(Glyphs.defaults['com.myname.myfilter.value'])
		
		# Set focus to text field
		self.myTextField.becomeFirstResponder()

	# Action triggered by UI
	@objc.IBAction
	def setValue_(self, sender):

		# Store value coming in from dialog
		Glyphs.defaults['com.myname.myfilter.value'] = sender.floatValue()

		# Trigger redraw of preview
		self.preview()

	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		
		# Called on font export, get value from customParameters
		if 'shift' in customParameters:
			value = customParameters['shift']

		# Called through UI, use stored value
		else:
			value = Glyphs.defaults['com.myname.myfilter.value']

		# Shift all nodes in x and y direction by the value
		for path in layer.paths:
			for node in path.nodes:
				node.position = NSPoint(node.position.x + value, node.position.y + value)
```


From there you can add the following methods:

#### settings()

In this method you set all attributes that describe the plug-in and need to be loaded when the app starts, such as its name or, optionally, a keyboard shortcut.

```python
	@objc.python_method
	def settings(self):

		# The name as it will appear in the Filter menu
		# You may use a simple string or Glyphs.localize() for localizations (see http://docu.glyphsapp.com#localize)
		self.menuName = Glyphs.localize({'en': u'My Filter', 'de': u'Mein Filter'})

		# A keyboard shortcut for activating/deactivating the plug-in (together with Command+Shift)
		self.keyboardShortcut = 'p'
		# Set any combination of NSShiftKeyMask | NSControlKeyMask | NSCommandKeyMask | NSAlternateKeyMask
		self.keyboardShortcutModifier = NSControlKeyMask | NSShiftKeyMask

		# The caption of the action button of the dialog. 'Apply' is the default.
		self.actionButtonLabel = 'Apply'

		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog')

```


#### start()

This method gets called when the plug-in gets initialized when the user invokes your plug-in through the menu or a keyboard shortcut, and the dialog gets displayed. You put all your initialization code here.

```python
	@objc.python_method
	def start(self):

		# Your init code goes here...
```

#### filter()

This is the main method that should contain your code to be executed on the glyphs. The actual filter.

- The argument `layer` will contain a `GSLayer` object to deal with.
- The argument `inEditView` is a boolean (`True`/`False`) and describes whether or not the user has called the filter through the filter menu while editing a single glyph in the Edit View.
- The argument `customParameters` contains a dictionary of values that came through the `Custom Parameters` field upon font export (other than the filter name and include/exclude statements). If these values were not defined in `key:value` format, but only `value` without a value name, the dictionary will contain integers starting with `0` as keys. You may use `len(customParameters)` to get hold of these keys for looping.

So there are three scenarios to consider:

##### 1. Call through Filter menu in Edit View

The user is editing a glyph in the Edit View and has clicked on the filter in the Filter menu.
`inEditView` will be set to `True` and `customParameters` will be empty and the `filter()` method will be called only once.

In this scenario, you could pay attention to what objects the user has selected in the Edit View using either `GSLayer.selection` (all objects such as paths, components, anchors) or the selectable object’s individual `.selected` attribute.

##### 2. Call through Filter menu in Font View

The user has selected several glyphs in the Font View and has clicked on the filter in the Filter menu.
`inEditView` will be set to `False` and `customParameters` will be empty and the `filter()` method will be called several times, each time containing a different `layer`.

##### 3. Call through Custom Parameters upon font export

The user is exporting a font whose instances contain Custom Parameters that call the plug-in.
`inEditView` will be set to `False` and `customParameters` will contain any custom parameter (other than the plug-in name, include and exclude statements) that the user has specified in the parameters. You will need to educate the users of your plug-in about what these parameters should look like. The `filter()` method will be called several times according to the results of the include/exclude statements, each time containing a different `layer`.

```python
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		
		# Apply your filter code here
```

#### generateCustomParameter()

If this method is implemented, the filter dialog will show a small gear icon in the lower left corner of the dialog. Upon click a menu will appear that will let you copy a string (returned by this method) to the clipboard describing the plug-in and the currently chosen values (in the dialog). These are the values needed to define Custom Parameters for the font’s instances to apply the filter on font export. You may paste this string directly into the Custom Parameters field as described below:

Copy Custom Parameters:

![](../_Readme_Images/filterwithdialog_copycustomparameters.png)

Paste into Custom Parameters field:

![](../_Readme_Images/filterwithdialog_pastecustomparameters.png)

```python
	@objc.python_method
	def generateCustomParameter(self):

		# Copy plug-in name (by its class name) with a 'shift' value
		return "%s; shift:%s;" % (self.__class__.__name__, Glyphs.defaults['com.myname.myfilter.value'])
```

# Other useful methods

#### update()

This method will display the original glyph as a background image and apply your custom `filter()` method.

This already happens directly after you activate the filter through the menu, and you should call the `update()` method each time the user changes the value in the dialog. Therefore, it makes sense to place it in whichever method receives the actions from the dialog (which is `setValue_()` in the example).

```python
	# Action triggered by UI
	@objc.IBAction
	def setValue_(self, sender):
		
		# Store value coming in from dialog
		Glyphs.defaults['com.myname.myfilter.value'] = sender.floatValue()

		# Trigger redraw of preview
		self.update()
```
# Use Vanilla for the dialog view

The sample code uses Xcode for the dialog, but you may use [Vanilla](https://vanilla.robotools.dev/en/) instead. Here is how:

As opposed to Xcode, dialogs get created entirely in code only using Vanilla, which might be advantageous for you if Xcode looks too daunting.

We need to create a so called [Group](https://vanilla.robotools.dev/en/latest/objects/Group.html) that contains a set of objects. Of this group, we can get hold of the wrapped `NSView` object to display in Glyphs. Note that due to Vanilla internals, we have to create a window first, although that window isn’t getting any attention anymore later on, and it must contain a `Group()` of the same size. Note that stretching the `Group` to the far corners of the windows using `(0, 0, -0, -0)` may not work, so explicitly define its size identical to the containing window.

Make sure that the .dialog gets defined in the `settings()` class, not at the class root.
Also, you may delete the two `IBdialog.xib/.nib` files from the `Resources` folder of the plug-in.


```python
# encoding: utf-8
from __future__ import division, print_function, unicode_literals
from GlyphsApp.plugins import *
from vanilla import *

class ____PluginClassName____(SelectTool):

	@objc.python_method
	def settings(self):
		self.name = 'My Select Tool'

		# Create Vanilla window and group with controls
		width = 150
		height = 80
		self.paletteView = Window((width, height))
		self.paletteView.group = Group((0, 0, width, height))
		self.paletteView.group.text = TextBox((10, 10, -10, 20), 'x/y shift')
		self.paletteView.group.editText = EditText((10, 35, 50, 25), callback = self.editTextCallback, continuous = False)

		# Set dialog to NSView
		self.dialog = self.paletteView.group.getNSView()

	# On dialog show
	@objc.python_method
	def start(self):

		# Set default setting if not present
		if not Glyphs.defaults['com.myname.myfilter.value']:
			Glyphs.defaults['com.myname.myfilter.value'] = 15.0

		# Set value of text field
		self.paletteView.group.editText.set(Glyphs.defaults['com.myname.myfilter.value'])

	# Action triggered by UI
	@objc.python_method
	def editTextCallback(self, sender):

		# Store value coming in from dialog
		Glyphs.defaults['com.myname.myfilter.value'] = sender.get()

		# Trigger redraw
		self.update()
```
