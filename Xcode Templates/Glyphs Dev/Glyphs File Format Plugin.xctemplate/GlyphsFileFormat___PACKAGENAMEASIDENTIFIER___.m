//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//___COPYRIGHT___
//

#import "GlyphsFileFormat___FILEBASENAME___.h"
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
	_toolbarIcon = [[NSImage alloc] initWithContentsOfFile:[thisBundle pathForImageResource: @"___FILEBASENAMEASIDENTIFIER___"]];
	return self;
}

- (NSUInteger) interfaceVersion {
	// to distinguish the API verison the plugin was build for. Return 1.
	return 1;
}
- (NSString *) title {
	//return the name of the tool as it will appear in the menu.
	return @"___PACKAGENAME___";
}
- (NSUInteger) groupID {
	//position in the export panel
	return 10;
}
- (GSFont*) fontFromURL:(NSURL *) URL ofType:(NSString*)typeName error:(NSError**)error {
	//load the font at URL and return a GSFont object
	return nil;
}
- (BOOL) writeFont:(GSFont *) Font error:(NSError**)error {
	// write the font to disk. You have to ask for the path yourself. This is called from the export dialog
	// return YES on sucess, NO otherwise
}
- (BOOL) writeFont:(GSFont*) Font toURL:(NSURL*) DestinationURL error:(NSError**) error {
	// write the font to disk at the location of the DestinationURL.
	// return YES on sucess, NO otherwise
}
@end
