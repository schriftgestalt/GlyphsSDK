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

@implementation ___FILEBASENAMEASIDENTIFIER___

- (id) init {
	self = [super init];
	[NSBundle loadNibNamed:@"___PACKAGENAMEASIDENTIFIER___Dialog" owner:self];
	return self;
}

- (NSUInteger) interfaceVersion {
	// Distinguishes the API verison the plugin was built for. Return 1.
	return 1;
}

- (NSString*) title {
	// Return the name of the tool as it will appear in the menu.
	return @"___PACKAGENAME___";
}

- (NSString*) actionName {
	// The title of the button in the filter dialog.
	return @"___PACKAGENAME___";
}

- (NSString*) keyEquivalent {
	// The key together with Cmd+Shift will be the shortcut for the filter.
	// Return nil if you do not want to set a shortcut.
	// Users can set their own shortcuts in System Prefs.
	return nil;
}

- (NSError*) setup {
	if ([_fontMaster.userData objectForKey:@"____TheFirstValue____"]) {
		_firstValue = [[_fontMaster.userData objectForKey:@"____TheFirstValue____"] floatValue];
	}
	else {
		_firstValue = 15; // set default value.
	}
	[_firstValueField setFloatValue:_firstValue];
	return nil;
}

- (void) processLayer:(GSLayer*)Layer withFirstValue:(CGFloat)FirstValue {
	// the method should contain all parameters as arguments
	
	// do stuff with the Layer.
	
	
}

- (void) processFont:(GSFont*)Font withArguments:(NSArray*)Arguments {
	// Invoked when called as Custom Parameter in an instance at export.
	// The Arguments come from the custom parameter in the instance settings. 
	// The first item in Arguments is the class-name. After that, it depends on the filter.
	CGFloat FirstValue;
	if ([Arguments count] > 1) {
		FirstValue = [[Arguments objectAtIndex:1] floatValue];
	}
	checkSelection = NO;
	NSString * FontMasterId = [Font fontMasterAtIndex:0].id;
	BOOL Include = NO;
	NSSet * Glyphs = getIncludeExcludeGlyphList(Arguments, &Include);
	for (GSGlyph * Glyph in Font.glyphs) {
		if (Glyphs && [Glyphs containsObject:Glyph.name] != Include) continue;
		
		GSLayer * Layer = [Glyph layerForKey:FontMasterId];
		[self processLayer:Layer withFirstValue:FirstValue];
	}
}

- (IBAction) setFirstValue:(id)sender {
	// This is only an example for a setter method.
	// Add methods like this for each option in the dialog.
	CGFloat FirstValue = [sender floatValue];
	if(fabs(FirstValue - _firstValue) > 0.01) {
		_firstValue = FirstValue;
		[self process:nil];
	}
}

- (void) process:(id)sender {
	int k;
	for (k = 0; k < [_shadowLayers count]; k++) {
		GSLayer * ShadowLayer = [_shadowLayers objectAtIndex:k];
		GSLayer * Layer = [_layers objectAtIndex:k];
		Layer.paths = [[NSMutableArray alloc] initWithArray:ShadowLayer.paths copyItems:YES];
		Layer.selection = [NSMutableArray array];
		if ([ShadowLayer.selection count] > 0 && checkSelection) {
			int i, j;
			for (i = 0; i < [ShadowLayer.paths count]; i++) {
				GSPath * currShadowPath = [ShadowLayer.paths objectAtIndex:i];
				GSPath * currLayerPath = [Layer.paths objectAtIndex:i];
				for (j = 0; j < [currShadowPath.nodes count]; j++) {
					GSNode * currShadowNode = [currShadowPath.nodes objectAtIndex:j];
					if ([ShadowLayer.selection containsObject:currShadowNode]) {
						[Layer addSelection:[currLayerPath.nodes objectAtIndex:j]];
					}
				}
			}
		}
		[self processLayer:Layer withFirstValue:_firstValue];
		[Layer clearSelection];
	}
	// Safe the value in the FontMaster. But could be saved in UserDefaults, too.
	[_fontMaster.userData setObject:[NSNumber numberWithDouble:_firstValue] forKey:@"____TheFirstValue____"];
	[super process:nil];
}

@end
