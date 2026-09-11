//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//  ___COPYRIGHT___
//

#import "___PACKAGENAMEASIDENTIFIER___.h"
#import <GlyphsApp/GSPaletteView.h>

@implementation ___FILEBASENAMEASIDENTIFIER___

@synthesize windowController;

- (instancetype)init {
	self = [super initWithNibName:@"___PACKAGENAMEASIDENTIFIER___View" bundle:[NSBundle bundleForClass:[self class]]];
	[(GSPaletteView *)self.view setController:self];
	return self;
}

- (NSUInteger)interfaceVersion {
	// Distinguishes the API version the plugin was built for. Return 1.
	return 1;
}

- (NSString *)title {
	// Return the name of the tool as it will appear in the menu.
	return @"___PACKAGENAME___";
}

- (NSInteger)minHeight {
	return 85;
}

- (NSInteger)maxHeight {
	return 265; // if this is bigger than minHeight, the palette is resizable
}

- (NSUInteger)currentHeight {
	return [NSUserDefaults.standardUserDefaults integerForKey:@"___PACKAGENAMEASIDENTIFIER___CurrentHeight"];
}

- (void)setCurrentHeight:(NSUInteger)newHeight {
	if (newHeight >= [self minHeight] && newHeight <= [self maxHeight]) {
		[NSUserDefaults.standardUserDefaults setInteger:newHeight forKey:@"___PACKAGENAMEASIDENTIFIER___CurrentHeight"];
	}
}

- (NSView *)theView {
	return [self view];
}

@end
