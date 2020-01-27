# encoding: utf-8

from __future__ import print_function

import objc, time, math, sys, os, re, traceback, copy, datetime

from Foundation import NSObject, NSString, NSArray, NSMutableArray, NSMutableDictionary, NSDictionary, NSNumber, NSConcreteValue, \
	NSClassFromString, NSUserDefaults, NSURL, NSNotificationCenter, NSMakePoint, NSNotFound, NSAttributedString, \
	NSMutableAttributedString, NSLog, NSBundle, NSAffineTransform, NSPoint, NSRect, NSRange, NSUserNotification, \
	NSUserNotificationCenter, NSDate, NSIndexSet
from AppKit import NSApp, NSDocumentController, NSOpenPanel, NSSavePanel, NSOKButton, NSWorkspace, \
	NSMenuItem, NSOnState, NSOffState, NSMixedState, NSColor

GSAlignmentZone = objc.lookUpClass("GSAlignmentZone")
GSAnchor = objc.lookUpClass("GSAnchor")
GSAnnotation = objc.lookUpClass("GSAnnotation")
GSApplication = objc.lookUpClass("GSApplication")
GSBackgroundImage = objc.lookUpClass("GSBackgroundImage")
GSBackgroundLayer = objc.lookUpClass("GSBackgroundLayer")
GSClass = objc.lookUpClass("GSClass")
GSComponent = objc.lookUpClass("GSComponent")
GSControlLayer = objc.lookUpClass("GSControlLayer")
GSCustomParameter = objc.lookUpClass("GSCustomParameter")
GSDocument = objc.lookUpClass("GSDocument")
GSProjectDocument = objc.lookUpClass("GSProjectDocument")
GSEditViewController = objc.lookUpClass("GSEditViewController")
GSElement = objc.lookUpClass("GSElement")
GSFeature = objc.lookUpClass("GSFeature")
GSFeaturePrefix = objc.lookUpClass("GSFeaturePrefix")
GSFont = objc.lookUpClass("GSFont")
GSFontMaster = objc.lookUpClass("GSFontMaster")
GSGlyph = objc.lookUpClass("GSGlyph")
GSGlyphInfo = objc.lookUpClass("GSGlyphInfo")
GSGlyphsInfo = objc.lookUpClass("GSGlyphsInfo")
GSGuideLine = objc.lookUpClass("GSGuideLine")
GSHint = objc.lookUpClass("GSHint")
GSInstance = objc.lookUpClass("GSInstance")
GSLayer = objc.lookUpClass("GSLayer")
GSNode = objc.lookUpClass("GSNode")
GSPath = objc.lookUpClass("GSPath")
GSSubstitution = objc.lookUpClass("GSSubstitution")
GSPartProperty = objc.lookUpClass("GSPartProperty")
MGOrderedDictionary = objc.lookUpClass("MGOrderedDictionary")
GSNotifyingDictionary = objc.lookUpClass("GSNotifyingDictionary")
GSPathFinder = objc.lookUpClass("GSPathOperator")
GSPathPen = objc.lookUpClass("GSPathPen")
GSCallbackHandler = objc.lookUpClass("GSCallbackHandler")
GSInterpolationFontProxy = objc.lookUpClass("GSInterpolationFontProxy")
GSFeatureGenerator = objc.lookUpClass("GSFeatureGenerator")
GSTTStem = objc.lookUpClass("GSTTStem")


__all__ = [

	"Glyphs", "GetFile",
	"wrapperVersion",
	"GSAlignmentZone", "GSAnchor", "GSAnnotation", "GSApplication", "GSBackgroundImage", "GSBackgroundLayer", "GSClass", "GSComponent", "GSControlLayer", "GSCustomParameter", "GSDocument", "GSProjectDocument", "GSEditViewController", "GSElement", "GSFeature", "GSFeaturePrefix", "GSFont", "GSFontMaster", "GSGlyph", "GSGlyphInfo", "GSGlyphsInfo", "GSGuideLine", "GSHint", "GSInstance", "GSLayer", "GSNode", "GSPath", "GSSubstitution", "GSPartProperty", "GSNotifyingDictionary", "GSPathFinder", "GSPathPen", "GSCallbackHandler", "GSFeatureGenerator", "GSTTStem",
	# Constants
	"MOVE", "LINE", "CURVE", "OFFCURVE", "QCURVE", "GSMOVE", "GSLINE", "GSCURVE", "GSOFFCURVE", "GSSHARP", "GSSMOOTH",
	"TAG", "TOPGHOST", "STEM", "BOTTOMGHOST", "FLEX", "TTANCHOR", "TTSTEM", "TTALIGN", "TTINTERPOLATE", "TTDIAGONAL", "TTDELTA", "CORNER", "CAP", "TTDONTROUND", "TTROUND", "TTROUNDUP", "TTROUNDDOWN", "TRIPLE",
	"TEXT", "ARROW", "CIRCLE", "PLUS", "MINUS",
	"LTR", "RTL", "LTRTTB", "RTLTTB", "GSTopLeft", "GSTopCenter", "GSTopRight", "GSCenterLeft", "GSCenterCenter", "GSCenterRight", "GSBottomLeft", "GSBottomCenter", "GSBottomRight",

	"OTF", "TTF", "VARIABLE", "UFO", "WOFF", "WOFF2", "PLAIN", "EOT",

	# Methods
	"divideCurve", "distance", "addPoints", "subtractPoints", "GetFolder", "GetSaveFile", "GetOpenFile", "Message", "LogToConsole", "LogError", "removeOverlap", "subtractPaths", "intersectPaths", "scalePoint",

	# Classes
	"GSSmartComponentAxis",

	# Menus
	"APP_MENU", "FILE_MENU", "EDIT_MENU", "GLYPH_MENU", "PATH_MENU", "FILTER_MENU", "VIEW_MENU", "SCRIPT_MENU", "WINDOW_MENU", "HELP_MENU",
	"ONSTATE", "OFFSTATE", "MIXEDSTATE",

	# Callbacks:

	"DRAWFOREGROUND", "DRAWBACKGROUND", "DRAWINACTIVE", "DOCUMENTOPENED", "DOCUMENTACTIVATED", "DOCUMENTWASSAVED", "DOCUMENTEXPORTED", "DOCUMENTCLOSED", "TABDIDOPEN", "TABWILLCLOSE", "UPDATEINTERFACE", "MOUSEMOVED",
	]


wrapperVersion = "2.5"


# Should help with making plugins backward compatible when they are prepared for Python3 already.
try:
	from objc import python_method
except ImportError:
	def python_method(arg):
		return arg
	objc.python_method = python_method


def _______________________(): pass
def ____CONSTANTS____(): pass





GSMOVE_ = 17
GSLINE_ = 1
GSCURVE_ = 35
GSQCURVE_ = 36
GSOFFCURVE_ = 65
GSSHARP = 0
GSSMOOTH = 100

GSMOVE = "move"
GSLINE = "line"
GSCURVE = "curve"
GSQCURVE = "qcurve"
GSOFFCURVE = "offcurve"

MOVE = "move"
LINE = "line"
CURVE = "curve"
QCURVE = "qcurve"
OFFCURVE = "offcurve"

TAG = -2
TOPGHOST = -1
STEM = 0
BOTTOMGHOST = 1
FLEX = 2
TTANCHOR = 3
TTSTEM = 4
TTALIGN = 5
TTINTERPOLATE = 6
TTDIAGONAL = 8
TTDELTA = 9
CORNER = 16
CAP = 17

TTDONTROUND = 4
TTROUND = 0
TTROUNDUP = 1
TTROUNDDOWN = 2
TRIPLE = 128

# annotations:
TEXT = 1
ARROW = 2
CIRCLE = 3
PLUS = 4
MINUS = 5

OTF = "OTF"
TTF = "TTF"
VARIABLE = "variable"
UFO = "UFO"
WOFF = "WOFF"
WOFF2 = "WOFF2"
PLAIN = "plain"
EOT = "EOT"

# Reverse lookup for __repr__
hintConstants = {
	-2: 'Tag',
	-1: 'TopGhost',
	0: 'Stem',
	1: 'BottomGhost',
	2: 'TTAnchor',
	3: 'TTStem',
	4: 'TTAlign',
	5: 'TTInterpolate',
	6: 'TTDiagonal',
	7: 'TTDelta',
	16: 'Corner',
	17: 'Cap',
}


GSTopLeft = 6
GSTopCenter = 7
GSTopRight = 8
GSCenterLeft = 3
GSCenterCenter = 4
GSCenterRight = 5
GSBottomLeft = 0
GSBottomCenter = 1
GSBottomRight = 2


# Writing direction
LTR = 0
RTL = 1
LTRTTB = 3
RTLTTB = 2

# Callbacks
DRAWFOREGROUND = "DrawForeground"
DRAWBACKGROUND = "DrawBackground"
DRAWINACTIVE = "DrawInactive"
DOCUMENTOPENED = "GSDocumentWasOpenedNotification"
DOCUMENTACTIVATED = "GSDocumentActivateNotification"
DOCUMENTWASSAVED = "GSDocumentWasSavedSuccessfully"
DOCUMENTEXPORTED = "GSDocumentWasExportedNotification"
DOCUMENTCLOSED = "GSDocumentCloseNotification"
TABDIDOPEN = "TabDidOpenNotification"
TABWILLCLOSE = "TabWillCloseNotification"
UPDATEINTERFACE = "GSUpdateInterface"
MOUSEMOVED = "mouseMovedNotification"
MOUSEDOWN = "mouseDownNotification"
MOUSEUP = "mouseUpNotification"

# Menus
APP_MENU = "APP_MENU"
FILE_MENU = "FILE_MENU"
EDIT_MENU = "EDIT_MENU"
GLYPH_MENU = "GLYPH_MENU"
PATH_MENU = "PATH_MENU"
FILTER_MENU = "FILTER_MENU"
VIEW_MENU = "VIEW_MENU"
SCRIPT_MENU = "SCRIPT_MENU"
WINDOW_MENU = "WINDOW_MENU"
HELP_MENU = "HELP_MENU"

ONSTATE = NSOnState
OFFSTATE = NSOffState
MIXEDSTATE = NSMixedState





'''


Changes in the API
==================

These changes could possibly break your code, so you need to keep track of them. Please see :attr:`GSApplication.versionNumber` for how to check for the app version in your code. Really, read it. There’s a catch.


--------------------
Major Changes in 2.5
--------------------

	- Add pointPen capabilities to `GSPathPen`
	- Add setter for :meth:`GSFont.selection`
	- Add :attr:`GSFont.axes`, :attr:`GSFontMaster.axes` and  :attr:`GSInstance.axes`
	- Add :attr:`GSLayer.componentLayer`
		The :class:`GSLayer` the component is pointing to. This is read-only. In order to change the referenced base glyph, set :attr:`GSComponent.componentName` to the new glyph name.
		For Smart Components, the `componentLayer` contains the interpolated result.
	- Add :meth:`GSInstance.generate(UFO)`
	- Add :meth:`GSFont.export()`
		This allows to export Variable fonts
	- Add :attr:`GSGlyph.unicodes`

--------------------
Major Changes in 2.3
--------------------

.. attribute:: *.bezierPath

We've created a distinct ``.bezierPath`` attribute for various objects (paths, components, etc.) to use to draw in plug-ins, over-writing the previous (and never documented) `.bezierPath()` method (from the Python-ObjC-bridge) by the same name that handed down an `NSBezierPath` object.

Old: ``.bezierPath()``

New: ``.bezierPath``

--------------------
Major Changes in 2.2
--------------------

.. attribute:: GSLayer.selection

We've created a distinct ``.selection`` attribute for the layer object that contains all items (paths, components etc. selected by the user in the UI), overwriting the previous `.selection()` method (from the PyObjC bridge).

Old: ``.selection()``

New: ``.selection``
'''


def GSObject__copy__(self, memo=None):
	return self.copy()

def GSObject__new__(typ, *args, **kwargs):
	return typ.alloc().init()

class Proxy(object):
	def __init__(self, owner):
		self._owner = owner
	def __repr__(self):
		"""Return list-lookalike of representation string of objects"""
		strings = []
		for currItem in self:
			strings.append("%s" % (currItem))
		return "(%s)" % (',\n'.join(strings))
	def __len__(self):
		Values = self.values()
		if Values is not None:
			return len(Values)
		return 0
	def pop(self, i):
		if type(i) == int:
			node = self[i]
			del self[i]
			return node
		else:
			raise(KeyError)
	def __iter__(self):
		Values = self.values()
		if Values is not None:
			for element in Values:
				yield element
	def index(self, Value):
		return self.values().index(Value)
	def __copy__(self):
		return list(self)
	def __deepcopy__(self, memo):
		return [x.copy() for x in self.values()]

	def setter(self, values):
		method = self.setterMethod()
		if isinstance(values, (list, NSArray)):
			method(NSMutableArray.arrayWithArray_(values))
		elif isinstance(values, (tuple, type(self))):
			method(NSMutableArray.arrayWithArray_(list(values)))
		elif values is None:
			method(NSMutableArray.array())
		else:
			raise TypeError


##################################################################################
#
#
#
#           GSApplication
#
#
#
##################################################################################

def _______________________(): pass
def ____GSApplication____(): pass
def _______________________(): pass


Glyphs = NSApp()


'''
:mod:`GSApplication`
===============================================================================

The mothership. Everything starts here.

.. code-block:: python

	print(Glyphs)

.. code-block:: python

	<Glyphs.app>


.. class:: GSApplication()

	Properties

	.. autosummary::

		font
		fonts
		reporters
		activeReporters
		filters
		defaults
		scriptAbbreviations
		scriptSuffixes
		languageScripts
		languageData
		unicodeRanges
		editViewWidth
		handleSize
		versionString
		versionNumber
		buildNumber
		menu

	Functions

	.. autosummary::

		open()
		showMacroWindow()
		clearLog()
		showGlyphInfoPanelWithSearchString()
		glyphInfoForName()
		glyphInfoForUnicode()
		niceGlyphName()
		productionGlyphName()
		ligatureComponents()
		addCallback()
		removeCallback()
		redraw()
		showNotification()
		localize()
		activateReporter()
		deactivateReporter()

	
	**Properties**
'''
GSApplication.currentDocument = property(lambda self: NSApp().currentFontDocument())

GSApplication.documents = property(lambda self: AppDocumentProxy(self))

def Glyphs__repr__(self):
	return '<Glyphs.app>'
GSApplication.__repr__ = python_method(Glyphs__repr__)

def currentFont():
	try:
		doc = NSApp().currentFontDocument()
		return doc.font
	except AttributeError:
		pass
	return None

# by Yanone
GSApplication.font = property(lambda self: currentFont())

'''
	.. attribute:: font

	:return: The active :class:`GSFont` object or None.
	:rtype: :class:`GSFont`

	.. code-block:: python

		# topmost open font
		font = Glyphs.font

'''



GSApplication.fonts = property(lambda self: AppFontProxy(self))


'''
	.. attribute:: fonts

	:return: All open :class:`fonts <GSFonts>`.

	.. code-block:: python

		# access all open fonts
		for font in Glyphs.fonts:
			print(font.familyName)

		# add a font

		font = GSFont()
		font.familyName = "My New Fonts"
		Glyphs.fonts.append(font)

'''

GSApplication.reporters = property(lambda self: GSCallbackHandler.sharedHandler().reporterInstances().allValues())

'''
	.. attribute:: reporters

	List of available reporter plug-ins (same as bottom section in the 'View' menu). These are the actual objects. You can get hold of their names using `object.__class__.__name__`.

	Also see :meth:`GSApplication.activateReporter()` and :meth:`GSApplication.deactivateReporter()` methods below to activate/deactivate them.

	.. code-block:: python

		# List of all reporter plug-ins
		print(Glyphs.reporters)

		# Individual plug-in class names
		for reporter in Glyphs.reporters:
			print(reporter.__class__.__name__)

		# Activate a plugin
		Glyphs.activateReporter(Glyphs.reporters[0]) # by object
		Glyphs.activateReporter('GlyphsMasterCompatibility') # by class name

	.. versionadded:: 2.3
'''

GSApplication.activeReporters = property(lambda self: GSCallbackHandler.activeReporters())

'''
	.. attribute:: activeReporters
	
	List of activated reporter plug-ins.

	.. versionadded:: 2.3
'''

GSApplication.filters = property(lambda self: NSApp.delegate().filterInstances())

'''
	.. attribute:: filters

	List of available filters (same as 'Filter' menu). These are the actual objects.

	Below sample code shows how to get hold of a particular filter and use it. You invoke it using the `processFont_withArguments_()` function for old plugins, or the `filter()` function for newer plugins.
	As arguments you use the list obtained by clicking on 'Copy Custom Parameter' button in the filter’s dialog (gear icon) and convert it to a list.
	In the `include` option you can supply a comma-separated list of glyph names.
	Here's a catch: old plugins will only run on the first layer of a glyph, because the function `processFont_withArguments_()` was designed to run on instances upon export that have already been reduced to one layer. You can work around that by changing the order of the layers, then changing them back (not shown in the sample code).

	.. code-block:: python

		# Helper function to get filter by its class name
		def filter(name):
			for filter in Glyphs.filters:
				if filter.__class__.__name__ == name:
					return filter

		# Get the filter
		offsetCurveFilter = filter('GlyphsFilterOffsetCurve')

		# Run the filter (old plugins)
		# The arguments came from the 'Copy Custom Parameter' as:
		# Filter = "GlyphsFilterOffsetCurve;10;10;1;0.5;"
		offsetCurveFilter.processFont_withArguments_(font, ['GlyphsFilterOffsetCurve', '10', '10', '1', '0.5', 'include:%s' % glyph.name])

		# If the plugin were a new filter, the same call would look like this:
		# (run on a specific layer, not the first layer glyphs in the include-list)
		# The arguments list is a dictionary with either incrementing integers as keys or names (as per 'Copy Custom Parameter' list)
		offsetCurveFilter.filter(layer, False, {0: 10, 1: 10, 2: 1, 3: 0.5})

	.. versionadded:: After 2.4.2

'''

if sys.version_info[0] == 2:
	STR_TYPES = (str, unicode, objc.pyobjc_unicode)
else:
	STR_TYPES = (str, objc.pyobjc_unicode)

def isString(string):
	return isinstance(string, STR_TYPES)

def objcObject(pyObject):
	if isinstance(pyObject, (str, unicode)):
		return NSString.stringWithString_(pyObject)
	if isinstance(pyObject, int):
		return NSNumber.numberWithInt_(pyObject)
	if isinstance(pyObject, float):
		return NSNumber.numberWithFloat_(pyObject)
	if isinstance(pyObject, list):
		array = NSMutableArray.array()
		for value in pyObject:
			array.addObject_(objcObject(value))
		return array
	if isinstance(pyObject, dict):
		dictionary = NSMutableDictionary.dictionary()
		for key, value in pyObject.viewitems():
			dictionary.setObject_forKey_(objcObject(value), objcObject(key))
		return dictionary
	return pyObject

class DefaultsProxy(Proxy):
	def __getitem__(self, Key):
		return NSUserDefaults.standardUserDefaults().objectForKey_(Key)
	def __setitem__(self, Key, Value):
		if Value is not None:
			NSUserDefaults.standardUserDefaults().setObject_forKey_(Value, Key)
		else:
			NSUserDefaults.standardUserDefaults().removeObjectForKey_(Key)
	def __delitem__(self, Key):
		NSUserDefaults.standardUserDefaults().removeObjectForKey_(Key)
	def __repr__(self):
		return "<Userdefaults>"

GSApplication.defaults = property(lambda self: DefaultsProxy(self))

def __registerDefault__(self, defaults, values=None):
	if defaults is not None and values is not None and len(defaults) > 2:
		NSUserDefaults.standardUserDefaults().registerDefaults_({defaults: values})
	elif defaults and not values:
		NSUserDefaults.standardUserDefaults().registerDefaults_(defaults)
	else:
		raise KeyError
GSApplication.registerDefault = __registerDefault__

def __registerDefaults__(self, defaults):
	if defaults is not None:
		NSUserDefaults.standardUserDefaults().registerDefaults_(defaults)
	else:
		raise ValueError
GSApplication.registerDefaults = __registerDefaults__

# TODO: docu for registerDefaults

'''
	.. attribute:: defaults

	A dict like object for storing preferences. You can get and set key-value pairs.

	Please be careful with your keys. Use a prefix that uses the reverse domain name. e.g. "com.MyName.foo.bar".

	.. code-block:: python

		# Check for whether or not a preference exists, because has_key() doesn't work in this PyObjC-brigde
		if Glyphs.defaults["com.MyName.foo.bar"] is None:
			# do stuff

		# Get and set values
		value = Glyphs.defaults["com.MyName.foo.bar"]
		Glyphs.defaults["com.MyName.foo.bar"] = newValue

		# Remove value
		# This will restore the default value
		del(Glyphs.defaults["com.MyName.foo.bar"])

	'''


class BoolDefaultsProxy(DefaultsProxy):
	def __getitem__(self, Key):
		return NSUserDefaults.standardUserDefaults().boolForKey_(Key)
	def __setitem__(self, Key, Value):
		if Value is not None:
			NSUserDefaults.standardUserDefaults().setBool_forKey_(Value, Key)
		else:
			NSUserDefaults.standardUserDefaults().removeObjectForKey_(Key)

GSApplication.boolDefaults = property(lambda self: BoolDefaultsProxy(self))

class IntDefaultsProxy(DefaultsProxy):
	def __getitem__(self, Key):
		return NSUserDefaults.standardUserDefaults().integerForKey_(Key)
	def __setitem__(self, Key, Value):
		if Value is not None:
			NSUserDefaults.standardUserDefaults().setInteger_forKey_(Value, Key)
		else:
			NSUserDefaults.standardUserDefaults().removeObjectForKey_(Key)

GSApplication.intDefaults = property(lambda self: IntDefaultsProxy(self))

GSApplication.scriptAbbreviations = property(lambda self: GSGlyphsInfo.scriptAbbreviations())
# fixed an typo in the property name. Kept this for compatibility.
def _old_scriptAbbreviations():
	print("The method name has changed. Please use new syntax: Glyphs.scriptAbbreviations")
	return GSGlyphsInfo.scriptAbbreviations()
GSApplication.scriptAbbrevations = property(lambda self: _old_scriptAbbreviations())

'''
	.. attribute:: scriptAbbreviations

	A dictionary with script name to abbreviation mapping, e.g., 'arabic': 'arab'

	:rtype: dict`
	'''

GSApplication.scriptSuffixes = property(lambda self: GSGlyphsInfo.scriptSuffixes())

'''
	.. attribute:: scriptSuffixes

	A dictionary with glyphs name suffixes for scripts and their respective script names, e.g., 'cy': 'cyrillic'

	:rtype: dict`
	'''

GSApplication.languageScripts = property(lambda self: GSGlyphsInfo.languageScripts())

'''
	.. attribute:: languageScripts

	A dictionary with language tag to script tag mapping, e.g., 'ENG': 'latn'

	:rtype: dict`
	'''

GSApplication.languageData = property(lambda self: GSGlyphsInfo.languageData())

'''
	.. attribute:: languageData

	A list of dictionaries with more detailed language informations.

	:rtype: list`
	'''

GSApplication.unicodeRanges = property(lambda self: GSGlyphsInfo.unicodeRanges())

'''
	.. attribute:: unicodeRanges

	Names of unicode ranges.

	:rtype: list`
	'''

def Glyphs_setUserDefaults(self, key, value):
	self.defaults[key] = value


def NSStr(string):
	if string:
		return NSString.stringWithString_(string)
	else:
		return None

GSApplication.editViewWidth = property(lambda self: self.intDefaults["GSFontViewWidth"], lambda self, value: Glyphs_setUserDefaults(self, "GSFontViewWidth", int(value)))
'''
	.. attribute:: editViewWidth

	.. versionadded:: 2.3

	Width of glyph Edit view. Corresponds to the "Width of editor" setting from the Preferences.

	:type: int
'''

GSApplication.handleSize = property(lambda self: self.intDefaults["GSHandleSize"], lambda self, value: Glyphs_setUserDefaults(self, "GSHandleSize", int(value)))
'''
	.. attribute:: handleSize

	.. versionadded:: 2.3

	Size of Bezier handles in Glyph Edit view. Possible value are 0–2. Corresponds to the "Handle size" setting from the Preferences.

	To use the handle size for drawing in reporter plugins, you need to convert the handle size to a point size, and divide by the view's scale factor. See example below.

	.. code-block:: python

		# Calculate handle size
		handSizeInPoints = 5 + Glyphs.handleSize * 2.5 # (= 5.0 or 7.5 or 10.0)
		scaleCorrectedHandleSize = handSizeInPoints / Glyphs.font.currentTab.scale

		# Draw point in size of handles
		point = NSPoint(100, 100)
		NSColor.redColor.set()
		rect = NSRect((point.x - scaleCorrectedHandleSize * 0.5, point.y - scaleCorrectedHandleSize * 0.5), (scaleCorrectedHandleSize, scaleCorrectedHandleSize))
		bezierPath = NSBezierPath.bezierPathWithOvalInRect_(rect)
		bezierPath.fill()

	:type: int
'''


GSApplication.versionString = NSBundle.mainBundle().infoDictionary()["CFBundleShortVersionString"]

'''
	.. attribute:: versionString

	.. versionadded:: 2.3

	String containing Glyph.app's version number. May contain letters also, like '2.3b'. To check for a specific version, use .versionNumber below.

	:type: string
'''


def Glyphs_FloatVersion(self):
	m = re.match(r"(\d+)\.(\d+)", self.versionString)
	return float(str(m.group(1)) + '.' + str(m.group(2)))

GSApplication.versionNumber = property(lambda self: Glyphs_FloatVersion(self))

'''
	.. attribute:: versionNumber

	.. versionadded:: 2.3

	Glyph.app's version number. Use this to check for version in your code.

	Here’s the catch: Since we only added this `versionNumber` attribute in Glyphs v2.3, it is not possible to use this attribute to check for versions of Glyphs older than 2.3. We’re deeply sorry for this inconvenience. Development is a slow and painful process.
	So you must first check for the existence of the `versionNumber` attribute like so:

	.. code-block:: python

		# Code valid for Glyphs.app v2.3 and above:
		if hasattr(Glyphs, 'versionNumber') and Glyphs.versionNumber >= 2.3:
			# do stuff

		# Code for older versions
		else:
			# do other stuff


	:type: float
'''


GSApplication.buildNumber = int(NSBundle.mainBundle().infoDictionary()["CFBundleVersion"])

'''
	.. attribute:: buildNumber

	.. versionadded:: 2.3

	Glyph.app's build number.

	Especially if you're using preview builds, this number may be more important to you than the version number. The build number increases with every released build and is the most significant evidence of new Glyphs versions, while the version number is set arbitrarily and stays the same until the next stable release.

	:type: int
'''


menuTagLookup = {
	APP_MENU: 1,
	FILE_MENU: 3,
	EDIT_MENU: 5,
	GLYPH_MENU: 7,
	PATH_MENU: 9,
	FILTER_MENU: 11,
	VIEW_MENU: 13,
	SCRIPT_MENU: 15,
	WINDOW_MENU: 17,
	HELP_MENU: 19,
}

class AppMenuProxy (Proxy):
	"""Access the main menu."""
	def __getitem__(self, Key):
		if isinstance(Key, int):
			return self._owner.mainMenu().itemAtIndex_(Key)
		elif isString(Key):
			Tag = menuTagLookup[Key]
			return self._owner.mainMenu().itemWithTag_(Tag)
	def values(self):
		return self._owner.mainMenu().itemArray()

GSApplication.menu = property(lambda self: AppMenuProxy(self))

'''
	.. attribute:: menu

	.. versionadded:: 2.3.1-910

	Add menu items to Glyphs’ main menus.

	Following constants for accessing the menus are defined:
	:const:`APP_MENU`, :const:`FILE_MENU`, :const:`EDIT_MENU`, :const:`GLYPH_MENU`, :const:`PATH_MENU`, :const:`FILTER_MENU`, :const:`VIEW_MENU`, :const:`SCRIPT_MENU`, :const:`WINDOW_MENU`, :const:`HELP_MENU`

	.. code-block:: python

		def doStuff(sender):
			# do stuff

		newMenuItem = NSMenuItem('My menu title', doStuff)
		Glyphs.menu[EDIT_MENU].append(newMenuItem)
	'''


NSMenuItem.__new__ = staticmethod(GSObject__new__)

def NSMenuItem__init__(self, title, callback, keyboard="", modifier=0):
	self.setTitle_(title)
	callbackTargets = None
	try:
		callbackTargets = callbackOperationTargets["NSMenuItem"]
	except KeyError:
		callbackTargets = []
		callbackOperationTargets["NSMenuItem"] = callbackTargets
	helper = callbackHelperClass(callback, None)
	callbackTargets.append(helper)
	selector = objc.selector(helper.callback, signature="v@:@")
	self.setAction_(selector)
	self.setTarget_(helper)
	if keyboard != "":
		self.setKeyEquivalent_(keyboard)
		self.setKeyEquivalentModifierMask_(modifier)
NSMenuItem.__init__ = NSMenuItem__init__

def __NSMenuItem__append__(self, item):
	self.submenu().addItem_(item)
NSMenuItem.append = __NSMenuItem__append__

def __NSMenuItem__insert__(self, index, item):
	self.submenu().insertItem_atIndex_(item, index)
NSMenuItem.insert = __NSMenuItem__insert__


'''
	**Functions**
'''

def OpenFont(self, Path, showInterface=True):
	URL = NSURL.fileURLWithPath_(Path)
	Doc = self.openDocumentWithContentsOfURL_display_(URL, showInterface)
	if Doc is not None:
		return Doc.font
	return None

GSApplication.open = OpenFont

'''
	.. function:: open(Path, [showInterface=True])

	Opens a document

	:param Path: The path where the document is located.
	:type Path: str
	:param showInterface: If a document window should be opened. Default: True
	:type showInterface: bool
	:return: The opened document object or None.
	:rtype: :class:`GSFont`
'''

def __ShowMacroWindow(self):
	Glyphs.delegate().showMacroWindow()

GSApplication.showMacroWindow = __ShowMacroWindow

'''
	.. function:: showMacroWindow

	Opens the macro window

	.. function:: clearLog()

	Deletes the content of the console in the macro window

'''


def __showGlyphInfoPanelWithSearchString__(self, String):
	Glyphs.delegate().showGlyphInfoPanelWithSearchString_(String)

GSApplication.showGlyphInfoPanelWithSearchString = __showGlyphInfoPanelWithSearchString__

'''
	.. function:: showGlyphInfoPanelWithSearchString(String)

	Shows the Glyph Info window with a preset search string

	:param String: The search term

'''

def _glyphInfoForName(self, String, font=None):
	if type(String) is int:
		return self.glyphInfoForUnicode(String)
	if font is not None:
		return font.glyphsInfo().glyphInfoForName_(String)
	return GSGlyphsInfo.sharedManager().glyphInfoForName_(String)

GSApplication.glyphInfoForName = _glyphInfoForName

'''
	.. function:: glyphInfoForName(String)

	Generates :class:`GSGlyphInfo` object for a given glyph name.

	:param String: Glyph name
	:param font: if you add a font, and the font has a local glyph info, it will be used instead of the global info data.
	:return: :class:`GSGlyphInfo`
'''

def _glyphInfoForUnicode(self, String, font=None):
	if type(String) is int:
		String = "%04X" % String
	if font is not None:
		return font.glyphsInfo().glyphInfoForUnicode_(String)
	return GSGlyphsInfo.sharedManager().glyphInfoForUnicode_(String)

GSApplication.glyphInfoForUnicode = _glyphInfoForUnicode

'''
	.. function:: glyphInfoForUnicode(Unicode)

	Generates :class:`GSGlyphInfo` object for a given hex unicode.

	:param String: Hex unicode
	:param font: if you add a font, and the font has a local glyph info, it will be used instead of the global info data.
	:return: :class:`GSGlyphInfo`
'''

def _niceGlyphName(self, String, font=None):
	if font is not None:
		return font.glyphsInfo().niceGlyphNameForName_(String)
	return GSGlyphsInfo.sharedManager().niceGlyphNameForName_(String)
GSApplication.niceGlyphName = _niceGlyphName

'''
	.. function:: niceGlyphName(Name)

	Converts glyph name to nice, human-readable glyph name (e.g. afii10017 or uni0410 to A-cy)

	:param string: glyph name
	:param font: if you add a font, and the font has a local glyph info, it will be used instead of the global info data.
	:return: string
'''

def _productionGlyphName(self, String, font=None):
	if font is not None:
		return font.glyphsInfo().productionGlyphNameForName_(String)
	return GSGlyphsInfo.sharedManager().productionGlyphNameForName_(String)
GSApplication.productionGlyphName = _productionGlyphName

'''
	.. function:: productionGlyphName(Name)

	Converts glyph name to production glyph name (e.g. afii10017 or A-cy to uni0410)

	:param string: glyph name
	:param font: if you add a font, and the font has a local glyph info, it will be used instead of the global info data.
	:return: string

	'''

def _ligatureComponents(self, String, font=None):
	if font is not None:
		return font.glyphsInfo().componentsForLigaName_font_(String, font)
	return GSGlyphsInfo.sharedManager().componentsForLigaName_font_(String, None)
GSApplication.ligatureComponents = _ligatureComponents

'''
	.. function:: ligatureComponents(String)

	If defined as a ligature in the glyph database, this function returns a list of glyph names that this ligature could be composed of.

	:param string: glyph name
	:param font: if you add a font, and the font has a local glyph info, it will be used instead of the global info data.
	:return: list

	.. code-block:: python

		print(Glyphs.ligatureComponents('allah-ar'))

		(
		    "alef-ar",
		    "lam-ar.init",
		    "lam-ar.medi",
		    "heh-ar.fina"
		)
	'''

##########################################################################################################
#
#
#      Callback section
#
#


DrawLayerCallbacks = (DRAWFOREGROUND, DRAWBACKGROUND, DRAWINACTIVE)
Observers = (DOCUMENTOPENED, DOCUMENTACTIVATED, DOCUMENTWASSAVED, DOCUMENTEXPORTED, DOCUMENTCLOSED, TABDIDOPEN, TABWILLCLOSE, UPDATEINTERFACE, MOUSEMOVED)

callbackOperationTargets = {}

class callbackHelperClass(NSObject):
	def __init__(self, func, operation):
		self.func = func
		self.operation = operation

	def __new__(typ, *args, **kwargs):
		self = callbackHelperClass.alloc().init()
		if len(args) > 1:
			self.func = args[0]
			self.operation = args[1]
		return self

	def drawForegroundForLayer_options_(self, Layer, options):
		try:
			if self.func:
				self.func(Layer, options)
		except:
			LogError(traceback.format_exc())

	def drawBackgroundForLayer_options_(self, Layer, options):
		try:
			if self.func:
				self.func(Layer, options)
		except:
			LogError(traceback.format_exc())

	def drawBackgroundForInactiveLayer_options_(self, Layer, options):
		try:
			if self.func:
				self.func(Layer, options)
		except:
			LogError(traceback.format_exc())

	@objc.python_method
	def callback(self, notification):
		if self.func:
			self.func(notification)

	def description(self):  # for debugging in Xcode
		desc = super(callbackHelperClass, self).description()
		return "%s %s" % (desc, str(self.func))


def __addCallback__(self, target, operation):

	# Remove possible old function by the same name
	targetName = str(target)

	try:
		callbackTargets = None
		try:
			callbackTargets = callbackOperationTargets[operation]
		except:
			callbackTargets = {}
			callbackOperationTargets[operation] = callbackTargets

		if targetName in callbackTargets:
			self.removeCallback(target, operation)

		# DrawLayerCallbacks
		if operation in DrawLayerCallbacks:

			# Add class to callbackTargets dict by the function name
			callbackTargets[targetName] = callbackHelperClass(target, operation)

			# Add to stack
			GSCallbackHandler.addCallback_forOperation_(callbackTargets[targetName], operation)

			# Redraw immediately
			self.redraw()

		# Other observers
		elif operation in Observers:
			# Add class to callbackTargets dict by the function name
			callbackTargets[targetName] = callbackHelperClass(target, operation)
			selector = objc.selector(callbackTargets[targetName].callback, signature="v@:@")
			NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(callbackTargets[targetName], selector, operation, objc.nil)
	except:
		NSLog(traceback.format_exc())

GSApplication.addCallback = __addCallback__

'''
	.. function:: addCallback(function, hook)

	.. versionadded:: 2.3

	Add a user-defined function to the glyph window's drawing operations, in the foreground and background for the active glyph as well as in the inactive glyphs.

	The function names are used to add/remove the functions to the hooks, so make sure to use unique function names.

	Your function needs to accept two values: `layer` which will contain the respective :class:`GSLayer` object of the layer we're dealing with and `info` which is a dictionary and contains the value `Scale` (for the moment).

	For the hooks these constants are defined: `DRAWFOREGROUND`, `DRAWBACKGROUND`, `DRAWINACTIVE`, `DOCUMENTWASSAVED`, `DOCUMENTOPENED`, `TABDIDOPEN`, `TABWILLCLOSE`, `UPDATEINTERFACE`, `MOUSEMOVED`. For more information check the constants section.

	.. code-block:: python

		def drawGlyphIntoBackground(layer, info):

			# Due to internal Glyphs.app structure, we need to catch and print exceptions
			# of these callback functions with try/except like so:
			try:

				# Your drawing code here
				NSColor.redColor().set()
				layer.bezierPath.fill()

			# Error. Print exception.
			except:
				import traceback
				print(traceback.format_exc())

		# add your function to the hook
		Glyphs.addCallback(drawGlyphIntoBackground, DRAWBACKGROUND)

	'''

def __do__removeCallback___(self, target, operation):

	targetName = str(target)
	callbackTargets = None
	try:
		callbackTargets = callbackOperationTargets[operation]
	except:
		return
	if targetName in callbackTargets:

		# DrawLayerCallbacks
		if callbackTargets[targetName].operation in DrawLayerCallbacks:
			GSCallbackHandler.removeCallback_(callbackTargets[targetName])
			del(callbackTargets[targetName])
			# Redraw immediately
			self.redraw()
		# Other observers
		elif callbackTargets[targetName].operation in Observers:
			NSNotificationCenter.defaultCenter().removeObserver_(callbackTargets[targetName])
			del(callbackTargets[targetName])

def __removeCallback___(self, target, operation=None):
	if operation is not None:
		__do__removeCallback___(self, target, operation)
	else:
		for operation in callbackOperationTargets.keys():
			__do__removeCallback___(self, target, operation)


GSApplication.removeCallback = __removeCallback___

'''
	.. function:: removeCallback(function)

	.. versionadded:: 2.3

	Remove the function you've previously added.

	.. code-block:: python

		# remove your function to the hook
		Glyphs.removeCallback(drawGlyphIntoBackground)

	'''



#
#
#      // end of Callback section
#
#
##########################################################################################################



def __redraw__(self):
	NSNotificationCenter.defaultCenter().postNotificationName_object_("GSRedrawEditView", None)
GSApplication.redraw = __redraw__

'''
	.. function:: redraw()

	Redraws all Edit views and Preview views.

	'''

def Glyphs_showNotification(self, title, message):
	notification = NSUserNotification.alloc().init()
	notification.setTitle_(title)
	notification.setInformativeText_(message)
	NSUserNotificationCenter.defaultUserNotificationCenter().deliverNotification_(notification)

GSApplication.showNotification = Glyphs_showNotification

'''
	.. function:: showNotification(title, message)

	Shows the user a notification in Mac's Notification Center.


	.. code-block:: python

		Glyphs.showNotification('Export fonts', 'The export of the fonts was successful.')


	'''

def Glyphs_localize(self, localization):
	if isString(localization):
		return localization
	elif type(localization) == dict:
		# Return first match of languages list
		for priority in self.defaults["AppleLanguages"]:
			priority = priority[:2]
			if priority in localization:
				return localization[priority]
		language = localization.get("en", None)  # frist look if there is a english entry.
		if language is not None:
			return language
		# None found, return first item in localization dict
		return localization[localization.keys()[0]]

GSApplication.localize = Glyphs_localize

'''
	.. function:: localize(localization)

	.. versionadded:: 2.3

	Return a string in the language of Glyphs.app’s UI locale, which must be supplied as a dictionary using language codes as keys.

	The argument is a dictionary in the `languageCode: translatedString` format.

	You don’t need to supply strings in all languages that the Glyphs.app UI supports. A subset will do. Just make sure that you add at least an English string to default to next to all your other translated strings. Also don’t forget to mark strings as unicode strings (`u'öäüß'`) when they contain non-ASCII content for proper encoding, and add a `# encoding: utf-8` to the top of all your .py files.

	Tip: You can find Glyphs’ localized languages here `Glyphs.defaults["AppleLanguages"]`.

	.. code-block:: python

		# encoding: utf-8

		print(Glyphs.localize({
			'en':  'Hello World',
			'de': u'Hallöle Welt',
			'fr':  'Bonjour tout le monde',
			'es':  'Hola Mundo',
		}))

		# Given that your Mac’s system language is set to German
		# and Glyphs.app UI is set to use localization (change in preferences),
		# it will print:
		> Hallöle Welt

	'''


def __GSApplication_activateReporter__(self, Reporter):
	if isString(Reporter):
		for r in self.reporters:
			if r.__class__.__name__ == Reporter:
				Reporter = r
				break

	GSCallbackHandler.activateReporter_(Reporter)

GSApplication.activateReporter = __GSApplication_activateReporter__

'''
	.. function:: activateReporter(reporter)

	.. versionadded:: 2.3

	Activate a reporter plug-in by its object (see Glyphs.reporters) or class name.

	.. code-block:: python

		Glyphs.activateReporter('GlyphsMasterCompatibility')

'''

def __GSApplication_deactivateReporter__(self, Reporter):
	if isString(Reporter):
		for r in self.reporters:
			if r.__class__.__name__ == Reporter:
				Reporter = r
				break

	GSCallbackHandler.deactivateReporter_(Reporter)

GSApplication.deactivateReporter = __GSApplication_deactivateReporter__

'''
	.. function:: deactivateReporter(reporter)

	.. versionadded:: 2.3

	Deactivate a reporter plug-in by its object (see Glyphs.reporters) or class name.

	.. code-block:: python

		Glyphs.deactivateReporter('GlyphsMasterCompatibility')
'''


GSDocument.__new__ = staticmethod(GSObject__new__)
GSProjectDocument.__new__ = staticmethod(GSObject__new__)


GSElement.x = property(lambda self: self.pyobjc_instanceMethods.position().x,
	lambda self, value: self.setPosition_(NSMakePoint(value, self.y)))

GSElement.y = property(lambda self: self.pyobjc_instanceMethods.position().y,
	lambda self, value: self.setPosition_(NSMakePoint(self.x, value)))

GSElement.layer = property(lambda self: self.pyobjc_instanceMethods.layer())

GSElement.__new__ = staticmethod(GSObject__new__)



def ____PROXIES____(): pass
def _______________________(): pass




class AppDocumentProxy (Proxy):
	"""The list of documents."""
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		if type(Key) is int:
			Values = self.values()
			if Key < 0:
				Key = len(Values) + Key
			return Values[Key]
		else:
			raise(KeyError)
	def append(self, doc):
		NSDocumentController.sharedDocumentController().addDocument_(doc)
		doc.makeWindowControllers()
		doc.showWindows()
	def values(self):
		return self._owner.fontDocuments()

class AppFontProxy (Proxy):
	"""The list of fonts."""
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		if type(Key) is int:
			Values = self.values()
			if Key < 0:
				Key = len(Values) + Key
			return Values[Key]
		else:
			raise(KeyError)
	def values(self):
		fonts = []
		for doc in self._owner.fontDocuments():
			fonts.append(doc.font)
		return fonts
	def append(self, font):
		doc = Glyphs.documentController().openUntitledDocumentAndDisplay_error_(True, None)[0]
		doc.setFont_(font)
	def extend(self, fonts):
		for font in fonts:
			self.append(font)

GSDocument.font = property(lambda self: self.pyobjc_instanceMethods.font(),
							lambda self, value: self.setFont_(value))

'''
.. attribute:: font
The active :class:`GSFont`
:type: list
'''




class FontGlyphsProxy (Proxy):
	"""The list of glyphs. You can access it with the index or the glyph name.
	Usage:
		Font.glyphs[index]
		Font.glyphs[name]
		for glyph in Font.glyphs:
		...
	"""
	def __getitem__(self, Key):
		if Key is None:
			return None
		if type(Key) == slice:
			return self.values().__getitem__(Key)

		# by index
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.glyphAtIndex_(Key)

		# by glyph name
		elif self._owner.glyphForName_(Key):
			return self._owner.glyphForName_(Key)

		# by string representation as u'ä'
		elif len(Key) == 1 and self._owner.glyphForCharacter_(ord(Key)):
			return self._owner.glyphForCharacter_(ord(Key))

		# by unicode
		else:
			return self._owner.glyphForUnicode_(Key.upper())

	def __setitem__(self, Key, Glyph):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.removeGlyph_(self._owner.glyphAtIndex_(Key))
			self._owner.addGlyph_(Glyph)
		else:
			self._owner.removeGlyph_(self._owner.glyphForName_(Key))
			self._owner.addGlyph_(Glyph)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.removeGlyph_(self._owner.glyphAtIndex_(Key))
		else:
			self._owner.removeGlyph_(self._owner.glyphForName_(Key))
	def __contains__(self, item):
		if isString(item):
			return self._owner.glyphForName_(item) is not None
		return self._owner.indexOfGlyph_(item) < NSNotFound  # indexOfGlyph_ returns NSNotFound which is some very big number
	def keys(self):
		return self._owner.pyobjc_instanceMethods.glyphs().valueForKeyPath_("@unionOfObjects.name")
	def values(self):
		return self._owner.pyobjc_instanceMethods.glyphs()
	def items(self):
		Items = []
		for Value in self._owner.pyobjc_instanceMethods.glyphs():
			Key = Value.name
			Items.append((Key, Value))
		return Items
	def has_key(self, Key):
		return self._owner.glyphForName_(Key) is not None
	def append(self, Glyph):
		if not self.has_key(Glyph.name):
			self._owner.addGlyph_(Glyph)
		else:
			raise NameError('There is a glyph with the name \"%s\" already in the font.' % Glyph.name)
	def extend(self, objects):
		self._owner.addGlyphsFromArray_(list(objects))
	def __len__(self):
		return self._owner.count()
	def setterMethod(self):
		return self._owner.setGlyphs_


class FontFontMasterProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.fontMasterAtIndex_(Key)
		elif isString(Key):
			return self._owner.fontMasterForId_(Key)
		else:
			raise(KeyError)
	def __setitem__(self, Key, FontMaster):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.replaceFontMasterAtIndex_withFontMaster_(Key, FontMaster)
		elif isString(Key):
			OldFontMaster = self._owner.fontMasterForId_(Key)
			self._owner.removeFontMaster_(OldFontMaster)
			return self._owner.addFontMaster_(FontMaster)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			removeFontMaster = self._owner.objectInFontMastersAtIndex_(Key)
		else:
			removeFontMaster = self._owner.fontMasterForId_(Key)
		if removeFontMaster:
			return self._owner.removeFontMasterAndContent_(removeFontMaster)
	def __iter__(self):
		for index in range(self._owner.countOfFontMasters()):
			yield self._owner.fontMasterAtIndex_(index)
	def __len__(self):
		return self._owner.countOfFontMasters()
	def values(self):
		return self._owner.pyobjc_instanceMethods.fontMasters()
	def setterMethod(self):
		return self._owner.setFontMasters_
	def append(self, FontMaster):
		self._owner.addFontMaster_(FontMaster)
	def remove(self, FontMaster):
		self._owner.removeFontMasterAndContent_(FontMaster)
	def insert(self, Index, FontMaster):
		self._owner.insertFontMaster_atIndex_(FontMaster, Index)
	def extend(self, FontMasters):
		for FontMaster in FontMasters:
			self._owner.addFontMaster_(FontMaster)



class FontInstancesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.objectInInstancesAtIndex_(Key)
		else:
			raise(KeyError)
	def __setitem__(self, Key, Class):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.replaceObjectInInstancesAtIndex_withObject_(Key, Class)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.removeObjectFromInstancesAtIndex_(Key)
	def __iter__(self):
		for index in range(self._owner.countOfInstances()):
			yield self._owner.objectInInstancesAtIndex_(index)
	def append(self, Instance):
		self._owner.addInstance_(Instance)
	def extend(self, Instances):
		for Instance in Instances:
			self._owner.addInstance_(Instance)
	def remove(self, Instance):
		self._owner.removeInstance_(Instance)
	def insert(self, Index, Instance):
		self._owner.insertObject_inInstancesAtIndex_(Instance, Index)
	def __len__(self):
		return self._owner.countOfInstances()
	def values(self):
		return self._owner.pyobjc_instanceMethods.instances()
	def setterMethod(self):
		return self._owner.setInstances_

class FontAxesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.objectInAxesAtIndex_(Key)
		else:
			raise(KeyError)
	def __setitem__(self, Key, Class):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.replaceObjectInAxesAtIndex_withObject_(Key, Class)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.removeObjectFromAxesAtIndex_(Key)
	def __iter__(self):
		for index in range(self._owner.countOfAxes()):
			yield self._owner.objectInAxesAtIndex_(index)
	def append(self, axis):
		self._owner.addAxis_(axis)
	def extend(self, Axes):
		for axis in Axes:
			self._owner.addAxis_(axis)
	def remove(self, axis):
		self._owner.removeAxis_(axis)
	def insert(self, Index, axis):
		self._owner.insertObject_inAxesAtIndex_(axis, Index)
	def __len__(self):
		return self._owner.countOfAxes()
	def values(self):
		return self._owner.pyobjc_instanceMethods.axes()
	def setterMethod(self):
		return self._owner.setAxes_

class MasterAxesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			count = self.__len__()
			if Key >= count:
				raise IndexError("list index out of range")
			if Key == 0:
				return self._owner.weightValue
			if Key == 1:
				return self._owner.widthValue
			if Key == 2:
				return self._owner.customValue
			if Key == 3:
				return self._owner.customValue1
			if Key == 4:
				return self._owner.customValue2
			if Key == 5:
				return self._owner.customValue3
		raise(KeyError)
	def __setitem__(self, Key, value):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			count = self.__len__()
			if Key >= count:
				raise IndexError("list index out of range")
			if Key == 0:
				self._owner.weightValue = value
				return
			if Key == 1:
				self._owner.widthValue = value
				return
			if Key == 2:
				self._owner.customValue = value
				return
			if Key == 3:
				self._owner.customValue1 = value
				return
			if Key == 4:
				self._owner.customValue2 = value
				return
			if Key == 5:
				self._owner.customValue3 = value
				return
		raise(KeyError)
	def __delitem__(self, Key):
		raise("Can't delete axis values")
	def __iter__(self):
		for index in range(self.__len__()):
			yield self.__getitem__(index)
	def append(self, value):
		raise("Can't append axis values")
	def extend(self, value):
		raise("Can't extend axis values")
	def remove(self, value):
		raise("Can't remove axis values")
	def insert(self, Index, value):
		raise("Can't insert axis values")
	def __len__(self):
		return min(6, self._owner.font.countOfAxes())
	def values(self):
		count = self.__len__()
		values = []
		for i in range(count):
			values.append(self.__getitem__(i))
		return values
	def setter(self, values):
		count = min(self.__len__(), len(values))
		for i in range(count):
			value = values[i]
			self.__setitem__(i, value)

class InstanceAxesProxy (MasterAxesProxy):
	def __getitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			count = self.__len__()
			if Key >= count:
				raise IndexError("list index out of range")
			if Key == 0:
				return self._owner.interpolationWeight()
			if Key == 1:
				return self._owner.interpolationWidth()
			if Key == 2:
				return self._owner.interpolationCustom()
			if Key == 3:
				return self._owner.interpolationCustom1()
			if Key == 4:
				return self._owner.interpolationCustom2()
			if Key == 5:
				return self._owner.interpolationCustom3()
		raise(KeyError)
	def __setitem__(self, Key, value):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			count = self.__len__()
			if Key >= count:
				raise IndexError("list index out of range")
			if Key == 0:
				self._owner.setInterpolationWeight_(value)
				return
			if Key == 1:
				self._owner.setInterpolationWidth_(value)
				return
			if Key == 2:
				self._owner.setInterpolationCustom_(value)
				return
			if Key == 3:
				self._owner.setInterpolationCustom1_(value)
				return
			if Key == 4:
				self._owner.setInterpolationCustom2_(value)
				return
			if Key == 5:
				self._owner.setInterpolationCustom3_(value)
				return
		raise(KeyError)

class CustomParametersProxy(Proxy):
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		if type(Key) is int:
			return self._owner.objectInCustomParametersAtIndex_(Key)
		else:
			return self._owner.customValueForKey_(Key)
	def __setitem__(self, Key, Parameter):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			Value = self._owner.objectInCustomParametersAtIndex_(Key)
			if Value is not None:
				Value.setValue_(objcObject(Parameter))
			else:
				raise ValueError
		else:
			self._owner.setCustomParameter_forKey_(objcObject(Parameter), objcObject(Key))
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.removeObjectFromCustomParametersAtIndex_(Key)
		else:
			self._owner.removeObjectFromCustomParametersForKey_(Key)
	def __contains__(self, item):
		if isString(item):
			return self._owner.customParameterForKey_(item) is not None
		return self._owner.pyobjc_instanceMethods.customParameters().containsObject_(item)
	def __iter__(self):
		for index in range(self._owner.countOfCustomParameters()):
			yield self._owner.objectInCustomParametersAtIndex_(index)
	def append(self, Parameter):
		self._owner.addCustomParameter_(Parameter)
	def extend(self, Parameters):
		for Parameter in Parameters:
			self._owner.addCustomParameter_(Parameter)
	def remove(self, Parameter):
		self._owner.removeObjectFromCustomParametersForKey_(Parameter.name)
	def insert(self, Index, Parameter):
		customParameters = copy.copy(self.values())
		customParameters.insert(Index, Parameter)
		self._owner.setCustomParameters_(customParameters)
	def __len__(self):
		return self._owner.countOfCustomParameters()
	def values(self):
		return self._owner.pyobjc_instanceMethods.customParameters()
	def setterMethod(self):
		return self._owner.setCustomParameters_


class FontClassesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.objectInClassesAtIndex_(Key)
		elif isString(Key):
			if len(Key) > 0:
				return self._owner.classForTag_(Key)
		raise(KeyError)
	def __setitem__(self, Key, Class):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.replaceObjectInClassesAtIndex_withObject_(Key, Class)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.removeObjectFromClassesAtIndex_(Key)
		elif isString(Key):
			Class = self._owner.classForTag_(Key)
			if Class is not None:
				return self._owner.removeClass_(Class)
	def __iter__(self):
		for index in range(self._owner.countOfClasses()):
			yield self._owner.objectInClassesAtIndex_(index)
	def append(self, Class):
		self._owner.addClass_(Class)
	def extend(self, Classes):
		for Class in Classes:
			self._owner.addClass_(Class)
	def remove(self, Class):
		self._owner.removeClass_(Class)
	def insert(self, Index, Class):
		self._owner.insertObject_inClassesAtIndex_(Class, Index)
	def __len__(self):
		return self._owner.countOfClasses()
	def values(self):
		return self._owner.pyobjc_instanceMethods.classes()
	def setterMethod(self):
		return self._owner.setClasses_


class FontFeaturesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.objectInFeaturesAtIndex_(Key)
		if isString(Key):
			return self._owner.featureForTag_(Key)
		else:
			raise(KeyError)
	def __setitem__(self, Key, Feature):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.replaceObjectInFeaturesAtIndex_withObject_(Key, Feature)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.removeObjectFromFeaturesAtIndex_(Key)
		elif isString(Key):
			Feature = self._owner.featureForTag_(Key)
			if Feature is not None:
				return self._owner.removeFeature_(Feature)
	def __iter__(self):
		for index in range(self._owner.countOfFeatures()):
			yield self._owner.objectInFeaturesAtIndex_(index)
	def append(self, Feature):
		self._owner.addFeature_(Feature)
	def extend(self, Features):
		for Feature in Features:
			self._owner.addFeature_(Feature)
	def remove(self, Class):
		self._owner.removeFeature_(Class)
	def insert(self, Index, Class):
		self._owner.insertObject_inFeaturesAtIndex_(Class, Index)
	def __len__(self):
		return self._owner.countOfFeatures()
	def text(self):
		LineList = []
		for Feature in self._owner.pyobjc_instanceMethods.features():
			LineList.append("feature ")
			LineList.append(Feature.name)
			LineList.append(" {\n")
			LineList.append("    " + Feature.code)
			LineList.append("\n} ")
			LineList.append(Feature.name)
			LineList.append(" ;\n")
		return "".join(LineList)
	def values(self):
		return self._owner.pyobjc_instanceMethods.features()
	def setterMethod(self):
		return self._owner.setFeatures_



class FontFeaturePrefixesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.objectInFeaturePrefixesAtIndex_(Key)
		if isString(Key):
			return self._owner.featurePrefixForTag_(Key)
		else:
			raise(KeyError)
	def __setitem__(self, Key, Feature):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			self._owner.replaceObjectInFeaturePrefixesAtIndex__withObject_(Key, Feature)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.removeObjectFromFeaturePrefixesAtIndex_(Key)
		elif isString(Key):
			FeaturePrefix = self._owner.featurePrefixForTag_(Key)
			if FeaturePrefix is not None:
				return self._owner.removeFeaturePrefix_(FeaturePrefix)
	def append(self, FeaturePrefix):
		self._owner.addFeaturePrefix_(FeaturePrefix)
	def extend(self, FeaturePrefixes):
		for FeaturePrefix in FeaturePrefixes:
			self._owner.addFeaturePrefix_(FeaturePrefix)
	def remove(self, FeaturePrefix):
		self._owner.removeFeaturePrefix_(FeaturePrefix)
	def insert(self, Index, FeaturePrefix):
		self._owner.insertObject_inFeaturePrefixesAtIndex_(FeaturePrefix, Index)
	def text(self):
		LineList = []
		for Prefixe in self._owner.pyobjc_instanceMethods.featurePrefixes():
			LineList.append("# " + Prefixe.name)
			LineList.append(Prefixe.code)
		return "".join(LineList)
	def values(self):
		return self._owner.pyobjc_instanceMethods.featurePrefixes()
	def setterMethod(self):
		return self._owner.setFeaturePrefixes_

class UserDataProxy(Proxy):
	def __getitem__(self, Key):
		return self._owner.userDataForKey_(Key)
	def __setitem__(self, Key, Value):
		self._owner.setUserData_forKey_(objcObject(Value), Key)
	def __delitem__(self, Key):
		self._owner.removeUserDataForKey_(Key)
	def values(self):
		userData = self._owner.pyobjc_instanceMethods.userData()
		if userData is not None:
			return userData.allValues()
		return None
	def keys(self):
		userData = self._owner.pyobjc_instanceMethods.userData()
		if userData is not None:
			return userData.allKeys()
		return None
	def __repr__(self):
		return self._owner.pyobjc_instanceMethods.userData().__repr__()
	def __contains__(self, item):
		return self._owner.pyobjc_instanceMethods.userData().objectForKey_(item) is not None
	def has_key(self, item):
		return self._owner.pyobjc_instanceMethods.userData().objectForKey_(item) is not None
	def get(self, key, default=None):
		value = self.__getitem__(key)
		if value is None:
			return default
		return value

class SmartComponentPoleMappingProxy(Proxy):
	def __getitem__(self, Key):
		poleMapping = self._owner.partSelection()
		if poleMapping is not None:
			return poleMapping[Key]
		return None
	def __setitem__(self, Key, Value):
		poleMapping = self._owner.partSelection()
		if poleMapping is None:
			self._owner.setPartSelection_(NSMutableDictionary.dictionaryWithObject_forKey_(objcObject(Value), Key))
		else:
			poleMapping[Key] = objcObject(Value)
	def __delitem__(self, Key):
		poleMapping = self._owner.partSelection()
		if poleMapping is not None:
			del(poleMapping[Key])
	def values(self):
		poleMapping = self._owner.partSelection()
		if poleMapping is not None:
			return poleMapping.allValues()
		return None
	def __repr__(self):
		poleMapping = self._owner.partSelection()
		return str(poleMapping)

class smartComponentValuesProxy(Proxy):
	def __getitem__(self, Key):
		pieceSettings = self._owner.pieceSettings()
		if pieceSettings is not None:
			return pieceSettings[Key]
		return None
	def __setitem__(self, Key, Value):
		pieceSettings = self._owner.pieceSettings()
		if pieceSettings is None:
			self._owner.setPieceSettings_({Key: objcObject(Value)})
		else:
			pieceSettings[Key] = objcObject(Value)
	def __delitem__(self, Key):
		pieceSettings = self._owner.pieceSettings()
		if pieceSettings is not None:
			del(pieceSettings[Key])
	def values(self):
		pieceSettings = self._owner.pieceSettings()
		if pieceSettings is not None:
			return pieceSettings.allValues()
		return None
	def __repr__(self):
		pieceSettings = self._owner.pieceSettings()
		return str(pieceSettings)

class LayersIterator:
	def __init__(self, owner):
		self.curInd = 0
		self._owner = owner
	def __iter__(self):
		return self
	def next(self):
		if self._owner.parent:
			if self.curInd < self._owner.parent.countOfFontMasters():
				FontMaster = self._owner.parent.fontMasterAtIndex_(self.curInd)
				Item = self._owner.layerForKey_(FontMaster.id)
			else:
				if self.curInd >= self._owner.countOfLayers():
					raise StopIteration
				ExtraLayerIndex = self.curInd - self._owner.parent.countOfFontMasters()
				Index = 0
				ExtraLayer = None
				while ExtraLayerIndex >= 0:
					ExtraLayer = self._owner.objectInLayersAtIndex_(Index)
					if ExtraLayer.layerId != ExtraLayer.associatedMasterId:
						ExtraLayerIndex -= 1
					Index += 1
				Item = ExtraLayer
			self.curInd += 1
			return Item
		else:
			if self.curInd >= self._owner.countOfLayers():
				raise StopIteration
			Item = self._owner.objectInLayersAtIndex_(self.curInd)
			self.curInd += 1
			return Item
		return None

class GlyphLayerProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
			if self._owner.parent:
				if Key < self._owner.parent.countOfFontMasters():
					FontMaster = self._owner.parent.fontMasterAtIndex_(Key)
					return self._owner.layerForKey_(FontMaster.id)
				else:
					ExtraLayerIndex = Key - len(self._owner.parent.masters)
					Index = 0
					ExtraLayer = None
					while ExtraLayerIndex >= 0:
						ExtraLayer = self._owner.pyobjc_instanceMethods.layers().objectAtIndex_(Index)
						if ExtraLayer.layerId != ExtraLayer.associatedMasterId:
							ExtraLayerIndex = ExtraLayerIndex - 1
						Index = Index + 1
					return ExtraLayer
			else:
				return self._owner.pyobjc_instanceMethods.layers().objectAtIndex_(Key)
		else:
			layer = self._owner.layerForKey_(Key)
			if layer is None:
				layer = self._owner.layerForName_(Key)
			return layer
	def __setitem__(self, Key, Layer):
		if type(Key) is int and self._owner.parent:
			if Key < 0:
				Key = self.__len__() + Key
			FontMaster = self._owner.parent.fontMasterAtIndex_(Key)
			Key = FontMaster.id
		return self._owner.setLayer_forKey_(Layer, Key)

	def __delitem__(self, Key):
		if type(Key) is int and self._owner.parent:
			if Key < 0:
				Key = self.__len__() + Key
			Layer = self.__getitem__(Key)
			Key = Layer.layerId
		return self._owner.removeLayerForKey_(Key)

	def __iter__(self):
		return LayersIterator(self._owner)
	def __len__(self):
		return self._owner.countOfLayers()
	def values(self):
		return self._owner.pyobjc_instanceMethods.layers().allValues()
	def append(self, Layer):
		if not Layer.associatedMasterId:
			Layer.associatedMasterId = self._owner.parent.masters[0].id
		self._owner.setLayer_forKey_(Layer, NSString.UUID())
	def extend(self, Layers):
		for Layer in Layers:
			self.append(Layer)
	def remove(self, Layer):
		return self._owner.removeLayerForKey_(Layer.layerId)
	def insert(self, Index, Layer):
		self.append(Layer)
	def setter(self, values):
		newLayers = NSMutableDictionary.dictionary()
		if type(values) == list or type(values) == tuple or type(values) == type(self):
			for layer in values:
				newLayers[layer.layerId] = layer
		elif type(values) == dict or isinstance(values, NSDictionary):
			for (key, layer) in values.items():
				layer.layerId = key
				newLayers[key] = layer
		else:
			raise TypeError
		self._owner.setLayers_(newLayers)

class LayerComponentsProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		if Key < 0:
			Key = self.__len__() + Key
		return self._owner.componentAtIndex_(Key)
	def __setitem__(self, Key, Component):
		if Key < 0:
			Key = self.__len__() + Key
		self._owner.setComponent_atIndex_(Component, Key)
	def __delitem__(self, Key):
		if Key < 0:
			Key = self.__len__() + Key
		self._owner.removeComponentAtIndex_(Key)
	def __copy__(self):
		return [x.copy() for x in self.values()]
	def append(self, Component):
		self._owner.addComponent_(Component)
	def extend(self, Components):
		for Component in Components:
			self._owner.addComponent_(Component)
	def insert(self, Index, Component):
		self._owner.insertComponent_atIndex_(Component, Index)
	def remove(self, Component):
		self._owner.removeComponent_(Component)
	def values(self):
		return self._owner.pyobjc_instanceMethods.components()
	def setterMethod(self):
		return self._owner.setComponents_

class GlyphSmartComponentAxesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		if isinstance(Key, int):
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.objectInPartsSettingsAtIndex_(Key)
		if isString(Key):
			for partSetting in self._owner.partsSettings():
				if partSetting.name == Key:
					return partSetting
		return None
	def __setitem__(self, Key, SmartComponentProperty):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
		self._owner.insertObject_inPartsSettingsAtIndex_(SmartComponentProperty, Key)
	def __delitem__(self, Key):
		if type(Key) is int:
			if Key < 0:
				Key = self.__len__() + Key
		self._owner.removeObjectFromPartsSettingsAtIndex_(Key)
	def append(self, SmartComponentProperty):
		self._owner.addPartsSetting_(SmartComponentProperty)
	def values(self):
		return self._owner.partsSettings()
	def setterMethod(self):
		return self._owner.setPartsSettings_

class LayerGuideLinesProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		elif type(Key) == int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.guideLineAtIndex_(Key)
		raise(KeyError)
	def __setitem__(self, Key, Component):
		self._owner.setGuideLine_atIndex_(Component, Key)
	def __delitem__(self, Key):
		self._owner.removeGuideLineAtIndex_(Key)
	def __copy__(self):
		return [x.copy() for x in self.values()]
	def append(self, GuideLine):
		self._owner.addGuideLine_(GuideLine)
	def extend(self, GuideLines):
		for GuideLine in GuideLines:
			self._owner.addGuideLine_(GuideLine)
	def insert(self, Index, GuideLine):
		self._owner.insertGuideLine_atIndex_(GuideLine, Index)
	def remove(self, GuideLine):
		self._owner.removeGuideLine_(GuideLine)
	def values(self):
		return self._owner.pyobjc_instanceMethods.guideLines()
	def setterMethod(self):
		return self._owner.setGuideLines_

class LayerAnnotationProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		elif type(Key) == int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.objectInAnnotationsAtIndex_(Key)
		raise(KeyError)
	def __setitem__(self, Key, Annotation):
		self._owner.insertObject_inAnnotationsAtIndex_(Annotation, Key)
	def __delitem__(self, Key):
		self._owner.removeObjectFromAnnotationsAtIndex_(Key)
	def __copy__(self):
		return [x.copy() for x in self.values()]
	def append(self, Annotation):
		self._owner.addAnnotation_(Annotation)
	def extend(self, Annotations):
		for Annotation in Annotations:
			self._owner.addAnnotation_(Annotation)
	def insert(self, Index, Annotation):
		annotations = self.values()
		annotations.insert(Index, Annotation)
		self._owner.setAnnotations_(annotations)
	def remove(self, Annotation):
		self._owner.removeAnnotation_(Annotation)
	def values(self):
		return self._owner.pyobjc_instanceMethods.annotations()
	def setterMethod(self):
		return self._owner.setAnnotations_



class LayerHintsProxy (Proxy):
	def __getitem__(self, Key):
		if type(Key) == slice:
			return self.values().__getitem__(Key)
		elif type(Key) == int:
			if Key < 0:
				Key = self.__len__() + Key
			return self._owner.hintAtIndex_(Key)
		raise(KeyError)
	def __setitem__(self, Key, Component):
		self._owner.setHint_atIndex_(Component, Key)
	def __delitem__(self, Key):
		self._owner.removeObjectFromHintsAtIndex_(Key)
	def __copy__(self):
		return [x.copy() for x in self.values()]
	def append(self, Hint):
		self._owner.addHint_(Hint)
	def extend(self, Hints):
		for Hint in Hints:
			self._owner.addHint_(Hint)
	def insert(self, Index, Hint):
		self._owner.insertHint_atIndex_(Hint, Index)
	def remove(self, Hint):
		self._owner.removeHint_(Hint)
	def values(self):
		return self._owner.pyobjc_instanceMethods.hints()
	def setterMethod(self):
		return self._owner.setHints_



class LayerAnchorsProxy (Proxy):
	"""layer.anchors is a dict!!!"""
	def __getitem__(self, Key):
		if isString(Key):
			return self._owner.anchorForName_(Key)
		else:
			raise KeyError
	def __setitem__(self, Key, Anchor):
		if isString(Key):
			Anchor.setName_(Key)
			self._owner.addAnchor_(Anchor)
		else:
			raise TypeError
	def __delitem__(self, Key):
		if isString(Key):
			self._owner.removeAnchorWithName_(Key)
		else:
			raise TypeError
	def __copy__(self):
		return [x.copy() for x in self.values()]
	def items(self):
		Items = []
		for key in self.keys():
			Value = self._owner.anchorForName_(key)
			Items.append((key, Value))
		return Items
	def values(self):
		if self._owner.pyobjc_instanceMethods.anchors() is not None:
			return self._owner.pyobjc_instanceMethods.anchors().allValues()
		else:
			return []
	def keys(self):
		if self._owner.pyobjc_instanceMethods.anchors() is not None:
			return self._owner.pyobjc_instanceMethods.anchors().allKeys()
		else:
			return []
	def append(self, Anchor):
		self._owner.addAnchor_(Anchor)
	def extend(self, Anchors):
		for Anchor in Anchors:
			self._owner.addAnchor_(Anchor)
	def remove(self, Anchor):
		self._owner.removeAnchor_(Anchor)
	def insert(self, Index, Anchor):
		self.append(Anchor)
	def __len__(self):
		return self._owner.countOfAnchors()

	def setter(self, values):
		newAnchors = NSMutableDictionary.dictionary()

		if isinstance(values, (list, tuple)):
			for anchor in values:
				newAnchors[anchor.name] = anchor
		elif isinstance(values, (NSDictionary, dict)):
			for (key, anchor) in values.items():
				newAnchors[anchor.name] = anchor
		elif values is None:
			pass
		elif type(values) == type(self):
			for anchor in values.values():
				newAnchors[anchor.name] = anchor
		else:
			raise TypeError
		self._owner.setAnchors_(newAnchors)


class LayerPathsProxy (Proxy):
	def __getitem__(self, idx):
		if type(idx) == slice:
			return self.values().__getitem__(idx)
		if idx < 0:
			idx = self._owner.countOfPaths() + idx
		return self._owner.pathAtIndex_(idx)
	def __setitem__(self, idx, Path):
		if idx < 0:
			idx = self._owner.countOfPaths() + idx
		self._owner.replacePathAtIndex_withPath_(idx, Path)
	def __delitem__(self, idx):
		if idx < 0:
			idx = self._owner.countOfPaths() + idx
		self._owner.removePathAtIndex_(idx)
	def __copy__(self):
		return [x.copy() for x in self.values()]
	def append(self, Path):
		if isinstance(Path, GSPath):
			self._owner.addPath_(Path)
		else:
			raise ValueError
	def extend(self, Paths):
		if type(Paths) == type(self):
			for path in Paths.values():
				self._owner.addPath_(path)
		elif isinstance(Paths, (list, tuple)):
			for Path in Paths:
				self.append(Path)
		else:
			raise ValueError
	def remove(self, Path):
		self._owner.removePath_(Path)
	def insert(self, Index, Path):
		self._owner.insertPath_atIndex_(Path, Index)
	def values(self):
		return self._owner.pyobjc_instanceMethods.paths()
	def setterMethod(self):
		return self._owner.setPaths_



class LayerSelectionProxy (Proxy):
	def __getitem__(self, idx):
		if type(idx) == slice:
			return self.values().__getitem__(idx)
		return self._owner.pyobjc_instanceMethods.selection().objectAtIndex_(idx)
	def values(self):
		return self._owner.pyobjc_instanceMethods.selection().array()
	def append(self, object):
		self._owner.addSelection_(object)
	def extend(self, objects):
		self._owner.addObjectsFromArrayToSelection_(list(objects))
	def remove(self, object):
		self._owner.removeObjectFromSelection_(object)
	def insert(self, Index, object):
		self._owner.addSelection_(object)
	def setterMethod(self):
		return self._owner.setSelection_



class PathNodesProxy (Proxy):
	def __getitem__(self, idx):
		if type(idx) == slice:
			return self.values().__getitem__(idx)
		return self._owner.nodeAtIndex_(idx)
	def __setitem__(self, idx, Node):
		self._owner.replaceObjectInNodesAtIndex_withObject_(idx, Node)
	def __delitem__(self, idx):
		self._owner.removeObjectFromNodesAtIndex_(idx)
	def __len__(self):
		return self._owner.countOfNodes()
	def append(self, Node):
		self._owner.addNode_(Node)
	def remove(self, Node):
		self._owner.removeNode_(Node)
	def insert(self, Index, Node):
		self._owner.insertNode_atIndex_(Node, Index)
	def extend(self, objects):
		self._owner.addNodes_(list(objects))
	def values(self):
		return self._owner.pyobjc_instanceMethods.nodes()
	def setterMethod(self):
		return self._owner.setNodes_



class FontTabsProxy (Proxy):
	def __getitem__(self, idx):
		if type(idx) == slice:
			return self.values().__getitem__(idx)
		if self._owner.parent:
			if type(idx) is int:
				if idx < 0:
					idx = self.__len__() + idx
				return self._owner.parent.windowController().tabBarControl().tabItemAtIndex_(idx + 1)
			else:
				raise(KeyError)
		else:
			raise Exception("The font is not connected to a document object")
	def __setitem__(self, Key, Tab):
		if type(Key) is int:
			raise(NotImplementedError)
		else:
			raise(KeyError)
	def __delitem__(self, idx):
		if type(idx) is int:
			if idx < 0:
				idx = self.__len__() + idx
			Tab = self._owner.parent.windowController().tabBarControl().tabItemAtIndex_(idx + 1)
			self._owner.parent.windowController().tabBarControl().closeTabItem_(Tab)
		else:
			raise(KeyError)
	def __iter__(self):
		for idx in range(self.__len__()):
			yield self.__getitem__(idx)
	def __len__(self):
		return self._owner.parent.windowController().tabBarControl().countOfTabItems() - 1
	def values(self):
		return self._owner.parent.windowController().tabBarControl().tabItems()[1:]


# Function shared by all user-selectable elements in a layer (nodes, anchors etc.)
def ObjectInLayer_selected(self):
	try:
		return self in self.layer.selection
	except:
		return False

def SetObjectInLayer_selected(self, state):

	# Add to selection
	if state and self not in self.layer.selection:
		self.layer.selection.append(self)

	# Remove
	elif not state and self in self.layer.selection:
		self.layer.selection.remove(self)



##################################################################################
#
#
#
#           GSFont
#
#
#
##################################################################################

def ________________(): pass
def ____GSFont____(): pass
def ________________(): pass


'''
:mod:`GSFont`
===============================================================================

Implementation of the font object. This object is host to the :class:`masters <GSFontMaster>` used for interpolation. Even when no interpolation is involved, for the sake of object model consistency there will still be one master and one instance representing a single font.

Also, the :class:`glyphs <GSGlyph>` are attached to the Font object right here, not one level down to the masters. The different masters’ glyphs are available as :class:`layers <GSLayer>` attached to the glyph objects which are attached here.

.. class:: GSFont()

	Properties

	.. autosummary::

		parent
		masters
		axes
		instances
		glyphs
		classes
		features
		featurePrefixes
		copyright
		designer
		designerURL
		manufacturer
		manufacturerURL
		versionMajor
		versionMinor
		date
		familyName
		upm
		note
		kerning
		userData
		grid
		gridSubDivisions
		gridLength
		keyboardIncrement
		disablesNiceNames
		customParameters
		selection
		selectedLayers
		selectedFontMaster
		masterIndex
		currentText
		tabs
		fontView
		currentTab
		filepath
		tool
		tools
		appVersion

	Functions

	.. autosummary::

		save()
		close()
		show()
		disableUpdateInterface()
		enableUpdateInterface()
		kerningForPair()
		setKerningForPair()
		removeKerningForPair()
		newTab()
		updateFeatures()
		compileFeatures()

	**Properties**

'''


def Font__new__(typ, *args, **kwargs):
	if len(args) > 0 and isinstance(args[0], (str, unicode)):
		path = args[0]
		URL = NSURL.fileURLWithPath_(path)
		typeName = NSWorkspace.sharedWorkspace().typeOfFile_error_(path, None)[0]
		if typeName is not None:
			Doc = GSDocument.alloc().initWithContentsOfURL_ofType_error_(URL, typeName, None)
			if Doc is not None:
				return Doc[0].font
		raise Exception("Unable to open font: %s", path)
	return GSFont.alloc().init()
GSFont.__new__ = staticmethod(Font__new__)

def Font__init__(self, path=None):
	pass

GSFont.__init__ = Font__init__

def Font__repr__(self):
	return "<GSFont \"%s\" v%s.%s with %s masters and %s instances>" % (self.familyName, self.versionMajor, self.versionMinor, len(self.masters), len(self.instances))
GSFont.__repr__ = python_method(Font__repr__)

def Font__copy__(self, memo=None):
	font = self.copy()
	font.setParent_(self.parent)
	return font
GSFont.mutableCopyWithZone_ = Font__copy__


GSFont.parent = property(lambda self: self.pyobjc_instanceMethods.parent())
'''
	.. attribute:: parent
	Returns the internal NSDocument document. Read-only.
	:type: NSDocument
'''

GSFont.masters = property(lambda self: FontFontMasterProxy(self),
							lambda self, value: FontFontMasterProxy(self).setter(value))
'''
	.. attribute:: masters
	Collection of :class:`GSFontMaster` objects.
	:type: list
'''
GSInterpolationFontProxy.masters = property(lambda self: FontFontMasterProxy(self))

GSFont.instances = property(lambda self: FontInstancesProxy(self),
							lambda self, value: FontInstancesProxy(self).setter(value))
'''
	.. attribute:: instances
	Collection of :class:`GSInstance` objects.
	:type: list
'''

GSFont.axes = property(lambda self: FontAxesProxy(self),
						lambda self, value: FontAxesProxy(self).setter(value))
'''
	.. attribute:: axes

	a list of dicts:
		{"Name":"Weight", "Tag":"wght"}
	
	:type: list
	
	.. versionadded:: 2.5
'''

def __GSFont_getitem__(self, value):
	return self.glyphForName_(value)
GSFont.__getitem__ = __GSFont_getitem__

GSFont.glyphs = property(lambda self: FontGlyphsProxy(self),
						lambda self, value: FontGlyphsProxy(self).setter(value))

GSInterpolationFontProxy.glyphs = property(lambda self: FontGlyphsProxy(self),
											lambda self, value: FontGlyphsProxy(self).setter(value))
'''
	.. attribute:: glyphs
	
	Collection of :class:`GSGlyph` objects. Returns a list, but you may also call glyphs using index or glyph name or character (as of v2.4) as key.
	
	.. code-block:: python

		# Access all glyphs
		for glyph in font.glyphs:
			print(glyph)
		<GSGlyph "A" with 4 layers>
		<GSGlyph "B" with 4 layers>
		<GSGlyph "C" with 4 layers>
		...

		# Access one glyph
		print(font.glyphs['A'])
		<GSGlyph "A" with 4 layers>

		# Access a glyph by character (new in v2.4.1)
		print(font.glyphs[u'Ư'])
		<GSGlyph "Uhorn" with 4 layers>

		# Access a glyph by unicode (new in v2.4.1)
		print(font.glyphs['01AF'])
		<GSGlyph "Uhorn" with 4 layers>

		# Add a glyph
		font.glyphs.append(GSGlyph('adieresis'))

		# Duplicate a glyph under a different name
		newGlyph = font.glyphs['A'].copy()
		newGlyph.name = 'A.alt'
		font.glyphs.append(newGlyph)

		# Delete a glyph
		del(font.glyphs['A.alt'])

	:type: list, dict
'''

GSFont.classes = property(lambda self: FontClassesProxy(self),
							lambda self, value: FontClassesProxy(self).setter(value))
'''
	.. attribute:: classes
	Collection of :class:`GSClass` objects, representing OpenType glyph classes.
	:type: list

	.. code-block:: python

		# add a class
		font.classes.append(GSClass('uppercaseLetters', 'A B C D E'))

		# access all classes
		for class in font.classes:
			print(class.name)

		# access one class
		print(font.classes['uppercaseLetters'].code)

		# delete a class
		del(font.classes['uppercaseLetters'])
'''

GSFont.features = property(lambda self: FontFeaturesProxy(self),
							lambda self, value: FontFeaturesProxy(self).setter(value))
'''
	.. attribute:: features
	Collection of :class:`GSFeature` objects, representing OpenType features.
	:type: list

	.. code-block:: python

		# add a feature
		font.features.append(GSFeature('liga', 'sub f i by fi;'))

		# access all features
		for feature in font.features:
			print(feature.code)

		# access one feature
		print(font.features['liga'].code)

		# delete a feature
		del(font.features['liga'])
'''

GSFont.featurePrefixes = property(lambda self: FontFeaturePrefixesProxy(self),
									lambda self, value: FontFeaturePrefixesProxy(self).setter(value))
'''
	.. attribute:: featurePrefixes
	Collection of :class:`GSFeaturePrefix` objects, containing stuff that needs to be outside of the OpenType features.
	:type: list

	.. code-block:: python

		# add a prefix
		font.featurePrefixes.append(GSFeaturePrefix('LanguageSystems', 'languagesystem DFLT dflt;'))

		# access all prefixes
		for prefix in font.featurePrefixes:
			print(prefix.code)

		# access one prefix
		print(font.featurePrefixes['LanguageSystems'].code)

		# delete
		del(font.featurePrefixes['LanguageSystems'])
'''

GSFont.copyright = property(lambda self: self.pyobjc_instanceMethods.copyright(), lambda self, value: self.setCopyright_(value))
'''
	.. attribute:: copyright
	:type: unicode'''
GSFont.designer = property(lambda self: self.pyobjc_instanceMethods.designer(), lambda self, value: self.setDesigner_(value))
'''
	.. attribute:: designer
	:type: unicode'''
GSFont.designerURL = property(lambda self: self.pyobjc_instanceMethods.designerURL(), lambda self, value: self.setDesignerURL_(value))
'''
	.. attribute:: designerURL
	:type: unicode'''
GSFont.manufacturer = property(lambda self: self.pyobjc_instanceMethods.manufacturer(), lambda self, value: self.setManufacturer_(value))
'''
	.. attribute:: manufacturer
	:type: unicode'''
GSFont.manufacturerURL = property(lambda self: self.pyobjc_instanceMethods.manufacturerURL(), lambda self, value: self.setManufacturerURL_(value))
'''
	.. attribute:: manufacturerURL
	:type: unicode'''
GSFont.versionMajor = property(lambda self: self.pyobjc_instanceMethods.versionMajor(), lambda self, value: self.setVersionMajor_(value))
'''
	.. attribute:: versionMajor
	:type: int
'''
GSFont.versionMinor = property(lambda self: self.pyobjc_instanceMethods.versionMinor(), lambda self, value: self.setVersionMinor_(value))
'''
	.. attribute:: versionMinor
	:type: int
'''

def __get_date__(self):
	return datetime.datetime.fromtimestamp(self.pyobjc_instanceMethods.date().timeIntervalSince1970())

def __set_date__(self, date):
	import datetime
	if isinstance(date, datetime.datetime):
		date = NSDate.alloc().initWithTimeIntervalSince1970_(time.mktime(date.timetuple()))
	self.setDate_(date)
GSFont.date = property(lambda self: __get_date__(self), lambda self, value: __set_date__(self, value))
'''
	.. attribute:: date
	:type: NSDate
	.. code-block:: python
		print(font.date)
		2015-06-08 09:39:05 +0000

		# set date to now
		font.date = NSDate.date()
'''
GSFont.familyName = property(lambda self: self.pyobjc_instanceMethods.familyName(),
								lambda self, value: self.setFamilyName_(value))
'''
	.. attribute:: familyName
	Family name of the typeface.
	:type: unicode'''
GSFont.upm = property(lambda self: self.unitsPerEm(), lambda self, value: self.setUnitsPerEm_(value))
'''
	.. attribute:: upm
	Units per Em
	:type: int
'''
GSFont.note = property(lambda self: self.pyobjc_instanceMethods.note(),
						lambda self, value: self.setNote_(value))
'''
	.. attribute:: note
	:type: unicode'''
GSFont.kerning = property(lambda self: self.pyobjc_instanceMethods.kerning(), lambda self, value: self.setKerning_(value))
'''
	.. attribute:: kerning
	A multi-level dictionary. The first level's key is the :attr:`GSFontMaster.id` (each master has its own kerning), the second level's key is the :attr:`GSGlyph.id` or class id (@MMK_L_XX) of the first glyph, the third level's key is a glyph id or class id (@MMK_R_XX) for the second glyph. The values are the actual kerning values.

	To set a value, it is better to use the method :meth:`GSFont.setKerningForPair()`. This ensures a better data integrity (and is faster).
	:type: dict
'''

GSFont.userData = property(lambda self: UserDataProxy(self))
'''
	.. attribute:: userData
	A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the data will not be recoverable from the saved file.
	:type: dict
	.. code-block:: python
		# set value
		font.userData['rememberToMakeCoffee'] = True

		# delete value
		del font.userData['rememberToMakeCoffee']
'''

GSFont.disablesNiceNames = property(lambda self: bool(self.pyobjc_instanceMethods.disablesNiceNames()), lambda self, value: self.setDisablesNiceNames_(value))
'''
	.. attribute:: disablesNiceNames
	Corresponds to the "Don't use nice names" setting from the Font Info dialog.
	:type: bool
'''

GSFont.customParameters = property(lambda self: CustomParametersProxy(self))
'''
	.. attribute:: customParameters
	The custom parameters. List of :class:`GSCustomParameter` objects. You can access them by name or by index.
	.. code-block:: python

		# access all parameters
		for parameter in font.customParameters:
			print(parameter)

		# set a parameter
		font.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'

		# delete a parameter
		del(font.customParameters['trademark'])

	:type: list, dict
'''
GSFont.grid = property(lambda self: self.pyobjc_instanceMethods.gridMain(), lambda self, value: self.setGridMain_(value))
'''
	.. attribute:: grid

	.. versionadded:: 2.3

	Corresponds to the "Grid spacing" setting from the Info dialog.
	:type: int
'''

GSFont.gridSubDivisions = property(lambda self: self.pyobjc_instanceMethods.gridSubDivision(), lambda self, value: self.setGridSubDivision_(value))
'''
	.. attribute:: gridSubDivisions

	.. versionadded:: 2.3

	Corresponds to the "Grid sub divisions" setting from the Info dialog.
	:type: int
'''

GSFont.gridLength = property(lambda self: self.pyobjc_instanceMethods.gridLength())
'''
	.. attribute:: gridLength
	Ready calculated size of grid for rounding purposes. Result of division of grid with gridSubDivisions.
	:type: float
'''

GSFont.disablesAutomaticAlignment = property(lambda self: bool(self.pyobjc_instanceMethods.disablesAutomaticAlignment()), lambda self, value: self.setDisablesAutomaticAlignment_(value))
'''
	.. attribute:: disablesAutomaticAlignment
	:type: bool
'''

GSFont.keyboardIncrement = property(lambda self: self.pyobjc_instanceMethods.keyboardIncrement(), lambda self, value: self.setKeyboardIncrement_(value))
'''
	.. attribute:: keyboardIncrement

	distance of movement by arrow keys. Default:1
	:type: float
	
	.. versionadded:: 2.3.1
'''

def Font_GetSelectedGlyphs(self):

	return self.parent.windowController().glyphsController().selectedObjects()

def Font_SetSelectedGlyphs(self, value):

	if not type(value) in (list, tuple):
		raise ValueError('Argument needs to be a list.')
	self.parent.windowController().glyphsController().setSelectedObjects_(value)

GSFont.selection = property(lambda self: Font_GetSelectedGlyphs(self), lambda self, value: Font_SetSelectedGlyphs(self, value))
'''
	.. attribute:: selection

	.. versionadded:: 2.3

	Returns a list of all selected glyphs in the Font View.
	:type: list
'''

def Font_selectedLayers(self):
	return self.parent.selectedLayers()

GSFont.selectedLayers = property(lambda self: Font_selectedLayers(self))
'''
	.. attribute:: selectedLayers
	Returns a list of all selected layers in the active tab.

	If a glyph is being edited, it will be the only glyph returned in this list. Otherwise the list will contain all glyphs selected with the Text tool.

	:type: list

'''

GSFont.selectedFontMaster = property(lambda self: self.parent.selectedFontMaster())
'''
	.. attribute:: selectedFontMaster
	Returns the active master (selected in the toolbar).
	:type: :class:`GSFontMaster`

'''

GSFont.masterIndex = property(lambda self: self.parent.windowController().masterIndex(), lambda self, value: self.parent.windowController().setMasterIndex_(value))
'''
	.. attribute:: masterIndex
	Returns the index of the active master (selected in the toolbar).
	:type: int

'''

def __current_Text__(self):
	try:
		return self.parent.windowController().activeEditViewController().graphicView().displayString()
	except:
		pass
	return None
def __set__current_Text__(self, String):
	# if String is None:
	# 	String = ""
	self.parent.windowController().activeEditViewController().graphicView().setDisplayString_(String)

GSFont.currentText = property(lambda self: __current_Text__(self),
								lambda self, value: __set__current_Text__(self, value))
'''
	.. attribute:: currentText
	The text of the current Edit view.

	Unencoded and none ASCII glyphs will use a slash and the glyph name. (e.g: /a.sc). Setting unicode strings works.

	:type: unicode
'''

# Tab interaction:

GSFont.tabs = property(lambda self: FontTabsProxy(self))

'''
	.. attribute:: tabs
	List of open Edit view tabs in UI, as list of :class:`GSEditViewController` objects.

	.. code-block:: python

		# open new tab with text
		font.newTab('hello')

		# access all tabs
		for tab in font.tabs:
			print(tab)

		# close last tab
		font.tabs[-1].close()

	:type: list

'''

GSFont.fontView = property(lambda self: self.parent.windowController().tabBarControl().tabItemAtIndex_(0))
'''
	.. attribute:: fontView
	:type GSFontViewController

'''

def __GSFont__currentTab__(self):
	try:
		return self.parent.windowController().activeEditViewController()
	except:
		return None

def __GSFont__set_currentTab__(self, TabItem):
	self.parent.windowController().tabBarControl().selectTabItem_(TabItem)

GSFont.currentTab = property(lambda self: __GSFont__currentTab__(self),
							lambda self, value: __GSFont__set_currentTab__(self, value))

'''
	.. attribute:: currentTab
	Active Edit view tab.
	:type: :class:`GSEditViewController`

'''

def Font_filepath(self):
	if self.parent is not None and self.parent.fileURL() is not None:
		return self.parent.fileURL().path()
	else:
		return None
GSFont.filepath = property(lambda self: Font_filepath(self))
'''
	.. attribute:: filepath
	On-disk location of GSFont object.
	:type: unicode
	
'''

GSFont.toolIndex = property(lambda self: self.parent.windowController().selectedToolIndex(), lambda self, value: self.parent.windowController().setSelectedToolIndex_(value))

toolClassAbrevations = {  # abrevation : className
	"SelectTool": "GlyphsToolSelect",
	"DrawTool": "GlyphsToolDraw",
	"OtherTool": "GlyphsToolOther",
	"PenTool": "PenTool",
	"PrimitivesTool": "GlyphsToolPrimitives",
	"RotateTool": "GlyphsToolRotate",
	"ScaleTool": "GlyphsToolScale",
	"TextTool": "GlyphsToolText",
	"AnnotationTool": "AnnotationTool",
	"HandTool": "GlyphsToolHand",
	"ZoomTool": "GlyphsToolZoom",
	"MeasurementTool": "GlyphsToolMeasurement",
	"TrueTypeTool": "GlyphsToolTrueTypeInstructor",
}

toolClassAbrevationsReverse = dict((v, k) for k, v in toolClassAbrevations.items())

def __GSFont_tool__(self):
	toolIndex = self.toolIndex
	tool = self.parent.windowController().toolInstances()[toolIndex]
	toolClassName = tool.className()
	if toolClassName in toolClassAbrevationsReverse:
		toolClassName = toolClassAbrevationsReverse[toolClassName]
	return toolClassName

def __GSFont_setTool__(self, toolName):

	if toolName in toolClassAbrevations:
		toolName = toolClassAbrevations[toolName]
	toolClass = NSClassFromString(toolName)

	if toolClass:
		self.parent.windowController().setToolForClass_(toolClass)
	else:
		sys.stderr.write('No tool found by the name "%s"' % (toolName))


GSFont.tool = property(lambda self: __GSFont_tool__(self), lambda self, value: __GSFont_setTool__(self, value))

'''
	.. attribute:: tool

	Name of tool selected in toolbar.

	For available names including third-party plug-ins that come in the form of selectable tools, see `GSFont.tools` below.

	.. code-block:: python

		font.tool = 'SelectTool' # Built-in tool
		font.tool = 'GlyphsAppSpeedPunkTool' # Third party plug-in

	:type: string

	.. versionadded:: 2.3

'''

def __GSFont_toolsList__(self):
	tools = []
	for tool in self.parent.windowController().toolInstances():
		toolClassName = tool.className()
		if toolClassName in toolClassAbrevationsReverse:
			toolClassName = toolClassAbrevationsReverse[toolClassName]
		tools.append(toolClassName)
	return tools

GSFont.tools = property(lambda self: __GSFont_toolsList__(self))

'''
	.. attribute:: tools
	Prints a list of available tool names, including third-party plug-ins.
	:type: list, string

	.. versionadded:: 2.3
	
'''


GSFont.appVersion = property(lambda self: self.pyobjc_instanceMethods.appVersion())

'''
	.. attribute:: appVersion
	returns the version that the file was last saved

	.. versionadded:: 2.5


	**Functions**

'''


def Font__save__(self, path=None):
	if self.parent is not None:
		if path is None:
			self.parent.saveDocument_(None)
		else:
			URL = NSURL.fileURLWithPath_(path)
			if path.endswith('.glyphs'):
				typeName = "com.schriftgestaltung.glyphs"
			elif path.endswith('.ufo'):
				typeName = "org.unifiedfontobject.ufo"
			self.parent.writeSafelyToURL_ofType_forSaveOperation_error_(URL, typeName, 1, objc.nil)
	elif path is not None:
		Doc = GSDocument()
		Doc.font = self
		URL = NSURL.fileURLWithPath_(path)
		if path.endswith('.glyphs'):
			typeName = "com.schriftgestaltung.glyphs"
		elif path.endswith('.ufo'):
			typeName = "org.unifiedfontobject.ufo"
		Doc.writeSafelyToURL_ofType_forSaveOperation_error_(URL, typeName, 1, objc.nil)
	else:
		raise("No path set")

GSFont.save = Font__save__
'''
	.. function:: save([filePath])

	Saves the font.
	if no path is given, it saves to the existing location.

	:param filePath: Optional file path
	:type filePath: str

'''

def Font__close__(self, ignoreChanges=True):
	if self.parent:
		if ignoreChanges:
			self.parent.close()
		else:
			self.parent.canCloseDocumentWithDelegate_shouldCloseSelector_contextInfo_(None, None, None)
GSFont.close = Font__close__

'''
	.. function:: close([ignoreChanges = False])

	Closes the font.

	:param ignoreChanges: Optional. Ignore changes to the font upon closing
	:type ignoreChanges: bool

	.. function:: disableUpdateInterface()

	Disables interface updates and thus speeds up glyph processing. Call this before you do big changes to the font, or to its glyphs. Make sure that you call Font.enableUpdateInterface() when you are done.

	.. function:: enableUpdateInterface()
	
	This re-enables the interface update. Only makes sense to call if you have disabled it earlier.

'''

def GSFont__show__(self):
	if self not in Glyphs.fonts:
		Glyphs.fonts.append(self)
	else:
		self.parent.windowController().showWindow_(None)
GSFont.show = GSFont__show__

'''
	.. function:: show()

	Makes font visible in the application, either by bringing an already open font window to the front or by appending a formerly invisible font object (such as the result of a `copy()` operation) as a window to the application.

	.. versionadded:: 2.4.1
'''


def kerningForPair(self, FontMasterID, LeftKeringId, RightKerningId, direction=LTR):
	if not LeftKeringId[0] == '@':
		LeftKeringId = self.glyphs[LeftKeringId].id
	if not RightKerningId[0] == '@':
		RightKerningId = self.glyphs[RightKerningId].id
	return self.kerningForFontMasterID_LeftKey_RightKey_direction_(FontMasterID, LeftKeringId, RightKerningId, direction)
GSFont.kerningForPair = kerningForPair
'''
	.. function:: kerningForPair(fontMasterId, leftKey, rightKey [, direction = LTR])

	This returns the kerning value for the two specified glyphs (leftKey or rightKey is the glyph name) or a kerning group key (@MMK_X_XX).

	:param fontMasterId: The id of the FontMaster
	:type fontMasterId: str
	:param leftKey: either a glyph name or a class name
	:type leftKey: str
	:param rightKey: either a glyph name or a class name
	:type rightKey: str
	:param direction: optional writing direction (see Constants). Default is LTR.
	:type direction: str
	:return: The kerning value
	:rtype: float

	.. code-block:: python

		# print(kerning between w and e for currently selected master)
		font.kerningForPair(font.selectedFontMaster.id, 'w', 'e')
		-15.0

		# print(kerning between group T and group A for currently selected master)
		# ('L' = left side of the pair and 'R' = left side of the pair)
		font.kerningForPair(font.selectedFontMaster.id, '@MMK_L_T', '@MMK_R_A')
		-75.0

		# in the same font, kerning between T and A would be zero, because they use group kerning instead.
		font.kerningForPair(font.selectedFontMaster.id, 'T', 'A')
		9.22337203685e+18 # (this is the maximum number for 64 bit. It is used as an empty value)

'''

def setKerningForPair(self, FontMasterID, LeftKeringId, RightKerningId, Value, direction=LTR):
	if not LeftKeringId[0] == '@':
		LeftKeringId = self.glyphs[LeftKeringId].id
	if not RightKerningId[0] == '@':
		RightKerningId = self.glyphs[RightKerningId].id
	self.setKerningForFontMasterID_LeftKey_RightKey_Value_direction_(FontMasterID, LeftKeringId, RightKerningId, Value, direction)
GSFont.setKerningForPair = setKerningForPair
'''
	.. function:: setKerningForPair(fontMasterId, leftKey, rightKey, value [, direction = LTR])

	This sets the kerning for the two specified glyphs (leftKey or rightKey is the glyphname) or a kerning group key (@MMK_X_XX).

	:param fontMasterId: The id of the FontMaster
	:type fontMasterId: str
	:param leftKey: either a glyph name or a class name
	:type leftKey: str
	:param rightKey: either a glyph name or a class name
	:type rightKey: str
	:param value: kerning value
	:type value: float
	:param direction: optional writing direction (see Constants). Default is LTR.
	:type direction: str

	.. code-block:: python
		# set kerning for group T and group A for currently selected master
		# ('L' = left side of the pair and 'R' = left side of the pair)
		font.setKerningForPair(font.selectedFontMaster.id, '@MMK_L_T', '@MMK_R_A', -75)

'''

def removeKerningForPair(self, FontMasterID, LeftKeringId, RightKerningId):
	if LeftKeringId[0] != '@':
		try:
			LeftKeringId = self.glyphs[LeftKeringId].id
		except:
			pass
	if RightKerningId[0] != '@':
		try:
			RightKerningId = self.glyphs[RightKerningId].id
		except:
			pass
	self.removeKerningForFontMasterID_LeftKey_RightKey_(FontMasterID, LeftKeringId, RightKerningId)
GSFont.removeKerningForPair = removeKerningForPair
'''
	.. function:: removeKerningForPair(FontMasterId, LeftKey, RightKey)

	Removes the kerning for the two specified glyphs (LeftKey or RightKey is the glyphname) or a kerning group key (@MMK_X_XX).

	:param FontMasterId: The id of the FontMaster
	:type FontMasterId: str
	:param LeftKey: either a glyph name or a class name
	:type LeftKey: str
	:param RightKey: either a glyph name or a class name
	:type RightKey: str

	.. code-block:: python
		# remove kerning for group T and group A for all masters
		# ('L' = left side of the pair and 'R' = left side of the pair)
		for master in font.masters:
			font.removeKerningForPair(master.id, '@MMK_L_T', '@MMK_R_A')

'''

def __GSFont__addTab__(self, tabText=""):
	if self.parent:
		return self.parent.windowController().addTabWithString_(tabText)
	return None

GSFont.newTab = __GSFont__addTab__
'''
	.. function:: newTab([tabText])

	Opens a new tab in the current document window, optionally with text, and return that tab object

	:param tabText: Text or glyph names escaped with '/'

	.. code-block:: python
		# open new tab
		font.newTab('abcdef')

		# or
		tab = font.newTab('abcdef')
		print(tab)

'''

def __GSFont__updateFeatures__(self):
	GSFeatureGenerator.alloc().init().makeFeatures_(self)
	self.compileFeatures()


GSFont.updateFeatures = __GSFont__updateFeatures__

'''
	.. function:: updateFeatures()

	Updates all OpenType features and classes at once, including generating necessary new features and classes. Equivalent to the "Update" button in the features panel. This already includes the compilation of the features (see `compileFeatures()`).

	.. versionadded:: 2.4
'''

def __GSFont__compileFeatures__(self):
	self.compileTempFontError_(None)


GSFont.compileFeatures = __GSFont__compileFeatures__

'''
	.. function:: compileFeatures()

	Compiles the features, thus making the new feature code functionally available in the editor. Equivalent to the "Test" button in the features panel.

	.. versionadded:: 2.5
'''



##################################################################################
#
#
#
#           GSFontMaster
#
#
#
##################################################################################

def _______________________(): pass
def ____GSFontMaster____(): pass
def _______________________(): pass

'''

:mod:`GSFontMaster`
===============================================================================

Implementation of the master object. This corresponds with the "Masters" pane in the Font Info. In Glyphs.app, the glyphs of each master are reachable not here, but as :class:`layers <GSLayer>` attached to the :class:`glyphs <GSGlyph>` attached to the :class:`font <GSFont>` object. See the infographic on top for better understanding.

.. class:: GSFontMaster()

'''

GSFontMaster.__new__ = staticmethod(GSObject__new__)

def FontMaster__init__(self):
	pass
GSFontMaster.__init__ = FontMaster__init__

def FontMaster__repr__(self):
	return "<GSFontMaster \"%s\" width %s weight %s>" % (self.name, self.widthValue, self.weightValue)
GSFontMaster.__repr__ = python_method(FontMaster__repr__)

GSFontMaster.mutableCopyWithZone_ = GSObject__copy__

'''

	.. autosummary::

		id
		name
		weight
		width
		axes
		weightValue
		widthValue
		customValue
		customName
		ascender
		capHeight
		xHeight
		descender
		italicAngle
		verticalStems
		horizontalStems
		alignmentZones
		blueValues
		otherBlues
		guides
		userData
		customParameters
		font

	**Properties**

'''

GSFontMaster.id = property(lambda self: self.pyobjc_instanceMethods.id(), lambda self, value: self.setId_(value))
'''
	.. attribute:: id
	Used to identify :class:`Layers` in the Glyph

	see :attr:`GSGlyph.layers`

	.. code-block:: python
		# ID of first master
		print(font.masters[0].id)
		3B85FBE0-2D2B-4203-8F3D-7112D42D745E

		# use this master to access the glyph's corresponding layer
		print(glyph.layers[font.masters[0].id])
		<GSLayer "Light" (A)>

	:type: unicode
'''

GSFontMaster.font = property(lambda self: self.pyobjc_instanceMethods.font(), lambda self, value: self.setFont_(value))
'''
	.. attribute:: font
	Reference to the :class:`GSFont` object that contains the master. Normally that is set by the app, only if the instance is not actually added to the font, then set this manually.

	:type: GSFont

	.. versionadded:: 2.5.2
'''

GSFontMaster.name = property(lambda self: self.pyobjc_instanceMethods.name(),
							 lambda self, value: self.setName_(value))
'''
	.. attribute:: name
	The human-readable identification of the master, e.g., "Bold Condensed".
	:type: string
'''

GSFontMaster.axes = property(lambda self: MasterAxesProxy(self),
							 lambda self, value: MasterAxesProxy(self).setter(value))
'''
	.. attribute:: axes
	List of floats specifying the positions for each axis

	.. code-block:: python
		# setting a value for a specific axis
		master.axes[2] = 12
		# setting all values at once
		master.axes = [100, 12, 3.5]

	:type: list

	.. versionadded:: 2.5.2
'''


# GSFontMaster.weight = property(lambda self: self.pyobjc_instanceMethods.weight(), lambda self, value: self.setWeight_(value))
'''
	.. attribute:: weight
	Human-readable weight name, chosen from list in Font Info. For the position in the interpolation design space, use :attr:`axes <GSFontMaster.axes>`.

	.. deprecated:: 2.5.2
		Use :attr:`GSFontMaster.name` instead.

	:type: string
'''

# GSFontMaster.width = property(lambda self: self.pyobjc_instanceMethods.width(), lambda self, value: self.setWidth_(value))
'''
	.. attribute:: width
	Human-readable width name, chosen from list in Font Info. For the position in the interpolation design space, use :attr:`axes <GSFontMaster.axes>`.

	.. deprecated:: 2.5.2
		Use :attr:`GSFontMaster.name` instead.

	:type: string
'''

# GSFontMaster.customName = property(lambda self: self.pyobjc_instanceMethods.custom(), lambda self, value: self.setCustom_(value))
'''
	.. attribute:: customName
	The name of the custom interpolation dimension.
	
	.. deprecated:: 2.5.2
		Use :attr:`GSFontMaster.axes` instead.
	
	:type: string
'''

GSFontMaster.weightValue = property(lambda self: self.pyobjc_instanceMethods.weightValue(), lambda self, value: self.setWeightValue_(value))
'''
	.. attribute:: weightValue
	Value for interpolation in design space.

	.. deprecated:: 2.5.2
		Use :attr:`GSFontMaster.axes` instead.

	:type: float
'''

GSFontMaster.widthValue = property(lambda self: self.pyobjc_instanceMethods.widthValue(), lambda self, value: self.setWidthValue_(value))
'''
	.. attribute:: widthValue
	Value for interpolation in design space.
	
	.. deprecated:: 2.5.2
		Use :attr:`GSFontMaster.axes` instead.
	
	:type: float
'''

GSFontMaster.customValue = property(lambda self: self.pyobjc_instanceMethods.customValue(), lambda self, value: self.setCustomValue_(value))
'''
	.. attribute:: customValue
	Value for interpolation in design space.
	
	.. deprecated:: 2.5.2
		Use :attr:`GSFontMaster.axes` instead.
	
	:type: float
'''

GSFontMaster.customValue1 = property(lambda self: self.pyobjc_instanceMethods.customValue1(), lambda self, value: self.setCustomValue1_(value))
'''
	.. attribute:: customValue1
	Value for interpolation in design space.
	
	.. deprecated:: 2.5.2
		Use :attr:`GSFontMaster.axes` instead.
	
	:type: float
'''

GSFontMaster.customValue2 = property(lambda self: self.pyobjc_instanceMethods.customValue2(), lambda self, value: self.setCustomValue2_(value))
'''
	.. attribute:: customValue2
	Value for interpolation in design space.
	
	.. deprecated:: 2.5.2
		Use :attr:`GSFontMaster.axes` instead.
	
	:type: float
'''

GSFontMaster.customValue3 = property(lambda self: self.pyobjc_instanceMethods.customValue3(), lambda self, value: self.setCustomValue3_(value))
'''
	.. attribute:: customValue3
	Value for interpolation in design space.
	
	.. deprecated:: 2.5.2
		Use :attr:`GSFontMaster.axes` instead.
	
	:type: float
'''

GSFontMaster.ascender = property(lambda self: self.pyobjc_instanceMethods.ascender(), lambda self, value: self.setAscender_(value))
'''
	.. attribute:: ascender
	:type: float
'''

GSFontMaster.capHeight = property(lambda self: self.pyobjc_instanceMethods.capHeight(), lambda self, value: self.setCapHeight_(value))
'''
	.. attribute:: capHeight
	:type: float
'''

GSFontMaster.xHeight = property(lambda self: self.pyobjc_instanceMethods.xHeight(), lambda self, value: self.setXHeight_(value))
'''
	.. attribute:: xHeight
	:type: float
'''

GSFontMaster.descender = property(lambda self: self.pyobjc_instanceMethods.descender(), lambda self, value: self.setDescender_(value))
'''
	.. attribute:: descender
	:type: float
'''

GSFontMaster.italicAngle = property(lambda self: self.pyobjc_instanceMethods.italicAngle(), lambda self, value: self.setItalicAngle_(value))
'''
	.. attribute:: italicAngle
	:type: float
'''

GSFontMaster.verticalStems = property(lambda self: list(self.pyobjc_instanceMethods.verticalStems()), lambda self, value: self.setVerticalStems_(value))
'''
	.. attribute:: verticalStems
	The vertical stems. This is a list of numbers. For the time being, this can be set only as an entire list at once.
	:type: list
	.. code-block:: python

		# Set stems
		font.masters[0].verticalStems = [10, 11, 20]
'''

GSFontMaster.horizontalStems = property(lambda self: list(self.pyobjc_instanceMethods.horizontalStems()), lambda self, value: self.setHorizontalStems_(value))
'''
	.. attribute:: horizontalStems
	The horizontal stems. This is a list of numbers.  For the time being, this can be set only as an entire list at once.
	:type: list
	.. code-block:: python

		# Set stems
		font.masters[0].horizontalStems = [10, 11, 20]
'''

GSFontMaster.alignmentZones = property(lambda self: self.pyobjc_instanceMethods.alignmentZones(), lambda self, value: self.setAlignmentZones_(value))
'''
	.. attribute:: alignmentZones
	Collection of :class:`GSAlignmentZone` objects.
	:type: list
'''

def FontMaster_blueValues(self):
	return GSGlyphsInfo.blueValues_(self.alignmentZones)
GSFontMaster.blueValues = property(lambda self: FontMaster_blueValues(self))
'''
	.. attribute:: blueValues
	PS hinting Blue Values calculated from the master's alignment zones. Read-only.
	:type: list
'''

def FontMaster_otherBlues(self):
	return GSGlyphsInfo.otherBlues_(self.alignmentZones)
GSFontMaster.otherBlues = property(lambda self: FontMaster_otherBlues(self))
'''
	.. attribute:: otherBlues
	PS hinting Other Blues calculated from the master's alignment zones. Read-only.
	:type: list
'''

# new (guidelines at layers are also called just 'guides')
GSFontMaster.guides = property(lambda self: self.pyobjc_instanceMethods.guideLines(), lambda self, value: self.setGuideLines_(value))
# keep for compatibility
GSFontMaster.guideLines = GSFontMaster.guides
'''
	.. attribute:: guides
	Collection of :class:`GSGuideLine` objects. These are the font-wide (actually master-wide) red guidelines. For glyph-level guidelines (attached to the layers) see :attr:`GSLayer.guides`
	:type: list
'''

GSFontMaster.userData = property(lambda self: UserDataProxy(self))
'''
	.. attribute:: userData
	A dictionary to store user data. Use a unique key, and only use objects that can be stored in a property list (bool, string, list, dict, numbers, NSData), otherwise the data will not be recoverable from the saved file.
	:type: dict
	.. code-block:: python
		# set value
		font.masters[0].userData['rememberToMakeTea'] = True

		# delete value
		del font.masters[0].userData['rememberToMakeTea']
'''

GSFontMaster.customParameters = property(lambda self: CustomParametersProxy(self))
'''
	.. attribute:: customParameters
	The custom parameters. List of :class:`GSCustomParameter` objects. You can access them by name or by index.

	.. code-block:: python

		# access all parameters
		for parameter in font.masters[0].customParameters:
			print(parameter)

		# set a parameter
		font.masters[0].customParameters['underlinePosition'] = -135

		# delete a parameter
		del(font.masters[0].customParameters['underlinePosition'])

	:type: list, dict
'''

##################################################################################
#
#
#
#           GSElement
#
#
#
##################################################################################


GSElement.selected = property(lambda self: ObjectInLayer_selected(self), lambda self, value: SetObjectInLayer_selected(self, value))


##################################################################################
#
#
#
#           GSAlignmentZone
#
#
#
##################################################################################


def ___________________________(): pass
def ____GSAlignmentZone____(): pass
def ___________________________(): pass

'''

:mod:`GSAlignmentZone`
===============================================================================

Implementation of the alignmentZone object.

There is no distinction between Blue Zones and Other Zones. All negative zones (except the one with position 0) will be exported as Other Zones.

The zone for the baseline should have position 0 (zero) and a negative width.

.. class:: GSAlignmentZone([pos, size])

	:param pos: The position of the zone
	:param size: The size of the zone
'''

GSAlignmentZone.__new__ = staticmethod(GSObject__new__)

def AlignmentZone__init__(self, pos=0, size=20):
	self.setPosition_(pos)
	self.setSize_(size)

GSAlignmentZone.__init__ = AlignmentZone__init__

def AlignmentZone__repr__(self):
	return "<GSAlignmentZone pos %s size %s>" % (self.position, self.size)
GSAlignmentZone.__repr__ = python_method(AlignmentZone__repr__)

GSAlignmentZone.mutableCopyWithZone_ = GSObject__copy__


'''
	Properties

	.. autosummary::

		position
		size

	**Properties**

'''

GSAlignmentZone.position = property(lambda self: self.pyobjc_instanceMethods.position(), lambda self, value: self.setPosition_(value))
'''
	.. attribute:: position
	:type: int
'''
	
GSAlignmentZone.size = property(lambda self: self.pyobjc_instanceMethods.size(), lambda self, value: self.setSize_(value))
'''
	.. attribute:: size
	:type: int
'''

def __elementDict__(self):
	return dict(self.elementDict())
GSAlignmentZone.plistValue = __elementDict__
def __propertyListValue__(self):
	return dict(self.propertyListValue())
GSTTStem.plistValue = __propertyListValue__

##################################################################################
#
#
#
#           GSInstance
#
#
#
##################################################################################


def ____________________(): pass
def ____GSInstance____(): pass
def ____________________(): pass


'''

:mod:`GSInstance`
===============================================================================

Implementation of the instance object. This corresponds with the "Instances" pane in the Font Info.

.. class:: GSInstance()

'''

GSInstance.__new__ = staticmethod(GSObject__new__)

def Instance__init__(self):
	pass
GSInstance.__init__ = Instance__init__

def Instance__repr__(self):
	return "<GSInstance \"%s\" width %s weight %s>" % (self.name, self.widthValue, self.weightValue)
GSInstance.__repr__ = python_method(Instance__repr__)

GSInstance.mutableCopyWithZone_ = GSObject__copy__


'''
	Properties

	.. autosummary::


		active
		name
		weight
		width
		axes
		weightValue
		widthValue
		customValue
		isItalic
		isBold
		linkStyle
		familyName
		preferredFamily
		preferredSubfamilyName
		windowsFamily
		windowsStyle
		windowsLinkedToStyle
		fontName
		fullName
		font
		customParameters
		instanceInterpolations
		manualInterpolation
		interpolatedFontProxy
		interpolatedFont
		lastExportedFilePath

	Functions

	.. autosummary::

		generate()
		addAsMaster()

	**Properties**

'''

GSInstance.active = property(lambda self: bool(self.pyobjc_instanceMethods.active()), lambda self, value: self.setActive_(value))
'''
	.. attribute:: active
	:type: bool
'''

GSInstance.name = property(lambda self: self.pyobjc_instanceMethods.name(), lambda self, value: self.setName_(value))
'''
	.. attribute:: name
	Name of instance. Corresponds to the "Style Name" field in the font info. This is used for naming the exported fonts.
	:type: string
'''

GSInstance.weight = property(lambda self: self.pyobjc_instanceMethods.weightClass(), lambda self, value: self.setWeightClass_(value))
GSInstance.weightClass = property(lambda self: self.pyobjc_instanceMethods.weightClass(), lambda self, value: self.setWeightClass_(value))
'''
	.. attribute:: weight
	Human-readable weight name, chosen from list in Font Info. For actual position in interpolation design space, use GSInstance.weightValue.
	:type: string
'''
GSInstance.width = property(lambda self: self.pyobjc_instanceMethods.widthClass(), lambda self, value: self.setWidthClass_(value))
GSInstance.widthClass = property(lambda self: self.pyobjc_instanceMethods.widthClass(), lambda self, value: self.setWidthClass_(value))
'''
	.. attribute:: width
	Human-readable width name, chosen from list in Font Info. For actual position in interpolation design space, use GSInstance.widthValue.
	:type: string
'''

GSInstance.axes = property(lambda self: InstanceAxesProxy(self),
							 lambda self, value: InstanceAxesProxy(self).setter(value))
'''
	.. attribute:: axes
	List of floats specifying the positions for each axis
	
	.. code-block:: python
		# setting a value for a specific axis
		instance.axes[2] = 12
		# setting all values at once
		instance.axes = [100, 12, 3.5]
		
	:type: list

	.. versionadded:: 2.5.2
'''

GSInstance.weightValue = property(lambda self: self.interpolationWeight(), lambda self, value: self.setInterpolationWeight_(value))
'''
	.. attribute:: weightValue
	Value for interpolation in design space.
	
	.. deprecated:: 2.5.2
		Use :attr:`axes <GSInstance.axes>` instead.
	
	:type: float
'''

GSInstance.widthValue = property(lambda self: self.interpolationWidth(), lambda self, value: self.setInterpolationWidth_(value))
'''
	.. attribute:: widthValue
	Value for interpolation in design space.
	
	.. deprecated:: 2.5.2
		Use :attr:`axes <GSInstance.axes>` instead.
	
	:type: float
'''

GSInstance.customValue = property(lambda self: self.interpolationCustom(), lambda self, value: self.setInterpolationCustom_(value))
'''
	.. attribute:: customValue
	Value for interpolation in design space.
	
	.. deprecated:: 2.5.2
		Use :attr:`axes <GSInstance.axes>` instead.
	
	:type: float
'''
GSInstance.isItalic = property(lambda self: bool(self.pyobjc_instanceMethods.isItalic()), lambda self, value: self.setIsItalic_(value))
'''
	.. attribute:: isItalic
	Italic flag for style linking
	:type: bool
'''

GSInstance.isBold = property(lambda self: bool(self.pyobjc_instanceMethods.isBold()), lambda self, value: self.setIsBold_(value))
'''
	.. attribute:: isBold
	Bold flag for style linking
	:type: bool
'''

GSInstance.linkStyle = property(lambda self: self.pyobjc_instanceMethods.linkStyle(), lambda self, value: self.setLinkStyle_(value))
'''
	.. attribute:: linkStyle
	Linked style
	:type: string
'''

GSInstance.familyName = property(lambda self: self.pyobjc_instanceMethods.familyName(), lambda self, value: self.setCustomParameter_forKey_(value, "familyName"))
'''
	.. attribute:: familyName
	familyName
	:type: string
'''

GSInstance.preferredFamily = property(lambda self: self.pyobjc_instanceMethods.preferredFamily(), lambda self, value: self.setCustomParameter_forKey_(value, "preferredFamily"))
'''
	.. attribute:: preferredFamily
	preferredFamily
	:type: string
'''

GSInstance.preferredSubfamilyName = property(lambda self: self.pyobjc_instanceMethods.preferredSubfamilyName(), lambda self, value: self.setCustomParameter_forKey_(value, "preferredSubfamilyName"))
'''
	.. attribute:: preferredSubfamilyName
	preferredSubfamilyName
	:type: string
'''

GSInstance.windowsFamily = property(lambda self: self.pyobjc_instanceMethods.windowsFamily(), lambda self, value: self.setCustomParameter_forKey_(value, "styleMapFamilyName"))
'''
	.. attribute:: windowsFamily
	windowsFamily
	:type: string
'''

GSInstance.windowsStyle = property(lambda self: self.pyobjc_instanceMethods.windowsStyle())
'''
	.. attribute:: windowsStyle
	windowsStyle
	This is computed from "isBold" and "isItalic". Read-only.
	:type: string
'''

GSInstance.windowsLinkedToStyle = property(lambda self: self.pyobjc_instanceMethods.windowsLinkedToStyle())
'''
	.. attribute:: windowsLinkedToStyle
	windowsLinkedToStyle. Read-only.
	:type: string
'''

GSInstance.fontName = property(lambda self: self.pyobjc_instanceMethods.fontName(), lambda self, value: self.setCustomParameter_forKey_(value, "postscriptFontName"))
'''
	.. attribute:: fontName
	fontName (postscriptFontName)
	:type: string
'''

GSInstance.fullName = property(lambda self: self.pyobjc_instanceMethods.fullName(), lambda self, value: self.setCustomParameter_forKey_(value, "postscriptFullName"))
'''
	.. attribute:: fullName
	fullName (postscriptFullName)
	:type: string
'''

GSInstance.font = property(lambda self: self.pyobjc_instanceMethods.font(), lambda self, value: self.setFont_(value))
'''
	.. attribute:: font

	Reference to the :class:`GSFont` object that contains the instance. Normally that is set by the app, only if the instance is not actually added to the font, then set this manually.

	:type: GSFont

	.. versionadded:: 2.5.1
'''

GSInstance.customParameters = property(lambda self: CustomParametersProxy(self))
'''
	.. attribute:: customParameters
	The custom parameters. List of :class:`GSCustomParameter` objects. You can access them by name or by index.

	.. code-block:: python

		# access all parameters
		for parameter in font.instances[0].customParameters:
			print(parameter)

		# set a parameter
		font.instances[0].customParameters['hheaLineGap'] = 10

		# delete a parameter
		del(font.instances[0].customParameters['hheaLineGap'])

	:type: list, dict
'''

GSInstance.instanceInterpolations = property(lambda self: self.pyobjc_instanceMethods.instanceInterpolations(), lambda self, value: self.setInstanceInterpolations_(value))
'''
	.. attribute:: instanceInterpolations
	A dict that contains the interpolation coefficients for each master.
	This is automatically updated if you change interpolationWeight, interpolationWidth, interpolationCustom. It contains FontMaster IDs as keys and coefficients for that master as values.
	Or, you can set it manually if you set manualInterpolation to True. There is no UI for this, so you need to do that with a script.
	:type: dict
	'''

GSInstance.manualInterpolation = property(lambda self: bool(self.pyobjc_instanceMethods.manualInterpolation()), lambda self, value: self.setManualInterpolation_(value))
'''
	.. attribute:: manualInterpolation
	Disables automatic calculation of instanceInterpolations
	This allowes manual setting of instanceInterpolations.
	:type: bool
	'''

GSInstance.interpolatedFontProxy = property(lambda self: self.pyobjc_instanceMethods.interpolatedFont())

'''
	.. attribute:: interpolatedFontProxy

	a proxy font that acts similar to a normal font object but only interpolates the glyphs you ask it for.

	It is not properly wrapped yet. So you need to use the ObjectiveC methods directly.
'''

def Instance_FontObject(self):
	return self.font.generateInstance_error_(self, None)

GSInstance.interpolatedFont = property(lambda self: Instance_FontObject(self))

'''
	.. attribute:: interpolatedFont

	.. versionadded:: 2.3

	Returns a ready interpolated :class:`GSFont` object representing this instance. Other than the source object, this interpolated font will contain only one master and one instance.

	Note: When accessing several properties of such an instance consecutively, it is advisable to create the instance once into a variable and then use that. Otherwise, the instance object will be completely interpolated upon each access. See sample below.

	.. code-block:: python

		# create instance once
		interpolated = Glyphs.font.instances[0].interpolatedFont

		# then access it several times
		print(interpolated.masters)
		print(interpolated.instances)

		(<GSFontMaster "Light" width 100.0 weight 75.0>)
		(<GSInstance "Web" width 100.0 weight 75.0>)


	:type: :class:`GSFont`
	'''

def __set__lastExportedFilePath__(self, value):
	if value:
		self.tempData().setObject_forKey_(value, "lastExportedFilePath")
	else:
		self.tempData().removeObjectForKey_("lastExportedFilePath")
GSInstance.lastExportedFilePath = property(lambda self: self.tempData().objectForKey_("lastExportedFilePath"), lambda self, value: __set__lastExportedFilePath__(self, value))

'''
	.. attribute:: lastExportedFilePath

	.. versionadded:: 2.4.2

	:type: unicode
	'''



'''
	**Functions**


	.. function:: generate([Format, FontPath, AutoHint, RemoveOverlap, UseSubroutines, UseProductionNames, Containers])

	Exports the instance. All parameters are optional.

	:param str The format of the outlines: :const:`OTF` or :const:`TTF`. Default: OTF
	:param str FontPath: The destination path for the final fonts. If None, it uses the default location set in the export dialog
	:param bool AutoHint: If autohinting should be applied. Default: True
	:param bool RemoveOverlap: If overlaps should be removed. Default: True
	:param bool UseSubroutines: If to use subroutines for CFF. Default: True
	:param bool UseProductionNames: If to use production names. Default: True
	:param bool Containers: list of container formats. Use any of the following constants: :const:`PLAIN`, :const:`WOFF`, :const:`WOFF2`, :const:`EOT`. Default: PLAIN
	:return: On success, True, on failure error message.
	:rtype: bool/list


	.. code-block:: python

		# export all instances as OpenType (.otf) and WOFF2 to user's font folder

		exportFolder = '/Users/myself/Library/Fonts'

		for instance in Glyphs.font.instances:
			instance.generate(FontPath = exportFolder, Containers = [PLAIN, WOFF2])

		Glyphs.showNotification('Export fonts', 'The export of %s was successful.' % (Glyphs.font.familyName))
'''


class _ExporterDelegate_ (NSObject):
	def init(self):
		self = super(_ExporterDelegate_, self).init()
		self.result = True
		return self

	def collectResults_(self, Error): # Error might be a NSString or a NSError
		if Error.__class__.__name__ == "NSError":
			String = Error.localizedDescription()
			if Error.localizedRecoverySuggestion() and Error.localizedRecoverySuggestion().length() > 0:
				String = String.stringByAppendingString_(Error.localizedRecoverySuggestion())
			Error = unicode(String)
		self.result = Error

def __Instance_Export__(self, Format=OTF, FontPath=None, AutoHint=True, RemoveOverlap=True, UseSubroutines=True, UseProductionNames=True, Containers=None, ConvertNames=False, DecomposeSmartStuff=True):

	if Format not in [OTF, WOFF, WOFF2, TTF, UFO]:
		raise KeyError('The font format is not supported: %s (only \'OTF\' and \'TTF\')' % Format)

	ContainerList = None
	if Containers is not None:
		ContainerList = []
		for Container in Containers:
			if Container in [PLAIN, WOFF, WOFF2, EOT]:
				ContainerList.append(Container.lower())
			else:
				raise KeyError('The container format is not supported: %s (only \'WOFF\' \'WOFF2\' \'plain\' and \'EOT\')' % Container)

	if Format == UFO:
		if not FontPath:
			print("!", FontPath)
			raise ValueError('Please provide a FontPath')
		instanceFont = self.interpolatedFont
		return instanceFont.export(Format=Format, FontPath=FontPath, UseProductionNames=UseProductionNames, DecomposeSmartStuff=DecomposeSmartStuff)
	else:
		Font = self.font
		if FontPath is None:
			FontPath = NSUserDefaults.standardUserDefaults().objectForKey_("OTFExportPath")

		Format = Format.lower()	# GSExportInstanceOperation uses Format as file .extension
		Exporter = NSClassFromString("GSExportInstanceOperation").alloc().initWithFont_instance_outlineFormat_containers_(Font, self, Format, ContainerList)
		if FontPath is None:
			FontPath = NSUserDefaults.standardUserDefaults().objectForKey_("OTFExportPath")
		Exporter.setInstallFontURL_(NSURL.fileURLWithPath_(FontPath))
		# the following parameters can be set here or directly read from the instance.
		Exporter.setAutohint_(AutoHint)
		Exporter.setRemoveOverlap_(RemoveOverlap)
		Exporter.setUseSubroutines_(UseSubroutines)
		Exporter.setUseProductionNames_(UseProductionNames)

		Exporter.setTempPath_(os.path.expanduser("~/Library/Application Support/Glyphs/Temp/")) # this has to be set correctly.

		Delegate = _ExporterDelegate_.alloc().init() # the collectResults_() method of this object will be called on case the exporter has to report a problem.
		Exporter.setDelegate_(Delegate)
		Exporter.main()
		if Delegate.result is True:
			self.lastExportedFilePath = Exporter.finalFontPath()
		else:
			self.lastExportedFilePath = None
		return Delegate.result

GSInstance.generate = __Instance_Export__

def __Font_Export__(self, Format=OTF, Instances=None, FontPath=None, AutoHint=True, RemoveOverlap=True, UseSubroutines=True, UseProductionNames=True, Containers=None, DecomposeSmartStuff=True):
	if Format not in [OTF, WOFF, WOFF2, TTF, VARIABLE, UFO]:
		raise KeyError('The font format is not supported: %s (only \'OTF\' and \'TTF\')' % Format)

	if FontPath is None:
		FontPath = Glyphs.defaults["OTFExportPath"]

	if Format == VARIABLE:
		Font = self.font()
		Exporter = NSClassFromString("GlyphsFileFormatVariationFonts").alloc().init()
		Exporter.setFont_(Font)
		result = Exporter._exportToURL_error_(NSURL.fileURLWithPath_(FontPath), None)
		return result
	elif Format == UFO:
		Font = self.font()
		Exporter = NSClassFromString("GlyphsFileFormatUFO").alloc().init()
		Exporter.setConvertNames_(UseProductionNames)
		Exporter.setDecomposeSmartStuff_(DecomposeSmartStuff)
		Exporter.setExportOptions_({"SeletedMasterIndexes": NSIndexSet.indexSetWithIndexesInRange_(NSRange(0, len(Font.masters)))})
		result = Exporter.exportFont_toDirectory_error_(Font, NSURL.fileURLWithPath_(FontPath), None)
		return result
	else:
		if not Instances:
			Instances = [i for i in self.instances if i.active]
		allResults = []
		for i in Instances:
			result = i.generate(Format=Format, FontPath=None, AutoHint=True, RemoveOverlap=True, UseSubroutines=True, UseProductionNames=True, Containers=None)
			allResults.append(result)
		return allResults

GSFont.export = __Font_Export__


def AddInstanceAsMaster(self):
	self.font.addFontAsNewMaster_(self.interpolatedFont.masters[0])

GSInstance.addAsMaster = AddInstanceAsMaster


'''
	.. function:: addAsMaster()

	New after 2.6.2

	Add this instance as a new master to the font. Identical to "Instance as Master" menu item in the Font Info’s Instances section.

'''




##################################################################################
#
#
#
#           GSCustomParameter
#
#
#
##################################################################################


def ______________________________(): pass
def ____GSCustomParameter____(): pass
def ______________________________(): pass


'''

:mod:`GSCustomParameter`
===============================================================================

Implementation of the Custom Parameter object. It stores a name/value pair.

You can append GSCustomParameter objects for example to GSFont.customParameters, but this way you may end up with duplicates.
It is best to access the custom parameters through its dictionary interface like this:
.. code-block:: python

	# access all parameters
	for parameter in font.customParameters:
		print(parameter)

	# set a parameter
	font.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'

	# delete a parameter
	del(font.customParameters['trademark'])

.. class:: GSCustomParameter([name, value])

	:param name: The name
	:param size: The value
'''

GSCustomParameter.__new__ = staticmethod(GSObject__new__)

def CustomParameter__init__(self, name, value):
	self.setName_(name)
	self.setValue_(value)

GSCustomParameter.__init__ = CustomParameter__init__

def CustomParameter__repr__(self):
	return "<GSCustomParameter %s: %s>" % (self.name, self.value)
GSCustomParameter.__repr__ = python_method(CustomParameter__repr__)

GSCustomParameter.mutableCopyWithZone_ = GSObject__copy__


'''
	Properties

	.. autosummary::

		name
		value

	**Properties**

'''

GSCustomParameter.name = property(lambda self: self.pyobjc_instanceMethods.name(), lambda self, value: self.setName_(value))
'''
	.. attribute:: name
	:type: str
'''
GSCustomParameter.value = property(lambda self: self.pyobjc_instanceMethods.value(), lambda self, value: self.setValue_(value))
'''
	.. attribute:: value
	:type: str, list, dict, int, float
'''










##################################################################################
#
#
#
#           GSClass
#
#
#
##################################################################################


def _________________(): pass
def ____GSClass____(): pass
def _________________(): pass

'''
:mod:`GSClass`
===============================================================================

Implementation of the class object. It is used to store OpenType classes.

For details on how to access them, please look at :class:`GSFont.classes`

.. class:: GSClass([tag, code])

	:param tag: The class name
	:param code: A list of glyph names, separated by space or newline

	.. autosummary::

		name
		code
		automatic
		active

	**Properties**

'''

GSClass.__new__ = staticmethod(GSObject__new__)

def Class__init__(self, name=None, code=None):
	if name is not None:
		self.setName_(name)
	if code is not None:
		self.setCode_(code)
GSClass.__init__ = Class__init__

def Class__repr__(self):
	return "<GSClass \"%s\">" % (self.name)
GSClass.__repr__ = python_method(Class__repr__)

GSClass.mutableCopyWithZone_ = GSObject__copy__

GSClass.name = property(lambda self: self.pyobjc_instanceMethods.name(),
						lambda self, value: self.setName_(value))
'''
	.. attribute:: name
	The class name
	:type: unicode
'''

GSClass.code = property(lambda self: self.pyobjc_instanceMethods.code(),
						lambda self, value: self.setCode_(value))
'''
	.. attribute:: code
	A string with space separated glyph names.
	:type: unicode
'''

GSClass.automatic = property(lambda self: self.pyobjc_instanceMethods.automatic(),
							lambda self, value: self.setAutomatic_(value))
'''
	.. attribute:: automatic
	Define whether this class should be auto-generated when pressing the 'Update' button in the Font Info.
	:type: bool
'''

GSClass.active = property(lambda self: not self.disabled(),
									lambda self, value: self.setDisabled_(not value))
'''
	.. attribute:: active
	:type: bool

	.. versionadded:: 2.5
'''


##################################################################################
#
#
#
#           GSFeaturePrefix
#
#
#
##################################################################################

def _________________________(): pass
def ____GSFeaturePrefix____(): pass
def _________________________(): pass


'''
:mod:`GSFeaturePrefix`
===============================================================================

Implementation of the featurePrefix object. It is used to store things that need to be outside of a feature like standalone lookups.

For details on how to access them, please look at :class:`GSFont.featurePrefixes`

.. class:: GSFeaturePrefix([tag, code])

	:param tag: The Prefix name
	:param code: The feature code in Adobe FDK syntax

	.. autosummary::

		name
		code
		automatic
		active

	**Properties**

'''

GSFeaturePrefix.__new__ = staticmethod(GSObject__new__)

def FeaturePrefix__init__(self, name=None, code=None):
	if name is not None:
		self.setName_(name)
	if code is not None:
		self.setCode_(code)

GSFeaturePrefix.__init__ = FeaturePrefix__init__

def FeaturePrefix__repr__(self):
	return "<GSFeaturePrefix \"%s\">" % (self.name)
GSFeaturePrefix.__repr__ = python_method(FeaturePrefix__repr__)

GSFeaturePrefix.mutableCopyWithZone_ = GSObject__copy__

GSFeaturePrefix.name = property(lambda self: self.pyobjc_instanceMethods.name(),
						lambda self, value: self.setName_(value))
'''
	.. attribute:: name
	The FeaturePrefix name
	:type: unicode
'''

GSFeaturePrefix.code = property(lambda self: self.pyobjc_instanceMethods.code(),
						lambda self, value: self.setCode_(value))
'''
	.. attribute:: code
	A String containing feature code.
	:type: unicode
'''

GSFeaturePrefix.automatic = property(lambda self: self.pyobjc_instanceMethods.automatic(),
									lambda self, value: self.setAutomatic_(value))
'''
	.. attribute:: automatic
	Define whether this should be auto-generated when pressing the 'Update' button in the Font Info.
	:type: bool
'''

GSFeaturePrefix.active = property(lambda self: not self.disabled(),
									lambda self, value: self.setDisabled_(not value))
'''
	.. attribute:: active
	:type: bool

	.. versionadded:: 2.5
'''



##################################################################################
#
#
#
#           GSFeature
#
#
#
##################################################################################

def ___________________(): pass
def ____GSFeature____(): pass
def ___________________(): pass

'''

:mod:`GSFeature`
===============================================================================

Implementation of the feature object. It is used to implement OpenType Features in the Font Info.

For details on how to access them, please look at :class:`GSFont.features`

.. class:: GSFeature([tag, code])

	:param tag: The feature name
	:param code: The feature code in Adobe FDK syntax

	Properties

	.. autosummary::

		name
		code
		automatic
		notes
		active

	Functions

	.. autosummary::

		update()

	**Properties**

'''


GSFeature.__new__ = staticmethod(GSObject__new__)

def Feature__init__(self, name=None, code=None):
	if name is not None:
		self.setName_(name)
	if code is not None:
		self.setCode_(code)

GSFeature.__init__ = Feature__init__

def Feature__repr__(self):
	return "<GSFeature \"%s\">" % (self.name)
GSFeature.__repr__ = python_method(Feature__repr__)

GSFeature.mutableCopyWithZone_ = GSObject__copy__

GSFeature.name = property(lambda self: self.pyobjc_instanceMethods.name(),
							lambda self, value: self.setName_(value))
'''
	.. attribute:: name
	The feature name
	:type: unicode
'''

GSFeature.code = property(lambda self: self.pyobjc_instanceMethods.code(),
							lambda self, value: self.setCode_(value))
'''
	.. attribute:: code
	The Feature code in Adobe FDK syntax.
	:type: unicode
'''
GSFeature.automatic = property(lambda self: self.pyobjc_instanceMethods.automatic(),
								lambda self, value: self.setAutomatic_(value))
'''
	.. attribute:: automatic
	Define whether this feature should be auto-generated when pressing the 'Update' button in the Font Info.
	:type: bool
'''

GSFeature.notes = property(lambda self: self.pyobjc_instanceMethods.notes(),
							lambda self, value: self.setNotes_(value))
'''
	.. attribute:: notes
	Some extra text. Is shown in the bottom of the feature window. Contains the stylistic set name parameter
	:type: unicode
'''

GSFeature.active = property(lambda self: not self.disabled(),
							lambda self, value: self.setDisabled_(not value))
'''
	.. attribute:: active
	:type: bool

	.. versionadded:: 2.5


	**Functions**

	.. function:: update()

	Calls the automatic feature code generator for this feature.
	You can use this to update all OpenType features before export.

	:return: None

	.. code-block:: python

		# first update all features
		for feature in font.features:
			if feature.automatic:
				feature.update()

		# then export fonts
		for instance in font.instances:
			if instance.active:
				instance.generate()

'''








##################################################################################
#
#
#
#           GSSubstitution
#
#
#
##################################################################################

def ________________________(): pass
def ____GSSubstitution____(): pass
def ________________________(): pass


"""

############ NOCH NICHT DOKUMENTIERT WEIL NOCH NICHT AUSGEREIFT ############

"""


GSSubstitution.__new__ = staticmethod(GSObject__new__)

def Substitution__init__(self):
	pass
GSSubstitution.__init__ = Substitution__init__


GSSubstitution.source = property(lambda self: self.pyobjc_instanceMethods.back(),
								lambda self, value: self.setBack_(value))
GSSubstitution.source = property(lambda self: self.pyobjc_instanceMethods.source(),
								lambda self, value: self.setSource_(value))
GSSubstitution.forward = property(lambda self: self.pyobjc_instanceMethods.fwd(),
								lambda self, value: self.setFwd_(value))

GSSubstitution.target = property(lambda self: self.pyobjc_instanceMethods.target(),
								lambda self, value: self.setTarget_(value))
GSSubstitution.languageTag = property(lambda self: self.pyobjc_instanceMethods.languageTag(),
								lambda self, value: self.setLanguageTag_(value))
GSSubstitution.scriptTag = property(lambda self: self.pyobjc_instanceMethods.scriptTag(),
								lambda self, value: self.setScriptTag_(value))











##################################################################################
#
#
#
#           GSGlyph
#
#
#
##################################################################################


def _________________(): pass
def ____GSGlyph____(): pass
def _________________(): pass


'''


:mod:`GSGlyph`
===============================================================================

Implementation of the glyph object.

For details on how to access these glyphs, please see :class:`GSFont.glyphs`

.. class:: GSGlyph([name])

	:param name: The glyph name

	Properties

	.. autosummary::

		parent
		layers
		name
		unicode
		string
		id
		category
		storeCategory
		subCategory
		storeSubCategory
		script
		storeScript
		productionName
		storeProductionName
		glyphInfo
		leftKerningGroup
		rightKerningGroup
		leftKerningKey
		rightKerningKey
		leftMetricsKey
		rightMetricsKey
		widthMetricsKey
		export
		color
		colorObject
		note
		selected
		mastersCompatible
		userData
		smartComponentAxes
		lastChange


	Functions

	.. autosummary::

		beginUndo()
		endUndo()
		updateGlyphInfo()
		duplicate()

	**Properties**

'''


GSGlyph.__new__ = staticmethod(GSObject__new__)

def Glyph__init__(self, name=None):
	if name and (isinstance(name, str) or isinstance(name, unicode)):
		self.setName_(name)
GSGlyph.__init__ = Glyph__init__

def Glyph__repr__(self):
	return "<GSGlyph \"%s\" with %s layers>" % (self.name, len(self.layers))
GSGlyph.__repr__ = python_method(Glyph__repr__)

GSGlyph.mutableCopyWithZone_ = GSObject__copy__

GSGlyph.parent = property(lambda self: self.pyobjc_instanceMethods.parent(),
									lambda self, value: self.setParent_(value))
'''
	.. attribute:: parent
	Reference to the :class:`GSFont` object.

	:type: :class:`GSFont`
'''
GSGlyph.layers = property(lambda self: GlyphLayerProxy(self),
							lambda self, value: GlyphLayerProxy(self).setter(value))

'''
	.. attribute:: layers

	The layers of the glyph, collection of :class:`GSLayer` objects. You can access them either by index or by layer ID, which can be a :attr:`GSFontMaster.id`.
	The layer IDs are usually a unique string chosen by Glyphs.app and not set manually. They may look like this: 3B85FBE0-2D2B-4203-8F3D-7112D42D745E

	:type: list, dict

	.. code-block:: python

		# get active layer
		layer = font.selectedLayers[0]

		# get glyph of this layer
		glyph = layer.parent

		# access all layers of this glyph
		for layer in glyph.layers:
			print(layer.name)

		# access layer of currently selected master of active glyph ...
		# (also use this to access a specific layer of glyphs selected in the Font View)
		layer = glyph.layers[font.selectedFontMaster.id]

		# ... which is exactly the same as:
		layer = font.selectedLayers[0]

		# directly access 'Bold' layer of active glyph
		for master in font.masters:
			if master.name == 'Bold':
				id = master.id
				break
		layer = glyph.layers[id]

		# add a new layer
		newLayer = GSLayer()
		newLayer.name = '{125, 100}' # (example for glyph-level intermediate master)
		# you may set the master ID that this layer will be associated with, otherwise the first master will be used
		newLayer.associatedMasterId = font.masters[-1].id # attach to last master
		font.glyphs['a'].layers.append(newLayer)

		# duplicate a layer under a different name
		newLayer = font.glyphs['a'].layers[0].copy()
		newLayer.name = 'Copy of layer'
		# FYI, this will still be the old layer ID (in case of duplicating) at this point
		print(newLayer.layerId)
		font.glyphs['a'].layers.append(newLayer)
		# FYI, the layer will have been assigned a new layer ID by now, after having been appended
		print(newLayer.layerId)

		# replace the second master layer with another layer
		newLayer = GSLayer()
		newLayer.layerId = font.masters[1].id # Make sure to sync the master layer ID
		font.glyphs['a'].layers[font.masters[1].id] = newLayer

		# delete last layer of glyph
		# (Also works for master layers. They will be emptied)
		del(font.glyphs['a'].layers[-1])

		# delete currently active layer
		del(font.glyphs['a'].layers[font.selectedLayers[0].layerId])

'''

def GSGlyph_setName(self, name):
	if name == self.name:
		pass
	elif (self.parent and not self.parent.glyphs.has_key(name)) or not self.parent:
		self.setName_changeName_update_(name, False, True)
	else:
		raise NameError('The glyph name \"%s\" already exists in the font.' % name)

GSGlyph.name = property(lambda self: self.pyobjc_instanceMethods.name(),
									lambda self, value: GSGlyph_setName(self, value))
'''
	.. attribute:: name
	The name of the glyph. It will be converted to a "nice name" (afii10017 to A-cy) (you can disable this behavior in font info or the app preference)
	:type: unicode
'''

GSGlyph.unicode = property(lambda self: self.pyobjc_instanceMethods.unicode(),
									lambda self, value: self.setUnicode_(value))
'''
	.. attribute:: unicode
	String with the hex Unicode value of glyph, if encoded.
	:type: unicode
'''
def __glyph__unicode__(self):
	codes = self.pyobjc_instanceMethods.unicodes()
	if codes and len(codes):
		return list(codes)
	return None

GSGlyph.unicodes = property(lambda self: __glyph__unicode__(self),
							lambda self, value: self.setUnicodes_(value))
'''
	.. attribute:: unicodes
	List of String‚ with the hex Unicode values of glyph, if encoded.
	:type: unicode
'''

GSGlyph.production = property(lambda self: self.pyobjc_instanceMethods.production(),
									lambda self, value: self.setProduction_(self, value))

GSGlyph.string = property(lambda self: self.charString())
'''
	.. attribute:: string
	String representation of glyph, if encoded.
	This is similar to the string representation that you get when copying glyphs into the clipboard.
	:type: unicode
'''

GSGlyph.id = property(lambda self: str(self.pyobjc_instanceMethods.id()),
									lambda self, value: self.setId_(value))
'''
	.. attribute:: id
	An unique identifier for each glyph
	:type: string
'''

GSGlyph.category = property(lambda self: self.pyobjc_instanceMethods.category(),
									lambda self, value: self.setCategory_(value))
'''
	.. attribute:: category
	The category of the glyph. e.g. 'Letter', 'Symbol'
	Setting only works if `storeCategory` is set (see below).
	:type: unicode
'''

GSGlyph.storeCategory = property(lambda self: bool(self.pyobjc_instanceMethods.storeCategory()),
									lambda self, value: self.setStoreCategory_(value))
'''
	.. attribute:: storeCategory
	Set to True in order to manipulate the `category` of the glyph (see above).
	Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.
	:type: bool
'''

GSGlyph.subCategory = property(lambda self: self.pyobjc_instanceMethods.subCategory(),
									lambda self, value: self.setSubCategory_(value))
'''
	.. attribute:: subCategory
	The subCategory of the glyph. e.g. 'Uppercase', 'Math'
	Setting only works if `storeSubCategory` is set (see below).
	:type: unicode
'''

GSGlyph.storeSubCategory = property(lambda self: bool(self.pyobjc_instanceMethods.storeSubCategory()),
									lambda self, value: self.setStoreSubCategory_(value))
'''
	.. attribute:: storeSubCategory
	Set to True in order to manipulate the `subCategory` of the glyph (see above).
	Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.
	:type: bool

	.. versionadded:: 2.3
'''

GSGlyph.script = property(lambda self: self.pyobjc_instanceMethods.script(),
									lambda self, value: self.setScript_(value))
'''
	.. attribute:: script
	The script of the glyph, e.g., 'latin', 'arabic'.
	Setting only works if `storeScript` is set (see below).
	:type: unicode
'''

GSGlyph.storeScript = property(lambda self: bool(self.pyobjc_instanceMethods.storeScript()),
									lambda self, value: self.setStoreScript_(value))
'''
	.. attribute:: storeScript
	Set to True in order to manipulate the `script` of the glyph (see above).
	Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.
	:type: bool

	.. versionadded:: 2.3
'''

GSGlyph.productionName = property(lambda self: self.pyobjc_instanceMethods.production(),
									lambda self, value: self.setProduction_(value))
'''
	.. attribute:: productionName
	The productionName of the glyph.
	Setting only works if `storeProductionName` is set (see below).
	:type: unicode

	.. versionadded:: 2.3
'''

GSGlyph.storeProductionName = property(lambda self: bool(self.storeProduction()),
									lambda self, value: self.setStoreProduction_(value))
'''
	.. attribute:: storeProductionName
	Set to True in order to manipulate the `productionName` of the glyph (see above).
	Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.
	:type: bool

	.. versionadded:: 2.3
'''


GSGlyph.glyphInfo = property(lambda self: self.parent.glyphsInfo().glyphInfoForGlyph_(self))
'''
	.. attribute:: glyphInfo
	:class:`GSGlyphInfo` object for this glyph with detailed information.
	:type: :class:`GSGlyphInfo`
'''

def __GSGlyph_glyphDataEntryString__(self):
	Unicode = self.unicode
	if Unicode is None or len(Unicode) < 3:
		Unicode = ""
	Decompose = self.layers[0].componentNamesText()
	if Decompose is not None and len(Decompose) > 0:
		Decompose = "decompose=\"%s\" " % Decompose
	else:
		Decompose = ""
	SubCategory = ""
	if self.subCategory != "Other":
		SubCategory = "subCategory=\"%s\" " % self.subCategory
	Anchors = self.layers[0].anchors.keys()
	if Anchors is not None and len(Anchors) > 0:
		Anchors = "anchors=\"%s\" " % ", ".join(sorted(Anchors))
	else:
		Anchors = ""
	GlyphInfo = self.glyphInfo
	Accents = None
	if GlyphInfo is not None:
		Accents = GlyphInfo.accents
	if Accents is not None and len(Accents) > 0:
		Accents = "accents=\"%s\"" % ", ".join(sorted(Accents))
	else:
		Accents = ""
	Production = ""
	if self.productionName is not None and len(self.productionName) > 0:
		Production = self.productionName
	else:
		Production = Glyphs.productionGlyphName(self.name)
	if len(Production) > 0:
		Production = "production=\"%s\"" % Production
	else:
		Production = ""
	if self.note is not None and len(self.note) > 0:
		Production += " altNames=\"%s\"" % self.note
	return "	<glyph unicode=\"%s\" name=\"%s\" %scategory=\"%s\" %sscript=\"%s\" description=\"\" %s%s%s />" % (Unicode, self.name, Decompose, self.category, SubCategory, self.script, Production, Anchors, Accents)

GSGlyph.glyphDataEntryString = __GSGlyph_glyphDataEntryString__

GSGlyph.leftKerningGroup = property(lambda self: self.pyobjc_instanceMethods.leftKerningGroup(),
									lambda self, value: self.setLeftKerningGroup_(NSStr(value)))
'''
	.. attribute:: leftKerningGroup
	The leftKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.
	:type: unicode'''
GSGlyph.rightKerningGroup = property(lambda self: self.pyobjc_instanceMethods.rightKerningGroup(),
									lambda self, value: self.setRightKerningGroup_(NSStr(value)))
'''
	.. attribute:: rightKerningGroup
	The rightKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.
	:type: unicode'''

def GSGlyph__leftKerningKey(self):
	if self.leftKerningGroupId():
		return self.leftKerningGroupId()
	else:
		return self.name
GSGlyph.leftKerningKey = property(lambda self: GSGlyph__leftKerningKey(self))

'''
	.. attribute:: leftKerningKey

	The key to be used with the kerning functions (:meth:`GSFont.kerningForPair()`, :meth:`GSFont.setKerningForPair()`:meth:`GSFont.removeKerningForPair()`).

	If the glyph has a :att:`leftKerningGroup <GSGlyph.leftKerningGroup>` attribute, the internally used `@MMK_R_xx` notation will be returned (note that the R in there stands for the right side of the kerning pair for LTR fonts, which corresponds to the left kerning group of the glyph). If no group is given, the glyph’s name will be returned.
	:type: string

	.. code-block:: python

		# Set kerning for 'T' and all members of kerning class 'a'
		# For LTR fonts, always use the .rightKerningKey for the first (left) glyph of the pair, .leftKerningKey for the second (right) glyph.
		font.setKerningForPair(font.selectedFontMaster.id, font.glyphs['T'].rightKerningKey, font.glyphs['a'].leftKerningKey, -60)

		# which corresponds to:
		font.setKerningForPair(font.selectedFontMaster.id, 'T', '@MMK_R_a', -60)

	.. versionadded:: 2.4
'''

def GSGlyph__rightKerningKey(self):
	if self.rightKerningGroupId():
		return self.rightKerningGroupId()
	else:
		return self.name
GSGlyph.rightKerningKey = property(lambda self: GSGlyph__rightKerningKey(self))

'''
	.. attribute:: rightKerningKey

	The key to be used with the kerning functions (:meth:`GSFont.kerningForPair()`, :meth:`GSFont.setKerningForPair()`:meth:`GSFont.removeKerningForPair()`).

	If the glyph has a  :att:`rightKerningGroup <GSGlyph.rightKerningGroup>` attribute, the internally used `@MMK_L_xx` notation will be returned (note that the L in there stands for the left side of the kerning pair for LTR fonts, which corresponds to the right kerning group of the glyph). If no group is given, the glyph’s name will be returned.

	See above for an example.

	:type: string

	.. versionadded:: 2.4
'''

GSGlyph.leftMetricsKey = property(lambda self: self.pyobjc_instanceMethods.leftMetricsKey(),
									lambda self, value: self.setLeftMetricsKey_(NSStr(value)))
'''
	.. attribute:: leftMetricsKey
	The leftMetricsKey of the glyph. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.
	:type: unicode'''
GSGlyph.rightMetricsKey = property(lambda self: self.pyobjc_instanceMethods.rightMetricsKey(),
									lambda self, value: self.setRightMetricsKey_(NSStr(value)))
'''
	.. attribute:: rightMetricsKey
	The rightMetricsKey of the glyph. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.
	:type: unicode'''
GSGlyph.widthMetricsKey = property(lambda self: self.pyobjc_instanceMethods.widthMetricsKey(),
									lambda self, value: self.setWidthMetricsKey_(NSStr(value)))
'''
	.. attribute:: widthMetricsKey
	The widthMetricsKey of the glyph. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.
	:type: unicode'''
GSGlyph.export = property(lambda self: bool(self.pyobjc_instanceMethods.export()),
							lambda self, value: self.setExport_(value))

'''
	.. attribute:: export
	Defines whether glyph will export upon font generation
	:type: bool
'''

def __getColorIndex__(self):
	color = self.colorIndex()
	if color > 20 or color < 0:
		return None
	return color

def __setColorIndex(self, value):
	if value is None:
		value = -1
	self.setColorIndex_(value)
	
GSGlyph.color = property(lambda self: __getColorIndex__(self),
						lambda self, value: __setColorIndex(self, value))
'''
	.. attribute:: color
	Color marking of glyph in UI
	:type: int

	.. code-block:: python

		glyph.color = 0		# red
		glyph.color = 1		# orange
		glyph.color = 2		# brown
		glyph.color = 3		# yellow
		glyph.color = 4		# light green
		glyph.color = 5		# dark green
		glyph.color = 6		# light blue
		glyph.color = 7		# dark blue
		glyph.color = 8		# purple
		glyph.color = 9		# magenta
		glyph.color = 10	# light gray
		glyph.color = 11	# charcoal
		glyph.color = None	# not colored, white (before version 1235, use -1)
'''

def _set_Glyph_setColor(self, colorValue):
	if isinstance(colorValue, (tuple, list)):
		if max(colorValue) > 1:
			colorValue = [c / 255.0 if c > 1 else c for c in colorValue]
		colorValue = list(colorValue)
		colorValue.extend((1, 1, 1))
		print(colorValue)
		colorValue = NSColor.colorWithDeviceRed_green_blue_alpha_(colorValue[0], colorValue[1], colorValue[2], colorValue[3])
	self.setColor_(colorValue)

GSGlyph.colorObject = property(lambda self: self.pyobjc_instanceMethods.color(),
								lambda self, value: _set_Glyph_setColor(self, value))
'''
	.. attribute:: colorObject

	

	NSColor object of glyph color, useful for drawing in plugins.
	:type: NSColor

	.. code-block:: python

		# use glyph color to draw the outline
		glyph.colorObject.set()

		# Get RGB (and alpha) values (as float numbers 0..1, multiply with 256 if necessary)
		R, G, B, A = glyph.colorObject.colorUsingColorSpace_(NSColorSpace.genericRGBColorSpace()).getRed_green_blue_alpha_(None, None, None, None)

		print(R, G, B)
		0.617805719376 0.958198726177 0.309286683798

		print(round(R * 256), int(G * 256), int(B * 256))
		158 245 245

		# Draw layer
		glyph.layers[0].bezierPath.fill()

		# set the glyph color.

		glyph.colorObject = NSColor.colorWithDeviceRed_green_blue_alpha_(247.0 / 255.0, 74.0 / 255.0, 62.9 / 255.0, 1)

		new in 2.4.2:
		glyph.colorObject = (247.0, 74.0, 62.9) #
		or
		glyph.colorObject = (247.0, 74.0, 62.9, 1) #
		or
		glyph.colorObject = (0.968, 0.29, 0.247, 1) #

	.. versionadded:: 2.3
'''


GSGlyph.note = property(lambda self: self.pyobjc_instanceMethods.note(),
						lambda self, value: self.setNote_(value))
'''
	.. attribute:: note
	:type: unicode
'''


def _get_Glyphs_is_selected(self):
	Doc = self.parent.parent
	return Doc.windowController().glyphsController().selectedObjects().containsObject_(self)

def _set_Glyphs_is_selected(self, isSelected):
	ArrayController = self.parent.parent.windowController().glyphsController()
	if isSelected:
		ArrayController.addSelectedObjects_([self])
	else:
		ArrayController.removeSelectedObjects_([self])

GSGlyph.selected = property(lambda self: _get_Glyphs_is_selected(self),
							lambda self, value: _set_Glyphs_is_selected(self, value))
'''
	.. attribute:: selected
	Return True if the Glyph is selected in the Font View.
	This is different to the property font.selectedLayers which returns the selection from the active tab.
	:type: bool

	.. code-block:: python

		# access all selected glyphs in the Font View
		for glyph in font.glyphs:
			if glyph.selected:
				print(glyph)
'''

GSGlyph.mastersCompatible = property(lambda self: bool(self.pyobjc_instanceMethods.mastersCompatible()))

'''
	.. attribute:: mastersCompatible

	.. versionadded:: 2.3

	Return True when all layers in this glyph are compatible (same components, anchors, paths etc.)
	:type: bool

'''

GSGlyph.userData = property(lambda self: UserDataProxy(self))
'''
	.. attribute:: userData

	.. versionadded:: 2.3

	A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the data will not be recoverable from the saved file.
	:type: dict
	.. code-block:: python
		# set value
		glyph.userData['rememberToMakeCoffee'] = True

		# delete value
		del glyph.userData['rememberToMakeCoffee']
'''

GSGlyph.smartComponentAxes = property(lambda self: GlyphSmartComponentAxesProxy(self), lambda self, value: GlyphSmartComponentAxesProxy(self).setter(value))
'''
	.. attribute:: smartComponentAxes

	.. versionadded:: 2.3

	A list of :class:`GSSmartComponentAxis` objects.

	These are the axis definitions for the interpolations that take place within the Smart Components. Corresponds to the 'Properties' tab of the glyph's 'Show Smart Glyph Settings' dialog.

	Also see https://glyphsapp.com/tutorials/smart-components for reference.

	:type: list

	.. code-block:: python
		# Adding two interpolation axes to the glyph

		axis1 = GSSmartComponentAxis()
		axis1.name = 'crotchDepth'
		axis1.topValue = 0
		axis1.bottomValue = -100
		g.smartComponentAxes.append(axis1)

		axis2 = GSSmartComponentAxis()
		axis2.name = 'shoulderWidth'
		axis2.topValue = 100
		axis2.bottomValue = 0
		g.smartComponentAxes.append(axis2)

		# Deleting one axis
		del g.smartComponentAxes[1]
'''

def __GSGlyph__lastChange__(self):
	try:
		return datetime.datetime.fromtimestamp(self.pyobjc_instanceMethods.lastChange().timeIntervalSince1970())
	except:
		return None
GSGlyph.lastChange = property(lambda self: __GSGlyph__lastChange__(self))

'''
	.. attribute:: lastChange

	.. versionadded:: 2.3

	Change date when glyph was last changed as datetime.

	Check Python’s :mod:`time` module for how to use the timestamp.
'''



'''

	**Functions**

'''



def __BeginUndo(self):
	self.undoManager().beginUndoGrouping()

GSGlyph.beginUndo = __BeginUndo

'''
	.. function:: beginUndo()

	Call this before you do a longer running change to the glyph. Be extra careful to call Glyph.endUndo() when you are finished.
'''

def __EndUndo(self):
	self.undoManager().endUndoGrouping()
GSGlyph.endUndo = __EndUndo

'''
	.. function:: endUndo()

	This closes a undo group that was opened by a previous call of Glyph.beginUndo(). Make sure that you call this for each beginUndo() call.
'''

def __updateGlyphInfo(self, changeName=True):
	if self.parent is not None:
		self.parent.glyphsInfo().updateGlyphInfo_changeName_(self, changeName)
	else:
		GSGlyphsInfo.sharedManager().updateGlyphInfo_changeName_(self, changeName)
GSGlyph.updateGlyphInfo = __updateGlyphInfo

'''
	.. function:: updateGlyphInfo(changeName = True)

	Updates all information like name, unicode etc. for this glyph.
'''


def Glyph_Duplicate(self, name=None):

	newGlyph = self.copyThin_options_(False, 4) # option: 4 copy all layers
	if newGlyph.unicode:
		newGlyph.unicode = None
	if name:
		newGlyph.name = name
	else:
		newGlyph.name = self.parent.saveNameForName_(newGlyph.name)  # will add a .00X suffix
	self.parent.glyphs.append(newGlyph)
	return newGlyph

GSGlyph.duplicate = Glyph_Duplicate

'''
	.. function:: duplicate([name])

	Duplicate the glyph under a new name and return it.

	If no name is given, .00n will be appended to it.
'''




##################################################################################
#
#
#
#           GSLayer
#
#
#
##################################################################################

def _________________(): pass
def ____GSLayer____(): pass
def _________________(): pass


'''

:mod:`GSLayer`
===============================================================================

Implementation of the layer object.

For details on how to access these layers, please see :attr:`GSGlyph.layers`

.. class:: GSLayer()

	Properties

	.. autosummary::

		parent
		name
		master
		associatedMasterId
		layerId
		color
		colorObject
		components
		guides
		annotations
		hints
		anchors
		paths
		selection
		LSB
		RSB
		TSB
		BSB
		width
		leftMetricsKey
		rightMetricsKey
		widthMetricsKey
		bounds
		selectionBounds
		background
		backgroundImage
		bezierPath
		openBezierPath
		userData
		smartComponentPoleMapping
		isSpecialLayer
		isMasterLayer

	Functions

	.. autosummary::

		decomposeComponents()
		decomposeCorners()
		compareString()
		connectAllOpenPaths()
		copyDecomposedLayer()
		syncMetrics()
		correctPathDirection()
		removeOverlap()
		roundCoordinates()
		addNodesAtExtremes()
		beginChanges()
		endChanges()
		cutBetweenPoints()
		intersectionsBetweenPoints()
		addMissingAnchors()
		clearSelection()
		clear()
		swapForegroundWithBackground()
		reinterpolate()
		applyTransform()

		**Properties**

	'''

GSLayer.__new__ = staticmethod(GSObject__new__)

def Layer__init__(self):
	pass
GSLayer.__init__ = Layer__init__

def Layer__repr__(self):
	try:
		assert self.name
		name = self.name
	except:
		name = 'orphan'
	try:
		assert self.parent.name
		parent = self.parent.name
	except:
		parent = 'orphan'
	return "<%s \"%s\" (%s)>" % (self.className(), name, parent)
GSLayer.__repr__ = python_method(Layer__repr__)

GSLayer.mutableCopyWithZone_ = GSObject__copy__

GSLayer.parent = property(lambda self: self.pyobjc_instanceMethods.parent(),
									lambda self, value: self.setParent_(value))
GSBackgroundLayer.parent = property(lambda self: self.pyobjc_instanceMethods.parent(),
									lambda self, value: self.setParent_(value))
GSControlLayer.parent = property(lambda self: self.pyobjc_instanceMethods.parent())
'''
	.. attribute:: parent
	Reference to the :class:`glyph <GSGlyph>` object that this layer is attached to.
	:type: :class:`GSGlyph`
'''

GSLayer.name = property(lambda self: self.pyobjc_instanceMethods.name(),
									lambda self, value: self.setName_(value))

GSBackgroundLayer.name = property(lambda self: self.pyobjc_instanceMethods.name(),
									lambda self, value: self.setName_(value))
'''
	.. attribute:: name
	Name of layer
	:type: unicode
'''

def GSLayer__master__(self):
	if self.associatedMasterId:
		master = self.parent.parent.masters[self.associatedMasterId]
		return master


GSLayer.master = property(lambda self: GSLayer__master__(self))
'''
	.. attribute:: master
	Master that this layer is connected to. Read only.
	:type: GSFontMaster
'''

GSLayer.associatedMasterId = property(lambda self: self.pyobjc_instanceMethods.associatedMasterId(),
										lambda self, value: self.setAssociatedMasterId_(value))
'''
	.. attribute:: associatedMasterId
	The ID of the :class:`fontMaster <GSFontMaster>` this layer belongs to, in case this isn't a master layer. Every layer that isn't a master layer needs to be attached to one master layer.
	:type: unicode

	.. code-block:: python

		# add a new layer
		newLayer = GSLayer()
		newLayer.name = '{125, 100}' # (example for glyph-level intermediate master)

		# you may set the master ID that this layer will be associated with, otherwise the first master will be used
		newLayer.associatedMasterId = font.masters[-1].id # attach to last master
		font.glyphs['a'].layers.append(newLayer)
'''

GSLayer.layerId = property(lambda self: self.pyobjc_instanceMethods.layerId(),
							lambda self, value: self.setLayerId_(value))
'''
	.. attribute:: layerId
	The unique layer ID is used to access the layer in the :class:`glyphs <GSGlyph>` layer dictionary.

	For master layers this should be the id of the :class:`fontMaster <GSFontMaster>`.
	It could look like this: "FBCA074D-FCF3-427E-A700-7E318A949AE5"
	:type: unicode

	.. code-block:: python

		# see ID of active layer
		id = font.selectedLayers[0].layerId
		print(id)
		FBCA074D-FCF3-427E-A700-7E318A949AE5

		# access a layer by this ID
		layer = font.glyphs['a'].layers[id]
		layer = font.glyphs['a'].layers['FBCA074D-FCF3-427E-A700-7E318A949AE5']

		# for master layers, use ID of masters
		layer = font.glyphs['a'].layers[font.masters[0].id]
'''

GSLayer.color = property(lambda self: __getColorIndex__(self),
						lambda self, value: __setColorIndex(self, value))
'''
	.. attribute:: color
	Color marking of glyph in UI
	:type: int

	.. code-block:: python

		glyph.color = 0		# red
		glyph.color = 1		# orange
		glyph.color = 2		# brown
		glyph.color = 3		# yellow
		glyph.color = 4		# light green
		glyph.color = 5		# dark green
		glyph.color = 6		# light blue
		glyph.color = 7		# dark blue
		glyph.color = 8		# purple
		glyph.color = 9		# magenta
		glyph.color = 10	# light gray
		glyph.color = 11	# charcoal
		glyph.color = None	# not colored, white (before version 1235, use -1)
'''

GSLayer.colorObject = property(lambda self: self.pyobjc_instanceMethods.color(), lambda self, value: self.setColor_(value))
'''
	.. attribute:: colorObject

	.. versionadded:: 2.3

	NSColor object of layer color, useful for drawing in plugins.
	:type: NSColor

	.. code-block:: python

		# use layer color to draw the outline
		layer.colorObject.set()

		# Get RGB (and alpha) values (as float numbers 0..1, multiply with 256 if necessary)
		R, G, B, A = layer.colorObject.colorUsingColorSpace_(NSColorSpace.genericRGBColorSpace()).getRed_green_blue_alpha_(None, None, None, None)

		print(R, G, B)
		0.617805719376 0.958198726177 0.309286683798

		print(round(R * 256), int(G * 256), int(B * 256))
		158 245 245

		# Draw layer
		layer.bezierPath.fill()

		# set the layer color.

		layer.colorObject = NSColor.colorWithDeviceRed_green_blue_alpha_(247.0 / 255.0, 74.0 / 255.0, 62.9 / 255.0, 1)

'''


GSLayer.components = property(lambda self: LayerComponentsProxy(self),
								lambda self, value: LayerComponentsProxy(self).setter(value))
'''
	.. attribute:: components
	Collection of :class:`GSComponent` objects
	:type: list

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		# add component
		layer.components.append(GSComponent('dieresis'))

		# add component at specific position
		layer.components.append(GSComponent('dieresis', NSPoint(100, 100)))

		# delete specific component
		for i, component in enumerate(layer.components):
		        if component.componentName == 'dieresis':
		                del(layer.components[i])
		                break

		# copy components from another layer
		import copy
		layer.components = copy.copy(anotherlayer.components)

		# copy one component to another layer
		layer.components.append(anotherlayer.component[0].copy())

'''

GSLayer.guides = property(lambda self: LayerGuideLinesProxy(self),
							lambda self, value: LayerGuideLinesProxy(self).setter(value))

GSLayer.guideLines = GSLayer.guides

'''
	.. attribute:: guides
	List of :class:`GSGuideLine` objects.
	:type: list

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		# access all guides
		for guide in layer.guides:
			print(guide)

		# add guideline
		newGuide = GSGuideLine()
		newGuide.position = NSPoint(100, 100)
		newGuide.angle = -10.0
		layer.guides.append(newGuide)

		# delete guide
		del(layer.guides[0])

		# copy guides from another layer
		import copy
		layer.guides = copy.copy(anotherlayer.guides)
'''

GSLayer.annotations = property(lambda self: LayerAnnotationProxy(self),
								lambda self, value: LayerAnnotationProxy(self).setter(value))
'''
	.. attribute:: annotations
	List of :class:`GSAnnotation` objects.
	:type: list

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		# access all annotations
		for annotation in layer.annotations:
			print(annotation)

		# add new annotation
		newAnnotation = GSAnnotation()
		newAnnotation.type = TEXT
		newAnnotation.text = 'Fuck, this curve is ugly!'
		layer.annotations.append(newAnnotation)

		# delete annotation
		del(layer.annotations[0])

		# copy annotations from another layer
		import copy
		layer.annotations = copy.copy(anotherlayer.annotations)
'''


GSLayer.hints = property(lambda self: LayerHintsProxy(self),
						lambda self, value: LayerHintsProxy(self).setter(value))
'''
	.. attribute:: hints
	List of :class:`GSHint` objects.
	:type: list

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		# access all hints
		for hint in layer.hints:
			print(hint)

		# add a new hint
		newHint = GSHint()
		# change behaviour of hint here, like its attachment nodes
		layer.hints.append(newHint)

		# delete hint
		del(layer.hints[0])

		# copy hints from another layer
		import copy
		layer.hints = copy.copy(anotherlayer.hints)
		# remember to reconnect the hints' nodes with the new layer's nodes

'''

GSLayer.anchors = property(lambda self: LayerAnchorsProxy(self),
							lambda self, value: LayerAnchorsProxy(self).setter(value))
'''
	.. attribute:: anchors
	List of :class:`GSAnchor` objects.
	:type: list, dict

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		# access all anchors:
		for a in layer.anchors:
			print(a)

		# add a new anchor
		layer.anchors['top'] = GSAnchor()

		# delete anchor
		del(layer.anchors['top'])

		# copy anchors from another layer
		import copy
		layer.anchors = copy.copy(anotherlayer.anchors)
'''

GSLayer.paths = property(lambda self: LayerPathsProxy(self),
						lambda self, value: LayerPathsProxy(self).setter(value))
'''
	.. attribute:: paths
	List of :class:`GSPath` objects.
	:type: list

	.. code-block:: python

		# access all paths
		for path in layer.paths:
			print(path)

		# delete path
		del(layer.paths[0])

		# copy paths from another layer
		import copy
		layer.paths = copy.copy(anotherlayer.paths)
'''

GSLayer.selection = property(lambda self: LayerSelectionProxy(self), lambda self, value: LayerSelectionProxy(self).setter(value))

'''
	.. attribute:: selection
	List of all selected objects in the glyph. Read-only.

	This list contains **all selected items**, including **nodes**, **anchors**, **guidelines** etc.
	If you want to work specifically with nodes, for instance, you may want to cycle through the nodes (or anchors etc.) and check whether they are selected. See example below.

	.. code-block:: python

		# access all selected nodes
		for path in layer.paths:
			for node in path.nodes: # (or path.anchors etc.)
				print(node.selected)

		# clear selection
		layer.clearSelection()

	:type: list
'''

GSLayer.LSB = property(lambda self: self.pyobjc_instanceMethods.LSB(),
						lambda self, value: self.setLSB_(float(value)))
'''
	.. attribute:: LSB
	Left sidebearing
	:type: float
'''

GSLayer.RSB = property(lambda self: self.pyobjc_instanceMethods.RSB(),
						lambda self, value: self.setRSB_(float(value)))
'''
	.. attribute:: RSB
	Right sidebearing
	:type: float
'''

GSLayer.TSB = property(lambda self: self.pyobjc_instanceMethods.TSB(),
						lambda self, value: self.setTSB_(float(value)))
'''
	.. attribute:: TSB
	Top sidebearing
	:type: float
'''

GSLayer.BSB = property(lambda self: self.pyobjc_instanceMethods.BSB(),
						lambda self, value: self.setBSB_(float(value)))
'''
	.. attribute:: BSB
	Bottom sidebearing
	:type: float
'''

GSLayer.width = property(lambda self: self.pyobjc_instanceMethods.width(),
						lambda self, value: self.setWidth_(float(value)))
						
GSBackgroundLayer.width = property(lambda self: self.pyobjc_instanceMethods.width(),
									lambda self, value: None)
'''
	.. attribute:: width
	Layer width
	:type: float
'''

def __GSLayer_vertWidth__(self):
	value = self.pyobjc_instanceMethods.vertWidth()
	if value >= 0 and value < 1000000:
		return value
	return None
		
def __GSLayer_setVertWidth__(self, value):
	if value is None or value > 1000000 or value < 0:
		value = NSNotFound
	else:
		value = float(value)
	self.setVertWidth_(value)
	
GSLayer.vertWidth = property(lambda self: __GSLayer_vertWidth__(self),
						lambda self, value: __GSLayer_setVertWidth__(self, value))
'''
	.. attribute:: vertWidth
	Layer vertical width
	
	set it to None to reset it to default
	:type: float

	.. versionadded:: 2.6.2
'''

def __GSLayer_vertOrigin__(self):
	value = self.pyobjc_instanceMethods.vertOrigin()
	if value > -1000000 and value < 1000000:
		return value
	return None

def __GSLayer_setVertOrigin__(self, value):
	if value is None or value > 1000000 or value < -1000000:
		value = NSNotFound
	else:
		value = float(value)
	self.setVertOrigin_(value)

GSLayer.vertOrigin = property(lambda self: __GSLayer_vertOrigin__(self),
						lambda self, value: __GSLayer_setVertOrigin__(self, value))
'''
	.. attribute:: vertOrigin
	Layer vertical origin

	set it to None to reset it to default

	:type: float

	.. versionadded:: 2.6.2
'''

GSLayer.leftMetricsKey = property(lambda self: self.pyobjc_instanceMethods.leftMetricsKey(),
									lambda self, value: self.setLeftMetricsKey_(NSStr(value)))
'''
	.. attribute:: leftMetricsKey
	The leftMetricsKey of the layer. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.
	:type: unicode'''
GSLayer.rightMetricsKey = property(lambda self: self.pyobjc_instanceMethods.rightMetricsKey(),
									lambda self, value: self.setRightMetricsKey_(NSStr(value)))
'''
	.. attribute:: rightMetricsKey
	The rightMetricsKey of the layer. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.
	:type: unicode'''
GSLayer.widthMetricsKey = property(lambda self: self.pyobjc_instanceMethods.widthMetricsKey(),
									lambda self, value: self.setWidthMetricsKey_(NSStr(value)))
'''
	.. attribute:: widthMetricsKey
	The widthMetricsKey of the layer. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.
	:type: unicode
'''

GSLayer.bounds = property(lambda self: self.pyobjc_instanceMethods.bounds())
'''
	.. attribute:: bounds
	Bounding box of whole glyph as NSRect. Read-only.
	:type: NSRect

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		# origin
		print(layer.bounds.origin.x, layer.bounds.origin.y)

		# size
		print(layer.bounds.size.width, layer.bounds.size.height)
'''

GSLayer.selectionBounds = property(lambda self: self.boundsOfSelection())
'''
	.. attribute:: selectionBounds
	Bounding box of the layer's selection (nodes, anchors, components etc). Read-only.
	:type: NSRect
'''

GSLayer.background = property(lambda self: self.pyobjc_instanceMethods.background(),
								lambda self, value: self.setBackground_(value))
'''
	.. attribute:: background
	The background layer
	:type: :class:`GSLayer`
'''

GSLayer.backgroundImage = property(lambda self: self.pyobjc_instanceMethods.backgroundImage(),
									lambda self, value: self.setBackgroundImage_(value))
'''
	.. attribute:: backgroundImage
	The background image. It will be scaled so that 1 em unit equals 1 of the image's pixels.
	:type: :class:`GSBackgroundImage`

	.. code-block:: python

		# set background image
		layer.backgroundImage = GSBackgroundImage('/path/to/file.jpg')

		# remove background image
		layer.backgroundImage = None
'''

GSLayer.bezierPath = property(lambda self: self.pyobjc_instanceMethods.bezierPath())
'''
	.. attribute:: bezierPath

	.. versionadded:: 2.3

	The layer as an NSBezierPath object. Useful for drawing glyphs in plug-ins.

	.. code-block:: python

		# draw the path into the Edit view
		NSColor.redColor().set()
		layer.bezierPath.fill()

	:type: NSBezierPath
'''

GSLayer.openBezierPath = property(lambda self: self.pyobjc_instanceMethods.openBezierPath())
'''
	.. attribute:: openBezierPath

	.. versionadded:: 2.3

	All open paths of the layer as an NSBezierPath object. Useful for drawing glyphs as outlines in plug-ins.

	.. code-block:: python

		# draw the path into the Edit view
		NSColor.redColor().set()
		layer.openBezierPath.stroke()

	:type: NSBezierPath
'''

# keep for compatibility:
def Layer__drawBezierPath(self):
	print("layer.drawBezierPath is deprecated. Please use layer.completeBezierPath")
	return self.pyobjc_instanceMethods.drawBezierPath()
GSLayer.drawBezierPath = property(lambda self: Layer__drawBezierPath(self))

GSLayer.completeBezierPath = property(lambda self: self.pyobjc_instanceMethods.drawBezierPath())
'''
	.. attribute:: completeBezierPath

	.. versionadded:: 2.3.1

	The layer as an NSBezierPath object including paths from components. Useful for drawing glyphs in plug-ins.

	.. code-block:: python

		# draw the path into the Edit view
		NSColor.redColor().set()
		layer.completeBezierPath.fill()

	:type: NSBezierPath
'''

# keep for compatibility:
def Layer__drawOpenBezierPath(self):
	print("layer.drawBezierPath is deprecated. Please use layer.completeBezierPath")
	return self.pyobjc_instanceMethods.drawOpenBezierPath()
GSLayer.drawOpenBezierPath = property(lambda self: Layer__drawOpenBezierPath(self))
GSLayer.completeOpenBezierPath = property(lambda self: self.pyobjc_instanceMethods.drawOpenBezierPath())
'''
	.. attribute:: completeOpenBezierPath

	.. versionadded:: 2.3.1

	All open paths of the layer as an NSBezierPath object including paths from components. Useful for drawing glyphs as outlines in plugins.

	.. code-block:: python

		# draw the path into the Edit view
		NSColor.redColor().set()
		layer.completeOpenBezierPath.stroke()

	:type: NSBezierPath
'''


GSLayer.isAligned = property(lambda self: self.pyobjc_instanceMethods.isAligned())
'''
	.. attribute:: isAligned

	.. versionadded:: 2.3.1

	Indicates if the components are auto aligned.

	:type: bool
'''

GSLayer.isSpecialLayer = property(lambda self: bool(self.pyobjc_instanceMethods.isSpecialLayer()))
'''
	.. attribute:: isSpecialLayer

	If the layer is a brace, bracket or a smart component layer

	:type: bool
'''

GSLayer.isMasterLayer = property(lambda self: bool(self.pyobjc_instanceMethods.isMasterLayer()))
'''
	.. attribute:: isMasterLayer
	
	If it is a master layer
	
	:type: bool
'''


GSLayer.userData = property(lambda self: UserDataProxy(self))
'''
	.. attribute:: userData

	.. versionadded:: 2.3

	A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the data will not be recoverable from the saved file.
	:type: dict
	.. code-block:: python
		# set value
		layer.userData['rememberToMakeCoffee'] = True

		# delete value
		del layer.userData['rememberToMakeCoffee']
'''

GSLayer.smartComponentPoleMapping = property(lambda self: SmartComponentPoleMappingProxy(self))

'''
	.. attribute:: smartComponentPoleMapping

	.. versionadded:: 2.3

	Maps this layer to the poles on the interpolation axes of the Smart Glyph. The dictionary keys are the names of the :class:`GSSmartComponentAxis` objects. The values are 1 for bottom pole and 2 for top pole. Corresponds to the 'Layers' tab of the glyph's 'Show Smart Glyph Settings' dialog.

	Also see https://glyphsapp.com/tutorials/smart-components for reference.

	:type: dict, int

	.. code-block:: python

		# Map layers to top and bottom poles:

		crotchDepthAxis = glyph.smartComponentAxes['crotchDepth']
		shoulderWidthAxis = glyph.smartComponentAxes['shoulderWidth']

		for layer in glyph.layers:

			# Regular layer
			if layer.name == 'Regular':
				layer.smartComponentPoleMapping[crotchDepthAxis.id] = 2
				layer.smartComponentPoleMapping[shoulderWidthAxis.id] = 2

			# NarrowShoulder layer
			elif layer.name == 'NarrowShoulder':
				layer.smartComponentPoleMapping[crotchDepthAxis.id] = 2
				layer.smartComponentPoleMapping[shoulderWidthAxis.id] = 1

			# LowCrotch layer
			elif layer.name == 'LowCrotch':
				layer.smartComponentPoleMapping[crotchDepthAxis.id] = 1
				layer.smartComponentPoleMapping[shoulderWidthAxis.id] = 2


	**Functions**


	.. function:: decomposeComponents()

		Decomposes all components of the layer at once.

	.. function:: decomposeCorners()

		.. versionadded:: 2.4

		Decomposes all corners of the layer at once.

	.. function:: compareString()

		Returns a string representing the outline structure of the glyph, for compatibility comparison.

		:return: The comparison string

		:rtype: string

		.. code-block:: python

			layer = Glyphs.font.selectedLayers[0] # current layer

			print(layer.compareString())
			oocoocoocoocooc_oocoocoocloocoocoocoocoocoocoocoocooc_

	.. function:: connectAllOpenPaths()

		Closes all open paths when end points are further than 1 unit away from each other.


	.. function:: copyDecomposedLayer()

		Returns a copy of the layer with all components decomposed.

		:return: A new layer object

		:rtype: :class:`GSLayer`

	.. function:: syncMetrics()

		Take over LSB and RSB from linked glyph.

		.. code-block:: python

			# sync metrics of all layers of this glyph
			for layer in glyph.layers:
				layer.syncMetrics()

	.. function:: correctPathDirection()

		Corrects the path direction.
'''

def RemoveOverlap(self, checkSelection=False):
	removeOverlapFilter = NSClassFromString("GlyphsFilterRemoveOverlap").alloc().init()
	removeOverlapFilter.removeOverlapFromLayer_checkSelection_error_(self, checkSelection, None)
GSLayer.removeOverlap = RemoveOverlap

'''
	.. function:: removeOverlap()

		Joins all contours.

		:param checkSelection: if the selection will be considered. Default: False

	.. function:: roundCoordinates()

		.. versionadded:: 2.3

		Round the positions of all coordinates to the grid (size of which is set in the Font Info).
'''

def Layer_addNodesAtExtremes(self, force=False):
	self.addExtremePoints()

GSLayer.addNodesAtExtremes = Layer_addNodesAtExtremes

'''
	.. function:: addNodesAtExtremes()

		.. versionadded:: 2.3

		Add nodes at layer's extrema, e.g., top, bottom etc.
'''

def __GSLayer_applyTransform__(self, transformStruct):
	Transform = NSAffineTransform.transform()
	Transform.setTransformStruct_(transformStruct)
	self.transform_checkForSelection_doComponents_(Transform, False, True)

GSLayer.applyTransform = __GSLayer_applyTransform__

'''
	.. function:: applyTransform

	Apply a transformation matrix to the layer.

	.. code-block:: python

		layer = Glyphs.font.selectedLayers[0] # current layer

		layer.applyTransform([
					0.5, # x scale factor
					0.0, # x skew factor
					0.0, # y skew factor
					0.5, # y scale factor
					0.0, # x position
					0.0  # y position
					])
'''



def BeginChanges(self):
	self.setDisableUpdates()
	self.undoManager().beginUndoGrouping()
GSLayer.beginChanges = BeginChanges


'''
	.. function:: beginChanges()

		Call this before you do bigger changes to the Layer.
		This will increase performance and prevent undo problems.
		Always call layer.endChanges() if you are finished.
'''

def EndChanges(self):
	self.setEnableUpdates()
	self.undoManager().endUndoGrouping()
GSLayer.endChanges = EndChanges


'''
	.. function:: endChanges()

		Call this if you have called layer.beginChanges before. Make sure to group bot calls properly.
'''

def CutBetweenPoints(self, Point1, Point2):
	GlyphsToolOther = NSClassFromString("GlyphsToolOther")
	GlyphsToolOther.cutPathsInLayer_forPoint_endPoint_(self, Point1, Point2)
GSLayer.cutBetweenPoints = CutBetweenPoints


'''
	.. function:: cutBetweenPoints(Point1, Point2)

		Cuts all paths that intersect the line from Point1 to Point2

		:param Point1: one point
		:param Point2: the other point

		.. code-block:: python

			layer = Glyphs.font.selectedLayers[0] # current layer

			# cut glyph in half horizontally at y=100
			layer.cutBetweenPoints(NSPoint(0, 100), NSPoint(layer.width, 100))
'''

def IntersectionsBetweenPoints(self, Point1, Point2, components=False):
	return self.calculateIntersectionsStartPoint_endPoint_decompose_(Point1, Point2, components)
GSLayer.intersectionsBetweenPoints = IntersectionsBetweenPoints

NSConcreteValue.x = property(lambda self: self.pointValue().x)
NSConcreteValue.y = property(lambda self: self.pointValue().y)

'''
	.. function:: intersectionsBetweenPoints(Point1, Point2, components = False)

		Return all intersection points between a measurement line and the paths in the layer. This is basically identical to the measurement tool in the UI.

		Normally, the first returned point is the starting point, the last returned point is the end point. Thus, the second point is the first intersection, the second last point is the last intersection.


		:param Point1: one point
		:param Point2: the other point
		:param components: if components should be measured. Default: False

		.. code-block:: python

			layer = Glyphs.font.selectedLayers[0] # current layer

			# show all intersections with glyph at y=100
			intersections = layer.intersectionsBetweenPoints((-1000, 100), (layer.width+1000, 100))
			print(intersections)

			# left sidebearing at measurement line
			print(intersections[1].x)

			# right sidebearing at measurement line
			print(layer.width - intersections[-2].x)
'''

def Layer_addMissingAnchors(self):
	GSGlyphsInfo.sharedManager().updateAnchor_(self)
GSLayer.addMissingAnchors = Layer_addMissingAnchors


'''
	.. function:: addMissingAnchors()

		Adds missing anchors defined in the glyph database.
'''


'''
	.. function:: clearSelection()

		.. versionadded:: 2.3

		Unselect all selected items in this layer.
'''

'''
	.. function:: clear()

		.. versionadded:: 2.3

		Remove all elements from layer.
'''

'''
	.. function:: swapForegroundWithBackground()

		.. versionadded:: 2.3

		Swap Foreground layer with Background layer.
'''

def Layer_replaceLayerWithInterpolation(self):

	if self.parent:
		self.parent.replaceLayerWithInterpolation_(self)


GSLayer.reinterpolate = Layer_replaceLayerWithInterpolation

'''
	.. function:: reinterpolate()

		.. versionadded:: 2.3

		Re-interpolate a layer according the other layers and its interpolation values.

		Applies to both master layers as well as brace layers and is equivalent to the 'Re-Interpolate' command from the Layers palette.

'''






def ControlLayer__new__(typ, *args, **kwargs):
	if len(args) > 0:
		return GSControlLayer.alloc().initWithChar_(args[0])
	else:
		return GSControlLayer.alloc().init()
GSControlLayer.__new__ = staticmethod(ControlLayer__new__)

def ControlLayer__init__(self, args):
	pass
GSControlLayer.__init__ = ControlLayer__init__

def ControlLayer__repr__(self):
	char = self.parent.unicodeChar()
	if char == 10:
		name = "newline"
	elif char == 129:
		name = "placeholder"
	else:
		name = GSGlyphsInfo.sharedManager().niceGlyphNameForName_("uni%.4X" % self.parent.unicodeChar())
	return "<%s \"%s\">" % (self.className(), name)
GSControlLayer.__repr__ = python_method(ControlLayer__repr__)

def ControlLayer__newline__():
	return GSControlLayer(10)
GSControlLayer.newline = staticmethod(ControlLayer__newline__)

def ControlLayer__placeholder__():
	return GSControlLayer(129)
GSControlLayer.placeholder = staticmethod(ControlLayer__placeholder__)



def DrawLayerWithPen(self, pen, contours=True, components=True):
	"""draw the object with a RoboFab segment pen"""
	try:
		pen.setWidth(self.width)
		if self.note is not None:
			pen.setNote(self.note)
	except AttributeError:
		# FontTools pens don't have these methods
		pass
	if contours:
		for a in self.anchors:
			a.draw(pen)
		for c in self.paths:
			c.draw(pen)
	if components:
		for c in self.components:
			c.draw(pen)
	try:
		pen.doneDrawing()
	except AttributeError:
		# FontTools pens don't have a doneDrawing() method
		pass

GSLayer.draw = DrawLayerWithPen

def DrawPointsWithPen(self, pen, contours=True, components=True):
	"""draw the object with a point pen"""
	if contours:
		for p in self.paths:
			p.drawPoints(pen)
	if components:
		for c in self.components:
			c.drawPoints(pen)

GSLayer.drawPoints = DrawPointsWithPen


def _getPen_(self):
	return GSPathPen.alloc().initWithLayer_(self)

GSLayer.getPen = _getPen_
GSLayer.getPointPen = _getPen_

def _invalidateContours_(self):
	pass

GSLayer._invalidateContours = _invalidateContours_







##################################################################################
#
#
#
#           GSAnchor
#
#
#
##################################################################################

def ___________________(): pass
def ____GSAnchor____(): pass
def ___________________(): pass

'''

:mod:`GSAnchor`
===============================================================================

Implementation of the anchor object.

For details on how to access them, please see :attr:`GSLayer.anchors`

.. class:: GSAnchor([name, pt])

	:param name: the name of the anchor
	:param pt: the position of the anchor

	Properties

	.. autosummary::

		position
		name
		selected

	**Properties**

'''



def Anchor__init__(self, name=None, pt=None):
	if pt:
		self.setPosition_(pt)
	if name:
		self.setName_(name)
GSAnchor.__init__ = Anchor__init__

def Anchor__repr__(self):
	return "<GSAnchor \"%s\" x=%s y=%s>" % (self.name, self.position.x, self.position.y)
GSAnchor.__repr__ = python_method(Anchor__repr__)

GSAnchor.mutableCopyWithZone_ = GSObject__copy__

GSAnchor.position = property(lambda self: self.pyobjc_instanceMethods.position(),
							lambda self, value: self.setPosition_(value))
'''
	.. attribute:: position
	The position of the anchor
	:type: NSPoint

	.. code-block:: python

		# read position
		print(layer.anchors['top'].position.x, layer.anchors['top'].position.y)

		# set position
		layer.anchors['top'].position = NSPoint(175, 575)

		# increase vertical position by 50 units
		layer.anchors['top'].position = NSPoint(layer.anchors['top'].position.x, layer.anchors['top'].position.y + 50)
'''

GSAnchor.name = property(lambda self: self.pyobjc_instanceMethods.name(),
						lambda self, value: self.setName_(value))
'''
	.. attribute:: name
	The name of the anchor
	:type: unicode

	.. attribute:: selected
	Selection state of anchor in UI.

	.. code-block:: python

		# select anchor
		layer.anchors[0].selected = True

		# log selection state
		print(layer.anchors[0].selected)

	:type: bool
'''

def DrawAnchorWithPen(self, pen):
	if hasattr(pen, "addAnchor"):
		pen.addAnchor(self.name, (self.x, self.y))
	else:
		pen.moveTo(self.position)
		pen.endPath()

GSAnchor.draw = DrawAnchorWithPen

def __GSAnchor_drawPoints__(self, pen):
	"""draw the object with a point pen"""
	pen.beginPath()
	pen.addPoint((self.x, self.y), segmentType="move", smooth=False, name=self.name)
	pen.endPath()
GSAnchor.drawPoints = __GSAnchor_drawPoints__


##################################################################################
#
#
#
#           GSComponent
#
#
#
##################################################################################

def _______________________(): pass
def ____GSComponent____(): pass
def _______________________(): pass



'''

:mod:`GSComponent`
===============================================================================

Implementation of the component object.
For details on how to access them, please see :attr:`GSLayer.components`

.. class:: GSComponent(glyph [, position])

	:param glyph: a :class:`GSGlyph` object or the glyph name
	:param position: the position of the component as NSPoint

	Properties

	.. autosummary::

		position
		scale
		rotation
		componentName
		component
		layer
		transform
		bounds
		automaticAlignment
		anchor
		selected
		smartComponentValues
		bezierPath
		userData

	Functions

	.. autosummary::

		decompose()
		applyTransform()

	**Properties**

'''


def Component__init__(self, glyph, offset=(0, 0), scale=(1, 1), transform=None):
	"""
	transformation: transform matrix as list of numbers
	"""
	if transform is None:
		if scale != (1, 1):
			xx, yy = scale
			dx, dy = offset
			self.transform = ((xx, 0, 0, yy, dx, dy))
		elif offset != (0, 0):
			self.setPositionFast_(offset)
	else:
		self.transform = transform

	if glyph:
		if isinstance(glyph, (str, unicode)):
			self.setComponentName_(glyph)
		elif isinstance(glyph, GSGlyph):
			self.setComponentName_(glyph.name)
		elif isinstance(glyph, "RGlyph"):
			self.setComponentName_(glyph.name)

GSComponent.__init__ = Component__init__

def Component__repr__(self):
	return "<GSComponent \"%s\" x=%s y=%s>" % (self.componentName, self.position.x, self.position.y)
GSComponent.__repr__ = python_method(Component__repr__)

GSComponent.mutableCopyWithZone_ = GSObject__copy__

GSComponent.position = property(lambda self: self.pyobjc_instanceMethods.position(),
								lambda self, value: self.setPosition_(value))
'''
	.. attribute:: position
	The Position of the component.
	:type: NSPoint
'''

def GSComponent_getScale(self):
	(x, y, r) = self.getScaleX_scaleY_rotation_(None, None, None)
	return (x, y)

def GSComponent_setScale(self, scale):
	(x, y, r) = self.getScaleX_scaleY_rotation_(None, None, None)
	if type(scale) == tuple:
		self.setScaleX_scaleY_rotation_(scale[0], scale[1], r)
	elif type(scale) == int or type(scale) == float:
		self.setScaleX_scaleY_rotation_(scale, scale, r)

GSComponent.scale = property(lambda self: GSComponent_getScale(self),
							lambda self, value: GSComponent_setScale(self, value))

'''
	.. attribute:: scale

	Scale factor of image.

	A scale factor of 1.0 (100%) means that 1 em unit equals 1 of the image's pixels.

	This sets the scale factor for x and y scale simultaneously. For separate scale factors, please use the transformation matrix.

	:type: float or tuple
'''

def GSComponent_getRotation(self):
	(x, y, rotation) = self.getScaleX_scaleY_rotation_(None, None, None)
	return rotation

def GSComponent_setRotation(self, rotation):
	(x, y, r) = self.getScaleX_scaleY_rotation_(None, None, None)
	self.setScaleX_scaleY_rotation_(x, y, rotation)

GSComponent.rotation = property(lambda self: GSComponent_getRotation(self),
								lambda self, value: GSComponent_setRotation(self, value))

'''
	.. attribute:: rotation
	Rotation angle of component.
	:type: float
'''

GSComponent.componentName = property(lambda self: self.pyobjc_instanceMethods.componentName(),
									lambda self, value: self.setComponentName_(objcObject(value)))
'''
	.. attribute:: componentName
	The glyph name the component is pointing to.
	:type: unicode
'''

GSComponent.name = property(lambda self: self.pyobjc_instanceMethods.componentName(),
									lambda self, value: self.setComponentName_(value))
'''
	.. attribute:: name
	The glyph name the component is pointing to.
	:type: unicode

	.. versionadded:: 2.5

'''

GSComponent.component = property(lambda self: self.pyobjc_instanceMethods.component())
'''
	.. attribute:: component
	The :class:`GSGlyph` the component is pointing to. This is read-only. In order to change the referenced base glyph, set :attr:`componentName <GSComponent.componentName>` to the new glyph name.
	:type: :class:`GSGlyph`
'''

GSComponent.componentLayer = property(lambda self: self.pyobjc_instanceMethods.componentLayer())
'''
	.. attribute:: componentLayer

	The :class:`GSLayer` the component is pointing to. This is read-only. In order to change the referenced base glyph, set :attr:`componentName <GSComponent.componentName>` to the new glyph name.

	For Smart Components, the `componentLayer` contains the interpolated result.

	:type: :class:`GSLayer`

	.. versionadded:: 2.5
'''

GSComponent.transform = property(lambda self: self.transformStruct(),
									lambda self, value: self.setTransformStruct_(value))
'''
	.. attribute:: transform

	Transformation matrix of the component.

	.. code-block:: python

		component = layer.components[0]

		component.transform = ((
					0.5, # x scale factor
					0.0, # x skew factor
					0.0, # y skew factor
					0.5, # y scale factor
					0.0, # x position
					0.0  # y position
					))

	:type: NSAffineTransformStruct
'''


GSComponent.bounds = property(lambda self: self.pyobjc_instanceMethods.bounds())
'''
	.. attribute:: bounds
	Bounding box of the component, read-only
	:type: NSRect

	.. code-block:: python

		component = layer.components[0] # first component

		# origin
		print(component.bounds.origin.x, component.bounds.origin.y)

		# size
		print(component.bounds.size.width, component.bounds.size.height)
'''

# keep for compatibility:
GSComponent.disableAlignment = property(lambda self: bool(self.pyobjc_instanceMethods.disableAlignment()),
										lambda self, value: self.setDisableAlignment_(value))
# new:
GSComponent.automaticAlignment = property(lambda self: bool(self.doesAlign() or self.doesAttach()),
											lambda self, value: self.setDisableAlignment_(not bool(value)))
'''
	.. attribute:: automaticAlignment

	Defines whether the component is automatically aligned.

	:type: bool'''
GSComponent.alignment = property(lambda self: self.pyobjc_instanceMethods.alignment(),
								lambda self, value: self.setAlignment_(value))

'''
	.. attribute:: alignment

	.. versionadded:: 2.5

	TODO
'''

GSComponent.locked = property(lambda self: bool(self.pyobjc_instanceMethods.locked()),
								lambda self, value: self.setLocked_(value))
'''
	.. attribute:: locked

	.. versionadded:: 2.5

	If the component is locked
	TODO

	:type: bool
'''

GSComponent.anchor = property(lambda self: self.pyobjc_instanceMethods.anchor(),
								lambda self, value: self.setAnchor_(value))
'''
	.. attribute:: anchor

	If more than one anchor/_anchor pair would match, this property can be used to set the anchor to use for automatic alignment

	This can be set from the anchor button in the component info box in the UI

	:type: unicode'''



'''
	.. attribute:: selected
	Selection state of component in UI.

	.. code-block:: python

		# select component
		layer.components[0].selected = True

		# print(selection state)
		print(layer.components[0].selected)

	:type: bool
'''

def DrawComponentWithPen(self, pen):
	pen.addComponent(self.componentName, self.transform)

GSComponent.draw = DrawComponentWithPen
GSComponent.drawPoints = DrawComponentWithPen

GSComponent.smartComponentValues = property(lambda self: smartComponentValuesProxy(self))
'''
	.. attribute:: smartComponentValues

	.. versionadded:: 2.3

	Dictionary of interpolations values of the Smart Component. Key are the names, values are between the top and the bottom value of the corresponding :class:`GSSmartComponentAxis` objects. Corresponds to the values of the 'Smart Component Settings' dialog. Returns None if the component is not a Smart Component.

	Also see https://glyphsapp.com/tutorials/smart-components for reference.

	:type: dict, int

	.. code-block:: python

		# Narrow shoulders of m
		glyph = font.glyphs['m']
		glyph.layers[0].components[1].smartComponentValues['shoulderWidth'] = 30 # First shoulder. Index is 1, given that the stem is also a component with index 0
		glyph.layers[0].components[2].smartComponentValues['shoulderWidth'] = 30 # Second shoulder. Index is 2, given that the stem is also a component with index 0

		# Low crotch of h
		glyph = font.glyphs['h']
		crotchDepthAxis = glyph.smartComponentAxes['crotchDepth']
		glyph.layers[0].components[1].smartComponentValues[crotchDepthAxis.id] = -77  # Shoulder. Index is 1, given that the stem is also a component with index 0

		# Check whether a component is a smart component
		for component in layer.components:
			if component.smartComponentValues is not None:
				# do stuff
'''

GSComponent.bezierPath = property(lambda self: self.pyobjc_instanceMethods.bezierPath())
'''
	.. attribute:: bezierPath

	.. versionadded:: 2.3

	The component as an NSBezierPath object. Useful for drawing glyphs in plugins.

	.. code-block:: python

		# draw the path into the Edit view
		NSColor.redColor().set()
		layer.components[0].bezierPath.fill()

	:type: NSBezierPath
'''

GSComponent.userData = property(lambda self: UserDataProxy(self))

'''
	.. attribute:: userData

	.. versionadded:: 2.5

	A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the data will not be recoverable from the saved file.
	:type: dict
	.. code-block:: python
		# set value
		component.userData['rememberToMakeCoffee'] = True

		# delete value
		del component.userData['rememberToMakeCoffee']
'''


'''


	**Functions**


'''

GSComponent.parent = property(lambda self: self.pyobjc_instanceMethods.parent(),
								lambda self, value: self.setParent_(value))

def __GSComponent_decompose__(self, doAnchors=True, doHints=True):
	self.parent.decomposeComponent_doAnchors_doHints_(self, doAnchors, doHints)
GSComponent.decompose = __GSComponent_decompose__

'''
	.. function:: decompose(doAnchors = True, doHints = True)

	:param doAnchors: get anchors from components
	:param doHints: get hints from components

	Decomposes the component.
'''

def __GSComponent_applyTransform__(self, transformStruct):
	transform = self.transform
	oldTransform = NSAffineTransform.transform()
	oldTransform.setTransformStruct_(transform)
	newTransform = NSAffineTransform.transform()
	newTransform.setTransformStruct_(transformStruct)
	oldTransform.appendTransform_(newTransform)
	self.setTransformStruct_(oldTransform.transformStruct())

GSComponent.applyTransform = __GSComponent_applyTransform__

'''
	.. function:: applyTransform

	Apply a transformation matrix to the component.

	.. code-block:: python

		component = layer.components[0]

		component.applyTransform((
					0.5, # x scale factor
					0.0, # x skew factor
					0.0, # y skew factor
					0.5, # y scale factor
					0.0, # x position
					0.0  # y position
					))
'''



##################################################################################
#
#
#
#           GSSmartComponentAxis
#
#
#
##################################################################################

def __________________________________(): pass
def ____GSSmartComponentAxis____(): pass
def __________________________________(): pass


'''

:mod:`GSSmartComponentAxis`
===============================================================================

Implementation of the Smart Component interpolation axis object.
For details on how to access them, please see :attr:`GSGlyph.smartComponentAxes`

.. versionadded:: 2.3

.. class:: GSSmartComponentAxis()

	Properties

	.. autosummary::

		name
		topValue
		bottomValue

	**Properties**

'''

GSSmartComponentAxis = GSPartProperty

GSSmartComponentAxis.__new__ = staticmethod(GSObject__new__)
def SmartComponentProperty__init__(self):
	pass
GSSmartComponentAxis.__init__ = SmartComponentProperty__init__
def SmartComponentProperty__repr__(self):
	return "<GSSmartComponentAxis \"%s\">" % (self.name)
GSSmartComponentAxis.__repr__ = python_method(SmartComponentProperty__repr__)

GSSmartComponentAxis.name = property(lambda self: self.pyobjc_instanceMethods.name(),
								lambda self, value: self.setName_(value))
'''
	.. attribute:: name
	Name of the axis. The name is for display purpose only.
	:type: str
'''
GSSmartComponentAxis.id = property(lambda self: self.pyobjc_instanceMethods.id())
'''
	.. attribute:: id
	Id of the axis. This Id will be used to map the Smart Glyph's layers to the poles of the interpolation. See :attr:`GSLayer.smartComponentPoleMapping`
	:type: str

	.. versionadded:: 2.5
'''

GSSmartComponentAxis.topValue = property(lambda self: self.pyobjc_instanceMethods.topValue(),
								lambda self, value: self.setTopValue_(value))
'''
	.. attribute:: topValue
	Top end (pole) value on interpolation axis.
	:type: int, float
'''

GSSmartComponentAxis.bottomValue = property(lambda self: self.pyobjc_instanceMethods.bottomValue(),
								lambda self, value: self.setBottomValue_(value))
'''
	.. attribute:: bottomValue
	Bottom end (pole) value on interpolation axis.
	:type: int, float
'''





##################################################################################
#
#
#
#           GSPath
#
#
#
##################################################################################


def ________________(): pass
def ____GSPath____(): pass
def ________________(): pass


'''

:mod:`GSPath`
===============================================================================

Implementation of the path object.

For details on how to access them, please see :attr:`GSLayer.paths`

If you build a path in code, make sure that the structure is valid. A curve node has to be preceded by two off-curve nodes. And an open path has to start with a line node.

.. class:: GSPath()

	Properties

	.. autosummary::

		parent
		nodes
		segments
		closed
		direction
		bounds
		selected
		bezierPath

	Functions

	.. autosummary::

		reverse()
		addNodesAtExtremes()
		applyTransform()

	**Properties**


'''


GSPath.__new__ = staticmethod(GSObject__new__)

def Path__init__(self):
	pass
GSPath.__init__ = Path__init__

def Path__repr__(self):
	return "<GSPath %s nodes and %s segments>" % (len(self.nodes), len(self.segments))
GSPath.__repr__ = python_method(Path__repr__)

GSPath.mutableCopyWithZone_ = GSObject__copy__

GSPath.parent = property(lambda self: self.pyobjc_instanceMethods.parent(),
						lambda self, value: self.setParent_(value))
'''
	.. attribute:: parent
	Reference to the :class:`layer <GSLayer>` object.
	:type: :class:`GSLayer`
'''

GSPath.nodes = property(lambda self: PathNodesProxy(self),
						lambda self, value: PathNodesProxy(self).setter(value))
'''
	.. attribute:: nodes
	A list of :class:`GSNode` objects
	:type: list

	.. code-block:: python

		# access all nodes
		for path in layer.paths:
			for node in path.nodes:
				print(node)
'''

GSPath.segments = property(lambda self: self.pyobjc_instanceMethods.segments(),
							lambda self, value: self.setSegments_(value))
'''
	.. attribute:: segments
	A list of segments as NSPoint objects. Two objects represent a line, four represent a curve. Start point of the segment is included.
	:type: list

	.. code-block:: python

		# access all segments
		for path in layer.paths:
			for segment in path.segments:
				print(segment)
'''

GSPath.closed = property(lambda self: bool(self.pyobjc_instanceMethods.closed()),
						lambda self, value: self.setClosed_(value))
'''
	.. attribute:: closed
	Returns True if the the path is closed
	:type: bool
'''

GSPath.direction = property(lambda self: self.pyobjc_instanceMethods.direction())
'''
	.. attribute:: direction
	Path direction. -1 for counter clockwise, 1 for clockwise.
	:type: int
'''

GSPath.bounds = property(lambda self: self.pyobjc_instanceMethods.bounds())
'''
	.. attribute:: bounds
	Bounding box of the path, read-only
	:type: NSRect

	.. code-block:: python

		path = layer.paths[0] # first path

		# origin
		print(path.bounds.origin.x, path.bounds.origin.y)

		# size
		print(path.bounds.size.width, path.bounds.size.height)
'''

def Path_selected(self):
	return set(self.nodes) <= set(self.parent.selection)

def Path_SetSelected(self, state):
	layer = self.parent
	if state:
		layer.addObjectsFromArrayToSelection_(self.pyobjc_instanceMethods.nodes())
	else:
		layer.removeObjectsFromSelection_(self.pyobjc_instanceMethods.nodes())

GSPath.selected = property(lambda self: Path_selected(self), lambda self, value: Path_SetSelected(self, value))
'''
	.. attribute:: selected
	Selection state of path in UI.

	.. code-block:: python

		# select path
		layer.paths[0].selected = True

		# print(selection state)
		print(layer.paths[0].selected)

	:type: bool
'''


GSPath.bezierPath = property(lambda self: self.pyobjc_instanceMethods.bezierPath())
'''
	.. attribute:: bezierPath

	.. versionadded:: 2.3

	The same path as an NSBezierPath object. Useful for drawing glyphs in plugins.

	.. code-block:: python

		# draw the path into the Edit view
		NSColor.redColor().set()
		layer.paths[0].bezierPath.fill()

	:type: NSBezierPath

	**Functions**

	.. function:: reverse()

		Reverses the path direction

'''

def DrawPathWithPen(self, pen):
	"""draw the object with a fontTools pen"""

	Start = 0
	if self.closed:
		for i in range(len(self) - 1, -1, -1):
			StartNode = self.nodeAtIndex_(i)
			GS_Type = StartNode.pyobjc_instanceMethods.type()
			if GS_Type is not GSOFFCURVE_:
				pen.moveTo(StartNode.pyobjc_instanceMethods.position())
				break
	else:
		for i in range(len(self)):
			StartNode = self.nodeAtIndex_(i)
			GS_Type = StartNode.pyobjc_instanceMethods.type()
			if GS_Type is not GSOFFCURVE_:
				pen.moveTo(StartNode.pyobjc_instanceMethods.position())
				Start = i + 1
				break
	for i in range(Start, len(self), 1):
		Node = self.nodeAtIndex_(i)
		GS_Type = Node.pyobjc_instanceMethods.type()
		if GS_Type == GSLINE_:
			pen.lineTo(Node.pyobjc_instanceMethods.position())
		elif GS_Type == GSCURVE_:
			pen.curveTo(self.nodeAtIndex_(i - 2).pyobjc_instanceMethods.position(), self.nodeAtIndex_(i - 1).pyobjc_instanceMethods.position(), Node.pyobjc_instanceMethods.position())
	if self.closed:
		pen.closePath()
	else:
		pen.endPath()
	return

GSPath.draw = DrawPathWithPen


def __GSPath__drawPoints__(self, pen):
	'''draw the object with a fontTools pen'''

	pen.beginPath()
	for i in range(len(self)):
		Node = self.nodeAtIndex_(i)
		node_type = Node.type
		if Node.type == GSOFFCURVE:
			node_type = None
		pen.addPoint(Node.position, segmentType=node_type, smooth=Node.smooth, name=Node.name)
	pen.endPath()

GSPath.drawPoints = __GSPath__drawPoints__


def Path_addNodesAtExtremes(self, force=False):
	self.addExtremes_(force)

GSPath.addNodesAtExtremes = Path_addNodesAtExtremes
'''
	.. function:: addNodesAtExtremes()

	Add nodes at path's extrema, e.g., top, bottom etc.
	
	.. versionadded:: 2.3
'''


def __CGPath_applyTransform__(self, transformStruct):
	Transform = NSAffineTransform.transform()
	Transform.setTransformStruct_(transformStruct)
	for node in self.nodes:
		node.position = Transform.transformPoint_(node.positionPrecise())

GSPath.applyTransform = __CGPath_applyTransform__

'''
	.. function:: applyTransform

	Apply a transformation matrix to the path.

	.. code-block:: python

		path = layer.paths[0]

		path.applyTransform((
					0.5, # x scale factor
					0.0, # x skew factor
					0.0, # y skew factor
					0.5, # y scale factor
					0.0, # x position
					0.0  # y position
					))
'''


##################################################################################
#
#
#
#           GSNode
#
#
#
##################################################################################

def ________________(): pass
def ____GSNode____(): pass
def ________________(): pass

'''

:mod:`GSNode`
===============================================================================

Implementation of the node object.

For details on how to access them, please see :attr:`GSPath.nodes`

.. class:: GSNode([pt, type = type])

	:param pt: The position of the node.
	:param type: The type of the node, LINE, CURVE or OFFCURVE

	Properties

	.. autosummary::

		position
		type
		connection
		selected
		index
		nextNode
		prevNode
		name

	Functions

	.. autosummary::

		makeNodeFirst()
		toggleConnection()


	**Properties**

'''



def Node__init__(self, pt=None, type=None, x=None, y=None, name=None, pointType=None):
	if type is None and pointType is not None:
		type = pointType
	if pt:
		self.setPosition_(pt)
	elif x is not None and y is not None:
		self.setPosition_((x, y))
	if type:
		self.type = type
	if name:
		self.name = name
GSNode.__init__ = Node__init__

def Node__repr__(self):
	NodeType = self.type
	if self.type != OFFCURVE and self.smooth:
		NodeType += " smooth"
	return "<GSNode x=%s y=%s %s>" % (self.position.x, self.position.y, NodeType)
GSNode.__repr__ = python_method(Node__repr__)

GSNode.mutableCopyWithZone_ = GSObject__copy__

GSNode.position = property(lambda self: self.pyobjc_instanceMethods.position(),
							lambda self, value: self.setPosition_(value))
'''
	.. attribute:: position
	The position of the node.
	:type: NSPoint
'''

def __GSNode_get_type__(self):
	GS_Type = self.pyobjc_instanceMethods.type()
	if GS_Type == GSMOVE_:
		return MOVE
	elif GS_Type == GSOFFCURVE_:
		return OFFCURVE
	elif GS_Type == GSCURVE_:
		return CURVE
	elif GS_Type == GSQCURVE_:
		return QCURVE
	else:
		return LINE

def __GSNode_set_type__(self, value):
	if value == MOVE:
		self.setType_(GSLINE_)
	elif value == LINE:
		self.setType_(GSLINE_)
	elif value == OFFCURVE:
		self.setType_(GSOFFCURVE_)
	elif value == CURVE:
		self.setType_(GSCURVE_)
	elif value == QCURVE:
		self.setType_(GSQCURVE_)

GSNode.type = property(__GSNode_get_type__, __GSNode_set_type__, doc="")
'''
	.. attribute:: type
	The type of the node, LINE, CURVE or OFFCURVE

	Always compare against the constants, never against the actual value.
	:type: str
'''

def __GSNode__get_smooth(self):
	return self.connection == GSSMOOTH

def __GSNode__set_smooth(self, value):
	if value is True:
		self.setConnection_(GSSMOOTH)
	else:
		self.setConnection_(GSSHARP)

GSNode.smooth = property(__GSNode__get_smooth, __GSNode__set_smooth, doc="")
'''
	.. attribute:: smooth
	If it is a smooth connection or not
	:type: BOOL

	.. versionadded:: 2.3
'''

def __GSNode_get_connection(self):
	GS_Type = self.pyobjc_instanceMethods.connection()
	if GS_Type == GSSHARP:
		return GSSHARP
	else:
		return GSSMOOTH

def __GSNode_set_connection(self, value):
	if value == GSSHARP:
		self.setConnection_(GSSHARP)
	else:
		self.setConnection_(GSSMOOTH)

GSNode.connection = property(__GSNode_get_connection, __GSNode_set_connection, doc="")
'''
	.. attribute:: connection
	The type of the connection, SHARP or SMOOTH
	:type: string

	.. deprecated:: 2.3
		Use :attr:`smooth <GSNode.smooth>` instead.
'''

GSNode.parent = property(lambda self: self.pyobjc_instanceMethods.parent())

GSNode.layer = property(lambda self: self.pyobjc_instanceMethods.layer())

'''
	.. attribute:: selected
	Selection state of node in UI.

	.. code-block:: python

		# select node
		layer.paths[0].nodes[0].selected = True

		# print(selection state)
		print(layer.paths[0].nodes[0].selected)

	:type: bool
'''

def __GSNode__index__(self):
	try:
		return self.parent.indexOfNode_(self)
	except:
		return NSNotFound

GSNode.index = property(lambda self: __GSNode__index__(self))
'''
	.. attribute:: index

	Returns the index of the node in the containing path or maxint if it is not in a path.
	:type: int
	
	.. versionadded:: 2.3
'''

def __GSNode__nextNode__(self):
	try:
		index = self.parent.indexOfNode_(self)
		if index == (len(self.parent.nodes) - 1):
			return self.parent.nodes[0]
		elif index < len(self.parent.nodes):
			return self.parent.nodes[index + 1]
	except:
		pass
	return None

GSNode.nextNode = property(lambda self: __GSNode__nextNode__(self))
'''
	.. attribute:: nextNode
	
	Returns the next node in the path.

	Please note that this is regardless of the position of the node in the path and will jump across the path border to the beginning of the path if the current node is the last.

	If you need to take into consideration the position of the node in the path, use the node’s index attribute and check it against the path length.

	.. code-block:: python

		print(layer.paths[0].nodes[0].nextNode # returns the second node in the path (index 0 + 1))
		print(layer.paths[0].nodes[-1].nextNode # returns the first node in the path (last node >> jumps to beginning of path))

		# check if node is last node in path (with at least two nodes)
		print(layer.paths[0].nodes[0].index == (len(layer.paths[0].nodes) - 1)) # returns False for first node
		print(layer.paths[0].nodes[-1].index == (len(layer.paths[0].nodes) - 1)) # returns True for last node

	:type: GSNode
	
	.. versionadded:: 2.3
'''

def __GSNode__prevNode__(self):
	try:
		index = self.parent.indexOfNode_(self)
		if index == 0:
			return self.parent.nodes[-1]
		elif index < len(self.parent.nodes):
			return self.parent.nodes[index - 1]
	except:
		pass
	return None

GSNode.prevNode = property(lambda self: __GSNode__prevNode__(self))
'''
	.. attribute:: prevNode

	Returns the previous node in the path.

	Please note that this is regardless of the position of the node in the path, and will jump across the path border to the end of the path if the current node is the first.

	If you need to take into consideration the position of the node in the path, use the node’s index attribute and check it against the path length.

	.. code-block:: python

		print(layer.paths[0].nodes[0].prevNode) # returns the last node in the path (first node >> jumps to end of path)
		print(layer.paths[0].nodes[-1].prevNode) # returns second last node in the path

		# check if node is first node in path (with at least two nodes)
		print(layer.paths[0].nodes[0].index == 0) # returns True for first node
		print(layer.paths[0].nodes[-1].index == 0) # returns False for last node

	:type: GSNode
	
	.. versionadded:: 2.3
'''


def __GSNode__get_name(self):
	try:
		return self.userDataForKey_("name")
	except:
		pass
	return None

def __GSNode__set_name(self, value):
	if value is None or isString(value):
		self.setUserData_forKey_(value, "name")
	else:
		raise(ValueError)

GSNode.name = property(__GSNode__get_name, __GSNode__set_name, doc="")
'''
	.. attribute:: name

	Attaches a name to a node.
	:type: unicode

	.. versionadded:: 2.3
'''

GSNode.userData = property(lambda self: UserDataProxy(self))
'''
	.. attribute:: userData

	A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the data will not be recoverable from the saved file.
	:type: dict
	.. code-block:: python
		# set value
		node.userData['rememberToMakeCoffee'] = True

		# delete value
		del node.userData['rememberToMakeCoffee']

	.. versionadded:: 2.4.1

	**Functions**

	.. function:: makeNodeFirst()

		Turn this node into the start point of the path.

	.. function:: toggleConnection()

		Toggle between sharp and smooth connections.
'''








##################################################################################
#
#
#
#           GSGuideLine
#
#
#
##################################################################################

def ______________________(): pass
def ____GSGuideline____(): pass
def ______________________(): pass


'''

:mod:`GSGuideLine`
===============================================================================

Implementation of the guide object.

For details on how to access them, please see :attr:`GSLayer.guides`


.. class:: GSGuideLine()

	**Properties**

	.. autosummary::

		position
		angle
		name
		selected
		locked
'''



def GuideLine__init__(self):
	pass
GSGuideLine.__init__ = GuideLine__init__

def GuideLine__repr__(self):
	return "<GSGuideLine x=%s y=%s angle=%s>" % (self.position.x, self.position.y, self.angle)
GSGuideLine.__repr__ = python_method(GuideLine__repr__)

GSGuideLine.mutableCopyWithZone_ = GSObject__copy__

GSGuideLine.position = property(lambda self: self.pyobjc_instanceMethods.position(),
								lambda self, value: self.setPosition_(value))
'''
	.. attribute:: position
	The position of the node.
	:type: NSPoint
'''

GSGuideLine.angle = property(lambda self: self.pyobjc_instanceMethods.angle(),
							lambda self, value: self.setAngle_(float(value)))
'''
	.. attribute:: angle
	Angle
	:type: float
'''

GSGuideLine.name = property(lambda self: self.pyobjc_instanceMethods.name(),
							lambda self, value: self.setName_(value))
'''
	.. attribute:: name
	a optional name
	:type: unicode

	.. attribute:: selected
	Selection state of guideline in UI.

	.. code-block:: python

		# select guideline
		layer.guidelines[0].selected = True

		# print(selection state)
		print(layer.guidelines[0].selected)

	:type: bool
'''

GSGuideLine.locked = property(lambda self: bool(self.pyobjc_instanceMethods.locked()),
							lambda self, value: self.setLocked_(value))
'''
	.. attribute:: locked
	Locked
	:type: bool
'''

##################################################################################
#
#
#
#           GSAnnotation
#
#
#
##################################################################################

def _______________________(): pass
def ____GSAnnotation____(): pass
def _______________________(): pass

'''

:mod:`GSAnnotation`
===============================================================================

Implementation of the annotation object.

For details on how to access them, please see :class:`GSLayer.annotations`

.. class:: GSAnnotation()

	.. autosummary::

		position
		type
		text
		angle
		width

	**Properties**

'''

GSAnnotation.__new__ = staticmethod(GSObject__new__)

def Annotation__init__(self):
	pass
GSAnnotation.__init__ = Annotation__init__

def Annotation__repr__(self):
	TypeName = "n/a"
	if (self.type == TEXT):
		TypeName = "Text"
	elif (self.type == ARROW):
		TypeName = "Arrow"
	elif (self.type == CIRCLE):
		TypeName = "Circle"
	elif (self.type == PLUS):
		TypeName = "Plus"
	elif (self.type == MINUS):
		TypeName = "Minus"
	return "<%s %s x=%s y=%s>" % (self.className(), TypeName, self.position.x, self.position.y)
GSAnnotation.__repr__ = python_method(Annotation__repr__)

GSAnnotation.mutableCopyWithZone_ = GSObject__copy__


GSAnnotation.position = property(lambda self: self.pyobjc_instanceMethods.position(),
								lambda self, value: self.setPosition_(value))
'''
	.. attribute:: position
	The position of the annotation.
	:type: NSPoint
'''

GSAnnotation.type = property(lambda self: self.pyobjc_instanceMethods.type(),
							lambda self, value: self.setType_(value))
'''
	.. attribute:: type
	The type of the annotation.

	Available constants are:
	:const:`TEXT`
	:const:`ARROW`
	:const:`CIRCLE`
	:const:`PLUS`
	:const:`MINUS`

	:type: int
'''

GSAnnotation.text = property(lambda self: self.pyobjc_instanceMethods.text(),
							lambda self, value: self.setText_(value))
'''
	.. attribute:: text
	The content of the annotation. Only useful if type == TEXT
	:type: unicode
'''

GSAnnotation.angle = property(lambda self: self.pyobjc_instanceMethods.angle(),
							lambda self, value: self.setAngle_(value))
'''
	.. attribute:: angle
	The angle of the annotation.
	:type: float
'''

GSAnnotation.width = property(lambda self: self.pyobjc_instanceMethods.width(),
							lambda self, value: self.setWidth_(value))
'''
	.. attribute:: width
	The width of the annotation.
	:type: float
'''



##################################################################################
#
#
#
#           GSHint
#
#
#
##################################################################################

def ________________(): pass
def ____GSHint____(): pass
def ________________(): pass

'''

:mod:`GSHint`
===============================================================================

Implementation of the hint object.

For details on how to access them, please see :class:`GSLayer.hints`

.. class:: GSHint()

	.. autosummary::

		parent
		originNode
		targetNode
		otherNode1
		otherNode2
		type
		horizontal
		selected

	**Properties**

	'''

GSHint.__new__ = staticmethod(GSObject__new__)

def Hint__init__(self):
	pass
GSHint.__init__ = Hint__init__

def Hint__origin__pos(self):
	if (self.originNode):
		if self.horizontal:
			return self.originNode.position.y
		else:
			return self.originNode.position.x
	return self.pyobjc_instanceMethods.origin()

def Hint__width__pos(self):
	if (self.targetNode):
		if self.horizontal:
			return self.targetNode.position.y
		else:
			return self.targetNode.position.x
	width = self.pyobjc_instanceMethods.width()
	if width > 100000:
		width = 0
	return width

def Hint__repr__(self):
	if self.isTrueType():
		return self.description()
	if self.horizontal:
		direction = "hori"
	else:
		direction = "vert"
	if self.type == BOTTOMGHOST or self.type == TOPGHOST:
		return "<GSHint %s origin=(%s)>" % (hintConstants[self.type], self.position)
	elif self.type == STEM:
		return "<GSHint %s Stem origin=(%s) target=(%s)>" % (direction, self.position, self.width)
	elif self.type == CORNER or self.type == CAP:
		return "<GSHint %s %s>" % (hintConstants[self.type], self.name)
	else:
		return "<GSHint %s %s>" % (hintConstants[self.type], direction)
GSHint.__repr__ = python_method(Hint__repr__)

GSHint.mutableCopyWithZone_ = GSObject__copy__

GSHint.parent = property(lambda self: self.pyobjc_instanceMethods.parent())

'''
	.. attribute:: parent

	Parent layer of hint.

	:type: GSLayer

	.. versionadded:: 2.4.2

'''


GSHint.scale = property(lambda self: self.pyobjc_instanceMethods.scale(),
						lambda self, value: self.setScale_(value))

GSHint.originNode = property(lambda self: self.pyobjc_instanceMethods.originNode(),
							lambda self, value: self.setOriginNode_(value))
'''
	.. attribute:: originNode
	The first node the hint is attached to.

	:type: :class:`GSNode`
'''
GSHint.position = property(lambda self: Hint__origin__pos(self),
							lambda self, value: self.setOrigin_(value))
GSHint.width = property(lambda self: Hint__width__pos(self),
						lambda self, value: self.setOrigin_(value))

def __indexPathToIndexes__(indexPath):
	if indexPath is not None:
		indexes = []
		for idx in range(len(indexPath)):
			indexes.append(indexPath.indexAtPosition_(idx))
		return indexes
	return None

GSHint.origin = property(lambda self: __indexPathToIndexes__(self.originIndex()))
GSHint.target = property(lambda self: __indexPathToIndexes__(self.targetIndex()))
GSHint.other1 = property(lambda self: __indexPathToIndexes__(self.otherIndex1()))
GSHint.other2 = property(lambda self: __indexPathToIndexes__(self.otherIndex2()))

GSHint.targetNode = property(lambda self: self.pyobjc_instanceMethods.targetNode(),
							lambda self, value: self.setTargetNode_(value))
'''
	.. attribute:: targetNode
	The the second node this hint is attached to. In the case of a ghost hint, this value will be empty.

	:type: :class:`GSNode`
'''

GSHint.otherNode1 = property(lambda self: self.valueForKey_("otherNode1"),
							lambda self, value: self.setOtherNode1_(value))
'''
	.. attribute:: otherNode1
	A third node this hint is attached to. Used for Interpolation or Diagonal hints.

	:type: :class:`GSNode`'''

GSHint.otherNode2 = property(lambda self: self.valueForKey_("otherNode2"),
							lambda self, value: self.setOtherNode2_(value))
'''
	.. attribute:: otherNode2
	A fourth node this hint is attached to. Used for Diagonal hints.

	:type: :class:`GSNode`'''

GSHint.type = property(lambda self: self.pyobjc_instanceMethods.type(),
						lambda self, value: self.setType_(value))
'''
	.. attribute:: type
	See Constants section at the bottom of the page.
	:type: int'''

GSHint.options = property(lambda self: self.pyobjc_instanceMethods.options(),
							lambda self, value: self.setOptions_(value))
'''
	.. attribute:: options
	Stores extra options for the hint. For TT hints, that might be the rounding settings.
	See Constants section at the bottom of the page.
	:type: int'''

GSHint.horizontal = property(lambda self: self.pyobjc_instanceMethods.horizontal(),
							lambda self, value: self.setHorizontal_(value))
'''
	.. attribute:: horizontal
	True if hint is horizontal, False if vertical.
	:type: bool'''

'''
	.. attribute:: selected
	Selection state of hint in UI.

	.. code-block:: python

		# select hint
		layer.hints[0].selected = True

		# print(selection state)
		print(layer.hints[0].selected)

	:type: bool
'''

GSHint.name = property(lambda self: self.pyobjc_instanceMethods.name(), lambda self, value: self.setName_(objcObject(value)))
'''
	.. attribute:: name

	.. versionadded:: 2.3.1

	Name of the hint. This is the referenced glyph for corner and cap components.
	:type: string'''


def GSHint__stem__(self):
	value = self.pyobjc_instanceMethods.stem()
	stems = self.parent.master.customParameters['TTFStems']
	if stems and -1 <= value <= (len(stems) - 1):
		return value
	else:
		return -2

def GSHint__setStem__(self, value):
	stems = self.parent.master.customParameters['TTFStems']
	if not stems:
		raise ValueError('The master of this layer has no defined "TTFStems" custom parameter')
	if stems and -1 <= value <= (len(stems) - 1):
		self.pyobjc_instanceMethods.setStem_(value)
	elif value == -2:
		self.pyobjc_instanceMethods.setStem_(sys.maxint)
	else:
		raise ValueError('Wrong value. Stem values can be indices of TT stems ("TTFStems" master custom parameter) or -1 for no stem or -2 for automatic.')


GSHint.stem = property(lambda self: GSHint__stem__(self),
						lambda self, value: GSHint__setStem__(self, value))
'''
	.. attribute:: stem

	.. versionadded:: 2.4.2

	Index of TrueType stem that this hint is attached to. The stems are defined in the custom parameter "TTFStems" per master.

	For no stem, value is -1.

	For automatic, value is -2.

	:type: integer'''


##################################################################################
#
#
#
#           GSBackgroundImage
#
#
#
##################################################################################

def ______________________________(): pass
def ____GSBackgroundImage____(): pass
def ______________________________(): pass


'''

:mod:`GSBackgroundImage`
===============================================================================

Implementation of background image.

For details on how to access it, please see :class:`GSLayer.backgroundImage`

.. class:: GSBackgroundImage([path])

	:param path: Initialize with an image file (optional)

	Properties

	.. autosummary::

		path
		image
		crop
		locked
		position
		scale
		rotation
		transform
		alpha

	Functions

	.. autosummary::

		resetCrop()
		scaleWidthToEmUnits()
		scaleHeightToEmUnits()

	**Properties**

'''

def BackgroundImage__init__(self, path=None):
	if path:
		self.setImagePath_(path)
		self.loadImage()
GSBackgroundImage.__init__ = BackgroundImage__init__

def BackgroundImage__repr__(self):
	return "<GSBackgroundImage '%s'>" % self.imagePath()
GSBackgroundImage.__repr__ = python_method(BackgroundImage__repr__)

GSBackgroundImage.mutableCopyWithZone_ = GSObject__copy__

def BackgroundImage_setPath(self, path):
	self.setImagePath_(path)
	self.loadImage()

GSBackgroundImage.path = property(lambda self: self.pyobjc_instanceMethods.imagePath(),
						lambda self, value: BackgroundImage_setPath(self, value))
'''
	.. attribute:: path
	Path to image file.
	:type: unicode
'''

GSBackgroundImage.image = property(lambda self: self.pyobjc_instanceMethods.image())
'''
	.. attribute:: image

	:class:`NSImage` object of background image, read-only (as in: not settable)

	:type: :class:`NSImage`
'''

GSBackgroundImage.crop = property(lambda self: self.pyobjc_instanceMethods.crop(),
									lambda self, value: self.setCrop_(value))
'''
	.. attribute:: crop

	Crop rectangle. This is relative to the image size in pixels, not the font's em units (just in case the image is scaled to something other than 100%).

	:type: :class:`NSRect`

	.. code-block:: python

		# change cropping
		layer.backgroundImage.crop = NSRect(NSPoint(0, 0), NSPoint(1200, 1200))

'''

GSBackgroundImage.locked = property(lambda self: bool(self.pyobjc_instanceMethods.locked()),
									lambda self, value: self.setLocked_(value))
'''
	.. attribute:: locked
	Defines whether image is locked for access in UI.
	:type: bool
'''

GSBackgroundImage.alpha = property(lambda self: self.pyobjc_instanceMethods.alpha(),
									lambda self, value: self.setAlpha_(value))
'''
	.. attribute:: alpha

	Defines the transparence of the image in the Edit view. Default is 50%, possible values are 10–100.

	To reset it to default, set it to anything other than the allowed values.

	:type: int

	.. versionadded:: 2.3

'''

def BackgroundImage_getPosition(self):
	return NSPoint(self.transform[4], self.transform[5])

def BackgroundImage_setPosition(self, pos):
	self.transform = ((self.transform[0], self.transform[1], self.transform[2], self.transform[3], pos.x, pos.y))

GSBackgroundImage.position = property(lambda self: BackgroundImage_getPosition(self),
										lambda self, value: BackgroundImage_setPosition(self, value))

'''
	.. attribute:: position

	Position of image in font units.

	:type: :class:`NSPoint`

	.. code-block:: python

		# change position
		layer.backgroundImage.position = NSPoint(50, 50)

'''

def BackgroundImage_getScale(self):
	(x, y, r) = self.getScaleX_scaleY_rotation_(None, None, None)
	return (x, y)

def BackgroundImage_setScale(self, scale):
	(x, y, r) = self.getScaleX_scaleY_rotation_(None, None, None)
	if type(scale) == tuple:
		self.setScaleX_scaleY_rotation_(scale[0], scale[1], r)
	elif type(scale) == int or type(scale) == float:
		self.setScaleX_scaleY_rotation_(scale, scale, r)

GSBackgroundImage.scale = property(lambda self: BackgroundImage_getScale(self),
										lambda self, value: BackgroundImage_setScale(self, value))

'''
	.. attribute:: scale

	Scale factor of image.

	A scale factor of 1.0 (100%) means that 1 font unit is equal to 1 point.

	Set the scale factor for x and y scale simultaneously with an integer or a float value. For separate scale factors, please use a tuple.

	.. code-block:: python

		# change scale
		layer.backgroundImage.scale = 1.2 # changes x and y to 120%
		layer.backgroundImage.scale = (1.1, 1.2) # changes x to 110% and y to 120%

	:type: tuple
'''

def BackgroundImage_getRotation(self):
	(x, y, rotation) = self.getScaleX_scaleY_rotation_(None, None, None)
	return rotation

def BackgroundImage_setRotation(self, rotation):
	(x, y, r) = self.getScaleX_scaleY_rotation_(None, None, None)
	self.setScaleX_scaleY_rotation_(x, y, rotation)

GSBackgroundImage.rotation = property(lambda self: BackgroundImage_getRotation(self),
										lambda self, value: BackgroundImage_setRotation(self, value))

'''
	.. attribute:: rotation

	Rotation angle of image.

	:type: float
'''

GSBackgroundImage.transform = property(lambda self: self.pyobjc_instanceMethods.transformStruct(),
										lambda self, value: self.setTransformStruct_(value))
'''
	.. attribute:: transform

	Transformation matrix.

	:type: :class:`NSAffineTransformStruct`

	.. code-block:: python

		# change transformation
		layer.backgroundImage.transform = ((
			1.0, # x scale factor
			0.0, # x skew factor
			0.0, # y skew factor
			1.0, # y scale factor
			0.0, # x position
			0.0  # y position
			))

	**Functions**

'''

def BackgroundImage_resetCrop(self):
	self.crop = NSRect(NSPoint(0, 0), self.image.size())
GSBackgroundImage.resetCrop = BackgroundImage_resetCrop
'''
	.. function:: resetCrop

	Resets the cropping to the image's original dimensions.
'''

def BackgroundImage_scaleWidthToEmUnits(self, value):
	self.scale = float(value) / float(self.crop.size.width)
GSBackgroundImage.scaleWidthToEmUnits = BackgroundImage_scaleWidthToEmUnits
'''
	.. function:: scaleWidthToEmUnits

	Scale the image's cropped width to a certain em unit value, retaining its aspect ratio.

	.. code-block:: python

		# fit image in layer's width
		layer.backgroundImage.scaleWidthToEmUnits(layer.width)

'''

def BackgroundImage_scaleHeightToEmUnits(self, value):
	self.scale = float(value) / float(self.crop.size.height)
GSBackgroundImage.scaleHeightToEmUnits = BackgroundImage_scaleHeightToEmUnits

'''
	.. function:: scaleHeightToEmUnits

	Scale the image's cropped height to a certain em unit value, retaining its aspect ratio.

	.. code-block:: python

		# position image's origin at descender line
		layer.backgroundImage.position = NSPoint(0, font.masters[0].descender)

		# scale image to UPM value
		layer.backgroundImage.scaleHeightToEmUnits(font.upm)
'''



##################################################################################
#
#
#
#           GSEditViewController
#
#
#
##################################################################################

def _______________________________(): pass
def ____GSEditViewController____(): pass
def _______________________________(): pass

'''

:mod:`GSEditViewController`
===============================================================================

Implementation of the GSEditViewController object, which represents Edit tabs in the UI.

For details on how to access them, please look at :class:`GSFont.tabs`


.. class:: GSEditViewController()

	Properties

	.. autosummary::

		parent
		text
		layers
		composedLayers
		scale
		viewPort
		bounds
		selectedLayerOrigin
		textCursor
		textRange
		direction
		features
		previewInstances
		previewHeight
		bottomToolbarHeight
		masterIndex

	Functions

	.. autosummary::

		close()
		saveToPDF()


	**Properties**

'''


GSEditViewController.parent = property(lambda self: self.representedObject())
'''
	.. attribute:: parent
	The :class:`GSFont` object that this tab belongs to.
	:type: :class:`GSFont`
'''

GSEditViewController.text = property(lambda self: self.graphicView().displayStringSave_(False),
									lambda self, value: self.graphicView().setDisplayString_(value))
'''
	.. attribute:: text
	The text of the tab, either as text, or slash-escaped glyph names, or mixed. OpenType features will be applied after the text has been changed.
	:type: Unicode
'''

def __GSEditViewController__repr__(self):
	nameString = self.text
	if len(nameString) > 30:
		nameString = nameString[:30] + '...'
	nameString = nameString.replace('\n', '\\n')
	import codecs
	return codecs.encode("<GSEditViewController %s>" % nameString, 'ascii', 'backslashreplace')

GSEditViewController.__repr__ = python_method(__GSEditViewController__repr__)

GSEditViewController.masterIndex = property(lambda self: self.pyobjc_instanceMethods.masterIndex(), lambda self, value: self.setMasterIndex_(value))
'''
	.. attribute:: masterIndex
	The index of the active master (selected in the toolbar).
	:type: int
	
	.. versionadded:: 2.6.1
	
'''


class TabLayersProxy (Proxy):

	def __getitem__(self, idx):
		if type(idx) == slice:
			return self.values().__getitem__(idx)
		else:
			return self.values()[idx]

	def deactivateFeatures(self):
		self.savedFeatures = copy.copy(self._owner.features)
		self._owner.features = []

	def activateFeatures(self):
		self._owner.features = self.savedFeatures

	def setter(self, layers):

		self.deactivateFeatures()

		if not (type(layers) is list or type(layers) is tuple or "objectAtIndex_" in layers.__class__.__dict__ or type(layers) is type(self)):
			raise ValueError
		if type(layers) is type(self):
			layers = layers.values()

		string = NSMutableAttributedString.alloc().init()
		Font = self._owner.representedObject()
		for l in layers:
			if l.className() == "GSLayer":
				char = Font.characterForGlyph_(l.parent)
				A = NSAttributedString.alloc().initWithString_attributes_(NSString.stringWithChar_(char), {"GSLayerIdAttrib": l.layerId})
			elif l.className() == "GSBackgroundLayer":
				char = Font.characterForGlyph_(l.parent)
				A = NSAttributedString.alloc().initWithString_attributes_(NSString.stringWithChar_(char), {"GSLayerIdAttrib": l.layerId, "GSShowBackgroundAttrib": True})
			elif l.className() == "GSControlLayer":
				char = l.parent.unicodeChar()
				A = NSAttributedString.alloc().initWithString_(NSString.stringWithChar_(char))
			else:
				raise ValueError
			string.appendAttributedString_(A)
		self._owner.graphicView().textStorage().setText_(string)
		self.activateFeatures()

	def composedLayers(self):
		return list(self._owner.graphicView().layoutManager().cachedGlyphs())

	def values(self):
		self.deactivateFeatures()
		layers = list(self._owner.graphicView().layoutManager().cachedGlyphs())
		self.activateFeatures()
		return layers

	def append(self, value):
		values = copy.copy(self.values())
		values.append(value)
		self.setter(values)

	def remove(self, value):
		values = self.values()
		values.remove(value)
		self.setter(values)


GSEditViewController.layers = property(lambda self: TabLayersProxy(self), lambda self, value: TabLayersProxy(self).setter(value))

'''
	.. attribute:: layers

	Alternatively, you can set (and read) a list of :class:`GSLayer` objects. These can be any of the layers of a glyph. OpenType features will be applied after the layers have been changed.

	:type: list

	.. code-block:: python


		font.tabs[0].layers = []

		# display all layers of one glyph next to each other
		for layer in font.glyphs['a'].layers:
			font.tabs[0].layers.append(layer)

		# append line break
		font.tabs[0].layers.append(GSControlLayer(10)) # 10 being the ASCII code of the new line character (\n)

'''

GSEditViewController.composedLayers = property(lambda self: TabLayersProxy(self).composedLayers())


'''
	.. attribute:: composedLayers

	Similar to the above, but this list contains the :class:`GSLayer` objects after the OpenType features have been applied (see :class:`GSEditViewController.features`). Read-only.

	:type: list

	.. versionadded:: 2.4
'''



GSEditViewController.scale = property(lambda self: self.graphicView().scale(), lambda self, value: self.graphicView().setScale_(value))

'''
	.. attribute:: scale

	Scale (zoom factor) of the Edit view. Useful for drawing activity in plugins.

	The scale changes with every zoom step of the Edit view. So if you want to draw objects (e.g. text, stroke thickness etc.) into the Edit view at a constant size relative to the UI (e.g. constant text size on screen), you need to calculate the object's size relative to the scale factor. See example below.

	.. code-block:: python

		print(font.currentTab.scale)
		0.414628537193

		# Calculate text size
		desiredTextSizeOnScreen = 10 #pt
		scaleCorrectedTextSize = desiredTextSizeOnScreen / font.currentTab.scale

		print(scaleCorrectedTextSize)
		24.1179733255


	:type: float

	.. versionadded:: 2.3
'''

GSEditViewController.viewPort = property(lambda self: self.frameView().visibleRect(), lambda self, value: self.frameView().zoomViewToRect_(value))


'''

	.. attribute:: viewPort

	The visible area of the Edit view in screen pixel coordinates (view coordinates).

	The NSRect’s origin value describes the top-left corner (top-right for RTL, both at ascender height) of the combined glyphs’ bounding box (see :attr:`bounds <GSEditViewController.bounds>`), which also serves as the origin of the view plane.

	The NSRect’s size value describes the width and height of the visible area.

	When using drawing methods such as the view-coordinate-relative method in the Reporter Plugin, use these coordinates.

	.. code-block:: python

		# The far corners of the Edit view:

		# Lower left corner of the screen
		x = font.currentTab.viewPort.origin.x
		y = font.currentTab.viewPort.origin.y

		# Top left corner of the screen
		x = font.currentTab.viewPort.origin.x
		y = font.currentTab.viewPort.origin.y + font.currentTab.viewPort.size.height

		# Top right corner of the screen
		x = font.currentTab.viewPort.origin.x + font.currentTab.viewPort.size.width
		y = font.currentTab.viewPort.origin.y + font.currentTab.viewPort.size.height

		# Bottom right corner of the screen
		x = font.currentTab.viewPort.origin.x + font.currentTab.viewPort.size.width
		y = font.currentTab.viewPort.origin.y

	:type: NSRect

	.. versionadded:: 2.3
'''

GSEditViewController.bounds = property(lambda self: self.frameView().glyphFrame())
'''
	.. attribute:: bounds
	Bounding box of all glyphs in the Edit view in view coordinate values.
	:type: NSRect

	.. versionadded:: 2.3
'''

GSEditViewController.selectedLayerOrigin = property(lambda self: self.graphicView().activePosition())

'''
	.. attribute:: selectedLayerOrigin
	Position of the active layer’s origin (0,0) relative to the origin of the view plane (see :attr:`bounds <GSEditViewController.bounds>`), in view coordinates.
	:type: NSPoint

	.. versionadded:: 2.3
'''

GSEditViewController.textCursor = property(lambda self: self.graphicView().selectedRange().location,
											lambda self, value: self.graphicView().setSelectedRange_(NSRange(value, self.graphicView().selectedRange().length)))
'''
	.. attribute:: textCursor
	Position of text cursor in text, starting with 0.
	:type: integer

	.. versionadded:: 2.3
'''

GSEditViewController.textRange = property(lambda self: self.contentView().selectedRange().length,
											lambda self, value: self.contentView().setSelectedRange_(NSRange(self.textCursor, value)))
'''
	.. attribute:: textRange
	Amount of selected glyphs in text, starting at cursor position (see above).
	:type: integer

	.. versionadded:: 2.3
'''

GSEditViewController.layersCursor = property(lambda self: self.graphicView().cachedLayerSelectionRange().location)

'''
	.. attribute:: layersCursor
	Position of cursor in the layers list, starting with 0.
	
	.. seealso:: `GSEditViewController.layers`
	:type: integer

	.. versionadded:: 2.4
'''


GSEditViewController.direction = property(lambda self: self.writingDirection(), lambda self, value: self.setWritingDirection_(value))

'''
	.. attribute:: direction

	Writing direction.

	Defined constants are: LTR (left to right), RTL (right to left), LTRTTB (left to right, vertical, top to bottom e.g. Mongolian), and RTLTTB (right to left, vertical, top to bottom e.g. Chinese, Japanese, Korean)

	:type: integer

	.. code-block:: python

		font.currentTab.direction = RTL

	.. versionadded:: 2.3
'''


class TabSelectedFeaturesProxy (Proxy):

	def reflow(self):
		self._owner.graphicView().reflow()
		self._owner.graphicView().layoutManager().updateActiveLayer()
		self._owner._updateFeaturePopup()


	def setter(self, values):

		if not (type(values) is list or type(values) is tuple or type(values) is type(self)):
			raise TypeError

		self._owner.pyobjc_instanceMethods.selectedFeatures().removeAllObjects()

		if type(values) is type(self):
			otherFeaturesProxy = values
			values = list(otherFeaturesProxy.values())

		for feature in values:
			self.append(feature)

		self.reflow()

	def hasFeature(self, feature):
		_hasFeature = False
		for featureInFont in self._owner.parent.features:
			if featureInFont.name == feature:
				_hasFeature = True

		if not _hasFeature:
			LogError('Info: Feature "%s" not in font.\n' % (feature))
		return _hasFeature

	def append(self, feature):
		if not isString(feature):
			raise TypeError
		if self.hasFeature(feature):
			self._owner.selectedFeatures().append(feature)

		self.reflow()

	def extend(self, features):
		if not isinstance(features, list):
			raise TypeError
		for feature in features:
			if self.hasFeature(feature):
				self._owner.selectedFeatures().append(feature)
		self.reflow()

	def remove(self, feature):
		if not isString(feature):
			raise TypeError
		try:
			self._owner.selectedFeatures().remove(feature)
		except:
			pass

		self.reflow()

	def values(self):
		return self._owner.pyobjc_instanceMethods.selectedFeatures()

GSEditViewController.features = property(lambda self: TabSelectedFeaturesProxy(self), lambda self, value: TabSelectedFeaturesProxy(self).setter(value))

'''
	.. attribute:: features
	List of OpenType features applied to text in Edit view.
	:type: list

	.. code-block:: python

		font.currentTab.features = ['locl', 'ss01']

	.. versionadded:: 2.3
'''

# TODO documentation
class TempDataProxy(Proxy):
	def __getitem__(self, Key):
		return self._owner.tempData().get(Key, None)
	def __setitem__(self, Key, Value):
		if self._owner.tempData() is None:
			self._owner.setTempData_(NSMutableDictionary.alloc().init())
		self._owner.tempData()[Key] = Value
	def __delitem__(self, Key):
		del(self._owner.tempData()[Key])
	def values(self):
		if self._owner.tempData() is not None:
			return self._owner.tempData().allValues()
		return None
	def __repr__(self):
		return str(self._owner.tempData())

GSEditViewController.userData = property(lambda self: TempDataProxy(self))


def Get_ShowInPreview(self):
	value = self.selectedInstance()
	if value == -2:
		value = 'live'
	elif value == -1:
		value = 'all'
	else:
		value = self.parent.instances[value]
	return value

def Set_ShowInPreview(self, value):
	if value == 'live':
		self.setSelectedInstance_(-2)
	elif value == 'all':
		self.setSelectedInstance_(-1)
	else:
		self.setSelectedInstance_(self.parent.instances.index(value))

GSEditViewController.previewInstances = property(lambda self: Get_ShowInPreview(self), lambda self, value: Set_ShowInPreview(self, value))
'''
	.. attribute:: previewInstances

	Instances to show in the Preview area.

	Values are ``'live'`` for the preview of the current content of the Edit view, ``'all'`` for interpolations of all instances of the current glyph, or individual GSInstance objects.

	:type: string/GSInstance

	.. code-block:: python

		# Live preview of Edit view
		font.currentTab.previewInstances = 'live'

		# Text of Edit view shown in particular Instance interpolation (last defined instance)
		font.currentTab.previewInstances = font.instances[-1]

		# All instances of interpolation
		font.currentTab.previewInstances = 'all'

	.. versionadded:: 2.3
'''

GSEditViewController.previewHeight = property(lambda self: self.pyobjc_instanceMethods.previewHeight(), lambda self, value: self.setPreviewHeight_(value))

'''
	.. attribute:: previewHeight

	Height of the preview panel in the Edit view in pixels.

	Needs to be set to 16 or higher for the preview panel to be visible at all. Will return 0 for a closed preview panel or the current size when visible.

	:type: float

	.. versionadded:: 2.3
'''


GSEditViewController.bottomToolbarHeight = property(lambda self: self.previewSplitView().frame().origin.y)

'''
	.. attribute:: bottomToolbarHeight
	Height of the little toolbar at the very bottom of the window. Read-only.
	:type: float

	.. versionadded:: 2.4
'''



'''
	**Functions**

'''

def Close_Tab(self):
	for i, tab in enumerate(self.parent.tabs):
		if tab == self:
			break
	del self.parent.tabs[i]

GSEditViewController.close = Close_Tab

'''
	.. function:: close()

	Close this tab.
'''


def GSEditViewController_saveToPDF(self, path, rect=None):

	if rect is None:
		rect = self.viewPort
	pdf = self.graphicView().dataWithPDFInsideRect_(rect)
	pdf.writeToFile_atomically_(path, True)


GSEditViewController.saveToPDF = GSEditViewController_saveToPDF


'''
	.. function:: saveToPDF(path[, rect])

	Save the view to a PDF file.

	:param path: Path to the file
	:param rect: Optional. NSRect defining the view port. If omitted, :attr:`GSEditViewController.viewPort` will be used.

	.. versionadded:: 2.4
'''



##################################################################################
#
#
#
#           GSGlyphInfo
#
#
#
##################################################################################


def _____________________(): pass
def ____GSGlyphInfo____(): pass
def _____________________(): pass


GSGlyphInfo.__new__ = staticmethod(GSObject__new__)
def GSGlyphInfo__init__(self):
	pass
GSGlyphInfo.__init__ = GSGlyphInfo__init__

def GSGlyphInfo__repr__(self):
	return "<GSGlyphInfo '%s'>" % (self.name)
GSGlyphInfo.__repr__ = python_method(GSGlyphInfo__repr__)


'''

:mod:`GSGlyphInfo`
===============================================================================

Implementation of the GSGlyphInfo object.

This contains valuable information from the glyph database. See :class:`GSGlyphsInfo` for how to create these objects.

.. class:: GSGlyphInfo()

	Properties

	.. autosummary::

		name
		productionName
		category
		subCategory
		components
		accents
		anchors
		unicode
		unicode2
		script
		index
		sortName
		sortNameKeep
		desc
		altNames
		desc

	**Properties**

'''

GSGlyphInfo.name = property(lambda self: self.pyobjc_instanceMethods.name())
'''
	.. attribute:: name
	Human-readable name of glyph ("nice name").
	:type: unicode
'''

GSGlyphInfo.productionName = property(lambda self: self.pyobjc_instanceMethods.production())
'''
	.. attribute:: productionName
	Production name of glyph. Will return a value only if production name differs from nice name, otherwise None.
	:type: unicode
'''

GSGlyphInfo.category = property(lambda self: self.pyobjc_instanceMethods.category())
'''
	.. attribute:: category
	This is mostly from the UnicodeData.txt file from unicode.org. Some corrections have been made (Accents, ...)
	e.g: "Letter", "Number", "Punctuation", "Mark", "Separator", "Symbol", "Other"
	:type: unicode
'''

GSGlyphInfo.subCategory = property(lambda self: self.pyobjc_instanceMethods.subCategory())
'''
	.. attribute:: subCategory
	This is mostly from the UnicodeData.txt file from unicode.org. Some corrections and additions have been made (Smallcaps, ...).
	e.g: "Uppercase", "Lowercase", "Smallcaps", "Ligature", "Decimal Digit", ...
	:type: unicode
'''

GSGlyphInfo.components = property(lambda self: self.pyobjc_instanceMethods.components())
'''
	.. attribute:: components
	This glyph may be composed of the glyphs returned as a list of :class:`GSGlyphInfo` objects.
	:type: list
'''

GSGlyphInfo.accents = property(lambda self: self.pyobjc_instanceMethods.accents())
'''
	.. attribute:: accents
	This glyph may be combined with these accents, returned as a list of glyph names.
	:type: list
'''

GSGlyphInfo.anchors = property(lambda self: self.pyobjc_instanceMethods.anchors())
'''
	.. attribute:: anchors
	Anchors defined for this glyph, as a list of anchor names.
	:type: list
'''

GSGlyphInfo.unicode = property(lambda self: self.pyobjc_instanceMethods.unicode())
'''
	.. attribute:: unicode
	Unicode value
	:type: unicode
'''

GSGlyphInfo.unicode2 = property(lambda self: self.pyobjc_instanceMethods.unicode2())
'''
	.. attribute:: unicode2
	a second unicode value it present
	:type: unicode
'''

GSGlyphInfo.script = property(lambda self: self.pyobjc_instanceMethods.script())
'''
	.. attribute:: script
	Script of glyph, e.g: "latin", "cyrillic", "greek".
	:type: unicode
'''

GSGlyphInfo.index = property(lambda self: self.pyobjc_instanceMethods.index())
'''
	.. attribute:: index
	Index of glyph in database. Used for sorting in UI.
	:type: unicode
'''

GSGlyphInfo.sortName = property(lambda self: self.pyobjc_instanceMethods.sortName())
'''
	.. attribute:: sortName
	Alternative name of glyph used for sorting in UI.
	:type: unicode
'''

GSGlyphInfo.sortNameKeep = property(lambda self: self.pyobjc_instanceMethods.sortNameKeep())
'''
	.. attribute:: sortNameKeep
	Alternative name of glyph used for sorting in UI, when using 'Keep Alternates Next to Base Glyph' from Font Info.
	:type: unicode
'''

GSGlyphInfo.desc = property(lambda self: self.pyobjc_instanceMethods.desc())
'''
	.. attribute:: desc
	Unicode description of glyph.
	:type: unicode
'''

GSGlyphInfo.altNames = property(lambda self: self.pyobjc_instanceMethods.altNames())
'''
	.. attribute:: altNames
	Alternative names for glyphs that are not used, but should be recognized (e.g., for conversion to nice names).
	:type: unicode
'''




def ____________________(): pass
def ____METHODS____(): pass
def ____________________(): pass


def __GSPathPen_beginPath__(self, identifier=None, **kwargs):
	self.beginPath_(identifier)
	path = self.currentPath()
	path.closed = True
GSPathPen.beginPath = __GSPathPen_beginPath__

def __GSPathPen_moveTo__(self, pt):
	self.moveTo_(pt)
GSPathPen.moveTo = __GSPathPen_moveTo__

def __GSPathPen_lineTo__(self, pt):
	self.lineTo_(pt)
GSPathPen.lineTo = __GSPathPen_lineTo__

def __GSPathPen_curveTo__(self, off1, off2, pt):
	self.curveTo_off1_off2_(pt, off1, off2)
GSPathPen.curveTo = __GSPathPen_curveTo__

def __GSPathPen_addPoint__(self, pt, segmentType=None, smooth=False, name=None, identifier=None, **kwargs):
	node = GSNode()
	node.position = pt
	path = self.currentPath()
	if segmentType == "move":
		path.closed = False
	elif segmentType is not None:
		node.type = segmentType
	else:
		node.type = OFFCURVE
	if smooth:
		node.smooth = True
	if name is not None:
		node.name = name
	path.nodes.append(node)
GSPathPen.addPoint = __GSPathPen_addPoint__

def __PathOperator_removeOverlap__(paths):
	try:
		Paths = NSMutableArray.arrayWithArray_(paths)
	except:
		Paths = NSMutableArray.arrayWithArray_(paths.values())

	result = GSPathFinder.alloc().init().removeOverlapPaths_error_(Paths, None)
	if result[0] != 1:
		return None
	return Paths

removeOverlap = __PathOperator_removeOverlap__

def __PathOperator_subtractPaths__(paths, subtract):
	try:
		Paths = NSMutableArray.arrayWithArray_(paths)
	except:
		Paths = NSMutableArray.arrayWithArray_(paths.values())
	try:
		Subtract = NSMutableArray.arrayWithArray_(subtract)
	except:
		Subtract = NSMutableArray.arrayWithArray_(subtract.values())
	result = GSPathFinder.alloc().init().subtractPaths_from_error_(Subtract, Paths, None)
	if result[0] != 1:
		return None
	return Paths

subtractPaths = __PathOperator_subtractPaths__


def __PathOperator_intersectPaths__(paths, otherPaths):
	try:
		Paths = NSMutableArray.arrayWithArray_(paths)
	except:
		Paths = NSMutableArray.arrayWithArray_(paths.values())
	try:
		OtherPaths = NSMutableArray.arrayWithArray_(otherPaths)
	except:
		OtherPaths = NSMutableArray.arrayWithArray_(otherPaths.values())
	result = GSPathFinder.alloc().init().intersectPaths_from_error_(Paths, OtherPaths, None)
	if result[0] != 1:
		return None
	return OtherPaths

intersectPaths = __PathOperator_intersectPaths__


'''

Methods
=======

.. autosummary::

	divideCurve()
	distance()
	addPoints()
	subtractPoints()
	GetOpenFile()
	GetSaveFile()
	GetFolder()
	Message()
	LogToConsole()
	LogError()
'''


def divideCurve(P0, P1, P2, P3, t):
	Q0x = P0[0] + ((P1[0] - P0[0]) * t)
	Q0y = P0[1] + ((P1[1] - P0[1]) * t)
	Q1x = P1[0] + ((P2[0] - P1[0]) * t)
	Q1y = P1[1] + ((P2[1] - P1[1]) * t)
	Q2x = P2[0] + ((P3[0] - P2[0]) * t)
	Q2y = P2[1] + ((P3[1] - P2[1]) * t)
	R0x = Q0x + ((Q1x - Q0x) * t)
	R0y = Q0y + ((Q1y - Q0y) * t)
	R1x = Q1x + ((Q2x - Q1x) * t)
	R1y = Q1y + ((Q2y - Q1y) * t)

	Sx = R0x + ((R1x - R0x) * t)
	Sy = R0y + ((R1y - R0y) * t)
	return (P0, NSMakePoint(Q0x, Q0y), NSMakePoint(R0x, R0y), NSMakePoint(Sx, Sy), NSMakePoint(R1x, R1y), NSMakePoint(Q2x, Q2y), P3)

'''
.. function:: divideCurve(P0, P1, P2, P3, t)

Divides the curve using the De Casteljau's algorithm.

:param P0: The Start point of the Curve (NSPoint)
:param P1: The first off curve point
:param P2: The second off curve point
:param P3: The End point of the Curve
:param t: The time parameter
:return: A list of points that represent two curves. (Q0, Q1, Q2, Q3, R1, R2, R3). Note that the "middle" point is only returned once.
:rtype: list
'''


def distance(P1, P2):
	return math.hypot(P1[0] - P2[0], P1[1] - P2[1])
'''
.. function:: distance(P0, P1)

calculates the distance between two NSPoints

:param P0: a NSPoint
:param P1: another NSPoint
:return: The distance
:rtype: float
'''


def addPoints(P1, P2):
	return NSMakePoint(P1[0] + P2[0], P1[1] + P2[1])
'''
.. function:: addPoints(P1, P2)

Add the points.

:param P0: a NSPoint
:param P1: another NSPoint
:return: The sum of both points
:rtype: NSPoint
'''


def subtractPoints(P1, P2):
	return NSMakePoint(P1[0] - P2[0], P1[1] - P2[1])
'''
.. function:: subtractPoints(P1, P2)

Subtracts the points.

:param P0: a NSPoint
:param P1: another NSPoint
:return: The subtracted point
:rtype: NSPoint
'''

def scalePoint(P, scalar):
	return NSMakePoint(P[0] * scalar, P[1] * scalar)
'''
.. function:: scalePoint(P, scalar)

Scaled a point.

:param P: a NSPoint
:param scalar: The Multiplier
:return: The multiplied point
:rtype: NSPoint
'''

def GetSaveFile(message=None, ProposedFileName=None, filetypes=None):
	Panel = NSSavePanel.savePanel().retain()
	if message is not None:
		Panel.setTitle_(message)
	Panel.setCanChooseFiles_(True)
	Panel.setCanChooseDirectories_(False)
	if filetypes is not None:
		Panel.setAllowedFileTypes_(filetypes)
	if ProposedFileName is not None:
		if ProposedFileName.find("/") >= 0:
			path, ProposedFileName = os.path.split(ProposedFileName)
			Panel.setDirectoryURL_(NSURL.fileURLWithPath_(path))
		Panel.setNameFieldStringValue_(ProposedFileName)
	pressedButton = Panel.runModal()
	if pressedButton == NSOKButton:
		return Panel.filename()
	return None

'''
.. function:: GetSaveFile(message=None, ProposedFileName=None, filetypes=None)

Opens a file chooser dialog.

:param message:
:param filetypes:
:param ProposedFileName:
:return: The selected file or None
:rtype: unicode
'''

def __allItems__(self):
	items = []
	for key in self.allKeys():
		value = self[key]
		items.append((key, value))
	return items
MGOrderedDictionary.items = __allItems__

def __allKeys__(self):
	return self.allKeys()
MGOrderedDictionary.keys = __allKeys__

def __Dict_removeObjectForKey__(self, key):
	if isinstance(key, int):
		if key < 0:
			key += len(self)
			if key < 0:
				raise IndexError("list index out of range")
		self.removeObjectAtIndex_(key)
		return
	self.removeObjectForKey_(key)

MGOrderedDictionary.__delitem__ = __Dict_removeObjectForKey__

GSNotifyingDictionary.items = __allItems__
GSNotifyingDictionary.keys = __allKeys__


# This should be possible but the way pyObjc wrapper works does not allow it.
# http://permalink.gmane.org/gmane.comp.python.pyobjc.devel/5493
# def __Dict__objectForKey__(self, key):
# 	if isinstance(key, int):
# 		if key < 0:
# 			key += len(self)
# 			if key < 0:
# 				raise IndexError("list index out of range")
# 		self.objectAtIndex_(key)
# 		return
# 	self.objectForKey_(key)
# MGOrderedDictionary.__getitem__ = __Dict__objectForKey__


def __Dict__iter__(self):
	Values = self.values()
	if Values is not None:
		for element in Values:
			yield element
MGOrderedDictionary.__iter__ = __Dict__iter__

def __Dict__del__(self, key):
	self.removeObjectForKey_(key)
MGOrderedDictionary.__delattr__ = __Dict__del__


def GetFile(message=None, allowsMultipleSelection=False, filetypes=None):
	return GetOpenFile(message, allowsMultipleSelection, filetypes)

def GetOpenFile(message=None, allowsMultipleSelection=False, filetypes=None, path=None):
	if filetypes is None:
		filetypes = []
	Panel = NSOpenPanel.openPanel().retain()
	Panel.setCanChooseFiles_(True)
	Panel.setCanChooseDirectories_(False)
	Panel.setAllowsMultipleSelection_(allowsMultipleSelection)
	if path is not None:
		Panel.setDirectory_(path)
	if message is not None:
		Panel.setTitle_(message)
	if filetypes is not None and len(filetypes) > 0:
		Panel.setAllowedFileTypes_(filetypes)
	pressedButton = Panel.runModal()
	if pressedButton == NSOKButton:
		if allowsMultipleSelection:
			return Panel.filenames()
		else:
			return Panel.filename()
	return None
'''
.. function:: GetOpenFile(message=None, allowsMultipleSelection=False, filetypes=None)

Opens a file chooser dialog.

:param message: A message string.
:param allowsMultipleSelection: Boolean, True if user can select more than one file
:param filetypes: list of strings indicating the filetypes, e.g., ["gif", "pdf"]
:param path: The initial directory path
:return: The selected file or a list of file names or None
:rtype: unicode or list
'''

def GetFolder(message=None, allowsMultipleSelection=False, path=None):
	Panel = NSOpenPanel.openPanel().retain()
	Panel.setCanChooseFiles_(False)
	Panel.setCanChooseDirectories_(True)
	Panel.setAllowsMultipleSelection_(allowsMultipleSelection)
	if path is not None:
		Panel.setDirectory_(path)
	pressedButton = Panel.runModal()
	if pressedButton == NSOKButton:
		if allowsMultipleSelection:
			return Panel.filenames()
		else:
			return Panel.filename()
	return None

'''
.. function:: GetFolder(message=None, allowsMultipleSelection = False)

Opens a folder chooser dialog.

:param message:
:param allowsMultipleSelection:
:param path:
:return: The selected folder or None
:rtype: unicode
'''

def Message(message, title="Alert", OKButton=None):
	Glyphs.showAlert_message_OKButton_(title, message, OKButton)

'''
.. function:: Message(title, message, OKButton=None)

Shows an alert panel.

:param title:
:param message:
:param OKButton:
'''

def LogToConsole(message, title=None):
	f = sys._getframe(1)

	if not title:
		title = "<>"
		try:
			title = f.f_code.co_name + " (line %d)" % f.f_lineno
		except:
			pass

	myLog = "Log message from \"%s\":\n%s" % (title, message)
	NSLog(myLog)

'''
.. function:: LogToConsole(message)

Write a message to the Mac's Console.app for debugging.

:param message:
'''


lastErrorMessage = ''
def LogError(message):
	global lastErrorMessage
	if message != lastErrorMessage:
		lastErrorMessage = message
		sys.stderr.write(message)

'''
.. function:: LogError(message)

Log an error message and write it to the Macro window’s output (in red).

:param message:
'''






'''
Constants
=========

Node types

.. data:: LINE

	Line node.

.. data:: CURVE

	Curve node. Make sure that each curve node is preceded by two off-curve nodes.

.. data:: QCURVE

	Quadratic curve node. Make sure that each curve node is preceded by at least one off-curve node.

.. data:: OFFCURVE

	Off-cuve node

Export formats
==============

.. data:: OTF

	Write CFF based font

.. data:: TTF

	Write CFF based font

.. data:: VARIABLE

	Write Variable font

.. data:: UFO

	Write UFO based font

.. data:: WOFF

	Write WOFF

.. data:: WOFF2

	Write WOFF

.. data:: PLAIN

	do not package as webfont

.. data:: EOT

	Write EOT

.. versionadded:: 2.5

Hint types
==========

.. data:: TOPGHOST

	Top ghost for PS hints

.. data:: STEM

	Stem for PS hints

.. data:: BOTTOMGHOST

	Bottom ghost for PS hints

.. data:: TTANCHOR

	Anchor for TT hints

.. data:: TTSTEM

	Stem for TT hints

.. data:: TTALIGN

	Align for TT hints

.. data:: TTINTERPOLATE

	Interpolation for TT hints

.. data:: TTDIAGONAL

	Diagonal for TT hints

.. data:: TTDELTA
	Delta TT hints

.. data:: CORNER

	Corner Component

.. data:: CAP

	Cap Component

Hint Option
===========

This is only used for TrueType hints.

.. data:: TTROUND

	Round to grid

.. data:: TTROUNDUP

	Round up

.. data:: TTROUNDDOWN

	Round down

.. data:: TTDONTROUND

	Don’t round at all

.. data:: TRIPLE = 128

	Indicates a triple hint group. There need to be exactly three horizontal TTStem hints with this setting to take effect.

Menu Tags
=========

This are tags to access the menu items in the apps main menu. Please see :attr:`GSApplication.menu` for details

.. data:: APP_MENU

	The 'Glyphs' menu

.. data:: FILE_MENU

	The File menu

.. data:: EDIT_MENU

	The Edit menu

.. data:: GLYPH_MENU

	The Glyph menu

.. data:: PATH_MENU

	The Path menu

.. data:: FILTER_MENU

	The Filter menu

.. data:: VIEW_MENU

	The View menu

.. data:: SCRIPT_MENU

	The Script menu

.. data:: WINDOW_MENU

	The Window menu

.. data:: HELP_MENU

	The Help menu

Menu States
===========

.. data:: ONSTATE

	The menu entry will have a checkbox

.. data:: OFFSTATE

	The menu entry will have no checkbox

.. data:: MIXEDSTATE

	The menu entry will have horizontal line

Callback Keys
=============

This are the available callbacks

.. data:: DRAWFOREGROUND

	to draw in the foreground

.. data:: DRAWBACKGROUND

	to draw in the background

.. data:: DRAWINACTIVE

	draw inactive glyphs

.. data:: DOCUMENTOPENED

	is called if a new document is opened

.. data:: DOCUMENTACTIVATED

	is called when the document becomes the active document

.. data:: DOCUMENTWASSAVED

	is called when the document is saved.
	The document itself is passed in notification.object()

.. data:: DOCUMENTEXPORTED

	if a font is exported. This is called for every instance and ``notification.object()`` will contain the path to the final font file.

.. code-block:: python
	def exportCallback(info):
		try:
			print(info.object())
		except:
			# Error. Print exception.
			import traceback
			print(traceback.format_exc())

	# add your function to the hook
	Glyphs.addCallback(exportCallback, DOCUMENTEXPORTED)


.. data:: DOCUMENTCLOSED

	is called when the document is closed

.. data:: TABDIDOPEN

	if a new tab is opened

.. data:: TABWILLCLOSE

	if a tab is closed

.. data:: UPDATEINTERFACE

	if some thing changed in the edit view. Maybe the selection or the glyph data.

.. data:: MOUSEMOVED

	is called if the mouse is moved. If you need to draw something, you need to call `Glyphs.redraw()` and also register to one of the drawing callbacks.

Writing Directions
==================

The writing directions of the Edit View.

.. data:: LTR

	Left To Right (e.g. Latin)

.. data:: RTL

	Right To Left (e.g. Arabic, Hebrew)

.. data:: LTRTTB

	Left To Right, Top To Bottom

.. data:: RTLTTB

	Right To Left, Top To Bottom


Annotation types
================

.. data:: TEXT

.. data:: ARROW

.. data:: CIRCLE

.. data:: PLUS

.. data:: MINUS

'''
