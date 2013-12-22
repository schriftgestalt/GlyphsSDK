#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *

class ____PluginClassName____ (GSToolSelect):
	def init(self):
		Bundle = NSBundle.bundleForClass_(NSClassFromString(self.className()));
		BundlePath = Bundle.pathForResource_ofType_("toolbar", "pdf")
		self.tool_bar_image = NSImage.alloc().initWithContentsOfFile_( BundlePath )		

		return self
	
	def title(self):
		return "____PluginMenuName____"
	
	def interfaceVersion(self):
		return 1
	
	def groupID(self):
		'''determines the position in the toolbar '''
		return 100

	def keyEquivalent(self):
		return "k"
	
 	def trigger(self):
		'''The key to select the tool with keyboard'''
		# TODO: check if trigger or keyEquivalent is used; remove the other method
		return "x"
	
	def toolBarIcon(self):
		'''return a instance of NSImage that represents the tool bar icon'''
		return self.tool_bar_image
	
	def willSelectTempTool_(self, TempTool):
		return TempTool.__class__.__name__ != "GlyphsToolSelect" # to prevent switching back to the regualat select tool when pressing cmd
	
	def willActivate(self):
		'''do stuff when the plugin is activated
		e.g. show a window or set a cursor.
		'''
		super(GlyphsExpandPathsPreviewTool, self).willActivate()
	
	def willDeactivate(self):
		super(GlyphsExpandPathsPreviewTool, self).willDeactivate()
		
	def drawBackgroundForLayer_(self, Layer):
		Path = Layer.bezierPath()
		try:
			FontMaster = Layer.font().masters[Layer.associatedMasterId]
			Offset = _fontMaster.userData()["GSOffsetHorizontal"].floatValue()
		except:
			Offset = 10
		
		if Offset > 0:
			Path.setLineWidth_(Offset*2)
			NSColor.grayColor().set()
			Path.stroke()

#TODO add all possible draw methods (Tool Draw delegate protocol)

	
	# def _drawLayer_atPoint_asActive_attributes_(self, Layer, aPoint, Active, Attributes): #GSLayer, NSPoint, BOOL, NSDictionary,
	# 	'''This method is called every time the view needs a redraw. This happens a lot, so try to cache some slow calculations
	# 	There is no easy way to determine if the content of the layer has changed. 
	# 	For now save the output of:
	# 		str(Layer.bezierPath())
	# 	and compare in the next run.
	# 	'''
	# 	
	# 	self.scale = 1
	# 	
	# 
	# 	
	# 	'''This will call the parent classes implementation. In this case it draws the outline, the nodes and the metrics If you want to draw your own outline, you can skip this.'''
	# 	super(GlyphsAppSpeedPunkTool, self).drawLayer_atPoint_asActive_attributes_(Layer, aPoint, Active, Attributes)
		
