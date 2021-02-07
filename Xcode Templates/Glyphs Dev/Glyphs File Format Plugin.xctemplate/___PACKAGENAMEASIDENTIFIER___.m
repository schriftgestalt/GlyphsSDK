//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//___COPYRIGHT___
//

#import "___FILEBASENAME___.h"
#import <GlyphsCore/GlyphsFilterProtocol.h>
#import <GlyphsCore/GSFont.h>

@implementation ___FILEBASENAMEASIDENTIFIER___ {
	NSImage *_toolbarIcon;
}

@synthesize font = _font;

- (instancetype)init {
	NSBundle *bundle = [NSBundle bundleForClass:[self class]];
	self = [super initWithNibName:@"___FILEBASENAMEASIDENTIFIER___Dialog" bundle:bundle];
	
	_toolbarIcon = [[NSImage alloc] initWithContentsOfFile:[bundle pathForImageResource: @"GenericExportTemplate"]];
	[_toolbarIcon setName: @"___FILEBASENAMEASIDENTIFIER___Icon"];
	return self;
}

- (NSUInteger)interfaceVersion {
	// Distinguishes the API verison the plugin was built for. Return 1.
	return 1;
}

- (NSString*)toolbarTitle {
	// Return the name of the tool as it will appear in export dialog.
	return @"___PACKAGENAME___";
}

- (NSString *)toolbarIconName {
	return @"___FILEBASENAMEASIDENTIFIER___Icon";
}

- (NSUInteger)groupID {
	// Position in the export panel. Higher numbers move it to the right.
	return 10;
}

- (NSView *)exportSettingsView {
	return [self view];
}

- (GSFont *)fontFromURL:(NSURL *)URL ofType:(NSString *)typeName error:(out NSError **)error {
	// Load the font at URL and return a GSFont object.
	return nil;
}

- (BOOL)writeFont:(GSFont *)Font error:(NSError **)error {
	// Write Font to disk. You have to ask for the path yourself. This is called from the export dialog.
	// Return YES on sucess, NO otherwise and add some infomation about the problem to 'error'). 
	return NO;
}

- (BOOL)writeFont:(GSFont *)font toURL:(NSURL *)destinationURL error:(out NSError **)error {
	// Write Font to DestinationURL.
	// Return YES on sucess, NO otherwise and add some infomation about the problem to 'error').
	return NO;
}

- (void)exportFont:(GSFont *)font {
	// Exprts a Font object.
	// This function should ask the user for the place to save the store the font.
 	// Eventually errors have to be presented by the plugin. Use `[font.parent presentError:error];`
}

@end
