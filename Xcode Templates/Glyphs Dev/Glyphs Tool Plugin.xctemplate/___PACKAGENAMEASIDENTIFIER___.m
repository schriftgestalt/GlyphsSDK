//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//___COPYRIGHT___
//

#import "___FILEBASENAME___.h"

@implementation ___FILEBASENAMEASIDENTIFIER___

- (id)init {
	self = [super init];
	NSBundle * thisBundle = [NSBundle bundleForClass:[self class]];
	if (thisBundle) {
		_toolBarIcon = [[NSImage alloc] initWithContentsOfFile:[thisBundle pathForImageResource: @"ToolbarIconTemplate"]];
		[_toolBarIcon setTemplate:YES];
	}
	return self;
}

- (NSUInteger) interfaceVersion {
	// to distinguish the API verison the plugin was build for. Return 1.
	return 1;
}

- (NSUInteger) groupID {
	// return a number between 50 and 1000 to position the icon in the toolbar.
	return 50;
}

- (NSString *) title {
	//return the name of the tool as it will appear in the tooltip of in the toolbar.
	return @"___PACKAGENAME___";
}

- (NSString *) trigger {
	// return the key that the user can press to activate the tool. Please make sure to not conflikct with other tools.
	return @"h";
}

- (NSInteger) tempTrigger {
	// return a modifierMask (e.g NSAlternateKeyMask, NSCommandKeyMask ...)
	return 0;
}

- (BOOL) willSelectTempTool:(id) tempTool {
	// this is called if the user presses any modifier key like the cmd key to swith to the select tool. return NO to prevent the tool switching.
	return YES;
}

- (void) keyDown:(NSEvent *) theEvent {
	NSLog(@"keyDown: %@", theEvent);
}

- (void) doCommandBySelector: (SEL)aSelector {
	NSLog(@"aSelector: %s", sel_getName(aSelector));
}

- (NSMenu*) defaultContextMenu {
	NSMenu *theMenu = [[NSMenu alloc] initWithTitle:@"Contextual Menu"];
	[theMenu addItemWithTitle:@"Foo" action:@selector(foo:) keyEquivalent:@""];
	[theMenu addItemWithTitle:@"Bar" action:@selector(bar:) keyEquivalent:@""];
	return theMenu;
}

- (void) addMenuItemsForEvent:(NSEvent*) theEvent toMenu:(NSMenu*) theMenu {
	[theMenu insertItemWithTitle:@"Wail" action:@selector(wail:) keyEquivalent:@"" atIndex:[theMenu numberOfItems]-1];
}

- (void)mouseDown:(NSEvent *) theEvent {
	editViewController = [windowController activeEditViewController];
	//editViewController.graphicView.cursor = [NSCursor closedHandCursor];
	_draggStart = [theEvent locationInWindow];
}

- (void)mouseDragged:(NSEvent *) theEvent{
	NSPoint Loc = [theEvent locationInWindow];
	NSLog(@"__mouse dragged to : %@", NSStringFromPoint(Loc));
}

- (void)mouseUp:(NSEvent *) theEvent{
	//editViewController.graphicView.cursor = [NSCursor openHandCursor];
}

- (void) drawBackground {
	// draw anything concerning the hole view.
}

- (void) drawForeground {
	// draw anything concerning the hole view.
}

- (void) drawLayer:(GSLayer *) Layer atPoint:(NSPoint) aPoint asActive:(BOOL) Active attributes:(NSDictionary*) Attributes {
	// draw anything concerning this particular layer.
	[editViewController.graphicView drawLayer:Layer atPoint:aPoint asActive:Active attributes: Attributes];
}

- (void) willActivate {
	//editViewController.graphicView.cursor = [NSCursor openHandCursor];
}

- (void) willDeactivate {}

@end
