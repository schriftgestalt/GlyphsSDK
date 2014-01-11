#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

GlyphsPaletteProtocol = objc.protocolNamed( "GlyphsPalette" )

class ____PluginClassName____ ( NSObject, GlyphsPaletteProtocol ):
	_theView = objc.IBOutlet()
	
	def init( self ):
		"""
		Do all initializing here.
		Customize the quadruple underscore items.
		Change other stuff only if you know what you are doing.
		"""
		
		if NSBundle.loadNibNamed_owner_( "____PaletteView____", self ):
			self.logToConsole( "Palette.Layers: Error loading Nib!" )
		
		s = objc.selector( self.update, signature="v@:" )
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSUpdateInterface", None )
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSDocumentCloseNotification", None )
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSDocumentActivateNotification", None )
		
		Frame = self._theView.frame()
		
		if NSUserDefaults.standardUserDefaults().objectForKey_( "____CFBundleIdentifier____.ViewHeight" ):
			Frame.size.height = NSUserDefaults.standardUserDefaults().integerForKey_( "____CFBundleIdentifier____.ViewHeight" )
			self._theView.setFrame_(Frame)
		
		#Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ));
		return self
		
	def title( self ):
		"""
		This is the name as it appears in the Palette section header.
		"""
		return "____PluginMenuName____"
	
	def interfaceVersion( self ):
		"""
		Must return 1.
		"""
		return 1
	
	def theView( self ):
		"""
		Returns an NSView to be displayed in the palette.
		"""
		return self._theView
	
	def minHeight( self ):
		"""
		The minimum height of the view in pixels.
		"""
		return 80
	
	def maxHeight( self ):
		"""
		The maximum height of the view in pixels.
		Must be equal to or bigger than minHeight.
		"""
		return 150
	
	def currentHeight( self ):
		"""
		The current height of the Palette section.
		Used for storing the current resized state.
		"""
		return NSUserDefaults.standardUserDefaults().integerForKey_( "____CFBundleIdentifier____.ViewHeight" )
	
	def setCurrentHeight_( self, newHeight ):
		"""
		Sets a new height for the Palette section.
		"""
		if newHeight >= self.minHeight() and newHeight <= self.maxHeight():
			NSUserDefaults.standardUserDefaults().setInteger_forKey_( newHeight, "____CFBundleIdentifier____.ViewHeight" )
	
	def currentWindowController( self, sender ):
		"""
		Returns a window controller object.
		Use self.currentWindowController()
		"""
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
	
	def update( self, sender ):
		"""
		Called from the notificationCenter if the info in the current Glyph window has changed.
		This can be called quite a lot, so keep the method fast.
		"""
		Layer = None
		try:
			windowController = self.currentWindowController( sender )
			Layer = windowController.activeLayer()
		except:
			pass
		if Layer:
			# Do stuff here
			pass
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )
	