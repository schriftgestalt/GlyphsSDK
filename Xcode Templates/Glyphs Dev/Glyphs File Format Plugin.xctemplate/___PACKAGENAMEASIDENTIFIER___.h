//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//___COPYRIGHT___
//

#import <Cocoa/Cocoa.h>
#import <GlyphsCore/GlyphsFileFormatProtocol.h>

@class GSFont;
@class GSProgressWindow;

@interface GlyphsFileFormat___FILEBASENAMEASIDENTIFIER___ : NSObject <GlyphsFileFormat> {
	NSImage*			_toolbarIcon;
	IBOutlet NSView*	_exportSettingsView;
	GSFont*				__unsafe_unretained _font;
}
@property(readonly) NSView *exportSettingsView;
@property(unsafe_unretained) GSFont *font;
@property(readonly) GSProgressWindow *progressWindow;

@end
