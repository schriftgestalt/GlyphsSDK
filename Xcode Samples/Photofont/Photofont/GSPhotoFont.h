//
//  GSPhotoFont.h
//  GSPhotoFont
//
//  Created by Georg Seifert on 30.07.10.
//  Copyright 2010 schriftgestaltung.de. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import <GlyphsCore/GlyphsFileFormatProtocol.h>

@class GSProgressWindow;

@interface GSPhotoFont : NSObject <GlyphsFileFormat> {
	NSView *__unsafe_unretained _exportSettingsView;
	GSFont *__unsafe_unretained _font;
	GSProgressWindow *__unsafe_unretained _progressWindow;
	NSImage *_toolbarIcon;
	NSInteger _sheetResult;
}
@property(readonly, unsafe_unretained) NSView *exportSettingsView;
@property(unsafe_unretained) GSFont *font;
@property(readonly, unsafe_unretained) GSProgressWindow *progressWindow;
@property(atomic, assign) NSInteger sheetResult;
@end
