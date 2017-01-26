#MenuTitle: Glyphs.app Unit Tests
# encoding: utf-8
# -*- coding: utf-8 -*-

#import GlyphsApp
#reload(GlyphsApp) 

import unittest

import GlyphsApp
from GlyphsApp import *
import os, time
import objc
import copy
from AppKit import *

PathToTestFile = os.path.join(os.path.dirname(__file__), 'Glyphs Unit Test Sans.glyphs')

class GlyphsAppTests(unittest.TestCase):
	
	def assertString(self, stringObject, assertType = True, readOnly = False):
		if assertType:
			self.assertIsInstance(str(stringObject), str)
		if readOnly == False:
			oldValue = stringObject
			stringObject = 'a'
			self.assertEqual(stringObject, 'a')
			stringObject = oldValue
	
	def assertDict(self, dictObject, assertType = True):
		if assertType:
			self.assertIsInstance(dict(dictObject), dict)
		var1 = 'abc'
		var2 = 'def'
		dictObject['uniTestValue'] = var1
		self.assertEqual(dictObject['uniTestValue'], var1)
		dictObject['uniTestValue'] = var2
		self.assertEqual(dictObject['uniTestValue'], var2)
	
	def assertInteger(self, intObject, assertType = True, readOnly = False):
		if assertType:
			assert type(int(intObject)) == int
		if readOnly == False:
			oldValue = intObject
			intObject = 1
			self.assertEqual(intObject, 1)
			intObject = oldValue
	
	def assertFloat(self, floatObject, assertType = True, readOnly = False):
		if assertType:
			self.assertIsInstance(float(floatObject), float)
		if readOnly == False:
			oldValue = floatObject
			floatObject = .5
			self.assertEqual(floatObject, .5)
			floatObject = oldValue
	
	def assertUnicode(self, unicodeObject, assertType = True, readOnly = False):
		if assertType:
			assert unicode(unicodeObject)
		if readOnly == False:
			oldValue = unicodeObject
			unicodeObject = u'Ə'
			self.assertEqual(unicodeObject, u'Ə')
			unicodeObject = oldValue
	
	def assertBool(self, boolObject, assertType = True, readOnly = False):
		if assertType:
			self.assertIsInstance(boolObject, bool)
		if readOnly == False:
			oldValue = boolObject
			boolObject = not boolObject
			self.assertEqual(boolObject, (not oldValue))
			boolObject = oldValue
	
	def setUp(self):
		if Glyphs.font is None:
			Glyphs.open(PathToTestFile)
	
	def tearDown(self):
		pass
	
	def test_GSApplication(self):
		
		# Main object
		self.assertIsNotNone(Glyphs)
		self.assertIsNotNone(Glyphs.__repr__())
		
		# close all fonts
		for font in Glyphs.fonts:
			font.close()
		
		# open font
		Glyphs.open(PathToTestFile)
		# Macro window
		Glyphs.showMacroWindow()
		
		# Assert font
		self.assertIsNotNone(Glyphs.font)
		self.assertEqual(len(Glyphs.fonts), 1)
		
		
		## Attributes
		
		# GSApplication.reporters
		self.assertGreater(len(list(Glyphs.reporters)), 0)
		self.assertGreater(len(Glyphs.reporters), 0)
		
		# activate all reporters
		
		for reporter in Glyphs.reporters:
			Glyphs.activateReporter(reporter)
		
		self.assertEqual(len(Glyphs.activeReporters), len(Glyphs.reporters))
		# deactivate all reporters
		for reporter in Glyphs.reporters:
			Glyphs.deactivateReporter(reporter)
		self.assertEqual(len(Glyphs.activeReporters), 0)
		
		# GSApplication.defaults
		self.assertDict(Glyphs.defaults, assertType = False)
		
		# GSApplication.scriptAbbreviations
		self.assertIsNotNone(dict(Glyphs.scriptAbbreviations))
		
		# GSApplication.scriptSuffixes
		self.assertIsNotNone(dict(Glyphs.scriptSuffixes))
		
		# GSApplication.languageScripts
		self.assertIsNotNone(dict(Glyphs.languageScripts))
		
		# GSApplication.languageData
		self.assertIsNotNone(list(map(dict, Glyphs.languageData)))
		
		# GSApplication.unicodeRanges
		self.assertIsNotNone(list(Glyphs.unicodeRanges))
		
		# GSApplication.editViewWidth
		self.assertInteger(Glyphs.editViewWidth)
		
		# GSApplication.handleSize
		self.assertInteger(Glyphs.handleSize)
		
		# GSApplication.versionString
		self.assertString(Glyphs.versionString, readOnly = True)
		
		# GSApplication.versionNumber
		self.assertFloat(Glyphs.versionNumber, readOnly = True)
		
		# GSApplication.buildNumber
		self.assertInteger(Glyphs.buildNumber, readOnly = True)

		# GSApplication.menu
		def a():
			print 'hello'
		newMenuItem = NSMenuItem('B', a)
		Glyphs.menu[EDIT_MENU].append(newMenuItem)

		
		## Methods
		
		# GSApplication.showGlyphInfoPanelWithSearchString()
		Glyphs.showGlyphInfoPanelWithSearchString('a')
		
		# GSApplication.glyphInfoForName()
		self.assertEqual(str(Glyphs.glyphInfoForName('a')), "<GSGlyphInfo 'a'>")
		
		# GSApplication.glyphInfoForUnicode()
		self.assertEqual(str(Glyphs.glyphInfoForUnicode('0061')), "<GSGlyphInfo 'a'>")
		
		# GSApplication.niceGlyphName()
		self.assertEqual(Glyphs.niceGlyphName('a'), 'a')
		
		# GSApplication.productionGlyphName()
		self.assertEqual(Glyphs.productionGlyphName('a'), 'a')
		
		# GSApplication.ligatureComponents()
		self.assertEqual(len(list(Glyphs.ligatureComponents('allah-ar'))), 4)
		
		# GSApplication.redraw()
		Glyphs.redraw()
		
		# GSApplication.showNotification()
		Glyphs.showNotification('Glyphs Unit Test', 'Hello World')
		
		self.assertIsNotNone(Glyphs.localize({
			'en':  'Hello World',
			'de': u'Hallöle Welt',
			'fr':  'Bonjour tout le monde',
			'es':  'Hola Mundo',
			}))


	def test_GSFont(self):
		
		font = Glyphs.font
		self.assertIsNotNone(font.__repr__())
		
		## Attributes
		
		# GSFont.parent
		self.assertIn('GSDocument', str(font.parent))

		
		# GSFont.masters
		amount = len(font.masters)
		self.assertGreaterEqual(len(list(font.masters)), 1)
		newMaster = GSFontMaster()
		font.masters.append(newMaster)
		self.assertEqual(newMaster, font.masters[-1])
		del font.masters[-1]
		newMaster1 = GSFontMaster()
		newMaster2 = GSFontMaster()
		font.masters.extend([newMaster1, newMaster2])
		self.assertEqual(newMaster1, font.masters[-2])
		self.assertEqual(newMaster2, font.masters[-1])
		font.masters.remove(font.masters[-1])
		font.masters.remove(font.masters[-1])
		newMaster = GSFontMaster()
		font.masters.insert(0, newMaster)
		self.assertEqual(newMaster, font.masters[0])
		font.masters.remove(font.masters[0])
		self.assertEqual(amount, len(font.masters))

		# GSFont.instances
		amount = len(font.instances)
		self.assertGreaterEqual(len(list(font.instances)), 1)
		newInstance = GSInstance()
		font.instances.append(newInstance)
		self.assertEqual(newInstance, font.instances[-1])
		del font.instances[-1]
		newInstance1 = GSInstance()
		newInstance2 = GSInstance()
		font.instances.extend([newInstance1, newInstance2])
		self.assertEqual(newInstance1, font.instances[-2])
		self.assertEqual(newInstance2, font.instances[-1])
		font.instances.remove(font.instances[-1])
		font.instances.remove(font.instances[-1])
		newInstance = GSInstance()
		font.instances.insert(0, newInstance)
		self.assertEqual(newInstance, font.instances[0])
		font.instances.remove(font.instances[0])
		self.assertEqual(amount, len(font.instances))
		
		# GSFont.glyphs
		self.assertGreaterEqual(len(list(font.glyphs)), 1)
		self.assertEqual(font.glyphs[u'ä'], font.glyphs['adieresis'])
		self.assertEqual(font.glyphs['00E4'], font.glyphs['adieresis'])
		self.assertEqual(font.glyphs['00e4'], font.glyphs['adieresis'])

		# GSFont.classes
		font.classes = []
		amount = len(font.classes)
		font.classes.append(GSClass('uppercaseLetters', 'A'))
		self.assertIsNotNone(font.classes[-1].__repr__())
		self.assertEqual(len(font.classes), 1)
		self.assertIn('<GSClass "uppercaseLetters">', str(font.classes))
		self.assertIn('A', font.classes['uppercaseLetters'].code)
		del(font.classes['uppercaseLetters'])
		newClass1 = GSClass('uppercaseLetters1', 'A')
		newClass2 = GSClass('uppercaseLetters2', 'A')
		font.classes.extend([newClass1, newClass2 ])
		self.assertEqual(newClass1, font.classes[-2])
		self.assertEqual(newClass2, font.classes[-1])
		newClass = GSClass('uppercaseLetters3', 'A')
		font.classes.insert(0, newClass)
		self.assertEqual(newClass, font.classes[0])
		font.classes.remove(font.classes[-1])
		font.classes.remove(font.classes[-1])
		font.classes.remove(font.classes[0])
		self.assertEqual(len(font.classes), amount)
		
		# GSFont.features
		font.features = []
		amount = len(font.features)
		font.features.append(GSFeature('liga', 'sub f i by fi;'))
		self.assertIsNotNone(font.features['liga'].__repr__())
		self.assertEqual(len(font.features), 1)
		self.assertIn('<GSFeature "liga">', str(font.features))
		self.assertIn('sub f i by fi;', font.features['liga'].code)
		del(font.features['liga'])
		newFeature1 = GSFeature('liga', 'sub f i by fi;')
		newFeature2 = GSFeature('liga', 'sub f l by fl;')
		font.features.extend([newFeature1, newFeature2])
		self.assertEqual(newFeature1, font.features[-2])
		self.assertEqual(newFeature2, font.features[-1])
		newFeature = GSFeature('liga', 'sub f i by fi;')
		font.features.insert(0, newFeature)
		self.assertEqual(newFeature, font.features[0])
		font.features.remove(font.features[-1])
		font.features.remove(font.features[-1])
		font.features.remove(font.features[0])
		self.assertEqual(len(font.features), amount)
		
		# GSFont.featurePrefixes
		font.featurePrefixes = []
		amount = len(font.featurePrefixes)
		font.featurePrefixes.append(GSFeaturePrefix('LanguageSystems', 'languagesystem DFLT dflt;'))
		self.assertIsNotNone(font.featurePrefixes[-1].__repr__())
		self.assertEqual(len(font.featurePrefixes), 1)
		self.assertIn('<GSFeaturePrefix "LanguageSystems">', str(font.featurePrefixes))
		self.assertIn('languagesystem DFLT dflt;', font.featurePrefixes[-1].code)
		del(font.featurePrefixes['LanguageSystems'])
		newFeaturePrefix1 = GSFeaturePrefix('LanguageSystems1', 'languagesystem DFLT dflt;')
		newFeaturePrefix2 = GSFeaturePrefix('LanguageSystems2', 'languagesystem DFLT dflt;')
		font.featurePrefixes.extend([newFeaturePrefix1, newFeaturePrefix2 ])
		self.assertEqual(newFeaturePrefix1, font.featurePrefixes[-2])
		self.assertEqual(newFeaturePrefix2, font.featurePrefixes[-1])
		newFeaturePrefix = GSFeaturePrefix('LanguageSystems3', 'languagesystem DFLT dflt;')
		font.featurePrefixes.insert(0, newFeaturePrefix)
		self.assertEqual(newFeaturePrefix, font.featurePrefixes[0])
		font.featurePrefixes.remove(font.featurePrefixes[-1])
		font.featurePrefixes.remove(font.featurePrefixes[-1])
		font.featurePrefixes.remove(font.featurePrefixes[0])
		self.assertEqual(len(font.featurePrefixes), amount)
		
		# GSFont.copyright
		self.assertUnicode(font.copyright)
		
		# GSFont.designer
		self.assertUnicode(font.designer)
		
		# GSFont.designerURL
		self.assertUnicode(font.designerURL)
		
		# GSFont.manufacturer
		self.assertUnicode(font.manufacturer)
		
		# GSFont.manufacturerURL
		self.assertUnicode(font.manufacturerURL)
		
		# GSFont.versionMajor
		self.assertInteger(font.versionMajor)
		
		# GSFont.versionMinor
		self.assertInteger(font.versionMinor)
		
		# GSFont.date
		self.assertIsInstance(font.date, NSDate)
		
		# GSFont.familyName
		self.assertUnicode(font.familyName)
		
		# GSFont.upm
		self.assertInteger(font.upm)
		
		# GSFont.note
		self.assertUnicode(font.note)
		
		# GSFont.kerning
		self.assertIsInstance(dict(font.kerning), dict)
		
		# GSFont.userData
		# self.assertDict(font.userData)
		self.assertIsNone(font.userData["TestData"])
		font.userData["TestData"] = 42
		self.assertEqual(font.userData["TestData"], 42)
		del(font.userData["TestData"])
		self.assertIsNone(font.userData["TestData"])
		
		# GSFont.disablesNiceNames
		self.assertBool(font.disablesNiceNames)
		
		# GSFont.customParameters
		font.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'
		self.assertEqual(font.customParameters['trademark'], 'ThisFont is a trademark by MyFoundry.com')
		amount = len(list(font.customParameters))
		newParameter = GSCustomParameter('hello1', 'world1')
		font.customParameters.append(newParameter)
		self.assertEqual(newParameter, list(font.customParameters)[-1])
		del font.customParameters[-1]
		newParameter1 = GSCustomParameter('hello2', 'world2')
		newParameter2 = GSCustomParameter('hello3', 'world3')
		font.customParameters.extend([newParameter1, newParameter2])
		self.assertEqual(newParameter1, list(font.customParameters)[-2])
		self.assertEqual(newParameter2, list(font.customParameters)[-1])
		font.customParameters.remove(list(font.customParameters)[-1])
		font.customParameters.remove(list(font.customParameters)[-1])
		newParameter = GSCustomParameter('hello1', 'world1')
		font.customParameters.insert(0, newParameter)
		self.assertEqual(newParameter, list(font.customParameters)[0])
		font.customParameters.remove(list(font.customParameters)[0])
		self.assertEqual(amount, len(list(font.customParameters)))
		del(font.customParameters['trademark'])
		
		# GSFont.grid
		self.assertInteger(font.grid)
		
		# GSFont.gridSubDivisions
		self.assertInteger(font.gridSubDivisions)
		
		# GSFont.gridLength
		self.assertFloat(font.gridLength, readOnly = True)
		
		# GSFont.selection
		for glyph in font.glyphs:
			glyph.selected = False
		font.glyphs['a'].selected = True
		self.assertEqual(len(list(font.selection)), 1)
		for glyph in font.glyphs:
			glyph.selected = True
		self.assertEqual(len(list(font.selection)), len(font.glyphs))
		
		# GSFont.selectedLayers
		# GSFont.currentText
		# GSFont.tabs
		# GSFont.currentTab
		for tab in font.tabs:
			tab.close()
		tab = font.newTab('a')
		self.assertEqual(tab, font.tabs[-1])
		self.assertIsNotNone(font.currentTab.__repr__())
		self.assertEqual(len(list(font.selectedLayers)), 1)
		self.assertEqual(len(list(font.tabs)), 1)
		self.assertEqual(font.currentText, 'a')
		self.assertEqual(font.currentTab, font.tabs[-1])
		font.tabs[0].close()
		
		# GSFont.selectedFontMaster
		# GSFont.masterIndex
		oldMasterIndex = font.masterIndex
		for i in range(len(list(font.masters))):
			font.masterIndex = i
			self.assertEqual(font.selectedFontMaster, font.masters[i])
		font.masterIndex = oldMasterIndex
		
		# GSFont.filepath
		self.assertIsNotNone(font.filepath)
		
		# GSFont.tool
		# GSFont.tools
		oldTool = font.tool
		for toolName in font.tools:
			font.tool = toolName
			self.assertEqual(font.tool, toolName)
		font.tool = oldTool
		
		
		## Methods
		
		# GSFont.save()
		font.save()
		
		# GSFont.close()
		font.close()
		Glyphs.open(PathToTestFile)
		
		# GSFont.disableUpdateInterface()
		font.disableUpdateInterface()
		
		# GSFontselfenableUpdateInterface()
		font.enableUpdateInterface()
		
		# GSFont.setKerningForPair()
		font.setKerningForPair(font.masters[0].id, 'a', 'a', -10)
		
		# GSFont.kerningForPair()
		self.assertEqual(font.kerningForPair(font.masters[0].id, 'a', 'a'), -10)
		
		# GSFont.removeKerningForPair()
		font.removeKerningForPair(font.masters[0].id, 'a', 'a')

		# GSFont.updateFeatures()
		font.updateFeatures()


	def test_GSFontMaster(self):
		
		master = Glyphs.font.masters[0]
		self.assertIsNotNone(master.__repr__())
		
		# GSFontMaster.id
		self.assertIsNotNone(unicode(master.id))
		
		# GSFontMaster.name
		self.assertIsNotNone(str(master.name))
		self.assertIsNotNone(master.name)
		# GSFontMaster.weight
		self.assertIsNotNone(str(master.weight))
		
		# GSFontMaster.width
		self.assertIsNotNone(str(master.width))
		
		# GSFontMaster.weightValue
		self.assertFloat(master.weightValue)
		
		# GSFontMaster.widthValue
		self.assertFloat(master.widthValue)
		
		# GSFontMaster.customName
		self.assertString(master.customName)
		
		# GSFontMaster.customValue
		self.assertFloat(master.customValue)
		
		# GSFontMaster.ascender
		self.assertFloat(master.ascender)
		
		# GSFontMaster.capHeight
		self.assertFloat(master.capHeight)
		
		# GSFontMaster.xHeight
		self.assertFloat(master.xHeight)
		
		# GSFontMaster.descender
		self.assertFloat(master.descender)
		
		# GSFontMaster.italicAngle
		self.assertFloat(master.italicAngle)
		
		# GSFontMaster.verticalStems
		oldStems = master.verticalStems
		master.verticalStems = [10, 15, 20]
		self.assertEqual(len(list(master.verticalStems)), 3)
		master.verticalStems = oldStems
		
		# GSFontMaster.horizontalStems
		oldStems = master.horizontalStems
		master.horizontalStems = [10, 15, 20]
		self.assertEqual(len(list(master.horizontalStems)), 3)
		master.horizontalStems = oldStems
		
		# GSFontMaster.alignmentZones
		self.assertIsInstance(list(master.alignmentZones), list)
		
		# GSFontMaster.blueValues
		self.assertIsInstance(list(master.blueValues), list)
		
		# GSFontMaster.otherBlues
		self.assertIsInstance(list(master.otherBlues), list)
		
		# GSFontMaster.guides
		self.assertIsInstance(list(master.guides), list)
		master.guides = []
		self.assertEqual(len(master.guides), 0)
		newGuide = GSGuideLine()
		newGuide.position = NSPoint(100, 100)
		newGuide.angle = -10.0
		master.guides.append(newGuide)
		self.assertIsNotNone(master.guides[0].__repr__())
		self.assertEqual(len(master.guides), 1)
		del master.guides[0]
		self.assertEqual(len(master.guides), 0)

		
		# GSFontMaster.userData
		self.assertIsNotNone(master.userData)
		master.userData["TestData"] = 42
		self.assertEqual(master.userData["TestData"], 42)
		del(master.userData["TestData"])
		self.assertIsNone(master.userData["TestData"])
		
		# GSFontMaster.customParameters
		master.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'
		self.assertGreaterEqual(len(list(master.customParameters)), 1)
		del(master.customParameters['trademark'])
	
	def test_GSAlignmentZone(self):
		
		master = Glyphs.font.masters[0]
		
		master.alignmentZones = []
		self.assertEqual(len(master.alignmentZones), 0)
		master.alignmentZones.append(GSAlignmentZone(100, 10))
		self.assertIsNotNone(master.alignmentZones[-1].__repr__())
		self.assertEqual(len(master.alignmentZones), 1)
		self.assertEqual(master.alignmentZones[-1].position, 100)
		self.assertEqual(master.alignmentZones[-1].size, 10)
		del master.alignmentZones[-1]
		self.assertEqual(len(master.alignmentZones), 0)
	
	def test_GSInstance(self):
		
		instance = Glyphs.font.instances[0]
		self.assertIsNotNone(instance.__repr__())
		
		# GSInstance.active
		self.assertBool(instance.active, readOnly = True)
		
		# GSInstance.name
		self.assertString(instance.name)
		
		# GSInstance.weight
		self.assertString(instance.weight, readOnly = True)
		
		# GSInstance.width
		self.assertString(instance.width, readOnly = True)
		
		# GSInstance.weightValue
		self.assertFloat(instance.weightValue)
		
		# GSInstance.widthValue
		self.assertFloat(instance.widthValue)
		
		# GSInstance.customValue
		self.assertFloat(instance.customValue)
		
		# GSInstance.isItalic
		self.assertBool(instance.isItalic)
		
		# GSInstance.isBold
		self.assertBool(instance.isBold)
		
		# GSInstance.linkStyle
		self.assertString(instance.linkStyle)
		
		# GSInstance.familyName
		self.assertString(instance.familyName)
		
		# GSInstance.preferredFamily
		self.assertString(instance.preferredFamily)
		
		# GSInstance.preferredSubfamilyName
		self.assertString(instance.preferredSubfamilyName)
		
		# GSInstance.windowsFamily
		self.assertString(instance.windowsFamily)
		
		# GSInstance.windowsStyle
		self.assertString(instance.windowsStyle)
		
		# GSInstance.windowsLinkedToStyle
		self.assertString(instance.windowsLinkedToStyle)
		
		# GSInstance.fontName
		self.assertString(instance.fontName)
		
		# GSInstance.fullName
		self.assertString(instance.fullName)
		
		# GSInstance.customParameters
		instance.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'
		self.assertGreaterEqual(len(instance.customParameters), 1)
		del(instance.customParameters['trademark'])
		
		# GSInstance.instanceInterpolations
		self.assertIsInstance(dict(instance.instanceInterpolations), dict)
		
		# GSInstance.manualInterpolation
		self.assertBool(instance.manualInterpolation)
		
		# GSInstance.interpolatedFont
		self.assertIsInstance(instance.interpolatedFont, type(Glyphs.font))
		
		
		## Methods
		
		# GSInstance.generate()
		path = os.path.join(os.path.dirname(__file__), 'Glyphs Unit Test Sans.otf')
		self.assertEqual(instance.generate(FontPath = path), True)
		self.assertTrue(os.path.exists(path))
		if os.path.exists(path):
			os.remove(path)
			


	def test_GSGlyph(self):
		
		font = Glyphs.font
		font.glyphs['a'].duplicate('a.test')
		glyph = font.glyphs['a.test']

		# GSGlyph.parent
		self.assertEqual(glyph.parent, Glyphs.font)
		
		# GSGlyph.layers
		self.assertIsNotNone(glyph.layers)
		
		# GSGlyph.name
		self.assertUnicode(glyph.name)
		
		# GSGlyph.unicode
		self.assertUnicode(glyph.unicode)
		
		# GSGlyph.string
		if glyph.unicode:
			self.assertIsInstance(glyph.string, unicode)
		
		# GSGlyph.id
		self.assertIsInstance(glyph.id, str)
		
		# GSGlyph.category
		self.assertTrue(type(glyph.category) == unicode or type(glyph.category) == objc.pyobjc_unicode or type(glyph.category) == type(None))
		
		# GSGlyph.storeCategory
		self.assertBool(glyph.storeCategory)
		
		# GSGlyph.subCategory
		self.assertTrue(type(glyph.subCategory) == unicode or type(glyph.category) == objc.pyobjc_unicode or type(glyph.subCategory) == type(None))
		
		# GSGlyph.storeSubCategory
		self.assertBool(glyph.storeSubCategory)
		
		# GSGlyph.script
		self.assertTrue(type(glyph.category) == unicode or type(glyph.category) == objc.pyobjc_unicode or type(glyph.category) == type(None))
		
		# GSGlyph.storeScript
		self.assertBool(glyph.storeScript)
		
		# GSGlyph.productionName
		self.assertTrue(type(glyph.productionName) == unicode or type(glyph.category) == objc.pyobjc_unicode or type(glyph.productionName) == type(None))
		
		# GSGlyph.storeProductionName
		self.assertBool(glyph.storeProductionName)
		
		# GSGlyph.glyphInfo
		self.assertTrue(glyph.glyphInfo != None or glyph.glyphInfo == None)
		
		# GSGlyph.leftKerningGroup
		self.assertUnicode(glyph.leftKerningGroup)
		
		# GSGlyph.rightKerningGroup
		self.assertUnicode(glyph.rightKerningGroup)
		
		# GSGlyph.leftKerningKey
		self.assertString(glyph.leftKerningKey)
		
		# GSGlyph.rightKerningKey
		self.assertString(glyph.rightKerningKey)

		# GSGlyph.leftMetricsKey
		self.assertUnicode(glyph.leftMetricsKey)
		
		# GSGlyph.rightMetricsKey
		self.assertUnicode(glyph.rightMetricsKey)
		
		# GSGlyph.widthMetricsKey
		self.assertUnicode(glyph.widthMetricsKey)
		
		# GSGlyph.export
		self.assertBool(glyph.export)
		
		# GSGlyph.color
		self.assertInteger(glyph.color)
		
		# GSGlyph.colorObject
		glyph.color = 1
		self.assertIsInstance(glyph.colorObject, NSColor)
		
		# GSGlyph.note
		self.assertUnicode(glyph.note)
		
		# GSGlyph.selected
		self.assertBool(glyph.selected)
		
		# GSGlyph.mastersCompatible
		self.assertIsInstance(glyph.mastersCompatible, bool)
		
		# GSGlyph.userData
		self.assertDict(glyph.userData)
		
		# GSGlyph.smartComponentAxes
		# postponed to its own test
		
		# GSGlyph.lastChange
		glyph.name = "a.test2"
		self.assertIsInstance(glyph.lastChange, float)
		glyph.name = "a.test1"
		## Methods
		glyph.beginUndo()
		glyph.endUndo()
		glyph.updateGlyphInfo()

		
		# Delete glyph
		del Glyphs.font.glyphs['a.test']
	

	def test_GSLayer(self):

		
		layer = Glyphs.font.glyphs['a'].layers[0]
		self.assertIsNotNone(layer.__repr__())

		# GSLayer.parent
		self.assertEqual(layer.parent, Glyphs.font.glyphs['a'])
		
		# GSLayer.name
		self.assertUnicode(layer.name)

		# GSLayer.associatedMasterId
		self.assertEqual(layer.associatedMasterId, Glyphs.font.masters[0].id)

		# GSLayer.layerId
		self.assertEqual(layer.layerId, Glyphs.font.masters[0].id)
		
		# GSLayer.color
		self.assertString(layer.color)
		
		# GSLayer.colorObject
		layer.color = 1
		self.assertIsInstance(layer.colorObject, NSColor)
		
		# GSLayer.components
		# -> own test

		# GSLayer.guides
		self.assertIsInstance(list(layer.guides), list)
		layer.guides = []
		self.assertEqual(len(layer.guides), 0)
		newGuide = GSGuideLine()
		newGuide.position = NSPoint(100, 100)
		newGuide.angle = -10.0
		layer.guides.append(newGuide)
		self.assertIsNotNone(layer.guides[0].__repr__())
		self.assertEqual(len(layer.guides), 1)
		del layer.guides[0]
		self.assertEqual(len(layer.guides), 0)

		# GSLayer.annotations
		layer.annotations = []
		self.assertEqual(len(layer.annotations), 0)
		newAnnotation = GSAnnotation()
		newAnnotation.type = TEXT
		newAnnotation.text = 'Fuck, this curve is ugly!'
		layer.annotations.append(newAnnotation)
		self.assertIsNotNone(layer.annotations[0].__repr__())
		self.assertEqual(len(layer.annotations), 1)
		del layer.annotations[0]
		self.assertEqual(len(layer.annotations), 0)

		# GSLayer.hints
		layer = Glyphs.font.glyphs['a'].layers[0]
		layer.hints = []
		self.assertEqual(len(layer.hints), 0)
		newHint = GSHint()
		newHint.originNode = layer.paths[0].nodes[0]
		newHint.targetNode = layer.paths[0].nodes[1]
		newHint.type = STEM
		layer.hints.append(newHint)
		self.assertIsNotNone(layer.hints[0].__repr__())
		self.assertEqual(len(layer.hints), 1)
		del layer.hints[0]
		self.assertEqual(len(layer.hints), 0)

		# GSLayer.anchors
		if layer.anchors['top']:
			oldPosition = layer.anchors['top'].position
		else:
			oldPosition = None
		layer.anchors['top'] = GSAnchor()
		self.assertGreaterEqual(len(layer.anchors), 1)
		self.assertIsNotNone(layer.anchors['top'].__repr__())
		layer.anchors['top'].position = NSPoint(100, 100)
		del layer.anchors['top']
		layer.anchors['top'] = GSAnchor()
		layer.anchors['top'].position = oldPosition
		self.assertString(layer.anchors['top'].name)

		# GSLayer.paths
		# postponed to own test
		
		# GSLayer.selection
		layer.selection = []
		self.assertEqual(len(layer.selection), 0)
		selection = 0
		for path in layer.paths:
			path.selected = True
			selection += len(path.nodes)
		for anchor in layer.anchors:
			anchor.selected = True
			selection += 1
		self.assertEqual(len(layer.selection), selection)
		layer.clearSelection()
		self.assertEqual(len(layer.selection), 0)

		
		# GSLayer.LSB
		self.assertFloat(layer.LSB)
		
		# GSLayer.RSB
		self.assertFloat(layer.RSB)

		# GSLayer.TSB
		self.assertFloat(layer.TSB)

		# GSLayer.BSB
		self.assertFloat(layer.BSB)

		# GSLayer.width
		self.assertFloat(layer.width)

		# GSLayer.leftMetricsKey
		self.assertUnicode(layer.leftMetricsKey)

		# GSLayer.rightMetricsKey
		self.assertUnicode(layer.rightMetricsKey)

		# GSLayer.widthMetricsKey
		self.assertUnicode(layer.widthMetricsKey)

		# GSLayer.bounds
		self.assertIsInstance(layer.bounds, NSRect)

		# GSLayer.selectionBounds
		self.assertIsInstance(layer.selectionBounds, NSRect)

		# GSLayer.background
		self.assertIn('GSBackgroundLayer', layer.background.__repr__())
		
		# GSLayer.backgroundImage
		# postponed to its own test

		# GSLayer.bezierPath
		self.assertIsInstance(layer.bezierPath, NSBezierPath)

		# GSLayer.openBezierPath
		self.assertIsInstance(layer.openBezierPath, NSBezierPath)

		# GSLayer.completeBezierPath
		self.assertIsInstance(layer.completeBezierPath, NSBezierPath)

		# GSLayer.completeOpenBezierPath
		self.assertIsInstance(layer.completeOpenBezierPath, NSBezierPath)

		# GSLayer.userData
		layer.userData["Hallo"] = "Welt"
		self.assertDict(layer.userData)


		## Methods
		decomposedLayer = layer.copyDecomposedLayer()
		self.assertGreaterEqual(decomposedLayer.paths, 1)
		
		layer = Glyphs.font.glyphs['adieresis'].layers[0]
		layer.decomposeComponents()
		self.assertGreaterEqual(layer.paths, 1)

		self.assertString(layer.compareString())
		
		layer.connectAllOpenPaths()
		
		layer.syncMetrics()

		layer.correctPathDirection()

		layer.removeOverlap()

		layer.roundCoordinates()

		layer.addNodesAtExtremes()

		layer.applyTransform(NSAffineTransformStruct(
					0.5, # x scale factor
					0.0, # x skew factor
					0.0, # y skew factor
					0.5, # y scale factor
					0.0, # x position
					0.0  # y position
					))

		layer.beginChanges()

		layer.endChanges()

		layer.cutBetweenPoints(NSPoint(0, 100), NSPoint(layer.width, 100))

		intersections = layer.intersectionsBetweenPoints((-1000, 100), (layer.width+1000, 100))

		layer.addMissingAnchors()
		
		#layer.clearSelection()
		# already tested
		
		layer.swapForegroundWithBackground()
		layer.swapForegroundWithBackground()

		layer.reinterpolate()

		layer.clear()
		
		
		
	def test_smartComponents(self):
		
		glyph = Glyphs.font.glyphs['_part.shoulder']
		
		glyph.smartComponentAxes = []
		self.assertEqual(len(glyph.smartComponentAxes), 0)
		
		# Add axes
		
		axis1 = GSSmartComponentAxis()
		axis1.name = 'crotchDepth'
		axis1.topValue = 0
		axis1.bottomValue = -100
		glyph.smartComponentAxes.append(axis1)

		axis2 = GSSmartComponentAxis()
		axis2.name = 'shoulderWidth'
		axis2.topValue = 100
		axis2.bottomValue = 0
		glyph.smartComponentAxes.append(axis2)

		self.assertEqual(len(glyph.smartComponentAxes), 2)
		
		# Map to poles

		for layer in glyph.layers:
			
			# NarrowShoulder layer
			if layer.name == 'NarrowShoulder':
				layer.smartComponentPoleMapping['crotchDepth'] = 2
				layer.smartComponentPoleMapping['shoulderWidth'] = 1

			# LowCrotch layer
			elif layer.name == 'LowCrotch':
				layer.smartComponentPoleMapping['crotchDepth'] = 1
				layer.smartComponentPoleMapping['shoulderWidth'] = 2

			# normal layer
			else:
				layer.smartComponentPoleMapping['crotchDepth'] = 2
				layer.smartComponentPoleMapping['shoulderWidth'] = 2
		layer = Glyphs.font.glyphs['n'].layers[0]
		layer.components[0].smartComponentValues['shoulderWidth'] = 30
		layer.components[0].smartComponentValues['crotchDepth'] = -77



	def test_GSComponent(self):
		
		
		Glyphs.font.glyphs['adieresis'].duplicate('adieresis.test')
		
		glyph = Glyphs.font.glyphs['adieresis.test']
		layer = glyph.layers[0]
		component = layer.components[0]
		self.assertIsNotNone(component.__repr__())

		# Delete and add
		self.assertEqual(len(layer.components), 2)
		layer.components = []
		self.assertEqual(len(layer.components), 0)
		layer.components.append(GSComponent('a'))
		self.assertIsNotNone(layer.components[0].__repr__())
		self.assertEqual(len(layer.components), 1)
		layer.components.append(GSComponent('dieresis'))
		self.assertEqual(len(layer.components), 2)
		layer.components = [GSComponent('a'), GSComponent('dieresis')]
		self.assertEqual(len(layer.components), 2)


		# GSComponent.position
		self.assertIsInstance(component.position, NSPoint)

		# GSComponent.scale
		self.assertTrue(type(component.scale) == float or type(component.scale) == tuple)
		
		# GSComponent.rotation
		self.assertFloat(component.rotation)

		# GSComponent.componentName
		# GSComponent.component
		# GSComponent.layer
		component.componentName = 'A'
		self.assertEqual(component.component, Glyphs.font.glyphs['A'])
# not defined yet		self.assertEqual(component.layer, Glyphs.font.glyphs['A'].layers[layer.layerId])
		component.componentName = 'a'
		self.assertEqual(component.component, Glyphs.font.glyphs['a'])
# not defined yet		self.assertEqual(component.layer, Glyphs.font.glyphs['a'].layers[layer.layerId])

		component = layer.components[0]

		# GSComponent.transform
		component.transform = (1.0, 0, 0, 1.0, 0, 0)

		# GSComponent.bounds
		self.assertIsInstance(component.bounds, NSRect)

		# GSComponent.automaticAlignment
		self.assertBool(component.automaticAlignment)

		# GSComponent.anchor
		self.assertUnicode(component.anchor)

		# GSComponent.selected
		self.assertBool(component.selected)
		
		# GSComponent.smartComponentValues
		# -> see test_smartComponents()
		
		# GSComponent.bezierPath
		self.assertIsInstance(component.bezierPath, NSBezierPath)

		## Methods
		component.applyTransform((.5, 0, 0, .5, 0, 0))
		component.decompose()
		
		del Glyphs.font.glyphs['adieresis.test']
		
		
	def test_GSPath(self):
		
		layer = Glyphs.font.glyphs['a'].layers[0]
		path = layer.paths[0]
		self.assertIsNotNone(path.__repr__())
		
		# GSPath.parent
		self.assertEqual(path.parent, Glyphs.font.glyphs['a'].layers[0])

		# GSPath.nodes
		amount = len(path.nodes)
		self.assertIsNotNone(list(path.nodes))
		newNode = GSNode(NSPoint(20,20))
		path.nodes.append(newNode)
		self.assertEqual(newNode, path.nodes[-1])
		del path.nodes[-1]
		newNode = GSNode(NSPoint(20,20))
		path.nodes.insert(0, newNode)
		self.assertEqual(newNode, path.nodes[0])
		path.nodes.remove(path.nodes[0])
		newNode1 = GSNode(NSPoint(10,10))
		newNode2 = GSNode(NSPoint(20,20))
		path.nodes.extend([newNode1, newNode2])
		self.assertEqual(newNode1, path.nodes[-2])
		self.assertEqual(newNode2, path.nodes[-1])
		del path.nodes[-2]
		del path.nodes[-1]
		self.assertEqual(amount, len(path.nodes))

		# GSPath.segments
		self.assertIsNotNone(list(path.segments))

		# GSPath.closed
		self.assertBool(path.closed, readOnly = True)

		# GSPath.direction
		self.assertTrue(path.direction == 1 or path.direction == -1)

		# GSPath.bounds
		self.assertIsInstance(path.bounds, NSRect)

		# GSPath.closed
		self.assertBool(path.selected)

		# GSPath.bounds
		self.assertIsInstance(path.bezierPath, NSBezierPath)

		## Methods

		path.reverse()
		path.reverse()
		path.addNodesAtExtremes()
		path.applyTransform([
					1.0, # x scale factor
					0.0, # x skew factor
					0.0, # y skew factor
					1.0, # y scale factor
					0.0, # x position
					0.0  # y position
					])


	def test_GSNode(self):
		
		layer = Glyphs.font.glyphs['a'].layers[0]
		path = layer.paths[0]
		node = path.nodes[0]
		self.assertIsNotNone(node.__repr__())
		
		# GSNode.position
		self.assertIsInstance(node.position, NSPoint)

		# GSNode.type
		self.assertTrue(node.type in [LINE, CURVE, OFFCURVE])
		
		# GSNode.smooth
		self.assertBool(node.smooth)

		# GSNode.selected
		self.assertBool(node.selected)

		# GSNode.index
		self.assertInteger(node.index, readOnly = True)
		self.assertNotEqual(node.index, 9223372036854775807) # theoretically, this value could be maxint in a node, but in our test font it should be 0, I guess (taken from actual glyph, not orphan path)

		# GSNode.nextNode
		self.assertIsInstance(node.nextNode, GSNode)

		# GSNode.prevNode
		self.assertIsInstance(node.prevNode, GSNode)

		# GSNode.name
		self.assertUnicode(node.name)
		
		## Methods

		node.makeNodeFirst()
		node.toggleConnection()



	def test_GSBackgroundImage(self):

		glyph = Glyphs.font.glyphs['A']
		layer = glyph.layers[0]
		
		layer.backgroundImage = GSBackgroundImage(os.path.join(os.path.dirname(PathToTestFile), 'A.jpg'))
		image = layer.backgroundImage
		self.assertIsNotNone(image.__repr__())
		
		
		# GSBackgroundImage.path
		self.assertEqual(image.path, os.path.abspath(os.path.join(os.path.dirname(PathToTestFile), 'A.jpg')))
		
		# GSBackgroundImage.image
		self.assertIsInstance(image.image, NSImage)
		
		# GSBackgroundImage.crop
		self.assertIsInstance(image.crop, NSRect)
		image.crop = NSRect(NSPoint(0, 0), NSPoint(100, 100))
		
		# GSBackgroundImage.locked
		self.assertBool(image.locked)
		
		# GSBackgroundImage.alpha
		self.assertInteger(image.alpha)
		
		# GSBackgroundImage.position
		self.assertIsInstance(image.position, NSPoint)

		# GSBackgroundImage.scale
		self.assertTrue(type(image.scale) == float or type(image.scale) == tuple)

		# GSBackgroundImage.rotation
		self.assertFloat(image.rotation)
		
		## Methods
		
		image.resetCrop()
		image.scaleWidthToEmUnits(layer.width)
		
		layer.backgroundImage = None


	def test_GSEditViewController(self):
		
		font = Glyphs.font
		tab = font.newTab('a')
		self.assertIsNotNone(tab.__repr__())
		
		# GSEditViewController.parent
		self.assertEqual(tab.parent, Glyphs.font)

		# GSEditViewController.text
		self.assertEqual(tab.text, 'a')

		# GSEditViewController.layers
		self.assertEqual(list(tab.layers), [Glyphs.font.glyphs['a'].layers[0]])
		tab.layers = [Glyphs.font.glyphs['a'].layers[0]]
		tab.layers.append(Glyphs.font.glyphs['A'].layers[0])
		tab.layers.remove(Glyphs.font.glyphs['A'].layers[0])
		self.assertEqual(list(tab.layers), [Glyphs.font.glyphs['a'].layers[0]])

		# GSEditViewController.composedLayers
		font.updateFeatures()
		self.assertEqual(list(tab.composedLayers), [Glyphs.font.glyphs['a'].layers[0]])
		tab.features = ['smcp']
		self.assertEqual(list(tab.composedLayers), [Glyphs.font.glyphs['a.sc'].layers[0]])
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
		font.features.append(GSFeature('liga', 'sub a by A;'))
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
		self.assertEqual(tab.previewHeight, 100)
		tab.previewHeight = 0
		self.assertEqual(tab.previewHeight, 0)

		# GSEditViewController.bottomToolbarHeight
		self.assertTrue(tab.bottomToolbarHeight > 0)

		
		# GSEditViewController.userData
		tab.userData['a'] = 'b'
		self.assertTrue(tab.userData['a'] == 'b')

		## Methods
		
		# GSEditViewController.saveToPDF()
		tab.saveToPDF(os.path.join(os.path.dirname(font.filepath), 'Unit Test.pdf'))

		# GSEditViewController.close()
		tab.close()



	def test_GSGlyphInfo(self):

		info = Glyphs.font.glyphs['a'].glyphInfo
		self.assertIsNotNone(info.__repr__())

		# GSGlyphInfo.name
		self.assertEqual(info.name, 'a')

		# GSGlyphInfo.productionName
		self.assertEqual(info.productionName, None)

		# GSGlyphInfo.category
		self.assertEqual(info.category, 'Letter')

		# GSGlyphInfo.subCategory
		self.assertEqual(info.subCategory, 'Lowercase')

		# GSGlyphInfo.components
		self.assertEqual(info.subCategory, 'Lowercase')

		# GSGlyphInfo.components
		info = Glyphs.font.glyphs['adieresis'].glyphInfo
		self.assertIsInstance(list(info.components), list)

		# GSGlyphInfo.accents
		info = Glyphs.font.glyphsInfo().glyphInfoForName_('lam_alef-ar')
		self.assertIsInstance(list(info.accents), list)

		# GSGlyphInfo.anchors
		self.assertIsInstance(list(info.anchors), list)

		# GSGlyphInfo.unicode
		self.assertEqual(info.unicode, 'FEFB')

		# GSGlyphInfo.unicode2
		self.assertIsNone(info.unicode2())

		# GSGlyphInfo.index
		self.assertIsInstance(info.index, int)
		
		# GSGlyphInfo.sortName
		self.assertEqual(info.sortName, "ar0010_ar0009")

		# GSGlyphInfo.sortNameKeep
		self.assertEqual(info.sortNameKeep, "ar0900_ar0009")

		# GSGlyphInfo.desc
#		self.assertEqual(info.desc, "ARABIC LIGATURE LAM WITH ALEF ISOLATED FORM")

		# GSGlyphInfo.altNames
		self.assertEqual(info.altNames[0], "lamalefisolatedarabic")


	def not_test_Methods(self):

		# divideCurve()
		self.assertEqual(len(divideCurve(
			NSPoint(0, 0),
			NSPoint(50, 0),
			NSPoint(100, 50),
			NSPoint(100, 100),
			.5
			)), 7)

		# distance()
		self.assertEqual(distance(NSPoint(0, 0), NSPoint(0, 2)), 2.0)

		# addPoints()
		self.assertEqual(addPoints(NSPoint(0, 0), NSPoint(1, 2)), NSPoint(1, 2))

		# scalePoint()
		self.assertEqual(scalePoint(NSPoint(2, 2), 2), NSPoint(4, 4))

		GetSaveFile(filetypes = ['glyphs'])
		GetOpenFile()
		GetFolder()
		Message('Title', 'Message')
		LogToConsole('Message')
		LogError('Error message created in test code. Ignore it.')


	def test_Constants(self):

		self.assertIsNotNone(LINE)
		self.assertIsNotNone(CURVE)
		self.assertIsNotNone(OFFCURVE)

		self.assertIsNotNone(GSSHARP)
		self.assertIsNotNone(GSSMOOTH)

		self.assertIsNotNone(TOPGHOST)
		self.assertIsNotNone(STEM)
		self.assertIsNotNone(BOTTOMGHOST)
		self.assertIsNotNone(TTANCHOR)
		self.assertIsNotNone(TTSTEM)
		self.assertIsNotNone(TTALIGN)
		self.assertIsNotNone(TTINTERPOLATE)
		self.assertIsNotNone(TTDIAGONAL)
		self.assertIsNotNone(TTDELTA)
		self.assertIsNotNone(CORNER)
		self.assertIsNotNone(CAP)

		self.assertIsNotNone(TTROUND)
		self.assertIsNotNone(TTROUNDUP)
		self.assertIsNotNone(TTROUNDDOWN)
		self.assertIsNotNone(TTDONTROUND)
		self.assertIsNotNone(TRIPLE)

		self.assertIsNotNone(APP_MENU)
		self.assertIsNotNone(FILE_MENU)
		self.assertIsNotNone(EDIT_MENU)
		self.assertIsNotNone(GLYPH_MENU)
		self.assertIsNotNone(PATH_MENU)
		self.assertIsNotNone(FILTER_MENU)
		self.assertIsNotNone(VIEW_MENU)
		self.assertIsNotNone(SCRIPT_MENU)
		self.assertIsNotNone(WINDOW_MENU)
		self.assertIsNotNone(HELP_MENU)

		self.assertIsNotNone(DRAWFOREGROUND)
		self.assertIsNotNone(DRAWBACKGROUND)
		self.assertIsNotNone(DRAWINACTIVE)
		self.assertIsNotNone(DOCUMENTOPENED)
		self.assertIsNotNone(DOCUMENTACTIVATED)
		self.assertIsNotNone(DOCUMENTWASSAVED)
		self.assertIsNotNone(DOCUMENTCLOSED)
		self.assertIsNotNone(TABDIDOPEN)
		self.assertIsNotNone(TABWILLCLOSE)
		self.assertIsNotNone(UPDATEINTERFACE)
		self.assertIsNotNone(MOUSEMOVED)


sys.argv = ["GlyphsAppTests"]

if __name__ == '__main__':
	unittest.main(exit=False, failfast=False)
