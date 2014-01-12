#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *

class ____PluginClassName____ ( GSToolSelect ):
	
	def init( self ):
		"""
		By default, toolbar.pdf will be your tool icon.
		Unless you know what you are doing, leave this as it is.
		"""
		Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ) );
		BundlePath = Bundle.pathForResource_ofType_( "toolbar", "pdf" )
		self.tool_bar_image = NSImage.alloc().initWithContentsOfFile_( BundlePath )		
		return self
		
	def toolBarIcon( self ):
		"""
		Return a instance of NSImage that represents the toolbar icon as established in init().
		Unless you know what you are doing, leave this as it is.
		"""
		return self.tool_bar_image
		
	def title( self ):
		"""
		The name of the Tool.
		"""
		return "____PluginMenuName____"
		
	def interfaceVersion( self ):
		"""
		Must return 1.
		"""
		return 1
		
	def groupID( self ):
		"""
		Determines the position in the toolbar.
		"""
		return 100
		
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "%s tool:\n%s" % ( self.title(), message )
		NSLog( myLog )
		
 	def trigger( self ):
		"""
		The key to select the tool with keyboard (like v for the select tool).
		Either use trigger() or keyEquivalent(), not both. Remove the method(s) you do not use.
		"""
		return "x"
		
	def willSelectTempTool_( self, TempTool ):
		"""
		Temporary Tool when user presses Cmd key.
		Should always be GlyphsToolSelect unless you have a better idea.
		"""
		return TempTool.__class__.__name__ != "GlyphsToolSelect"
		
	def willActivate( self ):
		"""
		Do stuff when the tool is selected.
		E.g. show a window, or set a cursor.
		"""
		super( ____PluginClassName____, self ).willActivate()
		
	def willDeactivate( self ):
		"""
		Do stuff when the tool is deselected.
		"""
		super( ____PluginClassName____, self ).willDeactivate()
		
	def drawBackgroundForLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed behind the paths while the tool is active.
		Use drawForegroundForLayer_() if you want to draw in front of the paths instead.
		"""
		try:
			Offset = 10
			NSColor.grayColor().set()
			Path = Layer.bezierPath()
			Path.setLineWidth_( Offset * 2 )
			Path.stroke()
		except Exception as e:
			self.logToConsole( str(e) )
