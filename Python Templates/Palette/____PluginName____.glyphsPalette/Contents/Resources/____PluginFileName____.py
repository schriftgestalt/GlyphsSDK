#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

"""
	Using Interface Builder (IB):
	
	Your code communicates with the UI through
	- IBOutlets (.py->GUI): values available to a UI element (e.g. a string for a text field)
	- IBActions (GUI->.py): methods in this class, triggered by buttons or other UI elements
	
	In order to make the Interface Builder items work, follow these steps:
	1. Make sure you have your IBOutlets (other than _theView)
	   defined as class variables at the beginning of this controller class.
	2. Immediately *before* the def statement of a method that is supposed to be triggered
	   by a UI action (e.g., setMyValue_() triggered by the My Value field), put:
		@objc.IBAction
	   Make sure the method name ends with an underscore, e.g. setValue_(),
	   otherwise the action will not be able to send its value to the class method.
	3. Open the .xib file in XCode, and add and arrange interface elements.
	4. Add this .py file via File > Add Files..., Xcode will recognize IBOutlets and IBACtions
	5. In the left sidebar, choose Placeholders > File's Owner,
	   in the right sidebar, open the Identity inspector (3rd icon),
	   and put the name of this controller class in the Custom Class > Class field
	6. IBOutlets: Ctrl-drag from the File's Owner to a UI element (e.g. text field),
	   and choose which outlet shall be linked to the UI element
	7. IBActions: Ctrl-drag from a UI element (e.g. button) to the File’s Owner in the left sidebar,
	   and choose the class method the UI element is supposed to trigger.
	   If you want a stepping field (change the value with up/downarrow),
	   then select the Entry Field, and set Identity Inspector > Custom Class to:
		GSSteppingTextField
	   ... and Attributes Inspector (top right, 4th icon) > Control > State to:
		Continuous
	8. Compile the .xib file to a .nib file with this Terminal command:
		ibtool xxx.xib --compile xxx.nib
	   (Replace xxx by the name of your xib/nib)
	   Please note: Every time the .xib is changed, it has to be recompiled to a .nib.
	   Check Console.app for error messages to see if everything went right.

	For a quick walkthrough, read:
	http://blog.adamw523.com/os-x-cocoa-application-python-pyobjc/
"""

GlyphsPaletteProtocol = objc.protocolNamed( "GlyphsPalette" )

class ____PluginClassName____ ( NSObject, GlyphsPaletteProtocol ):
	# Define all your IB outlets for your .xib here:
	_theView = objc.IBOutlet() # Palette view on which you can place UI elements.
	
	def init( self ):
		"""
		Do all initializing here, and customize the quadruple underscore items.
		____CFBundleIdentifier____ should be the reverse domain name you specified in Info.plist.
		"""
		try:
			if not NSBundle.loadNibNamed_owner_( "____PaletteView____", self ):
				self.logToConsole( "Error loading .nib into Palette." )
		
			s = objc.selector( self.update, signature="v@:" )
			NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSUpdateInterface", None )
			NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSDocumentCloseNotification", None )
			NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSDocumentActivateNotification", None )
		
			Frame = self._theView.frame()
			if NSUserDefaults.standardUserDefaults().objectForKey_( "____CFBundleIdentifier____.ViewHeight" ):
				Frame.size.height = NSUserDefaults.standardUserDefaults().integerForKey_( "____CFBundleIdentifier____.ViewHeight" )
				self._theView.setFrame_( Frame )
		
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		return 1
	
	def title( self ):
		"""
		This is the name as it appears in the Palette section header.
		"""
		try:
			return "____PluginMenuName____"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
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
			return 80
		except Exception as e:
			self.logToConsole( "minHeight: %s" % str(e) )
	
	def maxHeight( self ):
		"""
		The maximum height of the view in pixels.
		Must be equal to or bigger than minHeight.
		"""
		try:
			return 150
		except Exception as e:
			self.logToConsole( "maxHeight: %s" % str(e) )
	
	def currentHeight( self ):
		"""
		The current height of the Palette section.
		Used for storing the current resized state.
		"""
		try:
			return NSUserDefaults.standardUserDefaults().integerForKey_( "____CFBundleIdentifier____.ViewHeight" )
		except Exception as e:
			self.logToConsole( "currentHeight: %s" % str(e) )
	
	def setCurrentHeight_( self, newHeight ):
		"""
		Sets a new height for the Palette section.
		"""
		try:
			if newHeight >= self.minHeight() and newHeight <= self.maxHeight():
				NSUserDefaults.standardUserDefaults().setInteger_forKey_( newHeight, "____CFBundleIdentifier____.ViewHeight" )
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
				# Do stuff here, e.g. an IBOutlet method like:
				# self._myTextFieldOutlet.setStringValue_( "xxx" )
				pass
		except Exception as e:
			self.logToConsole( "update: %s" % str(e) )

	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Palette plugin %s:\n%s" % ( self.title(), message )
		NSLog( myLog )
