//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//___COPYRIGHT___
//

#import <Cocoa/Cocoa.h>
#import <GlyphsCore/GlyphsReporterProtocol.h>
#import <GlyphsCore/GlyphsPluginProtocol.h>
#import <GlyphsCore/GSGlyphViewControllerProtocol.h>

@interface ___FILEBASENAMEASIDENTIFIER___ : NSObject <GlyphsReporter, GlyphsPlugin> {
    NSViewController *editViewController;
}

@property (nonatomic) NSViewController <GSGlyphEditViewControllerProtocol>* controller;

@end
