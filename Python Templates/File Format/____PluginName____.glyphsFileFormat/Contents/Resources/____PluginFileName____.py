#!/usr/bin/env python
# encoding: utf-8

###########################################################################################################
#
#
#	File Format Plugin
#	Implementation for exporting fonts through the Export dialog
#
#	For help on the use of Interface Builder, please read the introduction at
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################



import objc
from Foundation import *
from AppKit import *
import sys, os, re, commands
from types import *

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

from GlyphsApp import *
GlyphsFileFormatProtocol = objc.protocolNamed( "GlyphsFileFormat" )



# Preference key names
# Part of the example. You may delete them
unicodePref = 'com.test.csvexport.exportUnicode'
glyphWidthPref = 'com.test.csvexport.exportGlyphWidth'



class ____PluginClassName____ ( NSObject, GlyphsFileFormatProtocol ):
	# The NSView object from the User Interface
	settings_view = objc.IBOutlet()
	
	# Example variables. You may delete them
	feedbackTextField = objc.IBOutlet()
	unicodeCheckBox = objc.IBOutlet()
	glyphWidthCheckbox = objc.IBOutlet()

	# Example function. You may delete it
	@objc.IBAction
	def setExportUnicode_(self, sender):
		Glyphs.defaults[unicodePref] = bool(sender.intValue())
		self.updateFeedBackTextField()

	# Example function. You may delete it
	@objc.IBAction
	def setExportGlyphWidth_(self, sender):
		Glyphs.defaults[glyphWidthPref] = bool(sender.intValue())
		self.updateFeedBackTextField()

	# Example function. You may delete it
	def updateFeedBackTextField(self):
		string = []
		if Glyphs.defaults[unicodePref]:
			string.append('Unicodes')
		if Glyphs.defaults[glyphWidthPref]:
			string.append('Glyph Width')
		self.feedbackTextField.setStringValue_(', '.join(string) if len(string) else 'Nothing')


	def init( self ):
		"""
		Do all initializing here.
		"""
		try:
			NSBundle.loadNibNamed_owner_( "____PluginFileName____Dialog", self )
			thisBundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ) )
			self.toolbarIcon = NSImage.alloc().initWithContentsOfFile_( thisBundle.pathForImageResource_( "ExportIcon" ) )
			self.toolbarIcon.setName_( "ExportIcon" )
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )

		# Init user preferences if not existent and set default value
		if Glyphs.defaults[unicodePref] == None:
			Glyphs.defaults[unicodePref] = True
		if Glyphs.defaults[glyphWidthPref] == None:
			Glyphs.defaults[glyphWidthPref] = True

		# Set initial state of checkboxes according to user variables
		self.unicodeCheckBox.setState_(Glyphs.defaults[unicodePref])
		self.glyphWidthCheckbox.setState_(Glyphs.defaults[glyphWidthPref])

		# Update text field. You may delete them
		self.updateFeedBackTextField()

		return self
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for.
		Return 1.
		"""
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def title( self ):
		"""
		This is a human-readable name, necessary for the export dialog.
		"""
		try:
			return "____PluginMenuName____"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def toolbarTitle( self ):
		"""
		Name below the icon in the Export dialog toolbar.
		"""
		try:
			return "____PluginToolbarTitle____"
		except Exception as e:
			self.logToConsole( "toolbarTitle: %s" % str(e) )
	
	def toolbarIconName( self ):
		"""
		The filename of the icon, without the suffix.
		"""
		try:
			return "ExportIcon"
		except Exception as e:
			self.logToConsole( "toolbarIconName: %s" % str(e) )
	
	def fileExtension( self ):
		"""
		Suffix of the filename without the dot.
		"""
		try:
			return "csv"
		except Exception as e:
			self.logToConsole( "fileExtension: %s" % str(e) )
	
	def groupID( self ):
		"""
		Determines the position in the Export dialog toolbar.
		Lower values are further to the left.
		"""
		try:
			return 100
		except Exception as e:
			self.logToConsole( "groupID: %s" % str(e) )
	
	def progressWindow( self ):
		try:
			return None
		except Exception as e:
			self.logToConsole( "progressWindow: %s" % str(e) )
	
	def exportSettingsView( self ):
		"""
		Returns the view to be displayed in the export dialog.
		Don't touch this.
		"""
		try:
			return self.settings_view
		except Exception as e:
			self.logToConsole( "exportSettingsView: %s" % str(e) )
	
	def font( self ):
		try:
			return self._font
		except Exception as e:
			self.logToConsole( "font: %s" % str(e) )
	
	def setFont_( self, GSFontObj ):
		"""
		The GSFont object is assigned to the plugin prior to the export.
		This is used to publish the export dialog.
		"""
		try:
			self._font = GSFontObj
		except Exception as e:
			self.logToConsole( "setFont_: %s" % str(e) )
	
	# Example function. You may delete it
	def writeCSVFile(self, font, filepath):
		import csv

		with open(filepath, 'w') as csvfile:
			fieldnames = ['glyph_name', 'unicode', 'glyph_width']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			writer.writeheader()
			
			for g in font.glyphs:
				writeDict = {}
				writeDict['glyph_name'] = g.name
				
				if Glyphs.defaults[unicodePref] == True and g.unicode:
					writeDict['unicode'] = g.unicode

				if Glyphs.defaults[glyphWidthPref] == True and g.layers[0].width:
					writeDict['glyph_width'] = g.layers[0].width
			
				writer.writerow(writeDict)

	def writeFont_error_( self, font, error ):
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
			
			# Ask for export destination and write the file:
			dialogMessage = "Choose export destination"
			dialogProposedFileName = font.familyName
			dialogFiletypes = [ self.fileExtension() ]
			filepath = self.saveFileDialog( message = dialogMessage, ProposedFileName = dialogProposedFileName, filetypes = dialogFiletypes )

			# Catch cancelled file dialog
			if filepath:
				self.writeCSVFile(font, filepath)


			# Export successful
			# Change the condition (True) to your own assessment on whether or not the export succeeded
			if True:
				
				# Use Mac Notification Center
				notification = NSUserNotification.alloc().init()
				notification.setTitle_(self.title())
				notification.setInformativeText_('The export of "%s" was successful.' % (os.path.basename(filepath)))
				NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
				
				return (True, None)
			
			# Export failed, give reason
			else:
				error = NSError.errorWithDomain_code_userInfo_(self.title(), -57, {
					NSLocalizedDescriptionKey: NSLocalizedString('Export failed', None),
					NSLocalizedFailureReasonErrorKey: None,
					NSLocalizedRecoverySuggestionErrorKey: NSLocalizedString('The reason is unclear', None)
					})
				return (False, error)


		# Python exception, return error message
		except Exception as e:
			self.logToConsole( "writeFont_error_: %s" % str(e) )
			error = NSError.errorWithDomain_code_userInfo_(self.title(), -57, {
				NSLocalizedDescriptionKey: NSLocalizedString('Python exception', None),
				NSLocalizedFailureReasonErrorKey: None,
				NSLocalizedRecoverySuggestionErrorKey: NSLocalizedString(str(e), None)
				})

			return (False, error)
	
	
	def saveFileDialog( self, message=None, ProposedFileName=None, filetypes=None ):
		"""
		Opens a standard Save File Dialog.
		"""
		try:
			if filetypes is None:
				filetypes = []
			Panel = NSSavePanel.savePanel().retain()
			if message is not None:
				Panel.setTitle_( message )
			Panel.setCanChooseFiles_( True )
			Panel.setCanChooseDirectories_( False )
			Panel.setAllowedFileTypes_( filetypes )
			if ProposedFileName is not None:
				Panel.setNameFieldStringValue_( ProposedFileName )
			pressedButton = Panel.runModalForTypes_(filetypes)
			if pressedButton == 1: # 1=OK, 0=Cancel
				return Panel.filename()
			return None
		except Exception as e:
			self.logToConsole( "saveFileDialog: %s" % str(e) )
		
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Font format %s:\n%s" % ( self.title(), message )
		NSLog( myLog )


########################################################################
#
#
#	def writeFont_toURL_error_()
#	To be implemented in Glyphs in the future
#	Don't delete, it needs to be present in the plugin already
#
#
########################################################################


	def writeFont_toURL_error_( self, font, URL, error ):
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
			self.writeCSVFile(font, filepath)

			return (True, None)
		except Exception as e:
			self.logToConsole( "writeFont_toURL_error_: %s" % str(e) )
			return (False, e)


########################################################################
#
#
#	def fontFromURL_ofType_error_()
#	Read fonts from files: To be implemented in Glyphs in the future
#	Don't delete, it needs to be present in the plugin already
#
#
########################################################################
	
	def fontFromURL_ofType_error_( self, URL, fonttype, error ):
		"""
		Reads a Font object from the specified URL.
		
		URL: the URL to read the font from.
		error: on return, if the document contents could not be read, a pointer to an error object that encapsulates the reason they could not be read.
		Return the font object, or None if an error occurred.
		"""
		try:
			# Create a new font object:
			font = GSFont()
			# Add glyphs and other info here...
			pass
			# Return the font object to be opened in Glyphs:
			return font
		except Exception as e:
			self.logToConsole( "fontFromURL_ofType_error_: %s" % str(e) )
			return None
