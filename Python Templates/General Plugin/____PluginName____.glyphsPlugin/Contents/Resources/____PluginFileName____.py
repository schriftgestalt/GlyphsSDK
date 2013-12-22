#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

GlyphsPluginProtocol = objc.protocolNamed('GlyphsPlugin')

class ____PluginClassName____ (NSObject, GlyphsPluginProtocol):
	
	def init(self):
		#Bundle = NSBundle.bundleForClass_(NSClassFromString(self.className()));
		selector = objc.selector(self.advertise, signature='v@:@')
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(self, selector, "GSDocumentWasSavedSuccessfully", objc.nil())
		
		print self.title(), 'init'
		return self
	
	def __del__(delf):
		NSNotificationCenter.defaultCenter().removeObserver_(self)
	
	def title(self):
		return "____PluginMenuName____"
		
	def interfaceVersion(self):
		return 1
	
	def documentWasSaved(self, sender):
		print "the document: %@ was saved" % sender.object().displayName()