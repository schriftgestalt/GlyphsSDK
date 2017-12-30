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

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *


# Preference key names
# Part of the example. You may delete them
unicodePref = 'com.test.csvexport.exportUnicode'
glyphWidthPref = 'com.test.csvexport.exportGlyphWidth'



class ____PluginClassName____(FileFormatPlugin):
	
	# Definitions of IBOutlets
	
	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()
	
	# Example variables. You may delete them
	feedbackTextField = objc.IBOutlet()
	unicodeCheckBox = objc.IBOutlet()
	glyphWidthCheckbox = objc.IBOutlet()
	
	def settings(self):
		self.name = Glyphs.localize({'en': u'My CSV Export', 'de': u'Mein CSV-Export'})
		self.icon = 'ExportIcon'
		self.toolbarPosition = 100
		
		# Load .nib dialog (with .extension)
		self.loadNib('IBdialog', __file__)
	
	def start(self):
		
		# Init user preferences if not existent and set default value
		if Glyphs.defaults[unicodePref] == None:
			Glyphs.defaults[unicodePref] = True
		if Glyphs.defaults[glyphWidthPref] == None:
			Glyphs.defaults[glyphWidthPref] = True
		
		# Set initial state of checkboxes according to user variables
		self.unicodeCheckBox.setState_(Glyphs.defaults[unicodePref])
		self.glyphWidthCheckbox.setState_(Glyphs.defaults[glyphWidthPref])

		# Update text field. You may delete them
		self.updateFeedBackTextField()
	
	# Example function. You may delete it
	@objc.IBAction
	def setExportUnicode_(self, sender):
		Glyphs.defaults[unicodePref] = bool(sender.intValue())
		self.updateFeedBackTextField()
	
	# Example function. You may delete it
	@objc.IBAction
	def setExportGlyphWidth_(self, sender):
		Glyphs.defaults[glyphWidthPref] = bool(sender.intValue())
		self.updateFeedBackTextField()
	
	# Example function. You may delete it
	def updateFeedBackTextField(self):
		string = []
		if Glyphs.defaults[unicodePref]:
			string.append('Unicodes')
		if Glyphs.defaults[glyphWidthPref]:
			string.append('Glyph Width')
		self.feedbackTextField.setStringValue_(', '.join(string) if len(string) else 'Nothing')
	
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
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
