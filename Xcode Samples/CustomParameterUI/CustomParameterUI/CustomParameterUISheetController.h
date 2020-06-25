//
//  CustomParameterUISheetController.h
//  CustomParameterUI
//
//  Created by Georg Seifert on 24.06.20.
//  Copyright © 2020 Georg Seifert. All rights reserved.
//

#import <Cocoa/Cocoa.h>

NS_ASSUME_NONNULL_BEGIN

@interface CustomParameterUISheetController : NSWindowController

@property (strong) NSString *value1Text;
@property (strong) NSString *value2Text;
@property (strong) NSString *value3Text;

@end

NS_ASSUME_NONNULL_END
