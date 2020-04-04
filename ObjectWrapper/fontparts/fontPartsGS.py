# encoding: utf-8

from __future__ import print_function
import objc
from GlyphsApp import *
from GlyphsApp import Proxy
from Foundation import NSString, NSAffineTransform

class FontInfoProxy(Proxy):
	
	def __set__(self, attr, value):
		# check to see if the attribute has been
		# deprecated. if so, warn the caller and
		# update the attribute and value.
		
		# if attr in self._deprecatedAttributes:
		# 	newAttr, newValue = ufoLib.convertFontInfoValueForAttributeFromVersion1ToVersion2(attr, value)
		# 	note = "The %s attribute has been deprecated. Use the new %s attribute." % (attr, newAttr)
		# 	warn(note, DeprecationWarning)
		# 	attr = newAttr
		# 	value = newValue
		print("__FontInfoProxy", attr, value)
		_baseAttributes = ["_owner", "changed", "selected", "getParent"]
		_renameAttributes = {"openTypeNameManufacturer": "manufacturer",
						  "openTypeNameManufacturerURL": "manufacturerURL",
								 "openTypeNameDesigner": "designer",
							  "openTypeNameDesignerURL": "designerURL",
								  # "openTypeNameLicense": "license",
								  # "openTypeNameLicenseURL": "licenseURL",
											 "fontName": "postscriptFontName",
											"vendorURL": "manufacturerURL",
											 "uniqueID": "postscriptUniqueID",
											"otMacName": "openTypeNameCompatibleFullName" };
		_masterAttributes = ["postscriptUnderlinePosition",
							 "postscriptUnderlineThickness",
							 "openTypeOS2StrikeoutSize",
							 "openTypeOS2StrikeoutPosition"]
		# setting a known attribute
		if attr in _masterAttributes:
			if type(value) == type([]):
				value = NSMutableArray.arrayWithArray_(value)
			elif type(value) == type(1):
				value = NSNumber.numberWithInt_(value)
			elif type(value) == type(1.2):
				value = NSNumber.numberWithFloat_(value)
			
			if attr in _renameAttributes:
				attr = _renameAttributes[attr]
			
			self._owner._font.fontMasterAtIndex_(self._owner._masterIndex).setValue_forKey_(value, attr)
			return
		
		if attr not in _baseAttributes:
			try:
				if type(value) == type([]):
					value = NSMutableArray.arrayWithArray_(value)
				elif type(value) == type(1):
					value = NSNumber.numberWithInt_(value)
				elif type(value) == type(1.2):
					value = NSNumber.numberWithFloat_(value)
				
				if attr in _renameAttributes:
					attr = _renameAttributes[attr]
				
				self._owner._font.setValue_forKey_(value, attr)
			except:
				raise AttributeError("Unknown attribute %s." % attr)
			return
		else:
			raise AttributeError("Unknown attribute %s." % attr)
	
	def __get__(self, attr):
		_baseAttributes = ["_owner", "changed", "selected", "getParent"]
		_renameAttributes = {
							 "openTypeNameManufacturer": "manufacturer",
						  "openTypeNameManufacturerURL": "manufacturerURL",
								 "openTypeNameDesigner": "designer",
							  "openTypeNameDesignerURL": "designerURL",
							}
		try:
			gsFont = self._owner._font
			value = gsFont.valueForKey_(attr)
			if value is None and attr in _renameAttributes:
				value = gsFont.valueForKey_(_renameAttributes[attr])
			if value is None:
				Instance = gsFont.fontMasterAtIndex_(self._owner._masterIndex)
				if Instance is None:
					raise ValueError("The font has no Instance")
				value = Instance.valueForKey_(attr)
				if value is None and attr in _renameAttributes:
					value = Instance.valueForKey_(_renameAttributes[attr])
				if value is None:
					if attr == "postscriptFullName" or attr == "fullName":
						value = "%s-%s" % (gsFont.valueForKey_("familyName"), Instance.name)
					elif attr == "postscriptFontName" or attr == "fontName":
						value = "%s-%s" % (gsFont.valueForKey_("familyName"), Instance.name)
						value = value.replace(" ", "")
					elif attr == "styleName":
						value = "%s" % (Instance.name)
			return value
		except:
			raise AttributeError("Unknown attribute %s." % attr)
	def __repr__(self):
		return "<GSFont.info \"%s\">" % self._owner.familyName

GSFont.info = property(lambda self: FontInfoProxy(self))

def GSFont__newGlyph__(self, name, clear=True):
	glyph = self.glyphForName_(name)
	if glyph is None:
		glyph = self.newGlyphWithName_changeName_(name, False)
	return glyph.layers[0]
GSFont.newGlyph = objc.python_method(GSFont__newGlyph__)

GSFont.__len__ = property(lambda self: self.countOfGlyphs) # return the method, not the count itself
def raise__NotImplemented(x=None):
	raise NotImplementedError
GSFont.defaultLayer = property(raise__NotImplemented)

def GS__appendGuideline__(self, position=None, angle=None, name=None, color=None, guideline=None):
	identifier = None 
	if position is None and angle is None and name is None:
		position = guideline.position
		angle = guideline.angle
		name = guideline.name
		identifier = guideline.identifier
	guide = GSGuide()
	if position is not None:
		guide.position = position
	if angle is not None:
		guide.angle = angle
	if name is not None:
		guide.name = name
	if identifier is not None:
		guide._setIdentifier(identifier)
	self.guidelines.append(guide)
	return guide

GSFont.appendGuideline = objc.python_method(GS__appendGuideline__)
GSFont.guidelines = property(lambda self: self.masters[0].guides)

def GSFontMaster__selection(self): # stub to silcense problems with global guide.selection
	return []
GSFontMaster.selection = property(GSFontMaster__selection)

def GSLayer__set_unicodeChar(self, value):
	self.glyph().setUnicode_("%X", value)

GSLayer.unicode = property(lambda self: self.glyph().unicodeChar(), 
						   lambda self, value: GSLayer__set_unicodeChar(self, value))

def GSLayer__appendComponent(self, baseGlyph=None, offset=None, scale=None, component=None):
	if baseGlyph is None and offset is None and scale is None:
		baseGlyph = component.baseGlyph
		offset = component.offset
		scale = component.scale
	newComponent = GSComponent()
	if baseGlyph is not None:
		newComponent.baseGlyph = baseGlyph
	if offset is not None:
		newComponent.offset = offset
	if scale is not None:
		newComponent.scale = scale
	self.shapes.append(newComponent)
	return newComponent
GSLayer.appendComponent = objc.python_method(GSLayer__appendComponent)

def GSLayer__addImage(self, path=None, data=None, scale=None, position=None, color=None):
	if path is not None:
		image = GSBackgroundImage.alloc().initWithPath_(path)
	elif data is not None:
		image = GSBackgroundImage.alloc().initWithData_imageType_(data, "png")
	if scale is not None:
		image.scale = scale
	if position is not None:
		image.position = position
	if color is not None:
		image.color = color
	self.backgroundImage = image
	return image

GSLayer.addImage = objc.python_method(GSLayer__addImage)
def GSLayer__appendContour(self, contour, offset=None):
	if offset is not None:
		contour.moveBy(offset)
	self.shapes.append(contour)
	return contour
GSLayer.appendContour = objc.python_method(GSLayer__appendContour)

def GSLayer__appendAnchor(self, name=None, position=None, color=None, anchor=None):
	if name is None and position is None and color is None:
		name = anchor.name
		position = anchor.position
		color = anchor.color
	newAnchor = GSAnchor()
	if name is not None:
		newAnchor.name = name
	if position is not None:
		newAnchor.position = position
	if color is not None:
		newAnchor.color = color
	self.anchors.append(newAnchor)
	return newAnchor
GSLayer.appendAnchor = objc.python_method(GSLayer__appendAnchor)
GSLayer.appendGuideline = objc.python_method(GS__appendGuideline__)
GSLayer.guidelines = GSLayer.guides
GSLayer.contours = GSLayer.paths

def GSLayer__appendGlyph(self, other, offset=None):
	if len(other.contours) > 0:
		for contour in other.contours:
			self.shapes.append(contour.copy())
	if len(other.contours) > 0:
		for contour in other.contours:
			self.shapes.append(contour.copy())
	if len(other.anchors) > 0:
		for anchor in other.anchors:
			self.anchors.append(anchor.copy())
	if len(other.guidelines) > 0:
		for guideline in other.guidelines:
			self.guidelines.append(guideline.copy())
GSLayer.appendGlyph = objc.python_method(GSLayer__appendGlyph)

def GSLayer__setHeight(self, value):
	try:
		self.setVertWidth_(float(value))
	except:
		raise TypeError
GSLayer.height = property(lambda self: self.vertWidth,
						  GSLayer__setHeight)

def GSLayer__setLeftMargin(self, value):
	try:
		self.setLSB_(float(value))
	except:
		raise TypeError
GSLayer.leftMargin = property(lambda self: self.LSB,
							  GSLayer__setLeftMargin)
def GSLayer__setRightMargin(self, value):
	try:
		self.setRSB_(float(value))
	except:
		raise TypeError
GSLayer.rightMargin = property(lambda self: self.RSB,
							   GSLayer__setRightMargin)
def GSLayer__setTopMargin(self, value):
	try:
		self.setTSB_(float(value))
	except:
		raise TypeError
GSLayer.topMargin = property(lambda self: self.TSB,
							 GSLayer__setTopMargin)
def GSLayer__setBottomMargin(self, value):
	try:
		self.setLSB_(float(value))
	except:
		raise TypeError
GSLayer.bottomMargin = property(lambda self: self.BSB,
								lambda self, value: GSLayer__setBottomMargin(self, value))

def GSLayer__clear(self, contours=True, components=True, anchors=True, guidelines=True, image=True):
	if contours:
		self.removeShapes_(list(self.contours))
	if components:
		self.removeShapes_(list(self.components))
	if anchors:
		self.setAnchors_(None)
	if guidelines:
		self.setGuides_(None)
	if image:
		self.setBackgroundImage_(None)
GSLayer.clear = objc.python_method(GSLayer__clear)

def GSLayer__clearAnchors(self):
	self.setAnchors_(None)
GSLayer.clearAnchors = objc.python_method(GSLayer__clearAnchors)
def GSLayer__removeAnchor(self, anchor):
	if isinstance(anchor, int):
		del self.anchors[anchor]
	elif isinstance(anchor, GSAnchor):
		self.anchors.remove(anchor)
	else:
		raise TypeError
GSLayer.removeAnchor = objc.python_method(GSLayer__removeAnchor)

def GSLayer__clearComponents(self):
	self.removeShapes_(list(self.components))
GSLayer.clearComponents = objc.python_method(GSLayer__clearComponents)
def GSLayer__removeComponent(self, component):
	if isinstance(component, int):
		component = self.components[component]
	if isinstance(component, GSShape):
		self.removeShape_(component)
	else:
		raise TypeError
GSLayer.removeComponent = objc.python_method(GSLayer__removeComponent)

def GSLayer__clearContours(self):
	self.removeShapes_(list(self.contours))
GSLayer.clearContours = objc.python_method(GSLayer__clearContours)
def GSLayer__removeContour(self, contour):
	if isinstance(contour, int):
		contour = self.contours[contour]
	if isinstance(contour, GSShape):
		self.removeShape_(contour)
	else:
		raise TypeError
GSLayer.removeContour = objc.python_method(GSLayer__removeContour)

def GSLayer__clearGuidelines(self):
	self.setGuides_(None)
GSLayer.clearGuidelines = objc.python_method(GSLayer__clearGuidelines)
def GSLayer__removeGuideline(self, guideline):
	if isinstance(guideline, int):
		del self.guides[guideline]
	elif isinstance(guideline, GSGuide):
		self.guides.remove(guideline)
	else:
		raise TypeError
GSLayer.removeGuideline = objc.python_method(GSLayer__removeGuideline)

def GSLayer__clearImage(self):
	sself.setBackgroundImage_(None)
GSLayer.clearImage = objc.python_method(GSLayer__clearImage)

def GSLayer__isEmpty(self):
	return self.countOfShapes() == 0
GSLayer.isEmpty = objc.python_method(GSLayer__isEmpty)
def GSLayer__isCompatible(self, other):
	return (self.compareString() == other.compareString(), None)
GSLayer.isCompatible = objc.python_method(GSLayer__isCompatible)


def getIdentifier(self):
	identifier = NSString.UUID()
	self.setUserData_forKey_(identifier, "public.identifier")
	return identifier
def _setIdentifier(self, identifier):
	self.setUserData_forKey_(identifier, "public.identifier")

GSGuide.color = property(lambda self: self.userDataForKey_("public.color"),
						 lambda self, value: self.setUserData_forKey_(value, "public.color"))

GSGuide.getIdentifier = objc.python_method(getIdentifier)
GSGuide.identifier = property(lambda self: self.userDataForKey_("public.identifier"))
GSGuide._setIdentifier = objc.python_method(_setIdentifier)

GSAnchor.getIdentifier = objc.python_method(getIdentifier)
GSAnchor.identifier = property(lambda self: self.userDataForKey_("public.identifier"))
GSAnchor._setIdentifier = objc.python_method(_setIdentifier)

GSPath.getIdentifier = objc.python_method(getIdentifier)
GSPath.identifier = property(lambda self: self.userDataForKey_("public.identifier"))
GSPath._setIdentifier = objc.python_method(_setIdentifier)

GSComponent.getIdentifier = objc.python_method(getIdentifier)
GSComponent.identifier = property(lambda self: self.userDataForKey_("public.identifier"))
GSComponent._setIdentifier = objc.python_method(_setIdentifier)

GSBackgroundImage.color = property(lambda self: self.userDataForKey_("public.color"),
								   lambda self, value: self.setUserData_forKey_(value, "public.color"))
GSAnchor.color = property(lambda self: self.userDataForKey_("public.color"),
						  lambda self, value: self.setUserData_forKey_(value, "public.color"))
def GSBackgroundImage__data(self):
	if self.imageData() is not None:
		return self.imageData()
	if self.hasValidImageToDraw():
		return self.image.TIFFRepresentation()
	else:
		raise ValueError
GSBackgroundImage.data = property(lambda self: GSBackgroundImage__data(self),
								  lambda self, value: self.setImageData_(value))
GSComponent.baseGlyph = property(lambda self: self.componentName,
								 lambda self, value: self.setComponentName_(value))
GSComponent.offset = GSComponent.position
GSComponent.transformation = GSComponent.transform
def GSPath__newPoint(position=None, type='line', smooth=False, name=None, identifier=None, point=None):
	if position is None and name is None and identifier is None:
		position = point.position
		type = point.type
		smooth = point.smooth
		name = point.name
		identifier = point.identifier
	node = GSNode()
	if position is not None:
		node.position = position
	if type is not None:
		node.type = type
	if smooth is not None:
		node.smooth = smooth
	if name is not None:
		node.name = name
	if identifier is not None:
		node.identifier = identifier
	return node
def GSPath__insertPoint(self, index, position=None, type='line', smooth=False, name=None, identifier=None, point=None):
	node = GSPath__newPoint(position, type, smooth, name, identifier, point)
	self.nodes.insert(index, node)
	return node
GSPath.insertPoint = objc.python_method(GSPath__insertPoint)
def GSPath__appendPoint(self, position=None, type='line', smooth=False, name=None, identifier=None, point=None):
	node = GSPath__newPoint(position, type, smooth, name, identifier, point)
	self.nodes.append(node)
	return node
GSPath.appendPoint = objc.python_method(GSPath__appendPoint)
GSPath.points = GSPath.nodes

def GSPath__moveBy(self, offset):
	transform = NSAffineTransform.new()
	transform.translateXBy_yBy_(offset[0], offset[1])
	self.transform_(transform)
GSPath.moveBy = objc.python_method(GSPath__moveBy)
def GSPath__scaleBy(selg, value, origin=None):
	transform = NSAffineTransform.new()
	if origin is not None:
		transform.translateXBy_yBy_(origin[0], origin[1])
	transform.scaleXBy_yBy_(value[0], value[1])
	if origin is not None:
		transform.translateXBy_yBy_(-origin[0], -origin[1])
	self.transform_(transform)
GSPath.scaleBy = objc.python_method(GSPath__scaleBy)
def GSPath__rotateBy(self, value, origin=None):
	transform = NSAffineTransform.new()
	if origin is not None:
		transform.translateXBy_yBy_(origin[0], origin[1])
	transform.rotateByDegrees_(value)
	if origin is not None:
		transform.translateXBy_yBy_(-origin[0], -origin[1])
	self.transform_(transform)
GSPath.rotateBy = objc.python_method(GSPath__rotateBy)
