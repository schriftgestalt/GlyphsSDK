//
//  CustomParameterUISheetController.m
//  CustomParameterUI
//
//  Created by Georg Seifert on 24.06.20.
//  Copyright © 2020 Georg Seifert. All rights reserved.
//

#import "CustomParameterUISheetController.h"
#import <GlyphsCore/GSCustomParameter.h>

@implementation CustomParameterUISheetController {
	NSArray<GSCustomParameter *> *_customParameters;
}
- (instancetype)init {
	self = [self initWithWindowNibName:@"CustomParameterUISheetController"];
	return self;
}

- (BOOL)setCustomParameters:(NSArray<GSCustomParameter *> *)customParameters error:(NSError *__autoreleasing *)error {
	_customParameters = customParameters;
	
	NSMutableOrderedSet *values1 = [NSMutableOrderedSet new];
	NSMutableOrderedSet *values2 = [NSMutableOrderedSet new];
	NSMutableOrderedSet *values3 = [NSMutableOrderedSet new];
	
	for (GSCustomParameter *customParameter in _customParameters) {
		NSString *value = customParameter.value;
		NSArray *values = [value componentsSeparatedByString:@";"];
		if (values.count > 0) {
			[values1 addObject:values[0]];
		}
		else {
			[values1 addObject:@""];
		}
		if (values.count > 1) {
			[values2 addObject:values[1]];
		}
		else {
			[values2 addObject:@""];
		}
		if (values.count > 2) {
			[values3 addObject:values[2]];
		}
		else {
			[values3 addObject:@""];
		}
	}
	if (values1.count == 1) {
		self.value1Text = values1.firstObject;
	}
	else {
		self.value1Text = NSMultipleValuesMarker;
	}
	if (values2.count == 1) {
		self.value2Text = values2.firstObject;
	}
	else {
		self.value2Text = NSMultipleValuesMarker;
	}
	if (values3.count == 1) {
		self.value3Text = values3.firstObject;
	}
	else {
		self.value3Text = NSMultipleValuesMarker;
	}
	return YES;
}

- (void)runDialog:(id)sender modalForWindow:(NSWindow *)window {
	[window beginSheet:self.window completionHandler:^(NSModalResponse returnCode) {
		NSLog(@"__returnCode %ld", (long)returnCode);
	}];
}

- (IBAction)okDialog:(id)sender {
	[[self window] makeFirstResponder:nil]; // to make sure to commit all editing
	for (GSCustomParameter * customParameter in _customParameters) {
		
		NSString *string1 = @"";
		NSString *string2 = @"";
		NSString *string3 = @"";
		
		NSString *value = customParameter.value;
		NSArray *values = [value componentsSeparatedByString:@";"];
		if (values.count > 0) {
			string1 = values[0];
		}
		if (values.count > 1) {
			string2 = values[1];
		}
		if (values.count > 2) {
			string3 = values[2];
		}
		if (_value1Text != NSMultipleValuesMarker) {
			string1 = _value1Text;
		}
		if (_value2Text != NSMultipleValuesMarker) {
			string2 = _value2Text;
		}
		if (_value3Text != NSMultipleValuesMarker) {
			string3 = _value3Text;
		}
		customParameter.value = [NSString stringWithFormat:@"%@;%@;%@", string1, string2, string3];
	}
	[[[self window] sheetParent] endSheet:[self window] returnCode:NSModalResponseOK];
}

- (IBAction)cancelDialog:(id)sender {
	[[[self window] sheetParent] endSheet:[self window] returnCode:NSModalResponseCancel];
}
@end
