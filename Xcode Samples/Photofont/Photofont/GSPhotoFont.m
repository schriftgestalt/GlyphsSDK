//
//  GSPhotoFont.m
//  GSPhotoFont
//
//  Created by Georg Seifert on 30.07.10.
//  Copyright 2010 schriftgestaltung.de. All rights reserved.
//

#import "GSPhotoFont.h"
#import <GlyphsCore/GSProgressWindow.h>
#import <GlyphsCore/GSFont.h>
#import <GlyphsCore/GSFontMaster.h>
#import <GlyphsCore/GSGlyph.h>
#import <GlyphsCore/GSLayer.h>
#import <GlyphsCore/GSBackgroundImage.h>
#import <GlyphsCore/GSGlyphsInfo.h>
#import <GlyphsCore/GSGlyphInfo.h>
#import <GlyphsCore/NSDictionary_KeyPath.h>
#import <GlyphsCore/NSStringHelpers.h>
#import <GlyphsCore/GSModalSavePanel.h>

@interface NSData (Base64)
- (NSString *)base64Encoding;
- (instancetype)initWithBase64Encoding:(NSString *)Base64String;
@end

@implementation GSPhotoFont

@synthesize exportSettingsView = _exportSettingsView;
@synthesize font = _font;
@synthesize progressWindow = _progressWindow;
@synthesize sheetResult = _sheetResult;

- (instancetype)init {
	self = [super init];
	[NSBundle loadNibNamed:@"ExportSettingsView" owner:self];

	NSBundle *thisBundle = [NSBundle bundleForClass:[self class]];
	_toolbarIcon = [thisBundle imageForResource:@"phf"];
	[_toolbarIcon setName:@"phf"];
	// UKLog(@"___%@", _exportSettingsView);
	return self;
}

- (void)dealloc {
	UKLog(@"");
}

- (NSUInteger)interfaceVersion {
	return 1;
}

- (NSString *)title {
	return @"PhotoFont";
}

- (NSString *)toolbarTitle {
	return @"PhotoFont";
}

- (NSUInteger)groupID {
	return 15;
}

- (BOOL)writeFont:(GSFont *)GSFontObj error:(NSError **)error {
	UKLog(@"");
	NSSavePanel *savePanel = [NSSavePanel savePanel];
	[savePanel setCanCreateDirectories:YES]; // Added by DustinVoss
	[savePanel setTitle:NSLocalizedStringFromTableInBundle(@"Choose folder.", nil, [NSBundle bundleForClass:[self class]], @"Export Panel")];
	[savePanel setPrompt:NSLocalizedStringFromTableInBundle(@"Export", nil, [NSBundle bundleForClass:[self class]], @"Export Panel")];
	[savePanel setAllowedFileTypes:@[@"phf"]];
	[savePanel setCanSelectHiddenExtension:YES];
	[savePanel setAllowedFileTypes:@[@"phf"]];

	self.sheetResult = [savePanel runModalForDirectory:nil file:nil types:nil relativeToWindow:[(NSDocument *)GSFontObj.parent windowForSheet]];
	if (self.sheetResult == NSFileHandlingPanelOKButton) {
		return [self writeFont:GSFontObj toURL:[savePanel URL] error:error];
	}
	return YES;
}

- (BOOL)writeFont:(GSFont *)Font toURL:(NSURL *)URL error:(NSError **)error {
	if ([Font.fontMasters count] > 1) {
		if (error) {
			UKLog(@"NSException 2");
			NSString *Description = @"You can’t save this Document to a Photofont file because the font has more than one Master and this is not supported by the PhotoFont format.\n\n Please use the Export function instead.";
			NSDictionary *errorDetail = @{NSLocalizedRecoverySuggestionErrorKey : Description};
			*error = [NSError errorWithDomain:@"GSGlyphsDomain" code:1 userInfo:errorDetail];
		}
		else {
			NSLog(@"You can’t save this Document to a PhotoFont file because the font has more than one Master and this is not supported by the PhotoFont format.\n\n Please use the Export function instead.");
		}
		return NO;
	}
	NSXMLElement *root = (NSXMLElement *)[NSXMLNode elementWithName:@"PhF"];
	[root addAttribute:[NSXMLNode attributeWithName:@"version" stringValue:@"1.0"]];
	NSXMLElement *Header = [NSXMLElement elementWithName:@"header"];
	NSXMLElement *Element = nil;

	if ([[Font valueForKey:@"version"] length] > 0) {
		Element = [NSXMLElement elementWithName:@"version"];
		[Element addAttribute:[NSXMLNode attributeWithName:@"type" stringValue:@"string"]];
		[Element setStringValue:[Font valueForKey:@"version"]];
		[Header addChild:Element];
	}
	else {
		Element = [NSXMLElement elementWithName:@"version"];
		[Element addAttribute:[NSXMLNode attributeWithName:@"type" stringValue:@"string"]];
		[Element setStringValue:[NSString stringWithFormat:@"%ld.%3ld", Font.versionMajor, Font.versionMinor]];
		[Header addChild:Element];
	}

	Element = [NSXMLElement elementWithName:@"family"];
	[Element addAttribute:[NSXMLNode attributeWithName:@"type" stringValue:@"string"]];
	[Element setStringValue:Font.familyName];
	[Header addChild:Element];
	Element = [NSXMLElement elementWithName:@"face_name"];
	[Element addAttribute:[NSXMLNode attributeWithName:@"type" stringValue:@"string"]];
	[Element setStringValue:Font.familyName];
	[Header addChild:Element];
	Element = [NSXMLElement elementWithName:@"full_name"];
	[Element addAttribute:[NSXMLNode attributeWithName:@"type" stringValue:@"string"]];
	[Element setStringValue:Font.familyName];
	[Header addChild:Element];
	if ([[Font valueForKey:@"copyright"] length] > 0) {
		Element = [NSXMLElement elementWithName:@"copyright"];
		[Element addAttribute:[NSXMLNode attributeWithName:@"type" stringValue:@"string"]];
		[Element setStringValue:[Font valueForKey:@"copyright"]];
		[Header addChild:Element];
	}
	if ([[Font valueForKey:@"designer"] length] > 0) {
		Element = [NSXMLElement elementWithName:@"source"];
		[Element addAttribute:[NSXMLNode attributeWithName:@"type" stringValue:@"string"]];
		[Element setStringValue:[Font valueForKey:@"designer"]];
		[Header addChild:Element];
	}
	GSFontMaster *FontMaster = [Font fontMasterAtIndex:0];
	Element = [NSXMLElement elementWithName:@"ascender"];
	[Element addAttribute:[NSXMLNode attributeWithName:@"type" stringValue:@"int"]];
	[Element setStringValue:[@((int)roundf(FontMaster.ascender)) stringValue]];
	[Header addChild:Element];
	Element = [NSXMLElement elementWithName:@"descender"];
	[Element addAttribute:[NSXMLNode attributeWithName:@"type" stringValue:@"int"]];
	[Element setStringValue:[@(-(int)roundf(FontMaster.descender)) stringValue]];
	[Header addChild:Element];
	Element = [NSXMLElement elementWithName:@"external_leading"];
	[Element addAttribute:[NSXMLNode attributeWithName:@"type" stringValue:@"int"]];
	[Element setStringValue:[@0 stringValue]];
	[Header addChild:Element];
	Element = [NSXMLElement elementWithName:@"upm"];
	[Element addAttribute:[NSXMLNode attributeWithName:@"type" stringValue:@"int"]];
	[Element setStringValue:[@((int)roundf(Font.unitsPerEm)) stringValue]];
	[Header addChild:Element];
	[root addChild:Header];
	NSXMLElement *Globals = [NSXMLElement elementWithName:@"globals"];
	NSXMLElement *Unicode = [NSXMLElement elementWithName:@"unicode_mapping"];
	[Unicode addAttribute:[NSXMLNode attributeWithName:@"type" stringValue:@"array"]];
	[Unicode addAttribute:[NSXMLNode attributeWithName:@"subtype" stringValue:@"map_unicode"]];
	for (GSGlyph *currGlyph in Font.glyphs) {
		if ([currGlyph.unicode length] > 1) {
			NSXMLElement *Map = [NSXMLElement elementWithName:@"map"];
			[Map addAttribute:[NSXMLNode attributeWithName:@"id" stringValue:currGlyph.name]];
			UniChar Char = [Font characterForGlyph:currGlyph];
			[Map addAttribute:[NSXMLNode attributeWithName:@"unc" stringValue:[NSString stringWithFormat:@"%d", Char]]];
			[Unicode addChild:Map];
			NSString *CharString = [NSString stringWithFormat:@"%C", Char];
			NSString *UppercaseCharString = [CharString uppercaseString];
			if (![CharString isEqualToString:UppercaseCharString]) {
				UniChar UppercaseChar = [UppercaseCharString characterAtIndex:0];
				GSGlyph *UppercaseGlyph = [Font glyphForCharacter:UppercaseChar];
				if (!UppercaseGlyph) {
					Map = [NSXMLElement elementWithName:@"map"];
					[Map addAttribute:[NSXMLNode attributeWithName:@"id" stringValue:currGlyph.name]];
					// Char = [Font characterForGlyph:currGlyph];
					[Map addAttribute:[NSXMLNode attributeWithName:@"unc" stringValue:[NSString stringWithFormat:@"%d", UppercaseChar]]];
					[Unicode addChild:Map];
				}
			}
			NSString *LowercaseCharString = [CharString lowercaseString];
			if (![CharString isEqualToString:LowercaseCharString]) {
				UniChar LowercaseChar = [LowercaseCharString characterAtIndex:0];
				GSGlyph *LowercaseGlyph = [Font glyphForCharacter:LowercaseChar];
				if (!LowercaseGlyph) {
					Map = [NSXMLElement elementWithName:@"map"];
					[Map addAttribute:[NSXMLNode attributeWithName:@"id" stringValue:currGlyph.name]];
					// Char = [Font characterForGlyph:currGlyph];
					[Map addAttribute:[NSXMLNode attributeWithName:@"unc" stringValue:[NSString stringWithFormat:@"%d", LowercaseChar]]];
					[Unicode addChild:Map];
				}
			}
		}
	}
	[Globals addChild:Unicode];
	NSDictionary *MasterKerning = (Font.kerning)[FontMaster.id];
	NSXMLElement *Kerning = [NSXMLElement elementWithName:@"kerning"];
	[Kerning addAttribute:[NSXMLNode attributeWithName:@"type" stringValue:@"array"]];
	[Kerning addAttribute:[NSXMLNode attributeWithName:@"subtype" stringValue:@"kerning_pair"]];
	for (NSString *LeftKerningKey in [MasterKerning allKeys]) {
		if ([LeftKerningKey hasPrefix:@"@MM_"]) {
			continue;
		}
		NSDictionary *LeftKerning = MasterKerning[LeftKerningKey];
		for (NSString *RightKerningKey in [LeftKerning allKeys]) {
			if ([RightKerningKey hasPrefix:@"@MM_"]) {
				continue;
			}
			GSGlyph *LeftGlyph = [Font glyphForId:LeftKerningKey];
			GSGlyph *RightGlyph = [Font glyphForId:RightKerningKey];
			NSNumber *Value = LeftKerning[RightKerningKey];
			if (LeftGlyph && RightGlyph && Value) {
				NSXMLElement *Pair = [NSXMLElement elementWithName:@"pair"];
				[Pair addAttribute:[NSXMLNode attributeWithName:@"left" stringValue:LeftGlyph.name]];
				[Pair addAttribute:[NSXMLNode attributeWithName:@"right" stringValue:RightGlyph.name]];
				[Pair addAttribute:[NSXMLNode attributeWithName:@"x" stringValue:[NSString stringWithFormat:@"%d", (int)roundf([Value floatValue])]]];
				[Kerning addChild:Pair];
			}
		}
	}
	if ([[Kerning children] count] > 0) {
		[Globals addChild:Kerning];
	}
	[root addChild:Globals];
	NSXMLElement *Glyphs = [NSXMLElement elementWithName:@"glyphs"];
	NSXMLElement *PhotoElement = [NSXMLElement elementWithName:@"photo"];
	for (GSGlyph *currGlyph in Font.glyphs) {
		/*
		   <glyph id="A">
			<image id="v0" type="photo">
				<shape embedded="img.png">
					<ppm int="72" />
					<bbox x="-13" y="-19" width="78" height="90" />
					<base x="13" y="71" />
					<delta x="50" y="0" />
				</shape>
			</image>
		   </glyph>
		 */
		GSLayer *Layer = [currGlyph layerForKey:FontMaster.id];
		NSXMLElement *ShapeElement = [NSXMLElement elementWithName:@"shape"];
		Element = [NSXMLElement elementWithName:@"ppm"];
		[Element addAttribute:[NSXMLNode attributeWithName:@"int" stringValue:[@((int)roundf(Font.unitsPerEm)) stringValue]]];
		[ShapeElement addChild:Element];
		NSRect BBox = NSZeroRect;
		NSPoint Base = NSZeroPoint;
		if (Layer.backgroundImage && Layer.backgroundImage.image) {
			NSString *ImageName = Layer.backgroundImage.imagePath;
			NSRange Range = [ImageName rangeOfString:@".phf-"];
			if (Range.location < NSNotFound) {
				ImageName = [ImageName substringFromIndex:Range.location + Range.length];
			}
			else {
				ImageName = [ImageName lastPathComponent];
			}
			ImageName = [ImageName ascciString];

			ImageName = [ImageName stringByDeletingPathExtension];
			NSXMLElement *ImageDataElement = [[PhotoElement nodesForXPath:[NSString stringWithFormat:@"image[@id='%@']", ImageName] error:error] lastObject];
			if (!ImageDataElement) {
				NSData *ImageData = [[NSData alloc] initWithContentsOfFile:Layer.backgroundImage.imagePath];
				if (ImageData) {
					NSMutableString *ImageDataString = [[ImageData base64Encoding] mutableCopy];
					NSInteger Count = floor([ImageDataString length] / 64.0) * 64;
					for (NSInteger i = Count; i > 0; i -= 64) {
						[ImageDataString insertString:@"\n" atIndex:i];
					}
					NSMutableString *ImageString = [NSMutableString stringWithFormat:@"\nContent-Type: image/png; charset=US-ASCII; name=%@\nContent-transfer-encoding: base64\n\n%@\n", ImageName, ImageDataString];

					ImageDataElement = [NSXMLElement elementWithName:@"image"];

					[ImageDataElement addAttribute:[NSXMLNode attributeWithName:@"id" stringValue:ImageName]];
					[ImageDataElement setStringValue:ImageString];
					[PhotoElement addChild:ImageDataElement];
				}
			}
			if (Layer.backgroundImage.image) {
				[ShapeElement addAttribute:[NSXMLNode attributeWithName:@"embedded" stringValue:ImageName]];

				NSSize ImageSize = [Layer.backgroundImage.image size];

				// BackgroundImage.crop = NSMakeRect(Base.x + BBox.origin.x, ImageSize.height - Base.y + BBox.origin.y, BBox.size.width, BBox.size.height);
				// Layer.backgroundImage.position = NSMakePoint(-Base.x, Base.y - ImageSize.height);

				NSRect Crop = Layer.backgroundImage.crop;
				Base = Layer.backgroundImage.position;
				Base = NSMakePoint(-Base.x, ImageSize.height + Base.y);

				BBox.origin.x = Crop.origin.x - Base.x;
				BBox.origin.y = Crop.origin.y - ImageSize.height + Base.y;
				BBox.size = Crop.size;
			}
		}
		Element = [NSXMLElement elementWithName:@"bbox"];
		[Element addAttribute:[NSXMLNode attributeWithName:@"x" stringValue:[NSString stringWithFormat:@"%d", (int)roundf(BBox.origin.x)]]];
		[Element addAttribute:[NSXMLNode attributeWithName:@"y" stringValue:[NSString stringWithFormat:@"%d", (int)roundf(BBox.origin.y)]]];
		[Element addAttribute:[NSXMLNode attributeWithName:@"width" stringValue:[NSString stringWithFormat:@"%d", (int)roundf(BBox.size.width)]]];
		[Element addAttribute:[NSXMLNode attributeWithName:@"height" stringValue:[NSString stringWithFormat:@"%d", (int)roundf(BBox.size.height)]]];
		[ShapeElement addChild:Element];
		Element = [NSXMLElement elementWithName:@"base"];
		[Element addAttribute:[NSXMLNode attributeWithName:@"x" stringValue:[NSString stringWithFormat:@"%d", (int)roundf(Base.x)]]];
		[Element addAttribute:[NSXMLNode attributeWithName:@"y" stringValue:[NSString stringWithFormat:@"%d", (int)roundf(Base.y)]]];
		[ShapeElement addChild:Element];

		Element = [NSXMLElement elementWithName:@"delta"];
		[Element addAttribute:[NSXMLNode attributeWithName:@"x" stringValue:[@((int)roundf(Layer.width)) stringValue]]];
		[Element addAttribute:[NSXMLNode attributeWithName:@"y" stringValue:@"0"]];
		[ShapeElement addChild:Element];

		NSXMLElement *ImageElement = [NSXMLElement elementWithName:@"image"];
		[ImageElement addAttribute:[NSXMLNode attributeWithName:@"id" stringValue:@"v0"]];
		[ImageElement addAttribute:[NSXMLNode attributeWithName:@"type" stringValue:@"photo"]];
		[ImageElement addChild:ShapeElement];
		NSXMLElement *GlyphElement = [NSXMLElement elementWithName:@"glyph"];
		[GlyphElement addAttribute:[NSXMLNode attributeWithName:@"id" stringValue:currGlyph.name]];

		[GlyphElement addChild:ImageElement];
		[Glyphs addChild:GlyphElement];
	}
	[root addChild:Glyphs];
	NSXMLElement *DataElement = [NSXMLElement elementWithName:@"data"];
	[DataElement addChild:PhotoElement];
	[root addChild:DataElement];
	NSXMLDocument *xmlDoc = [[NSXMLDocument alloc] initWithRootElement:root];
	[xmlDoc setVersion:@"1.0"];
	[xmlDoc setCharacterEncoding:@"UTF-8"];
	NSString *xmlString = [xmlDoc XMLStringWithOptions:NSXMLNodePrettyPrint | NSXMLNodeCompactEmptyElement];
	if (![xmlString writeToURL:URL atomically:YES encoding:NSUTF8StringEncoding error:error]) {
		UKLog(@"Error photofont");
		return NO;
	}
	return YES;
}

- (GSFont *)fontFromURL:(NSURL *)URL ofType:(NSString *)Type error:(NSError **)error {
	UKLog(@"URL: %@", URL);
	NSXMLDocument *xmlDoc = [[NSXMLDocument alloc] initWithContentsOfURL:URL options:0 error:error];
	if (!xmlDoc) {
		return nil;
	}
	NSXMLElement *root = [xmlDoc rootElement];
	NSXMLElement *Header = [[root elementsForName:@"header"] lastObject];
	GSFont *Font = [[GSFont alloc] init];
	NSXMLElement *Element = [[Header elementsForName:@"family"] lastObject];
	if (Element) {
		Font.familyName = [Element stringValue];
	}
	Element = [[Header elementsForName:@"copyright"] lastObject];
	if (Element) {
		[Font setValue:[Element stringValue] forKey:@"copyright"];
	}
	Element = [[Header elementsForName:@"source"] lastObject];
	if (Element) {
		[Font setValue:[Element stringValue] forKey:@"designer"];
	}
	Element = [[Header elementsForName:@"version"] lastObject];
	if (Element && [[Element stringValue] length] > 0) {
		[Font setValue:[Element stringValue] forKey:@"version"];
	}
	GSFontMaster *FontMaster = [Font fontMasterAtIndex:0];
	[Font willChangeValueForKey:@"fontMasers"];
	Element = [[Header elementsForName:@"ascender"] lastObject];
	if (Element) {
		FontMaster.ascender = [[Element stringValue] intValue];
		FontMaster.capHeight = [[Element stringValue] intValue];
		FontMaster.xHeight = [[Element stringValue] intValue];
	}
	Element = [[Header elementsForName:@"descender"] lastObject];
	if (Element) {
		FontMaster.descender = -[[Element stringValue] intValue];
	}
	Element = [[Header elementsForName:@"upm"] lastObject];
	if (Element) {
		[Font setValue:@([[Element stringValue] intValue]) forKey:@"unitsPerEm"];
	}
	[Font didChangeValueForKey:@"fontMasers"];
	[Font willChangeValueForKey:@"glyphs"];
	NSXMLElement *Glyphs = [[root elementsForName:@"glyphs"] lastObject];
	for (NSXMLElement *GlyphsElement in [Glyphs children]) {
		GSGlyph *newGlyph = [[GSGlyph alloc] init];
		[[newGlyph undoManager] disableUndoRegistration];
		newGlyph.name = [[GlyphsElement attributeForName:@"id"] stringValue];
		[Font addGlyph:newGlyph];
		int i = 0;
		for (NSXMLElement *ImageElement in [GlyphsElement elementsForName:@"image"]) {
			NSXMLElement *ShapeElement = [[ImageElement elementsForName:@"shape"] lastObject];
			NSString *ImagePath = nil;
			NSString *ImageName = [[ShapeElement attributeForName:@"embedded"] stringValue];
			NSFileManager *manager = [NSFileManager defaultManager];
			GSBackgroundImage *BackgroundImage = nil;
			BOOL isDir;
			if (ImageName) {
				ImagePath = [[URL path] stringByAppendingString:[NSString stringWithFormat:@"-%@.png", ImageName]];
				if (![manager fileExistsAtPath:ImagePath isDirectory:&isDir]) {
					NSXMLElement *ImageDataElement = [[root nodesForXPath:[NSString stringWithFormat:@"/PhF/data/photo/image[@id='%@']", ImageName] error:nil] lastObject];
					if (ImageDataElement) {
						NSString *Base64String = [ImageDataElement stringValue];
						NSRange HeaderRange = [Base64String rangeOfString:@"Content-transfer-encoding: base64"];
						if (HeaderRange.location < NSNotFound) {
							Base64String = [Base64String substringFromIndex:HeaderRange.location + HeaderRange.length];
						}
						Base64String = [Base64String stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
						Base64String = [Base64String stringByReplacingOccurrencesOfString:@"\n" withString:@""];
						if ([Base64String hasSuffix:@"=="]) {}

						NSData *ImageData = [[NSData alloc] initWithBase64Encoding:Base64String];
						[ImageData writeToFile:ImagePath atomically:YES];
					}
				}
			}
			// set ImagePath to external image
			if (ImageName) {
				if (ImagePath && [manager fileExistsAtPath:ImagePath isDirectory:&isDir] && !isDir) {
					BackgroundImage = [[GSBackgroundImage alloc] initWithURL:[[NSURL alloc] initFileURLWithPath:ImagePath]];

					if (!BackgroundImage.image) {
						[NSException raise:@"could’n load Image data" format:@"The embedded Image couldn’t be loaded"];
					}
					NSSize ImageSize = [BackgroundImage.image size];
					/*
					   <shape embedded="img.png">
						<ppm int="72" />
						<bbox x="-13" y="-19" width="66" height="87" />
						<base x="13" y="68" />
						<delta x="37" y="0" />
					   </shape>
					 */
					NSXMLElement *DetailElement = [[ShapeElement elementsForName:@"base"] lastObject];
					NSPoint Base = NSZeroPoint;
					if (DetailElement) {
						Base.x = [[[DetailElement attributeForName:@"x"] stringValue] intValue];
						Base.y = [[[DetailElement attributeForName:@"y"] stringValue] intValue];
					}
					DetailElement = [[ShapeElement elementsForName:@"bbox"] lastObject];
					NSRect BBox = NSZeroRect;
					if (DetailElement) {
						BBox.origin.x = [[[DetailElement attributeForName:@"x"] stringValue] intValue];
						BBox.origin.y = [[[DetailElement attributeForName:@"y"] stringValue] intValue];
						BBox.size.width = [[[DetailElement attributeForName:@"width"] stringValue] intValue];
						BBox.size.height = [[[DetailElement attributeForName:@"height"] stringValue] intValue];
					}

					BackgroundImage.crop = NSMakeRect(Base.x + BBox.origin.x, ImageSize.height - Base.y + BBox.origin.y, BBox.size.width, BBox.size.height);
					BackgroundImage.position = NSMakePoint(-Base.x, Base.y - ImageSize.height);
				}
				else {
					[NSException raise:@"could’n load Image data" format:@"The embedded Image couldn’t be loaded"];
				}
			}
			NSXMLElement *DetailElement = [[ShapeElement elementsForName:@"delta"] lastObject];
			NSInteger Width = 0;
			if (DetailElement) {
				Width = [[[DetailElement attributeForName:@"x"] stringValue] intValue];
			}

			GSLayer *Layer = [newGlyph layerForKey:[Font fontMasterAtIndex:i].id];
			Layer.width = (CGFloat)Width;
			[Layer setBackgroundImage:BackgroundImage];
			i++;
		}
		[newGlyph setChangeCount:0];
		[[newGlyph undoManager] enableUndoRegistration];
		[[newGlyph undoManager] removeAllActions];
	}
	NSXMLElement *KerningElement = [[root nodesForXPath:@"/PhF/globals/kerning[@type='array']" error:nil] lastObject];
	for (NSXMLElement *PairElement in [KerningElement children]) {
		NSString *LeftName = [[PairElement attributeForName:@"left"] stringValue];
		NSString *RightName = [[PairElement attributeForName:@"right"] stringValue];
		CGFloat Value = [[[PairElement attributeForName:@"x"] stringValue] floatValue];
		GSGlyph *LeftGlyph = [Font glyphForName:LeftName];
		GSGlyph *RightGlyph = [Font glyphForName:RightName];
		if (LeftGlyph && RightGlyph && Value != 0 && Value < 32000) {
			[Font setKerningForFontMasterID:FontMaster.id LeftKey:LeftGlyph.id RightKey:RightGlyph.id Value:Value];
		}
	}
	[Font didChangeValueForKey:@"glyphs"];
	return Font;
}

@end
