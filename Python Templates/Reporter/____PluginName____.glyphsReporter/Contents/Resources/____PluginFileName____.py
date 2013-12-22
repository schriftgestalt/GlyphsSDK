#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

GlyphsReporterProtocol = objc.protocolNamed('GlyphsReporter')

class ____PluginClassName____ (NSObject, GlyphsReporterProtocol):
	
	def init(self):
		#Bundle = NSBundle.bundleForClass_(NSClassFromString(self.className()));
		return self
	
	def title(self):
		return "____PluginMenuName____"
	
	def interfaceVersion(self):
		return 1
	
	def keyEquivalent(self):
		# Choose the keyboard chortcut
		# Please check if the shortcut is not used elsewhere in the app
		return "y"
	
	def modifierMask(self):
		# return the combination of NSCommandKeyMask ...
		return 0
	
	def drawBackgroundForLayer_(self, Layer):
		#TODO add comment about the scaling and positioning. See the calling methods in YLLayoutManager.m
		Rect = Layer.bounds
		NSColor.blueColor().set()
		NSBezierPath.fillRect_(Rect)
		
	def drawForgroundForLayer_(self, Layer):
		pass
	
	def drawBackgroundForInactiveLayer_(self, Layer):
		pass
	
	def setController_(self, Controller):
		# property accessor
		self.controller = Controller
