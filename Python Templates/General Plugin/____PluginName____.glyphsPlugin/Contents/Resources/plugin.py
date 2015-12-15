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

GlyphsPluginProtocol = objc.protocolNamed( "GlyphsPlugin" )

class GeneralPlugin ( NSObject, GlyphsPluginProtocol ):
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "%s:\n%s" % ( self.__class__.__name__, message )
		NSLog( myLog )

	def loadPlugin(self):
		if hasattr(self, 'start'):
			self.start()
		return None
