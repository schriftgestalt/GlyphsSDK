//
//  Plugin_With_Window.h
//  Plugin With Window
//
//  Created by Mark Frömberg on 24.02.22.
//
//

#import <Cocoa/Cocoa.h>

#import <GlyphsCore/GlyphsPluginProtocol.h>

@interface PluginWithWindow : NSWindowController <GlyphsPlugin>

@property (strong) IBOutlet NSTextFieldCell *fontNameLabel;

@end
