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
		try:
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
		This is the human-readable name as it appears in the Filter menu.
		"""
		try:
			return "____PluginMenuName____"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def setController_( self, Controller ):
		"""
		Sets the controller, you can access it with controller().
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
	
	def keyEquivalent( self ):
		""" 
		The key together with Cmd+Shift will be the shortcut for the filter.
		Return None if you do not want to set a shortcut.
		Users can set their own shortcuts in System Prefs.
		"""
		try:
			return None
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	
	def processLayer( self, Layer, selectionCounts ):
		"""
		Each layer is eventually processed here. This is where your code goes.
		If selectionCounts is True, then apply the code only to the selection.
		"""
		try:
			if selectionCounts == True:
				selection = Layer.selection()
				if selection == (): # empty selection
					selectionCounts = False
			
			# Do stuff here.
			
			return True
		except Exception as e:
			self.logToConsole( "processLayer: %s" % str(e) )
			return False
	
	def runFilterWithLayers_error_( self, Layers, Error ):
		"""
		Invoked when user triggers the filter through the Filter menu
		and more than one layer is selected.
		"""
		try:
			for k in range(len(Layers)):
				Layer = Layers[k]
				Layer.clearSelection()
				self.processLayer( Layer, False ) # ignore selection
		except Exception as e:
			self.logToConsole( "runFilterWithLayers_error_: %s" % str(e) )
			
	def runFilterWithLayer_error_( self, Layer, Error ):
		"""
		Invoked when user triggers the filter through the Filter menu
		and only one layer is selected.
		"""
		try:
			return self.processLayer( Layer, True ) # respect selection
		except Exception as e:
			self.logToConsole( "runFilterWithLayer_error_: %s" % str(e) )
			return False
	
	def processFont_withArguments_( self, Font, Arguments ):
		"""
		Invoked when called as Custom Parameter in an instance at export.
		The Arguments come from the custom parameter in the instance settings. 
		Item 0 in Arguments is the class-name. The consecutive items should be your filter options.
		"""
		try:
			FontMasterId = Font.fontMasterAtIndex_(0).id
			for thisGlyph in Font.glyphs:
				Layer = thisGlyph.layerForKey_( FontMasterId )
				self.processLayer( Layer, False )
		except Exception as e:
			self.logToConsole( "processFont_withArguments_: %s" % str(e) )
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Filter %s:\n%s" % ( self.title(), message )
		NSLog( myLog )
