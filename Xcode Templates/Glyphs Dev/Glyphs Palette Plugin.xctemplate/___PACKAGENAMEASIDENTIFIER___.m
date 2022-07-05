//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//  ___COPYRIGHT___
//

#import "___PACKAGENAMEASIDENTIFIER___.h"

@implementation ___FILEBASENAMEASIDENTIFIER___

@synthesize windowController;

- (id) init {
	self = [super initWithNibName:@"___PACKAGENAMEASIDENTIFIER___View" bundle:[NSBundle bundleForClass:[self class]]];
	return self;
}

- (NSUInteger)interfaceVersion {
	// Distinguishes the API verison the plugin was built for. Return 1.
	return 1;
}

- (NSString *)title {
	// Return the name of the tool as it will appear in the menu.
	return @"___PACKAGENAME___";
}

- (NSInteger)maxHeight {
	return 265;
}

- (NSInteger)minHeight {
	return 125;
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
