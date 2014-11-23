#!/usr/bin/env python
# encoding: utf-8

import objc, sys
from Foundation import *
from AppKit import *

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp

class ____PluginClassName____ ( GSToolSelect ):
	
	def init( self ):
		"""
		By default, toolbar.pdf will be your tool icon.
		Use this for any initializations you need.
		"""
		try:
			Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ) );
			BundlePath = Bundle.pathForResource_ofType_( "toolbar", "pdf" ) # Set this to the filename and type of your icon.
			self.tool_bar_image = NSImage.alloc().initWithContentsOfFile_( BundlePath )
			self.tool_bar_image.setTemplate_( True ) # Makes the icon blend in with the toolbar.
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
		
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
		The name of the Tool as it appears in the tooltip.
		"""
		try:
			return "____PluginMenuName____"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
		
	def toolBarIcon( self ):
		"""
		Return a instance of NSImage that represents the toolbar icon as established in init().
		Unless you know what you are doing, leave this as it is.
		"""
		try:
			return self.tool_bar_image
		except Exception as e:
			self.logToConsole( "toolBarIcon: %s" % str(e) )
		
	def groupID( self ):
		"""
		Determines the position in the toolbar.
		Higher values are further to the right.
		"""
		try:
			return 100
		except Exception as e:
			self.logToConsole( "groupID: %s" % str(e) )
		
 	def trigger( self ):
		"""
		The key to select the tool with keyboard (like v for the select tool).
		Either use trigger() or keyEquivalent(), not both. Remove the method(s) you do not use.
		"""
		try:
			return "x"
		except Exception as e:
			self.logToConsole( "trigger: %s" % str(e) )
		
	def willSelectTempTool_( self, TempTool ):
		"""
		Temporary Tool when user presses Cmd key.
		Should always be GlyphsToolSelect unless you have a better idea.
		"""
		try:
			return TempTool.__class__.__name__ != "GlyphsToolSelect"
		except Exception as e:
			self.logToConsole( "willSelectTempTool_: %s" % str(e) )
		
	def willActivate( self ):
		"""
		Do stuff when the tool is selected.
		E.g. show a window, or set a cursor.
		"""
		try:
			super( ____PluginClassName____, self ).willActivate()
		except Exception as e:
			self.logToConsole( "willActivate: %s" % str(e) )
		
	def willDeactivate( self ):
		"""
		Do stuff when the tool is deselected.
		"""
		try:
			super( ____PluginClassName____, self ).willDeactivate()
		except Exception as e:
			self.logToConsole( "willDeactivate: %s" % str(e) )
		
	def elementAtPoint_atLayer_( currentPoint, activeLayer ):
		"""
		Return an element in the vicinity of currentPoint (NSPoint), and it will be captured by the tool.
		Use Boolean ...
			distance( currentPoint, referencePoint ) < clickTolerance / Scale )
		... for determining whether the NSPoint referencePoint is captured or not.
		Use:
			myPath.nearestPointOnPath_pathTime_( currentPoint, 0.0 )
		
		"""
		try:
			Scale = self.editViewController().graphicView().scale()
			clickTolerance = 4.0
		except Exception as e:
			self.logToConsole( "elementAtPoint_atLayer_: %s" % str(e) )
		
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "%s tool:\n%s" % ( self.title(), message )
		NSLog( myLog )
