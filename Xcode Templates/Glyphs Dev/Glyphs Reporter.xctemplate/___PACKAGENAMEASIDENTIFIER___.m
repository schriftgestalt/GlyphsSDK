//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//___COPYRIGHT___
//

#import "___FILEBASENAME___.h"
#import <GlyphsCore/GlyphsFilterProtocol.h>
#import <GlyphsCore/GSFilterPlugin.h>
#import <GlyphsCore/GSGlyph.h>
#import <GlyphsCore/GSLayer.h>
#import <GlyphsCore/GSFont.h>
#import <GlyphsCore/GSFontMaster.h>
#import <GlyphsCore/GSComponent.h>

@implementation ___FILEBASENAMEASIDENTIFIER___  {
	NSViewController <GSGlyphEditViewControllerProtocol> *_editViewController;
}

- (instancetype)init {
	self = [super init];
	if (self) {
		// do stuff
	}
	return self;
}

- (NSUInteger)interfaceVersion {
	// Distinguishes the API version the plugin was built for. Return 1.
	return 1;
}

- (NSString *)title {
	// This is the name as it appears in the menu in combination with 'Show'.
	// E.g. 'return @"Nodes";' will make the menu item read "Show Nodes".
	return NSLocalizedStringFromTableInBundle(@"___PACKAGENAME___", nil, [NSBundle bundleForClass:[self class]], @"DESCRIPTION");
}

- (NSString *)keyEquivalent {
	// The key for the keyboard shortcut. Set modifier keys in modifierMask further below.
	// Pretty tricky to find a shortcut that is not taken yet, so be careful.
	// If you are not sure, use 'return nil;'. Users can set their own shortcuts in System Prefs.
	return nil;
}

- (NSEventModifierFlags)modifierMask {
	// Use any combination of these to determine the modifier keys for your default shortcut:
	// return NSShiftKeyMask | NSControlKeyMask | NSCommandKeyMask | NSAlternateKeyMask;
	// Or:
	// return 0;
	// ... if you do not want to set a shortcut.
	return 0;
}


- (void)drawForegroundForLayer:(GSLayer *)layer options:(NSDictionary *)options {
	// Whatever you draw here will be displayed IN FRONT OF the paths.
	// To get an NSBezierPath from a GSPath, use the bezierPath method:
	//  [[myPath bezierPath] fill];
	// You can apply that to a full layer at once:
	// [layer bezierPath];	   # all closed paths
	// [layer openBezierPath];   # all open paths

	NSRect rect = [layer bounds];
	[[NSColor blueColor] set];
	[NSBezierPath fillRect:rect];
}


- (void)drawBackgroundForLayer:(GSLayer*)layer options:(NSDictionary *)options {
	// Whatever you draw here will be displayed BEHIND the paths.
	
}

- (void)drawBackgroundForInactiveLayer:(GSLayer*)layer options:(NSDictionary *)options {
	// Whatever you draw here will be displayed behind the paths, but for inactive masters.
	
}

- (BOOL)needsExtraMainOutlineDrawingForInactiveLayer:(GSLayer*)layer {
	// Return NO to disable the black outline. Otherwise remove the method.
	return NO;
}

- (float)getScale {
	// [self getScale]; returns the current scale factor of the Edit View UI.
	// Divide any scalable size by this value in order to keep the same apparent pixel size.
	
	if (_editViewController) {
		return _editViewController.graphicView.scale;
	} else {
		return 1.0;
	}
}

- (void)setController:(NSViewController <GSGlyphEditViewControllerProtocol>*)controller {
	// Use [self controller]; as object for the current view controller.
	_editViewController = controller;
}

@end
