#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

GlyphsFileFormatProtocol = objc.protocolNamed( "GlyphsFileFormat" )

class ____PluginClassName____ ( NSObject, GlyphsFileFormatProtocol ):
	
	def init( self ):
		"""
		Do all initializing here.
		"""
		#Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ));
		return self
		
	def title( self ):
		"""
		This is the name as it appears in the menu in combination with 'Show'.
		E.g. 'return "Nodes"' will make the menu item read "Show Nodes".
		"""
		return "____PluginMenuName____"
	
	def groupID( self ):
		"""
		Determines the position in the toolbar.
		"""
		return 100
	
	def interfaceVersion( self ):
		"""
		Must return 1.
		"""
		return 1
	
	def exportSettingsView():
		"""
		Return an NSView to be displayed in the export dialog.
		"""
		return 
	
	def setFont_( self, GSFontObj ):
		"""
		The GSFont object is assigned to the plugin prior to the export.
		This is used to publish the export dialog.
		"""
		self.font = GSFontObj
	
	def writeFont_error_( self, font, error ):
		"""
		Outputs a Font object.
		This function should ask the user for the place to save the store the font.
		
		param: Font The font to export.
		param: error On return, If the document contents could not be read, a pointer to an error object that encapsulates the reason they could not be read.

		return (True, None) if the operation was successful;
		otherwise return a tuple with False and a NSError object that contains info about the problem (False, NSError).
		"""
		
		return ( True, None )
	
	def writeFont_toURL_error_( self, font, URL, error ):
		"""
		Outputs a Font object to the specified URL.
		font: the font to export.
		URL: the URL to save the font to.
		error: on return, if the document contents could not be read, a pointer to an error object that encapsulates the reason they could not be read.
		return ( True, None ) if the operation was successful; otherwise return a tuple with False and a NSError object that contains info about the problem ( False, NSError ).
		"""
		
		return ( True, None )
	
	def fontFromURL_ofType_error_( self, URL, type, error ):
		"""
		Reads a Font object from the specified URL.
		
		param: URL The URL to read the font from.
		param: error On return, If the document contents could not be read, a pointer to an error object that encapsulates the reason they could not be read.
		return: The font object, or nil if an error occurred.
		"""
		
		font = GSFont()
		# add some glyphs...
		return font
		
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Font format %s:\n%s" % ( self.title(), message )
		NSLog( myLog )
	
