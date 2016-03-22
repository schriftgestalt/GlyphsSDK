#MenuTitle: Glyphs.app Unit Tests
# -*- coding: utf-8 -*-

#import GlyphsApp
#reload(GlyphsApp) 

import unittest

import GlyphsApp
from GlyphsApp import *
import os, time

PathToTestFile = "/Users/georg/Programmierung/GlyphsSDK/ObjectWrapper/Unit Test/Glyphs Unit Test Sans.glyphs"

class GlyphsAppTests(unittest.TestCase):
	
	def assertString(self, stringObject, assertType = True):
		if assertType:
			self.assertIsInstance(str(stringObject), str)
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
	
	def assertInteger(self, intObject, assertType = True):
		if assertType:
			assert type(int(intObject)) == int
		oldValue = intObject
		intObject = 1
		self.assertEqual(intObject, 1)
		intObject = oldValue
	
	def assertFloat(self, floatObject, assertType = True):
		if assertType:
			self.assertIsInstance(float(floatObject), float)
		oldValue = floatObject
		floatObject = .5
		self.assertEqual(floatObject, .5)
		floatObject = oldValue
	
	def assertUnicode(self, unicodeObject, assertType = True):
		if assertType:
			assert unicode(unicodeObject)
		oldValue = unicodeObject
		unicodeObject = u'Ə'
		self.assertEqual(unicodeObject, u'Ə')
		unicodeObject = oldValue
	
	def assertBool(self, boolObject, assertType = True):
		if assertType:
			assert type(boolObject) == bool
		oldValue = boolObject
		boolObject = not boolObject
		self.assertEqual(boolObject, (not oldValue))
		boolObject = oldValue
	
	def setUp(self):
		if Glyphs.font is None:
			Glyphs.open(PathToTestFile)
	
	def test_GSApplication(self):
		
		# Main object
		self.assertIsNotNone(Glyphs)
		
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
		
		assert len(Glyphs.activeReporters) == len(Glyphs.reporters)
		# deactivate all reporters
		for reporter in Glyphs.reporters:
			Glyphs.deactivateReporter(reporter)
		self.assertEqual(len(Glyphs.activeReporters), 0)
		
		# GSApplication.defaults
		self.assertDict(Glyphs.defaults, assertType = False)
		
		# GSApplication.scriptAbbrevations
		self.assertIsNotNone(dict(Glyphs.scriptAbbrevations))
		
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
		assert str(Glyphs.versionString)
		
		# GSApplication.versionNumber
		assert float(Glyphs.versionNumber)
		
		# GSApplication.buildNumber
		assert int(Glyphs.buildNumber)
		
		## Methods
		
		# GSApplication.showGlyphInfoPanelWithSearchString()
		Glyphs.showGlyphInfoPanelWithSearchString('a')
		
		# GSApplication.glyphInfoForName()
		assert str(Glyphs.glyphInfoForName('a')) == "<GSGlyphInfo 'a'>"
		
		# GSApplication.glyphInfoForUnicode()
		assert str(Glyphs.glyphInfoForUnicode('0061')) == "<GSGlyphInfo 'a'>"
		
		# GSApplication.niceGlyphName()
		assert Glyphs.niceGlyphName('a') == 'a'
		
		# GSApplication.productionGlyphName()
		assert Glyphs.productionGlyphName('a') == 'a'
		
		# GSApplication.ligatureComponents()
		assert len(list(Glyphs.ligatureComponents('allah-ar'))) == 4
		
		# GSApplication.redraw()
		Glyphs.redraw()
		
		# GSApplication.showNotification()
		Glyphs.showNotification('Glyphs Unit Test', 'Hello World')
		
		assert Glyphs.localize({
			'en':  'Hello World',
			'de': u'Hallöle Welt',
			'fr':  'Bonjour tout le monde',
			'es':  'Hola Mundo',
			})


	def test_GSFont(self):
		
		font = Glyphs.font
		
		## Attributes
		
		# GSFont.parent
		assert 'GSDocument' in str(font.parent)
		
		# GSFont.masters
		assert len(list(font.masters)) >= 1
		
		# GSFont.instances
		assert len(list(font.instances)) >= 1
		
		# GSFont.glyphs
		assert len(list(font.glyphs)) >= 1
		
		# GSFont.classes
		font.classes.append(GlyphsApp.GSClass('uppercaseLetters', 'A'))
		assert 'uppercaseLetters' in str(font.classes)
		assert 'A' in font.classes['uppercaseLetters'].code
		del(font.classes['uppercaseLetters'])
		
		# GSFont.features
		font.features.append(GlyphsApp.GSFeature('liga', 'sub f i by fi;'))
		assert '<GSFeature "liga">' in str(font.features)
		assert 'sub f i by fi;' in font.features['liga'].code
		del(font.features['liga'])
		
		# GSFont.featurePrefixes
		font.featurePrefixes.append(GlyphsApp.GSFeaturePrefix('LanguageSystems', 'languagesystem DFLT dflt;'))
		assert 'LanguageSystems' in str(font.featurePrefixes)
		assert 'languagesystem DFLT dflt;' in font.featurePrefixes['LanguageSystems'].code
		del(font.featurePrefixes['LanguageSystems'])
		
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
		assert font.date
		
		# GSFont.familyName
		self.assertUnicode(font.familyName)
		
		# GSFont.upm
		self.assertInteger(font.upm)
		
		# GSFont.note
		self.assertUnicode(font.note)
		
		# GSFont.kerning
		assert dict(font.kerning)
		
		# GSFont.userData
		self.assertDict(font.userData)
		
		# GSFont.disablesNiceNames
		self.assertBool(font.disablesNiceNames)
		
		# GSFont.customParameters
		font.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'
		assert len(list(font.customParameters)) >= 1
		del(font.customParameters['trademark'])
		
		# GSFont.grid
		self.assertInteger(font.grid)
		
		# GSFont.gridSubDivisions
		self.assertInteger(font.gridSubDivisions)
		
		# GSFont.gridLength
		assert type(font.gridLength) == float
		
		# GSFont.selection
		for glyph in font.glyphs:
			glyph.selected = False
		font.glyphs['a'].selected = True
		assert len(list(font.selection)) == 1
		
		# GSFont.selectedLayers
		# GSFont.currentText
		# GSFont.tabs
		# GSFont.currentTab
		font.newTab('a')
		assert len(list(font.selectedLayers)) == 1
		assert len(list(font.tabs)) >= 1
		assert font.currentText == 'a'
		assert font.currentTab == font.tabs[-1]
		font.tabs[0].close()
		
		# GSFont.selectedFontMaster
		# GSFont.masterIndex
		oldMasterIndex = font.masterIndex
		for i in range(len(list(font.masters))):
			font.masterIndex = i
			assert font.selectedFontMaster == font.masters[i]
		font.masterIndex = oldMasterIndex
		
		# GSFont.filepath
		assert font.filepath
		
		# GSFont.tool
		# GSFont.tools
		oldTool = font.tool
		for toolName in font.tools:
			font.tool = toolName
			assert font.tool == toolName
		font.tool = oldTool
		
		
		## Methods
		
		# GSFont.save()
		font.save()
		
		# GSFont.close()
		font.close()
		Glyphs.open(os.path.join(os.path.dirname(__file__), 'Glyphs Unit Test Sans.glyphs'))
		Glyphs.showMacroWindow()
		
		# GSFont.disableUpdateInterface()
		font.disableUpdateInterface()
		
		# GSFontselfenableUpdateInterface()
		font.enableUpdateInterface()
		
		# GSFont.setKerningForPair()
		font.setKerningForPair(font.masters[0].id, 'a', 'a', -10)
		
		# GSFont.kerningForPair()
		assert font.kerningForPair(font.masters[0].id, 'a', 'a') == -10
		
		# GSFont.removeKerningForPair()
		font.removeKerningForPair(font.masters[0].id, 'a', 'a')


	def test_GSFontMaster(self):
		
		master = Glyphs.font.masters[0]
		
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
		
		# GSFontMaster.userData
		self.assertDict(master.userData)
		
		# GSFontMaster.customParameters
		master.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'
		assert len(list(master.customParameters)) >= 1
		del(master.customParameters['trademark'])
	
	def test_GSAlignmentZone(self):
		
		master = Glyphs.font.masters[0]
		
		master.alignmentZones.append(GlyphsApp.GSAlignmentZone(100, 10))
		self.assertEqual(master.alignmentZones[-1].position, 100)
		self.assertEqual(master.alignmentZones[-1].size, 10)
		del master.alignmentZones[-1]
	
	def test_GSInstance(self):
		
		instance = Glyphs.font.instances[0]
		
		# GSInstance.active
		self.assertIsInstance(instance.active, bool)
		
		# GSInstance.name
		self.assertString(instance.name)
		
		# GSInstance.weight
		assert str(instance.weight)
		
		# GSInstance.width
		assert str(instance.width)
		
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
		assert str(instance.windowsStyle)
		
		# GSInstance.windowsLinkedToStyle
		assert str(instance.windowsLinkedToStyle)
		
		# GSInstance.fontName
		self.assertString(instance.fontName)
		
		# GSInstance.fullName
		self.assertString(instance.fullName)
		
		# GSInstance.customParameters
		instance.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'
		self.assertGreater(len(instance.customParameters), 0)
		del(instance.customParameters['trademark'])
		
		# GSInstance.instanceInterpolations
		self.assertIsInstance(dict(instance.instanceInterpolations), dict)
		
		# GSInstance.manualInterpolation
		self.assertBool(instance.manualInterpolation)
		
		# GSInstance.interpolatedFont
		self.assertIsInstance(instance.interpolatedFont, type(Glyphs.font))
		
		
		## Methods
		
		# GSInstance.generate()
		assert instance.generate(FontPath = os.path.join(os.path.dirname(__file__), 'Glyphs Unit Test Sans.otf')) == True


	def test_GSGlyph(self):
		
		glyph = GlyphsApp.GSGlyph()
		glyph.name = 'test'
		Glyphs.font.glyphs.append(glyph)
		
		# GSGlyph.parent
		assert glyph.parent == Glyphs.font
		
		# GSGlyph.layers
		glyph.layers = Glyphs.font.glyphs['a'].layers
		
		# GSGlyph.name
		self.assertUnicode(glyph.name)
		
		# GSGlyph.unicode
		self.assertUnicode(glyph.unicode)
		
		# GSGlyph.string
		if glyph.unicode:
			assert type(glyph.string) == unicode
		
		# GSGlyph.id
		assert type(glyph.id) == str
		
		# GSGlyph.category
		assert type(glyph.category) == unicode or type(glyph.category) == type(None)
		
		# GSGlyph.storeCategory
		self.assertBool(glyph.storeCategory)
		
		# GSGlyph.subCategory
		assert type(glyph.subCategory) == unicode or type(glyph.subCategory) == type(None)
		
		# GSGlyph.storeSubCategory
		self.assertBool(glyph.storeSubCategory)
		
		# GSGlyph.script
		assert type(glyph.script) == unicode or type(glyph.script) == type(None)
		
		# GSGlyph.storeScript
		self.assertBool(glyph.storeScript)
		
		# GSGlyph.productionName
		assert type(glyph.productionName) == unicode or type(glyph.productionName) == type(None)
		
		# GSGlyph.storeProductionName
		self.assertBool(glyph.storeProductionName)
		
		# GSGlyph.glyphInfo
		assert glyph.glyphInfo or glyph.glyphInfo == None
		
		# GSGlyph.leftKerningGroup
		self.assertUnicode(glyph.leftKerningGroup)
		
		# GSGlyph.rightKerningGroup
		self.assertUnicode(glyph.rightKerningGroup)
		
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
		a = glyph.colorObject
		
		# GSGlyph.note
		self.assertUnicode(glyph.note)
		
		# GSGlyph.selected
		self.assertBool(glyph.selected)
		
		# GSGlyph.mastersCompatible
		self.assertIsInstance(glyph.mastersCompatible, bool)
		
		# GSGlyph.userData
		self.assertIsNotNone(glyph.userData)
		if (len(glyph.userData) > 0):
			self.assertDict(glyph.userData)
		
		# GSGlyph.smartComponentAxes
		self.assertIsInstance(list(glyph.smartComponentAxes), list)
		
		# GSGlyph.lastChange
		assert int(glyph.lastChange)
		
		
		## Methods
		glyph.beginUndo()
		glyph.endUndo()
		glyph.updateGlyphInfo()

		
		# Delete glyph
		del Glyphs.font.glyphs['test']
	

sys.argv = ["GlyphsAppTests"]

if __name__ == '__main__':
	unittest.main(exit=False)
