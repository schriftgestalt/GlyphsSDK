# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re, commands, traceback
from types import *

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

from GlyphsApp import *
GlyphsFileFormatProtocol = objc.protocolNamed( "GlyphsFileFormat" )






class FileFormatPlugin ( NSObject, GlyphsFileFormatProtocol ):
	


	def init( self ):
		"""
		Do all initializing here.
		"""
		try:

			self.lastErrorMessage = ''

			# Settings, default values
			self.name = 'My File Format'
			self.dialog = '____PluginFileName____Dialog'
			self.icon = 'ExportIcon'
			self.toolbarPosition = 100

			if hasattr(self, 'settings'):
				self.settings()


			NSBundle.loadNibNamed_owner_(self.dialog, self )
			thisBundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ) )
			self.toolbarIcon = NSImage.alloc().initWithContentsOfFile_( thisBundle.pathForImageResource_(self.icon) )
			self.toolbarIcon.setName_(self.icon)

			if hasattr(self, 'loadPlugin'):
				self.loadPlugin()

		except:
			self.logError(traceback.format_exc())

		return self
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for.
		Return 1.
		"""
		try:
			return 1
		except:
			self.logError(traceback.format_exc())
	
	def title( self ):
		"""
		This is the name as it appears in the menu in combination with 'Show'.
		E.g. 'return "Nodes"' will make the menu item read "Show Nodes".
		"""
		try:
			return self.name or self.__class__.__name__ or 'New FileFormat Plugin'
		except:
			self.logError(traceback.format_exc())
	
	def toolbarTitle( self ):
		"""
		Name below the icon in the Export dialog toolbar.
		"""
		try:
			return self.name
		except:
			self.logError(traceback.format_exc())
	
	def toolbarIconName( self ):
		"""
		The filename of the icon, without the suffix.
		"""
		try:
			return self.icon or "ExportIcon"
		except:
			self.logError(traceback.format_exc())


	def groupID( self ):
		"""
		Determines the position in the Export dialog toolbar.
		Lower values are further to the left.
		"""
		try:
			return self.toolbarPosition or 100
		except:
			self.logError(traceback.format_exc())
	
	def progressWindow( self ):
		try:
			return None
		except:
			self.logError(traceback.format_exc())
	
	def exportSettingsView( self ):
		"""
		Returns the view to be displayed in the export dialog.
		Don't touch this.
		"""
		try:
			return self.dialog
		except:
			self.logError(traceback.format_exc())
	
	def font( self ):
		try:
			return self._font
		except:
			self.logError(traceback.format_exc())
	
	def setFont_( self, GSFontObj ):
		"""
		The GSFont object is assigned to the plugin prior to the export.
		This is used to publish the export dialog.
		"""
		try:
			self._font = GSFontObj
		except:
			self.logError(traceback.format_exc())
	

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
					NSLocalizedFailureReasonErrorKey: None,
					NSLocalizedRecoverySuggestionErrorKey: NSLocalizedString(returnMessage, None)
					})
				return (False, error)


		# Python exception, return error message
		except Exception as e:
			self.logError(traceback.format_exc())
			error = NSError.errorWithDomain_code_userInfo_(self.title(), -57, {
				NSLocalizedDescriptionKey: NSLocalizedString('Python exception', None),
				NSLocalizedFailureReasonErrorKey: None,
				NSLocalizedRecoverySuggestionErrorKey: NSLocalizedString(str(e), None)
				})

			return (False, error)
	
	
	def saveFileDialog( self, title=None, proposedFilename=None, fileTypes=None ):
		"""
		Opens a standard Save File Dialog.
		"""
		try:
			if fileTypes is None:
				fileTypes = []
			Panel = NSSavePanel.savePanel().retain()
			if title is not None:
				Panel.setTitle_( title )
			Panel.setCanChooseFiles_( True )
			Panel.setCanChooseDirectories_( False )
			Panel.setAllowedFileTypes_( fileTypes )
			if proposedFilename is not None:
				Panel.setNameFieldStringValue_( proposedFilename )
			pressedButton = Panel.runModalForTypes_(fileTypes)
			if pressedButton == 1: # 1=OK, 0=Cancel
				return Panel.filename()
			return None
		except:
			self.logError(traceback.format_exc())
		
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Font format %s:\n%s" % ( self.title(), message )
		NSLog( myLog )

	def logError(self, message):
		try:
			if message != self.lastErrorMessage:
				self.logToConsole(message)
				self.lastErrorMessage = message
#				Glyphs.showNotification('Error in %s' % self.title(), 'Check the Console output for details.')
		except:
			self.logToConsole(traceback.format_exc())


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
