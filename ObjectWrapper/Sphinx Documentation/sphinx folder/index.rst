.. Glyphs documentation master file, created by
   sphinx-quickstart on Sat Apr 17 17:11:16 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. highlight:: python
	:linenothreshold: 5

.. _module:: Glyphs
   :synopsis: The Glyphs.app Python Scripting API Documentation.

.. moduleauthor:: Georg Seifert <info@schriftgestaltung.de>

.. toctree::
   :maxdepth: 2


Glyphs.app Python Scripting API Documentation
=============================================

This is the documentation for the Python Scripting API for Glyphs.app (`glyphsapp.com <http://glyphsapp.com/>`_)

Calling font objects starts with the mothership, the Glyphs object::

	print Glyphs

.. code-block:: python

	<Glyphs.app>
	
The currently open fonts are attached to it::

	# topmost open font
	font = Glyphs.font
	print font

.. code-block:: python
	
	<GSFont "My Font" v1.0 with 2 masters and 5 instances>

.. code-block:: python
	
	# all open fonts
	fonts = Glyphs.fonts
	print fonts

.. code-block:: python
	
	[<GSFont "My Font" v1.0 with 2 masters and 5 instances>,
	<GSFont "My Other Font" v1.0 with 1 masters and 1 instances>]

.. image:: _static/objectmodel.png


More Details
============

This document covers all methods that are implemented in the wrapper. There is a lot more available. Please have a look at the Core part of the documentation.



:mod:`GSApplication`
===============================================================================

The mothership. Everything starts here.


.. code-block:: python


	print Glyphs


.. code-block:: python


	<Glyphs.app>

	
.. class:: GSApplication()

Properties

.. autosummary::

	font
	fonts
	defaults
	boolDefaults
	intDefaults
	scriptAbbrevations
	scriptSuffixes
	languageScripts
	languageData
	unicodeRanges

	
Functions

.. autosummary::

	open()
	showMacroWindow()
	clearLog()
	showGlyphInfoPanelWithSearchString()
	glyphInfoForName()
	glyphInfoForUnicode()
	niceGlyphName()
	productionGlyphName()
	ligatureComponents()
	redraw()
	
	
----------
Properties
----------


.. attribute:: font

	
	:return: The active :class:`GSFont` object or None.
	:rtype: :class:`GSFont`
	

	.. code-block:: python


		# topmost open font
		font = Glyphs.font



.. attribute:: fonts

	
	:return: All open :class:`Fonts <GSFont>`.
	:rtype: list of :class:`GSFont` objects
	

	.. code-block:: python


		# access all open fonts
		for font in Glyphs.fonts:
			print font.familyName
			
		# add a font
		
		font = GSFont()
		font.familyName = "My New Fonts"
		Glyphs.fonts.append(font)
		


.. attribute:: defaults

	
	A dict like object. You can get and set key value pairs.
	
	Please be careful with your keys. Use a prefix that uses the reverse domain name. e.g. "com.MyName.foo.bar".
	
	use it like this:
	

	.. code-block:: python

	
		Value = Glyphs.defaults["com.MyName.foo.bar"]
		Glyphs.defaults["com.MyName.foo.bar"] = NewValue
	
	

.. attribute:: boolDefaults

	
	A dict like object. Same as Glyphs.defaults only that value is a bool.
	
	Please be careful with your keys. Use a prefix that uses the reverse domain name. e.g. "com.MyName.foo.bar".
	

.. attribute:: intDefaults

	
	A dict like object. Same as Glyphs.defaults only that value is a int.
	
	Please be careful with your keys. Use a prefix that uses the reverse domain name. e.g. "com.MyName.foo.bar".
	
	

.. attribute:: scriptAbbrevations

	
	A dictionary with script name to abbreviation mapping, e.g. 'arabic': 'arab'
	
	:rtype: dict`
	

.. attribute:: scriptSuffixes

	
	A dictionary with glyphs name suffixes for scripts and their respective script names, e.g. 'cy': 'cyrillic'
	
	:rtype: dict`
	

.. attribute:: languageScripts

	
	A dictionary with language tag to script tag mapping, e.g. 'ENG': 'latn'
	
	:rtype: dict`
	

.. attribute:: languageData

	
	A list of dictionaries with more detailed language informations.
	
	:rtype: list`
	

.. attribute:: unicodeRanges

	
	Names of unicode ranges.
	
	:rtype: list`
	

---------
Functions
---------

.. function:: open(Path)
	
	Opens a document
	
	:param Path: The path where the document is located.

	:type Path: str
	:return: The opened document object or None.
	:rtype: :class:`GSFont`
.. function:: showMacroWindow
	
	Opens the macro window


.. function:: clearLog
	
	Deletes the content of the console in the macro window
	

.. function:: showGlyphInfoPanelWithSearchString(String)
	
	Shows the Glyph Info window with a preset search string
	
	:param String: The search term
	
	
.. function:: glyphInfoForName(String)
	
	Generates :class:`GSGlyphInfo` object for given glyph name.
	
	:param String: Glyph name
	:return: :class:`GSGlyphInfo`
	
	
.. function:: glyphInfoForUnicode(Unicode)
	
	Generates :class:`GSGlyphInfo` object for given hex unicode.
	
	:param String: Hex unicode
	:return: :class:`GSGlyphInfo`
	
	
.. function:: niceGlyphName(Name)
	
	Converts glyph name to nice, human readable glyph name (e.g. afii10017 or uni0410 to A-cy)
	
	:param string: glyph name
	:return: string
	
	
.. function:: productionGlyphName(Name)
	
	Converts glyph name to production glyph name (e.g. afii10017 or A-cy to uni0410)
	
	:param string: glyph name
	:return: string
	
	
.. function:: ligatureComponents(String)
	
	If defined as a ligature in the glyph database, this function returns a list of glyph names that this ligature could be composed of.
	
	:param string: glyph name
	:return: list
	

	.. code-block:: python

	
		print Glyphs.ligatureComponents('allah-ar')

		(
		    "alef-ar",
		    "lam-ar.init",
		    "lam-ar.medi",
		    "heh-ar.fina"
		)
	
.. function:: redraw()
	
	Redraws all Edit views and Preview views.
	
	

:mod:`GSFont`
===============================================================================

Implementation of the font object. This object is host to the :class:`Masters <GSFontMaster>` used for interpolation. Even when no interpolation is involved, for the sake of object model consistency there will still be one master and one instance representing a single font.

Also, the :class:`Glyphs <GSGlyph>` are attached to the Font object right here, not one level down to the masters. The different master's glyphs are available as :class:`Layers <GSLayer>` attached to the :class:`Glyph <GSGlyph>` objects which are attached here.

.. class:: GSFont()

Properties

.. autosummary::

	masters
	instances
	glyphs
	classes
	features
	featurePrefixes
	copyright
	designer
	designerURL
	manufacturer
	manufacturerURL
	versionMajor
	versionMinor
	date
	familyName
	upm
	note
	kerning
	userData
	gridLength
	disablesNiceNames
	customParameters
	selectedLayers
	selectedFontMaster
	masterIndex
	currentText
	tabs
	currentTab
	filepath

Functions

.. autosummary::
	
	disableUpdateInterface()
	enableUpdateInterface()
	kerningForPair()
	setKerningForPair()
	removeKerningForPair()
	newTab()

----------
Properties
----------



.. attribute:: masters

	Collection of :class:`GSFontMaster <GSFontMaster>`.

	:type: list
	

.. attribute:: instances

	Collection of :class:`GSInstance <GSInstance>`.

	:type: list


.. attribute:: glyphs

	Collection of :class:`GSGlyph <GSGlyph>`. Returns a list, but you may also call glyphs using index or glyph name as key.

	.. code-block:: python

		# Access all glyphs
		for glyph in font.glyphs:
			print glyph
		<GSGlyph "A" with 4 layers>
		<GSGlyph "B" with 4 layers>
		<GSGlyph "C" with 4 layers>
		...

		# Access one glyph
		print font.glyphs['A']
		<GSGlyph "A" with 4 layers>
		
		# Add a glyph
		font.glyphs.append(GSGlyph('adieresis'))
		
		# Duplicate a glyph under a different name
		newGlyph = font.glyphs['A'].copy()
		newGlyph.name = 'A.alt'
		font.glyphs.append(newGlyph)

		# Delete a glyph
		del(font.glyphs['A.alt'])


	:type: list, dict

.. attribute:: classes

	Collection of :class:`GSClass <GSClass>` objects, representing OpenType glyph classes.

	:type: list
	

	.. code-block:: python

	
		# add a class
		font.classes.append(GSClass('uppercaseLetters', 'A B C D E'))
	
		# access all classes
		for class in font.classes:
			print class.name
	
		# access one class
		print font.classes['uppercaseLetters'].code
	
		# delete a class
		del(font.classes['uppercaseLetters'])


.. attribute:: features

	Collection of :class:`GSFeature <GSFeature>` objects, representing OpenType features.

	:type: list


	.. code-block:: python

	
		# add a feature
		font.features.append(GSFeature('liga', 'sub f i by fi;'))
	
		# access all features
		for feature in font.features:
			print feature.code
	
		# access one feature
		print font.features['liga'].code
	
		# delete a feature
		del(font.features['liga'])


.. attribute:: featurePrefixes

	Collection of :class:`GSFeaturePrefix <GSFeaturePrefix>` objects, containing stuff that needs to be outside of the OpenType features.

	:type: list


	.. code-block:: python

	
		# add a prefix
		font.featurePrefixes.append(GSFeaturePrefix('LanguageSystems', 'languagesystem DFLT dflt;'))
	
		# access all prefixes
		for prefix in font.featurePrefixes:
			print prefix.code
	
		# access one prefix
		print font.featurePrefixes['LanguageSystems'].code
	
		# delete
		del(font.featurePrefixes['LanguageSystems'])


.. attribute:: copyright


	:type: unicode

.. attribute:: designer


	:type: unicode

.. attribute:: designerURL


	:type: unicode

.. attribute:: manufacturer


	:type: unicode

.. attribute:: manufacturerURL


	:type: unicode

.. attribute:: versionMajor


	:type: int

.. attribute:: versionMinor


	:type: int

.. attribute:: date


	:type: NSDate

	.. code-block:: python

		print font.date
		2015-06-08 09:39:05 +0000
		
		# set date to now
		font.date = NSDate.date()


.. attribute:: familyName

	Family name of the typeface.

	:type: unicode

.. attribute:: upm

	Units per Em

	:type: int

.. attribute:: note


	:type: unicode

.. attribute:: kerning

	A multi-level dictionary. The first level's key is the :class:`GSFontMaster`.id (each master has its own kerning), the second level's key is the :class:`GSGlyph <GSGlyph>`.id or class id (@MMK_L_XX), the third level's key is again a glyph id or class id (@MMK_R_XX). The values are the actual kerning values.
	
	To set a value, is is better to use the method :class:`GSFont`.setKerningForPair(). This ensures a better data integrity (and is faster).

	:type: dict


.. attribute:: userData

	A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the dats will not be recoverable from the saved file.

	:type: dict

	.. code-block:: python

		# set value
		font.userData['rememberToMakeCoffee'] = True


.. attribute:: disablesNiceNames

	Corresponds to the "Don't use nice names" setting from the Info dialogue.

	:type: bool

.. attribute:: customParameters

	The custom parameters. List of :class:`GSCustomParameter` objects. You can access them by name or by index.

	.. code-block:: python

		
		# access all parameters
		for parameter in font.customParameters:
			print parameter
		
		# set a parameter
		font.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'

		# delete a parameter
		del(font.customParameters['trademark'])
	

	:type: list, dict

.. attribute:: gridLength

	Corresponds to the "Grid spacing" setting from the Info dialogue. When set to 0, point positions may contain float values.

	:type: int

.. attribute:: selectedLayers

	Returns a list of all selected layers in the active tab.

	:type: list

.. attribute:: selectedFontMaster

	Returns the active master (selected in the toolbar).

	:type: :class:`GSFontMaster <GSFontMaster>`

.. attribute:: masterIndex

	Returns the index of the active master (selected in the toolbar).

	:type: int

.. attribute:: currentText

	The text of the current edit view. 
	
	Unencoded and none ASCII glyphs will use a slash and the glyph name. (e.g: /a.sc). Setting unicode strings works.
	

	:type: unicode

.. attribute:: tabs

	List of open edit view tabs in UI, as list of :class:`GSEditViewController` objects.
	

	.. code-block:: python

		
		# open new tab with text
		font.newTab('hello')
		
		# access all tabs
		for tab in font.tabs:
			print tab
			
		# close last tab
		del(font.tabs[-1])
	

	:type: list

.. attribute:: currentTab

	Active edit view tab.
	

	:type: :class:`GSEditViewController`

.. attribute:: filepath

	On-disk location of GSFont object.

	:type: unicode

---------
Functions
---------

.. function:: disableUpdateInterface()
	
	Call this before you do big changes to the font, or to its glyphs. Make sure that you call Font.enableUpdateInterface() when you are done.
	
	
.. function:: enableUpdateInterface()
	
	This re-enables the interface update. Only makes sense to call if you have disabled it earlier.
	
	
.. function:: kerningForPair(FontMasterId, LeftKey, RightKey)
	
	This returns the kerning value for the two specified glyphs (LeftKey or RightKey is the glyphname) or a kerning group key (@MMK_X_XX).
	
	:param FontMasterId: The id of the FontMaster

	:type FontMasterId: str
	:param LeftKey: either a glyph name or a class name

	:type LeftKey: str
	:param RightKey: either a glyph name or a class name

	:type RightKey: str
	:return: The kerning value
	:rtype: float


	.. code-block:: python

		
		# print kerning between w and e for currently selected master
		font.kerningForPair(font.selectedFontMaster.id, 'w', 'e')
		-15.0

		# print kerning between group T and group A for currently selected master
		# ('L' = left side of the pair and 'R' = left side of the pair)
		font.kerningForPair(font.selectedFontMaster.id, '@MMK_L_T', '@MMK_R_A')
		-75.0

		# in the same font, kerning between T and A would be zero, because they use group kerning instead.
		font.kerningForPair(font.selectedFontMaster.id, 'T', 'A')
		9.22337203685e+18 # (this is the float value for 0, an integer transformation would actually return 0)

.. function:: setKerningForPair(FontMasterId, LeftKey, RightKey, Value)
	
	This sets the kerning for the two specified glyphs (LeftKey or RightKey is the glyphname) or a kerning group key (@MMK_X_XX).
	
	:param FontMasterId: The id of the FontMaster

	:type FontMasterId: str
	:param LeftKey: either a glyph name or a class name

	:type LeftKey: str
	:param RightKey: either a glyph name or a class name

	:type RightKey: str
	:param Value: kerning value

	:type Value: float


	.. code-block:: python

		# set kerning for group T and group A for currently selected master
		# ('L' = left side of the pair and 'R' = left side of the pair)
		font.setKerningForPair(font.selectedFontMaster.id, '@MMK_L_T', '@MMK_R_A', -75)

.. function:: removeKerningForPair(FontMasterId, LeftKey, RightKey)
	
	Removes the kerning for the two specified glyphs (LeftKey or RightKey is the glyphname) or a kerning group key (@MMK_X_XX).
	
	:param FontMasterId: The id of the FontMaster

	:type FontMasterId: str
	:param LeftKey: either a glyph name or a class name

	:type LeftKey: str
	:param RightKey: either a glyph name or a class name

	:type RightKey: str


	.. code-block:: python

		# remove kerning for group T and group A for all masters
		# ('L' = left side of the pair and 'R' = left side of the pair)
		for master in font.masters:
			font.removeKerningForPair(master.id, '@MMK_L_T', '@MMK_R_A')

.. function:: newTab([tabText])
	
	Opens a new tab in the current document window, optionally with text
	
	:param tabText: Text or glyph names with '/'



:mod:`GSFontMaster`
===============================================================================

Implementation of the master object. This corresponds with the "Masters" pane in the Font Info.

In Glyphs.app the glyphs of each master are reachable not here, but as :class:`Layers <GSLayer>` attached to the :class:`Glyphs <GSGlyph>` attached to the :class:`Font <GSFont>` object. See info graphic on top for better understanding.

.. class:: GSFontMaster()




Properties

.. autosummary::

	id
	name
	weight
	width
	weightValue
	widthValue
	customValue
	customName
	ascender
	capHeight
	xHeight
	descender
	italicAngle
	verticalStems
	horizontalStems
	alignmentZones
	blueValues
	otherBlues
	guides
	userData
	customParameters

----------
Properties
----------



.. attribute:: id

	Used to identify :class:`Layers <GSLayer>` in the Glyph

	see :attr:`GSGlyph.layers <layers>`


	.. code-block:: python

		# ID of first master
		print font.masters[0].id
		3B85FBE0-2D2B-4203-8F3D-7112D42D745E
		
		# use this master to access the glyph's corresponding layer
		print glyph.layers[font.masters[0].id]
		<GSLayer "Light" (A)>
	

	:type: unicode

.. attribute:: name

	Name of the master. This is a combination of GSFontMaster.weight and GSFontMaster.width and is a human readable identification of each master, e.g. "Bold Condensed".

	:type: string

.. attribute:: weight

	Human readable weight name, chosen from list in Font Info. For actual position in interpolation design space, use GSFontMaster.weightValue.

	:type: string

.. attribute:: width

	Human readable width name, chosen from list in Font Info. For actual position in interpolation design space, use GSFontMaster.widthValue.

	:type: string

.. attribute:: weightValue

	Value for interpolation in design space.

	:type: float

.. attribute:: widthValue

	Value for interpolation in design space.

	:type: float

.. attribute:: customName

	The name of the custom interpolation dimension.

	:type: string

.. attribute:: customValue

	Value for interpolation in design space.

.. attribute:: ascender


	:type: float

.. attribute:: capHeight


	:type: float

.. attribute:: xHeight


	:type: float

.. attribute:: descender


	:type: float

.. attribute:: italicAngle


	:type: float

.. attribute:: verticalStems

	The vertical stems. This is a list of numbers. 

	:type: list

.. attribute:: horizontalStems

	The horizontal stems. This is a list of numbers. 

	:type: list

.. attribute:: alignmentZones

	Collection of :class:`GSAlignmentZone <GSAlignmentZone>`.

	:type: list

.. attribute:: blueValues

	PS hinting Blue Values calculated from the master's alignment zones. Read only.

	:type: list

.. attribute:: otherBlues

	PS hinting Other Blues calculated from the master's alignment zones. Read only.

	:type: list

.. attribute:: guides

	Collection of :class:`GSGuideLine <GSGuideLine>`. These are the font-wide (actually master-wide) red guidelines. For glyph-level guidelines (attached to the layers) see :attr:`GSLayer`.guides

	:type: list

.. attribute:: userData

	A dictionary to store user data. Use a unique key and only use objects that can be stored in a property list (string, list, dict, numbers, NSData) otherwise the date will not be recoverable from the saved file.

	:type: dict

	.. code-block:: python

		# set value
		font.masters[0].userData['rememberToMakeTea'] = True


.. attribute:: customParameters

	The custom parameters. List of :class:`GSCustomParameter` objects. You can access them by name or by index.
	

	.. code-block:: python

		
		# access all parameters
		for parameter in font.masters[0].customParameters:
			print parameter
		
		# set a parameter
		font.masters[0].customParameters['underlinePosition'] = -135

		# delete a parameter
		del(font.masters[0].customParameters['underlinePosition'])
	

	:type: list, dict

	
:mod:`GSAlignmentZone`
===============================================================================

Implementation of the alignmentZone object.

There is no distinction between Blue zones and other Zones. All negative zone (except the one with position 0) will be exported as Other zones.

The zone for the baseline should have position 0 (zero) and a negative width.

.. class:: GSAlignmentZone([pos, size])

	:param pos: The position of the zone
	:param size: The size of the zone


Properties

.. autosummary::

	position
	size
	
	
----------
Properties
----------
	


.. attribute:: position

	

	:type: int
	
	

.. attribute:: size

	

	:type: int



:mod:`GSInstance`
===============================================================================

Implementation of the instance object. This corresponds with the "Instances" pane in the Font Info.

.. class:: GSInstance()



Properties

.. autosummary::


	active
	name
	weight
	width
	weightValue
	widthValue
	customValue
	isItalic
	isBold
	linkStyle
	customParameters
	instanceInterpolations
	manualInterpolation
	
Functions
	
.. autosummary::
	
	generate()

----------
Properties
----------



.. attribute:: active


	:type: bool

.. attribute:: name

	Name of instance. Corresponds to the "Style Name" field in the font info. This is used for naming the exported fonts.

	:type: string

.. attribute:: weight

	Human readable weight name, chosen from list in Font Info. For actual position in interpolation design space, use GSInstance.weightValue.

	:type: string

.. attribute:: width

	Human readable width name, chosen from list in Font Info. For actual position in interpolation design space, use GSInstance.widthValue.

	:type: string

.. attribute:: weightValue

	Value for interpolation in design space.

	:type: float

.. attribute:: widthValue

	Value for interpolation in design space.

	:type: float

.. attribute:: customValue

	Value for interpolation in design space.

	:type: float

.. attribute:: isItalic

	Italic flag for style linking

	:type: bool

.. attribute:: isBold

	Bold flag for style linking

	:type: bool

.. attribute:: linkStyle

	Linked style

	:type: string

.. attribute:: customParameters

	The custom parameters. List of :class:`GSCustomParameter` objects. You can access them by name or by index.
	

	.. code-block:: python

		
		# access all parameters
		for parameter in font.instances[0].customParameters:
			print parameter
		
		# set a parameter
		font.instances[0].customParameters['hheaLineGap'] = 10

		# delete a parameter
		del(font.instances[0].customParameters['hheaLineGap'])
	

	:type: list, dict

.. attribute:: instanceInterpolations

	A dict that contains the interpolation coefficents for each master.
	This is automatcially updated if you change interpolationWeight, interpolationWidth, interpolationCustom. It contains FontMaster IDs as keys and coeffients for that master as values.
	Or, you can set it manually if you set manualInterpolation to True. There is no UI for this, so you need to do that with a script.

	:type: dict
	

.. attribute:: manualInterpolation

	Disables automatic calculation of instanceInterpolations
	This allowes manual setting of instanceInterpolations.

	:type: bool
	

---------
Functions
---------


.. function:: generate([Format, FontPath, AutoHint, RemoveOverlap, UseSubroutines, UseProductionNames])
	
	Exports the instance.
	
	:param str Format: 'OTF' or 'TTF'. Default: 'OTF'
	:param str FontPath: The destination path for the final fonts. If None, it uses the default location set in the export dialog
	:param bool AutoHint: If autohinting should be applied. Default: True
	:param bool RemoveOverlap: If overlaps should be removed. Default: True
	:param bool UseSubroutines: If to use subroutines for CFF. Default: True
	:param bool UseProductionNames: If to use production names. Default: True
	:return: On success, True, on failure error message.
	:rtype: bool/list


	
:mod:`GSCustomParameter`
===============================================================================

Implementation of the Custom Parameter object. It stores a name/value pair.

You can append GSCustomParameter objects for example to GSFont.customParameters, but this way you may end up with duplicates.
It is best to access the custom parameters through its dictionary interface like this:

.. code-block:: python

	
	# access all parameters
	for parameter in font.customParameters:
		print parameter
	
	# set a parameter
	font.customParameters['trademark'] = 'ThisFont is a trademark by MyFoundry.com'

	# delete a parameter
	del(font.customParameters['trademark'])

.. class:: GSCustomParameter([name, value])
	
	:param name: The name
	:param size: The value


Properties

.. autosummary::

	name
	value
	
	
----------
Properties
----------
	
	

.. attribute:: name

	

	:type: str
	

.. attribute:: value

	

	:type: str, list, dict, int, float
	
	

:mod:`GSClass`
===============================================================================

Implementation of the class object. It is used to store OpenType classes.

For details on how to access them, please look at :class:`GSFont`.classes

.. class:: GSClass([tag, code])

	:param tag: The class name
	:param code: A list of glyph names, separated by space or newline

Properties

.. autosummary::

	name
	code
	automatic

----------
Properties
----------



.. attribute:: name

	The class name

	:type: unicode

.. attribute:: code

	A string with space separated glyph names.

	:type: unicode


.. attribute:: automatic

	Define whether this class should be auto-generated when pressing the 'Update' button in the Font Info.

	:type: bool


:mod:`GSFeaturePrefix`
===============================================================================
	
Implementation of the featurePrefix object. It is used to store things that need to be outside of a feature like standalone lookups.

For details on how to access them, please look at :class:`GSFont`.featurePrefixes
	
.. class:: GSFeaturePrefix([tag, code])
	
	:param tag: The Prefix name
	:param code: The feature code in Adobe FDK syntax
	
Properties

.. autosummary::

	name
	code
	automatic

----------
Properties
----------
	
	

.. attribute:: name

	The FeaturePrefix name

	:type: unicode

.. attribute:: code

	A String containing feature code.

	:type: unicode
	

.. attribute:: automatic

	Define whether this should be auto-generated when pressing the 'Update' button in the Font Ínfo.

	:type: bool
	


:mod:`GSFeature`
===============================================================================

Implementation of the feature object. It is used to implement OpenType Features in the Font Info.

For details on how to access them, please look at :class:`GSFont`.features

.. class:: GSFeature([tag, code])
	
	:param tag: The feature name
	:param code: The feature code in Adobe FDK syntax
	
Properties

.. autosummary::

	name
	code
	automatic
	notes
	
Functions

.. autosummary::

	update()
	

----------
Properties
----------



.. attribute:: name

	The feature name

	:type: unicode

.. attribute:: code

	The Feature code in Adobe FDK syntax.

	:type: unicode

.. attribute:: automatic

	Define whether this feature should be auto-generated when pressing the 'Update' button in the Font Ínfo.

	:type: bool


.. attribute:: notes

	Some extra text. Is shown in the bottom of the feature window. Contains the stylistic set name parameter

	:type: unicode
	


---------
Functions
---------



.. function:: update()
	
	Calls the automatic feature code generator for this feature.
	You can use this to update all OpenType features before export.
	
	:return: None


.. code-block:: python

	
	# first update all features
	for feature in font.features:
		if feature.automatic:
			feature.update()
	
	# then export fonts
	for instance in font.instances:
		if instance.active:
			instance.generate()
	




:mod:`GSGlyph`
===============================================================================

Implementation of the glyph object.

For details on how to access these glyphs, please see :class:`GSFont`.glyphs

.. class:: GSGlyph([name])

	:param name: The glyph name
	
Properties
	
.. autosummary::

	parent
	layers
	name
	unicode
	string
	id
	category
	subCategory
	script
	glyphInfo
	leftKerningGroup
	rightKerningGroup
	leftMetricsKey
	rightMetricsKey
	export
	color
	note
	selected
	
	
Functions

.. autosummary::

	beginUndo()
	endUndo()
	updateGlyphInfo()

----------
Properties
----------
	


.. attribute:: parent

	Reference to the :class:`GSFont` object.


	:type: :class:`GSFont <GSFont>`


.. attribute:: layers

	The layers of the glyph, collection of :class:`GSLayer` objects. You can access them either by index or by layer ID, which can be a :attr:`GSFontMaster.id <id>`.
	The layer IDs are usually a unique string chosen by Glyphs.app and not set manually. They may look like this: 3B85FBE0-2D2B-4203-8F3D-7112D42D745E


	:type: list, dict


	.. code-block:: python


		# get active layer
		layer = font.selectedLayers[0]
		
		# get glyph of this layer
		glyph = layer.parent
		
		# access all layers of this glyph
		for layer in glyph.layers:
			print layer.name
			
		# access layer of currently selected master of active glyph ...
		# (also use this to access a specific layer of glyphs selected in the Font View)
		layer = glyph.layers[font.selectedFontMaster.id]
		
		# ... which is exactly the same as:
		layer = font.selectedLayers[0]
	
		# directly access 'Bold' layer of active glyph
		for master in font.masters:
			if master.name == 'Bold':
				id = master.id
				break
		layer = glyph.layers[id]

		# add a new layer
		newLayer = GSLayer()
		newLayer.name = '{125, 100}' # (example for glyph-level intermediate master)
		# you may set the master ID that this layer will be associated with, otherwise the first master will be used
		newLayer.associatedMasterId = font.masters[-1].id # attach to last master
		font.glyphs['a'].layers.append(newLayer)

		# duplicate a layer under a different name
		newLayer = font.glyphs['a'].layers[0].copy()
		newLayer.name = 'Copy of layer'
		# FYI, this will still be the old layer ID (in case of duplicating) at this point
		print newLayer.layerId
		font.glyphs['a'].layers.append(newLayer)
		# FYI, the layer will have been assigned a new layer ID by now, after having been appended
		print newLayer.layerId

		# replace the second master layer with another layer
		newLayer = GSLayer()
		newLayer.layerId = font.masters[1].id # Make sure to sync the master layer ID
		font.glyphs['a'].layers[font.masters[1].id] = newLayer
		
		# delete last layer of glyph
		# (Also works for master layers. They will be emptied)
		del(font.glyphs['a'].layers[-1])

		# delete currently active layer
		del(font.glyphs['a'].layers[font.selectedLayers[0].layerId])
		


.. attribute:: name

	The name of the glyph. It will be converted to a "nice name" (afii10017 to A-cy) (you can disable this behavior in font info or the app preference)

	:type: unicode


.. attribute:: unicode

	String with the hex Unicode value of glyph, if encoded.
	Read only.

	:type: unicode


.. attribute:: string

	String representation of glyph, if encoded.
	This is similar to the string representation that you get when copying glyphs into the clipboard.

	:type: unicode


.. attribute:: id

	An unique identifier for each glyph

	:type: unicode

.. attribute:: category

	The category of the glyph. e.g. 'Letter', 'Symbol'

	:type: unicode


.. attribute:: subCategory

	The subCategory of the glyph. e.g. 'Uppercase', 'Math'

	:type: unicode


.. attribute:: script

	The script of the glyph, e.g. 'latin', 'arabic'.

	:type: unicode


.. attribute:: glyphInfo

	:class:`GSGlyphInfo` object for this glyph with detailed information.

	:type: :class:`GSGlyphInfo`


.. attribute:: leftKerningGroup

	The leftKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.

	:type: unicode

.. attribute:: rightKerningGroup

	The rightKerningGroup of the glyph. All glyphs with the same text in the kerning group end up in the same kerning class.

	:type: unicode

.. attribute:: leftMetricsKey

	The leftMetricsKey of the glyph. This is a reference to another glyph by name. It is used to synchronize the metrics with the linked glyph.

	:type: unicode

.. attribute:: rightMetricsKey

	The rightMetricsKey of the glyph. This is a reference to another glyph by name. It is used to synchronize the metrics with the linked glyph.

	:type: unicode

.. attribute:: export

	Defines whether glyph will export upon font generation

	:type: bool

.. attribute:: color

	Color marking of glyph in UI

	:type: int


	.. code-block:: python


		glyph.color = 0		# red
		glyph.color = 1		# orange
		glyph.color = 2		# brown
		glyph.color = 3		# yellow
		glyph.color = 4		# light green
		glyph.color = 5		# dark green
		glyph.color = 6		# light blue
		glyph.color = 7		# dark blue
		glyph.color = 8		# purple
		glyph.color = 9		# magenta
		glyph.color = 10	# light gray
		glyph.color = 11	# charcoal
		glyph.color = 9223372036854775807	# not colored, white


.. attribute:: note


	:type: unicode

.. attribute:: selected

	Return True if the Glyph is selected in the Font View. 
	This is different to the property font.selectedLayers which returns the selection from the active tab.

	:type: bool


	.. code-block:: python


		# access all selected glyphs in the Font View
		for glyph in font.glyphs:
			if glyph.selected:
				print glyph



---------
Functions
---------

.. function:: beginUndo()
	
	Call this before you do a longer running change to the glyph. Be extra careful to call Glyph.endUndo() when you are finished.

.. function:: endUndo()
	
	This closes a undo group that was opened by a previous call of Glyph.beginUndo(). Make sure that you call this for each beginUndo() call.

.. function:: updateGlyphInfo(changeName = True)
	
	Updates all information like name, unicode etc. for this glyph.



:mod:`GSLayer`
===============================================================================

Implementation of the layer object.

For details on how to access these layers, please see :class:`GSGlyph`.layers

.. class:: GSLayer()

Properties

.. autosummary::
	
	parent
	name
	associatedMasterId
	layerId
	components
	guides
	hints
	anchors
	paths
	LSB
	RSB
	TSB
	BSB
	width
	bounds
	background
	backgroundImage

Functions

.. autosummary::
	
	decomposeComponents()
	compareString()
	connectAllOpenPaths()
	copyDecomposedLayer()
	syncMetrics()
	correctPathDirection()
	removeOverlap()
	beginChanges()
	endChanges()
	cutBetweenPoints()
	intersectionsBetweenPoints()
	addMissingAnchors()

----------
Properties
----------

	
	

.. attribute:: parent

	Reference to the :class:`Glyph <GSGlyph>` object that this layer is attached to.

	:type: :class:`GSGlyph <GSGlyph>`


.. attribute:: name

	Name of layer

	:type: unicode

.. attribute:: associatedMasterId

	The ID of the :class:`FontMaster <GSFontMaster>` this layer belongs to, in case this isn't a master layer. Every layer that isn't a master layer needs to be attached to one master layer.

	:type: unicode


	.. code-block:: python


		# add a new layer
		newLayer = GSLayer()
		newLayer.name = '{125, 100}' # (example for glyph-level intermediate master)
		# you may set the master ID that this layer will be associated with, otherwise the first master will be used
		newLayer.associatedMasterId = font.masters[-1].id # attach to last master
		font.glyphs['a'].layers.append(newLayer)



.. attribute:: layerId

	The unique layer ID is used to access the layer in the :class:`glyphs <GSGlyph>` layer dictionary.
	
	For master layers this should be the id of the :class:`FontMaster <GSFontMaster>`.
	It could look like this: "FBCA074D-FCF3-427E-A700-7E318A949AE5"

	:type: unicode


	.. code-block:: python


		# see ID of active layer
		id = font.selectedLayers[0].layerId
		print id
		FBCA074D-FCF3-427E-A700-7E318A949AE5
		
		# access a layer by this ID
		layer = font.glyphs['a'].layers[id]
		layer = font.glyphs['a'].layers['FBCA074D-FCF3-427E-A700-7E318A949AE5']
		
		# for master layers, use ID of masters
		layer = font.glyphs['a'].layers[font.masters[0].id]



.. attribute:: components

	Collection of :class:`GSComponent` objects

	:type: list


	.. code-block:: python


		layer = Glyphs.font.selectedLayers[0] # current layer

		# add component
		layer.components.append(GSComponent('dieresis'))

		# add component at specific position
		layer.components.append(GSComponent('dieresis', NSPoint(100, 100)))

		# delete specific component
		for i, component in enumerate(layer.components):
		        if component.componentName == 'dieresis':
		                del(layer.components[i])
		                break


.. attribute:: guides

	List of :class:`GSGuideLine` objects.

	:type: list


	.. code-block:: python


		layer = Glyphs.font.selectedLayers[0] # current layer

		# access all guides
		for guide in layer.guides:
			print guide

		# add guideline
		newGuide = GSGuideLine()
		newGuide.position = NSPoint(100, 100)
		newGuide.angle = -10.0
		layer.guides.append(newGuide)

		# delete guide
		del(layer.guides[0])


.. attribute:: hints

	List of :class:`GSHint` objects.

	:type: list


	.. code-block:: python


		layer = Glyphs.font.selectedLayers[0] # current layer

		# access all hints
		for hint in layer.hints:
			print hint

		## todo: add hint

		# delete hint
		del(layer.hint[0])


.. attribute:: anchors

	List of :class:`GSAnchor` objects.

	:type: list, dict


	.. code-block:: python


		layer = Glyphs.font.selectedLayers[0] # current layer

		# access all anchors:
		for a in layer.anchors:
			print a

		# add a new anchor
		layer.anchors['top'] = GSAnchor()

		# delete anchor
		del(layer.anchors['top'])


.. attribute:: paths

	List of :class:`GSPath <GSPath>` objects.

	:type: list


	.. code-block:: python


		# access all paths
		for path in layer.paths:
			print path

		# delete path
		del(layer.paths[0])


.. attribute:: LSB

	Left sidebearing

	:type: float


.. attribute:: RSB

	Right sidebearing

	:type: float

.. attribute:: TSB

	Top sidebearing

	:type: float

.. attribute:: BSB

	Bottom sidebearing

	:type: float

.. attribute:: width

	Glyph width

	:type: float

.. attribute:: bounds

	Bounding box as NSRect. Read-only.

	:type: NSRect
	

	.. code-block:: python


		layer = Glyphs.font.selectedLayers[0] # current layer

		# origin
		print layer.bounds.origin.x, layer.bounds.origin.y

		# size
		print layer.bounds.size.width, layer.bounds.size.height


.. attribute:: background

	The background layer

	:type: :class:`GSLayer <GSLayer>`



.. attribute:: backgroundImage

	The background image. It will be scaled so that 1 em unit equals 1 of the image's pixels.

	:type: :class:`GSBackgroundImage`


	.. code-block:: python


		# set background image
		layer.backgroundImage = GSBackgroundImage('/path/to/file.jpg')

		# remove background image
		layer.backgroundImage = None


---------
Functions
---------

.. function:: decomposeComponents()
	
	Decomposes all components of the layer at once.

.. function:: compareString()
	
	Returns a string representing the outline structure of the glyph, for compatibility comparison.

	:return: The comparison string

	:rtype: string


	.. code-block:: python


		layer = Glyphs.font.selectedLayers[0] # current layer

		print layer.compareString()
		oocoocoocoocooc_oocoocoocloocoocoocoocoocoocoocoocooc_

.. function:: connectAllOpenPaths()
	
	Closes all open paths when end points are further than 1 unit away from each other.


.. function:: copyDecomposedLayer()
	
	Returns a copy of the layer with all components decomposed.

	:return: A new layer object

	:rtype: :class:`GSLayer <GSLayer>`

.. function:: syncMetrics()
	
	Take over LSB and RSB from linked glyph.


	.. code-block:: python


		# sync metrics of all layers of this glyph
		for layer in glyph.layers:
			layer.syncMetrics()

.. function:: correctPathDirection()
	
	Corrects the path direction.


.. function:: removeOverlap()
	
	Joins all contours.


.. function:: beginChanges()

	Call this before you do bigger changes to the Layer.
	This will increase performance and prevent undo problems.
	Always call layer.endChanges() if you are finished.


.. function:: endChanges()

	Call this if you have called layer.beginChanges before. Make sure to group bot calls properly.

	
.. function:: cutBetweenPoints(Point1, Point2)

	Cuts all paths that intersect the line from Point1 to Point2
	
	:param Point1: one point
	:param Point2: the other point


	.. code-block:: python


		layer = Glyphs.font.selectedLayers[0] # current layer

		# cut glyph in half horizontally at y=100
		layer.cutBetweenPoints(NSPoint(0, 100), NSPoint(layer.width, 100))


.. function:: intersectionsBetweenPoints(Point1, Point2)

	Return all intersection points between a measurement line and the paths in the layer. This is basically identical to the measurement tool in the UI.
	
	Normally, the first returned point is the starting point, the last returned point is the end point. Thus, the second point is the first intersection, the second last point is the last intersection.
	
	
	:param Point1: one point
	:param Point2: the other point


	.. code-block:: python


		layer = Glyphs.font.selectedLayers[0] # current layer

		# show all intersections with glyph at y=100
		intersections = layer.intersectionsBetweenPoints((-1000, 100), (layer.width+1000, 100))
		print intersections
		
		# left sidebearing at measurement line
		print intersections[1].x

		# right sidebearing at measurement line
		print layer.width - intersections[-2].x


.. function:: addMissingAnchors()

	Adds missing anchors defined in the glyph database.



:mod:`GSAnchor`
===============================================================================

Implementation of the anchor object.

For details on how to access them, please see :class:`GSLayer`.anchors

.. class:: GSAnchor([name, pt])

	:param name: the name of the anchor
	:param pt: the position of the anchor

Properties

.. autosummary::
	
	position
	name
	

----------
Properties
----------



.. attribute:: position

	The position of the anchor

	:type: NSPoint
	

	.. code-block:: python

	
		# read position
		print layer.anchors['top'].position.x, layer.anchors['top'].position.y

		# set position
		layer.anchors['top'].position = NSPoint(175, 575)

		# increase vertical position by 50 units
		layer.anchors['top'].position = NSPoint(layer.anchors['top'].position.x, layer.anchors['top'].position.y + 50)



.. attribute:: name

	The name of the anchor

	:type: unicode


:mod:`GSComponent`
===============================================================================

Implementation of the component object.
For details on how to access them, please see :class:`GSLayer`.components

.. class:: GSComponent(glyph [, position])
	
	:param glyph: a :class:`GSGlyph` object or the glyph name
	:param position: the position of the component as NSPoint

Properties

.. autosummary::
	
	position
	componentName
	component
	transform
	bounds
	
Functions

.. autosummary::
	
	decompose

	
----------
Properties
----------

	

.. attribute:: position

	The Position of the component.

	:type: NSPoint

.. attribute:: componentName

	The glyph name the component is pointing to.

	:type: unicode

.. attribute:: component

	The :class:`GSGlyph` the component is pointing to. This is read only. In order to change the referenced base glyph, set :class:`GSComponent`.componentName to the new glyph name.

	:type: :class:`GSGlyph`


.. attribute:: transform

	
	returns a six number tuple that contrains a transformation matrix: (1, 0, 0, 1, 0, 0) (m11, m12, m21, m22, tX, tY)
	

	:type: NSAffineTransformStruct

.. attribute:: bounds

	
	Bounding box of the component, read only
	

	:type: NSRect
	

	.. code-block:: python


		component = layer.components[0] # first component

		# origin
		print component.bounds.origin.x, component.bounds.origin.y

		# size
		print component.bounds.size.width, component.bounds.size.height


.. attribute:: disableAlignment

	
	Defines whether the component is automatically aligned.
	

	:type: bool

.. attribute:: anchor

	
	If more than one anchor/_anchor pair would match, this property can be used to set the anchor to use for automatic alignment
	
	This can be set from the anchor button in the component info box in the UI
	

	:type: unicode



----------
Functions
----------


.. function:: decompose()
	
	Decomposes the component.



:mod:`GSPath`
===============================================================================

Implementation of the path object.

For details on how to access them, please see :class:`GSLayer`.paths

If you build a path in code, make sure that the structure is valid. A curve node has to be preceded by two off-curve nodes. And an open path has to start with a line node.

.. class:: GSPath()

Properties

.. autosummary::
	
	parent
	nodes
	segments
	closed
	direction
	bounds
	
Functions

.. autosummary::
	
	reverse

----------
Properties
----------

	


.. attribute:: parent

	Reference to the :class:`Layer <GSLayer>` object.


	:type: :class:`GSLayer <GSLayer>`


.. attribute:: nodes

	A list of :class:`GSNode <GSNode>` objects

	:type: list
	

	.. code-block:: python


		# access all nodes
		for path in layer.paths:
			for node in path.nodes:
				print node

	

.. attribute:: segments

	A list of segments as NSPoint objects. Two objects represent a line, four represent a curve. Start point of the segment is included.

	:type: list


	.. code-block:: python


		# access all segments
		for path in layer.paths:
			for segment in path.segments:
				print segment


.. attribute:: closed

	Returns True if the the path is closed

	:type: bool

.. attribute:: direction

	Path direction. -1 for counter clockwise, 1 for clockwise.

	:type: int

.. attribute:: bounds

	Bounding box of the path, read only

	:type: NSRect


	.. code-block:: python


		path = layer.paths[0] # first path

		# origin
		print path.bounds.origin.x, path.bounds.origin.y

		# size
		print path.bounds.size.width, path.bounds.size.height
	


----------
Functions
----------

.. function:: reverse()
	
	Reverses the path direction



:mod:`GSNode`
===============================================================================

Implementation of the node object.

For details on how to access them, please see :class:`GSPath`.nodes


.. class:: GSNode([pt, type])
	
	:param pt: The position of the node.
	:param type: The type of the node, GSLINE, GSCURVE or GSOFFCURVE

Properties

.. autosummary::
	
	position
	type
	connection

----------
Properties
----------

	

.. attribute:: position

	The position of the node.

	:type: NSPoint

.. attribute:: type

	The type of the node, GSLINE, GSCURVE or GSOFFCURVE

	:type: int

.. attribute:: connection

	The type of the connection, GSSHARP or GSSMOOTH

	:type: int


:mod:`GSGuideLine`
===============================================================================

Implementation of the guide line object.

For details on how to access them, please see :class:`GSLayer`.guides


.. class:: GSGuideLine()

Properties

.. autosummary::
	
	position
	angle
	name


----------
Properties
----------
	
	position
	angle
	name

	

.. attribute:: position

	The position of the node.

	:type: NSPoint

.. attribute:: angle

	Angle

	:type: float

.. attribute:: name

	a optional name

	:type: unicode


:mod:`GSHint`
===============================================================================

Implementation of the hint object.

For details on how to access them, please see :class:`GSLayer`.hints

.. class:: GSHint()

Properties

.. autosummary::
	
	originNode
	targetNode
	type
	horizontal

----------
Properties
----------

	

.. attribute:: originNode

	The the first node this hint is attached to.
	

	:type: :class:`GSNode <GSNode>`


.. attribute:: targetNode

	The the second node this hint is attached to. In case of a ghost hint this value will be empty.
	

	:type: :class:`GSNode`


.. attribute:: otherNode1

	A third node this hint is attached to. Used for Interpolation or Diagonal hints.
	

	:type: :class:`GSNode`

.. attribute:: otherNode2

	A forth node this hint is attached to. Used for Diagonal hints.


	:type: :class:`GSNode`

.. attribute:: type

	See Constants section at the bottom of the page

	:type: int

.. attribute:: horizontal

	True if hint is horizontal, False if vertical.

	:type: bool


:mod:`GSBackgroundImage`
===============================================================================

Implementation of background image.

For details on how to access it, please see :class:`GSLayer`.backgroundImage

.. class:: GSBackgroundImage([path])

	:param path: Initialize with an image file (optional)

Properties

.. autosummary::
	
	path
	image
	crop
	locked
	position
	scale
	transform
	
Functions

.. autosummary::

	resetCrop
	scaleWidthToEmUnits
	scaleHeightToEmUnits

----------
Properties
----------

	

.. attribute:: path

	Path of image file

	:type: unicode


.. attribute:: image

	
	:class:`NSImage <NSImage>` object of background image, read only (as in: not settable)
	

	:type: :class:`NSImage <NSImage>`


.. attribute:: crop

	
	Crop rectangle. This is relative to the image's size in pixels, not the font's em units (just in case the image is scaled to something other than 100%).
	

	:type: :class:`NSRect`


	.. code-block:: python


		# change cropping
		layer.backgroundImage.crop = NSRect(NSPoint(0, 0), NSPoint(1200, 1200))


.. attribute:: locked

	
	Defines whether image is locked for access in UI.
	

	:type: bool


.. attribute:: position

	
	Position of image in font's em units.
	

	:type: :class:`NSPoint`


	.. code-block:: python


		# change position
		layer.backgroundImage.position = NSPoint(50, 50)


.. attribute:: scale

	
	Scale factor of image.
	
	A scale factor of 1.0 (100%) means that 1 em unit equals 1 of the image's pixels.
	
	This sets the scale factor for x and y scale simultaneously. For separate scale factors, please use the transormation matrix.
	

	:type: float


.. attribute:: transform

	
	Transformation matrix.
	

	:type: :class:`NSAffineTransformStruct`


	.. code-block:: python


		# change transformation
		layer.backgroundImage.transform = (
			1.0, # x scale factor
			0.0, # x skew factor
			0.0, # y skew factor
			1.0, # y scale factor
			0.0, # x position
			0.0  # y position
			)


----------
Functions
----------



.. function:: resetCrop
	
	Resets the cropping to the image's original dimensions.

.. function:: scaleWidthToEmUnits
	
	Scale the image's cropped width to a certain em unit value, retaining its aspect ratio.


	.. code-block:: python


		# fit image in layer's width
		layer.backgroundImage.scaleWidthToEmUnits(layer.width)
		


.. function:: scaleHeightToEmUnits
	
	Scale the image's cropped height to a certain em unit value, retaining its aspect ratio.


	.. code-block:: python


		# position image's origin at descender line
		layer.backgroundImage.position = NSPoint(0, font.masters[0].descender)

		# scale image to UPM value
		layer.backgroundImage.scaleHeightToEmUnits(font.upm)



:mod:`GSEditViewController`
===============================================================================

Implementation of the GSEditViewController object, which represents edit tabs in the UI.

For details on how to access them, please look at :class:`GSFont`.tabs


.. class:: GSEditViewController()

Properties

.. autosummary::

	text
	layers


----------
Properties
----------





.. attribute:: text

	The text of the tab, either as text or glyph names with / , or mixed.
	

	:type: Unicode



.. attribute:: layers

	Alternatively, you can set (and read) a list of :class:`GSLayer` objects. These can be any of the layers of a glyph.
	
	


	:type: list


	.. code-block:: python


		
		font.tabs[0].layers = []
		
		# display all layers of one glyph next to each other
		for layer in font.glyphs['a'].layers:
			font.tabs[0].layers.append(layer)
	



:mod:`GSGlyphInfo`
===============================================================================

Implementation of the GSGlyphInfo object.

This contains valuable information from the glyph database. See :class:`GSGlyphsInfo` for how to create these objects.

.. class:: GSGlyphInfo()

Properties

.. autosummary::

	name
	productionName
	category
	subCategory
	components
	accents
	anchors
	unicode
	unicode2
	script
	index
	sortName
	sortNameKeep
	desc
	altNames
	desc


----------
Properties
----------





.. attribute:: name

	Human readable name of glyph ("nice name")

	:type: unicode



.. attribute:: productionName

	Production name of glyph. Will return a value only if production name differs from nice name, otherwise None.

	:type: unicode



.. attribute:: category

	This is mostly from the UnicodeData.txt file from unicode.org. Some corrections have been made (Accents, ...)
	e.g: "Letter", "Number", "Punctuation", "Mark", "Separator", "Symbol", "Other"

	:type: unicode



.. attribute:: subCategory

	This is mostly from the UnicodeData.txt file from unicode.org. Some corrections and additions have been made (Smallcaps, ...)
	e.g: "Uppercase", "Lowercase", "Smallcaps", "Ligature", "Decimal Digit", ...

	:type: unicode



.. attribute:: components

	This glyph may be composed of the glyphs returned as a list of :class:`GSGlyphInfo` objects.

	:type: list



.. attribute:: accents

	This glyph may be combined with these accents, returned as a list of glyph names

	:type: list



.. attribute:: anchors

	Anchors defined for this glyph, as a list of anchor names

	:type: list



.. attribute:: unicode

	Unicode value of glyph

	:type: list



.. attribute:: script

	Script of glyph, e.g: "latin", "cyrillic", "greek"

	:type: unicode




.. attribute:: index

	Index of glyph in database. Used for sorting in UI.

	:type: unicode




.. attribute:: sortName

	Alternative name of glyph used for sorting in UI.

	:type: unicode




.. attribute:: sortNameKeep

	Alternative name of glyph used for sorting in UI, when using 'keep alternate glyphs together'.

	:type: unicode




.. attribute:: desc

	Unicode description of glyph

	:type: unicode




.. attribute:: altNames

	Alternative names for glyphs that are not used but should get recognized.

	:type: unicode




Methods
=======

.. autosummary::

	divideCurve()
	distance()
	addPoints()
	subtractPoints()
	GetOpenFile()
	GetSaveFile()
	Message()
	
.. function:: divideCurve(P0, P1, P2, P3, t)
	
	Divides the curve using the De Casteljau's algorithm.
	
	:param P0: The Start point of the Curve (NSPoint)
	:param P1: The first off curve point
	:param P2: The second off curve point
	:param P3: The End point of the Curve
	:param t: The time parameter
	:return: A list of points that represent two curves. (Q0, Q1, Q2, Q3, R1, R2, R3). Note that the "middle" point is only returned once.
	:rtype: list
.. function:: distance(P0, P1)
	
	calculates the distance between two NSPoints
	
	:param P0: a NSPoint
	:param P1: another NSPoint
	:return: The distance
	:rtype: float
.. function:: addPoints(P1, P2)
	
	Add the points.

	:param P0: a NSPoint
	:param P1: another NSPoint
	:return: The sum of both points
	:rtype: NSPoint
.. function:: subtractPoints(P1, P2)
	
	Subtracts the points.
	
	:param P0: a NSPoint
	:param P1: another NSPoint
	:return: The subtracted point
	:rtype: NSPoint
.. function:: scalePoint(P, scalar)
	
	Scaled a point.

	:param P: a NSPoint
	:param scalar: The Multiplier
	:return: The multiplied point
	:rtype: NSPoint

.. function:: GetSaveFile(message=None, ProposedFileName=None, filetypes=None)
	
	Opens a file chooser dialog.
	
	:param message:
	:param filetypes:
	:param ProposedFileName:
	:return: The selected file or None
	:rtype: unicode

.. function:: GetOpenFile(message=None, allowsMultipleSelection=False, filetypes=None)
	
	Opens a file chooser dialog.
	
	:param message: A message string.
	:param allowsMultipleSelection: Boolean, True if user can select more than one file
	:param filetypes: list of strings indicating the filetypes, e.g. ["gif", "pdf"]
	
	:return: The selected file or a list of file names or None
	:rtype: unicode or list

.. function:: GetFolder(message=None, allowsMultipleSelection = False)
	
	Opens a folder chooser dialog.
	
	:param message:
	:param allowsMultipleSelection:
	:return: The selected folder or None
	:rtype: unicode

.. function:: Message(title, message, OKButton=None)
	
	Shows a alert panel
	
	:param title:
	:param message:
	:param OKButton:


Constants
=========

Node types

	GSLINE = 1
		Line node.

	GSCURVE = 35
		Curve node. Make sure that each curve node is preceded by two off-curve nodes.

	GSOFFCURVE = 65
		Off-cuve node

Node connection

	GSSHARP = 0
		Sharp connection.

	GSSMOOTH = 100
		A smooth or tangent node

Hint types

	TOPGHOST = -1
		Top ghost for PS hints
	
	STEM = 0
		Stem for PS hints
	
	BOTTOMGHOST = 1
		Bottom ghost for PS hints
	
	TTANCHOR = 2
		Anchor for TT hints

	TTSTEM = 3
		Stem for TT hints
	
	TTALIGN = 4
		Aling for TT hints

	TTINTERPOLATE = 5
		Interpolation for TT hints

	TTDIAGONAL = 6
		Diagonal for TT hints

	CORNER = 16
		Corner Component

	CAP = 17
		Cap Component
	
Hint Option 
	
	This is only used for TrueType hints.
	
	TTROUND = 0
		Round to grid
		
	TTROUNDUP = 1
		Round up
		
	TTROUNDDOWN = 2
		Round down
		
	TTDONTROUND = 4
		Don’t round at all
		
	TRIPLE = 128
		Indicates a triple hint group. There need to be exactly three horizontal TTStem hints with this setting to take effect.
	
