#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

GlyphsPaletteProtocol = objc.protocolNamed( "GlyphsPalette" )

class SmileyPalette ( NSObject, GlyphsPaletteProtocol ):
	_theView = objc.IBOutlet()
	_theImageView = objc.IBOutlet()

	def init( self ):
		"""
		Do all initializing here.
		"""
		try:
			if not NSBundle.loadNibNamed_owner_( "SmileyPaletteView", self ):
				self.logToConsole( "Palette Layers: Error loading Nib!" )
		
			s = objc.selector( self.update, signature='v@:' )
			NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSUpdateInterface", None )
			NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSDocumentCloseNotification", None )
			NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSDocumentActivateNotification", None )
		
			Frame = self._theView.frame()
		
			if NSUserDefaults.standardUserDefaults().objectForKey_( "com.GeorgSeifert.SmileyPalette.ViewHeight" ):
				Frame.size.height = NSUserDefaults.standardUserDefaults().integerForKey_( "com.GeorgSeifert.SmileyPalette.ViewHeight" )
				self._theView.setFrame_(Frame)
		
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
		
	def title( self ):
		"""
		This is the name as it appears in the Palette section header.
		"""
		try:
			return "Smiley"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def theView( self ):
		"""
		Returns an NSView to be displayed in the palette.
		This is the grey background in the palette, on which you can place UI items.
		"""
		try:
			return self._theView
		except Exception as e:
			self.logToConsole( "theView: %s" % str(e) )
	
	def minHeight( self ):
		"""
		The minimum height of the view in pixels.
		"""
		try:
			return 78
		except Exception as e:
			self.logToConsole( "minHeight: %s" % str(e) )
	
	def maxHeight( self ):
		"""
		The maximum height of the view in pixels.
		Must be equal to or bigger than minHeight.
		"""
		try:
			return 78
		except Exception as e:
			self.logToConsole( "maxHeight: %s" % str(e) )
	
	def currentHeight( self ):
		"""
		The current height of the Palette section.
		Used for storing the current resized state.
		If you have a fixed height, you can return the height in pixels
		"""
		try:
			return 78
			# NSUserDefaults.standardUserDefaults().integerForKey_( "com.GeorgSeifert.SmileyPalette.ViewHeight" )
		except Exception as e:
			self.logToConsole( "currentHeight: %s" % str(e) )
	
	def setCurrentHeight_( self, newHeight ):
		"""
		Sets a new height for the Palette section.
		"""
		try:
			if newHeight >= self.minHeight() and newHeight <= self.maxHeight():
				NSUserDefaults.standardUserDefaults().setInteger_forKey_( newHeight, "com.GeorgSeifert.SmileyPalette.ViewHeight" )
		except Exception as e:
			self.logToConsole( "setCurrentHeight_: %s" % str(e) )
	
	def currentWindowController( self, sender ):
		"""
		Returns a window controller object.
		Use self.currentWindowController() to access it.
		"""
		try:
			windowController = None
			try:
				windowController = NSDocumentController.sharedDocumentController().currentDocument().windowController()
				if not windowController and sender.respondsToSelector_( "object" ):
					if sender.object().__class__ == NSClassFromString( "GSFont" ):
						Font = sender.object()
						windowController = Font.parent().windowControllers()[0]
						self.logToConsole( "__windowController1", windowController )
					else:
						windowController = sender.object()
						self.logToConsole( "__windowController2", windowController )
			except:
				pass
			return windowController
		except Exception as e:
			self.logToConsole( "currentWindowController: %s" % str(e) )
	
	def update( self, sender ):
		"""
		Called from the notificationCenter if the info in the current Glyph window has changed.
		This can be called quite a lot, so keep this method fast.
		"""
		try:
			Layer = None
			
			try:
				windowController = self.currentWindowController( sender )
				Layer = windowController.activeLayer()
			except:
				pass
				
			if Layer:
				self._theImageView.setHidden_( False )
			else:
				self._theImageView.setHidden_( True )
		except Exception as e:
			self.logToConsole( "update: %s" % str(e) )
			
		
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )
	
