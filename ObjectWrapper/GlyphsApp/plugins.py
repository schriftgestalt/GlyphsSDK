# encoding: utf-8

from __future__ import print_function

import objc
from Foundation import NSBundle, NSLog, NSObject, NSClassFromString, NSMutableArray, NSMutableOrderedSet, \
	NSString, NSAttributedString, NSNumber, NSUserDefaults, NSUserNotification, NSUserNotificationCenter, \
	NSNotificationCenter, NSError, NSLocalizedDescriptionKey, NSLocalizedRecoverySuggestionErrorKey, \
	NSLocalizedString, NSNotFound, NSPoint, NSMakePoint, NSZeroPoint, NSMakeRect, NSMakeSize, NSMinX, \
	NSMinY, NSMaxX, NSMaxY, NSRect, NSSize, NSUnarchiver
from AppKit import NSApplication, NSColor, NSNib, NSMenu, NSMenuItem, NSView, NSImage, NSDocumentController, \
	NSBezierPath, NSFont, NSFontAttributeName, NSForegroundColorAttributeName, NSControlKeyMask, \
	NSCommandKeyMask, NSShiftKeyMask, NSAlternateKeyMask, NSEvent, NSAffineTransform
import sys, traceback
from types import *
from GlyphsApp import *

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append(path)


############################################################################################


# Forward compatibility for plugins that wish to use their self-created contextual NSMenuItem entries instead of Glyphs' wrapper
# Set to True once this functionality shall be published. (It's working as of this writing)
USESELFCREATEDNSMENUITEMS = True

# Forward compatibility to notify plugins if all contextual menu items will be forced into one sub menu per plugin.
# Set to True once the contextual menu items of plugins will be grouped and forced into sub menus.
PLUGINMENUSINFORCEDSUBMENU = False

GSFilterPlugin = objc.lookUpClass("GSFilterPlugin")
GSToolSelect = objc.lookUpClass("GSToolSelect")

__all__ = ["Glyphs", "FileFormatPlugin", "FilterWithDialog", "FilterWithoutDialog", "GeneralPlugin", "PalettePlugin", "ReporterPlugin", "SelectTool",
	"NSBundle", "NSLog", "NSObject", "NSClassFromString", "NSMutableArray", "NSMutableOrderedSet", "NSString", "NSAttributedString", "NSNumber", "NSUserDefaults", "NSUserNotification", "NSUserNotificationCenter", "NSNotificationCenter", "NSError", 
		"NSLocalizedDescriptionKey", "NSLocalizedRecoverySuggestionErrorKey", "NSLocalizedString", "NSNotFound", "NSPoint", "NSMakePoint", "NSZeroPoint", "NSMakeRect", "NSMakeSize", "NSMinX", "NSMinY", "NSMaxX", "NSMaxY", "NSRect", "NSSize", "NSUnarchiver",
	"NSApplication", "NSColor", "NSNib", "NSMenu", "NSMenuItem", "NSView", "NSImage", "NSDocumentController", "NSBezierPath", "NSFont", "NSFontAttributeName", "NSForegroundColorAttributeName", "NSControlKeyMask", "NSCommandKeyMask", "NSShiftKeyMask", "NSAlternateKeyMask", "NSEvent", "NSAffineTransform",
	"GSFilterPlugin", "setUpMenuHelper",
	"objc"
]

############################################################################################

#  Helper methods

def LogToConsole_AsClassExtension(self, message):
	LogToConsole(message, self.title()) # from GlyhsApp.py

def LogError_AsClassExtension(self, message):
	LogError(message) # from GlyhsApp.py

def LoadNib(self, nibname, path = None):
	if path and len(path) > 10:
		bundlePath = path[:path.find("/Contents/Resources/")]
		bundle = NSBundle.bundleWithPath_(bundlePath)
		nib = NSNib.alloc().initWithNibNamed_bundle_(nibname, bundle)
		if not nib:
			self.logError("Error loading nib for Class: %s" % self.__class__.__name__)
		
		result = nib.instantiateWithOwner_topLevelObjects_(self, None)
		try:
			error = bool(result[0])
		except:
			error = bool(result) # in 10.9, the result is a bool
		if not error:
			self.logError("Error instantiating nib for Class: %s" % self.__class__.__name__)
		else:
			try:
				self.topLevelObjects = result[1]
			except:
				pass
	else:
		if not NSBundle.loadNibNamed_owner_(nibname, self):
			self.logError("Error loading %s.nib." % nibname)

def pathForResource(resourceName, extension, path = None):
	if path and len(path) > 10:
		bundlePath = path[:path.find("/Contents/Resources/")]
		bundle = NSBundle.bundleWithPath_(bundlePath)
		return bundle.pathForResource_ofType_(resourceName, extension)
	else:
		raise("Please supply path")

def setUpMenuHelper(Menu, Items, defaultTarget):
	if type(Items) == list:
		for entry in Items:
			
			if "index" in entry:
				index = int(entry["index"])
			else:
				index = -1

			# Use supplied NSMenuItem 
			if "menu" in entry:
				newMenuItem = entry["menu"]

			# Create menu item
			else:


				if "view" in entry and not "name" in entry:
					entry["name"] = ""
				if "view" in entry and not "action" in entry:
					entry["action"] = None
				
				
				newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(entry["name"], entry["action"], "")
				
				if "view" in entry:
					try:
						view = entry["view"]
						if isinstance(view, NSView):
							newMenuItem.setView_(view)
					except:
						LogToConsole(traceback.format_exc(), "setUpMenuHelper") # from GlyhsApp.py
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
				Menu.insertItem_atIndex_(newMenuItem, index)
			else:
				Menu.addItem_(newMenuItem)
		




############################################################################################

#  Plug-in wrapper


GlyphsFileFormatProtocol = objc.protocolNamed("GlyphsFileFormat")

class FileFormatPlugin (NSObject):
	__pyobjc_protocols__ = [GlyphsFileFormatProtocol]
	def init(self):
		"""
		Do all initializing here.
		"""
		try:
			# Settings, default values
			self.name = 'My File Format'
			self.icon = 'ExportIcon'
			self.toolbarPosition = 100
			
			if hasattr(self, 'settings'):
				self.settings()
			
			# Dialog stuff
			# Initiate empty self.dialog here in case of Vanilla dialog,
			# where .dialog is not defined at the class’s root.
			if not hasattr(self, 'dialog'):
				self.dialog = None
			
			if hasattr(self, "__file__"):
				path = self.__file__()
				thisBundle = NSBundle.bundleWithPath_(path[:path.rfind("Contents/Resources/")])
			else:
				thisBundle = NSBundle.bundleForClass_(NSClassFromString(self.className()));
			self.toolbarIcon = NSImage.alloc().initWithContentsOfFile_(thisBundle.pathForImageResource_(self.icon))
			# Using self.toolbarIconName() instead of self.icon to
			#   make sure registered NSImage name is unique
			self.toolbarIcon.setName_(self.toolbarIconName())
			
			if hasattr(self, 'start'):
				self.start()
		
		except:
			self.logError(traceback.format_exc())
		
		return self
	
	def interfaceVersion(self):
		"""
		Distinguishes the API version the plugin was built for.
		Return 1.
		"""
		try:
			return 1
		except:
			self.logError(traceback.format_exc())
	
	def title(self):
		"""
		This is the name as it appears in the menu in combination with 'Show'.
		E.g. 'return "Nodes"' will make the menu item read "Show Nodes".
		"""
		try:
			return self.name or self.__class__.__name__ or 'New FileFormat Plugin'
		except:
			self.logError(traceback.format_exc())
	
	def toolbarTitle(self):
		"""
		Name below the icon in the Export dialog toolbar.
		"""
		try:
			return self.name
		except:
			self.logError(traceback.format_exc())
	
	def toolbarIconName(self):
		"""
		Used for image and tab tags. Should be unique.
		The className + the filename of the icon (without the suffix).
		"""
		try:
			return "{}{}".format(self.className(), self.icon)
		except:
			self.logError(traceback.format_exc())
	
	def groupID(self):
		"""
		Determines the position in the Export dialog toolbar.
		Lower values are further to the left.
		"""
		try:
			return self.toolbarPosition or 100
		except:
			self.logError(traceback.format_exc())
	
	def progressWindow(self):
		try:
			return None
		except:
			self.logError(traceback.format_exc())
	
	def exportSettingsView(self):
		"""
		Returns the view to be displayed in the export dialog.
		Don't touch this.
		"""
		try:
			return self.dialog
		except:
			self.logError(traceback.format_exc())
	
	def font(self):
		try:
			return self._font
		except:
			self.logError(traceback.format_exc())
	
	def setFont_(self, GSFontObj):
		"""
		The GSFont object is assigned to the plugin prior to the export.
		This is used to publish the export dialog.
		"""
		try:
			self._font = GSFontObj
		except:
			self.logError(traceback.format_exc())
	
	def writeFont_error_(self, font, error):
		"""
		EXPORT dialog
		
		This method is called when the Next button is pressed in the Export dialog,
		and should ask the user for the place to store the font (not necessarily, you could choose to hard-wire the destination in the code).
		
		Parameters:
		- font: The font object to export
		- error: PyObjc-Requirement. It is required here in order to return the error object upon export failure. Ignore its existence here.
		
		return (True, None) if the export was successful
		return (False, NSError) if the export failed
		"""
		try:
			
			returnStatus, returnMessage = [False, 'export() is not implemented in the plugin.']
			if hasattr(self, 'export'):
				returnStatus, returnMessage = self.export(font)
			
			# Export successful
			# Change the condition (True) to your own assessment on whether or not the export succeeded
			if returnStatus == True:
				# Use Mac Notification Center
				notification = NSUserNotification.alloc().init()
				notification.setTitle_(self.title())
				notification.setInformativeText_(returnMessage)
				NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
				
				return (True, None)
			
			# Export failed, give reason
			else:
				error = NSError.errorWithDomain_code_userInfo_(self.title(), -57, {
					NSLocalizedDescriptionKey: NSLocalizedString('Export failed', None),
					NSLocalizedRecoverySuggestionErrorKey: returnMessage
					})
				return (False, error)
		
		# Python exception, return error message
		except Exception as e:
			self.logError(traceback.format_exc())
			error = NSError.errorWithDomain_code_userInfo_(self.title(), -57, {
				NSLocalizedDescriptionKey: NSLocalizedString('Python exception', None),
				NSLocalizedRecoverySuggestionErrorKey: str(e) + '\nCheck Macro window output.'
				})
			return (False, error)
		return True


########################################################################
#
#
#	def writeFont_toURL_error_()
#	To be implemented in Glyphs in the future
#	Don't delete, it needs to be present in the plugin already
#
#
########################################################################


	def writeFont_toURL_error_(self, font, URL, error):
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
				return (True, None)
			else:
				error = NSError.errorWithDomain_code_userInfo_(self.title(), -57, {NSLocalizedDescriptionKey: "The plugin does not support exporting the file"})
				return None, error
		except:
			self.logError(traceback.format_exc())


########################################################################
#
#
#	def fontFromURL_ofType_error_()
#	Read fonts from files: To be implemented in Glyphs in the future
#	Don't delete, it needs to be present in the plugin already
#
#
########################################################################


	def fontFromURL_ofType_error_(self, URL, fonttype, error):
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
				error = NSError.errorWithDomain_code_userInfo_(self.title(), -57, {NSLocalizedDescriptionKey: "The plugin does not support opening the file"})
				return None, error
		except:
			print(traceback.format_exc())
		return None, None


FileFormatPlugin.logToConsole = LogToConsole_AsClassExtension
FileFormatPlugin.logError = LogError_AsClassExtension
FileFormatPlugin.loadNib = LoadNib












class FilterWithDialog (GSFilterPlugin):
	"""
	All 'myValue' and 'myValueField' references are just an example.
	They correspond to the 'My Value' field in the .xib file.
	Replace and add your own class variables.
	"""
	
	def init(self):
		"""
		Do all initializing here.
		This is a good place to call random.seed() if you want to use randomisation.
		In that case, don't forget to import random at the top of this file.
		"""
		
		try:
			self.menuName = 'My Filter'
			self.keyboardShortcut = None # With Cmd+Shift
			self.actionButtonLabel = 'Apply'
			
			if hasattr(self, 'settings'):
				self.settings()
			
			# Dialog stuff
			# Initiate emtpy self.dialog here in case of Vanilla dialog,
			# where .dialog is not defined at the class’s root.
			if not hasattr(self, 'dialog'):
				self.dialog = None
			
			return self
		
		except:
			self.logError(traceback.format_exc())
	
	def setup(self):
		try:
			objc.super(FilterWithDialog, self).setup()
			
			if hasattr(self, 'start'):
				self.start()
			
			self.process_(None)
			
			return None
		except:
			self.logError(traceback.format_exc())
	
	def interfaceVersion(self):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except:
			self.logError(traceback.format_exc())
	
	def title(self):
		"""
		This is the name as it appears in the menu
		and in the title of the dialog window.
		"""
		try:
			return self.menuName
		except:
			self.logError(traceback.format_exc())
	
	def actionName(self):
		"""
		This is the title of the button in the settings dialog.
		Use something descriptive like 'Move', 'Rotate', or at least 'Apply'.
		"""
		try:
			return self.actionButtonLabel
		except:
			self.logError(traceback.format_exc())
	
	def keyEquivalent(self):
		""" 
		The key together with Cmd+Shift will be the shortcut for the filter.
		Return None if you do not want to set a shortcut.
		Users can set their own shortcuts in System Prefs.
		"""
		try:
			return self.keyboardShortcut
		except:
			self.logError(traceback.format_exc())
	
	def processFont_withArguments_(self, Font, Arguments):
		"""
		Invoked when called as Custom Parameter in an instance at export.
		The Arguments come from the custom parameter in the instance settings. 
		Item 0 in Arguments is the class-name. The consecutive items should be your filter options.
		"""
		try:
			
			# set glyphList (list of glyphs to be processed) to all glyphs in the font
			glyphList = Font.glyphs
			
			# customParameters delivered to filter()
			customParameters = {}
			unnamedCustomParameterCount = 0
			for i in range(1, len(Arguments)):
				if not 'include' in Arguments[i] and not 'exclude' in Arguments[i]:
					
					# if key:value pair
					if ':' in Arguments[i]:
						key, value = Arguments[i].split(':')
					# only value given, no key. make key name
					else:
						key = unnamedCustomParameterCount
						unnamedCustomParameterCount += 1
						value = Arguments[i]
					
					# attempt conversion to float value
					try:
						customParameters[key] = float(value)
					except:
						customParameters[key] = value
			
			# change glyphList to include or exclude glyphs
			if len(Arguments) > 1:
				if "exclude:" in Arguments[-1]:
					excludeList = [ n.strip() for n in Arguments.pop(-1).replace("exclude:","").strip().split(",") ]
					glyphList = [ g for g in glyphList if not g.name in excludeList ]
				elif "include:" in Arguments[-1]:
					includeList = [ n.strip() for n in Arguments.pop(-1).replace("include:","").strip().split(",") ]
					glyphList = [ Font.glyphs[n] for n in includeList ]
			
			# With these values, call your code on every glyph:
			FontMasterId = Font.fontMasterAtIndex_(0).id
			for thisGlyph in glyphList:
				Layer = thisGlyph.layerForKey_(FontMasterId)
				
				if hasattr(self, 'filter'):
					self.filter(Layer, False, customParameters)
		
		except:
			
			# Custom Parameter
			if len(Arguments) > 1:
				Message(title='Error in %s' % self.menuName, message="There was an error in %s's filter() method when called through a Custom Parameter upon font export. Check your Macro window output." % self.menuName)
			
			self.logError(traceback.format_exc())


	def processLayer_withArguments_(self, Layer, Arguments):
		"""
		Invoked when called as Custom Parameter in an instance to generate the Preview.
		The Arguments come from the custom parameter in the instance settings. 
		Item 0 in Arguments is the class-name. The consecutive items should be your filter options.
		"""
		try:
			if not hasattr(self, 'filter'):
				print("The filter: %s doesn’t fully support the plugin API. The method 'filter()' is missing" % self.menuName)
				return
			
			# customParameters delivered to filter()
			customParameters = {}
			unnamedCustomParameterCount = 0
			for i in range(1, len(Arguments)):
				# if key:value pair
				if ':' in Arguments[i]:
					key, value = Arguments[i].split(':')
				# only value given, no key. make key name
				else:
					key = unnamedCustomParameterCount
					unnamedCustomParameterCount += 1
					value = Arguments[i]
				# attempt conversion to float value
				try:
					customParameters[key] = float(value)
				except:
					customParameters[key] = value
			self.filter(Layer, False, customParameters)
		
		except:
			# Custom Parameter
			if len(Arguments) > 1:
				Message(title='Error in %s' % self.menuName, message="There was an error in %s's filter() method when called through a Custom Parameter upon font export. Check your Macro window output." % self.menuName)
			
			self.logError(traceback.format_exc())
	
	def process_(self, sender):
		"""
		This method gets called when the user invokes the Dialog.
		"""
		try:
			# Create Preview in Edit View, and save & show original in ShadowLayers:
			ShadowLayers = self.valueForKey_("shadowLayers")
			Layers = self.valueForKey_("layers")
			checkSelection = True
			for k in range(len(ShadowLayers)):
				ShadowLayer = ShadowLayers[k]
				Layer = Layers[k]
				Layer.setPaths_(NSMutableArray.alloc().initWithArray_copyItems_(ShadowLayer.pyobjc_instanceMethods.paths(), True))
				Layer.setSelection_(None)
				try:
					# Glyphs 2.1 and earlier:
					if len(ShadowLayer.selection()) > 0 and checkSelection:
						for i in range(len(ShadowLayer.paths)):
							currShadowPath = ShadowLayer.paths[i]
							currLayerPath = Layer.paths[i]
							for j in range(len(currShadowPath.nodes)):
								currShadowNode = currShadowPath.nodes[j]
								if ShadowLayer.selection().containsObject_(currShadowNode):
									Layer.addSelection_(currLayerPath.nodes[j])
				except:
					# Glyphs 2.2 and later:
					if len(ShadowLayer.selection) > 0 and checkSelection:
						for i in range(len(ShadowLayer.paths)):
							currShadowPath = ShadowLayer.paths[i]
							currLayerPath = Layer.paths[i]
							for j in range(len(currShadowPath.nodes)):
								currShadowNode = currShadowPath.nodes[j]
								if currShadowNode in ShadowLayer.selection:
									Layer.addSelection_(currLayerPath.nodes[j])
				
				self.filter(Layer, Glyphs.font.currentTab != None, {}) # add your class variables here
				Layer.clearSelection()
			
			# Safe the values in the FontMaster. But could be saved in UserDefaults, too.
			# FontMaster = self.valueForKey_("fontMaster")
			# FontMaster.userData[ "____myValue____" ] = NSNumber.numberWithInteger_(self.____myValue____)
			
			# call the superclass to trigger the immediate redraw:
			objc.super(FilterWithDialog, self).process_(sender)
		except:
			self.logError(traceback.format_exc())
	
	def view(self):
		return self.dialog
	
	def update(self):
		self.process_(None)
		Glyphs.redraw()
	
	def customParameterString(self):
		try:
			if hasattr(self, 'generateCustomParameter'):
				return self.generateCustomParameter()
		except:
			self.logError(traceback.format_exc())

FilterWithDialog.logToConsole = LogToConsole_AsClassExtension
FilterWithDialog.logError = LogError_AsClassExtension
FilterWithDialog.loadNib = LoadNib












GlyphsFilterWithoutDialogProtocol = objc.protocolNamed("GlyphsFilter")

class FilterWithoutDialog (NSObject):
	__pyobjc_protocols__ = [GlyphsFilterWithoutDialogProtocol]
	def init(self):
		"""
		Do all initializing here.
		"""
		try:
			self.menuName = 'My Filter'
			self.keyboardShortcut = None
			
			if hasattr(self, 'settings'):
				self.settings()
			
			if hasattr(self, 'start'):
				self.start()
			
			return self
		except:
			self.logError(traceback.format_exc())
	
	def interfaceVersion(self):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except:
			self.logError(traceback.format_exc())
	
	def title(self):
		"""
		This is the human-readable name as it appears in the Filter menu.
		"""
		try:
			return self.menuName
		except:
			self.logError(traceback.format_exc())
	
	def setController_(self, Controller):
		"""
		Sets the controller, you can access it with controller().
		Do not touch this.
		"""
		try:
			self._controller = Controller
		except:
			self.logError(traceback.format_exc())
	
	def controller(self):
		"""
		Do not touch this.
		"""
		try:
			return self._controller
		except:
			self.logError(traceback.format_exc())
	
	def setup(self):
		"""
		Do not touch this.
		"""
		try:
			return None
		except:
			self.logError(traceback.format_exc())
	
	def keyEquivalent(self):
		""" 
		The key together with Cmd+Shift will be the shortcut for the filter.
		Return None if you do not want to set a shortcut.
		Users can set their own shortcuts in System Prefs.
		"""
		try:
			return self.keyboardShortcut
		except:
			self.logError(traceback.format_exc())
	
	def runFilterWithLayers_error_(self, Layers, Error):
		"""
		Invoked when user triggers the filter through the Filter menu
		and more than one layer is selected.
		"""
		try:
			for Layer in Layers:
				# Layer = Layers[k]
				# Layer.clearSelection()
				
				if hasattr(self, 'filter'):
					self.filter(Layer, False, {})
					
			return (True, None)
		except:
			self.logError(traceback.format_exc())
	
	def runFilterWithLayer_options_error_(self, Layer, Options, Error):
		"""
		Required for compatibility with Glyphs version 702 or later.
		Leave this as it is.
		"""
		try:
			return self.runFilterWithLayer_error_(self, Layer, Error)
		except:
			self.logError(traceback.format_exc())
	
	def runFilterWithLayer_error_(self, Layer, Error):
		"""
		Invoked when user triggers the filter through the Filter menu
		and only one layer is selected.
		"""
		try:
			if hasattr(self, 'filter'):
				self.filter(Layer, True, {})
			return (True, None)
		except:
			self.logError(traceback.format_exc())
			return (False, None)
	
	def processFont_withArguments_(self, Font, Arguments):
		"""
		Invoked when called as Custom Parameter in an instance at export.
		The Arguments come from the custom parameter in the instance settings. 
		Item 0 in Arguments is the class-name. The consecutive items should be your filter options.
		"""
		try:
			# set glyphList to all glyphs
			glyphList = Font.glyphs
			
			# customParameters delivered to filter()
			customParameters = {}
			unnamedCustomParameterCount = 0
			for i in range(1, len(Arguments)):
				if not 'include' in Arguments[i] and not 'exclude' in Arguments[i]:
					
					# if key:value pair
					if ':' in Arguments[i]:
						key, value = Arguments[i].split(':')
					# only value given, no key. make key name
					else:
						key = unnamedCustomParameterCount
						unnamedCustomParameterCount += 1
						value = Arguments[i]
					
					# attempt conversion to float value
					try:
						customParameters[key] = float(value)
					except:
						customParameters[key] = value
			
			
			# change glyphList to include or exclude glyphs
			if len(Arguments) > 1:
				if "exclude:" in Arguments[-1]:
					excludeList = [ n.strip() for n in Arguments.pop(-1).replace("exclude:","").strip().split(",") ]
					glyphList = [ g for g in glyphList if not g.name in excludeList ]
				elif "include:" in Arguments[-1]:
					includeList = [ n.strip() for n in Arguments.pop(-1).replace("include:","").strip().split(",") ]
					glyphList = [ Font.glyphs[n] for n in includeList ]
			
			FontMasterId = Font.fontMasterAtIndex_(0).id
			for thisGlyph in glyphList:
				Layer = thisGlyph.layerForKey_(FontMasterId)
				
				if hasattr(self, 'filter'):
					self.filter(Layer, False, customParameters)
		except:
			
			# Custom Parameter
			if len(Arguments) > 1:
				Message(title='Error in %s' % self.menuName, message="There was an error in %s's filter() method when called through a Custom Parameter upon font export. Check your Macro window output." % self.menuName)

			self.logError(traceback.format_exc())

FilterWithoutDialog.logToConsole = LogToConsole_AsClassExtension
FilterWithoutDialog.logError = LogError_AsClassExtension












GlyphsGeneralPluginProtocol = objc.protocolNamed("GlyphsPlugin")

class GeneralPlugin (NSObject):
	__pyobjc_protocols__ = [GlyphsGeneralPluginProtocol]
	def interfaceVersion(self):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except:
			self.logError(traceback.format_exc())
	
	def loadPlugin(self):
		try:
			self.name = 'My General Plugin'
			
			if hasattr(self, 'settings'):
				self.settings()
			
			if hasattr(self, 'start'):
				self.start()
			return None
		except:
			self.logError(traceback.format_exc())
	
	def title(self):
		"""
		This is the name as it appears in the menu in combination with 'Show'.
		E.g. 'return "Nodes"' will make the menu item read "Show Nodes".
		"""
		try:
			return self.name
		except:
			self.logError(traceback.format_exc())

GeneralPlugin.logToConsole = LogToConsole_AsClassExtension
GeneralPlugin.logError = LogError_AsClassExtension
GeneralPlugin.loadNib = LoadNib











GlyphsPaletteProtocol = objc.protocolNamed("GlyphsPalette")

class PalettePlugin (NSObject):
	__pyobjc_protocols__ = [GlyphsPaletteProtocol]
	# Define all your IB outlets for your .xib after _theView:
	_windowController = None
	# _theView = objc.IBOutlet() # Palette view on which you can place UI elements.
	
	def init(self):
		"""
		Do all initializing here, and customize the quadruple underscore items.
		____CFBundleIdentifier____ should be the reverse domain name you specified in Info.plist.
		"""
		try:
		# if True:
			self.name = 'My Palette'

			self.sortId = 0
			
			# Call settings
			if hasattr(self, 'settings'):
				self.settings()
			
			# Dialog stuff
			# Initiate emtpy self.dialog here in case of Vanilla dialog,
			# where .dialog is not defined at the class’s root.
			Frame = None
			if hasattr(self, 'dialog'):
				Frame = self.dialog.frame()
			else:
				self.dialog = None
				
			if self.theView() is not None:
				Frame = self.theView().frame()
				# Set minimum and maximum height to height of Frame
				if not hasattr(self, "min"):
					self.min = Frame.size.height
				if not hasattr(self, "max"):
					self.max = Frame.size.height
			
			if hasattr(self, 'start'):
				self.start()
			try:
				self.theView().setController_(self)
			except:
				pass
			return self
		except:
			self.logError(traceback.format_exc())
	
	def interfaceVersion(self):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except:
			self.logError(traceback.format_exc())
	
	def title(self):
		"""
		This is the name as it appears in the Palette section header.
		"""
		try:
			return self.name
		except:
			self.logError(traceback.format_exc())
	
	def sortID(self):
		return self.sortId
	
	def windowController(self):
		try:
			return self._windowController
		except:
			self.logError(traceback.format_exc())
	
	def setWindowController_(self, windowController):
		try:
			self._windowController = windowController
		except:
			self.logError(traceback.format_exc())
	
	def theView(self):
		"""
		Returns an NSView to be displayed in the palette.
		This is the grey background in the palette, on which you can place UI items.
		"""
		try:
			return self.dialog
		except:
			self.logError(traceback.format_exc())
	
	def minHeight(self):
		"""
		The minimum height of the view in pixels.
		"""
		try:
			return self.min
		except:
			self.logError(traceback.format_exc())
	
	def maxHeight(self):
		"""
		The maximum height of the view in pixels.
		Must be equal to or bigger than minHeight.
		"""
		try:
			return self.max
		except:
			self.logError(traceback.format_exc())
	
	def currentHeight(self):
		"""
		The current height of the Palette section.
		Used for storing the current resized state.
		If you have a fixed height, you can also return the height in pixels
		"""
		try:
			# return 150
			return NSUserDefaults.standardUserDefaults().integerForKey_(self.dialogName + ".ViewHeight")
		except:
			self.logError(traceback.format_exc())
	
	def setCurrentHeight_(self, newHeight):
		"""
		Sets a new height for the Palette section.
		"""
		try:
			if newHeight >= self.minHeight() and newHeight <= self.maxHeight():
				NSUserDefaults.standardUserDefaults().setInteger_forKey_(newHeight, self.dialogName + ".ViewHeight")
		except:
			self.logError(traceback.format_exc())
	
	def currentWindowController(self):
		"""
		Returns a window controller object.
		Use self.currentWindowController() to access it.
		"""
		try:
			windowController = None
			try:
				windowController = NSDocumentController.sharedDocumentController().currentDocument().windowController()
				if not windowController and sender.respondsToSelector_("object"):
					if sender.object().__class__ == NSClassFromString("GSFont"):
						Font = sender.object()
						windowController = Font.parent().windowControllers()[0]
						self.logToConsole("__windowController1", windowController)
					else:
						windowController = sender.object()
						self.logToConsole("__windowController2", windowController)
			except:
				pass
			return windowController
		except:
			self.logError(traceback.format_exc())

PalettePlugin.logToConsole = LogToConsole_AsClassExtension
PalettePlugin.logError = LogError_AsClassExtension
PalettePlugin.loadNib = LoadNib












GlyphsReporterProtocol = objc.protocolNamed("GlyphsReporter")

class ReporterPlugin (NSObject):
	__pyobjc_protocols__ = [GlyphsReporterProtocol]
	def init(self):
		"""
		Put any initializations you want to make here.
		"""
		self.needsExtraMainOutlineDrawingForInactiveLayers = True
		try:
			#Bundle = NSBundle.bundleForClass_(NSClassFromString(self.className()));
			# Default values
			self.menuName = 'New ReporterPlugin'
			self.keyboardShortcut = None
			self.keyboardShortcutModifier = 0 # Set any combination of NSShiftKeyMask | NSControlKeyMask | NSCommandKeyMask | NSAlternateKeyMask
			self.drawDefaultInactiveLayers = True
			self.generalContextMenus = []

			if hasattr(self, 'settings'):
				self.settings()

			if hasattr(self, 'start'):
				self.start()

			return self
		except:
			self.logError(traceback.format_exc())
	
	def interfaceVersion(self):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except:
			self.logError(traceback.format_exc())
	
	def title(self):
		"""
		This is the name as it appears in the menu in combination with 'Show'.
		E.g. 'return "Nodes"' will make the menu item read "Show Nodes".
		"""
		try:
			return self.menuName or self.__class__.__name__ or 'New ReporterPlugin'
		except:
			self.logError(traceback.format_exc())
	
	def keyEquivalent(self):
		"""
		The key for the keyboard shortcut. Set modifier keys in modifierMask() further below.
		Pretty tricky to find a shortcut that is not taken yet, so be careful.
		If you are not sure, use 'return None'. Users can set their own shortcuts in System Prefs.
		"""
		try:
			return self.keyboardShortcut or None
		except Exception as e:
			self.logError(traceback.format_exc())
	
	def modifierMask(self):
		"""
		Use any combination of these to determine the modifier keys for your default shortcut:
			return NSShiftKeyMask | NSControlKeyMask | NSCommandKeyMask | NSAlternateKeyMask
		Or:
			return 0
		... if you do not want to set a shortcut.
		"""
		try:
			return self.keyboardShortcutModifier or 0
		except:
			self.logError(traceback.format_exc())
	
	def drawForegroundForLayer_options_(self, Layer, options):
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
			self._scale = options["Scale"]
			self.black = options["Black"]
			if hasattr(self, 'foreground'):
				self.foreground(Layer)
		except:
			self.logError(traceback.format_exc())
	
	def drawForegroundWithOptions_(self, options):
		"""
		Whatever you draw here will be displayed IN FRONT OF the paths. The difference to drawForegroundForLayer_options_() is that you need to deal with the scaling and current layer yourself.
		
		examples::
			layer = self.activeLayer()
			layerPosition = self.activePosition()
			scale = options["Scale"]
			allLayers = self.controller.graphicView().layoutManager().cachedGlyphs()
			indexOfActiveLayer = self.controller.graphicView().activeIndex()
			selectionRange = self.controller.graphicView().selectedRange()
		"""
		try:
			self._scale = options["Scale"]
			self.black = options["Black"]
			if hasattr(self, 'foregroundInViewCoords'):

				self.foregroundInViewCoords(self.activeLayer())

		except:
			self.logError(traceback.format_exc())
	
	def drawBackgroundForLayer_options_(self, Layer, options):
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			self._scale = options["Scale"]
			self.black = options["Black"]
			if hasattr(self, 'background'):
				self.background(Layer)
		except:
			self.logError(traceback.format_exc())
	
	def drawBackgroundWithOptions_(self, options):
		"""
		Whatever you draw here will be displayed BEHIND the paths. The difference to drawBackgroundForLayer_options_() is that you need to deal with the scaling and current layer yourself.
		"""
		try:
			self._scale = options["Scale"]
			self.black = options["Black"]
			if hasattr(self, 'backgroundInViewCoords'):
				self.backgroundInViewCoords(Glyphs.font.selectedLayers[0])
		except:
			self.logError(traceback.format_exc())
	
	def drawBackgroundForInactiveLayer_options_(self, Layer, options):
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
				if hasattr(self, 'inactiveLayers'):
					self.inactiveLayers(Layer)
			else:
				if hasattr(self, 'preview'):
					self.preview(Layer)
				elif hasattr(self, 'inactiveLayers'):
					self.inactiveLayers(Layer)
		
		except:
			self.logError(traceback.format_exc())
	
	def drawForegroundForInactiveLayer_options_(self, Layer, options):
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
			if self.controller:
				if hasattr(self, 'inactiveLayerForeground'):
					self.inactiveLayerForeground(Layer)
		except:
			print(traceback.format_exc())
	
	def needsExtraMainOutlineDrawingForInactiveLayer_(self, Layer):
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
		except:
			self.logError(traceback.format_exc())
	
	def addMenuItemsForEvent_toMenu_(self, event, contextMenu):
		'''
		The event can tell you where the user had clicked.
		'''
		try:
			
			if self.generalContextMenus:
				setUpMenuHelper(contextMenu, self.generalContextMenus, self)
			
			if hasattr(self, 'conditionalContextMenus'):
				contextMenus = self.conditionalContextMenus()
				if contextMenus:
					setUpMenuHelper(contextMenu, contextMenus, self)
		
		except:
			self.logError(traceback.format_exc())

	@objc.python_method
	def drawTextAtPoint(self, text, textPosition, fontSize=10.0, fontColor=NSColor.blackColor(), align='bottomleft'):
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
				NSFontAttributeName: NSFont.labelFontOfSize_(fontSize/currentZoom),
				NSForegroundColorAttributeName: fontColor }
			displayText = NSAttributedString.alloc().initWithString_attributes_(unicode(text), fontAttributes)
			textAlignment = alignment[align] # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
			displayText.drawAtPoint_alignment_(textPosition, textAlignment)
		except:
			self.logError(traceback.format_exc())
	
	def getHandleSize(self):
		"""
		Returns the current handle size as set in user preferences.
		Use: self.getHandleSize() / self.getScale()
		to determine the right size for drawing on the canvas.
		"""
		try:
			Selected = NSUserDefaults.standardUserDefaults().integerForKey_("GSHandleSize")
			if Selected == 0:
				return 5.0
			elif Selected == 2:
				return 10.0
			else:
				return 7.0 # Regular
		except:
			self.logError(traceback.format_exc())
			return 7.0
	
	def getScale(self):
		"""
		self.getScale() returns the current scale factor of the Edit View UI.
		Divide any scalable size by this value in order to keep the same apparent pixel size.
		"""
		return self._scale
	
	def activeLayer(self):
		try:
			return self.controller.graphicView().activeLayer()
		except:
			self.logError(traceback.format_exc())
	
	def activePosition(self):
		try:
			return self.controller.graphicView().activePosition()
		except:
			self.logError(traceback.format_exc())
	
	def setController_(self, Controller):
		"""
		Use self.controller as object for the current view controller.
		"""
		try:
			self.controller = Controller
		except:
			self.logError(traceback.format_exc())

ReporterPlugin.logToConsole = LogToConsole_AsClassExtension
ReporterPlugin.logError = LogError_AsClassExtension
ReporterPlugin.loadNib = LoadNib












class SelectTool (GSToolSelect):
	
	def init(self):
		"""
		By default, toolbar.pdf will be your tool icon.
		Use this for any initializations you need.
		"""
		try:
			self = objc.super(SelectTool, self).init()
			self.name = 'My Select Tool'
			self.toolbarPosition = 100
			self._icon = 'toolbar.pdf'
			self.keyboardShortcut = None
			self.generalContextMenus = ()
			
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
					Bundle = NSBundle.bundleWithPath_(path[:path.rfind("Contents/Resources/")])
				else:
					Bundle = NSBundle.bundleForClass_(NSClassFromString(self.className()));
				if self._icon != None:
					self.tool_bar_image = Bundle.imageForResource_(self._icon)
					self.tool_bar_image.setTemplate_(True) # Makes the icon blend in with the toolbar.
			except:
				self.logError(traceback.format_exc())
			if hasattr(self, 'start'):
				self.start()
			
			return self
		except:
			self.logError(traceback.format_exc())
		return objc.nil

	def view(self):
		return self.inspectorDialogView
	
	def inspectorViewControllers(self):
		ViewControllers = objc.super(SelectTool, self).inspectorViewControllers()
		if ViewControllers is None:
			ViewControllers = []
		try:
			# self.inspectorDialogView may also be defined witut a .nib,
			# so it could be a Vanilla dialog
			if self.inspectorDialogView:
				ViewControllers.append(self)
		
		except:
			self.logError(traceback.format_exc())
		
		return ViewControllers
	
	def interfaceVersion(self):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except:
			self.logError(traceback.format_exc())
	
	def title(self):
		"""
		The name of the Tool as it appears in the tooltip.
		"""
		try:
			return self.name
		except:
			self.logError(traceback.format_exc())
	
	def toolBarIcon(self):
		"""
		Return a instance of NSImage that represents the toolbar icon as established in init().
		Unless you know what you are doing, leave this as it is.
		"""
		try:
			return self.tool_bar_image
		except:
			self.logError(traceback.format_exc())
		return objc.nil
	
	def groupID(self):
		"""
		Determines the position in the toolbar.
		Higher values are further to the right.
		"""
		try:
			return self.toolbarPosition
		except:
			self.logError(traceback.format_exc())

	@objc.python_method
	def trigger(self):
		"""
		The key to select the tool with keyboard (like v for the select tool).
		Either use trigger() or keyEquivalent(), not both. Remove the method(s) you do not use.
		"""
		try:
			return self.keyboardShortcut
		except:
			self.logError(traceback.format_exc())
	
	def willSelectTempTool_(self, TempTool):
		"""
		Temporary Tool when user presses Cmd key.
		Should always be GlyphsToolSelect unless you have a better idea.
		"""
		try:
			return TempTool.__class__.__name__ != "GlyphsToolSelect"
		except:
			self.logError(traceback.format_exc())
	
	def willActivate(self):
		"""
		Do stuff when the tool is selected.
		E.g. show a window, or set a cursor.
		"""
		try:
			objc.super(SelectTool, self).willActivate()
			if hasattr(self, 'activate'):
				self.activate()
		except:
			self.logError(traceback.format_exc())
	
	def willDeactivate(self):
		"""
		Do stuff when the tool is deselected.
		"""
		try:
			objc.super(SelectTool, self).willDeactivate()
			if hasattr(self, 'deactivate'):
				self.deactivate()
		except:
			self.logError(traceback.format_exc())
	
	def elementAtPoint_atLayer_(self, currentPoint, activeLayer):
		"""
		Return an element in the vicinity of currentPoint (NSPoint), and it will be captured by the tool.
		Use Boolean ...
			distance(currentPoint, referencePoint) < clickTolerance / Scale)
		... for determining whether the NSPoint referencePoint is captured or not.
		Use:
			myPath.nearestPointOnPath_pathTime_(currentPoint, 0.0)
		
		"""
		return objc.super(SelectTool, self).elementAtPoint_atLayer_(currentPoint, activeLayer)
		
		try:
			Scale = self.editViewController().graphicView().scale()
			clickTolerance = 4.0
			
			for p in activeLayer.paths:
				for n in p.nodes:
					if distance(currentPoint, n.position) < clickTolerance / Scale:
						return n
			
			for a in activeLayer.anchors:
				if distance(currentPoint, a.position) < clickTolerance / Scale:
					return a
		
		except:
			self.logError(traceback.format_exc())
	
	# The following four methods are optional, and only necessary
	# if you intend to extend the context menu with extra items.
	# Remove them if you do not want to change the context menu:
	
	def defaultContextMenu(self):
		"""
		Sets the default content of the context menu and returns the menu.
		Add menu items that do not depend on the context,
		e.g., actions that affect the whole layer, no matter what is selected.
		Remove this method if you do not want any extra context menu items.
		"""
		try:
			# Get the current default context menu:
			theMenu = objc.super(SelectTool, self).defaultContextMenu()
			
			# Add separator at the bottom:
			newSeparator = NSMenuItem.separatorItem()
			theMenu.addItem_(newSeparator)
			
			# Add menu items at the bottom:
			setUpMenuHelper(theMenu, self.generalContextMenus, self)
			
			return theMenu
		except:
			self.logError(traceback.format_exc())
	
	def addMenuItemsForEvent_toMenu_(self, theEvent, theMenu):
		"""
		Adds menu items to default context menu.
		Remove this method if you do not want any extra context menu items.
		"""
		try:
			
			if hasattr(self, 'conditionalContextMenus'):
				contextMenus = self.conditionalContextMenus()
			
				if contextMenus:
					# Todo: Make sure that the index is 0 for all items,
					# i.e., add at top rather than at bottom of menu:
					newSeparator = NSMenuItem.separatorItem()
					theMenu.addItem_(newSeparator)
					setUpMenuHelper(theMenu, contextMenus, self)
					
		except:
			self.logError(traceback.format_exc())
	
	def drawForegroundForLayer_(self, Layer):
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
			if hasattr(self, 'foreground'):
				self.foreground(Layer)
		except:
			self.logError(traceback.format_exc())
	
	def drawBackgroundForLayer_(self, Layer):
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			if hasattr(self, 'background'):
				self.background(Layer)
		except:
			self.logError(traceback.format_exc())


SelectTool.logToConsole = LogToConsole_AsClassExtension
SelectTool.logError = LogError_AsClassExtension
SelectTool.loadNib = LoadNib

