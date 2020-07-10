#MenuTitle: Glyphs.app Unit Tests
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
from AppKit import *

if sys.version_info[0] == 3:
	unicode = str

PathToTestFile = os.path.join(os.path.dirname(__file__), 'Glyphs Unit Test Sans.glyphs')


class GlyphsAppTests(unittest.TestCase):
	
	def assertString(self, stringObject, assertType = True, readOnly = False, allowNone = True):
		if assertType and not (stringObject is None and allowNone):
			self.assertIsInstance(stringObject, str)
		if readOnly == False:
			oldValue = stringObject
			stringObject = 'a'
			self.assertEqual(stringObject, 'a')
			stringObject = oldValue
	
	def assertDict(self, dictObject, assertType = True):
		if assertType:
			self.assertIsInstance(dictObject, dict)
		var1 = 'abc'
		var2 = 'def'
		dictObject['uniTestValue'] = var1
		self.assertEqual(dictObject['uniTestValue'], var1)
		dictObject['uniTestValue'] = var2
		self.assertEqual(dictObject['uniTestValue'], var2)
		dictObject.pop('uniTestValue')
	
	def assertList(self, listObject, assertType = True, testValues = []):
		if assertType:
			self.assertIsInstance(listObject, list)
		if testValues:
			initial_len = len(listObject)
			listObject.append(testValues[0])
			self.assertEqual(listObject[-1], testValues[0])
			self.assertEqual(len(listObject), initial_len+1)
			self.assertEqual(listObject.index(testValues[0]), initial_len)
			listObject[-1] = testValues[-1]
			self.assertEqual(listObject[-1], testValues[-1])
			del listObject[-1]
			listObject.extend(testValues[1:])
			listObject.insert(-(len(testValues) - 1), testValues[0])
			for i, val in enumerate(testValues):
				self.assertEqual(listObject[initial_len+i], val)
			self.assertEqual(len(listObject), initial_len+len(testValues))
			for _ in testValues:
				listObject.remove(listObject[-1])
			listObject.insert(0, testValues[-1])
			self.assertEqual(listObject[0], testValues[-1])
			self.assertEqual(listObject.index(testValues[-1]), 0)
			self.assertEqual(listObject.pop(0), testValues[-1])
			self.assertEqual(len(listObject), initial_len)
		cp = copy.copy(listObject)
		for i, element in enumerate(listObject):
			self.assertIs(cp[i], element)
		self.assertEqual(len(copy.deepcopy(listObject)), len(listObject))
	
	def assertInteger(self, intObject, assertType = True, readOnly = False):
		if assertType:
			self.assertIsInstance(intObject, int)
		if readOnly == False:
			oldValue = intObject
			intObject = 1
			self.assertEqual(intObject, 1)
			intObject = oldValue
	
	def assertFloat(self, floatObject, assertType = True, readOnly = False):
		if assertType:
			self.assertIsInstance(floatObject, float)
		if readOnly == False:
			oldValue = floatObject
			floatObject = .5
			self.assertEqual(floatObject, .5)
			floatObject = oldValue
	
	def assertUnicode(self, unicodeObject, assertType = True, readOnly = False, allowNone = True):
		if assertType and not (unicodeObject is None and allowNone):
			self.assertIsInstance(unicodeObject, unicode)
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
		if Glyphs.font is not None:
			Glyphs.font.close()

	def test_GSApplication(self):
		
		# Main object
		self.assertIsNotNone(Glyphs)
		self.assertIsNotNone(Glyphs.__repr__())
		
		# close all fonts
		for font in Glyphs.fonts:
			font.close()
		self.assertEqual(len(Glyphs.fonts), 0)

		# AppFontProxy
		newFont = GSFont()
		Glyphs.fonts.append(newFont)
		self.assertIn(newFont, Glyphs.fonts)
		self.assertEqual(len(Glyphs.fonts), 1)
		self.assertEqual(newFont, Glyphs.font)
		copyfont = copy.copy(font)
		self.assertNotIn(copyfont, Glyphs.fonts)
		newFont.close()
		self.assertNotIn(newFont, Glyphs.fonts)
		self.assertEqual(len(Glyphs.fonts), 0)
		Glyphs.fonts.extend([copyfont])
		self.assertIn(copyfont, Glyphs.fonts)
		copyfont.close()
		with self.assertRaises(TypeError):
			Glyphs.fonts['a']

		# open font
		Glyphs.open(PathToTestFile)
		# Macro window
		Glyphs.showMacroWindow()
		
		# Assert font
		self.assertIsNotNone(Glyphs.font)
		self.assertEqual(len(Glyphs.fonts), 1)

		# GSApplication.documents
		self.assertEqual(len(Glyphs.documents), 1)
		self.assertIs(Glyphs.documents[0].font, Glyphs.fonts[0])
		with self.assertRaises(TypeError):
			Glyphs.documents['a']
		self.assertIsInstance(copy.copy(Glyphs.documents), list)
		
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
		
		del(Glyphs.defaults["TestKey"])
		Glyphs.registerDefaults({"TestKey":12})
		self.assertEqual(Glyphs.defaults["TestKey"], 12)
		Glyphs.registerDefaults({"TestKey":12})
		Glyphs.defaults["TestKey"] = 24
		self.assertEqual(Glyphs.defaults["TestKey"], 24)
		del(Glyphs.defaults["TestKey"])
		self.assertEqual(Glyphs.defaults["TestKey"], 12)
		
		# GSApplication.boolDefaults
		self.assertIsNone(Glyphs.defaults["BoolKey"])
		self.assertIs(Glyphs.boolDefaults["BoolKey"], False)
		Glyphs.boolDefaults["BoolKey"] = True
		self.assertEqual(Glyphs.boolDefaults["BoolKey"], True)
		del Glyphs.boolDefaults["BoolKey"]
		with self.assertRaises(TypeError):
			Glyphs.boolDefaults["BoolKey"] = 12

		# GSApplication.intDefaults
		self.assertIsNone(Glyphs.defaults["IntKey"])
		self.assertIs(Glyphs.intDefaults["IntKey"], 0)
		Glyphs.intDefaults["IntKey"] = 14
		self.assertEqual(Glyphs.intDefaults["IntKey"], 14)
		del Glyphs.intDefaults["IntKey"]
		with self.assertRaises(TypeError):
			Glyphs.intDefaults["IntKey"] = 12.5

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
			print('hello')
		newMenuItem = NSMenuItem('B', a)
		Glyphs.menu[EDIT_MENU].append(newMenuItem)
		self.assertIsNotNone(Glyphs.menu[0])
		with self.assertRaises(TypeError):
			Glyphs.menu[1.5]
		self.assertList(copy.copy(Glyphs.menu))
		
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
		font.show()
		self.assertIsNotNone(font.__repr__())
		
		## Attributes
		
		# GSFont.parent
		self.assertIn('GSDocument', str(font.parent))

		
		# GSFont.masters
		amountLayersPerGlyph = len(font.glyphs['a'].layers)
		self.assertGreaterEqual(len(list(font.masters)), 1)
		self.assertList(font.masters, assertType=False, testValues=[
				GSFontMaster(), GSFontMaster(), copy.copy(GSFontMaster())])
		self.assertEqual(amountLayersPerGlyph, len(font.glyphs['a'].layers))
		self.assertEqual(font.masters[0], font.masters[font.masters[0].id])
		with self.assertRaises(TypeError):
			font.masters[2.2]

		# GSFont.instances
		self.assertGreaterEqual(len(list(font.instances)), 1)
		self.assertList(font.instances, assertType=False, testValues=[
				GSInstance(), GSInstance(), copy.copy(GSInstance())])
		
		# GSFont.glyphs
		self.assertGreaterEqual(len(list(font.glyphs)), 1)
		self.assertEqual(font.glyphs[u'ä'], font.glyphs['adieresis'])
		self.assertEqual(font.glyphs['00E4'], font.glyphs['adieresis'])
		self.assertEqual(font.glyphs['00e4'], font.glyphs['adieresis'])
		with self.assertRaises(TypeError):
			font.glyphs[1.4]
		with self.assertRaises(NameError):
			font.glyphs.append(GSGlyph('adieresis'))

		# GSFont.classes
		font.classes = []
		self.assertList(font.classes, assertType=False, testValues=[
				GSClass('uppercaseLetters0', 'A'),
				GSClass('uppercaseLetters1', 'A'),
				copy.copy(GSClass('uppercaseLetters2', 'A'))])
		amount = len(font.classes)
		newClass = GSClass('uppercaseLetters', 'A')
		font.classes.append(newClass)
		self.assertIsNotNone(font.classes[-1].__repr__())
		self.assertIn('<GSClass "uppercaseLetters">', str(font.classes))
		self.assertEqual('A', font.classes['uppercaseLetters'].code)
		copyClass = copy.copy(newClass)
		self.assertIsNone(copyClass.parent())
		self.assertIs(newClass.parent(), font)
		font.classes.insert(0, copyClass)
		self.assertEqual(copyClass.parent(), newClass.parent())
		font.classes.remove(font.classes[0])
		self.assertEqual(len(font.classes), amount)
		
		# GSFont.features
		font.features = []
		self.assertList(font.features, assertType=False, testValues=[
				GSFeature('liga', 'sub f i by fi;'),
				copy.copy(GSFeature('liga', 'sub f l by fl;'))])
		font.features.append(GSFeature('liga', 'sub f i by fi;'))
		self.assertIsNotNone(font.features['liga'].__repr__())
		self.assertEqual(len(font.features), 1)
		self.assertIn('<GSFeature "liga">', str(font.features))
		self.assertEqual('sub f i by fi;', font.features['liga'].code)
		del(font.features['liga'])
		
		# GSFont.featurePrefixes
		font.featurePrefixes = []
		self.assertList(font.featurePrefixes, assertType=False, testValues=[
				GSFeaturePrefix('LanguageSystems0', 'languagesystem DFLT dflt;'),
				GSFeaturePrefix('LanguageSystems1', 'languagesystem DFLT dflt;'),
				copy.copy(GSFeaturePrefix('LanguageSystems2', 'languagesystem DFLT dflt;'))])
		font.featurePrefixes.append(GSFeaturePrefix('LanguageSystems', 'languagesystem DFLT dflt;'))
		self.assertIsNotNone(font.featurePrefixes[-1].__repr__())
		self.assertEqual(len(font.featurePrefixes), 1)
		self.assertIn('<GSFeaturePrefix "LanguageSystems">', str(font.featurePrefixes))
		self.assertEqual('languagesystem DFLT dflt;', font.featurePrefixes[-1].code)
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
		self.assertIsInstance(font.date, datetime.datetime)
		
		# GSFont.familyName
		self.assertUnicode(font.familyName)
		
		# GSFont.upm
		self.assertInteger(font.upm)
		
		# GSFont.note
		self.assertUnicode(font.note)
		
		# GSFont.kerning
		self.assertIsInstance(dict(font.kerning), dict)
		
		# GSFont.userData
		self.assertDict(font.userData, assertType=False)
		
		# GSFont.disablesNiceNames
		self.assertBool(font.disablesNiceNames)
		
		# GSFont.customParameters
		font.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'
		self.assertEqual(font.customParameters['trademark'], 'ThisFont is a trademark by MyFoundry.com')
		self.assertList(font.customParameters, assertType=False, testValues=[
				GSCustomParameter('hello0', 'world0'),
				GSCustomParameter('hello1', 'world1'),
				copy.copy(GSCustomParameter('hello2', 'world2'))])
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





		font = copy.copy(font) # Testing this at the end because otherwise some UI-dependent tests fail (like selection of glyphs)




	def test_GSFontMaster(self):
		font = Glyphs.font
		self.assertEqual(len(font.axes), 1)
		master = font.masters[0]
		masterCopy = copy.copy(master)
		self.assertIsNotNone(masterCopy.__repr__())
		
		# GSFontMaster.id
		self.assertString(master.id, allowNone=False)

		# GSFontMaster.font
		self.assertIs(master.font, font)
		
		# GSFontMaster.name
		self.assertString(master.name, allowNone=False)
		
		# GSFontMaster.axes
		self.assertIsNotNone(master.axes)
		self.assertEqual(len(master.axes), 1)
		self.assertFloat(master.axes[0])
		
		# # GSFontMaster.weight
		# self.assertIsNotNone(str(master.weight))
		#
		# # GSFontMaster.width
		# self.assertIsNotNone(str(master.width))
		#
		# # GSFontMaster.weightValue
		# self.assertFloat(master.weightValue)
		#
		# # GSFontMaster.widthValue
		# self.assertFloat(master.widthValue)
		#
		# # GSFontMaster.customName
		# self.assertString(master.customName)
		#
		# # GSFontMaster.customValue
		# self.assertFloat(master.customValue)
		
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
		# oldStems = master.verticalStems
		# master.verticalStems = [10, 15, 20]
		# self.assertEqual(len(list(master.verticalStems)), 3)
		# master.verticalStems = oldStems
		#
		# # GSFontMaster.horizontalStems
		# oldStems = master.horizontalStems
		# master.horizontalStems = [10, 15, 20]
		# self.assertEqual(len(list(master.horizontalStems)), 3)
		# master.horizontalStems = oldStems
		
		# GSFontMaster.alignmentZones
		self.assertIsInstance(list(master.alignmentZones), list)
		for az in master.alignmentZones:
			self.assertIsInstance(az, GSAlignmentZone)
		
		# GSFontMaster.blueValues
		self.assertIsInstance(list(master.blueValues), list)
		for bv in master.blueValues:
			self.assertFloat(bv)
		
		# GSFontMaster.otherBlues
		self.assertIsInstance(list(master.otherBlues), list)
		for ob in master.otherBlues:
			self.assertFloat(ob)
		
		# GSFontMaster.guides
		self.assertIsInstance(list(master.guides), list)
		master.guides = []
		self.assertEqual(len(master.guides), 0)
		newGuide = GSGuide()
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
		
		'''
		master.alignmentZones = []
		self.assertEqual(len(master.alignmentZones), 0)
		master.alignmentZones.append(GSAlignmentZone(100, 10))
		self.assertIsNotNone(master.alignmentZones[-1].__repr__())
		zone = copy.copy(master.alignmentZones[-1])
		self.assertEqual(len(master.alignmentZones), 1)
		self.assertEqual(master.alignmentZones[-1].position, 100)
		self.assertEqual(master.alignmentZones[-1].size, 10)
		del master.alignmentZones[-1]
		self.assertEqual(len(master.alignmentZones), 0)
		'''
		zone = master.alignmentZones[0]
		copyZone = copy.copy(zone)
		self.assertIsInstance(copyZone, GSAlignmentZone)

		# GSAlignmentZone.position
		self.assertFloat(zone.position)

		# GSAlignmentZone.size
		self.assertFloat(zone.size)


	def test_GSInstance(self):
		
		instance = Glyphs.font.instances[0]
		copyInstance = copy.copy(instance)
		self.assertIsNotNone(copyInstance.__repr__())
		
		# GSInstance.active
		self.assertBool(instance.active)
		
		# GSInstance.name
		self.assertString(instance.name)
		
		# GSInstance.weightClass
		self.assertInteger(instance.weightClass)
		with self.assertRaises(TypeError):
			instance.weightClass = 'a'

		# GSInstance.weightClassName
		self.assertString(instance.weightClassName, readOnly = True)
		
		# GSInstance.widthClass
		self.assertInteger(instance.widthClass)
		with self.assertRaises(TypeError):
			instance.widthClass = 'a'

		# GSInstance.widthClassName
		self.assertString(instance.widthClassName, readOnly = True)

		# GSInstance.axes
		self.assertIsNotNone(instance.axes)
		self.assertEqual(len(instance.axes), 1)

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
		path = os.path.join(os.path.dirname(__file__), 'GlyphsUnitTestSans-Thin.otf')
		result = instance.generate(FontPath=path)
		self.assertEqual(result, True)
		self.assertTrue(os.path.exists(path))
		if os.path.exists(path):
			os.remove(path)



	def test_GSGlyph(self):
		
		font = Glyphs.font
		glyph = font.glyphs['a'].duplicate('a.test')
		glyph = copy.copy(glyph)
		glyph.parent = font
		# GSGlyph.parent
		self.assertEqual(glyph.parent, Glyphs.font)
		
		# GSGlyph.layers
		self.assertIsNotNone(glyph.layers)
		amount = len(glyph.layers)
		newLayer = GSLayer()
		newLayer.name = '1'
		glyph.layers.append(newLayer)
		self.assertIn('<GSLayer "1" (a.test)>', str(glyph.layers[-1]))
		self.assertEqual(newLayer, glyph.layers[-1])
		del glyph.layers[-1]
		newLayer1 = GSLayer()
		newLayer1.name = '2'
		newLayer2 = GSLayer()
		newLayer2.name = '3'
		glyph.layers.extend([newLayer1, newLayer2])
		self.assertEqual(newLayer1, glyph.layers[-2])
		self.assertEqual(newLayer2, glyph.layers[-1])
		newLayer = GSLayer()
		newLayer.name = '4'
		glyph.layers.insert(0, newLayer) # indices here don't make sense because layer get appended using a UUID
		self.assertEqual(newLayer, glyph.layers[-1]) # so the latest layer got appended at the end also
		glyph.layers.remove(glyph.layers[-1])
		glyph.layers.remove(glyph.layers[-1])
		glyph.layers.remove(glyph.layers[-1])
		self.assertEqual(amount, len(glyph.layers))
		
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
		self.assertDict(glyph.userData, assertType=False)
		
		# GSGlyph.smartComponentAxes
		# postponed to its own test
		
		# GSGlyph.lastChange
		glyph.name = "a.test2"
		self.assertIsInstance(glyph.lastChange, datetime.datetime)
		glyph.name = "a.test1"
		## Methods
		glyph.beginUndo()
		glyph.endUndo()
		glyph.updateGlyphInfo()

		
		# Delete glyph
		del Glyphs.font.glyphs['a.test']

	def test_GSLayer(self):

		font = Glyphs.font
		glyph = font.glyphs['a']
		layer = glyph.layers[0]
		layer = copy.copy(layer)
		self.assertIsNotNone(layer.__repr__())
		layer.parent = glyph
		# GSLayer.parent
		self.assertEqual(layer.parent, glyph)
		
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
		newGuide = GSGuide()
		newGuide = copy.copy(newGuide)
		newGuide.position = NSPoint(100, 100)
		newGuide.angle = -10.0
		newGuide1 = GSGuide()
		newGuide1.position = NSPoint(100, 100)
		newGuide1.angle = -10.0
		newGuide2 = GSGuide()
		newGuide2.position = NSPoint(100, 100)
		newGuide2.angle = -10.0
		self.assertList(layer.guides, assertType=False, testValues=[
				newGuide, newGuide1, newGuide2, GSGuide()])

		# GSLayer.annotations
		layer.annotations = []
		self.assertEqual(len(layer.annotations), 0)
		newAnnotation = GSAnnotation()
		newAnnotation.type = TEXT
		newAnnotation.text = 'Fuck, this curve is ugly!'
		newAnnotation1 = GSAnnotation()
		newAnnotation1.type = ARROW
		newAnnotation2 = GSAnnotation()
		newAnnotation2.type = CIRCLE
		newAnnotation3 = GSAnnotation()
		newAnnotation3.type = PLUS
		newAnnotation4 = GSAnnotation()
		newAnnotation4 = copy.copy(newAnnotation)
		newAnnotation4.type = MINUS
		self.assertList(layer.annotations, assertType=False, testValues=[
				newAnnotation, newAnnotation1, newAnnotation2, newAnnotation3, newAnnotation4])

		# GSLayer.hints
		layer = Glyphs.font.glyphs['a'].layers[0]
		layer.hints = []
		self.assertEqual(len(layer.hints), 0)
		newHint = GSHint()
		newHint = copy.copy(newHint)
		newHint.originNode = layer.shapes[0].nodes[0]
		newHint.targetNode = layer.shapes[0].nodes[1]
		newHint.type = STEM
		newHint1 = GSHint()
		newHint1.originNode = layer.shapes[0].nodes[0]
		newHint1.targetNode = layer.shapes[0].nodes[1]
		newHint1.type = STEM
		newHint2 = GSHint()
		newHint2.originNode = layer.shapes[0].nodes[0]
		newHint2.targetNode = layer.shapes[0].nodes[1]
		newHint2.type = STEM
		newHint3 = GSHint()
		newHint3.originNode = layer.shapes[0].nodes[0]
		newHint3.targetNode = layer.shapes[0].nodes[1]
		self.assertList(layer.hints, assertType=False, testValues=[
				newHint, newHint1, newHint2, newHint3])

		# GSLayer.anchors
		amount = len(layer.anchors)
		if layer.anchors['top']:
			oldPosition = layer.anchors['top'].position
		else:
			oldPosition = None
		layer.anchors['top'] = GSAnchor()
		self.assertGreaterEqual(len(layer.anchors), 1)
		self.assertIsNotNone(layer.anchors['top'].__repr__())
		layer.anchors['top'].position = NSPoint(100, 100)
		anchor = copy.copy(layer.anchors['top'])
		del layer.anchors['top']
		layer.anchors['top'] = GSAnchor()
		layer.anchors['top'].position = oldPosition
		self.assertString(layer.anchors['top'].name)
		newAnchor1 = GSAnchor()
		newAnchor1.name = 'testPosition1'
		newAnchor2 = GSAnchor()
		newAnchor2.name = 'testPosition2'
		layer.anchors.extend([newAnchor1, newAnchor2])
		self.assertEqual(layer.anchors['testPosition1'], newAnchor1)
		self.assertEqual(layer.anchors['testPosition2'], newAnchor2)
		newAnchor3 = GSAnchor()
		newAnchor3.name = 'testPosition3'
		layer.anchors.append(newAnchor3)
		self.assertEqual(layer.anchors['testPosition3'], newAnchor3)
		layer.anchors.remove(layer.anchors['testPosition3'])
		layer.anchors.remove(layer.anchors['testPosition2'])
		layer.anchors.remove(layer.anchors['testPosition1'])
		self.assertEqual(amount, len(layer.anchors))

		# GSLayer.paths
		# has its own test
		
		# GSLayer.selection
		layer.selection.clear()
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
		layer.selection.append(layer.shapes[0])
		layer.selection.extend(layer.anchors)
		layer.selection.remove(layer.shapes[0])
		layer.selection.insert(0, layer.shapes[0])
		self.assertEqual(len(layer.selection), 1 + len(layer.anchors)) # 1 for the single path

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
		# self.assertIsInstance(layer.openBezierPath, NSBezierPath) # TODO: is NULL if there are no open paths

		# GSLayer.completeBezierPath
		self.assertIsInstance(layer.completeBezierPath, NSBezierPath)

		# GSLayer.completeOpenBezierPath
		# self.assertIsInstance(layer.completeOpenBezierPath, NSBezierPath) # TODO: is NULL if there are no open paths

		# GSLayer.userData
		layer.userData["Hallo"] = "Welt"
		self.assertDict(layer.userData, assertType=False)


		## Methods
		decomposedLayer = layer.copyDecomposedLayer()
		self.assertGreaterEqual(len(decomposedLayer.shapes), 1)
		
		layer = Glyphs.font.glyphs['adieresis'].layers[0]
		layer.decomposeComponents()
		self.assertGreaterEqual(len(layer.paths), 1)

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
		
		Glyphs.font.close()
		
		
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
		layer.shapes[1].smartComponentValues['shoulderWidth'] = 30
		layer.shapes[1].smartComponentValues['crotchDepth'] = -77


	def test_GSShapesComponents(self):
		font = Glyphs.font
		font.glyphs['adieresis'].duplicate('adieresis.test')
		
		glyph = font.glyphs['adieresis.test']
		layer = glyph.layers[0]
		component = layer.shapes[0]
		component = copy.copy(component)
		self.assertIsNotNone(component.__repr__())
		component.parent = layer
		# Delete and add
		self.assertEqual(len(layer.shapes), 2)
		layer.shapes = []
		self.assertEqual(len(layer.shapes), 0)
		layer.shapes.append(GSComponent('a'))
		self.assertIsNotNone(layer.shapes[0].__repr__())
		self.assertEqual(len(layer.shapes), 1)
		layer.shapes.append(GSComponent('dieresis'))
		self.assertEqual(len(layer.shapes), 2)
		layer.shapes = [GSComponent('a'), GSComponent('dieresis')]
		self.assertEqual(len(layer.shapes), 2)
		layer.shapes = []
		layer.shapes.extend([GSComponent('a'), GSComponent('dieresis')])
		self.assertEqual(len(layer.shapes), 2)
		newComponent = GSComponent('dieresis')
		layer.shapes.insert(0, newComponent)
		self.assertEqual(newComponent, layer.shapes[0])
		layer.shapes.remove(layer.shapes[0])
		self.assertEqual(len(layer.shapes), 2)

		# GSComponent.position
		self.assertIsInstance(component.position, NSPoint)

		# GSComponent.scale
		self.assertTrue(isinstance(component.scale, NSPoint))
		
		# GSComponent.rotation
		self.assertFloat(component.rotation)

		# GSComponent.componentName
		# GSComponent.component
		# GSComponent.layer
		component.componentName = 'A'

		self.assertEqual(component.component, font.glyphs['A'])
# not defined yet		self.assertEqual(component.layer, font.glyphs['A'].layers[layer.layerId])
		component.componentName = 'a'
		self.assertEqual(component.component, font.glyphs['a'])
# not defined yet		self.assertEqual(component.layer, font.glyphs['a'].layers[layer.layerId])

		component = layer.shapes[0]

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
		
		del font.glyphs['adieresis.test']
		self.assertIsNone(font.glyphs['adieresis.test'])
		font.close()

	def test_GSComponentLegacy(self):
		return
		Glyphs.font.glyphs['adieresis'].duplicate('adieresis.test')
		
		glyph = Glyphs.font.glyphs['adieresis.test']
		layer = glyph.layers[0]
		component = layer.components[0]
		component = copy.copy(component)
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
		layer.components = []
		layer.components.extend([GSComponent('a'), GSComponent('dieresis')])
		self.assertEqual(len(layer.components), 2)
		newComponent = GSComponent('dieresis')
		layer.components.insert(0, newComponent)
		self.assertEqual(newComponent, layer.components[0])
		layer.components.remove(layer.components[0])
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
		
		
	def test_GSPathShapes(self):
		
		layer = Glyphs.font.glyphs['a'].layers[0]
		path = layer.shapes[0]
		copyPath = copy.copy(path)
		self.assertIsNotNone(copyPath.__repr__())

		# Proxy
		pathCopy1 = copy.copy(path)
		pathCopy2 = copy.copy(pathCopy1)
		pathCopy3 = copy.copy(pathCopy2)
		self.assertList(layer.shapes, assertType=False, testValues=[
				pathCopy1, pathCopy2, pathCopy3])
		
		# GSPath.parent
		self.assertEqual(path.parent, Glyphs.font.glyphs['a'].layers[0])

		# GSPath.nodes
		self.assertIsNotNone(list(path.nodes))
		newNode = GSNode(NSPoint(20,20))
		newNode1 = GSNode(NSPoint(10,10))
		newNode2 = GSNode(NSPoint(20,20))
		newNode3 = copy.copy(newNode)
		self.assertList(path.nodes, assertType=False, testValues=[
				newNode, newNode1, newNode2, newNode3])

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

	def test_GSPathLegacy(self):
		return
		layer = Glyphs.font.glyphs['a'].layers[0]
		path = layer.paths[0]
		path = copy.copy(path)
		self.assertIsNotNone(path.__repr__())

		# Proxy
		amount = len(layer.paths)
		pathCopy1 = copy.copy(path)
		layer.paths.append(pathCopy1)
		pathCopy2 = copy.copy(pathCopy1)
		layer.paths.extend([pathCopy2])
		self.assertEqual(layer.paths[-2], pathCopy1)
		self.assertEqual(layer.paths[-1], pathCopy2)
		pathCopy3 = copy.copy(pathCopy2)
		layer.paths.insert(0, pathCopy3)
		self.assertEqual(layer.paths[0], pathCopy3)
		layer.paths.remove(layer.paths[0])
		layer.paths.remove(layer.paths[-1])
		layer.paths.remove(layer.paths[-1])
		self.assertEqual(amount, len(layer.paths))
		
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
		path = layer.shapes[0]
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




		# Copy, then test again
		node = copy.copy(node)
		self.assertEqual(node.index, 9223372036854775807) # theoretically, this value could be maxint in a node, but in our test font it should be 0, I guess (taken from actual glyph, not orphan path)



	def test_GSBackgroundImage(self):

		glyph = Glyphs.font.glyphs['A']
		layer = glyph.layers[0]
		
		layer.backgroundImage = GSBackgroundImage(os.path.join(os.path.dirname(PathToTestFile), 'A.jpg'))
		image = layer.backgroundImage
		copyImage = copy.copy(image)
		self.assertIsNotNone(copyImage.__repr__())
		
		
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
		self.assertTrue(isinstance(image.scale, NSPoint))
		self.assertEqual(image.scale.x, 1)

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
		self.assertEqual(info.case, GSLowercase)

		# GSGlyphInfo.components
		self.assertIsNone(info.components)

		# GSGlyphInfo.components
		info = Glyphs.font.glyphs['adieresis'].glyphInfo
		self.assertIsInstance(list(info.components), list)

		# GSGlyphInfo.accents
		info = Glyphs.glyphInfoForName('lam_alef-ar')
		self.assertIsInstance(list(info.accents), list)

		# GSGlyphInfo.anchors
		self.assertIsInstance(list(info.anchors), list)

		# GSGlyphInfo.unicode
		self.assertEqual(info.unicode, 'FEFB')

		# GSGlyphInfo.unicode2
		self.assertEqual(len(info.unicodes), 1)

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

	def test_objcObject(self):
		from GlyphsApp import objcObject
		obj = objcObject(["a"])
		self.assertIsInstance(obj, NSArray)
		obj = objcObject({"a":1})
		self.assertIsInstance(obj, NSDictionary)
		obj = objcObject(3.145)
		self.assertIsInstance(obj, NSNumber)
		obj = objcObject(1)
		self.assertIsInstance(obj, NSNumber)
		obj = objcObject(None)
		self.assertIsInstance(obj, NSNull)

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
	#import coverage  # pip3 install coverage
	#cov = coverage.Coverage()
	#cov.start()

	unittest.main(exit=False, failfast=False)

	#cov.stop()
	#cov.save()

	#cov.html_report()
