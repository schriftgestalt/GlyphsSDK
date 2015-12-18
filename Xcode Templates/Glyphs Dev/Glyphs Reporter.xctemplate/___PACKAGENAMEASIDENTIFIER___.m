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
// #import "GSEditViewController.h"
// #import "GSWindowController.h"
#import <GlyphsCore/GSComponent.h>

@implementation ___FILEBASENAMEASIDENTIFIER___

- (id) init {
	self = [super init];
	if (self) {
		// do stuff
	}
	return self;
}

- (void) loadPlugin {
    // Is called when the plugin is loaded.
    
}


- (NSUInteger) interfaceVersion {
	// Distinguishes the API verison the plugin was built for. Return 1.
	return 1;
}

- (NSString*) title {
	// This is the name as it appears in the menu in combination with 'Show'.
    // E.g. 'return @"Nodes";' will make the menu item read "Show Nodes".
	return @"___PACKAGENAME___";
    
    // or localise it:
    // return NSLocalizedStringFromTableInBundle(@"TITLE", nil, [NSBundle bundleForClass:[self class]], @"DESCRIPTION");
}

- (NSString*) keyEquivalent {
	// The key for the keyboard shortcut. Set modifier keys in modifierMask further below.
    // Pretty tricky to find a shortcut that is not taken yet, so be careful.
    // If you are not sure, use 'return nil;'. Users can set their own shortcuts in System Prefs.
	return nil;
}

- (int) modifierMask {
    // Use any combination of these to determine the modifier keys for your default shortcut:
    // return NSShiftKeyMask | NSControlKeyMask | NSCommandKeyMask | NSAlternateKeyMask;
    // Or:
    // return 0;
    // ... if you do not want to set a shortcut.
    return 0;
}


- (void) drawForegroundForLayer:(GSLayer*)Layer {
    // Whatever you draw here will be displayed IN FRONT OF the paths.
    // To get an NSBezierPath from a GSPath, use the bezierPath method:
    //  [[myPath bezierPath] fill];
    // You can apply that to a full layer at once:
    // [myLayer bezierPath];       # all closed paths
    // [myLayer openBezierPath];   # all open paths

    NSRect Rect = [Layer bounds];
    [[NSColor blueColor] set];
    [NSBezierPath fillRect:Rect];
}


- (void) drawBackgroundForLayer:(GSLayer*)Layer {
    // Whatever you draw here will be displayed BEHIND the paths.
    
}

- (void) drawBackgroundForInactiveLayer:(GSLayer*)Layer {
    // Whatever you draw here will be displayed behind the paths, but for inactive masters.
    
}

- (BOOL) needsExtraMainOutlineDrawingForInactiveLayer:(GSLayer*)Layer {
    // Return NO to disable the black outline. Otherwise remove the method.
    return NO;
}

- (float) getScale {
    // [self getScale]; returns the current scale factor of the Edit View UI.
    // Divide any scalable size by this value in order to keep the same apparent pixel size.
    
    if (editViewController) {
        return [[editViewController graphicView] scale];
    } else {
        return 1.0;
    }
}

- (void) setController:(NSViewController <GSGlyphEditViewControllerProtocol>*)Controller {
    // Use [self controller]; as object for the current view controller.
    editViewController = Controller;
}

- (void) logToConsole:(NSString*)message {
    // The NSString 'message' will be passed to Console.app.
    // Use [self logToConsole:@"bla bla"]; for debugging.
    NSLog( @"Show %@ plugin:\n%@", [self title], message );
}

@end
