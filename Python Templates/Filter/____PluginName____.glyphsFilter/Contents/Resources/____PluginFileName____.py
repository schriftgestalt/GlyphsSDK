#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

#GlyphsFileFormatProtocol = objc.protocolNamed( "GlyphsFileFormat" )

class ____PluginClassName____ ( GSFilterPlugin ):
	
	firstValueField = objc.IBOutlet()
	
	def init( self ):
		"""
		Do all initializing here.
		"""
		NSBundle.loadNibNamed_owner_("____PluginFileName____Dialog", self)
		#Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ));
		return self
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		return 1
	
	def title( self ):
		"""
		This is the human-readable name as it appears in the menu.
		"""
		return "____PluginMenuName____"
	
	def actionName( self ):
		"""
		This is the title of the button in the settings dialog.
		"""
		return "____PluginActionName____"
	
	def keyEquivalent( self ):
		""" 
		The key together with Cmd+Shift will be the shortcut for the filter.
		Return None if you do not want to set a shortcut.
		Users can set their own shortcuts in System Prefs.
		"""
		return None
	
	def setup(self):
		super(____PluginClassName____, self).setup()
		FontMaster = self.valueForKey_("fontMaster")
		if "____TheFirstValue____" in FontMaster.userData:
			self.firstValue = FontMaster.userData["____TheFirstValue____"].floatValue()
		
		else:
			self.firstValue = 15 # set default value.
		
		self.firstValueField.setFloatValue_(self.firstValue)
		return None # or if somthing goes wrong, a NSError object with details
	
	@objc.IBAction
	def setFirstValue_(self ,sender):
		"""
		This is only an example for a setter method.
		Add methods like this for each option in the dialog.
		"""
		FirstValue = sender.floatValue()
		if FirstValue != self.firstValue:
			self.firstValue = FirstValue
			self.process_(None)
	
	def processLayerWithFirstValue(self, Layer, FirstValue):
		# the method should contain all parameters as arguments
	
		# do stuff with the Layer.
		pass
	
	def processFont_withArguments_(self, Font, Arguments):
		"""
		Invoked when called as Custom Parameter in an instance at export.
		The Arguments come from the custom parameter in the instance settings. 
		The first item in Arguments is the class-name. After that, it depends on the filter.
		"""
		FirstValue = 0
		if len(Arguments) > 1:
			FirstValue = Arguments[1].floatValue()
		
		checkSelection = False
		FontMasterId = Font.fontMasterAtIndex_(0).id
		for Glyph in Font.glyphs():
			Layer = Glyph.layerForKey_(FontMasterId)
			self.processLayerWithFirstValue(Layer, FirstValue)
	
	def process_(self, sender):
		try:
			ShadowLayers = self.valueForKey_("shadowLayers")
			Layers = self.valueForKey_("layers")
			for k in range(len(ShadowLayers)):
				ShadowLayer = ShadowLayers[k]
				Layer = Layers[k]
				Layer.setPaths_(NSMutableArray.alloc().initWithArray_copyItems_(ShadowLayer.pyobjc_instanceMethods.paths(), True))
				Layer.setSelection_(NSMutableArray.array())
				if len(ShadowLayer.selection()) > 0 and checkSelection:
					for i in range(len(ShadowLayer.paths)):
						currShadowPath = ShadowLayer.paths[i]
						currLayerPath = Layer.paths[i]
						for j in range(len(currShadowPath.nodes)):
							currShadowNode = currShadowPath.nodes[j]
							if ShadowLayer.selection.containsObject_(currShadowNode):
								Layer.addSelection_(currLayerPath.nodes[j])
				self.processLayerWithFirstValue(Layer, self.firstValue)
				Layer.clearSelection()
		
			# Safe the value in the FontMaster. But could be saved in UserDefaults, too.
			#_fontMaster = [Font fontMasterForId:Layer.associatedMasterId];
			FontMaster = self.valueForKey_("fontMaster")
			FontMaster.userData["____TheFirstValue____"] = NSNumber.numberWithDouble_(self.firstValue)
			super(____PluginClassName____, self).process_(sender)
		except Exception as e:
			self.logToConsole( str(e) )
			
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Filter %s:\n%s" % (self.title(), message )
		NSLog( myLog )
