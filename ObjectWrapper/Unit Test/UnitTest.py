#MenuTitle: Glyphs.app Unit Tests
# encoding: utf-8
# -*- coding: utf-8 -*-

from __future__ import print_function
from cgi import test

#import GlyphsApp
#reload(GlyphsApp)

import unittest

import GlyphsApp
from GlyphsApp import *
import os, time, sys, datetime
import objc
import copy

from AppKit import \
NSAffineTransform, \
NSArray, \
NSBezierPath, \
NSColor, \
NSDate, \
NSDictionary, \
NSImage, \
NSMenuItem, \
NSNull, \
NSNumber, \
NSPoint, \
NSPredicate, \
NSKeyValueFastMutableArray2, \
NSClassFromString, \
NSRect

import pathlib as Pathlib

## Development Settings <MF>
SKIP_FILE_SAVING = True # default: `False`
PRINT_VERBOSE = 1 # `2` or default: `1`
## ====================

if sys.version_info[0] == 3:
	unicode = str

PathToTestFile = os.path.join(os.path.dirname(__file__), 'Glyphs Unit Test Sans.glyphs')

Glyphs.clearLog()

class GlyphsAppTests(unittest.TestCase):

	def assertReadOnly(self, readOnlyObject, _instance, _property):
		"""Needs the actual instance to test for readOnly-nes"""
		self.assertIsNotNone(_instance) # if `readOnly=True` we need the instance object.
		self.assertIsNotNone(_property) # if `readOnly=True` we need the property to be checked.
		oldValue = readOnlyObject
		self.assertHasAttr(_instance, _property)
		with self.assertRaises(AttributeError) as ctx:
			setattr(_instance, _property, "This should not happen")
			setattr(_instance, _property, oldValue)
		self.assertEqual("can't set attribute", str(ctx.exception))

	def assertHasAttr(self, obj, intendedAttr):
		testBool = hasattr(obj, intendedAttr)
		self.assertTrue(testBool, msg="'%s' object has no attribute '%s'" % (obj.__class__.__name__, intendedAttr))

	def assertString(self, stringObject, assertType=True, allowNone=True):
		if not allowNone:
			self.assertIsNotNone(stringObject)	
		if assertType and not (stringObject is None and allowNone):
			self.assertIsInstance(stringObject, str)
		# if readOnly == False:
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

	def assertList(self, listObject, assertType=True, testValues = []):
		# Also checks for mutability
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
			self.assertEqual(len(listObject), initial_len)
			listObject.extend(testValues[1:])
			listObject.insert(-(len(testValues) - 1), testValues[0])
			for i, val in enumerate(testValues):
				self.assertEqual(listObject[initial_len+i], val)
			self.assertEqual(len(listObject), initial_len+len(testValues))
			del listObject[initial_len:-1]
			listObject.remove(listObject[-1])
			listObject.insert(0, testValues[-1])
			self.assertEqual(listObject[0], testValues[-1])
			self.assertEqual(listObject.index(testValues[-1]), 0)
			self.assertEqual(listObject.pop(), testValues[-1])
			self.assertEqual(len(listObject), initial_len)
		with self.assertRaises(IndexError):
			listObject[len(listObject)]
		with self.assertRaises(IndexError):
			listObject[-len(listObject)-1]
		cp = copy.copy(listObject)
		for i, element in enumerate(listObject):
			self.assertIs(cp[i], element)
		self.assertEqual(len(copy.deepcopy(listObject)), len(listObject))
	
	def assertInteger(self, intObject, assertType=True):
		if assertType:
			self.assertIsInstance(intObject, int)
		# if readOnly == False:
			oldValue = intObject
			intObject = 1
			self.assertEqual(intObject, 1)
			intObject = oldValue
	
	def assertFloat(self, floatObject, assertType=True, allowNone = False):
		if not allowNone:
			self.assertIsNotNone(floatObject)
		if assertType and not (floatObject is None and allowNone):
			self.assertIsInstance(floatObject, float)
		# if readOnly == False:
			oldValue = floatObject
			floatObject = .5
			self.assertEqual(floatObject, .5)
			floatObject = oldValue
	
	def assertUnicode(self, unicodeObject, assertType=True, allowNone = True):
		if not allowNone:
			self.assertIsNotNone(unicodeObject)
		if assertType and not (unicodeObject is None and allowNone):
			self.assertIsInstance(unicodeObject, unicode)
		# if readOnly == False:
			oldValue = unicodeObject
			unicodeObject = u'Ə'
			self.assertEqual(unicodeObject, u'Ə')
			unicodeObject = oldValue
	
	def assertBool(self, boolObject, assertType=True):
		if assertType:
			self.assertIsInstance(boolObject, bool)
		# if readOnly == False:
			oldValue = boolObject
			boolObject = not boolObject
			self.assertEqual(boolObject, (not oldValue))
			boolObject = oldValue
	
	## Helper Methods

	def assertIsFile(self, path):
		# NOTE: can you confirm if this is proper? <MF @GS>
		if not Pathlib.Path(path).resolve().is_file():
			raise AssertionError("File does not exist: %s" % str(path))

	def fontFromPath(self):
		theFont = GSFont(PathToTestFile)
		self.assertIsNotNone(theFont.__repr__())
		self.assertIsNotNone(theFont)
		return theFont

	def setUp(self):
		self.font = self.fontFromPath()
	
	def test_GSFont(self):
		font = self.font

		## Properties
		## Mostly type checking.
		
		with self.subTest("masters"):
			self.assertIsInstance(font.masters, GlyphsApp.FontFontMasterProxy)

		with self.subTest("instances"):
			self.assertIsInstance(font.instances, GlyphsApp.FontInstancesProxy)

		with self.subTest("axes"):
			self.assertIsInstance(font.axes, GlyphsApp.FontAxesProxy)

		with self.subTest("stems"):
			self.assertIsInstance(font.stems, GlyphsApp.FontStemsProxy)

		with self.subTest("properties"):
			self.assertIsInstance(font.properties, NSKeyValueFastMutableArray2)

		with self.subTest("glyphs"):
			self.assertIsInstance(font.glyphs, GlyphsApp.FontGlyphsProxy)

		with self.subTest("classes"):
			self.assertIsInstance(font.classes, GlyphsApp.FontClassesProxy)

		with self.subTest("features"):
			self.assertIsInstance(font.features, GlyphsApp.FontFeaturesProxy)

		with self.subTest("featurePrefixes"):
			self.assertIsInstance(font.featurePrefixes, GlyphsApp.FontFeaturePrefixesProxy)
		
		with self.subTest("copyright"):
			self.assertUnicode(font.copyright)

		with self.subTest("copyrights"):
			self.assertIsInstance(font.copyrights, GlyphsApp.FontInfoPropertiesProxy)
		
		with self.subTest("license"):
			self.assertUnicode(font.license)
		
		with self.subTest("licenses"):
			self.assertIsInstance(font.licenses, GlyphsApp.FontInfoPropertiesProxy)
		
		with self.subTest("compatibleFullName"):
			self.assertUnicode(font.compatibleFullName)
		
		with self.subTest("compatibleFullNames"):
			self.assertIsInstance(font.compatibleFullNames, GlyphsApp.FontInfoPropertiesProxy)
		
		with self.subTest("sampleText"):
			self.assertUnicode(font.sampleText)
		
		with self.subTest("sampleTexts"):
			self.assertIsInstance(font.sampleTexts, GlyphsApp.FontInfoPropertiesProxy)
		
		with self.subTest("description"):
			self.assertUnicode(font.description)
		
		with self.subTest("descriptions"):
			self.assertIsInstance(font.descriptions, GlyphsApp.FontInfoPropertiesProxy)
		
		with self.subTest("trademark"):
			self.assertUnicode(font.trademark)
		
		with self.subTest("trademarks"):
			self.assertIsInstance(font.trademarks, GlyphsApp.FontInfoPropertiesProxy)
		
		with self.subTest("designer"):
			self.assertUnicode(font.designer)
		
		with self.subTest("designers"):
			self.assertIsInstance(font.designers, GlyphsApp.FontInfoPropertiesProxy)
		
		with self.subTest("designerURL"):	
			self.assertUnicode(font.designerURL)

		with self.subTest("manufacturer"):
			self.assertUnicode(font.manufacturer)
		
		with self.subTest("manufacturers"):
			self.assertIsInstance(font.manufacturers, GlyphsApp.FontInfoPropertiesProxy)
		
		with self.subTest("manufacturerURL"):
			self.assertUnicode(font.manufacturerURL)
		
		with self.subTest("versionMajor"):
			self.assertInteger(font.versionMajor)
		
		with self.subTest("versionMinor"):
			self.assertInteger(font.versionMinor)
				
		with self.subTest("familyName"):
			self.assertUnicode(font.familyName)
				
		with self.subTest("familyNames"):
			self.assertIsInstance(font.familyNames, GlyphsApp.FontInfoPropertiesProxy)

		with self.subTest("fontName"):
			self.assertEqual(font.fontName, font.familyName)

		with self.subTest("date"):
			self.assertIsInstance(font.date, datetime.datetime)

		with self.subTest("kerning"):
			self.assertIsInstance(font.kerning, NSClassFromString("MGOrderedDictionary"))

		with self.subTest("userData"):
			self.assertIsInstance(font.userData, GlyphsApp.UserDataProxy)

		with self.subTest("grid"):
			self.assertInteger(font.grid)

		with self.subTest("gridSubDivisions"):
			self.assertInteger(font.gridSubDivisions)

		with self.subTest("disablesAutomaticAlignment"):
			self.assertBool(font.disablesAutomaticAlignment)

		with self.subTest("gridLength"):
			self.assertFloat(font.gridLength)
				
		with self.subTest("keyboardIncrementHuge"):
			self.assertFloat(font.keyboardIncrementHuge)

		with self.subTest("keyboardIncrementBig"):
			self.assertFloat(font.keyboardIncrementBig)

		with self.subTest("keyboardIncrement"):
			self.assertFloat(font.keyboardIncrement)

		with self.subTest("snapToObjects"):
			self.assertBool(font.snapToObjects)

		with self.subTest("previewRemoveOverlap"):
			self.assertBool(font.previewRemoveOverlap)
		
		with self.subTest("upm"):
			self.assertInteger(font.upm)
		
		with self.subTest("note"):
			self.assertUnicode(font.note)
				
		with self.subTest("disablesNiceNames"):
			self.assertBool(font.disablesNiceNames)

		with self.subTest("appVersion"): #::Rafal
			self.assertUnicode(font.appVersion, allowNone=False)
			self.assertReadOnly(font.appVersion, _instance=font, _property="appVersion")
		
		with self.subTest("formatVersion"): #::Rafal
			self.assertInteger(font.formatVersion)
		
		with self.subTest("filepath"):
			pass # Has its dedicated test method now.

		## Methods
		
		# GSFont.disableUpdateInterface()
		font.disableUpdateInterface()
		
		# GSFontselfenableUpdateInterface()
		font.enableUpdateInterface()

		# GSFont.updateFeatures()
		font.updateFeatures()

		# GSFont.updateFeatures()  #::Rafal
		font.compileFeatures()


		#::Rafal
		with self.subTest("properties of GSFont"):
			propertyKeys = [
				"familyName",
				"familyNames",
				"designer",
				"designers",
				"manufacturer",
				"manufacturers",
				"copyright",
				"copyrights",
				"license",
				"licenses",
				"trademark",
				"trademarks",
				"description",
				"descriptions",
				"sampleText",
				"sampleTexts",
				"compatibleFullName",
				"compatibleFullNames",
			]
			# testing ammount of properties
			#TODO: font.properties has length 0
			#self.assertEqual(len(font.properties), len(propertyKeys)/2)

			# testing if empty properties return None

			for k in propertyKeys:
				a = getattr(font, k)
				#TODO: The "familyName" property is "Glyphs Unit Test Sans", not None
				#self.assertEqual(a, None)

			# testing assignment for properties

			for k in propertyKeys:
				if k[-1] != "s":
					a = setattr(font, k, "test singlular")
				else:
					a = getattr(font, k)
					a["ENG"] = "test localised"
			
			# testing assignment for properties
			for k in propertyKeys:
				if k[-1] != "s":
					a = setattr(font, k, "test singlular")
					self.assertString(a)
				else:
					a = getattr(font, k)
					self.assertIsInstance(a["ENG"], GSFontInfoValue)
					self.assertEqual(a["ENG"].value, "test localised")

			# testing deletion of plural properties
			for k in propertyKeys:
				if k[-1] == "s":
					a = getattr(font, k)
					del a['ENG']

	## GSFont Atributes

	@unittest.skip("font.filepath seems to not work with `GSFont({PATH})` <MF @GS>")
	def test_GSFont_filepath(self):
		font = self.font
		self.assertIsNotNone(font.filepath)
		self.assertIsInstance(font.filepath, str)
		# make sure this is a valid and existing path
		self.assertTrue(os.path.exists(font.filepath))

	def test_GSFont_date(self):
		font = self.font
		self.assertIsInstance(font.date, datetime.datetime)
		old_date = font.date
		dt = datetime.datetime.now()
		font.date = dt
		self.assertEqual(font.date, dt.replace(microsecond=0))
		unixtime = time.time()
		font.date = unixtime
		self.assertEqual(font.date, datetime.datetime.fromtimestamp(unixtime))
		nsdate = NSDate.alloc().init()
		font.date = nsdate
		self.assertEqual(font.date, datetime.datetime.fromtimestamp(nsdate.timeIntervalSince1970()))
		font.date = old_date		

	def test_GSFont_masters(self):
		font = self.font
		amountLayersPerGlyph = len(font.glyphs['a'].layers)
		self.assertGreaterEqual(len(list(font.masters)), 1)
		# TODO: reactivate this again and make it work <MF @MF>
		# self.assertList(font.masters, assertType=False, testValues=[
		# 		GSFontMaster(), GSFontMaster(), copy.copy(GSFontMaster())])
		# GS: I think the `assertList()` is meant to compare the list in the first argument to the `testValues`. And as the test font is quite empty, a new GSFontMaster (or a copy of it) should make it. We probably should check the `copy.copy()` somewhere else.
		self.assertEqual(amountLayersPerGlyph, len(font.glyphs['a'].layers))
		# ???: ^ What’s the intention here? `amountLayersPerGlyph` is the same as `len(font.glyphs['a'].layers)` -- Why the assertEqual of those? <MF @GS>
		# GS: I seems that it was intended to add a master on some point. Or just to make sure that there are no side effects.
		self.assertEqual(font.masters[0], font.masters[font.masters[0].id])
		with self.assertRaises(TypeError) as ctx:
			font.masters[2.2]
		self.assertEqual("need int or str, got: float", str(ctx.exception))
		
		# Masters can’t be indexed by name.
		firstMasterName = font.masters[0].name
		self.assertIsNone(font.masters[firstMasterName])

	def test_GSFont_intances(self):
		font = self.font
		self.assertGreaterEqual(len(list(font.instances)), 1)
		# TODO: reactivate this again and make it work <MF @MF>
		# self.assertList(font.instances, assertType=False, testValues=[
		# 		GSInstance(), GSInstance(), copy.copy(GSInstance())])
		# ???: ^ What’s the intention here? Fails with the test font. Shall it compare with another, empty font (because then it would pass) <MF @GS>
		with self.assertRaises(TypeError) as ctx:
			font.instances['a']
		self.assertEqual("list indices must be integers or slices, not str", str(ctx.exception))

	def test_GSFont_axes(self):
		font = self.font
		# TODO: reactivate this again and make it work <MF @MF>
		# self.assertList(font.axes, assertType=False, testValues=[
		# 		GSAxis(), GSAxis(), copy.copy(GSAxis())])
		# ???: ^ What’s the intention here? Fails with the test font. Shall it compare with another, empty font (because then it would pass) <MF @GS>
		with self.assertRaises(TypeError) as ctx:
			font.axes['a']
		self.assertEqual("list indices must be integers or slices, not str", str(ctx.exception))
		
		# Add an axis
		# old_axes = font.axes
		# testAxis = GSAxis()
		# testAxis.name = "Test Axis"

		# # Reset axes to former state
		# font.axes = old_axes
		# self.assertEqual(len(font.axes), 1)
		
		# self.assertEqual(font.axes[0].axisId, '72A59FFB-3C17-45EE-9D3F-A5FD5045AA83') # not testable like this, as the id is different with each font opening

	def test_GSAxis(self):
		"""
		- (x) name
		- (x) axisTag
		- ( ) axisId
		- (x) hidden
		- (x) font
		"""
		font = self.font
		testAxis = font.axes[0]
	
		# Properties

		with self.subTest("name"):
			self.assertEqual(testAxis.name, 'Weight')
			
			old_axisName = testAxis.name
			testAxis.name = "Test Axis Name"
			self.assertEqual(testAxis.name, "Test Axis Name")
			
			# QUESTION: Should we raise when an axis name is not a string? <MF @GS>
			# with self.assertRaises(TypeError) as ctx:
			# 	font.axes[0].name = 3 # Expecting a string
			# self.assertUnicode(font.axes[0].name)

			font.axes[0].name = old_axisName
		
		with self.subTest("font"):
			self.assertIs(testAxis.font, font)
			self.assertEqual(testAxis.font, font)
		
		with self.subTest("name"):
			self.assertUnicode(testAxis.name)
		
		with self.subTest("axisTag"):
			# - axisTags will not be limited to four letter strings. <MF>
			# - registed axisTags cannot be renamed in the UI, but programmatically. "Probably OK". <MF>
			self.assertUnicode(testAxis.axisTag)
			self.assertEqual(testAxis.axisTag, 'wght')
			self.assertEqual(len(font.axes[-1].axisTag), 4)
		
		with self.subTest("axisId"):
			self.assertUnicode(testAxis.axisId)

		with self.subTest("hidden"):
			self.assertBool(testAxis.hidden)
			self.assertEqual(testAxis.hidden, False)

	def test_GSMetric(self):
		"""
		- (x) name
		- (x) id
		- (x) filter
		- (x) type
		- (x) horizontal
		Not implemented in wrapper:
		- (x) title()
		- (x) titles()
		"""
		font = self.font
		metric = font.metrics[0]

		with self.subTest("font"):		
			self.assertIs(metric.font, font)

		with self.subTest("type"):		
			self.assertInteger(metric.type)
			self.assertIs(metric.type, 1)
			# test mutability
			metric.type = 2
			self.assertIs(metric.type, 2)
			metric.type = 1

		with self.subTest("name"):		
			self.assertUnicode(metric.name)
			self.assertIsNone(metric.name)
			# test mutability
			metric.name = "Test Name"
			self.assertIsNotNone(metric.name)
			self.assertEqual(metric.name, "Test Name")
			metric.name = None
			self.assertIsNone(metric.name)
		
		with self.subTest("id"):
			self.assertUnicode(metric.id)
			self.assertReadOnly(metric.id, _instance=metric, _property="id")

		with self.subTest("horizontal"):
			self.assertBool(metric.horizontal)
			self.assertEqual(metric.horizontal, False) # "This is used for stem metrics. so only use this for font.stems"

		with self.subTest("filter"):
			self.assertIsNone(metric.filter)
			# test mutability
			tetsFilter = NSPredicate.predicateWithFormat_('(category == "Letter")')
			metric.filter = tetsFilter
			self.assertEqual(metric.filter, tetsFilter)
			self.assertIsInstance(metric.filter, NSPredicate)
			metric.filter = None
			self.assertIsNone(metric.filter)

		with self.subTest("title()"):
			self.assertEqual(metric.title(), "Ascender")

		with self.subTest("titles()"):
			self.assertEqual(metric.titles(), ["Ascender"])

	def test_GSFont_stems(self):
		"""
		- ( ) hoizontal 
		"""
		font = self.font

		# self.assertIsInstance(font.stems[0], GSFontInfoValueSingle)
		self.assertIsInstance(font.stems[0], GSMetric)

		with self.subTest("horizontal"):
			self.assertBool(font.stems[0].horizontal)
			self.assertEqual(font.stems[0].horizontal, True)

		#TODO get working testvalues
		#self.assertList(font.stems, assertType=False, testValues=[...])
		with self.assertRaises(TypeError) as ctx:
			font.stems[12.4]
		self.assertEqual("keys must be integers or strings, not float", str(ctx.exception))

		self.assertEqual(font.stems['hStem0'], font.stems[0])

		with self.assertRaises(KeyError) as ctx:
			font.stems['nonExistingName']
		self.assertEqual("'No stem for key nonExistingName'", str(ctx.exception))

	def test_GSFont_glyphs(self):
		font = self.font
		self.assertGreaterEqual(len(list(font.glyphs)), 1)
		self.assertIs(font['a'], font.glyphs['a'])  # direct access
		self.assertEqual(font.glyphs[u'ä'], font.glyphs['adieresis'])
		self.assertEqual(font.glyphs['00E4'], font.glyphs['adieresis'])
		self.assertEqual(font.glyphs['00e4'], font.glyphs['adieresis'])
		with self.assertRaises(TypeError):
			font.glyphs[1.4]
		with self.assertRaises(NameError):
			font.glyphs.append(GSGlyph('adieresis'))


	def test_GSFont_classes(self):
		font = self.font
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
		with self.assertRaises(TypeError):
			font.classes[1.23]

	def test_GSFont_features(self):
		font = self.font
		font.features = []
		testFeature = GSFeature('liga', 'sub f i by fi;')
		self.assertList(font.features, assertType=False, testValues=[
				testFeature,
				copy.copy(GSFeature('liga', 'sub f l by fl;'))])
		font.features.append(testFeature)
		self.assertListEqual( list(font.features), [testFeature])
		self.assertIsNotNone(font.features['liga'].__repr__())
		self.assertEqual(len(font.features), 1)
		self.assertIn('<GSFeature "liga">', str(font.features))
		self.assertEqual('sub f i by fi;', font.features['liga'].code)
		del(font.features['liga'])
		with self.assertRaises(TypeError):
			font.features[12.43]

	def test_GSFont_featurePrefixes(self):
		font = self.font
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
		with self.assertRaises(TypeError):
			font.featurePrefixes[1.23]

	def test_GSFont_kerning(self):
		font = self.font
		test_kerning = {"C4872ECA-A3A9-40AB-960A-1DB2202F16DE": {"@MMK_L_A": {"@MMK_R_J": -22}}}
		# GSFont.kerning
		self.assertDict(font.kerning, assertType=False)
		old_kerning = font.kerning
		font.kerning = test_kerning
		self.assertEqual(font.kerning, test_kerning)
		font.kerning = old_kerning
		
		# GSFont.kerningVertical  #::Rafal
		"""To set a value, it is better to use the method GSFont.setKerningForPair(). This ensures a better data integrity (and is faster)."""
		self.assertDict(font.kerningVertical, assertType=False)
		old_kerning = font.kerningVertical
		font.kerningVertical = test_kerning
		self.assertEqual(font.kerningVertical, test_kerning)
		font.kerningVertical = old_kerning

		# GSFont.kerningRTL  #::Rafal
		"""To set a value, it is better to use the method GSFont.setKerningForPair(). This ensures a better data integrity (and is faster)."""
		self.assertDict(font.kerningRTL, assertType=False)
		old_kerning = font.kerningRTL
		font.kerningRTL = test_kerning
		self.assertEqual(font.kerningRTL, test_kerning)
		font.kerningRTL = old_kerning		

	def test_GSFont_userData(self):
		font = self.font
		self.assertIsNotNone(font.userData)
		font.userData["TestData"] = 42
		self.assertEqual(font.userData["TestData"], 42)
		del(font.userData["TestData"])
		self.assertIsNone(font.userData["TestData"])

	def test_GSFont_tempData(self):
		font = self.font
		self.assertIsNotNone(font.tempData)
		font.tempData["TestData"] = 42
		self.assertEqual(font.tempData["TestData"], 42)
		del(font.tempData["TestData"])
		self.assertIsNone(font.tempData["TestData"])		

	def test_GSFont_customParameters(self):
		font = self.font
		font.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'
		self.assertEqual(font.customParameters['trademark'], 'ThisFont is a trademark by MyFoundry.com')
		# self.assertList(font.customParameters, assertType=False, testValues=[
		# 		GSCustomParameter('hello0', 'world0'),
		# 		GSCustomParameter('hello1', 'world1'),
		# 		copy.copy(GSCustomParameter('hello2', 'world2'))])
		# ???: ^ What’s the intention here? Fails with the test font. Shall it compare with another, empty font (because then it would pass) <MF @GS>
		del(font.customParameters['trademark'])
		with self.assertRaises(TypeError):
			font.customParameters[12.3]

	def test_GSFont_grid(self):
		font = self.font
		self.assertInteger(font.grid)
		# TODO: test against float and throw if float.
		old_grid = font.grid
		font.grid = 9
		self.assertEqual(font.grid, 9)
		
		# GSFont.gridSubDivisions
		self.assertInteger(font.gridSubDivisions)
		# TODO: test against float and throw if float.
		old_gridSubDivisions = font.gridSubDivisions
		font.gridSubDivisions = 11
		self.assertEqual(font.gridSubDivisions, 11)
		
		# GSFont.gridLength
		self.assertFloat(font.gridLength)
		self.assertReadOnly(font.gridLength, _instance=font, _property='gridLength')
		# assert that gridLength == grid / gridSubDivisions
		self.assertAlmostEqual(font.gridLength, 9./11)
		font.grid = old_grid
		font.gridSubDivisions = old_gridSubDivisions
		self.assertAlmostEqual(font.gridLength, float(font.grid)/font.gridSubDivisions)		

	## GSFont Methods

	@unittest.skipIf(SKIP_FILE_SAVING, "Don’t save when developping this file.")
	def test_GSFont_save_dotglyphs(self):
		font = self.font
		
		# GSFont.save()
		# Test saving early to not save in a bad state.
		# This still slightly mutates the test file.
		# font.save()
		# NOTE: ^ This does not work, as save() expects a file path (Docu says 'If no path is given, it saves to the existing location.')
		# Also, needs to be implemented again somewhere. <MF @GS>

		copypath = PathToTestFile[:-7] + "-copy.glyphs"
		font.save(path=copypath, makeCopy=True)
		with self.assertRaises(ValueError):
			font.save(path="wrong.extension")
		
		self.assertIsFile(copypath)
	
	@unittest.skip("Test not implemented")
	def test_GSFont_save_dotglyphspackage(self):
		pass

	@unittest.skipIf(GSApplication.versionNumber < 3.2, 'UFO saving with `GSFont({PATH})` [should work with 3.2] <MF>')
	def test_GSFont_save_dotufo(self):
		font = self.font
		copypath_ufo = PathToTestFile[:-7] + "-copy.ufo"
		font.save(path=copypath_ufo, makeCopy=True)
		with self.assertRaises(ValueError):
			font.save(path="wrong.extension")

		self.assertIsFile(copypath_ufo) # TODO: UFO not created #1471 <MF @GS>

	@unittest.skip("Test not implemented")
	def test_instance_export(self):
		pass # [OTF, WOFF, WOFF2, TTF, UFO, VARIABLE]

	@unittest.skip("Test not implemented")
	def test_addInstanceAsMaster(self):
		pass # maybe inside GSFont test <@MF>

	def test_GSFont_kerning(self):
		"""To set a value, it is better to use the method GSFont.setKerningForPair(). This ensures a better data integrity (and is faster)."""
		font = self.font

		with self.subTest("GSFont.setKerningForPair()"):
			font.setKerningForPair(font.masters[0].id, 'a', 'a', -10)
		
		with self.subTest("GSFont.kerningForPair()"):
			self.assertEqual(font.kerningForPair(font.masters[0].id, 'a', 'a'), -10)
		
		with self.subTest("GSFont.removeKerningForPair()"):
			font.removeKerningForPair(font.masters[0].id, 'a', 'a')
			self.assertIsNone(font.kerningForPair(font.masters[0].id, 'a', 'a'))


	@unittest.skip("Test not implemented")
	def test_GSFont_kerningRTL(self):
		"""To set a value, it is better to use the method GSFont.setKerningForPair(). This ensures a better data integrity (and is faster)."""
		pass	

	@unittest.skip("Test not implemented")
	def test_GSFont_kerningVertical(self):
		"""To set a value, it is better to use the method GSFont.setKerningForPair(). This ensures a better data integrity (and is faster)."""
		pass


	#::Rafal
	def test_GSCustomParameter(self):
		font = self.font

		font.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'
		customParameter = font.customParameters[0]

		with self.subTest("name"):
			self.assertUnicode(customParameter.name)

		with self.subTest("value"):
			self.assertUnicode(customParameter.value)

		with self.subTest("parent"):
			self.assertEqual(customParameter.parent, font)

		# ??
		del(font.customParameters['trademark'])

	#::Rafal
	def test_GSClass(self):
		font = self.font
		
		feaClass = font.classes[0]
		
		with self.subTest("name"):
			self.assertUnicode(feaClass.name)

		with self.subTest("code"):
			self.assertUnicode(feaClass.code)

		with self.subTest("automatic"):
			self.assertInteger(feaClass.automatic)

		with self.subTest("active"):
			self.assertBool(feaClass.active)

		with self.subTest("tempData"):
			self.assertIsNotNone(feaClass.tempData)
			feaClass.tempData["TestData"] = 42
			self.assertEqual(feaClass.tempData["TestData"], 42)
			del(feaClass.tempData["TestData"])
			self.assertIsNone(feaClass.tempData["TestData"])
	
	#::Rafal
	def test_GSFeaturePrefix(self):
		font = self.font
		
		featurePrefix = font.featurePrefixes[0]
		
		with self.subTest("name"):
			self.assertUnicode(featurePrefix.name)

		with self.subTest("code"):
			self.assertUnicode(featurePrefix.code)

		with self.subTest("automatic"):
			self.assertBool(featurePrefix.automatic)

		with self.subTest("active"):
			self.assertBool(featurePrefix.active)

	def test_GSFeature(self):
		font = self.font
		
		feature = font.features[0]

		with self.subTest("name"):
			self.assertUnicode(feature.name)

		with self.subTest("code"):
			self.assertUnicode(feature.code)

		with self.subTest("automatic"):
			self.assertBool(feature.automatic)

		with self.subTest("notes"):
			self.assertUnicode(feature.notes)

		with self.subTest("active"):
			self.assertBool(feature.active)

		with self.subTest("tempData"):
			tempData_len = len(feature.tempData)
			feature.tempData["test_key"] = 45
			self.assertEqual(feature.tempData["test_key"], 45)
			self.assertEqual(len(feature.tempData), tempData_len + 1)
			del feature.tempData["test_key"]
			self.assertEqual(len(feature.tempData), tempData_len)

	def test_GSFontMaster(self):
		font = self.font

		with self.subTest("copy master"):
			self.assertEqual(len(font.axes), 1)
			master = font.masters[0]
			masterCopy = copy.copy(master)
			self.assertIsNotNone(masterCopy.__repr__())
		
		with self.subTest("id"):
			self.assertString(master.id, allowNone=False)

		# GSFontMaster.font
		with self.subTest("font"):
			self.assertIs(master.font, font)
		
		with self.subTest("name"):
			self.assertString(master.name, allowNone=False)
		
		with self.subTest("axes"):
			self.assertIsNotNone(master.axes)
			self.assertEqual(len(master.axes), 1)
			for val in master.axes:
				self.assertFloat(val)
			with self.assertRaises(TypeError):
				master.axes['a']
		
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

		with self.subTest("metrics"):
			self.assertList(master.metrics, assertType=False)
			for metric in master.metrics:
				self.assertIsInstance(metric, GSMetricValue)
			
		with self.subTest("ascender"):
			self.assertFloat(master.ascender)
		
		with self.subTest("capHeight"):
			self.assertFloat(master.capHeight)
		
		with self.subTest("xHeight"):
			self.assertFloat(master.xHeight)
		
		with self.subTest("descender"):
			self.assertFloat(master.descender)
		
		with self.subTest("italicAngle"):
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
		
		with self.subTest("stems"):#::Rafal
			oldStems = master.stems
			master.stems = [10, 15, 20, 25, 30]
			self.assertEqual(len(list(master.stems)), 5)
			master.stems = oldStems
			for stem in master.stems:
				self.assertFloat(stem)
		
		with self.subTest("alignmentZones"):
			self.assertIsInstance(list(master.alignmentZones), list)
			for az in master.alignmentZones:
				self.assertIsInstance(az, GSAlignmentZone)
		
		with self.subTest("blueValues"):
			self.assertIsInstance(list(master.blueValues), list)
			for bv in master.blueValues:
				self.assertFloat(bv)
		
		with self.subTest("otherBlues"):
			self.assertIsInstance(list(master.otherBlues), list)
			for ob in master.otherBlues:
				self.assertFloat(ob)
		
		with self.subTest("guides"):
			master.guides = []
			self.assertEqual(len(master.guides), 0)
			newGuide = GSGuide()
			newGuide.position = NSPoint(100, 100)
			newGuide.angle = -10.0
			newGuide2 = GSGuide()
			newGuide2.position = NSPoint(50, 150)
			newGuide2.angle = 15.0
			self.assertList(master.guides, assertType=False,
							testValues=[newGuide, newGuide2])

		with self.subTest("userData"):
			self.assertIsNotNone(master.userData)
			master.userData["TestData"] = 42
			self.assertEqual(master.userData["TestData"], 42)
			del(master.userData["TestData"])
			self.assertIsNone(master.userData["TestData"])
		
		with self.subTest("customParameter"):
			master.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'
			self.assertGreaterEqual(len(list(master.customParameters)), 1)
			del(master.customParameters['trademark'])



	def test_GSAlignmentZone(self):	
		font = self.font
		
		master = font.masters[0]
		
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

		with self.subTest("position"):
			self.assertFloat(zone.position)

		with self.subTest("size"):
			self.assertFloat(zone.size)


	def test_GSInstance(self):
		font = self.font
		
		instance = font.instances[0]
		copyInstance = copy.copy(instance)

		self.assertIsNotNone(copyInstance.__repr__())
		
		with self.subTest("font"):#::Rafal
			self.assertIsInstance(instance.font, GSFont)
		
		with self.subTest("active"):
			self.assertBool(instance.active)

		with self.subTest("visible"):
			self.assertBool(instance.visible)
		
		with self.subTest("name"):
			self.assertString(instance.name)
		
		with self.subTest("weightClass"):
			self.assertInteger(instance.weightClass)
			with self.assertRaises(TypeError):
				instance.weightClass = 'a'

		with self.subTest("weightClassName"):
			self.assertString(instance.weightClassName)
			self.assertReadOnly(instance.weightClassName, _instance=instance, _property='weightClassName')
		
		with self.subTest("widthClass"):
			self.assertInteger(instance.widthClass)
			with self.assertRaises(TypeError):
				instance.widthClass = 'a'

		with self.subTest("widthClassName"):
			self.assertString(instance.widthClassName)
			self.assertReadOnly(instance.widthClassName, _instance=instance, _property='widthClassName',)

		with self.subTest("axes"):
			self.assertIsNotNone(instance.axes)
			self.assertEqual(len(instance.axes), 1)

		with self.subTest("isItalic"):
			self.assertBool(instance.isItalic)
		
		with self.subTest("isBold"):
			self.assertBool(instance.isBold)
		
		with self.subTest("linkStyle"):
			self.assertString(instance.linkStyle)
		
		with self.subTest("familyName"):
			self.assertString(instance.familyName)
		
		with self.subTest("preferredFamily"):
			self.assertString(instance.preferredFamily)
		
		with self.subTest("preferredSubfamilyName"):
			self.assertString(instance.preferredSubfamilyName)
		
		with self.subTest("windowsFamily"):
			self.assertString(instance.windowsFamily)
		
		with self.subTest("windowsStyle"):
			self.assertString(instance.windowsStyle)
		
		with self.subTest("windowsLinkedToStyle"):
			self.assertString(instance.windowsLinkedToStyle)
		
		with self.subTest("fontName"):
			self.assertString(instance.fontName)
		
		with self.subTest("fullName"):
			self.assertString(instance.fullName)

		with self.subTest("designerURL"):
			self.assertString(instance.designerURL)

		with self.subTest("manufacturerURL"):
			self.assertString(instance.manufacturerURL)
		
		with self.subTest("customParameters"):
			instance.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'
			self.assertGreaterEqual(len(instance.customParameters), 1)
			del(instance.customParameters['trademark'])
		
		with self.subTest("instanceInterpolations"):
			self.assertIsInstance(dict(instance.instanceInterpolations), dict)
		
		with self.subTest("manualInterpolation"):
			self.assertBool(instance.manualInterpolation)
		
		with self.subTest("interpolatedFont"):
			self.assertIsInstance(instance.interpolatedFont, GSFont)
		
		with self.subTest("userData"):
			self.assertIsNotNone(instance.userData)
			instance.userData["TestData"] = 42
			self.assertEqual(instance.userData["TestData"], 42)
			del(instance.userData["TestData"])
			self.assertIsNone(instance.userData["TestData"])
		
		with self.subTest("tempData"):
			self.assertIsNotNone(instance.tempData)
			instance.tempData["TestData"] = 42
			self.assertEqual(instance.tempData["TestData"], 42)
			del(instance.tempData["TestData"])
			self.assertIsNone(instance.tempData["TestData"])
		
		## Methods
		
		with self.subTest("generate()"):
			path = os.path.join(os.path.dirname(__file__), 'GlyphsUnitTestSans-Thin.otf')
			result = instance.generate(FontPath=path)
			self.assertEqual(result, True)
			self.assertTrue(os.path.exists(path))
			if os.path.exists(path):
				os.remove(path)

		# GSInstance.lastExportedFilePath #::Rafal
		# self.assertString(insrtance.lastExportedFilePath)
 
		with self.subTest("addAsMaster"):#::Rafal
			oldNumbnerOfMasters = len(instance.font.masters)
			instance.addAsMaster()
			self.assertEqual(len(instance.font.masters), oldNumbnerOfMasters + 1)

		#::Rafal
		with self.subTest("properties of GSInstance"):
			propertyKeys = [
				'compatibleFullName',
				'compatibleFullNames',
				'copyright',
				'copyrights',
				'description',
				'descriptions',
				'designer',
				'designers',
				'familyName',
				'familyNames',
				'license',
				'licenses',
				'manufacturer',
				'manufacturers',
				'preferredFamilyName',
				'preferredFamilyNames',
				'preferredSubfamilyName',
				'preferredSubfamilyNames',
				'sampleText',
				'sampleTexts',
				'styleMapFamilyName',
				'styleMapFamilyNames',
				'styleMapStyleName',
				'styleMapStyleNames',
				'styleName',
				'styleNames',
				'trademark',
				'trademarks',
				'variableStyleName',
				'variableStyleNames'
			]

			# testing ammount of properties
			#TODO: self.assertEqual(len(instance.properties), len(propertyKeys)/2)

			# testing if empty properties return None

			for k in propertyKeys:
				a = getattr(instance, k)
				if isinstance(a, GlyphsApp.Proxy):
					self.assertEqual(a.values(), None)
				else:
					self.assertEqual(a, None)

			# testing assignment for properties

			for k in propertyKeys:
				if k[-1] != "s":
					a = setattr(instance, k, "test singlular")
				else:
					a = getattr(instance, k)
					a["ENG"] = "test localised"
			
			# testing assignment for properties

			for k in propertyKeys:
				if k[-1] != "s":
					a = setattr(instance, k, "test singlular")
					self.assertString(a)
				else:
					a = getattr(instance, k)
					self.assertIsInstance(a["ENG"], GSFontInfoValue)
					self.assertEqual(a["ENG"].value, "test localised")

			# testing deletion of plural properties
			for k in propertyKeys:
				if k[-1] == "s":
					a = getattr(instance, k)
					del a['ENG']




	def test_GSGlyph(self):
		"""
		- (x) parent
		- (x) layers
		- (x) font
		- (x) name
		- (x) unicode
		- (x) string
		- (x) id
		- (x) locked
		- (x) category
		- (x) storeCategory
		- (x) subCategory
		- (x) storeSubCategory
		- (x) case
		- (x) storeCase
		- (x) script
		- (x) storeScript
		- (x) direction
		- (x) productionName
		- (x) storeProductionName
		- (x) sortName
		- (x) sortNameKeep
		- (x) storeSortName
		- (x) glyphInfo
		- (x) leftKerningGroup
		- (x) leftKerningKey
		- (x) rightKerningGroup
		- (x) rightKerningKey
		- (x) topKerningGroup
		- (x) topKerningKey
		- (x) bottomKerningKey
		- (x) bottomKerningKey
		- (x) leftMetricsKey
		- (x) rightMetricsKey
		- (x) widthMetricsKey
		- (x) export
		- (x) color
		- (x) colorObject
		- (x) note
		- (x) selected --> UI
		- (x) mastersCompatible
		- (x) userData
		- (x) smartComponentAxes --> own test
		- (x) tags
		- (x) lastChange

		- (x) beginUndo()
		- (x) endUndo()
		- (x) updateGlyphInfo()
		- (x) duplicate()
		"""
		# font = Glyphs.font
		font = self.font

		glyph = font.glyphs['a'].duplicate('a.test')
		glyph = copy.copy(glyph)
		glyph.parent = font

		with self.subTest("parent"):
			self.assertIs(glyph.parent, font)

		with self.subTest("font"):
			self.assertIs(glyph.font, font)
		
		with self.subTest("layers"):
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
			with self.assertRaises(TypeError):
				glyph.layers[12.3]
		
		with self.subTest("name"):
			self.assertUnicode(glyph.name)
			with self.assertRaises(NameError):
				glyph.name = 'A'
		
		# Get a glyph directly, because the duplicated glyph a.test does not have its unicode values set
		realglyph = font.glyphs['a']
		with self.subTest("unicode"):
			self.assertUnicode(glyph.unicode)
			self.assertEqual(realglyph.unicode, '0061')

		with self.subTest("unicodes"):
			self.assertIn(realglyph.unicode, realglyph.unicodes)

		with self.subTest("production"):
			self.assertString(glyph.production)
		
		with self.subTest("string"):
			self.assertIsInstance(realglyph.string, unicode)
			self.assertEqual(realglyph.string, 'a')
		
		with self.subTest("id"):
			self.assertIsInstance(glyph.id, str)

		with self.subTest("locked"):
			self.assertBool(glyph.locked)
		
		with self.subTest("category"):
			self.assertIsInstance(glyph.category, (unicode, objc.pyobjc_unicode, type(None)))
		
		with self.subTest("storeCategory"):
			self.assertBool(glyph.storeCategory)
		
		with self.subTest("subCategory"):
			self.assertIsInstance(glyph.subCategory, (unicode, objc.pyobjc_unicode, type(None)))
		
		with self.subTest("storeSubCategory"):
			self.assertBool(glyph.storeSubCategory)

		with self.subTest("case"):
			self.assertInteger(glyph.case)

		with self.subTest("storeCase"):
			self.assertBool(glyph.storeCase)

		with self.subTest("direction"):
			self.assertInteger(glyph.direction)

		with self.subTest("storeDirection"):
			self.assertBool(glyph.storeDirection)

		with self.subTest("script"):
			self.assertIsInstance(glyph.script, (unicode, objc.pyobjc_unicode, type(None)))

		with self.subTest("storeScript"):
			self.assertBool(glyph.storeScript)
		
		with self.subTest("productionName"):
			self.assertIsInstance(glyph.productionName, (unicode, objc.pyobjc_unicode, type(None)))
		
		with self.subTest("storeProductionName"):
			self.assertBool(glyph.storeProductionName)

		with self.subTest("tags"):
			self.assertList(glyph.tags, assertType=False, testValues=["tag1", "tag2", "tag3"])
		
		with self.subTest("glyphInfo"):
			self.assertIsInstance(glyph.glyphInfo, (GSGlyphInfo, type(None)))

		with self.subTest("sortName"):
			self.assertString(glyph.sortName)

		with self.subTest("sortNameKeep"):
			self.assertString(glyph.sortNameKeep)

		with self.subTest("storeSortName"):
			self.assertBool(glyph.storeSortName)

		with self.subTest("glyphDataEntryString()"):
			self.assertString(glyph.glyphDataEntryString())
		
		with self.subTest("leftKerningGroup"):
			self.assertUnicode(glyph.leftKerningGroup)
		
		with self.subTest("rightKerningGroup"):
			self.assertUnicode(glyph.rightKerningGroup)
		
		with self.subTest("topKerningGroup"):
			self.assertUnicode(glyph.topKerningGroup)
		
		with self.subTest("bottomKerningGroup"):
			self.assertUnicode(glyph.bottomKerningGroup)

		with self.subTest("leftKerningKey"):
			self.assertString(glyph.leftKerningKey)

		with self.subTest("rightKerningKey"):
			self.assertString(glyph.rightKerningKey)

		with self.subTest("topKerningKey"):
			self.assertString(glyph.topKerningKey)

		with self.subTest("bottomKerningKey"):
			self.assertString(glyph.bottomKerningKey)

		with self.subTest("leftMetricsKey"):
			self.assertUnicode(glyph.leftMetricsKey)

		with self.subTest("rightMetricsKey"):
			self.assertUnicode(glyph.rightMetricsKey)
		
		with self.subTest("widthMetricsKey"):
			self.assertUnicode(glyph.widthMetricsKey)
		
		with self.subTest("export"):
			self.assertBool(glyph.export)
		
		with self.subTest("color"):
			self.assertInteger(glyph.color)
		
		with self.subTest("colorObject"):
			glyph.color = 1
			self.assertIsInstance(glyph.colorObject, NSColor)
			glyph.colorObject = (255, 255, 0)
		
		with self.subTest("note"):
			self.assertUnicode(glyph.note)
		
		with self.subTest("mastersCompatible"):
			self.assertIsInstance(glyph.mastersCompatible, bool)
		
		with self.subTest("userData"):
			self.assertIsNotNone(glyph.userData)
			glyph.userData["TestData"] = 42
			self.assertEqual(glyph.userData["TestData"], 42)
			del(glyph.userData["TestData"])
			self.assertIsNone(glyph.userData["TestData"])
		
		with self.subTest("smartComponentAxes"):
			pass # postponed to its own test
		
		with self.subTest("lastChange"):
			glyph.name = "a.test2"
			self.assertIsInstance(glyph.lastChange, datetime.datetime)
			glyph.name = "a.test1"
		
		## Methods
		glyph.beginUndo()
		glyph.endUndo()

		with self.subTest("updateGlyphInfo()"):
			# some random samples:
			glyph.updateGlyphInfo()
			self.assertEqual(glyph.glyphInfo.name, "a.test1")
			self.assertEqual(glyph.glyphInfo.script, "latin")
			self.assertEqual(glyph.glyphInfo.case, GSLowercase)
			self.assertIsNone(glyph.glyphInfo.unicode)
			# self.assertIsNone(glyph.glyphInfo.unicode2)
			self.assertIsNone(glyph.glyphInfo.subCategory)
			self.assertIsNone(glyph.glyphInfo.components)

		with self.subTest("duplicate"):
			# Duplicate default
			duplicateName = "a.test1.001"
			self.assertIsNone(font.glyphs[duplicateName])
			glyph.duplicate()
			self.assertIsNotNone(font.glyphs[duplicateName])
			del font.glyphs[duplicateName]
			# Duplicate with custom name
			duplicateName = "a.dupe"
			self.assertIsNone(font.glyphs[duplicateName])
			glyph.duplicate(duplicateName)
			self.assertIsNotNone(font.glyphs[duplicateName])
			del font.glyphs[duplicateName]

		with self.subTest("delete Glyph"):
			del font.glyphs["a.test"]

	def test_GSLayer(self):
		# font = Glyphs.font
		font = self.font

		glyph = font.glyphs['a']
		layer = glyph.layers[0]
		layer = copy.copy(layer)
		self.assertIsNotNone(layer.__repr__())
		layer.parent = glyph
		
		with self.subTest("parent"):
			self.assertEqual(layer.parent, glyph)
		
		with self.subTest("name"):
			self.assertUnicode(layer.name)

		with self.subTest("associatedMasterID"):
			self.assertEqual(layer.associatedMasterId, font.masters[0].id)

		with self.subTest("layerId"):
			self.assertEqual(layer.layerId, font.masters[0].id)
		
		with self.subTest("color"):
			self.assertString(layer.color)
		
		with self.subTest("colorObject"):
			layer.color = 1
			self.assertIsInstance(layer.colorObject, NSColor)
		
		# GSLayer.components
		# -> own test

		with self.subTest("guides"):
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
			with self.assertRaises(TypeError):
				layer.guides['a']

		with self.subTest("annotations"):
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
			with self.assertRaises(TypeError):
				layer.annotations['a']

		with self.subTest("hints"):
			layer = font.glyphs['a'].layers[0]
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
			with self.assertRaises(TypeError):
				layer.hints['a']

		with self.subTest("anchors"):
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
			with self.assertRaises(TypeError):
				layer.anchors[12.3]

		# GSLayer.paths
		# has its own test

		# GSLayer.shapes
		# self.assertList(layer.shapes, assertType=False, testValues=[
		# 		GSPath(), GSPath(), copy.copy(GSPath())])
		# ???: ^ What’s the intention here? Fails with the test font. Shall it compare with another, empty font (because then it would pass) <MF @GS>
		with self.assertRaises(TypeError):
			layer.shapes['a']
		
		with self.subTest("selection"):
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

		with self.subTest("LSB"):
			self.assertFloat(layer.LSB)
		
		with self.subTest("RSB"):
			self.assertFloat(layer.RSB)

		with self.subTest("TSB"):
			self.assertFloat(layer.TSB)

		with self.subTest("BSB"):
			self.assertFloat(layer.BSB)

		with self.subTest("width"):
			self.assertFloat(layer.width)

		with self.subTest("vertWidth"):
			self.assertFloat(layer.vertWidth, allowNone=True)

		with self.subTest("vertOrigin"):
			self.assertFloat(layer.vertOrigin, allowNone=True)

		with self.subTest("ascender"):
			self.assertFloat(layer.ascender)

		with self.subTest("descender"):
			self.assertFloat(layer.descender)

		with self.subTest("leftMetricsKey"):
			self.assertUnicode(layer.leftMetricsKey)

		with self.subTest("rightMetricsKey"):
			self.assertUnicode(layer.rightMetricsKey)

		with self.subTest("widthMetricsKey"):
			self.assertUnicode(layer.widthMetricsKey)

		with self.subTest("bounds"):
			self.assertIsInstance(layer.bounds, NSRect)

		with self.subTest("selectionBounds"):
			self.assertIsInstance(layer.selectionBounds, NSRect)

		with self.subTest("metrics"):
			for m in layer.metrics:
				if m.name == "Ascender":
					self.assertEqual(m.position, layer.ascender)
				elif m.name == "Descender":
					self.assertEqual(m.position, layer.descender)

		with self.subTest("background"):
			self.assertIn('GSBackgroundLayer', layer.background.__repr__())
		
		# GSLayer.backgroundImage
		# postponed to its own test

		with self.subTest("bezierPath"):
			self.assertIsInstance(layer.bezierPath, NSBezierPath)

		# GSLayer.openBezierPath
		# self.assertIsInstance(layer.openBezierPath, NSBezierPath) # TODO: is NULL if there are no open paths

		with self.subTest("completeBezierPath"):
			self.assertIsInstance(layer.completeBezierPath, NSBezierPath)

		# GSLayer.completeOpenBezierPath
		# self.assertIsInstance(layer.completeOpenBezierPath, NSBezierPath) # TODO: is NULL if there are no open paths

		with self.subTest("isAligned"):
			self.assertBool(layer.isAligned)
			self.assertReadOnly(layer.isAligned, _instance=layer, _property="isAligned")

		with self.subTest("isSpecialLayer"):
			self.assertBool(layer.isSpecialLayer)
			self.assertReadOnly(layer.isSpecialLayer, _instance=layer, _property="isSpecialLayer")

		with self.subTest("isMasterLayer"):
			self.assertBool(layer.isMasterLayer)
			self.assertReadOnly(layer.isMasterLayer, _instance=layer, _property="isMasterLayer")

		with self.subTest("italicAngle"):
			self.assertFloat(layer.italicAngle)
			self.assertReadOnly(layer.italicAngle, _instance=layer, _property='italicAngle')

		with self.subTest("userData"):
			self.assertIsNotNone(layer.userData)
			layer.userData["TestData"] = 42
			self.assertEqual(layer.userData["TestData"], 42)
			del(layer.userData["TestData"])
			self.assertIsNone(layer.userData["TestData"])

		with self.subTest("tempData"):
			self.assertIsNotNone(layer.tempData)
			layer.tempData["TestData"] = 42
			self.assertEqual(layer.tempData["TestData"], 42)
			del(layer.tempData["TestData"])
			self.assertIsNone(layer.tempData["TestData"])
		
		## Methods
		decomposedLayer = layer.copyDecomposedLayer()
		self.assertGreaterEqual(len(decomposedLayer.shapes), 1)
		
		layer = font.glyphs['adieresis'].layers[0]
		self.assertIsNotNone(layer)
		layer.decomposeComponents()
		self.assertGreaterEqual(len(layer.paths), 1)

		self.assertString(layer.compareString())
		
		layer.connectAllOpenPaths()
		
		layer.syncMetrics()

		layer.correctPathDirection()

		layer.removeOverlap()

		layer.roundCoordinates()

		layer.addNodesAtExtremes()
		
		transform = NSAffineTransform.new()
		transform.scaleXBy_yBy_(0.5, 0.5)
		layer.applyTransform(transform.transformStruct())

		# layer.beginChanges()
		# TODO: `'NoneType' object has no attribute 'beginUndoGrouping'` even though layer exists until here. <MF>
		# `beginUndoGrouping` is called on `layer.parent.undomanager`, it seems to be nil, here. <GS>

		# layer.endChanges()
		## TODO: ^ Re-enable once this is fixed <MF @MF @GS>

		layer.cutBetweenPoints(NSPoint(0, 100), NSPoint(layer.width, 100))

		intersections = layer.intersectionsBetweenPoints((-1000, 100), (layer.width+1000, 100))

		layer.addMissingAnchors()
		
		#layer.clearSelection()
		# already tested
		
		layer.swapForegroundWithBackground()
		layer.swapForegroundWithBackground()

		layer.reinterpolate()

		layer.clear()
		
		### MARK ### Glyphs.font.close()
		
		
	def test_smartComponents(self):
		font = self.font
		
		glyph = font.glyphs['_part.shoulder']
		
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
		layer = font.glyphs['n'].layers[0]
		layer.shapes[1].smartComponentValues['shoulderWidth'] = 30
		layer.shapes[1].smartComponentValues['crotchDepth'] = -77

		with self.assertRaises(TypeError):
			glyph.smartComponentAxes[12.3]


	def test_GSShapesComponents(self):
		# font = Glyphs.font
		font = self.font

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

		with self.subTest("position"):
			self.assertIsInstance(component.position, NSPoint)
			component.position = (20, 10)
			self.assertEqual(component.position, NSPoint(20, 10))

		with self.subTest("scale"):
			self.assertIsInstance(component.scale, NSPoint)
			component.scale = (2, 3)
			self.assertEqual(component.scale, NSPoint(2, 3))
		
		with self.subTest("rotation"):
			self.assertFloat(component.rotation)
		
		with self.subTest("userData"):
			self.assertIsNotNone(component.userData)
			component.userData["TestData"] = 42
			self.assertEqual(component.userData["TestData"], 42)
			del(component.userData["TestData"])
			self.assertIsNone(component.userData["TestData"])
		
		# GSComponent.componentName
		# GSComponent.component
		# GSComponent.componentLayer
		component.componentName = 'A'

		self.assertEqual(component.component, font.glyphs['A'])
		self.assertEqual(component.componentLayer, font.glyphs['A'].layers[layer.layerId])
		component.componentName = 'a'
		self.assertEqual(component.component, font.glyphs['a'])
		self.assertEqual(component.componentLayer, font.glyphs['a'].layers[layer.layerId])

		component = layer.shapes[0]

		with self.subTest("transform"):
			component.transform = (1.0, 0, 0, 1.0, 0, 0)
			self.assertEqual(component.transform, (1.0, 0, 0, 1.0, 0, 0))
			component.scale = (3, 5)
			self.assertEqual(component.transform, (3.0, 0, 0, 5.0, 0, 0))
			component.transform = (1.0, 0, 0, 1.0, 0, 0)

		with self.subTest("bounds"):
			self.assertIsInstance(component.bounds, NSRect)

		with self.subTest("automaticAlignment"):
			self.assertBool(component.automaticAlignment)

		with self.subTest("alignment"):
			#TODO
			self.assertIsNotNone(component.alignment)

		with self.subTest("locked"):
			self.assertBool(component.locked)

		with self.subTest("anchor"):
			self.assertUnicode(component.anchor)

		with self.subTest("selected"):
			self.assertBool(component.selected)
		
		# GSComponent.smartComponentValues
		# -> see test_smartComponents()
		
		with self.subTest("bezierPath"):
			self.assertIsInstance(component.bezierPath, NSBezierPath)

		with self.subTest("tempData"):
			component.tempData['testKey'] = font
			self.assertIs(component.tempData['testKey'], font)
			del component.tempData['testKey']

		## Methods
		component.applyTransform((.5, 0, 0, .5, 0, 0))
		component.decompose()
		
		del font.glyphs['adieresis.test']
		self.assertIsNone(font.glyphs['adieresis.test'])

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
		font = self.font

		layer = font.glyphs['a'].layers[0]
		path = layer.shapes[0]
		copyPath = copy.copy(path)
		self.assertIsNotNone(copyPath.__repr__())

		# Proxy
		pathCopy1 = copy.copy(path)
		pathCopy2 = copy.copy(pathCopy1)
		pathCopy3 = copy.copy(pathCopy2)
		self.assertList(layer.shapes, assertType=False, testValues=[
				pathCopy1, pathCopy2, pathCopy3])
		# !!!: `copy.copy(path)` breaks `path.parent` to be `None` <MF @GS>
		
		# GSPath.parent
		# self.assertIsNotNone(path)
		# self.assertIsNotNone(path.parent)
		# self.assertEqual(path.parent, font.glyphs['a'].layers[0])
		## TODO: ^ Re-enable once path.parent is fixed to be not lost by the copying <MF @MF @GS>

		# GSPath.nodes
		self.assertIsNotNone(list(path.nodes))
		newNode = GSNode(NSPoint(20,20))
		newNode1 = GSNode(NSPoint(10,10))
		newNode2 = GSNode(NSPoint(20,20))
		newNode3 = copy.copy(newNode)
		# self.assertList(path.nodes, assertType=False, testValues=[
		# 		newNode, newNode1, newNode2, newNode3])
		# ???:  ^ What’s the intention here? Fails with the test font. Shall it compare with another, empty font (because then it would pass) <MF @GS>
		with self.assertRaises(TypeError):
			path.nodes['a']

		with self.subTest("segments"):
			self.assertIsNotNone(list(path.segments))

		with self.subTest("closed"):
			self.assertBool(path.closed)
			# not readOnly

		with self.subTest("direction"):
			self.assertTrue(path.direction == 1 or path.direction == -1)

		with self.subTest("bounds"):
			self.assertIsInstance(path.bounds, NSRect)

		# GSPath.selected
		# self.assertBool(path.selected)
		# TODO: ^ Move to UI Test <MF @MF>

		with self.subTest("bezierPath"):
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
		font = self.font

		layer = font.glyphs['a'].layers[0]
		path = layer.shapes[0]
		node = path.nodes[0]
		self.assertIsNotNone(node.__repr__())
		
		with self.subTest("position"):
			self.assertIsInstance(node.position, NSPoint)

		with self.subTest("type"):
			self.assertTrue(node.type in [LINE, CURVE, OFFCURVE])
		
		with self.subTest("smooth"):
			self.assertBool(node.smooth)

		with self.subTest("selected"):
			self.assertBool(node.selected)

		with self.subTest("index"):
			self.assertInteger(node.index)
			self.assertReadOnly(node.index, _instance=node, _property='index')
			self.assertNotEqual(node.index, 9223372036854775807) # theoretically, this value could be maxint in a node, but in our test font it should be 0, I guess (taken from actual glyph, not orphan path)

		with self.subTest("nextNode"):
			self.assertIsInstance(node.nextNode, GSNode)

		with self.subTest("prevNode"):
			self.assertIsInstance(node.prevNode, GSNode)

		with self.subTest("name"):
			self.assertUnicode(node.name)
		
		with self.subTest("userData"):
			self.assertIsNotNone(node.userData)
			node.userData["TestData"] = 42
			self.assertEqual(node.userData["TestData"], 42)
			del(node.userData["TestData"])
			self.assertIsNone(node.userData["TestData"])
		
		## Methods

		node.makeNodeFirst()
		node.toggleConnection()




		# Copy, then test again
		node = copy.copy(node)
		self.assertEqual(node.index, 9223372036854775807) # theoretically, this value could be maxint in a node, but in our test font it should be 0, I guess (taken from actual glyph, not orphan path)

	def test_GSAnchor(self):
		font = self.font

		layer = font.glyphs['a'].layers[0]
		anchor = layer.anchors["top"]

		self.assertIsNotNone(anchor.__repr__())
		
		with self.subTest("position"):
			self.assertIsInstance(anchor.position, NSPoint)
		
		with self.subTest("selected"):
			self.assertBool(anchor.selected)

		with self.subTest("name"):
			self.assertUnicode(anchor.name)
			anchor.name = "top123"
			self.assertEqual(anchor.name, "top123")
		
		with self.subTest("userData"):
			self.assertIsNotNone(anchor.userData)
			anchor.userData["TestData"] = 42
			self.assertEqual(anchor.userData["TestData"], 42)
			del(anchor.userData["TestData"])
			self.assertIsNone(anchor.userData["TestData"])

	def test_GSGuide(self):
		font = self.font

		layer = font.glyphs['a'].layers[0]
		guide = layer.guides[0]
		
		with self.subTest("position"):
			self.assertIsInstance(guide.position, NSPoint)

		with self.subTest("lockAngle"):
			self.assertBool(guide.lockAngle)

		with self.subTest("angle"):
			self.assertFloat(guide.angle)
		
		with self.subTest("name"):
			self.assertIsNone(guide.name)
			guide.name = "test_guide"
			self.assertEqual(guide.name, "test_guide")

		with self.subTest("locked"):
			self.assertBool(guide.locked)
		
		with self.subTest("userData"):
			self.assertIsNotNone(guide.userData)
			guide.userData["TestData"] = 42
			self.assertEqual(guide.userData["TestData"], 42)
			del(guide.userData["TestData"])
			self.assertIsNone(guide.userData["TestData"])
		
		
	def test_GSBackgroundImage(self):
		font = self.font

		glyph = font.glyphs['A']
		layer = glyph.layers[0]
		
		layer.backgroundImage = GSBackgroundImage(os.path.join(os.path.dirname(PathToTestFile), 'A.jpg'))
		image = layer.backgroundImage
		copyImage = copy.copy(image)
		self.assertIsNotNone(copyImage.__repr__())
		
		
		with self.subTest("path"):
			self.assertEqual(image.path, os.path.abspath(os.path.join(os.path.dirname(PathToTestFile), 'A.jpg')))
		
		with self.subTest("image"):
			self.assertIsInstance(image.image, NSImage)
		
		with self.subTest("crop"):
			self.assertIsInstance(image.crop, NSRect)
			image.crop = NSRect(NSPoint(0, 0), NSPoint(100, 100))
		
		with self.subTest("locked"):
			self.assertBool(image.locked)
		
		with self.subTest("alpha"):
			self.assertInteger(image.alpha)
		
		with self.subTest("position"):
			self.assertIsInstance(image.position, NSPoint)

		with self.subTest("scale"):
			self.assertTrue(isinstance(image.scale, NSPoint))
			self.assertEqual(image.scale.x, 1)

		with self.subTest("rotation"):
			self.assertFloat(image.rotation)
		
		## Methods
		
		image.resetCrop()
		image.scaleWidthToEmUnits(layer.width)
		
		layer.backgroundImage = None


	def test_GSGlyphInfo(self):
		"""
		- ( ) name
		- ( ) productionName
		- ( ) category
		- ( ) subCategory
		- ( ) components
		- ( ) accents
		- ( ) anchors
		- ( ) unicode
		- ( ) unicode2
		- ( ) script
		- ( ) index
		- ( ) sortName
		- ( ) sortNameKeep
		- ( ) desc
		- ( ) altNames
		- ( ) direction
		- ( ) desc
		- ( ) case
		"""
		font = self.font

		info = font.glyphs['a'].glyphInfo
		self.assertIsNotNone(info.__repr__())

		with self.subTest("name"):
			self.assertEqual(info.name, 'a')

		with self.subTest("productionName"):
			self.assertEqual(info.productionName, None)

		with self.subTest("category"):
			self.assertEqual(info.category, 'Letter')

		with self.subTest("case"): # former subCategory?
			self.assertEqual(info.case, GSLowercase)

		with self.subTest("components"):
			self.assertIsNone(info.components)

			info = font.glyphs['adieresis'].glyphInfo
			self.assertIsInstance(list(info.components), list)

		with self.subTest("unicode"):
			self.assertEqual(info.unicode, '00E4')
			self.assertEqual(len(info.unicodes), 1)

		with self.subTest("accents"):
			info = Glyphs.glyphInfoForName('lam_alef-ar')
			self.assertIsInstance(list(info.accents), list)

		with self.subTest("anchors"):
			self.assertIsInstance(list(info.anchors), list)

		with self.subTest("index"):
			self.assertIsInstance(info.index, int)
		
		with self.subTest("sortName"):
			self.assertEqual(info.sortName, "ar0010_ar0009")

		with self.subTest("sortNameKeep"):
			self.assertEqual(info.sortNameKeep, "ar0900_ar0009")

		# GSGlyphInfo.desc
#		self.assertEqual(info.desc, "ARABIC LIGATURE LAM WITH ALEF ISOLATED FORM")

		with self.subTest("altNames"):
			self.assertEqual(info.altNames[0], "lamalefisolatedarabic")


	def test_Methods(self):

		with self.subTest("divideCurve()"):
			self.assertEqual(len(divideCurve(
				NSPoint(0, 0),
				NSPoint(50, 0),
				NSPoint(100, 50),
				NSPoint(100, 100),
				.5
				)), 7)

		with self.subTest("distance()"):
			self.assertEqual(distance(NSPoint(0, 0), NSPoint(0, 2)), 2.0)

		with self.subTest("addPoints()"):
			self.assertEqual(addPoints(NSPoint(0, 0), NSPoint(1, 2)), NSPoint(1, 2))

		with self.subTest("scalePoint()"):
			self.assertEqual(scalePoint(NSPoint(2, 2), 2), NSPoint(4, 4))

		# GetSaveFile(filetypes = ['glyphs'])
		# GetOpenFile()
		# GetFolder()
		# Message('Title', 'Message')
		# LogToConsole('Message')
		# LogError('Error message created in test code. Ignore it.')

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

		self.assertIsNotNone(MOVE)
		self.assertIsNotNone(LINE)
		self.assertIsNotNone(CURVE)
		self.assertIsNotNone(QCURVE)
		self.assertIsNotNone(OFFCURVE)
		self.assertIsNotNone(HOBBYCURVE)

		self.assertIsNotNone(GSSHARP)
		self.assertIsNotNone(GSSMOOTH)

		self.assertIsNotNone(TAG)
		self.assertIsNotNone(TOPGHOST)
		self.assertIsNotNone(STEM)
		self.assertIsNotNone(BOTTOMGHOST)
		self.assertIsNotNone(FLEX)
		self.assertIsNotNone(TTSNAP)
		self.assertIsNotNone(TTANCHOR)
		self.assertIsNotNone(TTSTEM)
		self.assertIsNotNone(TTSHIFT)
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
		self.assertIsNotNone(DOCUMENTEXPORTED)
		self.assertIsNotNone(DOCUMENTCLOSED)
		self.assertIsNotNone(TABDIDOPEN)
		self.assertIsNotNone(TABWILLCLOSE)
		self.assertIsNotNone(UPDATEINTERFACE)
		self.assertIsNotNone(MOUSEMOVED)
		self.assertIsNotNone(MOUSEDRAGGED)
		self.assertIsNotNone(MOUSEDOWN)
		self.assertIsNotNone(MOUSEUP)
		self.assertIsNotNone(CONTEXTMENUCALLBACK)


sys.argv = ["GlyphsAppTests"]

if __name__ == '__main__':
	### MARK ### import coverage  # pip3 install coverage
	### MARK ### cov = coverage.Coverage(include=["*/GlyphsApp/__init__.py"])
	### MARK ### cov.start()

	# Hides Docstring from Verbosis mode (e.g.`verbosity=2`)
	unittest.TestCase.shortDescription = lambda x: None

	unittest.main(exit=False, failfast=False, verbosity=PRINT_VERBOSE)

	### MARK ### cov.stop()
	### MARK ### cov.save()

	### MARK ### cov.html_report()
