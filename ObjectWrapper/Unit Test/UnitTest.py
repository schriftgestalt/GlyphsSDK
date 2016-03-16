#MenuTitle: Glyphs.app Unit Tests
# -*- coding: utf-8 -*-

from GlyphsApp import *
import os


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
		assert int(intObject)
	oldValue = intObject
	intObject += 1
	assert intObject == oldValue + 1
	intObject = oldValue

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


	################################################
	# GSApplication
	
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
	print Glyphs.glyphInfoForName('a')

	# GSApplication.glyphInfoForUnicode()
	print Glyphs.glyphInfoForUnicode('0061')

	# GSApplication.niceGlyphName()
	print Glyphs.niceGlyphName('a')

	# GSApplication.productionGlyphName()
	print Glyphs.productionGlyphName('a')

	# GSApplication.ligatureComponents()
	print Glyphs.ligatureComponents('allah-ar')
	
	
def unitTest():
	testGSApplication()

	GSApplication()