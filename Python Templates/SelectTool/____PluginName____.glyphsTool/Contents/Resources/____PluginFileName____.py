#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *

class ____PluginClassName____ ( GSToolSelect ):
	
	def init( self ):
		"""
		By default, toolbar.pdf will be your tool icon.
		Use this for any initializations you need.
		"""
		Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ) );
		BundlePath = Bundle.pathForResource_ofType_( "toolbar", "pdf" ) # Set this to the filename and type of your icon.
		self.tool_bar_image = NSImage.alloc().initWithContentsOfFile_( BundlePath )
		self.tool_bar_image.setTemplate_( True ) # Makes the icon blend in with the toolbar.
		return self
		
	def toolBarIcon( self ):
		"""
		Return a instance of NSImage that represents the toolbar icon as established in init().
		Unless you know what you are doing, leave this as it is.
		"""
		return self.tool_bar_image
		
	def title( self ):
		"""
		The name of the Tool as it appears in the tooltip.
		"""
		return "____PluginMenuName____"
		
	def interfaceVersion( self ):
		"""
		API version, must return 1.
		"""
		return 1
		
	def groupID( self ):
		"""
		Determines the position in the toolbar.
		Higher values are further to the right.
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
		
	def elementAtPoint_atLayer_( currentPoint, activeLayer ):
		"""
		Return an element in the vicinity of currentPoint (NSPoint), and it will be captured by the tool.
		Use Boolean ...
			distance( currentPoint, referencePoint ) < clickTolerance / Scale )
		... for determining whether the NSPoint referencePoint is captured or not.
		Use:
			myPath.nearestPointOnPath_pathTime_( currentPoint, 0.0 )
		
		"""
		Scale = self.editViewController().graphicView().scale()
		clickTolerance = 4.0
	pass
