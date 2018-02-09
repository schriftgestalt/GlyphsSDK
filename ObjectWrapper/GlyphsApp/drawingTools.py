#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

from AppKit import NSBezierPath, NSColor, NSFont, NSImage, NSGradient, NSColorSpace, NSMiterLineJoinStyle, NSRoundLineJoinStyle, NSBevelLineJoinStyle, NSFontAttributeName, NSForegroundColorAttributeName, NSGraphicsContext, NSCompositeSourceOver, NSGradientDrawsBeforeStartingLocation, NSGradientDrawsAfterEndingLocation
from Foundation import NSMakeRect, NSAffineTransform, NSClassFromString, NSMakePoint, NSZeroRect

def drawGlyph(glyph):
	path = glyph._layer.bezierPath
	drawPath(path)

def save():
	# save the current graphic state 
	NSGraphicsContext.currentContext().saveGraphicsState()
	
def restore():
	# restore the current graphic state 
	NSGraphicsContext.currentContext().restoreGraphicsState()

currentPath = None
currentFillColor = NSColor.blackColor()
currentStrokeColor = None
currentGradient = None
currentFont = NSFont.systemFontOfSize_(NSFont.systemFontSize())

def rect(x, y, width, height):
	# draws a rectangle 
	drawPath(NSBezierPath.bezierPathWithRect_(NSMakeRect(x, y, width, height)))
	
def oval(x, y, width, height):
	# draws an oval
	drawPath(NSBezierPath.bezierPathWithOvalInRect_(NSMakeRect(x, y, width, height)))
	
def line(x1, y1, x2=None, y2=None):
	# draws a line
	if x2 is None and y2 is None and isinstance(x1, tuple) and isinstance(y1, tuple):
		(x1, y1), (x2, y2) = x1, y1
	p = NSBezierPath.bezierPath()
	p.moveToPoint_(NSMakePoint(x1, y1))
	p.lineToPoint_(NSMakePoint(x2, y2))
	drawPath(p)
	
def newPath():
	# creates a new path 
	currentPath = NSBezierPath.bezierPath()
	
def moveTo(pt):
	# move to point
	if currentPath is not None:
		currentPath.moveToPoint_(NSMakePoint(pt[0], pt[1]))
	
def lineTo(pt):
	# line to point
	if currentPath is not None:
		currentPath.lineToPoint_(NSMakePoint(pt[0], pt[1]))
	
def curveTo(h1, h2, pt):
	# curve to point with bcps
	if currentPath is not None:
		currentPath.curveToPoint_controlPoint1_controlPoint2_(NSMakePoint(pt[0], pt[1]), NSMakePoint(h1[0], h1[1]), NSMakePoint(h2[0], h2[1]))

def closePath():
	# close the path
	if currentPath is not None:
		currentPath.closePath()

def drawPath(path=None):
	# draws the path
	if path is None:
		path = currentPath
	if currentFillColor is not None:
		currentFillColor.set()
		path.fill()
	if currentGradient is not None:
		save()
		path.addClip()
		(gradientType, startPoint, endPoint, colors, locations) = currentGradient
		NSColors = []
		for color in colors:
			a = 1
			g = None
			if len(color) == 1:
				r = color[0]
			elif len(color) == 2:
				r, a = color
			elif len(color) == 3:
				r, g, b = color
			elif len(color) == 4:
				r, g, b, a = color
			if g is not None:
				NSColors.append(NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a))
			else:
				NSColors.append(NSColor.colorWithCalibratedWhite_alpha_(r, a))
		gradient = NSGradient.alloc().initWithColors_atLocations_colorSpace_(NSColors, locations, NSColorSpace.deviceRGBColorSpace())
		if gradientType == "linear":
			gradient.drawFromPoint_toPoint_options_(startPoint, endPoint, NSGradientDrawsBeforeStartingLocation | NSGradientDrawsAfterEndingLocation)
		elif gradient.gradientType == "radial":
			pass
		restore()
	if currentStrokeColor is not None:
		currentStrokeColor.set()
		path.stroke()
	
def fill(r=None, g=None, b=None, a=1):
	# Set the fill color as RGB value.
	global currentFillColor
	global currentGradient
	if r is None:
		currentFillColor = None
	elif g is None:
		currentFillColor = NSColor.colorWithDeviceWhite_alpha_(r, a)
		currentGradient = None
	else:
		currentFillColor = NSColor.colorWithDeviceRed_green_blue_alpha_(r, g, b, a)
		currentGradient = None
	
def stroke(r=None, g=None, b=None, a=1):
	# Set the stroke color as RGB value.
	global currentStrokeColor
	if r is None:
		currentStrokeColor = None
	elif g is None:
		currentStrokeColor = NSColor.colorWithDeviceWhite_alpha_(r, a)
	else:
		currentStrokeColor = NSColor.colorWithDeviceRed_green_blue_alpha_(r, g, b, a)
	
def strokeWidth(value):
	# Set the stroke width for a path.
	if currentPath is not None:
		currentPath.lineWidth = value
	
def miterLimit(value):
	# Set the miter limit for a path.
	if currentPath is not None:
		currentPath.miterLimit = value

def lineJoin(join):
	# Set the line join for a path, possible join arguments are: "bevel", "miter" or "round"
	if currentPath is not None:
		Style = NSMiterLineJoinStyle
		if join == "bevel":
			Style = NSBevelLineJoinStyle
		elif join == "round":
			Style = NSRoundLineJoinStyle
		currentPath.lineJoinStyle = Style
	
def dashLine(dash):
	# dash is a list of of values 
	pass

def translate(x, y):
	# Translate the art board pane to "x", "y"
	Transform = NSAffineTransform.alloc().init()
	Transform.translateXBy_yBy_(x, y)
	Transform.concat()
	
def rotate(angle):
	# Rotate the art board by an angle.
	Transform = NSAffineTransform.alloc().init()
	Transform.rotateByDegrees(angle)
	Transform.concat()
	
def scale(x, y = None):
	# Scale the art board by "x", "y", if "y" is not set the art board will be scaled proportionally.
	Transform = NSAffineTransform.alloc().init()
	if y is None:
		y = x
	Transform.scaleXBy_yBy_(x, y)
	Transform.concat()
	
def skew(a, b = None):
	# Skew the art board by "a", "b", if "b" is not set the art board will be skew with "a" = "b"
	Transform = NSAffineTransform.alloc().init()
	if b is None:
		b = a
	Transform.shearXBy_yBy_(a, b)
	Transform.concat()
	
def font(fontName, fontSize=None):
	# Set the font by PostScript name.
	# Optionally set the font size.
	if fontSize is None:
		fontSize = NSFont.systemFontSize()
	NSFont.fontWithName_size_(fontName, fontSize)
	
def fontSize(fontSize):
	# Set the font size.
	currentFont = NSFont.fontWithName_size_(currentFont.fontName(), fontSize)

def text(textString, pt):
	# Draw a text on position "x", "y".
	NSString.stringWithString_(textString).drawAtPoint_withAttributes_(NSMakePoint(pt[0], pt[1]), {NSFontAttributeName: currentFont, NSForegroundColorAttributeName:currentFillColor})
	
def image(image, pt, alpha=1):
	if type(image) == NSImage:
		image.drawAtPoint_fromRect_operation_fraction_(NSMakePoint(pt[0], pt[1]), NSZeroRect, NSCompositeSourceOver, 1)
		
def linearGradient(startPoint=None, endPoint=None, colors=None, locations=None):
	global currentGradient
	global currentFillColor
	if colors is None:
		colors = [NSColor.greenColor(), NSColor.redColor()]
	if locations is None:
		locations = [i / float(len(colors)-1) for i in range(len(colors))]
	currentGradient = ("linear", startPoint, endPoint, colors, locations)
	currentFillColor = None
	