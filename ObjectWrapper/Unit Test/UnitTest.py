#MenuTitle: Glyphs.app Unit Tests
# -*- coding: utf-8 -*-

#import GlyphsApp
#reload(GlyphsApp) 

import unittest

import GlyphsApp
from GlyphsApp import *
import os, time


def testString(stringObject, assertType = True):
	if assertType:
		assert type(str(stringObject)) == str
	oldValue = stringObject
	stringObject = 'a'
	assert stringObject == 'a'
	stringObject = oldValue

def testDict(dictObject, assertType = True):
	if assertType:
		assert type(dict(dictObject)) == dict
	var1 = 'abc'
	var2 = 'def'
	dictObject['uniTestValue'] = var1
	assert dictObject['uniTestValue'] == var1
	dictObject['uniTestValue'] = var2
	assert dictObject['uniTestValue'] == var2

def testInteger(intObject, assertType = True):
	if assertType:
		assert type(int(intObject)) == int
	oldValue = intObject
	intObject = 1
	assert intObject == 1
	intObject = oldValue

def testFloat(floatObject, assertType = True):
	if assertType:
		assert type(float(floatObject)) == float
	oldValue = floatObject
	floatObject = .5
	assert floatObject == .5
	floatObject = oldValue

def testUnicode(unicodeObject, assertType = True):
	if assertType:
		assert unicode(unicodeObject)
	oldValue = unicodeObject
	unicodeObject = u'Ə'
	assert unicodeObject == u'Ə'
	unicodeObject = oldValue

def testBool(boolObject, assertType = True):
	if assertType:
		assert type(boolObject) == bool
	oldValue = boolObject
	boolObject = not boolObject
	assert boolObject == (not oldValue)
	boolObject = oldValue


class GlyphsAppTests(unittest.TestCase):
	
	def test_GSApplication(self):

		# Main object
		self.assertIsNotNone(Glyphs)

		# close all fonts
		for font in Glyphs.fonts:
			font.close()

		# open font
		Glyphs.open("/Users/georg/Programmierung/GlyphsSDK/ObjectWrapper/Unit Test/Glyphs Unit Test Sans.glyphs")

		# Macro window
		Glyphs.showMacroWindow()

		# Assert font
		self.assertIsNotNone(Glyphs.font)
		self.assertEqual(len(Glyphs.fonts), 1)



		## Attributes
	
		# GSApplication.reporters
		assert len(list(Glyphs.reporters)) > 0
		# activate all reporters
		for reporter in Glyphs.reporters:
			Glyphs.activateReporter(reporter)
		assert len(Glyphs.activeReporters) == len(Glyphs.reporters)
		# deactivate all reporters
		for reporter in Glyphs.reporters:
			Glyphs.deactivateReporter(reporter)
		assert len(Glyphs.activeReporters) == 0

		# GSApplication.defaults
		testDict(Glyphs.defaults, assertType = False)

		# GSApplication.scriptAbbrevations
		assert dict(Glyphs.scriptAbbrevations)

		# GSApplication.scriptSuffixes
		assert dict(Glyphs.scriptSuffixes)

		# GSApplication.languageScripts
		assert dict(Glyphs.languageScripts)

		# GSApplication.languageData
		assert list(map(dict, Glyphs.languageData))

		# GSApplication.unicodeRanges
		assert list(Glyphs.unicodeRanges)
	
		# GSApplication.editViewWidth
		testInteger(Glyphs.editViewWidth)

		# GSApplication.handleSize
		testInteger(Glyphs.handleSize)

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
		testUnicode(font.copyright)

		# GSFont.designer
		testUnicode(font.designer)

		# GSFont.designerURL
		testUnicode(font.designerURL)

		# GSFont.manufacturer
		testUnicode(font.manufacturer)

		# GSFont.manufacturerURL
		testUnicode(font.manufacturerURL)

		# GSFont.versionMajor
		testInteger(font.versionMajor)

		# GSFont.versionMinor
		testInteger(font.versionMinor)
	
		# GSFont.date
		assert font.date

		# GSFont.familyName
		testUnicode(font.familyName)

		# GSFont.upm
		testInteger(font.upm)

		# GSFont.note
		testUnicode(font.note)
	
		# GSFont.kerning
		assert dict(font.kerning)

		# GSFont.userData
		testDict(font.userData)
	
		# GSFont.disablesNiceNames
		testBool(font.disablesNiceNames)
	
		# GSFont.customParameters
		font.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'
		assert len(list(font.customParameters)) >= 1
		del(font.customParameters['trademark'])
	
		# GSFont.grid
		testInteger(font.grid)

		# GSFont.gridSubDivisions
		testInteger(font.gridSubDivisions)

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

		# GSFont.enableUpdateInterface()
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
		assert unicode(master.id)
	
		# GSFontMaster.name
		assert str(master.name)

		# GSFontMaster.weight
		assert str(master.weight)

		# GSFontMaster.width
		assert str(master.width)
	
		# GSFontMaster.weightValue
		testFloat(master.weightValue)
	
		# GSFontMaster.widthValue
		testFloat(master.widthValue)

		# GSFontMaster.customName
		testString(master.customName)

		# GSFontMaster.customValue
		testFloat(master.customValue)

		# GSFontMaster.ascender
		testFloat(master.ascender)

		# GSFontMaster.capHeight
		testFloat(master.capHeight)

		# GSFontMaster.xHeight
		testFloat(master.xHeight)

		# GSFontMaster.descender
		testFloat(master.descender)

		# GSFontMaster.italicAngle
		testFloat(master.italicAngle)
	
		# GSFontMaster.verticalStems
		oldStems = master.verticalStems
		master.verticalStems = [10, 15, 20]
		assert len(list(master.verticalStems)) == 3
		master.verticalStems = oldStems

		# GSFontMaster.horizontalStems
		oldStems = master.horizontalStems
		master.horizontalStems = [10, 15, 20]
		assert len(list(master.horizontalStems)) == 3
		master.horizontalStems = oldStems

		# GSFontMaster.alignmentZones
		assert type(list(master.alignmentZones)) == list

		# GSFontMaster.blueValues
		assert type(list(master.blueValues)) == list

		# GSFontMaster.otherBlues
		assert type(list(master.otherBlues)) == list

		# GSFontMaster.guides
		assert type(list(master.guides)) == list

		# GSFontMaster.userData
		testDict(master.userData)

		# GSFontMaster.customParameters
		master.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'
		assert len(list(master.customParameters)) >= 1
		del(master.customParameters['trademark'])


	def test_GSAlignmentZone(self):

		master = Glyphs.font.masters[0]

		master.alignmentZones.append(GlyphsApp.GSAlignmentZone(100, 10))
		assert master.alignmentZones[-1].position == 100
		assert master.alignmentZones[-1].size == 10
		del master.alignmentZones[-1]
	
	def test_GSInstance(self):
	
		instance = Glyphs.font.instances[0]
	
		# GSInstance.active
		self.assertIsInstance(instance.active, bool)

		# GSInstance.name
		testString(instance.name)

		# GSInstance.weight
		assert str(instance.weight)

		# GSInstance.width
		assert str(instance.width)

		# GSInstance.weightValue
		testFloat(instance.weightValue)
	
		# GSInstance.widthValue
		testFloat(instance.widthValue)

		# GSInstance.customValue
		testFloat(instance.customValue)

		# GSInstance.isItalic
		testBool(instance.isItalic)

		# GSInstance.isBold
		testBool(instance.isBold)

		# GSInstance.linkStyle
		testString(instance.linkStyle)

		# GSInstance.familyName
		testString(instance.familyName)

		# GSInstance.preferredFamily
		testString(instance.preferredFamily)

		# GSInstance.preferredSubfamilyName
		testString(instance.preferredSubfamilyName)

		# GSInstance.windowsFamily
		testString(instance.windowsFamily)

		# GSInstance.windowsStyle
		assert str(instance.windowsStyle)

		# GSInstance.windowsLinkedToStyle
		assert str(instance.windowsLinkedToStyle)

		# GSInstance.fontName
		testString(instance.fontName)

		# GSInstance.fullName
		testString(instance.fullName)

		# GSInstance.customParameters
		instance.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'
		assert len(list(instance.customParameters)) >= 1
		del(instance.customParameters['trademark'])

		# GSInstance.instanceInterpolations
		assert type(dict(instance.instanceInterpolations)) == dict

		# GSInstance.manualInterpolation
		testBool(instance.manualInterpolation)
	
		# GSInstance.interpolatedFont
		assert type(instance.interpolatedFont) == type(Glyphs.font)


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
		testUnicode(glyph.name)

		# GSGlyph.unicode
		testUnicode(glyph.unicode)

		# GSGlyph.string
		if glyph.unicode:
			assert type(glyph.string) == unicode

		# GSGlyph.id
		assert type(glyph.id) == str

		# GSGlyph.category
		assert type(glyph.category) == unicode or type(glyph.category) == type(None)

		# GSGlyph.storeCategory
		testBool(glyph.storeCategory)

		# GSGlyph.subCategory
		assert type(glyph.subCategory) == unicode or type(glyph.subCategory) == type(None)

		# GSGlyph.storeSubCategory
		testBool(glyph.storeSubCategory)

		# GSGlyph.script
		assert type(glyph.script) == unicode or type(glyph.script) == type(None)

		# GSGlyph.storeScript
		testBool(glyph.storeScript)

		# GSGlyph.productionName
		assert type(glyph.productionName) == unicode or type(glyph.productionName) == type(None)

		# GSGlyph.storeProductionName
		testBool(glyph.storeProductionName)

		# GSGlyph.glyphInfo
		assert glyph.glyphInfo or glyph.glyphInfo == None

		# GSGlyph.leftKerningGroup
		testUnicode(glyph.leftKerningGroup)

		# GSGlyph.rightKerningGroup
		testUnicode(glyph.rightKerningGroup)

		# GSGlyph.leftMetricsKey
		testUnicode(glyph.leftMetricsKey)

		# GSGlyph.rightMetricsKey
		testUnicode(glyph.rightMetricsKey)

		# GSGlyph.widthMetricsKey
		testUnicode(glyph.widthMetricsKey)

		# GSGlyph.export
		testBool(glyph.export)

		# GSGlyph.color
		testInteger(glyph.color)

		# GSGlyph.colorObject
		a = glyph.colorObject
	
		# GSGlyph.note
		testUnicode(glyph.note)
	
		# GSGlyph.selected
		testBool(glyph.selected)
	
		# GSGlyph.mastersCompatible
		assert type(glyph.mastersCompatible) == bool

		# GSGlyph.userData
		testDict(glyph.userData)

		# GSGlyph.smartComponentAxes
		assert type(list(glyph.smartComponentAxes)) == list

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
	unittest.main()
