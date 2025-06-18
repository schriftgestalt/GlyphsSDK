//
//  CustomParameterUI.m
//  CustomParameterUI
//
//  Created by Georg Seifert on 24.06.20.
//Copyright © 2020 Glyphs. All rights reserved.
//

#import "CustomParameterUI.h"
#import "CustomParameterUIValueViewController.h"
#import "CustomParameterUISheetController.h"

#import <GlyphsCore/GSCallbackHandler.h>

@implementation CustomParameterUI

+ (void)initialize {
	static dispatch_once_t onceToken;
	dispatch_once(&onceToken, ^{
		[GSCallbackHandler addCustomParameterViewClass:[CustomParameterUIValueViewController class] forParameter:@"TestParameter"];
		[GSCallbackHandler addCustomParameterSheetController:[CustomParameterUISheetController class] forParameter:@"TestMultiParameter"];
	});
}

- (id) init {
	self = [super init];
	if (self) {
		// do stuff
	}
	return self;
}

- (NSUInteger) interfaceVersion {
	// Distinguishes the API version the plugin was built for. Return 1.
	return 1;
}

- (void) loadPlugin {
	// Set up stuff
}

@end
