# encoding: utf-8
# Example tool plugin with subtools
# Georg Seifert, 2016

from GlyphsApp.plugins import *
import traceback, os

class MultipleTools(SelectTool):
	def settings(self):
		self.name = u'Multiple Tools'
		self.keyboardShortcut = 'x'
		self._icon = None
		self.toolbarPosition = 250
		
		osource_image = os.path.join(os.path.dirname(__file__), 'toolbarX.pdf')
		self.xImage = NSImage.alloc().initByReferencingFile_(osource_image)
		self.xImage.setTemplate_(True)
		
		nsource_image = os.path.join(os.path.dirname(__file__), 'toolbarY.pdf')
		self.yImage = NSImage.alloc().initByReferencingFile_(nsource_image)
		self.yImage.setTemplate_(True)
		
		self.activeToolIndex = Glyphs.intDefaults["MultipleToolsActiveTool"]
	
	def activate(self):
		pass
	
	def deactivate(self):
		pass
	
	def toolBarIcon(self):
		if self.activeToolIndex == 0:
			return self.xImage
		if self.activeToolIndex == 1:
			return self.yImage
	
	def activateToolX(self):
		self.activeToolIndex = 0
		Glyphs.intDefaults["MultipleToolsActiveTool"] = self.activeToolIndex
	
	def activateToolY(self):
		self.activeToolIndex = 1
		Glyphs.intDefaults["MultipleToolsActiveTool"] = self.activeToolIndex
	
	def selectNextSubTool_(self, sender):
		# is called when the user presses shift + the self.keyboardShortcut to access all subtools by keyboard
		if self.activeToolIndex == 0:
			self.activateToolY()
		else:
			self.activateToolX()
	
	def toolbarMenu(self):
		try:
			theMenu = NSMenu.alloc().initWithTitle_(self.title())
			
			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Tool X", self.activateToolX, "")
			newMenuItem.setTarget_(self)
			newMenuItem.setImage_(self.xImage) # it has to be an NSImage, this is optional
			theMenu.addItem_(newMenuItem)
			
			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Tool Y", self.activateToolY, "")
			newMenuItem.setTarget_(self)
			newMenuItem.setImage_(self.yImage) # it has to be an NSImage, this is optional
			theMenu.addItem_(newMenuItem)
			
			return theMenu;
		except Exception as e:
			print traceback.format_exc()
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__