#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp

GlyphsFilterProtocol = objc.protocolNamed( "GlyphsFilter" )

class FilterWithoutDialog ( NSObject, GlyphsFilterProtocol ):

	def init( self ):
		"""
		Do all initializing here.
		"""
		try:


			self.menuName = 'My Filter'
			self.keyboardShortcut = None

			if hasattr(self, 'settings'):
				self.settings()

			if hasattr(self, 'loadPlugin'):
				self.loadPlugin()

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
			return self.menuName
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
			return self.keyboardShortcut
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	
	# deprecated --> filter() in user code
	def __processLayer( self, Layer, selectionCounts ): 
		"""
		Each layer is eventually processed here. This is where your code goes.
		If selectionCounts is True, then apply the code only to the selection.
		"""
		try:
			if selectionCounts == True:
				selection = ()
				try:
					selection = Layer.selection() # Glyphs v2.1 and earlier
				except:
					selection = Layer.selection # Glyphs v2.2 and later
				if selection == (): # empty selection
					selectionCounts = False
			
			# Do stuff here.
			
			return (True, None)
		except Exception as e:
			self.logToConsole( "processLayer: %s" % str(e) )
			return (False, None)
	
	def runFilterWithLayers_error_( self, Layers, Error ):
		"""
		Invoked when user triggers the filter through the Filter menu
		and more than one layer is selected.
		"""
		try:
#			print Layers
			for Layer in Layers:
#				Layer = Layers[k]
#				Layer.clearSelection()
				
				if hasattr(self, 'filter'):
					self.filter( Layer, False, {} )
					
			return (True, None)
		except Exception as e:
			self.logToConsole( "runFilterWithLayers_error_: %s" % str(e) )
	
	def runFilterWithLayer_options_error_( self, Layer, Options, Error ):
		"""
		Required for compatibility with Glyphs version 702 or later.
		Leave this as it is.
		"""
		try:
			return self.runFilterWithLayer_error_( self, Layer, Error )
		except Exception as e:
			self.logToConsole( "runFilterWithLayer_options_error_: %s" % str(e) )
			
	def runFilterWithLayer_error_( self, Layer, Error ):
		"""
		Invoked when user triggers the filter through the Filter menu
		and only one layer is selected.
		"""
		try:
			if hasattr(self, 'filter'):
				self.filter( Layer, True, {} )
			return (True, None)
		except Exception as e:
			self.logToConsole( "runFilterWithLayer_error_: %s" % str(e) )
			return (False, None)
	
	def processFont_withArguments_( self, Font, Arguments ):
		"""
		Invoked when called as Custom Parameter in an instance at export.
		The Arguments come from the custom parameter in the instance settings. 
		Item 0 in Arguments is the class-name. The consecutive items should be your filter options.
		"""
		try:
			# set glyphList to all glyphs
			glyphList = Font.glyphs
			
#			print Arguments
			
			# customParameters delivered to filter()
			customParameters = {}
			unnamedCustomParameterCount = 0
			for i in range(1, len(Arguments)):
				if not 'include' in Arguments[i] and not 'exclude' in Arguments[i]:

					# if key:value pair
					if ':' in Arguments[i]:
						key, value = Arguments[i].split(':')
					# only value given, no key. make key name
					else:
						key = unnamedCustomParameterCount
						unnamedCustomParameterCount += 1
						value = Arguments[i]
					
					# attempt conversion to float value
					try:
						customParameters[key] = float(value)
					except:
						customParameters[key] = value
			
			
			
			# change glyphList to include or exclude glyphs
			if len( Arguments ) > 1:
				if "exclude:" in Arguments[-1]:
					excludeList = [ n.strip() for n in Arguments.pop(-1).replace("exclude:","").strip().split(",") ]
					glyphList = [ g for g in glyphList if not g.name in excludeList ]
				elif "include:" in Arguments[-1]:
					includeList = [ n.strip() for n in Arguments.pop(-1).replace("include:","").strip().split(",") ]
					glyphList = [ Font.glyphs[n] for n in includeList ]
			
			FontMasterId = Font.fontMasterAtIndex_(0).id
			for thisGlyph in glyphList:
				Layer = thisGlyph.layerForKey_( FontMasterId )

				if hasattr(self, 'filter'):
					self.filter( Layer, False, customParameters )
		except Exception as e:
			self.logToConsole( "processFont_withArguments_: %s" % str(e) )
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Filter %s:\n%s" % ( self.title(), message )
		NSLog( myLog )
