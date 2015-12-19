# encoding: utf-8

import objc, sys, os, traceback
from Foundation import *
from AppKit import *

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp
from GlyphsApp import *

class SelectTool ( GSToolSelect ):
	
	def init( self ):
		"""
		By default, toolbar.pdf will be your tool icon.
		Use this for any initializations you need.
		"""
		try:
			self.name = 'My Select Tool'
			self.toolbarPosition = 100
			self._icon = 'toolbar.pdf'
			self.keyboardShortcut = None
			self.generalContextMenus = ()
			
			if hasattr(self, 'settings'):
				self.settings()
			
			Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ) );
			BundlePath = Bundle.pathForResource_ofType_( os.path.splitext(self._icon)[0], os.path.splitext(self._icon)[1] ) # Set this to the filename and type of your icon.
			self.tool_bar_image = NSImage.alloc().initWithContentsOfFile_( BundlePath )
			self.tool_bar_image.setTemplate_( True ) # Makes the icon blend in with the toolbar.

			if hasattr(self, 'start'):
				self.start()

			return self
		except:
			self.logToConsole(traceback.format_exc())
		
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except:
			self.logToConsole(traceback.format_exc())

	def title( self ):
		"""
		The name of the Tool as it appears in the tooltip.
		"""
		try:
			return self.name
		except:
			self.logToConsole(traceback.format_exc())
		
	def toolBarIcon( self ):
		"""
		Return a instance of NSImage that represents the toolbar icon as established in init().
		Unless you know what you are doing, leave this as it is.
		"""
		try:
			return self.tool_bar_image
		except:
			self.logToConsole(traceback.format_exc())
		
	def groupID( self ):
		"""
		Determines the position in the toolbar.
		Higher values are further to the right.
		"""
		try:
			return self.toolbarPosition
		except:
			self.logToConsole(traceback.format_exc())
		
 	def trigger( self ):
		"""
		The key to select the tool with keyboard (like v for the select tool).
		Either use trigger() or keyEquivalent(), not both. Remove the method(s) you do not use.
		"""
		try:
			return self.keyboardShortcut
		except:
			self.logToConsole(traceback.format_exc())
		
	def willSelectTempTool_( self, TempTool ):
		"""
		Temporary Tool when user presses Cmd key.
		Should always be GlyphsToolSelect unless you have a better idea.
		"""
		try:
			return TempTool.__class__.__name__ != "GlyphsToolSelect"
		except:
			self.logToConsole(traceback.format_exc())
		
	def willActivate( self ):
		"""
		Do stuff when the tool is selected.
		E.g. show a window, or set a cursor.
		"""
		try:
			super( SelectTool, self ).willActivate()
			if hasattr(self, 'activate'):
				self.activate()
		except:
			self.logToConsole(traceback.format_exc())
		
	def willDeactivate( self ):
		"""
		Do stuff when the tool is deselected.
		"""
		try:
			super( SelectTool, self ).willDeactivate()
			if hasattr(self, 'deactivate'):
				self.deactivate()
		except:
			self.logToConsole(traceback.format_exc())
		
	def elementAtPoint_atLayer_( self, currentPoint, activeLayer ):
		"""
		Return an element in the vicinity of currentPoint (NSPoint), and it will be captured by the tool.
		Use Boolean ...
			distance( currentPoint, referencePoint ) < clickTolerance / Scale )
		... for determining whether the NSPoint referencePoint is captured or not.
		Use:
			myPath.nearestPointOnPath_pathTime_( currentPoint, 0.0 )
		
		"""
		return super(SelectTool, self).elementAtPoint_atLayer_(currentPoint, activeLayer)

		try:
			Scale = self.editViewController().graphicView().scale()
			clickTolerance = 4.0

			for p in activeLayer.paths:
				for n in p.nodes:
					if distance( currentPoint, n.position ) < clickTolerance / Scale:
						return n

			for a in activeLayer.anchors:
				if distance( currentPoint, a.position ) < clickTolerance / Scale:
					return a
			
		except:
			self.logToConsole(traceback.format_exc())
	
	# The following four methods are optional, and only necessary
	# if you intend to extend the context menu with extra items.
	# Remove them if you do not want to change the context menu:
	
	def defaultContextMenu( self ):
		"""
		Sets the default content of the context menu and returns the menu.
		Add menu items that do not depend on the context,
		e.g., actions that affect the whole layer, no matter what is selected.
		Remove this method if you do not want any extra context menu items.
		"""
		try:
			# Get the current default context menu:
			theMenu = super(SelectTool, self).defaultContextMenu()
			
			# Add separator at the bottom:
			newSeparator = NSMenuItem.separatorItem()
			theMenu.addItem_( newSeparator )
			
			# Add menu items at the bottom:
			for name, method in self.generalContextMenus:
				theMenu.addItemWithTitle_action_keyEquivalent_(name, method, "" )
			
			return theMenu
		except:
			self.logToConsole(traceback.format_exc())
			
	def addMenuItemsForEvent_toMenu_( self, theEvent, theMenu ):
		"""
		Adds menu items to default context menu.
		Remove this method if you do not want any extra context menu items.
		"""
		try:
			
			if hasattr(self, 'conditionalContextMenus'):
				contextMenus = self.conditionalContextMenus()
			
				if contextMenus:
					for name, method in contextMenus:
						newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_( name, method, "" )
						newMenuItem.setTarget_( self ) # method of this class will be called
						theMenu.insertItem_atIndex_( newMenuItem, 0 ) # adds item at the top of the menu
					
					newSeparator = NSMenuItem.separatorItem()
					theMenu.insertItem_atIndex_( newSeparator, 1 )
								
		except:
			self.logToConsole(traceback.format_exc())
	
		
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "%s tool:\n%s" % ( self.title(), message )
		NSLog( myLog )