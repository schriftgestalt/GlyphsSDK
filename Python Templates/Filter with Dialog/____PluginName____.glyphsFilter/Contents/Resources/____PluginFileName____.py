# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re, traceback

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp
from GlyphsApp import *

"""
	Using Interface Builder (IB):
	
	Your code communicates with the UI through
	- IBOutlets (.py->GUI): values available to a UI element (e.g. a string for a text field)
	- IBActions (GUI->.py): methods in this class, triggered by buttons or other UI elements
	
	In order to make the Interface Builder items work, follow these steps:
	1. Make sure you have your IBOutlets for all your UI controls defined as class variables
	   at the beginning of this controller class, e.g.:
#	      myValueField = objc.IBOutlet()
	   To keep the oversight, I recommend you name it after the value, and add "Field" to
	   the end of the name, e.g., myValue -> myValueField.
	2. Immediately *before* the def statement of a method that is supposed to be triggered
	   by a UI action (e.g., setMyValue_() triggered by the My Value field), put:
#	      @objc.IBAction
	   Make sure the method name ends with an underscore, e.g. setValue_(),
	   otherwise the action will not be able to send its value to the class method.
	3. Open the .xib file in Xcode, and add and arrange interface elements.
	4. Add this .py file via File > Add Files..., Xcode will recognize IBOutlets and IBActions.
	   Depending on your Xcode version and settings, the .py file may not be selectable.
	   In that case, simply add its enclosing folder.
	5. In the left sidebar, choose Placeholders > File's Owner,
	   in the right sidebar, open the Identity inspector (3rd icon),
	   and put the name of this controller class in the Custom Class > Class field
	6. IBOutlets: Ctrl-drag from the File's Owner to a UI element (e.g. text field),
	   and choose which outlet shall be linked to the UI element
	7. IBActions: Ctrl-drag from a UI element (e.g. button) to the File’s Owner in the left sidebar,
	   and choose the class method the UI element is supposed to trigger.
	   If you want a stepping field (i.e., change the value with up/downarrow),
	   then select the Entry Field, and set Identity Inspector > Custom Class to:
#	      GSSteppingTextField
	   ... and Attributes Inspector (top right, 4th icon) > Control > State to:
#	      Continuous
	8. Compile the .xib file to a .nib file with this Terminal command:
#	      ibtool xxxDialog.xib --compile xxxDialog.nib
	   (Replace xxxDialog by the name of your xib/nib)
	   Please note: Every time the .xib is changed, it has to be recompiled to a .nib.
	   Check Console.app for error messages to see if everything went right.
	9. In process_(), the last values entered for every value field are saved in the defaults.
	   Add a line like this for every value:
#	      FontMaster.userData[ "myValue" ] = NSNumber.numberWithFloat_( self.myValue )
	   Likewise, use NSNumber.numberWithInteger_() for integers.
	10. In setup(), for every outlet, add these two lines. These will restore the last
	   value entered from the font master defaults, and put it back into the field.
#	      self.myValue = self.setDefaultFloatValue( "myValue", 15.0, FontMaster )
#	      self.myValueField.setFloatValue_( self.myValue )
	   Use setDefaultFloatValue() for float values, and setDefaultIntegerValue() for integers.
	   Feel free to roll your own setDefault...() methods for other types.
	11. Do not forget to expand the arguments in processLayerWithValues() if you have multiple
	   value entry fields in your UI.
	12. Adjust processFont_withArguments_() accordingly if you want to enable
	   the triggering of your filter through an instance custom parameter.
	   Your values will be stored in Arguments[1], Arguments[2], etc.
"""

#GlyphsFilterProtocol = objc.protocolNamed( "GlyphsFilter" )

#class FilterWithDialog ( NSObject, GlyphsFilterProtocol ):


class FilterWithDialog ( GSFilterPlugin ):
	"""
	All 'myValue' and 'myValueField' references are just an example.
	They correspond to the 'My Value' field in the .xib file.
	Replace and add your own class variables.
	"""
	
	
	
	def init( self ):
		"""
		Do all initializing here.
		This is a good place to call random.seed() if you want to use randomisation.
		In that case, don't forget to import random at the top of this file.
		"""

		try:

			self.menuName = 'My Filter'
			self.keyboardShortcut = None # With Cmd+Shift
			self.dialogName = '____PluginFileName____Dialog'
			self.actionButtonLabel = 'Apply'
	
	
			if hasattr(self, 'settings'):
				self.settings()

	

#			self._view = self.dialog
			NSBundle.loadNibNamed_owner_(self.dialogName, self )

		
#			if hasattr(self, 'loadPlugin'):
#				self.loadPlugin()

	#			self.setup()

			return self

		except:
			self.logToConsole(traceback.format_exc())
	
	
	def setup(self):
		try:
#
			super( FilterWithDialog, self ).setup()

			if hasattr(self, 'loadPlugin'):
				self.loadPlugin()

			self.process_(None)

			return None
		except:
			self.logToConsole(traceback.format_exc())
			
		
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def title( self ):
		"""
		This is the name as it appears in the menu
		and in the title of the dialog window.
		"""
		try:
			return self.menuName
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def actionName( self ):
		"""
		This is the title of the button in the settings dialog.
		Use something descriptive like 'Move', 'Rotate', or at least 'Apply'.
		"""
		try:
			return self.actionButtonLabel
		except Exception as e:
			self.logToConsole( "actionName: %s" % str(e) )
	
	def keyEquivalent( self ):
		""" 
		The key together with Cmd+Shift will be the shortcut for the filter.
		Return None if you do not want to set a shortcut.
		Users can set their own shortcuts in System Prefs.
		"""
		try:
			return self.keyboardShortcut
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	


	def processFont_withArguments_( self, Font, Arguments ):
		"""
		Invoked when called as Custom Parameter in an instance at export.
		The Arguments come from the custom parameter in the instance settings. 
		Item 0 in Arguments is the class-name. The consecutive items should be your filter options.
		"""
		try:
			
			# set glyphList (list of glyphs to be processed) to all glyphs in the font
			glyphList = Font.glyphs

			# customParameters delivered to filter()
			customParameters = {}
			unnamedCustomParameterCount = 0
			for i in range(1, len(Arguments)):
				if not 'include' in Arguments[i] and not 'exclude' in Arguments[i]:
					
					# if key:value pair
					if ':' in Arguments[i]:
						key, value = Arguments[i].split(':')
					# only value given, no key. make key name
					else:
						key = unnamedCustomParameterCount
						unnamedCustomParameterCount += 1
						value = Arguments[i]
					
					# attempt conversion to float value
					try:
						customParameters[key] = float(value)
					except:
						customParameters[key] = value
			
			# change glyphList to include or exclude glyphs
			if len( Arguments ) > 1:
				if "exclude:" in Arguments[-1]:
					excludeList = [ n.strip() for n in Arguments.pop(-1).replace("exclude:","").strip().split(",") ]
					glyphList = [ g for g in glyphList if not g.name in excludeList ]
				elif "include:" in Arguments[-1]:
					includeList = [ n.strip() for n in Arguments.pop(-1).replace("include:","").strip().split(",") ]
					glyphList = [ Font.glyphs[n] for n in includeList ]
			
			# With these values, call your code on every glyph:
			FontMasterId = Font.fontMasterAtIndex_(0).id
			for thisGlyph in glyphList:
				Layer = thisGlyph.layerForKey_( FontMasterId )

				if hasattr(self, 'filter'):
					self.filter( Layer, False, customParameters )

		except:
			self.logToConsole(traceback.format_exc())
	
	def process_( self, sender ):
		"""
		This method gets called when the user invokes the Dialog.
		"""
		try:
			# Create Preview in Edit View, and save & show original in ShadowLayers:
			ShadowLayers = self.valueForKey_( "shadowLayers" )
			Layers = self.valueForKey_( "layers" )
			checkSelection = True
			for k in range(len( ShadowLayers )):
				ShadowLayer = ShadowLayers[k]
				Layer = Layers[k]
				Layer.setPaths_( NSMutableArray.alloc().initWithArray_copyItems_( ShadowLayer.pyobjc_instanceMethods.paths(), True ) )
				Layer.setSelection_( NSMutableArray.array() )
				try:
					# Glyphs 2.1 and earlier:
					if len(ShadowLayer.selection()) > 0 and checkSelection:
						for i in range(len( ShadowLayer.paths )):
							currShadowPath = ShadowLayer.paths[i]
							currLayerPath = Layer.paths[i]
							for j in range(len(currShadowPath.nodes)):
								currShadowNode = currShadowPath.nodes[j]
								if ShadowLayer.selection().containsObject_( currShadowNode ):
									Layer.addSelection_( currLayerPath.nodes[j] )
				except:
					# Glyphs 2.2 and later:
					if len(ShadowLayer.selection) > 0 and checkSelection:
						for i in range(len( ShadowLayer.paths )):
							currShadowPath = ShadowLayer.paths[i]
							currLayerPath = Layer.paths[i]
							for j in range(len(currShadowPath.nodes)):
								currShadowNode = currShadowPath.nodes[j]
								if currShadowNode in ShadowLayer.selection:
									Layer.addSelection_( currLayerPath.nodes[j] )
								
				self.filter( Layer, Glyphs.font.currentTab != None, {} ) # add your class variables here
				Layer.clearSelection()
		
			# Safe the values in the FontMaster. But could be saved in UserDefaults, too.
#			FontMaster = self.valueForKey_( "fontMaster" )
#			FontMaster.userData[ "____myValue____" ] = NSNumber.numberWithInteger_( self.____myValue____ )
			
			# call the superclass to trigger the immediate redraw:
			super( FilterWithDialog, self ).process_( sender )
		except:
			self.logToConsole(traceback.format_exc())
	
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Filter %s:\n%s" % ( self.title(), message )
		NSLog( myLog )

	def view(self):
		return self.dialog
	
	def preview(self):
		self.process_( None )
		Glyphs.redraw()
		
########################################################################		
# encoding: utf-8

#from plugin import *
from AppKit import *
from GlyphsApp import *

class ____PluginClassName____(FilterWithDialog):

	# Definitions of IBOutlets
	
	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()

	# Text field in dialog
	myTextField = objc.IBOutlet()
	
	def settings(self):
		self.menuName = 'My Filter'

	# On UI trigger
	def loadPlugin(self):

		# Set default setting if not present
		if not Glyphs.defaults['com.myname.myfilter.value']:
			Glyphs.defaults['com.myname.myfilter.value'] = 15.0

		# Set value of text field
		self.myTextField.setFloatValue_(Glyphs.defaults['com.myname.myfilter.value'])
		
		# Set focus to text field
		self.myTextField.becomeFirstResponder()

	# Action triggered by UI
	@objc.IBAction
	def setValue_( self, sender ):

		# Store value coming in from dialog
		Glyphs.defaults['com.myname.myfilter.value'] = sender.floatValue()

		# Trigger redraw of preview
		self.preview()

	# Actual filter
	def filter(self, layer, inEditView, customParameters):
		
		# Called on font export, get value from customParameters
		if customParameters.has_key('shift'):
			value = customParameters['shift']

		# Called through UI, use stored value
		else:
			value = Glyphs.defaults['com.myname.myfilter.value']

		# Shift all nodes in x and y direction by the value
		for path in layer.paths:
			for node in path.nodes:
				node.position = NSPoint(node.position.x + value, node.position.y + value)

	
	def customParameterString( self ):
		return "%s; shift:%s;" % (self.__class__.__name__, Glyphs.defaults['com.myname.myfilter.value'] )
