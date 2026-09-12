# mypy: check_untyped_defs=True

from __future__ import annotations

import copy
import datetime
import math
import os
import re
import sys
import time
import traceback
from abc import ABC, abstractmethod
from typing import (
	TYPE_CHECKING,
	Any,
	Callable,
	Dict,
	Generic,
	Iterator,
	List,
	MutableMapping,
	Sequence,
	Type,
	TypeVar,
	cast,
	overload,
)

import objc
from AppKit import (
	NSApp,
	NSBundle,
	NSColor,
	NSControlStateValueMixed,
	NSControlStateValueOff,
	NSControlStateValueOn,
	NSDocumentController,
	NSError,
	NSLog,
	NSMenu,
	NSMenuItem,
	NSModalResponseOK,
	NSNotificationCenter,
	NSOpenPanel,
	NSSavePanel,
	NSUserDefaults,
	NSWorkspace,
	# NSImage,
)
from Foundation import (
	NSURL,
	NSAffineTransform,
	NSAffineTransformStruct,
	NSArray,
	NSAttributedString,
	NSClassFromString,
	NSConcreteValue,
	NSDate,
	NSDictionary,
	NSIndexSet,
	NSMakePoint,
	NSMakeRange,
	NSMutableArray,
	NSMutableAttributedString,
	NSMutableDictionary,
	NSNotFound,
	NSNull,
	NSNumber,
	NSObject,
	NSPoint,
	NSRange,
	NSRect,
	NSSelectorFromString,
	NSString,
)
from objc import python_method

objc.addConvenienceForClass(
	"GSApplication",
	(
		("currentDocument", property(lambda self: NSApp().currentFontDocument())),
		("versionNumber", property(lambda self: GSFloatVersion(self.versionString))),
		("buildNumber", property(lambda self: cast(NSNumber, NSBundle.mainBundle().objectForInfoDictionaryKey_("CFBundleVersion")).floatValue())),
	)
)


if TYPE_CHECKING:
	from .classes import (  # type: ignore
		FTPointArray,
		GlyphsToolKnife,
		GSAlignmentZone,
		GSAnchor,
		GSAnnotation,
		GSApplication,
		GSAxis,
		GSBackgroundImage,
		GSBackgroundLayer,
		GSCallbackHandler,
		GSClass,
		GSColorStop,
		GSComponent,
		GSControlLayer,
		GSCustomParameter,
		GSCustomParameterValueViewController,
		GSDocument,
		GSEditViewController,
		GSElement,
		GSExportInstanceOperation,
		GSFeature,
		GSFeatureGenerator,
		GSFeaturePrefix,
		GSFilterHandler,
		GSFont,
		GSFontMaster,
		GSFontViewController,
		GSGlyph,
		GSGlyphEditView,
		GSGlyphInfo,
		GSGlyphReference,
		GSGlyphsInfo,
		GSGradient,
		GSGuide,
		GSHandle,
		GSHint,
		GSImage,
		GSInfoProperty,
		GSInfoValue,
		GSInfoValueLocalized,
		GSInfoValueSingle,
		GSInstance,
		GSInterpolationFontProxy,
		GSLayer,
		GSMacroViewController,
		GSMetric,
		GSMetricStore,
		GSNode,
		GSNotifyingDictionary,
		GSParameterValueViewController,
		GSPartProperty,
		GSPath,
		GSPathFinder,
		GSPathPen,
		GSPathSegment,
		GSProjectDocument,
		GSPropertyDialogController,
		GSProxyShapes,
		GSSelectGlyphsDialogController,
		GSShape,
		GSShapeClass,
		GSSubstitution,
		GSToolGroup,
		GSTransformableElement,
		GSTTStem,
		GSUserNotification,
		GSValueStore,
		MGOrderedDictionary,
		PreviewTextWindow,
	)
else:
	GSFont: Type = objc.lookUpClass("GSFont")
	GSFontMaster = objc.lookUpClass("GSFontMaster")
	GSAxis = objc.lookUpClass("GSAxis")
	GSMetric = objc.lookUpClass("GSMetric")
	GSValueStore = objc.lookUpClass("GSValueStore")
	GSGlyph = objc.lookUpClass("GSGlyph")
	GSGlyphInfo = objc.lookUpClass("GSGlyphInfo")
	GSGlyphsInfo = objc.lookUpClass("GSGlyphsInfo")
	GSGuide = objc.lookUpClass("GSGuide")
	GSHint = objc.lookUpClass("GSHint")
	GSInstance = objc.lookUpClass("GSInstance")
	GSLayer = objc.lookUpClass("GSLayer")
	GSNode = objc.lookUpClass("GSNode")
	GSPath = objc.lookUpClass("GSPath")
	GSShapeClass = objc.lookUpClass("GSShape")
	GSShape = cast(Type['GSShape'], GSShapeClass)
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
	GSGlyphEditView = objc.lookUpClass("GSGlyphEditView")
	GSFontViewController = objc.lookUpClass("GSFontViewController")
	GSElement = objc.lookUpClass("GSElement")
	GSGradient = objc.lookUpClass("GSGradient")
	GSColorStop = objc.lookUpClass("GSColorStop")
	GSFeature = objc.lookUpClass("GSFeature")
	GSFeaturePrefix = objc.lookUpClass("GSFeaturePrefix")
	GSProxyShapes = objc.lookUpClass("GSProxyShapes")
	GSSubstitution = objc.lookUpClass("GSSubstitution")
	GSPartProperty = objc.lookUpClass("GSAxisPart")
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
	GSInfoValueLocalized = objc.lookUpClass("GSInfoValueLocalized")
	GSInfoValueSingle = objc.lookUpClass("GSInfoValueSingle")
	GSInfoValue = objc.lookUpClass("GSInfoValue")
	GSMetricStore = objc.lookUpClass("GSMetricStore")
	GSGlyphReference = objc.lookUpClass("GSGlyphReference")
	FTPointArray = objc.lookUpClass("FTPointArray")
	GSSelectGlyphsDialogController = objc.lookUpClass("GSSelectGlyphsDialogController")
	GSTransformableElement = objc.lookUpClass("GSTransformableElement")
	GSHandle = objc.lookUpClass("GSHandle")
	GSUserNotification = objc.lookUpClass("GSUserNotification")
	GSFilterHandler = objc.lookUpClass("GSFilterHandler")
	GSRoundCorner = objc.lookUpClass("GSRoundCorner")
	GSInfoProperty = objc.lookUpClass("GSInfoProperty")
	GSToolGroup = objc.lookUpClass("GSToolGroup")
	GSCustomParameterValueViewController = objc.lookUpClass("GSCustomParameterValueViewController")
	GSPropertyDialogController = objc.lookUpClass("GSPropertyDialogController")
	GSParameterValueViewController = objc.lookUpClass("GSParameterValueViewController")
	GSIconPreset = objc.lookUpClass("GSIconPreset")
__all__ = [

	"Glyphs", "GetFile",
	"wrapperVersion",
	"GSAlignmentZone", "GSAnchor", "GSAnnotation", "GSApplication", "GSBackgroundImage", "GSBackgroundLayer", "GSClass", "GSComponent", "GSControlLayer", "GSGlyphReference",
	"GSCustomParameter", "GSDocument", "GSProjectDocument", "GSEditViewController", "GSFontViewController", "GSElement", "GSFeature", "GSFeaturePrefix", "GSFont", "GSFontMaster",
	"GSGlyph", "GSGlyphInfo", "GSGlyphsInfo", "GSGuide", "GSHint", "GSInstance", "GSLayer", "GSNode", "GSPath", "GSShape", "GSSubstitution", "GSPartProperty", "GSAxis", "GSMetric", "GSMetricStore", "GSValueStore", "GSInfoValueLocalized", "GSInfoValueSingle", "GSInfoValue", "GSNotifyingDictionary", "GSGradient", "GSIconPreset",
	"GSPathFinder", "GSPathPen", "GSCallbackHandler", "GSFeatureGenerator", "GSTTStem", "GSPathSegment", "GSUserNotification",
	# Constants
	"MOVE", "LINE", "CURVE", "OFFCURVE", "QCURVE", "HOBBYCURVE", "GSRAPHNEWSPIRAL", "GSMOVE", "GSLINE", "GSCURVE", "GSQCURVE", "GSOFFCURVE", "GSHOBBYCURVE", "GSRAPHNEWSPIRAL", "GSSHARP", "GSSMOOTH", "GSSUPERSMOOTH",
	"FILL", "FILLCOLOR", "FILLPATTERNANGLE", "FILLPATTERNBLENDMODE", "FILLPATTERNFILE", "FILLPATTERNOFFSET", "FILLPATTERNSCALE", "STROKECOLOR", "STROKELINECAPEND", "STROKELINECAPSTART", "STROKELINEJOIN", "STROKEPOSITION", "STROKEWIDTH", "STROKEHEIGHT", "GRADIENT", "SHADOW", "INNERSHADOW", "MASK",
	"INSTANCETYPESINGLE", "INSTANCETYPEVARIABLE", "INSTANCETYPEICON",
	"TAG", "TOPGHOST", "STEM", "BOTTOMGHOST", "FLEX", "TTSNAP", "TTSTEM", "TTSHIFT", "TTINTERPOLATE", "TTDIAGONAL", "TTDELTA", "TTDONTROUND", "TTROUND", "TTROUNDUP", "TTROUNDDOWN", "TRIPLE",
	"TTANCHOR", "TTALIGN",  # backwards compatibility

	"CORNER", "CAP", "BRUSH", "SEGMENT",

	"TEXT", "ARROW", "CIRCLE", "PLUS", "MINUS",

	"GSBIDI", "GSLTR", "GSRTL", "GSVertical", "GSVerticalToRight", "GSTopLeft", "GSTopCenter", "GSTopRight", "GSCenterLeft", "GSCenterCenter", "GSCenterRight", "GSBottomLeft", "GSBottomCenter", "GSBottomRight",

	"GSAlignmentNoAligned", "GSAlignmentDisabled", "GSAlignmentDefault", "GSAlignmentForce", "GSAlignmentAligned", "GSAlignmentHorizontal",

	"CFF", "TT", "OTF", "TTF", "VARIABLE", "UFO", "WOFF", "WOFF2", "PLAIN", "VariableTT", "VariableCFF",

	"GSInspectorSizeSmall", "GSInspectorSizeRegular", "GSInspectorSizeLarge", "GSInspectorSizeXLarge",

	"GSPropertyNameFamilyNamesKey", "GSPropertyNameDesignersKey", "GSPropertyNameDesignerURLKey",
	"GSPropertyNameManufacturersKey", "GSPropertyNameManufacturerURLKey", "GSPropertyNameCopyrightsKey",
	"GSPropertyNameVersionStringKey", "GSPropertyNameVendorIDKey", "GSPropertyNameUniqueIDKey",
	"GSPropertyNameLicensesKey", "GSPropertyNameLicenseURLKey", "GSPropertyNameTrademarksKey",
	"GSPropertyNameDescriptionsKey", "GSPropertyNameSampleTextsKey", "GSPropertyNameFullFontNamesKey",
	"GSPropertyNamePostScriptNameKey", "GSPropertyNameCompatibleFullNamesKey",
	"GSPropertyNameStyleNamesKey", "GSPropertyNameStyleMapFamilyNamesKey",
	"GSPropertyNameStyleMapStyleNamesKey", "GSPropertyNamePreferredFamilyNamesKey",
	"GSPropertyNamePreferredSubfamilyNamesKey", "GSPropertyNameVariableStyleNamesKey",
	"GSPropertyNameWWSFamilyNameKey", "GSPropertyNameWWSSubfamilyNameKey",
	"GSPropertyNameVariablePostScriptNamePrefixKey",

	# Methods
	"divideCurve", "pointOnLine", "pointOnQuadratic", "distance", "addPoints", "subtractPoints", "GetFolder", "GetSaveFile", "GetOpenFile", "Message", "AskString", "PickGlyphs", "LogToConsole", "LogError", "removeOverlap", "subtractPaths", "intersectPaths", "scalePoint",

	# Menus
	"APP_MENU", "FILE_MENU", "EDIT_MENU", "GLYPH_MENU", "PATH_MENU", "FILTER_MENU", "VIEW_MENU", "SCRIPT_MENU", "WINDOW_MENU", "HELP_MENU",
	"ONSTATE", "OFFSTATE", "MIXEDSTATE",

	# Callbacks:

	"DRAWFOREGROUND", "DRAWBACKGROUND", "DRAWINACTIVE", "DOCUMENTOPENED", "DOCUMENTACTIVATED", "DOCUMENTWASSAVED", "DOCUMENTEXPORTED", "DOCUMENTCLOSED", "DOCUMENTWILLCLOSE", "DOCUMENTDIDCLOSE", "TABDIDOPEN", "TABWILLCLOSE", "UPDATEINTERFACE", "UPDATEEDITVIEWFRAME",
	"MOUSEMOVED", "MOUSEDRAGGED", "MOUSEDOWN", "MOUSEUP", "CONTEXTMENUCALLBACK", "FILTER_FLAT_KERNING",

	"GSMetricsKeyAscender", "GSMetricsKeyCapHeight", "GSMetricsKeySlantHeight", "GSMetricsKeyxHeight", "GSMetricsKeyTopHeight", "GSMetricsKeyDescender", "GSMetricsKeyBaseline",
	"GSNoCase", "GSUppercase", "GSLowercase", "GSSmallcaps", "GSMinor", "GSOtherCase",

	"GSFormatVersion1", "GSFormatVersion3", "GSFormatVersionCurrent",

	"GSShapeTypePath", "GSShapeTypeComponent",
	"PreviewTextWindow",
	"GSCustomParameterValueViewController", "GSPropertyDialogController", "GSParameterValueViewController"
]


wrapperVersion: str = "4.0"


def add_type(cls: Type[Any], name: str, typ: Any) -> None:
	if not hasattr(cls, '__annotations__'):
		cls.__annotations__ = {}
	cls.__annotations__[name] = typ


def ____CONSTANTS____(): pass


GSFormatVersion1: int = 1
GSFormatVersion3: int = 3
GSFormatVersionCurrent: int = 3

GSPackageFlatFile: int = 1
GSPackageBundle: int = 2

GSPropertyNameFamilyNamesKey: str = "familyNames"
GSPropertyNameDesignersKey: str = "designers"
GSPropertyNameDesignerURLKey: str = "designerURL"
GSPropertyNameManufacturersKey: str = "manufacturers"
GSPropertyNameManufacturerURLKey: str = "manufacturerURL"
GSPropertyNameCopyrightsKey: str = "copyrights"
GSPropertyNameVersionStringKey: str = "versionString"
GSPropertyNameVendorIDKey: str = "vendorID"
GSPropertyNameUniqueIDKey: str = "uniqueID"
GSPropertyNameLicensesKey: str = "licenses"
GSPropertyNameLicenseURLKey: str = "licenseURL"
GSPropertyNameTrademarksKey: str = "trademarks"
GSPropertyNameDescriptionsKey: str = "descriptions"
GSPropertyNameSampleTextsKey: str = "sampleTexts"
GSPropertyNameFullFontNamesKey: str = "postscriptFullNames"
GSPropertyNameFullFontNameKey: str = "postscriptFullName"  # Typo? or distinct key?
GSPropertyNamePostScriptNameKey: str = "postscriptFontName"
GSPropertyNameCompatibleFullNamesKey: str = "compatibleFullNames"
GSPropertyNameStyleNamesKey: str = "styleNames"
GSPropertyNameStyleMapFamilyNamesKey: str = "styleMapFamilyNames"
GSPropertyNameStyleMapStyleNamesKey: str = "styleMapStyleNames"
GSPropertyNamePreferredFamilyNamesKey: str = "preferredFamilyNames"
GSPropertyNamePreferredSubfamilyNamesKey: str = "preferredSubfamilyNames"
GSPropertyNameVariableStyleNamesKey: str = "variableStyleNames"
GSPropertyNameWWSFamilyNameKey: str = "WWSFamilyName"
GSPropertyNameWWSSubfamilyNameKey: str = "WWSSubfamilyName"
GSPropertyNameVariablePostScriptNamePrefixKey: str = "variationsPostScriptNamePrefix"

GSShapeTypePath: int = 1 << 1
GSShapeTypeComponent: int = 1 << 2

GSMOVE_: int = 17
GSLINE_: int = 1
GSCURVE_: int = 35
GSQCURVE_: int = 36
GSHOBBYCURVE_: int = 37
GSRAPHNEWSPIRAL_: int = 39
GSOFFCURVE_: int = 65
GSSHARP: int = 0
GSSMOOTH: int = 100
GSSUPERSMOOTH: int = 102

GSMOVE: str = "move"
GSLINE: str = "line"
GSCURVE: str = "curve"
GSQCURVE: str = "qcurve"
GSOFFCURVE: str = "offcurve"
GSHOBBYCURVE: str = "hobbycurve"
GSRAPHNEWSPIRAL: str = "raphnewspiral"

MOVE: str = "move"
LINE: str = "line"
CURVE: str = "curve"
QCURVE: str = "qcurve"
OFFCURVE: str = "offcurve"
HOBBYCURVE: str = "hobbycurve"
RAPHNEWSPIRAL: str = "raphnewspiral"

# Path Attributes
FILL: str = "fill"
FILLCOLOR: str = "fillColor"
FILLPATTERNANGLE: str = "fillPatternAngle"
FILLPATTERNBLENDMODE: str = "fillPatternBlendMode"
FILLPATTERNFILE: str = "fillPatternFile"
FILLPATTERNOFFSET: str = "fillPatternOffset"
FILLPATTERNSCALE: str = "fillPatternScale"
STROKECOLOR: str = "strokeColor"
STROKELINECAPEND: str = "lineCapEnd"
STROKELINECAPSTART: str = "lineCapStart"
STROKELINEJOIN: str = "lineJoin"
STROKEPOSITION: str = "strokePos"
STROKEWIDTH: str = "strokeWidth"
STROKEHEIGHT: str = "strokeHeight"
GRADIENT: str = "gradient"
SHADOW: str = "shadow"
INNERSHADOW: str = "shadowIn"
MASK: str = "mask"

# instance type

INSTANCETYPESINGLE: int = 0
INSTANCETYPEVARIABLE: int = 1
INSTANCETYPEICON: int = 3

TAG: int = -2
TOPGHOST: int = -1
STEM: int = 0
BOTTOMGHOST: int = 1
FLEX: int = 2
TTSNAP: int = 3
TTANCHOR: int = 3  # backwards compatibility
TTSTEM: int = 4
TTSHIFT: int = 5
TTALIGN: int = 5  # backwards compatibility
TTINTERPOLATE: int = 6
TTDIAGONAL: int = 8
TTDELTA: int = 9
CORNER: int = 16
CAP: int = 17
BRUSH: int = 18
SEGMENT: int = 19

TTDONTROUND: int = 4
TTROUND: int = 0
TTROUNDUP: int = 1
TTROUNDDOWN: int = 2
TRIPLE: int = 128

# annotations:
TEXT: int = 1
ARROW: int = 2
CIRCLE: int = 3
PLUS: int = 4
MINUS: int = 5

CFF: str = "CFF"
CFF2: str = "CFF2"
TT: str = "TT"
OTF: str = "OTF"
TTF: str = "TTF"
VARIABLE: str = "variableTT"
VariableTT: str = "variableTT"
VariableCFF: str = "variableCFF"
UFO: str = "UFO"
WOFF: str = "WOFF"
WOFF2: str = "WOFF2"
PLAIN: str = "plain"

GSOutlineFormatCFF: int = 1
GSOutlineFormatTrueType: int = 2
GSOutlineFormatVariableTT: int = 3
GSOutlineFormatVariableCFF: int = 4

GSMetricsKeyAscender: str = "ascender"
GSMetricsKeyCapHeight: str = "cap height"
GSMetricsKeySlantHeight: str = "slant height"  # defaults to half xHeight
GSMetricsKeyxHeight: str = "x-height"
GSMetricsKeyTopHeight: str = "topHeight"  # global top boundary, can be xHeight, CapHeight, ShoulderHeight...
GSMetricsKeyDescender: str = "descender"
GSMetricsKeyBaseline: str = "baseline"

GSMetricsTypeUndefined: int = 0
GSMetricsTypeAscender: int = 1
GSMetricsTypeCapHeight: int = 2
GSMetricsTypeSlantHeight: int = 3
GSMetricsTypexHeight: int = 4
GSMetricsTypeMidHeight: int = 5
GSMetricsTypeBodyHeight: int = 6
GSMetricsTypeDescender: int = 7
GSMetricsTypeBaseline: int = 8
GSMetricsTypeItalicAngle: int = 9

GSNoCase: int = 0
GSUppercase: int = 1
GSLowercase: int = 2
GSSmallcaps: int = 3
GSMinor: int = 4
GSOtherCase: int = 5  # ??

GSTopLeft: int = 6
GSTopCenter: int = 7
GSTopRight: int = 8
GSCenterLeft: int = 3
GSCenterCenter: int = 4
GSCenterRight: int = 5
GSBottomLeft: int = 0
GSBottomCenter: int = 1
GSBottomRight: int = 2

# Writing direction
GSBIDI: int = 1
GSLTR: int = 0
GSRTL: int = 2
GSVertical: int = 4  # CJK
GSVerticalToRight: int = 8  # Mongolian

GSAlignmentNoAligned: int = -2
GSAlignmentDisabled: int = -1
GSAlignmentDefault: int = 0
GSAlignmentForce: int = 1
GSAlignmentAligned: int = 2
GSAlignmentHorizontal: int = 3

# Callbacks
DRAWFOREGROUND: str = "DrawForeground"
DRAWBACKGROUND: str = "DrawBackground"
DRAWINACTIVE: str = "DrawInactive"
DOCUMENTOPENED: str = "GSDocumentWasOpenedNotification"
DOCUMENTACTIVATED: str = "GSDocumentActivateNotification"
DOCUMENTWASSAVED: str = "GSDocumentWasSavedSuccessfully"
DOCUMENTEXPORTED: str = "GSDocumentWasExportedNotification"
DOCUMENTCLOSED: str = "GSDocumentWillCloseNotification"  # deprecated use DOCUMENTWILLCLOSE
DOCUMENTWILLCLOSE: str = "GSDocumentWillCloseNotification"
DOCUMENTDIDCLOSE: str = "GSDocumentDidCloseNotification"
TABDIDOPEN: str = "TabDidOpenNotification"
TABWILLCLOSE: str = "TabWillCloseNotification"
UPDATEINTERFACE: str = "GSUpdateInterface"
UPDATEEDITVIEWFRAME: str = "GSUpdateEditViewFrame"
MOUSEMOVED: str = "mouseMovedNotification"
MOUSEDRAGGED: str = "mouseDraggedNotification"
MOUSEDOWN: str = "mouseDownNotification"
MOUSEUP: str = "mouseUpNotification"
CONTEXTMENUCALLBACK: str = "GSContextMenuCallbackName"
FILTER_FLAT_KERNING: str = "GSFilterFlatKerning"

# Menus
APP_MENU: str = "APP_MENU"
FILE_MENU: str = "FILE_MENU"
EDIT_MENU: str = "EDIT_MENU"
GLYPH_MENU: str = "GLYPH_MENU"
PATH_MENU: str = "PATH_MENU"
FILTER_MENU: str = "FILTER_MENU"
VIEW_MENU: str = "VIEW_MENU"
SCRIPT_MENU: str = "SCRIPT_MENU"
WINDOW_MENU: str = "WINDOW_MENU"
HELP_MENU: str = "HELP_MENU"

ONSTATE: int = NSControlStateValueOn
OFFSTATE: int = NSControlStateValueOff
MIXEDSTATE: int = NSControlStateValueMixed

GSInspectorSizeSmall: int = 1
GSInspectorSizeRegular: int = 2
GSInspectorSizeLarge: int = 3
GSInspectorSizeXLarge: int = 4
'''

Changes in the API
==================

These changes could possibly break your code, so you need to keep track of them. Please see :attr:`GSApplication.versionNumber` for how to check for the app version in your code. Really, read it. There’s a catch.
'''

def __empty__init__(self) -> None:
	pass


def __GSObject__copy__(self: NSObject, memo: Any | None = None) -> Any:
	return self.copy()


NSObject.__copy__ = python_method(__GSObject__copy__)  # type: ignore
NSObject.__deepcopy__ = python_method(__GSObject__copy__)  # type: ignore


def __GSObject__deepcopy__(self: NSObject, memo: Any | None = None) -> Any:  # Returns Self
	return self.deepMutableCopy()  # type: ignore

NSArray.__deepcopy__ = python_method(__GSObject__deepcopy__)  # type: ignore
NSDictionary.__deepcopy__ = python_method(__GSObject__deepcopy__)  # type: ignore
MGOrderedDictionary.__deepcopy__ = python_method(__GSObject__deepcopy__)  # type: ignore


def __GSObject__new__(typ: Type[NSObject], *args: Any, **kwargs: Any) -> NSObject:
	"""__new__(...)"""
	return typ.alloc().init()


def _validate_idx(self: Sequence[Any], idx: int, offset: int = 0) -> int:
	if not isinstance(idx, int):
		raise TypeError(f"indices must be integers, not {type(idx).__name__}")
	if idx < 0:
		idx += len(self)
	if not (0 <= idx < len(self) + offset):
		raise IndexError(f"index {idx} out of range (size {len(self)})")
	return idx

T = TypeVar('T')
# K = TypeVar('K')  # Key type for mappings
V = TypeVar('V')  # Value type for mappings (can be T for sequences)

type OwnerType = GSFont | GSFontMaster | GSInstance

class OrderedDictProxy(Generic[T], ABC):  # T is the type of items in the sequence/values in mapping

	_owner: OwnerType
	KEY_TYPE: Type = str

	def __init__(self, owner: OwnerType) -> None:
		self._owner = owner

	#
	# —— Sequence protocol ——
	#
	def __iter__(self) -> Iterator[T]:
		return iter(self.values())

	def __len__(self) -> int:
		return len(self.values())

	def insert(self, index: int, value: T) -> None:
		idx = _validate_idx(cast(Sequence, self), index, offset=1)
		self.insertAtIndex(idx, value)

	# For a class that can be accessed by int (sequence) or K (mapping-like key)
	@overload
	def __getitem__(self, key: int) -> T: ...
	@overload
	def __getitem__(self, key: str) -> T: ...

	def __getitem__(self, key: int | str | slice) -> T | List[T]:
		if isinstance(key, int):
			idx = _validate_idx(cast(Sequence, self), key)
			return self.getByIndex(idx)
		elif isinstance(key, slice):
			# Handle slice access
			length = len(self)
			start, stop, step = key.indices(length)
			# Collect items at the specified indices
			result = []
			for idx in range(start, stop, step):
				result.append(self.getByIndex(idx))
			return result
		elif not self.KEY_TYPE or isinstance(key, self.KEY_TYPE):
			return self.getByKey(key)
		else:
			raise TypeError(f"Keys must be integers or strings, not {type(key).__name__}")

	@overload
	def __setitem__(self, key: int, value: T) -> None: ...
	@overload
	def __setitem__(self, key: str, value: T) -> None: ...

	def __setitem__(self, key: int | str, value: T) -> None:
		if isinstance(key, int):
			idx = _validate_idx(cast(Sequence, self), key)
			self.setByIndex(idx, value)
		elif not self.KEY_TYPE or isinstance(key, self.KEY_TYPE):
			self.setByKey(key, value)
		else:
			raise TypeError(f"Keys must be integers or strings, not {type(key).__name__}")

	@overload
	def __delitem__(self, key: int) -> None: ...
	@overload
	def __delitem__(self, key: str) -> None: ...

	def __delitem__(self, key: int | str) -> None:
		if isinstance(key, int):
			idx = _validate_idx(cast(Sequence, self), key)
			self.removeByIndex(idx)
		elif isinstance(key, slice):
			# Handle slice deletion
			length = len(self)
			start, stop, step = key.indices(length)
			indices_to_delete = reversed(range(start, stop, step))
			for idx in indices_to_delete:
				self.removeByIndex(idx)
		elif not self.KEY_TYPE or isinstance(key, self.KEY_TYPE):
			self.removeByKey(key)
		else:
			raise TypeError(f"Keys must be integers or strings, not {type(key).__name__}")

	@overload
	def pop(self, key: int = -1) -> T: ...
	@overload
	def pop(self, key: str) -> T: ...

	def pop(self, key: int | str = -1) -> T:
		if isinstance(key, int):
			idx = key if key != -1 else len(self) - 1
			idx = _validate_idx(cast(Sequence, self), idx)
			item: T = self.values()[idx]
			self.removeByIndex(idx)
			return item
		else:
			item = self.getByKey(key)
			self.removeByKey(key)
			return item

	def keys(self) -> List[str]:
		return [self.getKeyOf(v) for v in self.values()]

	def items(self) -> Iterator[tuple[str, T]]:
		for v in self.values():
			yield (self.getKeyOf(v), v)

	def get(self, key: str, default: Any = None) -> T:
		try:
			return self.getByKey(key)
		except KeyError:
			return default

	def __contains__(self, key: Any) -> bool:
		if isinstance(key, int):
			try:
				_validate_idx(cast(Sequence, self), key)
				return True
			except IndexError:
				return False
		try:
			self.getByKey(key)  # Assuming key is of type str
			return True
		except (KeyError, TypeError):  # TypeError if key is not hash-able or not of type str
			pass
		return False

	def __str__(self) -> str:
		body = ''.join(f'\t{v},\n' for v in self.values())
		if len(body) > 0:
			body = "\n" + body
		return '(' + body + ')'

	def __repr__(self) -> str:
		body = ''.join(f'\t{repr(v)},\n' for v in self.values())
		if len(body) > 0:
			body = "\n" + body
		return f"<GlyphsApp.{self.__class__.__name__} at 0x{hex(id(self))} ({body})>"

	def index(self, value: T) -> int:
		return self.values().index(value)

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

	def clear(self) -> None:
		self.setter(None)

	#
	# —— Your subclass must override these seven methods ——
	#
	@abstractmethod
	def values(self) -> List[T]:
		"""Return the ordered list of items."""
		raise NotImplementedError

	@abstractmethod
	def getKeyOf(self, value: T) -> str:
		"""Extract the key (e.g. name) from a single item."""
		raise NotImplementedError

	@abstractmethod
	def getByKey(self, key: str) -> T:
		"""Lookup an item by its key (must raise KeyError if missing)."""
		raise NotImplementedError

	@abstractmethod
	def getByIndex(self, idx: int) -> T:
		"""Lookup an item by its index (must raise IndexError if missing)."""
		raise NotImplementedError

	@abstractmethod
	def removeByIndex(self, idx: int) -> None:
		"""Remove the item at position `idx`."""
		raise NotImplementedError

	@abstractmethod
	def removeByKey(self, key: str) -> None:
		"""Remove the item with that key (or raise KeyError)."""
		raise NotImplementedError

	# @abstractmethod
	def remove(self, item: T) -> None:
		"""Remove the item (or raise KeyError)."""
		raise NotImplementedError

	@abstractmethod
	def setByIndex(self, idx: int, value: T) -> None:
		"""Overwrite the item at position `idx`."""
		raise NotImplementedError

	@abstractmethod
	def setByKey(self, key: str, value: T) -> None:
		"""Replace the item at key with `value` (or raise KeyError)."""
		raise NotImplementedError

	@abstractmethod
	def insertAtIndex(self, idx: int, value: T) -> None:
		"""Insert a new item at position `idx`."""
		raise NotImplementedError

	def append(self, value: T) -> None:
		"""Insert a new item at position `idx`."""
		raise NotImplementedError

	def extend(self, values: List[T]) -> None:
		"""Extends the items."""
		for value in values:
			self.append(value)


class ListProxy(Generic[T], ABC):  # T is the type of items in the sequence
	_owner: OwnerType

	def __init__(self, owner: OwnerType) -> None:
		self._owner = owner

	#
	# —— Sequence protocol ——
	#
	def __iter__(self) -> Iterator[T]:
		return iter(self.values())

	def __len__(self) -> int:
		return len(self.values())

	def insert(self, idx: int, value: T) -> None:
		if not isinstance(idx, int):
			raise TypeError(f"list indices must be integers or slices, not {type(idx).__name__}")

		idx = _validate_idx(cast(Sequence, self), idx, offset=1)
		self.insertAtIndex(idx, value)

	def __getitem__(self, key: int) -> T:
		if isinstance(key, int):
			idx = _validate_idx(cast(Sequence, self), key)
			return self.getByIndex(idx)
		elif isinstance(key, slice):
			# Handle slice access
			length = len(self)
			start, stop, step = key.indices(length)
			# Collect items at the specified indices
			result = []
			for idx in range(start, stop, step):
				result.append(self.getByIndex(idx))
			return result
		else:
			raise TypeError(f"list indices must be integers or slices, not {type(key).__name__}")

	def __setitem__(self, key: int, value: T) -> None:
		if isinstance(key, int):
			idx = _validate_idx(cast(Sequence, self), key)
			self.setByIndex(idx, value)
		elif isinstance(key, slice):
			length = len(self)
			start, stop, step = key.indices(length)
			indices_to_replace = list(range(start, stop, step))

			# Convert value to list
			if not isinstance(value, (list, tuple, Sequence)):
				try:
					new_values = list(value)
				except TypeError:
					raise TypeError("can only assign an iterable")
			else:
				new_values = list(value)

			# Check that lengths match for extended slices
			if len(indices_to_replace) != len(new_values):
				raise ValueError(
					f"attempt to assign sequence of size {len(new_values)} "
					f"to extended slice of size {len(indices_to_replace)}"
				)

			# Replace items at specified indices
			for idx, new_value in zip(indices_to_replace, new_values):
				self.setByIndex(idx, new_value)
		else:
			raise TypeError(f"list indices must be integers or slices, not {type(idx).__name__}")

	def __delitem__(self, idx: int | slice) -> None:
		if isinstance(idx, int):
			idx = _validate_idx(cast(Sequence, self), idx)
			self.removeByIndex(idx)
		elif isinstance(idx, slice):
			# Handle slice deletion
			length = len(self)
			start, stop, step = idx.indices(length)
			indices_to_delete = reversed(range(start, stop, step))
			for jdx in indices_to_delete:
				self.removeByIndex(jdx)
		else:
			raise TypeError(f"list indices must be integers or slices, not {type(idx).__name__}")

	def pop(self, key: int = -1) -> T:
		if isinstance(key, int):
			idx = key if key != -1 else len(self) - 1
			idx = _validate_idx(cast(Sequence, self), idx)
			item: T = self.values()[idx]
			self.removeByIndex(idx)
			return item
		else:
			raise TypeError(f"list indices must be integers or slices, not {type(idx).__name__}")

	def __contains__(self, key: Any) -> bool:
		if isinstance(key, int):
			try:
				_validate_idx(cast(Sequence, self), key)
				return True
			except IndexError:
				pass
		return False

	def index(self, value: T) -> int:
		return self.values().index(value)

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

	def remove(self, value: T) -> None:
		"""Remove the first occurrence of value from the list.
		Raises ValueError if the value is not found.
		"""
		try:
			idx = self.index(value)
			self.removeByIndex(idx)
		except ValueError:
			raise ValueError(f"{value!r} not in list")

	def __copy__(self) -> list:
		return list(self.values())

	def __deepcopy__(self, memo) -> list:
		return [cast(NSObject, x).copy() for x in self.values()]

	def __str__(self) -> str:
		body = ''.join(f'\t{v},\n' for v in self.values())
		if len(body) > 0:
			body = "\n" + body
		return '(' + body + ')'

	def __repr__(self) -> str:
		body = ''.join(f'\t{repr(v)},\n' for v in self.values())
		if len(body) > 0:
			body = "\n" + body
		return f"<GlyphsApp.{self.__class__.__name__} at 0x{hex(id(self))} ({body})>"

	@abstractmethod
	def values(self) -> List[T]:
		"""Return the ordered list of items."""
		raise NotImplementedError

	@abstractmethod
	def getByIndex(self, idx: int) -> T:
		"""Lookup an item by its index (must raise IndexError if missing)."""
		raise NotImplementedError

	@abstractmethod
	def removeByIndex(self, idx: int) -> None:
		"""Remove the item at position `idx`."""
		raise NotImplementedError

	@abstractmethod
	def setByIndex(self, idx: int, value: T) -> None:
		"""Overwrite the item at position `idx`."""
		raise NotImplementedError

	@abstractmethod
	def insertAtIndex(self, idx: int, value: T) -> None:
		"""Insert a new item at position `idx`."""
		raise NotImplementedError


class DictProxy(Generic[T], ABC):
	"""A proxy for dictionary-like objects where K is the key type and T is the value type."""

	_owner: 'OwnerType'
	KEY_TYPE: Type = str

	def __init__(self, owner: 'OwnerType') -> None:
		self._owner = owner

	def __len__(self) -> int:
		return len(self.values())

	def __getitem__(self, key: str) -> T:
		if self.KEY_TYPE and not isinstance(key, self.KEY_TYPE):
			raise TypeError(f"Key must be strings, not {type(key).__name__}")
		return self.getByKey(key)

	def __setitem__(self, key: str, value: T) -> None:
		if self.KEY_TYPE and not isinstance(key, self.KEY_TYPE):
			raise TypeError(f"Key must be strings, not {type(key).__name__}")
		self.setByKey(key, value)

	def __delitem__(self, key: str) -> None:
		if self.KEY_TYPE and not isinstance(key, self.KEY_TYPE):
			raise TypeError(f"Key must be strings, not {type(key).__name__}")
		self.removeByKey(key)

	def __iter__(self) -> Iterator[str]:
		"""Iterate over keys (standard dict behavior)."""
		return iter(self.keys())

	def keys(self) -> List[str]:
		return [self.getKeyOf(v) for v in self.values()]

	def items(self) -> Iterator[tuple[str, T]]:
		for v in self.values():
			yield (self.getKeyOf(v), v)

	def get(self, key: str, default: Any = None) -> T | Any:
		if self.KEY_TYPE and not isinstance(key, self.KEY_TYPE):
			raise TypeError(f"Key must be strings, not {type(key).__name__}")
		try:
			return self.getByKey(key)
		except KeyError:
			return default

	def __contains__(self, key: Any) -> bool:
		if self.KEY_TYPE and not isinstance(key, self.KEY_TYPE):
			raise TypeError(f"Key must be strings, not {type(key).__name__}")
		try:
			return self.getByKey(key) is not None
		except (KeyError, TypeError):  # TypeError if key is not hashable or not of type str
			return False

	def pop(self, key: str, default: Any = None) -> T | Any:
		"""Remove and return the value for key, or default if not found."""
		if self.KEY_TYPE and not isinstance(key, self.KEY_TYPE):
			raise TypeError(f"Key must be strings, not {type(key).__name__}")
		try:
			value = self.getByKey(key)
			self.removeByKey(key)
			return value
		except KeyError:
			if default is None:
				raise
			return default

	def setdefault(self, key: str, default: T = None) -> T:
		"""Insert key with default value if key is not in the dictionary."""
		if self.KEY_TYPE and not isinstance(key, self.KEY_TYPE):
			raise TypeError(f"Key must be strings, not {type(key).__name__}")

		try:
			return self.getByKey(key)
		except KeyError:
			self.setByKey(key, default)
			return default

	def clear(self) -> None:
		"""Remove all items from the dictionary."""
		# Create a copy of keys to avoid modification during iteration
		keys_to_remove = list(self.keys())
		for key in keys_to_remove:
			self.removeByKey(key)

	def setterMethod(self):
		raise AttributeError("This collection cannot be directly overwritten")

	def setter(self, values):
		method = self.setterMethod()
		if isinstance(values, (list, NSArray)):
			method('NSMutableArray'.arrayWithArray_(values))
		elif isinstance(values, (tuple, type(self))):
			method('NSMutableArray'.arrayWithArray_(list(values)))
		elif values is None:
			method('NSMutableArray'.array())
		else:
			raise TypeError("Can't set value of type %s" % type(values).__name__)

	#
	# —— Your subclass must override these methods ——
	#

	@abstractmethod
	def values(self) -> List[T]:
		"""Return the ordered list of items."""
		raise NotImplementedError

	@abstractmethod
	def getKeyOf(self, value: T) -> str:
		"""Extract the key (e.g. name) from a single item."""
		raise NotImplementedError

	@abstractmethod
	def getByKey(self, key: str) -> T:
		"""Lookup an item by its key (must raise KeyError if missing)."""
		raise NotImplementedError

	@abstractmethod
	def removeByKey(self, key: str) -> None:
		"""Remove the item with that key (or raise KeyError)."""
		raise NotImplementedError

	@abstractmethod
	def setByKey(self, key: str, value: T) -> None:
		"""Replace the item at key with `value` (or raise KeyError)."""
		raise NotImplementedError


class GSProxyShapesIterator:
	proxy: GSProxyShapes
	n: int

	def __init__(self, proxy: GSProxyShapes) -> None:
		self.proxy = proxy
		self.n = 0

	def __iter__(self) -> GSProxyShapesIterator:
		return self

	def __next__(self) -> GSShape:
		shape = self.proxy.objectAtIndex_(self.n)
		self.n += 1
		if shape:
			return shape
		else:
			raise StopIteration


def GSProxyShapes__iter__(self: GSProxyShapes) -> GSProxyShapesIterator:
	return GSProxyShapesIterator(self)

GSProxyShapes.__iter__ = python_method(GSProxyShapes__iter__)  # type: ignore

@overload
def __GSProxyShapes__getitem__(self: GSProxyShapes, idx: int) -> GSShape: ...
@overload
def __GSProxyShapes__getitem__(self: GSProxyShapes, idx: slice) -> List[GSShape]: ...
def __GSProxyShapes__getitem__(self: GSProxyShapes, idx: int | slice) -> GSShape | List[GSShape]:
	if isinstance(idx, slice):
		# PyObjC sequence slicing might work directly or need manual implementation
		indices = idx.indices(self.count())
		return [self.objectAtIndex_(i) for i in range(*indices)]
	if idx < self.count():
		return self.objectAtIndex_(idx)
	raise IndexError("list index out of range")


GSProxyShapes.__getitem__ = python_method(__GSProxyShapes__getitem__)  # type: ignore
GSProxyShapes.__len__ = property(lambda self: self.count)  # type: ignore
add_type(GSProxyShapes, '__len__', int)


GSProxyShapes.__contains__ = python_method(lambda self, item: self.containsObject_(item))  # type: ignore
add_type(GSProxyShapes, '__contains__', Callable[[GSProxyShapes, GSShape], bool])


def ProxyShapes__str__(self: GSProxyShapes) -> str:
	strings: List[str] = []
	for currItem in self:
		strings.append(str(currItem))
	if len(strings) == 0:
		return "()"
	return "(\n\t%s\n)" % (',\n\t'.join(strings))


GSProxyShapes.__str__ = python_method(ProxyShapes__str__)  # type: ignore

def ProxyShapes__repr__(self: GSProxyShapes) -> str:
	strings: List[str] = []
	for currItem in self:
		strings.append(repr(currItem))
	if len(strings) == 0:
		return "()"
	return "(\n\t%s\n)" % (',\n\t'.join(strings))


GSProxyShapes.__repr__ = python_method(ProxyShapes__repr__)  # type: ignore

##################################################################################
#
#
#
#           GSApplication
#
#
#
##################################################################################


Glyphs: GSApplication = NSApp()

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
		* :attr:`currentDocument`
		* :attr:`documents`
		* :attr:`font`
		* :attr:`fonts`
		* :attr:`reporters`
		* :attr:`activeReporters`
		* :attr:`filters`
		* :attr:`defaults`
		* :attr:`scriptAbbreviations`
		* :attr:`scriptSuffixes`
		* :attr:`languageScripts`
		* :attr:`languageData`
		* :attr:`unicodeRanges`
		* :attr:`editViewWidth`
		* :attr:`handleSize`
		* :attr:`versionString`
		* :attr:`versionNumber`
		* :attr:`buildNumber`
		* :attr:`menu`

	Functions

		* :meth:`open`
		* :meth:`showMacroWindow`
		* :meth:`clearLog`
		* :meth:`showGlyphInfoPanelWithSearchString`
		* :meth:`glyphInfoForName()`
		* :meth:`glyphInfoForUnicode()`
		* :meth:`niceGlyphName()`
		* :meth:`productionGlyphName()`
		* :meth:`ligatureComponents()`
		* :meth:`addCallback()`
		* :meth:`removeCallback()`
		* :meth:`redraw()`
		* :meth:`showNotification()`
		* :meth:`localize()`
		* :meth:`activateReporter()`
		* :meth:`deactivateReporter()`


	**Properties**
'''

# GSApplication.currentDocument already handled by addConvenienceForClass or should be added with add_type
# add_type(GSApplication, "currentDocument", GSDocument | None)
'''
	.. attribute:: currentDocument
		The active :class:`GSDocument` object or None.

		:type: :class:`GSDocument`

		.. code-block:: python
			# topmost open document
			document = Glyphs.currentDocument
'''


GSApplication.documents = property(lambda self: AppDocumentProxy(self))  # type: ignore
add_type(GSApplication, "documents", List['GSDocument'])
'''
	.. attribute:: documents

		An array of open :class:`GSDocument` objects.

		:type: list
'''


def __GSApp__str__(self: GSApplication) -> str:
	return '<Glyphs.app>'


GSApplication.__str__ = python_method(__GSApp__str__)  # type: ignore


def __GSApp_currentFont__() -> GSFont | None:
	try:
		doc: GSDocument | None = NSApp().currentFontDocument()
		if doc:
			return doc.font
	except AttributeError:
		pass
	return None


GSApplication.font = property(lambda self: __GSApp_currentFont__())  # type: ignore
add_type(GSApplication, "font", GSFont | None)
'''
	.. attribute:: font

		The active :class:`GSFont` object or None.

		:type: :class:`GSFont`
'''


GSApplication.fonts = property(lambda self: AppFontProxy(self))  # type: ignore
add_type(GSApplication, "fonts", List[GSFont])  # Or List[GSFont]
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
			font.familyName = "My New Font"
			Glyphs.fonts.append(font)
'''


GSApplication.reporters = property(lambda self: GSCallbackHandler.reporterInstances().allValues())  # type: ignore
add_type(GSApplication, "reporters", List[Any])  # List of reporter plugin instances
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
			Glyphs.activateReporter(Glyphs.reporters[0])  # by object
			Glyphs.activateReporter('GlyphsMasterCompatibility')  # by class name
'''


GSApplication.activeReporters = property(lambda self: GSCallbackHandler.activeReporters())  # type: ignore
add_type(GSApplication, "activeReporters", List[Any])  # List of active reporter instances
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


GSApplication.filters = property(lambda self: list(GSFilterHandler.filterInstances()))  # type: ignore
add_type(GSApplication, "filters", List[Any])  # List of filter plugin instances
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
STR_TYPES: tuple[Type[str], Type[objc.pyobjc_unicode]] = (str, objc.pyobjc_unicode)  # type: ignore

def isString(string: Any) -> bool:
	return isinstance(string, STR_TYPES)

def objcObject(pyObject: Any) -> NSObject:
	if isString(pyObject):
		return NSString.stringWithString_(pyObject)
	if isinstance(pyObject, bool):
		return NSNumber.numberWithBool_(pyObject)
	if isinstance(pyObject, int):
		return NSNumber.numberWithInteger_(pyObject)
	if isinstance(pyObject, float):
		return NSNumber.numberWithFloat_(pyObject)
	if isinstance(pyObject, list):
		array: NSMutableArray = NSMutableArray.new()
		for value in pyObject:
			array.addObject_(objcObject(value))
		return array
	if isinstance(pyObject, dict):
		dictionary: NSMutableDictionary = NSMutableDictionary.new()
		for key, value in pyObject.items():
			dictionary.setObject_forKey_(objcObject(value), objcObject(key))
		return dictionary
	if pyObject is None:
		return NSNull.null()
	return pyObject  # Assuming pyObject is already an NSObject or compatible

def validatePoint(value: tuple[float, float] | NSPoint) -> tuple[float, float]:
	return validateTuple(2, value)  # type: ignore

def validateScale(value: float | tuple[float, ...]) -> tuple[float, float]:
	# Assuming validateTuple handles conversion from single float to tuple
	v = validateTuple(1, value)  # type: ignore
	if len(v) == 1:
		return (v[0], v[0])
	elif len(v) == 2:
		return (v[0], v[1])  # type: ignore
	raise ValueError("Scale must be a number or a tuple of two numbers")


def validateTuple(expectedLength: int, value: Any) -> tuple[float, ...]:
	if value is None:
		if expectedLength == 2:
			return (0.0, 0.0)
		if expectedLength == 1:
			return (0.0,)
		# Adjust for other expected lengths or raise error
		return tuple([0.0] * expectedLength)

	if expectedLength == 1 and isinstance(value, (float, int)):
		value = (float(value),)
	if not isinstance(value, (tuple, NSPoint)):  # NSPoint is tuple-like
		raise TypeError(f"Expected tuple or NSPoint, not {type(value).__name__}")
	if len(value) < expectedLength:
		raise ValueError(f"Expected at least {expectedLength} items, not {len(value)}")

	# Ensure all elements are numbers and convert to float
	processed_value: List[float] = []
	for v_item in value:
		if not isinstance(v_item, (float, int)):
			raise TypeError(f"Tuple elements must be float or int, not {type(v_item).__name__}")
		processed_value.append(float(v_item))
	return tuple(processed_value)


def validateNumber(value: Any) -> float | int:
	if value is None:
		return 0
	if not isinstance(value, (float, int)):
		raise TypeError(f"Expect float or int, not {type(value).__name__}")
	return value


class DefaultsProxy(MutableMapping[str, Any]):
	"""
	A dict-like proxy for NSUserDefaults.
	Keys must be str; values can be any ObjC object or None.
	"""

	def __getitem__(self, key: str) -> Any:
		if not isinstance(key, str):
			raise TypeError(f"default key must be str, not {type(key).__name__}")
		obj: Any = NSUserDefaults.standardUserDefaults().objectForKey_(objcObject(key))
		return obj

	def __setitem__(self, key: str, value: Any) -> None:
		if not isString(key):
			raise TypeError(f"defaults key must be str, not {type(key).__name__}")
		if value is not None:
			NSUserDefaults.standardUserDefaults().setObject_forKey_(objcObject(value), objcObject(key))
		else:  # value is None means remove
			NSUserDefaults.standardUserDefaults().removeObjectForKey_(objcObject(key))

	def __delitem__(self, key: str) -> None:
		if not isString(key):
			raise TypeError(f"defaults key must be str, not {type(key).__name__}")
		NSUserDefaults.standardUserDefaults().removeObjectForKey_(objcObject(key))

	def get(self, key: str, default: Any = None) -> Any:
		if not isString(key):
			raise TypeError(f"defaults key must be str, not {type(key).__name__}")
		value: Any = NSUserDefaults.standardUserDefaults().objectForKey_(objcObject(key))
		if value is None:  # This includes key not found or key explicitly set to nil
			return default
		return value

	def pop(self, key: str) -> Any:
		if isinstance(key, str):
			# doesn‘t make sense to delete the value. This is mostly here for the unit tests
			return self[key]
		else:
			raise KeyError(f"Invalid key type for pop: {type(key).__name__}")

	def __iter__(self) -> Iterator[str]:
		raise NotImplementedError("Iteration over NSUserDefaults keys not directly implemented in this proxy.")

	def __len__(self) -> int:
		raise NotImplementedError("Length of NSUserDefaults not directly implemented in this proxy.")


	def __str__(self) -> str:
		return "<Userdefaults>"

	def __repr__(self) -> str:
		return NSUserDefaults.standardUserDefaults().description()


GSApplication.defaults = property(lambda self: DefaultsProxy())
add_type(GSApplication, "defaults", DefaultsProxy)


def printtraceback() -> None:
	code: List[str] = []
	for threadId, stack in sys._current_frames().items():
		# code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""), threadId))
		for filename, lineno, name, line in traceback.extract_stack(stack):
			code.append('File: "%s", line %d, in %s' % (filename, lineno, name))
			if line:
				code.append("  %s" % (line.strip()))
	if len(code) > 1:
		del (code[-1])
	if len(code) > 1:
		del (code[-1])
	print("\n".join(code))


def __GSApp_registerDefault__(self: GSApplication, key: str, value: Any) -> None:
	if key is not None and value is not None and len(key) > 2:
		NSUserDefaults.standardUserDefaults().registerDefaults_(cast(NSDictionary, objcObject({key: value})))
	else:
		# This should perhaps raise ValueError for invalid value, or TypeError for bad key type
		raise KeyError("Invalid key or value for registerDefault")


GSApplication.registerDefault = python_method(__GSApp_registerDefault__)  # type: ignore


def __GSApp_registerDefaults__(self: GSApplication, defaults: Dict[str, Any]) -> None:
	if defaults is not None:  # Should check isinstance(defaults, dict)
		NSUserDefaults.standardUserDefaults().registerDefaults_(cast(NSDictionary, objcObject(defaults)))
	else:
		raise ValueError("Defaults dictionary cannot be None")

GSApplication.registerDefaults = python_method(__GSApp_registerDefaults__)  # type: ignore
'''
	.. attribute:: defaults

		A dict like object for storing preferences. You can get and set key-value pairs.

		Please be careful with your keys. Use a prefix that uses the reverse domain name. e.g. :samp:`com_MyName_foo_bar`.

		:type: dict

		.. code-block:: python
			# Check for whether or not a preference exists
			if "com_MyName_foo_bar" in Glyphs.defaults:
			    # do stuff

			# Get and set values
			value = Glyphs.defaults["com_MyName_foo_bar"]
			Glyphs.defaults["com_MyName_foo_bar"] = newValue

			# Remove value
			# This will restore the default value
			del Glyphs.defaults["com_MyName_foo_bar"]
'''

'''
	.. function:: registerDefault(key, value)
		give it a key value pair to set a default value in the user defaults

		.. code-block:: python
			Glyphs.registerDefault("com_MyName_foo_bar", 12)

'''

'''
	.. function:: registerDefaults(dictionary)
		give it a doct with key value pairs to set default values in the user defaults

		.. code-block:: python
			values = {
				"com_MyName_foo": 12,
				"com_MyName_bar": "foo",
			}
			Glyphs.registerDefaults(values)

'''


class BoolDefaultsProxy(DefaultsProxy):
	def __getitem__(self, key: str) -> bool:  # NSUserDefaults.boolForKey_ returns a Python bool
		if not isString(key):
			raise TypeError(f"defaults key must be str, not {type(key).__name__}")
		return NSUserDefaults.standardUserDefaults().boolForKey_(objcObject(key))

	def __setitem__(self, key: str, value: bool | None) -> None:
		if not isString(key):
			raise TypeError(f"defaults key must be str, not {type(key).__name__}")
		if value is None:  # Remove the key
			NSUserDefaults.standardUserDefaults().removeObjectForKey_(objcObject(key))
		elif isinstance(value, bool):
			NSUserDefaults.standardUserDefaults().setBool_forKey_(value, objcObject(key))
		else:
			raise TypeError(f"boolDefaults only accepts values of type bool or None, not {type(value).__name__}")

	def get(self, key: str, default: bool | None = None) -> bool | None:  # type: ignore
		if not isString(key):
			raise TypeError("defaults key must be str, not %s" % type(key).__name__)
		value: NSNumber = cast(NSNumber, NSUserDefaults.standardUserDefaults().objectForKey_(objcObject(key)))
		if not value:
			return default
		return value.boolValue()


GSApplication.boolDefaults = property(lambda self: BoolDefaultsProxy())  # type: ignore
add_type(GSApplication, "boolDefaults", BoolDefaultsProxy)  # Or Dict[str, bool] if viewed as a dict
'''
	.. attribute:: boolDefaults
		Access to default settings cast to a bool.

		:type: bool

		.. code-block:: python
			if Glyphs.boolDefaults["com_MyName_foo_bar"]:
			    print('"com_MyName_foo_bar" is set')
'''


class ColorDefaultsProxy(DefaultsProxy):
	def __getitem__(self, key: str) -> NSColor | None:  # colorForKey can return nil
		if not isString(key):
			raise TypeError(f"defaults key must be str, not {type(key).__name__}")
		color_val: NSColor | None = NSUserDefaults.standardUserDefaults().colorForKey_(objcObject(key))
		if color_val is None:
			raise KeyError(key)  # Or return None if that's preferred for missing keys
		return color_val


	def __setitem__(self, key: str, value: NSColor | str | None) -> None:
		if not isString(key):
			raise TypeError(f"defaults key must be str, not {type(key).__name__}")
		if value is not None:
			color_to_set: NSColor | None = None
			if isString(value):  # value is str
				color_to_set = NSColor.colorWithString_(cast(str, value))
				if color_to_set is None:
					raise ValueError(f"Invalid color string: {value}")
			elif isinstance(value, NSColor):
				color_to_set = value
			else:
				raise TypeError(f"color must be string or NSColor type, not {type(value).__name__}")

			if color_to_set is not None:
				NSUserDefaults.standardUserDefaults().setColor_forKey_(color_to_set, objcObject(key))
		else:  # value is None
			NSUserDefaults.standardUserDefaults().removeObjectForKey_(objcObject(key))

GSApplication.colorDefaults = property(lambda self: ColorDefaultsProxy())  # type: ignore
add_type(GSApplication, "colorDefaults", ColorDefaultsProxy)
'''
	.. attribute:: colorDefaults
		Access to default settings cast to a color.

		:type: NSColor

		.. code-block:: python
			color = Glyphs.colorDefaults["GSColorCanvas"]
			color.set()
			NSBezierPath.fillRect_(rect)
'''


class IntDefaultsProxy(DefaultsProxy):
	def __getitem__(self, key: str) -> int:  # integerForKey_ returnsNSInteger (Python int)
		if not isString(key):
			raise TypeError(f"defaults key must be str, not {type(key).__name__}")
		return NSUserDefaults.standardUserDefaults().integerForKey_(objcObject(key))

	def __setitem__(self, key: str, value: int | float | None) -> None:
		if not isString(key):
			raise TypeError(f"defaults key must be str, not {type(key).__name__}")
		if value is None:
			NSUserDefaults.standardUserDefaults().removeObjectForKey_(objcObject(key))
		elif isinstance(value, (int, float)):  # NSUserDefaults.setInteger takes NSInteger
			NSUserDefaults.standardUserDefaults().setInteger_forKey_(int(value), objcObject(key))
		else:
			raise TypeError(f"intDefaults only accepts values of type int, float or None, not {type(value).__name__}")

	def get(self, key: str, default: Any | None = None) -> int | None:  # type: ignore
		if not isString(key):
			raise TypeError(f"defaults key must be str, not {type(key).__name__}")
		obj: Any = NSUserDefaults.standardUserDefaults().objectForKey_(objcObject(key))
		if obj is None:  # Key not present
			return default  # type: ignore
		# If key is present, integerForKey_ will give its integer value, or 0 if not convertible.
		return NSUserDefaults.standardUserDefaults().integerForKey_(objcObject(key))


GSApplication.intDefaults = property(lambda self: IntDefaultsProxy())  # type: ignore
add_type(GSApplication, "intDefaults", IntDefaultsProxy)
'''
	.. attribute:: intDefaults
		Access to default settings cast to a int.

		:type: int

		.. code-block:: python
			number = Glyphs.intDefaults["GSHandleSize"]
'''


class FloatDefaultsProxy(DefaultsProxy):
	def __getitem__(self, key: str) -> float:  # doubleForKey_ returns float
		if not isString(key):
			raise TypeError(f"defaults key must be str, not {type(key).__name__}")
		return NSUserDefaults.standardUserDefaults().doubleForKey_(objcObject(key))

	def __setitem__(self, key: str, value: int | float | None) -> None:
		if not isString(key):
			raise TypeError(f"defaults key must be str, not {type(key).__name__}")
		if value is None:
			NSUserDefaults.standardUserDefaults().removeObjectForKey_(objcObject(key))
		elif isinstance(value, (int, float)):
			NSUserDefaults.standardUserDefaults().setDouble_forKey_(float(value), objcObject(key))  # setFloat_ takes float
		else:
			raise TypeError(f"floatDefaults only accepts values of type float, int or None, not {type(value).__name__}")

	def get(self, key: str, default: Any | None = None) -> float | None:  # type: ignore
		if not isString(key):
			raise TypeError(f"defaults key must be str, not {type(key).__name__}")
		obj: Any = NSUserDefaults.standardUserDefaults().objectForKey_(objcObject(key))
		if obj is None:
			return default  # type: ignore
		return NSUserDefaults.standardUserDefaults().doubleForKey_(objcObject(key))


GSApplication.floatDefaults = property(lambda self: FloatDefaultsProxy())  # type: ignore
add_type(GSApplication, "floatDefaults", FloatDefaultsProxy)
'''
	.. attribute:: floatDefaults
		Access to default settings cast to a float.

		:type: float

		.. code-block:: python
			scaleX = Glyphs.floatDefaults["GSTransformScaleX"]
'''


GSApplication.scriptAbbreviations = property(lambda self: GSGlyphsInfo.script2Tag())  # type: ignore
add_type(GSApplication, "scriptAbbreviations", Dict[str, str])
'''
	.. attribute:: scriptAbbreviations
		A dictionary with script name to tag mapping, e.g., 'arabic': 'arab' or 'devanagari': 'dev2'

		:type: dict

		.. code-block:: python
			scriptTag = Glyphs.scriptAbbreviations["devanagari"]
			print(scriptTag) -> "dev2"
'''

GSApplication.scriptSuffixes = property(lambda self: GSGlyphsInfo.scriptSuffixes())  # type: ignore
add_type(GSApplication, "scriptSuffixes", Dict[str, str])
'''
	.. attribute:: scriptSuffixes
		A dictionary with glyphs name suffixes for scripts and their respective script names, e.g., 'cy': 'cyrillic'

		:type: dict
'''

GSApplication.languageScripts = property(lambda self: GSGlyphsInfo.languageScripts())  # type: ignore
add_type(GSApplication, "languageScripts", Dict[str, str])
'''
	.. attribute:: languageScripts
		A dictionary with language tag to script tag mapping, e.g., 'ENG': 'latn'

		:type: dict
'''


GSApplication.languageData = property(lambda self: GSGlyphsInfo.languageData())  # type: ignore
add_type(GSApplication, "languageData", List[Dict[str, Any]])
'''
	.. attribute:: languageData
		A list of dictionaries with more detailed language informations.

		:type: list
'''


GSApplication.unicodeRanges = property(lambda self: GSGlyphsInfo.unicodeRanges())  # type: ignore
add_type(GSApplication, "unicodeRanges", List[str])
'''
	.. attribute:: unicodeRanges
		Names of unicode ranges.

		:type: list
'''


def __GSApp_setUserDefaults__(self: GSApplication, key: str, value: Any) -> None:
	self.defaults[key] = value


def NSStr(string: str | None) -> NSString | None:  # Allow None input
	if string:
		return NSString.stringWithString_(string)
	else:
		return None


GSApplication.editViewWidth = property(
	lambda self: self.intDefaults["GSFontViewWidth"],
	lambda self, value: __GSApp_setUserDefaults__(self, "GSFontViewWidth", int(value))
)
add_type(GSApplication, "editViewWidth", int)
'''
	.. attribute:: editViewWidth
		Width of glyph Edit view. Corresponds to the "Width of editor" setting from the Preferences.

		:type: int
'''


GSApplication.handleSize = property(
	lambda self: self.intDefaults["GSHandleSize"],
	lambda self, value: __GSApp_setUserDefaults__(self, "GSHandleSize", int(value))
)
add_type(GSApplication, "handleSize", int)
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


GSApplication.versionString = NSBundle.mainBundle().objectForInfoDictionaryKey_("CFBundleShortVersionString")
add_type(GSApplication, "versionString", str)
'''
	.. attribute:: versionString
		String containing Glyph.app’s version number. May contain letters also, like ‘2.3b’. To check for a specific version, use :attr:`Glyphs.versionNumber <GSApplication.versionNumber>` below.

		:type: str
'''


def GSFloatVersion(versionString: str) -> float:
	m: re.Match | None = re.match(r"(\d+)\.(\d+)", versionString)
	if m is None:
		return 0.0  # Ensure float return
	mainVersionString: str = m.group(1)
	minorVersionString: str = m.group(2)
	return float(mainVersionString + '.' + minorVersionString)


add_type(GSApplication, "versionNumber", float)
'''
	.. attribute:: versionNumber
		Glyph.app’s version number. Use this to check for version in your code.

		:type: float
'''


add_type(GSApplication, "buildNumber", float)
'''
	.. attribute:: buildNumber
		Glyph.app’s build number.

		Especially if you’re using preview builds, this number may be more important to you than the version number. The build number increases with every released build and is the most significant evidence of new Glyphs versions, while the version number is set arbitrarily and stays the same until the next stable release.

		:type: float
'''


menuTagLookup: Dict[str, int] = {
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


class AppMenuProxy(Sequence[NSMenuItem]):
	"""Access the main menu."""

	def __len__(self) -> int:
		return NSApp.mainMenu().numberOfItems()

	def __iter__(self) -> Iterator[NSMenuItem]:
		return iter(self.values())

	@overload
	def __getitem__(self, key: int) -> NSMenuItem: ...
	@overload
	def __getitem__(self, key: str) -> NSMenuItem: ...

	def __getitem__(self, key: int | str) -> NSMenuItem:
		if isinstance(key, int):
			idx = _validate_idx(self, key)  # type: ignore # self is AppMenuProxy
			return NSApp.mainMenu().itemAtIndex_(idx)
		elif isString(key):  # Original uses isString
			Tag: int = menuTagLookup[key]
			menu_item: NSMenuItem | None = NSApp.mainMenu().itemWithTag_(Tag)
			if menu_item is None:
				raise KeyError(f"No menu item with tag for key: {key}")
			return menu_item
		raise TypeError(f"Expected int or str, not {type(key).__name__}")

	def values(self) -> List[NSMenuItem]:
		return NSApp.mainMenu().itemArray()


GSApplication.menu = property(lambda self: AppMenuProxy())  # type: ignore
add_type(GSApplication, "menu", AppMenuProxy)
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


def __NSURL__new__(typ: Type[NSURL], *args: str, **kwargs: Any) -> NSURL:
	if len(args) > 0 and args[0] is not None:  # Assuming first arg is path if present
		return typ.fileURLWithPath_(args[0])
	return typ.new()


NSURL.__new__ = staticmethod(__NSURL__new__)  # type: ignore


'''
	**Functions**
'''


def __GSApp_OpenFont__(self: GSApplication, path: str, showInterface: bool = True) -> GSFont | None:
	URL: NSURL = NSURL.fileURLWithPath_(path)  # type: ignore # NSURL() call through __new__
	doc_tuple = self.openDocumentWithContentsOfURL_display_(URL, showInterface)  # type: ignore
	# This method in NSDocumentController can return (doc, error) or just doc
	# Assuming it returns the document directly or nil if failed
	doc: GSDocument | None
	if isinstance(doc_tuple, tuple):  # As in (doc, wasAlreadyOpen) or (doc, error)
		doc = doc_tuple[0]
	else:
		doc = doc_tuple

	if doc is not None:
		return doc.font
	return None

GSApplication.open = python_method(__GSApp_OpenFont__)
# add_type(GSApplication, "open", Callable[[str, bool], GSFont | None]) already implied
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


def __GSApp_ShowMacroWindow__(self: GSApplication) -> None:
	Glyphs.delegate().showMacroWindow()

GSApplication.showMacroWindow = python_method(__GSApp_ShowMacroWindow__)
'''
	.. function:: showMacroWindow

		Opens the macro window

	.. function:: clearLog

		Deletes the content of the console in the macro window
'''


def __showGlyphInfoPanelWithSearchString__(self: GSApplication, String: str) -> None:
	Glyphs.delegate().showGlyphInfoPanelWithSearchString_(String)

GSApplication.showGlyphInfoPanelWithSearchString = python_method(__showGlyphInfoPanelWithSearchString__)
'''
	.. function:: showGlyphInfoPanelWithSearchString(String)

		Shows the Glyph Info window with a preset search string

		:param String: The search term
'''


def _glyphInfoForName(self: GSApplication, name: str | int, font: GSFont | None = None) -> GSGlyphInfo | None:
	if isinstance(name, int):  # If int, treat as unicode codepoint
		return self.glyphInfoForUnicode(name, font=font)  # type: ignore

	info: GSGlyphInfo | None
	if font is not None:
		info = font.glyphsInfo().glyphInfoForName_(name)
	else:
		info = GSGlyphsInfo.sharedManager().glyphInfoForName_(name)
	return info

GSApplication.glyphInfoForName = python_method(_glyphInfoForName)  # type: ignore
'''
	.. function:: glyphInfoForName(name, [font=None])

		Generates :class:`GSGlyphInfo` object for a given glyph name.

		:param name: Glyph name
		:param font: if you add a font, and the font has a local glyph info, it will be used instead of the global info data.
		:return: :class:`GSGlyphInfo`
'''


def _glyphInfoForUnicode(self: GSApplication, string_or_int: str | int, font: GSFont | None = None) -> GSGlyphInfo | None:
	unicode_str: str
	if isinstance(string_or_int, int):
		unicode_str = f"{string_or_int:04X}"
	else:
		unicode_str = string_or_int

	info: GSGlyphInfo | None
	if font is not None:
		info = font.glyphsInfo().glyphInfoForUnicode_(unicode_str)
	else:
		info = GSGlyphsInfo.sharedManager().glyphInfoForUnicode_(unicode_str)
	return info

GSApplication.glyphInfoForUnicode = python_method(_glyphInfoForUnicode)  # type: ignore
'''
	.. function:: glyphInfoForUnicode(Unicode, [font=None])

		Generates :class:`GSGlyphInfo` object for a given hex unicode.

		:param Unicode: Hex unicode
		:param font: if you add a font, and the font has a local glyph info, it will be used instead of the global info data.
		:return: :class:`GSGlyphInfo`
'''


def __GSApp_niceGlyphName__(self: GSApplication, name: str, font: GSFont | None = None) -> str | None:
	nice_name: str | None
	if font is not None:
		nice_name = font.glyphsInfo().niceGlyphNameForName_(name)
	else:
		nice_name = GSGlyphsInfo.sharedManager().niceGlyphNameForName_(name)
	return nice_name

GSApplication.niceGlyphName = python_method(__GSApp_niceGlyphName__)  # type: ignore
'''
	.. function:: niceGlyphName(name, [font=None])

		Converts glyph name to nice, human-readable glyph name (e.g. afii10017 or uni0410 to A-cy)

		:param name: glyph name
		:param font: if you add a font, and the font has a local glyph info, it will be used instead of the global info data.
		:return: str
'''


def __GSApp_productionGlyphName__(self: GSApplication, name: str, font: GSFont | None = None) -> str | None:
	prod_name: str | None
	if font is not None:
		prod_name = font.glyphsInfo().productionGlyphNameForName_(name)
	else:
		prod_name = GSGlyphsInfo.sharedManager().productionGlyphNameForName_(name)
	return prod_name

GSApplication.productionGlyphName = python_method(__GSApp_productionGlyphName__)  # type: ignore
'''
	.. function:: productionGlyphName(name, [font=None])

		Converts glyph name to production glyph name (e.g. afii10017 or A-cy to uni0410)

		:param name: glyph name
		:param font: if you add a font, and the font has a local glyph info, it will be used instead of the global info data.
		:return: str
'''


def __GSApp_ligatureComponents__(self: GSApplication, name: str, font: GSFont | None = None) -> List[str] | None:
	glyph_info_manager: GSGlyphsInfo
	if font is not None:
		glyph_info_manager = font.glyphsInfo()
	else:
		glyph_info_manager = GSGlyphsInfo.sharedManager()

	info: GSGlyphInfo | None = glyph_info_manager.glyphInfoForName_(name)
	if info:
		componentInfos: NSArray | None = info.components
		if componentInfos and componentInfos.count() > 0:
			# valueForKey_ returns NSArray of names here
			return list(componentInfos.valueForKey_("name"))  # type: ignore
	return None

GSApplication.ligatureComponents = python_method(__GSApp_ligatureComponents__)
'''
	.. function:: ligatureComponents(name, [font=None])

		If defined as a ligature in the glyph database, this function returns a list of glyph names that this ligature could be composed of.

		:param name: glyph name
		:param font: if you add a font, and the font has a local glyph info, it will be used instead of the global info data.
		:rtype: list

		.. code-block:: python
			print(Glyphs.ligatureComponents('allah-ar'))

			>> (
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
##########################################################################################################

DrawLayerCallbacks = (
	DRAWFOREGROUND, DRAWBACKGROUND, DRAWINACTIVE
)
Observers = (
	DOCUMENTOPENED, DOCUMENTACTIVATED, DOCUMENTWASSAVED, DOCUMENTEXPORTED, DOCUMENTCLOSED, DOCUMENTWILLCLOSE, DOCUMENTDIDCLOSE, TABDIDOPEN,
	TABWILLCLOSE, UPDATEINTERFACE, UPDATEEDITVIEWFRAME, MOUSEMOVED, MOUSEDRAGGED, MOUSEDOWN, MOUSEUP
)

callbackOperationTargets: dict[str, dict] = {}


class callbackHelperClass(NSObject):

	def __init__(self, func, operation):
		self.func = func
		self.operation = operation

	def __new__(cls, *args, **kwargs):
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
		desc = objc.super(callbackHelperClass, self).description()
		return "%s %s" % (desc, str(self.func))


def __GSApp_addCallback__(self, target: Any | None = None, operation: str | None = None, callbackType: str | None = None, callee: Any | None = None, selector: Any | None = None):
	if callbackType is None and operation is not None:
		__GSApp_addCallback__Old__(self, target, operation)
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


def __GSApp_addCallback__Old__(self, target: Any, operation: str):
	# Remove possible old function by the same name
	targetName = str(target)
	try:
		callbackTargets: dict
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
			if isinstance(target, objc.Class):  # type: ignore
				GSCallbackHandler.addCallback_forOperation_(target, operation)
			else:
				raise TypeError("Target must be a (objc) class, not %s" % type(target).__name__)
		# Other observers
		elif operation in Observers:
			# Add class to callbackTargets dict by the function name
			callbackTargets[targetName] = callbackHelperClass(target, operation)
			selector = objc.selector(callbackTargets[targetName].callback_, signature=b"v@:@")  # type: ignore
			NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(callbackTargets[targetName], selector, operation, objc.nil)
	except:
		NSLog(traceback.format_exc())


GSApplication.addCallback = python_method(__GSApp_addCallback__)
'''
	.. function:: addCallback(function, hook)

		Add a user-defined function to the glyph window’s drawing operations, in the foreground and background for the active glyph as well as in the inactive glyphs.

		The function names are used to add/remove the functions to the hooks, so make sure to use unique function names.

		Your function needs to accept two values: `layer` which will contain the respective :class:`GSLayer` object of the layer we’re dealing with and `info` which is a dictionary and contains the value `Scale` (for the moment).

		For the defined keys see `Callback Keys`_

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


def __GSApp_do__removeCallback__(self, target, operation):

	targetName = str(target)
	callbackTargets: dict
	try:
		callbackTargets = callbackOperationTargets[operation]
	except:
		return
	if targetName in callbackTargets:

		# DrawLayerCallbacks
		if callbackTargets[targetName].operation in DrawLayerCallbacks:
			GSCallbackHandler.removeCallback_(callbackTargets[targetName])
			del (callbackTargets[targetName])
			# Redraw immediately
			self.redraw()
		# Other observers
		elif callbackTargets[targetName].operation in Observers:
			NSNotificationCenter.defaultCenter().removeObserver_(callbackTargets[targetName])
			del (callbackTargets[targetName])


def __GSApp_removeCallback__(self, target=None, operation=None, callbackType=None, callee=None):
	if callee is None:
		if operation is not None:
			__GSApp_do__removeCallback__(self, target, operation)
		else:
			for operation in callbackOperationTargets.keys():
				__GSApp_do__removeCallback__(self, target, operation)
		return

	if callbackType is None:
		raise ValueError("You need to supply the callbackType to remove it")

	if callbackType in DrawLayerCallbacks or callbackType == CONTEXTMENUCALLBACK:

		GSCallbackHandler.removeCallback_forOperation_(callee, callbackType)

		# Redraw immediately
		self.redraw()

	elif callbackType in Observers:
		NSNotificationCenter.defaultCenter().removeObserver_(callee)


GSApplication.removeCallback = python_method(__GSApp_removeCallback__)
'''
	.. function:: removeCallback(function)

		Remove the function you’ve previously added.

		.. code-block:: python
			# remove your function from the hook
			Glyphs.removeCallback(drawGlyphIntoBackground)
'''

##########################################################################################################
#
#
#           // end of Callback section
#
#
##########################################################################################################


def __GSApp_redraw__(self):
	NSNotificationCenter.defaultCenter().postNotificationName_object_("GSRedrawEditView", None)


GSApplication.redraw = python_method(__GSApp_redraw__)
'''
	.. function:: redraw()

		Redraws all Edit views and Preview views.
'''


GSUserNotification.title = property(
	lambda self: self.pyobjc_instanceMethods.title(),
	lambda self, value: self.setTitle_(value)
)
add_type(GSUserNotification, "title", str)
'''
	.. attribute:: title

		the title of the notification

		:type: str
'''


GSUserNotification.subtitle = property(
	lambda self: self.pyobjc_instanceMethods.subtitle(),
	lambda self, value: self.setSubtitle_(value)
)
add_type(GSUserNotification, "subtitle", str)
'''
	.. attribute:: subtitle

		the subtitle of the notification

		:type: str
'''


GSUserNotification.message = property(
	lambda self: self.informativeText(),
	lambda self, value: self.setInformativeText_(value)
)
add_type(GSUserNotification, "message", str)
'''
	.. attribute:: message

		the message of the notification

		:type: str
'''
GSUserNotification.userInfo = property(
	lambda self: self.pyobjc_instanceMethods.userInfo(),
	lambda self, value: self.setUserInfo_(value)
)
add_type(GSUserNotification, "userInfo", dict)
'''
	.. attribute:: userInfo
		the userInfo of the notification

		:type: dict
'''
'''
	.. function:: deliver()

		Shows the notification
'''


GSUserNotification.actionButtonTitle = property(
	lambda self: self.pyobjc_instanceMethods.actionButtonTitle(),
	lambda self, value: self.setActionButtonTitle_(value)
)
add_type(GSUserNotification, "actionButtonTitle", str)
'''
	.. attribute:: actionButtonTitle
		the actionButtonTitle of the notification

		:type: str
'''


def __GSApp_showNotification__(self: GSApplication, title: str, message: str) -> None:
	notification: GSUserNotification = GSUserNotification.new()  # type: ignore
	notification.setTitle_(title)
	notification.setInformativeText_(message)
	notification.deliver()


GSApplication.showNotification = python_method(__GSApp_showNotification__)
'''
	.. function:: showNotification(title, message)

		Shows the user a notification in Mac’s Notification Center.

		.. code-block:: python
			Glyphs.showNotification('Export fonts', 'The export of the fonts was successful.')
'''

def __GSApp_localize__(self: GSApplication, localization: str | Dict[str, str]) -> str:
	if isString(localization):  # localization is str
		return cast(str, localization)
	elif isinstance(localization, dict):  # localization is Dict[str, str]
		# Ensure self.defaults["AppleLanguages"] returns a list of strings
		apple_languages: List[str] = self.defaults.get("AppleLanguages", [])  # type: ignore
		for language in apple_languages:
			if language in localization:
				return localization[language]
			# Simplified BCP 47 primary language check
			primary_language = language.split("-")[0]
			if primary_language in localization:
				return localization[primary_language]

		# Fallback to 'en' or first item
		english_translation: str | None = localization.get("en")
		if english_translation is not None:
			return english_translation
		if localization:  # If dict is not empty
			return list(localization.values())[0]
		return ""  # Should not happen if localization is dict and not empty
	return str(localization)  # Fallback if not str or dict (though types say it is)

GSApplication.localize = python_method(__GSApp_localize__)
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
			# and Glyphs.app UI is set to use localization (change in app settings),
			# it will print:
			>> Hallöle Welt
'''


def __GSApplication_activateReporter__(self: GSApplication, reporter: NSObject | str) -> None:
	GSCallbackHandler.activateReporter_(reporter)


GSApplication.activateReporter = python_method(__GSApplication_activateReporter__)  # type: ignore
'''
	.. function:: activateReporter(reporter)

		Activate a reporter plug-in by its object (see Glyphs.reporters) or class name.

		.. code-block:: python
			Glyphs.activateReporter('GlyphsMasterCompatibility')
'''


def __GSApplication_deactivateReporter__(self: GSApplication, reporter: NSObject | str) -> None:
	GSCallbackHandler.deactivateReporter_(reporter)


GSApplication.deactivateReporter = python_method(__GSApplication_deactivateReporter__)  # type: ignore
'''
	.. function:: deactivateReporter(reporter)

		Deactivate a reporter plug-in by its object (see Glyphs.reporters) or class name.

		.. code-block:: python
			Glyphs.deactivateReporter('GlyphsMasterCompatibility')
'''

GSDocument.__new__ = staticmethod(__GSObject__new__)
GSDocument.__new__.__name__ = "__new__"
GSProjectDocument.__new__ = staticmethod(__GSObject__new__)
GSProjectDocument.__new__.__name__ = "__new__"

GSElement.x = property(
	lambda self: self.pyobjc_instanceMethods.position().x,
	lambda self, value: self.setPosition_(NSMakePoint(validateNumber(value), self.y)))

GSElement.y = property(
	lambda self: self.pyobjc_instanceMethods.position().y,
	lambda self, value: self.setPosition_(NSMakePoint(self.x, validateNumber(value)))
)

GSNode.x = property(
	lambda self: self.pyobjc_instanceMethods.position().x,
	lambda self, value: self.setPosition_(NSMakePoint(validateNumber(value), self.y)))

GSNode.y = property(
	lambda self: self.pyobjc_instanceMethods.position().y,
	lambda self, value: self.setPosition_(NSMakePoint(self.x, validateNumber(value)))
)

GSElement.layer = property(lambda self: self.pyobjc_instanceMethods.layer())

GSElement.glyph = property(lambda self: self.pyobjc_instanceMethods.glyph())

GSElement.__new__ = staticmethod(__GSObject__new__)
GSElement.__new__.__name__ = "__new__"


def ____PROXIES____(): pass


class AppDocumentProxy(ListProxy[GSDocument]):
	"""The list of documents."""

	def __getitem__(self, idx) -> GSDocument | None:
		idx = _validate_idx(cast(Sequence, self), idx)
		return self.values().__getitem__(idx)

	def append(self, doc: GSDocument):
		NSDocumentController.sharedDocumentController().addDocument_(doc)
		doc.makeWindowControllers()
		doc.showWindows()

	def values(self) -> list[GSDocument]:
		return self._owner.fontDocuments()


class AppFontProxy(Sequence[GSFont], ABC):
	"""The list of fonts."""

	def __init__(self, owner: OwnerType) -> None:
		self._owner = owner

	def __len__(self) -> int:
		return self._owner.fontDocuments().count()

	def __getitem__(self, idx) -> GSFont | None:
		idx = _validate_idx(cast(Sequence, self), idx)
		return self.values().__getitem__(idx)

	def values(self) -> List[GSFont]:
		fonts = []
		for doc in self._owner.fontDocuments():
			fonts.append(doc.font)
		return fonts

	def append(self, font: GSFont):
		doc = Glyphs.documentController().openUntitledDocumentAndDisplay_error_(True, None)[0]
		doc.setFont_(font)


'''
:mod:`GSDocument`
===============================================================================

The document class

.. class:: GSDocument()

	Properties

		* :attr:`font`
		* :attr:`filePath`

	**Properties**
'''

GSDocument.font = property(
	lambda self: self.pyobjc_instanceMethods.font(),
	lambda self, value: self.setFont_(value)
)
add_type(GSDocument, "font", GSFont)
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
add_type(GSDocument, "filePath", str)
'''
	.. attribute:: filePath
		The last save location

		:type: str
'''
add_type(GSDocument, "filePath", str | None)



class FontGlyphsProxy(OrderedDictProxy[GSGlyph]):
	"""The list of glyphs. You can access it with the idx or the glyph name.
	Usage:
		Font.glyphs[idx]
		Font.glyphs[name]
		for glyph in Font.glyphs:
		    ...
	"""

	def getKeyOf(self, value: GSGlyph) -> str:
		return value.name

	def getByIndex(self, idx: int) -> GSGlyph:
		return self._owner.glyphAtIndex_(idx)

	def getByKey(self, key: str) -> GSGlyph:
		# by glyph name
		glyph: GSGlyph = self._owner.glyphForName_(key)
		if glyph:
			return glyph
		# by string representation as 'ä'
		if len(key) == 1:
			glyph = self._owner.glyphForCharacter_(ord(key))
			if glyph:
				return glyph
		# by unicode
		return self._owner.glyphForUnicode_(key.upper())

	def setByIndex(self, idx: int, glyph: GSGlyph) -> None:
		if not isinstance(glyph, GSGlyph):
			raise TypeError("Cannot add %s, not a Glyph" % glyph)
		self._owner.removeGlyph_(self._owner.glyphAtIndex_(idx))
		self._owner.addGlyph_(glyph)

	def setByKey(self, key: str, glyph: GSGlyph) -> None:
		if not isinstance(glyph, GSGlyph):
			raise TypeError("Cannot add %s, not a Glyph" % glyph)
		self._owner.removeGlyph_(self._owner.glyphForName_(key))
		if glyph.name != key:
			glyph.name = key
		self._owner.addGlyph_(glyph)

	def insertAtIndex(self, idx: int, value: GSGlyph) -> None:
		self._owner.addGlyph(value)

	def removeByIndex(self, idx: int) -> None:
		self._owner.removeGlyph_(self._owner.glyphAtIndex_(idx))

	def removeByKey(self, key: str) -> None:
		self._owner.removeGlyph_(self._owner.glyphForName_(key))

	def __contains__(self, item):
		if isString(item):
			return self._owner.glyphForName_(item) is not None
		return self._owner.indexOfGlyph_(item) < NSNotFound  # indexOfGlyph_ returns NSNotFound which is some very big number

	def keys(self):
		return self._owner.pyobjc_instanceMethods.glyphs().valueForKey_("name")

	def values(self):
		return self._owner.pyobjc_instanceMethods.glyphs()

	def items(self):
		for value in self._owner.pyobjc_instanceMethods.glyphs():
			key = value.name
			yield (key, value)

	def append(self, glyph):
		if not isinstance(glyph, GSGlyph):
			raise TypeError("Cannot add %s, not a Glyph" % glyph)
		if glyph.name not in self:
			self._owner.addGlyph_(glyph)
		else:
			raise NameError('There is a glyph with the name \"%s\" already in the font.' % glyph.name)

	def extend(self, objects):
		for glyph in objects:
			if not isinstance(glyph, GSGlyph):
				raise TypeError("Cannot add %s, not a Glyph" % glyph)
			if glyph.name in self:
				raise NameError('There is a glyph with the name \"%s\" already in the font.' % glyph.name)
		self._owner.addGlyphsFromArray_(list(objects))

	def __len__(self) -> int:
		return self._owner.count()

	def setterMethod(self):
		return self._owner.setGlyphs_


class FontFontMasterProxy(OrderedDictProxy[GSFontMaster]):

	def getKeyOf(self, value: GSFontMaster) -> str:
		return value.id

	def getByIndex(self, idx: int):
		return self._owner.fontMasterAtIndex_(idx)

	def getByKey(self, key: str) -> Any:
		return self._owner.fontMasterForId_(key)

	def setByIndex(self, idx: int, fontMaster: GSFontMaster):
		if not isinstance(fontMaster, GSFontMaster):
			raise TypeError("Cannot add %s, not a FontMaster" % fontMaster)
		self._owner.replaceFontMasterAtIndex_withFontMaster_(idx, fontMaster)

	def setByKey(self, key: str, fontMaster: GSFontMaster) -> None:
		oldFontMaster = self._owner.fontMasterForId_(key)
		self._owner.removeFontMaster_(oldFontMaster)
		return self._owner.addFontMaster_(fontMaster)

	def removeByIndex(self, idx: int) -> None:
		removeFontMaster = self._owner.objectInFontMastersAtIndex_(idx)
		if removeFontMaster:
			return self._owner.removeFontMasterAndContent_(removeFontMaster)

	def removeByKey(self, key: str) -> None:
		removeFontMaster = self._owner.fontMasterForId_(key)
		if removeFontMaster:
			return self._owner.removeFontMasterAndContent_(removeFontMaster)

	def __len__(self) -> int:
		return self._owner.countOfFontMasters()

	def values(self):
		return self._owner.fontMasters()

	def setterMethod(self):
		return self._owner.setFontMasters_

	def append(self, fontMaster):
		if not isinstance(fontMaster, GSFontMaster):
			raise TypeError("Cannot add %s, not a FontMaster" % fontMaster)
		self._owner.addFontMaster_(fontMaster)

	def remove(self, fontMaster):
		self._owner.removeFontMasterAndContent_(fontMaster)

	def insertAtIndex(self, idx: int, fontMaster: GSFontMaster) -> None:
		if not isinstance(fontMaster, GSFontMaster):
			raise TypeError("Cannot add %s, not a FontMaster" % fontMaster)
		self._owner.insertFontMaster_atIndex_(fontMaster, idx)


class FontInstancesProxy(ListProxy[GSInstance]):

	def getByIndex(self, idx: int) -> GSInstance:
		return self._owner.objectInInstancesAtIndex_(idx)

	def setByIndex(self, idx: int, instance: GSInstance):
		self._owner.replaceObjectInInstancesAtIndex_withObject_(idx, instance)

	def removeByIndex(self, idx: int):
		return self._owner.removeObjectFromInstancesAtIndex_(idx)

	def append(self, instance):
		self._owner.addInstance_(instance)

	def extend(self, instances):
		for instance in instances:
			self._owner.addInstance_(instance)

	def remove(self, instance):
		self._owner.removeInstance_(instance)

	def insertAtIndex(self, idx: int, instance: GSInstance) -> None:
		self._owner.insertObject_inInstancesAtIndex_(instance, idx)

	def __len__(self) -> int:
		return self._owner.countOfInstances()

	def values(self):
		return self._owner.pyobjc_instanceMethods.instances()

	def setterMethod(self):
		return self._owner.setInstances_


class FontAxesProxy(ListProxy[GSAxis]):

	def getByIndex(self, idx: int) -> GSAxis:
		return self._owner.objectInAxesAtIndex_(idx)

	def setByIndex(self, idx: int, value: GSAxis) -> None:
		self._owner.replaceObjectInAxesAtIndex_withObject_(idx, value)

	def removeByIndex(self, idx: int) -> None:
		self._owner.removeObjectFromAxesAtIndex_(idx)

	def append(self, axis):
		self._owner.addAxis_(axis)

	def extend(self, axes):
		for axis in axes:
			self._owner.addAxis_(axis)

	def insertAtIndex(self, idx: int, axis: GSAxis):
		self._owner.insertObject_inAxesAtIndex_(axis, idx)

	def __len__(self) -> int:
		return self._owner.countOfAxes()

	def values(self):
		return self._owner.pyobjc_instanceMethods.axes()

	def setterMethod(self):
		return self._owner.setAxes_


class InternalAxesProxy(OrderedDictProxy[float]):

	def getKeyOf(self, value: float) -> str:
		NotImplementedError()
		return ""

	def getByIndex(self, idx: int) -> float | None:
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return None
		axis = self._owner.font.axes[idx]
		if axis is None:
			return None
		return self._owner.axisInternalValueValueForId_(axis.axisId)

	def getByKey(self, key: str) -> float | None:
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return None
		return self._owner.axisInternalValueValueForId_(key)

	def setByIndex(self, idx: int, value: float) -> None:
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return
		axis = self._owner.font.axes[idx]
		self._owner.setAxisInternalValueValue_forId_(value, axis.axisId)

	def setByKey(self, key: str, value: float) -> None:
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return
		self._owner.setAxisInternalValueValue_forId_(value, key)

	def insertAtIndex(self, idx: int, value: float) -> None:
		raise TypeError("Can’t insert axis Values. Insert the Axis on the font")

	def removeByIndex(self, idx: int) -> None:
		raise TypeError("Can’t remove axis Values. Remove the Axis on the font")

	def removeByKey(self, key: str) -> None:
		raise TypeError("Can’t remove axis Values. Remove the Axis on the font")

	def values(self):
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return []
		if self._owner.font is None:
			return []
		values = []
		for axis in self._owner.font.axes:
			value = self._owner.axisInternalValueValueForId_(axis.axisId)
			values.append(value)
		return values

	def __len__(self) -> int:
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return 0
		if self._owner.font is None:
			return 0
		return self._owner.font.countOfAxes()

	def _setterMethod(self, values):
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return None
		idx = 0
		if self._owner.font is None:
			raise AttributeError("cannot set 'axesValues' if 'font' property is not set")
		axesValues = {}
		for axis in self._owner.font.axes:
			axisValue = GSMetricStore(values[idx])
			axesValues[axis.axisId] = axisValue
			idx += 1
		self._owner.setAxesValues_(axesValues)

	def setterMethod(self):
		return self._setterMethod


class ExternalAxesProxy(OrderedDictProxy[float]):

	def getKeyOf(self, value: float) -> str:
		NotImplementedError()
		return ""

	def getByIndex(self, idx: int) -> float | None:
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return None
		axis = self._owner.font.axes[idx]
		if axis is None:
			return None
		return self._owner.axisExternalValueValueForId_(axis.axisId)

	def getByKey(self, key: str) -> float | None:
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return None
		return self._owner.axisExternalValueValueForId_(key)

	def setByIndex(self, idx: int, value: float) -> None:
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return
		axis = self._owner.font.axes[idx]
		self._owner.setAxisExternalValueValue_forId_(value, axis.axisId)

	def setByKey(self, key: str, value: float) -> None:
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return
		self._owner.setAxisExternalValueValue_forId_(value, key)

	def insertAtIndex(self, idx: int, value: float) -> None:
		raise TypeError("Can’t insert axis Values. Insert the Axis on the font")

	def removeByIndex(self, idx: int) -> None:
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return None
		axis = self._owner.font.axes[idx]
		if axis is None:
			return
		metricsStore: GSMetricStore = self._owner.axisExternalValueForId_(axis.axisId)
		metricsStore.setOvershootValue_(None)

	def removeByKey(self, key: str) -> None:
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return
		metricsStore: GSMetricStore = self._owner.axisExternalValueForId_(key)
		metricsStore.setOvershootValue_(None)

	def values(self):
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return []
		if self._owner.font is None:
			return []
		values = []
		for axis in self._owner.font.axes:
			value = self._owner.axisExternalValueValueForId_(axis.axisId)
			values.append(value)
		return values

	def __len__(self) -> int:
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return 0
		if self._owner.font is None:
			return 0
		return self._owner.font.countOfAxes()

	def _setterMethod(self, values):
		if isinstance(self._owner, GSInstance) and self._owner.type == INSTANCETYPEVARIABLE:
			return
		idx = 0
		if self._owner.font is None:
			return
		for axis in self._owner.font.axes:
			self._owner.setAxisExternalValueValue_forId_(values[idx], axis.axisId)
			idx += 1

	def setterMethod(self):
		return self._setterMethod


class PropertiesProxy(OrderedDictProxy[GSInfoProperty]):

	def getKeyOf(self, value: GSInfoProperty) -> str:
		return value.name

	def getByIndex(self, idx: int) -> GSInfoProperty:
		return self._owner.objectInPropertiesAtIndex_(idx)

	def getByKey(self, key: str) -> GSInfoProperty:
		return self._owner.propertyForName_(key)

	def setByIndex(self, idx: int, value: Any):
		assert isinstance(value, GSInfoProperty)
		self._owner.replaceObjectInPropertiesAtIndex_withObject_(idx, value)

	def setByKey(self, key: str, value: GSInfoProperty):
		assert isinstance(value, GSInfoProperty)
		self._owner.setProperty_value_languageTag_(key, value, None)

	def removeByIndex(self, idx: int) -> None:
		self._owner.removeObjectFromPropertiesAtIndex_(idx)

	def removeByKey(self, key: str) -> None:
		oldValue = self._owner.removeObjectFromProperties_(key)
		self._owner.removeObjectFromProperties_(oldValue)

	def insertAtIndex(self, idx: int, value: GSInfoProperty) -> None:
		self._owner.insertObject_inPropertiesAtIndex_(value, idx)

	def getProperty(self, key, language="dflt"):
		self._owner.propertyForName_languageTag_(key, language)

	def setProperty(self, key, value, language="dflt"):
		self._owner.setProperty_value_languageTag_(key, value, language)

	def append(self, value):
		self._owner.addProperty_(value)

	def values(self):
		return self._owner.pyobjc_instanceMethods.properties()

	def _setterMethod(self, values):
		if not isinstance(values, (list, NSArray)):
			values = list(values)
		self._owner.setProperties_(values)

	def setterMethod(self):
		return self._setterMethod


class FontMetricsProxy(OrderedDictProxy[GSMetric]):

	def getKeyOf(self, value: GSMetric) -> str:
		return value.id

	def getByIndex(self, idx: int) -> Any:
		return self._owner.objectInMetricsAtIndex_(idx)

	def getByKey(self, key: str) -> GSMetric:
		metric: GSMetric = None
		metric = self._owner.metricForName_(key)
		if metric is None:
			metric = self._owner.metricForId_(key)
		if metric is None:
			raise KeyError("No metric for key %s" % key)
		return metric

	def insertAtIndex(self, idx: int, value: GSMetric) -> None:
		self._owner.insertObject_inMetricsAtIndex_(value, idx)

	def setByIndex(self, idx: int, value: GSMetric) -> None:
		self._owner.removeObjectFromMetricsAtIndex_(idx)
		self._owner.insertObject_inMetricsAtIndex_(value, idx)

	def setByKey(self, key: str, value: Any) -> None:
		raise TypeError("only accessible by integer index, not %s" % key)

	def removeByIndex(self, idx: int) -> None:
		self._owner.removeObjectFromMetricsAtIndex_(idx)

	def removeByKey(self, key: str) -> None:
		oldValue = self.getByKey(key)
		if oldValue:
			self._owner.removeObjectFromMetrics_(oldValue)

	def values(self):
		return self._owner.pyobjc_instanceMethods.metrics()

	def __len__(self) -> int:
		return self._owner.countOfMetrics()

	def append(self, value):
		if not isinstance(value, GSMetric):
			raise TypeError("only object of type GSMetric allowed, not %s" % type(value).__name__)
		self._owner.addStem_(value)

	def setterMethod(self):
		return self.setMetrics_  # type: ignore


class MasterMetricsProxy(OrderedDictProxy[GSMetricStore]):

	def getKeyOf(self, value: float) -> str:
		NotImplementedError()
		return ""

	def _metricForKey(self, key):
		if isinstance(key, int):
			if key < 0:
				key += self.__len__()
			metric = self._owner.font.objectInMetricsAtIndex_(key)
		elif isString(key):
			metric = self._owner.font.metricForName_(key)
			if metric is None:
				metric = self._owner.font.metricForId_(key)
		else:
			raise TypeError("list indices must be integers or strings, not %s" % type(key).__name__)
		return metric

	def getByIndex(self, idx: int) -> GSMetricStore:
		metric = self._metricForKey(idx)
		if metric is None:
			raise KeyError("No metric for %d" % idx)
		print("******", metric, type(metric))
		return self._owner.valueForMetric_(metric)

	def getByKey(self, key: str) -> GSMetricStore:
		return self._owner.valueForMetricId_(key)

	def setByIndex(self, idx: int, value: GSMetricStore) -> None:
		metric = self._metricForKey(idx)
		self._owner.setMetricValueValue_forId_(value, metric.id)

	def setByKey(self, key: str, value: GSMetricStore) -> None:
		self._owner.setMetricValueValue_forId_(value, key)

	def insertAtIndex(self, idx: int, value: GSMetricStore) -> None:
		raise TypeError("Can’t insert metric Values. Insert the Metric on the font")

	def removeByIndex(self, idx: int) -> None:
		raise TypeError("Can’t remove metric Values. Remove the Metric on the font")

	def removeByKey(self, key: str) -> None:
		raise TypeError("Can’t remove metric Values. Remove the Metric on the font")

	def values(self):
		return self._owner.pyobjc_instanceMethods.metrics()

	def __len__(self) -> int:
		if self._owner.font is None:
			return 0
		return self._owner.font.countOfMetrics()

	def _setterMethod(self, values):
		idx = 0
		if self._owner.font is None:
			return
		if self.__len__() != len(values):
			raise ValueError("Count of values doesn’t match metrics")
		for metric in self._owner.font.metrics:
			self._owner.setMetricValueValue_forId_(values[idx], metric.id)
			idx += 1

	def setterMethod(self):
		return self._setterMethod


class FontStemsProxy(OrderedDictProxy[GSMetric]):

	def getKeyOf(self, value: GSMetric) -> str:
		return value.id

	def getByIndex(self, idx: int) -> Any:
		return self._owner.objectInStemsAtIndex_(idx)

	def getByKey(self, key: str) -> GSMetric:
		stem: GSMetric = None
		stem = self._owner.stemForName_(key)
		if stem is None:
			stem = self._owner.stemForId_(key)
		if stem is None:
			raise KeyError("No stem for key %s" % key)
		return stem

	def insertAtIndex(self, idx: int, value: GSMetric) -> None:
		self._owner.insertObject_inStemsAtIndex_(value, idx)

	def setByIndex(self, idx: int, value: GSMetric) -> None:
		self._owner.removeObjectFromStemsAtIndex_(idx)
		self._owner.insertObject_inStemsAtIndex_(value, idx)

	def setByKey(self, key: str, value: Any) -> None:
		raise TypeError("only accessible by integer index, not %s" % key)

	def removeByIndex(self, idx: int) -> None:
		self._owner.removeObjectFromStemsAtIndex_(idx)

	def removeByKey(self, key: str) -> None:
		oldValue = self.getByKey(key)
		if oldValue:
			self._owner.removeObjectFromStems_(oldValue)

	def values(self):
		return self._owner.pyobjc_instanceMethods.stems()

	def __len__(self) -> int:
		return self._owner.countOfStems()

	def append(self, value):
		if not isinstance(value, GSMetric):
			raise TypeError("only object of type GSMetric allowed, not %s" % type(value).__name__)
		self._owner.addStem_(value)

	def setterMethod(self):
		return self.setStems_  # type: ignore


class MasterStemsProxy(OrderedDictProxy[float]):

	def getKeyOf(self, value: float) -> str:
		NotImplementedError()
		return ""

	def _stemForKey(self, key):
		if isinstance(key, int):
			if key < 0:
				key += self.__len__()
			stem = self._owner.font.objectInStemsAtIndex_(key)
		elif isString(key):
			stem = self._owner.font.stemForName_(key)
			if stem is None:
				stem = self._owner.font.stemForId_(key)
		else:
			raise TypeError("list indices must be integers or strings, not %s" % type(key).__name__)
		return stem

	def getByIndex(self, idx: int) -> float:
		stem = self._stemForKey(idx)
		if stem is None:
			raise KeyError("No stem for %d" % idx)
		return self._owner.valueValueForStemId_(stem.id)

	def getByKey(self, key: str) -> float:
		stemValue = self._owner.valueValueForStemId_(key)
		if stemValue is None:
			raise KeyError("No stem for %s" % key)
		return stemValue

	def setByIndex(self, idx: int, value: float) -> None:
		stem = self._stemForKey(idx)
		self._owner.setStemValueValue_forId_(value, stem.id)

	def setByKey(self, key: str, value: float) -> None:
		self._owner.setStemValueValue_forId_(value, key)

	def insertAtIndex(self, idx: int, value: float) -> None:
		raise TypeError("Can’t insert stem Values. Insert the Stem on the font")

	def removeByIndex(self, idx: int) -> None:
		raise TypeError("Can’t remove stem Values. Remove the Stem on the font")

	def removeByKey(self, key: str) -> None:
		raise TypeError("Can’t remove stem Values. Remove the Stem on the font")

	def values(self):
		return self._owner.stemValuesArray()

	def __len__(self) -> int:
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


class FontNumbersProxy(OrderedDictProxy[GSMetric]):

	def getKeyOf(self, value: GSMetric) -> str:
		return value.id

	def _numberForKey(self, key):
		number = None
		if isinstance(key, int):
			idx = _validate_idx(cast(Sequence, self), key)
			number = self._owner.objectInNumbersAtIndex_(idx)
		elif isString(key):
			number = self._owner.numberForName_(key)
			if number is None:
				number = self._owner.numberForId_(key)
		else:
			raise TypeError("keys must be integers or strings, not %s" % type(key).__name__)
		if number is None:
			raise KeyError("No number for key %s" % key)
		return number

	def getByIndex(self, idx: int) -> GSMetric:
		return self._owner.objectInNumbersAtIndex_(idx)

	def getByKey(self, key: str) -> GSMetric:
		number: GSMetric = self._owner.numberForName_(key)
		if number is None:
			number = self._owner.numberForId_(key)
		return number

	def setByIndex(self, idx: int, value: GSMetric) -> None:
		self._owner.insertObject_inNumbersAtIndex_(value, idx)

	def setByKey(self, key: str, value: GSMetric) -> None:
		raise TypeError("only accessible by integer index, not %s" % key)

	def removeByIndex(self, idx: int) -> None:
		self._owner.removeObjectFromNumbersAtIndex_(idx)

	def removeByKey(self, key: str) -> None:
		number = self.getByKey(key)
		self._owner.removeObjectFromNumbers_(number)

	def insertAtIndex(self, idx: int, value: GSMetric) -> None:
		self._owner.insertObject_inNumbersAtIndex_(value, idx)

	def values(self) -> List[GSMetric]:
		return self._owner.pyobjc_instanceMethods.numbers()

	def __len__(self) -> int:
		return self._owner.countOfNumbers()

	def append(self, value):
		if not isinstance(value, GSMetric):
			raise TypeError("only object of type GSMetric allowed, not %s" % type(value).__name__)
		self._owner.addNumber_(value)

	def setterMethod(self):
		return self.setNumbers_  # type: ignore


class MasterNumbersValuesProxy(OrderedDictProxy):

	def getKeyOf(self, value: float) -> str:
		NotImplementedError()
		return ""

	def _numForKey(self, key):
		if isinstance(key, int):
			if key < 0:
				key += self.__len__()
			num = self._owner.font.objectInNumbersAtIndex_(key)
		elif isString(key):
			num = self._owner.font.numberForName_(key)
			if num is None:
				num = self._owner.font.numberForId_(key)
		else:
			raise TypeError("list indices must be integers or strings, not %s" % type(key).__name__)
		return num

	def getByIndex(self, idx: int) -> Any:
		num = self._owner.font.objectInNumbersAtIndex_(idx)
		if num is None:
			raise KeyError("No number for %s" % idx)
		return self._owner.numberValueValueForId_(num.id)

	def getByKey(self, key: str) -> Any:
		return self._owner.numberValueValueForId_(key)

	def setByIndex(self, idx: int, value: float) -> Any:
		num = self._owner.font.objectInNumbersAtIndex_(idx)
		if num is None:
			raise KeyError("No number for %s" % idx)
		return self._owner.setNumberValueValue_forId_(value, num.id)

	def setByKey(self, key: str, value: float) -> Any:
		return self._owner.setNumberValueValue_forId_(value, key)

	def insertAtIndex(self, idx: int, value: float) -> None:
		raise TypeError("Can’t insert number Values. Insert a Number on the font")

	def removeByIndex(self, idx: int) -> None:
		raise TypeError("Can’t remove number Values. Remove a Number on the font")

	def removeByKey(self, key: str) -> None:
		raise TypeError("Can’t remove anumberxis Values. Remove a Number on the font")

	def values(self):
		return self._owner.numberValuesArray()

	def __len__(self) -> int:
		if self._owner.font is None:
			return 0
		return self._owner.font.countOfNumbers()

	def _setterMethod(self, values):
		idx = 0
		if self._owner.font is None:
			return
		if self.__len__() != len(values):
			raise ValueError("Count of values doesn’t match numbers")
		for number in self._owner.font.numbers:
			self._owner.setNumberValueValue_forId_(values[idx], number.id)
			idx += 1

	def setterMethod(self):
		return self._setterMethod


class CustomParametersProxy(OrderedDictProxy[GSCustomParameter]):

	def getKeyOf(self, value: GSCustomParameter) -> str:
		if isinstance(value, GSCustomParameter):
			return value.name
		parameter: GSCustomParameter
		for parameter in self.values():
			if parameter.value == value:
				return parameter.name
		return ""

	def getByIndex(self, idx: int) -> GSCustomParameter:
		return self._owner.objectInCustomParametersAtIndex_(idx)

	def getByKey(self, key: str) -> GSCustomParameter:
		return self._owner.customValueForKey_(key)

	def setByIndex(self, idx: int, value: Any) -> None:
		self._owner.replaceObjectInCustomParametersAtIndex_withObject_(idx, value)

	def setByKey(self, key: str, value: Any) -> None:
		# TODO: This expects a value in Parameter, not a Parameter object which the list elements are
		self._owner.setCustomValue_forKey_(objcObject(value), objcObject(key))

	def removeByIndex(self, idx: int) -> None:
		self._owner.removeObjectFromCustomParametersAtIndex_(idx)

	def removeByKey(self, key: str) -> None:
		self._owner.removeObjectFromCustomParametersForKey_(key)

	def __contains__(self, parameter: GSCustomParameter | str):
		if isString(parameter):
			return self._owner.customParameterForKey_(parameter) is not None
		return self._owner.pyobjc_instanceMethods.customParameters().containsObject_(parameter)

	def append(self, parameter: GSCustomParameter):
		self._owner.addCustomParameter_(parameter)

	def extend(self, parameters: List[GSCustomParameter]):
		for parameter in parameters:
			self._owner.addCustomParameter_(parameter)

	def remove(self, parameter: GSCustomParameter):
		self._owner.removeObjectFromCustomParameters_(parameter)

	def insertAtIndex(self, idx: int, parameter: GSCustomParameter):
		self._owner.insertObject_inCustomParametersAtIndex_(parameter, idx)

	def __len__(self) -> int:
		return self._owner.countOfCustomParameters()

	def values(self) -> List[GSCustomParameter]:
		return self._owner.pyobjc_instanceMethods.customParameters()

	def setterMethod(self):
		return self._owner.setCustomParameters_


class FontClassesProxy(OrderedDictProxy[GSClass]):

	def getKeyOf(self, value: GSClass) -> str:
		return value.name

	def getByIndex(self, idx: int) -> Any:
		return self._owner.objectInClassesAtIndex_(idx)

	def getByKey(self, key: str) -> Any:
		return self._owner.classForTag_(key)

	def setByIndex(self, idx: int, value: GSClass) -> None:
		self._owner.replaceObjectInClassesAtIndex_withObject_(idx, value)

	def setByKey(self, key: str, value: GSClass) -> None:
		Class = self._owner.classForTag_(key)
		idx = self._owner.indexOfObjectInClasses_(Class)
		self.setByIndex(idx, value)

	def removeByIndex(self, idx: int) -> None:
		return self._owner.removeObjectFromClassesAtIndex_(idx)

	def removeByKey(self, key: str) -> None:
		Class = self._owner.classForTag_(key)
		if Class is not None:
			return self._owner.removeClass_(Class)

	def append(self, value: GSClass):
		self._owner.addClass_(value)

	def extend(self, classes: List[GSClass]):
		for Class in classes:
			self._owner.addClass_(Class)

	def remove(self, Class):
		self._owner.removeClass_(Class)

	def insertAtIndex(self, idx: int, value: GSClass):
		idx = _validate_idx(cast(Sequence, self), idx, offset=1)
		self._owner.insertObject_inClassesAtIndex_(value, idx)

	def __len__(self) -> int:
		return self._owner.countOfClasses()

	def values(self):
		return self._owner.pyobjc_instanceMethods.classes()

	def setterMethod(self):
		return self._owner.setClasses_


class FontFeaturesProxy(OrderedDictProxy[GSFeature]):

	def getKeyOf(self, value: GSFeature) -> str:
		return value.tag

	def getByIndex(self, idx: int) -> GSFeature:
		return self._owner.objectInFeaturesAtIndex_(idx)

	def getByKey(self, key: str) -> GSFeature:
		return self._owner.featureForTag_(key)

	def setByIndex(self, idx: int, feature: GSFeature) -> None:
		self._owner.replaceObjectInFeaturesAtIndex_withObject_(idx, feature)

	def setByKey(self, key: str, feature: GSFeature) -> None:
		raise TypeError("keys must be integers, not %s" % type(key).__name__)

	def insertAtIndex(self, idx: int, feature: GSFeature) -> None:
		self._owner.insertObject_inFeaturesAtIndex_(feature, idx)

	def removeByIndex(self, idx: int) -> None:
		self._owner.removeObjectFromFeaturesAtIndex_(idx)

	def removeByKey(self, key: str) -> None:
		feature = self._owner.featureForTag_(key)
		if feature is not None:
			return self._owner.removeFeature_(feature)
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
		idx = _validate_idx(cast(Sequence, self), idx, offset=1)
		self._owner.insertObject_inFeaturesAtIndex_(Class, idx)

	def __len__(self) -> int:
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

class FontFeaturePrefixesProxy(OrderedDictProxy[GSFeaturePrefix]):

	def getKeyOf(self, value: GSFeaturePrefix) -> str:
		return value.name

	def getByIndex(self, idx: int) -> GSFeaturePrefix:
		return self._owner.objectInFeaturePrefixesAtIndex_(idx)

	def getByKey(self, key: str) -> GSFeaturePrefix:
		return self._owner.featurePrefixForTag_(key)

	def setByIndex(self, idx: int, featurePrefix: GSFeaturePrefix):
		self._owner.replaceObjectInFeaturePrefixesAtIndex_withObject_(idx, featurePrefix)

	def setByKey(self, key: str, featurePrefix: GSFeaturePrefix):
		raise TypeError("keys must be integers, not %s" % type(key).__name__)

	def insertAtIndex(self, idx: int, featurePrefix: GSFeaturePrefix) -> None:
		self._owner.insertObject_inFeaturePrefixesAtIndex_(featurePrefix, idx)

	def removeByIndex(self, idx: int):
		self._owner.removeObjectFromFeaturePrefixesAtIndex_(idx)

	def removeByKey(self, key: str) -> None:
		featurePrefix = self._owner.featurePrefixForTag_(key)
		if featurePrefix is not None:
			return self._owner.removeFeaturePrefix_(featurePrefix)
		else:
			raise TypeError("didn’t find Prefix with key: {key}")

	def append(self, featurePrefix):
		self._owner.addFeaturePrefix_(featurePrefix)

	def extend(self, FeaturePrefixes):
		for featurePrefix in FeaturePrefixes:
			self._owner.addFeaturePrefix_(featurePrefix)

	def remove(self, featurePrefix):
		self._owner.removeFeaturePrefix_(featurePrefix)

	def insert(self, idx, featurePrefix):
		idx = _validate_idx(cast(Sequence, self), idx, offset=1)
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


class UserDataProxy(DictProxy):

	def getKeyOf(self, value: Any) -> str:
		userData: NSMutableDictionary = self._owner.pyobjc_instanceMethods.userData()
		keys: list = userData.keysForObject_(value)
		if keys:
			return keys[0]
		return ""

	def getByKey(self, key: str) -> Any:
		return self._owner.userDataForKey_(key)

	def setByKey(self, key: str, value: Any) -> None:
		self._owner.setUserData_forKey_(objcObject(value), key)

	def removeByKey(self, key: str) -> None:
		self._owner.removeUserDataForKey_(key)

	def __len__(self) -> int:
		return self._owner.countOfUserData()

	def values(self):
		userData = self._owner.pyobjc_instanceMethods.userData()
		if userData is not None:
			return userData.allValues()
		return []

	def keys(self):
		userData = self._owner.pyobjc_instanceMethods.userData()
		if userData is not None:
			return userData.allKeys()
		return []

	def __str__(self):
		return self._owner.pyobjc_instanceMethods.userData().__str__()

	def __contains__(self, item):
		return self._owner.userDataForKey_(item) is not None

	def get(self, key, default=None):
		value = self.__getitem__(key)
		if value is None:
			return default
		return value

	def items(self):
		if self._owner.pyobjc_instanceMethods.userData() is None:
			return []
		return self._owner.pyobjc_instanceMethods.userData().items()

	def __copy__(self):
		return self._owner.pyobjc_instanceMethods.userData().copy()

	def __deepcopy__(self, memo):
		return self._owner.pyobjc_instanceMethods.userData().deepMutableCopy()

	def setter(self, values: dict):
		if values is not None and not isinstance(values, (dict, NSDictionary, self.__class__)):
			ValueError("%s is not a dict" % values)
		self._owner.setUserData_(values)

class TempDataProxy(DictProxy):

	def getKeyOf(self, value: Any) -> str:
		tempData: NSMutableDictionary = self._owner.pyobjc_instanceMethods.tempData()
		keys: list = tempData.keysForObject_(value)
		if keys:
			return keys[0]
		return ""

	def getByKey(self, key: str) -> Any:
		return self._owner.tempDataForKey_(key)

	def setByKey(self, key: str, value: Any) -> None:
		self._owner.setTempData_forKey_(objcObject(value), key)

	def removeByKey(self, key: str) -> None:
		self._owner.setTempData_forKey_(None, key)

	def values(self) -> List[Any]:
		tempData = self._owner.pyobjc_instanceMethods.tempData()
		if tempData is not None:
			return tempData.allValues()
		return []

	def keys(self) -> List[str]:
		tempData = self._owner.pyobjc_instanceMethods.tempData()
		if tempData is not None:
			return tempData.allKeys()
		return []

	def __str__(self) -> str:
		return self._owner.pyobjc_instanceMethods.tempData().__str__()

	def __contains__(self, item) -> bool:
		return self._owner.tempDataForKey_(item) is not None

	def get(self, key: str, default=None) -> Any | None:
		value = self.__getitem__(key)
		if value is None:
			return default
		return value

	def __copy__(self):
		return self._owner.pyobjc_instanceMethods.tempData().copy()

	def __deepcopy__(self, memo):
		return self._owner.pyobjc_instanceMethods.tempData().deepMutableCopy()

	def setter(self, values: dict):
		if values is not None and not isinstance(values, (dict, NSDictionary, self.__class__)):
			ValueError("%s is not a dict" % values)
		self._owner.setTempData_(values)

class AttributesProxy(DictProxy):

	def getKeyOf(self, value: Any) -> str:
		NotImplementedError()
		return ""

	def getByKey(self, key: str) -> Any:
		return self._owner.attributeForKey_(key)

	def setByKey(self, key: str, value: Any) -> None:
		if value is None:
			self._owner.removeAttributeForKey_(objcObject(key))
		else:
			self._owner.setAttribute_forKey_(objcObject(value), objcObject(key))

	def removeByKey(self, key: str) -> None:
		self._owner.setAttribute_forKey_(None, key)

	def values(self) -> list[Any]:
		attribute = self._owner.pyobjc_instanceMethods.attributes()
		if attribute is not None:
			return attribute.allValues()
		return []

	def keys(self) -> list[str]:
		attribute = self._owner.pyobjc_instanceMethods.attributes()
		if attribute is not None:
			return attribute.allKeys()
		return []

	def __str__(self):
		return self._owner.pyobjc_instanceMethods.attributes().__str__()

	def __repr__(self):
		return self._owner.pyobjc_instanceMethods.attributes().__repr__()

	def __contains__(self, item):
		return self._owner.pyobjc_instanceMethods.attributeForKey_(item) is not None

	def get(self, key, default=None) -> Any:
		value = self.__getitem__(key)
		if value is None:
			return default
		return value

	def __copy__(self):
		return self._owner.pyobjc_instanceMethods.attributes().copy()

	def __deepcopy__(self, memo):
		return self._owner.pyobjc_instanceMethods.attributes().deepMutableCopy()


class FontInfoPropertyProxy(DictProxy[GSInfoValue]):

	_propertyKey: str

	def getKeyOf(self, value: Any) -> str:
		return self._propertyKey

	def __init__(self, owner, propertyKey):
		self._owner = owner
		self._propertyKey = propertyKey

	def getByKey(self, languageKey: str) -> Any:
		return self._owner.propertyForName_languageTag_(self._propertyKey, languageKey)

	def setByKey(self, languageKey: str, value: Any) -> None:
		self._owner.setProperty_value_languageTag_(self._propertyKey, objcObject(value), objcObject(languageKey))

	def removeByKey(self, languageKey: str):
		self._owner.removeObjectFromProperties_(self._owner.propertyForName_languageTag_(self._propertyKey, languageKey))

	def values(self):
		_property = self._owner.propertyForName_(self._propertyKey)
		if _property is not None:
			return [value.value for value in _property.values]
		return []

	def keys(self):
		_property = self._owner.propertyForName_(self._propertyKey)
		if _property is not None:
			return [value.languageTag for value in _property.values]
		return []

	def __str__(self):
		_property = self._owner.propertyForName_(self._propertyKey)
		if _property is None:
			return None.__str__()
		reprValue = "".join([f'\t{value.languageTag}, {value.value}\n' for value in _property.values])
		return f"(\n{reprValue})"

	def __contains__(self, item):
		_property = self._owner.propertyForName_(self._propertyKey)
		if _property is not None:
			return item in [value.key for value in _property.values]
		return False

	def get(self, key, default=None):
		value = self.__getitem__(key)
		if value is None:
			return default
		return value


class SmartComponentValuesProxy(DictProxy[float]):

	def getKeyOf(self, value: float) -> str:
		pieceSettings = self._owner.pieceSettings()
		keys = pieceSettings.allKeysForObject_(value)
		if keys:
			return keys[0]
		return ""

	def getByKey(self, key: str) -> float | None:
		pieceSettings = self._owner.pieceSettings()
		if pieceSettings is not None:
			return pieceSettings.objectForKey_(key)
		return None

	def setByKey(self, key: str, value: float):
		self._owner.setPieceValue_forKey_(float(value), key)

	def removeByKey(self, key: str):
		pieceSettings = self._owner.pieceSettings()
		if pieceSettings is not None:
			del (pieceSettings[key])

	def keys(self):
		pieceSettings = self._owner.pieceSettings()
		if pieceSettings is not None and len(pieceSettings) > 0:
			return pieceSettings.allKeys()
		return None

	def values(self):
		pieceSettings = self._owner.pieceSettings()
		if pieceSettings is not None and len(pieceSettings) > 0:
			return [float(v) for v in pieceSettings.allValues()]
		return None

	def __str__(self):
		pieceSettings = self._owner.pieceSettings()
		return str(pieceSettings)

	def items(self):
		return self._owner.pieceSettings().items()


class LayersIterator(Iterator[GSLayer]):

	def __init__(self, owner):
		self.curInd = 0
		self._owner = owner

	def __iter__(self) -> Iterator[GSLayer]:
		return self

	def __next__(self) -> GSLayer:
		if self._owner.parent:
			if self.curInd < self._owner.parent.countOfFontMasters():
				FontMaster = self._owner.parent.fontMasterAtIndex_(self.curInd)
				item: GSLayer = self._owner.layerForId_(FontMaster.id)
			else:
				if self.curInd >= self._owner.countOfLayers():
					raise StopIteration
				ExtraLayerIndex = self.curInd - self._owner.parent.countOfAllMasters()
				idx = 0
				ExtraLayer = None
				while ExtraLayerIndex >= 0:
					ExtraLayer = self._owner.objectInLayersAtIndex_(idx)
					if not ExtraLayer.isMasterLayer:
						ExtraLayerIndex -= 1
					idx += 1
				item = ExtraLayer
			self.curInd += 1
			return item
		else:
			if self.curInd >= self._owner.countOfLayers():
				raise StopIteration
			Item = self._owner.objectInLayersAtIndex_(self.curInd)
			self.curInd += 1
			return Item


class GlyphLayerProxy(OrderedDictProxy[GSLayer]):

	def getKeyOf(self, value: GSLayer) -> str:
		return value.layerId

	def getByIndex(self, key: int) -> GSLayer:
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
			key = _validate_idx(cast(Sequence, self), key)
			return self._owner.objectInLayersAtIndex_(key)

	def getByKey(self, key: str) -> GSLayer:
		layer = self._owner.layerForId_(key)
		if layer is None:
			layer = self._owner.layerForName_(key)
		return layer

	def setByIndex(self, idx: int, value: GSLayer) -> None:
		FontMaster = self._owner.parent.fontMasterAtIndex_(idx)
		key = FontMaster.id
		self._owner.setLayer_forId_(value, key)

	def setByKey(self, key: str, value: GSLayer) -> None:
		self._owner.setLayer_forId_(value, key)

	def insertAtIndex(self, idx: int, value: GSLayer) -> None:
		self._owner.setLayer_forId_(value, value.layerId)

	def removeByIndex(self, idx: int):
		layer: GSLayer = self.getByIndex(idx)
		key = layer.layerId
		return self._owner.removeLayerForId_(key)

	def removeByKey(self, key: str):
		return self._owner.removeLayerForId_(key)

	def __iter__(self):
		return LayersIterator(self._owner)

	def __len__(self) -> int:
		return self._owner.countOfLayers()

	def values(self):
		return self._owner.pyobjc_instanceMethods.layers().allValues()

	def append(self, Layer):
		if not Layer.associatedMasterId:
			Layer.associatedMasterId = self._owner.parent.masters[0].id
		self._owner.setLayer_forId_(Layer, NSString.UUID())

	def remove(self, layer: GSLayer):
		return self._owner.removeLayerForId_(layer.layerId)

	def insert(self, idx: int, layer: GSLayer):
		idx = _validate_idx(cast(Sequence, self), idx, offset=1)
		self.append(layer)

	def setter(self, values: list[GSLayer]):
		newLayers: NSMutableDictionary = NSMutableDictionary.dictionary()
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

def __NSOrderedSet__iter__(self):
	for each in self.array():
		yield each


objc.addConvenienceForClass(
	"NSOrderedSet",
	(
		("__iter__", python_method(__NSOrderedSet__iter__)),
	)
)

class GlyphsTagsProxy(ListProxy[str]):

	def getByIndex(self, idx: int) -> str:
		return self._owner.objectInTagsAtIndex_(idx)

	def setByIndex(self, idx: int, tag: str):
		self._validate_value(tag)
		self._owner.replaceObjectInTagsAtIndex_withObject_(idx, tag)

	def insertAtIndex(self, idx: int, value: str) -> None:
		self._validate_value(value)
		self._owner.insertObject_inTagsAtIndex_(value, idx)

	def removeByIndex(self, idx: int):
		return self._owner.removeObjectFromTagsAtIndex_(idx)

	def append(self, tag):
		self._validate_value(tag)
		self._owner.addTag_(tag)

	def extend(self, tags):
		for tag in tags:
			self._owner.addTag_(tag)

	def insert(self, idx, tag):
		idx = _validate_idx(cast(Sequence, self), idx, offset=1)
		self._owner.insertObject_inTagsAtIndex_(tag, idx)

	def remove(self, tag):
		self._owner.removeObjectFromTags_(tag)

	def values(self):
		return self._owner.pyobjc_instanceMethods.tags().array()

	def setterMethod(self):
		return self._owner.setTags_

	def _validate_value(self, tag):
		if not isString(tag):
			raise TypeError("“Tag” must be str, not %s" % type(tag).__name__)


class LayerGuidesProxy(ListProxy[GSGuide]):

	def getByIndex(self, idx: int) -> GSGuide:
		return self._owner.objectInGuidesAtIndex_(idx)

	def setByIndex(self, idx: int, value: GSGuide) -> None:
		self._owner.replaceObjectInGuidesAtIndex_withObject_(idx, value)

	def insertAtIndex(self, idx: int, value: GSGuide) -> None:
		self._owner.insertObject_inGuidesAtIndex_(value, idx)

	def removeByIndex(self, idx: int):
		return self._owner.removeObjectFromGuidesAtIndex_(idx)

	def append(self, Guide):
		self._owner.addGuide_(Guide)

	def extend(self, Guides):
		for Guide in Guides:
			self._owner.addGuide_(Guide)

	def insert(self, idx, guide):
		idx = _validate_idx(cast(Sequence, self), idx, offset=1)
		self._owner.insertObject_inGuidesAtIndex_(guide, idx)

	def remove(self, Guide):
		self._owner.removeObjectFromGuides_(Guide)

	def values(self):
		return self._owner.pyobjc_instanceMethods.guides()

	def setterMethod(self):
		return self._owner.setGuides_


class LayerAnnotationProxy(ListProxy[GSAnnotation]):

	def getByIndex(self, idx: int) -> GSAnnotation:
		return self._owner.objectInAnnotationsAtIndex_(idx)

	def setByIndex(self, idx: int, annotation: GSAnnotation):
		idx = _validate_idx(cast(Sequence, self), idx)
		self._owner.replaceObjectInAnnotationsAtIndex_withObject_(idx, annotation)

	def insertAtIndex(self, idx: int, value: Any) -> None:
		self._owner.insertObject_inAnnotationsAtIndex_(value, idx)

	def removeByIndex(self, idx: int):
		return self._owner.removeObjectFromAnnotationsAtIndex_(idx)

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


class LayerHintsProxy(ListProxy[GSHint]):

	def getByIndex(self, idx: int) -> GSHint:
		return self._owner.objectInHintsAtIndex_(idx)

	def setByIndex(self, idx: int, hint: GSHint):
		self._owner.replaceObjectInHintsAtIndex_withObject_(idx, hint)

	def insertAtIndex(self, idx: int, value: Any) -> None:
		self._owner.insertObject_inHintsAtIndex_(value, idx)

	def removeByIndex(self, idx: int):
		return self._owner.removeObjectFromHintsAtIndex_(idx)

	def append(self, hint):
		self._owner.addHint_(hint)

	def extend(self, hints):
		for hint in hints:
			self._owner.addHint_(hint)

	def insert(self, idx, hint):
		idx = _validate_idx(cast(Sequence, self), idx, offset=1)
		self._owner.insertObject_inHintsAtIndex_(hint, idx)

	def remove(self, Hint):
		self._owner.removeHint_(Hint)

	def values(self):
		return self._owner.pyobjc_instanceMethods.hints()

	def setterMethod(self):
		return self._owner.setHints_

class LayerAnchorsProxy(DictProxy[GSAnchor]):
	"""layer.anchors is a dict!!!"""

	def getKeyOf(self, value: GSAnchor) -> str:
		return value.name

	def getByKey(self, key: str) -> GSAnchor:
		return self._owner.anchorForName_(key)

	def setByKey(self, key: str, value: GSAnchor) -> None:
		value.name = key
		self._owner.addAnchor_(value)

	def removeByKey(self, key: str) -> None:
		self._owner.removeAnchorWithName_(key)

	def __iter__(self) -> Iterator[str]:
		return iter(self.values())

	def items(self):
		items = []
		for key in self.keys():
			value = self._owner.anchorForName_(key)
			items.append((key, value))
		return items

	def values(self):
		anchors = self._owner.pyobjc_instanceMethods.anchors()
		if anchors is not None:
			return anchors.allValues()
		else:
			return []

	def keys(self):
		anchors = self._owner.pyobjc_instanceMethods.anchors()
		if anchors is not None:
			return anchors.allKeys()
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

	def __len__(self) -> int:
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


class LayerShapesProxy(ListProxy[GSShape]):

	def getByIndex(self, idx: int) -> GSShape:
		return self._owner.objectInShapesAtIndex_(idx)

	def setByIndex(self, idx: int, shape: GSShape):
		self._owner.replaceShapeAtIndex_withShape_(idx, shape)

	def insertAtIndex(self, idx: int, value: GSShape) -> None:
		self._owner.insertObject_inShapesAtIndex_(value, idx)

	def removeByIndex(self, idx: int):
		return self._owner.removeObjectFromShapesAtIndex_(idx)

	def __len__(self) -> int:
		return self._owner.countOfShapes()

	def __contains__(self, item):
		return self._owner.pyobjc_instanceMethods.shapes().containsObject_(item)

	def append(self, shape):
		if not isinstance(shape, (GSPath, GSComponent)):
			raise TypeError("only GSShape objects are accepted, not %s" % type(shape).__name__)
		self._owner.addShape_(shape)

	def extend(self, shapes):
		if isinstance(shapes, type(self)):
			for shape in shapes.values():
				self.append(shape)
		elif isinstance(shapes, (list, tuple, NSArray)):
			for shape in shapes:
				self.append(shape)
		else:
			raise TypeError

	def remove(self, shape):
		self._owner.removeShape_(shape)

	def insert(self, idx, shape):
		idx = _validate_idx(cast(Sequence, self), idx, offset=1)
		if not isinstance(shape, (GSPath, GSComponent)):
			raise TypeError("only GSShape objects are accepted, not %s" % type(shape).__name__)
		self._owner.insertObject_inShapesAtIndex_(shape, idx)

	def values(self):
		return self._owner.pyobjc_instanceMethods.shapes()

	def index(self, value: Any) -> int:
		return self._owner.indexOfObjectInShapes_(value)

	def setterMethod(self):
		return self._owner.setShapes_


class LayerSelectionProxy(ListProxy[GSElement]):

	def getByIndex(self, idx: int) -> GSElement:
		if self._owner.countOfSelection() == 0:
			raise IndexError("Nothing selected (%d)" % idx)
		return self._owner.pyobjc_instanceMethods.selection().objectAtIndex_(idx)

	def setByIndex(self, idx: int, value: Any) -> None:
		self._owner.removeObjectFromSelectionAtIndex_(idx)
		self._owner.insertObject_inSelectionAtIndex_(value, idx)

	def insertAtIndex(self, idx: int, object: GSElement):
		self._owner.addSelection_(object)

	def removeByIndex(self, idx: int) -> None:
		self._owner.removeObjectFromSelectionAtIndex_(idx)

	def __len__(self) -> int:
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


	def clear(self):
		self._owner.clearSelection()

	def _setSelecetion_(self, selection):
		self.clear()
		if selection is not None:
			self.extend(selection)

	def setterMethod(self):
		return self._setSelecetion_

class PathNodesProxy(ListProxy[GSNode]):

	def getByIndex(self, idx: int) -> GSNode:
		if not self._owner.closed:
			idx = _validate_idx(cast(Sequence, self), idx)
		node = self._owner.nodeAtIndex_(idx)
		if node is None:
			IndexError("list index %s out of range %s" % (idx, self.__len__()))
		return node

	def setByIndex(self, idx: int, node: GSNode):
		self._owner.replaceObjectInNodesAtIndex_withObject_(idx, node)

	def insertAtIndex(self, idx: int, value: Any) -> None:
		self._owner.insertObject_inNodesAtIndex_(value, idx)

	def removeByIndex(self):
		return self._owner.removeObjectFromNodesAtIndex_

	def __len__(self) -> int:
		return self._owner.countOfNodes()

	def append(self, node):
		self._owner.addNode_(node)

	def remove(self, node):
		self._owner.removeNode_(node)

	def insert(self, idx, node):
		idx = _validate_idx(cast(Sequence, self), idx, offset=1)
		self._owner.insertNode_atIndex_(node, idx)

	def extend(self, objects):
		self._owner.addNodes_(list(objects))

	def index(self, node):
		idx = self._owner.indexOfNode_(node)
		if idx > 100000:
			raise ValueError("%s is not in list" % node)
		return idx

	def __iter__(self):
		return self.NodeIterator(self)

	class NodeIterator:
		def __init__(self, proxy):
			self.index = 0
			self.path = proxy._owner
			self.count = self.path.countOfNodes()

		def __iter__(self):
			return self

		def __next__(self):
			if self.index < self.count:
				result = self.path.nodeAtIndex_(self.index)
				self.index += 1
				return result
			else:
				raise StopIteration

	def values(self):
		return self._owner.pyobjc_instanceMethods.nodes()

	def __contains__(self, item):
		return self._owner.pyobjc_instanceMethods.nodes().containsObject_(item)

	def setterMethod(self):
		return self._owner.setNodes_


class GradientColorsProxy(ListProxy[GSColorStop]):

	def getByIndex(self, idx: int) -> GSColorStop:
		return self._owner.colorLine().objectInColorStopsAtIndex_(idx)

	def setByIndex(self, idx, color: GSColorStop):
		idx = _validate_idx(cast(Sequence, self), idx)
		self._owner.replaceObjectInColorsAtIndex_withObject_(idx, color)

	def insertAtIndex(self, idx: int, value: Any) -> None:
		self._owner.colorLine().insertObject_inColorStopsAtIndex_(value, idx)

	def removeByIndex(self, idx: int):
		return self._owner.removeObjectFromColorsAtIndex_(idx)

	def append(self, color):
		self._owner.addColor_(color)

	def extend(self, colors):
		for color in colors:
			self._owner.addColor_(color)

	def remove(self, color):
		self._owner.removeObjectFromColors_(color)

	def insert(self, idx, color):
		if isinstance(idx, int):
			idx = _validate_idx(cast(Sequence, self), idx, offset=1)
			self._owner.insertObject_inColorsAtIndex_(color, idx)
		else:
			raise TypeError("list indices must be integers, not %s" % type(idx).__name__)

	def __len__(self) -> int:
		return self._owner.countOfColors()

	def values(self):
		return self._owner.pyobjc_instanceMethods.colors()

	def setterMethod(self):
		return self._owner.setColors_


class FontTabsProxy(ListProxy[GSEditViewController]):

	def getByIndex(self, idx: int) -> GSEditViewController:
		if self._owner.parent:
			if isinstance(idx, int):
				idx = _validate_idx(cast(Sequence, self), idx)
				return self._owner.parent.windowController().tabBarControl().tabItemAtIndex_(idx + 1)
			else:
				raise TypeError("list indices must be integers or slices, not %s" % type(idx).__name__)
		else:
			raise Exception("The font is not connected to a document object")

	def setByIndex(self, idx: int, tab: GSEditViewController) -> None:
		if isinstance(idx, int):
			raise (NotImplementedError)  # TODO
		else:
			raise TypeError("list indices must be integers, not %s" % type(idx).__name__)

	def insertAtIndex(self, idx: int, tab: GSEditViewController) -> None:
		self._owner.parent.windowController().tabBarControl().insertTabItem_atIndex_(tab, idx)

	def removeByIndex(self, idx: int):
		Tab = self._owner.parent.windowController().tabBarControl().tabItemAtIndex_(idx + 1)
		self._owner.parent.windowController().tabBarControl().closeTabItem_(Tab)

	def __len__(self) -> int:
		return self._owner.parent.windowController().tabBarControl().countOfTabItems() - 1

	def values(self):
		return self._owner.parent.windowController().tabBarControl().tabItems()[1:]


# Function shared by all user-selectable elements in a layer (nodes, anchors etc.)
def __ObjectInLayer_selected__(self):
	try:
		return self in self.layer.selection
	except:
		return False


def __SetObjectInLayer_selected__(self, state):

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


def ____GSFont____(): pass


'''

:mod:`GSFont`
===============================================================================

Implementation of the font object. This object is host to the :class:`masters <GSFontMaster>` used for interpolation. Even when no interpolation is involved, for the sake of object model consistency there will still be one master and one instance representing a single font.

Also, the :class:`glyphs <GSGlyph>` are attached to the Font object right here, not one level down to the masters. The different masters’ glyphs are available as :class:`layers <GSLayer>` attached to the glyph objects which are attached here.

.. class:: GSFont(([path]))

	:param path: the path to a glyphs file

	Properties

		* :attr:`parent`
		* :attr:`masters`
		* :attr:`axes`
		* :attr:`properties`
		* :attr:`stems`
		* :attr:`instances`
		* :attr:`glyphs`
		* :attr:`classes`
		* :attr:`features`
		* :attr:`featurePrefixes`
		* :attr:`copyright`
		* :attr:`copyrights`
		* :attr:`license`
		* :attr:`licenses`
		* :attr:`designer`
		* :attr:`designers`
		* :attr:`designerURL`
		* :attr:`manufacturer`
		* :attr:`manufacturers`
		* :attr:`manufacturerURL`
		* :attr:`familyNames`
		* :attr:`trademark`
		* :attr:`trademarks`
		* :attr:`sampleText`
		* :attr:`sampleTexts`
		* :attr:`description`
		* :attr:`descriptions`
		* :attr:`compatibleFullName`
		* :attr:`compatibleFullNames`
		* :attr:`versionMajor`
		* :attr:`versionMinor`
		* :attr:`date`
		* :attr:`familyName`
		* :attr:`upm`
		* :attr:`note`
		* :attr:`kerning`
		* :attr:`userData`
		* :attr:`grid`
		* :attr:`gridSubDivision`
		* :attr:`gridLength`
		* :attr:`keyboardIncrement`
		* :attr:`keyboardIncrementBig`
		* :attr:`keyboardIncrementHuge`
		* :attr:`snapToObjects`
		* :attr:`disablesNiceNames`
		* :attr:`customParameters`
		* :attr:`selection`
		* :attr:`selectedLayers`
		* :attr:`selectedFontMaster`
		* :attr:`masterIndex`
		* :attr:`currentText`
		* :attr:`tabs`
		* :attr:`fontView`
		* :attr:`currentTab`
		* :attr:`filepath`
		* :attr:`tool`
		* :attr:`tools`
		* :attr:`appVersion`

	Functions

		* :meth:`close`
		* :meth:`compileFeatures`
		* :meth:`copy`
		* :meth:`disableUpdateInterface`
		* :meth:`enableUpdateInterface`
		* :meth:`export`
		* :meth:`kerningForPair`
		* :meth:`newTab`
		* :meth:`removeKerningForPair`
		* :meth:`save`
		* :meth:`setKerningForPair`
		* :meth:`show`
		* :meth:`updateFeatures`


	**Properties**
'''


def __GSFont__new__(typ, *args, **kwargs):
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


GSFont.__new__ = staticmethod(__GSFont__new__)


def __GSFont__init__(self, path: str | None = None) -> None:
	pass

GSFont.__init__ = python_method(__GSFont__init__)  # type: ignore


def __GSFont__str__(self: GSFont) -> str:
	return "<GSFont \"%s\" v%s.%s with %s masters and %s instances>" % (
		self.familyName, self.versionMajor, self.versionMinor,
		len(self.masters), len(self.instances)  # type: ignore
	)
GSFont.__str__ = python_method(__GSFont__str__)  # type: ignore


def Font__copy__(self, memo=None):
	font = self.copy()
	font.setParent_(self.parent)
	return font


GSFont.mutableCopyWithZone_ = Font__copy__
GSFont.__copy__ = python_method(Font__copy__)
GSFont.__deepcopy__ = python_method(Font__copy__)


def __GSFont__contains__(self, key):
	raise NotImplementedError("Font can't access values like this")


GSFont.__contains__ = python_method(__GSFont__contains__)

GSFont.parent = property(lambda self: self.pyobjc_instanceMethods.parent())
add_type(GSFont, "parent", GSDocument | None)
'''
	.. attribute:: parent

		Returns the internal NSDocument document. Read-only.

		:type: NSDocument
'''

GSFont.masters = property(
	lambda self: FontFontMasterProxy(self),
	lambda self, value: FontFontMasterProxy(self).setter(value)
)
add_type(GSFont, 'masters', List[GSFontMaster])

'''
	.. attribute:: masters

		Collection of :class:`GSFontMaster` objects.

		:type: list
'''
GSInterpolationFontProxy.masters = property(lambda self: FontFontMasterProxy(self))

GSFont.instances = property(
	lambda self: FontInstancesProxy(self),
	lambda self, value: FontInstancesProxy(self).setter(value)
)
add_type(GSFont, 'instances', List[GSInstance])
'''
	.. attribute:: instances

		Collection of :class:`GSInstance` objects.

		.. code-block:: python
			for instance in font.instances:
			    print(instance)

			# to add a new instance
			instance = GSInstance()
			instance.name = "Some Instance"
			font.instances.append(instance)

			# to delete an instances
			del font.instances[0]

			font.instances.remove(someInstance)

		:type: list
'''

GSProjectDocument.font = property(lambda self: self.pyobjc_instanceMethods.font())

GSProjectDocument.instances = property(
	lambda self: FontInstancesProxy(self),
	lambda self, value: FontInstancesProxy(self).setter(value)
)

GSProjectDocument.customParameters = property(
	lambda self: CustomParametersProxy(self.font()),
	lambda self, value: CustomParametersProxy(self.font()).setter(value)
)

GSFont.axes = property(
	lambda self: FontAxesProxy(self),
	lambda self, value: FontAxesProxy(self).setter(value)
)
add_type(GSFont, 'axes', List[GSAxis])
'''
	.. attribute:: axes

		Collection of :class:`GSAxis`:

		.. code-block:: python
			for axis in font.axes:
			    print(axis)

			# to add a new axis
			axis = GSAxis()
			axis.name = "Some custom Axis"
			axis.axisTag = "SCAX"
			font.axes.append(axis)

			# to delete an axis
			del font.axes[0]

			font.axes.remove(someAxis)

		:type: list

		.. versionadded:: 2.5
		.. versionchanged:: 3
'''

GSFont.properties = property(
	lambda self: PropertiesProxy(self),
	lambda self, values: PropertiesProxy(self).setter(values)
)
add_type(GSFontMaster, 'properties', list[GSInfoValueSingle | GSInfoValueLocalized])
'''
	.. attribute:: properties

		Holds the fonts info properties. Can be instances of :class:`GSInfoValueSingle` and :class:`GSInfoValueLocalized`.

		The localized values use language tags defined in the middle column of `Language System Tags table`: <https://docs.microsoft.com/en-us/typography/opentype/spec/languagetags>.

		The names are listed in the constants: `Info Property Keys`_

		.. code-block:: python
			# To access the default value:

			font.properties["versionString"]

			font.properties["versionString"] = "version 1.0"

			# To access specific languages:

			font.properties.getProperty(GSPropertyNameDesignersKey, "DEU")

			font.properties.setProperty(GSPropertyNameDesignersKey, "SomeName", "DEU")

		:type: list

		.. versionadded:: 3
'''

GSFont.metrics = property(
	lambda self: FontMetricsProxy(self),
	lambda self, values: FontMetricsProxy(self).setter(values)
)

add_type(GSFont, 'metrics', List[GSMetric])
'''
	.. attribute:: metrics

		a list of all :class:`GSMetric` objects.

		:type: list

		.. code-block:: python
			# to add a new metric
			metric = GSMetric(GSMetricsTypexHeight)
			font.metrics.append(metric)
			metricValue = master.metrics[metric.id]
			metricValue.position = 543
			metricValue.overshoot = 17
'''

GSFont.stems = property(
	lambda self: FontStemsProxy(self),
	lambda self, value: FontStemsProxy(self).setter(value)
)
add_type(GSFont, 'stems', List[GSMetric])
'''
	.. attribute:: stems

		The stems. A list of :class:`GSMetric` objects. For each metric, there is a metricsValue in the masters, linked by the `id`.

		:type: list, dict

		.. code-block:: python
			font.stems[0].horizontal = False

			# add a stem
			stem = GSMetric()
			stem.horizontal = False # or True
			stem.name = "Some Name"
			font.stems.append(stem)
			master.stems[stem.name] = 123
'''

GSFont.numbers = property(
	lambda self: FontNumbersProxy(self),
	lambda self, value: FontNumbersProxy(self).setter(value)
)
add_type(GSFont, 'numbers', List[GSMetric])
'''
	.. attribute:: numbers

		The numbers. A list of :class:`GSMetric` objects. For each number, there is a metricsValue in the masters, linked by the `id`.

		:type: list, dict

		.. code-block:: python
			print(font.numbers[0].name)

			# add a number
			number = GSMetric()
			number.horizontal = False # or True
			number.name = "Some Name"
			font.numbers.append(number)
			master.numbers[number.name] = 123

'''


def __GSFont_getitem__(self, key):
	return self.glyphs[key]


GSFont.__getitem__ = python_method(__GSFont_getitem__)

GSFont.glyphs = property(
	lambda self: FontGlyphsProxy(self),
	lambda self, value: FontGlyphsProxy(self).setter(value))
add_type(GSFont, 'glyphs', List[GSGlyph] | Dict[str, GSGlyph])


GSInterpolationFontProxy.glyphs = property(
	lambda self: FontGlyphsProxy(self),
	lambda self, value: FontGlyphsProxy(self).setter(value)
)
'''
	.. attribute:: glyphs

		Collection of :class:`GSGlyph` objects. Returns a list, but you may also call glyphs using index or glyph name or character as key.

		:type: list, dict

		.. code-block:: python
			# Access all glyphs
			for glyph in font.glyphs:
			    print(glyph)
			>> <GSGlyph "A" with 4 layers>
			>> <GSGlyph "B" with 4 layers>
			>> <GSGlyph "C" with 4 layers>
			...

			# Access one glyph
			print(font.glyphs['A'])
			>> <GSGlyph "A" with 4 layers>

			# Access a glyph by character (new in v2.4.1)
			print(font.glyphs['Ư'])
			>> <GSGlyph "Uhorn" with 4 layers>

			# Access a glyph by unicode (new in v2.4.1)
			print(font.glyphs['01AF'])
			>> <GSGlyph "Uhorn" with 4 layers>

			# Access a glyph by index
			print(font.glyphs[145])
			>> <GSGlyph "Uhorn" with 4 layers>

			# Add a glyph
			font.glyphs.append(GSGlyph('adieresis'))

			# Duplicate a glyph under a different name
			newGlyph = font.glyphs['A'].copy()
			newGlyph.name = 'A.alt'
			font.glyphs.append(newGlyph)

			# Delete a glyph
			del font.glyphs['A.alt']
'''

GSFont.characterForGlyph = python_method(GSFont.characterForGlyph_)
'''
	.. function:: characterForGlyph(glyph)
		The (internal) character that is used in the edit view. It the glyph has a unicode, that is used, otherwise a temporary code is assigned. That can change over time, so don’t rely on it. This is mostly useful for constructing a string for see :attr:`tab.text <GSEditViewController.text>`

		.. versionadded:: 3.1
'''

GSFont.classes = property(
	lambda self: FontClassesProxy(self),
	lambda self, value: FontClassesProxy(self).setter(value)
)
add_type(GSFont, 'classes', List[GSClass])
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
			del font.classes['uppercaseLetters']
'''

GSFont.features = property(
	lambda self: FontFeaturesProxy(self),
	lambda self, value: FontFeaturesProxy(self).setter(value)
)
add_type(GSFont, 'features', List[GSFeature])
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
			del font.features['liga']
'''

GSFont.featurePrefixes = property(
	lambda self: FontFeaturePrefixesProxy(self),
	lambda self, value: FontFeaturePrefixesProxy(self).setter(value)
)
add_type(GSFont, 'featurePrefixes', List[GSFeaturePrefix])
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
			del font.featurePrefixes['LanguageSystems']
'''

GSFont.copyright = property(
	lambda self: self.defaultPropertyForName_("copyrights"),
	lambda self, value: self.setProperty_value_languageTag_("copyrights", value, None)
)
add_type(GSFont, 'copyright', str)
'''
	.. attribute:: copyright

		This accesses the default value only. The localizations can be accessed by :attr:`GSFont.properties`

		:type: str
'''

GSFont.copyrights = property(lambda self: FontInfoPropertyProxy(self, "copyrights"))
add_type(GSFont, 'copyrights', Dict[str, str])
'''
	.. attribute:: copyrights

		This accesses all localized copyright values.
		For details :attr:`GSFont.properties`

		:type: dict
		.. code-block:: python
			font.copyrights["ENG"] = "All rights reserved"

		.. versionadded:: 3.0.3
'''

GSFont.license = property(
	lambda self: self.defaultPropertyForName_("licenses"),
	lambda self, value: self.setProperty_value_languageTag_("licenses", value, None)
)
add_type(GSFont, 'license', str)
'''
	.. attribute:: license

		This accesses the default value only. The localizations can be accessed by :attr:`GSFont.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSFont.licenses = property(lambda self: FontInfoPropertyProxy(self, "licenses"))
add_type(GSFont, 'licenses', Dict[str, str])
'''
	.. attribute:: licenses

		This accesses all localized license values.
		For details :attr:`GSFont.properties`

		:type: dict

		.. code-block:: python
			font.licenses["ENG"] = "This font may be installed on all of your machines and printers, but you may not sell or give these fonts to anyone else."

		.. versionadded:: 3.0.3
'''

GSFont.compatibleFullName = property(
	lambda self: self.defaultPropertyForName_("compatibleFullNames"),
	lambda self, value: self.setProperty_value_languageTag_("compatibleFullNames", value, None))

add_type(GSFont, 'compatibleFullName', str)
'''
	.. attribute:: compatibleFullName

		This accesses the default value only. The localizations can be accessed by :attr:`GSFont.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSFont.compatibleFullNames = property(lambda self: FontInfoPropertyProxy(self, "compatibleFullNames"))
add_type(GSFont, 'compatibleFullNames', Dict[str, str])
'''
	.. attribute:: compatibleFullNames

		This accesses all localized designer values.
		For details :attr:`GSFont.properties`

		:type: dict

		.. code-block:: python
			font.compatibleFullNames["ENG"] = "MyFont Condensed Bold"

		.. versionadded:: 3.0.3
'''

GSFont.sampleText = property(
	lambda self: self.defaultPropertyForName_("sampleTexts"),
	lambda self, value: self.setProperty_value_languageTag_("sampleTexts", value, None)
)
add_type(GSFont, 'sampleText', str)
'''
	.. attribute:: sampleText

		This accesses the default value only. The localizations can be accessed by :attr:`GSFont.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSFont.sampleTexts = property(lambda self: FontInfoPropertyProxy(self, "sampleTexts"))
add_type(GSFont, 'sampleTexts', Dict[str, str])
'''
	.. attribute:: sampleTexts

		This accesses all localized designer values.
		For details :attr:`GSFont.properties`

		:type: dict

		.. code-block:: python
			font.sampleTexts["ENG"] = "This is my sample text"

		.. versionadded:: 3.0.3
'''

GSFont.description = property(
	lambda self: self.defaultPropertyForName_("descriptions"),
	lambda self, value: self.setProperty_value_languageTag_("descriptions", value, None)
)
'''
	.. attribute:: description

		This accesses the default value only. The localizations can be accessed by :attr:`GSFont.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSFont.descriptions = property(lambda self: FontInfoPropertyProxy(self, "descriptions"))
'''
	.. attribute:: descriptions

		This accesses all localized designer values.
		For details :attr:`GSFont.properties`

		:type: dict

		.. code-block:: python
			font.descriptions["ENG"] = "This is my description"

		.. versionadded:: 3.0.3
'''

GSFont.designer = property(
	lambda self: self.defaultPropertyForName_("designers"),
	lambda self, value: self.setProperty_value_languageTag_("designers", value, None)
)
'''
	.. attribute:: designer

		This accesses the default value only. The localizations can be accessed by :attr:`GSFont.properties`

		:type: str
'''

GSFont.designers = property(lambda self: FontInfoPropertyProxy(self, "designers"))
'''
	.. attribute:: designers

		This accesses all localized designer values.
		For details :attr:`GSFont.properties`

		:type: dict

		.. code-block:: python
			font.designers["ENG"] = "John Smith"

		.. versionadded:: 3.0.3
'''

GSFont.trademark = property(
	lambda self: self.defaultPropertyForName_("trademarks"),
	lambda self, value: self.setProperty_value_languageTag_("trademarks", value, None)
)
'''
	.. attribute:: trademark

		This accesses the default value only. The localizations can be accessed by :attr:`GSFont.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSFont.trademarks = property(lambda self: FontInfoPropertyProxy(self, "trademarks"))
'''
	.. attribute:: trademarks

		This accesses all localized trademark values.
		For details :attr:`GSFont.properties`

		:type: dict

		.. code-block:: python
			font.trademarks["ENG"] = "ThisFont is a trademark by MyFoundry.com"

		.. versionadded:: 3.0.3
'''

GSFont.designerURL = property(
	lambda self: self.defaultPropertyForName_("designerURL"),
	lambda self, value: self.setProperty_value_languageTag_("designerURL", value, None)
)
'''
	.. attribute:: designerURL

		:type: str
'''

GSFont.manufacturer = property(
	lambda self: self.defaultPropertyForName_("manufacturers"),
	lambda self, value: self.setProperty_value_languageTag_("manufacturers", value, None)
)
'''
	.. attribute:: manufacturer

		This accesses the default value only. The localizations can be accessed by :attr:`GSFont.properties`

		:type: str
'''

GSFont.manufacturers = property(lambda self: FontInfoPropertyProxy(self, "manufacturers"))
'''
	.. attribute:: manufacturers

		This accesses all localized manufacturer values.
		For details :attr:`GSFont.properties`

		:type: dict

		.. code-block:: python
			font.manufacturers["ENG"] = "My English Corporation"

		.. versionadded:: 3.0.3
'''

GSFont.manufacturerURL = property(
	lambda self: self.defaultPropertyForName_("manufacturerURL"),
	lambda self, value: self.setProperty_value_languageTag_("manufacturerURL", value, None)
)
'''
	.. attribute:: manufacturerURL

		:type: str
'''

GSFont.versionMajor = property(
	lambda self: self.pyobjc_instanceMethods.versionMajor(),
	lambda self, value: self.setVersionMajor_(value)
)
'''
	.. attribute:: versionMajor

		:type: int
'''

GSFont.versionMinor = property(
	lambda self: self.pyobjc_instanceMethods.versionMinor(),
	lambda self, value: self.setVersionMinor_(value)
)
'''
	.. attribute:: versionMinor

		:type: int
'''


def __GSFont_get_date__(self):
	return datetime.datetime.fromtimestamp(self.pyobjc_instanceMethods.date().timeIntervalSince1970())


def __GSFont_set_date__(self, date):
	if isinstance(date, datetime.datetime):
		self.setDate_(NSDate.alloc().initWithTimeIntervalSince1970_(time.mktime(date.timetuple())))
	elif isinstance(date, (int, float)):
		self.setDate_(NSDate.alloc().initWithTimeIntervalSince1970_(date))
	elif isinstance(date, NSDate):
		self.setDate_(date)
	else:
		raise TypeError("date must be a datetime object, NSDate object, int or float, not %s" % type(date).__name__)


GSFont.date = property(
	lambda self: __GSFont_get_date__(self),
	lambda self, value: __GSFont_set_date__(self, value)
)
'''
	.. attribute:: date

		:type: datetime.datetime

		.. code-block:: python
			print(font.date)
			>> 2015-06-08 09:39:05

			# set date to now
			font.date = datetime.datetime.now()
			# using NSDate
			font.date = NSDate.date()
			# or in seconds since Epoch
			font.date = time.time()
'''

GSFont.familyName = property(
	lambda self: self.pyobjc_instanceMethods.fontName(),
	lambda self, value: self.setFontName_(value)
)

GSFont.fontName = property(
	lambda self: self.pyobjc_instanceMethods.fontName(),
	lambda self, value: self.setFontName_(value)
)
'''
	.. attribute:: familyName

		Family name of the typeface.

		:type: str
'''

GSFont.familyNames = property(lambda self: FontInfoPropertyProxy(self, "familyNames"))
'''
	.. attribute:: familyNames

		This accesses all localized family name values.
		For details :attr:`GSFont.properties`

		:type: dict
		.. code-block:: python
			font.familyNames["ENG"] = "MyFamilyName"

		.. versionadded:: 3.0.3
'''

GSFont.upm = property(
	lambda self: self.unitsPerEm(),
	lambda self, value: self.setUnitsPerEm_(value)
)
'''
	.. attribute:: upm

		Units per Em

		:type: int
'''

GSFont.note = property(
	lambda self: self.pyobjc_instanceMethods.note(),
	lambda self, value: self.setNote_(value)
)
'''
	.. attribute:: note

		:type: str
'''

GSFont.kerningLTR = property(
	lambda self: self.pyobjc_instanceMethods.kerningLTR(),
	lambda self, value: self.setKerningLTR_(value)
)
GSFont.kerning = GSFont.kerningLTR
'''
	.. attribute:: kerning

		Kerning for LTR writing
		A multi-level dictionary. The first level’s key is the :attr:`GSFontMaster.id` (each master has its own kerning), the second level’s key is the :attr:`GSGlyph.id` or class id (@MMK_L_XX) of the first glyph, the third level’s key is a glyph id or class id (@MMK_R_XX) for the second glyph. The values are the actual kerning values.

		To set a value, it is better to use the method :meth:`GSFont.setKerningForPair()`. This ensures a better data integrity (and is faster).

		:type: dict
'''

GSFont.kerningRTL = property(
	lambda self: self.pyobjc_instanceMethods.kerningRTL(),
	lambda self, value: self.setKerningRTL_(value)
)
'''
	.. attribute:: kerningRTL

		Kerning for RTL writing
		A multi-level dictionary. The first level’s key is the :attr:`GSFontMaster.id` (each master has its own kerning), the second level’s key is the :attr:`GSGlyph.id` or class id (@MMK_L_XX) of the first glyph, the third level’s key is a glyph id or class id (@MMK_R_XX) for the second glyph. The values are the actual kerning values.

		To set a value, it is better to use the method :meth:`GSFont.setKerningForPair()`. This ensures a better data integrity (and is faster).

		:type: dict
'''

GSFont.kerningVertical = property(
	lambda self: self.pyobjc_instanceMethods.kerningVertical(),
	lambda self, value: self.setKerningVertical_(value)
)
'''
	.. attribute:: kerningVertical

		Kerning for vertical writing
		A multi-level dictionary. The first level’s key is the :attr:`GSFontMaster.id` (each master has its own kerning), the second level’s key is the :attr:`GSGlyph.id` or class id (@MMK_L_XX) of the first glyph, the third level’s key is a glyph id or class id (@MMK_R_XX) for the second glyph. The values are the actual kerning values.

		To set a value, it is better to use the method :meth:`GSFont.setKerningForPair()`. This ensures a better data integrity (and is faster).

		:type: dict
'''

GSFont.userData = property(
	lambda self: UserDataProxy(self),
	lambda self, value: UserDataProxy(self).setter(value)
)
add_type(GSFont, "userData", dict)
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

GSFont.tempData = property(
	lambda self: TempDataProxy(self),
	lambda self, value: TempDataProxy(self).setter(value)
)
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

GSFont.disablesNiceNames = property(
	lambda self: bool(self.pyobjc_instanceMethods.disablesNiceNames()),
	lambda self, value: self.setDisablesNiceNames_(value)
)
'''
	.. attribute:: disablesNiceNames

		Corresponds to the “Don't use nice names” setting from the Font Info dialog.

		:type: bool
'''

GSFont.customParameters = property(
	lambda self: CustomParametersProxy(self),
	lambda self, value: CustomParametersProxy(self).setter(value)
)
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

			# add multiple parameters:
			parameter = GSCustomParameter("Name Table Entry", "1 1;"font name")
			font.customParameters.append(parameter)
			parameter = GSCustomParameter("Name Table Entry", "2 1;"style name")
			font.customParameters.append(parameter)

			# delete a parameter
			del font.customParameters['glyphOrder']

'''
GSFont.grid = property(
	lambda self: self.pyobjc_instanceMethods.gridMain(),
	lambda self, value: self.setGridMain_(value)
)
'''
	.. attribute:: grid

		Corresponds to the “Grid spacing” setting from the Info dialog.

		:type: int
'''

GSFont.gridSubDivisions = property(
	lambda self: self.pyobjc_instanceMethods.gridSubDivision(),
	lambda self, value: self.setGridSubDivision_(value)
)

GSFont.gridSubDivision = property(
	lambda self: self.pyobjc_instanceMethods.gridSubDivision(),
	lambda self, value: self.setGridSubDivision_(value)
)
'''
	.. attribute:: gridSubDivision

		Corresponds to the “Grid sub divisions” setting from the Info dialog.

		:type: int
'''

GSFont.gridLength = property(lambda self: self.pyobjc_instanceMethods.gridLength())
'''
	.. attribute:: gridLength

		Ready calculated size of grid for rounding purposes. Result of division of grid with gridSubDivisions.

		:type: float (readonly)
'''

GSFont.disablesAutomaticAlignment = property(
	lambda self: bool(self.pyobjc_instanceMethods.disablesAutomaticAlignment()),
	lambda self, value: self.setDisablesAutomaticAlignment_(value)
)
'''
	.. attribute:: disablesAutomaticAlignment

		:type: bool
'''

GSFont.keyboardIncrement = property(
	lambda self: self.pyobjc_instanceMethods.keyboardIncrement(),
	lambda self, value: self.setKeyboardIncrement_(value)
)
'''
	.. attribute:: keyboardIncrement

		Distance of movement by arrow keys. Default:1

		:type: float
'''

GSFont.keyboardIncrementBig = property(
	lambda self: self.pyobjc_instanceMethods.keyboardIncrementBig(),
	lambda self, value: self.setKeyboardIncrementBig_(value)
)
'''
	.. attribute:: keyboardIncrementBig

		Distance of movement by arrow plus Shift key. Default:10

		:type: float

		.. versionadded:: 3.0
'''

GSFont.keyboardIncrementHuge = property(
	lambda self: self.pyobjc_instanceMethods.keyboardIncrementHuge(),
	lambda self, value: self.setKeyboardIncrementHuge_(value)
)
'''
	.. attribute:: keyboardIncrementHuge

		Distance of movement by arrow plus Command key. Default:100

		:type: float

		.. versionadded:: 3.0
'''

GSFont.snapToObjects = property(
	lambda self: bool(self.pyobjc_instanceMethods.snapToObjects()),
	lambda self, value: self.setSnapToObjects_(value)
)
'''
	.. attribute:: snapToObjects

		disable snapping to nodes and background

		:type: bool

		.. versionadded:: 3.0.1
'''

GSFont.previewRemoveOverlap = property(
	lambda self: bool(self.pyobjc_instanceMethods.previewRemoveOverlap()),
	lambda self, value: self.setPreviewRemoveOverlap_(value)
)
'''
	.. attribute:: previewRemoveOverlap

		disable preview remove overlap

		:type: bool

		.. versionadded:: 3.0.1
'''


def __GSFont_getSelectedGlyphs__(self):
	try:
		return self.parent.windowController().glyphsController().selectedObjects()
	except:
		return None


def __GSFont_setSelectedGlyphs__(self, value):
	if not isinstance(value, (list, tuple, NSArray)):
		raise TypeError('Argument needs to be a list, not %s' % type(value).__name__)
	try:
		self.parent.windowController().glyphsController().setSelectedObjects_(value)
	except:
		pass


GSFont.selection = property(
	lambda self: __GSFont_getSelectedGlyphs__(self),
	lambda self, value: __GSFont_setSelectedGlyphs__(self, value)
)
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

GSFont.masterIndex = property(
	lambda self: self.parent.windowController().masterIndex(),
	lambda self, value: self.parent.windowController().setMasterIndex_(value)
)
'''
	.. attribute:: masterIndex

		Returns the index of the active master (selected in the toolbar).

		:type: int
'''


def __GSFont_current_Text__(self):
	try:
		return self.parent.windowController().activeEditViewController().graphicView().displayString_(GSFormatVersionCurrent)
	except:
		pass
	return None


def __GSFont_set_current_Text__(self, string):
	self.parent.windowController().activeEditViewController().graphicView().setDisplayString_(string)


GSFont.currentText = property(
	lambda self: __GSFont_current_Text__(self),
	lambda self, value: __GSFont_set_current_Text__(self, value)
)
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


GSFont.currentTab = property(
	lambda self: __GSFont__currentTab__(self),
	lambda self, value: __GSFont__set_currentTab__(self, value)
)
'''
	.. attribute:: currentTab

		Active Edit view tab.

		:type: :class:`GSEditViewController`
'''


def __GSFont_filepath__(self):
	if self.parent is not None and self.parent.fileURL() is not None:
		return self.parent.fileURL().path()
	else:
		return self.tempData["filePath"]


GSFont.filepath = property(lambda self: __GSFont_filepath__(self))
'''
	.. attribute:: filepath

		On-disk location of GSFont object.

		:type: str
'''

GSFont.toolIndex = property(
	lambda self: self.parent.windowController().selectedToolGroupIndex()
)

toolClassAbbreviations = {  # abbreviation : className
	"SelectTool": "GlyphsToolSelect",
	"DrawTool": "GlyphsToolDraw",
	"KnifeTool": "GlyphsToolKnife",
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

toolClassAbbreviationsReverse = dict((v, k) for k, v in toolClassAbbreviations.items())


def __GSFont_tool__(self):
	tool = Glyphs.font.parent.windowController().toolEventDelegate()
	if isinstance(tool, GSToolGroup):
		tool = tool.currentTool()

	toolClassName = tool.className()
	if toolClassName in toolClassAbbreviationsReverse:
		toolClassName = toolClassAbbreviationsReverse[toolClassName]
	return toolClassName


def __GSFont_setTool__(self, toolName):
	if toolName in toolClassAbbreviations:
		toolName = toolClassAbbreviations[toolName]
	toolClass = NSClassFromString(toolName)

	if toolClass:
		self.parent.windowController().setToolForClass_(toolClass)
	else:
		sys.stderr.write('No tool found by the name "%s"' % (toolName))


GSFont.tool = property(
	lambda self: __GSFont_tool__(self),
	lambda self, value: __GSFont_setTool__(self, value)
)
'''
	.. attribute:: tool

		Name of tool selected in toolbar.

		For available names including third-party plug-ins that come in the form of selectable tools, see `GSFont.tools` below.

		:type: str

		.. code-block:: python
			font.tool = 'SelectTool' # Built-in tool
			font.tool = 'GlyphsAppSpeedPunkTool' # Third party plug-in
'''


def __GSFont_toolsList__(self):
	tools = []
	for tool in self.parent.windowController().toolInstances():
		toolClassName = tool.className()
		if toolClassName in toolClassAbbreviationsReverse:
			toolClassName = toolClassAbbreviationsReverse[toolClassName]
		tools.append(toolClassName)
	return tools


GSFont.tools = property(lambda self: __GSFont_toolsList__(self))
'''
	.. attribute:: tools

		Returns a list of available tool names, including third-party plug-ins.

		:type: list, str
'''

GSFont.appVersion = property(lambda self: self.pyobjc_instanceMethods.appVersion())
'''
	.. attribute:: appVersion

		Returns the version that the file was last saved

		.. versionadded:: 2.5
'''

GSFont.formatVersion = property(
	lambda self: self.pyobjc_instanceMethods.formatVersion(),
	lambda self, value: self.setFormatVersion_(value)
)
'''
	.. attribute:: formatVersion

		The file-format the font should be written. possible values are '2' and '3'.
		You can use :ref:`file-format-versions`

		:type: int

		.. versionadded:: 3
'''
GSFont.displayStrings = property(lambda self: list(self.pyobjc_instanceMethods.displayStrings()))

'''
	**Functions**

	.. function:: copy()

		Returns a full copy of the font

'''


def _checkReturnValue(result):
	if result is not None and len(result) == 2 and result[0] is False:
		error = result[1]
		if error.localizedRecoverySuggestion():
			return error.localizedRecoverySuggestion()
		elif error.localizedFailureReason():
			return error.localizedFailureReason()
		else:
			return error.localizedDescription()
	return None


def __GSFont__save__(self, path: str | None = None, formatVersion: int | None = None, makeCopy: bool | None = False) -> None:
	if self.parent is not None and not makeCopy:  # save via NSDocument. Will change the file path of the doc
		if path is None:
			self.parent.saveDocument_(None)
			return
		if path.endswith('.glyphs'):
			typeName = "com.schriftgestaltung.glyphs"
		elif path.endswith('.glyphspackage'):
			typeName = "com.glyphsapp.glyphspackage"
		elif path.endswith('.ufo'):
			typeName = "org.unifiedfontobject.ufo"
		else:
			raise ValueError("Save file must have file extension .glyphs, .glyphspackage or .ufo")
		URL = NSURL.fileURLWithPath_(path)
		result = self.parent.saveToURL_ofType_forSaveOperation_error_(URL, typeName, 1, objc.nil)
		return

	if path is None:
		path = self.filePath

	if path is None:
		raise ValueError("No path set")

	if path.endswith('.ufo'):  # export as ufo
		GlyphsFileFormatUFO = objc.lookUpClass("GlyphsFileFormatUFO")
		ufoWriter = GlyphsFileFormatUFO.new()
		URL = NSURL.fileURLWithPath_(path)
		result = ufoWriter.writeFont_toURL_error_(self, URL, None)

	else:  # export as glyphs file
		if path.endswith('.glyphs'):
			typeId = GSPackageFlatFile
		elif path.endswith('.glyphspackage'):
			typeId = GSPackageBundle
		else:
			raise ValueError("Save file path must have file extension .glyphs, .glyphspackage or .ufo")

		if formatVersion is None:
			formatVersion = self.formatVersion
		URL = NSURL.fileURLWithPath_(path)
		self.tempData["filePath"] = path  # GSFontFilePathKey
		result = self.saveToURL_type_format_error_(URL, typeId, formatVersion, None)
		self.tempData["filePath"] = None  # GSFontFilePathKey

	if result is not None:
		result = _checkReturnValue(result)
		if result is not None:
			raise ValueError(result)


GSFont.save = python_method(__GSFont__save__)
'''
	.. function:: save([path=None, formatVersion=3, makeCopy=False])

		Saves the font.

		If no path is given, it saves to the existing location.

		:param path: (Optional) file path including filename and suffix. When the font is loaded directly (`GSFont(path)`), the path argument is required.
		:type path: str
		:param formatVersion: The format of the file. Requires `makeCopy=True`
		:type formatVersion: int
		:param makeCopy: saves a new file without changing the documents file paths. So it always need a `path` argument
		:type makeCopy: bool
'''


def __GSFont__close__(self, ignoreChanges: bool | None = True) -> None:
	if self.parent:
		if ignoreChanges:
			self.parent.close()
		else:
			self.parent.canCloseDocumentWithDelegate_shouldCloseSelector_contextInfo_(None, None, None)


GSFont.close = python_method(__GSFont__close__)
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


def __GSFont__show__(self) -> None:
	if self not in Glyphs.fonts:
		Glyphs.fonts.append(self)
	else:
		self.parent.windowController().showWindow_(None)


GSFont.show = python_method(__GSFont__show__)
'''
	.. function:: show()

		Makes font visible in the application, either by bringing an already open font window to the front or by appending a formerly invisible font object (such as the result of a `copy()` operation) as a window to the application.

		.. versionadded:: 2.4.1
'''


def __GSFont_kerningForPair__(self: GSFont, FontMasterID: str, LeftKerningId: str, RightKerningId: str, direction: int = GSLTR) -> float | None:
	# ... implementation ...
	# Convert LeftKerningId/RightKerningId from glyph name to ID if not a group key
	actual_left_id: str
	if not LeftKerningId.startswith('@'):
		glyph_l: GSGlyph | None = self.glyphs.get(LeftKerningId)  # type: ignore
		if glyph_l is None:
			raise KeyError(f"Glyph {LeftKerningId} not found")
		actual_left_id = glyph_l.id  # type: ignore
	else:
		actual_left_id = LeftKerningId

	actual_right_id: str
	if not RightKerningId.startswith('@'):
		glyph_r: GSGlyph | None = self.glyphs.get(RightKerningId)  # type: ignore
		if glyph_r is None:
			raise KeyError(f"Glyph {RightKerningId} not found")
		actual_right_id = glyph_r.id  # type: ignore
	else:
		actual_right_id = RightKerningId

	value: float = self.kerningForFontMasterID_leftKey_rightKey_direction_(FontMasterID, actual_left_id, actual_right_id, direction)  # type: ignore
	if value > 1000000:  # GS convention for NSNotFound like value
		return None
	return value
GSFont.kerningForPair = python_method(__GSFont_kerningForPair__)  # type: ignore


'''
	.. function:: kerningForPair(fontMasterId, leftKey, rightKey [, direction=LTR])

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
			>> -15.0

			# print(kerning between group T and group A for currently selected master)
			# ('L' = left side of the pair and 'R' = left side of the pair)
			font.kerningForPair(font.selectedFontMaster.id, '@MMK_L_T', '@MMK_R_A')
			>> -75.0

			# in the same font, kerning between T and A would be zero, because they use group kerning instead.
			font.kerningForPair(font.selectedFontMaster.id, 'T', 'A')
			>> None
'''


def __GSFont_setKerningForPair__(self, FontMasterID: str, LeftKerningId: str, RightKerningId: str, Value: float, direction: int | None = GSLTR):
	if not LeftKerningId[0] == '@':
		glyph = self.glyphs[LeftKerningId]
		if glyph is not None:
			LeftKerningId = glyph.id
		else:
			raise KeyError("Glyphs with name: %s not found" % LeftKerningId)
	if not RightKerningId[0] == '@':
		glyph = self.glyphs[RightKerningId]
		if glyph is not None:
			RightKerningId = glyph.id
		else:
			raise KeyError("Glyphs with name: %s not found" % RightKerningId)
	self.setKerningForFontMasterID_leftKey_rightKey_value_direction_(FontMasterID, LeftKerningId, RightKerningId, Value, direction)


GSFont.setKerningForPair = python_method(__GSFont_setKerningForPair__)
'''
	.. function:: setKerningForPair(fontMasterId, leftKey, rightKey, value [, direction=GSLTR])

		This sets the kerning for the two specified glyphs (leftKey or rightKey is the glyph name) or a kerning group key (@MMK_X_XX).

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


def removeKerningForPair(self, fontMasterID: str, leftKerningId: str, rightKerningId: str, direction: int | None = GSLTR):
	if not leftKerningId[0] == '@':
		glyph = self.glyphs[leftKerningId]
		if glyph is not None:
			leftKerningId = glyph.id
		else:
			raise KeyError("Glyphs with name: %s not found" % leftKerningId)
	if not rightKerningId[0] == '@':
		glyph = self.glyphs[rightKerningId]
		if glyph is not None:
			rightKerningId = glyph.id
		else:
			raise KeyError("Glyphs with name: %s not found" % rightKerningId)
	self.removeKerningForFontMasterID_leftKey_rightKey_direction_(fontMasterID, leftKerningId, rightKerningId, direction)


GSFont.removeKerningForPair = python_method(removeKerningForPair)
'''
	.. function:: removeKerningForPair(fontMasterId, leftKey, rightKey, direction=GSLTR)

		Removes the kerning for the two specified glyphs (LeftKey or RightKey is the glyph name) or a kerning group key (@MMK_X_XX).

		:param FontMasterId: The id of the FontMaster
		:type FontMasterId: str
		:param leftKey: either a glyph name or a class name
		:type leftKey: str
		:param rightKey: either a glyph name or a class name
		:type rightKey: str
		:param direction: optional writing direction (see Constants; 'GSLTR' (0) or 'GSVertical'). Default is GSLTR. (added in 2.6.6)
		:type direction: int

		.. code-block:: python
			# remove kerning for group T and group A for all masters
			# ('L' = left side of the pair and 'R' = left side of the pair)
			for master in font.masters:
			    font.removeKerningForPair(master.id, '@MMK_L_T', '@MMK_R_A')
'''


def __GSFont__addTab__(self, tabText: str | None = "") -> GSEditViewController | None:
	if self.parent:
		if isString(tabText):
			return self.parent.windowController().addTabWithDisplayString_(tabText)
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

'''

	.. function:: export([format, instances, fontPath, autoHint, removeOverlap, useSubroutines, useProductionNames, containers, decomposeSmartStuff)

		exports the font

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


def ____GSAxis____(): pass


'''
:mod:`GSAxis`
===============================================================================

Implementation of the axis object.

.. class:: GSAxis()

	Properties

		* :attr:`name`
		* :attr:`axisTag`
		* :attr:`id`
		* :attr:`hidden`
		* :attr:`font`

	**Properties**
'''

GSAxis.__new__ = staticmethod(__GSObject__new__)
GSAxis.__init__ = python_method(__empty__init__)
GSAxis.__copy__ = python_method(__GSObject__copy__)
GSAxis.__deepcopy__ = python_method(__GSObject__copy__)

GSAxis.font = property(lambda self: self.pyobjc_instanceMethods.parent())
add_type(GSAxis, "font", GSFont)
'''
	.. attribute:: font

		Reference to the :class:`GSFont` object that contains the axis. Normally that is set by the app.

		:type: GSFont
'''

GSAxis.name = property(
	lambda self: self.pyobjc_instanceMethods.name(),
	lambda self, value: self.setName_(value)
)
add_type(GSAxis, "name", str)
'''
	.. attribute:: name

		The name of the axis

		:type: str
'''

GSAxis.axisTag = property(
	lambda self: self.pyobjc_instanceMethods.axisTag(),
	lambda self, value: self.setAxisTag_(value)
)
add_type(GSAxis, "axisTag", str)
'''
	.. attribute:: axisTag

		The axisTag. this is a four letter string. see `OpenType Design-Variation Axis Tag Registry <https://docs.microsoft.com/en-us/typography/opentype/spec/dvaraxisreg>`_.

		:type: str
'''

GSAxis.axisId = property(
	lambda self: self.pyobjc_instanceMethods.axisId(),
	lambda self, value: self.setAxisId_(value)
)
add_type(GSAxis, "axisId", str)
GSAxis.id = property(
	lambda self: self.pyobjc_instanceMethods.axisId(),
	lambda self, value: self.setAxisId_(value)
)
add_type(GSAxis, "id", str)
'''
	.. attribute:: id

		The id to link the values in the masters

		:type: str
'''

GSAxis.hidden = property(
	lambda self: bool(self.pyobjc_instanceMethods.hidden()),
	lambda self, value: self.setHidden_(value)
)
add_type(GSAxis, "hidden", bool)
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


def ____GSMetric____(): pass


'''
:mod:`GSMetric`
===============================================================================

Implementation of the metric object. It is used to link the metrics and stems in the masters.

.. class:: GSMetric()

	Properties

		* :attr:`font`
		* :attr:`name`
		* :attr:`id`
		* :attr:`title`
		* :attr:`filter`
		* :attr:`type`
		* :attr:`horizontal`

	**Properties**
'''

GSMetric.__new__ = staticmethod(__GSObject__new__)
GSMetric.__init__ = python_method(__empty__init__)
GSMetric.__copy__ = python_method(__GSObject__copy__)
GSMetric.__deepcopy__ = python_method(__GSObject__copy__)

GSMetric.font = property(lambda self: self.pyobjc_instanceMethods.font())
'''
	.. attribute:: font

		Reference to the :class:`GSFont` object that contains the metric. Normally that is set by the app.

		:type: GSFont
'''

GSMetric.name = property(
	lambda self: self.pyobjc_instanceMethods.name(),
	lambda self, value: self.setName_(value)
)
add_type(GSMetric, "name", str)
'''
	.. attribute:: name

		The name of the metric or stem

		:type: str
'''

GSMetric.id = property(lambda self: self.pyobjc_instanceMethods.id())
add_type(GSMetric, "id", str)
'''
	.. attribute:: id

		The id to link the values in the masters

		:type: str
'''

GSMetric.title = property(lambda self: self.pyobjc_instanceMethods.title())
'''
	.. attribute:: title

		The title as shown in the UI. It is readonly as it is computed by the name, type and filter.

		:type: str
'''

GSMetric.type = property(
	lambda self: self.pyobjc_instanceMethods.type(),
	lambda self, value: self.setType_(value)
)
'''
	.. attribute:: type

		The metrics type

		:type: int
'''

GSMetric.filter = property(
	lambda self: self.pyobjc_instanceMethods.filter(),
	lambda self, value: self.setFilter_(value)
)
'''
	.. attribute:: filter

		A filter to limit the scope of the metric.

		:type: NSPredicate
'''
GSMetric.horizontal = property(
	lambda self: bool(self.pyobjc_instanceMethods.horizontal()),
	lambda self, value: self.setHorizontal_(value)
)
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


def ____GSFontMaster____(): pass


'''
:mod:`GSFontMaster`
===============================================================================

Implementation of the master object. This corresponds with the "Masters" pane in the Font Info. In Glyphs.app, the glyphs of each master are reachable not here, but as :class:`layers <GSLayer>` attached to the :class:`glyphs <GSGlyph>` attached to the :class:`font <GSFont>` object. See the infographic on top for better understanding.

.. class:: GSFontMaster()
'''

GSFontMaster.__new__ = staticmethod(__GSObject__new__)
GSFontMaster.__init__ = python_method(__empty__init__)


def __GSFontMaster__str__(self):
	return "<GSFontMaster \"%s\" %s (%s)>" % (self.name, str(self.axes).replace("\n", "").replace("\t", ""), self.id)


GSFontMaster.__str__ = python_method(__GSFontMaster__str__)

GSFontMaster.mutableCopyWithZone_ = __GSObject__copy__
GSFontMaster.__copy__ = python_method(__GSObject__copy__)
GSFontMaster.__deepcopy__ = python_method(__GSObject__copy__)
'''

		* :attr:`id`
		* :attr:`name`
		* :attr:`internalAxesValues`
		* :attr:`externalAxesValues`
		* :attr:`properties`
		* :attr:`metrics`
		* :attr:`ascender`
		* :attr:`capHeight`
		* :attr:`xHeight`
		* :attr:`descender`
		* :attr:`italicAngle`
		* :attr:`alignmentZones`
		* :attr:`blueValues`
		* :attr:`otherBlues`
		* :attr:`guides`
		* :attr:`stems`
		* :attr:`numbers`
		* :attr:`userData`
		* :attr:`customParameters`
		* :attr:`font`
		* :attr:`iconName`

	Functions

		* :meth:`copy()`

	**Properties**
'''
GSFontMaster.id = property(
	GSFontMaster.instanceMethodForSelector_(NSSelectorFromString("id")),
	lambda self, value: self.setId_(value)
)
'''
	.. attribute:: id

		Used to identify :class:`Layers` in the Glyph

		see :attr:`GSGlyph.layers`

		:type: str

		.. code-block:: python
			# ID of first master
			print(font.masters[0].id)
			>> 3B85FBE0-2D2B-4203-8F3D-7112D42D745E

			# use this master to access the glyph’s corresponding layer
			print(glyph.layers[font.masters[0].id])
			>> <GSLayer "Light" (A)>
'''

GSFontMaster.font = property(
	lambda self: self.pyobjc_instanceMethods.font(),
	lambda self, value: self.setFont_(value)
)
'''
	.. attribute:: font

		Reference to the :class:`GSFont` object that contains the master. Normally that is set by the app, only if the instance is not actually added to the font, then set this manually.

		:type: GSFont

		.. versionadded:: 2.5.2
'''

GSFontMaster.name = property(
	lambda self: self.pyobjc_instanceMethods.name(),
	lambda self, value: self.setName_(value)
)
'''
	.. attribute:: name

		The human-readable identification of the master, e.g., "Bold Condensed".

		:type: str
'''

GSFontMaster.iconName = property(
	lambda self: self.pyobjc_instanceMethods.iconName(),
	lambda self, value: self.setIconName_(value)
)
'''
	.. attribute:: iconName

		The name of the icon

		:type: str
'''

GSFontMaster.axes = property(
	lambda self: InternalAxesProxy(self),
	lambda self, value: InternalAxesProxy(self).setter(value)
)
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
		.. deprecated:: 3.2
'''

GSFontMaster.internalAxesValues = property(
	lambda self: InternalAxesProxy(self),
	lambda self, value: InternalAxesProxy(self).setter(value)
)
'''
	.. attribute:: internalAxesValues

		List of floats specifying the positions for each axis

		:type: list

		.. code-block:: python
			# setting a value for a specific axis
			master.internalAxesValues[2] = 12
			# or more precisely
			master.internalAxesValues[axis.axisId] = 12
			# setting all values at once
			master.internalAxesValues = [100, 12, 3.5]

		.. versionadded:: 3.2
'''

GSFontMaster.externalAxesValues = property(
	lambda self: ExternalAxesProxy(self),
	lambda self, value: ExternalAxesProxy(self).setter(value)
)
'''
	.. attribute:: externalAxesValues

		List of floats specifying the positions for each axis for the user facing values

		:type: list

		.. code-block:: python
			# setting a value for a specific axis
			master.externalAxesValues[2] = 12
			# or more precisely
			master.externalAxesValues[axis.axisId] = 12
			# setting all values at once
			master.externalAxesValues = [100, 12, 3.5]

		.. versionadded:: 3.2
'''

GSFontMaster.properties = property(
	lambda self: PropertiesProxy(self),
	lambda self, values: PropertiesProxy(self).setter(values)
)
add_type(GSFontMaster, 'properties', list[GSInfoValueSingle | GSInfoValueLocalized])
'''
	.. attribute:: properties

		Holds the fonts info properties. Can be instances of :class:`GSInfoValueSingle` and :class:`GSInfoValueLocalized`

		The localized values use language tags defined in the middle column of `Language System Tags table`: <https://docs.microsoft.com/en-us/typography/opentype/spec/languagetags>.

		To find specific values, use master.propertyForName_(name) or master.propertyForName_languageTag_(name, languageTag).

		:type: list

		.. versionadded:: 3
'''


GSFontMaster.metrics = property(
	lambda self: MasterMetricsProxy(self),
	lambda self, values: MasterMetricsProxy(self).setter(values)
)


GSFontMaster.metricValues = property(lambda self: self.pyobjc_instanceMethods.metricValues())  # fallback for G3 scripts
'''
	.. attribute:: metrics

		a dict of all :class:`GSMetricStore` objects. Keys are font.metrics[].id

		:type: dict

		.. code-block:: python
			for metric in Font.metrics:
			    if metric.type == GSMetricsTypexHeight and metric.filter is None:
			        metricValue = master.metrics[metric.id]
			        metricValue.position = 543
			        metricValue.overshoot = 17

		.. versionadded:: 3
'''

GSFontMaster.ascender = property(
	lambda self: int(self.defaultAscender()),
	lambda self, value: self.setDefaultAscender_(value)
)
'''
	.. attribute:: ascender

		This is the default ascender of the master. There might be other values that are for specific glyphs. See :attr:`master.metrics <GSFontMaster.metrics>` and :attr:`layer.metrics <GSLayer.metrics>`

		:type: float
'''

GSFontMaster.capHeight = property(
	lambda self: int(self.defaultCapHeight()),
	lambda self, value: self.setDefaultCapHeight_(value)
)
'''
	.. attribute:: capHeight

		This is the default capHeight of the master. There might be other values that are for specific glyphs. See :attr:`master.metrics <GSFontMaster.metrics>` and :attr:`layer.metrics <GSLayer.metrics>`

		:type: float
'''

GSFontMaster.xHeight = property(
	lambda self: int(self.defaultXHeight()),
	lambda self, value: self.setDefaultXHeight_(value)
)
'''
	.. attribute:: xHeight

		This is the default xHeight of the master. There might be other values that are for specific glyphs. See :attr:`master.metrics <GSFontMaster.metrics>` and :attr:`layer.metrics <GSLayer.metrics>`

		:type: float
'''

GSFontMaster.descender = property(
	lambda self: int(self.defaultDescender()),
	lambda self, value: self.setDefaultDescender_(value)
)
'''
	.. attribute:: descender

		This is the default descender of the master. There might be other values that are for specific glyphs. See :attr:`master.metrics <GSFontMaster.metrics>` and :attr:`layer.metrics <GSLayer.metrics>`

		:type: float
'''

GSFontMaster.italicAngle = property(
	lambda self: self.defaultItalicAngle(),
	lambda self, value: self.setDefaultItalicAngle_(value)
)
'''
	.. attribute:: italicAngle

		:type: float
'''

GSFontMaster.stems = property(
	lambda self: MasterStemsProxy(self),
	lambda self, value: MasterStemsProxy(self).setter(value)
)
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

GSFontMaster.numbers = property(
	lambda self: MasterNumbersValuesProxy(self),
	lambda self, value: MasterNumbersValuesProxy(self).setter(value)
)
'''
	.. attribute:: numbers

		The numbers. This is a list of numbers.

		:type: list

		.. code-block:: python

			font.masters[0].numbers = [10, 11, 20]

			print(master.numbers[0])

			master.numbers[0] = 12

			master.numbers["numberName"] = 12

	.. versionadded:: 3.1
'''

GSFontMaster.alignmentZones = property(lambda self: tuple(self.defaultAlignmentZones()))
'''
	.. attribute:: alignmentZones

		Collection of :class:`GSAlignmentZone` objects. Read-only.

		:type: list
'''


def __GSFontMaster_blueValues__(self):
	return GSGlyphsInfo.blueValues_(self.alignmentZones)


GSFontMaster.blueValues = property(lambda self: __GSFontMaster_blueValues__(self))
add_type(GSFontMaster, "blueValues", list[int])
'''
	.. attribute:: blueValues

		PS hinting Blue Values calculated from the master’s alignment zones. Read-only.

		:type: list
'''


def __GSFontMaster_otherBlues__(self):
	return GSGlyphsInfo.otherBlues_(self.alignmentZones)


GSFontMaster.otherBlues = property(
	lambda self: __GSFontMaster_otherBlues__(self)
)
add_type(GSFontMaster, "otherBlues", list[int])
'''
	.. attribute:: otherBlues

		PS hinting Other Blues calculated from the master’s alignment zones. Read-only.

		:type: list
'''

GSFontMaster.guides = property(
	lambda self: LayerGuidesProxy(self),
	lambda self, value: LayerGuidesProxy(self).setter(value)
)
add_type(GSFontMaster, "guides", list[GSGuide])
# keep for compatibility
GSFontMaster.guideLines = GSFontMaster.guides
add_type(GSFontMaster, "guideLines", list[GSGuide])
'''
	.. attribute:: guides

		Collection of :class:`GSGuide` objects. These are the font-wide (actually master-wide) red guidelines. For glyph-level guidelines (attached to the layers) see :attr:`GSLayer.guides`

		:type: list
'''

GSFontMaster.userData = property(
	lambda self: UserDataProxy(self),
	lambda self, value: UserDataProxy(self).setter(value)
)
add_type(GSFontMaster, "userData", dict)
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

GSFontMaster.customParameters = property(
	lambda self: CustomParametersProxy(self),
	lambda self, value: CustomParametersProxy(self).setter(value)
)
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

			# add multiple parameters:
			parameter = GSCustomParameter("CJK Guide", 10)
			font.customParameters.append(parameter)
			parameter = GSCustomParameter("CJK Guide", 20)
			font.customParameters.append(parameter)

			# delete a parameter
			del font.masters[0].customParameters['underlinePosition']

	**Functions**

	.. function:: copy()

		Returns a full copy of the master

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

GSElement.selected = property(
	lambda self: __ObjectInLayer_selected__(self),
	lambda self, value: __SetObjectInLayer_selected__(self, value)
)
add_type(GSElement, "selected", bool)

GSElement.orientation = property(
	lambda self: self.pyobjc_instanceMethods.orientation(),
	lambda self, value: self.setOrientation_(validateNumber(value))
)


##################################################################################
#
#
#
#           GSAlignmentZone
#
#
#
##################################################################################


def ____GSAlignmentZone____(): pass


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

GSAlignmentZone.__new__ = staticmethod(__GSObject__new__)


def __GSAlignmentZone__init__(self, pos: float = 0, size: float = 20):
	self.setPosition_(pos)
	self.setSize_(size)


GSAlignmentZone.__init__ = python_method(__GSAlignmentZone__init__)


def __GSAlignmentZone__str__(self):
	return "<GSAlignmentZone pos %s size %s>" % (self.position, self.size)


GSAlignmentZone.__str__ = python_method(__GSAlignmentZone__str__)

GSAlignmentZone.mutableCopyWithZone_ = __GSObject__copy__
'''
	Properties

		* :meth:`position`
		* :meth:`size`

	**Properties**
'''

GSAlignmentZone.position = property(
	lambda self: self.pyobjc_instanceMethods.position(),
	lambda self, value: self.setPosition_(validateNumber(value))
)
add_type(GSAlignmentZone, "position", float)
'''
	.. attribute:: position

		:type: float
'''

GSAlignmentZone.size = property(
	lambda self: self.pyobjc_instanceMethods.size(),
	lambda self, value: self.setSize_(value)
)
add_type(GSAlignmentZone, "size", float)
'''
	.. attribute:: size

		:type: float
'''


def __propertyListValue__(self) -> dict:
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


def ____GSInstance____(): pass


'''

:mod:`GSInstance`
===============================================================================

Implementation of the instance object. This corresponds with the "Exports" pane in Font Info.

.. class:: GSInstance()
'''


def GSInstance__new__(typ, *args, **kwargs):
	instanceType = 0
	if args:
		instanceType = args[0]
	elif kwargs:
		instanceType = kwargs.get("type", 0)
	return typ.alloc().initWithType_(instanceType)


GSInstance.__new__ = staticmethod(GSInstance__new__)


def __GSInstance__init__(self, type: int | None = None):
	pass


GSInstance.__init__ = python_method(__GSInstance__init__)


def __GSInstance__str__(self) -> str:
	return self.pyobjc_instanceMethods.description()


GSInstance.__str__ = python_method(__GSInstance__str__)
GSInstance.__repr__ = python_method(__GSInstance__str__)

GSInstance.mutableCopyWithZone_ = __GSObject__copy__
'''
	Properties

		* :attr:`active`
		* :attr:`name`
		* :attr:`type`
		* :attr:`visible`
		* :attr:`weightClass`
		* :attr:`widthClass`
		* :attr:`axes`
		* :attr:`properties`
		* :attr:`isItalic`
		* :attr:`isBold`
		* :attr:`linkStyle`
		* :attr:`preferredFamily`
		* :attr:`preferredSubfamilyName`
		* :attr:`windowsFamily`
		* :attr:`windowsStyle`
		* :attr:`windowsLinkedToStyle`
		* :attr:`fontName`
		* :attr:`fullName`
		* :attr:`compatibleFullName`
		* :attr:`compatibleFullNames`
		* :attr:`copyright`
		* :attr:`copyrights`
		* :attr:`description`
		* :attr:`descriptions`
		* :attr:`designer`
		* :attr:`designers`
		* :attr:`designerURL`
		* :attr:`familyName`
		* :attr:`familyNames`
		* :attr:`license`
		* :attr:`licenses`
		* :attr:`manufacturer`
		* :attr:`manufacturers`
		* :attr:`manufacturerURL`
		* :attr:`preferredFamilyName`
		* :attr:`preferredFamilyNames`
		* :attr:`preferredSubfamilyName`
		* :attr:`preferredSubfamilyNames`
		* :attr:`sampleText`
		* :attr:`sampleTexts`
		* :attr:`styleMapFamilyName`
		* :attr:`styleMapFamilyNames`
		* :attr:`styleMapStyleName`
		* :attr:`styleMapStyleNames`
		* :attr:`styleName`
		* :attr:`styleNames`
		* :attr:`trademark`
		* :attr:`trademarks`
		* :attr:`variableStyleName`
		* :attr:`variableStyleNames`
		* :attr:`font`
		* :attr:`customParameters`
		* :attr:`instanceInterpolations`
		* :attr:`manualInterpolation`
		* :attr:`interpolatedFontProxy`
		* :attr:`interpolatedFont`
		* :attr:`lastExportedFilePath`

	Functions

		* :meth:`generate`
		* :meth:`addAsMaster`

	**Properties**
'''

GSInstance.active = property(
	lambda self: bool(self.pyobjc_instanceMethods.exports()),
	lambda self, value: self.setExports_(value)
)
add_type(GSInstance, 'active', bool)

GSInstance.exports = property(
	lambda self: bool(self.pyobjc_instanceMethods.exports()),
	lambda self, value: self.setExports_(value)
)
add_type(GSInstance, 'exports', bool)
'''
	.. attribute:: exports

		:type: bool
'''

GSInstance.visible = property(
	lambda self: bool(self.pyobjc_instanceMethods.visible()),
	lambda self, value: self.setVisible_(value)
)
add_type(GSInstance, 'visible', bool)
'''
	.. attribute:: visible

		if visible in the preview in edit view

		:type: bool
'''

GSInstance.name = property(
	lambda self: self.pyobjc_instanceMethods.name(),
	lambda self, value: self.setName_(value)
)
add_type(GSInstance, 'name', str)
'''
	.. attribute:: name

		Name of instance. Corresponds to the "Style Name" field in the font info. This is used for naming the exported fonts.

		:type: str
'''

GSInstance.type = property(
	lambda self: self.pyobjc_instanceMethods.type()
)
add_type(GSInstance, "type", int)
'''
	.. attribute:: type

		the type of the instance. Can be either INSTANCETYPESINGLE or INSTANCETYPEVARIABLE.

		:type: int
'''


def __GSInstance_setValueValidation__(self: GSInstance, key: str, value: Any, valuetype: Type):
	if not isinstance(value, valuetype):
		raise TypeError("Type for {} should be {}, not {}".format(key, valuetype.__name__, type(value).__name__))
	self.setValue_forKey_(value, key)


GSInstance.weightClass = property(
	lambda self: self.weightClassValue(),
	lambda self, value: __GSInstance_setValueValidation__(self, "weightClassValue", value, int)
)
add_type(GSInstance, 'weightClass', int)
'''
	.. attribute:: weightClass

		Weight class, as set in Font Info, as an integer. Values from 1 to 1000 are supported but 100–900 is recommended.

		For actual position in interpolation designspace, use GSInstance.axes.

		:type: int
'''

GSInstance.weightClassName = property(
	lambda self: self.weightClassUI()
)
add_type(GSInstance, "weightClassName", str)
'''
	.. attribute:: weightClassName

		Human readable name corresponding to the value of GSInstance.weightClass. This attribute is read-only.
		Can be None if GSInstance.weightClass is not a multiple of 100.

		:type: str
'''

GSInstance.widthClass = property(
	lambda self: self.widthClassValue(),
	lambda self, value: __GSInstance_setValueValidation__(self, "widthClassValue", value, int)
)
add_type(GSInstance, 'widthClass', int)
'''
	.. attribute:: widthClass

		Width class, as set in Font Info, as an integer. Values from 1 to 9 are supported.

		For actual position in interpolation designspace, use GSInstance.axes.

		:type: int
'''

GSInstance.widthClassName = property(
	lambda self: self.widthClassUI()
)
add_type(GSInstance, 'widthClassName', str)
'''
	.. attribute:: widthClassName

		Human readable name corresponding to the value of GSInstance.widthClass. This attribute is read-only.

		:type: str
'''

GSInstance.axes = property(
	lambda self: InternalAxesProxy(self),
	lambda self, value: InternalAxesProxy(self).setter(value)
)
add_type(GSInstance, 'axes', List[float])
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
		.. deprecated:: 3.2
'''

GSInstance.internalAxesValues = property(
	lambda self: InternalAxesProxy(self),
	lambda self, value: InternalAxesProxy(self).setter(value)
)
add_type(GSInstance, 'internalAxesValues', List[float])
'''
	.. attribute:: internalAxesValues

		List of floats specifying the positions for each axis

		:type: list

		.. code-block:: python
			# setting a value for a specific axis
			instance.internalAxesValues[2] = 12
			# or more precisely
			instance.internalAxesValues[axis.axisId] = 12
			# setting all values at once
			instance.internalAxesValues = [100, 12, 3.5]

		.. versionadded:: 3.2
'''

GSInstance.externalAxesValues = property(
	lambda self: ExternalAxesProxy(self),
	lambda self, value: ExternalAxesProxy(self).setter(value)
)
add_type(GSInstance, 'externalAxesValues', List[float])
'''
	.. attribute:: externalAxesValues

		List of floats specifying the positions for each axis for the user facing values

		:type: list

		.. code-block:: python
			# setting a value for a specific axis
			instance.externalAxesValues[2] = 12
			# or more precisely
			instance.externalAxesValues[axis.axisId] = 12
			# setting all values at once
			instance.externalAxesValues = [100, 12, 3.5]

		.. versionadded:: 3.2
'''

GSInstance.properties = property(
	lambda self: PropertiesProxy(self),
	lambda self, values: PropertiesProxy(self).setter(values)
)
add_type(GSInstance, 'properties', list[GSInfoValueSingle | GSInfoValueLocalized])
'''
	.. attribute:: properties

		Holds the fonts info properties. Can be instances of :class:`GSInfoValueSingle` and :class:`GSInfoValueLocalized`

		The localized values use language tags defined in the middle column of `Language System Tags table`: <https://docs.microsoft.com/en-us/typography/opentype/spec/languagetags>.

		The names are listed in the constants: `Info Property Keys`_

		.. code-block:: python
			# To access the default value:

			instance.properties["versionString"]

			instance.properties["versionString"] = "version 1.0"

			# To access specific languages:

			instance.properties.getProperty(GSPropertyNameDesignersKey, "DEU")

			instance.properties.setProperty(GSPropertyNameDesignersKey, "SomeName", "DEU")


		:type: list

		.. versionadded:: 3
'''

GSInstance.isItalic = property(
	lambda self: bool(self.pyobjc_instanceMethods.isItalic()),
	lambda self, value: self.setIsItalic_(value)
)
add_type(GSInstance, 'isItalic', bool)
'''
	.. attribute:: isItalic

		Italic flag for style linking

		:type: bool
'''

GSInstance.isBold = property(
	lambda self: bool(self.pyobjc_instanceMethods.isBold()),
	lambda self, value: self.setIsBold_(value)
)
add_type(GSInstance, 'isBold', bool)
'''
	.. attribute:: isBold

		Bold flag for style linking

		:type: bool
'''

GSInstance.linkStyle = property(
	lambda self: self.pyobjc_instanceMethods.linkStyle(),
	lambda self, value: self.setLinkStyle_(value)
)
add_type(GSInstance, 'linkStyle', str)
'''
	.. attribute:: linkStyle

		Linked style

		:type: str
'''

GSInstance.preferredFamily = property(
	lambda self: self.pyobjc_instanceMethods.preferredFamily(),
	lambda self, value: self.setProperty_value_languageTag_("preferredFamilyNames", value, None)
)
add_type(GSInstance, 'preferredFamily', str)
'''
	.. attribute:: preferredFamily

		preferredFamily

		:type: str
'''

GSInstance.windowsFamily = property(
	lambda self: self.pyobjc_instanceMethods.styleMapFamilyName(),
	lambda self, value: self.setProperty_value_languageTag_("styleMapFamilyNames", value, None)
)
add_type(GSInstance, "windowsFamily", str)
'''
	.. attribute:: windowsFamily

		windowsFamily

		:type: str
'''

GSInstance.windowsStyle = property(
	lambda self: self.pyobjc_instanceMethods.styleMapStyleName(),
	lambda self, value: self.setProperty_value_languageTag_("styleMapStyleNames", value, None)
)
add_type(GSInstance, "windowsStyle", str)
'''
	.. attribute:: windowsStyle

		This is computed from "isBold" and "isItalic". Read-only.

		:type: str
'''

GSInstance.windowsLinkedToStyle = property(
	lambda self: self.pyobjc_instanceMethods.windowsLinkedToStyle_(None)[0]
)
add_type(GSInstance, "windowsLinkedToStyle", str)
'''
	.. attribute:: windowsLinkedToStyle

		windowsLinkedToStyle. Read-only.

		:type: str
'''

GSInstance.fontName = property(
	lambda self: self.pyobjc_instanceMethods.fontName_(None)[0],
	lambda self, value: self.setProperty_value_languageTag_("postscriptFontName", value, None)
)
add_type(GSInstance, "fontName", str)
'''
	.. attribute:: fontName

		fontName (postscriptFontName)

		:type: str
'''

GSInstance.fullName = property(
	lambda self: self.pyobjc_instanceMethods.fullName_(None)[0],
	lambda self, value: self.setProperty_value_languageTag_("postscriptFullName", value, None)
)
add_type(GSInstance, "fullName", str)
'''
	.. attribute:: fullName

		fullName (postscriptFullName)

		:type: str
'''

GSInstance.compatibleFullName = property(
	lambda self: self.defaultPropertyForName_("compatibleFullNames"),
	lambda self, value: self.setProperty_value_languageTag_("compatibleFullNames", value, None)
)
add_type(GSInstance, "compatibleFullName", str)
'''
	.. attribute:: compatibleFullName

		This accesses the default value only. The localizations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.compatibleFullNames = property(
	lambda self: FontInfoPropertyProxy(self, "compatibleFullNames")
)
add_type(GSInstance, "compatibleFullNames", dict[str, str])
'''
	.. attribute:: compatibleFullNames

		This accesses all localized compatibleFullNames values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			instance.compatibleFullNames["ENG"] = "MyFont Condensed Bold"

		.. versionadded:: 3.0.3
'''

GSInstance.copyright = property(
	lambda self: self.defaultPropertyForName_("copyrights"),
	lambda self, value: self.setProperty_value_languageTag_("copyrights", value, None)
)
add_type(GSInstance, "copyright", str)
'''
	.. attribute:: copyright

		This accesses the default value only. The localizations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.2
'''

GSInstance.copyrights = property(
	lambda self: FontInfoPropertyProxy(self, "copyrights")
)
add_type(GSInstance, "copyrights", dict[str, str])
'''
	.. attribute:: copyrights

		This accesses all localized copyright values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			instance.copyrights["ENG"] = "All rights reserved"

		.. versionadded:: 3.0.3
'''

GSInstance.description = property(
	lambda self: self.defaultPropertyForName_("descriptions"),
	lambda self, value: self.setProperty_value_languageTag_("descriptions", value, None)
)
add_type(GSInstance, "description", str)
'''
	.. attribute:: description

		This accesses the default value only. The localizations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.descriptions = property(
	lambda self: FontInfoPropertyProxy(self, "descriptions")
)
add_type(GSInstance, "descriptions", dict[str, str])
'''
	.. attribute:: descriptions

		This accesses all localized description values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			instance.descriptions["ENG"] = "This is my description"

		.. versionadded:: 3.0.3
'''

GSInstance.designer = property(
	lambda self: self.defaultPropertyForName_("designers"),
	lambda self, value: self.setProperty_value_languageTag_("designers", value, None)
)
add_type(GSInstance, "designer", str)
'''
	.. attribute:: designer

		This accesses the default value only. The localizations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.2
'''

GSInstance.designerURL = property(
	lambda self: self.defaultPropertyForName_("designerURL"),
	lambda self, value: self.setProperty_value_languageTag_("designerURL", value, None)
)
'''
	.. attribute:: designerURL

		:type: str

		.. versionadded:: 3.0.2
'''

GSInstance.designers = property(
	lambda self: FontInfoPropertyProxy(self, "designers")
)
add_type(GSInstance, "designers", dict[str, str])
'''
	.. attribute:: designers

		This accesses all localized designer values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			instance.designers["ENG"] = "John Smith"

		.. versionadded:: 3.0.3
'''

GSInstance.familyName = property(
	lambda self: self.defaultPropertyForName_("familyNames"),
	lambda self, value: self.setProperty_value_languageTag_("familyNames", value, None)
)
'''
	.. attribute:: familyName

		familyName

		:type: str
'''

GSInstance.familyNames = property(
	lambda self: FontInfoPropertyProxy(self, "familyNames")
)
add_type(GSInstance, "familyNames", dict[str, str])
'''
	.. attribute:: familyNames

		This accesses all localized family name values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			instance.familyNames["ENG"] = "MyFamilyName"

		.. versionadded:: 3.0.3
'''

GSInstance.license = property(
	lambda self: self.defaultPropertyForName_("licenses"),
	lambda self, value: self.setProperty_value_languageTag_("licenses", value, None)
)
'''
	.. attribute:: license

		This accesses the default value only. The localizations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.licenses = property(lambda self: FontInfoPropertyProxy(self, "licenses"))
add_type(GSInstance, "licenses", dict[str, str])
'''
	.. attribute:: licenses

		This accesses all localized family name values.
		For details :attr:`GSInstance.properties`

		:type: dict
		.. code-block:: python
			instance.licenses["ENG"] = "This font may be installed on all of your machines and printers, but you may not sell or give these fonts to anyone else."

		.. versionadded:: 3.0.3
'''

GSInstance.manufacturer = property(
	lambda self: self.defaultPropertyForName_("manufacturers"),
	lambda self, value: self.setProperty_value_languageTag_("manufacturers", value, None)
)
'''
	.. attribute:: manufacturer

		This accesses the default value only. The localizations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.2
'''

GSInstance.manufacturers = property(
	lambda self: FontInfoPropertyProxy(self, "manufacturers")
)
add_type(GSInstance, "manufacturers", dict[str, str])
'''
	.. attribute:: manufacturers

		This accesses all localized family name values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			instance.manufacturers["ENG"] = "My English Corporation"

		.. versionadded:: 3.0.3
'''

GSInstance.preferredFamilyName = property(
	lambda self: self.defaultPropertyForName_("preferredFamilyNames"),
	lambda self, value: self.setProperty_value_languageTag_("preferredFamilyNames", value, None)
)
'''
	.. attribute:: preferredFamilyName

		This accesses the default value only. The localizations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.preferredFamilyNames = property(lambda self: FontInfoPropertyProxy(self, "preferredFamilyNames"))
add_type(GSInstance, "preferredFamilyNames", dict[str, str])
'''
	.. attribute:: preferredFamilyNames

		This accesses all localized designer values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			instance.preferredFamilyNames["ENG"] = "MyFamilyName"

		.. versionadded:: 3.0.3
'''

GSInstance.preferredSubfamilyName = property(
	lambda self: self.defaultPropertyForName_("preferredSubfamilyNames"),
	lambda self, value: self.setProperty_value_languageTag_("preferredSubfamilyNames", value, None)
)
'''
	.. attribute:: preferredSubfamilyName

		preferredSubfamilyName

		:type: str
'''

GSInstance.preferredSubfamilyNames = property(lambda self: FontInfoPropertyProxy(self, "preferredSubfamilyNames"))
add_type(GSInstance, "preferredSubfamilyNames", dict[str, str])
'''
	.. attribute:: preferredSubfamilyNames

		This accesses all localized designer values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			instance.preferredSubfamilyNames["ENG"] = "Regular"

		.. versionadded:: 3.0.3
'''

GSInstance.sampleText = property(
	lambda self: self.defaultPropertyForName_("sampleTexts"),
	lambda self, value: self.setProperty_value_languageTag_("sampleTexts", value, None)
)
'''
	.. attribute:: sampleText

		This accesses the default value only. The localizations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.sampleTexts = property(lambda self: FontInfoPropertyProxy(self, "sampleTexts"))
add_type(GSInstance, "sampleTexts", dict[str, str])
'''
	.. attribute:: sampleTexts

		This accesses all localized designer values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			instance.sampleTexts["ENG"] = "This is my sample text"

		.. versionadded:: 3.0.3
'''

GSInstance.styleMapFamilyName = property(
	lambda self: self.defaultPropertyForName_("styleMapFamilyNames"),
	lambda self, value: self.setProperty_value_languageTag_("styleMapFamilyNames", value, None)
)
'''
	.. attribute:: styleMapFamilyName

		This accesses the default value only. The localizations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.styleMapFamilyNames = property(
	lambda self: FontInfoPropertyProxy(self, "styleMapFamilyNames")
)
add_type(GSInstance, "styleMapFamilyNames", dict[str, str])
'''
	.. attribute:: styleMapFamilyNames

		This accesses all localized designer values.
		For details :attr:`GSInstance.properties`

		:type: dict


		.. code-block:: python
			instance.styleMapFamilyNames["ENG"] = "MyFamily Bold"

		.. versionadded:: 3.0.3
'''

GSInstance.styleMapStyleName = property(
	lambda self: self.defaultPropertyForName_("styleMapStyleNames"),
	lambda self, value: self.setProperty_value_languageTag_("styleMapStyleNames", value, None)
)
'''
	.. attribute:: styleMapStyleName

		This accesses the default value only. The localizations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.styleMapStyleNames = property(
	lambda self: FontInfoPropertyProxy(self, "styleMapStyleNames")
)
add_type(GSInstance, "styleMapStyleNames", dict[str, str])
'''
	.. attribute:: styleMapStyleNames

		This accesses all localized designer values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			instance.styleMapStyleNames["ENG"] = "Bold"

		.. versionadded:: 3.0.3
'''

GSInstance.styleName = property(
	lambda self: self.defaultPropertyForName_("styleNames"),
	lambda self, value: self.setProperty_value_languageTag_("styleNames", value, None)
)
'''
	.. attribute:: styleName

		This accesses the default value only. The localizations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.styleNames = property(
	lambda self: FontInfoPropertyProxy(self, "styleNames")
)
'''
	.. attribute:: styleNames

		This accesses all localized styleName values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			instance.styleNames["ENG"] = "Regular"

		.. versionadded:: 3.0.3
'''

GSInstance.trademark = property(
	lambda self: self.defaultPropertyForName_("trademarks"),
	lambda self, value: self.setProperty_value_languageTag_("trademarks", value, None)
)
'''
	.. attribute:: trademark

		This accesses the default value only. The localizations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.trademarks = property(
	lambda self: FontInfoPropertyProxy(self, "trademarks")
)
'''
	.. attribute:: trademarks

		This accesses all localized trademark values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			instance.trademarks["ENG"] = "ThisFont is a trademark by MyFoundry.com"

		.. versionadded:: 3.0.3
'''

GSInstance.variableStyleName = property(
	lambda self: self.defaultPropertyForName_("variableStyleNames"),
	lambda self, value: self.setProperty_value_languageTag_("variableStyleNames", value, None)
)
'''
	.. attribute:: variableStyleName

		This accesses the default value only. The localizations can be accessed by :attr:`GSInstance.properties`

		:type: str

		.. versionadded:: 3.0.3
'''

GSInstance.variableStyleNames = property(
	lambda self: FontInfoPropertyProxy(self, "variableStyleNames")
)
'''
	.. attribute:: variableStyleNames

		This accesses all localized variableStyleName values.
		For details :attr:`GSInstance.properties`

		:type: dict

		.. code-block:: python
			instance.variableStyleNames["ENG"] = "Roman"

		.. versionadded:: 3.0.3
'''

GSInstance.manufacturerURL = property(
	lambda self: self.defaultPropertyForName_("manufacturerURL"),
	lambda self, value: self.setProperty_value_languageTag_("manufacturerURL", value, None)
)
'''
	.. attribute:: manufacturerURL

		:type: str

		.. versionadded:: 3.0.2
'''

GSInstance.font = property(
	lambda self: self.pyobjc_instanceMethods.font(),
	lambda self, value: self.setFont_(value)
)
'''
	.. attribute:: font

		Reference to the :class:`GSFont` object that contains the instance. Normally that is set by the app, only if the instance is not actually added to the font, then set this manually.

		:type: GSFont

		.. versionadded:: 2.5.1
'''

GSInstance.customParameters = property(
	lambda self: CustomParametersProxy(self),
	lambda self, value: CustomParametersProxy(self).setter(value)
)
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

			# add multiple parameters:
			parameter = GSCustomParameter("Name Table Entry", "1 1;"font name")
			font.customParameters.append(parameter)
			parameter = GSCustomParameter("Name Table Entry", "2 1;"style name")
			font.customParameters.append(parameter)

			# delete a parameter
			del font.instances[0].customParameters['hheaLineGap']
'''

GSInstance.userData = property(
	lambda self: UserDataProxy(self),
	lambda self, value: UserDataProxy(self).setter(value)
)
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

GSInstance.tempData = property(
	lambda self: TempDataProxy(self),
	lambda self, value: TempDataProxy(self).setter(value)
)
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

GSInstance.instanceInterpolations = property(
	lambda self: self.pyobjc_instanceMethods.instanceInterpolations(),
	lambda self, value: self.setInstanceInterpolations_(value)
)
'''
	.. attribute:: instanceInterpolations

		A dict that contains the interpolation coefficients for each master.
		This is automatically updated if you change interpolationWeight, interpolationWidth, interpolationCustom. It contains FontMaster IDs as keys and coefficients for that master as values.
		Or, you can set it manually if you set manualInterpolation to True. There is no UI for this, so you need to do that with a script.

		:type: dict
	'''

GSInstance.manualInterpolation = property(
	lambda self: bool(self.pyobjc_instanceMethods.manualInterpolation()),
	lambda self, value: self.setManualInterpolation_(value)
)
'''
	.. attribute:: manualInterpolation

		Disables automatic calculation of instanceInterpolations
		This allows manual setting of instanceInterpolations.

		:type: bool
	'''


def __GSInstance_InterpolatedFontProxy__(self):
	result = self.interpolatedFont_(None)
	if not result[0]:
		raise result[1].localizedDescription()
	return result[0]


GSInstance.interpolatedFontProxy = property(lambda self: __GSInstance_InterpolatedFontProxy__(self))
'''
	.. attribute:: interpolatedFontProxy

		a proxy font that acts similar to a normal font object but only interpolates the glyphs you ask it for.

		It is not properly wrapped yet. So you need to use the ObjectiveC methods directly.
'''


def __GSInstance_FontObject__(self):
	return self.font.generateInstance_error_(self, None)[0]


GSInstance.interpolatedFont = property(lambda self: __GSInstance_FontObject__(self))
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
			>> (<GSFontMaster "Light" width 100.0 weight 75.0>)
			print(interpolated.instances)
			>> (<GSInstance "Web" width 100.0 weight 75.0>)

'''
'''
	**Functions**

	.. function:: generate([format, fontPath, autoHint, removeOverlap, useSubroutines, useProductionNames, containers, decomposeSmartStuff])

		Exports the instance. All parameters are optional.

		:param str format: The format of the outlines: :const:`CFF` or :const:`TT`. Default: CFF
		:param str fontPath: The destination path for the final fonts. If None, it uses the default location set in the export dialog
		:param bool autoHint: If auto hinting should be applied. Default: True
		:param bool removeOverlap: If overlaps should be removed. Default: True
		:param bool useSubroutines: If to use subroutines for CFF. Default: True
		:param bool useProductionNames: If to use production names. Default: True
		:param list containers: list of container formats. Use any of the following constants: :const:`PLAIN`, :const:`WOFF`, :const:`WOFF2`. Default: PLAIN
		:param bool decomposeSmartStuff: If smart components should be decomposed. Default: True
		:return: On success, True; on failure, error message.
		:rtype: bool/list

		.. code-block:: python
			# export all instances as OpenType (.otf) and WOFF2 to user’s font folder

			exportFolder = '/Users/myself/Library/Fonts'

			for instance in Glyphs.font.instances:
			    instance.generate(FontPath=exportFolder, Containers=[PLAIN, WOFF2])

			Glyphs.showNotification('Export fonts', 'The export of %s was successful.' % (Glyphs.font.familyName))
'''


class _ExporterDelegate_(NSObject):

	result: str | None = None

	def init(self):
		self = objc.super(_ExporterDelegate_, self).init()  # type: ignore
		return self

	def collectResult_instance_title_(
		self,
		error: str | NSString | NSError,
		instancePath: str,
		title: str,
	):
		if isinstance(error, NSError):
			string = error.localizedDescription()  # type: ignore
			string = "Error in instance: %s: %s " % (title, string)
			if error.localizedRecoverySuggestion() and error.localizedRecoverySuggestion().length() > 0:  # type: ignore
				string += error.localizedRecoverySuggestion()  # type: ignore
			error = string
		self.result = cast(str, error)


def __GSInstance_Export__(
	self,
	format: str = CFF,
	fontPath: str | None = None,
	autoHint: bool = True,
	removeOverlap: bool = True,
	useSubroutines: bool = True,
	useProductionNames: bool = True,
	containers: list | None = None,
	decomposeSmartStuff: bool = True
) -> str | None:

	if format == OTF:
		format = CFF
	if format == TTF:
		format = TT

	if format not in [CFF, TT, UFO]:
		raise KeyError('The font format is not supported: %s (only \'OTF\' and \'TTF\')' % format)

	if self.type == INSTANCETYPEVARIABLE and format == UFO:
		raise KeyError('Variable instances can only be exported as TTF')

	if fontPath and fontPath.startswith("~"):
		fontPath = os.path.expanduser(fontPath)

	containerList = None
	if containers is not None:
		containerList = []
		for container in containers:
			if container in [PLAIN, WOFF, WOFF2]:
				containerList.append(container.lower())
			else:
				raise KeyError('The container format is not supported: %s (only \'WOFF\' \'WOFF2\' \'plain\')' % container)

	if not containerList:
		containerList = [PLAIN]

	if format == UFO:
		if not fontPath:
			raise ValueError('Please provide a FontPath')
		instanceFont = self.interpolatedFont
		return instanceFont.export(format=format, fontPath=fontPath, useProductionNames=useProductionNames, decomposeSmartStuff=decomposeSmartStuff)
	else:
		font = self.font
		gs_format = None
		if fontPath is None:
			fontPath = cast(str, NSUserDefaults.standardUserDefaults().objectForKey_(objcObject("OTFExportPath")))
		if self.type == INSTANCETYPEVARIABLE:
			gs_format = GSOutlineFormatVariableCFF if format == CFF else GSOutlineFormatVariableTT
			removeOverlap = False
		else:
			if format == OTF or format == CFF:
				gs_format = GSOutlineFormatCFF
			elif format == TTF or format == TT:
				gs_format = GSOutlineFormatTrueType
			elif format == VARIABLE:
				raise KeyError("Use Variable instance instead of “format=VARIABLE”")
		if gs_format is None:
			raise KeyError(f"Invalid format: {format}")
		exporterClass: GSExportInstanceOperation = NSClassFromString("GSExportInstanceOperation")
		exporter = exporterClass.alloc().initWithFont_instance_outlineFormat_containers_(font, self, gs_format, containerList)
		if fontPath is None:
			fontPath = NSUserDefaults.standardUserDefaults().objectForKey_("OTFExportPath")
		if fontPath is not None:
			exporter.setInstallFontURL_(NSURL.fileURLWithPath_(fontPath))
		# the following parameters can be set here or directly read from the instance.
		exporter.setAutohint_(autoHint)
		exporter.setRemoveOverlap_(removeOverlap)
		exporter.setUseSubroutines_(useSubroutines)
		exporter.setUseProductionNames_(useProductionNames)

		# the collectResults_() method of this object will be called on case the exporter has to report a problem.
		delegate: _ExporterDelegate_ = _ExporterDelegate_.new()
		exporter.setDelegate_(delegate)
		exporter.main()
		if delegate.result is None:
			self.lastExportedFilePath = exporter.tempFontPath()
		else:
			self.lastExportedFilePath = None
		return delegate.result


GSInstance.generate = python_method(__GSInstance_Export__)


def __GSFont_Export__(
	self,
	format: str | None = OTF,
	instances: list[GSInstance] | None = None,
	fontPath: str | None = None,
	autoHint: bool = True,
	removeOverlap: bool | None = None,
	useSubroutines: bool = True,
	useProductionNames: bool = True,
	containers: bool | None = None,
	decomposeSmartStuff: bool = True
):
	if format not in [OTF, WOFF, WOFF2, TTF, VARIABLE, UFO]:
		raise KeyError('The font format is not supported: %s (only \'OTF\' and \'TTF\')' % format)

	if fontPath is None:
		fontPath = Glyphs.defaults["OTFExportPath"]

	if fontPath and fontPath.startswith("~"):
		fontPath = os.path.expanduser(fontPath)

	if format == UFO:
		font = self.font()
		GlyphsFileFormatUFO = objc.lookUpClass("GlyphsFileFormatUFO")
		ufoWriter = GlyphsFileFormatUFO.new()
		ufoWriter.setConvertNames_(useProductionNames)
		ufoWriter.setDecomposeSmartStuff_(decomposeSmartStuff)
		ufoWriter.setExportOptions_({"SelectedMasterIndexes": NSIndexSet.indexSetWithIndexesInRange_(NSRange(0, len(font.masters)))})
		url: NSURL | None = None
		if fontPath is not None:
			url = NSURL.fileURLWithPath_(fontPath)
		result = ufoWriter.exportFont_toURL_error_(font, url, None)
		result = _checkReturnValue(result)
		if result is not None:
			raise ValueError(result)
		return
	else:
		if not instances:
			instances = []
			for instance in self.instances:
				if not instance.active:
					continue
				if (format == VARIABLE) == (instance.type == INSTANCETYPESINGLE):
					continue
				instances.append(instance)
		if len(instances) == 0:
			instanceType = INSTANCETYPEVARIABLE if format == VARIABLE else INSTANCETYPESINGLE
			instance = GSInstance.alloc().initWithType_(instanceType)
			instance.font = self
			instances.append(instance)
		allResults = []
		for instance in instances:
			result = instance.generate(
				format=format,
				fontPath=fontPath,
				autoHint=autoHint,
				removeOverlap=removeOverlap,
				useSubroutines=useSubroutines,
				useProductionNames=useSubroutines,
				containers=containers
			)
			allResults.append(result)
		return allResults


GSFont.export = python_method(__GSFont_Export__)

GSInstance.lastExportedFilePath = property(
	lambda self: self.tempDataForKey_("lastExportedFilePath"),
	lambda self, value: self.setTempData_forKey_(value, "lastExportedFilePath")
)
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
			>> (<GSFontMaster "Light" width 100.0 weight 75.0>)
			print(interpolated.instances)
			>> (<GSInstance "Web" width 100.0 weight 75.0>)

	'''


def __GSInstance_AddInstanceAsMaster__(self) -> "GSFontMaster":
	self.font.addMasterFromInstance_error_(self, None)


GSInstance.addAsMaster = python_method(__GSInstance_AddInstanceAsMaster__)
'''
	.. function:: addAsMaster()

		Add this instance as a new master to the font. Identical to "Instance as Master" menu item in the Font Info’s Instances section.

		.. versionadded:: 2.6.2
'''

def __GSInstance__fileName__(self, format: str) -> str:
	return self.fileName_error_(format, None)[0]


GSInstance.fileName = python_method(__GSInstance__fileName__)
'''
	.. function:: fileName(format)

		returns the filename with the suffix depending on the format (OTF, TTF)

		.. versionadded:: 4
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


def ____GSCustomParameter____(): pass


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

	# add multiple parameters:
	parameter = GSCustomParameter("Name Table Entry", "1 1;"font name")
	font.customParameters.append(parameter)
	parameter = GSCustomParameter("Name Table Entry", "2 1;"style name")
	font.customParameters.append(parameter)

	# delete a parameter
	del font.customParameters['trademark']

.. class:: GSCustomParameter([name, value])

	:param name: The name
	:param value: The value
'''

GSCustomParameter.__new__ = staticmethod(__GSObject__new__)


def __GSCustomParameter__init__(self, name: str, value: Any):
	self.setName_(name)
	self.setValue_(value)


GSCustomParameter.__init__ = python_method(__GSCustomParameter__init__)


def __GSCustomParameter__str__(self):
	return "<GSCustomParameter %s: %s>" % (self.name, self.value)


GSCustomParameter.__str__ = python_method(__GSCustomParameter__str__)

GSCustomParameter.mutableCopyWithZone_ = __GSObject__copy__
'''
	Properties

		* :attr:`active`
		* :attr:`name`
		* :attr:`value`

	**Properties**
'''

GSCustomParameter.name = property(
	lambda self: self.pyobjc_instanceMethods.name(),
	lambda self, value: self.setName_(value)
)
'''
	.. attribute:: name

		:type: str
'''

GSCustomParameter.value = property(
	lambda self: self.pyobjc_instanceMethods.value(),
	lambda self, value: self.setValue_(value)
)
'''
	.. attribute:: value

		:type: str, list, dict, int, float
'''

GSCustomParameter.active = property(
	lambda self: self.pyobjc_instanceMethods.active(),
	lambda self, value: self.setActive_(value)
)
'''
	.. attribute:: active

		If the the parameter should be used or not

		:type: bool
'''

GSCustomParameter.parent = property(lambda self: self.pyobjc_instanceMethods.parent())
'''
	.. attribute:: parent

		:type: GSFont, GSFontMaster or GSInstance
'''

def __GSCustomParameter_registerCustomType__(
	cls,
	parameterName: str,
	parameterType: str | None = None,
	listUIClass: Type[GSParameterValueViewController] | str | None = None,
	dialogUIClass: Type[GSPropertyDialogController] | str | None = None,
	description: str | None = None,
):
	# print("__registerCustomType__", parameterName, parameterType, listUIClass, dialogUIClass, description)
	if parameterType:
		assert listUIClass is None and dialogUIClass is None, "parameter Type and UI classes can’t be set at the same time"
		GSGlyphsInfo.addType_forParameter_(parameterType, parameterName)
	elif listUIClass:
		assert dialogUIClass is None, "listUIClass and dialogUIClass can’t be set at the same time"
		if isinstance(listUIClass, str):
			listUIClass = objc.lookUpClass(listUIClass)
		assert issubclass(cast(Type, listUIClass), GSParameterValueViewController), "wrong class, got: %s" % type(listUIClass)
		GSCustomParameterValueViewController.addClass_forParameter_(listUIClass, parameterName)
	elif dialogUIClass:
		if isinstance(dialogUIClass, str):
			dialogUIClass = objc.lookUpClass(dialogUIClass)
		assert issubclass(cast(Type, dialogUIClass), GSPropertyDialogController), "wrong class, got: %s" % type(dialogUIClass)
		GSCustomParameterValueViewController.addSheetController_forParameter_(dialogUIClass, parameterName)

	if description:
		GSGlyphsInfo.addDescription_forParameter_(description, parameterName)


GSCustomParameter.__class__.registerCustomType = python_method(__GSCustomParameter_registerCustomType__)


##################################################################################
#
#
#
#           GSClass
#
#
#
##################################################################################


def ____GSClass____(): pass


'''

:mod:`GSClass`
===============================================================================

Implementation of the class object. It is used to store OpenType classes.

For details on how to access them, please look at :class:`GSFont.classes`

.. class:: GSClass([tag, code])

	:param tag: The class name
	:param code: A list of glyph names, separated by space or newline

		* :attr:`name`
		* :attr:`code`
		* :attr:`automatic`
		* :attr:`active`

	**Properties**
'''

GSClass.__new__ = staticmethod(__GSObject__new__)


def __GSClass__init__(self, name=None, code=None):
	if name is not None:
		self.setName_(name)
	if code is not None:
		self.setCode_(code)


GSClass.__init__ = python_method(__GSClass__init__)


def __GSClass__str__(self):
	return "<GSClass \"%s\">" % (self.name)


GSClass.__str__ = python_method(__GSClass__str__)

GSClass.__eq__ = python_method(lambda self, other: self.isEqual_(other))

GSClass.mutableCopyWithZone_ = __GSObject__copy__

GSClass.name = property(
	lambda self: self.pyobjc_instanceMethods.name(),
	lambda self, value: self.setName_(value)
)
'''
	.. attribute:: name

		The class name

		:type: str
'''

GSClass.code = property(
	lambda self: self.pyobjc_instanceMethods.code(),
	lambda self, value: self.setCode_(value)
)
'''
	.. attribute:: code

		A string with space separated glyph names.

		:type: str
'''

GSClass.automatic = property(
	lambda self: self.pyobjc_instanceMethods.automatic(),
	lambda self, value: self.setAutomatic_(value)
)
'''
	.. attribute:: automatic

		Define whether this class should be auto-generated when pressing the 'Update' button in the Font Info.

		:type: bool
'''

GSClass.active = property(
	lambda self: not self.disabled(),
	lambda self, value: self.setDisabled_(not value)
)
'''
	.. attribute:: active

		:type: bool

		.. versionadded:: 2.5
'''

GSClass.parent = property(
	lambda self: self.pyobjc_instanceMethods.parent(),
	lambda self, value: self.setParent_(value)
)

GSClass.tempData = property(
	lambda self: TempDataProxy(self),
	lambda self, value: TempDataProxy(self).setter(value)
)
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


def ____GSFeaturePrefix____(): pass


'''

:mod:`GSFeaturePrefix`
===============================================================================

Implementation of the featurePrefix object. It is used to store things that need to be outside of a feature like standalone lookups.

For details on how to access them, please look at :class:`GSFont.featurePrefixes`

.. class:: GSFeaturePrefix([tag, code])

	:param tag: The Prefix name
	:param code: The feature code in Adobe FDK syntax

		* :attr:`name`
		* :attr:`code`
		* :attr:`automatic`
		* :attr:`active`

	**Properties**
'''

GSFeaturePrefix.__new__ = staticmethod(__GSObject__new__)
GSFeaturePrefix.__init__ = python_method(__GSClass__init__)


def __GSFeaturePrefix__str__(self):
	return "<GSFeaturePrefix \"%s\">" % (self.name)


GSFeaturePrefix.__str__ = python_method(__GSFeaturePrefix__str__)

GSFeaturePrefix.mutableCopyWithZone_ = __GSObject__copy__

GSFeaturePrefix.name = property(
	lambda self: self.pyobjc_instanceMethods.name(),
	lambda self, value: self.setName_(value)
)
'''
	.. attribute:: name

		The FeaturePrefix name

		:type: str
'''

GSFeaturePrefix.code = property(
	lambda self: self.pyobjc_instanceMethods.code(),
	lambda self, value: self.setCode_(value)
)
'''
	.. attribute:: code

		A String containing feature code.

		:type: str
'''

GSFeaturePrefix.automatic = property(
	lambda self: bool(self.pyobjc_instanceMethods.automatic()),
	lambda self, value: self.setAutomatic_(value)
)
'''
	.. attribute:: automatic

		Define whether this should be auto-generated when pressing the 'Update' button in the Font Info.

		:type: bool
'''

GSFeaturePrefix.active = property(
	lambda self: not self.disabled(),
	lambda self, value: self.setDisabled_(not value)
)
'''
	.. attribute:: active

		:type: bool

		.. versionadded:: 2.5
'''

GSFeaturePrefix.parent = property(
	lambda self: self.pyobjc_instanceMethods.parent(),
	lambda self, value: self.setParent_(value)
)

GSFeaturePrefix.tempData = property(
	lambda self: TempDataProxy(self),
	lambda self, value: TempDataProxy(self).setter(value)
)
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
#           GSFeature
#
#
#
##################################################################################


def ____GSFeature____(): pass


'''

:mod:`GSFeature`
===============================================================================

Implementation of the feature object. It is used to implement OpenType Features in the Font Info.

For details on how to access them, please look at :class:`GSFont.features`

.. class:: GSFeature([tag, code])

	:param tag: The feature name
	:param code: The feature code in Adobe FDK syntax

	Properties

		* :attr:`name`
		* :attr:`code`
		* :attr:`automatic`
		* :attr:`notes`
		* :attr:`active`
		* :attr:`layers`

	Functions

		* :meth:`update`

	**Properties**
'''

GSFeature.__new__ = staticmethod(__GSObject__new__)


def __GSFeature__init__(self, name=None, code=None):
	if name is not None:
		self.setTag_(objcObject(name))
	if code is not None:
		self.setCode_(objcObject(code))


GSFeature.__init__ = python_method(__GSFeature__init__)


def __GSFeature__str__(self):
	return "<GSFeature \"%s\">" % (self.name)


GSFeature.__str__ = python_method(__GSFeature__str__)

GSFeature.__eq__ = python_method(lambda self, other: self.isEqualToFeature_(other))

GSFeature.mutableCopyWithZone_ = __GSObject__copy__

GSFeature.name = property(
	lambda self: self.tag(),
	lambda self, value: self.setTag_(value)
)
'''
	.. attribute:: name

		The feature name

		:type: str
'''

GSFeature.code = property(
	lambda self: self.pyobjc_instanceMethods.code(),
	lambda self, value: self.setCode_(value)
)
'''
	.. attribute:: code

		The Feature code in Adobe FDK syntax.

		:type: str
'''

GSFeature.automatic = property(
	lambda self: bool(self.pyobjc_instanceMethods.automatic()),
	lambda self, value: self.setAutomatic_(value)
)
'''
	.. attribute:: automatic

		Define whether this feature should be auto-generated when pressing the 'Update' button in the Font Info.

		:type: bool
'''

GSFeature.notes = property(
	lambda self: self.pyobjc_instanceMethods.notes(),
	lambda self, value: self.setNotes_(value)
)
'''
	.. attribute:: notes

		Some extra text. Is shown in the bottom of the feature window. Contains the stylistic set name parameter

		:type: str
'''

GSFeature.active = property(
	lambda self: not self.disabled(),
	lambda self, value: self.setDisabled_(not value)
)
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

GSFeature.labels = property(
	lambda self: self.pyobjc_instanceMethods.labels(),
	lambda self, value: self.setLabels_(value)
)
'''
	.. attribute:: labels

		List of Feature names for stylistic set features

		:type: list
'''

GSFeature.parent = property(
	lambda self: self.pyobjc_instanceMethods.parent(),
	lambda self, value: self.setParent_(value)
)

GSFeature.tempData = property(
	lambda self: TempDataProxy(self),
	lambda self, value: TempDataProxy(self).setter(value)
)
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


def ____GSSubstitution____(): pass


"""

############ NOCH NICHT DOKUMENTIERT WEIL NOCH NICHT AUSGEREIFT ############

"""

GSSubstitution.__new__ = staticmethod(__GSObject__new__)
GSSubstitution.__init__ = python_method(__empty__init__)

GSSubstitution.back = property(
	lambda self: self.pyobjc_instanceMethods.back(),
	lambda self, value: self.setBack_(value)
)

GSSubstitution.source = property(
	lambda self: self.pyobjc_instanceMethods.source(),
	lambda self, value: self.setSource_(value)
)

GSSubstitution.forward = property(
	lambda self: self.pyobjc_instanceMethods.fwd(),
	lambda self, value: self.setFwd_(value)
)

GSSubstitution.target = property(
	lambda self: self.pyobjc_instanceMethods.target(),
	lambda self, value: self.setTarget_(value)
)

GSSubstitution.languageTag = property(
	lambda self: self.pyobjc_instanceMethods.languageTag(),
	lambda self, value: self.setLanguageTag_(value)
)

GSSubstitution.scriptTag = property(
	lambda self: self.pyobjc_instanceMethods.scriptTag(),
	lambda self, value: self.setScriptTag_(value)
)

##################################################################################
#
#
#
#           GSGlyph
#
#
#
##################################################################################


def ____GSGlyph____(): pass


'''

:mod:`GSGlyph`
===============================================================================

Implementation of the glyph object.

For details on how to access these glyphs, please see :class:`GSFont.glyphs`

.. class:: GSGlyph([name, autoName=True])

	:param name: The glyph name
	:param autoName: if the name should be converted to nice name

	Properties

		* :attr:`parent`
		* :attr:`layers`
		* :attr:`name`
		* :attr:`unicode`
		* :attr:`unicodes`
		* :attr:`string`
		* :attr:`id`
		* :attr:`category`
		* :attr:`storeCategory`
		* :attr:`subCategory`
		* :attr:`storeSubCategory`
		* :attr:`group`
		* :attr:`groupIdx`
		* :attr:`storeGroup`
		* :attr:`case`
		* :attr:`storeCase`
		* :attr:`script`
		* :attr:`storeScript`
		* :attr:`productionName`
		* :attr:`storeProductionName`
		* :attr:`sortName`
		* :attr:`sortNameKeep`
		* :attr:`storeSortName`
		* :attr:`glyphInfo`
		* :attr:`leftKerningGroup`
		* :attr:`rightKerningGroup`
		* :attr:`leftKerningKey`
		* :attr:`topKerningGroup`
		* :attr:`bottomKerningKey`
		* :attr:`rightKerningKey`
		* :attr:`topKerningKey`
		* :attr:`leftMetricsKey`
		* :attr:`rightMetricsKey`
		* :attr:`widthMetricsKey`
		* :attr:`topMetricsKey`
		* :attr:`bottomMetricsKey`
		* :attr:`export`
		* :attr:`color`
		* :attr:`colorObject`
		* :attr:`note`
		* :attr:`selected`
		* :attr:`mastersCompatible`
		* :attr:`userData`
		* :attr:`smartComponentAxes`
		* :attr:`tags`
		* :attr:`lastChange`

	Functions

		* :meth:`beginUndo`
		* :meth:`copy`
		* :meth:`duplicate`
		* :meth:`endUndo`
		* :meth:`updateGlyphInfo`

	**Properties**
'''

GSGlyph.__new__ = staticmethod(__GSObject__new__)
GSGlyph.__new__.__name__ = "__new__"


def __GSGlyph__init__(self, name: str | None = None, autoName: bool | None = True) -> None:
	if name and isString(name):
		if not autoName:
			self.setName_changeName_(name, autoName)
		else:
			self.setName_(name)


GSGlyph.__init__ = python_method(__GSGlyph__init__)


def __GSGlyph__str__(self):
	return "<GSGlyph \"%s\" with %s layers>" % (self.name, len(self.layers))


GSGlyph.__str__ = python_method(__GSGlyph__str__)


def __GSGlyph__copy__(self: NSObject, memo: Any | None = None) -> Any:
	glyph: GSGlyph = self.copy()
	glyph.initLock()
	return glyph

GSGlyph.mutableCopyWithZone_ = __GSGlyph__copy__
GSGlyph.__copy__ = python_method(__GSGlyph__copy__)
GSGlyph.__deepcopy__ = python_method(__GSGlyph__copy__)

GSGlyph.__eq__ = python_method(lambda self, other: self.isEqualToGlyph_(other))

GSGlyph.parent = property(
	lambda self: self.pyobjc_instanceMethods.parent(),  # was: GSGlyph.instanceMethodForSelector_(NSSelectorFromString("parent")
	lambda self, value: self.setParent_(value)
)

GSGlyph.font = GSGlyph.parent
'''
	.. attribute:: parent

		Reference to the :class:`GSFont` object.

		:type: :class:`GSFont`
'''

GSGlyph.layers = property(
	lambda self: GlyphLayerProxy(self),
	lambda self, value: GlyphLayerProxy(self).setter(value)
)
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
			del font.glyphs['a'].layers[-1]

			# delete currently active layer
			del font.glyphs['a'].layers[font.selectedLayers[0].layerId]
'''


def GSGlyph_setName(self, name):
	if name == self.name:
		pass
	elif (self.parent and name not in self.parent.glyphs) or not self.parent:
		self.setName_changeName_update_validate_(name, False, True, True)
	else:
		raise NameError('The glyph name \"%s\" already exists in the font.' % name)


GSGlyph.name = property(
	lambda self: self.pyobjc_instanceMethods.name(),
	lambda self, value: GSGlyph_setName(self, value)
)
'''
	.. attribute:: name

		The name of the glyph. It will be converted to a "nice name" (afii10017 to A-cy) (you can disable this behavior in font info or the app preference)

		:type: str
'''

GSGlyph.unicode = property(
	lambda self: self.pyobjc_instanceMethods.unicode(),
	lambda self, value: self.setUnicode_(value)
)
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


GSGlyph.unicodes = property(
	lambda self: __glyph__unicode__(self),
	lambda self, value: self.setUnicodes_(value)
)
'''
	.. attribute:: unicodes

		List of Strings‚ with the hex Unicode values of glyph, if encoded.

		:type: list
'''

GSGlyph.production = property(
	lambda self: self.pyobjc_instanceMethods.production(),
	lambda self, value: self.setProduction_(value)
)

GSGlyph.string = property(lambda self: self.charString())
'''
	.. attribute:: string

		String representation of glyph, if encoded.
		This is similar to the string representation that you get when copying glyphs into the clipboard.

		:type: str
'''

GSGlyph.id = property(
	lambda self: str(self.pyobjc_instanceMethods.id()),
	lambda self, value: self.setId_(value)
)
'''
	.. attribute:: id

		An unique identifier for each glyph

		:type: str
'''

GSGlyph.locked = property(
	lambda self: bool(self.pyobjc_instanceMethods.locked()),
	lambda self, value: self.setLocked_(value)
)
'''
	.. attribute:: locked

		If the glyph is locked

		:type: bool
'''

GSGlyph.category = property(
	lambda self: self.pyobjc_instanceMethods.category(),
	lambda self, value: self.setCategory_(value)
)
'''
	.. attribute:: category

		The category of the glyph. e.g. ‘Letter’, ‘Symbol’
		Setting only works if :attr:`GSGlyph.storeCategory` is set (see below).

		:type: str
'''

GSGlyph.storeCategory = property(
	lambda self: bool(self.pyobjc_instanceMethods.storeCategory()),
	lambda self, value: self.setStoreCategory_(value)
)
'''
	.. attribute:: storeCategory

		Set to True in order to manipulate the :attr:`GSGlyph.category` of the glyph (see above).
		Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.

		:type: bool
'''

GSGlyph.subCategory = property(
	lambda self: self.pyobjc_instanceMethods.subCategory(),
	lambda self, value: self.setSubCategory_(value)
)
'''
	.. attribute:: subCategory

		The subCategory of the glyph. e.g. ‘Currency’, ‘Math’
		Setting it only works if :attr:`GSGlyph.storeSubCategory` is set (see below).

		:type: str
'''

GSGlyph.storeSubCategory = property(
	lambda self: bool(self.pyobjc_instanceMethods.storeSubCategory()),
	lambda self, value: self.setStoreSubCategory_(value)
)
'''
	.. attribute:: storeSubCategory
		Set to True in order to manipulate the :attr:`GSGlyph.subCategory` of the glyph (see above).
		Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.

		:type: bool
'''

GSGlyph.groupIdx = property(
	lambda self: self.pyobjc_instanceMethods.groupIdx(),
	lambda self, value: self.setGroupIdx_(value)
)
'''
	.. attribute:: storeGroupIdx

		:type: int

		.. versionadded:: 4
'''

GSGlyph.group = property(
	lambda self: self.pyobjc_instanceMethods.group(),
	lambda self, value: self.setGroup_(value)
)
'''
	.. attribute:: storeGroup

		:type: str

		.. versionadded:: 4
'''

GSGlyph.storeGroup = property(
	lambda self: bool(self.pyobjc_instanceMethods.storeGroup()),
	lambda self, value: self.setStoreGroup_(value)
)
'''
	.. attribute:: storeStoreGroup

		:type: bool

				.. versionadded:: 4
'''

GSGlyph.case = property(
	lambda self: self.pyobjc_instanceMethods.case(),
	lambda self, value: self.setCase_(value)
)
'''
	.. attribute:: case

		e.g: GSUppercase, GSLowercase, GSSmallcaps

		:type: int

		.. versionadded:: 3
'''

GSGlyph.storeCase = property(
	lambda self: bool(self.pyobjc_instanceMethods.storeCase()),
	lambda self, value: self.setStoreCase_(value)
)
'''
	.. attribute:: storeCase
		Set to True in order to manipulate the :attr:`GSGlyph.case` of the glyph (see above).
		Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.

		:type: bool

		.. versionadded:: 3
'''

GSGlyph.direction = property(
	lambda self: self.pyobjc_instanceMethods.direction(),
	lambda self, value: self.setDirection_(value)
)
'''
	.. attribute:: direction

		Writing direction.

		See `Writing Directions`_

		:type: integer

		.. code-block:: python
			glyph.direction = GSRTL

		.. versionadded:: 3
'''

GSGlyph.storeDirection = property(
	lambda self: bool(self.pyobjc_instanceMethods.storeDirection()),
	lambda self, value: self.setStoreDirection_(value)
)
'''
	.. attribute:: storeDirection
		Set to True in order to manipulate the :attr:`GSGlyph.direction` of the glyph (see above).
		Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.

		:type: bool

		.. versionadded:: 3
'''

GSGlyph.script = property(
	lambda self: self.pyobjc_instanceMethods.script(),
	lambda self, value: self.setScript_(value)
)
'''
	.. attribute:: script

		The script of the glyph, e.g., 'latin', 'arabic'.
		Setting only works if :attr:`GSGlyph.storeScript` is set (see below).

		:type: str
'''

GSGlyph.storeScript = property(
	lambda self: bool(self.pyobjc_instanceMethods.storeScript()),
	lambda self, value: self.setStoreScript_(value)
)
'''
	.. attribute:: storeScript
		Set to True in order to manipulate the :attr:`GSGlyph.script` of the glyph (see above).
		Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.

		:type: bool
'''

GSGlyph.productionName = property(
	lambda self: self.pyobjc_instanceMethods.production(),
	lambda self, value: self.setProduction_(value)
)
'''
	.. attribute:: productionName
		The productionName of the glyph.
		Setting only works if :attr:`GSGlyph.storeProductionName` is set (see below).

		:type: str
'''

GSGlyph.storeProductionName = property(
	lambda self: bool(self.storeProduction()),
	lambda self, value: self.setStoreProduction_(value)
)
'''
	.. attribute:: storeProductionName
		Set to True in order to manipulate the :attr:`GSGlyph.productionName` of the glyph (see above).
		Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.

		:type: bool
'''

GSGlyph.tags = property(
	lambda self: GlyphsTagsProxy(self),
	lambda self, value: GlyphsTagsProxy(self).setter(value)
)
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

GSGlyph.sortName = property(
	lambda self: self.pyobjc_instanceMethods.sortName(),
	lambda self, value: self.setSortName_(value)
)
'''
	.. attribute:: sortName
		Alternative name of glyph used for sorting in UI.

		:type: str
'''

GSGlyph.sortNameKeep = property(
	lambda self: self.pyobjc_instanceMethods.sortNameKeep(),
	lambda self, value: self.setSortNameKeep_(value)
)
'''
	.. attribute:: sortNameKeep
		Alternative name of glyph used for sorting in UI, when using 'Keep Alternates Next to Base Glyph' from Font Info.
		see :attr:`GSGlyph.storeSortName`
		:type: str
'''

GSGlyph.storeSortName = property(
	lambda self: bool(self.pyobjc_instanceMethods.storeSortName()),
	lambda self, value: self.setStoreSortName_(value)
)
'''
	.. attribute:: storeSortName
		Set to True in order to manipulate the :attr:`GSGlyph.sortName` and :attr:`GSGlyph.sortNameKeep` of the glyph (see above).
		Makes it possible to ship custom glyph data inside a .glyphs file without a separate GlyphData file. Same as Cmd-Alt-i dialog in UI.

		:type: bool
'''


def __GSGlyph_glyphDataEntryString__(self) -> str:
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
	return '	<glyph unicode="%s" name="%s" %scategory="%s" %sscript="%s" description="" %s%s%s/>' % (
		Unicode, self.name, Decompose, self.category, SubCategory, self.script, Production, Anchors, Accents)


GSGlyph.glyphDataEntryString = python_method(__GSGlyph_glyphDataEntryString__)

GSGlyph.leftKerningGroup = property(
	lambda self: self.pyobjc_instanceMethods.leftKerningGroup(),
	lambda self, value: self.setLeftKerningGroup_(NSStr(value))
)
'''
	.. attribute:: leftKerningGroup
		The leftKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.

		:type: str
'''
GSGlyph.rightKerningGroup = property(
	lambda self: self.pyobjc_instanceMethods.rightKerningGroup(),
	lambda self, value: self.setRightKerningGroup_(NSStr(value))
)
'''
	.. attribute:: rightKerningGroup
		The rightKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.

		:type: str'''

GSGlyph.topKerningGroup = property(
	lambda self: self.pyobjc_instanceMethods.topKerningGroup(),
	lambda self, value: self.setTopKerningGroup_(NSStr(value))
)
'''
	.. attribute:: topKerningGroup
		The topKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.

		:type: str'''

GSGlyph.bottomKerningGroup = property(
	lambda self: self.pyobjc_instanceMethods.bottomKerningGroup(),
	lambda self, value: self.setBottomKerningGroup_(NSStr(value))
)
'''
	.. attribute:: bottomKerningGroup
		The bottomKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.

		:type: str'''


def __GSGlyph_leftKerningKey__(self):
	if self.leftKerningGroupId():
		return self.leftKerningGroupId()
	else:
		return self.name


GSGlyph.leftKerningKey = property(lambda self: __GSGlyph_leftKerningKey__(self))
'''
	.. attribute:: leftKerningKey
		The key to be used with the kerning functions (:meth:`GSFont.kerningForPair()`, :meth:`GSFont.setKerningForPair()`, :meth:`GSFont.removeKerningForPair()`).

		If the glyph has a :attr:`leftKerningGroup <GSGlyph.leftKerningGroup>` attribute, the internally used `@MMK_R_xx` notation will be returned (note that the R in there stands for the right side of the kerning pair for LTR fonts, which corresponds to the left kerning group of the glyph). If no group is given, the glyph’s name will be returned.

		:type: str

		.. code-block:: python
			# Set kerning for 'T' and all members of kerning class 'a'
			# For LTR fonts, always use the .rightKerningKey for the first (left) glyph of the pair, .leftKerningKey for the second (right) glyph.
			font.setKerningForPair(font.selectedFontMaster.id, font.glyphs['T'].rightKerningKey, font.glyphs['a'].leftKerningKey, -60)

			# which corresponds to:
			font.setKerningForPair(font.selectedFontMaster.id, 'T', '@MMK_R_a', -60)
'''


def __GSGlyph_rightKerningKey__(self):
	if self.rightKerningGroupId():
		return self.rightKerningGroupId()
	else:
		return self.name


GSGlyph.rightKerningKey = property(lambda self: __GSGlyph_rightKerningKey__(self))
'''
	.. attribute:: rightKerningKey
		The key to be used with the kerning functions (:meth:`GSFont.kerningForPair()`, :meth:`GSFont.setKerningForPair()`:meth:`GSFont.removeKerningForPair()`).

		If the glyph has a :attr:`rightKerningGroup <GSGlyph.rightKerningGroup>` attribute, the internally used `@MMK_L_xx` notation will be returned (note that the L in there stands for the left side of the kerning pair for LTR fonts, which corresponds to the right kerning group of the glyph). If no group is given, the glyph’s name will be returned.

		See above for an example.

		:type: str

		.. versionadded:: 2.4
'''


def __GSGlyph_topKerningKey__(self):
	if self.topKerningGroupId():
		return self.topKerningGroupId()
	else:
		return self.name


GSGlyph.topKerningKey = property(lambda self: __GSGlyph_topKerningKey__(self))
'''
	.. attribute:: topKerningKey
		The key to be used with the kerning functions (:meth:`GSFont.kerningForPair()`, :meth:`GSFont.setKerningForPair()`, :meth:`GSFont.removeKerningForPair()`).

		.. versionadded:: 3
'''


def __GSGlyph_bottomKerningKey__(self):
	if self.bottomKerningGroupId():
		return self.bottomKerningGroupId()
	else:
		return self.name


GSGlyph.bottomKerningKey = property(lambda self: __GSGlyph_bottomKerningKey__(self))
'''
	.. attribute:: bottomKerningKey
		The key to be used with the kerning functions (:meth:`GSFont.kerningForPair()`, :meth:`GSFont.setKerningForPair()`, :meth:`GSFont.removeKerningForPair()`).

		.. versionadded:: 3
'''

GSGlyph.leftMetricsKey = property(
	lambda self: self.pyobjc_instanceMethods.leftMetricsKey(),
	lambda self, value: self.setLeftMetricsKey_(NSStr(value))
)
'''
	.. attribute:: leftMetricsKey
		The leftMetricsKey of the glyph. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str
'''

GSGlyph.rightMetricsKey = property(
	lambda self: self.pyobjc_instanceMethods.rightMetricsKey(),
	lambda self, value: self.setRightMetricsKey_(NSStr(value))
)
'''
	.. attribute:: rightMetricsKey
		The rightMetricsKey of the glyph. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str
'''

GSGlyph.widthMetricsKey = property(
	lambda self: self.pyobjc_instanceMethods.widthMetricsKey(),
	lambda self, value: self.setWidthMetricsKey_(NSStr(value))
)
'''
	.. attribute:: widthMetricsKey
		The widthMetricsKey of the glyph. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str
'''

GSGlyph.topMetricsKey = property(lambda self: self.pyobjc_instanceMethods.topMetricsKey(),
								   lambda self, value: self.setTopMetricsKey_(NSStr(value)))
'''
	.. attribute:: topMetricsKey
		The topMetricsKey of the glyph. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str

		.. versionadded:: 3.4
'''

GSGlyph.bottomMetricsKey = property(lambda self: self.pyobjc_instanceMethods.bottomMetricsKey(),
								   lambda self, value: self.setBottomMetricsKey_(NSStr(value)))
'''
	.. attribute:: bottomMetricsKey
		The bottomMetricsKey of the glyph. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str

		.. versionadded:: 3.4
'''

GSGlyph.export = property(
	lambda self: bool(self.pyobjc_instanceMethods.export()),
	lambda self, value: self.setExport_(value)
)
'''
	.. attribute:: export

		Defines whether glyph will export upon font generation

		:type: bool
'''


def __GSGlyph_getColorIndex__(self):
	color = self.colorIndex()
	if color > 20 or color < 0:
		return None
	return color


def __GSGlyph_setColorIndex__(self, value):
	if value is None or value > 0xff:
		value = 0xff
	self.setColorIndex_(value)


GSGlyph.color = property(
	lambda self: __GSGlyph_getColorIndex__(self),
	lambda self, value: __GSGlyph_setColorIndex__(self, value)
)
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


def __GSGlyph_setColor(self, colorValue: tuple | list | NSColor) -> None:
	if isinstance(colorValue, (tuple, list)):
		if max(colorValue) > 1:
			colorValue = [c / 255.0 if c > 1 else c for c in colorValue]
		colorValue = list(colorValue)
		colorValue.extend((1, 1, 1))
		colorValue = NSColor.colorWithDeviceRed_green_blue_alpha_(*colorValue[:4])
	self.setColor_(colorValue)


GSGlyph.colorObject = property(
	lambda self: self.pyobjc_instanceMethods.color(),
	lambda self, value: __GSGlyph_setColor(self, value)
)
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
			>> 0.617805719376 0.958198726177 0.309286683798

			print(round(R * 256), int(G * 256), int(B * 256))
			>> 158 245 245

			# Draw layer
			glyph.layers[0].bezierPath.fill()

			# set the glyph color.

			glyph.colorObject = NSColor.colorWithDeviceRed_green_blue_alpha_(247.0 / 255.0, 74.0 / 255.0, 62.9 / 255.0, 1)
			# or:
			glyph.colorObject = (247.0, 74.0, 62.9)  # max 255.0
			# or:
			glyph.colorObject = (247.0, 74.0, 62.9, 1)  # with alpha
			# or:
			glyph.colorObject = (0.968, 0.29, 0.247, 1)  # max 1.0
'''

GSGlyph.note = property(
	lambda self: self.pyobjc_instanceMethods.note(),
	lambda self, value: self.setNote_(value)
)
'''
	.. attribute:: note

		:type: str
'''


def __GSGlyph_getSelected__(self):
	Doc = self.parent.parent
	return Doc.windowController().glyphsController().selectedObjects().containsObject_(self)


def __GSGlyph_setSelected__(self, isSelected):
	ArrayController = self.parent.parent.windowController().glyphsController()
	if isSelected:
		ArrayController.addSelectedObjects_([self])
	else:
		ArrayController.removeSelectedObjects_([self])


GSGlyph.selected = property(
	lambda self: __GSGlyph_getSelected__(self),
	lambda self, value: __GSGlyph_setSelected__(self, value)
)
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

GSGlyph.mastersCompatible = property(
	lambda self: bool(self.pyobjc_instanceMethods.mastersCompatible())
)
'''
	.. attribute:: mastersCompatible
		Return True when all layers in this glyph are compatible (same components, anchors, paths etc.)

		:type: bool
'''

GSGlyph.userData = property(
	lambda self: UserDataProxy(self),
	lambda self, value: UserDataProxy(self).setter(value)
)
add_type(GSGlyph, "userData", dict)
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

GSGlyph.axes = property(
	lambda self: FontAxesProxy(self),
	lambda self, value: FontAxesProxy(self).setter(value)
)
add_type(GSGlyph, 'axes', List[GSAxis])
'''
	.. attribute:: axes

		Collection of :class:`GSAxis`:

		.. code-block:: python
			for axis in font.axes:
			    print(axis)

			# to add a new axis
			axis = GSAxis()
			axis.name = "Some custom Axis"
			axis.axisTag = "SCAX"
			glyph.axes.append(axis)

			# to delete an axis
			del glyph.axes[0]

						glyph.axes.remove(someAxis)

		:type: list

		.. versionadded:: 4
'''


def __GSGlyph_getSmartComponentAxes__(self):
	print("!! smartComponentAxes are deprecated. Please use glyph.axes")
	return self.axes

def __GSGlyph_setSmartComponentAxes__(self, axes):
	print("smartComponentAxes are deprecated. Please use glyph.axes")
	self.axes = axes

GSGlyph.smartComponentAxes = property(
	lambda self: __GSGlyph_getSmartComponentAxes__(self),
	lambda self, value: __GSGlyph_setSmartComponentAxes__(self, value)
)


def __GSGlyph__lastChange__(self):
	try:
		return datetime.datetime.fromtimestamp(self.pyobjc_instanceMethods.lastChange().timeIntervalSince1970())
	except:
		return None


GSGlyph.lastChange = property(lambda self: __GSGlyph__lastChange__(self))
add_type(GSGlyph, "lastChange", datetime)
'''
	.. attribute:: lastChange
		Change date when glyph was last changed as datetime.

		Check Python’s :mod:`time` module for how to use the timestamp.
'''
'''
	**Functions**

	.. function:: copy()

		Returns a full copy of the glyph

'''


def __GSGlyph_BeginUndo__(self) -> None:
	self.undoManager().beginUndoGrouping()


GSGlyph.beginUndo = python_method(__GSGlyph_BeginUndo__)
'''
	.. function:: beginUndo()

		Call this before you do a longer running change to the glyph. Be extra careful to call :meth:`glyph.endUndo() <GSGlyph.endUndo()>` when you are finished.
'''


def __GSGlyph_EndUndo__(self) -> None:
	self.undoManager().endUndoGrouping()


GSGlyph.endUndo = python_method(__GSGlyph_EndUndo__)
'''
	.. function:: endUndo()

		This closes a undo group that was opened by a previous call of :meth:`glyph.beginUndo() <GSGlyph.beginUndo()>` Make sure that you call this for each `beginUndo()` call.
'''


def __GSGlyph_updateGlyphInfo__(self, changeName: bool | None = True) -> None:
	if self.parent is not None:
		self.parent.glyphsInfo().updateGlyphInfo_changeName_(self, changeName)
	else:
		GSGlyphsInfo.sharedManager().updateGlyphInfo_changeName_(self, changeName)


GSGlyph.updateGlyphInfo = python_method(__GSGlyph_updateGlyphInfo__)
'''
	.. function:: updateGlyphInfo(changeName = True)

		Updates all information like name, unicode etc. for this glyph.
'''


def __GSGlyph_Duplicate__(self, name: str | None = None) -> GSGlyph:

	newGlyph = self.copyWithOptions_(3)  # option: 1 (masters) + 2 (special) layers
	if newGlyph.unicode:
		newGlyph.unicode = None
	if name:
		newGlyph.name = name
	else:
		newGlyph.name = self.parent.saveNameForName_(newGlyph.name)  # will add a .00X suffix
	newGlyph.initLock()
	self.parent.glyphs.append(newGlyph)
	return newGlyph


GSGlyph.duplicate = python_method(__GSGlyph_Duplicate__)
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


def ____GSLayer____(): pass


'''

:mod:`GSLayer`
===============================================================================

Implementation of the layer object.

For details on how to access these layers, please see :attr:`GSGlyph.layers`

.. class:: GSLayer()

	Properties

		* :attr:`parent`
		* :attr:`name`
		* :attr:`master`
		* :attr:`associatedMasterId`
		* :attr:`layerId`
		* :attr:`attributes`
		* :attr:`color`
		* :attr:`colorObject`
		* :attr:`shapes`
		* :attr:`guides`
		* :attr:`annotations`
		* :attr:`hints`
		* :attr:`anchors`
		* :attr:`components`
		* :attr:`paths`
		* :attr:`selection`
		* :attr:`LSB`
		* :attr:`RSB`
		* :attr:`TSB`
		* :attr:`BSB`
		* :attr:`width`
		* :attr:`vertWidth`
		* :attr:`leftMetricsKey`
		* :attr:`rightMetricsKey`
		* :attr:`widthMetricsKey`
		* :attr:`topMetricsKey`
		* :attr:`bottomMetricsKey`
		* :attr:`bounds`
		* :attr:`selectionBounds`
		* :attr:`background`
		* :attr:`backgroundImage`
		* :attr:`bezierPath`
		* :attr:`openBezierPath`
		* :attr:`userData`
		* :attr:`smartComponentPoleMapping`
		* :attr:`isSpecialLayer`
		* :attr:`isMasterLayer`
		* :attr:`isBraceLayer`
		* :attr:`isBracketLayer`
		* :attr:`italicAngle`
		* :attr:`visible`

	Functions

		* :meth:`addMissingAnchors`
		* :meth:`addNodesAtExtremes`
		* :meth:`applyTransform`
		* :meth:`beginChanges`
		* :meth:`clear`
		* :meth:`clearSelection`
		* :meth:`compareString`
		* :meth:`connectAllOpenPaths`
		* :meth:`copy`
		* :meth:`copyDecomposedLayer`
		* :meth:`correctPathDirection`
		* :meth:`cutBetweenPoints`
		* :meth:`decomposeComponents`
		* :meth:`decomposeCorners`
		* :meth:`endChanges`
		* :meth:`intersections`
		* :meth:`intersectionsBetweenPoints`
		* :meth:`reinterpolate`
		* :meth:`removeOverlap`
		* :meth:`roundCoordinates`
		* :meth:`swapForegroundWithBackground`
		* :meth:`syncMetrics`
		* :meth:`transform`

	**Properties**
'''

GSLayer.__new__ = staticmethod(__GSObject__new__)
GSLayer.__new__.__name__ = "__new__"
GSLayer.__init__ = python_method(__empty__init__)


GSLayer.mutableCopyWithZone_ = __GSObject__copy__

GSLayer.__eq__ = python_method(lambda self, other: self.isEqualToLayer_(other))

GSLayer.parent = property(
	lambda self: self.pyobjc_instanceMethods.parent(),
	lambda self, value: self.setParent_(value)
)

GSBackgroundLayer.parent = property(
	lambda self: self.pyobjc_instanceMethods.parent(),
	lambda self, value: self.setParent_(value)
)

GSControlLayer.parent = property(lambda self: self.pyobjc_instanceMethods.parent())

GSControlLayer.bezierPath = property(lambda self: self.pyobjc_instanceMethods.bezierPath())
'''
	.. attribute:: parent

		Reference to the :class:`glyph <GSGlyph>` object that this layer is attached to.

		:type: :class:`GSGlyph`
'''

GSLayer.name = property(
	lambda self: self.nameUI(),
	lambda self, value: self.setName_(value),
	doc="Name of layer."
)
add_type(GSLayer, 'name', str)

GSBackgroundLayer.name = property(
	lambda self: self.pyobjc_instanceMethods.name(),
	lambda self, value: self.setName_(value)
)
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
GSLayer.associatedMasterId = property(
	GSLayer.instanceMethodForSelector_(NSSelectorFromString("associatedMasterId")),
	lambda self, value: self.setAssociatedMasterId_(value)
)
GSBackgroundLayer.associatedMasterId = property(
	GSBackgroundLayer.instanceMethodForSelector_(NSSelectorFromString("associatedMasterId")),
	lambda self, value: self.setAssociatedMasterId_(value)
)
GSBackgroundLayer.associatedMasterId = GSLayer.associatedMasterId

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

GSLayer.layerId = property(
	GSLayer.instanceMethodForSelector_(NSSelectorFromString("layerId")),
	lambda self, value: self.setLayerId_(value)
)
GSBackgroundLayer.layerId = GSLayer.layerId
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
			>> FBCA074D-FCF3-427E-A700-7E318A949AE5

			# access a layer by this ID
			layer = font.glyphs["a"].layers[id]
			layer = font.glyphs["a"].layers['FBCA074D-FCF3-427E-A700-7E318A949AE5']

			# for master layers, use ID of masters
			layer = font.glyphs["a"].layers[font.masters[0].id]
'''

GSLayer.attributes = property(
	lambda self: AttributesProxy(self),
	lambda self, value: self.setAttributes_(value)
)
'''
	.. attribute:: attributes

		layer attributes like :samp:`axisRules`, :samp:`coordinates`, :samp:`colorPalette`, :samp:`sbixSize`, :samp:`color`, :samp:`svg`

		.. code-block:: python

			axis = font.axes[0]
			layer.attributes["axisRules"] = {axis.axisId: {'min': 100}}
			layer.attributes["coordinates"] = {axis.axisId: 99}
			layer.attributes["colorPalette"] = 2  # This makes the layer a CPAL layer for color index 2

		:type: dict
'''


def __GSLayer__axesValuesArrayFontAxes__(self):
	return self.axesValuesArrayFontAxes_(self.font().axes.values())


GSLayer.axesValues = property(lambda self: __GSLayer__axesValuesArrayFontAxes__(self))

'''
	.. attribute:: axesValues
		a list of floats, one per axis

		:type: list
'''

GSLayer.color = property(
	lambda self: __GSGlyph_getColorIndex__(self),
	lambda self, value: __GSGlyph_setColorIndex__(self, value)
)
'''
	.. attribute:: color

		Color marking of glyph in UI

		:type: int

		.. code-block:: python
			glyph.color = 0     # red
			glyph.color = 1     # orange
			glyph.color = 2     # brown
			glyph.color = 3     # yellow
			glyph.color = 4     # light green
			glyph.color = 5     # dark green
			glyph.color = 6     # light blue
			glyph.color = 7     # dark blue
			glyph.color = 8     # purple
			glyph.color = 9     # magenta
			glyph.color = 10    # light gray
			glyph.color = 11    # charcoal
			glyph.color = None  # not colored, white (before version 1235, use -1)
'''

GSLayer.colorObject = property(
	lambda self: self.pyobjc_instanceMethods.color(),
	lambda self, value: self.setColor_(value)
)
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
			>> 0.617805719376 0.958198726177 0.309286683798

			print(round(R * 256), int(G * 256), int(B * 256))
			>> 158 245 245

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

GSLayer.guides = property(
	lambda self: LayerGuidesProxy(self),
	lambda self, value: LayerGuidesProxy(self).setter(value)
)
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
			del layer.guides[0]

			# copy guides from another layer
			import copy
			layer.guides = copy.copy(anotherlayer.guides)
'''

GSLayer.annotations = property(
	lambda self: LayerAnnotationProxy(self),
	lambda self, value: LayerAnnotationProxy(self).setter(value)
)
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
			del layer.annotations[0]

			# copy annotations from another layer
			import copy
			layer.annotations = copy.copy(anotherLayer.annotations)
'''

GSLayer.hints = property(
	lambda self: LayerHintsProxy(self),
	lambda self, value: LayerHintsProxy(self).setter(value)
)
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
			# change behavior of hint here, like its attachment nodes
			layer.hints.append(newHint)

			# delete hint
			del layer.hints[0]

			# copy hints from another layer
			import copy
			layer.hints = copy.copy(anotherlayer.hints)
			# remember to reconnect the hints’ nodes with the new layer’s nodes
'''

GSLayer.anchors = property(
	lambda self: LayerAnchorsProxy(self),
	lambda self, value: LayerAnchorsProxy(self).setter(value)
)
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
			del layer.anchors['top']

			# copy anchors from another layer
			import copy
			layer.anchors = copy.copy(anotherlayer.anchors)
'''

GSLayer.shapes = property(
	lambda self: LayerShapesProxy(self),
	lambda self, value: LayerShapesProxy(self).setter(value)
)
'''
	.. attribute:: shapes

		List of :class:`GSShape` objects. That are most likely :class:`GSPath` or :class:`GSComponent`

		:type: list

		.. code-block:: python
			# access all shapes
			for shape in layer.shapes:
			    print(shape)

			# delete shape
			del layer.shapes[0]

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
'''

GSLayer.selection = property(
	lambda self: LayerSelectionProxy(self),
	lambda self, value: LayerSelectionProxy(self).setter(value)
)

'''
	.. attribute:: selection

		List of all selected objects in the glyph.

		This list contains **all selected items**, including **nodes**, **anchors**, **guides** etc.
		If you want to work specifically with nodes, for instance, you may want to cycle through the nodes (or anchors etc.) and check whether they are selected. See example below.

		:type: list

		.. code-block:: python
			# access all selected nodes
			for path in layer.paths:
			    for node in path.nodes:  # (or path.anchors etc.)
			        print(node.selected)

			# clear selection
			layer.clearSelection()
'''

GSLayer.LSB = property(
	lambda self: self.pyobjc_instanceMethods.LSB(),
	lambda self, value: self.setLSB_(float(value))
)
'''
	.. attribute:: LSB
		Left sidebearing

		:type: float
'''

GSLayer.RSB = property(
	lambda self: self.pyobjc_instanceMethods.RSB(),
	lambda self, value: self.setRSB_(float(value))
)
'''
	.. attribute:: RSB
		Right sidebearing

		:type: float
'''

GSLayer.TSB = property(
	lambda self: self.pyobjc_instanceMethods.TSB(),
	lambda self, value: self.setTSB_(float(value))
)
'''
	.. attribute:: TSB
		Top sidebearing

		:type: float
'''

GSLayer.BSB = property(
	lambda self: self.pyobjc_instanceMethods.BSB(),
	lambda self, value: self.setBSB_(float(value))
)
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


GSLayer.width = property(
	lambda self: self.pyobjc_instanceMethods.width(),
	GSLayer__setWidth
)

GSBackgroundLayer.width = property(
	lambda self: self.pyobjc_instanceMethods.width(),
	lambda self, value: None
)
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


GSLayer.vertWidth = property(
	lambda self: __GSLayer_vertWidth__(self),
	lambda self, value: __GSLayer_setVertWidth__(self, value)
)
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


GSLayer.vertOrigin = property(
	lambda self: __GSLayer_vertOrigin__(self),
	lambda self, value: __GSLayer_setVertOrigin__(self, value)
)
'''
	.. attribute:: vertOrigin
		Layer vertical origin

		set it to None to reset it to default

		:type: float

		.. versionadded:: 2.6.2
'''

GSLayer.ascender = property(
	lambda self: self.pyobjc_instanceMethods.ascender()
)
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

GSLayer.leftMetricsKey = property(
	lambda self: self.pyobjc_instanceMethods.leftMetricsKey(),
	lambda self, value: self.setLeftMetricsKey_(NSStr(value)),
	doc="The leftMetricsKey of the layer.\n\nThis is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph."
)
'''
	.. attribute:: leftMetricsKey
		The leftMetricsKey of the layer. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str
'''

GSLayer.rightMetricsKey = property(
	lambda self: self.pyobjc_instanceMethods.rightMetricsKey(),
	lambda self, value: self.setRightMetricsKey_(NSStr(value))
)
'''
	.. attribute:: rightMetricsKey
		The rightMetricsKey of the layer. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str
'''

GSLayer.widthMetricsKey = property(
	lambda self: self.pyobjc_instanceMethods.widthMetricsKey(),
	lambda self, value: self.setWidthMetricsKey_(NSStr(value))
)
'''
	.. attribute:: widthMetricsKey
		The widthMetricsKey of the layer. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str
'''

GSLayer.topMetricsKey = property(
	lambda self: self.pyobjc_instanceMethods.topMetricsKey(),
	lambda self, value: self.setTopMetricsKey_(NSStr(value))
)
'''
	.. attribute:: topMetricsKey
		The topMetricsKey of the glyph. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str

		.. versionadded:: 3.4
'''

GSLayer.bottomMetricsKey = property(
	lambda self: self.pyobjc_instanceMethods.bottomMetricsKey(),
	lambda self, value: self.setBottomMetricsKey_(NSStr(value))
)
'''
	.. attribute:: bottomMetricsKey
		The bottomMetricsKey of the glyph. This is a reference to another glyph by name or formula. It is used to synchronize the metrics with the linked glyph.

		:type: str

		.. versionadded:: 3.4
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

GSLayer.metrics = property(lambda self: self.pyobjc_instanceMethods.metrics())
'''
	.. attribute:: metrics

		The metrics layer are a list of horizontal metrics filtered specifically for this layer. Use this instead of :attr:`master.alignmentZones <GSFontMaster.alignmentZones>`.

		:type: :class:`GSMetricStore`

		.. versionadded:: 3.0.1
'''

GSLayer.background = property(
	lambda self: self.pyobjc_instanceMethods.background(),
	lambda self, value: self.setBackground_(value)
)

GSBackgroundLayer.background = property(lambda self: self.pyobjc_instanceMethods.background())

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

GSLayer.backgroundImage = property(
	lambda self: self.pyobjc_instanceMethods.backgroundImage(),
	lambda self, value: self.setBackgroundImage_(value)
)
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


def __GSLayer__completeBezierPath(self):
	path = self.pyobjc_instanceMethods.drawBezierPath()
	if path:
		path.autorelease()
	return path


GSLayer.completeBezierPath = property(lambda self: __GSLayer__completeBezierPath(self))
'''
	.. attribute:: completeBezierPath
		The layer as an NSBezierPath object including paths from components. Useful for drawing glyphs in plug-ins.

		:type: NSBezierPath

		.. code-block:: python
			# draw the path into the Edit view
			NSColor.redColor().set()
			layer.completeBezierPath.fill()
'''


def __GSLayer__completeOpenBezierPath(self):
	path = self.pyobjc_instanceMethods.drawOpenBezierPath()
	return path


GSLayer.completeOpenBezierPath = property(lambda self: __GSLayer__completeOpenBezierPath(self))
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
add_type(GSLayer, 'isSpecialLayer', bool)
'''
	.. attribute:: isSpecialLayer
		If the layer is a brace, bracket or a smart component layer

		:type: bool
'''

GSLayer.isMasterLayer = property(GSLayer.instanceMethodForSelector_(NSSelectorFromString("isMasterLayer")))
'''
	.. attribute:: isMasterLayer
		If it is a master layer

		:type: bool
'''

GSLayer.isBraceLayer = property(GSLayer.instanceMethodForSelector_(NSSelectorFromString("isBraceLayer")))
'''
	.. attribute:: isBraceLayer
		If it is a intermediate layer

		:type: bool
'''

GSLayer.isBracketLayer = property(GSLayer.instanceMethodForSelector_(NSSelectorFromString("isBracketLayer")))
'''
	.. attribute:: isBracketLayer
		If it is a alternate layer

		:type: bool
'''

GSLayer.italicAngle = property(lambda self: float(self.pyobjc_instanceMethods.italicAngle()))
'''
	.. attribute:: italicAngle
		The italic angle that applies to this layer

		:type: float
'''

GSLayer.visible = property(
	lambda self: self.pyobjc_instanceMethods.visible(),
	lambda self, value: self.setVisible_(value)
)
'''
	.. attribute:: visible

		if the layer is visible (the eye icon in the layer panel)

		:type: bool
'''

GSLayer.userData = property(
	lambda self: UserDataProxy(self),
	lambda self, value: UserDataProxy(self).setter(value)
)
add_type(GSLayer, "userData", dict)
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

GSLayer.tempData = property(
	lambda self: TempDataProxy(self),
	lambda self, value: TempDataProxy(self).setter(value)
)
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

def __GSLayer_smartComponentPoleMapping__(self):
	raise NotImplementedError('smartComponentPoleMapping has been removed. Position smart layers in the design space with layer.attributes["coordinates"], a dict keyed by axis.axisId (see glyph.axes).')


GSLayer.smartComponentPoleMapping = property(__GSLayer_smartComponentPoleMapping__)
'''
	**Functions**

	.. function:: copy()

		Returns a full copy of the layer

	.. function:: decomposeComponents()

		Decomposes all components of the layer at once.

	.. function:: decomposeCorners()

		Decomposes all corners of the layer at once.

		.. versionadded:: 2.4

	.. function:: compareString()

		Returns a string representing the outline structure of the glyph, for compatibility comparison.

		:return: The comparison string

		:rtype: str

		.. code-block:: python

			print(layer.compareString())
			>> oocoocoocoocooc_oocoocoocloocoocoocoocoocoocoocoocooc_

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


def __GSLayer_RemoveOverlap__(self, checkSelection: bool | None = False):
	self.removeOverlapCheckSelection_error_(checkSelection, None)


GSLayer.removeOverlap = python_method(__GSLayer_RemoveOverlap__)
'''
	.. function:: removeOverlap([checkSelection=False])

		Joins all contours.

		:param checkSelection: If the selection will be considered. Default: False

	.. function:: roundCoordinates()

		Round the positions of all coordinates to the grid (size of which is set in the Font Info).
'''


def Layer_addNodesAtExtremes(self, force: bool | None = False, checkSelection: bool | None = False):
	self.addExtremePointsForce_checkSelection_(force, checkSelection)


GSLayer.addNodesAtExtremes = python_method(Layer_addNodesAtExtremes)
'''
	.. function:: addNodesAtExtremes([force=False, checkSelection=False])

		Add nodes at layer’s extrema, e.g., top, bottom etc.

		:param force: if points are always added, even if that would distort the shape
		:param checkSelection: only process selected segments
'''


def __GSLayer_applyTransform__(self, transformStruct: tuple | NSAffineTransformStruct | NSAffineTransform) -> None:
	if isinstance(transformStruct, (NSAffineTransformStruct, list, tuple)):
		transform = NSAffineTransform.transform()
		transform.setTransformStruct_(transformStruct)
	else:
		transform = transformStruct
	self.transform_checkForSelection_doComponents_(transform, False, True)


GSLayer.applyTransform = python_method(__GSLayer_applyTransform__)
'''
	.. function:: applyTransform(transform)

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

			from Foundation import NSAffineTransform, NSMidX, NSMidY
			bounds = Layer.bounds
			transform = NSAffineTransform.new()
			transform.translateXBy_yBy_(NSMidX(bounds), NSMidY(bounds))
			transform.rotateByDegrees_(-30)
			transform.translateXBy_yBy_(-NSMidX(bounds), -NSMidY(bounds))
			Layer.applyTransform(transform)

		:param transform: a list of 6 numbers, a NSAffineTransform or a NSAffineTransformStruct
'''


def __GSLayer_transform__(self, transform, selection: bool | None = False, components: bool | None = True):
	self.transform_checkForSelection_doComponents_(transform, selection, components)


GSLayer.transform = python_method(__GSLayer_transform__)
'''
	.. function:: transform(transform, [selection=False, components=True])

		Apply a :attr:`NSAffineTransform` to the layer.

		:param transform: A :attr:`NSAffineTransform`
		:param selection: check selection
		:param components: if components should be transformed

		.. code-block:: python
			transformation = NSAffineTransform()
			transformation.rotate(45, (200, 200))
			layer.transform(transformation)
'''


def __GSLayer_BeginChanges__(self):
	self.stopUpdates()
	undoManager = self.undoManagerCheck()
	if undoManager is not None:
		undoManager.beginUndoGrouping()


GSLayer.beginChanges = python_method(__GSLayer_BeginChanges__)
'''
	.. function:: beginChanges()

		Call this before you do bigger changes to the Layer.
		This will increase performance and prevent undo problems.
		Always call layer.endChanges() if you are finished.
'''


def __GSLayer_EndChanges__(self):
	self.startUpdates()
	undoManager = self.undoManagerCheck()
	if undoManager is not None:
		undoManager.endUndoGrouping()


GSLayer.endChanges = python_method(__GSLayer_EndChanges__)
'''
	.. function:: endChanges()

		Call this if you have called layer.beginChanges before. Make sure to group bot calls properly.
'''


def __GSLayer_CutBetweenPoints__(self, point1: NSPoint, point2: NSPoint):
	GlyphsToolKnifeCls: Type[GlyphsToolKnife] = NSClassFromString("GlyphsToolKnife")
	GlyphsToolKnifeCls.cutPathsInLayer_forPoint_endPoint_(self, point1, point2)


GSLayer.cutBetweenPoints = python_method(__GSLayer_CutBetweenPoints__)
'''
	.. function:: cutBetweenPoints(Point1, Point2)

		Cuts all paths that intersect the line from Point1 to Point2

		:param Point1: one point
		:param Point2: the other point

		.. code-block:: python
			# cut glyph in half horizontally at y=100
			layer.cutBetweenPoints(NSPoint(0, 100), NSPoint(layer.width, 100))

'''
'''
	.. function:: intersections()

		returns a list of all intersections between overlapping paths in the layer.
'''


def __GSLayer_IntersectionsBetweenPoints__(self, point1: NSPoint, point2: NSPoint, components: bool = False, ignoreLocked: bool = False):
	return self.calculateIntersectionsStartPoint_endPoint_decompose_ignoreLocked_(point1, point2, components, ignoreLocked)


GSLayer.intersectionsBetweenPoints = python_method(__GSLayer_IntersectionsBetweenPoints__)

NSConcreteValue.x = property(lambda self: self.pointValue().x)  # type: ignore
NSConcreteValue.y = property(lambda self: self.pointValue().y)  # type: ignore
'''
	.. function:: intersectionsBetweenPoints(Point1, Point2, components: bool | None = False)

		Return all intersection points between a measurement line and the paths in the layer. This is basically identical to the measurement tool in the UI.

		Normally, the first returned point is the starting point, the last returned point is the end point. Thus, the second point is the first intersection, the second last point is the last intersection.

		:param Point1: one point
		:param Point2: the other point
		:param components: if components should be measured. Default: False
		:param ignoreLocked: ignore locked or unfocused paths. Default: False

		.. code-block:: python
			# show all intersections with glyph at y=100
			intersections = layer.intersectionsBetweenPoints((-1000, 100), (layer.width+1000, 100))
			print(intersections)

			# left sidebearing at measurement line
			print(intersections[1].x)

			# right sidebearing at measurement line
			print(layer.width - intersections[-2].x)
'''


def __GSLayer_addMissingAnchors__(self):
	GSGlyphsInfo.sharedManager().updateAnchors_(self)


GSLayer.addMissingAnchors = python_method(__GSLayer_addMissingAnchors__)
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


def __GSControlLayer__new__(typ, *args, **kwargs):
	if len(args) > 0:
		return GSControlLayer.alloc().initWithChar_(args[0])
	else:
		return GSControlLayer.alloc().init()


GSControlLayer.__new__ = staticmethod(__GSControlLayer__new__)
GSControlLayer.__init__ = python_method(__empty__init__)


def __GSControlLayer__str__(self):
	char = self.parent.unicodeChar()
	if char == 10:
		name = "newline"
	elif char == 129:
		name = "placeholder"
	else:
		name = GSGlyphsInfo.sharedManager().niceGlyphNameForName_("uni%.4X" % self.parent.unicodeChar())
	return "<%s \"%s\">" % (self.className(), name)


GSControlLayer.__str__ = python_method(__GSControlLayer__str__)


def __GSControlLayer__newline__():
	return GSControlLayer(10)


GSControlLayer.newline = staticmethod(__GSControlLayer__newline__)


def __GSControlLayer__placeholder__():
	return GSControlLayer(129)


GSControlLayer.placeholder = staticmethod(__GSControlLayer__placeholder__)


def DrawLayerWithPen(self, pen, contours: bool | None = True, components: bool | None = True):
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


def DrawPointsWithPen(self, pen, contours: bool | None = True, components: bool | None = True):
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


def __GSLayer__add__(self, summand: NSPoint | tuple | GSLayer):
	if isinstance(summand, NSPoint):
		transform = NSAffineTransform.new()
		transform.translateXBy_yBy_(summand.x, summand.y)
		newLayer = self.copy()
		newLayer.transform_checkForSelection_doComponents_(transform, False, False)
		return newLayer
	elif isinstance(summand, GSLayer):
		otherLayer: GSLayer = cast(GSLayer, summand)
		if self.compareString() != otherLayer.compareString():
			raise ValueError("Layers are not compatible: %s, %s" % (self.compareString(), otherLayer.compareString()))
		newLayer = self.copy()
		newShapes = NSMutableArray.new()
		for idx in range(len(otherLayer.shapes)):
			shape1 = newLayer.shapes[idx]
			shape2 = otherLayer.shapes[idx]
			newShape = shape1 + shape2
			newShapes.addObject_(newShape)
		newLayer.shapes = newShapes

		if len(self.anchors):
			newAnchors = NSMutableDictionary.new()
			for anchorName in self.anchors.keys():
				anchor1 = newLayer.anchors[anchorName]
				anchor2 = otherLayer.anchors[anchorName]
				newAnchor = anchor1 + anchor2
				newAnchors.setObject_forKey_(newAnchor, anchorName)
			newLayer.anchors = newAnchors

		newLayer.width += otherLayer.width
		return newLayer
	else:
		raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (type(self).__name__, type(summand).__name__))


GSLayer.__add__ = python_method(__GSLayer__add__)


def __GSLayer__i_add__(self, summand: NSPoint | tuple | GSLayer):
	if isinstance(summand, NSPoint):
		transform = NSAffineTransform.new()
		transform.translateXBy_yBy_(summand.x, summand.y)
		self.transform_checkForSelection_doComponents_(transform, False, False)
	elif isinstance(summand, GSLayer):
		otherLayer: GSLayer = cast(GSLayer, summand)
		if self.compareString() != otherLayer.compareString():
			raise ValueError("Layers are not compatible: %s, %s" % (self.compareString(), otherLayer.compareString()))
		for idx in range(len(otherLayer.shapes)):
			shape1 = self.shapes[idx]
			shape2 = otherLayer.shapes[idx]
			shape1 += shape2

		if len(self.anchors):
			for anchorName in self.anchors.keys():
				anchor1 = self.anchors[anchorName]
				anchor2 = otherLayer.anchors[anchorName]
				anchor1 += anchor2

		self.width += otherLayer.width
		return self
	else:
		raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (type(self).__name__, type(summand).__name__))


GSLayer.__iadd__ = python_method(__GSLayer__add__)

def __GSLayer__sub__(self, summand: NSPoint | tuple | GSLayer):
	if isinstance(summand, NSPoint):
		transform = NSAffineTransform.new()
		transform.translateXBy_yBy_(-summand.x, -summand.y)
		newLayer = self.copy()
		newLayer.transform_checkForSelection_doComponents_(transform, False, False)
		return newLayer
	elif isinstance(summand, GSLayer):
		otherLayer: GSLayer = cast(GSLayer, summand)
		if self.compareString() != otherLayer.compareString():
			raise ValueError("Layers are not compatible: %s, %s" % (self.compareString(), otherLayer.compareString()))
		newLayer = self.copy()
		newShapes = NSMutableArray.new()
		for idx in range(len(otherLayer.shapes)):
			shape1 = newLayer.shapes[idx]
			shape2 = otherLayer.shapes[idx]
			newShape = shape1 - shape2
			newShapes.addObject_(newShape)
		newLayer.shapes = newShapes

		if len(self.anchors):
			newAnchors = NSMutableDictionary.new()
			for anchorName in self.anchors.keys():
				anchor1 = newLayer.anchors[anchorName]
				anchor2 = otherLayer.anchors[anchorName]
				newAnchor = anchor1 - anchor2
				newAnchors.setObject_forKey_(newAnchor, anchorName)
			newLayer.anchors = newAnchors

		newLayer.width += otherLayer.width
		return newLayer
	else:
		raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (type(self).__name__, type(summand).__name__))


GSLayer.__sub__ = python_method(__GSLayer__add__)


def __GSLayer__iadd__(self, summand: NSPoint | tuple | GSLayer):
	if isinstance(summand, NSPoint):
		transform = NSAffineTransform.new()
		transform.translateXBy_yBy_(summand.x, summand.y)
		self.transform_checkForSelection_doComponents_(transform, False, False)
	elif isinstance(summand, GSLayer):
		otherLayer: GSLayer = cast(GSLayer, summand)
		if self.compareString() != otherLayer.compareString():
			raise ValueError("Layers are not compatible: %s, %s" % (self.compareString(), otherLayer.compareString()))
		for idx in range(len(otherLayer.shapes)):
			shape1 = self.shapes[idx]
			shape2 = otherLayer.shapes[idx]
			shape1 += shape2

		if len(self.anchors):
			for anchorName in self.anchors.keys():
				anchor1 = self.anchors[anchorName]
				anchor2 = otherLayer.anchors[anchorName]
				anchor1 += anchor2

		self.width += otherLayer.width
		return self
	else:
		raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (type(self).__name__, type(summand).__name__))


GSLayer.__iadd__ = python_method(__GSLayer__iadd__)


def __GSLayer__mul__(self, factor: float):
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

def __GSLayer__imul__(self, factor: float):
	if isinstance(factor, (int, float)):
		transform = NSAffineTransform.new()
		transform.scaleBy_(factor)
		self.width = self.width * factor
		self.transform_checkForSelection_doComponents_(transform, False, True)
		return self
	else:
		raise TypeError("unsupported operand type(s) for *: '%s' and '%s'" % (type(self).__name__, type(factor).__name__))


GSLayer.__imul__ = python_method(__GSLayer__mul__)


def __GSPath__add__(self, summand: NSPoint | tuple | GSLayer):
	if isinstance(summand, NSPoint):
		transform = NSAffineTransform.new()
		transform.translateXBy_yBy_(summand.x, summand.y)
		newPath = self.copy()
		newPath.transform_(transform)
		return newPath
	if isinstance(summand, tuple):
		transform = NSAffineTransform.new()
		transform.translateXBy_yBy_(summand[0], summand[1])
		newPath = self.copy()
		newPath.transform_(transform)
		return newPath
	elif isinstance(summand, GSPath):
		otherPath: GSPath = cast(GSPath, summand)
		if len(self.nodes) != len(otherPath.nodes) or self.closed != otherPath.closed:
			raise ValueError("Paths are not compatible: %s, %s" % (len(self.nodes), len(otherPath.nodes)))
		newPath = self.copy()
		newNodes = NSMutableArray.new()
		for idx in range(len(otherPath.nodes)):
			node1 = newPath.nodes[idx]
			node2 = otherPath.nodes[idx]
			newNode = node1 + node2
			newNodes.addObject_(newNode)
		newPath.nodes = newNodes
		return newPath
	else:
		raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (type(self).__name__, type(summand).__name__))


GSPath.__add__ = python_method(__GSPath__add__)


def __GSPath__i_add__(self, summand: NSPoint | tuple | GSLayer):
	if isinstance(summand, NSPoint):
		transform = NSAffineTransform.new()
		transform.translateXBy_yBy_(summand.x, summand.y)
		self.transform_(transform)
	elif isinstance(summand, tuple):
		transform = NSAffineTransform.new()
		transform.translateXBy_yBy_(summand[0], summand[1])
		self.transform_(transform)
	elif isinstance(summand, GSPath):
		if len(self.nodes) != len(summand.nodes) or self.closed != summand.closed:
			raise ValueError("Paths are not compatible: %s, %s" % (len(self.nodes), len(summand.nodes)))
		for idx in range(len(summand.nodes)):
			node1 = self.nodes[idx]
			node2 = summand.nodes[idx]
			node1 += node2
	else:
		raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (type(self).__name__, type(summand).__name__))
	return self


GSPath.__iadd__ = python_method(__GSPath__i_add__)


def __GSNode__add__(self, summand):
	if isinstance(summand, (NSPoint, tuple)):
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


def __GSNode__i_add__(self, summand):
	if isinstance(summand, (NSPoint, tuple)):
		self.position = addPoints(self.position, summand)
	elif isinstance(summand, GSNode):
		if self.type != summand.type:
			raise ValueError("Nodes are not compatible: %s, %s" % (self.type, summand.type))
		self.position = addPoints(self.position, summand.position)
	else:
		raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (type(self).__name__, type(summand).__name__))
	return self


GSNode.__iadd__ = python_method(__GSNode__i_add__)


def __GSComponent__add__(self, summand):
	if isinstance(summand, (NSPoint, tuple)):
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


def __GSComponent__i_add__(self, summand):
	if isinstance(summand, (NSPoint, tuple)):
		self.position = addPoints(self.position, summand)
	elif isinstance(summand, GSComponent):
		if self.component != summand.component:
			raise ValueError("Components are not compatible: %s, %s" % (self, summand))
		self.position = addPoints(self.position, summand.position)
		self.scale = addPoints(self.scale, summand.scale)
		self.rotation = self.rotation + summand.rotation
	else:
		raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (type(self).__name__, type(summand).__name__))
	return self


GSComponent.__iadd__ = python_method(__GSComponent__i_add__)


def __GSAnchor__add__(self, summand):
	if isinstance(summand, (NSPoint, tuple)):
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


def __GSAnchor__i_add__(self, summand):
	if isinstance(summand, (NSPoint, tuple)):
		self.position = addPoints(self.position, summand)
	elif isinstance(summand, GSAnchor):
		if self.name != summand.name:
			raise ValueError("Anchors are not compatible: %s, %s" % (self, summand))
		self.position = addPoints(self.position, summand.position)
	else:
		raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (type(self).__name__, type(summand).__name__))
	return self


GSAnchor.__iadd__ = python_method(__GSAnchor__i_add__)


##################################################################################
#
#
#
#           GSAnchor
#
#
#
##################################################################################


class ____GSAnchor____():
	""" Marker: Initialization """


'''

:mod:`GSAnchor`
===============================================================================

Implementation of the anchor object.

For details on how to access them, please see :attr:`GSLayer.anchors`

.. class:: GSAnchor([name, position])

	:param name: the name of the anchor
	:param pt: the position of the anchor

	Properties

		* :attr:`position`
		* :attr:`name`
		* :attr:`selected`
		* :attr:`orientation`

	Functions

		* :meth:`copy()`

	**Properties**
'''


def __GSAnchor__init__(self, name: str | None = None, pt: NSPoint | None = None, position: NSPoint | None = None) -> None:
	if pt:
		self.setPosition_(pt)
	if position:
		self.setPosition_(position)
	if name:
		self.setName_(name)


GSAnchor.__init__ = python_method(__GSAnchor__init__)
GSAnchor.__new__ = staticmethod(__GSObject__new__)


def __GSAnchor__str__(self):
	return "<GSAnchor \"%s\" x=%s y=%s>" % (self.name, self.position.x, self.position.y)


GSAnchor.__str__ = python_method(__GSAnchor__str__)

GSAnchor.__eq__ = python_method(lambda self, other: self.isEqualToAnchor_(other))

GSAnchor.mutableCopyWithZone_ = __GSObject__copy__

GSAnchor.position = property(
	lambda self: self.pyobjc_instanceMethods.position(),
	lambda self, value: self.setPosition_(value),
	doc="The position of the anchor."
)
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

GSAnchor.name = property(
	lambda self: self.pyobjc_instanceMethods.name(),
	lambda self, value: self.setName_(value),
	doc="The name of the anchor."
)
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

	.. attribute:: orientation

		If the position of the anchor is relative to the LSB (0), center (2) or RSB (1).

		:type: int
'''

GSAnchor.userData = property(
	lambda self: UserDataProxy(self),
	lambda self, value: UserDataProxy(self).setter(value)
)
add_type(GSAnchor, "userData", dict)
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

	**Functions**

	.. function:: copy()

		Returns a full copy of the anchor

'''

GSAnchor.attributes = property(
	lambda self: AttributesProxy(self),
	lambda self, value: self.setAttributes_(value)
)
'''
	.. attribute:: attributes

		attributes attributes like :samp:`identifier`

		.. code-block:: python

			component.attributes['identifier'] = "220238F0"

		:type: dict
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


def ____GSComponent____(): pass


'''

:mod:`GSComponent`
===============================================================================

Implementation of the component object.
For details on how to access them, please see :attr:`GSLayer.components`

.. class:: GSComponent(glyph [, position])

	:param glyph: a :class:`GSGlyph` object or the glyph name
	:param position: the position of the component as NSPoint

	Properties

		* :attr:`position`
		* :attr:`scale`
		* :attr:`rotation`
		* :attr:`slant`
		* :attr:`componentName`
		* :attr:`componentMasterId`
		* :attr:`component`
		* :attr:`alignment`
		* :attr:`layer`
		* :attr:`transform`
		* :attr:`bounds`
		* :attr:`automaticAlignment`
		* :attr:`anchor`
		* :attr:`selected`
		* :attr:`smartComponentValues`
		* :attr:`bezierPath`
		* :attr:`userData`
		* :attr:`traverseAnchors`

	Functions

		* :meth:`applyTransform`
		* :meth:`copy`
		* :meth:`decompose`

	**Properties**
'''


def __GSComponent__init__(self, glyph: str | GSGlyph | None = None, offset: NSPoint | None = None, scale: NSPoint | None = None, rotation: float | None = None, transform: tuple | None = None):
	"""
	transformation: transform matrix as list of numbers
	"""
	if transform is not None:
		self.transform = transform

	if scale:
		self.scale = scale
	if offset:
		self.setPositionFast_(offset)
	if rotation:
		self.rotation = rotation

	if glyph:
		if isString(glyph):
			self.setComponentName_(glyph)
		elif isinstance(glyph, GSGlyph):
			self.setComponentName_(cast(GSGlyph, glyph).name)


GSComponent.__init__ = python_method(__GSComponent__init__)
GSComponent.__new__ = staticmethod(__GSObject__new__)


def __GSComponent__str__(self):
	return "<GSComponent \"%s\" x=%s y=%s>" % (self.componentName, self.position.x, self.position.y)


GSComponent.__str__ = python_method(__GSComponent__str__)

GSComponent.__eq__ = python_method(lambda self, other: self.isEqualToComponent_(other))

GSComponent.mutableCopyWithZone_ = __GSObject__copy__

GSComponent.position = property(
	lambda self: self.pyobjc_instanceMethods.position(),
	lambda self, value: self.setPosition_(validatePoint(value)),
	doc="The position of the component."
)
'''
	.. attribute:: position

		The position of the component.

		:type: NSPoint
'''

GSComponent.scale = property(
	lambda self: self.pyobjc_instanceMethods.scale(),
	lambda self, value: self.setScale_(value),
	doc="Scale factor of the component."
)
'''
	.. attribute:: scale

		Scale factor of the component.

		A tuple containing the horizontal and vertical scale.

		:type: tuple, NSPoint
'''

GSComponent.rotation = property(
	lambda self: self.angle(),
	lambda self, value: self.setAngle_(value),
	doc="Rotation angle of the component."
)
'''
	.. attribute:: rotation

		Rotation angle of the component.

		:type: float
'''


def __GSTransformable_get_slant__(self):
	return (self.slantHorizontal(), self.slantVertical())


def __GSTransformable_set_slant__(self, value):
	if isinstance(value, NSPoint):
		self.setSlantHorizontal_(value.x)
		self.setSlantVertical_(value.y)
	elif isinstance(value, (list, tuple)):
		self.setSlantHorizontal_(value[0])
		self.setSlantVertical_(value[1])
	else:
		raise ValueError


GSTransformableElement.slant = property(
	lambda self: __GSTransformable_get_slant__(self),
	lambda self, value: __GSTransformable_set_slant__(self, value),
	doc="The slant of the element."
)
'''
	.. attribute:: slant

		The slant of the component.

		:type: tuple, NSPoint
'''

GSComponent.componentName = property(
	lambda self: self.pyobjc_instanceMethods.componentName(),
	lambda self, value: self.setComponentName_(value),
	doc="The glyph name the component is pointing to."
)
'''
	.. attribute:: componentName
		The glyph name the component is pointing to.

		:type: str
'''

GSComponent.name = property(
	lambda self: self.pyobjc_instanceMethods.componentName(),
	lambda self, value: self.setComponentName_(value),
	doc="The glyph name the component is pointing to."
)
'''
	.. attribute:: name

		The glyph name the component is pointing to.

		:type: str

		.. versionadded:: 2.5
'''

GSComponent.componentMasterId = property(
	lambda self: self.pyobjc_instanceMethods.componentMasterId(),
	lambda self, value: self.setComponentMasterId_(value),
	doc="The ID of the master to component is pointing to."
)
'''
	.. attribute:: componentMasterId
		The ID of the master to component is pointing to.

		:type: str

		.. versionadded:: 3.1
'''

GSComponent.component = property(
	lambda self: self.pyobjc_instanceMethods.component(),
	doc="The glyph the component is pointing to."
)
'''
	.. attribute:: component

		The :class:`GSGlyph` the component is pointing to. This is read-only. In order to change the referenced base glyph, set :attr:`componentName <GSComponent.componentName>` to the new glyph name.

		:type: :class:`GSGlyph`
'''

GSComponent.componentLayer = property(
	lambda self: self.pyobjc_instanceMethods.componentLayer(),
	doc="The layer the component is pointing to."
)
'''
	.. attribute:: componentLayer
		The :class:`GSLayer` the component is pointing to. This is read-only. In order to change the referenced base glyph, set :attr:`componentName <GSComponent.componentName>` to the new glyph name.

		For Smart Components, the `componentLayer` contains the interpolated result.

		:type: :class:`GSLayer`

		.. versionadded:: 2.5
'''

GSComponent.transform = property(
	lambda self: self.transformStruct(),
	lambda self, value: self.setTransformStruct_(value),
	doc="Transformation matrix of the component."
)
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

GSComponent.bounds = property(
	lambda self: self.pyobjc_instanceMethods.bounds(),
	doc="Bounding box of the component. (read-only)"
)
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

GSComponent.layer = property(lambda self: self.pyobjc_instanceMethods.layer())

GSComponent.selected = property(
	lambda self: __ObjectInLayer_selected__(self),
	lambda self, value: __SetObjectInLayer_selected__(self, value)
)


# keep for compatibility:
GSComponent.disableAlignment = property(
	lambda self: bool(self.pyobjc_instanceMethods.disableAlignment()),
	lambda self, value: self.setDisableAlignment_(value)
)
# new:
GSComponent.automaticAlignment = property(
	lambda self: bool(self.pyobjc_instanceMethods.alignment() >= 0),
	lambda self, value: self.setDisableAlignment_(not bool(value)),
	doc="Defines whether the component is automatically aligned."
)
'''
	.. attribute:: automaticAlignment
		Defines whether the component is automatically aligned.

		:type: bool
'''

GSComponent.alignment = property(
	lambda self: self.pyobjc_instanceMethods.alignment(),
	lambda self, value: self.setAlignment_(value)
)

'''
	.. attribute:: alignment


		See :ref:`component-alignment` for available constants.

		.. versionadded:: 2.5

'''

GSComponent.locked = property(
	lambda self: bool(self.isLocked()),
	lambda self, value: self.setLocked_(value)
)
'''
	.. attribute:: locked

		.. versionadded:: 2.5

		If the component is locked

		:type: bool
'''

GSComponent.anchor = property(
	lambda self: self.pyobjc_instanceMethods.anchor(),
	lambda self, value: self.setAnchor_(value)
)
'''
	.. attribute:: anchor

		If more than one anchor/_anchor pair would match, this property can be used to set the anchor to use for automatic alignment

		This can be set from the anchor button in the component info box in the UI

		:type: str
'''

GSComponent.traverseAnchors = property(
	lambda self: self.pyobjc_instanceMethods.traverseAnchors(),
	lambda self, value: self.setTraverseAnchors_(value)
)
'''
	.. attribute:: traverseAnchors
		If anchors should be traversed from this component

		:type: bool
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

GSComponent.attributes = property(
	lambda self: AttributesProxy(self),
	lambda self, value: self.setAttributes_(value)
)
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
		Dictionary of interpolation values of the Smart Component. Keys are the ``axisId`` of the :class:`GSAxis` objects in the smart glyph’s :attr:`GSGlyph.axes` (or the font’s :attr:`GSFont.axes`). Corresponds to the values of the ‘Smart Component Settings’ dialog. Returns None if the component is not a Smart Component.

		For newly setup smart glyphs, the axis.axisId is a random string. After saving and re-opening the file, the name and axisId stay the same, as long as you don't change the name. So it is safer to always go through the smart glyph > axis > axisId (as explained in the code sample below).

		Also see https://glyphsapp.com/learn/smart-components for reference.

		:type: dict, int

		.. code-block:: python

			component = glyph.layers[0].shapes[1]
			widthAxis = component.component.axes[0]  # get the width axis from the smart glyph
			component.smartComponentValues[widthAxis.axisId] = 45

			# Check whether a component is a smart component
			for component in layer.components:
			    if component.smartComponentValues is not None:
			        # do stuff
'''

GSComponent.bezierPath = property(lambda self: self.pyobjc_instanceMethods.bezierPath())
'''
	.. attribute:: bezierPath
		Returns the closed paths of the component as bezier path, already transformed. Useful for drawing glyphs in plugins.

		:type: NSBezierPath

		.. code-block:: python
			# draw the path into the Edit view
			NSColor.redColor().set()
			layer.components[0].bezierPath.fill()
'''

GSComponent.openBezierPath = property(lambda self: self.pyobjc_instanceMethods.openBezierPath())
'''
	.. attribute:: openBezierPath
		Returns the open paths of the component as bezier path, already transformed. Useful for drawing glyphs in plugins.

		:type: NSBezierPath

		.. code-block:: python
			# draw the path into the Edit view
			NSColor.redColor().set()
			layer.components[0].openBezierPath.stroke()
'''

GSTransformableElement.userData = property(
	lambda self: UserDataProxy(self),
	lambda self, value: UserDataProxy(self).setter(value)
)
add_type(GSTransformableElement, "userData", dict)
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

GSComponent.tempData = property(
	lambda self: TempDataProxy(self),
	lambda self, value: TempDataProxy(self).setter(value)
)
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

GSComponent.parent = property(
	lambda self: self.pyobjc_instanceMethods.parent(),
	lambda self, value: self.setParent_(value)
)


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

	.. function:: copy()

		Returns a full copy of the component
'''


def __GSComponent_decompose__(self, doAnchors: bool | None = True, doHints: bool | None = True):
	assert (self.parent is not None)
	self.parent.decomposeComponent_doAnchors_doHints_(self, doAnchors, doHints)


GSComponent.decompose = python_method(__GSComponent_decompose__)
'''
	.. function:: decompose([doAnchors=True, doHints=True])

		Decomposes the component.

		:param doAnchors: get anchors from components
		:param doHints: get hints from components
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

		* :attr:`glyph`

	**Properties**
'''

GSGlyphReference.glyph = property(
	lambda self: self.pyobjc_instanceMethods.glyph(),
	lambda self, value: self.setGlyph_(value)
)
'''
	.. attribute:: glyph

	the GSGlyph to keep track of

	:type: GSGlyph

	.. code-block:: python

		glyphReference = GSGlyphReference(font.glyphs["A"])
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


def ____GSSmartComponentAxis____(): pass


'''

:mod:`GSSmartComponentAxis`
===============================================================================

Implementation of the Smart Component interpolation axis object.
For details on how to access them, please see :attr:`GSGlyph.smartComponentAxes`

.. versionadded:: 2.3

.. deprecated:: 4
	Smart glyphs now use regular :class:`GSAxis` objects in :attr:`GSGlyph.axes` (exactly like :attr:`GSFont.axes`). Smart layers are positioned with :attr:`GSLayer.attributes` ["coordinates"], keyed by ``axis.axisId``.

.. class:: GSSmartComponentAxis()

	Properties

		* :attr:`name`
		* :attr:`topValue`
		* :attr:`bottomValue`

	**Properties**
'''

GSSmartComponentAxis = GSPartProperty

GSSmartComponentAxis.__new__ = staticmethod(__GSObject__new__)
GSSmartComponentAxis.__new__.__name__ = "__new__"
GSSmartComponentAxis.__init__ = python_method(__empty__init__)


def __GSSmartComponentProperty__str__(self):
	return "<GSSmartComponentAxis \"%s\">" % (self.name)


GSSmartComponentAxis.__str__ = python_method(__GSSmartComponentProperty__str__)

GSSmartComponentAxis.name = property(
	lambda self: self.pyobjc_instanceMethods.name(),
	lambda self, value: self.setName_(objcObject(value))
)
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

GSSmartComponentAxis.topValue = property(
	lambda self: self.pyobjc_instanceMethods.topValue(),
	lambda self, value: self.setTopValue_(value)
)
'''
	.. attribute:: topValue
		Top end (pole) value on interpolation axis.

		:type: int, float
'''

GSSmartComponentAxis.bottomValue = property(
	lambda self: self.pyobjc_instanceMethods.bottomValue(),
	lambda self, value: self.setBottomValue_(value)
)
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


def ____GSShape____(): pass


'''

:mod:`GSShape`
===============================================================================

Implementation of the shape object. This a superclass for GSPath and GSComponent. You can’t instantiate GSShape directly

For details on how to access them, please see :attr:`GSLayer.shapes`

.. class:: GSShape()

	Properties

		* :attr:`position`
		* :attr:`locked`
		* :attr:`shapeType`
'''

GSShape.locked = property(
	lambda self: bool(self.pyobjc_instanceMethods.locked()),
	lambda self, value: self.setLocked_(value)
)

GSPath.locked = property(
	lambda self: bool(self.pyobjc_instanceMethods.locked()),
	lambda self, value: self.setLocked_(value)
)
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


def ____GSPath____(): pass


'''

:mod:`GSPath`
===============================================================================

Implementation of the path object.

For details on how to access them, please see :attr:`GSLayer.paths`

If you build a path in code, make sure that the structure is valid. A curve node has to be preceded by two off-curve nodes. And an open path has to start with a line node.

.. class:: GSPath()

	Properties

		* :attr:`parent`
		* :attr:`nodes`
		* :attr:`segments`
		* :attr:`closed`
		* :attr:`direction`
		* :attr:`bounds`
		* :attr:`selected`
		* :attr:`bezierPath`
		* :attr:`attributes`
		* :attr:`tempData`

	Functions

		* :meth:`addNodesAtExtremes`
		* :meth:`applyTransform`
		* :meth:`copy`
		* :meth:`reverse`

	**Properties**
'''

GSPath.__new__ = staticmethod(__GSObject__new__)
GSPath.__new__.__name__ = "__new__"
GSPath.__init__ = python_method(__empty__init__)


def __GSPath__str__(self):
	return "<GSPath %s nodes>" % len(self.nodes)


GSPath.__str__ = python_method(__GSPath__str__)

GSPath.__eq__ = python_method(lambda self, other: self.isEqualToPath_(other))

GSPath.mutableCopyWithZone_ = __GSObject__copy__

GSPath.parent = property(
	lambda self: self.pyobjc_instanceMethods.parent(),
	lambda self, value: self.setParent_(value)
)
'''
	.. attribute:: parent

		Reference to the :class:`layer <GSLayer>` object.

		:type: :class:`GSLayer`
'''

GSPath.nodes = property(
	lambda self: PathNodesProxy(self),
	lambda self, value: PathNodesProxy(self).setter(value)
)
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

GSPath.__len__ = python_method(lambda self: self.countOfNodes())

GSPath.segments = property(
	lambda self: self.pyobjc_instanceMethods.segments(),
	lambda self, value: self.setSegments_(value)
)
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

GSPath.closed = property(
	lambda self: bool(self.pyobjc_instanceMethods.closed()),
	lambda self, value: self.setClosed_(value)
)
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


def __GSPath_selected__(self):
	return set(self.nodes) <= set(self.parent.selection)


def __GSPath_SetSelected__(self, state):
	layer = self.parent
	if state:
		layer.addObjectsFromArrayToSelection_(self.pyobjc_instanceMethods.nodes())
	else:
		layer.removeObjectsFromSelection_(self.pyobjc_instanceMethods.nodes())


GSPath.selected = property(
	lambda self: __GSPath_selected__(self),
	lambda self, value: __GSPath_SetSelected__(self, value)
)
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

GSPath.attributes = property(
	lambda self: AttributesProxy(self),
	lambda self, value: self.setAttributes_(value)
)
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

GSPath.userData = property(
	lambda self: UserDataProxy(self),
	lambda self, value: UserDataProxy(self).setter(value)
)
add_type(GSNode, "userData", dict)
'''
	.. attribute:: userData
		A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the data will not be recoverable from the saved file.

		:type: dict

		.. code-block:: python
			# set value
			path.userData['rememberToMakeCoffee'] = True

			# delete value
			del path.userData['rememberToMakeCoffee']

		.. versionadded:: 4
'''

GSPath.tempData = property(
	lambda self: TempDataProxy(self),
	lambda self, value: TempDataProxy(self).setter(value)
)
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
	"""draw the object with a fontTools pen"""

	Start = 0
	if self.closed:
		for idx in range(len(self) - 1, -1, -1):
			StartNode = self.nodeAtIndex_(idx)
			GS_Type = StartNode.pyobjc_instanceMethods.type()
			if GS_Type is not GSOFFCURVE_:
				pen.moveTo(StartNode.pyobjc_instanceMethods.position())
				break
	else:
		for idx in range(len(self)):
			StartNode = self.nodeAtIndex_(idx)
			GS_Type = StartNode.pyobjc_instanceMethods.type()
			if GS_Type is not GSOFFCURVE_:
				pen.moveTo(StartNode.pyobjc_instanceMethods.position())
				Start = idx + 1
				break
	for idx in range(Start, len(self), 1):
		node = self.nodeAtIndex_(idx)
		GS_Type = node.pyobjc_instanceMethods.type()
		if GS_Type == GSLINE_:
			pen.lineTo(node.pyobjc_instanceMethods.position())
		elif GS_Type == GSCURVE_:
			pen.curveTo(
				self.nodeAtIndex_(idx - 2).pyobjc_instanceMethods.position(),
				self.nodeAtIndex_(idx - 1).pyobjc_instanceMethods.position(), node.pyobjc_instanceMethods.position())
	if self.closed:
		pen.closePath()
	else:
		pen.endPath()


GSPath.draw = python_method(DrawPathWithPen)


def __GSPath__drawPoints__(self, pen):
	'''draw the object with a fontTools pen'''
	pen.beginPath()
	for node in self.pyobjc_instanceMethods.nodes():
		node_type = node.type
		if node.type == GSOFFCURVE:
			node_type = None
		pen.addPoint(node.position, segmentType=node_type, smooth=node.smooth, name=node.name)
	pen.endPath()


GSPath.drawPoints = python_method(__GSPath__drawPoints__)


def __GSPath_addNodesAtExtremes__(self, force: bool | None = False, checkSelection: bool | None = False):
	self.addExtremes_checkSelection_(force, checkSelection)


GSPath.addNodesAtExtremes = python_method(__GSPath_addNodesAtExtremes__)
'''
	.. function:: addNodesAtExtremes([force=False, checkSelection=False])

		Add nodes at path’s extrema, e.g., top, bottom etc.

		:param force: if points are always added, even if that would distort the shape
		:param checkSelection: only process selected segments
'''


def __GSPath_applyTransform__(self, transformStruct):
	transform = NSAffineTransform.transform()
	transform.setTransformStruct_(transformStruct)
	for node in self.nodes:
		node.position = transform.transformPoint_(node.positionPrecise())


GSPath.applyTransform = python_method(__GSPath_applyTransform__)
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

	.. function:: copy()

		Returns a full copy of the path

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


def ____GSNode____(): pass


'''

:mod:`GSNode`
===============================================================================

Implementation of the node object.

For details on how to access them, please see :attr:`GSPath.nodes`

.. class:: GSNode([pt, type = type])

	:param pt: The position of the node.
	:param type: The type of the node, LINE, CURVE or OFFCURVE

	Properties

		* :attr:`position`
		* :attr:`type`
		* :attr:`connection`
		* :attr:`selected`
		* :attr:`index`
		* :attr:`nextNode`
		* :attr:`prevNode`
		* :attr:`name`
		* :attr:`orientation`

	Functions

		* :meth:`copy`
		* :meth:`makeNodeFirst`
		* :meth:`toggleConnection`

	**Properties**
'''


def __GSNode__init__(self, pt: NSPoint | None = None, type: int | str | None = None, x: float | None = None, y: float | None = None, name: str | None = None, pointType: int | None = None) -> None:
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


GSNode.__init__ = python_method(__GSNode__init__)
GSNode.__new__ = staticmethod(__GSObject__new__)
GSNode.__new__.__name__ = "__new__"

GSNode.__eq__ = python_method(lambda self, other: self.isEqualToNode_(other))

GSNode.mutableCopyWithZone_ = __GSObject__copy__

GSElement.position = property(
	lambda self: self.pyobjc_instanceMethods.position(),
	lambda self, value: self.setPosition_(validatePoint(value))
)
'''
	.. attribute:: position

		The position of the node.

		:type: NSPoint
'''

GSNode.position = property(
	lambda self: self.pyobjc_instanceMethods.position(),
	lambda self, value: self.setPosition_(validatePoint(value))
)

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
	elif GS_Type == GSRAPHNEWSPIRAL_:
		return RAPHNEWSPIRAL
	else:
		return LINE


def __GSNode_set_type__(self, value):
	if isinstance(value, int):
		self.setType_(value)
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
	elif value == RAPHNEWSPIRAL:
		self.setType_(GSRAPHNEWSPIRAL_)


GSNode.type = property(__GSNode_get_type__, __GSNode_set_type__)
'''
	.. attribute:: type

		The type of the node, LINE, CURVE or OFFCURVE

		Always compare against the constants, never against the actual value.

		:type: str
'''


def __GSNode__set_smooth(self, value):
	if value is True:
		self.setConnection_(GSSMOOTH)
	else:
		self.setConnection_(GSSHARP)


GSNode.smooth = property(lambda self: bool(self.isSmooth()), __GSNode__set_smooth)
'''
	.. attribute:: smooth

		If it is a smooth connection or not

		:type: BOOL
'''

GSNode.connection = property(
	lambda self: self.pyobjc_instanceMethods.connection(),
	lambda self, value: self.setConnection_(value)
)
'''
	.. attribute:: connection

		The type of the connection, SHARP or SMOOTH

		:type: str

		.. deprecated:: 2.3
			Use :attr:`smooth <GSNode.smooth>` instead.
'''

GSNode.selected = property(
	lambda self: __ObjectInLayer_selected__(self),
	lambda self, value: __SetObjectInLayer_selected__(self, value)
)

GSNode.parent = property(lambda self: self.pyobjc_instanceMethods.parent())

GSNode.layer = property(lambda self: self.pyobjc_instanceMethods.layer())

GSNode.glyph = property(lambda self: self.pyobjc_instanceMethods.glyph())
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
			print(layer.paths[0].nodes[0].index == (len(layer.paths[0].nodes) - 1))  # returns False for first node
			print(layer.paths[0].nodes[-1].index == (len(layer.paths[0].nodes) - 1))  # returns True for last node
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
			print(layer.paths[0].nodes[0].prevNode)  # returns the last node in the path (first node >> jumps to end of path)
			print(layer.paths[0].nodes[-1].prevNode)  # returns second last node in the path

			# check if node is first node in path (with at least two nodes)
			print(layer.paths[0].nodes[0].index == 0)  # returns True for first node
			print(layer.paths[0].nodes[-1].index == 0)  # returns False for last node
'''

GSNode.name = property(
	lambda self: self.pyobjc_instanceMethods.name(),
	lambda self, value: self.setName_(str(value))
)
'''
	.. attribute:: name

		Attaches a name to a node.

		:type: str
'''

GSNode.attributes = property(
	lambda self: AttributesProxy(self),
	lambda self, value: self.setAttributes_(value)
)
'''
	.. attribute:: attributes

		attributes attributes like :samp:`mask` or :samp:`reversePaths`

		.. code-block:: python

			component.attributes['mask'] = True
			component.attributes['reversePaths'] = True

		:type: dict
'''


GSNode.userData = property(
	lambda self: UserDataProxy(self),
	lambda self, value: UserDataProxy(self).setter(value)
)
add_type(GSNode, "userData", dict)
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

	.. function:: copy()

		Returns a full copy of the node

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


def ____GSPathSegment____(): pass


'''

:mod:`GSPathSegment`
===============================================================================

Implementation of the segment object.

For details on how to access them, please see :attr:`GSPath.segments`

.. class:: GSPathSegment()

	Properties

		* :attr:`type`
		* :attr:`bounds`
		* :attr:`length`

	Functions

		* :meth:`copy`
		* :meth:`curvatureAtTime_`
		* :meth:`extremePoints`
		* :meth:`extremeTimes`
		* :meth:`inflectionPoints`
		* :meth:`lastPoint`
		* :meth:`middlePoint`
		* :meth:`normalAtTime_`
		* :meth:`normalizeHandles`
		* :meth:`pointAtTime_`
		* :meth:`reverse`
		* :meth:`tangentAtTime_`
'''


def __GSPathSegment__getitem__(self, idx):
	return self.pointAtIndex_(idx)


GSPathSegment.__getitem__ = python_method(__GSPathSegment__getitem__)

GSPathSegment.__len__ = property(lambda self: self.countOfPoints)


def __GSPathSegment__new__(typ, p1=NSPoint(0, 0), p2=NSPoint(0, 0), p3=None, p4=None):
	if (p3 is not None and p4 is not None):
		return typ.alloc().initWithCurvePoint1_point2_point3_point4_options_(p1, p2, p3, p4, 0)
	else:
		return typ.alloc().initWithLinePoint1_point2_options_(p1, p2, 0)


GSPathSegment.__new__ = staticmethod(__GSPathSegment__new__)

GSPathSegment.bounds = property(lambda self: self.pyobjc_instanceMethods.bounds())
'''
	.. attribute:: bounds

		Bounding box of the segment as NSRect. Read-only.

		:type: NSRect

		.. code-block:: python
			bounds = segment.bounds
			# origin
			print(bounds.origin.x, bounds.origin.y)

			# size
			print(bounds.size.width, bounds.size.height)
'''

GSPathSegment.type = property(__GSNode_get_type__)
'''
	.. attribute:: type

		The type of the node, LINE, CURVE or QCURVE

		Always compare against the constants, never against the actual value.

		:type: str
'''

'''
	.. function:: copy()

		Returns a full copy of the segment

	.. function:: reverse()

		reverses the segments

	.. function:: middlePoint()

		the point at t=0.5

	.. function:: lastPoint()

		the ending point of the segment

	.. function:: inflectionPoints()

		a list of "t" values of inflection points on the segment

	.. function:: curvatureAtTime_(t)

		the curvature at "t"

	.. function:: pointAtTime_(t)

		the point a "t"

	.. function:: normalAtTime_(t)

		the normal vector at "t"

	.. function:: tangentAtTime_(t)

		the tangent at "t"

	.. function:: extremePoints()

		a list of extreme points

	.. function:: extremeTimes()

		a list of "t" value for the extreme points

	.. function:: normalizeHandles()

		balances the length of the handle while trying to keep the shape as good as possible

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


def ____GSGuide____(): pass


'''

:mod:`GSGuide`
===============================================================================

Implementation of the guide object.

For details on how to access them, please see :attr:`GSLayer.guides`


.. class:: GSGuide()

	Properties

		* :attr:`position`
		* :attr:`angle`
		* :attr:`name`
		* :attr:`filter`
		* :attr:`showMeasurement`
		* :attr:`selected`
		* :attr:`locked`
		* :attr:`userData`

	Functions

		* :meth:`copy`

'''


def __GSGuide__init__(self, pt=None, angle=None, name=None):
	if pt:
		self.setPosition_(pt)
	if angle:
		self.angle = angle
	if name:
		self.name = name


GSGuide.__init__ = python_method(__GSGuide__init__)

GSGuide.__new__ = staticmethod(__GSObject__new__)


def __GSGuide__str__(self):
	return "<GSGuide x=%s y=%s angle=%s>" % (self.position.x, self.position.y, self.angle)


GSGuide.__str__ = python_method(__GSGuide__str__)

GSGuide.__eq__ = python_method(lambda self, other: self.isEqualToGuide_(other))

GSGuide.mutableCopyWithZone_ = __GSObject__copy__

GSGuide.lockAngle = property(
	lambda self: bool(self.pyobjc_instanceMethods.lockAngle()),
	lambda self, value: self.setLockAngle_(value)
)
'''
	.. attribute:: lockAngle

		locks the angle

		:type: bool
'''

GSGuide.angle = property(
	lambda self: self.pyobjc_instanceMethods.angle(),
	lambda self, value: self.setAngle_(float(value))
)
'''
	.. attribute:: angle

		Angle

		:type: float
'''


def __GSGuide_setName(self, name):
	if isString(name) or name is None:
		self.setName_(name)
	else:
		raise TypeError


GSGuide.name = property(lambda self: self.pyobjc_instanceMethods.name(), __GSGuide_setName)
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

GSGuide.locked = property(
	lambda self: bool(self.pyobjc_instanceMethods.isLocked()),
	lambda self, value: self.setLocked_(value)
)
'''
	.. attribute:: locked

		Locked

		:type: bool
'''

GSGuide.filter = property(
	lambda self: self.pyobjc_instanceMethods.filter(),
	lambda self, value: self.setFilter_(value)
)
'''
	.. attribute:: filter

		A filter to only show the guide in certain glyphs. Only relevant in global guides

		:type: NSPredicate
'''

GSGuide.showMeasurement = property(
	lambda self: bool(self.pyobjc_instanceMethods.showMeasurement()),
	lambda self, value: self.setShowMeasurement_(value)
)
'''
	.. attribute:: showMeasurement
		If the guide is showing measurements

		:type: bool

		.. versionadded:: 3.1
'''

GSGuide.userData = property(
	lambda self: UserDataProxy(self),
	lambda self, value: UserDataProxy(self).setter(value)
)
add_type(GSGuide, "userData", dict)
'''
	.. attribute:: userData
		A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the data will not be recoverable from the saved file.

		:type: dict

		.. code-block:: python
			# set value
			guide.userData['rememberToMakeCoffee'] = True

			# delete value
			del guide.userData['rememberToMakeCoffee']

	**Functions**

	.. function:: copy()

		Returns a full copy of the guide
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


def ____GSAnnotation____(): pass


'''

:mod:`GSAnnotation`
===============================================================================

Implementation of the annotation object.

For details on how to access them, please see :class:`GSLayer.annotations`

.. class:: GSAnnotation()

		* :attr:`position`
		* :attr:`type`
		* :attr:`text`
		* :attr:`angle`
		* :attr:`width`

	**Properties**
'''

GSAnnotation.__new__ = staticmethod(__GSObject__new__)
GSAnnotation.__new__.__name__ = "__new__"


def __GSAnnotation__init__(self, pt: NSPoint | None = None, type: int | None = None, text: str | None = None, angle: float | None = None, width: int | None = None):
	if pt:
		self.setPosition_(pt)
	if type:
		self.type = type
	if text:
		self.setType_(text)
	if angle:
		self.setAngle_(angle)
	if width:
		self.setWidth_(width)


GSAnnotation.__init__ = python_method(__GSAnnotation__init__)


def __GSAnnotation__str__(self):
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


GSAnnotation.__str__ = python_method(__GSAnnotation__str__)

GSAnnotation.mutableCopyWithZone_ = __GSObject__copy__

GSAnnotation.position = property(
	lambda self: self.pyobjc_instanceMethods.position(),
	lambda self, value: self.setPosition_(value)
)
'''
	.. attribute:: position

		The position of the annotation.

		:type: NSPoint
'''

GSAnnotation.type = property(
	lambda self: self.pyobjc_instanceMethods.type(),
	lambda self, value: self.setType_(value)
)
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

GSAnnotation.text = property(
	lambda self: self.pyobjc_instanceMethods.text(),
	lambda self, value: self.setText_(value)
)
'''
	.. attribute:: text

		The content of the annotation. Only useful if type == TEXT

		:type: str
'''

GSAnnotation.angle = property(
	lambda self: self.pyobjc_instanceMethods.angle(),
	lambda self, value: self.setAngle_(value)
)
'''
	.. attribute:: angle

		The angle of the annotation.

		:type: float
'''

GSAnnotation.width = property(
	lambda self: self.pyobjc_instanceMethods.width(),
	lambda self, value: self.setWidth_(value)
)
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


def ____GSHint____(): pass


'''

:mod:`GSHint`
===============================================================================

Implementation of the hint object.

For details on how to access them, please see :class:`GSLayer.hints`

.. class:: GSHint()

		* :attr:`parent`
		* :attr:`originNode`
		* :attr:`targetNode`
		* :attr:`otherNode1`
		* :attr:`otherNode2`
		* :attr:`originIndex`
		* :attr:`targetIndex`
		* :attr:`otherIndex1`
		* :attr:`otherIndex2`
		* :attr:`type`
		* :attr:`horizontal`
		* :attr:`selected`
		* :attr:`isTrueType`
		* :attr:`isPostScript`
		* :attr:`isCorner`
		* :attr:`name`
		* :attr:`stem`
		* :attr:`alignment`

	**Properties**
'''

GSHint.__new__ = staticmethod(__GSObject__new__)
GSHint.__new__.__name__ = "__new__"
GSHint.__init__ = python_method(__empty__init__)


def __GSHint__origin__pos(self):
	if (self.originNode):
		if self.horizontal:
			return self.originNode.position.y
		else:
			return self.originNode.position.x
	return self.pyobjc_instanceMethods.origin()


def __GSHint__width__pos(self):
	if (self.targetNode):
		if self.horizontal:
			return self.targetNode.position.y
		else:
			return self.targetNode.position.x
	width = self.pyobjc_instanceMethods.width()
	if width > 100000:
		width = 0
	return width


GSHint.mutableCopyWithZone_ = __GSObject__copy__

GSHint.parent = property(lambda self: self.pyobjc_instanceMethods.parent())
'''
	.. attribute:: parent

		Parent layer of hint.

		:type: GSLayer
'''

GSHint.scale = property(
	lambda self: self.pyobjc_instanceMethods.scale(),
	lambda self, value: self.setScale_(value)
)

GSHint.originNode = property(
	lambda self: self.pyobjc_instanceMethods.originNode(),
	lambda self, value: self.setOriginNode_(value)
)
'''
	.. attribute:: originNode
		The first node the hint is attached to.

		:type: :class:`GSNode` or :class:`GSHandle` (e.g. when attached to intersections)
'''

GSHint.position = property(
	__GSHint__origin__pos,
	lambda self, value: self.setOrigin_(value)
)

GSHint.width = property(
	lambda self: __GSHint__width__pos(self),
	lambda self, value: self.setOrigin_(value)
)

GSHandle.position = property(lambda self: self.pyobjc_instanceMethods.position())


def __indexPathToIndexes__(indexPath):
	if indexPath is not None:
		indexes = []
		for idx in range(len(indexPath)):
			indexes.append(indexPath.indexAtPosition_(idx))
		return indexes
	return None


GSHint.origin = property(lambda self: __indexPathToIndexes__(self.originIndex))

GSHint.target = property(lambda self: __indexPathToIndexes__(self.targetIndex))

GSHint.other1 = property(lambda self: __indexPathToIndexes__(self.otherIndex1))

GSHint.other2 = property(lambda self: __indexPathToIndexes__(self.otherIndex2))

GSHint.targetNode = property(
	lambda self: self.pyobjc_instanceMethods.targetNode(),
	lambda self, value: self.setTargetNode_(value)
)
'''
	.. attribute:: targetNode
		The the second node this hint is attached to. In the case of a ghost hint, this value will be empty.

		:type: :class:`GSNode` or :class:`GSHandle` (e.g. when attached to intersections)
'''

GSHint.otherNode1 = property(
	lambda self: self.pyobjc_instanceMethods.otherNode1(),
	lambda self, value: self.setOtherNode1_(value)
)
'''
	.. attribute:: otherNode1
		A third node this hint is attached to. Used for Interpolation or Diagonal hints.

		:type: :class:`GSNode` or :class:`GSHandle` (e.g. when attached to intersections)
'''

GSHint.otherNode2 = property(
	lambda self: self.pyobjc_instanceMethods.otherNode2(),
	lambda self, value: self.setOtherNode2_(value)
)
'''
	.. attribute:: otherNode2
		A fourth node this hint is attached to. Used for Diagonal hints.

		:type: :class:`GSNode` or :class:`GSHandle` (e.g. when attached to intersections)
'''

GSHint.originIndex = property(
	lambda self: self.pyobjc_instanceMethods.originIndex(),
	lambda self, value: self.setOriginIndex_(value)
)
'''
	.. attribute:: originIndex
		The indexPath to the first node the hint is attached to.

		:type: :class:`NSIndexPath`
'''

GSHint.targetIndex = property(
	lambda self: self.pyobjc_instanceMethods.targetIndex(),
	lambda self, value: self.setTargetIndex_(value)
)
'''
	.. attribute:: targetIndex
		The indexPath to the second node this hint is attached to. In the case of a ghost hint, this value will be empty.

		:type: :class:`NSIndexPath`
'''

GSHint.otherIndex1 = property(
	lambda self: self.pyobjc_instanceMethods.otherIndex1(),
	lambda self, value: self.setOtherIndex1_(value)
)
'''
	.. attribute:: otherIndex1
		A indexPath to the third node this hint is attached to. Used for Interpolation or Diagonal hints.

		:type: :class:`NSIndexPath`
'''

GSHint.otherIndex2 = property(
	lambda self: self.pyobjc_instanceMethods.otherIndex2(),
	lambda self, value: self.setOtherIndex2_(value)
)
'''
	.. attribute:: otherIndex2
		A indexPath to the fourth node this hint is attached to. Used for Diagonal hints.

		:type: :class:`NSIndexPath`
'''

GSHint.type = property(
	lambda self: self.pyobjc_instanceMethods.type(),
	lambda self, value: self.setType_(value)
)
'''
	.. attribute:: type

		See `Hint Types`_

		:type: int
'''

GSHint.options = property(
	lambda self: self.pyobjc_instanceMethods.options(),
	lambda self, value: self.setOptions_(value)
)
'''
	.. attribute:: options

		Stores extra options for the hint. For TT hints, that might be the rounding settings.

		See `Hint Option`_

		For corner components, it stores the alignment settings: left = 0, center = 2, right = 1, auto (for caps) = alignment | 8

		:type: int
'''

GSHint.horizontal = property(
	lambda self: bool(self.pyobjc_instanceMethods.horizontal()),
	lambda self, value: self.setHorizontal_(value)
)
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

GSHint.name = property(
	lambda self: self.pyobjc_instanceMethods.name(),
	lambda self, value: self.setName_(objcObject(value))
)
'''
	.. attribute:: name

		Name of the hint. This is the referenced glyph for corner and cap components.

		:type: str
'''


def GSHint__stem__(self):
	value = self.pyobjc_instanceMethods.stem()
	if self.isTrueType:
		stems = self.parent.master.customParameters['TTFStems']
		if stems is None:
			stems = self.parent.metrics
		if stems and -1 <= value <= (len(stems) - 1):
			return value
		else:
			return -2
	else:
		return value

def GSHint__setStem__(self, value):
	if self.isTrueType:
		if value == -2:
			self.setStem_(NSNotFound)
			return
		elif value == -1:
			self.setStem_(value)
			return
		stems = self.parent.master.customParameters['TTFStems']
		if stems is None:
			stems = self.parent.metrics
		if not stems:
			raise ValueError('The master of this layer has no defined "TTFStems" custom parameter')
		if 0 <= value <= (len(stems) - 1):
			self.setStem_(value)
			return
		raise ValueError(
			'Wrong value. Stem values can be indices of TT stems ("TTFStems" master custom parameter) or -1 for no stem or -2 for automatic.')
	else:
		self.setStem_(value)


GSHint.stem = property(
	GSHint__stem__,
	lambda self, value: GSHint__setStem__(self, value)
)
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

GSHint.tempData = property(
	lambda self: TempDataProxy(self),
	lambda self, value: TempDataProxy(self).setter(value)
)
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

GSHint.alignment = property(
	lambda self: self.pyobjc_instanceMethods.alignment(),
	lambda self, value: self.setAlignment_(value)
)
'''
	.. attribute:: alignment

		For corner components: left = 0, center = 2, right = 1, fixed = 4

		:type: int

		.. versionadded:: 3.2
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


def ____GSBackgroundImage____(): pass


'''

:mod:`GSBackgroundImage`
===============================================================================

Implementation of background image.

For details on how to access it, please see :class:`GSLayer.backgroundImage`

.. class:: GSBackgroundImage([path])

	:param path: Initialize with an image file (optional)

	Properties

		* :attr:`path`
		* :attr:`image`
		* :attr:`crop`
		* :attr:`locked`
		* :attr:`position`
		* :attr:`scale`
		* :attr:`rotation`
		* :attr:`slant`
		* :attr:`transform`
		* :attr:`alpha`

	Functions

		* :meth:`resetCrop`
		* :meth:`scaleWidthToEmUnits`
		* :meth:`scaleHeightToEmUnits`

	**Properties**
'''


def __GSBackgroundImage__init__(self, path: str | None = None):
	if path:
		self.setImagePath_(path)


GSBackgroundImage.__init__ = python_method(__GSBackgroundImage__init__)
GSBackgroundImage.__new__ = staticmethod(__GSObject__new__)


def __GSBackgroundImage__str__(self):
	return "<GSBackgroundImage '%s'>" % self.path


GSBackgroundImage.__str__ = python_method(__GSBackgroundImage__str__)

GSBackgroundImage.mutableCopyWithZone_ = __GSObject__copy__
GSBackgroundImage.__copy__ = python_method(__GSObject__copy__)
GSBackgroundImage.__deepcopy__ = python_method(__GSObject__copy__)

GSBackgroundImage.path = property(
	lambda self: self.imagePath(),
	lambda self, value: self.setImagePath_(value)
)
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

GSBackgroundImage.crop = property(
	lambda self: self.pyobjc_instanceMethods.crop(),
	lambda self, value: self.setCrop_(value)
)
'''
	.. attribute:: crop

		Crop rectangle. This is relative to the image size in pixels, not the font’s em units (just in case the image is scaled to something other than 100%).

		:type: :class:`NSRect`

		.. code-block:: python
			# change cropping
			layer.backgroundImage.crop = NSRect(NSPoint(0, 0), NSPoint(1200, 1200))
'''

GSBackgroundImage.locked = property(
	lambda self: bool(self.isLocked()),
	lambda self, value: self.setLocked_(value)
)
'''
	.. attribute:: locked

		Defines whether image is locked for access in UI.

		:type: bool
'''

GSBackgroundImage.alpha = property(
	lambda self: self.pyobjc_instanceMethods.alpha(),
	lambda self, value: self.setAlpha_(value)
)
'''
	.. attribute:: alpha

		Defines the transparence of the image in the Edit view. Default is 50%, possible values are 10–100.

		To reset it to default, set it to anything other than the allowed values.

		:type: int
'''


def __GSBackgroundImage_getPosition(self):
	return NSPoint(self.transform[4], self.transform[5])


def __GSBackgroundImage_setPosition(self, pos):
	self.transform = ((self.transform[0], self.transform[1], self.transform[2], self.transform[3], pos.x, pos.y))


GSBackgroundImage.position = property(
	__GSBackgroundImage_getPosition,
	lambda self, value: __GSBackgroundImage_setPosition(self, value)
)
'''
	.. attribute:: position

		Position of image in font units.

		:type: :class:`NSPoint`

	.. code-block:: python
		# change position
		layer.backgroundImage.position = NSPoint(50, 50)
'''

GSBackgroundImage.scale = property(
	lambda self: self.pyobjc_instanceMethods.scale(),
	lambda self, value: self.setScale_(value)
)
'''
	.. attribute:: scale

		Scale factor of image.

		A scale factor of 1.0 (100%) means that 1 font unit is equal to 1 point.

		Set the scale factor for x and y scale simultaneously with an integer or a float value. For separate scale factors, please use a tuple.

		:type: tuple, NSPoint

		.. code-block:: python
			# change scale
			layer.backgroundImage.scale = 1.2 # changes x and y to 120%
			layer.backgroundImage.scale = (1.1, 1.2)  # changes x to 110% and y to 120%
'''

GSBackgroundImage.rotation = property(
	lambda self: self.angle(),
	lambda self, value: self.setAngle_(value)
)
'''
	.. attribute:: rotation

		Rotation angle of image.

		:type: float
'''

'''
	.. attribute:: slant

		The slant of the image.

		:type: tuple, NSPoint
'''

GSBackgroundImage.transform = property(
	lambda self: self.transformStruct(),
	lambda self, value: self.setTransformStruct_(value)
)
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


def __GSBackgroundImage_resetCrop(self: GSImage):
	self.crop = NSRect(NSPoint(0, 0), self.image.size())


GSBackgroundImage.resetCrop = python_method(__GSBackgroundImage_resetCrop)
'''
	.. function:: resetCrop

		Resets the cropping to the image’s original dimensions.
'''


def __GSBackgroundImage_scaleWidthToEmUnits(self, value):
	scale = float(value) / float(self.crop.size.width)
	self.scale = NSPoint(scale, scale)


GSBackgroundImage.scaleWidthToEmUnits = python_method(__GSBackgroundImage_scaleWidthToEmUnits)
'''
	.. function:: scaleWidthToEmUnits

		Scale the image’s cropped width to a certain em unit value, retaining its aspect ratio.

		.. code-block:: python
			# fit image in layer’s width
			layer.backgroundImage.scaleWidthToEmUnits(layer.width)
'''


def __GSBackgroundImage_scaleHeightToEmUnits(self, value):
	self.scale = float(value) / float(self.crop.size.height)


GSBackgroundImage.scaleHeightToEmUnits = python_method(__GSBackgroundImage_scaleHeightToEmUnits)
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
#           GSGradient
#
#
#
##################################################################################


def ____GSGradient____(): pass


'''

:mod:`GSGradient`
===============================================================================

Implementation of the gradient object.

.. class:: GSGradient()

	Properties

		* :attr:`colors`
		* :attr:`type`
		* :attr:`start`
		* :attr:`end`
		* :attr:`absoluteStart`
		* :attr:`absoluteEnd`

	**Properties**
'''

GSGradient.__new__ = staticmethod(__GSObject__new__)
GSGradient.__init__ = python_method(__empty__init__)
GSGradient.__copy__ = python_method(__GSObject__copy__)
GSGradient.__deepcopy__ = python_method(__GSObject__copy__)

GSGradient.colors = property(
	lambda self: GradientColorsProxy(self),
	lambda self, value: GradientColorsProxy(self).setter(value)
)
'''
	.. attribute:: colors

		A list of colors. Each is an list containing a NSColor and and position between 0.0 and 1.0.

		:type: list
'''

GSGradient.type = property(
	lambda self: self.pyobjc_instanceMethods.type(),
	lambda self, value: self.setType_(value)
)
'''
	.. attribute:: type

		The gradient type.
		Linear = 0, Circular = 1

		:type: int
'''
GSGradient.start = property(
	lambda self: self.pyobjc_instanceMethods.start(),
	lambda self, value: self.setStart_(value)
)
'''
	.. attribute:: start

		A NSPoint that relatively to the shapes bounding box defines the starting point of the gradient

		:type: NSPoint
'''
GSGradient.end = property(
	lambda self: self.pyobjc_instanceMethods.end(),
	lambda self, value: self.setEnd_(value)
)
'''
	.. attribute:: end

		A NSPoint that relatively to the shapes bounding box defines the ending point of the gradient

		:type: NSPoint
'''
GSGradient.absoluteStart = property(
	lambda self: self.pyobjc_instanceMethods.absoluteStart(),
	lambda self, value: self.setAbsoluteStart_(value)
)
'''
	.. attribute:: absoluteStart
		A NSPoint of the absolute starting point of the gradient

		:type: NSPoint
'''
GSGradient.absoluteEnd = property(
	lambda self: self.pyobjc_instanceMethods.absoluteEnd(),
	lambda self, value: self.setAbsoluteEnd_(value)
)
'''
	.. attribute:: absoluteEnd
		A NSPoint of the absolute ending point of the gradient

		:type: NSPoint
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


def ____GSEditViewController____(): pass


'''

:mod:`GSEditViewController`
===============================================================================

Implementation of the GSEditViewController object, which represents Edit tabs in the UI.

For details on how to access them, please look at :class:`GSFont.tabs`


.. class:: GSEditViewController()

	Properties

		* :attr:`parent`
		* :attr:`text`
		* :attr:`textCursor`
		* :attr:`textRange`
		* :attr:`selectedTextRange`
		* :attr:`layers`
		* :attr:`layersCursor`
		* :attr:`layersRange`
		* :attr:`selectedLayerRange`
		* :attr:`scale`
		* :attr:`viewPort`
		* :attr:`bounds`
		* :attr:`selectedLayerOrigin`
		* :attr:`direction`
		* :attr:`features`
		* :attr:`previewInstances`
		* :attr:`previewHeight`
		* :attr:`bottomToolbarHeight`
		* :attr:`masterIndex`
		* :attr:`tempData`

	Functions

		* :meth:`close`
		* :meth:`saveToPDF`
		* :meth:`redraw`

	**Properties**
'''

GSEditViewController.parent = property(lambda self: self.representedObject())

GSFontViewController.parent = property(lambda self: self.representedObject())
'''
	.. attribute:: parent

		The :class:`GSFont` object that this tab belongs to.

		:type: :class:`GSFont`
'''

GSEditViewController.text = property(
	lambda self: self.graphicView().displayString_(GSFormatVersionCurrent),
	lambda self, value: self.graphicView().setDisplayString_(value)
)
'''
	.. attribute:: text

		The text of the tab, either as text, or slash-escaped glyph names, or mixed. OpenType features will be applied after the text has been changed.

		:type: str

		.. code-block:: python
			string = ""
			for layer in font.selectedLayers:
			    string += "/" + layer.parent.name
			tab = font.tabs[-1]
			tab.text = string
'''

GSEditViewController.string = property(
	lambda self: self.graphicView().stringValue(),
	lambda self, value: self.graphicView().setStringValue_(value)
)
'''
	.. attribute:: string

		The plain underlying string of the tab

		:type: str

		.. code-block:: python
			string = ""
			for layer in font.selectedLayers:
			    char = font.characterForGlyph(layer.parent)
			    string += chr(char)
			tab = font.tabs[-1]
			tab.text = string

		.. versionadded:: 3.2
'''


def __GSEditViewController__str__(self):
	nameString = self.graphicView().displayString_(GSFormatVersionCurrent)
	if len(nameString) > 30:
		nameString = nameString[:30] + '...'
	nameString = nameString.replace('\n', '\\n')
	return self.description() + nameString


GSEditViewController.__str__ = python_method(__GSEditViewController__str__)

GSEditViewController.masterIndex = property(
	lambda self: self.pyobjc_instanceMethods.masterIndex(),
	lambda self, value: self.setMasterIndex_(value)
)
'''
	.. attribute:: masterIndex
		The index of the active master (selected in the toolbar).

		:type: int

		.. versionadded:: 2.6.1
'''

GSEditViewController.selectedLayers = property(lambda self: self.pyobjc_instanceMethods.selectedLayers())

GSFontViewController.selectedLayers = property(lambda self: self.pyobjc_instanceMethods.selectedLayers())


class TabLayersProxy(Generic[TypeVar('GSLayer')], ABC):

	_owner: GSEditViewController

	def __init__(self, owner: OwnerType) -> None:
		self._owner = owner

	def __getitem__(self, idx: int) -> GSLayer:
		return self.values().__getitem__(idx)

	def __delitem__(self, idx: int) -> None:
		layerRange = NSMakeRange(idx, 1)
		graphicView = self._owner.graphicView()
		charRange = graphicView.layoutManager().characterRangeForLayerRange_(layerRange)
		graphicView.insertText_replacementRange_("", charRange)

	def append(self, value):
		values = copy.copy(self.values())
		values.append(value)
		self.setter(values)

	def remove(self, value):
		values = self.values()
		values.remove(value)
		self.setter(values)

	def clear(self):
		self.setter([])

	def deactivateFeatures(self):
		self.savedFeatures = copy.copy(self._owner.features)
		self._owner.features = []

	def activateFeatures(self):
		self._owner.features = self.savedFeatures

	def setter(self, layers):
		if not isinstance(layers, (list, tuple, type(self), NSArray)):
			raise ValueError
		if isinstance(layers, type(self)):
			layers = layers.values()

		string = NSMutableAttributedString.alloc().init()
		Font = self._owner.representedObject()
		for layer in layers:
			if isinstance(layer, GSBackgroundLayer):
				char = Font.characterForGlyph_(layer.parent)
				A = NSAttributedString.alloc().initWithString_attributes_(NSString.stringWithChar_(char), {
					"GSLayerIdAttrib": layer.layerId,
					"GSShowBackgroundAttrib": True
				})
			elif isinstance(layer, GSControlLayer):
				char = layer.parent.unicodeChar()
				A = NSAttributedString.alloc().initWithString_(NSString.stringWithChar_(char))
			elif isinstance(layer, GSLayer):
				char = Font.characterForGlyph_(layer.parent)
				A = NSAttributedString.alloc().initWithString_attributes_(NSString.stringWithChar_(char), {"GSLayerIdAttrib": layer.layerId})
			elif isinstance(layer, GSGlyph):
				char = Font.characterForGlyph_(layer)
				A = NSAttributedString.alloc().initWithString_(NSString.stringWithChar_(char))
			else:
				raise ValueError
			string.appendAttributedString_(A)
		self._owner.graphicView().setStringValue_(string)

	def composedLayers(self):
		return list(self._owner.graphicView().layoutManager().cachedLayers())

	def values(self):
		layers = list(self._owner.graphicView().layoutManager().cachedLayers())
		return layers


GSEditViewController.layers = property(
	lambda self: TabLayersProxy(self),
	lambda self, value: TabLayersProxy(self).setter(value)
)
add_type(GSEditViewController, "layers", List[GSLayer])
'''
	.. attribute:: layers

		Alternatively, you can set (and read) a list of :class:`GSLayer` objects. These can be any of the layers of a glyph.

		:type: list

		.. code-block:: python
			layers = []

			# display all layers of one glyph next to each other
			for layer in font.glyphs['a'].layers:
			    layers.append(layer)

			# append line break
			layers.append(GSControlLayer(10))  # 10 being the ASCII code of the new line character (\n)

			font.tabs[0].layers = layers
'''

GSEditViewController.composedLayers = property(lambda self: TabLayersProxy(self).composedLayers())
add_type(GSEditViewController, "composedLayers", List[GSLayer])
'''
	.. attribute:: composedLayers
		Similar to the above, but this list contains the :class:`GSLayer` objects after the OpenType features have been applied (see :class:`GSEditViewController.features`). Read-only.

		Deprecated. .layers behave like this now.

		:type: list

		.. versionadded:: 2.4
'''

GSEditViewController.scale = property(
	lambda self: self.graphicView().scale(),
	lambda self, value: self.graphicView().setScale_(value)
)
add_type(GSEditViewController, "scale", float)
'''
	.. attribute:: scale

		Scale (zoom factor) of the Edit view. Useful for drawing activity in plugins.

		The scale changes with every zoom step of the Edit view. So if you want to draw objects (e.g. text, stroke thickness etc.) into the Edit view at a constant size relative to the UI (e.g. constant text size on screen), you need to calculate the object’s size relative to the scale factor. See example below.

		:type: float

		.. code-block:: python
			print(font.currentTab.scale)
			>> 0.414628537193

			# Calculate text size
			desiredTextSizeOnScreen = 10 #pt
			scaleCorrectedTextSize = desiredTextSizeOnScreen / font.currentTab.scale

			print(scaleCorrectedTextSize)
			>> 24.1179733255
'''

GSEditViewController.viewPort = property(
	lambda self: self.graphicView().userVisibleRect(),
	lambda self, value: self.graphicView().setUserVisibleRect_(value)
)

GSEditViewController.safeViewPort = property(lambda self: self.graphicView().safeVisibleRect())
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

GSEditViewController.textCursor = property(
	lambda self: self.graphicView().selectedRange().location,
	lambda self, value: self.graphicView().setSelectedRange_(NSRange(value, self.graphicView().selectedRange().length))
)
'''
	.. attribute:: textCursor
		Position of text cursor in text, starting with 0.

		:type: integer
'''

GSEditViewController.textRange = property(
	lambda self: self.contentView().selectedRange().length,
	lambda self, value: self.contentView().setSelectedRange_(NSRange(self.textCursor, value))
)
'''
	.. attribute:: textRange
		Amount of selected glyphs in text, starting at cursor position (see above).

		:type: integer
'''

GSEditViewController.selectedTextRange = property(
	lambda self: self.graphicView().selectedRange(),
	lambda self, value: self.graphicView().setSelectedRange_(value)
)
'''
	.. attribute:: selectedTextRange
		range of of selection in the text

		.. seealso:: `GSEditViewController.layers`

		:type: NSRange

		.. versionadded:: 4
'''

GSEditViewController.layersCursor = property(
	lambda self: self.graphicView().selectedLayerRange().location,
	lambda self, value: self.graphicView().setSelectedLayerRange_(NSRange(value, 0))
)
'''
	.. attribute:: layersCursor
		Position of cursor in the layers list, starting with 0.

		.. seealso:: `GSEditViewController.layers`

		:type: integer

		.. versionadded:: 2.4
'''

GSEditViewController.layersRange = property(
	lambda self: self.graphicView().selectedLayerRange().length,
	lambda self, value: self.graphicView().setSelectedLayerRange_(NSRange(self.layersCursor, value))
)
'''
	.. attribute:: layersRange
		number of selected layers

		.. seealso:: `GSEditViewController.layers`

		:type: integer

		.. versionadded:: 4
'''

GSEditViewController.selectedLayerRange = property(
	lambda self: self.graphicView().selectedLayerRange(),
	lambda self, value: self.graphicView().setSelectedLayerRange_(value)
)
'''
	.. attribute:: selectedLayerRange
		range of of selection in the layers list

		.. seealso:: `GSEditViewController.layers`

		:type: NSRange

		.. versionadded:: 4
'''

GSEditViewController.direction = property(
	lambda self: self.writingDirection(),
	lambda self, value: self.setWritingDirection_(value)
)
'''
	.. attribute:: direction

		Writing direction.

		See `Writing Directions`_

		:type: integer

		.. code-block:: python
			font.currentTab.direction = GSRTL
'''


class TabSelectedFeaturesProxy(ListProxy[GSFeature]):

	def getByIndex(self, idx: int) -> Any:
		return self._owner.selectedFeatures()[idx]

	def setByIndex(self, idx: int, value: Any) -> None:
		NotImplementedError()

	def insertAtIndex(self, idx: int, value: Any) -> None:
		NotImplementedError()

	def removeByIndex(self, idx: int) -> Any:
		del self._owner.selectedFeatures()[idx]

	def reflow(self):
		self._owner.graphicView().reflow()
		self._owner.graphicView().layoutManager().updateActiveLayer()
		self._owner._updateFeaturePopup()

	def setter(self, values):
		if not isinstance(values, (list, tuple, type(self))):
			raise TypeError
		self._owner.selectedFeatures().removeAllObjects()

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
		return self._owner.selectedFeatures()


GSEditViewController.features = property(
	lambda self: TabSelectedFeaturesProxy(self),
	lambda self, value: TabSelectedFeaturesProxy(self).setter(value)
)
'''
	.. attribute:: features

		List of OpenType features applied to text in Edit view.

		:type: list

	.. code-block:: python

		font.currentTab.features = ['locl', 'ss01']
'''

GSEditViewController.tempData = property(
	lambda self: TempDataProxy(self),
	lambda self, value: TempDataProxy(self).setter(value)
)
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


GSEditViewController.previewInstances = property(Get_ShowInPreview, Set_ShowInPreview)
'''
	.. attribute:: previewInstances
		Instances to show in the Preview area.

		Values are ``'live'`` for the preview of the current content of the Edit view, ``'all'`` for interpolations of all instances of the current glyph, or individual GSInstance objects.

		:type: str/GSInstance

		.. code-block:: python
			# Live preview of Edit view
			font.currentTab.previewInstances = 'live'

			# Text of Edit view shown in particular Instance interpolation (last defined instance)
			font.currentTab.previewInstances = font.instances[-1]

			# All instances of interpolation
			font.currentTab.previewInstances = 'all'
'''

GSEditViewController.previewHeight = property(
	lambda self: self.pyobjc_instanceMethods.previewHeight(),
	lambda self, value: self.setPreviewHeight_(value)
)
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


GSEditViewController.close = python_method(Close_Tab)
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

GSGlyphEditView.drawDark = python_method(lambda self: self.shouldDrawDark())  # type: ignore

GSMacroViewController.title = property(
	lambda self: self.pyobjc_instanceMethods.title(),
	lambda self, value: self.setTitleSave_(value)
)

##################################################################################
#
#
#
#           GSGlyphInfo
#
#
#
##################################################################################


def ____GSGlyphInfo____(): pass


GSGlyphInfo.__new__ = staticmethod(__GSObject__new__)
GSGlyphInfo.__new__.__name__ = "__new__"
GSGlyphInfo.__init__ = python_method(__empty__init__)


def __GSGlyphInfo__str__(self):
	return "<GSGlyphInfo '%s'>" % self.name


GSGlyphInfo.__str__ = python_method(__GSGlyphInfo__str__)
'''

:mod:`GSGlyphInfo`
===============================================================================

Implementation of the GSGlyphInfo object.

This contains valuable information from the glyph database. See :class:`GSGlyphsInfo` for how to create these objects.

.. class:: GSGlyphInfo()

	Properties

		* :attr:`name`
		* :attr:`productionName`
		* :attr:`category`
		* :attr:`subCategory`
		* :attr:`components`
		* :attr:`accents`
		* :attr:`anchors`
		* :attr:`unicode`
		* :attr:`unicode2`
		* :attr:`script`
		* :attr:`index`
		* :attr:`sortName`
		* :attr:`sortNameKeep`
		* :attr:`desc`
		* :attr:`altNames`
		* :attr:`direction`
		* :attr:`desc`

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

		See `Writing Directions`_

		:type: integer

		.. code-block:: python
			glyph.direction = GSRTL

		.. versionadded:: 3
'''
'''
:mod:`GSInfoValueLocalized`
===============================================================================

The GSInfoValueLocalized

.. class:: GSInfoValueLocalized()

	Properties

		* :attr:`key`
		* :attr:`values`
		* :attr:`defaultValue`

	**Properties**

'''
GSInfoValueLocalized.__new__ = staticmethod(__GSObject__new__)

GSInfoValueLocalized.__str__ = python_method(lambda self: self.values.__str__())

GSInfoValueLocalized.key = property(
	lambda self: self.pyobjc_instanceMethods.key(),
	lambda self, values: self.setKey_(values)
)
'''
	.. attribute:: key

		the key

		:type: str

	.. code-block:: python
		# searching for GSInfoValueLocalized with given "designers" key
		for fontInfo in font.properties:
		    if fontInfo.key == "designers":
		        print(fontInfo)
'''

GSInfoValueLocalized.values = property(
	lambda self: self.mutableArrayValueForKey_("values"),
	lambda self, values: self.setValues_(values)
)
'''
	.. attribute:: values

		A list of :class:`GSInfoValue` objects.

		:type: list

	.. code-block:: python
		# listing values of GSInfoValueLocalized
		for fontInfoValue in fontInfoValueLocalized.values:
		    print(fontInfoValue)
'''

GSInfoValueLocalized.defaultValue = property(lambda self: self.pyobjc_instanceMethods.defaultValue())

GSInfoValueLocalized.value = GSInfoValueLocalized.defaultValue

'''
	.. attribute:: defaultValue
		the value that is considered the default (either the dflt or English entry)

		:type: str

	.. code-block:: python
		# prints the default value for given GSInfoValueLocalized instance
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

:mod:`GSInfoValueSingle`
===============================================================================

The GSInfoValueSingle

.. class:: GSInfoValueSingle()

	Properties

		* :attr:`key`
		* :attr:`value`

	**Properties**

'''
GSInfoValueSingle.__new__ = staticmethod(__GSObject__new__)

GSInfoValueSingle.key = property(
	lambda self: self.pyobjc_instanceMethods.key(),
	lambda self, values: self.setKey_(values)
)
'''
	.. attribute:: key

		the key

		:type: str

	.. code-block:: python
		# GSInfoValueSingle is stored in e.g. font.properties
		# one of the differences between GSInfoValueSingle and GSInfoValueLocalized
		# is that the first doesn't have "values" attribute
		for fontProperty in font.properties:
		    if not hasattr(fontProperty, "values"):
		        print(fontProperty.key)
'''

GSInfoValueSingle.value = property(
	lambda self: self.pyobjc_instanceMethods.value(),
	lambda self, value: self.setValue_(value)
)
'''
	.. attribute:: value

		The value

		:type: str

	.. code-block:: python
		# GSInfoValueSingle is stored in e.g. font.properties
		# one of the differences between GSInfoValueSingle and GSInfoValueLocalized
		# is that the first doesn't have "values" attribute
		for fontProperty in font.properties:
		    if not hasattr(fontProperty, "values"):
		        print(fontProperty.value)
'''
'''
:mod:`GSInfoValue`
===============================================================================

The GSInfoValue

.. class:: GSInfoValue()

		* :attr:`key`
		* :attr:`value`
		* :attr:`languageTag`

	**Properties**

'''
GSInfoValue.__new__ = staticmethod(__GSObject__new__)


def __GSInfoValue__str__(self):
	return f"{self.key}: {self.value}"


GSInfoValue.__str__ = python_method(__GSInfoValue__str__)

GSInfoValue.key = property(
	lambda self: self.pyobjc_instanceMethods.key(),
	lambda self, values: self.setKey_(values)
)
'''
	.. attribute:: key

		the key

		:type: str

	.. code-block:: python
		# GSInfoValue is stored in e.g. values attribute of font.properties
		for fontProperty in font.properties:

		    # not all of font.properties contains this attribute
		    # so we are going to look for those, that have it
		    if hasattr(fontProperty, "values"):
		        for fontInfoValue in fontProperty.values:
		            # this line prints out the key attribute of
		            # found GSInfoValue instance
		            print(fontInfoValue.key)
'''

GSInfoValue.value = property(
	lambda self: self.pyobjc_instanceMethods.value(),
	lambda self, value: self.setValue_(value)
)
'''
	.. attribute:: value

		The value

		:type: str

	.. code-block:: python
		# GSInfoValue is stored in e.g. values attribute of font.properties
		for fontProperty in font.properties:

		    # not all of font.properties contains this attribute
		    # so we are going to look for those, that have it
		    if hasattr(fontProperty, "values"):
		        for fontInfoValue in fontProperty.values:
		            # this line prints out the value attribute of
		            # found GSInfoValue instance
		            print(fontInfoValue.value)
'''

GSInfoValue.languageTag = property(
	lambda self: self.pyobjc_instanceMethods.languageTag(),
	lambda self, value: self.setLanguageTag_(value)
)
'''
	.. attribute:: languageTag
		The languageTag

		:type: str

	.. code-block:: python
		# GSInfoValue is stored in e.g. values attribute of font.properties
		for fontProperty in font.properties:

		    # not all of font.properties contains this attribute
		    # so we are going to look for those, that have it
		    if hasattr(fontProperty, "values"):
		        for fontInfoValue in fontProperty.values:
		            # this line prints out the languageTag attribute of
		            # found GSInfoValue instance
		            print(fontInfoValue.languageTag)
'''
'''
:mod:`GSMetricStore`
===============================================================================

The GSMetricStore objects represent vertical metrics values and theirs overshoots.

.. class:: GSMetricStore()

		* :attr:`position`
		* :attr:`overshoot`
		* :attr:`name`
		* :attr:`filter`
		* :attr:`metric`

	**Properties**
'''


def __GSMetricStore__init__(self, position: float | None = None, overshoot: float | None = None):
	if position is not None:
		self.position = float(position)
	if overshoot is not None:
		self.overshoot = float(overshoot)


GSMetricStore.__new__ = staticmethod(__GSObject__new__)
GSMetricStore.__new__.__name__ = "__new__"
GSMetricStore.__init__ = python_method(__GSMetricStore__init__)


GSMetricStore.position = property(
	lambda self: self.pyobjc_instanceMethods.position(),
	lambda self, value: self.setPosition_(value)
)
'''
	.. attribute:: position

		The y position of the metric.

		:type: float
'''

GSMetricStore.overshoot = property(
	lambda self: self.pyobjc_instanceMethods.overshoot(),
	lambda self, value: self.setOvershoot_(value)
)
'''
	.. attribute:: overshoot

		Value of overshoot’s width.

		:type: float
'''

GSMetricStore.size = GSMetricStore.overshoot  # compatibility

GSMetricStore.name = property(lambda self: self.title())
'''
	.. attribute:: name

		The name of the metric value. Eg. Descender, Small Cap, Cap Height etc.

		:type: str
'''

GSMetricStore.filter = property(lambda self: self.pyobjc_instanceMethods.filter())
'''
	.. attribute:: filter

		A filter to limit the scope of the metric.

		:type: NSPredicate
'''

GSMetricStore.metric = property(lambda self: self.pyobjc_instanceMethods.metric())
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

		* :attr:`text`
		* :attr:`font`
		* :attr:`instanceIndex`
		* :attr:`fontSize`

	Functions

		* :meth:`open`
		* :meth:`close`

	**Properties**
'''

PreviewTextWindow.__class__.font = property(lambda self: self.defaultInstance().activeFont())
'''
	.. attribute:: font

		The font

		:type: GSFont
'''

PreviewTextWindow.__class__.text = property(
	lambda self: self.defaultInstance().textView().string(),
	lambda self, value: self.defaultInstance().textView().setString_(value)
)
'''
	.. attribute:: text

		The text

		:type: str
'''

PreviewTextWindow.__class__.instanceIndex = property(
	lambda self: Glyphs.intDefaults["GSPreviewTextInstanceIndex"],
	lambda self, value: NSUserDefaults.standardUserDefaults().setObject_forKey_(value, objcObject("GSPreviewTextInstanceIndex"))
)
'''
	.. attribute:: instanceIndex
		The index of the selected instance

		:type: int
'''

PreviewTextWindow.__class__.fontSize = property(
	lambda self: Glyphs.intDefaults["GSPreviewTextFontSize"],
	lambda self, value: NSUserDefaults.standardUserDefaults().setObject_forKey_(value, objcObject("GSPreviewTextFontSize"))
)
'''
	.. attribute:: fontSize
		The font size

		:type: int
'''


def __PreviewTextWindow__open(self):
	PreviewTextWindow.defaultInstance().openWindow()


PreviewTextWindow.open = classmethod(__PreviewTextWindow__open)
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


def __PreviewTextWindow__reloadFont(self):
	PreviewTextWindow.defaultInstance().reloadFont()


PreviewTextWindow.reloadFont = classmethod(__PreviewTextWindow__reloadFont)
'''
	.. function:: reloadFont()

		refreshes the Preview Text Window
'''


def __PreviewTextWindow__close(self):
	PreviewTextWindow.defaultInstance().closeWindow_(None)


PreviewTextWindow.close = classmethod(__PreviewTextWindow__close)
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


def __GSPathPen_addPoint__(self, pt, segmentType=None, smooth: bool | None = False, name=None, identifier=None, **kwargs):
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

	Properties

		* :attr:`matrix`

	Functions

		* :meth:`shift`
		* :meth:`scale`
		* :meth:`rotate`
		* :meth:`skew`

	**Functions**

'''

NSAffineTransform.__new__ = staticmethod(__GSObject__new__)  # type: ignore


def NSAffineTransform__shift(self, value):
	value = validatePoint(value)
	self.translateXBy_yBy_(value[0], value[1])


NSAffineTransform.shift = python_method(NSAffineTransform__shift)  # type: ignore
'''
	.. function:: shift(x, y)

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


NSAffineTransform.scale = python_method(NSAffineTransform__scale)  # type: ignore
'''
	.. function:: scale(x, [y])

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


NSAffineTransform.rotate = python_method(NSAffineTransform__rotate)  # type: ignore
'''
	.. function:: rotate(angle)

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


NSAffineTransform.skew = python_method(NSAffineTransform__skew)  # type: ignore
'''
	.. function:: skew(x, [center])

		if a single number, skew in x-direction otherwise skew by x, y
		if center is given, that is used as the origin of the skew

		:type: int/float or tuple
'''

NSAffineTransform.matrix = property(  # type: ignore
	lambda self: tuple(self.transformStruct()),
	lambda self, value: self.setTransformStruct_(value)
)
'''
	**Properties**

	.. attribute:: matrix

		a transform matrix (m11, m12, m21, m22, x, y)

		:type: tuple
'''

'''

:mod:`NSMenu`
===============================================================================

The NSMenuItem object.

.. class:: NSMenu()

	Functions

		* :meth:`append`
		* :meth:`insert`

	**Functions**
'''


def __NSMenu__append__(self, item):
	self.addItem_(item)


NSMenu.append = python_method(__NSMenu__append__)  # type: ignore

'''
	.. function:: append(item)

		:param item: a NSMenuItem

		adds the item to the menu
'''


def __NSMenu__insert__(self, idx, item):
	self.insertItem_atIndex_(item, idx)


NSMenu.insert = python_method(__NSMenu__insert__)  # type: ignore
'''
	.. function:: insert(idx, item)

		:param idx: the index
		:param item: a NSMenuItem

		inserts the item into the items submenu at the specified index


:mod:`NSMenuItem`
===============================================================================

The NSMenuItem object.

.. class:: NSMenuItem([title, callback=None, target=None, keyboard=None, modifier=0])

	:param title: The title of the item.
	:param callback: a method/selector that is called when the menu item is clicked.
	:param target: the object that the selector is called on.
	:param keyboard: A keyboard short key. e.g. "k"
	:param modifier: the modifiers (e.g. the Command key). Add all modifier of all keys you like together (e.g. NSCommandKeyMask + NSAlternateKeyMask)

	When called from a class that inherits from NSObject (e.g. plugins), use callback and target=self. Don’t add the ``@objc.python_method`` decorator.
	When called from a script, only set the callback with any python method

	Properties

	Functions

		* :meth:`append`
		* :meth:`insert`

'''

NSMenuItem.__new__ = staticmethod(__GSObject__new__)  # type: ignore


def __NSMenuItem__init__(self, title, callback=None, target=None, keyboard=None, modifier=0):
	self.setTitle_(title)
	if callback:
		if isinstance(callback, objc.selector) or target:
			self.setAction_(callback)
			if target:
				self.setTarget_(target)
		else:
			callbackTargets: list
			try:
				callbackTargets = callbackOperationTargets["NSMenuItem"]  # type: ignore XXX
			except KeyError:
				callbackTargets = []
				callbackOperationTargets["NSMenuItem"] = callbackTargets  # type: ignore XXX
			helper = callbackHelperClass(callback, None)
			callbackTargets.append(helper)
			selector = objc.selector(helper.callback_, signature=b"v@:@")
			self.setAction_(selector)
			self.setTarget_(helper)
	if keyboard and keyboard != "":
		self.setKeyEquivalent_(keyboard)
		self.setKeyEquivalentModifierMask_(modifier)


NSMenuItem.__init__ = python_method(__NSMenuItem__init__)  # type: ignore


def __NSMenuItem__append__(self, item):
	self.submenu().addItem_(item)


NSMenuItem.append = python_method(__NSMenuItem__append__)  # type: ignore
'''
	.. function:: append(item)

		:param item: a NSMenuItem

		adds another item to the items submenu
'''


def __NSMenuItem__insert__(self, idx, item):
	self.submenu().insertItem_atIndex_(item, idx)


NSMenuItem.insert = python_method(__NSMenuItem__insert__)  # type: ignore
'''
	.. function:: insert(idx, item)

		:param idx: the index
		:param item: a NSMenuItem

		inserts the item into the items submenu at the specified index
'''


FTPointArray.__len__ = python_method(lambda self: self.count())


def __FTPointArray__getitem__(self, key):
	if isinstance(key, int):
		idx = _validate_idx(cast(Sequence, self), key)
		return self.pointAtIndex_(idx)
	elif isinstance(key, slice):
		# Handle slice access
		length = len(self)
		start, stop, step = key.indices(length)
		# Collect items at the specified indices
		result = []
		for idx in range(start, stop, step):
			result.append(self.pointAtIndex_(idx))
		return result
	raise IndexError("list index out of range")


FTPointArray.__getitem__ = python_method(__FTPointArray__getitem__)


def __FTPointArray__setitem__(self, point, idx):
	if idx <= self.count():
		return self.setPoint_atIndex_(point, idx)
	raise IndexError("list index out of range")


FTPointArray.__setitem__ = python_method(__FTPointArray__getitem__)


def __FTPointArray__insert__(self, idx, point):
	if idx <= self.count():
		return self.insertPoint_atIndex_(point, idx)
	raise IndexError("list index out of range")


FTPointArray.insert = python_method(__FTPointArray__insert__)


'''

Methods
=======

	* :meth:`divideCurve`
	* :meth:`pointOnLine`
	* :meth:`pointOnQuadratic`
	* :meth:`distance`
	* :meth:`addPoints`
	* :meth:`subtractPoints`
	* :meth:`scalePoint`
	* :meth:`removeOverlap`
	* :meth:`subtractPaths`
	* :meth:`intersectPaths`
	* :meth:`GetOpenFile`
	* :meth:`GetSaveFile`
	* :meth:`GetFolder`
	* :meth:`AskString`
	* :meth:`PickGlyphs`
	* :meth:`Message`
	* :meth:`LogToConsole`
	* :meth:`LogError`

'''
def divideCurve(P0: NSPoint, P1: NSPoint, P2: NSPoint, P3: NSPoint, t: float) -> tuple[NSPoint, NSPoint, NSPoint, NSPoint, NSPoint, NSPoint, NSPoint]:
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

	return (
		P0,
		NSMakePoint(Q0x, Q0y),
		NSMakePoint(R0x, R0y),
		NSMakePoint(Sx, Sy),
		NSMakePoint(R1x, R1y),
		NSMakePoint(Q2x, Q2y),
		P3
	)


'''
.. function:: divideCurve(P0, P1, P2, P3, t)

	Divides the curve using the De Casteljau’s algorithm.

	:param P0: The start point of the curve (NSPoint)
	:param P1: The first off curve point
	:param P2: The second off curve point
	:param P3: The end point of the curve
	:param t: The time parameter
	:return: A list of points that represent two curves. (Q0, Q1, Q2, Q3, R1, R2, R3). Note that the ‘middle’ point is only returned once.
	:rtype: list
'''


def pointOnLine(P0: NSPoint, P1: NSPoint, t: float) -> NSPoint:
	return NSMakePoint(P0.x + ((P1.x - P0.x) * t), P0.y + ((P1.y - P0.y) * t))

'''
.. function:: pointOnLine(P0, P1, t)

	the point at t

	:param P0: The Start point of the line (NSPoint)
	:param P1: The End point of the line
	:param t: The time parameter
	:return: a point
	:rtype: NSPoint
'''


def pointOnQuadratic(P0: NSPoint, P1: NSPoint, P2: NSPoint, t: float) -> NSPoint:
	Q0x = P0.x + ((P1.x - P0.x) * t)
	Q0y = P0.y + ((P1.y - P0.y) * t)

	Q1x = P1.x + ((P2.x - P1.x) * t)
	Q1y = P1.y + ((P2.y - P1.y) * t)
	return NSMakePoint(Q0x + ((Q1x - Q0x) * t), Q0y + ((Q1y - Q0y) * t))


'''
.. function:: pointOnQuadratic(P0, P1, P2, t):

	the point at t

	:param P0: The start point of the curve (NSPoint)
	:param P1: The first off curve point
	:param P2: The end point of the curve
	:param t: The time parameter
	:return: a point
	:rtype: NSPoint
'''


def distance(P1: NSPoint, P2: NSPoint) -> float:
	return math.hypot(P1[0] - P2[0], P1[1] - P2[1])


'''
.. function:: distance(P0, P1)

	calculates the distance between two NSPoints

	:param P0: a NSPoint
	:param P1: another NSPoint
	:return: The distance
	:rtype: float
'''


def addPoints(P1: NSPoint | tuple, P2: NSPoint | tuple) -> NSPoint:
	return NSMakePoint(P1[0] + P2[0], P1[1] + P2[1])


'''
.. function:: addPoints(P1, P2)

	Add the points.

	:param P0: a NSPoint
	:param P1: another NSPoint
	:return: The sum of both points
	:rtype: NSPoint
'''


def subtractPoints(P1: NSPoint | tuple, P2: NSPoint | tuple) -> NSPoint:
	return NSMakePoint(P1[0] + P2[0], P1[1] - P2[1])


'''
.. function:: subtractPoints(P1, P2)

	Subtracts the points.

	:param P0: a NSPoint
	:param P1: another NSPoint
	:return: The subtracted point
	:rtype: NSPoint
'''


def scalePoint(P: NSPoint, scalar: float) -> NSPoint:
	return NSMakePoint(P[0] * scalar, P[1] * scalar)


'''
.. function:: scalePoint(P, scalar)

	Scaled a point.

	:param P: a NSPoint
	:param scalar: The multiplier
	:return: The multiplied point
	:rtype: NSPoint
'''

def removeOverlap(paths: Sequence[GSPath]) -> NSMutableArray[GSPath] | None:
	mutable_paths: NSMutableArray = NSMutableArray.arrayWithArray_(cast(NSArray, paths))

	result_tuple: tuple[bool, NSError | None] = GSPathFinder.removeOverlapPaths_error_(mutable_paths, None)

	if result_tuple[0] != 1:
		return None
	return mutable_paths


'''
.. function:: removeOverlap(paths)

	removes the overlaps from the list of paths

	.. code-block:: python
		paths = [path1, path2, path3]
		mergePaths = removeOverlap(paths)

	:param paths: A list of paths
	:return: The resulting list of paths
	:rtype: list
'''


def subtractPaths(paths: Sequence[GSPath], subtract: Sequence[GSPath]) -> List[GSPath] | None:

	mutablePath: NSMutableArray
	if isinstance(paths, LayerShapesProxy):
		mutablePath = NSMutableArray.arrayWithArray_(paths.values())
	else:
		mutablePath = NSMutableArray.arrayWithArray_(cast(NSArray, paths))

	mutableSubtract: NSMutableArray
	if isinstance(subtract, LayerShapesProxy):
		mutableSubtract = NSMutableArray.arrayWithArray_(subtract.values())
	else:
		mutableSubtract = NSMutableArray.arrayWithArray_(cast(NSArray, subtract))

	result = GSPathFinder.subtractPaths_from_error_(mutableSubtract, mutablePath, None)
	if result[0] != 1:
		return None
	return cast(List, paths)


'''
.. function:: subtractPaths(paths, subtract)

	removes the overlaps from the list of paths

	:param paths: a list of paths
	:param subtract: the subtracting paths
	:return: The resulting list of paths
	:rtype: list
'''


def intersectPaths(paths: Sequence[GSPath], otherPaths: Sequence[GSPath]) -> List[GSPath] | None:
	mutablePath: NSMutableArray
	if isinstance(paths, LayerShapesProxy):
		mutablePath = NSMutableArray.arrayWithArray_(paths.values())
	else:
		mutablePath = NSMutableArray.arrayWithArray_(cast(NSArray, paths))

	mutableOther: NSMutableArray
	if isinstance(otherPaths, LayerShapesProxy):
		mutableOther = NSMutableArray.arrayWithArray_(otherPaths.values())
	else:
		mutableOther = NSMutableArray.arrayWithArray_(cast(NSArray, otherPaths))

	result = GSPathFinder.intersectPaths_with_error_(mutablePath, mutableOther, None)
	if result[0] != 1:
		return None
	return cast(list, mutableOther)


'''
.. function:: intersectPaths(paths, otherPaths)

	removes the overlaps from the list of paths

	:param paths: a list of paths
	:param otherPaths: the other paths
	:return: The resulting list of paths
	:rtype: list
'''

def GetSaveFile(message: str | None = None, proposedFileName: str | None = None, filetypes: List[str] | None = None, filetype: str | None = None) -> str | None:
	panel = NSSavePanel.savePanel().retain()
	panel.setExtensionHidden_(False)
	panel.setCanCreateDirectories_(True)
	if message is not None:
		panel.setTitle_(message)
	if filetype is not None and filetypes is None:
		filetypes = [filetype]
	if filetypes is not None and len(filetypes) > 0:
		panel.setAllowedFileTypes_(cast(NSArray, objcObject(filetypes)))
	if proposedFileName is not None:
		if proposedFileName.find("/") >= 0:
			path, proposedFileName = os.path.split(proposedFileName)
			panel.setDirectoryURL_(NSURL.fileURLWithPath_(path))
		panel.setNameFieldStringValue_(proposedFileName)
	pressedButton = panel.runModal()
	if pressedButton == NSModalResponseOK:
		return panel.filename()
	return None


'''
.. function:: GetSaveFile(message=None, ProposedFileName=None, filetypes=None)

	Opens a file chooser dialog.

	:param message:
	:param filetypes:
	:param ProposedFileName:
	:return: The selected file or None
	:rtype: str
'''


def __Dict_allItems__(self):
	items = []
	for key in self.allKeys():
		value = self.objectForKey_(key)
		items.append((key, value))
	return items


MGOrderedDictionary.items = python_method(__Dict_allItems__)


def __Dict_allKeys__(self):
	return self.allKeys()


MGOrderedDictionary.keys = python_method(__Dict_allKeys__)


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


def __Dict_getitem__(self, key):
	return self.objectForKey_(key)


MGOrderedDictionary.__getitem__ = python_method(__Dict_getitem__)

GSNotifyingDictionary.items = python_method(__Dict_allItems__)
GSNotifyingDictionary.keys = python_method(__Dict_allKeys__)
GSNotifyingDictionary.__len__ = property(lambda self: self.count)
GSNotifyingDictionary.__getitem__ = python_method(__Dict_getitem__)

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

MGOrderedDictionary.__delattr__ = python_method(lambda self, key: self.removeObjectForKey_(key))


def GetFile(message=None, title=None, allowsMultipleSelection: bool = False, filetypes=None):
	return GetOpenFile(message, title, allowsMultipleSelection, filetypes)


def GetOpenFile(message: str | None = None, title: str | None = None, allowsMultipleSelection: bool = False, filetypes: list | None = None, path: str | None = None) -> str | NSArray | None:
	if filetypes is None:
		filetypes = []
	panel = NSOpenPanel.new()
	panel.setCanChooseFiles_(True)
	panel.setCanChooseDirectories_(False)
	panel.setCanCreateDirectories_(True)
	panel.setAllowsMultipleSelection_(allowsMultipleSelection)
	if path is not None:
		panel.setDirectory_(path)
	if message is not None:
		panel.setMessage_(message)
	if title is not None:
		panel.setTitle_(title)
	if filetypes is not None:
		if isString(filetypes):
			filetypes = [filetypes]
		if len(filetypes) > 0:
			panel.setAllowedFileTypes_(cast(NSArray, objcObject(filetypes)))
	pressedButton = panel.runModal()
	result: str | NSArray | None = None
	if pressedButton == NSModalResponseOK:
		if allowsMultipleSelection:
			result = panel.filenames()
		else:
			result = panel.filename()
	panel.release()
	return result


'''
.. function:: GetOpenFile(message=None, allowsMultipleSelection=False, filetypes=None, path=None)

	Opens a file chooser dialog.

	:param message: A message string.
	:param allowsMultipleSelection: Boolean, True if user can select more than one file
	:param filetypes: list of strings indicating the filetypes, e.g., ["gif", "pdf"]
	:param path: The initial directory path
	:return: The selected file or a list of file names or None
	:rtype: str or list
'''


def GetFolder(message: str | None = None, allowsMultipleSelection: bool = False, path: str | None = None):
	panel = NSOpenPanel.new()
	panel.setCanChooseFiles_(False)
	panel.setCanChooseDirectories_(True)
	panel.setCanCreateDirectories_(True)
	panel.setAllowsMultipleSelection_(allowsMultipleSelection)
	if message is not None:
		panel.setMessage_(message)
	if path is not None:
		panel.setDirectory_(path)
	pressedButton = panel.runModal()
	result = None
	if pressedButton == NSModalResponseOK:
		if allowsMultipleSelection:
			result = panel.filenames()
		else:
			result = panel.filename()
	panel.release()
	return result


'''
.. function:: GetFolder(message=None, allowsMultipleSelection=False, path=None)

	Opens a folder chooser dialog.

	:param message:
	:param allowsMultipleSelection:
	:param path:
	:return: The selected folder or None
	:rtype: str
'''


def Message(message, title="Alert", OKButton=None, cancelButton=None, otherButton=None):
	print("__message", message, "__OKButton", OKButton, "__cancelButton", cancelButton)
	return Glyphs.showAlert_message_OKButton_cancelButton_otherButton_(title, message, OKButton, cancelButton, otherButton)


'''
.. function:: Message(message, title="Alert", OKButton=None)

	Shows an alert panel.

	:param message: the string
	:param title: a title of the dialog
	:param OKButton: the label of the confirmation button
'''


def AskString(message, value=None, title="Glyphs", OKButton=None, placeholder=None):
	result = Glyphs.showAskString_message_defaultText_placeholder_OKButton_(title, message, value, placeholder, OKButton)
	return result


'''

.. function:: AskString(message, value=None, title="Glyphs", OKButton=None, placeholder=None)

	AskString Dialog

	:param message: the string
	:param value: a default value
	:param title: a title of the dialog
	:param OKButton: the label of the confirmation button
	:param placeholder: a placeholder value that is displayed in gray when the text field is empty
	:return: the string
	:rtype: str
'''


def PickGlyphs(content=None, masterID=None, searchString=None, defaultsKey=None):
	selectGlyphPanel = GSSelectGlyphsDialogController.sharedHandler()

	if defaultsKey is not None:
		selectGlyphPanel.setSearchUserDefaultsKey_(defaultsKey)
	elif searchString and len(searchString) > 0:
		selectGlyphPanel.setSearch_(searchString)

	if masterID is None:
		masterID = Glyphs.font.selectedFontMaster.id
	selectGlyphPanel.setMasterID_(masterID)
	if content is not None:
		if not isinstance(content, (list, NSArray)):
			raise TypeError("content needs to be a list, not %@", type(content))
		selectGlyphPanel.setContent_(content)
	else:
		selectGlyphPanel.setContent_(list(Glyphs.font.glyphs))

	if selectGlyphPanel.runModal():
		glyphs = list(selectGlyphPanel.selectedGlyphs())
		search = selectGlyphPanel.search()
		return (glyphs, search)

	return None


'''

.. function:: PickGlyphs(content=None, masterID=None, searchString=None, defaultsKey=None)

	Shows a dialog to select a glyph and returns the selected glyphs.

	:param content: a list of glyphs from with to pick from (e.g. filter for corner components)
	:param masterID: The master ID to use for the previews
	:param searchString: to pre-populate the search
	:param defaultsKey: The userDefaults to read and store the search key. Setting this will ignore the searchString

	:return: the list of selected glyphs and the typed search string
	:rtype: tuple(list, str)

	.. versionadded:: 3.2
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


def LogError(message: str):
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


.. _node-types:

Node Types
----------

.. data:: LINE

	Line node.

.. data:: CURVE

	Curve node. Make sure that each curve node is preceded by two off-curve nodes.

.. data:: QCURVE

	Quadratic curve node. Make sure that each curve node is preceded by at least one off-curve node.

.. data:: OFFCURVE

	Off-curve node


.. _path-attributes:

Path Attributes
---------------

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


.. _file-format-versions:

File Format Versions
--------------------

A constant that is used when saving are reading .glyphs file but also for the clipboard.

.. data:: GSFormatVersion1

	The Format used by Glyphs 2

.. data:: GSFormatVersion3

	The Format used by Glyphs 3

.. data:: GSFormatVersionCurrent

	This will always return the format of the current app.


.. _export-formats:

Export Formats
--------------

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

.. versionadded:: 2.5


.. _info-property-keys:

Info Property Keys
------------------

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

.. data:: GSPropertyNameFullFontNamesKey

	FullFontNames

.. data:: GSPropertyNamePostScriptNameKey

	PostscriptName

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

.. data:: GSPropertyNameVariablePostScriptNamePrefixKey

	VariablePostScriptNamePrefix

.. versionadded:: 3.1


.. _instance-types:

Instance Types
--------------

.. data:: INSTANCETYPESINGLE

	single interpolation instance

.. data:: INSTANCETYPEVARIABLE

	variable font setting

.. versionadded:: 3.0.1


.. _hint-types:

Hint Types
----------

.. data:: GSHintTypeTopGhost

	Top ghost for PS hints

.. data:: STEM

	Stem for PS hints

.. data:: GSHintTypeBottomGhost

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


.. _hint_option:

Hint Option
-----------

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


.. _menu-tags:

Menu Tags
---------

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


.. _menu_states:

Menu States
-----------

.. data:: ONSTATE

	The menu entry will have a checkbox

.. data:: OFFSTATE

	The menu entry will have no checkbox

.. data:: MIXEDSTATE

	The menu entry will have horizontal line


.. _callback-keys:

Callback Keys
-------------

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

.. data:: FILTER_FLAT_KERNING

	is called when exporting a kern table

	In a (general) plugin, implement a method like this:

	.. code-block:: python
		@objc.typedSelector(b'@@:@o^@')
		def filterFlatKerning_error_(self, flatKerning, error):
			newKerning = list()
			for kern in flatKerning:
				name1 = kern[0]
				name2 = kern[1]
				if len(name1) > 1 and len(name2) > 1:  # this is way oversimplified.
					continue
				if abs(kern[2]) < 10:  # ignore small pairs
					continue
				newKerning.append(kern)
			return newKerning, None

	Register the callback like this:

	.. code-block:: python
		GSCallbackHandler.addCallback_forOperation_(self, FILTER_FLAT_KERNING)  # self needs to be a subclass of NSObject (as all plugins are)

	.. versionadded:: 3.2


.. _writing-directions:

Writing Directions
------------------

The writing directions of the Edit View.

.. data:: GSBIDI

	for characters that follow the main writing direction (like punctuation)

.. data:: GSLTR

	Left to Right (e.g. Latin)

.. data:: GSRTL

	Right to Left (e.g. Arabic, Hebrew)

.. data:: GSVertical

	Top to Bottom, Right to Left (e.g. Chinese, Japanese, Korean)

.. data:: GSVerticalToRight

	Top to Bottom, Left to Right (e.g. Mongolian)


.. _shape-types:

Shape Type
----------

.. data:: GSShapeTypePath

	Path

.. data:: GSShapeTypeComponent

	Component


.. _annotation_types:

Annotation Types
----------------

.. data:: TEXT

.. data:: ARROW

.. data:: CIRCLE

.. data:: PLUS

.. data:: MINUS


.. _inspector-sizes:

Inspector Sizes
---------------

.. data:: GSInspectorSizeSmall

.. data:: GSInspectorSizeRegular

.. data:: GSInspectorSizeLarge

.. data:: GSInspectorSizeXLarge


.. _metrics-types:

Metrics Types
-------------

metrics types are used in :attr:`GSFont.metrics`. see :attr:`GSMetric.type`

.. data:: GSMetricsTypeUndefined

.. data:: GSMetricsTypeAscender

.. data:: GSMetricsTypeCapHeight

.. data:: GSMetricsTypeSlantHeight

.. data:: GSMetricsTypexHeight

.. data:: GSMetricsTypeMidHeight

.. data:: GSMetricsTypeBodyHeight

.. data:: GSMetricsTypeDescender

.. data:: GSMetricsTypeBaseline

.. data:: GSMetricsTypeItalicAngle


.. _component-alignment:

Component Alignment
-------------------

constant for the :attr:`GSComponent.alignment` property

.. data:: GSAlignmentNoAligned

.. data:: GSAlignmentDisable

.. data:: GSAlignmentDefault

.. data:: GSAlignmentForce

.. data:: GSAlignmentAligned

.. data:: GSAlignmentHorizontal


'''

# bundle = NSBundle.bundleForClass_(GSFont)
# objc.loadBundleFunctions(bundle, globals(), [("GSExtremeTimesOfCubic", b'v{CGPoint=dd}{CGPoint=dd}{CGPoint=dd}{CGPoint=dd}o^do^do^do^d')])
# objc.loadBundleFunctions(bundle, globals(), [("GSIntersectLineLineUnlimited", '{CGPoint=dd}{CGPoint=dd}{CGPoint=dd}{CGPoint=dd}{CGPoint=dd}')])
