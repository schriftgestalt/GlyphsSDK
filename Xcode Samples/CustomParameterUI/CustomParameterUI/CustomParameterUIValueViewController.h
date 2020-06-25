//
//  CustomParameterUIValueViewController.h
//  CustomParameterUI
//
//  Created by Georg Seifert on 24.06.20.
//  Copyright © 2020 Georg Seifert. All rights reserved.
//

#import <Cocoa/Cocoa.h>

NS_ASSUME_NONNULL_BEGIN

@interface CustomParameterUIValueViewController : NSViewController

@property (weak) IBOutlet NSTextField *value1TextField;

@property (weak) IBOutlet NSTextField *value2TextField;

@property (weak) IBOutlet NSTextField *value3TextField;

@end

NS_ASSUME_NONNULL_END
