#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

GlyphsPluginProtocol = objc.protocolNamed( "GlyphsPlugin" )

class ____PluginClassName____ ( NSObject, GlyphsPluginProtocol ):
	
	def init( self ):
		"""
		Unless you know what you are doing, leave this as it is.
		"""
		#Bundle = NSBundle.bundleForClass_(NSClassFromString(self.className()));
		selector = objc.selector( self.advertise, signature="v@:@" )
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, selector, "GSDocumentWasSavedSuccessfully", objc.nil() )
		#print self.title(), "init"
		return self
	
	def __del__( self ):
		"""
		Unless you know what you are doing, leave this as it is.
		"""
		NSNotificationCenter.defaultCenter().removeObserver_( self )
	
	def title( self ):
		"""
		The Title of your Plugin as it appears in in the app menu.
		"""
		return "____PluginMenuName____"
		
	def interfaceVersion( self ):
		"""
		Must return 1.
		"""
		return 1
	
	def documentWasSaved( self, sender ):
		self.logToConsole( "The document: %@ was saved" % sender.object().displayName() )

	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "%s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )
	