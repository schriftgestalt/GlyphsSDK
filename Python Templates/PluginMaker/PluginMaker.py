"""PluginMaker -- A tool to quickly instantiate a plugin"""
from __future__ import print_function, unicode_literals

from Cocoa import NSObject, NSUserDefaults, NSBundle, NSError, NSLocalizedDescriptionKey, NSLocalizedRecoverySuggestionErrorKey, NSApp, NSSavePanel, NSOKButton, NSURL
from PyObjCTools import AppHelper
import objc
import os
import shutil

_pluginTypes = [
	{
		"name": "General",
		"path": "General Plugin/____PluginName____.glyphsPlugin",
	},
	{
		"name": "Reporter",
		"path": "Reporter/____PluginName____.glyphsReporter",
	},
	{
		"name": "Filter, Dialog with xib",
		"path": "Filter/dialog with xib/____PluginName____.glyphsFilter",
	},
	{
		"name": "Filter, without Dialog",
		"path": "Filter/without dialog/____PluginName____.glyphsFilter",
	},
	{
		"name": "Palette",
		"path": "Palette/____PluginName____.glyphsPalette"
	},
	{
		"name": "SelectTool",
		"path": "SelectTool/____PluginName____.glyphsTool",
	},
	{
		"name": "File Format, Dialog with vanilla",
		"path": "File Format/dialog with vanilla/____PluginName____.glyphsFileFormat",
	},
	{
		"name": "File Format, Dialog with xib",
		"path": "File Format/dialog with xib/____PluginName____.glyphsFileFormat",
	}
]

_pluginTypesNames = [x["name"] for x in _pluginTypes]


def GetSaveFile(message=None, ProposedFileName=None, filetypes=None):
	Panel = NSSavePanel.savePanel().retain()
	if message is not None:
		Panel.setTitle_(message)
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


try:
	from objc import python_method
except ImportError:
	def python_method(arg):
		return arg
	objc.python_method = python_method


class PluginMaker(NSObject):
	window = objc.IBOutlet()

	def pluginTypesNames(self):
		return _pluginTypesNames

	@objc.python_method
	def replacePlaceholders(self, filePath, replaceDict):
		try:
			import codecs
			pluginFile = codecs.open(filePath, mode="r", encoding="utf-8")
			plugin = pluginFile.read()
			assert len(plugin) > 1
			pluginFile.close()
			for key, value in replaceDict.items():
				plugin = plugin.replace(key, value)
			pluginFile = codecs.open(filePath, "w", encoding="utf-8")
			pluginFile.write(plugin)
			pluginFile.close()
		except Exception as e:
			description = "could not convert file: %s" % os.path.basename(filePath)
			recovery = str(e)
			errorDetail = {
				NSLocalizedDescriptionKey: description,
				NSLocalizedRecoverySuggestionErrorKey: recovery
			}
			error = NSError.errorWithDomain_code_userInfo_("error", 1, errorDetail)
			NSApp.presentError_(error)

	@objc.IBAction
	def makePlugin_(self, sender):
		self.window.endEditingFor_(None)
		defaults = NSUserDefaults.standardUserDefaults()
		pluginTypeIndex = defaults.integerForKey_("SelectedPluginType")
		pluginType = _pluginTypes[pluginTypeIndex]
		pluginName = defaults.objectForKey_("PluginName")
		warningExplanation = "Must be at least 2 letters. Make sure to tab out of the text field to confirm the entry."
		if pluginName is None or len(pluginName) < 2:
			description = "Plugin Name (‘%s’) too short. %s" % (pluginName, warningExplanation)
			errorDetail = {NSLocalizedDescriptionKey: description}
			error = NSError.errorWithDomain_code_userInfo_("error", 1, errorDetail)
			NSApp.presentError_(error)
			return
		pluginClass = defaults.objectForKey_("PluginClass")
		if pluginClass is None or len(pluginClass) < 2:
			description = "Plugin Class (‘%s’) too short. %s" % (pluginClass, warningExplanation)
			errorDetail = {NSLocalizedDescriptionKey: description}
			error = NSError.errorWithDomain_code_userInfo_("error", 2, errorDetail)
			NSApp.presentError_(error)
			return
		developer = defaults.objectForKey_("Developer")
		if developer is None or len(developer) < 2:
			description = "Developer Name (‘%s’) too short. %s" % (developer, warningExplanation)
			errorDetail = {NSLocalizedDescriptionKey: description}
			error = NSError.errorWithDomain_code_userInfo_("error", 3, errorDetail)
			NSApp.presentError_(error)
			return
		appPath = NSBundle.mainBundle().bundlePath()

		appIsInTemplateFolder = appPath.find("/Python Templates/")
		if appIsInTemplateFolder < 0:
			description = "The app must be inside the /Python Templates/ folder"
			errorDetail = {NSLocalizedDescriptionKey: description}
			error = NSError.errorWithDomain_code_userInfo_("error", 4, errorDetail)
			NSApp.presentError_(error)
			return
		templateFolder = appPath[:appIsInTemplateFolder + 18]

		fileName = os.path.basename(pluginType["path"])
		fileName = fileName.replace("____PluginName____", pluginName)
		exportFilePath = GetSaveFile("Where to put the plugin", fileName)
		if exportFilePath is not None and len(exportFilePath) > 2:
			templatePath = os.path.join(templateFolder, pluginType["path"])
			if os.path.exists(exportFilePath):
				shutil.rmtree(exportFilePath)
			result = shutil.copytree(templatePath, exportFilePath)
			os.utime(exportFilePath, None)
			import datetime
			now = datetime.datetime.now()
			replaceDict = {
				"____PluginName____": pluginName,
				"____Developer____": developer,
				"____PluginClassName____": pluginClass,
				"____BundleVersion____": "1",
				"____BundleVersionString____": "0.1",
				"____YEAR____": str(now.year),
			}
			infoPlistFile = os.path.join(exportFilePath, "Contents/Info.plist")
			self.replacePlaceholders(infoPlistFile, replaceDict)

			pluginFile = os.path.join(exportFilePath, "Contents/Resources/plugin.py")
			self.replacePlaceholders(pluginFile, replaceDict)

			xibFile = os.path.join(exportFilePath, "Contents/Resources/IBdialog.xib")
			if os.path.exists(xibFile):
				self.replacePlaceholders(pluginFile, replaceDict)

	@objc.IBAction
	def showWindow_(self, sender):
		self.window.makeKeyAndOrderFront_(objc.nil)


if __name__ == "__main__":
	AppHelper.runEventLoop()
