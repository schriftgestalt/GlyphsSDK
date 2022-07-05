//
//  InspectorDemoViewController.m
//  InspectorDemo
//
//  Created by Georg Seifert on 19.12.16.
//  Copyright © 2016 Georg Seifert. All rights reserved.
//

#import "InspectorDemoViewController.h"

@interface InspectorDemoViewController ()

@end

@implementation InspectorDemoViewController

- (instancetype)init {
	self = [super initWithNibName:@"InspectorDemoView" bundle:[NSBundle bundleForClass:[InspectorDemoViewController class]]];
	return self;
}

- (void)setRepresentedObject:(id)representedObject {
	[super setRepresentedObject:representedObject];
	[_titleButton setTitle:representedObject];
}

@end
