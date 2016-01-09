# encoding: utf-8

###########################################################################################################
#
#
#	Select Tool Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/SelectTool
#
#
###########################################################################################################


from GlyphsPlugins import *

class ____PluginClassName____(SelectTool):
	
	def settings(self):
		self.name = Glyphs.localize({'en': 'My Select Tool', 'de': 'Mein Auswahlwerkzeug'})
		self.generalContextMenus = [
			[Glyphs.localize({'en': 'Layer info in Macro window', 'de': 'Ebenen-Infos in Makro-Fenster'}), self.printInfo],
		]

	def start(self):
		pass

	def activate(self):
		pass

	def deactivate(self):
		pass
		
	def conditionalContextMenus(self):

		# Empty list of context menu items
		contextMenus = []

		# Execute only if layers are actually selected
		if Glyphs.font.selectedLayers:
			layer = Glyphs.font.selectedLayers[0]
			
			# Exactly one object is selected and it’s an anchor
			if len(layer.selection) == 1 and type(layer.selection[0]) == GSAnchor:
					
				# Add context menu item
				contextMenus.append([Glyphs.localize({'en': 'Randomly move anchor', 'de': u'Anker zufällig verschieben'}), self.randomlyMoveAnchor])

		# Return list of context menu items
		return contextMenus

	def printInfo(self):
		"""
		Example for a method triggered by a context menu item.
		Fill in your own method name and code.
		Remove this method if you do not want any extra context menu items.
		"""

		# Execute only if layers are actually selected
		if Glyphs.font.selectedLayers:
			layer = Glyphs.font.selectedLayers[0]
		
			# Do stuff:
			print "Current layer:", layer.parent.name, layer.name
			print "  Number of paths:", len(layer.paths)
			print "  Number of components:", len(layer.components)
			print "  Number of anchors:", len(layer.anchors)

	def randomlyMoveAnchor( self, sender ):
		"""
		Example for a method triggered by a conditional context menu item.
		Fill in your own method name and code.
		Sender contains the NSMenuItem, so that’s not really useful for you.
		Remove this method if you do not want any extra context menu items.
		"""
		import random
		
		# Just for your understanding:
		# Here we don’t need to check how many objects are selected and what types they are.
		# Because this has already been done in conditionalContextMenus() and didn’t change since.
		# So our anchor is the first and only selected item in the layer.

		anchor = Glyphs.font.selectedLayers[0].selection[0]
		anchor.position = NSPoint(anchor.position.x + random.randint(-50, 50), anchor.position.y + random.randint(-50, 50))
