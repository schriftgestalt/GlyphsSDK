#!/usr/bin/env python
from __future__ import print_function

from typing import List, Optional, Tuple

# from typing import Any, List, Dict, Optional
from AppKit import (  # type: ignore
	NSBezierPath,
	NSColor,
	NSColorSpace,
	NSCompositingOperationSourceOver,
	NSFont,
	NSFontAttributeName,
	NSForegroundColorAttributeName,
	NSGradient,
	NSGradientDrawsAfterEndingLocation,
	NSGradientDrawsBeforeStartingLocation,
	NSGraphicsContext,
	NSImage,
	NSLineCapStyleButt,
	NSLineCapStyleRound,
	NSLineCapStyleSquare,
	NSLineJoinStyleMiter,
	NSLineJoinStyleRound,
)
from Foundation import (
	NSAffineTransform,
	NSMakePoint,
	NSMakeRect,
	NSPoint,
	NSPointLike,
	NSString,
	NSZeroRect,
)


def save():
	# save the current graphic state
	NSGraphicsContext.saveGraphicsState()


def restore():
	# restore the current graphic state
	NSGraphicsContext.restoreGraphicsState()


currentPath: NSBezierPath | None = None
currentFillColor: NSColor | None = NSColor.blackColor()
currentStrokeColor: NSColor | None = None
currentGradient: Tuple[str, NSPoint, NSPoint, List[Tuple], list] | None = None
currentStrokeWidth: float | None = None
currentFont: NSFont = NSFont.systemFontOfSize_(NSFont.systemFontSize())


def rect(x: float, y: float, width: float, height: float):
	# draws a rectangle
	drawPath(NSBezierPath.bezierPathWithRect_(NSMakeRect(x, y, width, height)))


def oval(x: float, y: float, width: float, height: float):
	# draws an oval
	drawPath(NSBezierPath.bezierPathWithOvalInRect_(NSMakeRect(x, y, width, height)))


def line(x1: float, y1: float, x2: float | None = None, y2: float | None = None):
	# draws a line
	if x2 is None and y2 is None and isinstance(x1, tuple) and isinstance(y1, tuple):
		(x1, y1), (x2, y2) = x1, y1
	if x2 and y2:
		p = NSBezierPath.bezierPath()
		p.moveToPoint_(NSMakePoint(x1, y1))
		p.lineToPoint_(NSMakePoint(x2, y2))
		drawPath(p)


def newPath():
	# creates a new path
	global currentPath
	currentPath = NSBezierPath.bezierPath()


def moveTo(pt: NSPointLike):
	# move to point
	if currentPath is not None:
		currentPath.moveToPoint_(NSMakePoint(pt[0], pt[1]))


def lineTo(pt: NSPointLike):
	# line to point
	if currentPath is not None:
		currentPath.lineToPoint_(NSMakePoint(pt[0], pt[1]))


def curveTo(h1: NSPointLike, h2: NSPointLike, pt: NSPointLike):
	# curve to point with bcps
	if currentPath is not None:
		currentPath.curveToPoint_controlPoint1_controlPoint2_(NSMakePoint(pt[0], pt[1]), NSMakePoint(h1[0], h1[1]), NSMakePoint(h2[0], h2[1]))


def closePath():
	# close the path
	if currentPath is not None:
		currentPath.closePath()


def drawPath(path: Optional[NSBezierPath] = None):
	# draws the path
	if path is None:
		path = currentPath
	if path is None:
		return
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
				NSColors.append(NSColor.colorWithSRGBRed_green_blue_alpha_(r, g, b, a))
			else:
				NSColors.append(NSColor.colorWithGenericGamma22White_alpha_(r, a))
		gradient = NSGradient.alloc().initWithColors_atLocations_colorSpace_(NSColors, locations, NSColorSpace.deviceRGBColorSpace())
		if gradientType == "linear":
			gradient.drawFromPoint_toPoint_options_(startPoint, endPoint, NSGradientDrawsBeforeStartingLocation | NSGradientDrawsAfterEndingLocation)
		elif gradientType == "radial":
			pass
		restore()
	if currentStrokeWidth is not None:
		path.setLineWidth_(currentStrokeWidth)
	if currentStrokeColor is not None:
		currentStrokeColor.set()
		path.stroke()


def fill(r: float | None = None, g: float | None = None, b: float | None = None, a=1):
	# Set the fill color as RGB value.
	global currentFillColor
	global currentGradient
	if r is None:
		currentFillColor = None
	elif isinstance(r, NSColor):
		currentFillColor = r
	elif g is None:
		currentFillColor = NSColor.colorWithDeviceWhite_alpha_(r, a)
		currentGradient = None
	elif b is not None:
		currentFillColor = NSColor.colorWithDeviceRed_green_blue_alpha_(r, g, b, a)
		currentGradient = None


def stroke(r: float | None = None, g: float | None = None, b: float | None = None, a: float = 1):
	# Set the stroke color as RGB value.
	global currentStrokeColor
	if r is None:
		currentStrokeColor = None
	elif g is None:
		currentStrokeColor = NSColor.colorWithDeviceWhite_alpha_(r, a)
	elif b is not None:
		currentStrokeColor = NSColor.colorWithDeviceRed_green_blue_alpha_(r, g, b, a)


def strokeWidth(value: float):
	# Set the stroke width for a path.
	global currentStrokeWidth
	currentStrokeWidth = value
	if currentPath is not None:
		currentPath.setLineWidth_(value)


def miterLimit(value: int):
	# Set the miter limit for a path.
	if currentPath is not None:
		currentPath.setMiterLimit_(value)


def lineJoin(join: int):
	# Set the line join for a path, possible join arguments are: "bevel", "miter" or "round"
	if currentPath is not None:
		style = NSLineJoinStyleMiter
		if join == "bevel":
			style = NSLineJoinStyleMiter
		elif join == "round":
			style = NSLineJoinStyleRound
		currentPath.setLineJoinStyle_(style)


def lineCap(cap: int):
	if currentPath is not None:
		style = NSLineCapStyleButt
		if cap == "square":
			style = NSLineCapStyleSquare
		elif cap == "round":
			style = NSLineCapStyleRound
		currentPath.setLineCapStyle_(style)


def dashLine(dash):
	# dash is a list of of values
	pass


def translate(x: float, y: float):
	# Translate the art board pane to "x", "y"
	Transform = NSAffineTransform.alloc().init()
	Transform.translateXBy_yBy_(x, y)
	Transform.concat()


def rotate(angle: float):
	# Rotate the art board by an angle.
	Transform = NSAffineTransform.alloc().init()
	Transform.rotateByDegrees_(angle)
	Transform.concat()


def scale(x: float, y: float | None = None):
	# Scale the art board by "x", "y", if "y" is not set the art board will be scaled proportionally.
	Transform = NSAffineTransform.alloc().init()
	if y is None:
		y = x
	Transform.scaleXBy_yBy_(x, y)
	Transform.concat()


def skew(a: float, b: float | None = None):
	# Skew the art board by "a", "b", if "b" is not set the art board will be skew with "a" = "b"
	Transform = NSAffineTransform.alloc().init()
	if b is None:
		b = a
	Transform.shearXBy_yBy_(a, b)
	Transform.concat()


def font(fontName: str, fontSize: float | None = None):
	# Set the font by PostScript name.
	# Optionally set the font size.
	if fontSize is None:
		fontSize = NSFont.systemFontSize()
	NSFont.fontWithName_size_(fontName, fontSize)


def fontSize(fontSize: float):
	# Set the font size.
	global currentFont
	currentFont = NSFont.fontWithName_size_(currentFont.fontName(), fontSize)


def text(textString: str, pt: NSPointLike):
	# Draw a text on position "x", "y".
	NSString.stringWithString_(textString).drawAtPoint_withAttributes_(NSMakePoint(pt[0], pt[1]), {
		NSFontAttributeName: currentFont,
		NSForegroundColorAttributeName: currentFillColor
	})


def image(image: NSImage, pt: NSPointLike, alpha: float = 1):
	if isinstance(image, NSImage):
		image.drawAtPoint_fromRect_operation_fraction_(NSMakePoint(pt[0], pt[1]), NSZeroRect, NSCompositingOperationSourceOver, alpha)


def linearGradient(startPoint: NSPointLike, endPoint: NSPointLike, colors: list[NSColor] | None = None, locations: list | None = None):
	global currentGradient
	global currentFillColor
	if colors is None:
		colors = [NSColor.greenColor(), NSColor.redColor()]
	if locations is None:
		locations = [i / float(len(colors) - 1) for i in range(len(colors))]
	currentGradient = ("linear", startPoint, endPoint, colors, locations)  # type: ignore XXX
	currentFillColor = None
