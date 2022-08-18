# encoding: utf-8

###########################################################################################################
#
#
#	File Format Plugin
#	Implementation for exporting fonts through the Export dialog
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/File%20Format
#
#	For help on the use of Interface Builder:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc, AppKit
from GlyphsApp import *
from GlyphsApp.plugins import *
from vanilla import Window, TextBox, CheckBox, Group

# Preference key names
# Part of the example. You may delete them
unicodePref = 'com.test.csvexport.exportUnicode'
glyphWidthPref = 'com.test.csvexport.exportGlyphWidth'



class ____PluginClassName____(FileFormatPlugin):

	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({'en': u'My CSV Export', 'de': u'Mein CSV-Export'})
		self.icon = 'ExportIcon'
		self.toolbarPosition = 100
		
		# Init user preferences if not existent and set default value
		Glyphs.registerDefaults({unicodePref: True, glyphWidthPref: False})
		
		# Build the UI
		self.w = Window((100, 100))
		self.w.group = Group("auto")
		self.w.group.Label1 = TextBox("auto", "In addition to glyph names, export:")
		self.w.group.UnicodesCheckBox = CheckBox("auto", "Unicodes", callback=self.setExportUnicode_, value=Glyphs.defaults[unicodePref])
		self.w.group.GlyphWidthCheckBox = CheckBox("auto", "Glyph width", callback=self.setExportGlyphWidth_, value=Glyphs.defaults[glyphWidthPref])
		self.w.group.Label2 = TextBox("auto", "Your selection (feedback demonstration):")
		self.w.group.FeedbackLabel = TextBox("auto", "Nothing")
		
		# for export settings dialogs, you **need** to use auto layout. https://vanilla.robotools.dev/en/latest/concepts/positioning.html?highlight=auto#auto-layout
		rules = [
			# Horizontal
			"H:|-[Label1]-|",
			"H:|-[UnicodesCheckBox]-|",
			"H:|-[GlyphWidthCheckBox]-|",
			"H:|-[Label2]-|",
			"H:|-[FeedbackLabel]-|",
			# Vertical
			"V:|-[Label1(20@999)]-[UnicodesCheckBox(20@999)]-[GlyphWidthCheckBox(20@999)]-[Label2(20@999)]-[FeedbackLabel(20@999)]-|"
		]
		metrics = {}
		self.w.group.addAutoPosSizeRules(rules, metrics)
		
		# We only need the group, not the window. But vanilla doesn’t seem to be able to build a view outside of a window
		self.dialog = self.w.group._nsObject

	@objc.python_method
	def start(self):
		# Update text field. You may delete this
		self.updateFeedBackTextField()
	
	# Example function. You may delete it
	def setExportUnicode_(self, sender):
		Glyphs.defaults[unicodePref] = bool(sender.get())
		self.updateFeedBackTextField()
	
	# Example function. You may delete it
	def setExportGlyphWidth_(self, sender):
		Glyphs.defaults[glyphWidthPref] = bool(sender.get())
		self.updateFeedBackTextField()
	
	# Example function. You may delete it
	@objc.python_method
	def updateFeedBackTextField(self):
		string = []
		if Glyphs.defaults[unicodePref]:
			string.append('Unicodes')
		if Glyphs.defaults[glyphWidthPref]:
			string.append('Glyph Width')
		self.w.group.FeedbackLabel.set(', '.join(string) if len(string) else 'Nothing')

	@objc.python_method
	def export(self, font):
		# Ask for export destination and write the file:
		title = "Choose export destination"
		proposedFilename = font.familyName
		fileTypes = ['csv']
		
		# Call dialog
		filepath = GetSaveFile(title, proposedFilename, fileTypes)
		
		if filepath:
			
			import csv
			
			with open(filepath, 'w') as csvfile:
				fieldnames = ['glyph_name', 'unicode', 'glyph_width']
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				
				writer.writeheader()
				
				for g in font.glyphs:
					writeDict = {}
					writeDict['glyph_name'] = g.name
					
					if Glyphs.defaults[unicodePref] == True and g.unicode:
						writeDict['unicode'] = g.unicode
					
					if Glyphs.defaults[glyphWidthPref] == True and g.layers[0].width:
						writeDict['glyph_width'] = g.layers[0].width
					
					writer.writerow(writeDict)
			
			return (True, 'The export of "%s" was successful.' % (os.path.basename(filepath)))
		
		else:
			return (False, 'No file chosen')

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
