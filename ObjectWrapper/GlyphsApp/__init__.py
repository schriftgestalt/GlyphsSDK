# encoding: utf-8

from __future__ import print_function

import objc, time, math, sys, os, re, traceback, copy, datetime

objc.registerCFSignature("NSObject", b"^{NSObject=#}", 0, "NSObject") # This is to circumvent a bug in clang <https://github.com/ronaldoussoren/pyobjc/issues/298> Could be remove if Xcode 11.4 is out
objc.registerCFSignature("NSMutableDictionary", b"^{NSMutableDictionary=#}16@0:8", 0, "NSMutableDictionary")

from Foundation import NSObject, NSString, NSArray, NSMutableArray, NSMutableDictionary, NSDictionary, NSNumber, NSConcreteValue, \
	NSClassFromString, NSUserDefaults, NSURL, NSNotificationCenter, NSMakePoint, NSNotFound, NSAttributedString, \
	NSMutableAttributedString, NSLog, NSBundle, NSAffineTransform, NSPoint, NSRect, NSRange, NSUserNotification, \
	NSUserNotificationCenter, NSDate, NSIndexSet, NSNull, NSAffineTransform
from AppKit import NSApp, NSDocumentController, NSOpenPanel, NSSavePanel, NSOKButton, NSWorkspace, \
	NSMenu, NSMenuItem, NSOnState, NSOffState, NSMixedState, NSColor, NSError

GSFont = objc.lookUpClass("GSFont")

bundle = NSBundle.bundleForClass_(GSFont.__class__)
foo = objc.initFrameworkWrapper("GlyphsCore",
	frameworkIdentifier="com.schriftgestaltung.GlyphsCore",
	frameworkPath=bundle.bundlePath(),
	globals=globals())

GSFontMaster = objc.lookUpClass("GSFontMaster")
GSAxis = objc.lookUpClass("GSAxis")
GSMetric = objc.lookUpClass("GSMetric")
GSInfoValue = objc.lookUpClass("GSInfoValue")
GSGlyph = objc.lookUpClass("GSGlyph")
GSGlyphInfo = objc.lookUpClass("GSGlyphInfo")
GSGlyphsInfo = objc.lookUpClass("GSGlyphsInfo")
GSGuide = objc.lookUpClass("GSGuide")
GSGuideLine = GSGuide # compatibility
GSHint = objc.lookUpClass("GSHint")
GSInstance = objc.lookUpClass("GSInstance")
GSLayer = objc.lookUpClass("GSLayer")
GSNode = objc.lookUpClass("GSNode")
GSPath = objc.lookUpClass("GSPath")
GSShape = objc.lookUpClass("GSShape")
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
GSFontViewController = objc.lookUpClass("GSFontViewController")
GSElement = objc.lookUpClass("GSElement")
GSFeature = objc.lookUpClass("GSFeature")
GSFeaturePrefix = objc.lookUpClass("GSFeaturePrefix")
GSProxyShapes = objc.lookUpClass("GSProxyShapes")
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
GSMacroViewController = objc.lookUpClass("GSMacroViewController")
GSPathSegment = objc.lookUpClass("GSPathSegment")
PreviewTextWindow = objc.lookUpClass("PreviewText")
GSFontInfoValueLocalized = objc.lookUpClass("GSFontInfoValueLocalized")
GSFontInfoValueSingle = objc.lookUpClass("GSFontInfoValueSingle")
GSFontInfoValue = objc.lookUpClass("GSFontInfoValue")
GSMetricValue = objc.lookUpClass("GSMetricValue")
__all__ = [

	"Glyphs", "GetFile",
	"wrapperVersion",
	"GSAlignmentZone", "GSAnchor", "GSAnnotation", "GSApplication", "GSBackgroundImage", "GSBackgroundLayer", "GSClass", "GSComponent", "GSControlLayer", "GSGlyphReference",
	"GSCustomParameter", "GSDocument", "GSProjectDocument", "GSEditViewController", "GSFontViewController", "GSElement", "GSFeature", "GSFeaturePrefix", "GSFont", "GSFontMaster",
	"GSGlyph", "GSGlyphInfo", "GSGlyphsInfo", "GSGuide", "GSGuideLine", "GSHint", "GSInstance", "GSLayer", "GSNode", "GSPath", "GSShape", "GSSubstitution", "GSPartProperty", "GSAxis", "GSMetric", "GSMetricValue", "GSFontInfoValue", "GSFontInfoValueLocalized", "GSFontInfoValueSingle", "GSInfoValue", "GSNotifyingDictionary",
	"GSPathFinder", "GSPathPen", "GSCallbackHandler", "GSFeatureGenerator", "GSTTStem", "GSPathSegment",
	# Constants
	"MOVE", "LINE", "CURVE", "OFFCURVE", "QCURVE", "HOBBYCURVE", "GSMOVE", "GSLINE", "GSCURVE", "GSQCURVE", "GSOFFCURVE", "GSHOBBYCURVE", "GSSHARP", "GSSMOOTH",
	"FILL", "FILLCOLOR", "FILLPATTERNANGLE", "FILLPATTERNBLENDMODE", "FILLPATTERNFILE", "FILLPATTERNOFFSET", "FILLPATTERNSCALE", "STROKECOLOR", "STROKELINECAPEND", "STROKELINECAPSTART", "STROKELINEJOIN", "STROKEPOSITION", "STROKEWIDTH", "STROKEHEIGHT", "GRADIENT", "SHADOW", "INNERSHADOW", "MASK", 
	"INSTANCETYPESINGLE", "INSTANCETYPEVARIABLE",
	"TAG", "TOPGHOST", "STEM", "BOTTOMGHOST", "FLEX", "TTSNAP", "TTSTEM", "TTSHIFT", "TTINTERPOLATE", "TTDIAGONAL", "TTDELTA", "TTDONTROUND", "TTROUND", "TTROUNDUP", "TTROUNDDOWN", "TRIPLE",
	"TTANCHOR", "TTALIGN", # backwards compatibilty

	"CORNER", "CAP", "BRUSH", "SEGMENT",

	"TEXT", "ARROW", "CIRCLE", "PLUS", "MINUS",
	"GSBIDI", "GSLTR", "GSRTL", "GSVertical", "GSVerticalToRight",
	# compatibilty
	"BIDI", "LTR", "RTL", "LTRTTB", "RTLTTB",
	"GSTopLeft", "GSTopCenter", "GSTopRight", "GSCenterLeft", "GSCenterCenter", "GSCenterRight", "GSBottomLeft", "GSBottomCenter", "GSBottomRight",

	"OTF", "TTF", "VARIABLE", "UFO", "WOFF", "WOFF2", "PLAIN", "EOT",

	"GSPropertyNameFamilyNamesKey", "GSPropertyNameDesignersKey", "GSPropertyNameDesignerURLKey",
	"GSPropertyNameManufacturersKey", "GSPropertyNameManufacturerURLKey", "GSPropertyNameCopyrightsKey",
	"GSPropertyNameVersionStringKey", "GSPropertyNameVendorIDKey", "GSPropertyNameUniqueIDKey",
	"GSPropertyNameLicensesKey", "GSPropertyNameLicenseURLKey", "GSPropertyNameTrademarksKey",
	"GSPropertyNameDescriptionsKey", "GSPropertyNameSampleTextsKey", "GSPropertyNamePostscriptFullNameKey",
	"GSPropertyNamePostscriptFontNameKey", "GSPropertyNameCompatibleFullNamesKey",
	"GSPropertyNameStyleNamesKey", "GSPropertyNameStyleMapFamilyNamesKey",
	"GSPropertyNameStyleMapStyleNamesKey", "GSPropertyNamePreferredFamilyNamesKey",
	"GSPropertyNamePreferredSubfamilyNamesKey", "GSPropertyNameVariableStyleNamesKey",
	"GSPropertyNameWWSFamilyNameKey", "GSPropertyNameWWSSubfamilyNameKey",
	"GSPropertyNameVariationsPostScriptNamePrefixKey",

	# Methods
	"divideCurve", "distance", "addPoints", "subtractPoints", "GetFolder", "GetSaveFile", "GetOpenFile", "Message", "AskString", "LogToConsole", "LogError", "removeOverlap", "subtractPaths", "intersectPaths", "scalePoint",

	# Classes
	"GSSmartComponentAxis",

	# Menus
	"APP_MENU", "FILE_MENU", "EDIT_MENU", "GLYPH_MENU", "PATH_MENU", "FILTER_MENU", "VIEW_MENU", "SCRIPT_MENU", "WINDOW_MENU", "HELP_MENU",
	"ONSTATE", "OFFSTATE", "MIXEDSTATE",

	# Callbacks:

	"DRAWFOREGROUND", "DRAWBACKGROUND", "DRAWINACTIVE", "DOCUMENTOPENED", "DOCUMENTACTIVATED", "DOCUMENTWASSAVED", "DOCUMENTEXPORTED", "DOCUMENTCLOSED", "DOCUMENTWILLCLOSE", "DOCUMENTDIDCLOSE", "TABDIDOPEN", "TABWILLCLOSE", "UPDATEINTERFACE",
	"MOUSEMOVED", "MOUSEDRAGGED", "MOUSEDOWN", "MOUSEUP", "CONTEXTMENUCALLBACK",
	
	"GSMetricsKeyAscender", "GSMetricsKeyCapHeight", "GSMetricsKeySlantHeight", "GSMetricsKeyxHeight", "GSMetricsKeyTopHeight", "GSMetricsKeyDescender", "GSMetricsKeyBaseline",
	"GSNoCase", "GSUppercase", "GSLowercase", "GSSmallcaps", "GSMinor", "GSOtherCase", 

	"GSFormatVersion1", "GSFormatVersion3", "GSFormatVersionCurrent",

	"GSShapeTypePath", "GSShapeTypeComponent",
	"PreviewTextWindow"
	]


wrapperVersion = "3.0"


try:
	from objc import python_method
except ImportError:
	def python_method(arg):
		return arg
	objc.python_method = python_method


def _________________(): pass
def ____CONSTANTS____(): pass
def _________________(): pass

GSFormatVersion1 = 1
GSFormatVersion3 = 3
GSFormatVersionCurrent = 3

GSPackageFlatFile = 1
GSPackageBundle = 2

GSPropertyNameFamilyNamesKey = "familyNames"
GSPropertyNameDesignersKey = "designers"
GSPropertyNameDesignerURLKey = "designerURL"
GSPropertyNameManufacturersKey = "manufacturers"
GSPropertyNameManufacturerURLKey = "manufacturerURL"
GSPropertyNameCopyrightsKey = "copyrights"
GSPropertyNameVersionStringKey = "versionString"
GSPropertyNameVendorIDKey = "vendorID"
GSPropertyNameUniqueIDKey = "uniqueID"
GSPropertyNameLicensesKey = "licenses"
GSPropertyNameLicenseURLKey = "licenseURL"
GSPropertyNameTrademarksKey = "trademarks"
GSPropertyNameDescriptionsKey = "descriptions"
GSPropertyNameSampleTextsKey = "sampleTexts"
GSPropertyNamePostscriptFullNameKey = "postscriptFullName"
GSPropertyNamePostscriptFontNameKey = "postscriptFontName"
GSPropertyNameCompatibleFullNamesKey = "compatibleFullNames"
GSPropertyNameStyleNamesKey = "styleNames"
GSPropertyNameStyleMapFamilyNamesKey = "styleMapFamilyNames"
GSPropertyNameStyleMapStyleNamesKey = "styleMapStyleNames"
GSPropertyNamePreferredFamilyNamesKey = "preferredFamilyNames"
GSPropertyNamePreferredSubfamilyNamesKey = "preferredSubfamilyNames"
GSPropertyNameVariableStyleNamesKey = "variableStyleNames"
GSPropertyNameWWSFamilyNameKey = "WWSFamilyName"
GSPropertyNameWWSSubfamilyNameKey = "WWSSubfamilyName"
GSPropertyNameVariationsPostScriptNamePrefixKey = "variationsPostScriptNamePrefix"

GSShapeTypePath = 1 << 1
GSShapeTypeComponent = 1 << 2

GSMOVE_ = 17
GSLINE_ = 1
GSCURVE_ = 35
GSQCURVE_ = 36
GSHOBBYCURVE_ = 37
GSOFFCURVE_ = 65
GSSHARP = 0
GSSMOOTH = 100

GSMOVE = "move"
GSLINE = "line"
GSCURVE = "curve"
GSQCURVE = "qcurve"
GSOFFCURVE = "offcurve"
GSHOBBYCURVE = "hobbycurve"

MOVE = "move"
LINE = "line"
CURVE = "curve"
QCURVE = "qcurve"
OFFCURVE = "offcurve"
HOBBYCURVE = "hobbycurve"

# Path Attributes 
FILL = "fill"
FILLCOLOR = "fillColor"
FILLPATTERNANGLE = "fillPatternAngle"
FILLPATTERNBLENDMODE = "fillPatternBlendMode"
FILLPATTERNFILE = "fillPatternFile"
FILLPATTERNOFFSET = "fillPatternOffset"
FILLPATTERNSCALE = "fillPatternScale"
STROKECOLOR = "strokeColor"
STROKELINECAPEND = "lineCapEnd"
STROKELINECAPSTART = "lineCapStart"
STROKELINEJOIN = "lineJoin"
STROKEPOSITION = "strokePos"
STROKEWIDTH = "strokeWidth"
STROKEHEIGHT = "strokeHeight"
GRADIENT = "gradient"
SHADOW = "shadow"
INNERSHADOW = "shadowIn"
MASK = "mask"


# instance type

INSTANCETYPESINGLE = 0
INSTANCETYPEVARIABLE = 1
# GSInstanceTypeIcon

TAG = -2
TOPGHOST = -1
STEM = 0
BOTTOMGHOST = 1
FLEX = 2
TTSNAP = 3
TTANCHOR = 3 # backwards compatibilty
TTSTEM = 4
TTSHIFT = 5
TTALIGN = 5 # backwards compatibilty
TTINTERPOLATE = 6
TTDIAGONAL = 8
TTDELTA = 9
CORNER = 16
CAP = 17
BRUSH = 18
SEGMENT = 19

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

GSOutlineFormatCFF = 1
GSOutlineFormatTrueType = 2
GSOutlineFormatVariableTT = 3

GSMetricsKeyAscender = "ascender"
GSMetricsKeyCapHeight = "cap height"
GSMetricsKeySlantHeight = "slant height"	# defaults to half xHeight
GSMetricsKeyxHeight = "x-height"			# better "Midheight"?
GSMetricsKeyTopHeight = "topHeight"			# global top boundary, can be xHeight, CapHeight, ShoulderHeight...
GSMetricsKeyDescender = "descender"
GSMetricsKeyBaseline = "baseline"


GSNoCase = 0
GSUppercase = 1
GSLowercase = 2
GSSmallcaps = 3
GSMinor = 4
GSOtherCase = 5 # ??


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
GSBIDI = 1
GSLTR = 0
GSRTL = 2
GSVertical = 4 # CJK
GSVerticalToRight = 8 # Mongolian

BIDI = 1
LTR = 0
RTL = 2
LTRTTB = 4
RTLTTB = 8

# Callbacks
DRAWFOREGROUND = "DrawForeground"
DRAWBACKGROUND = "DrawBackground"
DRAWINACTIVE = "DrawInactive"
DOCUMENTOPENED = "GSDocumentWasOpenedNotification"
DOCUMENTACTIVATED = "GSDocumentActivateNotification"
DOCUMENTWASSAVED = "GSDocumentWasSavedSuccessfully"
DOCUMENTEXPORTED = "GSDocumentWasExportedNotification"
DOCUMENTCLOSED = "GSDocumentWillCloseNotification" # deprecated use DOCUMENTWILLCLOSE
DOCUMENTWILLCLOSE = "GSDocumentWillCloseNotification"
DOCUMENTDIDCLOSE = "GSDocumentDidCloseNotification"
TABDIDOPEN = "TabDidOpenNotification"
TABWILLCLOSE = "TabWillCloseNotification"
UPDATEINTERFACE = "GSUpdateInterface"
MOUSEMOVED = "mouseMovedNotification"
MOUSEDRAGGED = "mouseDraggedNotification"
MOUSEDOWN = "mouseDownNotification"
MOUSEUP = "mouseUpNotification"
CONTEXTMENUCALLBACK = "GSContextMenuCallbackName"

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
'''

def GSObject__copy__(self, memo=None):
	return self.copy()
	
NSObject.__copy__ = python_method(GSObject__copy__)
NSObject.__deepcopy__ = python_method(GSObject__copy__)

def GSObject__new__(typ, *args, **kwargs):
	"""__new__(...)"""
	return typ.alloc().init()

class Proxy(object):
	_owner = None
	def __init__(self, owner):
		self._owner = owner
	def __repr__(self):
		"""Return list-lookalike of representation string of objects"""
		strings = []
		for currItem in self:
			strings.append(str(currItem))
		if len(strings) == 0:
			return "()"
		return "(\n\t%s\n)" % (',\n\t'.join(strings))
	def __len__(self):
		Values = self.values()
		if Values is not None:
			return len(Values)
		return 0
	def pop(self, idx=-1):
		if isinstance(idx, int):
			node = self[idx]
			del self[idx]
			return node
		else:
			raise(KeyError)
	def __delitem__(self, key):
		if isinstance(key, slice):
			for i in sorted(range(*key.indices(self.__len__())), reverse=True):
				self.__delitem__(i)
			return
		elif isinstance(key, int):
			idx = self._validate_idx(key)
			self.removeItemAtIndexMethod()(idx)
		else:
			raise TypeError("list indices must be integers, not %s" % type(key).__name__)
	def __iter__(self):
		Values = self.values()
		if Values is None:
			return None
		return iter(Values)
	def values(self):
		raise AttributeError("This collection does not support item iteration")
	def index(self, Value):
		return self.values().index(Value)
	def __copy__(self):
		return list(self)
	def __deepcopy__(self, memo):
		return [x.copy() for x in self.values()]
	def copy(self):
		return self.__copy__()
	def count(self, value):
		return list(self).count(value)
	def __contains__(self, key):
		return key in self.values()

	def clear(self):
		for i in range(len(self)-1, -1, -1):
			self.__delitem__(i)

	def __add__(self, value):
		return list(self).__add__(list(value))
	def __iadd__(self, value):
		self.extend(value)
		return self
	def __mul__(self, value):
		return list(self).__mul__(value)
	def __imul__(self, value):
		if not isinstance(value, int):
			raise TypeError("can't multiply sequence by non-int of type %s" %type(value).__name__)
		if value <= 0:
			self.clear()
		if value <= 1:
			return self
		old_values = self.copy()
		for _ in range(value-1):
			self.extend(old_values)
		return self

	def extend(self, value):
		for e in value:
			self.append(e)

	def __eq__(self, other):
		""" Support comparison to other proxies, NSArrays or lists"""
		return list(self).__eq__(list(other))
	def __ne__(self, other):
		return list(self).__ne__(list(other))
	def __lt__(self, other):
		return list(self).__lt__(list(other))
	def __le__(self, other):
		return list(self).__le__(list(other))
	def __gt__(self, other):
		return list(self).__gt__(list(other))
	def __ge__(self, other):
		return list(self).__ge__(list(other))

	def _validate_idx(self, idx, offset=0):
		"""Handle negative indices and check for IndexError
		Use offset to adjust the valid range, e.g. for insert len(self) is
		still a valid index.
		"""
		if not isinstance(idx, int):
			raise TypeError("indices must be integers, not %s" % type(idx).__name__)
		if idx < 0:
			idx += self.__len__()
		if not (0 <= idx < self.__len__() + offset):
			raise IndexError("list index %s out of range %s" % (idx, self.__len__() + offset))
		return idx
	def setterMethod(self):
		raise AttributeError("This collection cannot be directly overwritten")
	def setter(self, values):
		method = self.setterMethod()
		if isinstance(values, (list, NSArray)):
			method(NSMutableArray.arrayWithArray_(values))
		elif isinstance(values, (tuple, type(self))):
			method(NSMutableArray.arrayWithArray_(list(values)))
		elif values is None:
			method(NSMutableArray.array())
		else:
			raise TypeError("Cant set value of type %s" % type(values).__name__)

class GSProxyShapesIterator:
	def __init__(self, proxy):
		self.proxy = proxy
		self.n = 0
	def next(self):
		return self.__next__()
	def __next__(self):
		shape = self.proxy.objectAtIndex_(self.n)
		self.n += 1
		if shape:
			return shape
		else:
			raise StopIteration

def GSProxyShapes__iter__(self):
	return GSProxyShapesIterator(self)
GSProxyShapes.__iter__ = python_method(GSProxyShapes__iter__)
def GSProxyShapes__getitem__(self, idx):
	if idx < self.count():
		return self.objectAtIndex_(idx)
	raise IndexError("list index out of range")
GSProxyShapes.__getitem__ = python_method(GSProxyShapes__getitem__)
GSProxyShapes.__len__ = property(lambda self: self.count)
GSProxyShapes.__contains__ = python_method(lambda self, item: self.containsObject_(item))
# this improves compatibility with Glyphs 2 code
GSProxyShapes.append = python_method(lambda self, item: self.layer().addShape_(item))
GSProxyShapes.extend = python_method(lambda self, items: self.layer().addShapes_(items))

##################################################################################
#
#
#
#           GSApplication
#
#
#
##################################################################################

def _____________________(): pass
def ____GSApplication____(): pass
def _____________________(): pass


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
		currentDocument
		documents
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
'''
	.. attribute:: currentDocument
		The active :class:`GSDocument` object or None.

		:type: :class:`GSDocument`

		.. code-block:: python
			# topmost open document
			document = Glyphs.currentDocument
'''

GSApplication.documents = property(lambda self: AppDocumentProxy(self))
'''
	.. attribute:: documents
		An array of open :class:`GSDocument` objects.

		:type: list
'''

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
		The active :class:`GSFont` object or None.

		:type: :class:`GSFont`
'''

GSApplication.fonts = property(lambda self: AppFontProxy(self))

'''
	.. attribute:: fonts
		Be aware that the order is defined by last used font. Append and extend generally don't insert at the end of the list.

		:type: list

		.. code-block:: python
			# access all open fonts
			for font in Glyphs.fonts:
				print(font.familyName)

			# add a font
			font = GSFont()
			font.familyName = "My New Fonts"
			Glyphs.fonts.append(font)
'''

GSApplication.reporters = property(lambda self: GSCallbackHandler.reporterInstances().allValues())

'''
	.. attribute:: reporters
		List of available reporter plug-ins (same as bottom section in the 'View' menu). These are the actual objects. You can get hold of their names using `object.__class__.__name__`.

		Also see :meth:`GSApplication.activateReporter()` and :meth:`GSApplication.deactivateReporter()` methods below to activate/deactivate them.

		:type: list

		.. code-block:: python
			# List of all reporter plug-ins
			print(Glyphs.reporters)

			# Individual plug-in class names
			for reporter in Glyphs.reporters:
				print(reporter.__class__.__name__)

			# Activate a plugin
			Glyphs.activateReporter(Glyphs.reporters[0]) # by object
			Glyphs.activateReporter('GlyphsMasterCompatibility') # by class name
'''

GSApplication.activeReporters = property(lambda self: GSCallbackHandler.activeReporters())

'''
	.. attribute:: activeReporters
		List of activated reporter plug-ins.

		:type: list

		.. code-block:: python
			# Activate a plugin
			Glyphs.activateReporter(Glyphs.reporters[0])

			# list of currently active reporter plug-ins 
			activeReporters = Glyphs.activeReporters
'''

GSApplication.filters = property(lambda self: list(NSApp.delegate().filterInstances()))

'''
	.. attribute:: filters
		List of available filters (same as 'Filter' menu). These are the actual objects.

		Below sample code shows how to get hold of a particular filter and use it. You invoke it using the `processFont_withArguments_()` function for old plugins, or the `filter()` function for newer plugins.
		As arguments you use the list obtained by clicking on 'Copy Custom Parameter' button in the filter’s dialog (gear icon) and convert it to a list.
		In the `include` option you can supply a comma-separated list of glyph names.

		:type: list

		.. code-block:: python
			# Helper function to get filter by its class name
			def filterForName(name):
				for filter in Glyphs.filters:
					if filter.__class__.__name__ == name:
						return filter

			# Get the filter
			offsetCurveFilter = filterForName('GlyphsFilterOffsetCurve')

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
	if isString(pyObject):
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
		for key, value in pyObject.items():
			dictionary.setObject_forKey_(objcObject(value), objcObject(key))
		return dictionary
	if pyObject is None:
		return NSNull.null()
	return pyObject

def validatePoint(value=None):
	return validateTuple(2, value)
def validateScale(value=None):
	value = validateTuple(1, value)
	if len(value) == 1:
		value = (value[0], value[0])
	elif len(value) > 2:
		raise ValueError
	return value
def validateTuple(expectedLenth, value=None):
	if value is None:
		return (0, 0)
	if expectedLenth == 1 and isinstance(value, (float, int)):
		value = (value,)
	if not isinstance(value, (tuple, NSPoint)):
		raise TypeError
	if len(value) < expectedLenth:
		raise ValueError
	for v in value:
		if not isinstance(v, (float, int)):
			raise TypeError
	return value
def validateNumber(value=None):
	if value is None:
		return 0
	if not isinstance(value, (float, int)):
		raise TypeError
	return value

class DefaultsProxy(Proxy):
	def __getitem__(self, key):
		if not isString(key):
			raise TypeError("defaults key must be str, not %s" % type(key).__name__)
		return NSUserDefaults.standardUserDefaults().objectForKey_(objcObject(key))
	def __setitem__(self, key, value):
		if not isString(key):
			raise TypeError("defaults key must be str, not %s" % type(key).__name__)
		if value is not None:
			NSUserDefaults.standardUserDefaults().setObject_forKey_(objcObject(value), objcObject(key))
		else:
			NSUserDefaults.standardUserDefaults().removeObjectForKey_(key)
	def __delitem__(self, key):
		if not isString(key):
			raise TypeError("defaults key must be str, not %s" % type(key).__name__)
		NSUserDefaults.standardUserDefaults().removeObjectForKey_(objcObject(key))
	def get(self, key, default = None):
		if not isString(key):
			raise TypeError("defaults key must be str, not %s" % type(key).__name__)
		value = NSUserDefaults.standardUserDefaults().objectForKey_(key)
		if value is None:
			return default
		return value
	def pop(self, key):
		if isinstance(key, str):
			return self[key] # doesn‘t make sense to delet the value. This is mostly here for the unit tests
		else:
			raise(KeyError)
	def __repr__(self):
		return "<Userdefaults>"

GSApplication.defaults = property(lambda self: DefaultsProxy(self))

def printtraceback():
	code = []
	for threadId, stack in sys._current_frames().items():
		#code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""), threadId))
		for filename, lineno, name, line in traceback.extract_stack(stack):
			code.append('File: "%s", line %d, in %s' % (filename, lineno, name))
			if line:
				code.append("  %s" % (line.strip()))
	if len(code) > 1:
		del(code[-1])
	if len(code) > 1:
		del(code[-1])
	print("\n".join(code))

def __registerDefault__(self, key, value):
	if key != None and value != None and len(key) > 2:
		NSUserDefaults.standardUserDefaults().registerDefaults_(objcObject({key : value}))
	else:
		raise KeyError
GSApplication.registerDefault = python_method(__registerDefault__)

def __registerDefaults__(self, defaults):
	if defaults is not None:
		NSUserDefaults.standardUserDefaults().registerDefaults_(objcObject(defaults))
	else:
		raise ValueError
GSApplication.registerDefaults = python_method(__registerDefaults__)

# TODO: docu for registerDefaults

'''
	.. attribute:: defaults
		A dict like object for storing preferences. You can get and set key-value pairs.

		Please be careful with your keys. Use a prefix that uses the reverse domain name. e.g. :samp:`com.MyName.foo.bar`.

		:type: dict

		.. code-block:: python
			# Check for whether or not a preference exists
			if "com.MyName.foo.bar" in Glyphs.defaults:
				# do stuff

			# Get and set values
			value = Glyphs.defaults["com.MyName.foo.bar"]
			Glyphs.defaults["com.MyName.foo.bar"] = newValue

			# Remove value
			# This will restore the default value
			del(Glyphs.defaults["com.MyName.foo.bar"])
'''

class BoolDefaultsProxy(DefaultsProxy):
	def __getitem__(self, key):
		if not isString(key):
			raise TypeError("defaults key must be str, not %s" % type(key).__name__)
		return NSUserDefaults.standardUserDefaults().boolForKey_(objcObject(key))
	def __setitem__(self, key, value):
		if not isString(key):
			raise TypeError("defaults key must be str, not %s" % type(key).__name__)
		if value is None:
			NSUserDefaults.standardUserDefaults().removeObjectForKey_(objcObject(key))
		elif isinstance(value, bool):
			NSUserDefaults.standardUserDefaults().setBool_forKey_(bool(value), objcObject(key))
		else:
			raise TypeError("boolDefaults only accepts values of type bool, not %s" % type(value).__name__)
	def get(self, key, default = None):
		if not isString(key):
			raise TypeError("defaults key must be str, not %s" % type(key).__name__)
		value = NSUserDefaults.standardUserDefaults().objectForKey_(key)
		if not value:
			return default
		return value.boolValue()

GSApplication.boolDefaults = property(lambda self: BoolDefaultsProxy(self))
'''
	.. attribute:: boolDefaults
		Access to default settings cast to a bool.

		:type: bool

		.. code-block:: python
			if Glyphs.boolDefaults["com.MyName.foo.bar"]:
				print('"com.MyName.foo.bar" is set')
'''

class ColorDefaultsProxy(DefaultsProxy):
	def __getitem__(self, key):
		if not isString(key):
			raise TypeError("defaults key must be str, not %s" % type(key).__name__)
		return NSUserDefaults.standardUserDefaults().colorForKey_(objcObject(key))
	def __setitem__(self, key, value):
		if not isString(key):
			raise TypeError("defaults key must be str, not %s" % type(key).__name__)
		if value is not None:
			if isString(value):
				color = NSColor.colorWithString_(value)
				if color is None:
					raise ValueError("Invalid color string: %s" % value)
				value = color
			if isinstance(value, NSColor):
				NSUserDefaults.standardUserDefaults().setColor_forKey_(value, objcObject(key))
			else:
				raise TypeError("color must be string or NSColor type, not %s" % type(value).__name__)
		else:
			NSUserDefaults.standardUserDefaults().removeObjectForKey_(objcObject(key))

GSApplication.colorDefaults = property(lambda self: ColorDefaultsProxy(self))

class IntDefaultsProxy(DefaultsProxy):
	def __getitem__(self, key):
		if not isString(key):
			raise TypeError("defaults key must be str, not %s" % type(key).__name__)
		return NSUserDefaults.standardUserDefaults().integerForKey_(objcObject(key))
	def __setitem__(self, key, value):
		if not isString(key):
			raise TypeError("defaults key must be str, not %s" % type(key).__name__)
		if value is None:
			NSUserDefaults.standardUserDefaults().removeObjectForKey_(objcObject(key))
		elif isinstance(value, int):
			NSUserDefaults.standardUserDefaults().setInteger_forKey_(value, objcObject(key))
		else:
			raise TypeError("intDefaults only accepts values of type int, not %s" % type(value).__name__)
	def get(self, key, default = None):
		if not isString(key):
			raise TypeError("defaults key must be str, not %s" % type(key).__name__)
		value = NSUserDefaults.standardUserDefaults().objectForKey_(objcObject(key))
		if not value:
			return default
		return value.integerValue()

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

		:type: dict
'''

GSApplication.scriptSuffixes = property(lambda self: GSGlyphsInfo.scriptSuffixes())
'''
	.. attribute:: scriptSuffixes
		A dictionary with glyphs name suffixes for scripts and their respective script names, e.g., 'cy': 'cyrillic'

		:type: dict
'''

GSApplication.languageScripts = property(lambda self: GSGlyphsInfo.languageScripts())

'''
	.. attribute:: languageScripts
		A dictionary with language tag to script tag mapping, e.g., 'ENG': 'latn'

		:type: dict
'''

GSApplication.languageData = property(lambda self: GSGlyphsInfo.languageData())

'''
	.. attribute:: languageData
		A list of dictionaries with more detailed language informations.

		:type: list
'''

GSApplication.unicodeRanges = property(lambda self: GSGlyphsInfo.unicodeRanges())

'''
	.. attribute:: unicodeRanges
		Names of unicode ranges.

		:type: list
'''

def Glyphs_setUserDefaults(self, key, value):
	self.defaults[key] = value


def NSStr(string):
	if string:
		return NSString.stringWithString_(string)
	else:
		return None

GSApplication.editViewWidth = property(lambda self: self.intDefaults["GSFontViewWidth"],
									   lambda self, value: Glyphs_setUserDefaults(self, "GSFontViewWidth", int(value)))
'''
	.. attribute:: editViewWidth
		Width of glyph Edit view. Corresponds to the "Width of editor" setting from the Preferences.

		:type: int
'''

GSApplication.handleSize = property(lambda self: self.intDefaults["GSHandleSize"],
									lambda self, value: Glyphs_setUserDefaults(self, "GSHandleSize", int(value)))
'''
	.. attribute:: handleSize
		Size of Bezier handles in Glyph Edit view. Possible value are 0–2. Corresponds to the ‘Handle size’ setting from the Preferences.

		To use the handle size for drawing in reporter plugins, you need to convert the handle size to a point size, and divide by the view’s scale factor. See example below.

		:type: int

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
'''

GSApplication.versionString = NSBundle.mainBundle().infoDictionary()["CFBundleShortVersionString"]

'''
	.. attribute:: versionString
		String containing Glyph.app’s version number. May contain letters also, like ‘2.3b’. To check for a specific version, use :attr:`Glyphs.versionNumber <GSApplication.versionNumber>` below.

		:type: string
'''

def Glyphs_FloatVersion(self):
	m = re.match(r"(\d+)\.(\d+)", self.versionString)
	return float(str(m.group(1)) + '.' + str(m.group(2)))
_versionNumber = Glyphs_FloatVersion(GSApplication)
GSApplication.versionNumber = _versionNumber

'''
	.. attribute:: versionNumber
		Glyph.app’s version number. Use this to check for version in your code.

		:type: float
'''

_buildNumber = float(NSBundle.mainBundle().infoDictionary()["CFBundleVersion"])
GSApplication.buildNumber = _buildNumber

'''
	.. attribute:: buildNumber
		Glyph.app’s build number.

		Especially if you’re using preview builds, this number may be more important to you than the version number. The build number increases with every released build and is the most significant evidence of new Glyphs versions, while the version number is set arbitrarily and stays the same until the next stable release.

		:type: float
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

class AppMenuProxy(Proxy):
	"""Access the main menu."""
	def __getitem__(self, key):
		if isinstance(key, int):
			idx = self._validate_idx(key)
			return self._owner.mainMenu().itemAtIndex_(idx)
		elif isString(key):
			Tag = menuTagLookup[key]
			return self._owner.mainMenu().itemWithTag_(Tag)
		raise TypeError("Expected int or str, not %s" % type(key).__name__)
	def values(self):
		return self._owner.mainMenu().itemArray()

GSApplication.menu = property(lambda self: AppMenuProxy(self))

'''
	.. attribute:: menu
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

def NSMenuItem__init__(self, title, callback=None, keyboard=None, modifier=0):
	self.setTitle_(title)
	if callback:
		callbackTargets = None
		try:
			callbackTargets = callbackOperationTargets["NSMenuItem"]
		except KeyError:
			callbackTargets = []
			callbackOperationTargets["NSMenuItem"] = callbackTargets
		helper = callbackHelperClass(callback, None)
		callbackTargets.append(helper)
		selector = objc.selector(helper.callback_, signature=b"v@:@")
		self.setAction_(selector)
		self.setTarget_(helper)
	if keyboard and keyboard != "":
		self.setKeyEquivalent_(keyboard)
		self.setKeyEquivalentModifierMask_(modifier)
NSMenuItem.__init__ = python_method(NSMenuItem__init__)

def __NSMenuItem__append__(self, item):
	self.submenu().addItem_(item)
NSMenuItem.append = python_method(__NSMenuItem__append__)

def __NSMenuItem__insert__(self, idx, item):
	self.submenu().insertItem_atIndex_(item, idx)
NSMenuItem.insert = python_method(__NSMenuItem__insert__)

def __NSMenu__append__(self, item):
	self.addItem_(item)
NSMenu.append = python_method(__NSMenu__append__)


def __NSURL__new__(typ, *args, **kwargs):
	if len(args) > 0:
		return typ.fileURLWithPath_(args[0])
	return typ.new()
NSURL.__new__ = staticmethod(__NSURL__new__)

'''
	**Functions**
'''

def OpenFont(self, Path, showInterface=True):
	URL = NSURL.fileURLWithPath_(Path)
	Doc = self.openDocumentWithContentsOfURL_display_(URL, showInterface)
	if Doc is not None:
		return Doc.font
	return None

GSApplication.open = python_method(OpenFont)

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

def __ShowMacroWindow__(self):
	Glyphs.delegate().showMacroWindow()

GSApplication.showMacroWindow = python_method(__ShowMacroWindow__)

'''
	.. function:: showMacroWindow

		Opens the macro window

	.. function:: clearLog

		Deletes the content of the console in the macro window
'''

def __showGlyphInfoPanelWithSearchString__(self, String):
	Glyphs.delegate().showGlyphInfoPanelWithSearchString_(String)

GSApplication.showGlyphInfoPanelWithSearchString = python_method(__showGlyphInfoPanelWithSearchString__)

'''
	.. function:: showGlyphInfoPanelWithSearchString(String)

		Shows the Glyph Info window with a preset search string

		:param String: The search term
'''

def _glyphInfoForName(self, String, font=None):
	if isinstance(String, int):
		return self.glyphInfoForUnicode(String)
	if font is not None:
		return font.glyphsInfo().glyphInfoForName_(String)
	return GSGlyphsInfo.sharedManager().glyphInfoForName_(String)

GSApplication.glyphInfoForName = python_method(_glyphInfoForName)

'''
	.. function:: glyphInfoForName(String)

		Generates :class:`GSGlyphInfo` object for a given glyph name.

		:param String: Glyph name
		:param font: if you add a font, and the font has a local glyph info, it will be used instead of the global info data.
		:return: :class:`GSGlyphInfo`
'''

def _glyphInfoForUnicode(self, String, font=None):
	if isinstance(String, int):
		String = "%04X" % String
	if font is not None:
		return font.glyphsInfo().glyphInfoForUnicode_(String)
	return GSGlyphsInfo.sharedManager().glyphInfoForUnicode_(String)

GSApplication.glyphInfoForUnicode = python_method(_glyphInfoForUnicode)

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
GSApplication.niceGlyphName = python_method(_niceGlyphName)

'''
	.. function:: niceGlyphName(Name)

		Converts glyph name to nice, human-readable glyph name (e.g. afii10017 or uni0410 to A-cy)

		:param string: glyph name
		:param font: if you add a font, and the font has a local glyph info, it will be used instead of the global info data.
		:return: string
'''

def _productionGlyphName(self, name, font=None):
	if font is not None:
		return font.glyphsInfo().productionGlyphNameForName_(name)
	return GSGlyphsInfo.sharedManager().productionGlyphNameForName_(name)
GSApplication.productionGlyphName = python_method(_productionGlyphName)

'''
	.. function:: productionGlyphName(name, [font=None])

		Converts glyph name to production glyph name (e.g. afii10017 or A-cy to uni0410)

		:param name: glyph name
		:param font: if you add a font, and the font has a local glyph info, it will be used instead of the global info data.
		:return: string
'''

def _ligatureComponents(self, String, font=None):
	if font is not None:
		return font.glyphsInfo().componentsForLigaName_font_(String, font)
	return GSGlyphsInfo.sharedManager().componentsForLigaName_font_(String, None)
GSApplication.ligatureComponents = python_method(_ligatureComponents)

'''
	.. function:: ligatureComponents(String)

		If defined as a ligature in the glyph database, this function returns a list of glyph names that this ligature could be composed of.
	
		:param string: glyph name
		:param font: if you add a font, and the font has a local glyph info, it will be used instead of the global info data.
		:rtype: list

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
Observers = (DOCUMENTOPENED, DOCUMENTACTIVATED, DOCUMENTWASSAVED, DOCUMENTEXPORTED, DOCUMENTCLOSED, DOCUMENTWILLCLOSE, DOCUMENTDIDCLOSE, TABDIDOPEN, TABWILLCLOSE, UPDATEINTERFACE, MOUSEMOVED, MOUSEDRAGGED, MOUSEDOWN, MOUSEUP)

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

	def callback_(self, notification):
		if self.func:
			self.func(notification)

	def description(self):  # for debugging in Xcode
		desc = super(callbackHelperClass, self).description()
		return "%s %s" % (desc, str(self.func))

def __addCallback__(self, target=None, operation=None, callbackType=None, callee=None, selector=None):
	if callbackType is None:
		__addCallback__Old__(self, target, operation)
		return

	if not isinstance(callee, NSObject):
		raise TypeError("Target must be a subclass of NSObject, not %s" % type(callee).__name__)

	if callbackType in DrawLayerCallbacks or callbackType == CONTEXTMENUCALLBACK:

		# Add to stack
		GSCallbackHandler.addCallback_forOperation_(callee, callbackType)

		# Redraw immediately
		self.redraw()

	elif callbackType in Observers:
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(callee, selector, callbackType, objc.nil)

def __addCallback__Old__(self, target, operation):
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
		elif operation == CONTEXTMENUCALLBACK:
			if isinstance(target, objc.Class):
				GSCallbackHandler.addCallback_forOperation_(target, operation)
			else:
				raise TypeError("Target must be a (objc) class, not %s" % type(target).__name__)
		# Other observers
		elif operation in Observers:
			# Add class to callbackTargets dict by the function name
			callbackTargets[targetName] = callbackHelperClass(target, operation)
			selector = objc.selector(callbackTargets[targetName].callback_, signature=b"v@:@")
			NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(callbackTargets[targetName], selector, operation, objc.nil)
	except:
		NSLog(traceback.format_exc())

GSApplication.addCallback = python_method(__addCallback__)

'''
	.. function:: addCallback(function, hook)

		Add a user-defined function to the glyph window’s drawing operations, in the foreground and background for the active glyph as well as in the inactive glyphs.

		The function names are used to add/remove the functions to the hooks, so make sure to use unique function names.

		Your function needs to accept two values: `layer` which will contain the respective :class:`GSLayer` object of the layer we’re dealing with and `info` which is a dictionary and contains the value `Scale` (for the moment).

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

def __do__removeCallback__(self, target, operation):

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

def __removeCallback__(self, target=None, operation=None, callbackType=None, callee=None):
	if callee is None:
		if operation is not None:
			__do__removeCallback__(self, target, operation)
		else:
			for operation in callbackOperationTargets.keys():
				__do__removeCallback__(self, target, operation)
		return

	if callbackType is None:
		raise ValueError("You need to supply the callbackType to remove it")

	if callbackType in DrawLayerCallbacks or callbackType == CONTEXTMENUCALLBACK:

		GSCallbackHandler.removeCallback_forOperation_(callee, callbackType)

		# Redraw immediately
		self.redraw()

	elif callbackType in Observers:
		NSNotificationCenter.defaultCenter().removeObserver_(callee)

GSApplication.removeCallback = python_method(__removeCallback__)

'''
	.. function:: removeCallback(function)

		Remove the function you’ve previously added.

		.. code-block:: python
			# remove your function to the hook
			Glyphs.removeCallback(drawGlyphIntoBackground)
'''

##########################################################################################################
#
#
#           // end of Callback section
#
#
##########################################################################################################



def __redraw__(self):
	NSNotificationCenter.defaultCenter().postNotificationName_object_("GSRedrawEditView", None)
GSApplication.redraw = python_method(__redraw__)

'''
	.. function:: redraw()

		Redraws all Edit views and Preview views.
'''

def Glyphs_showNotification(self, title, message):
	notification = NSUserNotification.alloc().init()
	notification.setTitle_(title)
	notification.setInformativeText_(message)
	NSUserNotificationCenter.defaultUserNotificationCenter().deliverNotification_(notification)

GSApplication.showNotification = python_method(Glyphs_showNotification)

'''
	.. function:: showNotification(title, message)

		Shows the user a notification in Mac’s Notification Center.

		.. code-block:: python
			Glyphs.showNotification('Export fonts', 'The export of the fonts was successful.')
'''

def Glyphs_localize(self, localization):
	if isString(localization):
		return localization
	elif isinstance(localization, dict):
		# Return first match of languages list
		for language in self.defaults["AppleLanguages"]:
			if language in localization:
				return localization[language]
			while "-" in language:
				language = "-".join(language.split("-")[0:-1])
				if language in localization:
					return localization[language]
		language = localization.get("en", None)  # first look if there is a english entry.
		if language is not None:
			return language
		# None found, return first item in localization dict
		return localization[localization.keys()[0]]

GSApplication.localize = python_method(Glyphs_localize)

'''
	.. function:: localize(localization)

		Return a string in the language of Glyphs.app’s UI locale, which must be supplied as a dictionary using language codes as keys.

		The argument is a dictionary in the `languageCode: translatedString` format.

		You don’t need to supply strings in all languages that the Glyphs.app UI supports. A subset will do. Just make sure that you add at least an English string to default to next to all your other translated strings. Also don’t forget to mark strings as unicode strings (:samp:`'öäüß'`) when they contain non-ASCII content for proper encoding, and add a `# encoding: utf-8` to the top of all your .py files.

		Tip: You can find Glyphs’ localized languages here :samp:`Glyphs.defaults["AppleLanguages"]`.

		.. code-block:: python
			print(Glyphs.localize({
				'en': 'Hello World',
				'de': 'Hallöle Welt',
				'fr': 'Bonjour tout le monde',
				'es': 'Hola Mundo',
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

GSApplication.activateReporter = python_method(__GSApplication_activateReporter__)

'''
	.. function:: activateReporter(reporter)

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

GSApplication.deactivateReporter = python_method(__GSApplication_deactivateReporter__)

'''
	.. function:: deactivateReporter(reporter)

		Deactivate a reporter plug-in by its object (see Glyphs.reporters) or class name.

		.. code-block:: python
			Glyphs.deactivateReporter('GlyphsMasterCompatibility')
'''

GSDocument.__new__ = staticmethod(GSObject__new__)
GSDocument.__new__.__name__ = "__new__"
GSProjectDocument.__new__ = staticmethod(GSObject__new__)
GSProjectDocument.__new__.__name__ = "__new__"

GSElement.x = property(lambda self: self.pyobjc_instanceMethods.position().x,
					   lambda self, value: self.setPosition_(NSMakePoint(validateNumber(value), self.y)))

GSElement.y = property(lambda self: self.pyobjc_instanceMethods.position().y,
					   lambda self, value: self.setPosition_(NSMakePoint(self.x, validateNumber(value))))

GSElement.layer = property(lambda self: self.pyobjc_instanceMethods.layer())
GSElement.glyph = property(lambda self: self.pyobjc_instanceMethods.glyph())
GSElement.__new__ = staticmethod(GSObject__new__)
GSElement.__new__.__name__ = "__new__"


def _______________(): pass
def ____PROXIES____(): pass
def _______________(): pass


class AppDocumentProxy(Proxy):
	"""The list of documents."""
	def __getitem__(self, key):
		return self.values().__getitem__(key)
	def append(self, doc):
		NSDocumentController.sharedDocumentController().addDocument_(doc)
		doc.makeWindowControllers()
		doc.showWindows()
	def values(self):
		return self._owner.fontDocuments()

class AppFontProxy(Proxy):
	"""The list of fonts."""
	def __getitem__(self, key):
		return self.values().__getitem__(key)
	def values(self):
		fonts = []
		for doc in self._owner.fontDocuments():
			fonts.append(doc.font)
		return fonts
	def append(self, font):
		doc = Glyphs.documentController().openUntitledDocumentAndDisplay_error_(True, None)[0]
		doc.setFont_(font)

'''
:mod:`GSDocument`
===============================================================================

The document class

.. class:: GSDocument()

	Properties

	.. autosummary::

		font
		filePath

	**Properties**
'''

GSDocument.font = property(lambda self: self.pyobjc_instanceMethods.font(),
						   lambda self, value: self.setFont_(value),
						   doc="")
'''
	.. attribute:: font
		The active :class:`GSFont`

		:type: GSFont
'''

def __GSDocument_filePath__(self):
	url = self.fileURL()
	if url is not None:
		return url.path()
	return None
GSDocument.filePath = property(lambda self: __GSDocument_filePath__(self))

'''
	.. attribute:: filePath
		The last save location

		:type: str
'''

class FontGlyphsProxy(Proxy):
	"""The list of glyphs. You can access it with the idx or the glyph name.
	Usage:
		Font.glyphs[idx]
		Font.glyphs[name]
		for glyph in Font.glyphs:
		...
	"""
	def __getitem__(self, key):
		if isinstance(key, slice):
			return self.values().__getitem__(key)
		# by idx
		if isinstance(key, int):
			idx = self._validate_idx(key)
			return self._owner.glyphAtIndex_(idx)
		if isString(key):
			# by glyph name
			if self._owner.glyphForName_(key):
				return self._owner.glyphForName_(key)
			# by string representation as 'ä'
			elif len(key) == 1 and self._owner.glyphForCharacter_(ord(key)):
				return self._owner.glyphForCharacter_(ord(key))
			# by unicode
			return self._owner.glyphForUnicode_(key.upper())
		raise TypeError("key for glyphs must be int or str, not %s" % type(key).__name__)
	def __setitem__(self, key, glyph):
		if not isinstance(glyph, GSGlyph):
			raise TypeError("Cannot add %s, not a Glyph" % glyph)
		if isinstance(key, int):
			idx = self._validate_idx(key)
			self._owner.removeGlyph_(self._owner.glyphAtIndex_(idx))
			self._owner.addGlyph_(glyph)
		elif isString(key):
			self._owner.removeGlyph_(self._owner.glyphForName_(key))
			
			if isinstance(glyph, GSLayer): # hack for fontParts
				_glyph = GSGlyph()
				_glyph.name = key
				glyph.setLayerId_(self._owner.masters[0].id)
				_glyph.layers[self._owner.masters[0].id] = glyph
				glyph = _glyph
			if glyph.name != key:
				glyph.name = key
			self._owner.addGlyph_(glyph)
		else:
			raise TypeError("key for glyphs must be int or str, not %s" % type(key).__name__)
	def __delitem__(self, key):
		if isinstance(key, slice):
			for i in sorted(range(*key.indices(self.__len__())), reverse=True):
				self.__delitem__(i)
			return
		elif isinstance(key, int):
			idx = self._validate_idx(key)
			self._owner.removeGlyph_(self._owner.glyphAtIndex_(idx))
		elif isString(key):
			self._owner.removeGlyph_(self._owner.glyphForName_(key))
		else:
			raise TypeError("key for glyphs must be int or str, not %s" % type(key).__name__)
	def __contains__(self, item):
		if isString(item):
			return self._owner.glyphForName_(item) is not None
		return self._owner.indexOfGlyph_(item) < NSNotFound  # indexOfGlyph_ returns NSNotFound which is some very big number
	def keys(self):
		return self._owner.pyobjc_instanceMethods.glyphs().valueForKeyPath_("@unionOfObjects.name")
	def values(self):
		return self._owner.pyobjc_instanceMethods.glyphs()
	def items(self):
		for value in self._owner.pyobjc_instanceMethods.glyphs():
			key = value.name
			yield (key, value)
	def append(self, Glyph):
		if not isinstance(Glyph, GSGlyph):
			raise TypeError("Cannot add %s, not a Glyph" % Glyph)
		if Glyph.name not in self:
			self._owner.addGlyph_(Glyph)
		else:
			raise NameError('There is a glyph with the name \"%s\" already in the font.' % Glyph.name)
	def extend(self, objects):
		for glyph in objects:
			if not isinstance(glyph, GSGlyph):
				raise TypeError("Cannot add %s, not a Glyph" % glyph)
			if glyph.name in self:
				raise NameError('There is a glyph with the name \"%s\" already in the font.' % Glyph.name)
		self._owner.addGlyphsFromArray_(list(objects))
	def __len__(self):
		return self._owner.count()
	def setterMethod(self):
		return self._owner.setGlyphs_


class FontFontMasterProxy(Proxy):
	def __getitem__(self, key):
		if isinstance(key, slice):
			return self.values().__getitem__(key)
		elif isinstance(key, int):
			idx = self._validate_idx(key)
			return self._owner.fontMasterAtIndex_(idx)
		elif isString(key):
			return self._owner.fontMasterForId_(key)
		raise TypeError("need int or str, got: %s" % type(key).__name__)
	def __setitem__(self, key, FontMaster):
		if not isinstance(FontMaster, GSFontMaster):
			raise TypeError("Cannot add %s, not a FontMaster" % FontMaster)
		if isinstance(key, int):
			idx = self._validate_idx(key)
			self._owner.replaceFontMasterAtIndex_withFontMaster_(idx, FontMaster)
		elif isString(key):
			OldFontMaster = self._owner.fontMasterForId_(key)
			self._owner.removeFontMaster_(OldFontMaster)
			return self._owner.addFontMaster_(FontMaster)
		else:
			raise TypeError("need int or str, got: %s" % type(key).__name__)
	def __delitem__(self, key):
		if isinstance(key, slice):
			for i in sorted(range(*key.indices(self.__len__())), reverse=True):
				self.__delitem__(i)
			return
		elif isinstance(key, int):
			idx = self._validate_idx(key)
			removeFontMaster = self._owner.objectInFontMastersAtIndex_(idx)
		elif isString(key):
			removeFontMaster = self._owner.fontMasterForId_(key)
		else:
			raise TypeError("need int or str, got: %s" % type(key).__name__)
		if removeFontMaster:
			return self._owner.removeFontMasterAndContent_(removeFontMaster)
	def __iter__(self):
		for idx in range(self._owner.countOfFontMasters()):
			yield self._owner.fontMasterAtIndex_(idx)
	def __len__(self):
		return self._owner.countOfFontMasters()
	def values(self):
		return self._owner.pyobjc_instanceMethods.fontMasters()
	def setterMethod(self):
		return self._owner.setFontMasters_
	def append(self, FontMaster):
		if not isinstance(FontMaster, GSFontMaster):
			raise TypeError("Cannot add %s, not a FontMaster" % FontMaster)
		self._owner.addFontMaster_(FontMaster)
	def remove(self, FontMaster):
		self._owner.removeFontMasterAndContent_(FontMaster)
	def insert(self, idx, FontMaster):
		if not isinstance(FontMaster, GSFontMaster):
			raise TypeError("Cannot add %s, not a FontMaster" % FontMaster)
		if isinstance(idx, int):
			idx = self._validate_idx(idx, offset=1)
			self._owner.insertFontMaster_atIndex_(FontMaster, idx)
		else:
			raise TypeError("index must be integer, got: %s" % type(key).__name__)


class FontInstancesProxy(Proxy):
	def __getitem__(self, idx):
		if isinstance(idx, slice):
			return self.values().__getitem__(idx)
		if isinstance(idx, int):
			idx = self._validate_idx(idx)
			return self._owner.objectInInstancesAtIndex_(idx)
		raise TypeError("list indices must be integers or slices, not %s" % type(idx).__name__)
	def __setitem__(self, idx, Class):
		if isinstance(idx, int):
			idx = self._validate_idx(idx)
			self._owner.replaceObjectInInstancesAtIndex_withObject_(idx, Class)
		else:
			raise TypeError("list indices must be integers, not %s" % type(idx).__name__)
	def removeItemAtIndexMethod(self):
		return self._owner.removeObjectFromInstancesAtIndex_
	def __iter__(self):
		for idx in range(self._owner.countOfInstances()):
			yield self._owner.objectInInstancesAtIndex_(idx)
	def append(self, instance):
		self._owner.addInstance_(instance)
	def extend(self, instances):
		for instance in instances:
			self._owner.addInstance_(instance)
	def remove(self, instance):
		self._owner.removeInstance_(instance)
	def insert(self, idx, instance):
		if isinstance(idx, int):
			idx = self._validate_idx(idx, offset=1)
			self._owner.insertObject_inInstancesAtIndex_(instance, idx)
		else:
			raise TypeError("list indices must be integers, not %s" % type(idx).__name__)
	def __len__(self):
		return self._owner.countOfInstances()
	def values(self):
		return self._owner.pyobjc_instanceMethods.instances()
	def setterMethod(self):
		return self._owner.setInstances_

class FontAxesProxy(Proxy):
	def __getitem__(self, idx):
		if isinstance(idx, slice):
			return self.values().__getitem__(idx)
		if isinstance(idx, int):
			idx = self._validate_idx(idx)
			return self._owner.objectInAxesAtIndex_(idx)
		raise TypeError("list indices must be integers or slices, not %s" % type(idx).__name__)
	def __setitem__(self, idx, Class):
		if isinstance(idx, int):
			idx = self._validate_idx(idx)
			self._owner.replaceObjectInAxesAtIndex_withObject_(idx, Class)
		else:
			raise TypeError("list indices must be integers, not %s" % type(idx).__name__)
	def removeItemAtIndexMethod(self):
		return self._owner.removeObjectFromAxesAtIndex_
	def __iter__(self):
		for idx in range(self._owner.countOfAxes()):
			yield self._owner.objectInAxesAtIndex_(idx)
	def append(self, axis):
		self._owner.addAxis_(axis)
	def extend(self, axes):
		for axis in axes:
			self._owner.addAxis_(axis)
	def remove(self, axis):
		self._owner.removeObjectFromAxes_(axis)
	def insert(self, idx, axis):
		if isinstance(idx, int):
			idx = self._validate_idx(idx, offset=1)
			self._owner.insertObject_inAxesAtIndex_(axis, idx)
		else:
			raise TypeError("list indices must be integers, not %s" % type(idx).__name__)
	def __len__(self):
		return self._owner.countOfAxes()
	def values(self):
		return self._owner.pyobjc_instanceMethods.axes()
	def setterMethod(self):
		return self._owner.setAxes_

class MasterAxesProxy(Proxy):
	def __getitem__(self, idx):
		if isinstance(idx, slice):
			return self.values().__getitem__(idx)
		elif isinstance(idx, int):
			idx = self._validate_idx(idx)
			axis = self._owner.font.axes[idx]
			if axis is None:
				return None
			return self._owner.axisValueValueForId_(axis.axisId)
		raise TypeError("list indices must be integers or slices, not %s" % type(idx).__name__)
	def __setitem__(self, idx, value):
		if isinstance(idx, int):
			idx = self._validate_idx(idx)
			count = self.__len__()
			axis = self._owner.font.axes[idx]
			return self._owner.setAxisValueValue_forId_(value, axis.axisId)
		raise TypeError("list indices must be integers or slices, not %s" % type(idx).__name__)
	def values(self):
		if self._owner.font is None:
			return []
		axisValues = GSFont.axesPositionsFromAxes_master_(self._owner.font.pyobjc_instanceMethods.axes(), self._owner)
		values = []
		for axisValue in axisValues:
			values.append(axisValue.position)
		return values
	def __len__(self):
		if self._owner.font is None:
			return 0
		return self._owner.font.countOfAxes()
	def _setterMethod(self, values):
		idx = 0
		if self._owner.font is None:
			return
		for axis in self._owner.font.axes:
			self._owner.setAxisValueValue_forId_(values[idx], axis.axisId)
			idx += 1
	def setterMethod(self):
		return self._setterMethod

class FontStemsProxy(Proxy):
	def _stemForKey(self, key):
		stem = None
		if isinstance(key, int):
			idx = self._validate_idx(key)
			stem = self._owner.objectInStemsAtIndex_(key)
		elif isString(key):
			stem = self._owner.stemForName_(key)
		else:
			raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
		if stem is None:
			raise KeyError("No stem for key %s" % key)
		return stem
	def __getitem__(self, key):
		if isinstance(key, slice):
			return [self.__getitem__(i) for i in range(*key.indices(self.__len__()))]
		return self._stemForKey(key)
	def __setitem__(self, key, value):
		if not isinstance(value, GSMetrics):
			raise TypeError("only object of type GSMetrics allowed, got %s" % type(value).__name__)
		if not isinstance(key, int):
			raise TypeError("only accessible by integer index, got %s" % key)
		idx = self._validate_idx(key)
		self._owner.insertObject_inStemsAtIndex_(value, idx)
	def values(self):
		return self._owner.pyobjc_instanceMethods.stems()
	def __len__(self):
		return self._owner.countOfStems()
	def append(self, value):
		if not isinstance(value, GSMetrics):
			raise TypeError("only object of type GSMetrics allowed, got %s" % type(value).__name__)
		self._owner.addStem_(value)
	def __delitem__(self, key):
		if isinstance(key, slice):
			for i in sorted(range(*key.indices(self.__len__())), reverse=True):
				self.__delitem__(i)
		else:
			stem = self._stemForKey(key)
			self._owner.removeObjectFromStems_(stem)
	def setterMethod(self):
		return self.setStems_

class MasterStemsProxy(Proxy):
	def _stemForKey(self, key):
		if isinstance(key, int):
			if key < 0:
				key += self.__len__()
			stem = self._owner.font.objectInStemsAtIndex_(key)
		elif isString(key):
			stem = self._owner.font.stemForName_(key)
		else:
			raise TypeError("list indices must be integers or strings, not %s" % type(key).__name__)
		return stem
	def __getitem__(self, key):
		if isinstance(key, slice):
			return [self.__getitem__(i) for i in range(*key.indices(self.__len__()))]
		stem = self._stemForKey(key)
		if stem is None:
			raise KeyError("No stem for %s" % key)
		return self._owner.valueValueForStemId_(stem.id)
	def __setitem__(self, key, value):
		stem = self._stemForKey(key)
		if stem is None:
			if isString(key):
				name = key
			else:
				name = "stem%s" % key
			stem = GSMetric.new()
			stem.setName_(name)
			stem.setHorizontal_(True)
			self._owner.font.addStem_(stem)
		self._owner.setStemValueValue_forId_(value, stem.id)
	def values(self):
		return self._owner.stemValuesArray()
	def __len__(self):
		if self._owner.font is None:
			return 0
		return self._owner.font.countOfStems()
	def _setterMethod(self, values):
		idx = 0
		if self._owner.font is None:
			return
		if self.__len__() != len(values):
			raise ValueError("Count of values doesn’t match stems")
		for stem in self._owner.font.stems:
			self._owner.setStemValueValue_forId_(values[idx], stem.id)
			idx += 1
	def setterMethod(self):
		return self._setterMethod

class CustomParametersProxy(Proxy):
	def __getitem__(self, key):
		if isinstance(key, slice):
			return self.values().__getitem__(key)
		elif isinstance(key, int):
			idx = self._validate_idx(key)
			return self._owner.objectInCustomParametersAtIndex_(idx)
		elif isString(key):
			return self._owner.customValueForKey_(key)
		raise TypeError("key must be integer or string, not %s" % type(key).__name__)
	def __setitem__(self, key, Parameter):
		if isinstance(key, int):
			idx = self._validate_idx(key)
			self._owner.replaceObjectInCustomParametersAtIndex_withObject_(idx, Parameter)
		elif isString(key):
			#TODO: This expects a value in Parameter, not a Parameter object which the list elements are
			self._owner.setCustomValue_forKey_(objcObject(Parameter), objcObject(key))
		else:
			raise TypeError("key must be integer or string, not %s" % type(key).__name__)
	def __delitem__(self, key):
		if isinstance(key, slice):
			for i in sorted(range(*key.indices(self.__len__())), reverse=True):
				self.__delitem__(i)
		elif isinstance(key, int):
			idx = self._validate_idx(key)
			self._owner.removeObjectFromCustomParametersAtIndex_(idx)
		elif isString(key):
			self._owner.removeObjectFromCustomParametersForKey_(key)
		else:
			raise TypeError("key must be integer or string, not %s" % type(key).__name__)
	def __contains__(self, item):
		if isString(item):
			return self._owner.customParameterForKey_(item) is not None
		return self._owner.pyobjc_instanceMethods.customParameters().containsObject_(item)
	def __iter__(self):
		for idx in range(self._owner.countOfCustomParameters()):
			yield self._owner.objectInCustomParametersAtIndex_(idx)
	def append(self, parameter):
		self._owner.addCustomParameter_(parameter)
	def extend(self, parameters):
		for parameter in parameters:
			self._owner.addCustomParameter_(parameter)
	def remove(self, parameter):
		self._owner.removeObjectFromCustomParametersForKey_(parameter.name)
	def insert(self, idx, parameter):
		idx = self._validate_idx(idx, offset=1)
		self._owner.insertObject_inCustomParametersAtIndex_(parameter, idx)
	def __len__(self):
		return self._owner.countOfCustomParameters()
	def values(self):
		return self._owner.pyobjc_instanceMethods.customParameters()
	def setterMethod(self):
		return self._owner.setCustomParameters_


class FontClassesProxy(Proxy):
	def __getitem__(self, key):
		if isinstance(key, slice):
			return self.values().__getitem__(key)
		elif isinstance(key, int):
			idx = self._validate_idx(key)
			return self._owner.objectInClassesAtIndex_(idx)
		elif isString(key):
			if len(key) > 0:
				return self._owner.classForTag_(key)
		raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
	def __setitem__(self, key, Class):
		if isinstance(key, int):
			idx = self._validate_idx(key)
			self._owner.replaceObjectInClassesAtIndex_withObject_(idx, Class)
		else:
			raise TypeError("keys must be integers, not %s" % type(key).__name__)
	def __delitem__(self, key):
		if isinstance(key, slice):
			for i in sorted(range(*key.indices(self.__len__())), reverse=True):
				self.__delitem__(i)
		elif isinstance(key, int):
			idx = self._validate_idx(key)
			return self._owner.removeObjectFromClassesAtIndex_(idx)
		elif isString(key):
			Class = self._owner.classForTag_(key)
			if Class is not None:
				return self._owner.removeClass_(Class)
		else:
			raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
	def __iter__(self):
		for idx in range(self._owner.countOfClasses()):
			yield self._owner.objectInClassesAtIndex_(idx)
	def append(self, Class):
		self._owner.addClass_(Class)
	def extend(self, Classes):
		for Class in Classes:
			self._owner.addClass_(Class)
	def remove(self, Class):
		self._owner.removeClass_(Class)
	def insert(self, idx, Class):
		idx = self._validate_idx(idx, offset=1)
		self._owner.insertObject_inClassesAtIndex_(Class, idx)
	def __len__(self):
		return self._owner.countOfClasses()
	def values(self):
		return self._owner.pyobjc_instanceMethods.classes()
	def setterMethod(self):
		return self._owner.setClasses_


class FontFeaturesProxy(Proxy):
	def __getitem__(self, key):
		if isinstance(key, slice):
			return self.values().__getitem__(key)
		elif isinstance(key, int):
			idx = self._validate_idx(key)
			return self._owner.objectInFeaturesAtIndex_(idx)
		elif isString(key):
			return self._owner.featureForTag_(key)
		raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
	def __setitem__(self, idx, feature):
		idx = self._validate_idx(idx)
		self._owner.replaceObjectInFeaturesAtIndex_withObject_(idx, feature)
	def __delitem__(self, key):
		if isinstance(key, slice):
			for i in sorted(range(*key.indices(self.__len__())), reverse=True):
				self.__delitem__(i)
		elif isinstance(key, int):
			idx = self._validate_idx(key)
			return self._owner.removeObjectFromFeaturesAtIndex_(idx)
		elif isString(key):
			Feature = self._owner.featureForTag_(key)
			if Feature is not None:
				return self._owner.removeFeature_(Feature)
		else:
			raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
	def __iter__(self):
		for idx in range(self._owner.countOfFeatures()):
			yield self._owner.objectInFeaturesAtIndex_(idx)
	def append(self, feature):
		self._owner.addFeature_(feature)
	def extend(self, features):
		for feature in features:
			self._owner.addFeature_(feature)
	def remove(self, Class):
		self._owner.removeFeature_(Class)
	def insert(self, idx, Class):
		idx = self._validate_idx(idx, offset=1)
		self._owner.insertObject_inFeaturesAtIndex_(Class, idx)
	def __len__(self):
		return self._owner.countOfFeatures()
	def text(self):
		text = ""
		for Feature in self._owner.pyobjc_instanceMethods.features():
			text += "feature "
			text += Feature.name
			text += " {\n"
			text += "    " + Feature.code
			text += "\n} "
			text += Feature.name
			text += " ;\n"
		return text
	def values(self):
		return self._owner.pyobjc_instanceMethods.features()
	def setterMethod(self):
		return self._owner.setFeatures_


class FontFeaturePrefixesProxy(Proxy):
	def __getitem__(self, key):
		if isinstance(key, slice):
			return self.values().__getitem__(key)
		elif isinstance(key, int):
			idx = self._validate_idx(key)
			return self._owner.objectInFeaturePrefixesAtIndex_(idx)
		elif isString(key):
			return self._owner.featurePrefixForTag_(key)
		raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
	def __setitem__(self, idx, featurePrefix):
		if isinstance(idx, int):
			idx = self._validate_idx(idx)
			self._owner.replaceObjectInFeaturePrefixesAtIndex_withObject_(idx, featurePrefix)
		else:
			raise TypeError("keys must be integers, not %s" % type(idx).__name__)
	def __delitem__(self, key):
		if isinstance(key, slice):
			for i in sorted(range(*key.indices(self.__len__())), reverse=True):
				self.__delitem__(i)
		elif isinstance(key, int):
			idx = self._validate_idx(key)
			return self._owner.removeObjectFromFeaturePrefixesAtIndex_(idx)
		elif isString(key):
			featurePrefix = self._owner.featurePrefixForTag_(key)
			if featurePrefix is not None:
				return self._owner.removeFeaturePrefix_(featurePrefix)
		else:
			raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
	def append(self, featurePrefix):
		self._owner.addFeaturePrefix_(featurePrefix)
	def extend(self, FeaturePrefixes):
		for featurePrefix in FeaturePrefixes:
			self._owner.addFeaturePrefix_(featurePrefix)
	def remove(self, featurePrefix):
		self._owner.removeFeaturePrefix_(featurePrefix)
	def insert(self, idx, featurePrefix):
		idx = self._validate_idx(idx, offset=1)
		self._owner.insertObject_inFeaturePrefixesAtIndex_(featurePrefix, idx)
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
	def __getitem__(self, key):
		return self._owner.userDataForKey_(key)
	def __setitem__(self, key, Value):
		self._owner.setUserData_forKey_(objcObject(Value), key)
	def __delitem__(self, key):
		self._owner.removeUserDataForKey_(key)
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
		return self._owner.userDataForKey_(item) is not None
	def get(self, key, default=None):
		value = self.__getitem__(key)
		if value is None:
			return default
		return value
	def __copy__(self):
		return self._owner.pyobjc_instanceMethods.userData().copy()
	def __deepcopy__(self, memo):
		return self._owner.pyobjc_instanceMethods.userData().deepMutableCopy()


class TempDataProxy(Proxy):
	def __getitem__(self, key):
		return self._owner.tempDataForKey_(key)
	def __setitem__(self, key, Value):
		self._owner.setTempData_forKey_(objcObject(Value), key)
	def __delitem__(self, key):
		self._owner.setTempData_forKey_(None, key)
	def values(self):
		tempData = self._owner.pyobjc_instanceMethods.tempData()
		if tempData is not None:
			return tempData.allValues()
		return None
	def keys(self):
		tempData = self._owner.pyobjc_instanceMethods.tempData()
		if tempData is not None:
			return tempData.allKeys()
		return None
	def __repr__(self):
		return self._owner.pyobjc_instanceMethods.tempData().__repr__()
	def __contains__(self, item):
		return self._owner.tempDataForKey_(item) is not None
	def get(self, key, default=None):
		value = self.__getitem__(key)
		if value is None:
			return default
		return value
	def __copy__(self):
		return self._owner.pyobjc_instanceMethods.tempData().copy()
	def __deepcopy__(self, memo):
		return self._owner.pyobjc_instanceMethods.tempData().deepMutableCopy()


class AttributesProxy(Proxy):
	def __getitem__(self, key):
		if not isString(key):
			raise TypeError("keys must be strings, not %s" % type(key).__name__)
		return self._owner.attributeForKey_(key)
	def __setitem__(self, key, value):
		if not isString(key):
			raise TypeError("keys must be strings, not %s" % type(key).__name__)
		if value is None:
			self._owner.removeAttributeForKey_(objcObject(key))
		else:
			self._owner.setAttribute_forKey_(objcObject(value), objcObject(key))
	def __delitem__(self, key):
		if not isString(key):
			raise TypeError("keys must be strings, not %s" % type(key).__name__)
		self._owner.setAttribute_forKey_(None, key)
	def values(self):
		attribute = self._owner.pyobjc_instanceMethods.attributes()
		if attribute is not None:
			return attribute.allValues()
		return None
	def keys(self):
		attribute = self._owner.pyobjc_instanceMethods.attributes()
		if attribute is not None:
			return attribute.allKeys()
		return None
	def __repr__(self):
		return repr(self._owner.pyobjc_instanceMethods.attributes())
	def __contains__(self, item):
		return self._owner.pyobjc_instanceMethods.attributeForKey_(item) is not None
	def get(self, key, default=None):
		value = self.__getitem__(key)
		if value is None:
			return default
		return value
	def __copy__(self):
		return self._owner.pyobjc_instanceMethods.attributes().copy()
	def __deepcopy__(self, memo):
		return self._owner.pyobjc_instanceMethods.attributes().deepMutableCopy()


class FontInfoPropertiesProxy(Proxy):
	def __init__(self, owner, propertyKey):
		self._owner = owner
		self._propertyKey = propertyKey
	
	def __getitem__(self, languageKey):
		if not isString(languageKey):
			raise TypeError("keys must be strings, not %s" % type(languageKey).__name__)
		return self._owner.propertyForName_languageTag_(self._propertyKey, languageKey)
	
	def __setitem__(self, languageKey, value):
		if not isString(languageKey):
			raise TypeError("keys must be strings, not %s" % type(languageKey).__name__)
		self._owner.setProperty_value_languageTag_(self._propertyKey, objcObject(value), objcObject(languageKey))
	
	def __delitem__(self, languageKey):
		if not isString(languageKey):
			raise TypeError("keys must be strings, not %s" % type(languageKey).__name__)
		self._owner.removeObject_fromPropertyWithKey_(
			self._owner.propertyForName_languageTag_(self._propertyKey, languageKey),
			self._propertyKey
			)
	
	def values(self):
		_property = self._owner.propertyForName_(self._propertyKey)
		if _property is not None:
			return [value.value for value in _property.values]
		return None
	
	def keys(self):
		_property = self._owner.propertyForName_(self._propertyKey)
		if _property is not None:
			return [value.languageTag for value in _property.values]
		return None	
	
	def __repr__(self):
		_property = self._owner.propertyForName_(self._propertyKey)
		if _property is None:
			return None.__repr__()
		reprValue = "".join([f'\t{value.languageTag}, {value.value}\n' for value in _property.values])
		return f"(\n{reprValue}\n)"
	
	def __contains__(self, item):
		_property = self._owner.propertyForName_(self._propertyKey)
		if _property is not None:
			return item in [value.key for value in _property.values]
		return None
	
	def get(self, key, default=None):
		value = self.__getitem__(key)
		if value is None:
			return default
		return value

class SmartComponentPoleMappingProxy(Proxy):
	def __getitem__(self, key):
		poleMapping = self._owner.partSelection()
		if poleMapping is not None:
			return poleMapping[key]
		return None
	def __setitem__(self, key, Value):
		poleMapping = self._owner.partSelection()
		if poleMapping is None:
			self._owner.setPartSelection_(NSMutableDictionary.dictionaryWithObject_forKey_(objcObject(Value), key))
		else:
			poleMapping[key] = objcObject(Value)
	def __delitem__(self, key):
		poleMapping = self._owner.partSelection()
		if poleMapping is not None:
			del(poleMapping[key])
	def values(self):
		poleMapping = self._owner.partSelection()
		if poleMapping is not None:
			return poleMapping.allValues()
		return None
	def __repr__(self):
		poleMapping = self._owner.partSelection()
		return str(poleMapping)

class SmartComponentValuesProxy(Proxy):
	def __getitem__(self, key):
		pieceSettings = self._owner.pieceSettings()
		if pieceSettings is not None:
			return pieceSettings.objectForKey_(key)
		return None
	def __setitem__(self, key, Value):
		self._owner.setPieceValue_forKey_(float(Value), key)
	def __delitem__(self, key):
		pieceSettings = self._owner.pieceSettings()
		if pieceSettings is not None:
			del(pieceSettings[key])
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
		return self.__next__()
	def __next__(self):
		if self._owner.parent:
			if self.curInd < self._owner.parent.countOfFontMasters():
				FontMaster = self._owner.parent.fontMasterAtIndex_(self.curInd)
				Item = self._owner.layerForId_(FontMaster.id)
			else:
				if self.curInd >= self._owner.countOfLayers():
					raise StopIteration
				ExtraLayerIndex = self.curInd - self._owner.parent.countOfFontMasters()
				idx = 0
				ExtraLayer = None
				while ExtraLayerIndex >= 0:
					ExtraLayer = self._owner.objectInLayersAtIndex_(idx)
					if ExtraLayer.layerId != ExtraLayer.associatedMasterId:
						ExtraLayerIndex -= 1
					idx += 1
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

class GlyphLayerProxy(Proxy):
	def __getitem__(self, key):
		if isinstance(key, slice):
			return self.values().__getitem__(key)
		elif isinstance(key, int):
			if self._owner.parent:
				count = max(self._owner.countOfLayers(), self._owner.parent.countOfFontMasters())
				if key < 0:
					key += count
				if key >= count:
					raise IndexError("list index %s out of range %s" % (key, count))
				if key < self._owner.parent.countOfFontMasters():
					FontMaster = self._owner.parent.fontMasterAtIndex_(key)
					return self._owner.layerForId_(FontMaster.id)
				else:
					ExtraLayerIndex = key - len(self._owner.parent.masters)
					idx = 0
					ExtraLayer = None
					while ExtraLayerIndex >= 0:
						ExtraLayer = self._owner.objectInLayersAtIndex_(idx)
						if not ExtraLayer.isMasterLayer:
							ExtraLayerIndex -= 1
						idx += 1
					return ExtraLayer
			else:
				key = self._validate_idx(key)
				return self._owner.objectInLayersAtIndex_(key)
		elif isString(key):
			layer = self._owner.layerForId_(key)
			if layer is None:
				layer = self._owner.layerForName_(key)
			return layer
		else:
			raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
	def __setitem__(self, key, Layer):
		if isinstance(key, int) and self._owner.parent:
			idx = self._validate_idx(key)
			FontMaster = self._owner.parent.fontMasterAtIndex_(idx)
			key = FontMaster.id
		if not isString(key):
			raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
		return self._owner.setLayer_forId_(Layer, key)

	def __delitem__(self, key):
		if isinstance(key, slice):
			for i in sorted(range(*key.indices(self.__len__())), reverse=True):
				self.__delitem__(i)
			return
		elif isinstance(key, int) and self._owner.parent:
			idx = self._validate_idx(key)
			Layer = self.__getitem__(idx)
			key = Layer.layerId
		elif not isString(key):
			raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
		return self._owner.removeLayerForId_(key)

	def __iter__(self):
		return LayersIterator(self._owner)
	def __len__(self):
		return self._owner.countOfLayers()
	def values(self):
		return self._owner.pyobjc_instanceMethods.layers().allValues()
	def append(self, Layer):
		if not Layer.associatedMasterId:
			Layer.associatedMasterId = self._owner.parent.masters[0].id
		self._owner.setLayer_forId_(Layer, NSString.UUID())
	def remove(self, Layer):
		return self._owner.removeLayerForId_(Layer.layerId)
	def insert(self, idx, Layer):
		idx = self._validate_idx(idx, offset=1)
		self.append(Layer)
	def setter(self, values):
		newLayers = NSMutableDictionary.dictionary()
		if isinstance(values, (list, tuple, type(self))):
			for layer in values:
				newLayers[layer.layerId] = layer
		elif isinstance(values, (dict, NSDictionary)):
			for (key, layer) in values.items():
				layer.layerId = key
				newLayers[key] = layer
		else:
			raise TypeError
		self._owner.setLayers_(newLayers)

class GlyphSmartComponentAxesProxy(Proxy):
	def __getitem__(self, key):
		if isinstance(key, slice):
			return self.values().__getitem__(key)
		elif isinstance(key, int):
			idx = self._validate_idx(key)
			return self._owner.objectInPartsSettingsAtIndex_(idx)
		elif isString(key):
			for partSetting in self._owner.partsSettings():
				if partSetting.name == key:
					return partSetting
			raise KeyError("no value for key: %s" % key)
		else:
			raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
	def __setitem__(self, key, SmartComponentProperty):
		if isinstance(key, int):
			idx = self._validate_idx(key)
			self._owner.replaceObjectInPartsSettingsAtIndex_withObject_(idx, SmartComponentProperty)
		#elif isString(key): # TODO implement setting by name
		#	for partSetting in self._owner.partsSettings():
		#		if partSetting.name == key:
		else:
			#raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
			raise TypeError("keys must be integers, not %s" % type(key).__name__)
	def __delitem__(self, key):
		if isinstance(key, slice):
			for i in sorted(range(*key.indices(self.__len__())), reverse=True):
				self.__delitem__(i)
		elif isinstance(key, int):
			key = self._validate_idx(key)
		elif isString(key):
			idx = 0
			for partSetting in self._owner.partsSettings():
				if partSetting.name == key:
					key = idx
					break
				idx += 1
			if isString(key):
				raise KeyError(key)
		else:
			raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
		self._owner.removeObjectFromPartsSettingsAtIndex_(key)
	def append(self, SmartComponentProperty):
		self._owner.addPartsSetting_(SmartComponentProperty)
	def values(self):
		return self._owner.partsSettings()
	def setterMethod(self):
		return self._owner.setPartsSettings_

class LayerGuidesProxy(Proxy):
	def __getitem__(self, idx):
		if isinstance(idx, slice):
			return self.values().__getitem__(idx)
		elif isinstance(idx, int):
			idx = self._validate_idx(idx)
			return self._owner.objectInGuidesAtIndex_(idx)
		raise TypeError("list indices must be integers or slices, not %s" % type(idx).__name__)
	def __setitem__(self, idx, Component):
		idx = self._validate_idx(idx)
		self._owner.replaceObjectInGuidesAtIndex_withObject_(idx, Component)
	def removeItemAtIndexMethod(self):
		return self._owner.removeObjectFromGuidesAtIndex_
	def __copy__(self):
		return [x.copy() for x in self.values()]
	def append(self, Guide):
		self._owner.addGuide_(Guide)
	def extend(self, Guides):
		for Guide in Guides:
			self._owner.addGuide_(Guide)
	def insert(self, idx, guide):
		idx = self._validate_idx(idx, offset=1)
		self._owner.insertObject_inGuidesAtIndex_(guide, idx)
	def remove(self, Guide):
		self._owner.removeObjectFromGuides_(Guide)
	def values(self):
		return self._owner.pyobjc_instanceMethods.guides()
	def setterMethod(self):
		return self._owner.setGuides_

class LayerAnnotationProxy(Proxy):
	def __getitem__(self, idx):
		if isinstance(idx, slice):
			return self.values().__getitem__(idx)
		elif isinstance(idx, int):
			idx = self._validate_idx(idx)
			return self._owner.objectInAnnotationsAtIndex_(idx)
		raise TypeError("list indices must be integers or slices, not %s" % type(idx).__name__)
	def __setitem__(self, idx, Annotation):
		idx = self._validate_idx(idx)
		self._owner.replaceObjectInAnnotationsAtIndex_withObject_(idx, Annotation)
	def removeItemAtIndexMethod(self):
		return self._owner.removeObjectFromAnnotationsAtIndex_
	def append(self, Annotation):
		self._owner.addAnnotation_(Annotation)
	def extend(self, Annotations):
		for Annotation in Annotations:
			self._owner.addAnnotation_(Annotation)
	def insert(self, idx, Annotation):
		annotations = self.values()
		annotations.insert(idx, Annotation)
		self._owner.setAnnotations_(annotations)
	def remove(self, Annotation):
		self._owner.removeAnnotation_(Annotation)
	def values(self):
		return self._owner.pyobjc_instanceMethods.annotations()
	def setterMethod(self):
		return self._owner.setAnnotations_

class LayerHintsProxy(Proxy):
	def __getitem__(self, idx):
		if isinstance(idx, slice):
			return self.values().__getitem__(idx)
		elif isinstance(idx, int):
			idx = self._validate_idx(idx)
			return self._owner.objectInHintsAtIndex_(idx)
		raise TypeError("list indices must be integers or slices, not %s" % type(idx).__name__)
	def __setitem__(self, idx, hint):
		idx = self._validate_idx(idx)
		self._owner.replaceObjectInHintsAtIndex_withObject_(idx, hint)
	def removeItemAtIndexMethod(self):
		return self._owner.removeObjectFromHintsAtIndex_
	def append(self, hint):
		self._owner.addHint_(hint)
	def extend(self, hints):
		for hint in hints:
			self._owner.addHint_(hint)
	def insert(self, idx, hint):
		idx = self._validate_idx(idx, offset=1)
		self._owner.insertObject_inHintsAtIndex_(hint, idx)
	def remove(self, Hint):
		self._owner.removeHint_(Hint)
	def values(self):
		return self._owner.pyobjc_instanceMethods.hints()
	def setterMethod(self):
		return self._owner.setHints_

class LayerAnchorsProxy(Proxy):
	"""layer.anchors is a dict!!!"""
	def __getitem__(self, key):
		if isString(key):
			return self._owner.anchorForName_(key)
		if isinstance(key, int):
			anchor = self._owner.objectInAnchorsAtIndex_(key)
			if anchor is not None:
				return anchor
			else:
				raise IndexError("anchor index out of range")
		else:
			raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
	def __setitem__(self, key, Anchor):
		if isString(key):
			Anchor.setName_(key)
			self._owner.addAnchor_(Anchor)
		else:
			raise TypeError("keys must be strings, not %s" % type(key).__name__)
	def __delitem__(self, key):
		anchor = self.__getitem__(key)
		if anchor is not None:
			self._owner.removeAnchor_(anchor)
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
	def insert(self, idx, Anchor):
		self.append(Anchor)
	def __len__(self):
		return self._owner.countOfAnchors()

	def setter(self, values):
		newAnchors = NSMutableDictionary.dictionary()

		if isinstance(values, (list, tuple, NSArray)):
			for anchor in values:
				newAnchors[anchor.name] = anchor
		elif isinstance(values, (NSDictionary, dict)):
			for (key, anchor) in values.items():
				newAnchors[anchor.name] = anchor
		elif values is None:
			pass
		elif isinstance(values, type(self)):
			for anchor in values.values():
				newAnchors[anchor.name] = anchor
		else:
			raise TypeError
		self._owner.setAnchors_(newAnchors)

class LayerShapesProxy(Proxy):
	def __getitem__(self, idx):
		if isinstance(idx, slice):
			return self.values().__getitem__(idx)
		elif isinstance(idx, int):
			idx = self._validate_idx(idx)
			return self._owner.objectInShapesAtIndex_(idx)
		else:
			raise TypeError("list indices must be integers or slices, not %s" % type(idx).__name__)
	def __setitem__(self, idx, Shape):
		idx = self._validate_idx(idx)
		self._owner.replaceShapeAtIndex_withShape_(idx, Shape)
	def __len__(self):
		return self._owner.countOfShapes()
	def removeItemAtIndexMethod(self):
		return self._owner.removeObjectFromShapesAtIndex_
	def __contains__(self, item):
		return self._owner.pyobjc_instanceMethods.shapes().containsObject_(item)
	def append(self, Shape):
		if isinstance(Shape, GSShape):
			self._owner.addShape_(Shape)
		else:
			raise TypeError("only GSShape objects are accepted, not %s" % type(Shape).__name__)
	def extend(self, Shapes):
		if isinstance(Shapes, type(self)):
			for path in Shapes.values():
				self._owner.addShape_(path)
		elif isinstance(Shapes, (list, tuple, NSArray)):
			for Shape in Shapes:
				self.append(Shape)
		else:
			raise TypeError
	def remove(self, Shape):
		self._owner.removeShape_(Shape)
	def insert(self, idx, Shape):
		idx = self._validate_idx(idx, offset=1)
		self._owner.insertObject_inShapesAtIndex_(Shape, idx)
	def values(self):
		return self._owner.pyobjc_instanceMethods.shapes()
	def setterMethod(self):
		return self._owner.setShapes_

# not used
class LayerPathsProxy(Proxy):
	def __getitem__(self, idx):
		raise ValueError
	def __setitem__(self, idx, Path):
		raise ValueError
	def __delitem__(self, idx):
		raise ValueError
	def __contains__(self, item):
		return self._owner.pyobjc_instanceMethods.shapes().containsObject_(item)
	def append(self, Path):
		raise ValueError
	def extend(self, Paths):
		raise ValueError
	def remove(self, Path):
		raise ValueError
	def insert(self, idx, Path):
		raise ValueError
	def values(self):
		return self._owner.pyobjc_instanceMethods.paths()
	def setterMethod(self):
		raise ValueError

class LayerSelectionProxy(Proxy):
	def __getitem__(self, idx):
		if isinstance(idx, slice):
			return self.values().__getitem__(idx)
		elif isinstance(idx, int):
			if  self._owner.countOfSelection() == 0:
				raise IndexError("Nothing selected (%d)" % idx)		
			idx = self._validate_idx(idx)
			return self._owner.pyobjc_instanceMethods.selection().objectAtIndex_(idx)
		else:
			raise TypeError("list indices must be integers or slices, not %s" % type(idx).__name__)
	def __len__(self):
		return self._owner.countOfSelection()
	def values(self):
		return self._owner.pyobjc_instanceMethods.selection().array()
	def __contains__(self, item):
		return self._owner.pyobjc_instanceMethods.selection().containsObject_(item)
	def append(self, object):
		self._owner.addSelection_(object)
	def extend(self, objects):
		self._owner.addObjectsFromArrayToSelection_(list(objects))
	def remove(self, object):
		self._owner.removeObjectFromSelection_(object)
	def insert(self, idx, object):
		self._owner.addSelection_(object)
	def clear(self):
		self._owner.clearSelection()
	def _setSelecetion_(self, selection):
		self.clear()
		if selection is not None:
			self.extend(selection)
	def setterMethod(self):
		return self._setSelecetion_

class PathNodesProxy(Proxy):
	def __getitem__(self, idx):
		if isinstance(idx, slice):
			return self.values().__getitem__(idx)
		elif isinstance(idx, int):
			idx = self._validate_idx(idx)
			return self._owner.nodeAtIndex_(idx)
		else:
			raise TypeError("list indices must be integers or slices, not %s" % type(idx).__name__)
	def __setitem__(self, idx, node):
		idx = self._validate_idx(idx)
		self._owner.replaceObjectInNodesAtIndex_withObject_(idx, node)
	def removeItemAtIndexMethod(self):
		return self._owner.removeObjectFromNodesAtIndex_
	def __len__(self):
		return self._owner.countOfNodes()
	def append(self, node):
		self._owner.addNode_(node)
	def remove(self, node):
		self._owner.removeNode_(node)
	def insert(self, idx, node):
		idx = self._validate_idx(idx, offset=1)
		self._owner.insertNode_atIndex_(node, idx)
	def extend(self, objects):
		self._owner.addNodes_(list(objects))
	def index(self, node):
		idx = self._owner.indexOfNode_(node)
		if idx > 100000:
			raise ValueError("%s is not in list" % node)
		return idx
	def values(self):
		return self._owner.pyobjc_instanceMethods.nodes()
	def __contains__(self, item):
		return self._owner.pyobjc_instanceMethods.nodes().containsObject_(item)
	def setterMethod(self):
		return self._owner.setNodes_

class PathSegmentsProxy(Proxy):
	def __getitem__(self, idx):
		return self.values().__getitem__(idx)
	# def __setitem__(self, idx, node):
	# 	self._owner.replaceObjectInNodesAtIndex_withObject_(idx, node)
	# def __delitem__(self, idx):
	# 	self._owner.removeObjectFromNodesAtIndex_(idx)
	# def append(self, node):
	# 	self._owner.addNode_(node)
	# def remove(self, node):
	# 	self._owner.removeNode_(node)
	# def insert(self, idx, node):
	# 	self._owner.insertNode_atIndex_(node, idx)
	# def extend(self, objects):
	# 	self._owner.addNodes_(list(objects))
	# def index(self, node):
	# 	idx = self._owner.indexOfNode_(node)
	# 	if idx > 100000:
	# 		raise ValueError("%s is not in list" % node)
	# 	return idx
	def values(self):
		return self._owner.pyobjc_instanceMethods.segments()
	def setterMethod(self):
		return self._owner.setSegments_

class FontTabsProxy(Proxy):
	def __getitem__(self, idx):
		if isinstance(idx, slice):
			return self.values().__getitem__(idx)
		if self._owner.parent:
			if isinstance(idx, int):
				idx = self._validate_idx(idx)
				return self._owner.parent.windowController().tabBarControl().tabItemAtIndex_(idx + 1)
			else:
				raise TypeError("list indices must be integers or slices, not %s" % type(idx).__name__)
		else:
			raise Exception("The font is not connected to a document object")
	def __setitem__(self, idx, Tab):
		if isinstance(idx, int):
			raise(NotImplementedError) #TODO
		else:
			raise TypeError("list indices must be integers, not %s" % type(idx).__name__)
	def __delitem__(self, idx):
		if isinstance(idx, slice):
			for i in sorted(range(*idx.indices(self.__len__())), reverse=True):
				self.__delitem__(i)
		elif isinstance(idx, int):
			idx = self._validate_idx(idx)
			Tab = self._owner.parent.windowController().tabBarControl().tabItemAtIndex_(idx + 1)
			self._owner.parent.windowController().tabBarControl().closeTabItem_(Tab)
		else:
			raise TypeError("list indices must be integers or slices, not %s" % type(idx).__name__)
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

def ______________(): pass
def ____GSFont____(): pass
def ______________(): pass


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
		properties
		stems
		instances
		glyphs
		classes
		features
		featurePrefixes
		copyright
		copyrights
		license 
		licenses 
		designer
		designers
		designerURL
		manufacturer
		manufacturers
		manufacturerURL
		familyNames
		trademark
		trademarks
		sampleText
		sampleTexts
		description
		descriptions
		compatibleFullName
		compatibleFullNames
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
		keyboardIncrementBig
		keyboardIncrementHuge
		snapToObjects
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
	if len(args) > 0 and isString(args[0]):
		path = args[0]
		URL = NSURL.fileURLWithPath_(path)
		if path.endswith(".glyphs"):
			result = GSFont.alloc().initWithURL_error_(URL, None)
			if isinstance(result, tuple):
				result = result[0]
			return result
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

GSFont.__init__ = python_method(Font__init__)

def Font__repr__(self):
	return "<GSFont \"%s\" v%s.%s with %s masters and %s instances>" % (self.familyName, self.versionMajor, self.versionMinor, len(self.masters), len(self.instances))
GSFont.__repr__ = python_method(Font__repr__)

def Font__copy__(self, memo=None):
	font = self.copy()
	font.setParent_(self.parent)
	return font

GSFont.mutableCopyWithZone_ = Font__copy__
GSFont.__copy__ = python_method(Font__copy__)
GSFont.__deepcopy__ = python_method(Font__copy__)

def GSFont__contains__(self, key):
	raise NotImplementedError("Font can't access values like this")
GSFont.__contains__ = python_method(GSFont__contains__)

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

GSProjectDocument.instances = property(lambda self: FontInstancesProxy(self),
									   lambda self, value: FontInstancesProxy(self).setter(value))

# TODO: This needs to be updated to reflect the change to a dedicated GSAxis class (elsewhere too?!)

GSFont.axes = property(lambda self: FontAxesProxy(self),
					   lambda self, value: FontAxesProxy(self).setter(value))
'''
	.. attribute:: axes
		Collection of :class:`GSAxis`:

		:type: list

		.. versionadded:: 2.5
		.. versionchanged:: 3
'''

GSFont.properties = property(lambda self: self.mutableArrayValueForKey_("properties"),
							 lambda self, values: self.setProperties_(values))
'''
	.. attribute:: properties
		Holds the fonts info properties. Can be instances of :class:`GSFontInfoValueSingle` and :class:`GSFontInfoValueLocalized`.
		
		The localized values use language tags defined in the middle column of `Language System Tags table`: <https://docs.microsoft.com/en-us/typography/opentype/spec/languagetags>.

		The names are listed in the constants: `Info Property Keys`_

		.. code-block:: python
			# To find specific values:
			font.propertyForName_(name)
			# or
			font.propertyForName_languageTag_(name, languageTag).

			# To add an entry:
			font.setProperty_value_languageTag_(GSPropertyNameFamilyNamesKey, "SomeName", None)

		:type: list

		.. versionadded:: 3
'''

GSFont.metrics = property(lambda self: self.pyobjc_instanceMethods.metrics())
'''
	.. attribute:: metrics
		a list of all :class:`GSMetric` objects.

		:type: list
'''

GSFont.stems = property(lambda self: FontStemsProxy(self),
						lambda self, value: FontStemsProxy(self).setter(value))
'''
	.. attribute:: stems
		The stems. A list of :class:`GSMetric` objects. For each metric, there is a metricsValue in the masters, linked by the `id`.

		:type: list, dict
		
		.. code-block:: python
			font.stems[0].horizontal = False

'''

def __GSFont_getitem__(self, value):
	return self.glyphForName_(value)
GSFont.__getitem__ = python_method(__GSFont_getitem__)

GSFont.glyphs = property(lambda self: FontGlyphsProxy(self),
						 lambda self, value: FontGlyphsProxy(self).setter(value))

GSInterpolationFontProxy.glyphs = property(lambda self: FontGlyphsProxy(self),
										   lambda self, value: FontGlyphsProxy(self).setter(value))
'''
	.. attribute:: glyphs
		Collection of :class:`GSGlyph` objects. Returns a list, but you may also call glyphs using index or glyph name or character as key.

		:type: list, dict

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
			print(font.glyphs['Ư'])
			<GSGlyph "Uhorn" with 4 layers>

			# Access a glyph by unicode (new in v2.4.1)
			print(font.glyphs['01AF'])
			<GSGlyph "Uhorn" with 4 layers>

			# Access a glyph by index
			print(font.glyphs[145])
			<GSGlyph "Uhorn" with 4 layers>

			# Add a glyph
			font.glyphs.append(GSGlyph('adieresis'))

			# Duplicate a glyph under a different name
			newGlyph = font.glyphs['A'].copy()
			newGlyph.name = 'A.alt'
			font.glyphs.append(newGlyph)

			# Delete a glyph
			del(font.glyphs['A.alt'])

'''

GSFont.characterForGlyph = python_method(GSFont.characterForGlyph_)
'''
	.. function:: characterForGlyph(glyph)
		retuns the (internal) character that is used in the edit view. It the glpyh has a unicode, that is used, otherwiese a temporary code is assined. That can change over time, so don’t rely on it. This is mostly useful for constructing a string for see :attr:`tab.text <GSEditViewController.text>`

		.. versionadded:: 3.1
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

GSFont.copyright = property(lambda self: self.defaultPropertyForName_("copyrights"),
							lambda self, value: self.setProperty_value_languageTag_("copyrights", value, None))
'''
	.. attribute:: copyright
		This accesses the default value only. The localisations can be accessed by :attr:`GSFont.properties`

		:type: str
'''

GSFont.copyrights = property(lambda self: FontInfoPropertiesProxy(self, "copyrights"))
'''
	.. attribute:: copyrights
		This accesses all localized copyright values.
		For details :attr:`GSFont.properties`

		:type: dict
		.. code-block:: python
			Font.copyrights["ENG"] = "All rights reserved"

		.. versionadded:: 3.0.3
'''

GSFont.license = property(lambda self: self.defaultPropertyForName_("licenses"),
						  lambda self, value: self.setProperty_value_languageTag_("licenses", value, None))

'''
	.. attribute:: license
		This accesses the default value only. The localisations can be accessed by :attr:`GSFont.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSFont.licenses = property(lambda self: FontInfoPropertiesProxy(self, "licenses"))

'''
	.. attribute:: licenses
		This accesses all localized license values.
		For details :attr:`GSFont.properties`

		:type: dict

		.. code-block:: python
			Font.licenses["ENG"] = "This font may be installed on all of your machines and printers, but you may not sell or give these fonts to anyone else."

		
		.. versionadded:: 3.0.3
'''

GSFont.compatibleFullName = property(lambda self: self.defaultPropertyForName_("compatibleFullNames"),
									 lambda self, value: self.setProperty_value_languageTag_("compatibleFullNames", value, None))

'''
	.. attribute:: compatibleFullName
		This accesses the default value only. The localisations can be accessed by :attr:`GSFont.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSFont.compatibleFullNames = property(lambda self: FontInfoPropertiesProxy(self, "compatibleFullNames"))

'''
	.. attribute:: compatibleFullNames
		This accesses all localized designer values.
		For details :attr:`GSFont.properties`

		:type: dict

		.. code-block:: python
			Font.compatibleFullNames["ENG"] = "MyFont Condensed Bold"

		
		.. versionadded:: 3.0.3
'''

GSFont.sampleText = property(lambda self: self.defaultPropertyForName_("sampleTexts"),
							 lambda self, value: self.setProperty_value_languageTag_("sampleTexts", value, None))

'''
	.. attribute:: sampleText
		This accesses the default value only. The localisations can be accessed by :attr:`GSFont.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSFont.sampleTexts = property(lambda self: FontInfoPropertiesProxy(self, "sampleTexts"))

'''
	.. attribute:: sampleTexts
		This accesses all localized designer values.
		For details :attr:`GSFont.properties`

		:type: dict

		.. code-block:: python
			Font.sampleTexts["ENG"] = "This is my sample text"

		
		.. versionadded:: 3.0.3
'''

GSFont.description = property(lambda self: self.defaultPropertyForName_("descriptions"),
							  lambda self, value: self.setProperty_value_languageTag_("descriptions", value, None))

'''
	.. attribute:: description
		This accesses the default value only. The localisations can be accessed by :attr:`GSFont.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSFont.descriptions = property(lambda self: FontInfoPropertiesProxy(self, "descriptions"))

'''
	.. attribute:: descriptions
		This accesses all localized designer values.
		For details :attr:`GSFont.properties`

		:type: dict

		.. code-block:: python
			Font.descriptions["ENG"] = "This is my description"

		
		.. versionadded:: 3.0.3
'''

GSFont.designer = property(lambda self: self.defaultPropertyForName_("designers"),
						   lambda self, value: self.setProperty_value_languageTag_("designers", value, None))
'''
	.. attribute:: designer
		This accesses the default value only. The localisations can be accessed by :attr:`GSFont.properties`

		:type: str
'''

GSFont.designers = property(lambda self: FontInfoPropertiesProxy(self, "designers"))

'''
	.. attribute:: designers
		This accesses all localized designer values.
		For details :attr:`GSFont.properties`

		:type: dict

		.. code-block:: python
			Font.designers["ENG"] = "John Smith"

		.. versionadded:: 3.0.3
'''

GSFont.trademark = property(lambda self: self.defaultPropertyForName_("trademarks"),
							lambda self, value: self.setProperty_value_languageTag_("trademarks", value, None))

'''
	.. attribute:: trademark
		This accesses the default value only. The localisations can be accessed by :attr:`GSFont.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSFont.trademarks = property(lambda self: FontInfoPropertiesProxy(self, "trademarks"))

'''
	.. attribute:: trademarks
		This accesses all localized trademark values.
		For details :attr:`GSFont.properties`

		:type: dict

		.. code-block:: python
			Font.trademarks["ENG"] = "ThisFont is a trademark by MyFoundry.com"

		.. versionadded:: 3.0.3
'''
GSFont.designerURL = property(lambda self: self.defaultPropertyForName_("designerURL"),
							  lambda self, value: self.setProperty_value_languageTag_("designerURL", value, None))
'''
	.. attribute:: designerURL

		:type: str
'''
GSFont.manufacturer = property(lambda self: self.defaultPropertyForName_("manufacturers"),
							   lambda self, value: self.setProperty_value_languageTag_("manufacturers", value, None))
'''
	.. attribute:: manufacturer
		This accesses the default value only. The localisations can be accessed by :attr:`GSFont.properties`

		:type: str
'''

GSFont.manufacturers = property(lambda self: FontInfoPropertiesProxy(self, "manufacturers"))
'''
	.. attribute:: manufacturers
		This accesses all localized manufacturer values.
		For details :attr:`GSFont.properties`

		:type: dict

		.. code-block:: python
			Font.manufacturers["ENG"] = "My English Corporation"

		.. versionadded:: 3.0.3
'''

GSFont.manufacturerURL = property(lambda self: self.defaultPropertyForName_("manufacturerURL"),
								  lambda self, value: self.setProperty_value_languageTag_("manufacturerURL", value, None))
'''
	.. attribute:: manufacturerURL

		:type: str
'''
GSFont.versionMajor = property(lambda self: self.pyobjc_instanceMethods.versionMajor(),
							   lambda self, value: self.setVersionMajor_(value))
'''
	.. attribute:: versionMajor

		:type: int
'''
GSFont.versionMinor = property(lambda self: self.pyobjc_instanceMethods.versionMinor(),
							   lambda self, value: self.setVersionMinor_(value))
'''
	.. attribute:: versionMinor

		:type: int
'''

def __get_date__(self):
	return datetime.datetime.fromtimestamp(self.pyobjc_instanceMethods.date().timeIntervalSince1970())

def __set_date__(self, date):
	if isinstance(date, datetime.datetime):
		self.setDate_(NSDate.alloc().initWithTimeIntervalSince1970_(time.mktime(date.timetuple())))
	elif isinstance(date, (int, float)):
		self.setDate_(NSDate.alloc().initWithTimeIntervalSince1970_(date))
	elif isinstance(date, NSDate):
		self.setDate_(date)
	else:
		raise TypeError("date must be a datetime object, NSDate object, int or float, not %s" % type(date).__name__)
GSFont.date = property(lambda self: __get_date__(self),
					   lambda self, value: __set_date__(self, value))
'''
	.. attribute:: date

		:type: datetime.datetime

		.. code-block:: python
			print(font.date)
			2015-06-08 09:39:05

			# set date to now
			font.date = datetime.datetime.now()
			# using NSDate
			font.date = NSDate.date()
			# or in seconds since Epoch
			font.date = time.time()
'''

GSFont.familyName = property(lambda self: self.pyobjc_instanceMethods.fontName(),
							 lambda self, value: self.setFontName_(value))

GSFont.fontName = property(lambda self: self.pyobjc_instanceMethods.fontName(),
						   lambda self, value: self.setFontName_(value))
'''
	.. attribute:: familyName
		Family name of the typeface.

		:type: str
'''

GSFont.familyNames = property(lambda self: FontInfoPropertiesProxy(self, "familyNames"))

'''
	.. attribute:: familyNames
		This accesses all localized family name values.
		For details :attr:`GSFont.properties`

		:type: dict
		.. code-block:: python
			Font.familyNames["ENG"] = "MyFamilyName"

		
		.. versionadded:: 3.0.3
'''

GSFont.upm = property(lambda self: self.unitsPerEm(),
					  lambda self, value: self.setUnitsPerEm_(value))
'''
	.. attribute:: upm
		Units per Em

		:type: int
'''
GSFont.note = property(lambda self: self.pyobjc_instanceMethods.note(),
					   lambda self, value: self.setNote_(value))
'''
	.. attribute:: note

		:type: str
'''
GSFont.kerning = property(lambda self: self.kerningLTR(),
						  lambda self, value: self.setKerningLTR_(value))
'''
	.. attribute:: kerning
		Kerning for LTR writing
		A multi-level dictionary. The first level’s key is the :attr:`GSFontMaster.id` (each master has its own kerning), the second level’s key is the :attr:`GSGlyph.id` or class id (@MMK_L_XX) of the first glyph, the third level’s key is a glyph id or class id (@MMK_R_XX) for the second glyph. The values are the actual kerning values.

		To set a value, it is better to use the method :meth:`GSFont.setKerningForPair()`. This ensures a better data integrity (and is faster).

		:type: dict
'''

GSFont.kerningRTL = property(lambda self: self.pyobjc_instanceMethods.kerningRTL(),
							 lambda self, value: self.setKerningRTL_(value))
'''
	.. attribute:: kerningRTL
		Kerning for RTL writing
		A multi-level dictionary. The first level’s key is the :attr:`GSFontMaster.id` (each master has its own kerning), the second level’s key is the :attr:`GSGlyph.id` or class id (@MMK_L_XX) of the first glyph, the third level’s key is a glyph id or class id (@MMK_R_XX) for the second glyph. The values are the actual kerning values.

		To set a value, it is better to use the method :meth:`GSFont.setKerningForPair()`. This ensures a better data integrity (and is faster).

		:type: dict
'''

GSFont.kerningVertical = property(lambda self: self.pyobjc_instanceMethods.kerningVertical(),
								  lambda self, value: self.setKerningVertical_(value))
'''
	.. attribute:: kerningVertical
		Kerning for vertical writing
		A multi-level dictionary. The first level’s key is the :attr:`GSFontMaster.id` (each master has its own kerning), the second level’s key is the :attr:`GSGlyph.id` or class id (@MMK_L_XX) of the first glyph, the third level’s key is a glyph id or class id (@MMK_R_XX) for the second glyph. The values are the actual kerning values.

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

GSFont.tempData = property(lambda self: TempDataProxy(self))

'''
	.. attribute:: tempData
		A dictionary to store data temporarily. Use a unique key. This will not be saved to file. If you need the data persistent, use layer.userData

		:type: dict

		.. code-block:: python
			# set value
			layer.tempData['rememberToMakeCoffee'] = True

			# delete value
			del layer.tempData['rememberToMakeCoffee']
'''

GSFont.disablesNiceNames = property(lambda self: bool(self.pyobjc_instanceMethods.disablesNiceNames()),
									lambda self, value: self.setDisablesNiceNames_(value))
'''
	.. attribute:: disablesNiceNames
		Corresponds to the “Don't use nice names” setting from the Font Info dialog.

		:type: bool

'''

GSFont.customParameters = property(lambda self: CustomParametersProxy(self),
								   lambda self, value: CustomParametersProxy(self).setter(value))
'''
	.. attribute:: customParameters
		The custom parameters. List of :class:`GSCustomParameter` objects. You can access them by name or by index.

		:type: list, dict

		.. code-block:: python
			# access all parameters
			for parameter in font.customParameters:
				print(parameter)

			# set a parameter
			font.customParameters['glyphOrder'] = ["a", "b", "c"]

			# delete a parameter
			del(font.customParameters['glyphOrder'])

'''
GSFont.grid = property(lambda self: self.pyobjc_instanceMethods.gridMain(),
					   lambda self, value: self.setGridMain_(value))
'''
	.. attribute:: grid
		Corresponds to the “Grid spacing” setting from the Info dialog.

		:type: int
'''

GSFont.gridSubDivisions = property(lambda self: self.pyobjc_instanceMethods.gridSubDivision(),
								   lambda self, value: self.setGridSubDivision_(value))
'''
	.. attribute:: gridSubDivisions
		Corresponds to the “Grid sub divisions” setting from the Info dialog.

		:type: int
'''

GSFont.gridLength = property(lambda self: self.pyobjc_instanceMethods.gridLength())
'''
	.. attribute:: gridLength
		Ready calculated size of grid for rounding purposes. Result of division of grid with gridSubDivisions.

		:type: float
'''

GSFont.disablesAutomaticAlignment = property(lambda self: bool(self.pyobjc_instanceMethods.disablesAutomaticAlignment()),
											 lambda self, value: self.setDisablesAutomaticAlignment_(value))
'''
	.. attribute:: disablesAutomaticAlignment

		:type: bool
'''

GSFont.keyboardIncrement = property(lambda self: self.pyobjc_instanceMethods.keyboardIncrement(),
									lambda self, value: self.setKeyboardIncrement_(value))
'''
	.. attribute:: keyboardIncrement
		Distance of movement by arrow keys. Default:1

		:type: float
'''

GSFont.keyboardIncrementBig = property(lambda self: self.pyobjc_instanceMethods.keyboardIncrementBig(),
									   lambda self, value: self.setKeyboardIncrementBig_(value))
'''
	.. attribute:: keyboardIncrementBig
		Distance of movement by arrow plus Shift key. Default:10

		:type: float

		.. versionadded:: 3.0
'''
GSFont.keyboardIncrementHuge = property(lambda self: self.pyobjc_instanceMethods.keyboardIncrementHuge(),
										lambda self, value: self.setKeyboardIncrementHuge_(value))
'''
	.. attribute:: keyboardIncrementHuge
		Distance of movement by arrow plus Command key. Default:100

		:type: float

		.. versionadded:: 3.0
'''

GSFont.snapToObjects = property(lambda self: bool(self.pyobjc_instanceMethods.snapToObjects()),
								lambda self, value: self.setSnapToObjects_(value))
'''
	.. attribute:: snapToObjects
		disable snapping to nodes and background

		:type: bool

		.. versionadded:: 3.0.1
'''

GSFont.previewRemoveOverlap = property(lambda self: bool(self.pyobjc_instanceMethods.previewRemoveOverlap()),
									   lambda self, value: self.setPreviewRemoveOverlap_(value))
'''
	.. attribute:: previewRemoveOverlap
		disable preview remove overlap

		:type: bool

		.. versionadded:: 3.0.1
'''

def Font_GetSelectedGlyphs(self):
	return self.parent.windowController().glyphsController().selectedObjects()

def Font_SetSelectedGlyphs(self, value):
	if not isinstance(value, (list, tuple, NSArray)):
		raise TypeError('Argument needs to be a list, not %s' % type(value).__name__)
	self.parent.windowController().glyphsController().setSelectedObjects_(value)

GSFont.selection = property(lambda self: Font_GetSelectedGlyphs(self),
							lambda self, value: Font_SetSelectedGlyphs(self, value))
'''
	.. attribute:: selection
		Returns a list of all selected glyphs in the Font View.

		:type: list
'''

GSFont.selectedLayers = property(lambda self: self.parent.selectedLayers())
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

GSFont.masterIndex = property(lambda self: self.parent.windowController().masterIndex(),
							  lambda self, value: self.parent.windowController().setMasterIndex_(value))
'''
	.. attribute:: masterIndex
		Returns the index of the active master (selected in the toolbar).

		:type: int

'''

def __current_Text__(self):
	try:
		return self.parent.windowController().activeEditViewController().graphicView().displayStringASCIIonly_(False)
	except:
		pass
	return None

def __set__current_Text__(self, String):
	self.parent.windowController().activeEditViewController().graphicView().setDisplayString_(String)

GSFont.currentText = property(lambda self: __current_Text__(self),
							  lambda self, value: __set__current_Text__(self, value))
'''
	.. attribute:: currentText
		The text of the current Edit view.

		Unencoded and none ASCII glyphs will use a slash and the glyph name. (e.g: /a.sc). Setting unicode strings works.

		:type: str
'''

# Tab interaction:

GSFont.tabs = property(lambda self: FontTabsProxy(self))

'''
	.. attribute:: tabs
		List of open Edit view tabs in UI, as list of :class:`GSEditViewController` objects.

		:type: list

		.. code-block:: python
			# open new tab with text
			font.newTab('hello')

			# access all tabs
			for tab in font.tabs:
				print(tab)

			# close last tab
			font.tabs[-1].close()

'''

GSFont.fontView = property(lambda self: self.parent.windowController().tabBarControl().tabItemAtIndex_(0))
'''
	.. attribute:: fontView

		:type: :class:`GSFontViewController`
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

		:type: str
'''

GSFont.toolIndex = property(lambda self: self.parent.windowController().selectedToolIndex(),
							lambda self, value: self.parent.windowController().setSelectedToolIndex_(value))

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

GSFont.tool = property(lambda self: __GSFont_tool__(self),
					   lambda self, value: __GSFont_setTool__(self, value))

'''
	.. attribute:: tool
		Name of tool selected in toolbar.

		For available names including third-party plug-ins that come in the form of selectable tools, see `GSFont.tools` below.

		:type: string

		.. code-block:: python
			font.tool = 'SelectTool' # Built-in tool
			font.tool = 'GlyphsAppSpeedPunkTool' # Third party plug-in

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
		Returns a list of available tool names, including third-party plug-ins.

		:type: list, string
'''

GSFont.appVersion = property(lambda self: self.pyobjc_instanceMethods.appVersion())

'''
	.. attribute:: appVersion
		Returns the version that the file was last saved

		.. versionadded:: 2.5
'''

GSFont.formatVersion = property(lambda self: self.pyobjc_instanceMethods.formatVersion(), 
								lambda self, value: self.setFormatVersion_(value))
'''
	.. attribute:: formatVersion
		The file-format the font should be written. possible values are '2' and '3'

		:type: int

		.. versionadded:: 3
'''

'''
	**Functions**
'''

def Font__save__(self, path=None, formatVersion=3, makeCopy=False):
	if self.parent is not None and not makeCopy:
		if path is None:
			self.parent.saveDocument_(None)
		else:
			if path.endswith('.glyphs'):
				typeName = "com.schriftgestaltung.glyphs"
			elif path.endswith('.glyphspackage'):
				typeName = "com.glyphsapp.glyphspackage"
			elif path.endswith('.ufo'):
				typeName = "org.unifiedfontobject.ufo"
			else:
				raise ValueError("Save file must have file extension .glyphs, .glyphspackage or .ufo")
			URL = NSURL.fileURLWithPath_(path)
			self.parent.saveToURL_ofType_forSaveOperation_error_(URL, typeName, 1, objc.nil)
	elif path is not None:
		URL = NSURL.fileURLWithPath_(path)
		if path.endswith('.glyphs'):
			typeId = GSPackageFlatFile
			self.saveToURL_type_error_(URL, typeId, None)
		elif path.endswith('.glyphspackage'):
			typeId = GSPackageBundle
			self.saveToURL_type_error_(URL, typeId, None)
		elif path.endswith('.ufo'):
			GlyphsFileFormatUFO = objc.lookUpClass("GlyphsFileFormatUFO")
			ufoWriter = GlyphsFileFormatUFO.new()
			ufoWriter.writeFont_toURL_error_(self, URL, None)
		else:
			raise ValueError("Save file must have file extension .glyphs, .glyphspackage or .ufo")
	else:
		raise ValueError("No path set")

GSFont.save = python_method(Font__save__)
'''
	.. function:: save([path=None, formatVersion=3, makeCopy])
		
		Saves the font.
		
		If no path is given, it saves to the existing location.

		:param path: Optional file path
		:type path: str
		:param formatVersion: the format of the file
		:type formatVersion: int
		:param makeCopy: saves a new file without changeing the documents file paths
		:type makeCopy: bool

'''

def Font__close__(self, ignoreChanges=True):
	if self.parent:
		if ignoreChanges:
			self.parent.close()
		else:
			self.parent.canCloseDocumentWithDelegate_shouldCloseSelector_contextInfo_(None, None, None)
GSFont.close = python_method(Font__close__)

'''
	.. function:: close([ignoreChanges=True])

		Closes the font.

		:param ignoreChanges: Optional. Ignore changes to the font upon closing
		:type ignoreChanges: bool

	.. function:: disableUpdateInterface()

		Disables interface updates and thus speeds up glyph processing. Call this before you do big changes to the font, or to its glyphs. Make sure that you call :meth:`font.enableUpdateInterface() <GSFont.enableUpdateInterface()>` when you are done.

	.. function:: enableUpdateInterface()
	
		This re-enables the interface update. Only makes sense to call if you have disabled it earlier.

'''

def GSFont__show__(self):
	if self not in Glyphs.fonts:
		Glyphs.fonts.append(self)
	else:
		self.parent.windowController().showWindow_(None)
GSFont.show = python_method(GSFont__show__)

'''
	.. function:: show()

		Makes font visible in the application, either by bringing an already open font window to the front or by appending a formerly invisible font object (such as the result of a `copy()` operation) as a window to the application.

		.. versionadded:: 2.4.1
'''

def kerningForPair(self, FontMasterID, LeftKeringId, RightKerningId, direction=GSLTR):
	if not LeftKeringId[0] == '@':
		glyph = self.glyphs[LeftKeringId]
		if glyph is not None:
			LeftKeringId = glyph.id
		else:
			raise KeyError("Glyphs with name: %s not found" % LeftKeringId)
	if not RightKerningId[0] == '@':
		glyph = self.glyphs[RightKerningId]
		if glyph is not None:
			RightKerningId = glyph.id
		else:
			raise KeyError("Glyphs with name: %s not found" % RightKerningId)
	value = self.kerningForFontMasterID_LeftKey_RightKey_direction_(FontMasterID, LeftKeringId, RightKerningId, direction)
	if value > 1000000:
		return None
	return value

GSFont.kerningForPair = python_method(kerningForPair)
'''
	.. function:: kerningForPair(fontMasterId, leftKey, rightKey [, direction = LTR])

		This returns the kerning value for the two specified glyphs (leftKey or rightKey is the glyph name) or a kerning group key (@MMK_X_XX).

		:param fontMasterId: The id of the FontMaster
		:type fontMasterId: str
		:param leftKey: either a glyph name or a class name
		:type leftKey: str
		:param rightKey: either a glyph name or a class name
		:type rightKey: str
		:param direction: optional writing direction (see Constants; 'LTR' (0) or 'RTLTTB'). Default is LTR.
		:type direction: int
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

def setKerningForPair(self, FontMasterID, LeftKeringId, RightKerningId, Value, direction=GSLTR):
	if not LeftKeringId[0] == '@':
		glyph = self.glyphs[LeftKeringId]
		if glyph is not None:
			LeftKeringId = glyph.id
		else:
			raise KeyError("Glyphs with name: %s not found" % LeftKeringId)
	if not RightKerningId[0] == '@':
		glyph = self.glyphs[RightKerningId]
		if glyph is not None:
			RightKerningId = glyph.id
		else:
			raise KeyError("Glyphs with name: %s not found" % RightKerningId)
	self.setKerningForFontMasterID_LeftKey_RightKey_Value_direction_(FontMasterID, LeftKeringId, RightKerningId, Value, direction)
GSFont.setKerningForPair = python_method(setKerningForPair)
'''
	.. function:: setKerningForPair(fontMasterId, leftKey, rightKey, value [, direction = GSLTR])

		This sets the kerning for the two specified glyphs (leftKey or rightKey is the glyphname) or a kerning group key (@MMK_X_XX).
	
		:param fontMasterId: The id of the FontMaster
		:type fontMasterId: str
		:param leftKey: either a glyph name or a class name
		:type leftKey: str
		:param rightKey: either a glyph name or a class name
		:type rightKey: str
		:param value: kerning value
		:type value: float
		:param direction: optional writing direction (see Constants). Default is GSLTR.
		:type direction: str

		.. code-block:: python
			# set kerning for group T and group A for currently selected master
			# ('L' = left side of the pair and 'R' = left side of the pair)
			font.setKerningForPair(font.selectedFontMaster.id, '@MMK_L_T', '@MMK_R_A', -75)
'''

def removeKerningForPair(self, FontMasterID, LeftKeringId, RightKerningId, direction=GSLTR):
	if not LeftKeringId[0] == '@':
		glyph = self.glyphs[LeftKeringId]
		if glyph is not None:
			LeftKeringId = glyph.id
		else:
			raise KeyError("Glyphs with name: %s not found" % LeftKeringId)
	if not RightKerningId[0] == '@':
		glyph = self.glyphs[RightKerningId]
		if glyph is not None:
			RightKerningId = glyph.id
		else:
			raise KeyError("Glyphs with name: %s not found" % RightKerningId)
	self.removeKerningForFontMasterID_LeftKey_RightKey_direction_(FontMasterID, LeftKeringId, RightKerningId, direction)
GSFont.removeKerningForPair = python_method(removeKerningForPair)
'''
	.. function:: removeKerningForPair(FontMasterId, LeftKey, RightKey, direction=GSLTR)

		Removes the kerning for the two specified glyphs (LeftKey or RightKey is the glyphname) or a kerning group key (@MMK_X_XX).

		:param FontMasterId: The id of the FontMaster
		:type FontMasterId: str
		:param LeftKey: either a glyph name or a class name
		:type LeftKey: str
		:param RightKey: either a glyph name or a class name
		:type RightKey: str
		:param direction: optional writing direction (see Constants; 'GSLTR' (0) or 'GSVertical'). Default is GSLTR. (added in 2.6.6)
		:type direction: int

		.. code-block:: python
			# remove kerning for group T and group A for all masters
			# ('L' = left side of the pair and 'R' = left side of the pair)
			for master in font.masters:
				font.removeKerningForPair(master.id, '@MMK_L_T', '@MMK_R_A')
'''

def __GSFont__addTab__(self, tabText=""):
	if self.parent:
		if isString(tabText):
			return self.parent.windowController().addTabWithString_(tabText)
		else:
			return self.parent.windowController().addTabWithLayers_(tabText)
	return None

GSFont.newTab = python_method(__GSFont__addTab__)
'''
	.. function:: newTab([tabText])

		Opens a new tab in the current document window, optionally with text, and return that tab object
	
		:param tabText: Text or glyph names escaped with '/' OR list of layers

		.. code-block:: python
			# open new tab
			tab = font.newTab('abcdef')
			print(tab)
		
			# or
			tab = font.newTab([layer1, layer2])
			print(tab)

	
'''

def __GSFont__updateFeatures__(self):
	GSFeatureGenerator.alloc().init().makeFeatures_error_(self, None)
	self.compileFeatures()
GSFont.updateFeatures = python_method(__GSFont__updateFeatures__)

'''
	.. function:: updateFeatures()

		Updates all OpenType features and classes at once, including generating necessary new features and classes. Equivalent to the "Update" button in the features panel. This already includes the compilation of the features (see :meth:`font.compileFeatures() <GSFont.compileFeatures()>`).

		.. versionadded:: 2.4
'''

def __GSFont__compileFeatures__(self):
	return self.compileTempFontError_(None)

GSFont.compileFeatures = python_method(__GSFont__compileFeatures__)

'''
	.. function:: compileFeatures()

		Compiles the features, thus making the new feature code functionally available in the editor. Equivalent to the "Compile" button in the features panel.

		.. versionadded:: 2.5
'''

##################################################################################
#
#
#
#           GSAxis
#
#
#
##################################################################################

def ______________(): pass
def ____GSAxis____(): pass
def ______________(): pass

'''

:mod:`GSAxis`
===============================================================================

Implementation of the axis object. 

.. class:: GSAxis()

	Properties

	.. autosummary::

		name
		axisTag
		axisId
		hidden
		font

	**Properties**
'''

GSAxis.__new__ = staticmethod(GSObject__new__)

def Axis__init__(self):
	pass
GSAxis.__init__ = python_method(Axis__init__)
GSAxis.__copy__ = python_method(GSObject__copy__)
GSAxis.__deepcopy__ = python_method(GSObject__copy__)

GSAxis.font = property(lambda self: self.pyobjc_instanceMethods.font())
'''
	.. attribute:: font
		Reference to the :class:`GSFont` object that contains the axis. Normally that is set by the app.

		:type: GSFont
'''
GSAxis.name = property(lambda self: self.pyobjc_instanceMethods.name(),
					   lambda self, value: self.setName_(value))
'''
	.. attribute:: name
		The name of the axis

		:type: str
'''
GSAxis.axisTag = property(lambda self: self.pyobjc_instanceMethods.axisTag(),
						  lambda self, value: self.setAxisTag_(value))
'''
	.. attribute:: axisTag
		The axisTag. this is a four letter string. see `OpenType Design-Variation Axis Tag Registry <https://docs.microsoft.com/en-us/typography/opentype/spec/dvaraxisreg>`_.

		:type: str
'''
GSAxis.axisId = property(lambda self: self.pyobjc_instanceMethods.axisId(),
						 lambda self, value: self.setAxisId_(value))
'''
	.. attribute:: id
		The id to link the values in the masters

		:type: str
'''
GSAxis.hidden = property(lambda self: bool(self.pyobjc_instanceMethods.hidden()),
						 lambda self, value: self.setHidden_(value))
'''
	.. attribute:: hidden
		If the axis should be shown to the user

		:type: bool
'''

##################################################################################
#
#
#
#           GSMetric
#
#
#
##################################################################################

def ________________(): pass
def ____GSMetric____(): pass
def ________________(): pass

'''

:mod:`GSMetric`
===============================================================================

Implementation of the metric object. It is used to link the metrics and stems in the masters.

.. class:: GSMetric()

	Properties

	.. autosummary::

		name
		id
		filter
		type
		horizontal

	**Properties**
'''

GSMetric.__new__ = staticmethod(GSObject__new__)

def GSMetric__init__(self):
	pass
GSMetric.__init__ = python_method(Axis__init__)
GSMetric.__copy__ = python_method(GSObject__copy__)
GSMetric.__deepcopy__ = python_method(GSObject__copy__)

GSMetric.font = property(lambda self: self.pyobjc_instanceMethods.font())
'''
	.. attribute:: font
		Reference to the :class:`GSFont` object that contains the metric. Normally that is set by the app.

		:type: GSFont
'''
GSMetric.name = property(lambda self: self.pyobjc_instanceMethods.name(),
						 lambda self, value: self.setName_(value))
'''
	.. attribute:: name
		The name of the metric or stem

		:type: str
'''
GSMetric.id = property(lambda self: self.pyobjc_instanceMethods.id())
'''
	.. attribute:: id
		The id to link the values in the masters

		:type: str
'''

GSMetric.type = property(lambda self: self.pyobjc_instanceMethods.type(),
						 lambda self, value: self.setType_(value))
'''
	.. attribute:: type
		The metrics type

		:type: int
'''

GSMetric.filter = property(lambda self: self.pyobjc_instanceMethods.filter(),
						   lambda self, value: self.setFilter_(value))
'''
	.. attribute:: filter
		A filter to limit the scope of the metric.

		:type: NSPredicate
'''
GSMetric.horizontal = property(lambda self: bool(self.pyobjc_instanceMethods.horizontal()),
							   lambda self, value: self.setHorizontal_(value))
'''
	.. attribute:: horizontal
		This is used for stem metrics. so only use this for font.stems

		:type: bool
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

def ____________________(): pass
def ____GSFontMaster____(): pass
def ____________________(): pass

'''

:mod:`GSFontMaster`
===============================================================================

Implementation of the master object. This corresponds with the "Masters" pane in the Font Info. In Glyphs.app, the glyphs of each master are reachable not here, but as :class:`layers <GSLayer>` attached to the :class:`glyphs <GSGlyph>` attached to the :class:`font <GSFont>` object. See the infographic on top for better understanding.

.. class:: GSFontMaster()

'''

GSFontMaster.__new__ = staticmethod(GSObject__new__)

def FontMaster__init__(self):
	pass
GSFontMaster.__init__ = python_method(FontMaster__init__)

def FontMaster__repr__(self):
	return "<GSFontMaster \"%s\" %s>" % (self.name, str(self.axes).replace("\n", "").replace("\t", ""))
GSFontMaster.__repr__ = python_method(FontMaster__repr__)

GSFontMaster.mutableCopyWithZone_ = GSObject__copy__
GSFontMaster.__copy__ = python_method(GSObject__copy__)
GSFontMaster.__deepcopy__ = python_method(GSObject__copy__)

'''

	.. autosummary::

		id
		name
		axes
		properties
		ascender
		capHeight
		xHeight
		descender
		italicAngle
		alignmentZones
		blueValues
		otherBlues
		guides
		stems
		userData
		customParameters
		font

	**Properties**

'''

GSFontMaster.id = property(lambda self: self.pyobjc_instanceMethods.id(),
						   lambda self, value: self.setId_(value))
'''
	.. attribute:: id
		Used to identify :class:`Layers` in the Glyph

		see :attr:`GSGlyph.layers`

		:type: str

		.. code-block:: python
			# ID of first master
			print(font.masters[0].id)
			3B85FBE0-2D2B-4203-8F3D-7112D42D745E

			# use this master to access the glyph’s corresponding layer
			print(glyph.layers[font.masters[0].id])
			<GSLayer "Light" (A)>

'''

GSFontMaster.font = property(lambda self: self.pyobjc_instanceMethods.font(),
							 lambda self, value: self.setFont_(value))
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

		:type: list

		.. code-block:: python
			# setting a value for a specific axis
			master.axes[2] = 12
			# setting all values at once
			master.axes = [100, 12, 3.5]

		.. versionadded:: 2.5.2
'''

GSFontMaster.properties = property(lambda self: self.mutableArrayValueForKey_("properties"),
								   lambda self, values: self.setProperties_(values))
'''
	.. attribute:: properties
		Holds the fonts info properties. Can be instances of :class:`GSFontInfoValueSingle` and :class:`GSFontInfoValueLocalized`

		The localized values use language tags defined in the middle column of `Language System Tags table`: <https://docs.microsoft.com/en-us/typography/opentype/spec/languagetags>.

		To find specific values, use master.propertyForName_(name) or master.propertyForName_languageTag_(name, languageTag).

		:type: list

		.. versionadded:: 3
'''

GSFontMaster.metrics = property(lambda self: self.pyobjc_instanceMethods.metrics())
'''
	.. attribute:: metrics
		a list of all :class:`GSMetricValue` objects.

		:type: list
'''

GSFontMaster.ascender = property(lambda self: self.defaultAscender(),
								 lambda self, value: self.setDefaultAscender_(value))
'''
	.. attribute:: ascender
		This is the default ascender of the master. There might be other values that are for specific glyphs. See :attr:`layer.metrics <GSLayer.metrics>`

		:type: float
'''

GSFontMaster.capHeight = property(lambda self: self.defaultCapHeight(),
								  lambda self, value: self.setDefaultCapHeight_(value))
'''
	.. attribute:: capHeight
		This is the default capHeight of the master. There might be other values that are for specific glyphs. See :attr:`layer.metrics <GSLayer.metrics>`

		:type: float
'''

GSFontMaster.xHeight = property(lambda self: self.defaultXHeight(),
								lambda self, value: self.setDefaultXHeight_(value))
'''
	.. attribute:: xHeight
		This is the default xHeight of the master. There might be other values that are for specific glyphs. See :attr:`layer.metrics <GSLayer.metrics>`

		:type: float
'''

GSFontMaster.descender = property(lambda self: self.defaultDescender(),
								  lambda self, value: self.setDefaultDescender_(value))
'''
	.. attribute:: descender
		This is the default descender of the master. There might be other values that are for specific glyphs. See :attr:`layer.metrics <GSLayer.metrics>`

		:type: float
'''

GSFontMaster.italicAngle = property(lambda self: self.defaultItalicAngle(),
									lambda self, value: self.setDefaultItalicAngle_(value))
'''
	.. attribute:: italicAngle

		:type: float
'''

GSFontMaster.stems = property(lambda self: MasterStemsProxy(self),
							  lambda self, value: MasterStemsProxy(self).setter(value))

'''
	.. attribute:: stems
		The stems. This is a list of numbers.

		:type: list

		.. code-block:: python

			font.masters[0].stems = [10, 11, 20]

			print(master.stems[0])

			master.stems[0] = 12

			master.stems["stemName"] = 12

'''

GSFontMaster.alignmentZones = property(lambda self: tuple(self.defaultAlignmentZones()))
'''
	.. attribute:: alignmentZones
		Collection of :class:`GSAlignmentZone` objects. Read-only.

		:type: list
'''

def FontMaster_blueValues(self):
	return GSGlyphsInfo.blueValues_(self.alignmentZones)

GSFontMaster.blueValues = property(lambda self: FontMaster_blueValues(self))
'''
	.. attribute:: blueValues
		PS hinting Blue Values calculated from the master’s alignment zones. Read-only.

		:type: list
'''

def FontMaster_otherBlues(self):
	return GSGlyphsInfo.otherBlues_(self.alignmentZones)

GSFontMaster.otherBlues = property(lambda self: FontMaster_otherBlues(self))
'''
	.. attribute:: otherBlues
		PS hinting Other Blues calculated from the master’s alignment zones. Read-only.

		:type: list
'''

GSFontMaster.guides = property(lambda self: LayerGuidesProxy(self),
							   lambda self, value: LayerGuidesProxy(self).setter(value))
# keep for compatibility
GSFontMaster.guideLines = GSFontMaster.guides
'''
	.. attribute:: guides
		Collection of :class:`GSGuide` objects. These are the font-wide (actually master-wide) red guidelines. For glyph-level guidelines (attached to the layers) see :attr:`GSLayer.guides`

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

GSFontMaster.customParameters = property(lambda self: CustomParametersProxy(self),
										 lambda self, value: CustomParametersProxy(self).setter(value))
'''
	.. attribute:: customParameters
		The custom parameters. List of :class:`GSCustomParameter` objects. You can access them by name or by index.

		:type: list, dict

		.. code-block:: python
			# access all parameters
			for parameter in font.masters[0].customParameters:
				print(parameter)

			# set a parameter
			font.masters[0].customParameters['underlinePosition'] = -135

			# delete a parameter
			del(font.masters[0].customParameters['underlinePosition'])

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


GSElement.selected = property(lambda self: ObjectInLayer_selected(self),
							  lambda self, value: SetObjectInLayer_selected(self, value))


##################################################################################
#
#
#
#           GSAlignmentZone
#
#
#
##################################################################################


def _______________________(): pass
def ____GSAlignmentZone____(): pass
def _______________________(): pass

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

GSAlignmentZone.__init__ = python_method(AlignmentZone__init__)

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

GSAlignmentZone.position = property(lambda self: self.pyobjc_instanceMethods.position(),
									lambda self, value: self.setPosition_(validateNumber(value)))
'''
	.. attribute:: position

		:type: float
'''
	
GSAlignmentZone.size = property(lambda self: self.pyobjc_instanceMethods.size(),
								lambda self, value: self.setSize_(value))
'''
	.. attribute:: size

		:type: float
'''

def __propertyListValue__(self):
	return dict(self.propertyListValueFormat_(GSFormatVersionCurrent))
GSAlignmentZone.plistValue = python_method(__propertyListValue__)
GSTTStem.plistValue = python_method(__propertyListValue__)

##################################################################################
#
#
#
#           GSInstance
#
#
#
##################################################################################


def __________________(): pass
def ____GSInstance____(): pass
def __________________(): pass

'''

:mod:`GSInstance`
===============================================================================

Implementation of the instance object. This corresponds with the "Instances" pane in the Font Info.

.. class:: GSInstance()

'''

def GSInstance__new__(typ, *args, **kwargs):
	instanceType = 0
	if kwargs is not None:
		instanceType = kwargs.get("type", 0)
	return typ.alloc().initWithType_(instanceType)
GSInstance.__new__ = staticmethod(GSInstance__new__)

def Instance__init__(self):
	pass
GSInstance.__init__ = python_method(Instance__init__)

def Instance__repr__(self):
	return "<GSInstance \"%s\" %s>" % (self.name, str(self.axes).replace("\n", "").replace("\t", ""))
GSInstance.__repr__ = python_method(Instance__repr__)

GSInstance.mutableCopyWithZone_ = GSObject__copy__

'''
	Properties

	.. autosummary::

		active
		name
		visible
		weightClass
		widthClass
		axes
		properties
		isItalic
		isBold
		linkStyle
		preferredFamily
		preferredSubfamilyName
		windowsFamily
		windowsStyle
		windowsLinkedToStyle
		fontName
		fullName
		compatibleFullName
		compatibleFullNames
		copyright
		copyrights
		description
		descriptions
		designer
		designers
		designerURL
		familyName
		familyNames
		license
		licenses
		manufacturer
		manufacturers
		manufacturerURL
		preferredFamilyName
		preferredFamilyNames
		preferredSubfamilyName
		preferredSubfamilyNames
		sampleText
		sampleTexts
		styleMapFamilyName
		styleMapFamilyNames
		styleMapStyleName
		styleMapStyleNames
		styleName
		styleNames
		trademark
		trademarks
		variableStyleName
		variableStyleNames
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

GSInstance.active = property(lambda self: bool(self.exports()),
							 lambda self, value: self.setExports_(value))
'''
	.. attribute:: active

		:type: bool
'''

GSInstance.visible = property(lambda self: bool(self.pyobjc_instanceMethods.visible()),
							  lambda self, value: self.setVisible_(value))
'''
	.. attribute:: visible
		if visible in the preview in edit view

		:type: bool
'''

GSInstance.name = property(lambda self: self.pyobjc_instanceMethods.name(),
						   lambda self, value: self.setName_(value))
'''
	.. attribute:: name
		Name of instance. Corresponds to the "Style Name" field in the font info. This is used for naming the exported fonts.

		:type: string
'''

GSInstance.type = property(lambda self: self.pyobjc_instanceMethods.type())
'''
	.. attribute:: type
		the type of the instance. Can be either INSTANCETYPESINGLE or INSTANCETYPEVARIABLE.

		:type: int
'''

def _setValueValidation(target, key, value, valuetype):
	if not isinstance(value, valuetype):
		raise TypeError("Type for {} should be {}, got {}".format(key, valuetype.__name__, type(value).__name__))
	target.setValue_forKey_(value, key)

GSInstance.weightClass = property(lambda self: self.weightClassValue(),
								  lambda self, value: _setValueValidation(self, "weightClassValue", value, int))
'''
	.. attribute:: weightClass
		Weight class, as set in Font Info, as an integer. Values from 1 to 1000 are supported but 100–900 is recommended.
	
		For actual position in interpolation design space, use GSInstance.axes.

		:type: int
'''

GSInstance.weightClassName = property(lambda self: self.weightClassUI())
'''
	.. attribute:: weightClassName
		Human readable name corresponding to the value of GSInstance.weightClass. This attribute is read-only.
		Can be None if GSInstance.weightClass is not a multiple of 100.

		:type: string
'''

GSInstance.widthClass = property(lambda self: self.widthClassValue(),
								 lambda self, value: _setValueValidation(self, "widthClassValue", value, int))
'''
	.. attribute:: widthClass
		Width class, as set in Font Info, as an integer. Values from 1 to 9 are supported.
		
		For actual position in interpolation design space, use GSInstance.axes.

		:type: int
'''

GSInstance.widthClassName = property(lambda self: self.widthClassUI())
'''
	.. attribute:: widthClassName
		Human readable name corresponding to the value of GSInstance.widthClass. This attribute is read-only.

		:type: string
'''

GSInstance.axes = property(lambda self: MasterAxesProxy(self),
						   lambda self, value: MasterAxesProxy(self).setter(value))
'''
	.. attribute:: axes
		List of floats specifying the positions for each axis

		:type: list

		.. code-block:: python
			# setting a value for a specific axis
			instance.axes[2] = 12
			# setting all values at once
			instance.axes = [100, 12, 3.5] # make sure that the count of numbers matches the count of axes

		.. versionadded:: 2.5.2
'''

GSInstance.properties = property(lambda self: self.mutableArrayValueForKey_("properties"),
								 lambda self, values: self.setProperties_(values))
'''
	.. attribute:: properties
		Holds the fonts info properties. Can be instances of :class:`GSFontInfoValueSingle` and :class:`GSFontInfoValueLocalized`

		The localized values use language tags defined in the middle column of `Language System Tags table`: <https://docs.microsoft.com/en-us/typography/opentype/spec/languagetags>.

		The names are listed in the constants: `Info Property Keys`_

		.. code-block:: python
			# To find specific values:
			instance.propertyForName_(name)
			# or
			instance.propertyForName_languageTag_(name, languageTag).

			# To add an entry:
			instance.setProperty_value_languageTag_(GSPropertyNameFamilyNamesKey, "SomeName", None)

		:type: list

		.. versionadded:: 3

'''

GSInstance.isItalic = property(lambda self: bool(self.pyobjc_instanceMethods.isItalic()),
							   lambda self, value: self.setIsItalic_(value))

'''
	.. attribute:: isItalic
		Italic flag for style linking

		:type: bool
'''

GSInstance.isBold = property(lambda self: bool(self.pyobjc_instanceMethods.isBold()),
							 lambda self, value: self.setIsBold_(value))

'''
	.. attribute:: isBold
		Bold flag for style linking

		:type: bool
'''

GSInstance.linkStyle = property(lambda self: self.pyobjc_instanceMethods.linkStyle(),
								lambda self, value: self.setLinkStyle_(value))

'''
	.. attribute:: linkStyle
		Linked style

		:type: string
'''

GSInstance.preferredFamily = property(lambda self: self.pyobjc_instanceMethods.preferredFamily(),
									  lambda self, value: self.setProperty_value_languageTag_("preferredFamilyNames", value, None))
'''
	.. attribute:: preferredFamily
		preferredFamily

		:type: string
'''

GSInstance.windowsFamily = property(lambda self: self.pyobjc_instanceMethods.styleMapFamilyName(),
									lambda self, value: self.setProperty_value_languageTag_("styleMapFamilyNames", value, None))
'''
	.. attribute:: windowsFamily
		windowsFamily

		:type: string
'''

GSInstance.windowsStyle = property(lambda self: self.pyobjc_instanceMethods.styleMapStyleName(),
								   lambda self, value: self.setProperty_value_languageTag_("styleMapStyleNames", value, None))
'''
	.. attribute:: windowsStyle
		This is computed from "isBold" and "isItalic". Read-only.

		:type: string
'''

GSInstance.windowsLinkedToStyle = property(lambda self: self.pyobjc_instanceMethods.windowsLinkedToStyle_(None)[0])
'''
	.. attribute:: windowsLinkedToStyle
		windowsLinkedToStyle. Read-only.

		:type: string
'''

GSInstance.fontName = property(lambda self: self.pyobjc_instanceMethods.fontName_(None)[0],
							   lambda self, value: self.setProperty_value_languageTag_("postscriptFontName", value, None))
'''
	.. attribute:: fontName
		fontName (postscriptFontName)

		:type: string
'''

GSInstance.fullName = property(lambda self: self.pyobjc_instanceMethods.fullName_(None)[0],
							   lambda self, value: self.setProperty_value_languageTag_("postscriptFullName", value, None))
'''
	.. attribute:: fullName
		fullName (postscriptFullName)

		:type: string
'''

GSInstance.compatibleFullName = property(lambda self: self.defaultPropertyForName_("compatibleFullNames"),
										 lambda self, value: self.setProperty_value_languageTag_("compatibleFullNames", value, None))
'''
	.. attribute:: compatibleFullName
		This accesses the default value only. The localisations can be accessed by :attr:`GSInstance.properties`

		:type: str
		
		.. versionadded:: 3.0.3
'''

GSInstance.compatibleFullNames = property(lambda self: FontInfoPropertiesProxy(self, "compatibleFullNames"))

'''
	.. attribute:: compatibleFullNames
		This accesses all localized compatibleFullNames values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			Instance.compatibleFullNames["ENG"] = "MyFont Condensed Bold"

		.. versionadded:: 3.0.3
'''

GSInstance.copyright = property(lambda self: self.defaultPropertyForName_("copyrights"),
							    lambda self, value: self.setProperty_value_languageTag_("copyrights", value, None))
'''
	.. attribute:: copyright
		This accesses the default value only. The localisations can be accessed by :attr:`GSInstance.properties`

		:type: str
		
		.. versionadded:: 3.0.2
'''

GSInstance.copyrights = property(lambda self: FontInfoPropertiesProxy(self, "copyrights"))

'''
	.. attribute:: copyrights
		This accesses all localized copyright values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			Instance.copyrights["ENG"] = "All rights reserved"

		
		.. versionadded:: 3.0.3
'''

GSInstance.description = property(lambda self: self.defaultPropertyForName_("descriptions"),
								  lambda self, value: self.setProperty_value_languageTag_("descriptions", value, None))
'''
	.. attribute:: description
		This accesses the default value only. The localisations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.descriptions = property(lambda self: FontInfoPropertiesProxy(self, "descriptions"))

'''
	.. attribute:: descriptions
		This accesses all localized description values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			Instance.descriptions["ENG"] = "This is my description"

		.. versionadded:: 3.0.3
'''
GSInstance.designer = property(lambda self: self.defaultPropertyForName_("designers"),
							   lambda self, value: self.setProperty_value_languageTag_("designers", value, None))
'''
	.. attribute:: designer
		This accesses the default value only. The localisations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.2
'''
GSInstance.designerURL = property(lambda self: self.defaultPropertyForName_("designerURL"),
								  lambda self, value: self.setProperty_value_languageTag_("designerURL", value, None))
'''
	.. attribute:: designerURL

		:type: str

		.. versionadded:: 3.0.2
'''

GSInstance.designers = property(lambda self: FontInfoPropertiesProxy(self, "designers"))

'''
	.. attribute:: designers
		This accesses all localized designer values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			Instance.designers["ENG"] = "John Smith"

		.. versionadded:: 3.0.3
'''

GSInstance.familyName = property(lambda self: self.defaultPropertyForName_("familyNames"),
								 lambda self, value: self.setProperty_value_languageTag_("familyNames", value, None))
'''
	.. attribute:: familyName
		familyName

		:type: string
'''

GSInstance.familyNames = property(lambda self: FontInfoPropertiesProxy(self, "familyNames"))
'''
	.. attribute:: familyNames
		This accesses all localized family name values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			Instance.familyNames["ENG"] = "MyFamilyName"

		.. versionadded:: 3.0.3
'''

GSInstance.license = property(lambda self: self.defaultPropertyForName_("licenses"),
							  lambda self, value: self.setProperty_value_languageTag_("licenses", value, None))
'''
	.. attribute:: license
		This accesses the default value only. The localisations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.licenses = property(lambda self: FontInfoPropertiesProxy(self, "licenses"))
'''
	.. attribute:: licenses
		This accesses all localized family name values.
		For details :attr:`GSInstance.properties`

		:type: dict
		.. code-block:: python
			Instance.licenses["ENG"] = "This font may be installed on all of your machines and printers, but you may not sell or give these fonts to anyone else."

		.. versionadded:: 3.0.3
'''

GSInstance.manufacturer = property(lambda self: self.defaultPropertyForName_("manufacturers"),
								   lambda self, value: self.setProperty_value_languageTag_("manufacturers", value, None))

'''
	.. attribute:: manufacturer
		This accesses the default value only. The localisations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.2
'''

GSInstance.manufacturers = property(lambda self: FontInfoPropertiesProxy(self, "manufacturers"))

'''
	.. attribute:: manufacturers
		This accesses all localized family name values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			Instance.manufacturers["ENG"] = "My English Corporation"

		.. versionadded:: 3.0.3
'''

GSInstance.preferredFamilyName = property(lambda self: self.defaultPropertyForName_("preferredFamilyNames"),
										  lambda self, value: self.setProperty_value_languageTag_("preferredFamilyNames", value, None))

'''
	.. attribute:: preferredFamilyName
		This accesses the default value only. The localisations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.preferredFamilyNames = property(lambda self: FontInfoPropertiesProxy(self, "preferredFamilyNames"))

'''
	.. attribute:: preferredFamilyNames
		This accesses all localized designer values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			Instance.preferredFamilyNames["ENG"] = "MyFamilyName"

		.. versionadded:: 3.0.3
'''

GSInstance.preferredSubfamilyName = property(lambda self: self.defaultPropertyForName_("preferredSubfamilyNames"),
											 lambda self, value: self.setProperty_value_languageTag_("preferredSubfamilyNames", value, None))
'''
	.. attribute:: preferredSubfamilyName
		preferredSubfamilyName

		:type: string
'''

GSInstance.preferredSubfamilyNames = property(lambda self: FontInfoPropertiesProxy(self, "preferredSubfamilyNames"))

'''
	.. attribute:: preferredSubfamilyNames
		This accesses all localized designer values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			Instance.preferredSubfamilyNames["ENG"] = "Regular"

		.. versionadded:: 3.0.3
'''

GSInstance.sampleText = property(lambda self: self.defaultPropertyForName_("sampleTexts"),
								 lambda self, value: self.setProperty_value_languageTag_("sampleTexts", value, None))

'''
	.. attribute:: sampleText
		This accesses the default value only. The localisations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.sampleTexts = property(lambda self: FontInfoPropertiesProxy(self, "sampleTexts"))

'''
	.. attribute:: sampleTexts
		This accesses all localized designer values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			Instance.sampleTexts["ENG"] = "This is my sample text"

		.. versionadded:: 3.0.3
'''
 

GSInstance.styleMapFamilyName = property(lambda self: self.defaultPropertyForName_("styleMapFamilyNames"),
										 lambda self, value: self.setProperty_value_languageTag_("styleMapFamilyNames", value, None))
'''
	.. attribute:: styleMapFamilyName
		This accesses the default value only. The localisations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.styleMapFamilyNames = property(lambda self: FontInfoPropertiesProxy(self, "styleMapFamilyNames"))

'''
	.. attribute:: styleMapFamilyNames
		This accesses all localized designer values.
		For details :attr:`GSInstance.properties`

		:type: dict


		.. code-block:: python
			Instance.styleMapFamilyNames["ENG"] = "MyFamily Bold"

		.. versionadded:: 3.0.3
'''

GSInstance.styleMapStyleName = property(lambda self: self.defaultPropertyForName_("styleMapStyleNames"),
										lambda self, value: self.setProperty_value_languageTag_("styleMapStyleNames", value, None))

'''
	.. attribute:: styleMapStyleName
		This accesses the default value only. The localisations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.styleMapStyleNames = property(lambda self: FontInfoPropertiesProxy(self, "styleMapStyleNames"))

'''
	.. attribute:: styleMapStyleNames
		This accesses all localized designer values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			Instance.styleMapStyleNames["ENG"] = "Bold"

		.. versionadded:: 3.0.3
'''

GSInstance.styleName = property(lambda self: self.defaultPropertyForName_("styleNames"),
								lambda self, value: self.setProperty_value_languageTag_("styleNames", value, None))

'''
	.. attribute:: styleName
		This accesses the default value only. The localisations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.styleNames = property(lambda self: FontInfoPropertiesProxy(self, "styleNames"))

'''
	.. attribute:: styleNames
		This accesses all localized styleName values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			Instance.styleNames["ENG"] = "Regular"

		.. versionadded:: 3.0.3
'''

GSInstance.trademark = property(lambda self: self.defaultPropertyForName_("trademarks"),
								lambda self, value: self.setProperty_value_languageTag_("trademarks", value, None))
'''
	.. attribute:: trademark
		This accesses the default value only. The localisations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.trademarks = property(lambda self: FontInfoPropertiesProxy(self, "trademarks"))

'''
	.. attribute:: trademarks
		This accesses all localized trademark values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			Instance.trademarks["ENG"] = "ThisFont is a trademark by MyFoundry.com"

		.. versionadded:: 3.0.3
'''

GSInstance.variableStyleName = property(lambda self: self.defaultPropertyForName_("variableStyleNames"),
										lambda self, value: self.setProperty_value_languageTag_("variableStyleNames", value, None))

'''
	.. attribute:: variableStyleName
		This accesses the default value only. The localisations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.variableStyleNames = property(lambda self: FontInfoPropertiesProxy(self, "variableStyleNames"))

'''
	.. attribute:: variableStyleNames
		This accesses all localized variableStyleName values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			Instance.variableStyleNames["ENG"] = "Roman"

		.. versionadded:: 3.0.3
'''

GSInstance.manufacturerURL = property(lambda self: self.defaultPropertyForName_("manufacturerURL"),
									  lambda self, value: self.setProperty_value_languageTag_("manufacturerURL", value, None))
'''
	.. attribute:: manufacturerURL

		:type: str

		.. versionadded:: 3.0.2
'''

GSInstance.font = property(lambda self: self.pyobjc_instanceMethods.font(),
						   lambda self, value: self.setFont_(value))
'''
	.. attribute:: font
		Reference to the :class:`GSFont` object that contains the instance. Normally that is set by the app, only if the instance is not actually added to the font, then set this manually.

		:type: GSFont

		.. versionadded:: 2.5.1
'''

GSInstance.customParameters = property(lambda self: CustomParametersProxy(self),
									   lambda self, value: CustomParametersProxy(self).setter(value))

'''
	.. attribute:: customParameters
		The custom parameters. List of :class:`GSCustomParameter` objects. You can access them by name or by index.

		:type: list, dict

		.. code-block:: python
			# access all parameters
			for parameter in font.instances[0].customParameters:
				print(parameter)

			# set a parameter
			font.instances[0].customParameters['hheaLineGap'] = 10

			# delete a parameter
			del(font.instances[0].customParameters['hheaLineGap'])

'''

GSInstance.userData = property(lambda self: UserDataProxy(self))
'''
	.. attribute:: userData
		A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the data will not be recoverable from the saved file.

		:type: dict

		.. code-block:: python
			# set value
			instance.userData['rememberToMakeCoffee'] = True

			# delete value
			del instance.userData['rememberToMakeCoffee']

'''

GSInstance.tempData = property(lambda self: TempDataProxy(self))

'''
	.. attribute:: tempData
		A dictionary to store data temporarily. Use a unique key. This will not be saved to file. If you need the data persistent, use instance.userData

		:type: dict

		.. code-block:: python
			# set value
			instance.tempData['rememberToMakeCoffee'] = True

			# delete value
			del instance.tempData['rememberToMakeCoffee']
'''

GSInstance.instanceInterpolations = property(lambda self: self.pyobjc_instanceMethods.instanceInterpolations(),
											 lambda self, value: self.setInstanceInterpolations_(value))
'''
	.. attribute:: instanceInterpolations
		A dict that contains the interpolation coefficients for each master.
		This is automatically updated if you change interpolationWeight, interpolationWidth, interpolationCustom. It contains FontMaster IDs as keys and coefficients for that master as values.
		Or, you can set it manually if you set manualInterpolation to True. There is no UI for this, so you need to do that with a script.

		:type: dict
	'''

GSInstance.manualInterpolation = property(lambda self: bool(self.pyobjc_instanceMethods.manualInterpolation()),
										  lambda self, value: self.setManualInterpolation_(value))
'''
	.. attribute:: manualInterpolation
		Disables automatic calculation of instanceInterpolations
		This allows manual setting of instanceInterpolations.

		:type: bool
	'''

GSInstance.interpolatedFontProxy = property(lambda self: self.pyobjc_instanceMethods.interpolatedFont())

'''
	.. attribute:: interpolatedFontProxy
		a proxy font that acts similar to a normal font object but only interpolates the glyphs you ask it for.

		It is not properly wrapped yet. So you need to use the ObjectiveC methods directly.

'''

def Instance_FontObject(self):
	return self.font.generateInstance_error_(self, None)[0]

GSInstance.interpolatedFont = property(lambda self: Instance_FontObject(self))

'''
	.. attribute:: interpolatedFont
		Returns a ready interpolated :class:`GSFont` object representing this instance. Other than the source object, this interpolated font will contain only one master and one instance.

		Note: When accessing several properties of such an instance consecutively, it is advisable to create the instance once into a variable and then use that. Otherwise, the instance object will be completely interpolated upon each access. See sample below.

		:type: :class:`GSFont`

		.. code-block:: python
			# create instance once
			interpolated = Glyphs.font.instances[0].interpolatedFont

			# then access it several times
			print(interpolated.masters)
			print(interpolated.instances)

			(<GSFontMaster "Light" width 100.0 weight 75.0>)
			(<GSInstance "Web" width 100.0 weight 75.0>)

'''

'''
	**Functions**

	.. function:: generate([Format, FontPath, AutoHint, RemoveOverlap, UseSubroutines, UseProductionNames, Containers, DecomposeSmartStuff])

		Exports the instance. All parameters are optional.

		:param str The format of the outlines: :const:`OTF` or :const:`TTF`. Default: OTF
		:param str FontPath: The destination path for the final fonts. If None, it uses the default location set in the export dialog
		:param bool AutoHint: If autohinting should be applied. Default: True
		:param bool RemoveOverlap: If overlaps should be removed. Default: True
		:param bool UseSubroutines: If to use subroutines for CFF. Default: True
		:param bool UseProductionNames: If to use production names. Default: True
		:param bool Containers: list of container formats. Use any of the following constants: :const:`PLAIN`, :const:`WOFF`, :const:`WOFF2`, :const:`EOT`. Default: PLAIN
		:param bool DecomposeSmartStuff: If smart components should be decomposed. Default: True
		:return: On success, True; on failure, error message.
		:rtype: bool/list

		.. code-block:: python
			# export all instances as OpenType (.otf) and WOFF2 to user’s font folder

			exportFolder = '/Users/myself/Library/Fonts'

			for instance in Glyphs.font.instances:
				instance.generate(FontPath = exportFolder, Containers = [PLAIN, WOFF2])

			Glyphs.showNotification('Export fonts', 'The export of %s was successful.' % (Glyphs.font.familyName))
'''

class _ExporterDelegate_(NSObject):
	def init(self):
		self = super(_ExporterDelegate_, self).init()
		self.result = True
		return self

	def collectResult_instance_(self, Error, instancePath): # Error might be a NSString or a NSError
		if Error.__class__.__name__ == "NSError":
			String = Error.localizedDescription()
			if Error.localizedRecoverySuggestion() and Error.localizedRecoverySuggestion().length() > 0:
				String = String.stringByAppendingString_(Error.localizedRecoverySuggestion())
			Error = String
		self.result = Error

def __Instance_Export__(self, Format=OTF, FontPath=None, AutoHint=True, RemoveOverlap=True, UseSubroutines=True, UseProductionNames=True, Containers=None, DecomposeSmartStuff=True):

	if Format not in [OTF, WOFF, WOFF2, TTF, UFO, VARIABLE]:
		raise KeyError('The font format is not supported: %s (only \'OTF\' and \'TTF\')' % Format)
	
	if self.type == INSTANCETYPEVARIABLE and Format == UFO:
		raise KeyError('Variable instances can only be exported as TTF')
	
	if FontPath and FontPath.startswith("~"):
		FontPath = os.path.expanduser(FontPath)

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
			raise ValueError('Please provide a FontPath')
		instanceFont = self.interpolatedFont
		return instanceFont.export(Format=Format, FontPath=FontPath, UseProductionNames=UseProductionNames, DecomposeSmartStuff=DecomposeSmartStuff)
	else:
		Font = self.font
		if self.type == INSTANCETYPEVARIABLE:
			Format = VARIABLE
			RemoveOverlap = False
		if FontPath is None:
			FontPath = NSUserDefaults.standardUserDefaults().objectForKey_("OTFExportPath")
		if Format == OTF:
			Format = GSOutlineFormatCFF
		elif Format == TTF:
			Format = GSOutlineFormatTrueType
		elif Format == VARIABLE:
			Format = GSOutlineFormatVariableTT
		else:
			raise KeyError("Invalid format: %" % Format)
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
			self.lastExportedFilePath = Exporter.tempFontPath()
		else:
			self.lastExportedFilePath = None
		return Delegate.result

GSInstance.generate = python_method(__Instance_Export__)

def __Font_Export__(self, Format=OTF, Instances=None, FontPath=None, AutoHint=True, RemoveOverlap=True, UseSubroutines=True, UseProductionNames=True, Containers=None, DecomposeSmartStuff=True):
	if Format not in [OTF, WOFF, WOFF2, TTF, VARIABLE, UFO]:
		raise KeyError('The font format is not supported: %s (only \'OTF\' and \'TTF\')' % Format)

	if FontPath is None:
		FontPath = Glyphs.defaults["OTFExportPath"]

	if FontPath and FontPath.startswith("~"):
		FontPath = os.path.expanduser(FontPath)

	if Format == UFO:
		Font = self.font()
		GlyphsFileFormatUFO = objc.lookUpClass("GlyphsFileFormatUFO")
		ufoWriter = GlyphsFileFormatUFO.new()
		ufoWriter.setConvertNames_(UseProductionNames)
		ufoWriter.setDecomposeSmartStuff_(DecomposeSmartStuff)
		ufoWriter.setExportOptions_({"SeletedMasterIndexes": NSIndexSet.indexSetWithIndexesInRange_(NSRange(0, len(Font.masters)))})
		result = ufoWriter.exportFont_toDirectory_error_(Font, NSURL.fileURLWithPath_(FontPath), None)
		return result
	else:
		if not Instances:
			Instances = []
			for instance in self.instances:
				if not instance.active:
					continue
				if (Format == VARIABLE) == (instance.type == INSTANCETYPESINGLE):
					continue
				Instances.append(instance)
		if len(Instances) == 0:
			instanceType = INSTANCETYPEVARIABLE if Format == VARIABLE else INSTANCETYPESINGLE
			instance = GSInstance.alloc().initWithType_(instanceType)
			instance.font = self
			Instances.append(instance)
		allResults = []
		for i in Instances:
			result = i.generate(Format=Format, FontPath=FontPath, AutoHint=AutoHint, RemoveOverlap=RemoveOverlap, UseSubroutines=UseSubroutines, UseProductionNames=UseSubroutines, Containers=Containers)
			allResults.append(result)
		return allResults

GSFont.export = python_method(__Font_Export__)

GSInstance.lastExportedFilePath = property(lambda self: self.tempDataForKey_("lastExportedFilePath"), 
										   lambda self, value: self.setTempData_forKey_(value, "lastExportedFilePath"))

'''
	.. attribute:: lastExportedFilePath
		Returns a ready interpolated :class:`GSFont` object representing this instance. Other than the source object, this interpolated font will contain only one master and one instance.

		Note: When accessing several properties of such an instance consecutively, it is advisable to create the instance once into a variable and then use that. Otherwise, the instance object will be completely interpolated upon each access. See sample below.

		:type: str

		.. code-block:: python
			# create instance once
			interpolated = Glyphs.font.instances[0].interpolatedFont

			# then access it several times
			print(interpolated.masters)
			print(interpolated.instances)

			(<GSFontMaster "Light" width 100.0 weight 75.0>)
			(<GSInstance "Web" width 100.0 weight 75.0>)

	'''

def __GSInstance_AddInstanceAsMaster__(self):
	self.font.addFontAsNewMaster_(self.interpolatedFont.masters[0])

GSInstance.addAsMaster = python_method(__GSInstance_AddInstanceAsMaster__)

'''
	.. function:: addAsMaster()

		Add this instance as a new master to the font. Identical to "Instance as Master" menu item in the Font Info’s Instances section.
	
		.. versionadded:: 2.6.2
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


def _________________________(): pass
def ____GSCustomParameter____(): pass
def _________________________(): pass


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
	:param value: The value
'''

GSCustomParameter.__new__ = staticmethod(GSObject__new__)

def CustomParameter__init__(self, name, value):
	self.setName_(name)
	self.setValue_(value)

GSCustomParameter.__init__ = python_method(CustomParameter__init__)

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

GSCustomParameter.name = property(lambda self: self.pyobjc_instanceMethods.name(),
								  lambda self, value: self.setName_(value))
'''
	.. attribute:: name

		:type: str
'''
GSCustomParameter.value = property(lambda self: self.pyobjc_instanceMethods.value(),
								   lambda self, value: self.setValue_(value))
'''
	.. attribute:: value

		:type: str, list, dict, int, float
'''
GSCustomParameter.parent = property(lambda self: self.pyobjc_instanceMethods.parent())
'''
	.. attribute:: parent

		:type: GSFont, GSFontMaster or GSInstance
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

def _______________(): pass
def ____GSClass____(): pass
def _______________(): pass

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
GSClass.__init__ = python_method(Class__init__)

def Class__repr__(self):
	return "<GSClass \"%s\">" % (self.name)
GSClass.__repr__ = python_method(Class__repr__)

GSClass.__eq__ = python_method(lambda self, other: self.isEqual_(other))

GSClass.mutableCopyWithZone_ = GSObject__copy__

GSClass.name = property(lambda self: self.pyobjc_instanceMethods.name(),
						lambda self, value: self.setName_(value))
'''
	.. attribute:: name
		The class name

		:type: str
'''

GSClass.code = property(lambda self: self.pyobjc_instanceMethods.code(),
						lambda self, value: self.setCode_(value))
'''
	.. attribute:: code
		A string with space separated glyph names.

		:type: str
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

GSClass.tempData = property(lambda self: TempDataProxy(self))

'''
	.. attribute:: tempData
		A dictionary to store data temporarily. Use a unique key. This will not be saved to file. If you need the data persistent, use class.userData

		:type: dict

		.. code-block:: python
			# set value
			class.tempData['rememberToMakeCoffee'] = True

			# delete value
			del class.tempData['rememberToMakeCoffee']
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

def _______________________(): pass
def ____GSFeaturePrefix____(): pass
def _______________________(): pass

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
GSFeaturePrefix.__init__ = python_method(Class__init__)

def FeaturePrefix__repr__(self):
	return "<GSFeaturePrefix \"%s\">" % (self.name)
GSFeaturePrefix.__repr__ = python_method(FeaturePrefix__repr__)

GSFeaturePrefix.mutableCopyWithZone_ = GSObject__copy__

GSFeaturePrefix.name = property(lambda self: self.pyobjc_instanceMethods.name(),
								lambda self, value: self.setName_(value))
'''
	.. attribute:: name
		The FeaturePrefix name

		:type: str
'''

GSFeaturePrefix.code = property(lambda self: self.pyobjc_instanceMethods.code(),
								lambda self, value: self.setCode_(value))
'''
	.. attribute:: code
		A String containing feature code.

		:type: str
'''

GSFeaturePrefix.automatic = property(lambda self: bool(self.pyobjc_instanceMethods.automatic()),
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

def _________________(): pass
def ____GSFeature____(): pass
def _________________(): pass

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
		self.setTag_(objcObject(name))
	if code is not None:
		self.setCode_(objcObject(code))
GSFeature.__init__ = python_method(Feature__init__)

def Feature__repr__(self):
	return "<GSFeature \"%s\">" % (self.name)
GSFeature.__repr__ = python_method(Feature__repr__)

GSFeature.__eq__ = python_method(lambda self, other: self.isEqualToFeature_(other))

GSFeature.mutableCopyWithZone_ = GSObject__copy__

GSFeature.name = property(lambda self: self.tag(),
						  lambda self, value: self.setTag_(value))
'''
	.. attribute:: name
		The feature name

		:type: str
'''

GSFeature.code = property(lambda self: self.pyobjc_instanceMethods.code(),
						  lambda self, value: self.setCode_(value))
'''
	.. attribute:: code
		The Feature code in Adobe FDK syntax.

		:type: str
'''
GSFeature.automatic = property(lambda self: bool(self.pyobjc_instanceMethods.automatic()),
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

		:type: str
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

GSFeature.tempData = property(lambda self: TempDataProxy(self))

'''
	.. attribute:: tempData
		A dictionary to store data temporarily. Use a unique key. This will not be saved to file. If you need the data persistent, use feature.userData

		:type: dict

		.. code-block:: python
			# set value
			feature.tempData['rememberToMakeCoffee'] = True

			# delete value
			del feature.tempData['rememberToMakeCoffee']
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

def ______________________(): pass
def ____GSSubstitution____(): pass
def ______________________(): pass


"""

############ NOCH NICHT DOKUMENTIERT WEIL NOCH NICHT AUSGEREIFT ############

"""

GSSubstitution.__new__ = staticmethod(GSObject__new__)

def Substitution__init__(self):
	pass
GSSubstitution.__init__ = python_method(Substitution__init__)

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


def _______________(): pass
def ____GSGlyph____(): pass
def _______________(): pass


'''

:mod:`GSGlyph`
===============================================================================

Implementation of the glyph object.

For details on how to access these glyphs, please see :class:`GSFont.glyphs`

.. class:: GSGlyph([name, autoName=True])

	:param name: The glyph name
	:param autoName: if the name should be converted to nice name

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
		case
		storeCase
		script
		storeScript
		productionName
		storeProductionName
		sortName
		sortNameKeep
		storeSortName
		glyphInfo
		leftKerningGroup
		rightKerningGroup
		leftKerningKey
		topKerningGroup
		bottomKerningKey
		rightKerningKey
		topKerningKey
		bottomKerningKey
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
		tags
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
GSGlyph.__new__.__name__ = "__new__"

def Glyph__init__(self, name=None, autoName=True):
	if name and isString(name):
		if not autoName:
			self.setName_changeName_(name, autoName)
		else:
			self.setName_(name)
GSGlyph.__init__ = python_method(Glyph__init__)

def Glyph__repr__(self):
	return "<GSGlyph \"%s\" with %s layers>" % (self.name, len(self.layers))
GSGlyph.__repr__ = python_method(Glyph__repr__)

GSGlyph.mutableCopyWithZone_ = GSObject__copy__
GSGlyph.__copy__ = python_method(GSObject__copy__)
GSGlyph.__deepcopy__ = python_method(GSObject__copy__)

GSGlyph.__eq__ = python_method(lambda self, other: self.isEqualToGlyph_(other))

GSGlyph.parent = property(lambda self: self.pyobjc_instanceMethods.parent(),
						  lambda self, value: self.setParent_(value))
GSGlyph.font = GSGlyph.parent
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
	elif (self.parent and name not in self.parent.glyphs) or not self.parent:
		self.setName_changeName_update_(name, False, True)
	else:
		raise NameError('The glyph name \"%s\" already exists in the font.' % name)

GSGlyph.name = property(lambda self: self.pyobjc_instanceMethods.name(),
						lambda self, value: GSGlyph_setName(self, value))
'''
	.. attribute:: name
		The name of the glyph. It will be converted to a "nice name" (afii10017 to A-cy) (you can disable this behavior in font info or the app preference)

		:type: str
'''

GSGlyph.unicode = property(lambda self: self.pyobjc_instanceMethods.unicode(),
						   lambda self, value: self.setUnicode_(value))
'''
	.. attribute:: unicode
		String with the hex Unicode value of glyph, if encoded.

		:type: str
'''
def __glyph__unicode__(self):
	codes = self.pyobjc_instanceMethods.unicodes()
	if codes and codes.count() > 0:
		return codes.array()
	return None

GSGlyph.unicodes = property(lambda self: __glyph__unicode__(self),
							lambda self, value: self.setUnicodes_(value))
'''
	.. attribute:: unicodes
		List of Strings‚ with the hex Unicode values of glyph, if encoded.

		:type: list
'''

GSGlyph.production = property(lambda self: self.pyobjc_instanceMethods.production(),
							  lambda self, value: self.setProduction_(self, value))

GSGlyph.string = property(lambda self: self.charString())
'''
	.. attribute:: string
		String representation of glyph, if encoded.
		This is similar to the string representation that you get when copying glyphs into the clipboard.

		:type: str
'''

GSGlyph.id = property(lambda self: str(self.pyobjc_instanceMethods.id()),
					  lambda self, value: self.setId_(value))
'''
	.. attribute:: id
		An unique identifier for each glyph

		:type: string
'''

GSGlyph.locked = property(lambda self: bool(self.pyobjc_instanceMethods.locked()),
						  lambda self, value: self.setLocked_(value))
'''
	.. attribute:: locked
		If the glyph is locked
		TODO

		:type: bool
'''

GSGlyph.category = property(lambda self: self.pyobjc_instanceMethods.category(),
							lambda self, value: self.setCategory_(value))
'''
	.. attribute:: category
		The category of the glyph. e.g. ‘Letter’, ‘Symbol’
		Setting only works if :attr:`GSGlyph.storeCategory` is set (see below).

		:type: str
'''

GSGlyph.storeCategory = property(lambda self: bool(self.pyobjc_instanceMethods.storeCategory()),
								 lambda self, value: self.setStoreCategory_(value))
'''
	.. attribute:: storeCategory
		Set to True in order to manipulate the :attr:`GSGlyph.category` of the glyph (see above).
		Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.

		:type: bool
'''

GSGlyph.subCategory = property(lambda self: self.pyobjc_instanceMethods.subCategory(),
							   lambda self, value: self.setSubCategory_(value))
'''
	.. attribute:: subCategory
		The subCategory of the glyph. e.g. ‘Currency’, ‘Math’
		Setting it only works if :attr:`GSGlyph.storeSubCategory` is set (see below).

		:type: str
'''

GSGlyph.storeSubCategory = property(lambda self: bool(self.pyobjc_instanceMethods.storeSubCategory()),
									lambda self, value: self.setStoreSubCategory_(value))
'''
	.. attribute:: storeSubCategory
		Set to True in order to manipulate the :attr:`GSGlyph.subCategory` of the glyph (see above).
		Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.

		:type: bool

'''

GSGlyph.case = property(lambda self: self.pyobjc_instanceMethods.case(),
						lambda self, value: self.setCase_(value))
'''
	.. attribute:: case
		e.g: GSUppercase, GSLowercase, GSSmallcaps

		:type: int
	
		.. versionadded:: 3
'''

GSGlyph.storeCase = property(lambda self: bool(self.pyobjc_instanceMethods.storeCase()),
							 lambda self, value: self.setStoreCase_(value))
'''
	.. attribute:: storeCase
		Set to True in order to manipulate the :attr:`GSGlyph.case` of the glyph (see above).
		Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.

		:type: bool
	
		.. versionadded:: 3
'''

GSGlyph.direction = property(lambda self: self.pyobjc_instanceMethods.direction(),
							 lambda self, value: self.setDirection_(value))
'''
	.. attribute:: direction
		Writing direction.

		Defined constants are: GSLTR (left to right), GSRTL (right to left), GSVertical (right to left, vertical, top to bottom e.g. Chinese, Japanese, Korean) and GSVerticalToRight (left to right, vertical, top to bottom e.g. Mongolian)

		:type: integer

		.. code-block:: python
			glyph.direction = GSRTL

		.. versionadded:: 3
'''

GSGlyph.storeDirection = property(lambda self: bool(self.pyobjc_instanceMethods.storeDirection()),
								  lambda self, value: self.setStoreDirection_(value))
'''
	.. attribute:: storeDirection
		Set to True in order to manipulate the :attr:`GSGlyph.direction` of the glyph (see above).
		Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.

		:type: bool

		.. versionadded:: 3
'''

GSGlyph.script = property(lambda self: self.pyobjc_instanceMethods.script(),
						  lambda self, value: self.setScript_(value))
'''
	.. attribute:: script
		The script of the glyph, e.g., 'latin', 'arabic'.
		Setting only works if :attr:`GSGlyph.storeScript` is set (see below).

		:type: str
'''

GSGlyph.storeScript = property(lambda self: bool(self.pyobjc_instanceMethods.storeScript()),
							   lambda self, value: self.setStoreScript_(value))
'''
	.. attribute:: storeScript
		Set to True in order to manipulate the :attr:`GSGlyph.script` of the glyph (see above).
		Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.

		:type: bool

'''

GSGlyph.productionName = property(lambda self: self.pyobjc_instanceMethods.production(),
								  lambda self, value: self.setProduction_(value))
'''
	.. attribute:: productionName
		The productionName of the glyph.
		Setting only works if :attr:`GSGlyph.storeProductionName` is set (see below).

		:type: str

'''

GSGlyph.storeProductionName = property(lambda self: bool(self.storeProduction()),
									   lambda self, value: self.setStoreProduction_(value))
'''
	.. attribute:: storeProductionName
		Set to True in order to manipulate the :attr:`GSGlyph.productionName` of the glyph (see above).
		Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.

		:type: bool
'''

GSGlyph.tags = property(lambda self: self.mutableArrayValueForKey_("tags"),
						lambda self, value: self.setTags_(value))

'''
	.. attribute:: tags
		store strings that can be used to filter glyphs or build OT-classes with token filters

		:type: list
'''

GSGlyph.glyphInfo = property(lambda self: self.parent.glyphsInfo().glyphInfoForGlyph_(self))
'''
	.. attribute:: glyphInfo
		:class:`GSGlyphInfo` object for this glyph with detailed information.

		:type: :class:`GSGlyphInfo`
'''

GSGlyph.sortName = property(lambda self: self.pyobjc_instanceMethods.sortName(),
							lambda self, value: self.setSortName_(value))
'''
	.. attribute:: sortName
		Alternative name of glyph used for sorting in UI.

		:type: str
'''

GSGlyph.sortNameKeep = property(lambda self: self.pyobjc_instanceMethods.sortNameKeep(),
								lambda self, value: self.setSortNameKeep_(value))
'''
	.. attribute:: sortNameKeep
		Alternative name of glyph used for sorting in UI, when using 'Keep Alternates Next to Base Glyph' from Font Info.
		see :attr:`GSGlyph.storeSortName`
		:type: str
'''

GSGlyph.storeSortName = property(lambda self: bool(self.pyobjc_instanceMethods.storeSortName()),
								 lambda self, value: self.setStoreSortName_(value))
'''
	.. attribute:: storeSortName
		Set to True in order to manipulate the :attr:`GSGlyph.sortName` and :attr:`GSGlyph.sortNameKeep` of the glyph (see above).
		Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.

		:type: bool
'''

def __GSGlyph_glyphDataEntryString__(self):
	Unicode = self.unicode
	if Unicode is None or len(Unicode) < 3:
		Unicode = ""
	Decompose = self.layers[0].componentNamesText()
	if Decompose is not None and len(Decompose) > 0:
		Decompose = 'decompose="%s" ' % Decompose
	else:
		Decompose = ""
	SubCategory = ""
	if self.subCategory != "Other":
		SubCategory = 'subCategory="%s" ' % self.subCategory
	Anchors = self.layers[0].anchors.keys()
	if Anchors is not None and len(Anchors) > 0:
		Anchors = 'anchors="%s" ' % ", ".join(sorted(Anchors))
	else:
		Anchors = ""
	GlyphInfo = self.glyphInfo
	Accents = None
	if GlyphInfo is not None:
		Accents = GlyphInfo.accents
	if Accents is not None and len(Accents) > 0:
		Accents = 'accents="%s" ' % ", ".join(sorted(Accents))
	else:
		Accents = ""
	Production = ""
	if self.productionName is not None and len(self.productionName) > 0:
		Production = self.productionName
	else:
		Production = Glyphs.productionGlyphName(self.name)
	if len(Production) > 0:
		Production = 'production="%s" ' % Production
	else:
		Production = ""
	if self.note is not None and len(self.note) > 0:
		Production += ' altNames="%s" ' % self.note
	return '	<glyph unicode="%s" name="%s" %scategory="%s" %sscript="%s" description="" %s%s%s/>' % (Unicode, self.name, Decompose, self.category, SubCategory, self.script, Production, Anchors, Accents)

GSGlyph.glyphDataEntryString = python_method(__GSGlyph_glyphDataEntryString__)

GSGlyph.leftKerningGroup = property(lambda self: self.pyobjc_instanceMethods.leftKerningGroup(),
									lambda self, value: self.setLeftKerningGroup_(NSStr(value)))
'''
	.. attribute:: leftKerningGroup
		The leftKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.

		:type: str
'''
GSGlyph.rightKerningGroup = property(lambda self: self.pyobjc_instanceMethods.rightKerningGroup(),
									 lambda self, value: self.setRightKerningGroup_(NSStr(value)))
'''
	.. attribute:: rightKerningGroup
		The rightKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.

		:type: str'''

GSGlyph.topKerningGroup = property(lambda self: self.pyobjc_instanceMethods.topKerningGroup(),
								   lambda self, value: self.setTopKerningGroup_(NSStr(value)))
'''
	.. attribute:: topKerningGroup
		The topKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.

		:type: str'''

GSGlyph.bottomKerningGroup = property(lambda self: self.pyobjc_instanceMethods.bottomKerningGroup(),
									  lambda self, value: self.setBottomKerningGroup_(NSStr(value)))
'''
	.. attribute:: bottomKerningGroup
		The bottomKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.

		:type: str'''

def GSGlyph__leftKerningKey(self):
	if self.leftKerningGroupId():
		return self.leftKerningGroupId()
	else:
		return self.name

GSGlyph.leftKerningKey = property(lambda self: GSGlyph__leftKerningKey(self))

'''
	.. attribute:: leftKerningKey
		The key to be used with the kerning functions (:meth:`GSFont.kerningForPair()`, :meth:`GSFont.setKerningForPair()`, :meth:`GSFont.removeKerningForPair()`).

		If the glyph has a :attr:`leftKerningGroup <GSGlyph.leftKerningGroup>` attribute, the internally used `@MMK_R_xx` notation will be returned (note that the R in there stands for the right side of the kerning pair for LTR fonts, which corresponds to the left kerning group of the glyph). If no group is given, the glyph’s name will be returned.

		:type: string

		.. code-block:: python
			# Set kerning for 'T' and all members of kerning class 'a'
			# For LTR fonts, always use the .rightKerningKey for the first (left) glyph of the pair, .leftKerningKey for the second (right) glyph.
			font.setKerningForPair(font.selectedFontMaster.id, font.glyphs['T'].rightKerningKey, font.glyphs['a'].leftKerningKey, -60)

			# which corresponds to:
			font.setKerningForPair(font.selectedFontMaster.id, 'T', '@MMK_R_a', -60)

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

		If the glyph has a :attr:`rightKerningGroup <GSGlyph.rightKerningGroup>` attribute, the internally used `@MMK_L_xx` notation will be returned (note that the L in there stands for the left side of the kerning pair for LTR fonts, which corresponds to the right kerning group of the glyph). If no group is given, the glyph’s name will be returned.

		See above for an example.

		:type: string

		.. versionadded:: 2.4
'''

def GSGlyph__topKerningKey(self):
	if self.topKerningGroupId():
		return self.topKerningGroupId()
	else:
		return self.name

GSGlyph.topKerningKey = property(lambda self: GSGlyph__topKerningKey(self))

'''
	.. attribute:: topKerningKey
		The key to be used with the kerning functions (:meth:`GSFont.kerningForPair()`, :meth:`GSFont.setKerningForPair()`, :meth:`GSFont.removeKerningForPair()`).

		.. versionadded:: 3
'''

def GSGlyph__bottomKerningKey(self):
	if self.bottomKerningGroupId():
		return self.bottomKerningGroupId()
	else:
		return self.name

GSGlyph.bottomKerningKey = property(lambda self: GSGlyph__bottomKerningKey(self))

'''
	.. attribute:: bottomKerningKey
		The key to be used with the kerning functions (:meth:`GSFont.kerningForPair()`, :meth:`GSFont.setKerningForPair()`, :meth:`GSFont.removeKerningForPair()`).

		.. versionadded:: 3
'''

GSGlyph.leftMetricsKey = property(lambda self: self.pyobjc_instanceMethods.leftMetricsKey(),
								  lambda self, value: self.setLeftMetricsKey_(NSStr(value)))
'''
	.. attribute:: leftMetricsKey
		The leftMetricsKey of the glyph. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str
'''

GSGlyph.rightMetricsKey = property(lambda self: self.pyobjc_instanceMethods.rightMetricsKey(),
								   lambda self, value: self.setRightMetricsKey_(NSStr(value)))
'''
	.. attribute:: rightMetricsKey
		The rightMetricsKey of the glyph. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str
'''

GSGlyph.widthMetricsKey = property(lambda self: self.pyobjc_instanceMethods.widthMetricsKey(),
								   lambda self, value: self.setWidthMetricsKey_(NSStr(value)))
'''
	.. attribute:: widthMetricsKey
		The widthMetricsKey of the glyph. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str
'''

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
		colorValue = NSColor.colorWithDeviceRed_green_blue_alpha_(*colorValue[:4])
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

'''

GSGlyph.note = property(lambda self: self.pyobjc_instanceMethods.note(),
						lambda self, value: self.setNote_(value))
'''
	.. attribute:: note

		:type: str
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
		Return True when all layers in this glyph are compatible (same components, anchors, paths etc.)

		:type: bool
'''

GSGlyph.userData = property(lambda self: UserDataProxy(self))
'''
	.. attribute:: userData
		A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the data will not be recoverable from the saved file.

		:type: dict

		.. code-block:: python
			# set value
			glyph.userData['rememberToMakeCoffee'] = True

			# delete value
			del glyph.userData['rememberToMakeCoffee']
'''

GSGlyph.smartComponentAxes = property(lambda self: GlyphSmartComponentAxesProxy(self),
									  lambda self, value: GlyphSmartComponentAxesProxy(self).setter(value))
'''
	.. attribute:: smartComponentAxes
		A list of :class:`GSSmartComponentAxis` objects.

		These are the axis definitions for the interpolations that take place within the Smart Components. Corresponds to the ‘Properties’ tab of the glyph’s ‘Show Smart Glyph Settings’ dialog.

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
		Change date when glyph was last changed as datetime.

		Check Python’s :mod:`time` module for how to use the timestamp.
'''

'''

	**Functions**
'''

def __BeginUndo__(self):
	self.undoManager().beginUndoGrouping()

GSGlyph.beginUndo = python_method(__BeginUndo__)

'''
	.. function:: beginUndo()

		Call this before you do a longer running change to the glyph. Be extra careful to call :meth:`glyph.endUndo() <GSGlyph.endUndo()>` when you are finished.

'''

def __EndUndo__(self):
	self.undoManager().endUndoGrouping()
GSGlyph.endUndo = python_method(__EndUndo__)

'''
	.. function:: endUndo()

		This closes a undo group that was opened by a previous call of :meth:`glyph.beginUndo() <GSGlyph.beginUndo()>` Make sure that you call this for each `beginUndo()` call.

'''

def __updateGlyphInfo__(self, changeName=True):
	if self.parent is not None:
		self.parent.glyphsInfo().updateGlyphInfo_changeName_(self, changeName)
	else:
		GSGlyphsInfo.sharedManager().updateGlyphInfo_changeName_(self, changeName)
GSGlyph.updateGlyphInfo = python_method(__updateGlyphInfo__)

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

GSGlyph.duplicate = python_method(Glyph_Duplicate)

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

def _______________(): pass
def ____GSLayer____(): pass
def _______________(): pass


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
		attributes
		color
		colorObject
		shapes
		guides
		annotations
		hints
		anchors
		components
		paths
		selection
		LSB
		RSB
		TSB
		BSB
		width
		vertWidth
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
GSLayer.__new__.__name__ = "__new__"

def Layer__init__(self):
	pass
GSLayer.__init__ = python_method(Layer__init__)

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

GSLayer.__eq__ = python_method(lambda self, other: self.isEqualToLayer_(other))

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
						lambda self, value: self.setName_(value), doc="Name of layer.")

GSBackgroundLayer.name = property(lambda self: self.pyobjc_instanceMethods.name(),
								  lambda self, value: self.setName_(value))

'''
	.. attribute:: name
		Name of layer

		:type: str
'''

GSLayer.master = property(lambda self: self.associatedFontMaster())
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

		.. code-block:: python
			# add a new layer
			newLayer = GSLayer()
			newLayer.name = '{125, 100}' # (example for glyph-level intermediate master)

			# you may set the master ID that this layer will be associated with, otherwise the first master will be used
			newLayer.associatedMasterId = font.masters[-1].id # attach to last master
			font.glyphs['a'].layers.append(newLayer)

		:type: str

'''

GSLayer.layerId = property(lambda self: self.pyobjc_instanceMethods.layerId(),
						   lambda self, value: self.setLayerId_(value))
'''
	.. attribute:: layerId
		The unique layer ID is used to access the layer in the :class:`glyphs <GSGlyph>` layer dictionary.

		For master layers this should be the id of the :class:`fontMaster <GSFontMaster>`.
		It could look like this: :samp:`FBCA074D-FCF3-427E-A700-7E318A949AE5`

		:type: str

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

GSLayer.attributes = property(lambda self: AttributesProxy(self))

'''
	.. attribute:: attributes
		layer attributes like :samp:`axisRules`, :samp:`coordinates`, :samp:`colorPalette`, :samp:`sbixSize`, :samp:`color`, :samp:`svg`

		.. code-block:: python

			axis = font.axes[0]
			layer.attributes['axisRules'] = {axis.axisId: {'min': 100}}
			layer.attributes['coordinates'] = {axis.axisId: 99}

		:type: dict
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

GSLayer.colorObject = property(lambda self: self.pyobjc_instanceMethods.color(),
							   lambda self, value: self.setColor_(value))
'''
	.. attribute:: colorObject
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


GSLayer.components = property(lambda self: self.pyobjc_instanceMethods.components())
'''
	.. attribute:: components
		Collection of :class:`GSComponent` objects. This is only a helper proxy to iterate all components (without paths). To add/remove items, use :attr:`GSLayer.shapes`.

		:type: list

		.. code-block:: python
			for component in layer.components:
				print(component)

'''

GSLayer.guides = property(lambda self: LayerGuidesProxy(self),
						  lambda self, value: LayerGuidesProxy(self).setter(value))

GSLayer.guideLines = GSLayer.guides

'''
	.. attribute:: guides
		List of :class:`GSGuide` objects.

		:type: list

		.. code-block:: python
			# access all guides
			for guide in layer.guides:
				print(guide)

			# add guide
			newGuide = GSGuide()
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
			# remember to reconnect the hints' nodes with the new layer’s nodes

'''

GSLayer.anchors = property(lambda self: LayerAnchorsProxy(self),
						   lambda self, value: LayerAnchorsProxy(self).setter(value))
'''
	.. attribute:: anchors
		List of :class:`GSAnchor` objects.

		:type: list, dict

		.. code-block:: python
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

GSLayer.shapes = property(lambda self: LayerShapesProxy(self),
						  lambda self, value: LayerShapesProxy(self).setter(value))
'''
	.. attribute:: shapes
		List of :class:`GSShape` objects. That are most likely :class:`GSPath` or :class:`GSComponent` 

		:type: list

		.. code-block:: python
			# access all shapes
			for shape in layer.shapes:
				print(shape)

			# delete shape
			del(layer.shapes[0])

			# copy shapes from another layer
			import copy
			layer.shapes = copy.copy(anotherlayer.shapes)
'''

GSLayer.paths = property(lambda self: self.pyobjc_instanceMethods.paths())
'''
	.. attribute:: paths
		List of :class:`GSPath` objects. This is only a helper proxy to iterate all paths (without components). To add/remove items, use :attr:`GSLayer.shapes`.

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

GSLayer.selection = property(lambda self: LayerSelectionProxy(self),
							 lambda self, value: LayerSelectionProxy(self).setter(value))

'''
	.. attribute:: selection
		List of all selected objects in the glyph.

		This list contains **all selected items**, including **nodes**, **anchors**, **guides** etc.
		If you want to work specifically with nodes, for instance, you may want to cycle through the nodes (or anchors etc.) and check whether they are selected. See example below.

		:type: list

		.. code-block:: python
			# access all selected nodes
			for path in layer.paths:
				for node in path.nodes: # (or path.anchors etc.)
					print(node.selected)

			# clear selection
			layer.clearSelection()

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
def GSLayer__setWidth(self, value):
	try:
		self.setWidth_(float(value))
	except:
		raise TypeError
GSLayer.width = property(lambda self: self.pyobjc_instanceMethods.width(),
						 GSLayer__setWidth)

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


GSLayer.ascender = property(lambda self: self.pyobjc_instanceMethods.ascender())
'''
	.. attribute:: ascender
		The ascender for this layer.

		:type: float
	
		.. versionadded:: 3.0.2
'''

GSLayer.descender = property(lambda self: self.pyobjc_instanceMethods.descender())
'''
	.. attribute:: descender
		The descender for this layer.

		:type: float
	
		.. versionadded:: 3.0.2
'''

GSLayer.leftMetricsKey = property(lambda self: self.pyobjc_instanceMethods.leftMetricsKey(),
								  lambda self, value: self.setLeftMetricsKey_(NSStr(value)),
								  doc="The leftMetricsKey of the layer.\n\nThis is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.")
'''
	.. attribute:: leftMetricsKey
		The leftMetricsKey of the layer. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str
'''
GSLayer.rightMetricsKey = property(lambda self: self.pyobjc_instanceMethods.rightMetricsKey(),
								   lambda self, value: self.setRightMetricsKey_(NSStr(value)))
'''
	.. attribute:: rightMetricsKey
		The rightMetricsKey of the layer. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str
'''
GSLayer.widthMetricsKey = property(lambda self: self.pyobjc_instanceMethods.widthMetricsKey(),
								   lambda self, value: self.setWidthMetricsKey_(NSStr(value)))
'''
	.. attribute:: widthMetricsKey
		The widthMetricsKey of the layer. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str
'''

GSLayer.bounds = property(lambda self: self.pyobjc_instanceMethods.bounds())
'''
	.. attribute:: bounds
		Bounding box of whole glyph as NSRect. Read-only.

		:type: NSRect

		.. code-block:: python
			# origin
			print(layer.bounds.origin.x, layer.bounds.origin.y)

			# size
			print(layer.bounds.size.width, layer.bounds.size.height)
'''

GSLayer.selectionBounds = property(lambda self: self.boundsOfSelection())
'''
	.. attribute:: selectionBounds
		Bounding box of the layer’s selection (nodes, anchors, components etc). Read-only.

		:type: NSRect
'''

GSLayer.metrics =  property(lambda self: self.pyobjc_instanceMethods.metrics())

'''
	.. attribute:: metrics
		The metrics layer are a list of horizontal metrics filtered specifically for this layer. Use this instead of :attr:`master.alignmentZones <GSFontMaster.alignmentZones>`.

		:type: :class:`GSMetricValue`

		.. versionadded:: 3.0.1
'''

GSLayer.background = property(lambda self: self.pyobjc_instanceMethods.background(),
							  lambda self, value: self.setBackground_(value))
'''
	.. attribute:: background
		The background layer

		:type: :class:`GSLayer`

		.. code-block:: python
			# copy layer to its background
			layer.background = layer.copy()

			# remove background layer
			layer.background = None
'''

GSLayer.backgroundImage = property(lambda self: self.pyobjc_instanceMethods.backgroundImage(),
								   lambda self, value: self.setBackgroundImage_(value))
'''
	.. attribute:: backgroundImage
		The background image. It will be scaled so that 1 em unit equals 1 of the image’s pixels.

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
		The layer as an NSBezierPath object. Useful for drawing glyphs in plug-ins.

		:type: NSBezierPath

		.. code-block:: python
			# draw the path into the Edit view
			NSColor.redColor().set()
			layer.bezierPath.fill()

			
'''

GSLayer.openBezierPath = property(lambda self: self.pyobjc_instanceMethods.openBezierPath())
'''
	.. attribute:: openBezierPath
		All open paths of the layer as an NSBezierPath object. Useful for drawing glyphs as outlines in plug-ins.

		:type: NSBezierPath

		.. code-block:: python
			# draw the path into the Edit view
			NSColor.redColor().set()
			layer.openBezierPath.stroke()

'''

# keep for compatibility:
def Layer__drawBezierPath(self):
	print("layer.drawBezierPath is deprecated. Please use layer.completeBezierPath")
	return self.pyobjc_instanceMethods.drawBezierPath()
GSLayer.drawBezierPath = property(lambda self: Layer__drawBezierPath(self))

GSLayer.completeBezierPath = property(lambda self: self.pyobjc_instanceMethods.drawBezierPath())
'''
	.. attribute:: completeBezierPath
		The layer as an NSBezierPath object including paths from components. Useful for drawing glyphs in plug-ins.

		:type: NSBezierPath

		.. code-block:: python
			# draw the path into the Edit view
			NSColor.redColor().set()
			layer.completeBezierPath.fill()

'''

# keep for compatibility:
def Layer__drawOpenBezierPath(self):
	print("layer.drawBezierPath is deprecated. Please use layer.completeBezierPath")
	return self.pyobjc_instanceMethods.drawOpenBezierPath()
GSLayer.drawOpenBezierPath = property(lambda self: Layer__drawOpenBezierPath(self))
GSLayer.completeOpenBezierPath = property(lambda self: self.pyobjc_instanceMethods.drawOpenBezierPath())
'''
	.. attribute:: completeOpenBezierPath
		All open paths of the layer as an NSBezierPath object including paths from components. Useful for drawing glyphs as outlines in plugins.

		:type: NSBezierPath

		.. code-block:: python
			# draw the path into the Edit view
			NSColor.redColor().set()
			layer.completeOpenBezierPath.stroke()

'''

GSLayer.isAligned = property(lambda self: bool(self.pyobjc_instanceMethods.isAligned()))
'''
	.. attribute:: isAligned
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

GSLayer.italicAngle = property(lambda self: float(self.pyobjc_instanceMethods.italicAngle()))
'''
	.. attribute:: italicAngle
		The italic angle that applies to this layer

		:type: float

'''

GSLayer.userData = property(lambda self: UserDataProxy(self))
'''
	.. attribute:: userData
		A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the data will not be recoverable from the saved file.

		:type: dict

		.. code-block:: python
			# set value
			layer.userData['rememberToMakeCoffee'] = True

			# delete value
			del layer.userData['rememberToMakeCoffee']

'''

GSLayer.tempData = property(lambda self: TempDataProxy(self))

'''
	.. attribute:: tempData
		A dictionary to store data temporarily. Use a unique key. This will not be saved to file. If you need the data persistent, use layer.userData

		:type: dict

		.. code-block:: python
			# set value
			layer.tempData['rememberToMakeCoffee'] = True

			# delete value
			del layer.tempData['rememberToMakeCoffee']

'''

GSLayer.smartComponentPoleMapping = property(lambda self: SmartComponentPoleMappingProxy(self))

'''
	.. attribute:: smartComponentPoleMapping
		Maps this layer to the poles on the interpolation axes of the Smart Glyph. The dictionary keys are the names of the :class:`GSSmartComponentAxis` objects. The values are 1 for bottom pole and 2 for top pole. Corresponds to the 'Layers' tab of the glyph’s ‘Show Smart Glyph Settings’ dialog.

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

		Decomposes all corners of the layer at once.

		.. versionadded:: 2.4

	.. function:: compareString()

		Returns a string representing the outline structure of the glyph, for compatibility comparison.

		:return: The comparison string

		:rtype: string

		.. code-block:: python
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
	self.removeOverlapCheckSelection_error_(checkSelection, None)
GSLayer.removeOverlap = python_method(RemoveOverlap)

'''
	.. function:: removeOverlap()

		Joins all contours.

		:param checkSelection: if the selection will be considered. Default: False

	.. function:: roundCoordinates()

		Round the positions of all coordinates to the grid (size of which is set in the Font Info).

'''

def Layer_addNodesAtExtremes(self, force=False):
	self.addExtremePointsForce_(force)

GSLayer.addNodesAtExtremes = python_method(Layer_addNodesAtExtremes)

'''
	.. function:: addNodesAtExtremes([force=False])

		Add nodes at layer's extrema, e.g., top, bottom etc.

		:param force: if points are always added, even if that would distort the shape

'''

def __GSLayer_applyTransform__(self, transformStruct):
	Transform = NSAffineTransform.transform()
	Transform.setTransformStruct_(transformStruct)
	self.transform_checkForSelection_doComponents_(Transform, False, True)

GSLayer.applyTransform = python_method(__GSLayer_applyTransform__)


'''
	.. function:: applyTransform

		Apply a transformation matrix to the layer.

		.. code-block:: python
			layer.applyTransform([
			    0.5, # x scale factor
			    0.0, # x skew factor
			    0.0, # y skew factor
			    0.5, # y scale factor
			    0.0, # x position
			    0.0  # y position
						])

'''

def __GSLayer_transform__(self, transform, selection=False, components=True):
	self.transform_checkForSelection_doComponents_(transform, selection, components)
GSLayer.transform = python_method(__GSLayer_transform__)
'''
	.. function:: transform

		Apply a :attr:`NSAffineTransform` to the layer.

		:param Point1: one point
		:param Point2: the other point

		.. code-block:: python
			transformation = NSAffineTransform()
			transformation.rotate(45, (200, 200))
			layer.transform(transformation)

'''

def BeginChanges(self):
	self.stopUpdates()
	self.undoManager().beginUndoGrouping()
GSLayer.beginChanges = python_method(BeginChanges)


'''
	.. function:: beginChanges()

		Call this before you do bigger changes to the Layer.
		This will increase performance and prevent undo problems.
		Always call layer.endChanges() if you are finished.

'''

def EndChanges(self):
	self.startUpdates()
	self.undoManager().endUndoGrouping()
GSLayer.endChanges = python_method(EndChanges)


'''
	.. function:: endChanges()

		Call this if you have called layer.beginChanges before. Make sure to group bot calls properly.

'''

def CutBetweenPoints(self, Point1, Point2):
	GlyphsToolOther = NSClassFromString("GlyphsToolOther")
	GlyphsToolOther.cutPathsInLayer_forPoint_endPoint_(self, Point1, Point2)
GSLayer.cutBetweenPoints = python_method(CutBetweenPoints)


'''
	.. function:: cutBetweenPoints(Point1, Point2)

		Cuts all paths that intersect the line from Point1 to Point2

		:param Point1: one point
		:param Point2: the other point

		.. code-block:: python
			# cut glyph in half horizontally at y=100
			layer.cutBetweenPoints(NSPoint(0, 100), NSPoint(layer.width, 100))

'''

def IntersectionsBetweenPoints(self, Point1, Point2, components=False):
	return self.calculateIntersectionsStartPoint_endPoint_decompose_(Point1, Point2, components)
GSLayer.intersectionsBetweenPoints = python_method(IntersectionsBetweenPoints)

NSConcreteValue.x = property(lambda self: self.pointValue().x)
NSConcreteValue.y = property(lambda self: self.pointValue().y)

'''
	.. function:: intersectionsBetweenPoints(Point1, Point2, components=False)

		Return all intersection points between a measurement line and the paths in the layer. This is basically identical to the measurement tool in the UI.

		Normally, the first returned point is the starting point, the last returned point is the end point. Thus, the second point is the first intersection, the second last point is the last intersection.

		:param Point1: one point
		:param Point2: the other point
		:param components: if components should be measured. Default: False

		.. code-block:: python
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
GSLayer.addMissingAnchors = python_method(Layer_addMissingAnchors)


'''
	.. function:: addMissingAnchors()

		Adds missing anchors defined in the glyph database.

'''

'''
	.. function:: clearSelection()
	
		Unselect all selected items in this layer.

'''

'''
	.. function:: clear()
	
		Remove all elements from layer.

'''

'''
	.. function:: swapForegroundWithBackground()
	
		Swap Foreground layer with Background layer.
'''

def Layer_replaceLayerWithInterpolation(self):
	if self.parent:
		self.parent.replaceLayersWithInterpolation_([self])

GSLayer.reinterpolate = python_method(Layer_replaceLayerWithInterpolation)

'''
	.. function:: reinterpolate()
	
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
GSControlLayer.__init__ = python_method(ControlLayer__init__)

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

GSLayer.draw = python_method(DrawLayerWithPen)

def DrawPointsWithPen(self, pen, contours=True, components=True):
	"""draw the object with a point pen"""
	if contours:
		for p in self.paths:
			p.drawPoints(pen)
	if components:
		for c in self.components:
			c.drawPoints(pen)

GSLayer.drawPoints = python_method(DrawPointsWithPen)


def _getPen_(self):
	return GSPathPen.alloc().initWithLayer_(self)

GSLayer.getPen = python_method(_getPen_)
GSLayer.getPointPen = python_method(_getPen_)

def _invalidateContours_(self):
	pass

GSLayer._invalidateContours = python_method(_invalidateContours_)

def __GSLayer__add__(self, summand):
	if isinstance(summand, NSPoint):
		transform = NSAffineTransform.new()
		transform.translateXBy_yBy_(summand.x, summand.y)
		newLayer = self.copy()
		newLayer.transform_checkForSelection_doComponents_(transform, False, False)
		return newLayer
	elif isinstance(summand, GSLayer):
		if self.compareString() != summand.compareString():
			raise ValueError("Layers are not compatible: %s, %s" % (self.compareString(), summand.compareString()))
		newLayer = self.copy()
		newShapes = NSMutableArray.new()
		for i in range(len(summand.shapes)):
			shape1 = newLayer.shapes[i]
			shape2 = summand.shapes[i]
			newShape = shape1 + shape2
			newShapes.addObject_(newShape)
		newLayer.shapes = newShapes
		
		if len(self.anchors):
			newAnchors = NSMutableDictionary.new()
			for anchorName in self.anchors.keys():
				anchor1 = newLayer.anchors[anchorName]
				anchor2 = summand.anchors[anchorName]
				newAnchor = anchor1 + anchor2
				newAnchors.setObject_forKey_(newAnchor, anchorName)
			newLayer.anchors = newAnchors
		
		newLayer.width += summand.width
		return newLayer
	else:
		raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (type(self).__name__, type(summand).__name__))
GSLayer.__add__ = python_method(__GSLayer__add__)

def __GSLayer__mul__(self, factor):
	if isinstance(factor, (int, float)):
		transform = NSAffineTransform.new()
		transform.scaleBy_(factor)
		newLayer = self.copy()
		newLayer.width = self.width * factor
		newLayer.transform_checkForSelection_doComponents_(transform, False, True)
		return newLayer
	else:
		raise TypeError("unsupported operand type(s) for *: '%s' and '%s'" % (type(self).__name__, type(factor).__name__))
GSLayer.__mul__ = python_method(__GSLayer__mul__)

def __GSPath__add__(self, summand):
	if isinstance(summand, NSPoint):
		transform = NSAffineTransform.new()
		transform.translateXBy_yBy_(summand.x, summand.y)
		newPath = self.copy()
		newPath.transform_(transform)
		return newPath
	elif isinstance(summand, GSPath):
		if len(self.nodes) != len(summand.nodes) or self.closed != summand.closed:
			raise ValueError("Paths are not compatible: %s, %s" % (len(self.nodes), len(summand.nodes)))
		newPath = self.copy()
		newNodes = NSMutableArray.new()
		for i in range(len(summand.nodes)):
			node1 = newPath.nodes[i]
			node2 = summand.nodes[i]
			newNode = node1 + node2
			newNodes.addObject_(newNode)
		newPath.nodes = newNodes
		return newPath
	else:
		raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (type(self).__name__, type(summand).__name__))
GSPath.__add__ = python_method(__GSPath__add__)

def __GSNode__add__(self, summand):
	if isinstance(summand, NSPoint):
		newNode = self.copy()
		newNode.position = addPoints(newNode.position, summand)
		return newNode
	elif isinstance(summand, GSNode):
		if self.type != summand.type:
			raise ValueError("Nodes are not compatible: %s, %s" % (self.type, summand.type))
		newNode = self.copy()
		newNode.position = addPoints(newNode.position, summand.position)
		return newNode
	else:
		raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (type(self).__name__, type(summand).__name__))
GSNode.__add__ = python_method(__GSNode__add__)

def __GSComponent__add__(self, summand):
	if isinstance(summand, NSPoint):
		newComponent = self.copy()
		newComponent.position = addPoints(newComponent.position, summand)
		return newComponent
	elif isinstance(summand, GSComponent):
		if self.component != summand.component:
			raise ValueError("Components are not compatible: %s, %s" % (self, summand))
		newComponent = self.copy()
		newComponent.position = addPoints(newComponent.position, summand.position)
		newComponent.scale = addPoints(newComponent.scale, summand.scale)
		newComponent.rotation = newComponent.rotation + summand.rotation
		return newComponent
	else:
		raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (type(self).__name__, type(summand).__name__))
GSComponent.__add__ = python_method(__GSComponent__add__)

def __GSAnchor__add__(self, summand):
	if isinstance(summand, NSPoint):
		newAnchor = self.copy()
		newAnchor.position = addPoints(newAnchor.position, summand)
		return newAnchor
	elif isinstance(summand, GSAnchor):
		if self.name != summand.name:
			raise ValueError("Anchors are not compatible: %s, %s" % (self, summand))
		newAnchor = self.copy()
		newAnchor.position = addPoints(newAnchor.position, summand.position)
		return newAnchor
	else:
		raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (type(self).__name__, type(summand).__name__))
GSAnchor.__add__ = python_method(__GSAnchor__add__)


##################################################################################
#
#
#
#           GSAnchor
#
#
#
##################################################################################

def ________________(): pass
def ____GSAnchor____(): pass
def ________________(): pass

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
GSAnchor.__init__ = python_method(Anchor__init__)

def Anchor__repr__(self):
	return "<GSAnchor \"%s\" x=%s y=%s>" % (self.name, self.position.x, self.position.y)
GSAnchor.__repr__ = python_method(Anchor__repr__)

GSAnchor.__eq__ = python_method(lambda self, other: self.isEqualToAnchor_(other))

GSAnchor.mutableCopyWithZone_ = GSObject__copy__

GSAnchor.position = property(lambda self: self.pyobjc_instanceMethods.position(),
							 lambda self, value: self.setPosition_(value),
							 doc="The position of the anchor.")
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
						 lambda self, value: self.setName_(value),
						 doc="The name of the anchor.")
'''
	.. attribute:: name
		The name of the anchor

		:type: str

	.. attribute:: selected
		Selection state of anchor in UI.

		.. code-block:: python
			# select anchor
			layer.anchors[0].selected = True

			# log selection state
			print(layer.anchors[0].selected)

		:type: bool

'''

GSAnchor.userData = property(lambda self: UserDataProxy(self))

'''
	.. attribute:: userData
		A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the data will not be recoverable from the saved file.

		:type: dict

		.. code-block:: python
			# set value
			anchor.userData['rememberToMakeCoffee'] = True

			# delete value
			del component.userData['rememberToMakeCoffee']

		.. versionadded:: 3

'''

def DrawAnchorWithPen(self, pen):
	if hasattr(pen, "addAnchor"):
		pen.addAnchor(self.name, (self.x, self.y))
	else:
		pen.moveTo(self.position)
		pen.endPath()

GSAnchor.draw = python_method(DrawAnchorWithPen)

def __GSAnchor_drawPoints__(self, pen):
	"""Draw the object with a point pen."""
	pen.beginPath()
	pen.addPoint((self.x, self.y), segmentType="move", smooth=False, name=self.name)
	pen.endPath()
GSAnchor.drawPoints = python_method(__GSAnchor_drawPoints__)
GSAnchor.drawPoints.__name__ = "drawPoints"

##################################################################################
#
#
#
#           GSComponent
#
#
#
##################################################################################

def ___________________(): pass
def ____GSComponent____(): pass
def ___________________(): pass



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

def Component__init__(self, glyph=None, offset=(0, 0), scale=(1, 1), transform=None):
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
		if isString(glyph):
			self.setComponentName_(glyph)
		elif isinstance(glyph, GSGlyph):
			self.setComponentName_(glyph.name)
		elif isinstance(glyph, "RGlyph"):
			self.setComponentName_(glyph.name)

GSComponent.__init__ = python_method(Component__init__)

def Component__repr__(self):
	return "<GSComponent \"%s\" x=%s y=%s>" % (self.componentName, self.position.x, self.position.y)
GSComponent.__repr__ = python_method(Component__repr__)

GSComponent.__eq__ = python_method(lambda self, other: self.isEqualToComponent_(other))

GSComponent.mutableCopyWithZone_ = GSObject__copy__

GSComponent.position = property(lambda self: self.pyobjc_instanceMethods.position(),
								lambda self, value: self.setPosition_(validatePoint(value)),
								doc="The position of the component.")
'''
	.. attribute:: position
		The position of the component.

		:type: NSPoint

'''

GSComponent.scale = property(lambda self: self.pyobjc_instanceMethods.scale(),
							 lambda self, value: self.setScale_(value),
							 doc="Scale factor of the component.")

'''
	.. attribute:: scale
		Scale factor of the component.

		A tuple containing the horizontal and vertical scale.

		:type: tuple

'''

GSComponent.rotation = property(lambda self: self.angle(),
								lambda self, value: self.setAngle_(value),
								doc="Rotation angle of the component.")

'''
	.. attribute:: rotation
		Rotation angle of the component.

		:type: float

'''

GSComponent.componentName = property(lambda self: self.pyobjc_instanceMethods.componentName(),
									lambda self, value: self.setComponentName_(value),
									doc="The glyph name the component is pointing to.")
'''
	.. attribute:: componentName
		The glyph name the component is pointing to.

		:type: str

'''

GSComponent.name = property(lambda self: self.pyobjc_instanceMethods.componentName(),
							lambda self, value: self.setComponentName_(value),
							doc="The glyph name the component is pointing to.")
'''
	.. attribute:: name
		The glyph name the component is pointing to.

		:type: str

		.. versionadded:: 2.5

'''

GSComponent.component = property(lambda self: self.pyobjc_instanceMethods.component(),
								 doc="The glyph the component is pointing to.")
'''
	.. attribute:: component
		The :class:`GSGlyph` the component is pointing to. This is read-only. In order to change the referenced base glyph, set :attr:`componentName <GSComponent.componentName>` to the new glyph name.

		:type: :class:`GSGlyph`

'''

GSComponent.componentLayer = property(lambda self: self.pyobjc_instanceMethods.componentLayer(),
									  doc="The layer the component is pointing to.")
'''
	.. attribute:: componentLayer
		The :class:`GSLayer` the component is pointing to. This is read-only. In order to change the referenced base glyph, set :attr:`componentName <GSComponent.componentName>` to the new glyph name.

		For Smart Components, the `componentLayer` contains the interpolated result.

		:type: :class:`GSLayer`

		.. versionadded:: 2.5

'''

GSComponent.transform = property(lambda self: self.transformStruct(),
								 lambda self, value: self.setTransformStruct_(value),
										doc="Transformation matrix of the component.")
'''
	.. attribute:: transform
		Transformation matrix of the component.
		If Glyphs 3, this is computed from the scale, rotation and position. 

		:type: NSAffineTransformStruct

		.. code-block:: python
			component.transform = ((
			    0.5, # x scale factor
			    0.0, # x skew factor
			    0.0, # y skew factor
			    0.5, # y scale factor
			    0.0, # x position
			    0.0  # y position
			))

'''

GSComponent.bounds = property(lambda self: self.pyobjc_instanceMethods.bounds(),
							  doc="Bounding box of the component. (read-only)")
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
										  lambda self, value: self.setDisableAlignment_(not bool(value)),
										  doc="Defines whether the component is automatically aligned.")
'''
	.. attribute:: automaticAlignment
		Defines whether the component is automatically aligned.

		:type: bool
'''
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

		:type: str
'''

'''
	.. attribute:: selected
		Selection state of component in UI.

		:type: bool

		.. code-block:: python
			# select component
			layer.components[0].selected = True

			# print(selection state)
			print(layer.components[0].selected)

'''

GSComponent.attributes = property(lambda self: AttributesProxy(self))

'''
	.. attribute:: attributes
		attributes attributes like :samp:`mask` or :samp:`reversePaths`

		.. code-block:: python

			component.attributes['mask'] = True
			component.attributes['reversePaths'] = True

		:type: dict
'''

def DrawComponentWithPen(self, pen):
	pen.addComponent(self.componentName, self.transform)

GSComponent.draw = python_method(DrawComponentWithPen)
GSComponent.drawPoints = python_method(DrawComponentWithPen)

GSComponent.smartComponentValues = property(lambda self: SmartComponentValuesProxy(self))
'''
	.. attribute:: smartComponentValues
		Dictionary of interpolations values of the Smart Component. Key are the names, values are between the top and the bottom value of the corresponding :class:`GSSmartComponentAxis` objects. Corresponds to the values of the ‘Smart Component Settings’ dialog. Returns None if the component is not a Smart Component.

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
		The component as an NSBezierPath object. Useful for drawing glyphs in plugins.

		:type: NSBezierPath

		.. code-block:: python
			# draw the path into the Edit view
			NSColor.redColor().set()
			layer.components[0].bezierPath.fill()
		
'''

GSTransformableElement.userData = property(lambda self: UserDataProxy(self))

'''
	.. attribute:: userData
		A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the data will not be recoverable from the saved file.

		:type: dict

		.. code-block:: python
			# set value
			component.userData['rememberToMakeCoffee'] = True

			# delete value
			del component.userData['rememberToMakeCoffee']

		.. versionadded:: 2.5
'''

GSComponent.tempData = property(lambda self: TempDataProxy(self))

'''
	.. attribute:: tempData
		A dictionary to store data temporarily. Use a unique key. This will not be saved to file. If you need the data persistent, use component.userData

		:type: dict

		.. code-block:: python
			# set value
			component.tempData['rememberToMakeCoffee'] = True

			# delete value
			del component.tempData['rememberToMakeCoffee']

'''

'''

	**Functions**


'''

GSComponent.parent = property(lambda self: self.pyobjc_instanceMethods.parent(),
							  lambda self, value: self.setParent_(value))

def __GSComponent_decompose__(self, doAnchors=True, doHints=True):
	assert(self.parent is not None)
	self.parent.decomposeComponent_doAnchors_doHints_(self, doAnchors, doHints)
GSComponent.decompose = python_method(__GSComponent_decompose__)

'''
	.. function:: decompose([doAnchors=True, doHints=True])

		Decomposes the component.

		:param doAnchors: get anchors from components
		:param doHints: get hints from components


'''

def __GSComponent_applyTransform__(self, transformStruct):
	transform = self.transform
	oldTransform = NSAffineTransform.transform()
	oldTransform.setTransformStruct_(transform)
	newTransform = NSAffineTransform.transform()
	newTransform.setTransformStruct_(transformStruct)
	oldTransform.appendTransform_(newTransform)
	self.setTransformStruct_(oldTransform.transformStruct())

GSComponent.applyTransform = python_method(__GSComponent_applyTransform__)

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

GSGlyphReference = objc.lookUpClass("GSGlyphReference")

def GSGlyphReference__new__(typ, glyph):
	return typ.alloc().initWithGlyph_(glyph)

GSGlyphReference.__new__ = staticmethod(GSGlyphReference__new__)
GSGlyphReference.__new__.__name__ = "__new__"

'''

:mod:`GSGlyphReference`
===============================================================================

a small helper class to store a reference to a glyph in userData that will keep track of changes to the glyph name.

.. versionadded:: 3.0.4

.. class:: GSGlyphReference()

	Properties

	.. autosummary::

		glyph

	**Properties**
'''

GSGlyphReference.glyph = property(lambda self: self.pyobjc_instanceMethods.glyph(),
								  lambda self, value: self.setGlyph_(value))
'''
	.. attribute:: glyph
	the GSGlyph to keep track of

	:type: GSGlyph

	.. code-block:: python

		glyphReference = GSGlyphReference(Font.glyphs["A"])

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

def ____________________________(): pass
def ____GSSmartComponentAxis____(): pass
def ____________________________(): pass

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
GSSmartComponentAxis.__new__.__name__ = "__new__"

def SmartComponentProperty__init__(self):
	pass
GSSmartComponentAxis.__init__ = python_method(SmartComponentProperty__init__)
def SmartComponentProperty__repr__(self):
	return "<GSSmartComponentAxis \"%s\">" % (self.name)
GSSmartComponentAxis.__repr__ = python_method(SmartComponentProperty__repr__)

GSSmartComponentAxis.name = property(lambda self: self.pyobjc_instanceMethods.name(),
									 lambda self, value: self.setName_(objcObject(value)))
'''
	.. attribute:: name
		Name of the axis. The name is for display purpose only.

		:type: str
'''
GSSmartComponentAxis.id = property(lambda self: self.axisId())
'''
	.. attribute:: id
		Id of the axis. This Id will be used to map the Smart Glyph’s layers to the poles of the interpolation. See :attr:`GSLayer.smartComponentPoleMapping`

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
#           GSShape
#
#
#
##################################################################################

def _______________(): pass
def ____GSShape____(): pass
def _______________(): pass

'''

:mod:`GSShape`
===============================================================================

Implementation of the shape object.

For details on how to access them, please see :attr:`GSLayer.shapes`

.. class:: GSShape()

	**Properties**

	.. autosummary::

		position
		locked
		shapeType
'''

GSShape.locked = property(lambda self: bool(self.pyobjc_instanceMethods.locked()),
						  lambda self, value: self.setLocked_(value))
GSPath.locked = property(lambda self: bool(self.pyobjc_instanceMethods.locked()),
						 lambda self, value: self.setLocked_(value))
'''
	.. attribute:: locked
		Locked

		:type: bool
'''

GSPath.shapeType = property(lambda self: self.pyobjc_instanceMethods.shapeType())
GSComponent.shapeType = property(lambda self: self.pyobjc_instanceMethods.shapeType())

'''
	.. attribute:: shapeType
		the type of the shapes. can be GSShapeTypePath or GSShapeTypeComponent

		:type: int
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


def ______________(): pass
def ____GSPath____(): pass
def ______________(): pass

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
		attributes
		tempData

	Functions

	.. autosummary::

		reverse()
		addNodesAtExtremes()
		applyTransform()

	**Properties**
'''

GSPath.__new__ = staticmethod(GSObject__new__)
GSPath.__new__.__name__ = "__new__"

def Path__init__(self):
	pass
GSPath.__init__ = python_method(Path__init__)

def Path__repr__(self):
	return "<GSPath %s nodes>" % len(self.nodes)
GSPath.__repr__ = python_method(Path__repr__)

GSPath.__eq__ = python_method(lambda self, other: self.isEqualToPath_(other))

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
def Path__len__(self):
	return self.countOfNodes()
GSPath.__len__ = python_method(Path__len__)

GSPath.segments = property(lambda self: PathSegmentsProxy(self),
						   lambda self, value: PathSegmentsProxy(self).setter(value))
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

GSPath.selected = property(lambda self: Path_selected(self),
						   lambda self, value: Path_SetSelected(self, value))
'''
	.. attribute:: selected
		Selection state of path in UI.

		:type: bool

		.. code-block:: python
			# select path
			layer.paths[0].selected = True

			# print(selection state)
			print(layer.paths[0].selected)
'''

GSPath.bezierPath = property(lambda self: self.pyobjc_instanceMethods.bezierPath())
'''
	.. attribute:: bezierPath
		The same path as an NSBezierPath object. Useful for drawing glyphs in plugins.

		:type: NSBezierPath

		.. code-block:: python
			# draw the path into the Edit view
			NSColor.redColor().set()
			layer.paths[0].bezierPath.fill()

	**Functions**

	.. function:: reverse()

		Reverses the path direction
'''

GSPath.attributes = property(lambda self: AttributesProxy(self))

'''
	.. attribute:: attributes
		path attributes like :samp:`fill`, :samp:`mask`, :samp:`strokeWidth`, :samp:`strokeHeight`, :samp:`strokeColor'`, :samp:`strokePos`

		.. code-block:: python

			# in B/W layers:
			path.attributes['fill'] = True
			path.attributes['mask'] = True
			path.attributes['strokeWidth'] = 100
			path.attributes['strokeHeight'] = 80
			
			# in color layers:
			path.attributes['strokeColor'] = NSColor.redColor()
			path.attributes['fillColor'] = NSColor.blueColor()
			path.attributes['strokePos'] = 1 # or 0, -1

		:type: dict
'''

GSPath.tempData = property(lambda self: TempDataProxy(self))

'''
	.. attribute:: tempData
		A dictionary to store data temporarily. Use a unique key. This will not be saved to file. If you need the data persistent, use path.userData

		:type: dict

		.. code-block:: python
			# set value
			path.tempData['rememberToMakeCoffee'] = True

			# delete value
			del path.tempData['rememberToMakeCoffee']

'''

def DrawPathWithPen(self, pen):
	# draw the object with a fontTools pen
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
		node = self.nodeAtIndex_(i)
		GS_Type = node.pyobjc_instanceMethods.type()
		if GS_Type == GSLINE_:
			pen.lineTo(node.pyobjc_instanceMethods.position())
		elif GS_Type == GSCURVE_:
			pen.curveTo(self.nodeAtIndex_(i - 2).pyobjc_instanceMethods.position(), self.nodeAtIndex_(i - 1).pyobjc_instanceMethods.position(), node.pyobjc_instanceMethods.position())
	if self.closed:
		pen.closePath()
	else:
		pen.endPath()
	return

GSPath.draw = python_method(DrawPathWithPen)

def __GSPath__drawPoints__(self, pen):
	'''draw the object with a fontTools pen'''
	pen.beginPath()
	for i in range(self.countOfNodes()):
		node = self.nodeAtIndex_(i)
		node_type = node.type
		if node.type == GSOFFCURVE:
			node_type = None
		pen.addPoint(node.position, segmentType=node_type, smooth=node.smooth, name=node.name)
	pen.endPath()

GSPath.drawPoints = python_method(__GSPath__drawPoints__)

def Path_addNodesAtExtremes(self, force=False):
	self.addExtremes_(force)

GSPath.addNodesAtExtremes = python_method(Path_addNodesAtExtremes)
'''
	.. function:: addNodesAtExtremes()

		Add nodes at path’s extrema, e.g., top, bottom etc.
'''

def __CGPath_applyTransform__(self, transformStruct):
	Transform = NSAffineTransform.transform()
	Transform.setTransformStruct_(transformStruct)
	for node in self.nodes:
		node.position = Transform.transformPoint_(node.positionPrecise())

GSPath.applyTransform = python_method(__CGPath_applyTransform__)

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

def ______________(): pass
def ____GSNode____(): pass
def ______________(): pass

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
GSNode.__init__ = python_method(Node__init__)

def Node__repr__(self):
	NodeType = self.type
	if self.type != OFFCURVE and self.smooth:
		NodeType += " smooth"
	return "<GSNode x=%s y=%s %s>" % (self.position.x, self.position.y, NodeType)
GSNode.__repr__ = python_method(Node__repr__)

GSNode.__eq__ = python_method(lambda self, other: self.isEqualToNode_(other))

GSNode.mutableCopyWithZone_ = GSObject__copy__

GSElement.position = property(lambda self: self.pyobjc_instanceMethods.position(),
							  lambda self, value: self.setPosition_(validatePoint(value)))
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
	elif GS_Type == GSHOBBYCURVE_:
		return GSHOBBYCURVE
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
	elif value == HOBBYCURVE:
		self.setType_(GSHOBBYCURVE_)

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
'''

GSNode.connection = property(lambda self: self.pyobjc_instanceMethods.connection(),
							 lambda self, value: self.setConnection_(value))

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

		:type: bool

		.. code-block:: python
			# select node
			layer.paths[0].nodes[0].selected = True

			# print(selection state)
			print(layer.paths[0].nodes[0].selected)
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
'''

def __GSNode__nextNode__(self):
	try:
		idx = self.parent.indexOfNode_(self)
		if idx == (len(self.parent.nodes) - 1):
			return self.parent.nodes[0]
		elif idx < len(self.parent.nodes):
			return self.parent.nodes[idx + 1]
	except:
		pass
	return None

GSNode.nextNode = property(lambda self: __GSNode__nextNode__(self))
'''
	.. attribute:: nextNode
		Returns the next node in the path.

		Please note that this is regardless of the position of the node in the path and will jump across the path border to the beginning of the path if the current node is the last.

		If you need to take into consideration the position of the node in the path, use the node’s index attribute and check it against the path length.

		:type: GSNode

		.. code-block:: python
			print(layer.paths[0].nodes[0].nextNode # returns the second node in the path (index 0 + 1))
			print(layer.paths[0].nodes[-1].nextNode # returns the first node in the path (last node >> jumps to beginning of path))

			# check if node is last node in path (with at least two nodes)
			print(layer.paths[0].nodes[0].index == (len(layer.paths[0].nodes) - 1)) # returns False for first node
			print(layer.paths[0].nodes[-1].index == (len(layer.paths[0].nodes) - 1)) # returns True for last node
'''

def __GSNode__prevNode__(self):
	try:
		idx = self.parent.indexOfNode_(self)
		if idx == 0:
			return self.parent.nodes[-1]
		elif idx < len(self.parent.nodes):
			return self.parent.nodes[idx - 1]
	except:
		pass
	return None

GSNode.prevNode = property(lambda self: __GSNode__prevNode__(self))
'''
	.. attribute:: prevNode
		Returns the previous node in the path.

		Please note that this is regardless of the position of the node in the path, and will jump across the path border to the end of the path if the current node is the first.

		If you need to take into consideration the position of the node in the path, use the node’s index attribute and check it against the path length.

		:type: GSNode

		.. code-block:: python
			print(layer.paths[0].nodes[0].prevNode) # returns the last node in the path (first node >> jumps to end of path)
			print(layer.paths[0].nodes[-1].prevNode) # returns second last node in the path

			# check if node is first node in path (with at least two nodes)
			print(layer.paths[0].nodes[0].index == 0) # returns True for first node
			print(layer.paths[0].nodes[-1].index == 0) # returns False for last node
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
		raise TypeError

GSNode.name = property(__GSNode__get_name, __GSNode__set_name, doc="")
'''
	.. attribute:: name
		Attaches a name to a node.

		:type: str
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
#           GSPathSegment
#
#
#
##################################################################################

def _____________________(): pass
def ____GSPathSegment____(): pass
def _____________________(): pass


'''

:mod:`GSPathSegment`
===============================================================================

Implementation of the segment object.

For details on how to access them, please see :attr:`GSPath.segments`


.. class:: GSPathSegment()

	**Properties**

	.. autosummary::

		type
		bounds
		count
		points
		length
'''

def __GSPathSegment__getitem__(self, idx):
	return self.pointAtIndex_(idx)
GSPathSegment.__getitem__ = python_method(__GSPathSegment__getitem__)

GSPathSegment.__len__ = property(lambda self: self.countOfPoints)

def GSPathSegment__new__(typ, p1=NSPoint(0, 0), p2=NSPoint(0, 0), p3=None, p4=None):
	if (p3 is not None and p4 is not None):
		return typ.alloc().initWithCurvePoint1_point2_point3_point4_options_(p1, p2, p3, p4, 0)
	else:
		return typ.alloc().initWithLinePoint1_point2_options_(p1, p2, 0)
	
GSPathSegment.__new__ = staticmethod(GSPathSegment__new__)
 
GSPathSegment.type = property(__GSNode_get_type__)

'''
	.. attribute:: type
		The type of the node, LINE, CURVE or QCURVE

		Always compare against the constants, never against the actual value.

		:type: str
'''

##################################################################################
#
#
#
#           GSGuide
#
#
#
##################################################################################

def _______________(): pass
def ____GSGuide____(): pass
def _______________(): pass


'''

:mod:`GSGuide`
===============================================================================

Implementation of the guide object.

For details on how to access them, please see :attr:`GSLayer.guides`


.. class:: GSGuide()

	**Properties**

	.. autosummary::

		position
		angle
		name
		filter
		selected
		locked
		userData
'''

def Guide__init__(self):
	pass
GSGuide.__init__ = python_method(Guide__init__)

def Guide__repr__(self):
	return "<GSGuide x=%s y=%s angle=%s>" % (self.position.x, self.position.y, self.angle)
GSGuide.__repr__ = python_method(Guide__repr__)

GSGuide.__eq__ = python_method(lambda self, other: self.isEqualToGuide_(other))

GSGuide.mutableCopyWithZone_ = GSObject__copy__

GSGuide.lockAngle = property(lambda self: bool(self.pyobjc_instanceMethods.lockAngle()),
							 lambda self, value: self.setLockAngle_(value))
'''
	.. attribute:: lockAngle
		locks the angle

		:type: bool
'''

GSGuide.angle = property(lambda self: self.pyobjc_instanceMethods.angle(),
						 lambda self, value: self.setAngle_(float(value)))
'''
	.. attribute:: angle
		Angle

		:type: float
'''

def GSGuide_setName(self, name):
	if isString(name):
		self.setName_(name)
	else:
		raise TypeError
GSGuide.name = property(lambda self: self.pyobjc_instanceMethods.name(),
						GSGuide_setName)
'''
	.. attribute:: name
		a optional name

		:type: str

	.. attribute:: selected
		Selection state of guide in UI.

		:type: bool

		.. code-block:: python
			# select guide
			layer.guides[0].selected = True

			# print(selection state)
			print(layer.guides[0].selected)
'''

GSGuide.locked = property(lambda self: bool(self.pyobjc_instanceMethods.locked()),
						  lambda self, value: self.setLocked_(value))
'''
	.. attribute:: locked
		Locked

		:type: bool
'''

GSGuide.filter = property(lambda self: self.pyobjc_instanceMethods.filter(),
						  lambda self, value: self.setFilter_(value))
'''
	.. attribute:: filter
		A filter to only show the guide in certain glyphs. Only relevant in global guides

		:type: NSPredicate
'''

GSGuide.userData = property(lambda self: UserDataProxy(self))

'''
	.. attribute:: userData
		A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the data will not be recoverable from the saved file.

		:type: dict

		.. code-block:: python
			# set value
			guide.userData['rememberToMakeCoffee'] = True

			# delete value
			del guide.userData['rememberToMakeCoffee']
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

def ____________________(): pass
def ____GSAnnotation____(): pass
def ____________________(): pass

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
GSAnnotation.__new__.__name__ = "__new__"

def Annotation__init__(self):
	pass
GSAnnotation.__init__ = python_method(Annotation__init__)

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

		:type: str
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

def ______________(): pass
def ____GSHint____(): pass
def ______________(): pass

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
		isTrueType
		isPostScript
		isCorner
		name
		stem

	**Properties**
'''

GSHint.__new__ = staticmethod(GSObject__new__)
GSHint.__new__.__name__ = "__new__"

def Hint__init__(self):
	pass
GSHint.__init__ = python_method(Hint__init__)

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
	if self.isTrueType:
		return self.description()
	if self.horizontal:
		direction = "hori"
	else:
		direction = "vert"
	if self.type == BOTTOMGHOST or self.type == TOPGHOST:
		return "<GSHint %s origin=(%s)>" % (self.typeName(), self.position)
	elif self.type == STEM:
		return "<GSHint %s Stem origin=(%s) target=(%s)>" % (direction, self.position, self.width)
	elif self.isCorner:
		return "<GSHint %s %s>" % (self.typeName(), self.name)
	else:
		return "<GSHint %s %s>" % (self.typeName(), direction)
GSHint.__repr__ = python_method(Hint__repr__)

GSHint.mutableCopyWithZone_ = GSObject__copy__

GSHint.parent = property(lambda self: self.pyobjc_instanceMethods.parent())

'''
	.. attribute:: parent
		Parent layer of hint.

		:type: GSLayer
'''

GSHint.scale = property(lambda self: self.pyobjc_instanceMethods.scale(),
						lambda self, value: self.setScale_(value))

GSHint.originNode = property(lambda self: self.pyobjc_instanceMethods.originNode(),
							 lambda self, value: self.setOriginNode_(value))
'''
	.. attribute:: originNode
		The first node the hint is attached to.

		:type: :class:`GSNode` or :class:`GSHandle` (e.g. when attached to intersections)
'''

GSHint.position = property(Hint__origin__pos,
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

		:type: :class:`GSNode` or :class:`GSHandle` (e.g. when attached to intersections)
'''

GSHint.otherNode1 = property(lambda self: self.pyobjc_instanceMethods.otherNode1(),
							 lambda self, value: self.setOtherNode1_(value))
'''
	.. attribute:: otherNode1
		A third node this hint is attached to. Used for Interpolation or Diagonal hints.

		:type: :class:`GSNode` or :class:`GSHandle` (e.g. when attached to intersections)
'''

GSHint.otherNode2 = property(lambda self: self.pyobjc_instanceMethods.otherNode2(),
							 lambda self, value: self.setOtherNode2_(value))
'''
	.. attribute:: otherNode2
		A fourth node this hint is attached to. Used for Diagonal hints.

		:type: :class:`GSNode` or :class:`GSHandle` (e.g. when attached to intersections)
'''

GSHint.type = property(lambda self: self.pyobjc_instanceMethods.type(),
					   lambda self, value: self.setType_(value))
'''
	.. attribute:: type
		See Constants section at the bottom of the page.

		:type: int
'''

GSHint.options = property(lambda self: self.pyobjc_instanceMethods.options(),
						  lambda self, value: self.setOptions_(value))
'''
	.. attribute:: options
		Stores extra options for the hint. For TT hints, that might be the rounding settings.
		See Constants section at the bottom of the page.

		For corner components, it stores the alingment settings: left = 0, center = 2, right = 1, auto (for caps) = alignment | 8

		:type: int
'''

GSHint.horizontal = property(lambda self: bool(self.pyobjc_instanceMethods.horizontal()),
							 lambda self, value: self.setHorizontal_(value))
'''
	.. attribute:: horizontal
		True if hint is horizontal, False if vertical.

		:type: bool
'''

'''
	.. attribute:: selected
		Selection state of hint in UI.

		:type: bool

		.. code-block:: python
			# select hint
			layer.hints[0].selected = True

			# print(selection state)
			print(layer.hints[0].selected)
'''

GSHint.name = property(lambda self: self.pyobjc_instanceMethods.name(),
					   lambda self, value: self.setName_(objcObject(value)))
'''
	.. attribute:: name
		Name of the hint. This is the referenced glyph for corner and cap components.

		:type: string
'''

def GSHint__stem__(self):
	value = self.pyobjc_instanceMethods.stem()
	stems = self.parent.master.customParameters['TTFStems']
	if stems is None:
		stems = self.parent.metrics
	if stems and -1 <= value <= (len(stems) - 1):
		return value
	else:
		return -2

def GSHint__setStem__(self, value):
	if self.isTrueType:
		stems = self.parent.master.customParameters['TTFStems']
		if not stems:
			raise ValueError('The master of this layer has no defined "TTFStems" custom parameter')
		if stems and -1 <= value <= (len(stems) - 1):
			self.pyobjc_instanceMethods.setStem_(value)
		elif value == -2:
			self.pyobjc_instanceMethods.setStem_(sys.maxint)
		else:
			raise ValueError('Wrong value. Stem values can be indices of TT stems ("TTFStems" master custom parameter) or -1 for no stem or -2 for automatic.')
	else:
		self.pyobjc_instanceMethods.setStem_(value)


GSHint.stem = property(GSHint__stem__,
						lambda self, value: GSHint__setStem__(self, value))
'''
	.. attribute:: stem
		Index of TrueType stem that this hint is attached to. The stems are defined in the custom parameter "TTFStems" per master.

		For no stem, value is -1.

		For automatic, value is -2.

		:type: int
'''

GSHint.isTrueType = property(lambda self: self.pyobjc_instanceMethods.isTrueType())
'''
	.. attribute:: isTrueType
		if it is a TrueType instruction

		:type: bool

		.. versionadded:: 3
'''
GSHint.isPostScript = property(lambda self: self.pyobjc_instanceMethods.isPostScript())
'''
	.. attribute:: isPostScript
		if it is a PostScript hint

		:type: bool

		.. versionadded:: 3
'''

GSHint.isCorner = property(lambda self: self.pyobjc_instanceMethods.isCorner())
'''
	.. attribute:: isCorner
		if it is a Corner (or Cap, Brush...) component

		:type: bool

		.. versionadded:: 3
'''

GSHint.tempData = property(lambda self: TempDataProxy(self))

'''
	.. attribute:: tempData
		A dictionary to store data temporarily. Use a unique key. This will not be saved to file. If you need the data persistent, use hint.userData

		:type: dict

		.. code-block:: python
			# set value
			hint.tempData['rememberToMakeCoffee'] = True

			# delete value
			del hint.tempData['rememberToMakeCoffee']
'''


##################################################################################
#
#
#
#           GSBackgroundImage
#
#
#
##################################################################################

def _________________________(): pass
def ____GSBackgroundImage____(): pass
def _________________________(): pass


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
		self.path = path
GSBackgroundImage.__init__ = python_method(BackgroundImage__init__)
GSBackgroundImage.__new__ = staticmethod(GSObject__new__)

def BackgroundImage__repr__(self):
	return "<GSBackgroundImage '%s'>" % self.path
GSBackgroundImage.__repr__ = python_method(BackgroundImage__repr__)

GSBackgroundImage.mutableCopyWithZone_ = GSObject__copy__
GSBackgroundImage.__copy__ = python_method(GSObject__copy__)
GSBackgroundImage.__deepcopy__ = python_method(GSObject__copy__)

def BackgroundImage_path(self):
	url = self.imageURL()
	if url is not None:
		return url.path()
	
def BackgroundImage_setPath(self, path):
	self.setImageURL_(NSURL.fileURLWithPath_(path))
	self.loadImage()

GSBackgroundImage.path = property(BackgroundImage_path,
								  lambda self, value: BackgroundImage_setPath(self, value))
'''
	.. attribute:: path
		Path to image file.

		:type: str
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
		Crop rectangle. This is relative to the image size in pixels, not the font’s em units (just in case the image is scaled to something other than 100%).

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
'''

def BackgroundImage_getPosition(self):
	return NSPoint(self.transform[4], self.transform[5])

def BackgroundImage_setPosition(self, pos):
	self.transform = ((self.transform[0], self.transform[1], self.transform[2], self.transform[3], pos.x, pos.y))

GSBackgroundImage.position = property(BackgroundImage_getPosition,
									  lambda self, value: BackgroundImage_setPosition(self, value))

'''
	.. attribute:: position
		Position of image in font units.

		:type: :class:`NSPoint`

	.. code-block:: python
		# change position
		layer.backgroundImage.position = NSPoint(50, 50)
'''

GSBackgroundImage.scale = property(lambda self: self.pyobjc_instanceMethods.scale(),
								   lambda self, value: self.setScale_(value))

'''
	.. attribute:: scale
		Scale factor of image.

		A scale factor of 1.0 (100%) means that 1 font unit is equal to 1 point.

		Set the scale factor for x and y scale simultaneously with an integer or a float value. For separate scale factors, please use a tuple.

		:type: tuple

		.. code-block:: python
			# change scale
			layer.backgroundImage.scale = 1.2 # changes x and y to 120%
			layer.backgroundImage.scale = (1.1, 1.2) # changes x to 110% and y to 120%
'''

GSBackgroundImage.rotation = property(lambda self: self.angle(),
									  lambda self, value: self.setAngle_(value))

'''
	.. attribute:: rotation
		Rotation angle of image.

		:type: float
'''

GSBackgroundImage.transform = property(lambda self: self.transformStruct(),
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
GSBackgroundImage.resetCrop = python_method(BackgroundImage_resetCrop)
'''
	.. function:: resetCrop

		Resets the cropping to the image’s original dimensions.
'''

def BackgroundImage_scaleWidthToEmUnits(self, value):
	scale = float(value) / float(self.crop.size.width)
	self.scale = NSPoint(scale, scale)
GSBackgroundImage.scaleWidthToEmUnits = python_method(BackgroundImage_scaleWidthToEmUnits)
'''
	.. function:: scaleWidthToEmUnits

		Scale the image’s cropped width to a certain em unit value, retaining its aspect ratio.

		.. code-block:: python
			# fit image in layer’s width
			layer.backgroundImage.scaleWidthToEmUnits(layer.width)
'''

def BackgroundImage_scaleHeightToEmUnits(self, value):
	self.scale = float(value) / float(self.crop.size.height)
GSBackgroundImage.scaleHeightToEmUnits = python_method(BackgroundImage_scaleHeightToEmUnits)

'''
	.. function:: scaleHeightToEmUnits

		Scale the image’s cropped height to a certain em unit value, retaining its aspect ratio.

		.. code-block:: python
			# position image’s origin at descender line
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

def ____________________________(): pass
def ____GSEditViewController____(): pass
def ____________________________(): pass

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
		redraw()

	**Properties**
'''

GSEditViewController.parent = property(lambda self: self.representedObject())
GSFontViewController.parent = property(lambda self: self.representedObject())
'''
	.. attribute:: parent
		The :class:`GSFont` object that this tab belongs to.

		:type: :class:`GSFont`
'''

GSEditViewController.text = property(lambda self: self.graphicView().displayStringASCIIonly_(False),
									 lambda self, value: self.graphicView().setDisplayString_(value))
'''
	.. attribute:: text
		The text of the tab, either as text, or slash-escaped glyph names, or mixed. OpenType features will be applied after the text has been changed.

		:type: str

		.. code-block:: python
			string = ""
			for l in Font.selectedLayers:
				char = Font.characterForGlyph_(l.parent)
				string += chr(char)
			tab = Font.tabs[0]
			tab.text = string
'''

def __GSEditViewController__repr__(self):
	nameString = self.graphicView().displayStringASCIIonly_(True)
	if len(nameString) > 30:
		nameString = nameString[:30] + '...'
	nameString = nameString.replace('\n', '\\n')
	return self.description() + nameString

GSEditViewController.__repr__ = python_method(__GSEditViewController__repr__)

GSEditViewController.masterIndex = property(lambda self: self.pyobjc_instanceMethods.masterIndex(),
											lambda self, value: self.setMasterIndex_(value))
'''
	.. attribute:: masterIndex
		The index of the active master (selected in the toolbar).

		:type: int
	
		.. versionadded:: 2.6.1
'''

GSEditViewController.selectedLayers = property(lambda self: self.pyobjc_instanceMethods.selectedLayers())

GSFontViewController.selectedLayers = property(lambda self: self.pyobjc_instanceMethods.selectedLayers())

class TabLayersProxy(Proxy):

	def __getitem__(self, idx):
		return self.values().__getitem__(idx)

	def deactivateFeatures(self):
		self.savedFeatures = copy.copy(self._owner.features)
		self._owner.features = []

	def activateFeatures(self):
		self._owner.features = self.savedFeatures

	def setter(self, layers):

		self.deactivateFeatures()

		if not (isinstance(layers, (list, tuple, type(self))) or "objectAtIndex_" in layers.__class__.__dict__):
			raise ValueError
		if isinstance(layers, type(self)):
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
			elif l.className() == "GSGlyph":
				char = Font.characterForGlyph_(l)
				A = NSAttributedString.alloc().initWithString_(NSString.stringWithChar_(char))
			else:
				raise ValueError
			string.appendAttributedString_(A)
		self._owner.graphicView().textStorage().setText_(string)
		self.activateFeatures()

	def composedLayers(self):
		return list(self._owner.graphicView().layoutManager().cachedLayers())

	def values(self):
		self.deactivateFeatures()
		layers = list(self._owner.graphicView().layoutManager().cachedLayers())
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


GSEditViewController.layers = property(lambda self: TabLayersProxy(self),
									   lambda self, value: TabLayersProxy(self).setter(value))

'''
	.. attribute:: layers
		Alternatively, you can set (and read) a list of :class:`GSLayer` objects. These can be any of the layers of a glyph. OpenType features will be applied after the layers have been changed.

		:type: list

		.. code-block:: python
			layers = []

			# display all layers of one glyph next to each other
			for layer in font.glyphs['a'].layers:
				layers.append(layer)

			# append line break
			layers.append(GSControlLayer(10)) # 10 being the ASCII code of the new line character (\n)

			font.tabs[0].layers = layers
'''

GSEditViewController.composedLayers = property(lambda self: TabLayersProxy(self).composedLayers())

'''
	.. attribute:: composedLayers
		Similar to the above, but this list contains the :class:`GSLayer` objects after the OpenType features have been applied (see :class:`GSEditViewController.features`). Read-only.

		:type: list

		.. versionadded:: 2.4
'''

GSEditViewController.scale = property(lambda self: self.graphicView().scale(),
									  lambda self, value: self.graphicView().setScale_(value))

'''
	.. attribute:: scale
		Scale (zoom factor) of the Edit view. Useful for drawing activity in plugins.

		The scale changes with every zoom step of the Edit view. So if you want to draw objects (e.g. text, stroke thickness etc.) into the Edit view at a constant size relative to the UI (e.g. constant text size on screen), you need to calculate the object’s size relative to the scale factor. See example below.

		:type: float

		.. code-block:: python
			print(font.currentTab.scale)
			0.414628537193

			# Calculate text size
			desiredTextSizeOnScreen = 10 #pt
			scaleCorrectedTextSize = desiredTextSizeOnScreen / font.currentTab.scale

			print(scaleCorrectedTextSize)
			24.1179733255
'''

GSEditViewController.viewPort = property(lambda self: self.graphicView().userVisibleRect(),
										 lambda self, value: self.graphicView().setUserVisibleRect_(value))

GSEditViewController.saveViewPort = property(lambda self: self.graphicView().saveVisibleRect())

'''
	.. attribute:: viewPort
		The visible area of the Edit view in screen pixel coordinates (view coordinates).

		The NSRect’s origin value describes the top-left corner (top-right for RTL, both at ascender height) of the combined glyphs’ bounding box (see :attr:`bounds <GSEditViewController.bounds>`), which also serves as the origin of the view plane.

		The NSRect’s size value describes the width and height of the visible area.

		When using drawing methods such as the view-coordinate-relative method in the Reporter Plugin, use these coordinates.

		:type: NSRect

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
'''

GSEditViewController.bounds = property(lambda self: self.frameView().glyphFrame())

'''
	.. attribute:: bounds
		Bounding box of all glyphs in the Edit view in view coordinate values.

		:type: NSRect
'''

GSEditViewController.selectedLayerOrigin = property(lambda self: self.graphicView().activePosition())

'''
	.. attribute:: selectedLayerOrigin
		Position of the active layer’s origin (0,0) relative to the origin of the view plane (see :attr:`bounds <GSEditViewController.bounds>`), in view coordinates.

		:type: NSPoint
'''

GSEditViewController.textCursor = property(lambda self: self.graphicView().selectedRange().location,
										   lambda self, value: self.graphicView().setSelectedRange_(NSRange(value, self.graphicView().selectedRange().length)))
'''
	.. attribute:: textCursor
		Position of text cursor in text, starting with 0.

		:type: integer
'''

GSEditViewController.textRange = property(lambda self: self.contentView().selectedRange().length,
										  lambda self, value: self.contentView().setSelectedRange_(NSRange(self.textCursor, value)))
'''
	.. attribute:: textRange
		Amount of selected glyphs in text, starting at cursor position (see above).

		:type: integer
'''

GSEditViewController.layersCursor = property(lambda self: self.graphicView().cachedLayerSelectionRange().location)

'''
	.. attribute:: layersCursor
		Position of cursor in the layers list, starting with 0.
		
		.. seealso:: `GSEditViewController.layers`

		:type: integer

		.. versionadded:: 2.4
'''

GSEditViewController.direction = property(lambda self: self.writingDirection(),
										  lambda self, value: self.setWritingDirection_(value))
'''
	.. attribute:: direction
		Writing direction.

		Defined constants are: LTR (left to right), RTL (right to left), LTRTTB (left to right, vertical, top to bottom e.g. Mongolian), and RTLTTB (right to left, vertical, top to bottom e.g. Chinese, Japanese, Korean)

		:type: integer

		.. code-block:: python
			font.currentTab.direction = RTL
'''

class TabSelectedFeaturesProxy(Proxy):

	def reflow(self):
		self._owner.graphicView().reflow()
		self._owner.graphicView().layoutManager().updateActiveLayer()
		self._owner._updateFeaturePopup()

	def setter(self, values):
		if not isinstance(values, (list, tuple, type(self))):
			raise TypeError
		self._owner.pyobjc_instanceMethods.selectedFeatures().removeAllObjects()

		if isinstance(values, type(self)):
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
			self._owner.selectedFeatures().addObject_(feature)

		self.reflow()

	def extend(self, features):
		if not isinstance(features, list):
			raise TypeError
		for feature in features:
			if self.hasFeature(feature):
				self._owner.selectedFeatures().addObject_(feature)
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

GSEditViewController.features = property(lambda self: TabSelectedFeaturesProxy(self),
										 lambda self, value: TabSelectedFeaturesProxy(self).setter(value))

'''
	.. attribute:: features
		List of OpenType features applied to text in Edit view.

		:type: list

	.. code-block:: python

		font.currentTab.features = ['locl', 'ss01']
'''

# TODO documentation
GSEditViewController.tempData = property(lambda self: TempDataProxy(self))

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

GSEditViewController.previewInstances = property(Get_ShowInPreview,
												 Set_ShowInPreview)
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
'''

GSEditViewController.previewHeight = property(lambda self: self.pyobjc_instanceMethods.previewHeight(),
											  lambda self, value: self.setPreviewHeight_(value))

'''
	.. attribute:: previewHeight
		Height of the preview panel in the Edit view in pixels.

		Needs to be set to 16 or higher for the preview panel to be visible at all. Will return 0 for a closed preview panel or the current size when visible.

		:type: float
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


GSEditViewController.saveToPDF = python_method(GSEditViewController_saveToPDF)


'''
	.. function:: saveToPDF(path[, rect])

		Save the view to a PDF file.

		:param path: Path to the file
		:param rect: Optional. NSRect defining the view port. If omitted, :attr:`GSEditViewController.viewPort` will be used.

		.. versionadded:: 2.4
'''

'''
	.. function:: redraw()
	
		forces a update of the edit view
'''

GSMacroViewController.title = property(lambda self: self.pyobjc_instanceMethods.title(), 
									   lambda self, value: self.setTitleSave_(value))

##################################################################################
#
#
#
#           GSGlyphInfo
#
#
#
##################################################################################


def ___________________(): pass
def ____GSGlyphInfo____(): pass
def ___________________(): pass


GSGlyphInfo.__new__ = staticmethod(GSObject__new__)
GSGlyphInfo.__new__.__name__ = "__new__"

def GSGlyphInfo__init__(self):
	pass
GSGlyphInfo.__init__ = python_method(GSGlyphInfo__init__)

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
		direction
		desc

	**Properties**

'''

GSGlyphInfo.name = property(lambda self: self.pyobjc_instanceMethods.name())
'''
	.. attribute:: name
		Human-readable name of glyph ("nice name").

		:type: str
'''

GSGlyphInfo.productionName = property(lambda self: self.pyobjc_instanceMethods.production())
'''
	.. attribute:: productionName
		Production name of glyph. Will return a value only if production name differs from nice name, otherwise None.

		:type: str
'''

GSGlyphInfo.category = property(lambda self: self.pyobjc_instanceMethods.category())
'''
	.. attribute:: category
		This is mostly from the UnicodeData.txt file from unicode.org. Some corrections have been made (Accents, ...)
		e.g: "Letter", "Number", "Punctuation", "Mark", "Separator", "Symbol", "Other"

		:type: str
'''

GSGlyphInfo.subCategory = property(lambda self: self.pyobjc_instanceMethods.subCategory())
'''
	.. attribute:: subCategory
		This is mostly from the UnicodeData.txt file from unicode.org. Some corrections and additions have been made.
		e.g: "Nonspacing", "Ligature", "Decimal Digit", ...

		:type: str
'''

GSGlyphInfo.case = property(lambda self: self.pyobjc_instanceMethods.case())
'''
	.. attribute:: case
		e.g: GSUppercase, GSLowercase, GSSmallcaps

		:type: int
'''

GSGlyphInfo.components = property(lambda self: self.pyobjc_instanceMethods.components())
'''
	.. attribute:: components
		This glyph may be composed of the glyphs returned as a list of :class:`GSGlyphInfo` objects.

		:type: list
'''

GSGlyphInfo.accents = property(lambda self: self.marks())
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

		:type: str
'''

GSGlyphInfo.unicodes = property(lambda self: self.unicodesArray())
'''
	.. attribute:: unicode2
		a second unicode value it present

		:type: str
'''

GSGlyphInfo.script = property(lambda self: self.pyobjc_instanceMethods.script())
'''
	.. attribute:: script
		Script of glyph, e.g: "latin", "cyrillic", "greek".

		:type: str
'''

GSGlyphInfo.index = property(lambda self: self.pyobjc_instanceMethods.index())
'''
	.. attribute:: index
		Index of glyph in database. Used for sorting in UI.

		:type: str
'''

GSGlyphInfo.sortName = property(lambda self: self.pyobjc_instanceMethods.sortName())
'''
	.. attribute:: sortName
		Alternative name of glyph used for sorting in UI.

		:type: str
'''

GSGlyphInfo.sortNameKeep = property(lambda self: self.pyobjc_instanceMethods.sortNameKeep())
'''
	.. attribute:: sortNameKeep
		Alternative name of glyph used for sorting in UI, when using 'Keep Alternates Next to Base Glyph' from Font Info.

		:type: str
'''

GSGlyphInfo.desc = property(lambda self: self.pyobjc_instanceMethods.desc())
'''
	.. attribute:: desc
		Unicode description of glyph.

		:type: str
'''

GSGlyphInfo.altNames = property(lambda self: self.pyobjc_instanceMethods.altNames())
'''
	.. attribute:: altNames
		Alternative names for glyphs that are not used, but should be recognized (e.g., for conversion to nice names).

		:type: str
'''

GSGlyphInfo.direction = property(lambda self: self.pyobjc_instanceMethods.direction())
'''
	.. attribute:: direction
		Writing direction.

		Defined constants are: GSLTR (left to right), GSRTL (right to left), GSVertical (right to left, vertical, top to bottom e.g. Chinese, Japanese, Korean) and GSVerticalToRight (left to right, vertical, top to bottom e.g. Mongolian)

		:type: integer

		.. code-block:: python
			glyph.direction = GSRTL

		.. versionadded:: 3
'''

'''
:mod:`GSFontInfoValueLocalized`
===============================================================================

The GSFontInfoValueLocalized

.. class:: GSFontInfoValueLocalized()

	Properties

	.. autosummary::
		
		key
		values
		defaultValue

	**Properties**

'''
GSFontInfoValueLocalized.__new__ = staticmethod(GSObject__new__)

GSFontInfoValueLocalized.key = property(lambda self: self.pyobjc_instanceMethods.key(),
										lambda self, values: self.setKey_(values))
'''
	.. attribute:: key
		the key

		:type: str

	.. code-block:: python
		# searching for GSFontInfoValueLocalized with given "designers" key
		for fontInfo in font.properties:
			if fontInfo.key == "designers":
				print(fontInfo)
'''

GSFontInfoValueLocalized.values = property(lambda self: self.mutableArrayValueForKey_("values"),
										   lambda self, values: self.setValues_(values))
'''
	.. attribute:: values
		A list of :class:`GSFontInfoValue` objects.

		:type: list

	.. code-block:: python
		# listing values of GSFontInfoValueLocalized
		for fontInfoValue in fontInfoValueLocalized.values:
			print(fontInfoValue)
'''

GSFontInfoValueLocalized.defaultValue = property(lambda self: self.pyobjc_instanceMethods.defaultValue())
'''
	.. attribute:: defaultValue
		the value that is considered the default (either the dflt or English entry)

		:type: str

	.. code-block:: python
		# prints the default value for given GSFontInfoValueLocalized instance
		print(fontInfoValueLocalized.defaultValue)
		
		# The print below will always return True, because 
		# font.designer represent the same value
		
		fontInfoValueLocalized = None
		for fontInfo in font.properties:
			if fontInfo.key == "designers":
				fontInfoValueLocalized = fontInfo

		print(fontInfoValueLocalized.defaultValue == font.designer) 
'''

'''
:mod:`GSFontInfoValueSingle`
===============================================================================

The GSFontInfoValueSingle

.. class:: GSFontInfoValueSingle()

	Properties

	.. autosummary::
		
		key
		value

	**Properties**

'''
GSFontInfoValueSingle.__new__ = staticmethod(GSObject__new__)

GSFontInfoValueSingle.key = property(lambda self: self.pyobjc_instanceMethods.key(),
									 lambda self, values: self.setKey_(values))
'''
	.. attribute:: key
		the key

		:type: str

	.. code-block:: python
		# GSFontInfoValueSingle is stored in e.g. font.properties
		# one of the differences between GSFontInfoValueSingle and GSFontInfoValueLocalized
		# is that the first doesn't have "values" attribute
		for fontProperty in font.properties:
			
			if not hasattr(fontProperty, "values"):
				print(fontProperty.key)
'''

GSFontInfoValueSingle.value = property(lambda self: self.pyobjc_instanceMethods.value(),
									   lambda self, value: self.setValue_(value))
'''
	.. attribute:: value
		The value

		:type: str

	.. code-block:: python
		# GSFontInfoValueSingle is stored in e.g. font.properties
		# one of the differences between GSFontInfoValueSingle and GSFontInfoValueLocalized
		# is that the first doesn't have "values" attribute
		for fontProperty in font.properties:
			
			if not hasattr(fontProperty, "values"):
				print(fontProperty.value)
'''
'''
:mod:`GSFontInfoValue`
===============================================================================

The GSFontInfoValue

.. class:: GSFontInfoValue()

	Properties

	.. autosummary::
		
		key
		value
		languageTag

	**Properties**

'''
GSFontInfoValue.__new__ = staticmethod(GSObject__new__)

GSFontInfoValue.key = property(lambda self: self.pyobjc_instanceMethods.key(),
							   lambda self, values: self.setKey_(values))
'''
	.. attribute:: key
		the key

		:type: str

	.. code-block:: python
		# GSFontInfoValue is stored in e.g. values attribute of font.properties
		for fontProperty in font.properties:
			
			# not all of font.properties contains this attribute
			# so we are going to look for those, that have it
			if hasattr(fontProperty, "values"):
				for fontInfoValue in fontProperty.values:

					# this line prints out the key attribute of
					# found GSFontInfoValue instance
					print(fontInfoValue.key)
'''

GSFontInfoValue.value = property(lambda self: self.pyobjc_instanceMethods.value(),
								 lambda self, value: self.setValue_(value))
'''
	.. attribute:: value
		The value

		:type: str

	.. code-block:: python
		# GSFontInfoValue is stored in e.g. values attribute of font.properties
		for fontProperty in font.properties:
			
			# not all of font.properties contains this attribute
			# so we are going to look for those, that have it
			if hasattr(fontProperty, "values"):
				for fontInfoValue in fontProperty.values:

					# this line prints out the value attribute of
					# found GSFontInfoValue instance
					print(fontInfoValue.value)
'''
GSFontInfoValue.languageTag = property(lambda self: self.pyobjc_instanceMethods.languageTag(),
									   lambda self, value: self.setLanguageTag_(value))
'''
	.. attribute:: languageTag
		The languageTag

		:type: str

	.. code-block:: python
		# GSFontInfoValue is stored in e.g. values attribute of font.properties
		for fontProperty in font.properties:
			
			# not all of font.properties contains this attribute
			# so we are going to look for those, that have it
			if hasattr(fontProperty, "values"):
				for fontInfoValue in fontProperty.values:

					# this line prints out the languageTag attribute of
					# found GSFontInfoValue instance
					print(fontInfoValue.languageTag)
'''

'''
:mod:`GSMetricValue`
===============================================================================

The GSMetricValue objects represent vertical metrics values and theirs overshoots.

.. class:: GSMetricValue()

	Properties

	.. autosummary::
		
		position
		overshoot
		name
		filter
		metric

	**Properties**

'''

GSMetricValue.position = property(lambda self: self.pyobjc_instanceMethods.position(),
								  lambda self, value: self.setPosition_(value))
'''
	.. attribute:: position
		The y position of the metric.

		:type: float
'''

GSMetricValue.overshoot = property(lambda self: self.pyobjc_instanceMethods.overshoot(),
								   lambda self, value: self.setOvershoot_(value))
'''
	.. attribute:: overshoot
		Value of overshoot’s width.

		:type: float
'''
GSMetricValue.size = GSMetricValue.overshoot # compatibilty

GSMetricValue.name = property(lambda self: self.title())
'''
	.. attribute:: name
		The name of the metric value. Eg. Descender, Small Cap, Cap Height etc.

		:type: str
'''

GSMetricValue.filter = property(lambda self: self.pyobjc_instanceMethods.filter())
'''
	.. attribute:: filter
		A filter to limit the scope of the metric.

		:type: NSPredicate
'''

GSMetricValue.metric = property(lambda self: self.pyobjc_instanceMethods.metric())
'''
	.. attribute:: metric
		Corresponding GSMetric object. see :attr:`GSFont.metrics`.

		:type: GSMetric
'''

'''

:mod:`PreviewTextWindow`
===============================================================================

The Text Preview Window

.. class:: PreviewTextWindow()

	Properties

	.. autosummary::

		text
		font
		instanceIndex
		fontSize

	Functions

	.. autosummary::

		open()
		close()

	**Properties**

'''

PreviewTextWindow.__class__.font = property(lambda self: self.defaultInstance().activeFont())
'''
	.. attribute:: font
		The font

		:type: GSFont
'''

PreviewTextWindow.__class__.text = property(lambda self: self.defaultInstance().textView().string(),
											lambda self, value: self.defaultInstance().textView().setString_(value))
'''
	.. attribute:: text
		The text

		:type: str
'''

PreviewTextWindow.__class__.instanceIndex = property(lambda self: Glyphs.intDefaults["GSPreviewText_instanceIndex"],
													 lambda self, value: NSUserDefaults.standardUserDefaults().setObject_forKey_(value, objcObject("GSPreviewText_instanceIndex")))
'''
	.. attribute:: instanceIndex
		The index of the selected instance

		:type: int
'''

PreviewTextWindow.__class__.fontSize = property(lambda self: Glyphs.intDefaults["GSPreviewText_fontSize"],
													lambda self, value: NSUserDefaults.standardUserDefaults().setObject_forKey_(value, objcObject("GSPreviewText_fontSize")))
'''
	.. attribute:: fontSize
		The font size

		:type: int
'''

def PreviewTextWindow__open(self):
	PreviewTextWindow.defaultInstance().openWindow()
PreviewTextWindow.open = classmethod(PreviewTextWindow__open)
'''
	.. function:: open()
		opens the Preview Text Window

	.. code-block:: python
		# open PreviewTextWindow
		PreviewTextWindow.open()

		# setting instance in PreviewTextWindow to "Regular"
		font = PreviewTextWindow.font
		instanceNames = [instance.name for instance in font.instances]
		regularIndex = instanceNames.index("Regular")
		PreviewTextWindow.instanceIndex = regularIndex

		# setting text and font size value
		PreviewTextWindow.text = 'hamburgefontsiv'
		PreviewTextWindow.fontSize = 200
'''

def PreviewTextWindow__close(self):
	PreviewTextWindow.defaultInstance().closeWindow_(None)
PreviewTextWindow.close = classmethod(PreviewTextWindow__close)
'''
	.. function:: close()
		closes the Preview Text Window
'''

def __GSPathPen_beginPath__(self, identifier=None, **kwargs):
	self.beginPath_(identifier)
	path = self.currentPath()
	path.closed = True
GSPathPen.beginPath = python_method(__GSPathPen_beginPath__)

def __GSPathPen_moveTo__(self, pt):
	self.moveTo_(pt)
GSPathPen.moveTo = python_method(__GSPathPen_moveTo__)

def __GSPathPen_lineTo__(self, pt):
	self.lineTo_(pt)
GSPathPen.lineTo = python_method(__GSPathPen_lineTo__)

def __GSPathPen_curveTo__(self, off1, off2, pt):
	self.curveTo_off1_off2_(pt, off1, off2)
GSPathPen.curveTo = python_method(__GSPathPen_curveTo__)

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
GSPathPen.addPoint = python_method(__GSPathPen_addPoint__)

'''

:mod:`NSAffineTransform`
===============================================================================

The NSAffineTransform object.

.. class:: NSAffineTransform()

	Functions

	.. autosummary::

		shift
		scale
		rotate
		skew

	**Properties**
		transformStruct

'''

NSAffineTransform.__new__ = staticmethod(GSObject__new__)

def NSAffineTransform__shift(self, value):
	value = validatePoint(value)
	self.translateXBy_yBy_(value[0], value[1])
NSAffineTransform.shift = python_method(NSAffineTransform__shift)
'''
	.. attribute:: shift
		shift by x, y

		:type: tuple or NSPoint
'''
def NSAffineTransform__scale(self, value, center=None):
	value = validateScale(value)
	if center is not None:
		center = validatePoint(center)
		self.translateXBy_yBy_(center[0], center[1])
	self.scaleXBy_yBy_(value[0], value[1])
	if center is not None:
		self.translateXBy_yBy_(-center[0], -center[1])
NSAffineTransform.scale = python_method(NSAffineTransform__scale)
'''
	.. attribute:: scale
		if a single number, scale uniformly, otherwise scale by x, y
		if center is given, that is used as the origin of the scale

		:type: int/float or tuple
	
'''
def NSAffineTransform__rotate(self, value, center=None):
	value = validateNumber(value)
	if center is not None:
		center = validatePoint(center)
		self.translateXBy_yBy_(center[0], center[1])
	self.rotateByDegrees_(value)
	if center is not None:
		self.translateXBy_yBy_(-center[0], -center[1])
NSAffineTransform.rotate = python_method(NSAffineTransform__rotate)
'''
	.. attribute:: rotate
		The angle of the rotation. In degree, positive angles are CCW
		if center is given, that is used as the origin of the rotation

		:type: int/float
	
'''
def NSAffineTransform__skew(self, value, center=(0, 0)):
	if isinstance(value, (int, float)):
		skewX = value
		skewY = 0
	elif isinstance(value, tuple):
		if len(value) != 2:
			raise ValueError
		skewX = value[0]
		skewY = value[1]
	if skewX != 0 or skewY != 0:
		self.shearXBy_yBy_atCenter_(skewX, skewY, center)
	
NSAffineTransform.skew = python_method(NSAffineTransform__skew)

'''
	.. attribute:: skew
		if a single number, skew in x-direction otherwise skew by x, y
		if center is given, that is used as the origin of the skew

		:type: int/float or tuple
'''

NSAffineTransform.matrix = property(lambda self: tuple(self.transformStruct()),
									lambda self, value: self.setTransformStruct_(value))

'''
	.. attribute:: matrix
		The transformation matrix.

		:type: tuple
'''
'''

Methods
=======

.. autosummary::

	divideCurve()
	distance()
	addPoints()
	subtractPoints()
	scalePoint()
	removeOverlap()
	subtractPaths()
	intersectPaths()
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

	Divides the curve using the De Casteljau’s algorithm.

	:param P0: The Start point of the Curve (NSPoint)
	:param P1: The first off curve point
	:param P2: The second off curve point
	:param P3: The End point of the Curve
	:param t: The time parameter
	:return: A list of points that represent two curves. (Q0, Q1, Q2, Q3, R1, R2, R3). Note that the ‘middle’ point is only returned once.
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
	:param scalar: The multiplier
	:return: The multiplied point
	:rtype: NSPoint
'''

def removeOverlap(paths):
	try:
		Paths = NSMutableArray.arrayWithArray_(paths)
	except:
		Paths = NSMutableArray.arrayWithArray_(paths.values())

	result = GSPathFinder.removeOverlapPaths_error_(Paths, None)
	if result[0] != 1:
		return None
	return Paths

'''
.. function:: removeOverlap(paths)

	removes the overlaps from the list of paths

	:param paths: A list of paths
	:return: The resulting list of paths
	:rtype: list
'''

def subtractPaths(paths, subtract):
	try:
		Paths = NSMutableArray.arrayWithArray_(paths)
	except:
		Paths = NSMutableArray.arrayWithArray_(paths.values())
	try:
		Subtract = NSMutableArray.arrayWithArray_(subtract)
	except:
		Subtract = NSMutableArray.arrayWithArray_(subtract.values())
	result = GSPathFinder.subtractPaths_from_error_(Subtract, Paths, None)
	if result[0] != 1:
		return None
	return Paths
'''
.. function:: subtractPaths(paths, subtract)

	removes the overlaps from the list of paths

	:param paths: a list of paths
	:param subtract: the subtracting paths
	:return: The resulting list of paths
	:rtype: list
'''
def intersectPaths(paths, otherPaths):
	try:
		Paths = NSMutableArray.arrayWithArray_(paths)
	except:
		Paths = NSMutableArray.arrayWithArray_(paths.values())
	try:
		OtherPaths = NSMutableArray.arrayWithArray_(otherPaths)
	except:
		OtherPaths = NSMutableArray.arrayWithArray_(otherPaths.values())
	result = GSPathFinder.intersectPaths_from_error_(Paths, OtherPaths, None)
	if result[0] != 1:
		return None
	return OtherPaths
'''
.. function:: intersectPaths(paths, otherPaths)

	removes the overlaps from the list of paths

	:param paths: a list of paths
	:param otherPaths: the other paths
	:return: The resulting list of paths
	:rtype: list
'''

def GetSaveFile(message=None, ProposedFileName=None, filetypes=None):
	Panel = NSSavePanel.savePanel().retain()
	Panel.setExtensionHidden_(False)
	if message is not None:
		Panel.setTitle_(message)
	if filetypes is not None:
		if isString(filetypes):
			filetypes = [filetypes]
		if len(filetypes) > 0:
			Panel.setAllowedFileTypes_(objcObject(filetypes))
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
MGOrderedDictionary.items = python_method(__allItems__)

def __allKeys__(self):
	return self.allKeys()
MGOrderedDictionary.keys = python_method(__allKeys__)

def __Dict_removeObjectForKey__(self, key):
	if isinstance(key, int):
		if key < 0:
			key += len(self)
			if key < 0:
				raise IndexError("list index out of range")
		self.removeObjectAtIndex_(key)
		return
	self.removeObjectForKey_(key)

MGOrderedDictionary.__delitem__ = python_method(__Dict_removeObjectForKey__)

GSNotifyingDictionary.items = python_method(__allItems__)
GSNotifyingDictionary.keys = python_method(__allKeys__)


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
# MGOrderedDictionary.__getitem__ = python_method(__Dict__objectForKey__)


def __Dict__iter__(self):
	Values = self.values()
	if Values is not None:
		for element in Values:
			yield element
MGOrderedDictionary.__iter__ = python_method(__Dict__iter__)

def __Dict__del__(self, key):
	self.removeObjectForKey_(key)
MGOrderedDictionary.__delattr__ = python_method(__Dict__del__)


def GetFile(message=None, title=None, allowsMultipleSelection=False, filetypes=None):
	return GetOpenFile(message, title, allowsMultipleSelection, filetypes)

def GetOpenFile(message=None, title=None, allowsMultipleSelection=False, filetypes=None, path=None):
	if filetypes is None:
		filetypes = []
	Panel = NSOpenPanel.new()
	Panel.setCanChooseFiles_(True)
	Panel.setCanChooseDirectories_(False)
	Panel.setAllowsMultipleSelection_(allowsMultipleSelection)
	if path is not None:
		Panel.setDirectory_(path)
	if message is not None:
		Panel.setMessage_(message)
	if title is not None:
		Panel.setTitle_(message)
	if filetypes is not None:
		if isString(filetypes):
			filetypes = [filetypes]
		if len(filetypes) > 0:
			Panel.setAllowedFileTypes_(objcObject(filetypes))
	pressedButton = Panel.runModal()
	if pressedButton == NSOKButton:
		if allowsMultipleSelection:
			return Panel.filenames()
		else:
			return Panel.filename()
	return None
'''
.. function:: GetOpenFile(message=None, allowsMultipleSelection=False, filetypes=None, path=None)

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
.. function:: GetFolder(message=None, allowsMultipleSelection=False, path=None)

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
.. function:: Message(message, title="Alert", OKButton=None)

	Shows an alert panel.

	:param message: the string
	:param title: a title of the dialog
	:param OKButton: the lable of the confirmation button

'''
def AskString(message, value=None, title="Glyphs", OKButton=None, placeholder=None):
	result = Glyphs.showAskString_message_defaultText_placeholder_OKButton_(title, message, value, placeholder, OKButton)
	return result

'''
.. function:: AskString(message, value=None, title="Glyphs", OKButton=None, placeholder=None):

	AskString Dialog

	:param message: the string
	:param value: a default value
	:param title: a title of the dialog
	:param OKButton: the lable of the confirmation button
	:param placeholder: a placeholder value that is displayed in gray when the text field is emtpy

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

	Write a message to the Mac’s Console.app for debugging.

	:param str message:
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

Node Types
==============

.. data:: LINE

	Line node.

.. data:: CURVE

	Curve node. Make sure that each curve node is preceded by two off-curve nodes.

.. data:: QCURVE

	Quadratic curve node. Make sure that each curve node is preceded by at least one off-curve node.

.. data:: OFFCURVE

	Off-cuve node

Path attributes
==============

.. data:: FILL

	fill

.. data:: FILLCOLOR

	fillColor

.. data:: FILLPATTERNANGLE

	fillPatternAngle

.. data:: FILLPATTERNBLENDMODE

	fillPatternBlendMode

.. data:: FILLPATTERNFILE

	fillPatternFile

.. data:: FILLPATTERNOFFSET

	fillPatternOffset

.. data:: FILLPATTERNSCALE

	fillPatternScale

.. data:: STROKECOLOR

	strokeColor

.. data:: STROKELINECAPEND

	lineCapEnd

.. data:: STROKELINECAPSTART

	lineCapStart

.. data:: STROKELINEJOIN

	lineJoin

.. data:: STROKEPOSITION

	strokePos

.. data:: STROKEWIDTH

	strokeWidth

.. data:: STROKEHEIGHT

	strokeHeight

.. data:: GRADIENT

	gradient

.. data:: SHADOW

	shadow

.. data:: INNERSHADOW

	shadowIn

.. data:: MASK

	mask

File Format Versions
====================

A constant that is used when saving are reading .glpyhs file but also for the clipboard.

.. data:: GSFormatVersion1

	The Format used by Glyhs 2

.. data:: GSFormatVersion3

	The Format used by Glyhs 3

.. data:: GSFormatVersionCurrent

	This will always return the format of the current app.


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


Info Property Keys
==================

.. data:: GSPropertyNameFamilyNamesKey

	Family Names

.. data:: GSPropertyNameDesignersKey

	Designers

.. data:: GSPropertyNameDesignerURLKey

	Designer URL

.. data:: GSPropertyNameManufacturersKey

	Manufacturers

.. data:: GSPropertyNameManufacturerURLKey

	Manufacturer URL

.. data:: GSPropertyNameCopyrightsKey

	Copyrights

.. data:: GSPropertyNameVersionStringKey

	Version String

.. data:: GSPropertyNameVendorIDKey

	VendorID

.. data:: GSPropertyNameUniqueIDKey

	UniqueID

.. data:: GSPropertyNameLicensesKey

	Licenses

.. data:: GSPropertyNameLicenseURLKey

	License URL

.. data:: GSPropertyNameTrademarksKey

	Trademarks

.. data:: GSPropertyNameDescriptionsKey

	Descriptions

.. data:: GSPropertyNameSampleTextsKey

	SampleTexts

.. data:: GSPropertyNamePostscriptFontNameKey

	PostscriptFontName

.. data:: GSPropertyNameCompatibleFullNamesKey

	CompatibleFullNames

.. data:: GSPropertyNameStyleNamesKey

	StyleNames

.. data:: GSPropertyNameStyleMapFamilyNamesKey

	StyleMapFamilyNames

.. data:: GSPropertyNameStyleMapStyleNamesKey

	StyleMapStyleNames

.. data:: GSPropertyNamePreferredFamilyNamesKey

	PreferredFamilyNames

.. data:: GSPropertyNamePreferredSubfamilyNamesKey

	PreferredSubfamilyNames

.. data:: GSPropertyNameVariableStyleNamesKey

	VariableStyleNames

.. data:: GSPropertyNameWWSFamilyNameKey

	WWSFamilyName

.. data:: GSPropertyNameWWSSubfamilyNameKey

	WWSSubfamilyName

.. data:: GSPropertyNameVariationsPostScriptNamePrefixKey

	VariationsPostScriptNamePrefix

.. versionadded:: 3.1

Instance Types
==============

.. data:: INSTANCETYPESINGLE

	single interpolation instance

.. data:: INSTANCETYPEVARIABLE

	variable font setting

.. versionadded:: 3.0.1

Hint types
==========

.. data:: TOPGHOST

	Top ghost for PS hints

.. data:: STEM

	Stem for PS hints

.. data:: BOTTOMGHOST

	Bottom ghost for PS hints

.. data:: TTSNAP

	Snap for TT hints

.. data:: TTSTEM

	Stem for TT hints

.. data:: TTSHIFT

	Shift for TT hints

.. data:: TTINTERPOLATE

	Interpolation for TT hints

.. data:: TTDIAGONAL

	Diagonal for TT hints

.. data:: TTDELTA

	Delta TT hints

.. data:: CORNER

	Corner Component

	.. code-block:: python
		path = Layer.shapes[0]
		brush = GSHint()
		brush.name = "_corner.test"
		brush.type = CORNER
		brush.originNode = path.nodes[1]
		Layer.hints.append(brush)

.. data:: CAP

	Cap Component

.. data:: BRUSH

	Brush Component

	.. versionadded:: 3.1

.. data:: SEGMENT

	Segment Component

	.. versionadded:: 3.1


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

	.. deprecated:: 3.0.4
		please use DOCUMENTWILLCLOSE

.. data:: DOCUMENTWILLCLOSE

	is called just before a document will be closed
	
	the info object contains the GSWindowController object
	
	.. versionadded:: 3.0.4

.. data:: DOCUMENTDIDCLOSE

	is called after a document was closed
	
	the info object contains the NSDocument object
	
	.. versionadded:: 3.0.4

.. data:: TABDIDOPEN

	if a new tab is opened

.. data:: TABWILLCLOSE

	if a tab is closed

.. data:: UPDATEINTERFACE

	if some thing changed in the edit view. Maybe the selection or the glyph data.

.. data:: MOUSEMOVED

	is called if the mouse is moved. If you need to draw something, you need to call :meth:`Glyphs.redraw() <GSApplication.redraw()>` and also register to one of the drawing callbacks.

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

Shape Type
==========

.. data:: GSShapeTypePath

	Path

.. data:: GSShapeTypeComponent

	Component

Annotation types
================

.. data:: TEXT

.. data:: ARROW

.. data:: CIRCLE

.. data:: PLUS

.. data:: MINUS

'''
