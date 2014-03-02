#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

GlyphsFilterProtocol = objc.protocolNamed( "GlyphsFilter" )

class ____PluginClassName____ ( NSObject, GlyphsFilterProtocol ):

	def init( self ):
		"""
		Do all initializing here.
		"""
		return self
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		return 1
	
	def setController_( self, Controller ):
		"""
		Do not touch this.
		"""
		try:
			self._controller = Controller
		except Exception as e:
			self.logToConsole( "setController_: %s" % str(e) )
	
	def controller( self ):
		"""
		Do not touch this.
		"""
		try:
			return self._controller
		except Exception as e:
			self.logToConsole( "controller: %s" % str(e) )
		
	def setup( self ):
		"""
		Do not touch this.
		"""
		try:
			return None
		except Exception as e:
			self.logToConsole( "setup: %s" % str(e) )
	
	def title( self ):
		"""
		This is the human-readable name as it appears in the Filter menu.
		"""
		return "____PluginMenuName____"
	
	def keyEquivalent( self ):
		""" 
		The key together with Cmd+Shift will be the shortcut for the filter.
		Return None if you do not want to set a shortcut.
		Users can set their own shortcuts in System Prefs.
		"""
		return None
	
	def runFilterWithLayers_error_( self, Layers, Error ):
		"""
		Invoked when user triggers the filter through the Filter menu
		and more than one layer is selected.
		"""
		try:
			for k in range(len(Layers)):
				Layer = Layers[k]
				Layer.clearSelection()
				self.processLayer( Layer, False )
		except Exception as e:
			self.logToConsole( "runFilterWithLayers_error_: %s" % str(e) )
			
	def runFilterWithLayer_error_( self, Layer, Error ):
		"""
		Invoked when user triggers the filter through the Filter menu
		and only one layer is selected.
		"""
		try:
			return self.processLayer( Layer, True )
		except Exception as e:
			self.logToConsole( "runFilterWithLayer_error_: %s" % str(e) )
	
	def processFont_withArguments_( self, Font, Arguments ):
		"""
		Invoked when called as Custom Parameter in an instance at export.
		The Arguments come from the custom parameter in the instance settings. 
		The first item in Arguments is the class-name. After that, it depends on the filter.
		"""
		try:
			FontMasterId = Font.fontMasterAtIndex_(0).id
			for thisGlyph in Font.glyphs:
				Layer = thisGlyph.layerForKey_( FontMasterId )
				self.processLayer( Layer, False )
		except Exception as e:
			self.logToConsole( "processFont_withArguments_: %s" % str(e) )
	
	def processLayer( self, Layer, selectionCounts ):
		"""
		Each layer is processed here.
		Put your code here.
		"""
		try:
			selection = Layer.selection()
			if selection == (): # empty selection
				selectionCounts = False
			
			# Do stuff here.
			
			return True
		except Exception as e:
			self.logToConsole( "processLayer: %s" % str(e) )
			return False
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Filter %s:\n%s" % (self.title(), message )
		NSLog( myLog )
