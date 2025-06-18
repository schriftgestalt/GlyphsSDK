//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//  ___COPYRIGHT___
//

#import "___FILEBASENAME___.h"

static NSImage *_toolBarIcon = nil;

@implementation ___FILEBASENAMEASIDENTIFIER___

- (instancetype)init {
	self = [super init];
	NSBundle *bundle = [NSBundle bundleForClass:[self class]];
	if (bundle) {
		// The toolbar icon:
		_toolBarIcon = [[NSImage alloc] initWithContentsOfFile:[bundle pathForImageResource:@"ToolbarIconTemplate"]];
		_toolBarIcon.template = YES;
	}
	return self;
}

- (NSUInteger)interfaceVersion {
	// Distinguishes the API version the plugin was built for. Return 1.
	return 1;
}

- (NSUInteger)groupID {
	// Return a number between 50 and 1000 to position the icon in the toolbar.
	return 50;
}

- (NSString *)title {
	// return the name of the tool as it will appear in the tooltip of in the toolbar.
	return @"___PACKAGENAME___";
}

- (NSString *)trigger {
	// Return the key that the user can press to activate the tool.
	// Please make sure to not conflict with other tools.
	return @"h";
}

- (NSEventModifierFlags)tempTrigger {
	// Return a modifierMask (e.g NSAlternateKeyMask, NSCommandKeyMask ...)
	return 0;
}

- (BOOL)willSelectTempTool:(id)tempTool {
	// This is called when the user presses a modifier key (e.g. the cmd key to swith to the Select Tool).
	// Return NO to prevent the tool switching.
	return YES;
}

- (void)keyDown:(NSEvent *)theEvent {
	// Called when a key is pressed while the tool is active.
	NSLog(@"keyDown: %@", theEvent);
}

- (void)doCommandBySelector:(SEL)aSelector {
	NSLog(@"aSelector: %s", sel_getName(aSelector));
}

- (NSMenu *)defaultContextMenu {
	// Adds items to the context menu.
	NSMenu *theMenu = [[NSMenu alloc] initWithTitle:@"Contextual Menu"];
	[theMenu addItemWithTitle:@"Foo" action:@selector(foo:) keyEquivalent:@""];
	[theMenu addItemWithTitle:@"Bar" action:@selector(bar:) keyEquivalent:@""];
	return theMenu;
}

- (void)addMenuItemsForEvent:(NSEvent *)theEvent toMenu:(NSMenu *)theMenu {
	// Adds an item to theMenu for theEvent.
	[theMenu insertItemWithTitle:@"Wail" action:@selector(wail:) keyEquivalent:@"" atIndex:[theMenu numberOfItems] - 1];
}

- (void)mouseDown:(NSEvent *)theEvent {
	// Called when the mouse button is clicked.
	_editViewController = [_windowController activeEditViewController];
	// editViewController.graphicView.cursor = [NSCursor closedHandCursor];
	_draggStart = [theEvent locationInWindow];
}

- (void)mouseDragged:(NSEvent *)theEvent {
	// Called when the mouse is moved with the primary button down.
	NSPoint loc = [theEvent locationInWindow];
	NSLog(@"__mouse dragged to : %@", NSStringFromPoint(loc));
}

- (void)mouseUp:(NSEvent *)theEvent {
	// Called when the primary mouse button is released.
	// editViewController.graphicView.cursor = [NSCursor openHandCursor];
}

- (void)drawBackgroundInRect:(NSRect)dirtyRect {
	// Draw in the background, concerns the complete view.
}

- (void)drawForegroundInRect:(NSRect)dirtyRect {
	// Draw in the foreground, concerns the complete view.
}

- (void)drawLayer:(GSLayer *)layer atPoint:(NSPoint)point asActive:(BOOL)active attributes:(NSDictionary *)attributes {
	// Draw anythin for this particular layer.
	[_editViewController.graphicView drawLayer:Layer atPoint:point asActive:active attributes:attributes];
}

- (void)willActivate {
	// Called when the tool is selected by the user.
	// editViewController.graphicView.cursor = [NSCursor openHandCursor];
}

- (void)willDeactivate {}

@end
