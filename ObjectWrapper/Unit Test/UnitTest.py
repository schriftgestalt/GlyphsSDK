#MenuTitle: Glyphs.app Unit Tests
# -*- coding: utf-8 -*-

#import GlyphsApp
#reload(GlyphsApp) 

import GlyphsApp
from GlyphsApp import *
import os, time


def testString(stringObject, assertType = True):
	if assertType:
		assert str(stringObject)

def testDict(dictObject, assertType = True):
	if assertType:
		assert dict(dictObject)
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
	try:
		intObject += 1
	except:
		intObject = 1
	assert intObject == oldValue + 1
	intObject = oldValue

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

def testGSApplication():

	# Main object
	assert Glyphs

	# Clear Log
	Glyphs.clearLog()

	# close all fonts
	for font in Glyphs.fonts:
		font.close()

	# open font
	Glyphs.open(os.path.join(os.path.dirname(__file__), 'Glyphs Unit Test Sans.glyphs'))

	# Macro window
	Glyphs.showMacroWindow()

	# Assert font
	assert Glyphs.font
	assert len(Glyphs.fonts) == 1



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
	

def testGSFont():
	
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
	
	


def unitTest():

	testGSApplication()
	testGSFont()
