//
//  InspectorDemo.m
//  InspectorDemo
//
//  Created by Georg Seifert on 19.12.16.
//  Copyright © 2016 Georg Seifert. All rights reserved.
//

#import "InspectorDemo.h"
#import "InspectorDemoViewController.h"

#import <GlyphsCore/GSLayer.h>

static NSImage *_toolBarIcon = nil;

@implementation InspectorDemo

- (id) init {
	self = [super init];
	NSBundle * thisBundle = [NSBundle bundleForClass:[self class]];
	if (thisBundle) {
		// The toolbar icon:
		_toolBarIcon = [[NSImage alloc] initWithContentsOfFile:[thisBundle pathForImageResource: @"ToolbarIconTemplate"]];
		[_toolBarIcon setTemplate:YES];
	}
	return self;
}

- (NSUInteger) interfaceVersion {
	// Distinguishes the API verison the plugin was built for. Return 1.
	return 1;
}

- (NSUInteger) groupID {
	// Return a number between 50 and 1000 to position the icon in the toolbar.
	return 50;
}

- (NSString*) title {
	//return the name of the tool as it will appear in the tooltip of in the toolbar.
	return @"InspectorDemo";
}

- (NSString*) trigger {
	// Return the key that the user can press to activate the tool.
	// Please make sure to not conflict with other tools.
	return @"h";
}

- (NSInteger) tempTrigger {
	// Return a modifierMask (e.g NSAlternateKeyMask, NSCommandKeyMask ...)
	return 0;
}

#if 0
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
	NSMenu *theMenu = [[ NSMenu alloc] initWithTitle:@"Contextual Menu" ];
	[ theMenu addItemWithTitle:@"Foo" action:@selector(foo:) keyEquivalent:@"" ];
	[ theMenu addItemWithTitle:@"Bar" action:@selector(bar:) keyEquivalent:@"" ];
	return theMenu;
}

- (void)addMenuItemsForEvent:(NSEvent *)theEvent toMenu:(NSMenu *)theMenu {
	// Adds an item to theMenu for theEvent.
	[ theMenu insertItemWithTitle:@"Wail" action:@selector(wail:) keyEquivalent:@"" atIndex:[theMenu numberOfItems]-1 ];
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

- (void)drawBackground {
	// Draw in the background, concerns the complete view.
}

- (void)drawForeground {
	// Draw in the foreground, concerns the complete view.
}

- (void) drawLayer:(GSLayer*)Layer atPoint:(NSPoint)aPoint asActive:(BOOL)Active attributes:(NSDictionary*)Attributes {
	// Draw anythin for this particular layer.
	[_editViewController.graphicView drawLayer:Layer atPoint:aPoint asActive:Active attributes:Attributes];
}

- (void) willActivate {
	// Called when the tool is selected by the user.
	// editViewController.graphicView.cursor = [NSCursor openHandCursor];
}

- (void) willDeactivate {}
#endif

- (NSArray *)inspectorViewControllers {
	NSMutableArray *inspectors = (NSMutableArray*)[super inspectorViewControllers];
	if (!inspectors) {
		inspectors = [NSMutableArray new];
	}
	GSInspectorViewController *inspector = nil;
	GSLayer* layer = _editViewController.graphicView.activeLayer;
	if (layer) {
		if (!_inspectorViewControllers) {
			_inspectorViewControllers = [[NSMutableDictionary alloc] init];
		}
		//NSLog(@"one Glyph selected");

		inspector = _inspectorViewControllers[@"InspectorDemoViewController"];
		if (!inspector) {
			inspector = [[InspectorDemoViewController alloc] init];
			[inspector view];
			_inspectorViewControllers[@"InspectorDemoViewController"] = inspector;
		}
		if (inspector) {
			[inspectors addObject:inspector];
			NSString* title = nil;
			if (layer.countOfSelection > 0) {
				id firstObject = [layer.selection firstObject];
				title = [firstObject className];
			}
			if (!title) {
				title = @"nothing selected";
			}
			inspector.representedObject = title;
		}
	}
	return inspectors;
}
@end
