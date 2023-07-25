#!/usr/bin/env python
# encoding: utf-8
"""
instanceGenerate.py

Created by Georg Seifert on 2016-10-13.
Copyright (c) 2016 schriftgestaltung.de. All rights reserved.
"""

import sys, os
from Glyphs import *
from Foundation import NSURL, NSString

def writeInstanceAsUFO():
	'''
	This will write the second instance of the active font as an .ufo to the desktop
	'''
	font = currentDocument.font()
	intance = font.instances()[2]
	
	InterpolatedFont = font.generateInstance_error_(intance, None)
	print(InterpolatedFont)
	doc = Glyphs.objectWithClassName_("GSDocument")
	doc.setFont_(InterpolatedFont)
	
	url = NSURL.fileURLWithPath_(os.path.expanduser("~/Desktop/%s-%s.ufo" % (font.familyName(), intance.name())))
	typeName = "org.unifiedfontobject.ufo"
	doc.writeToURL_ofType_forSaveOperation_originalContentsURL_error_(url, typeName, 0, url, None)
	
def exportAllInstances():
	'''
	This will export all instances of the font at 'path' as TrueType fonts.
	'''
	path = os.path.expanduser("~/Desktop/test/file.glyphs")
	doc = Glyphs.openDocumentWithContentsOfFile_display_(path, False)
	print("Exporting:", doc.displayName())
	font = doc.font()
	for instance in font.instances():
		print("Instance:", instance)
		instance.generate_({
			'ExportFormat': "TTF",
			'ExportContainer': "woff",
			'Destination': NSURL.fileURLWithPath_(os.path.expanduser("~/Desktop/test/"))
		})
		
	'''
	possible keys:
		ExportContainer: "woff", "woff2", "eot"
		Destination: NSURL
		autoHint: bool (default = true)
		removeOverlap: bool (default = true)
		useSubroutines: bool (default = true)
		useProductionNames: bool (default = true)
	'''
	
	doc.close()
	print("Ready!")

def classTeste():
	pen = Glyphs.objectWithClassName_("GSSVGPen")
	print(pen)
	print(Glyphs.mainBundle())

def runScriptInsideGlyphs():
	code = "print(Layer)"
	if Glyphs.versionString < "3.1":
		# the print output will be in the Glyphs console. Maybe set "Use system console for script output" in Preferences > Addons
		macroViewController = Glyphs.objectWithClassName_("GSMacroViewController")
		macroViewController.runMacroString_(code)
	else:
		RunScript(code)
		
def accessGlyphsInfo():
	font = currentDocument.font()
	print(font.glyphsInfo())
	glyphsInfo = Glyphs.objectWithClassName_("GSGlyphsInfo")
	print(glyphsInfo)
	print(glyphsInfo.glyphInfoForName_("A"))

def accessLayers():
	font = currentDocument.font()
	glyph = font.glyphForName_("A")
	master = font.fontMasterAtIndex_(0)
	print(master.id())
	layer = glyph.layerForId_(master.id())
	print(layer)
	path = layer.objectInShapesAtIndex_(0)
	print(path)
	

if __name__ == '__main__':
	#exportAllInstances()
	#writeInstanceAsUFO()
	#runScriptInsideGlyphs()
	#accessGlyphsInfo()
	accessLayers()