//
//  InspectorDemoViewController.h
//  InspectorDemo
//
//  Created by Georg Seifert on 19.12.16.
//  Copyright © 2016 Georg Seifert. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import <GlyphsCore/GSInspectorViewController.h>

@interface InspectorDemoViewController : GSInspectorViewController

@property (nonatomic, weak) IBOutlet NSButton* titleButton;
@end
