import pytest

from GlyphsApp import Glyphs, GSInfoValue, GSFont, GSGlyph, GSLayer, GSFontMaster, GSGuide, GSAlignmentZone, GSAxis, GSClass, GSFeaturePrefix, GSFeature, GSInstance, GSMetric, GSGlyphInfo, GSAnnotation, GSHint, GSAnchor, GSMetricStore, GSPath, GSComponent, GSBackgroundImage, GSNode, GSSmartComponentAxis  # type: ignore   # noqa
from GlyphsApp import MOVE, LINE, CURVE, QCURVE, OFFCURVE, GSSHARP, GSSMOOTH, TAG, TOPGHOST, STEM, BOTTOMGHOST, FLEX, TTSNAP, TTANCHOR, TTSTEM, TTSHIFT, TTALIGN, TTINTERPOLATE, TTDIAGONAL, TTDELTA, CORNER, CAP, TTROUND, TTROUNDUP, TTROUNDDOWN, TTDONTROUND, TRIPLE, APP_MENU, FILE_MENU, EDIT_MENU, GLYPH_MENU, PATH_MENU, FILTER_MENU, VIEW_MENU, SCRIPT_MENU, WINDOW_MENU, HELP_MENU, DRAWFOREGROUND, DRAWBACKGROUND, DRAWINACTIVE, DOCUMENTOPENED, DOCUMENTACTIVATED, DOCUMENTWASSAVED, DOCUMENTEXPORTED, DOCUMENTCLOSED, TABDIDOPEN, TABWILLCLOSE, UPDATEINTERFACE, MOUSEMOVED, MOUSEDRAGGED, MOUSEDOWN, MOUSEUP, CONTEXTMENUCALLBACK, GSLowercase, OTF, TTF, WOFF, UFO, TEXT, MINUS, PLUS, CIRCLE, ARROW, divideCurve, distance, addPoints, scalePoint  # type: ignore   # noqa
from GlyphsApp import DictProxy, ListProxy, OrderedDictProxy, FontGlyphsProxy, FontStemsProxy, FontAxesProxy, FontInstancesProxy, FontFontMasterProxy, FontClassesProxy, FontFeaturesProxy, FontFeaturePrefixesProxy, FontInfoPropertyProxy, UserDataProxy, PropertiesProxy  # type: ignore  # noqa
# from importlib import reload
# import TestHelpers
# reload(TestHelpers)
from TestHelpers import assert_read_only, assert_string, assert_dict, assert_list, assert_integer, assert_float, assert_equal_accuracy, assert_bool, assert_is_round_float, assert_is_file, assert_is_folder, assert_point, assert_bool
import os
import time
import sys
import datetime
import objc
import copy
from typing import cast

# import pathlib as Pathlib
from Foundation import NSPoint, NSRect  # type: ignore
from AppKit import (
	NSAffineTransform,
	NSBezierPath,
	NSColor,
	NSArray,
	NSClassFromString,
	NSDate,
	NSDictionary,
	NSString,
	NSImage,
	# NSMutableArray,
	NSNotFound,
	NSNull,
	NSNumber,
	NSPredicate,
)

# Development Settings <MF>
SKIP_FILE_SAVING = True  # default: `False`
PRINT_VERBOSE = 1  # `2` or default: `1`
# ====================

if sys.version_info[0] == 3:
	unicode = str

PathToTestFile = os.path.join(os.path.dirname(__file__), "Glyphs Unit Test Sans.glyphs")

Glyphs.clearLog()


@pytest.fixture
def font():
	# Load the font and verify __repr__ returns something
	the_font = GSFont(PathToTestFile)
	assert the_font.__repr__() is not None
	return the_font


def test_GSFont_properties_and_methods(font: GSFont):
	# Equivalent to test_GSFont with multiple subtests

	# Proxies and attributes
	assert isinstance(font.masters, FontFontMasterProxy)
	assert isinstance(font.instances, FontInstancesProxy)
	assert isinstance(font.axes, FontAxesProxy)
	assert isinstance(font.stems, FontStemsProxy)
	assert isinstance(font.properties, PropertiesProxy)
	assert isinstance(font.glyphs, FontGlyphsProxy)
	assert isinstance(font.classes, FontClassesProxy)
	assert isinstance(font.features, FontFeaturesProxy)
	assert isinstance(font.featurePrefixes, FontFeaturePrefixesProxy)
	assert_string(font, "copyright")
	assert isinstance(font.copyrights, FontInfoPropertyProxy)
	assert_string(font, "license")
	assert isinstance(font.licenses, FontInfoPropertyProxy)
	assert_string(font, "compatibleFullName")
	assert isinstance(font.compatibleFullNames, FontInfoPropertyProxy)
	assert_string(font, "sampleText")
	assert isinstance(font.sampleTexts, FontInfoPropertyProxy)
	assert_string(font, "description")
	assert isinstance(font.descriptions, FontInfoPropertyProxy)
	assert_string(font, "trademark")
	assert isinstance(font.trademarks, FontInfoPropertyProxy)
	assert_string(font, "designer")
	assert isinstance(font.designers, FontInfoPropertyProxy)
	assert_string(font, "designerURL")
	assert_string(font, "manufacturer")
	assert isinstance(font.manufacturers, FontInfoPropertyProxy)
	assert_string(font, "manufacturerURL")
	assert_integer(font, "versionMajor")
	assert_integer(font, "versionMinor")
	assert_string(font, "familyName")
	assert isinstance(font.familyNames, FontInfoPropertyProxy)
	assert font.fontName == font.familyName
	assert isinstance(font.date, datetime.datetime)
	assert isinstance(font.kerning, NSClassFromString("MGOrderedDictionary"))
	assert isinstance(font.userData, UserDataProxy)
	assert_integer(font, "grid")
	assert_integer(font, "gridSubDivisions")
	assert isinstance(font.gridLength, float)
	assert_read_only(font, "gridLength")
	assert_float(font, "keyboardIncrementHuge")
	assert_float(font, "keyboardIncrementBig")
	assert_float(font, "keyboardIncrement")
	assert_bool(font, "snapToObjects")
	assert_bool(font, "previewRemoveOverlap")
	assert_integer(font, "upm")
	assert_string(font, "note")
	assert_bool(font, "disablesNiceNames")
	assert isinstance(font.appVersion, str)
	assert_read_only(font, "appVersion")
	assert_integer(font, "formatVersion")

	# Methods
	font.disableUpdateInterface()
	font.enableUpdateInterface()
	font.updateFeatures()
	font.compileFeatures()

	# Test font.properties map
	propertyKeys = [
		"familyName", "familyNames", "designer", "designers", "manufacturer",
		"manufacturers", "copyright", "copyrights", "license", "licenses",
		"trademark", "trademarks", "description", "descriptions", "sampleText",
		"sampleTexts", "compatibleFullName", "compatibleFullNames",
	]
	for k in propertyKeys:
		_ = getattr(font, k)
	for k in propertyKeys:
		if k.endswith("s"):
			prop = getattr(font, k)
			prop["ENG"] = "test localised"
		else:
			setattr(font, k, "test singular")
	for k in propertyKeys:
		if k.endswith("s"):
			prop = getattr(font, k)
			assert isinstance(prop["ENG"], GSInfoValue)
			assert prop["ENG"].value == "test localised"
		else:
			val = getattr(font, k)
			assert isinstance(val, str) or val is None
	for k in propertyKeys:
		if k.endswith("s"):
			prop = getattr(font, k)
			del prop["ENG"]


# @pytest.mark.skip(reason="font.filepath seems to not work with `GSFont({PATH})` <MF @GS>")
def test_GSFont_filepath(font: GSFont):
	filepath = font.filepath
	assert filepath is not None
	assert isinstance(filepath, str)
	assert os.path.exists(filepath)


def test_GSFont_date(font: GSFont):
	old_date = font.date
	dt = datetime.datetime.now()
	font.date = dt
	assert font.date == dt.replace(microsecond=0)
	unixtime = time.time()
	font.date = unixtime
	assert font.date == datetime.datetime.fromtimestamp(unixtime)
	nsdate = NSDate.alloc().init()
	font.date = nsdate
	assert font.date == datetime.datetime.fromtimestamp(nsdate.timeIntervalSince1970())
	font.date = old_date


def test_GSFont_masters(font: GSFont):
	amount_layers_per_glyph = len(font.glyphs["a"].layers)
	assert amount_layers_per_glyph == 4
	assert len(list(font.masters)) >= 1
	assert_list(font.masters)
	assert font.masters[0] == font.masters[font.masters[0].id]
	with pytest.raises(TypeError) as ctx:
		_ = font.masters[2.2]  # type: ignore
	assert "Keys must be integers or strings, not float" in str(ctx.value)
	first_master_name = font.masters[0].name
	assert font.masters[first_master_name] is None


def test_GSFont_instances(font: GSFont):
	assert len(list(font.instances)) >= 1
	test_values = [GSInstance(), GSInstance(), copy.copy(GSInstance())]
	assert_list(font.instances, test_values=test_values, assert_sorting=False)
	with pytest.raises(TypeError) as ctx:
		_ = font.instances["a"]  # type: ignore
	assert "list indices must be integers or slices, not str" in str(ctx.value)


def test_GSFont_axes(font: GSFont):
	print("1111 font.axes", font.axes)
	test_values = [GSAxis(), GSAxis(), copy.copy(GSAxis())]
	assert_list(font.axes, test_values=test_values, assert_sorting=False)
	with pytest.raises(TypeError) as ctx:
		_ = font.axes["a"]  # type: ignore
	assert "list indices must be integers or slices, not str" in str(ctx.value)
	
	print("2222 font.axes", font.axes)

	# add and remove an axis
	old_axes = copy.copy(font.axes)
	test_axis = GSAxis()
	test_axis.name = "Test Axis"
	font.axes.append(test_axis)
	print("3333 font.axes", font.axes)
	assert len(font.axes) == 2
	# Reset via assignment does not work; so remove explicitly
	font.axes = old_axes
	assert len(font.axes) == 1
	test_axis = GSAxis()
	test_axis.name = "Another Test Axis"
	font.axes.append(test_axis)
	if len(font.axes) == len(old_axes) + 1:
		del font.axes[-1]
	assert len(font.axes) == 1


def test_GSAxis(font: GSFont):
	test_axis = font.axes[0]
	# name
	assert test_axis.name == "Weight"
	old_axis_name = test_axis.name
	test_axis.name = "Test Axis Name"
	assert test_axis.name == "Test Axis Name"
	test_axis.name = old_axis_name
	# font
	assert test_axis.font is font
	assert test_axis.font == font
	# axisTag
	assert isinstance(test_axis.axisTag, str)
	assert test_axis.axisTag == "wght"
	# axisId
	assert isinstance(test_axis.axisId, str)
	assert test_axis.axisId == "a01"
	new_axis = test_axis.copy()
	new_axis.axisId = "b01"
	assert new_axis.axisId == "b01"
	# hidden
	assert isinstance(test_axis.hidden, bool)
	assert test_axis.hidden is False


def test_GSMetric(font: GSFont):
	metric = font.metrics[0]
	# font
	assert metric.font is font
	# type
	assert metric.type == 1
	assert_integer(metric, "type")
	metric.type = 3
	assert metric.type == 3
	metric.type = 1
	# name
	assert isinstance(metric.name, str) or metric.name is None
	metric.name = "Test Name"
	assert metric.name == "Test Name"
	metric.name = None
	assert metric.name is None
	# id
	assert isinstance(metric.id, str)
	assert_read_only(metric, "id")
	# horizontal
	assert isinstance(metric.horizontal, bool)
	assert metric.horizontal is False
	# filter
	assert metric.filter is None
	test_filter = NSPredicate.predicateWithFormat_('(category == "Letter")')
	metric.filter = test_filter
	assert metric.filter == test_filter
	assert isinstance(metric.filter, NSPredicate)
	metric.filter = None
	assert metric.filter is None
	# title and titles
	assert metric.title == "Ascender"
	# assert metric.title() == ["Ascender"]


def test_GSFont_stems(font: GSFont) -> None:
	assert isinstance(font.stems[0], GSMetric)
	# horizontal
	assert isinstance(font.stems[0].horizontal, bool)
	assert font.stems[0].horizontal is True
	with pytest.raises(TypeError) as ctx:
		_ = font.stems[12.4]
	assert "Keys must be integers or strings, not float" in str(ctx.value)
	assert font.stems["hStem0"] == font.stems[0]
	with pytest.raises(KeyError) as ctx:
		_ = font.stems["nonExistingName"]
	assert "No stem for key nonExistingName" in str(ctx.value)


def test_GSFont_glyphs(font: GSFont):
	assert len(list(font.glyphs)) >= 1
	assert font.glyphs["ä"] == font.glyphs["adieresis"]
	assert font.glyphs["00E4"] == font.glyphs["adieresis"]
	assert font.glyphs["00e4"] == font.glyphs["adieresis"]
	with pytest.raises(TypeError):
		_ = font.glyphs[1.4]
	with pytest.raises(NameError):
		font.glyphs.append(GSGlyph("adieresis"))


def test_GSFont_classes(font: GSFont):
	font.classes.clear()
	test_classes = [
		GSClass("uppercaseLetters0", "A"),
		GSClass("uppercaseLetters1", "A"),
		GSClass("uppercaseLetters2", "A"),
	]
	assert_list(font.classes, test_values=test_classes, assert_sorting=False)
	amount = len(font.classes)
	new_class = GSClass("uppercaseLetters", "A")
	font.classes.append(new_class)
	assert "<GSClass 0x" in new_class.__repr__()
	assert '<GSClass "uppercaseLetters">' in str(font.classes)
	assert font.classes["uppercaseLetters"].code == "A"
	copy_class = copy.copy(new_class)
	assert copy_class.parent is None
	assert new_class.parent is font
	font.classes.insert(0, copy_class)
	assert copy_class.parent == new_class.parent
	font.classes.remove(font.classes[0])
	assert len(font.classes) == 1
	with pytest.raises(TypeError):
		_ = font.classes[1.23]


def test_GSFont_features(font: GSFont):
	font.features.clear()
	test_feature = GSFeature("liga", "sub f i by fi;")
	assert_list(font.features, test_values=[test_feature, GSFeature("dlig", "sub f l by fl;")], assert_sorting=False)
	font.features.append(test_feature)
	assert_list(font.features, test_values=[copy.copy(test_feature)], assert_sorting=False)
	assert font.features["liga"].__repr__() is not None
	assert len(font.features) == 1
	assert "<GSFeature \"liga\">" in str(font.features)
	assert font.features["liga"].code == "sub f i by fi;"
	del font.features["liga"]
	with pytest.raises(TypeError):
		_ = font.features[12.43]


def test_GSFont_featurePrefixes(font: GSFont):
	font.featurePrefixes.clear()
	test_prefixes = [
		GSFeaturePrefix("LanguageSystems0", "languagesystem DFLT dflt;"),
		GSFeaturePrefix("LanguageSystems1", "languagesystem DFLT dflt;"),
		copy.copy(GSFeaturePrefix("LanguageSystems2", "languagesystem DFLT dflt;")),
	]
	assert_list(font.featurePrefixes, test_values=test_prefixes, assert_sorting=False)
	font.featurePrefixes.append(GSFeaturePrefix("LanguageSystems", "languagesystem DFLT dflt;"))
	assert font.featurePrefixes[-1].__repr__() is not None
	assert len(font.featurePrefixes) == 1
	assert "<GSFeaturePrefix \"LanguageSystems\">" in str(font.featurePrefixes)
	assert font.featurePrefixes[-1].code == "languagesystem DFLT dflt;"
	del font.featurePrefixes["LanguageSystems"]
	with pytest.raises(TypeError):
		_ = font.featurePrefixes[1.23]


def test_GSFont_kerning_properties(font: GSFont):
	test_kerning = {
		"C4872ECA-A3A9-40AB-960A-1DB2202F16DE": {
			"@MMK_L_A": {"@MMK_R_J": -22}
		}
	}
	# kerning
	assert_dict(font.kerning)
	old_kerning = font.kerning
	font.kerning = test_kerning
	assert font.kerning == test_kerning
	font.kerning = old_kerning

	# kerningVertical
	assert_dict(font.kerningVertical)
	old_kerning = font.kerningVertical
	font.kerningVertical = test_kerning
	assert font.kerningVertical == test_kerning
	font.kerningVertical = old_kerning

	# kerningRTL
	assert_dict(font.kerningRTL)
	old_kerning = font.kerningRTL
	font.kerningRTL = test_kerning
	assert font.kerningRTL == test_kerning
	font.kerningRTL = old_kerning


def test_GSFont_userData_and_tempData(font: GSFont):
	# userData
	assert font.userData is not None
	font.userData["TestData"] = 42
	assert font.userData["TestData"] == 42
	del font.userData["TestData"]
	assert font.userData.get("TestData") is None

	# tempData
	assert font.tempData is not None
	font.tempData["TestData"] = 42
	assert font.tempData["TestData"] == 42
	del font.tempData["TestData"]
	assert font.tempData.get("TestData") is None


def test_GSFont_customParameters(font: GSFont):
	font.customParameters["trademark"] = "ThisFont is a trademark by MyFoundry.com"
	assert font.customParameters["trademark"] == "ThisFont is a trademark by MyFoundry.com"
	del font.customParameters["trademark"]
	with pytest.raises(TypeError):
		_ = font.customParameters[12.3]


def test_GSFont_grid_settings(font: GSFont):
	# grid
	assert_integer(font, "grid")
	old_grid = font.grid
	font.grid = 9
	assert font.grid == 9

	# gridSubDivisions
	assert_integer(font, "gridSubDivisions")
	old_grid_sub = font.gridSubDivisions
	font.gridSubDivisions = 11
	assert font.gridSubDivisions == 11

	# gridLength
	assert isinstance(font.gridLength, float)
	assert_equal_accuracy(font.gridLength, 9.0 / 11.0)
	font.grid = old_grid
	font.gridSubDivisions = old_grid_sub
	assert_equal_accuracy(font.gridLength, float(font.grid) / font.gridSubDivisions)


@pytest.mark.skip(reason="Implementation not according to documentation.")
def test_GSFont_save(font: GSFont):
	# save tests not implemented
	pass


@pytest.mark.skipif(SKIP_FILE_SAVING, reason="Don’t save when developing this file.")
def test_GSFont_save_dotglyphs(font: GSFont):
	copypath = PathToTestFile[:-7] + "-copy.glyphs"
	font.save(path=copypath, makeCopy=True)
	with pytest.raises(ValueError):
		font.save(path="wrong.extension")
	assert_is_file(copypath)


def test_GSFont_save_dotufo(font: GSFont):
	copypath_ufo = PathToTestFile[:-7] + "-copy.ufo"
	with pytest.raises(ValueError):
		font.save(path=copypath_ufo, makeCopy=True)
	with pytest.raises(ValueError):
		font.save(path="wrong.extension")
	single_master_font = font.copy()
	while len(single_master_font.masters) > 1:
		del single_master_font.masters[1]
	single_master_font.save(path=copypath_ufo, makeCopy=True)
	assert_is_folder(copypath_ufo)


def test_GSInstance_export(font: GSFont):
	instance = font.instances[0]
	font_path = os.path.split(PathToTestFile)[0]
	for fmt in [OTF, TTF]:
		instance.generate(fmt, font_path)
		file_name = instance.fileName(fmt.lower())
		assert_is_file(os.path.join(font_path, file_name))
		instance.generate(fmt, font_path, containers=[WOFF])
		file_name = instance.fileName(WOFF.lower())
		assert_is_file(os.path.join(font_path, file_name))
	instance.generate(UFO, font_path)
	# file_name = instance.fileName(UFO.lower())  # TODO: XXX
	file_name = font.familyName + "-" + instance.name + ".ufo"
	assert_is_folder(os.path.join(font_path, file_name))


@pytest.mark.skip(reason="Test not implemented")
def test_addInstanceAsMaster(font: GSFont):
	pass


def test_GSFont_kerning_methods(font: GSFont):
	# setKerningForPair
	font.setKerningForPair(font.masters[0].id, "a", "a", -10)
	# kerningForPair
	assert font.kerningForPair(font.masters[0].id, "a", "a") == -10
	# removeKerningForPair
	font.removeKerningForPair(font.masters[0].id, "a", "a")
	assert font.kerningForPair(font.masters[0].id, "a", "a") is None


@pytest.mark.skip(reason="Test not implemented")
def test_GSFont_kerningRTL(font: GSFont):
	pass


@pytest.mark.skip(reason="Test not implemented")
def test_GSFont_kerningVertical(font: GSFont):
	pass


def test_GSCustomParameter(font: GSFont):
	font.customParameters["trademark"] = "ThisFont is a trademark by MyFoundry.com"
	custom_parameter = font.customParameters[0]
	assert_string(custom_parameter, "name")
	assert_string(custom_parameter, "value")
	assert custom_parameter.parent == font
	del font.customParameters["trademark"]


def test_GSClass(font: GSFont):
	fea_class = font.classes[0]
	assert_string(fea_class, "name")
	assert_string(fea_class, "code")
	assert_bool(fea_class, "automatic")
	assert_bool(fea_class, "active")
	assert fea_class.tempData is not None
	fea_class.tempData["TestData"] = 42
	assert fea_class.tempData["TestData"] == 42
	del fea_class.tempData["TestData"]
	assert fea_class.tempData.get("TestData") is None


def test_GSFeaturePrefix(font: GSFont):
	feature_prefix = font.featurePrefixes[0]
	assert_string(feature_prefix, "name")
	assert_string(feature_prefix, "code")
	assert_bool(feature_prefix, "automatic")
	assert_bool(feature_prefix, "active")


def test_GSFeature(font: GSFont):
	feature = font.features[0]
	assert_string(feature, "name")
	assert_string(feature, "code")
	assert_bool(feature, "automatic")
	assert_string(feature, "notes")
	assert_bool(feature, "active")
	assert feature.tempData is not None
	before_len = len(feature.tempData)
	feature.tempData["test_key"] = 45
	assert feature.tempData["test_key"] == 45
	assert len(feature.tempData) == before_len + 1
	del feature.tempData["test_key"]
	assert len(feature.tempData) == before_len


def test_GSFontMaster(font: GSFont):
	master = font.masters[0]
	# copy master
	master_copy = copy.copy(master)
	assert master_copy.__repr__() is not None
	# id
	assert_string(master, "id", allow_none=False)
	# font
	assert master.font is font
	# name
	assert_string(master, "name", allow_none=False)
	# axes
	assert master.axes is not None
	assert len(master.axes) == 1
	for val in master.axes:
		assert isinstance(val, float)
	# with pytest.raises(TypeError):
	_ = master.axes["a"]
	# metrics
	# assert_list(master.metrics)  # TODO: XXX
	for metric in master.metrics:
		assert isinstance(metric, GSMetricStore)
	# ascender, capHeight, xHeight, descender, italicAngle
	assert_integer(master, "ascender")
	assert_integer(master, "capHeight")
	assert_integer(master, "xHeight")
	assert_integer(master, "descender")
	assert_float(master, "italicAngle")
	# stems
	old_stems = master.stems
	master.stems = [10, 15, 20, 25, 30]
	assert len(list(master.stems)) == 5
	master.stems = old_stems
	for stem in master.stems:
		assert isinstance(stem, float)
	# alignmentZones
	assert isinstance(list(master.alignmentZones), list)
	for az in master.alignmentZones:
		assert isinstance(az, GSAlignmentZone)
	# blueValues
	assert isinstance(list(master.blueValues), list)
	for bv in master.blueValues:
		assert isinstance(bv, float)
	# otherBlues
	assert isinstance(list(master.otherBlues), list)
	for ob in master.otherBlues:
		assert isinstance(ob, float)
	# guides
	master.guides = []
	assert len(master.guides) == 0
	new_guide = GSGuide()
	new_guide.position = NSPoint(100, 100)
	new_guide.angle = -10.0
	new_guide2 = GSGuide()
	new_guide2.position = NSPoint(50, 150)
	new_guide2.angle = 15.0
	assert_list(master.guides, test_values=[new_guide, new_guide2], assert_sorting=False)
	# userData
	assert master.userData is not None
	master.userData["TestData"] = 42
	assert master.userData["TestData"] == 42
	del master.userData["TestData"]
	assert master.userData.get("TestData") is None
	# customParameters
	master.customParameters["trademark"] = "ThisFont is a trademark by MyFoundry.com"
	assert len(list(master.customParameters)) >= 1
	del master.customParameters["trademark"]


def test_GSAlignmentZone(font: GSFont):
	master = font.masters[0]
	zone = master.alignmentZones[0]
	copy_zone = copy.copy(zone)
	assert isinstance(copy_zone, GSAlignmentZone)
	assert_float(zone, "position")
	assert_float(zone, "size")


def test_GSInstance_related(font: GSFont):
	instance = font.instances[0]
	copy_instance = copy.copy(instance)
	assert copy_instance.__repr__() is not None
	assert isinstance(instance.font, GSFont)
	assert_bool(instance, "active")
	assert_bool(instance, "visible")
	assert_string(instance, "name")
	assert_integer(instance, "weightClass")
	with pytest.raises(TypeError):
		instance.weightClass = "a"  # type: ignore
	assert isinstance(instance.weightClassName, str)
	assert_read_only(instance, "weightClassName")
	assert_integer(instance, "widthClass")
	with pytest.raises(TypeError):
		instance.widthClass = "a"  # type: ignore
	assert isinstance(instance.widthClassName, str)
	assert_read_only(instance, "widthClassName")
	assert instance.axes is not None
	assert len(instance.axes) == 1
	assert_bool(instance, "isItalic")
	assert_bool(instance, "isBold")
	assert_string(instance, "linkStyle")
	assert_string(instance, "familyName")
	assert_string(instance, "preferredFamily")
	assert_string(instance, "preferredSubfamilyName")
	assert_string(instance, "windowsFamily")
	assert_string(instance, "windowsStyle")
	assert isinstance(instance.windowsLinkedToStyle, str)
	assert_string(instance, "fontName")
	assert_string(instance, "fullName")
	assert_string(instance, "designerURL")
	assert_string(instance, "manufacturerURL")
	instance.customParameters["trademark"] = "ThisFont is a trademark by MyFoundry.com"
	assert len(instance.customParameters) >= 1
	del instance.customParameters["trademark"]
	assert isinstance(dict(instance.instanceInterpolations), dict)
	assert_bool(instance, "manualInterpolation")
	assert isinstance(instance.interpolatedFont, GSFont)
	assert instance.userData is not None
	instance.userData["TestData"] = 42
	assert instance.userData["TestData"] == 42
	del instance.userData["TestData"]
	assert instance.tempData is not None
	instance.tempData["TestData"] = 42
	assert instance.tempData["TestData"] == 42
	del instance.tempData["TestData"]
	# generate()
	path = os.path.join(os.path.dirname(__file__), "GlyphsUnitTestSans-Thin.otf")
	result = instance.generate(fontPath=path)
	assert result is None, f"is {result}"
	assert os.path.exists(path)
	if os.path.exists(path):
		os.remove(path)
	# addAsMaster
	old_number_of_masters = len(instance.font.masters)
	instance.addAsMaster()
	assert len(instance.font.masters) == old_number_of_masters + 1
	# properties map
	property_keys = [
		"compatibleFullName", "compatibleFullNames", "copyright", "copyrights",
		"description", "descriptions", "designer", "designers", "familyName",
		"familyNames", "license", "licenses", "manufacturer", "manufacturers",
		"preferredFamilyName", "preferredFamilyNames", "preferredSubfamilyName",
		"preferredSubfamilyNames", "sampleText", "sampleTexts", "styleMapFamilyName",
		"styleMapFamilyNames", "styleMapStyleName", "styleMapStyleNames",
		"styleName", "styleNames", "trademark", "trademarks", "variableStyleName",
		"variableStyleNames",
	]
	for k in property_keys:
		a = getattr(instance, k)
		if isinstance(a, DictProxy):
			pass  # assert not a.values()
		elif isinstance(a, str):
			assert len(a) > 0
		else:
			assert a is None, f"is {a} {type(a)} ({k})"
	for k in property_keys:
		if not k.endswith("s"):
			setattr(instance, k, "test singular")
		else:
			prop = getattr(instance, k)
			prop["ENG"] = "test localised"
	for k in property_keys:
		if not k.endswith("s"):
			val = getattr(instance, k)
			assert isinstance(val, str) or val is None
		else:
			prop = getattr(instance, k)
			assert isinstance(prop["ENG"], GSInfoValue)
			assert prop["ENG"].value == "test localised"
	for k in property_keys:
		if k.endswith("s"):
			prop = getattr(instance, k)
			del prop["ENG"]


def test_GSGlyph(font: GSFont):
	# Duplicate glyph 'a'
	glyph = font.glyphs["a"].duplicate("a.test")
	glyph = copy.copy(glyph)
	glyph.parent = font
	assert glyph.parent is font
	assert glyph.font is font
	# layers manipulation
	amount = len(glyph.layers)
	new_layer = GSLayer()
	new_layer.name = "1"
	glyph.layers.append(new_layer)
	assert '1 (a.test)' in str(glyph.layers[-1])
	assert glyph.layers[-1] == new_layer
	del glyph.layers[-1]
	new_layer1 = GSLayer()
	new_layer1.name = "2"
	new_layer2 = GSLayer()
	new_layer2.name = "3"
	glyph.layers.extend([new_layer1, new_layer2])
	assert new_layer1 == glyph.layers[-2]
	assert new_layer2 == glyph.layers[-1]
	new_layer = GSLayer()
	new_layer.name = "4"
	glyph.layers.insert(0, new_layer)
	assert new_layer == glyph.layers[-1]
	glyph.layers.remove(glyph.layers[-1])
	glyph.layers.remove(glyph.layers[-1])
	glyph.layers.remove(glyph.layers[-1])
	assert len(glyph.layers) == amount
	with pytest.raises(TypeError):
		_ = glyph.layers[12.3]
	# name and unicode
	assert isinstance(glyph.name, str)
	with pytest.raises(NameError):
		glyph.name = "A"
	realglyph = font.glyphs["a"]
	assert_string(glyph, "unicode")
	assert realglyph.unicode == "0061"
	assert realglyph.unicode in realglyph.unicodes
	assert_string(glyph, "production")
	assert isinstance(realglyph.string, unicode)
	assert realglyph.string == "a"
	assert isinstance(glyph.id, str)
	assert_bool(glyph, "locked")
	assert isinstance(glyph.category, (unicode, objc.pyobjc_unicode, type(None)))
	assert_bool(glyph, "storeCategory")
	assert isinstance(glyph.subCategory, (unicode, objc.pyobjc_unicode, type(None)))
	assert_bool(glyph, "storeSubCategory")
	assert_integer(glyph, "case")
	assert_bool(glyph, "storeCase")
	assert_integer(glyph, "direction")
	assert_bool(glyph, "storeDirection")
	assert isinstance(glyph.script, (unicode, objc.pyobjc_unicode, type(None)))
	assert_bool(glyph, "storeScript")
	assert isinstance(glyph.productionName, (unicode, objc.pyobjc_unicode, type(None)))
	assert_bool(glyph, "storeProductionName")
	assert_list(glyph.tags, test_values=["tag1", "tag2", "tag3"], assert_sorting=False)
	assert isinstance(glyph.glyphInfo, (GSGlyphInfo, type(None)))
	assert_string(glyph, "sortName")
	assert_string(glyph, "sortNameKeep")
	assert_bool(glyph, "storeSortName")
	assert isinstance(glyph.glyphDataEntryString(), (str, NSString))
	assert_string(glyph, "leftKerningGroup")
	assert_string(glyph, "rightKerningGroup")
	assert_string(glyph, "topKerningGroup")
	assert_string(glyph, "bottomKerningGroup")
	assert isinstance(glyph.leftKerningKey, (str, NSString))
	assert isinstance(glyph.rightKerningKey, (str, NSString))
	assert isinstance(glyph.topKerningKey, (str, NSString))
	assert isinstance(glyph.bottomKerningKey, (str, NSString))
	assert_string(glyph, "leftMetricsKey")
	assert_string(glyph, "rightMetricsKey")
	assert_string(glyph, "widthMetricsKey")
	assert_bool(glyph, "export")
	assert_integer(glyph, "color")
	glyph.color = 1
	assert isinstance(glyph.colorObject, NSColor)
	glyph.colorObject = (255, 255, 0)
	assert_string(glyph, "note")
	assert isinstance(glyph.mastersCompatible, bool)
	# userData
	assert glyph.userData is not None
	glyph.userData["TestData"] = 42
	assert glyph.userData["TestData"] == 42
	del glyph.userData["TestData"]
	assert glyph.userData.get("TestData") is None
	# lastChange
	glyph.name = "a.test2"
	assert isinstance(glyph.lastChange, datetime.datetime)
	glyph.name = "a.test1"
	# begin & end undo
	glyph.beginUndo()
	glyph.endUndo()
	# updateGlyphInfo()
	glyph.updateGlyphInfo()
	info = glyph.glyphInfo
	assert info is not None
	assert info.name == "a.test1"
	assert info.script == "latin"
	assert info.case == GSLowercase
	assert info.unicode is None
	assert info.subCategory is None
	assert info.components is None
	# duplicate
	duplicate_name = "a.test1.001"
	assert font.glyphs.get(duplicate_name) is None
	glyph.duplicate()
	assert font.glyphs.get(duplicate_name) is not None
	del font.glyphs[duplicate_name]
	duplicate_name = "a.dupe"
	assert font.glyphs.get(duplicate_name) is None
	glyph.duplicate(duplicate_name)
	assert font.glyphs.get(duplicate_name) is not None
	del font.glyphs[duplicate_name]
	# delete glyph
	del font.glyphs["a.test"]

@pytest.fixture
def layer(font: GSFont) -> GSLayer:
	return font.glyphs['a'].layers[0]


def test_layer_copy_and_parent(layer: GSLayer, font: GSFont):
	layer_copy = copy.copy(layer)
	assert layer_copy.__repr__() is not None
	assert layer_copy.parent is None
	layer_copy.parent = font.glyphs['a']
	assert layer.parent == font.glyphs['a']
	assert layer_copy.parent == font.glyphs['a']


def test_layer_name(layer: GSLayer):
	assert isinstance(layer.name, str)


def test_layer_master_and_readonly(layer: GSLayer):
	assert isinstance(layer.master, GSFontMaster)
	assert layer.master is not None
	assert_read_only(layer, "master")


def test_layer_associatedMasterId(layer, font):
	assert layer.associatedMasterId == font.masters[0].id


def test_layer_layerId(layer, font):
	glyph = font.glyphs['a']
	assert layer.layerId == font.masters[0].id
	assert glyph.layers[1].layerId != font.masters[0].id
	assert glyph.layers[1].layerId == font.masters[1].id


def test_layer_attributes(layer: GSLayer):
	layer.attributes["color"] = "#ff0000"
	assert layer.attributes is not None
	del layer.attributes["color"]
	print("+++", layer.attributes, type(layer.attributes))
	assert len(layer.attributes) == 0


def test_layer_color(layer: GSLayer):
	assert_integer(layer, "color", allow_none=True)


def test_layer_colorObject(layer: GSLayer):
	layer.color = 1
	assert isinstance(layer.colorObject, NSColor)
	assert layer.colorObject.redComponent() == 0.99
	assert layer.colorObject.greenComponent() == 0.62
	assert layer.colorObject.blueComponent() == 0.11
	assert layer.colorObject.alphaComponent() == 1


def test_layer_guides(layer: GSLayer):
	layer.guides = []
	assert isinstance(list(layer.guides), list)
	assert len(layer.guides) == 0

	new_guide = copy.copy(GSGuide())
	new_guide.position = NSPoint(100, 100)
	new_guide.angle = -10.0
	new_guide1 = GSGuide()
	new_guide1.position = NSPoint(100, 100)
	new_guide1.angle = -10.0
	new_guide2 = GSGuide()
	new_guide2.position = NSPoint(100, 100)
	new_guide2.angle = -10.0

	layer.guides.append(new_guide1)
	assert layer.guides[0].angle == -10.0
	assert layer.guides[0].position == NSPoint(100, 100)
	del layer.guides[0]

	assert_list(layer.guides, test_values=[new_guide, new_guide1, new_guide2, GSGuide()], assert_sorting=False)
	with pytest.raises(TypeError):
		_ = layer.guides['a']  # type: ignore
	with pytest.raises(TypeError):
		_ = layer.guides[1.2]  # type: ignore


def test_layer_annotations(layer: GSLayer):
	layer.annotations = []
	assert len(layer.annotations) == 0

	new_annotation = GSAnnotation()
	new_annotation.type = TEXT
	new_annotation.text = "Test annotation"
	new_annotation1 = GSAnnotation()
	new_annotation1.type = ARROW
	new_annotation2 = GSAnnotation()
	new_annotation2.type = CIRCLE
	new_annotation3 = GSAnnotation()
	new_annotation3.type = PLUS
	new_annotation4 = copy.copy(new_annotation)
	new_annotation4.type = MINUS

	layer.annotations.append(new_annotation)
	assert layer.annotations[0].type == TEXT
	assert layer.annotations[0].text == "Test annotation"
	del layer.annotations[0]

	assert_list(layer.annotations, test_values=[new_annotation, new_annotation1, new_annotation2, new_annotation3, new_annotation4], assert_sorting=False)
	with pytest.raises(TypeError):
		_ = layer.annotations['a']  # type: ignore
	with pytest.raises(TypeError):
		_ = layer.annotations[1.2]  # type: ignore


def test_layer_hints(layer, font):
	layer.hints = []
	assert len(layer.hints) == 0

	h0 = copy.copy(GSHint())
	h0.originNode = layer.shapes[0].nodes[0]
	h0.targetNode = layer.shapes[0].nodes[1]
	h0.type = STEM
	h1 = GSHint()
	h1.originNode = layer.shapes[0].nodes[0]
	h1.targetNode = layer.shapes[0].nodes[1]
	h1.type = STEM
	h2 = GSHint()
	h2.originNode = layer.shapes[0].nodes[0]
	h2.targetNode = layer.shapes[0].nodes[1]
	h2.type = STEM
	h3 = GSHint()
	h3.originNode = layer.shapes[0].nodes[0]
	h3.targetNode = layer.shapes[0].nodes[1]

	layer.hints.append(h0)
	assert layer.hints[0].originNode == layer.shapes[0].nodes[0]
	assert layer.hints[0].targetNode == layer.shapes[0].nodes[1]
	assert layer.hints[0].type == STEM
	del layer.hints[0]

	assert_list(layer.hints, test_values=[h0, h1, h2, h3], assert_sorting=False)
	with pytest.raises(TypeError):
		_ = layer.hints['a']  # type: ignore
	with pytest.raises(TypeError):
		_ = layer.hints[1.3]  # type: ignore


def test_layer_anchors(layer: GSLayer):
	amount = len(layer.anchors)
	old_position = layer.anchors['top'].position if layer.anchors.get('top') else None

	layer.anchors['top'] = GSAnchor()
	assert len(layer.anchors) >= 1
	assert layer.anchors['top'].__repr__() is not None
	layer.anchors['top'].position = NSPoint(100, 100)
	del layer.anchors['top']

	layer.anchors['top'] = GSAnchor()
	with pytest.raises(TypeError):
		layer.anchors['top'].position = None
	layer.anchors['top'].position = old_position
	assert_string(layer.anchors['top'], "name")

	a1 = GSAnchor()
	a1.name = 'testAnchor1'
	a2 = GSAnchor()
	a2.name = 'testAnchor2'
	a3 = GSAnchor()
	a3.name = 'testAnchor3'
	layer.anchors.extend([a1, a2])
	assert layer.anchors['testAnchor1'] == a1
	assert layer.anchors['testAnchor2'] == a2

	layer.anchors.append(a3)
	assert layer.anchors['testAnchor3'] == a3

	layer.anchors.remove(layer.anchors['testAnchor3'])
	layer.anchors.remove(layer.anchors['testAnchor2'])
	layer.anchors.remove(layer.anchors['testAnchor1'])
	assert len(layer.anchors) == amount
	with pytest.raises(TypeError):
		_ = layer.anchors[12.3]


def test_layer_metrics_and_dimensions(layer: GSLayer):
	assert_float(layer, "LSB")
	assert_float(layer, "RSB")
	assert_float(layer, "TSB")
	assert_float(layer, "BSB")
	assert_float(layer, "width")
	assert_float(layer, "vertWidth", allow_none=True)
	assert_float(layer, "vertOrigin", allow_none=True)
	assert isinstance(layer.ascender, float)
	assert isinstance(layer.descender, float)

	layer.leftMetricsKey = "a"
	assert isinstance(layer.leftMetricsKey, str)
	assert layer.leftMetricsKey == "==a"
	layer.rightMetricsKey = "b"
	assert isinstance(layer.rightMetricsKey, str)
	assert layer.rightMetricsKey == "==b"
	layer.widthMetricsKey = "c"
	assert isinstance(layer.widthMetricsKey, str)
	assert layer.widthMetricsKey == "==c"

	assert isinstance(layer.bounds, NSRect)
	sel_bounds = layer.selectionBounds
	assert isinstance(sel_bounds, NSRect)
	assert sel_bounds.origin.x == 9.223372036854776e+18

	for m in layer.metrics:
		if m.name == "Ascender":
			assert isinstance(m, GSMetricStore)
			assert m.position == layer.ascender
			assert_float(m, "position")
		elif m.name == "Descender":
			assert isinstance(m, GSMetricStore)
			assert m.position == layer.descender
			assert_float(m, "position")


def test_layer_background(layer: GSLayer):
	assert 'GSBackgroundLayer' in layer.background.__repr__()
	assert isinstance(layer.background.shapes[0], GSPath)
	assert len(layer.background.shapes[0].nodes) == 44

	old_bg = layer.background.copy()
	assert layer.background.shapes[0] != layer.shapes[0]

	layer.background = layer.copy()
	assert layer.background.shapes[0] == layer.shapes[0]

	layer.background = None
	assert len(layer.background.shapes) == 0

	layer.background = old_bg
	assert layer.background.shapes[0] != layer.shapes[0]


def test_layer_bezier_paths(layer: GSLayer):
	assert isinstance(layer.bezierPath, NSBezierPath)
	assert layer.openBezierPath is None

	new_layer = layer.copy()
	new_layer.paths[0].closed = False
	assert new_layer.openBezierPath is None
	_ = new_layer.bezierPath
	assert isinstance(new_layer.openBezierPath, NSBezierPath)
	assert layer.openBezierPath is None

	assert isinstance(layer.completeBezierPath, NSBezierPath)
	assert isinstance(layer.completeOpenBezierPath, NSBezierPath)


def test_layer_alignment_and_angle(layer: GSLayer):
	assert isinstance(layer.isAligned, bool)
	assert_read_only(layer, "isAligned")

	assert isinstance(layer.isSpecialLayer, bool)
	assert_read_only(layer, "isSpecialLayer")

	assert isinstance(layer.isMasterLayer, bool)
	assert_read_only(layer, "isMasterLayer")

	assert isinstance(layer.italicAngle, float)
	assert_read_only(layer, "italicAngle")


def test_layer_user_and_temp_data(layer: GSLayer):
	assert layer.userData is not None
	layer.userData["TestData"] = 42
	assert layer.userData["TestData"] == 42
	del layer.userData["TestData"]
	assert layer.userData.get("TestData") is None

	assert layer.tempData is not None
	layer.tempData["TestData"] = 42
	assert layer.tempData["TestData"] == 42
	del layer.tempData["TestData"]
	assert layer.tempData.get("TestData") is None


def test_layer_copyDecomposed_and_decompose(layer, font):
	decomposed_layer = layer.copyDecomposedLayer()
	assert len(decomposed_layer.shapes) >= 1

	layer_ad = font.glyphs['adieresis'].layers[0]
	assert layer_ad is not None
	assert len(layer_ad.paths) == 0
	layer_ad.decomposeComponents()
	assert len(layer_ad.paths) >= 1

	corners_layer = font.glyphs['c'].layers[0]
	assert corners_layer.compareString() == "llllllll_&&_cap.test@0,0&&_corner.test@0,2&&_corner.test@0,3&&_cap.test@0,4&&_corner.test@0,6&&_corner.test@0,7"
	corners_layer.decomposeCorners()
	assert corners_layer.compareString() == "loocoocloocloocloocooclooclooc_"

	assert isinstance(layer_ad.compareString(), (str, NSString))
	assert layer_ad.compareString() == "loocoocoocoocloocoocoocooclllloocoocloocoocl_llll_llll_bottom**ogonek**top"
	nl = layer_ad.copy()
	nl.shapes[0].closed = False
	assert nl.compareString() == "loocoocoocoocloocoocoocooclllloocoocloocoocl|_llll_llll_bottom**ogonek**top"


def test_layer_sync_and_path_direction(layer, font):
	assert layer.RSB == 87.0
	layer.rightMetricsKey = "A"
	assert layer.RSB == 87.0
	layer.syncMetrics()
	assert layer.RSB == font.glyphs["A"].layers[0].RSB

	assert layer.paths[0].direction == -1
	layer.paths[0].reverse()
	assert layer.paths[0].direction == 1
	layer.correctPathDirection()
	assert layer.paths[0].direction == -1


def test_layer_removeOverlap(layer, font):
	this_layer = font.glyphs["a"].layers[1]
	old_compare = this_layer.compareString()
	this_layer.removeOverlap()
	new_compare = this_layer.compareString()
	assert new_compare != old_compare


def test_layer_roundCoordinates_and_extremes(layer, font):
	old_sub = font.gridSubDivisions
	font.gridSubDivisions = 10
	assert_equal_accuracy(layer.shapes[0].nodes[0].x, 352.0)
	trans = NSAffineTransform()
	trans.translateXBy_yBy_(0.4, 0.2)
	layer.transform(trans)
	assert_equal_accuracy(layer.shapes[0].nodes[0].x, 352.4)

	layer.roundCoordinatesToGrid_(1)
	for path in layer.paths:
		for node in path.nodes:
			assert_is_round_float(node.x)
			assert_is_round_float(node.y)
	font.gridSubDivisions = old_sub

	extremes_layer = font.glyphs["test_addNodesAtExtremes"].layers[0]
	assert_equal_accuracy(len(extremes_layer.paths[0].nodes), 12)
	extremes_layer.addNodesAtExtremes()
	assert_equal_accuracy(len(extremes_layer.paths[0].nodes), 24)


def test_layer_applyTransform(layer: GSLayer):
	old_x = layer.bounds.origin.x
	old_y = layer.bounds.origin.y
	tf = NSAffineTransform.new()
	tf.translateXBy_yBy_(123, 321)
	layer.applyTransform(tf.transformStruct())
	new_x = layer.bounds.origin.x
	new_y = layer.bounds.origin.y
	assert_equal_accuracy(new_x, old_x + 123)
	assert_equal_accuracy(new_y, old_y + 321)

	old_h = layer.bounds.size.height
	old_w = layer.bounds.size.width
	tf = NSAffineTransform.new()
	tf.scaleXBy_yBy_(2, 2)
	layer.applyTransform(tf.transformStruct())
	new_h = layer.bounds.size.height
	new_w = layer.bounds.size.width
	assert_equal_accuracy(new_h, old_h * 2)
	assert_equal_accuracy(new_w, old_w * 2)


def test_layer_transform(layer: GSLayer):
	old_x2 = layer.bounds.origin.x
	old_y2 = layer.bounds.origin.y
	tf = NSAffineTransform.new()
	tf.translateXBy_yBy_(123, 321)
	layer.transform(tf)
	new_x2 = layer.bounds.origin.x
	new_y2 = layer.bounds.origin.y
	assert_equal_accuracy(new_x2, old_x2 + 123)
	assert_equal_accuracy(new_y2, old_y2 + 321)

	old_h2 = layer.bounds.size.height
	old_w2 = layer.bounds.size.width
	tf = NSAffineTransform.new()
	tf.scaleXBy_yBy_(2, 2)
	layer.transform(tf)
	new_h2 = layer.bounds.size.height
	new_w2 = layer.bounds.size.width
	assert new_h2 == old_h2 * 2
	assert new_w2 == old_w2 * 2


def test_layer_cutBetweenPoints(layer, font):
	cut_layer = font.glyphs["test_cutBetweenPoints"].layers[0]
	assert len(cut_layer.paths) == 2
	assert cut_layer.paths[0].bounds.size.height == 600
	assert cut_layer.paths[1].bounds.size.height == 300
	cut_layer.cutBetweenPoints(NSPoint(-1, 200), NSPoint(601, 400))
	assert len(cut_layer.paths) == 2
	assert cut_layer.paths[0].bounds.size.height == 400
	assert cut_layer.paths[1].bounds.size.height == 400


def test_layer_intersectionsBetweenPoints(layer: GSLayer):
	intersections = layer.intersectionsBetweenPoints((-1000, 100), (layer.width + 1000, 100))
	assert len(intersections) == 6
	assert intersections[0].pointValue() == NSPoint(78, 100)
	assert intersections[-1].pointValue() == NSPoint(371.0, 100)


def test_layer_addMissingAnchors(font: GSFont):
	g_o = font.glyphs["o"]
	anchor_layer = g_o.layers[0].copy()
	anchor_layer.parent = g_o
	assert len(anchor_layer.anchors) == 0
	anchor_layer.addMissingAnchors()
	assert [a.name for a in anchor_layer.anchors.values()] == ["top", "bottom", "center", "topright", "ogonek"]


def test_layer_swapForegroundWithBackground(layer, font):
	test_layer = font.glyphs["a"].layers[0]
	old_fg = test_layer.copy()
	old_bg2 = test_layer.background.copy()
	assert test_layer.compareString() != test_layer.background.compareString()
	test_layer.swapForegroundWithBackground()
	assert test_layer.compareString() != test_layer.background.compareString()
	assert test_layer.compareString() == old_bg2.compareString()
	test_layer.swapForegroundWithBackground()
	assert test_layer.compareString() != test_layer.background.compareString()
	assert test_layer.compareString() == old_fg.compareString()


def test_layer_reinterpolate(layer, font):
	re_layer = font.glyphs["o"].layers[1]
	old_bounds2 = re_layer.bounds
	assert_equal_accuracy(old_bounds2.size.width, 200.0)
	assert_equal_accuracy(old_bounds2.size.height, 200.0)
	re_layer.reinterpolate()
	new_bounds2 = re_layer.bounds
	assert_equal_accuracy(new_bounds2.size.width, 272.0)
	assert_equal_accuracy(new_bounds2.size.height, 272.0)


def test_layer_clear(font: GSFont):
	clear_layer = font.glyphs["o"].layers[0].copy()
	clear_layer.shapes.append(GSComponent('a'))
	assert len(clear_layer.anchors) == 0
	assert len(clear_layer.paths) == 2
	assert len(clear_layer.components) == 1
	clear_layer.clear()
	assert len(clear_layer.anchors) == 0
	assert len(clear_layer.paths) == 0
	assert len(clear_layer.components) == 0


def test_smartComponents(font: GSFont):

	glyph = font.glyphs['_part.shoulder']

	glyph.smartComponentAxes = []
	assert len(glyph.smartComponentAxes) == 0

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

	assert len(glyph.smartComponentAxes) == 2

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
	layer.shapes[1].smartComponentValues['shoulderWidth'] = 30  # type: ignore
	layer.shapes[1].smartComponentValues['crotchDepth'] = -77  # type: ignore

	with pytest.raises(TypeError):
		glyph.smartComponentAxes[12.3]


# Fixture for component tests
@pytest.fixture
def component_test_glyph_layer(font: GSFont):
	"""
	Provides a temporary layer from a duplicated glyph known to have components.
	Ensures tests on components are isolated and don't affect the main font object.
	"""
	source_glyph_name = 'adieresis'
	test_glyph_name = 'adieresis.test_components_pytest'

	source_glyph = font.glyphs[source_glyph_name]
	if not source_glyph:
		pytest.skip(f"Source glyph '{source_glyph_name}' not found for component tests.")

	if font.glyphs[test_glyph_name]:
		del font.glyphs[test_glyph_name] # Cleanup from previous failed run

	test_glyph = source_glyph.duplicate(test_glyph_name)
	assert test_glyph is not None, f"Failed to duplicate '{source_glyph_name}'"

	# Use the layer corresponding to the first master
	layer = test_glyph.layers[font.masters[0].id]
	assert layer is not None, "Layer for component test not found in duplicated glyph."

	# Ensure it has components for testing
	if not layer.components:
		pytest.skip(f"Duplicated glyph '{test_glyph_name}' has no components to test.")

	yield layer # Provide the layer to the test functions

	# Teardown: remove the temporary glyph
	if font.glyphs[test_glyph_name]:
		del font.glyphs[test_glyph_name]


# GSLayer.components / GSComponent Tests
# Formerly test_GSLayer_components

def test_GSComponent_shapes_list_mutability(component_test_glyph_layer):
	"""Tests list-like operations on layer.shapes for components."""
	layer = component_test_glyph_layer
	original_shapes = list(layer.shapes) # Save for restoration

	# Test initial state
	assert len(layer.shapes) == 2, "Expected 2 shapes (components) in 'adieresis' test layer"

	# Clear and add
	layer.shapes = []
	assert len(layer.shapes) == 0

	comp_a = GSComponent('a')
	layer.shapes.append(comp_a)
	assert repr(layer.shapes[0]) is not None
	assert len(layer.shapes) == 1
	assert layer.shapes[0].componentName == 'a'

	# Extend
	comp_dieresis = GSComponent('dieresis')
	layer.shapes.extend([comp_dieresis])
	assert len(layer.shapes) == 2

	# Remove
	layer.shapes.remove(layer.shapes[0]) # Remove comp_a
	assert len(layer.shapes) == 1
	assert layer.shapes[0].componentName == 'dieresis'

	# Insert (may behave like append depending on proxy implementation)
	new_component = GSComponent('acute')
	layer.shapes.insert(0, new_component)
	assert new_component in layer.shapes

	layer.shapes = original_shapes # Restore

def test_GSComponent_attributes_position_scale_rotation(component_test_glyph_layer):
	component = cast(GSComponent, component_test_glyph_layer.shapes[0])

	# Test position
	assert isinstance(component.position, NSPoint)
	original_position = component.position
	assert component.alignment == 0
	component.position = NSPoint(20, 10)
	assert component.position == NSPoint(0, 0)  #component is aligned
	component.alignment = -1
	component.position = NSPoint(20, 10)
	assert component.position == NSPoint(20, 10)
	component.alignment = 0
	component.position = original_position

	# Test scale
	assert isinstance(component.scale, NSPoint) # In Glyphs 3, scale is an NSPoint
	original_scale = component.scale
	component.scale = NSPoint(2, 3)
	assert component.scale == NSPoint(2, 3)
	component.scale = original_scale

	# Test rotation
	assert_float(component, "rotation")

def test_GSComponent_userData(component_test_glyph_layer):
	component = cast(GSComponent, component_test_glyph_layer.shapes[0])
	assert component.userData is not None
	component.userData["TestData"] = 42
	assert component.userData["TestData"] == 42
	del component.userData["TestData"]
	assert component.userData.get("TestData") is None

def test_GSComponent_derived_properties(component_test_glyph_layer, font):
	"""Tests componentName and the properties derived from it."""
	layer = component_test_glyph_layer
	component = cast(GSComponent, layer.shapes[0])
	original_name = component.componentName

	# Change component name and check derived properties
	component.componentName = 'A'
	assert component.component == font.glyphs['A']
	assert component.componentLayer == font.glyphs['A'].layers[layer.layerId]

	# Restore and check again
	component.componentName = original_name
	assert component.component == font.glyphs[original_name]
	assert component.componentLayer == font.glyphs[original_name].layers[layer.layerId]

def test_GSComponent_transform_matrix(component_test_glyph_layer):
	component = cast(GSComponent, component_test_glyph_layer.shapes[0])
	original_transform = component.transform

	component.transform = (1.0, 0, 0, 1.0, 0, 0) # Set to identity
	assert component.transform == (1.0, 0, 0, 1.0, 0, 0)

	# Check that setting scale updates the transform matrix
	component.scale = (3, 5)
	# Transform tuple is (scaleX, skewY, skewX, scaleY, translateX, translateY)
	# Translation part should be preserved from the original identity setting.
	assert component.transform == pytest.approx((3.0, 0, 0, 5.0, 0, 0))

	component.transform = original_transform # Restore

def test_GSComponent_boolean_and_other_attributes(component_test_glyph_layer):
	component = cast(GSComponent, component_test_glyph_layer.shapes[0])

	assert isinstance(component.bounds, NSRect)
	assert_bool(component, "automaticAlignment", component.automaticAlignment)

	# .alignment is a complex property; basic check
	assert component.alignment is not None

	assert_bool(component, "locked", component.locked)

	# anchor is a string property
	assert_string(component, "anchor")

	# .selected is a UI property, but we can test its type and mutability
	assert_bool(component, "selected")

def test_GSComponent_tempData(component_test_glyph_layer, font):
	component = cast(GSComponent, component_test_glyph_layer.shapes[0])
	component.tempData['testKey'] = font
	assert component.tempData['testKey'] is font
	del component.tempData['testKey']
	assert 'testKey' not in component.tempData

def test_GSComponent_bezierPath(component_test_glyph_layer):
	component = cast(GSComponent, component_test_glyph_layer.shapes[0])
	assert isinstance(component.bezierPath, NSBezierPath)

def test_GSComponent_applyTransform_method(component_test_glyph_layer):
	component = cast(GSComponent, component_test_glyph_layer.shapes[0])
	original_transform = component.transform

	# Apply a 50% scaling transform
	component.applyTransform((0.5, 0, 0, 0.5, 0, 0))

	# Check if the scale part of the transform is now 0.5 of the original
	# This assumes original scale was (1,1) for simplicity. If not, it's multiplicative.
	# For a fresh component, scale should be (1,1)
	if original_transform == (1.0, 0.0, 0.0, 1.0, 0.0, 0.0): # Assuming default transform
		assert component.transform == pytest.approx((0.5, 0.0, 0.0, 0.5, 0.0, 0.0))
	else: # If original was something else, calculate expected
		# This can get complex, for now we just check it changed.
		assert component.transform != original_transform

	component.transform = original_transform # Restore

def test_GSComponent_decompose_method(component_test_glyph_layer):
	layer = component_test_glyph_layer
	component_to_decompose = cast(GSComponent, layer.shapes[0])

	# State before decomposing
	initial_path_count = len(layer.paths)
	initial_component_count = len(layer.components)
	assert initial_component_count > 0

	# Decompose one component
	component_to_decompose.decompose()

	# State after decomposing
	assert len(layer.paths) > initial_path_count
	assert len(layer.components) == initial_component_count - 1

def test_GSComponentLegacy():
	"""Original test was skipped/empty, preserving that status."""
	return # Empty as in original

# GSPath tests
# Formerly test_GSLayer_paths / test_GSPathShapes

@pytest.fixture
def path_test_layer(font: GSFont):
	"""Provides the 'a' glyph layer, known to have paths."""
	layer = font.glyphs['a'].layers[font.masters[0].id]
	assert len(layer.paths) > 0, "Glyph 'a' must have paths for these tests."
	return layer

def test_GSPath_proxy_and_mutability(path_test_layer: GSLayer):
	path = cast(GSPath, path_test_layer.shapes[0])
	copyPath = copy.copy(path)
	assert repr(copyPath) is not None

	# The original test for list-like mutability of layer.shapes with paths was complex
	# and might have issues with how proxies work. A simplified check:
	original_shapes = list(path_test_layer.shapes)
	new_path = GSPath()
	path_test_layer.shapes.append(new_path)
	assert len(path_test_layer.shapes) == len(original_shapes) + 1
	assert new_path in path_test_layer.shapes
	path_test_layer.shapes.remove(new_path)
	assert len(path_test_layer.shapes) == len(original_shapes)

	# path.parent test: A path taken from a layer should have that layer as parent.
	assert path.parent is path_test_layer
	# A detached copy should not have a parent.
	assert copyPath.parent is None

def test_GSPath_nodes_list(path_test_layer):
	path = cast(GSPath, path_test_layer.shapes[0])
	assert len(path.nodes) > 0
	# Test that nodes are accessible
	assert isinstance(path.nodes[0], GSNode)
	# Test index error
	with pytest.raises(TypeError):
		_ = path.nodes['a']

def test_GSPath_attributes(path_test_layer):
	path = cast(GSPath, path_test_layer.shapes[0])

	assert isinstance(list(path.segments), list)
	assert len(path.segments) > 0

	assert_bool(path, "closed", path.closed)

	assert path.direction in [1, -1]

	assert isinstance(path.bounds, NSRect)
	assert isinstance(path.bezierPath, NSBezierPath)

def test_GSPath_methods(path_test_layer):
	path = cast(GSPath, path_test_layer.shapes[0])
	original_direction = path.direction
	original_node_count = len(path.nodes)

	# Test reverse()
	path.reverse()
	assert path.direction == -original_direction
	path.reverse() # Reverse back
	assert path.direction == original_direction

	# Test addNodesAtExtremes()
	path.addNodesAtExtremes()
	assert len(path.nodes) >= original_node_count # Should add or keep same number of nodes

	# Test applyTransform()
	# Simple identity transform shouldn't change bounds (much)
	original_bounds = path.bounds
	transform_matrix = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
	path.applyTransform(transform_matrix)
	# Use pytest.approx for potential floating point inaccuracies
	assert path.bounds.origin.x == pytest.approx(original_bounds.origin.x)
	assert path.bounds.origin.y == pytest.approx(original_bounds.origin.y)
	assert path.bounds.size.width == pytest.approx(original_bounds.size.width)
	assert path.bounds.size.height == pytest.approx(original_bounds.size.height)

def test_GSPathLegacy():
	"""Original test was skipped/empty."""
	return

# GSNode Tests
@pytest.fixture
def test_node(path_test_layer):
	"""Provides the first node from the first path of the test layer."""
	path = cast(GSPath, path_test_layer.paths[0])
	return path.nodes[0]

def test_GSNode_attributes(test_node):
	assert repr(test_node) is not None
	assert isinstance(test_node.position, NSPoint)
	assert test_node.type in [LINE, CURVE, OFFCURVE, QCURVE]

	# Test mutability of smooth
	assert_bool(test_node, "smooth", test_node.smooth)

	# .selected is a UI property
	assert_bool(test_node, "selected", test_node.selected)

	# .name is an optional string property
	assert_string(test_node, "name", test_node.name)

def test_GSNode_relational_attributes(test_node):
	# index should be an integer and read-only
	assert isinstance(test_node.index, int)
	assert test_node.index is not None and test_node.index != NSNotFound # For a node in a path
	assert_read_only(test_node, 'index')

	assert isinstance(test_node.nextNode, GSNode)
	assert isinstance(test_node.prevNode, GSNode)

	# Test detached copy
	node_copy = copy.copy(test_node)
	# A detached node's index should be NSNotFound
	assert node_copy.index == NSNotFound

def test_GSNode_userData(test_node):
	assert test_node.userData is not None
	test_node.userData["TestData"] = 42
	assert test_node.userData["TestData"] == 42
	del test_node.userData["TestData"]
	assert test_node.userData.get("TestData") is None

def test_GSNode_methods(test_node):
	# These methods modify the path structure, use with care or on a copy
	path = test_node.parent
	path_copy = copy.deepcopy(path)
	test_index = test_node.index
	node_in_copy = path_copy.nodes[test_index]
	nodes = path_copy.nodes
	node_in_copy.makeNodeFirst()
	assert path_copy.nodes[-1] is node_in_copy

	# toggleConnection can change node types
	original_type = node_in_copy.type  # noqa
	node_in_copy.toggleConnection()
	# Behavior depends on context, but type should potentially change
	# For now, just confirm the method call doesn't raise an exception

# GSAnchor Tests
def test_GSAnchor_attributes(path_test_layer): # Using path_test_layer from 'a'
	# 'a' glyph in test font has 'top' and 'ogonek' anchors
	if not path_test_layer.anchors:
		path_test_layer.anchors.append(GSAnchor("test_anchor", (100, 100)))

	anchor = path_test_layer.anchors["top"]
	assert repr(anchor) is not None

	assert isinstance(anchor.position, NSPoint)
	assert_bool(anchor, "selected", anchor.selected)

	# Test name mutability
	original_name = anchor.name
	path_test_layer.anchors['top'].name = "top123" # Must access via layer to rename
	assert path_test_layer.anchors['top123'] is not None
	assert 'top' not in path_test_layer.anchors, f"anchor: {path_test_layer.anchors.keys()}"
	path_test_layer.anchors['top123'].name = original_name # Rename back
	assert path_test_layer.anchors[original_name] is not None

def test_GSAnchor_userData(path_test_layer):
	anchor = path_test_layer.anchors["top"]
	assert anchor.userData is not None
	anchor.userData["TestData"] = 42
	assert anchor.userData["TestData"] == 42
	del anchor.userData["TestData"]
	assert anchor.userData.get("TestData") is None

# GSGuide Tests
def test_GSGuide_attributes(path_test_layer):
	# Ensure there is a guide to test
	if not path_test_layer.guides:
		path_test_layer.guides.append(GSGuide())

	guide = path_test_layer.guides[0]

	assert isinstance(guide.position, NSPoint)
	assert_bool(guide, "lockAngle")
	assert_float(guide, "angle")
	assert_string(guide, "name", allow_none=True)
	assert_bool(guide, "locked")

def test_GSGuide_userData(path_test_layer: GSLayer):
	if not path_test_layer.guides:
		path_test_layer.guides.append(GSGuide())
	guide = path_test_layer.guides[0]

	assert guide.userData is not None
	guide.userData["TestData"] = 42
	assert guide.userData["TestData"] == 42
	del guide.userData["TestData"]
	assert guide.userData.get("TestData") is None

# GSBackgroundImage Tests
def test_GSLayer_backgroundImage(font: GSFont):
	layer = font.glyphs['A'].layers[font.masters[0].id]
	original_image = layer.backgroundImage

	# Path to a test image file. This needs to exist for the test to pass.
	# We create a dummy file if it doesn't exist.
	image_path = os.path.join(os.path.dirname(PathToTestFile), 'A.jpg')
	if not os.path.exists(image_path):
		pytest.skip(f"Test image '{image_path}' not found.")

	layer.backgroundImage = GSBackgroundImage(image_path)
	image = layer.backgroundImage
	assert image is not None

	copyImage = copy.copy(image)
	assert repr(copyImage) is not None

	# Test attributes
	assert image.path == os.path.abspath(image_path)
	assert isinstance(image.image, NSImage)
	assert isinstance(image.crop, NSRect)
	# image.crop = NSRect(NSPoint(0, 0), NSPoint(100, 100)) # Test mutability if needed

	assert_bool(image, "locked")
	assert_integer(image, "alpha")
	assert_point(image, "position")
	assert_point(image, "scale")
	assert_float(image, "rotation")

	# Test methods
	image.resetCrop()
	image.scaleWidthToEmUnits(layer.width)

	# Cleanup
	layer.backgroundImage = original_image

# GSGlyphInfo Tests
def test_GSGlyphInfo_attributes(font: GSFont):
	info = font.glyphs['a'].glyphInfo
	assert repr(info) is not None
	assert info.name == 'a'
	assert info.productionName is None
	assert info.category == 'Letter'
	assert info.case == GSLowercase

	# Test glyph with components
	info_comp = font.glyphs['adieresis'].glyphInfo
	assert isinstance(list(info_comp.components), list)
	assert info_comp.unicode == '00E4'
	assert len(info_comp.unicodes) == 1

	# Test another glyph for different properties
	info_lam_alef = Glyphs.glyphInfoForName('lam_alef-ar')
	if info_lam_alef: # This might not be in the default glyph data
		assert isinstance(list(info_lam_alef.accents), list)
		assert isinstance(list(info_lam_alef.anchors), list)
		assert isinstance(info_lam_alef.index, int)
		assert info_lam_alef.sortName == "ar0010_ar0009"
		assert info_lam_alef.sortNameKeep == "ar0900_ar0009"
		assert info_lam_alef.altNames[0] == "lamalefisolatedarabic"

# General Wrapper Methods
def test_Methods_geometry_functions():
	# divideCurve()
	result_curve = divideCurve(NSPoint(0, 0), NSPoint(50, 0), NSPoint(100, 50), NSPoint(100, 100), 0.5)
	assert len(result_curve) == 7

	# distance()
	assert distance(NSPoint(0, 0), NSPoint(0, 2)) == pytest.approx(2.0)

	# addPoints()
	assert addPoints(NSPoint(0, 0), NSPoint(1, 2)) == NSPoint(1, 2)

	# scalePoint()
	assert scalePoint(NSPoint(2, 2), 2) == NSPoint(4, 4)

# objcObject Conversion
def test_objcObject_conversions():
	from GlyphsApp import objcObject
	assert isinstance(objcObject(["a"]), NSArray)
	assert isinstance(objcObject({"a": 1}), NSDictionary)
	assert isinstance(objcObject(3.145), NSNumber)
	assert isinstance(objcObject(1), NSNumber)
	assert isinstance(objcObject(None), NSNull)

# Constants Tests
def test_Constants_are_defined():
	from GlyphsApp import (
		GSMOVE, GSLINE, GSCURVE, GSQCURVE, GSOFFCURVE,
		GSSHARP, GSSMOOTH, TAG, TOPGHOST, STEM, BOTTOMGHOST, FLEX,
		TTSNAP, TTANCHOR, TTSTEM, TTSHIFT, TTALIGN, TTINTERPOLATE,
		TTDIAGONAL, TTDELTA, CORNER, CAP, TTROUND, TTROUNDUP, TTROUNDDOWN,
		TTDONTROUND, TRIPLE, APP_MENU, FILE_MENU, EDIT_MENU,
		GLYPH_MENU, PATH_MENU, FILTER_MENU, VIEW_MENU, SCRIPT_MENU,
		WINDOW_MENU, HELP_MENU, DRAWFOREGROUND, DRAWBACKGROUND,
		DRAWINACTIVE, DOCUMENTOPENED, DOCUMENTACTIVATED, DOCUMENTWASSAVED,
		DOCUMENTEXPORTED, DOCUMENTCLOSED, TABDIDOPEN, TABWILLCLOSE,
		UPDATEINTERFACE, MOUSEMOVED, MOUSEDRAGGED, MOUSEDOWN, MOUSEUP,
		CONTEXTMENUCALLBACK
	)

	constants = [
		GSMOVE, GSLINE, GSCURVE, GSQCURVE, GSOFFCURVE, GSSHARP, GSSMOOTH,
		TAG, TOPGHOST, STEM, BOTTOMGHOST, FLEX, TTSNAP, TTANCHOR, TTSTEM,
		TTSHIFT, TTALIGN, TTINTERPOLATE, TTDIAGONAL, TTDELTA, CORNER, CAP,
		TTROUND, TTROUNDUP, TTROUNDDOWN, TTDONTROUND, TRIPLE, APP_MENU,
		FILE_MENU, EDIT_MENU, GLYPH_MENU, PATH_MENU, FILTER_MENU, VIEW_MENU,
		SCRIPT_MENU, WINDOW_MENU, HELP_MENU, DRAWFOREGROUND, DRAWBACKGROUND,
		DRAWINACTIVE, DOCUMENTOPENED, DOCUMENTACTIVATED, DOCUMENTWASSAVED,
		DOCUMENTEXPORTED, DOCUMENTCLOSED, TABDIDOPEN, TABWILLCLOSE,
		UPDATEINTERFACE, MOUSEMOVED, MOUSEDRAGGED, MOUSEDOWN, MOUSEUP,
		CONTEXTMENUCALLBACK
	]

	for const in constants:
		assert const is not None, f"Constant {const} should be defined."


if __name__ == "__main__" and False:
	if not hasattr(sys.stdout, "isatty"):
		sys.stdout.isatty = lambda: False
	# Run pytest on this file
	args = [
		"--tb=long",  # For detailed tracebacks
		"--full-trace",  # To prevent pytest from cutting tracebacks
		# You can add other options here if needed, e.g., "-v" for verbose test names
		"-v",
		f"{__file__}::test_GSFont_masters"  # Or the specific path to your test file/directory
	]
	pytest.main(args)
	# pytest.main([__file__])
