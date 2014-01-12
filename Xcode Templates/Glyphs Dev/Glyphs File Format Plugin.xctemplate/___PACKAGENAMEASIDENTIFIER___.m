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

@implementation GlyphsFileFormat___FILEBASENAMEASIDENTIFIER___

@synthesize exportSettingsView = _exportSettingsView;
@synthesize font = _font;
@synthesize progressWindow = _progressWindow;

- (id)init {
	self = [super init];
	[NSBundle loadNibNamed:@"___FILEBASENAMEASIDENTIFIER___Dialog" owner:self];
	NSBundle * thisBundle = [NSBundle bundleForClass:[self class]];
	_toolbarIcon = [[NSImage alloc] initWithContentsOfFile:[thisBundle pathForImageResource: @"ExportIcon"]];
	[_toolbarIcon setName: @"ExportIcon"];
	return self;
}

- (NSUInteger) interfaceVersion {
	// Distinguishes the API verison the plugin was built for. Return 1.
	return 1;
}

- (NSString*) toolbarTitle {
	// Return the name of the tool as it will appear in export dialog.
	return @"___PACKAGENAME___";
}

- (NSUInteger) groupID {
	// Position in the export panel. Higher numbers move it to the right.
	return 10;
}

- (GSFont*) fontFromURL:(NSURL*)URL ofType:(NSString*)typeName error:(NSError**)error {
	// Load the font at URL and return a GSFont object.
	return nil;
}

- (BOOL) writeFont:(GSFont*)Font error:(NSError**)error {
	// Write Font to disk. You have to ask for the path yourself. This is called from the export dialog.
	// Return YES on sucess, NO otherwise and add some infomation about the problem to 'error'). 
	return NO;
}

- (BOOL) writeFont:(GSFont*)Font toURL:(NSURL*)DestinationURL error:(NSError**)error {
	// Write Font to DestinationURL.
	// Return YES on sucess, NO otherwise and add some infomation about the problem to 'error').
	return NO;
}

@end
