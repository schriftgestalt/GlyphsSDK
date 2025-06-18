//
//  Plugin_With_Window.m
//  Plugin With Window
//
//  Created by Mark Frömberg on 24.02.22.
//
//

#import <GlyphsCore/GSFont.h>
#import <GlyphsCore/GSWindowControllerProtocol.h>
#import "PluginWithWindow.h"

static void *DocumentBindingContext = (void *)@"Document";
static NSString *ShowPluginWindowKey = @"XYShowMyPluginWindow"; /// Use your own prefix instead of `XY`

@protocol GSApplicationPluginProtocol <NSObject>

- (NSArray *)fontDocuments;

- (GSDocument *)currentFontDocument;

@end

@interface GSDocument : NSObject

- (GSFont *)font;

- (NSWindowController<GSWindowControllerProtocol> *)windowController;

@end

@implementation PluginWithWindow {
	BOOL _hasRegisteredObservers;
	GSFont *__weak _currentFont;
	NSViewController<GSGlyphEditViewControllerProtocol> *__weak _currentEditViewController;
}

- (NSUInteger)interfaceVersion {
	// Distinguishes the API version the plugin was built for. Return 1.
	return 1;
}

- (instancetype)init {
	self = [super initWithWindowNibName:@"MyPluginWindow"];
	if (self) {
		[self window];
	}
	return self;
}

- (NSString *)title {
	return @"Plugin With Window";
}

- (void)loadPlugin {
	NSMenu *mainMenu = [[NSApplication sharedApplication] mainMenu];
	NSMenuItem *newMenuItem = [[NSMenuItem alloc] initWithTitle:[self title] action:@selector(showMyPluginWindow:) keyEquivalent:@""];
	newMenuItem.target = self;
	NSMenu *submenu = [[mainMenu itemWithTag:17] submenu];
	[submenu addItem:newMenuItem];
	
	if ([[NSUserDefaults standardUserDefaults] boolForKey:ShowPluginWindowKey]) {
		[self showMyPluginWindow:nil];
	}
}

- (void)awakeFromNib {
	self.fontNameLabel.stringValue = @"No Font Open";
	self.window.title = [NSString stringWithFormat:@"%@", self.title];
	self.window.level = NSFloatingWindowLevel;
}

- (void)dealloc {
	[self removeNotifications];
}

- (void)_updateDoc {
	NSApplication<GSApplicationPluginProtocol> *app = NSApp;
	GSDocument *Doc = [app currentFontDocument];
	if (Doc.font == _currentFont) return;
	[self setCurrentFont:Doc.font];
	self.fontNameLabel.stringValue = _currentFont.fontName;
	self.window.title = [NSString stringWithFormat:@"%@: %@", self.title, _currentFont.fontName];
	/// Optionally call update methods of your plugin here.
}


- (void)observeValueForKeyPath:(NSString *)keyPath
					  ofObject:(id)object
						change:(NSDictionary *)change
					   context:(void *)context {
	
	if (context == DocumentBindingContext) {
		[self performSelector:@selector(_updateDoc) withObject:nil afterDelay:0.0];
	}
}

- (void)setUpNotifications {
	if (!_hasRegisteredObservers) {
		[NSApp addObserver:self forKeyPath:@"mainWindow.windowController.document" options:1 context:DocumentBindingContext];
		_hasRegisteredObservers = YES;
	}
}

- (void)removeNotifications {
	if (_hasRegisteredObservers) {
		[NSApp removeObserver:self forKeyPath:@"mainWindow.windowController.document"];
		_hasRegisteredObservers = NO;
	}
}

- (IBAction)showMyPluginWindow:(id)sender {
	if ([[self window] isVisible]) {
		[[NSUserDefaults standardUserDefaults] setBool:NO forKey:ShowPluginWindowKey];
		[self.window orderOut:sender];
		[self removeNotifications];
	}
	else {
		[[NSUserDefaults standardUserDefaults] setBool:YES forKey:ShowPluginWindowKey];
		[self.window makeKeyAndOrderFront:sender];
		[self setUpNotifications];
	}
}


- (void)setCurrentFont:(GSFont *)currentFont {
	if (_currentFont != currentFont) {
		_currentFont = currentFont;
	}
}

#pragma mark window delegate

- (BOOL)windowShouldClose:(id)window {
	if (self.window == window) {
		[[NSUserDefaults standardUserDefaults] setBool:NO forKey:ShowPluginWindowKey];
		[self removeNotifications];
	}
	return YES;
}

@end
