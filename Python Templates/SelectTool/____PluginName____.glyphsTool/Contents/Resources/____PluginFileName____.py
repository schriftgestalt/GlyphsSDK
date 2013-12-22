#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *

class ____PluginClassName____ ( GSToolSelect ):
	
	def init( self ):
		"""
		Unless you know what you are doing, leave this as it is.
		"""
		Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ) );
		BundlePath = Bundle.pathForResource_ofType_( "toolbar", "pdf" )
		self.tool_bar_image = NSImage.alloc().initWithContentsOfFile_( BundlePath )		
		return self
		
	def toolBarIcon( self ):
		"""
		Unless you know what you are doing, leave this as it is.
		Return a instance of NSImage that represents the toolbar icon as established in init().
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
		
	def keyEquivalent( self ):
		"""
		The key for the keyboard shortcut.
		Pretty tricky to find a shortcut that is not taken yet, so be careful.
		If you are not sure, use 'return None'. Users can set their own shortcuts in System Prefs.
		"""
		return "k"
		
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
		super( GlyphsExpandPathsPreviewTool, self ).willActivate()
		
	def willDeactivate( self ):
		"""
		Do stuff when the tool is deselected.
		"""
		super( GlyphsExpandPathsPreviewTool, self ).willDeactivate()
		
	def drawBackgroundForLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed IN FRONT OF the paths while the tool is active.
		Use drawForegroundForLayer_() if you want to draw in front of the paths instead.
		"""
		try:
			try:
				FontMaster = Layer.font().masters[ Layer.associatedMasterId ]
				Offset = _fontMaster.userData()[ "GSOffsetHorizontal" ].floatValue()
			except:
				Offset = 10
				
			Path = Layer.bezierPath()
			if Offset > 0:
				Path.setLineWidth_(Offset*2)
				NSColor.grayColor().set()
				Path.stroke()
		except Exception as e:
			self.logToConsole( str(e) )

# TODO add all possible draw methods (Tool Draw delegate protocol)
#
#	
#	def _drawLayer_atPoint_asActive_attributes_( self, Layer, aPoint, Active, Attributes ): # GSLayer, NSPoint, BOOL, NSDictionary,
#
#		"""
#		This method is called every time the view needs a redraw.
#		This happens a lot, so try to cache some slow calculations.
#		There is no easy way to determine if the content of the layer has changed. 
#		For now, save the output of:
#			str( Layer.bezierPath() )
#		and compare in the next run.
#		"""
#		self.scale = 1
#
#		"""
#		This will call the parent classes implementation.
#		In this case it draws the outline, the nodes and the metrics.
#		If you want to draw your own outline, you can skip this.
#		"""
#		super( GlyphsAppSpeedPunkTool, self ).drawLayer_atPoint_asActive_attributes_( Layer, aPoint, Active, Attributes )
#		
#