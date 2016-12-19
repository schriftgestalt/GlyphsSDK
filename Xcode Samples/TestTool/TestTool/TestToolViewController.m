//
//  TestToolViewController.m
//  TestTool
//
//  Created by Georg Seifert on 19.12.16.
//  Copyright © 2016 Georg Seifert. All rights reserved.
//

#import "TestToolViewController.h"

@interface TestToolViewController ()

@end

@implementation TestToolViewController

- (instancetype)init {
	self = [super initWithNibName:@"TestToolView" bundle:[NSBundle bundleForClass:[TestToolViewController class]]];
	return self;
}

- (void)setRepresentedObject:(id)representedObject {
	[super setRepresentedObject:representedObject];
	[_titleButton setTitle:representedObject];
}

@end
