# encoding: utf-8

from __future__ import annotations
import os
import traceback
import objc
from objc import python_method
from typing import Optional, List, Dict, Tuple, Any, TYPE_CHECKING, cast

from Foundation import NSPoint, NSString, NSAttributedString, NSURL, NSClassFromString

from AppKit import (
	NSUserDefaults,
	NSError,
	NSLocalizedDescriptionKey,
	NSLocalizedRecoverySuggestionErrorKey,
	NSLocalizedString,
	NSBundle,
	NSColor,
	NSNib,
	NSMenu,
	NSMenuItem,
	NSView,
	NSImage,
	NSFont,
	NSFontAttributeName,
	NSForegroundColorAttributeName,
	NSEvent,
	NSViewController,
)

if TYPE_CHECKING:
	from . import Glyphs, GSFont, GSLayer, GSUserNotification, GSEditViewController, LogToConsole, LogError, ONSTATE, OFFSTATE, MIXEDSTATE, Message, objcObject, GSWindowController
	from .plugins import GSToolPlugin, GSFilterPlugin, GSToolSelect, BaseFileFormatPlugin, BaseFilterWithoutDialog, BaseGeneralPlugin, BasePalettePlugin, BaseReporterPlugin, GSPaletteView
else:
	from GlyphsApp import GSEditViewController, Glyphs, LogError
	GSWindowController = objc.lookUpClass("GSWindowController")
	GSToolPlugin = objc.lookUpClass("GSToolPlugin")
	GSToolPlugin = objc.lookUpClass("GSToolPlugin")
	GSFilterPlugin = objc.lookUpClass("GSFilterPlugin")
	GSToolSelect = objc.lookUpClass("GSToolSelect")
	BaseFileFormatPlugin = objc.lookUpClass("BaseFileFormatPlugin")
	BaseFilterWithoutDialog = objc.lookUpClass("BaseFilterWithoutDialog")
	BaseGeneralPlugin = objc.lookUpClass("BaseGeneralPlugin")
	BasePalettePlugin = objc.lookUpClass("BasePalettePlugin")
	BaseReporterPlugin = objc.lookUpClass("BaseReporterPlugin")
	GSPaletteView = objc.lookUpClass("GSPaletteView")

__all__ = [
	"Glyphs", "FileFormatPlugin", "FilterWithDialog", "FilterWithoutDialog", "GeneralPlugin", "PalettePlugin", "ReporterPlugin", "SelectTool",
	"GSFilterPlugin", "GSToolSelect", "BaseFileFormatPlugin", "BaseFilterWithoutDialog", "BaseGeneralPlugin", "BasePalettePlugin", "BasePalettePlugin", "BaseReporterPlugin",
	"setUpMenuHelper"
]

############################################################################################

#  Helper methods


def LogToConsole_AsClassExtension(self, message: str) -> None:
	LogToConsole(message, self.title())  # from GlyphsApp.py


def LogError_AsClassExtension(self, message: str) -> None:
	LogError("Error in Plugin: %s: %s" % (self.__class__.__name__, message))  # from GlyphsApp.py


def LoadNib(self, nibname: str, path: Optional[str] = None) -> None:
	if path and len(path) > 10:
		try:
			bundlePath = path[:path.find("/Contents/Resources/")]
			bundle = NSBundle.bundleWithPath_(bundlePath)
			nib: NSNib = NSNib.alloc().initWithNibNamed_bundle_(nibname, bundle)
			if not nib:
				LogError("Error loading nib for Class: %s" % self.__class__.__name__)

			result = nib.instantiateWithOwner_topLevelObjects_(self, None)
			if not bool(result[0]):
				LogError("Error instantiating nib for Class: %s" % self.__class__.__name__)
			else:
				self.topLevelObjects = result[1]
		except:
			LogError(traceback.format_exc())
	else:
		if not NSBundle.loadNibNamed_owner_(nibname, self):
			LogError("Error loading %s.nib." % nibname)


def pathForResource(resourceName: str, extension: str, path: Optional[str] = None) -> Optional[str]:
	if path and len(path) > 10:
		bundlePath = path[:path.find("/Contents/Resources/")]
		bundle = NSBundle.bundleWithPath_(bundlePath)
		return bundle.pathForResource_ofType_(resourceName, extension)
	else:
		raise ValueError("Please supply path")


def setUpMenuHelper(menu: NSMenu, items: List[Dict[str, Any]], defaultTarget: Any) -> None:
	if not isinstance(items, list):
		return

	for entry in items:

		if "index" in entry:
			index = int(entry["index"])
		else:
			index = -1

		# Use supplied NSMenuItem
		if "menu" in entry:
			newMenuItem = entry["menu"]

		# Create menu item
		else:
			if "view" in entry and "name" not in entry:
				entry["name"] = ""
			if "view" in entry and "action" not in entry:
				entry["action"] = None

			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(entry["name"], entry["action"], "")

			if "view" in entry:
				try:
					view = entry["view"]
					if isinstance(view, NSView):
						newMenuItem.setView_(view)
				except:
					LogToConsole(traceback.format_exc(), "setUpMenuHelper")  # from GlyphsApp.py

			if "state" in entry:
				state = entry["state"]
				if state == ONSTATE or state == OFFSTATE or state == MIXEDSTATE:
					newMenuItem.setState_(entry["state"])
				else:
					LogToConsole("illegal state for menu item '%s'" % entry["name"], "setUpMenuHelper")

		if "target" in entry:
			newMenuItem.setTarget_(entry["target"])
		else:
			newMenuItem.setTarget_(defaultTarget)

		if index >= 0:
			menu.insertItem_atIndex_(newMenuItem, index)
		else:
			menu.addItem_(newMenuItem)


############################################################################################
#  Plug-in wrapper
# GlyphsFileFormatProtocol = objc.protocolNamed("GlyphsFileFormat")
#
# class FileFormatPlugin (NSObject):
# 	__pyobjc_protocols__ = [GlyphsFileFormatProtocol]

class FileFormatPlugin(BaseFileFormatPlugin):

	toolbarIcon: Optional[NSImage] = None
	dialog: Optional[NSView] = None

	def init(self: 'FileFormatPlugin') -> 'FileFormatPlugin':
		"""
		Do all initializing here.
		"""
		self = objc.super(FileFormatPlugin, self).init()  # type: ignore
		# Settings, default values
		self.name = 'My File Format'
		self.icon = "ExportIcon"
		self.toolbarPosition = 100

		if hasattr(self, 'settings'):
			self.settings()

		# Dialog stuff
		# Initiate empty self.dialog here in case of Vanilla dialog,
		# where .dialog is not defined at the class’s root.
		if not hasattr(self, 'dialog'):
			self.dialog = None

		if self.toolbarIcon is None and self.name and self.icon:
			if hasattr(self, "__file__"):
				path = self.__file__()
				thisBundle = NSBundle.bundleWithPath_(path[:path.rfind("Contents/Resources/")])
			else:
				thisBundle = NSBundle.bundleForClass_(NSClassFromString(self.className()))
			self.toolbarIcon = thisBundle.imageForResource_(self.icon)

		if self.toolbarIcon:
			# Using self.toolbarIconName instead of self.icon to
			#   make sure registered NSImage name is unique
			if self.toolbarIcon.name() is None:
				self.toolbarIcon.setName_("%s%s" % (self.className(), self.icon or "ExportIcon"))
		else:
			print("Error loading icon", self.icon, "for plugin:", self)

		if hasattr(self, 'start'):
			self.start()

		return self

	def interfaceVersion(self) -> int:
		"""
		Distinguishes the API version the plugin was built for.
		Return 1.
		"""
		return 1

	def title(self) -> str:
		"""
		This is the name as it appears in the menu in combination with 'Show'.
		E.g. 'return "Nodes"' will make the menu item read "Show Nodes".
		"""
		try:
			return self.name or self.__class__.__name__ or 'New FileFormat Plugin'
		except:
			LogError(traceback.format_exc())
			return "None"

	def toolbarTitle(self) -> Optional[str]:
		"""
		Name below the icon in the Export dialog toolbar.
		"""
		try:
			return self.name
		except:
			LogError(traceback.format_exc())
			return None

	def toolbarIconName(self):
		"""
		Used for image and tab tags. Should be unique.
		The className + the filename of the icon (without the suffix).
		"""
		try:
			return self.toolbarIcon.name() if self.toolbarIcon else None
		except:
			LogError(traceback.format_exc())
			return None

	def groupID(self) -> int:
		"""
		Determines the position in the Export dialog toolbar.
		Lower values are further to the left.
		"""
		try:
			return self.toolbarPosition or 100
		except:
			LogError(traceback.format_exc())
			return 100

	def exportSettingsView(self) -> NSView | None:
		"""
		Returns the view to be displayed in the export dialog.
		Don't touch this.
		"""
		return self.dialog

	def font(self) -> GSFont:
		return self._font

	def setFont_(self, font: GSFont) -> None:
		"""
		The GSFont object is assigned to the plugin prior to the export.
		This is used to publish the export dialog.
		"""
		try:
			self._font = font
		except:
			LogError(traceback.format_exc())

	def exportFont_(self, font: GSFont) -> None:
		"""
		EXPORT dialog

		This method is called when the Next button is pressed in the Export dialog,
		and should ask the user for the place to store the font (not necessarily, you could choose to hard-wire the destination in the code).

		Parameters:
		- font: The font object to export
		//- error: PyObjc-Requirement. It is required here in order to return the error object upon export failure. Ignore its existence here.

		return (True, None) if the export was successful
		return (False, NSError) if the export failed
		"""
		try:

			returnStatus, returnMessage = [False, 'export() is not implemented in the plugin.']
			if hasattr(self, 'export'):
				returnStatus, returnMessage = self.export(font)

			# Export successful
			# Change the condition (True) to your own assessment on whether or not the export succeeded
			if returnStatus:
				# Use Mac Notification Center
				notification = GSUserNotification.new()
				notification.title = self.title()
				notification.informativeText = returnMessage
				if hasattr(self, "exportPath") and self.exportPath:
					notification.userInfo = {"destinationPath": self.exportPath}
					notification.actionButtonTitle = "Show"
				notification.deliver()

				return

			# Export failed, give reason
			else:
				error = NSError.errorWithDomain_code_userInfo_(self.title(), -57, {
					NSLocalizedDescriptionKey: NSLocalizedString('Export failed', None),
					NSLocalizedRecoverySuggestionErrorKey: returnMessage
				})
				font.parent.presentError_(error)

		# Python exception, return error message
		except Exception as e:
			LogError(traceback.format_exc())
			error = NSError.errorWithDomain_code_userInfo_(
				self.title(), -57, {
					NSLocalizedDescriptionKey: NSLocalizedString('Python exception', None),
					NSLocalizedRecoverySuggestionErrorKey: str(e) + '\nCheck Macro window output.'
				})
			font.parent.presentError_(error)

	def exportFont_toURL_error_(self, font: GSFont, destinationURL: NSURL, error: Any) -> Tuple[bool, Optional[NSError]]:
		"""
		EXPORT dialog

		This is called from "Export All font" or from other plugins

		Parameters:
		- font: The font object to export
		- destinationURL: The URL where to write to. That can be the final file or a folder
		- error: PyObjc-Requirement. It is required here in order to return the error object upon export failure. Ignore its existence here.

		return True, None) if the export was successful
		return (False, NSError) if the export failed
		"""
		try:

			returnStatus, returnMessage = [False, 'export() is not implemented in the plugin.']
			if hasattr(self, 'export'):
				returnStatus, returnMessage = self.export(font, destinationURL.path())

			# Export successful
			# Change the condition (True) to your own assessment on whether or not the export succeeded
			if returnStatus:
				# Use Mac Notification Center
				notification = GSUserNotification.new()
				notification.title = self.title()
				notification.informativeText = returnMessage
				notification.userInfo = {"destinationPath": destinationURL.path()}
				notification.actionButtonTitle = "Show"
				notification.deliver()

				return (True, None)

			# Export failed, give reason
			else:
				ns_error = NSError.errorWithDomain_code_userInfo_(self.title(), -58, {
					NSLocalizedDescriptionKey: NSLocalizedString('Export failed', None),
					NSLocalizedRecoverySuggestionErrorKey: returnMessage
				})
				return (False, ns_error)

		# Python exception, return error message
		except Exception as e:
			LogError(traceback.format_exc())
			ns_error = NSError.errorWithDomain_code_userInfo_(
				self.title(), -57, {
					NSLocalizedDescriptionKey: NSLocalizedString('Python exception', None),
					NSLocalizedRecoverySuggestionErrorKey: str(e) + '\nCheck Macro window output.'
				})
			return (False, ns_error)
		return (True, None)

########################################################################
#
#
# def writeFont_toURL_error_()
# To be implemented in Glyphs in the future
# Don't delete, it needs to be present in the plugin already
#
#
########################################################################

	@objc.typedSelector(b'c32@:@@o^@')
	def writeFont_toURL_error_(self, font: GSFont, URL: NSURL, error: Any) -> Tuple[bool, Optional[NSError]]:
		"""
		SAVE FONT dialog

		This method is called when the save dialog is invoked by the user.
		You don't have to create a file dialog.

		Parameters:
		- font: the font object to save
		- URL: the URL (file path) to save the font to
		- error: on return, if the document contents could not be read, a pointer to an error object that encapsulates the reason they could not be read.
		"""
		try:
			if hasattr(self, 'export'):
				self.export(font, URL.path())
				return True, None
			else:
				ns_error = NSError.errorWithDomain_code_userInfo_(self.title(), -59, {
					NSLocalizedDescriptionKey: "The plugin does not support exporting the file"
				})
				return False, ns_error
		except:
			LogError(traceback.format_exc())
			# Fallback error for unexpected Python exceptions
			ns_error = NSError.errorWithDomain_code_userInfo_(self.title(), -59, {
				NSLocalizedDescriptionKey: "An unexpected error occurred during save.",
				NSLocalizedRecoverySuggestionErrorKey: traceback.format_exc()
			})
			return False, ns_error

########################################################################
#
#
# def fontFromURL_ofType_error_()
# Read fonts from files: To be implemented in Glyphs in the future
# Don't delete, it needs to be present in the plugin already
#
#
########################################################################

	@objc.typedSelector(b'@@:@@o^@')
	def fontFromURL_ofType_error_(self, URL: NSURL, fonttype: Any, error: Any) -> Tuple[Optional[GSFont], Optional[NSError]]:
		"""
		Reads a Font object from the specified URL.

		URL: the URL to read the font from.
		error: on return, if the document contents could not be read, a pointer to an error object that encapsulates the reason they could not be read.
		Return the font object, or None if an error occurred.
		"""
		try:
			# Create a new font object:
			if hasattr(self, 'read'):
				font = self.read(URL.path(), fonttype)
				return font, None
			else:
				ns_error = NSError.errorWithDomain_code_userInfo_(self.title(), -60, {
					NSLocalizedDescriptionKey: "The plugin does not support opening the file"
				})
				return None, ns_error
		except:
			print(traceback.format_exc())
			# Fallback error for unexpected Python exceptions
			ns_error = NSError.errorWithDomain_code_userInfo_(self.title(), -60, {
				NSLocalizedDescriptionKey: "An unexpected error occurred during open.",
				NSLocalizedRecoverySuggestionErrorKey: traceback.format_exc()
			})
			return None, ns_error
		return None, None

	@objc.typedSelector(b"v@:@")
	def raiseException_(self, e: Exception) -> None:
		raise e


FileFormatPlugin.logToConsole = python_method(LogToConsole_AsClassExtension)  # type: ignore
FileFormatPlugin.logError = python_method(LogError_AsClassExtension)  # type: ignore
FileFormatPlugin.loadNib = python_method(LoadNib)  # type: ignore


########################################################################
#
#
# FilterWithDialog
#
#
########################################################################


class FilterWithDialog(GSFilterPlugin):
	"""
	All 'myValue' and 'myValueField' references are just an example.
	They correspond to the 'My Value' field in the .xib file.
	Replace and add your own class variables.
	"""

	def loadPlugin(self) -> None:
		"""
		Do all initializing here.
		This is a good place to call random.seed() if you want to use randomization.
		In that case, don't forget to import random at the top of this file.
		"""

		self.menuName = 'My Filter'
		self.keyboardShortcut = None  # With Cmd+Shift
		self.actionButtonLabel = 'Apply'

		if hasattr(self, 'settings'):
			self.settings()

		# Dialog stuff
		# Initiate empty self.dialog here in case of Vanilla dialog,
		# where .dialog is not defined at the class’s root.
		if not hasattr(self, 'dialog'):
			self.dialog = None

	def setup(self) -> Optional[NSError]:
		try:
			objc.super(FilterWithDialog, self).setup()  # type: ignore

			if hasattr(self, 'start'):
				self.start()

			self.process_(None)

			return None
		except:
			LogError(traceback.format_exc())
			return None

	def interfaceVersion(self) -> int:
		"""
		Distinguishes the API version the plugin was built for.
		Return 1.
		"""
		return 1

	def title(self) -> Optional[NSString | str]:
		"""
		This is the name as it appears in the menu
		and in the title of the dialog window.
		"""
		try:
			return self.menuName
		except:
			LogError(traceback.format_exc())
			return None

	def actionName(self) -> Optional[NSString | str]:
		"""
		This is the title of the button in the settings dialog.
		Use something descriptive like 'Move', 'Rotate', or at least 'Apply'.
		"""
		try:
			return self.actionButtonLabel
		except:
			LogError(traceback.format_exc())
			return None

	def keyEquivalent(self) -> Optional[NSString]:
		"""
		The key together with Cmd+Shift will be the shortcut for the filter.
		Return None if you do not want to set a shortcut.
		Users can set their own shortcuts in System Prefs.
		"""
		try:
			return self.keyboardShortcut
		except:
			LogError(traceback.format_exc())
			return None

	@objc.typedSelector(b'v@:@@')
	def processFont_withArguments_(self, font: GSFont, arguments: List[str]) -> None:
		"""
		Invoked when called as Custom Parameter in an instance at export.
		The arguments come from the custom parameter in the instance settings.
		Item 0 in arguments is the class-name. The consecutive items should be your filter options.
		"""
		try:

			# set glyphList (list of glyphs to be processed) to all glyphs in the font
			glyphList = font.glyphs

			# customParameters delivered to filter()
			customParameters = {}
			unnamedCustomParameterCount = 0
			for i in range(1, len(arguments)):
				if 'include' not in arguments[i] and 'exclude' not in arguments[i]:

					# if key:value pair
					if ':' in arguments[i]:
						key, value = arguments[i].split(':')
					# only value given, no key. make key name
					else:
						key = unnamedCustomParameterCount
						unnamedCustomParameterCount += 1
						value = arguments[i]

					# attempt conversion to float value
					try:
						customParameters[key] = float(value)
					except:
						customParameters[key] = value

			# change glyphList to include or exclude glyphs
			if len(arguments) > 1:
				if "exclude:" in arguments[-1]:
					excludeList = [n.strip() for n in arguments.pop().replace("exclude:", "").strip().split(",")]
					glyphList = [g for g in glyphList if g.name not in excludeList]
				elif "include:" in arguments[-1]:
					includeList = [n.strip() for n in arguments.pop().replace("include:", "").strip().split(",")]
					glyphList = [font.glyphs[n] for n in includeList]

			# With these values, call your code on every glyph:
			fontMasterId = font.fontMasterAtIndex_(0).id
			for thisGlyph in glyphList:
				layer: GSLayer | None = thisGlyph.layerForId_(fontMasterId)

				if layer is not None and hasattr(self, 'filter'):
					self.filter(layer, False, customParameters)

		except:

			# Custom Parameter
			if len(arguments) > 1:
				Message(
					title="Error in %s" % self.menuName,
					message="There was an error in %s's filter() method when called through a Custom Parameter upon font export. Check your Macro window output." % self.menuName
				)
			LogError(traceback.format_exc())

	def processLayer_withArguments_(self, layer: GSLayer, arguments: List[str]) -> None:
		"""
		Invoked when called as Custom Parameter in an instance to generate the Preview.
		The arguments come from the custom parameter in the instance settings.
		Item 0 in arguments is the class-name. The consecutive items should be your filter options.
		"""
		try:
			if not hasattr(self, 'filter'):
				print("The filter: %s doesn’t fully support the plugin API. The method 'filter()' is missing" % self.menuName)
				return

			# customParameters delivered to filter()
			customParameters = {}
			unnamedCustomParameterCount = 0
			for i in range(1, len(arguments)):
				# if key:value pair
				if ':' in arguments[i]:
					key, value = arguments[i].split(':')
				# only value given, no key. make key name
				else:
					key = unnamedCustomParameterCount
					unnamedCustomParameterCount += 1
					value = arguments[i]
				# attempt conversion to float value
				try:
					customParameters[key] = float(value)
				except:
					customParameters[key] = value
			self.filter(layer, False, customParameters)

		except:
			# Custom Parameter
			if len(arguments) > 1:
				Message(
					title="Error in %s" % self.menuName,
					message="There was an error in %s's filter() method when called through a Custom Parameter upon font export. Check your Macro window output." % self.menuName
				)
			LogError(traceback.format_exc())

	def process_(self, sender: Optional[Any]) -> None:
		"""
		This method gets called when the user invokes the Dialog.
		"""
		try:
			# Create Preview in Edit View, and save & show original in ShadowLayers:
			shadowLayers = self.valueForKey_("shadowLayers")
			layers = self.valueForKey_("layers")
			checkSelection = True
			for k in range(len(shadowLayers)):
				shadowLayer = shadowLayers[k]
				layer = layers[k]
				layer.getCopyOfContentFromLayer_doSelection_(shadowLayer, checkSelection)

				self.filter(layer, True, {})  # add your class variables here

			# Safe the values in the fontMaster. But could be saved in UserDefaults, too.
			# fontMaster = self.valueForKey_("fontMaster")
			# fontMaster.userData["____myValue____"] = NSNumber.numberWithInteger_(self.____myValue____)

			# call the superclass to trigger the immediate redraw:
			objc.super(FilterWithDialog, self).process_(sender)  # type: ignore
		except:
			LogError(traceback.format_exc())

	def view(self) -> Optional[NSView]:
		return self.dialog

	def update(self) -> None:
		self.process_(None)
		Glyphs.redraw()

	def customParameterString(self) -> Optional[str]:
		if hasattr(self, 'generateCustomParameter'):
			return self.generateCustomParameter()
		return objc.nil

	@objc.typedSelector(b"v@:@")
	def raiseException_(self, e: Exception) -> None:
		raise e


FilterWithDialog.logToConsole = python_method(LogToConsole_AsClassExtension)  # type: ignore
FilterWithDialog.logError = python_method(LogError_AsClassExtension)  # type: ignore
FilterWithDialog.loadNib = python_method(LoadNib)  # type: ignore

########################################################################
#
#
# FilterWithoutDialog
#
#
########################################################################

# GlyphsFilterWithoutDialogProtocol = objc.protocolNamed("GlyphsFilter")
#
# class FilterWithoutDialog (NSObject):
# 	__pyobjc_protocols__ = [GlyphsFilterWithoutDialogProtocol]


class FilterWithoutDialog(BaseFilterWithoutDialog):

	_controller: GSEditViewController | None = None

	def loadPlugin(self) -> None:
		"""
		Do all initializing here.
		"""
		self.menuName = 'My Filter'
		self.keyboardShortcut = None

		if hasattr(self, 'settings'):
			self.settings()

		if hasattr(self, 'start'):
			self.start()
		self._filter = hasattr(self, 'filter')

	def interfaceVersion(self) -> int:
		"""
		Distinguishes the API version the plugin was built for.
		Return 1.
		"""
		return 1

	def title(self) -> NSString | str:
		"""
		This is the human-readable name as it appears in the Filter menu.
		"""
		return self.menuName

	@property
	def controller(self) -> Optional[GSEditViewController]:
		"""
		Use self.controller as object for the current view controller.
		"""
		return self._controller

	@controller.setter
	def controller(self, controller: Optional[GSEditViewController]) -> None:  # python setter
		self._controller = controller

	@objc.typedSelector(b'v@:@')  # objc setter
	def setController_(self, controller: Optional[GSEditViewController]) -> None:
		"""
		Do not touch this.
		"""
		assert isinstance(controller, GSEditViewController)
		self._controller = controller

	def setup(self) -> Optional[NSError]:
		"""
		Do not touch this.
		"""
		return None

	def keyEquivalent(self) -> Optional[NSString]:
		"""
		The key together with Cmd+Shift will be the shortcut for the filter.
		Return None if you do not want to set a shortcut.
		Users can set their own shortcuts in System Prefs.
		"""
		try:
			return self.keyboardShortcut
		except:
			LogError(traceback.format_exc())
			return None

	@objc.typedSelector(b'c32@0:8@16o^@24')
	def runFilterWithLayers_error_(self, layers: List[GSLayer], error: NSError | None) -> Tuple[bool, Optional[NSError]]:
		"""
		Invoked when user triggers the filter through the Filter menu
		from the font View
		"""
		try:
			if self._filter:
				for layer in layers:
					self.filter(layer, False, {})
			return (True, None)
		except:
			LogError(traceback.format_exc())
			ns_error = NSError.errorWithDomain_code_userInfo_(self.title(), -1, {
				NSLocalizedDescriptionKey: "Filter execution failed.",
				NSLocalizedRecoverySuggestionErrorKey: traceback.format_exc()
			})
			return (False, ns_error)

	@objc.typedSelector(b'c40@0:8@16@24o^@32')
	def runFilterWithLayer_options_error_(self, layer: GSLayer, options: Optional[Dict[str, Any]], error: NSError | None) -> Tuple[bool, Optional[NSError]]:
		"""
		Required for compatibility with Glyphs version 702 or later.
		Leave this as it is.
		"""
		try:
			return self.runFilterWithLayer_error_(layer, error)
		except:
			LogError(traceback.format_exc())
			ns_error = NSError.errorWithDomain_code_userInfo_(self.title(), -1, {
				NSLocalizedDescriptionKey: "Filter execution with options failed.",
				NSLocalizedRecoverySuggestionErrorKey: traceback.format_exc()
			})
			return (False, ns_error)

	@objc.typedSelector(b'c32@0:8@16o^@24')
	def runFilterWithLayer_error_(self, layer: GSLayer, error: NSError | None) -> Tuple[bool, Optional[NSError]]:
		"""
		Invoked when user triggers the filter through the Filter menu
		and only one layer is selected.
		"""
		try:
			if self._filter:
				self.filter(layer, True, {})
			return (True, None)
		except:
			LogError(traceback.format_exc())
			ns_error = NSError.errorWithDomain_code_userInfo_(self.title(), -1, {
				NSLocalizedDescriptionKey: "Filter execution on single layer failed.",
				NSLocalizedRecoverySuggestionErrorKey: traceback.format_exc()
			})
			return (False, ns_error)

	@objc.typedSelector(b'v@:@@')
	def processFont_withArguments_(self, font: GSFont, arguments: List[str]) -> None:
		"""
		Invoked when called as Custom Parameter in an instance at export.
		The arguments come from the custom parameter in the instance settings.
		Item 0 in arguments is the class-name. The consecutive items should be your filter options.
		"""
		try:
			# set glyphList to all glyphs
			glyphList = font.glyphs

			# customParameters delivered to filter()
			customParameters = {}
			unnamedCustomParameterCount = 0
			for i in range(1, len(arguments)):
				if 'include' not in arguments[i] and 'exclude' not in arguments[i]:
					# if key:value pair
					if ':' in arguments[i]:
						key, value = arguments[i].split(':')
					# only value given, no key. make key name
					else:
						key = unnamedCustomParameterCount
						unnamedCustomParameterCount += 1
						value = arguments[i]

					# attempt conversion to float value
					try:
						customParameters[key] = float(value)
					except:
						customParameters[key] = value

			# change glyphList to include or exclude glyphs
			if len(arguments) > 1:
				if "exclude:" in arguments[-1]:
					excludeList = [n.strip() for n in arguments.pop().replace("exclude:", "").strip().split(",")]
					glyphList = [g for g in glyphList if g.name not in excludeList]
				elif "include:" in arguments[-1]:
					includeList = [n.strip() for n in arguments.pop().replace("include:", "").strip().split(",")]
					glyphList = [font.glyphs[n] for n in includeList]

			fontMasterId = font.fontMasterAtIndex_(0).id
			for thisGlyph in glyphList:
				layer = thisGlyph.layerForId_(fontMasterId)

				if layer is not None and self._filter:
					self.filter(layer, False, customParameters)
		except:

			# Custom Parameter
			if len(arguments) > 1:
				Message(
					title="Error in %s" % self.menuName,
					message="There was an error in %s's filter() method when called through a Custom Parameter upon font export. Check your Macro window output." % self.menuName
				)
			LogError(traceback.format_exc())


FilterWithoutDialog.logToConsole = python_method(LogToConsole_AsClassExtension)  # type: ignore
FilterWithoutDialog.logError = python_method(LogError_AsClassExtension)  # type: ignore


########################################################################
#
#
# GeneralPlugin
#
#
########################################################################


# GlyphsGeneralPluginProtocol = objc.protocolNamed("GlyphsPlugin")
#
# class GeneralPlugin (NSObject):
# 	__pyobjc_protocols__ = [GlyphsGeneralPluginProtocol]


class GeneralPlugin(BaseGeneralPlugin):

	def interfaceVersion(self) -> int:
		"""
		Distinguishes the API version the plugin was built for.
		Return 1.
		"""
		return 1

	def loadPlugin(self) -> None:
		if hasattr(self, 'settings'):
			self.settings()

		if hasattr(self, 'start'):
			self.start()


	@objc.typedSelector(b"v@:@")
	def raiseException_(self, e: Exception) -> None:
		raise e


GeneralPlugin.logToConsole = python_method(LogToConsole_AsClassExtension)  # type: ignore
GeneralPlugin.logError = python_method(LogError_AsClassExtension)  # type: ignore
GeneralPlugin.loadNib = python_method(LoadNib)  # type: ignore


########################################################################
#
#
# PalettePlugin
#
#
########################################################################


# GlyphsPaletteProtocol = objc.protocolNamed("GlyphsPalette")
#
# class PalettePlugin (NSObject):
# 	__pyobjc_protocols__ = [GlyphsPaletteProtocol]


class PalettePlugin(BasePalettePlugin):
	# Define all your IB outlets for your .xib after _theView:
	_windowController: GSWindowController | None = None
	# _theView = objc.IBOutlet() # Palette view on which you can place UI elements.

	def init(self: 'PalettePlugin') -> 'PalettePlugin':
		"""
		Do all initializing here, and customize the quadruple underscore items.
		____CFBundleIdentifier____ should be the reverse domain name you specified in Info.plist.
		"""

		self = objc.super(PalettePlugin, self).init()  # type: ignore
		self.name = 'My Palette'
		self.dialog = None  # make sure we have that property
		self.sortId = 0

		# Call settings
		if hasattr(self, 'settings'):
			self.settings()

		# Dialog stuff
		view: GSPaletteView = cast(GSPaletteView, self.theView())
		if view is not None:
			frame = view.frame()
			# Set minimum and maximum height to height of Frame
			if not hasattr(self, "min"):
				self.min = frame.size.height
			if not hasattr(self, "max"):
				self.max = frame.size.height

		if hasattr(self, 'start'):
			self.start()
		if view is not None:
			try:
				view.setController_(self)
			except:
				pass
		return self

	def loadPlugin(self) -> None:
		pass

	@objc.typedSelector(b'L@:')
	def interfaceVersion(self) -> int:
		"""
		Distinguishes the API version the plugin was built for.
		Return 1.
		"""
		return 1

	def title(self) -> NSString | str:
		"""
		This is the name as it appears in the Palette section header.
		"""
		try:
			return cast(NSString, self.name)
		except:
			LogError(traceback.format_exc())
			return self.__class__.__name__

	@objc.typedSelector(b'L@:')
	def sortID(self) -> int:
		return self.sortId

	@objc.typedSelector(b'@@:')  # id, self, SEL
	def windowController(self):
		try:
			return self._windowController
		except:
			LogError(traceback.format_exc())

	@objc.typedSelector(b'v@:@')  # void, self, SEL, id
	def setWindowController_(self, windowController: Optional[GSWindowController]) -> None:
		try:
			self._windowController = windowController
		except:
			LogError(traceback.format_exc())

	def theView(self) -> Optional[NSView]:
		"""
		Returns an NSView to be displayed in the palette.
		This is the grey background in the palette, on which you can place UI items.
		"""
		try:
			return self.dialog
		except:
			LogError(traceback.format_exc())
			return None

	@objc.typedSelector(b'l@:')
	def minHeight(self) -> int:
		"""
		The minimum height of the view in pixels.
		"""
		try:
			return round(self.min)
		except:
			LogError(traceback.format_exc())
			return 0

	@objc.typedSelector(b'l@:')
	def maxHeight(self) -> int:
		"""
		The maximum height of the view in pixels.
		Must be equal to or bigger than minHeight.
		"""
		try:
			return round(self.max)
		except:
			LogError(traceback.format_exc())
			return 0

	@objc.typedSelector(b'L@:')
	def currentHeight(self) -> int:
		"""
		The current height of the Palette section.
		Used for storing the current resized state.
		If you have a fixed height, you can also return the height in pixels
		"""
		try:
			# return 150
			return NSUserDefaults.standardUserDefaults().integerForKey_(self.name + ".ViewHeight")
		except:
			LogError(traceback.format_exc())
			return 0

	@objc.typedSelector(b'v@:L')  # void, self, SEL, unsigned long
	def setCurrentHeight_(self, newHeight: int) -> None:
		"""
		Sets a new height for the Palette section.
		"""
		try:
			if newHeight >= self.minHeight() and newHeight <= self.maxHeight():
				NSUserDefaults.standardUserDefaults().setInteger_forKey_(newHeight, objcObject(self.name + ".ViewHeight"))
		except:
			LogError(traceback.format_exc())

	@objc.typedSelector(b"v@:@")
	def raiseException_(self, e: Exception) -> None:
		raise e


PalettePlugin.logToConsole = python_method(LogToConsole_AsClassExtension)  # type: ignore
PalettePlugin.logError = python_method(LogError_AsClassExtension)  # type: ignore
PalettePlugin.loadNib = python_method(LoadNib)  # type: ignore

########################################################################
#
#
# ReporterPlugin
#
#
########################################################################


# GlyphsReporterProtocol = objc.protocolNamed("GlyphsReporter")
# class ReporterPlugin (NSObject):
# 	__pyobjc_protocols__ = [GlyphsReporterProtocol]


class ReporterPlugin(BaseReporterPlugin):

	_controller: Optional[GSEditViewController]

	def init(self: ReporterPlugin):
		"""
		Put any initializations you want to make here.
		"""
		self = objc.super(ReporterPlugin, self).init()  # type: ignore

		self.needsExtraMainOutlineDrawingForInactiveLayers = True
		self.needsExtraMainOutlineDrawingForActiveLayer = True

		# Default values
		self.menuName = 'New ReporterPlugin'
		self.keyboardShortcut = None
		self.keyboardShortcutModifier = 0  # Set any combination of NSEventModifierFlagShift | NSEventModifierFlagControl | NSEventModifierFlagCommand | NSEventModifierFlagOption
		self.drawDefaultInactiveLayers = True
		self.generalContextMenus = []

		if hasattr(self, 'settings'):
			self.settings()

		if hasattr(self, 'start'):
			self.start()
		self.hasWarned = False

		self._foregroundInViewCoords = hasattr(self, 'foregroundInViewCoords')

		self._background = hasattr(self, 'background')

		self._backgroundInViewCoords = hasattr(self, 'backgroundInViewCoords')

		self._inactiveLayerBackground = hasattr(self, 'inactiveLayerBackground')

		self._foreground = hasattr(self, 'foreground')

		if hasattr(self, 'inactiveLayerBackground'):
			self._inactiveLayerBackground = True
		elif hasattr(self, 'inactiveLayers'):
			if not self.hasWarned:
				print("%s: the method 'inactiveLayers' has been deprecated. Please use 'inactiveLayerBackground'" % self.className())
				self.hasWarned = True
			self.inactiveLayerBackground = self.inactiveLayers  # type: ignore
			self._inactiveLayerBackground = True
		else:
			self._inactiveLayerBackground = False

		self._inactiveLayerForeground = hasattr(self, 'inactiveLayerForeground')

		if hasattr(self, 'preview'):
			self._preview = True
		elif hasattr(self, 'inactiveLayers'):
			self.preview = self.inactiveLayers  # type: ignore
			self._preview = True
		else:
			self._preview = False

		self._conditionalContextMenus = hasattr(self, 'conditionalContextMenus')
		return self

	@objc.typedSelector(b'L@:')
	def interfaceVersion(self) -> int:
		"""
		Distinguishes the API version the plugin was built for.
		Return 1.
		"""
		return 1

	def title(self) -> NSString | str:
		"""
		This is the name as it appears in the menu in combination with 'Show'.
		E.g. 'return "Nodes"' will make the menu item read "Show Nodes".
		"""
		try:
			return self.menuName or self.__class__.__name__ or 'New ReporterPlugin'
		except:
			LogError(traceback.format_exc())
			return self.__class__.__name__

	def keyEquivalent(self) -> Optional[NSString]:
		"""
		The key for the keyboard shortcut. Set modifier keys in modifierMask() further below.
		Pretty tricky to find a shortcut that is not taken yet, so be careful.
		If you are not sure, use 'return None'. Users can set their own shortcuts in System Prefs.
		"""
		try:
			return cast(NSString, self.keyboardShortcut)
		except:
			LogError(traceback.format_exc())
			return None

	@objc.typedSelector(b'i@:')
	def modifierMask(self) -> int:
		"""
		Use any combination of these to determine the modifier keys for your default shortcut:
			return NSEventModifierFlagShift | NSEventModifierFlagControl | NSEventModifierFlagCommand | NSEventModifierFlagOption
		Or:
			return 0
		... if you do not want to set a shortcut.
		"""
		try:
			return self.keyboardShortcutModifier or 0
		except:
			LogError(traceback.format_exc())
			return 0

	def drawForegroundForLayer_options_(self, layer: GSLayer, options: Dict[str, Any]) -> None:
		"""
		Whatever you draw here will be displayed IN FRONT OF the paths.
		Setting a color:
			NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 1.0, 1.0, 1.0).set() # sets RGBA values between 0.0 and 1.0
			NSColor.redColor().set() # predefined colors: blackColor, blueColor, brownColor, clearColor, cyanColor, darkGrayColor, grayColor, greenColor, lightGrayColor, magentaColor, orangeColor, purpleColor, redColor, whiteColor, yellowColor
		Drawing a path:
			myPath = NSBezierPath.alloc().init()  # initialize a path object myPath
			myPath.appendBezierPath_(subpath)   # add subpath to myPath
			myPath.fill()   # fill myPath with the current NSColor
			myPath.stroke() # stroke myPath with the current NSColor
		To get an NSBezierPath from a GSPath, use the bezierPath() method:
			myPath.bezierPath().fill()
		You can apply that to a full layer at once:
			if len(myLayer.paths > 0):
				myLayer.bezierPath()       # all closed paths
				myLayer.openBezierPath()   # all open paths
		See:
		https://developer.apple.com/library/mac/documentation/Cocoa/Reference/ApplicationKit/Classes/NSBezierPath_Class/Reference/Reference.html
		https://developer.apple.com/library/mac/documentation/cocoa/reference/applicationkit/classes/NSColor_Class/Reference/Reference.html
		"""
		try:
			if self._foreground:
				self._scale = options["Scale"]
				self.black = options["Black"]
				self.foreground(layer)
		except:
			LogError(traceback.format_exc())

	def drawForegroundWithOptions_(self, options: Dict[str, Any]) -> None:
		"""
		Whatever you draw here will be displayed IN FRONT OF the paths. The difference to drawForegroundForLayer_options_() is that you need to deal with the scaling and current layer yourself.

		examples::
			layer = self.activeLayer()
			layerPosition = self.activePosition()
			scale = options["Scale"]
			allLayers = self.controller.graphicView().layoutManager().cachedLayers()
			indexOfActiveLayer = self.controller.graphicView().activeIndex()
			selectionRange = self.controller.graphicView().selectedRange()
		"""
		try:
			if self._foregroundInViewCoords:
				self._scale = options["Scale"]
				self.black = options["Black"]
				self.foregroundInViewCoords()
		except:
			LogError(traceback.format_exc())

	def drawBackgroundForLayer_options_(self, layer: GSLayer, options: Dict[str, Any]) -> None:
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			if self._background:
				self._scale = options["Scale"]
				self.black = options["Black"]
				self.background(layer)
		except Exception as e:
			self.performSelector_withObject_afterDelay_("raiseException:", e, 0.1)

	def drawBackgroundWithOptions_(self, options: Dict[str, Any]) -> None:
		"""
		Whatever you draw here will be displayed BEHIND the paths. The difference to drawBackgroundForLayer_options_() is that you need to deal with the scaling and current layer yourself.
		"""
		try:
			if self._backgroundInViewCoords:
				self._scale = options["Scale"]
				self.black = options["Black"]
				self.backgroundInViewCoords()
		except Exception as e:
			self.performSelector_withObject_afterDelay_("raiseException:", e, 0.1)

	def drawBackgroundForInactiveLayer_options_(self, layer: GSLayer, options: Dict[str, Any]) -> None:
		"""
		Whatever you draw here will be displayed behind the paths, but
		- for inactive glyphs in the EDIT VIEW
		- and for glyphs in the PREVIEW
		Please note: If you are using this method, you probably want
		self.needsExtraMainOutlineDrawingForInactiveLayer_() to return False
		because otherwise Glyphs will draw the main outline on top of it, and
		potentially cover up your background drawing.
		"""

		try:
			self._scale = options["Scale"]
			self.black = options["Black"]
			assert Glyphs
			if self.controller:
				if self._inactiveLayerBackground:
					self.inactiveLayerBackground(layer)
			else:
				if self._preview:
					self.preview(layer)
		except Exception as e:
			self.performSelector_withObject_afterDelay_("raiseException:", e, 0.1)

	def drawForegroundForInactiveLayer_options_(self, layer: GSLayer, options: Dict[str, Any]) -> None:
		"""
		Whatever you draw here will be displayed behind the paths, but
		- for inactive glyphs in the EDIT VIEW
		- and for glyphs in the PREVIEW
		Please note: If you are using this method, you probably want
		self.needsExtraMainOutlineDrawingForInactiveLayer_() to return False
		because otherwise Glyphs will draw the main outline on top of it, and
		potentially cover up your background drawing.
		"""

		try:
			if self._inactiveLayerForeground and self.controller:
				self._scale = options["Scale"]
				self.black = options["Black"]
				self.inactiveLayerForeground(layer)
		except Exception as e:
			self.performSelector_withObject_afterDelay_("raiseException:", e, 0.1)

	def drawBackgroundInPreviewLayer_options_(self, layer, options):
		try:
			self._scale = options["Scale"]
			self.black = options["Black"]
			assert Glyphs
			if self._preview:
				self.preview(layer)
		except Exception as e:
			self.performSelector_withObject_afterDelay_("raiseException:", e, 0.1)

	@objc.typedSelector(b'Z@:@')
	def needsExtraMainOutlineDrawingForInactiveLayer_(self, layer: GSLayer) -> bool:
		"""
		Decides whether inactive glyphs in Edit View and glyphs in Preview should be drawn
		by Glyphs (‘the main outline drawing’).
		Return True to let Glyphs draw the main outline.
		Return False to prevent Glyphs from drawing the glyph (the main outline
		drawing), which is probably what you want if you are drawing the glyph
		yourself in self.inactiveLayerForeground() (self.drawForegroundForInactiveLayer_options_()).
		"""
		try:
			return self.needsExtraMainOutlineDrawingForInactiveLayers
		except Exception as e:
			self.performSelector_withObject_afterDelay_("raiseException:", e, 0.1)
			return True

	@objc.typedSelector(b'Z@:@')
	def needsExtraMainOutlineDrawingForActiveLayer_(self, layer: GSLayer) -> bool:
		"""
		Decides whether inactive glyphs in Edit View and glyphs in Preview should be drawn
		by Glyphs (‘the main outline drawing’).
		Return True to let Glyphs draw the main outline.
		Return False to prevent Glyphs from drawing the glyph (the main outline
		drawing), which is probably what you want if you are drawing the glyph
		yourself in self.inactiveLayerForeground() (self.drawForegroundForInactiveLayer_options_()).
		"""
		try:
			return self.needsExtraMainOutlineDrawingForActiveLayer
		except:
			LogError(traceback.format_exc())
			return True

	def addMenuItemsForEvent_toMenu_(self, event: NSEvent, contextMenu: NSMenu) -> None:
		'''
		The event can tell you where the user had clicked.
		'''
		try:
			if self.generalContextMenus:
				setUpMenuHelper(contextMenu, self.generalContextMenus, self)

			if self._conditionalContextMenus:
				contextMenus = self.conditionalContextMenus()
				if contextMenus:
					setUpMenuHelper(contextMenu, contextMenus, self)

		except:
			LogError(traceback.format_exc())

	@objc.python_method
	def drawTextAtPoint(self, text: str, textPosition: NSPoint, fontSize: float = 10.0, fontColor: NSColor = NSColor.textColor(), align: str = 'bottomleft') -> None:
		"""
		Use self.drawTextAtPoint("blabla", myNSPoint) to display left-aligned text at myNSPoint.
		"""
		try:
			alignment = {
				'topleft': 6,
				'topcenter': 7,
				'topright': 8,
				'left': 3,
				'center': 4,
				'right': 5,
				'bottomleft': 0,
				'bottomcenter': 1,
				'bottomright': 2
			}
			currentZoom = self.getScale()
			fontAttributes = {
				NSFontAttributeName: NSFont.labelFontOfSize_(fontSize / currentZoom),
				NSForegroundColorAttributeName: fontColor,
			}
			displayText = NSAttributedString.alloc().initWithString_attributes_(text, fontAttributes)
			textAlignment = alignment.get(align, 6)
			displayText.drawAtPoint_alignment_(textPosition, textAlignment)
		except:
			LogError(traceback.format_exc())

	@objc.python_method
	def getHandleSize(self) -> float:
		"""
		Returns the current handle size as set in user preferences.
		Use: self.getHandleSize() / self.getScale()
		to determine the right size for drawing on the canvas.
		"""
		try:
			selected = NSUserDefaults.standardUserDefaults().integerForKey_("GSHandleSize")
			if selected == 0:
				return 5.0
			elif selected == 2:
				return 10.0
			else:
				return 7.0  # Regular
		except:
			LogError(traceback.format_exc())
			return 7.0

	@objc.python_method
	def getScale(self) -> float:
		"""
		self.getScale() returns the current scale factor of the Edit View UI.
		Divide any scalable size by this value in order to keep the same apparent pixel size.
		"""
		return self._scale

	def activeLayer(self) -> Optional[GSLayer]:
		try:
			if self.controller:
				return self.controller.graphicView().activeLayer()
		except:
			LogError(traceback.format_exc())
		return None

	def activePosition(self) -> Optional[NSPoint]:
		try:
			if self.controller:
				return self.controller.graphicView().activePosition()
		except:
			LogError(traceback.format_exc())
		return None

	@property
	def controller(self) -> Optional[GSEditViewController]:
		"""
		Use self.controller as object for the current view controller.
		"""
		return self._controller

	@controller.setter
	def controller(self, controller: Optional[GSEditViewController]):  # python setter
		self._controller = controller

	@objc.typedSelector(b'v@:@')  # objc setter
	def setController_(self, controller: Optional[GSEditViewController]) -> None:
		self._controller = controller

	@objc.typedSelector(b"v@:@")
	def raiseException_(self, e: Exception) -> None:
		raise e


ReporterPlugin.logToConsole = python_method(LogToConsole_AsClassExtension)  # type: ignore
ReporterPlugin.logError = python_method(LogError_AsClassExtension)  # type: ignore
ReporterPlugin.loadNib = python_method(LoadNib)  # type: ignore

########################################################################
#
#
# SelectTool
#
#
########################################################################


class SelectTool(GSToolSelect):

	def init(self: 'SelectTool') -> 'SelectTool':
		"""
		By default, toolbar.pdf will be your tool icon.
		Use this for any initializations you need.
		"""

		self = objc.super(SelectTool, self).init()  # type: ignore
		self.name = 'My Select Tool'
		self.toolbarPosition = 100
		self._icon = 'toolbar.pdf'
		self.tool_bar_image = None
		self.keyboardShortcut = None
		self.generalContextMenus = []

		# Inspector dialog stuff
		# Initiate self.inspectorDialogView here in case of Vanilla dialog,
		# where inspectorDialogView is not defined at the class’s root.
		if not hasattr(self, 'inspectorDialogView'):
			self.inspectorDialogView = None

		if hasattr(self, 'settings'):
			self.settings()
		try:
			if hasattr(self, "__file__"):
				path = self.__file__()
				bundle = NSBundle.bundleWithPath_(path[:path.rfind("Contents/Resources/")])
			else:
				bundle = NSBundle.bundleForClass_(NSClassFromString(self.className()))
			if self._icon is not None and self.tool_bar_image is None:
				self.tool_bar_image = bundle.imageForResource_(self._icon)
			if self.tool_bar_image is not None and self._icon:
				self.tool_bar_image.setTemplate_(True)  # Makes the icon blend in with the toolbar.
				iconNameStem = os.path.splitext(self._icon)[0]
				iconBaseName = self.name + iconNameStem
				self.tool_bar_image.setName_(iconBaseName)
				# search for and register Highlight icon variant, if present
				highlightIconNameStem = iconNameStem + 'Highlight'
				highlightIcon = bundle.imageForResource_(highlightIconNameStem)
				if highlightIcon is not None:
					highlightIcon.setTemplate_(True)
					highlightIcon.setName_(iconBaseName + 'Highlight')
		except:
			LogError(traceback.format_exc())
		if hasattr(self, 'start'):
			self.start()
		self._activate = hasattr(self, 'activate')
		self._deactivate = hasattr(self, 'deactivate')

		self._foreground = hasattr(self, 'foreground')
		self._background = hasattr(self, 'background')

		self._conditionalContextMenus = hasattr(self, 'conditionalContextMenus')
		return self

	def view(self) -> Optional[NSView]:
		return self.inspectorDialogView

	def inspectorViewControllers(self) -> List[NSViewController]:
		viewControllers = objc.super(SelectTool, self).inspectorViewControllers()  # type: ignore
		if viewControllers is None:
			viewControllers = []
		try:
			# self.inspectorDialogView may also be defined with a .nib,
			# or it could be a vanilla dialog
			if self.inspectorDialogView:
				viewControllers.append(self)

		except:
			LogError(traceback.format_exc())

		return viewControllers

	def interfaceVersion(self) -> int:
		"""
		Distinguishes the API version the plugin was built for.
		Return 1.
		"""
		return 1

	def title(self) -> NSString | str:
		"""
		The name of the Tool as it appears in the tooltip.
		"""
		try:
			return self.name
		except:
			LogError(traceback.format_exc())
			return self.__class__.__name__

	def toolBarIcon(self) -> Optional[NSImage]:
		"""
		Return a instance of NSImage that represents the toolbar icon as established in init().
		Unless you know what you are doing, leave this as it is.
		"""
		try:
			return self.tool_bar_image
		except:
			LogError(traceback.format_exc())
		return objc.nil

	def groupID(self) -> int:
		"""
		Determines the position in the toolbar.
		Higher values are further to the right.
		"""
		try:
			return self.toolbarPosition
		except:
			LogError(traceback.format_exc())
			return 100

	def trigger(self) -> Optional[str]:
		"""
		The key to select the tool with keyboard (like v for the select tool).
		Either use trigger() or keyEquivalent(), not both. Remove the method(s) you do not use.
		"""
		try:
			return self.keyboardShortcut
		except:
			LogError(traceback.format_exc())
			return None

	def willSelectTempTool_(self, TempTool: GSToolPlugin) -> bool:
		"""
		Temporary Tool when user presses Cmd key.
		Should always be GlyphsToolSelect unless you have a better idea.
		"""
		try:
			return TempTool.__class__.__name__ != "GlyphsToolSelect"
		except:
			LogError(traceback.format_exc())
			return False

	def willActivate(self) -> None:
		"""
		Do stuff when the tool is selected.
		E.g. show a window, or set a cursor.
		"""
		try:
			objc.super(SelectTool, self).willActivate()  # type: ignore
			if self._activate:
				self.activate()
		except:
			LogError(traceback.format_exc())

	def willDeactivate(self) -> None:
		"""
		Do stuff when the tool is deselected.
		"""
		try:
			objc.super(SelectTool, self).willDeactivate()  # type: ignore
			if self._deactivate:
				self.deactivate()
		except:
			LogError(traceback.format_exc())

	def elementAtPoint_atLayer_(self, currentPoint: NSPoint, layer: GSLayer) -> Optional[Any]:  # Returns GSNode, GSAnchor, etc.
		"""
		Return an element in the vicinity of currentPoint (NSPoint), and it will be captured by the tool.
		Use Boolean ...
			distance(currentPoint, referencePoint) < clickTolerance / scale)
		... for determining whether the NSPoint referencePoint is captured or not.
		Use:
			myPath.nearestPointOnPath_pathTime_(currentPoint, 0.0)

			"""
		super_result = objc.super(SelectTool, self).elementAtPoint_atLayer_(currentPoint, layer)  # type: ignore
		if super_result is not None:  # Prioritize super if it finds something.
			return super_result

		return None

	# The following four methods are optional, and only necessary
	# if you intend to extend the context menu with extra items.
	# Remove them if you do not want to change the context menu:

	def defaultContextMenu(self) -> Optional[NSMenu]:
		"""
		Sets the default content of the context menu and returns the menu.
		Add menu items that do not depend on the context,
		e.g., actions that affect the whole layer, no matter what is selected.
		Remove this method if you do not want any extra context menu items.
		"""
		try:
			# Get the current default context menu:
			theMenu = objc.super(SelectTool, self).defaultContextMenu()  # type: ignore

			# Add separator at the bottom:
			newSeparator = NSMenuItem.separatorItem()
			theMenu.addItem_(newSeparator)

			# Add menu items at the bottom:
			setUpMenuHelper(theMenu, self.generalContextMenus, self)

			return theMenu
		except:
			LogError(traceback.format_exc())
			return None

	def addMenuItemsForEvent_toMenu_(self, theEvent: NSEvent, theMenu: NSMenu) -> None:
		"""
		Adds menu items to default context menu.
		Remove this method if you do not want any extra context menu items.
		"""
		try:

			if self._conditionalContextMenus:
				contextMenus = self.conditionalContextMenus()
				if contextMenus:
					# Todo: Make sure that the index is 0 for all items,
					# i.e., add at top rather than at bottom of menu:
					newSeparator = NSMenuItem.separatorItem()
					theMenu.addItem_(newSeparator)
					setUpMenuHelper(theMenu, contextMenus, self)

		except:
			LogError(traceback.format_exc())

	def drawForegroundForLayer_options_(self, layer: GSLayer, options: Dict[str, Any]) -> None:
		"""
		Whatever you draw here will be displayed IN FRONT OF the paths.
		Setting a color:
			NSColor.colorWithCalibratedRed_green_blue_alpha_(1.0, 1.0, 1.0, 1.0).set() # sets RGBA values between 0.0 and 1.0
			NSColor.redColor().set() # predefined colors: blackColor, blueColor, brownColor, clearColor, cyanColor, darkGrayColor, grayColor, greenColor, lightGrayColor, magentaColor, orangeColor, purpleColor, redColor, whiteColor, yellowColor
		Drawing a path:
			myPath = NSBezierPath.alloc().init()  # initialize a path object myPath
			myPath.appendBezierPath_(subpath)   # add subpath to myPath
			myPath.fill()   # fill myPath with the current NSColor
			myPath.stroke() # stroke myPath with the current NSColor
		To get an NSBezierPath from a GSPath, use the bezierPath() method:
			myPath.bezierPath().fill()
		You can apply that to a full layer at once:
			if len(myLayer.paths > 0):
				myLayer.bezierPath()       # all closed paths
				myLayer.openBezierPath()   # all open paths
		See:
		https://developer.apple.com/library/mac/documentation/Cocoa/Reference/ApplicationKit/Classes/NSBezierPath_Class/Reference/Reference.html
		https://developer.apple.com/library/mac/documentation/cocoa/reference/applicationkit/classes/NSColor_Class/Reference/Reference.html
		"""
		try:
			if self._foreground:
				self.foreground(layer)
		except:
			LogError(traceback.format_exc())

	def drawBackgroundForLayer_options_(self, layer: GSLayer, options: Dict[str, Any]) -> None:
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			if self._background:
				self.background(layer)
		except:
			LogError(traceback.format_exc())

	@objc.typedSelector(b"v@:@")
	def raiseException_(self, e: Exception) -> None:
		raise e


SelectTool.logToConsole = python_method(LogToConsole_AsClassExtension)  # type: ignore
SelectTool.logError = python_method(LogError_AsClassExtension)  # type: ignore
SelectTool.loadNib = python_method(LoadNib)  # type: ignore
