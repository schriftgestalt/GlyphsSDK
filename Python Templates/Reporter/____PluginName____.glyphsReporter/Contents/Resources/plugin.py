#!/usr/bin/env python
# encoding: utf-8


import objc
from Foundation import *
from AppKit import *
import sys, os, re, traceback

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

#import GlyphsApp
from GlyphsApp import *

GlyphsReporterProtocol = objc.protocolNamed( "GlyphsReporter" )

class ReporterPlugin ( NSObject, GlyphsReporterProtocol ):
	
	def init( self ):
		"""
		Put any initializations you want to make here.
		"""
		try:
			#Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ));

			self.lastErrorMessage = ''

			# Default values
			self.menuName = 'New ReporterPlugin'
			self.keyboardShortcut = None
			self.keyboardShortcutModifier = 0 # Set any combination of NSShiftKeyMask | NSControlKeyMask | NSCommandKeyMask | NSAlternateKeyMask
			self.drawDefaultInactiveLayers = True
			self.generalContextMenus = []
			

			if hasattr(self, 'settings'):
				self.settings()

			if hasattr(self, 'start'):
				self.start()

			return self
		except:
			self.logError(traceback.format_exc())
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except:
			self.logError(traceback.format_exc())
	
	def title( self ):
		"""
		This is the name as it appears in the menu in combination with 'Show'.
		E.g. 'return "Nodes"' will make the menu item read "Show Nodes".
		"""
		try:
			return self.menuName or self.__class__.__name__ or 'New ReporterPlugin'
		except:
			self.logError(traceback.format_exc())
	
	def keyEquivalent( self ):
		"""
		The key for the keyboard shortcut. Set modifier keys in modifierMask() further below.
		Pretty tricky to find a shortcut that is not taken yet, so be careful.
		If you are not sure, use 'return None'. Users can set their own shortcuts in System Prefs.
		"""
		try:
			return self.keyboardShortcut or None
		except Exception as e:
			self.logError(traceback.format_exc())
	
	def modifierMask( self ):
		"""
		Use any combination of these to determine the modifier keys for your default shortcut:
			return NSShiftKeyMask | NSControlKeyMask | NSCommandKeyMask | NSAlternateKeyMask
		Or:
			return 0
		... if you do not want to set a shortcut.
		"""
		try:
			return self.keyboardShortcutModifier or 0
		except:
			self.logError(traceback.format_exc())
	
	def drawForegroundForLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed IN FRONT OF the paths.
		Setting a color:
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 1.0, 1.0, 1.0, 1.0 ).set() # sets RGBA values between 0.0 and 1.0
			NSColor.redColor().set() # predefined colors: blackColor, blueColor, brownColor, clearColor, cyanColor, darkGrayColor, grayColor, greenColor, lightGrayColor, magentaColor, orangeColor, purpleColor, redColor, whiteColor, yellowColor
		Drawing a path:
			myPath = NSBezierPath.alloc().init()  # initialize a path object myPath
			myPath.appendBezierPath_( subpath )   # add subpath to myPath
			myPath.fill()   # fill myPath with the current NSColor
			myPath.stroke() # stroke myPath with the current NSColor
		To get an NSBezierPath from a GSPath, use the bezierPath() method:
			myPath.bezierPath().fill()
		You can apply that to a full layer at once:
			if len( myLayer.paths > 0 ):
				myLayer.bezierPath()       # all closed paths
				myLayer.openBezierPath()   # all open paths
		See:
		https://developer.apple.com/library/mac/documentation/Cocoa/Reference/ApplicationKit/Classes/NSBezierPath_Class/Reference/Reference.html
		https://developer.apple.com/library/mac/documentation/cocoa/reference/applicationkit/classes/NSColor_Class/Reference/Reference.html
		"""
		try:
			if hasattr(self, 'drawForeground'):
				self.drawForeground(Layer)
		except:
			self.logError(traceback.format_exc())

	
	def drawBackgroundForLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			if hasattr(self, 'drawBackground'):
				self.drawBackground(Layer)
		except:
			self.logError(traceback.format_exc())
		
	
	def drawBackgroundForInactiveLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed behind the paths, but
		- for inactive glyphs in the EDIT VIEW
		- and for glyphs in the PREVIEW
		Please note: If you are using this method, you probably want
		self.needsExtraMainOutlineDrawingForInactiveLayer_() to return False
		because otherwise Glyphs will draw the main outline on top of it, and
		potentially cover up your background drawing.
		"""

		try:
			assert Glyphs

			if self.controller:
				if hasattr(self, 'drawBackgroundForInactiveLayers'):
					self.drawBackgroundForInactiveLayers(Layer)
				

			else:
				if hasattr(self, 'drawPreview'):
					self.drawPreview(Layer)
				elif hasattr(self, 'drawBackgroundForInactiveLayers'):
					self.drawBackgroundForInactiveLayers(Layer)

		except:
			self.logError(traceback.format_exc())
		
	def logError(self, message):
		try:
			if message != self.lastErrorMessage:
				self.logToConsole(message)
				self.lastErrorMessage = message
#				Glyphs.showNotification('Error in %s' % self.title(), 'Check the Console output for details.')
		except:
			self.logToConsole(traceback.format_exc())
	
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		"""
		Decides whether inactive glyphs in Edit View and glyphs in Preview should be drawn
		by Glyphs (‘the main outline drawing’).
		Return True (or remove the method) to let Glyphs draw the main outline.
		Return False to prevent Glyphs from drawing the glyph (the main outline 
		drawing), which is probably what you want if you are drawing the glyph
		yourself in self.drawBackgroundForInactiveLayer_().
		"""
		try:
			return self.drawDefaultInactiveLayers
		except:
			self.logError(traceback.format_exc())
	
		
	def addMenuItemsForEvent_toMenu_(self, event, contextMenu):
		'''
		The event can tell you where the user had clicked.
		'''
		try:
			
			if self.generalContextMenus:
				for entry in self.generalContextMenus:
					newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(entry[0], entry[1], "")
					newMenuItem.setTarget_(self)
					
					if len(entry) == 3:
						index = int(entry[3])
					else:
						index = 0
						
					if index >= 0:
						contextMenu.insertItem_atIndex_(newMenuItem, index)
					else:
						contextMenu.addItem_(newMenuItem)

			if hasattr(self, 'conditionalContextMenus'):
				contextMenus = self.conditionalContextMenus()
			
				if contextMenus:
					for name, method in contextMenus:
						newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_( name, method, "" )
						newMenuItem.setTarget_( self ) # method of this class will be called
						contextMenu.insertItem_atIndex_( newMenuItem, 0 ) # adds item at the top of the menu

		except:
			self.logError(traceback.format_exc())
	
	def drawTextAtPoint( self, text, textPosition, fontSize=10.0, fontColor=NSColor.blackColor(), align='bottomleft'):
		"""
		Use self.drawTextAtPoint( "blabla", myNSPoint ) to display left-aligned text at myNSPoint.
		"""
		try:

			alignment = {
				'topleft': 6, 
				'topcenter': 7, 
				'topright': 8,
				'left': 3, 
				'center': 4, 
				'right': 5, 
				'bottomleft': 0, 
				'bottomcenter': 1, 
				'bottomright': 2
				}


			glyphEditView = self.controller.graphicView()
			currentZoom = self.getScale()
			fontAttributes = { 
				NSFontAttributeName: NSFont.labelFontOfSize_( fontSize/currentZoom ),
				NSForegroundColorAttributeName: fontColor }
			displayText = NSAttributedString.alloc().initWithString_attributes_( text, fontAttributes )
			textAlignment = alignment[align] # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
			glyphEditView.drawText_atPoint_alignment_( displayText, textPosition, textAlignment )
		except:
			self.logError(traceback.format_exc())
	
	def getHandleSize( self ):
		"""
		Returns the current handle size as set in user preferences.
		Use: self.getHandleSize() / self.getScale()
		to determine the right size for drawing on the canvas.
		"""
		try:
			Selected = NSUserDefaults.standardUserDefaults().integerForKey_( "GSHandleSize" )
			if Selected == 0:
				return 5.0
			elif Selected == 2:
				return 10.0
			else:
				return 7.0 # Regular
		except:
			self.logError(traceback.format_exc())
			return 7.0

	def getScale( self ):
		"""
		self.getScale() returns the current scale factor of the Edit View UI.
		Divide any scalable size by this value in order to keep the same apparent pixel size.
		"""
		try:
			return self.controller.graphicView().scale()
		except:
			self.logError(traceback.format_exc())
			return 1.0
	
	def setController_( self, Controller ):
		"""
		Use self.controller as object for the current view controller.
		"""
		try:
			self.controller = Controller
		except Exception as e:
			self.logToConsole( "Could not set controller" )
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )
