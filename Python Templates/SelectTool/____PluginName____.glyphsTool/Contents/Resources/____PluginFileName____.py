#!/usr/bin/env python
# encoding: utf-8

import objc, sys
from Foundation import *
from AppKit import *

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp

class ____PluginClassName____ ( GSToolSelect ):
	
	def init( self ):
		"""
		By default, toolbar.pdf will be your tool icon.
		Use this for any initializations you need.
		"""
		try:
			Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ) );
			BundlePath = Bundle.pathForResource_ofType_( "toolbar", "pdf" ) # Set this to the filename and type of your icon.
			self.tool_bar_image = NSImage.alloc().initWithContentsOfFile_( BundlePath )
			self.tool_bar_image.setTemplate_( True ) # Makes the icon blend in with the toolbar.
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
		The name of the Tool as it appears in the tooltip.
		"""
		try:
			return "____PluginMenuName____"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
		
	def toolBarIcon( self ):
		"""
		Return a instance of NSImage that represents the toolbar icon as established in init().
		Unless you know what you are doing, leave this as it is.
		"""
		try:
			return self.tool_bar_image
		except Exception as e:
			self.logToConsole( "toolBarIcon: %s" % str(e) )
		
	def groupID( self ):
		"""
		Determines the position in the toolbar.
		Higher values are further to the right.
		"""
		try:
			return 100
		except Exception as e:
			self.logToConsole( "groupID: %s" % str(e) )
		
 	def trigger( self ):
		"""
		The key to select the tool with keyboard (like v for the select tool).
		Either use trigger() or keyEquivalent(), not both. Remove the method(s) you do not use.
		"""
		try:
			return "x"
		except Exception as e:
			self.logToConsole( "trigger: %s" % str(e) )
		
	def willSelectTempTool_( self, TempTool ):
		"""
		Temporary Tool when user presses Cmd key.
		Should always be GlyphsToolSelect unless you have a better idea.
		"""
		try:
			return TempTool.__class__.__name__ != "GlyphsToolSelect"
		except Exception as e:
			self.logToConsole( "willSelectTempTool_: %s" % str(e) )
		
	def willActivate( self ):
		"""
		Do stuff when the tool is selected.
		E.g. show a window, or set a cursor.
		"""
		try:
			super( ____PluginClassName____, self ).willActivate()
		except Exception as e:
			self.logToConsole( "willActivate: %s" % str(e) )
		
	def willDeactivate( self ):
		"""
		Do stuff when the tool is deselected.
		"""
		try:
			super( ____PluginClassName____, self ).willDeactivate()
		except Exception as e:
			self.logToConsole( "willDeactivate: %s" % str(e) )
		
	def elementAtPoint_atLayer_( self, currentPoint, activeLayer ):
		"""
		Return an element in the vicinity of currentPoint (NSPoint), and it will be captured by the tool.
		Use Boolean ...
			distance( currentPoint, referencePoint ) < clickTolerance / Scale )
		... for determining whether the NSPoint referencePoint is captured or not.
		Use:
			myPath.nearestPointOnPath_pathTime_( currentPoint, 0.0 )
		
		"""
		try:
			Scale = self.editViewController().graphicView().scale()
			clickTolerance = 4.0
		except Exception as e:
			self.logToConsole( "elementAtPoint_atLayer_: %s" % str(e) )
	
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
			theMenu = super(SelectAnchors, self).defaultContextMenu()
			
			# Add separator at the bottom:
			newSeparator = NSMenuItem.separatorItem()
			theMenu.addItem_( newSeparator )
			
			# Add menu items at the bottom:
			actionMethod = self.genericLayerAction # Class method invoked by the menu item
			theMenu.addItemWithTitle_action_keyEquivalent_( "Layer info in Macro Window", actionMethod, "" )
			
			return theMenu
		except Exception as e:
			self.logToConsole( "defaultContextMenu: %s" % str(e) )
			
	def addMenuItemsForEvent_toMenu_( self, theEvent, theMenu ):
		"""
		Adds menu items to default context menu.
		Remove this method if you do not want any extra context menu items.
		"""
		try:
			# Determining the current layer and selected object:
			graphicView = self.editViewController().graphicView()
			currentLayer = graphicView.activeLayer()
			clickPosition = graphicView.getActiveLocation_( theEvent )
			self.overElement = self.elementAtPoint_atLayer_( clickPosition, currentLayer )
			
			# If click goes somewhere else, but only one item is selected:
			if not self.overElement and len( currentLayer.selection() ) == 1:
				self.overElement = currentLayer.selection()[0]
			
			# Add a contextual menu item:
			if type( self.overElement ) == GSAnchor: # Check type of selected object
				# Build up a new menu item:
				actionName = "Move Anchor" # The name as it appears in the menu
				actionMethod = "moveAnchor:" # Class method invoked by the menu item
				
				# Call a method of this plugin class:
				newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_( actionName, actionMethod, "" )
				newMenuItem.setTarget_( self ) # method of this class will be called
				
				# Or call a method of self.overElement:
				# newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_( actionName, actionMethod, "" )
				# newMenuItem.setTarget_( self.overElement ) # method of overElement will be called

				# You can set a tool tip:
				newMenuItem.setToolTip_( "Moves the anchor a little." ) # Short description

				# Add the new item to the menu, pick one:
				theMenu.insertItem_atIndex_( newMenuItem, 0 ) # adds item at the top of the menu
				# theMenu.addItem( newMenuItem ) # adds item to the bottom of the menu
				
				# Add a separator:
				newSeparator = NSMenuItem.separatorItem()
				theMenu.insertItem_atIndex_( newSeparator, 1 )
								
		except Exception as e:
			self.logToConsole( "addMenuItemsForEvent_toMenu_: %s" % str(e) )
	
	def genericLayerAction( self ):
		"""
		Invoked from self.defaultContextMenu().
		Fill in your own method name and code.
		Remove this method if you do not want any extra context menu items.
		"""
		try:
			# Determine the active layer:
			graphicView = self.editViewController().graphicView()
			currentLayer = graphicView.activeLayer()
			
			# Do stuff:
			print "Current layer:", currentLayer.parent.name, currentLayer.name
			print "  Number of paths:", len(currentLayer.paths)
			print "  Number of components:", len(currentLayer.components)
			print "  Number of anchors:", len(currentLayer.anchors)
		except Exception as e:
			self.logToConsole( "genericLayerAction: %s" % str(e) )
	
	def moveAnchor_( self, sender ):
		"""
		Example for a method triggered by a context menu item.
		Fill in your own method name and code.
		Invoked from self.addMenuItemsForEvent_toMenu_().
		- sender contains the NSMenuItem.
		- self.overElement contains the object clicked upon.
		Remove this method if you do not want any extra context menu items.
		"""
		try:
			if type( self.overElement ) == GSAnchor:
				thisAnchor = self.overElement
				oldPosition = thisAnchor.position
				newPosition = NSPoint( oldPosition.x + 20, oldPosition.y - 50 )
				thisAnchor.setPosition_( newPosition )
		except Exception as e:
			self.logToConsole( "moveAnchor_: %s" % str(e) )	
		
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "%s tool:\n%s" % ( self.title(), message )
		NSLog( myLog )
