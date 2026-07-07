# MenuTitle: Glyphs.app UI Tests
# encoding: utf-8

"""
UI-dependent tests.

These tests need the font opened in the Glyphs UI (documents, tabs, tools,
selection, edit view). The plain object tests live in UnitTestKopie.py.
"""

import pytest

from GlyphsApp import Glyphs, GSFont, GSFeature, GSDocument, GSFontViewController
from GlyphsApp import GSLTR, GSRTL, GSVertical, GSVerticalToRight

from TestHelpers import assert_list
import os
import sys
import copy

from Foundation import NSPoint, NSRect  # type: ignore

PathToTestFile = os.path.join(os.path.dirname(__file__), "Glyphs Unit Test Sans.glyphs")

Glyphs.clearLog()


@pytest.fixture
def ui_font():
	"""The test font, opened in the UI. Closed again on teardown."""
	Glyphs.open(PathToTestFile)
	font = Glyphs.font
	assert font is not None
	yield font
	if Glyphs.font is not None:
		Glyphs.font.close()


# GSApplication Tests
def test_GSApplication():
	assert Glyphs is not None
	assert Glyphs.__repr__() is not None

	# close all fonts
	for app_font in Glyphs.fonts:
		app_font.close()
	assert len(Glyphs.fonts) == 0

	# AppFontProxy
	new_font = GSFont()
	Glyphs.fonts.append(new_font)
	assert new_font in Glyphs.fonts
	assert len(Glyphs.fonts) == 1
	assert new_font == Glyphs.font
	copy_font = copy.copy(new_font)
	assert copy_font not in Glyphs.fonts
	new_font.close()
	assert new_font not in Glyphs.fonts
	assert len(Glyphs.fonts) == 0
	Glyphs.fonts.extend([copy_font])
	assert copy_font in Glyphs.fonts
	copy_font.close()
	with pytest.raises(TypeError):
		_ = Glyphs.fonts['a']  # type: ignore

	# open font
	Glyphs.open(PathToTestFile)

	# showMacroWindow()
	Glyphs.showMacroWindow()

	assert Glyphs.font is not None
	assert len(Glyphs.fonts) == 1

	# documents
	assert len(Glyphs.documents) == 1
	assert Glyphs.documents[0].font is Glyphs.fonts[0]
	with pytest.raises(TypeError):
		_ = Glyphs.documents['a']  # type: ignore
	assert isinstance(copy.copy(Glyphs.documents), list)

	# currentDocument / GSDocument.filePath
	assert isinstance(Glyphs.currentDocument, GSDocument)
	assert Glyphs.currentDocument.filePath is not None

	# reporters / activeReporters
	assert len(list(Glyphs.reporters)) > 0
	assert len(Glyphs.reporters) > 0
	for reporter in Glyphs.reporters:
		Glyphs.activateReporter(reporter)
	assert len(Glyphs.activeReporters) == len(Glyphs.reporters)
	for reporter in Glyphs.reporters:
		Glyphs.deactivateReporter(reporter)
	assert len(Glyphs.activeReporters) == 0

	# filters
	assert isinstance(Glyphs.filters, list)

	# defaults
	Glyphs.defaults["uniTestValue"] = "abc"
	assert Glyphs.defaults["uniTestValue"] == "abc"
	del Glyphs.defaults["uniTestValue"]
	del Glyphs.defaults["TestKey"]
	Glyphs.registerDefaults({"TestKey": 12})
	assert Glyphs.defaults["TestKey"] == 12
	Glyphs.registerDefault("TestKey", 36)
	assert Glyphs.defaults["TestKey"] == 36
	Glyphs.registerDefaults({"TestKey": 12})
	Glyphs.defaults["TestKey"] = 24
	assert Glyphs.defaults["TestKey"] == 24
	del Glyphs.defaults["TestKey"]
	assert Glyphs.defaults["TestKey"] == 12

	# boolDefaults
	assert Glyphs.defaults["BoolKey"] is None
	assert Glyphs.boolDefaults["BoolKey"] is False
	Glyphs.boolDefaults["BoolKey"] = True
	assert Glyphs.boolDefaults["BoolKey"] is True
	del Glyphs.boolDefaults["BoolKey"]
	with pytest.raises(TypeError):
		Glyphs.boolDefaults["BoolKey"] = 12

	# colorDefaults
	assert Glyphs.colorDefaults["colorKey"] is None
	Glyphs.colorDefaults["colorKey"] = "#ff0000"
	assert Glyphs.colorDefaults["colorKey"] is not None
	del Glyphs.colorDefaults["colorKey"]
	assert Glyphs.colorDefaults["colorKey"] is None
	with pytest.raises(ValueError):
		Glyphs.colorDefaults["colorKey"] = "not a color"
	with pytest.raises(TypeError):
		Glyphs.colorDefaults["colorKey"] = 12

	# intDefaults
	assert Glyphs.defaults["IntKey"] is None
	assert Glyphs.intDefaults["IntKey"] == 0
	Glyphs.intDefaults["IntKey"] = 14
	assert Glyphs.intDefaults["IntKey"] == 14
	del Glyphs.intDefaults["IntKey"]
	with pytest.raises(TypeError):
		Glyphs.intDefaults["IntKey"] = 12.5

	# floatDefaults
	assert Glyphs.defaults["FloatKey"] is None
	Glyphs.floatDefaults["FloatKey"] = 12.5
	assert Glyphs.floatDefaults["FloatKey"] == 12.5
	del Glyphs.floatDefaults["FloatKey"]

	# script and language data
	assert dict(Glyphs.scriptAbbreviations) is not None
	assert dict(Glyphs.scriptSuffixes) is not None
	assert dict(Glyphs.languageScripts) is not None
	assert list(map(dict, Glyphs.languageData)) is not None
	assert list(Glyphs.unicodeRanges) is not None

	# editViewWidth / handleSize
	assert isinstance(Glyphs.editViewWidth, int)
	assert isinstance(Glyphs.handleSize, int)

	# version info
	assert isinstance(Glyphs.versionString, str)
	assert isinstance(Glyphs.versionNumber, float)
	assert isinstance(Glyphs.buildNumber, float)

	# menu
	with pytest.raises(TypeError):
		_ = Glyphs.menu[1.5]  # type: ignore
	assert_list(copy.copy(Glyphs.menu))

	## Methods

	Glyphs.showGlyphInfoPanelWithSearchString('a')
	assert str(Glyphs.glyphInfoForName('a')) == "<GSGlyphInfo 'a'>"
	assert str(Glyphs.glyphInfoForUnicode('0061')) == "<GSGlyphInfo 'a'>"
	assert Glyphs.niceGlyphName('a') == 'a'
	assert Glyphs.productionGlyphName('a') == 'a'
	assert len(list(Glyphs.ligatureComponents('allah-ar'))) == 4
	Glyphs.redraw()
	Glyphs.showNotification('Glyphs Unit Test', 'Hello World')
	assert Glyphs.localize({
		'en': 'Hello World',
		'de': 'Hallöle Welt',
		'fr': 'Bonjour tout le monde',
		'es': 'Hola Mundo',
	}) is not None

	# addCallback / removeCallback
	def test_callback_method(**kwargs):
		pass

	callbacks = (
		"DrawForeground", "DrawBackground", "DrawInactive", "GSDocumentWasOpenedNotification", "GSDocumentActivateNotification",
		"GSDocumentWasSavedSuccessfully", "GSDocumentWasExportedNotification", "GSDocumentCloseNotification",
		"TabDidOpenNotification", "TabWillCloseNotification", "GSUpdateInterface", "mouseMovedNotification",
		"mouseDraggedNotification", "mouseDownNotification", "mouseUpNotification", "GSContextMenuCallbackName"
	)
	for callback in callbacks:
		Glyphs.addCallback(test_callback_method, callback)
		Glyphs.removeCallback(test_callback_method)

	Glyphs.font.close()


# GSFont Tests (UI-dependent properties)
def test_GSFont_parent(ui_font: GSFont):
	# GSFont.parent is the GSDocument when the font is opened in the UI
	assert 'GSDocument' in str(ui_font.parent)


def test_GSFont_UI(ui_font: GSFont):
	# show()
	ui_font.show()

	# fontView / GSFontViewController
	assert isinstance(ui_font.fontView, GSFontViewController)
	assert ui_font.fontView.parent is not None
	assert list(ui_font.fontView.selectedLayers) is not None

	# selection
	for glyph in ui_font.glyphs:
		glyph.selected = False
	ui_font.glyphs['a'].selected = True
	assert len(list(ui_font.selection)) == 1
	for glyph in ui_font.glyphs:
		glyph.selected = True
	assert set(ui_font.selection) == set(ui_font.glyphs)
	ui_font.selection = [ui_font.glyphs['a']]
	assert list(ui_font.selection) == [ui_font.glyphs['a']]
	with pytest.raises(TypeError):
		ui_font.selection = 0  # type: ignore

	# tabs / currentTab / currentText / selectedLayers / newTab()
	for tab in ui_font.tabs:
		tab.close()
	tab = ui_font.newTab('a')
	assert tab == ui_font.tabs[-1]
	assert ui_font.currentTab.__repr__() is not None
	assert len(list(ui_font.selectedLayers)) == 1
	assert len(list(ui_font.tabs)) == 1
	assert ui_font.currentText == 'a'
	ui_font.currentText = 'A'
	assert ui_font.currentText == 'A'
	assert ui_font.currentTab == ui_font.tabs[-1]
	tab2 = ui_font.newTab('n')
	assert ui_font.currentTab == tab2
	ui_font.currentTab = tab
	assert ui_font.currentTab == tab
	ui_font.tabs[0].close()
	assert ui_font.currentTab == tab2
	ui_font.tabs[0].close()
	# values are None when no tabs are open
	assert ui_font.currentText is None
	assert ui_font.currentTab is None
	with pytest.raises(TypeError):
		_ = ui_font.tabs['']  # type: ignore

	# selectedFontMaster / masterIndex
	old_master_index = ui_font.masterIndex
	for i in range(len(list(ui_font.masters))):
		ui_font.masterIndex = i
		assert ui_font.selectedFontMaster == ui_font.masters[i]
	ui_font.masterIndex = old_master_index

	# tool / tools / toolIndex
	old_tool = ui_font.tool
	for tool_name in ui_font.tools:
		ui_font.tool = tool_name
		assert ui_font.tool == tool_name
		assert isinstance(ui_font.toolIndex, int)
		assert ui_font.tools[ui_font.toolIndex] == tool_name
	ui_font.tool = old_tool


# GSEditViewController Tests
def test_GSEditViewController(ui_font: GSFont):
	tab = ui_font.newTab('a')
	assert tab.__repr__() is not None

	# parent
	assert tab.parent == ui_font

	# text
	assert tab.text == 'a'

	# layers
	assert list(tab.layers) == [ui_font.glyphs['a'].layers[0]]
	tab.layers = [ui_font.glyphs['a'].layers[0]]
	tab.layers.append(ui_font.glyphs['A'].layers[0])
	tab.layers.remove(ui_font.glyphs['A'].layers[0])
	assert list(tab.layers) == [ui_font.glyphs['a'].layers[0]]

	# composedLayers
	ui_font.updateFeatures()
	assert list(tab.composedLayers) == [ui_font.glyphs['a'].layers[0]]
	tab.features = ['smcp']
	assert list(tab.composedLayers) == [ui_font.glyphs['a.sc'].layers[0]]
	tab.features = []

	# scale / viewPort / bounds / origins
	assert isinstance(tab.scale, float)
	assert isinstance(tab.viewPort, NSRect)
	assert isinstance(tab.safeViewPort, NSRect)
	assert isinstance(tab.bounds, NSRect)
	assert isinstance(tab.selectedLayerOrigin, NSPoint)

	# text cursor and ranges
	assert isinstance(tab.textCursor, int)
	assert isinstance(tab.textRange, int)
	assert tab.selectedTextRange is not None
	assert isinstance(tab.layersCursor, int)
	assert isinstance(tab.layersRange, int)
	assert tab.selectedLayerRange is not None

	# masterIndex
	assert isinstance(tab.masterIndex, int)

	# selectedLayers
	assert list(tab.selectedLayers) is not None

	# direction
	assert tab.direction in [GSLTR, GSRTL, GSVertical, GSVerticalToRight]
	tab.direction = GSRTL
	assert tab.direction in [GSLTR, GSRTL, GSVertical, GSVerticalToRight]
	tab.direction = GSLTR
	assert tab.direction in [GSLTR, GSRTL, GSVertical, GSVerticalToRight]

	# features
	new_feature = GSFeature('liga', 'sub a by A;')
	ui_font.features.append(new_feature)
	tab.features = ['liga']
	assert list(tab.features) == ['liga']
	tab.features = []
	del ui_font.features['liga']

	# previewInstances
	tab.previewInstances = 'all'
	assert tab.previewInstances == 'all'
	tab.previewInstances = 'live'
	assert tab.previewInstances == 'live'
	for instance in ui_font.instances:
		tab.previewInstances = instance
		assert tab.previewInstances == instance

	# previewHeight
	tab.previewHeight = 100
	tab.previewHeight = 0

	# bottomToolbarHeight
	assert tab.bottomToolbarHeight > 0

	# tempData
	tab.tempData['a'] = 'b'
	assert tab.tempData['a'] == 'b'

	## Methods

	# saveToPDF()
	tab.saveToPDF(os.path.join(os.path.dirname(PathToTestFile), 'Unit Test.pdf'))

	# close()
	tab.close()


'''
Dialog functions from the old test_Methods are not testable without user
interaction, so they are left out here:

	GetSaveFile(filetypes=['glyphs'])
	GetOpenFile()
	GetFolder()
	Message('Title', 'Message')
	LogToConsole('Message')
	LogError('Error message created in test code. Ignore it.')
'''


if __name__ == "__main__":
	if not hasattr(sys.stdout, "isatty"):
		sys.stdout.isatty = lambda: False  # type: ignore
	pytest.main(["-v", __file__])
