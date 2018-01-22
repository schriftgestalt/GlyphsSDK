//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//  ___COPYRIGHT___
//

#import "___PACKAGENAMEASIDENTIFIER___.h"
#import <GlyphsCore/GSFont.h>
#import <GlyphsCore/GSFontMaster.h>
#import <GlyphsCore/GSGlyph.h>
#import <GlyphsCore/GSLayer.h>
#import <GlyphsCore/GSPath.h>

@interface NSBundle (NibLoading)
+ (NSArray *)loadNibNamed:(NSString *)nibName owner:(id)owner error:(NSError **)error;
@end

@implementation ___FILEBASENAMEASIDENTIFIER___

@synthesize windowController;

- (id) init {
	self = [super init];
	[NSBundle loadNibNamed:@"___PACKAGENAMEASIDENTIFIER___View" owner:self error:nil];
	return self;
}

- (NSUInteger) interfaceVersion {
	// Distinguishes the API verison the plugin was built for. Return 1.
	return 1;
}

- (NSString*) title {
	// Return the name of the tool as it will appear in the menu.
	return @"___PACKAGENAME___";
}

- (NSInteger) maxHeight {
	return 265;
}
- (NSInteger) minHeight {
	return 125;
}
- (NSUInteger) currentHeight {
	return [[NSUserDefaults standardUserDefaults] integerForKey:@"___PACKAGENAMEASIDENTIFIER___CurrentHeight"];
}
@end
