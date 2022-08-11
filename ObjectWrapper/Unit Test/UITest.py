#MenuTitle: Glyphs.app UI Tests
# encoding: utf-8
# -*- coding: utf-8 -*-

from __future__ import print_function

#import GlyphsApp
#reload(GlyphsApp)

import unittest

import GlyphsApp
from GlyphsApp import *
import os, time, sys, datetime
import objc
import copy

from UnitTest import GlyphsAppTests

from AppKit import \
NSAffineTransform, \
NSArray, \
NSBezierPath, \
NSColor, \
NSDate, \
NSDictionary, \
NSImage, \
NSMenuItem, \
NSMenuItem, \
NSNull, \
NSNumber, \
NSPoint, \
NSRect

if sys.version_info[0] == 3:
	unicode = str

PathToTestFile = os.path.join(os.path.dirname(__file__), 'Glyphs Unit Test Sans.glyphs')

Glyphs.clearLog()

class GlyphsAppUITests(unittest.TestCase):

	def test_setUp(self):
		if Glyphs.font is None:
			Glyphs.open(PathToTestFile)
			print(Glyphs.font)

	def test_tearDown(self):
		if Glyphs.font is not None:
			Glyphs.font.close()

	def test_GSApplication(self):
		
		# Main object
		GlyphsAppTests.assertIsNotNone(Glyphs)
		GlyphsAppTests.assertIsNotNone(Glyphs.__repr__())
		
		# close all fonts
		for font in Glyphs.fonts:
			font.close()
		GlyphsAppTests.assertEqual(len(Glyphs.fonts), 0)
		


		# AppFontProxy
		newFont = GSFont()
		Glyphs.fonts.append(newFont)
		GlyphsAppTests.assertIn(newFont, Glyphs.fonts)
		GlyphsAppTests.assertEqual(len(Glyphs.fonts), 1)
		GlyphsAppTests.assertEqual(newFont, Glyphs.font)
		copyfont = copy.copy(newFont)
		GlyphsAppTests.assertNotIn(copyfont, Glyphs.fonts)
		newFont.close()
		GlyphsAppTests.assertNotIn(newFont, Glyphs.fonts)
		GlyphsAppTests.assertEqual(len(Glyphs.fonts), 0)
		Glyphs.fonts.extend([copyfont])
		GlyphsAppTests.assertIn(copyfont, Glyphs.fonts)
		copyfont.close()
		with GlyphsAppTests.assertRaises(TypeError):
			Glyphs.fonts['a']

		# open font
		Glyphs.open(PathToTestFile)
		# Macro window
		Glyphs.showMacroWindow()
		
		# Assert font
		GlyphsAppTests.assertIsNotNone(Glyphs.font)
		GlyphsAppTests.assertEqual(len(Glyphs.fonts), 1)

		# GSApplication.documents
		GlyphsAppTests.assertEqual(len(Glyphs.documents), 1)
		GlyphsAppTests.assertIs(Glyphs.documents[0].font, Glyphs.fonts[0])
		with GlyphsAppTests.assertRaises(TypeError):
			Glyphs.documents['a']
		GlyphsAppTests.assertIsInstance(copy.copy(Glyphs.documents), list)
		
		# current document #::Rafal
		GlyphsAppTests.assertIsInstance(Glyphs.currentDocument, GSDocument)

		## Attributes
		
		# GSApplication.reporters
		GlyphsAppTests.assertGreater(len(list(Glyphs.reporters)), 0)
		GlyphsAppTests.assertGreater(len(Glyphs.reporters), 0)
		
		# activate all reporters
		
		for reporter in Glyphs.reporters:
			Glyphs.activateReporter(reporter)
		
		GlyphsAppTests.assertEqual(len(Glyphs.activeReporters), len(Glyphs.reporters))
		# deactivate all reporters
		for reporter in Glyphs.reporters:
			Glyphs.deactivateReporter(reporter)
		GlyphsAppTests.assertEqual(len(Glyphs.activeReporters), 0)
		
		GlyphsAppTests.assertIsInstance(Glyphs.filters, list)
		
		# GSApplication.defaults
		GlyphsAppTests.assertDict(Glyphs.defaults, assertType = False)
		
		del(Glyphs.defaults["TestKey"])
		Glyphs.registerDefaults({"TestKey":12})
		GlyphsAppTests.assertEqual(Glyphs.defaults["TestKey"], 12)
		Glyphs.registerDefault("TestKey",36) #::Rafal
		GlyphsAppTests.assertEqual(Glyphs.defaults["TestKey"], 36)
		Glyphs.registerDefaults({"TestKey":12})
		Glyphs.defaults["TestKey"] = 24
		GlyphsAppTests.assertEqual(Glyphs.defaults["TestKey"], 24)
		del(Glyphs.defaults["TestKey"])
		GlyphsAppTests.assertEqual(Glyphs.defaults["TestKey"], 12)
		
		# GSApplication.boolDefaults
		GlyphsAppTests.assertIsNone(Glyphs.defaults["BoolKey"])
		GlyphsAppTests.assertIs(Glyphs.boolDefaults["BoolKey"], False)
		Glyphs.boolDefaults["BoolKey"] = True
		GlyphsAppTests.assertEqual(Glyphs.boolDefaults["BoolKey"], True)
		del Glyphs.boolDefaults["BoolKey"]
		with GlyphsAppTests.assertRaises(TypeError):
			Glyphs.boolDefaults["BoolKey"] = 12

		# GSApplication.colorDefaults
		GlyphsAppTests.assertIsNone(Glyphs.colorDefaults["colorKey"])
		Glyphs.colorDefaults["colorKey"] = "#ff0000"
		GlyphsAppTests.assertIsNotNone(Glyphs.colorDefaults["colorKey"])
		del Glyphs.colorDefaults["colorKey"]
		GlyphsAppTests.assertIsNone(Glyphs.colorDefaults["colorKey"])
		with GlyphsAppTests.assertRaises(ValueError):
			Glyphs.colorDefaults["colorKey"] = "not a color"
		with GlyphsAppTests.assertRaises(TypeError):
			Glyphs.colorDefaults["colorKey"] = 12

		# GSApplication.intDefaults
		GlyphsAppTests.assertIsNone(Glyphs.defaults["IntKey"])
		GlyphsAppTests.assertIs(Glyphs.intDefaults["IntKey"], 0)
		Glyphs.intDefaults["IntKey"] = 14
		GlyphsAppTests.assertEqual(Glyphs.intDefaults["IntKey"], 14)
		del Glyphs.intDefaults["IntKey"]
		with GlyphsAppTests.assertRaises(TypeError):
			Glyphs.intDefaults["IntKey"] = 12.5

		# GSApplication.scriptAbbreviations
		GlyphsAppTests.assertIsNotNone(dict(Glyphs.scriptAbbreviations))
		
		# GSApplication.scriptSuffixes
		GlyphsAppTests.assertIsNotNone(dict(Glyphs.scriptSuffixes))
		
		# GSApplication.languageScripts
		GlyphsAppTests.assertIsNotNone(dict(Glyphs.languageScripts))
		
		# GSApplication.languageData
		GlyphsAppTests.assertIsNotNone(list(map(dict, Glyphs.languageData)))
		
		# GSApplication.unicodeRanges
		GlyphsAppTests.assertIsNotNone(list(Glyphs.unicodeRanges))
		
		# GSApplication.editViewWidth
		GlyphsAppTests.assertInteger(Glyphs.editViewWidth)
		
		# GSApplication.handleSize
		GlyphsAppTests.assertInteger(Glyphs.handleSize)
		
		# GSApplication.versionString
		self.assertString(Glyphs.versionString, readOnly = True)
		
		# GSApplication.versionNumber
		self.assertFloat(Glyphs.versionNumber, readOnly = True)
		
		# GSApplication.buildNumber
		self.assertFloat(Glyphs.buildNumber, readOnly = True)

		# GSApplication.menu
		def a():
			print('hello')
		newMenuItem = NSMenuItem('B', a)
		Glyphs.menu[EDIT_MENU].append(newMenuItem)
		GlyphsAppTests.assertIsNotNone(Glyphs.menu[0])
		with GlyphsAppTests.assertRaises(TypeError):
			Glyphs.menu[1.5]
		GlyphsAppTests.assertList(copy.copy(Glyphs.menu))
		
		## Methods
		
		# GSApplication.showGlyphInfoPanelWithSearchString()
		Glyphs.showGlyphInfoPanelWithSearchString('a')
		
		# GSApplication.glyphInfoForName()
		GlyphsAppTests.assertEqual(str(Glyphs.glyphInfoForName('a')), "<GSGlyphInfo 'a'>")
		
		# GSApplication.glyphInfoForUnicode()
		GlyphsAppTests.assertEqual(str(Glyphs.glyphInfoForUnicode('0061')), "<GSGlyphInfo 'a'>")
		
		# GSApplication.niceGlyphName()
		GlyphsAppTests.assertEqual(Glyphs.niceGlyphName('a'), 'a')
		
		# GSApplication.productionGlyphName()
		GlyphsAppTests.assertEqual(Glyphs.productionGlyphName('a'), 'a')
		
		# GSApplication.ligatureComponents()
		GlyphsAppTests.assertEqual(len(list(Glyphs.ligatureComponents('allah-ar'))), 4)
		
		# GSApplication.redraw()
		Glyphs.redraw()
		
		# GSApplication.showNotification()
		Glyphs.showNotification('Glyphs Unit Test', 'Hello World')
		
		GlyphsAppTests.assertIsNotNone(Glyphs.localize({
			'en':  'Hello World',
			'de': u'Hallöle Welt',
			'fr':  'Bonjour tout le monde',
			'es':  'Hola Mundo',
			}))
		
		# callbacks #::Rafal # don't know if it makes sense at all
		def testCallbackMethod(**kwrgs):
			pass
		callbacks = ("DrawForeground", "DrawBackground", "DrawInactive", "GSDocumentWasOpenedNotification", "GSDocumentActivateNotification", "GSDocumentWasSavedSuccessfully", "GSDocumentWasExportedNotification", "GSDocumentCloseNotification", "TabDidOpenNotification", "TabWillCloseNotification", "GSUpdateInterface", "mouseMovedNotification", "mouseDraggedNotification", "mouseDownNotification", "mouseUpNotification", "GSContextMenuCallbackName")
		for callback in callbacks:
			Glyphs.addCallback(testCallbackMethod, callback)
			Glyphs.removeCallback(testCallbackMethod)

	def test_GSFont_parent():
		return
		# TODO: Implement <GS @MF>
		# GSFont.parent
		# self.assertIn('GSDocument', str(font.parent))

	def test_GSFont_selection(self):
		# TODO: Implement <GS @MF>
		return
		# for glyph in font.glyphs:
		# 	glyph.selected = False
		# font.glyphs['a'].selected = True
		# self.assertEqual(len(list(font.selection)), 1)
		# for glyph in font.glyphs:
		# 	glyph.selected = True
		# self.assertEqual(set(font.selection), set(font.glyphs))
		# font.selection = [font.glyphs['a']]
		# self.assertEqual(list(font.selection), [font.glyphs['a']])
		# with self.assertRaises(TypeError):
		# 	font.selection = 0
		
		# GSFont.selectedLayers
		# GSFont.currentText
		# GSFont.tabs
		# GSFont.currentTab
		# for tab in font.tabs:
		# 	tab.close()
		# tab = font.newTab('a')
		# self.assertEqual(tab, font.tabs[-1])
		# self.assertIsNotNone(font.currentTab.__repr__())
		# self.assertEqual(len(list(font.selectedLayers)), 1)
		# self.assertEqual(len(list(font.tabs)), 1)
		# self.assertEqual(font.currentText, 'a')
		# font.currentText = 'A'
		# self.assertEqual(font.currentText, 'A')
		# self.assertEqual(font.currentTab, font.tabs[-1])
		# tab2 = font.newTab('n')
		# self.assertEqual(font.currentTab, tab2)
		# font.currentTab = tab
		# self.assertEqual(font.currentTab, tab)
		# font.tabs[0].close()
		# self.assertEqual(font.currentTab, tab2)
		# font.tabs[0].close()
		# # values are None when no tabs are open
		# self.assertIsNone(font.currentText)
		# self.assertIsNone(font.currentTab)
		# with self.assertRaises(TypeError):
		# 	font.tabs['']
		
		# GSFont.selectedFontMaster
		# GSFont.masterIndex
		# oldMasterIndex = font.masterIndex
		# for i in range(len(list(font.masters))):
		# 	font.masterIndex = i
		# 	self.assertEqual(font.selectedFontMaster, font.masters[i])
		# font.masterIndex = oldMasterIndex
	
	def test_GSFont_close(self):
		return
		# GSFont.close()
		# font = self.font
		# font.close()
		# self.assertIsNone(font.__repr__())
		# self.assertIsNone(font)


	def test_GSEditViewController(self):
		return
		font = self.font
		# font.show()

		tab = font.newTab('a')
		self.assertIsNotNone(tab.__repr__())
		
		# GSEditViewController.parent
		self.assertEqual(tab.parent, font)

		# GSEditViewController.text
		self.assertEqual(tab.text, 'a')

		# GSEditViewController.layers
		self.assertEqual(list(tab.layers), [font.glyphs['a'].layers[0]])
		tab.layers = [font.glyphs['a'].layers[0]]
		tab.layers.append(font.glyphs['A'].layers[0])
		tab.layers.remove(font.glyphs['A'].layers[0])
		self.assertEqual(list(tab.layers), [font.glyphs['a'].layers[0]])

		# GSEditViewController.composedLayers
		font.updateFeatures()
		self.assertEqual(list(tab.composedLayers), [font.glyphs['a'].layers[0]])
		tab.features = ['smcp']
		self.assertEqual(list(tab.composedLayers), [font.glyphs['a.sc'].layers[0]])
		tab.features = []

		# GSEditViewController.scale
		self.assertFloat(tab.scale)

		# GSEditViewController.viewPort
		self.assertIsInstance(tab.viewPort, NSRect)

		# GSEditViewController.bounds
		self.assertIsInstance(tab.bounds, NSRect)

		# GSEditViewController.selectedLayerOrigin
		self.assertIsInstance(tab.selectedLayerOrigin, NSPoint)

		# GSEditViewController.textCursor
		self.assertInteger(tab.textCursor)

		# GSEditViewController.textRange
		self.assertInteger(tab.textRange)

		# GSEditViewController.direction
		self.assertTrue(tab.direction in [LTR, RTL, LTRTTB, RTLTTB])
		tab.direction = RTL
		self.assertTrue(tab.direction in [LTR, RTL, LTRTTB, RTLTTB])
		tab.direction = LTR
		self.assertTrue(tab.direction in [LTR, RTL, LTRTTB, RTLTTB])

		# GSEditViewController.features
		newFeature = GSFeature('liga', 'sub a by A;')
		font.features.append(newFeature)
		tab.features = ['liga']
		self.assertEqual(list(tab.features), ['liga'])
		tab.features = []
		del(font.features['liga'])

		# GSEditViewController.previewInstances
		tab.previewInstances = 'all'
		self.assertEqual(tab.previewInstances, 'all')
		tab.previewInstances = 'live'
		self.assertEqual(tab.previewInstances, 'live')
		for instance in font.instances:
			tab.previewInstances = instance
			self.assertEqual(tab.previewInstances, instance)

		# GSEditViewController.previewHeight
		tab.previewHeight = 100
		# self.assertEqual(tab.previewHeight, 100)
		tab.previewHeight = 0
		# self.assertEqual(tab.previewHeight, 0)

		# GSEditViewController.bottomToolbarHeight
		self.assertTrue(tab.bottomToolbarHeight > 0)

		
		# GSEditViewController.userData
		tab.tempData['a'] = 'b'
		self.assertTrue(tab.tempData['a'] == 'b')

		## Methods
		
		# GSEditViewController.saveToPDF()
		self.assertIsNotNone(font.filepath)
		tab.saveToPDF(os.path.join(os.path.dirname(font.filepath), 'Unit Test.pdf'))

		# GSEditViewController.close()
		tab.close()

	def test_GSFont_tools(self):
		return
		# GSFont.tool
		# GSFont.tools
		# GSFont.toolIndex
		# oldTool = font.tool
		# for toolName in font.tools:
		# 	font.tool = toolName
		# 	self.assertEqual(font.tool, toolName)
		# 	self.assertInteger(font.toolIndex)
		# 	self.assertEqual(font.tools[font.toolIndex], toolName)
		# font.tool = oldTool
	
	def test_GSFont_fontView(self):
		return
		# GSFont.fontView #::Rafal
		# self.assertIsInstance(font.fontView, GlyphsApp.GSFontViewController)

'''
Stuff from UnitTest.py which seems to not make sense

def test_Methods(self):
	...
	GetSaveFile(filetypes = ['glyphs'])
	GetOpenFile()
	GetFolder()
	Message('Title', 'Message')
	LogToConsole('Message')
	LogError('Error message created in test code. Ignore it.')
	...

'''

sys.argv = ["GlyphsAppUITests"]

if __name__ == '__main__':
	### MARK ### import coverage  # pip3 install coverage
	### MARK ### cov = coverage.Coverage(include=["*/GlyphsApp/__init__.py"])
	### MARK ### cov.start()

	unittest.main(exit=False, failfast=False)

	### MARK ### cov.stop()
	### MARK ### cov.save()

	### MARK ### cov.html_report()

