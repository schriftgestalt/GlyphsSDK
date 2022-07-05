//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//___COPYRIGHT___
//

#import "___PACKAGENAMEASIDENTIFIER___.h"
#import <GlyphsCore/GSFont.h>
#import <GlyphsCore/GSFontMaster.h>
#import <GlyphsCore/GSGlyph.h>
#import <GlyphsCore/GSLayer.h>
#import <GlyphsCore/GSPath.h>
#import <GlyphsCore/GSCallbackHandler.h>

@implementation ___FILEBASENAMEASIDENTIFIER___ {
	CGFloat _firstValue;
}

- (instancetype)init {
	self = [super init];
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

- (NSString *)actionName {
	// The title of the button in the filter dialog.
	return @"___PACKAGENAME___";
}

- (NSString *)keyEquivalent {
	// The key together with Cmd+Shift will be the shortcut for the filter.
	// Return nil if you do not want to set a shortcut.
	// Users can set their own shortcuts in System Prefs.
	return nil;
}

- (NSView *)view {
	if (!_view) {
		[[NSBundle bundleForClass:[self class]] loadNibNamed:@"___PACKAGENAMEASIDENTIFIER___Dialog" owner:self topLevelObjects:nil];
	}
	return _view;
}

- (NSError *)setup {
	NSNumber *firstValueNumber = (NSNumber *)[_fontMaster userDataForKey:@"theFirstValue"];
	if (firstValueNumber) {
		_firstValue = [firstValueNumber floatValue];
	}
	else {
		_firstValue = 15; // set default value.
	}
	_firstValueField.floatValue = _firstValue;
	return nil;
}

- (void)processLayer:(GSLayer *)layer withFirstValue:(CGFloat)firstValue {
	// this is a menthod specially for your filter. Add/remove arguments as you need
	
	// do stuff with the Layer.

}

- (void)processFont:(GSFont *)font withArguments:(NSArray *)arguments {
	// Invoked when called as Custom Parameter in an instance at export.
	// The Arguments come from the custom parameter in the instance settings. 
	// The first item in Arguments is the class-name. After that, it depends on the filter.
	CGFloat firstValue = 15;
	if (arguments.count > 1) {
		firstValue = [arguments[1] floatValue];
	}
	_checkSelection = NO;
	NSString *fontMasterId = [font fontMasterAtIndex:0].id;
	BOOL include = NO;
	NSError *error = nil;
	NSSet *glyphs = getIncludeExcludeGlyphListFilter(arguments, &include, font, &error);
	for (GSGlyph *glyph in font.glyphs) {
		if (glyphs && [glyphs containsObject:glyph.name] != include) {
			continue;
		}
		GSLayer *layer = [glyph layerForId:fontMasterId];
		[self processLayer:layer withFirstValue:firstValue];
	}
}

- (IBAction)setFirstValue:(id)sender {
	// This is only an example for a setter method.
	// Add methods like this for each option in the dialog.
	CGFloat firstValue = [sender floatValue];
	if(fabs(firstValue - _firstValue) > 0.01) {
		_firstValue = firstValue;
		[self process:nil];
	}
}

- (void)process:(id)sender {
	int k;
	for (k = 0; k < [_shadowLayers count]; k++) {
		GSLayer *shadowLayer = [_shadowLayers objectAtIndex:k];
		GSLayer *layer = [_layers objectAtIndex:k];
		layer.shapes = [[NSMutableArray alloc] initWithArray:shadowLayer.shapes copyItems:YES];
		layer.selection = [NSMutableOrderedSet new];
		if ([shadowLayer.selection count] > 0 && _checkSelection) {
			int i, j;
			for (i = 0; i < [shadowLayer.shapes count]; i++) {
				GSPath *shadowPath = (GSPath *)[shadowLayer objectInShapesAtIndex:i];
				if (![shadowPath isKindOfClass:[GSPath class]]) {
					continue;
				}
				GSPath *layerPath = (GSPath *)[layer objectInShapesAtIndex:i];
				for (j = 0; j < [shadowPath.nodes count]; j++) {
					GSNode *shadowNode = [shadowPath nodeAtIndex:j];
					if ([shadowLayer.selection containsObject:shadowNode]) {
						[layer addSelection:[layerPath nodeAtIndex:j]];
					}
				}
			}
		}
		[self processLayer:layer withFirstValue:_firstValue];
		[layer clearSelection];
	}
	// Safe the value in the FontMaster. But could be saved in UserDefaults, too.
	[_fontMaster setUserData:@(_firstValue) forKey:@"____TheFirstValue____"];
	[super process:nil];
}

@end
