# Glyphs File Format, Version 2

Glyphs saves its source files in a plain-text format.
This way, files can be viewed and edited in any text editor.

## File Format Details

- The file format is based on OpenStep Property Lists (also known as NeXTSTEP, ASCII, or old-style Property Lists).
- This format can be converted to JSON for validation against a JSON Schema.
- The file contents are UTF-8 encoded.
- In addition to the four core data types (dictionary, array, string, and data), Glyphs uses unquoted strings to represent numbers (integers, floats, and booleans).
  Booleans are encoded as `1` or `"1"` (true) and `0` or `"0"` (false).
  Strings that look like numbers are always encoded in quotes.
- Whitespace is restricted to ASCII spaces, line feeds, and horizontal tabs.
- No comments (like `// ...` or `/* .... */`) are present.
- Indentation, while allowed, is generally omitted to reduce file size.
- Dictionaries and arrays are generally broken onto lines such that each key or element starts on a new line.
  When empty, they span two lines, one for the opening and one for the closing bracket.
- Some arrays are encoded on a single line for better readability and to reduce file size.
  These are mostly arrays used as tuples like points with X/Y coordinates.
  The `glyphsCompact` attribute in the JSON Schema indicates that the array is encoded on a single line.
- Some string values do not escape horizontal tab and line feed characters, instead using the literal characters.
  This improves readability.
- Several values cannot be edited in isolation, as they are dependent on one another.
  For example, changing the ID of a master requires updating the matching associated master ID of layers.
- Empty dictionaries and arrays are generally omitted, except for values of a `userData` property where the structure is preserved.

## Syntax

The following Backus–Naur form describes the syntax of the Glyphs file format.

```xml
<document>       ::= <ws> <value> <ws>;
<ws>             ::= ( ' ' | '\t' | '\n' )*;
<value>          ::= <dictionary> | <array> | <string> | <number> | <data>;
<dictionary>     ::= '{' <ws> ( <key-value-pair> <ws> )* '}';
<key-value-pair> ::= <string> <ws> '=' <ws> <value> ';';
<array>          ::= '(' <ws> [ <array-elements> <ws> ] ')';
<array-elements> ::= <value> [ <ws> ',' ]
                   | <value> <ws> ',' <ws> <array-elements>;
<string>         ::= <string-quoted> | <string-bare>;
<string-quoted>  ::= '"' ( '\' <escaped-char> | <quoted-char> )* '"';
<escaped-char>   ::= '\' | 'a' | 'b' | 'e' | 'f' | 'n' | 'r' | 't' | 'v' | '\n'
                   | <base8> [ <base8> [ <base8> ] ]
                   | 'U' <base16> <base16> <base16> <base16>;
<base8>          ::= '0'-'7';
<base16>         ::= '0'-'9' | 'A'-'F' | 'a'-'f';
<quoted-char>    ::= { any character except '"' and '\' };
<string-bare>    ::= <unquoted-start> ( <unquoted-char> )*;
<unquoted-start> ::= '$' | '+' | '.' | '/' | ':' | 'A'-'Z' | '_' | 'a'-'z';
<unquoted-char>  ::= <unquoted-start> | '-' | '0'-'9';
<number>         ::= [ '-' ] ( '0'-'9' )+ [ '.' ( '0'-'9' )+ ];
<data>           ::= '<' <ws> [ <data-content> <ws> ] '>';
<data-content>   ::= <data-byte> [ <ws> <data-byte> ]*;
<data-byte>      ::= <base16> <ws> <base16>;
```

## Schema

Use the following JSON schemas to validate files.

- [glyphs-1.schema.json](https://github.com/schriftgestalt/GlyphsSDK/blob/Glyphs3/GlyphsFileFormat/Schemas/glyphs-1.schema.json)
- [glyphs-autosave-1.schema.json](https://github.com/schriftgestalt/GlyphsSDK/blob/Glyphs3/GlyphsFileFormat/Schemas/glyphs-autosave-1.schema.json)

## Document

- <code><strong>.appVersion</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The build number of Glyphs used to save the file. Example: `"4012"`.
- <code><strong>DisplayStrings</strong>: array = []</code> – The strings of the Edit View tabs. Omitted when the `Write DisplayStrings` custom parameter is set to false. Omitted and written as `displayStrings` to `UIState.plist` in case of a package file. See [`displayStrings`](#spec-glyphs-1-displayStrings).
- <code><strong>classes</strong>: array = []</code> – The OpenType layout classes of the font.
 See [`class`](#spec-glyphs-1-class) for items.
- <code><strong>copyright</strong>: string</code> – The copyright notice.
- <code><strong>customParameters</strong>: array = []</code> – The custom parameters of the font.
 See [`customParameter`](#spec-glyphs-1-customParameter) for items.
- <code><strong>date</strong>: string</code> – The moment in time that is used as the creation date of exported font files including date, time, and timezone. Example: `"2026-07-17 03:14:15 +0000"`.
- <code><strong>designer</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the designer.
- <code><strong>designerURL</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The URL to the designer.
- <code><strong>disablesAutomaticAlignment</strong> = false</code> – Whether automatic alignment of components is disabled.
    - Possible values: `0`, `"0"`, `1`, `"1"`.
- <code><strong>disablesNiceNames</strong> = false</code> – Whether to use production names instead of nice names.
    - Possible values: `0`, `"0"`, `1`, `"1"`.
- <code><strong>familyName</strong>: string</code> – The font family name. Corresponds to the default value of the `familyNames` property.
- <code><strong>featurePrefixes</strong>: array = []</code> – The OpenType layout feature prefixes of the font.
 See [`featurePrefix`](#spec-glyphs-1-featurePrefix) for items.
- <code><strong>features</strong>: array = []</code> – The OpenType layout features of the font.
 See [`feature`](#spec-glyphs-1-feature) for items.
- <code><strong>fontMaster</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The masters of the font.
 Min count: 1.
 See [`fontMaster`](#spec-glyphs-1-fontMaster) for items.
- <code><strong>glyphs</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The glyphs of the font. The order is used on export unless the `glyphOrder` custom parameter is set.
 See [`glyph`](#spec-glyphs-1-glyph) for items.
- <code><strong>gridLength</strong>: integer = 1</code> (`u32`) – The main grid length.
- <code><strong>gridSubDivision</strong>: integer = 1</code> (`u32`) – The grid sub-division size.
- <code><strong>instances</strong>: array = []</code> – The instances of the font.
 See [`instance`](#spec-glyphs-1-instance) for items.
- <code><strong>keepAlternatesTogether</strong> = false</code> – Whether to keep alternates glyphs together in Font View.
    - Possible values: `0`, `"0"`, `1`, `"1"`.
- <code><strong>kerning</strong>: object = {}</code> – The kerning of the font. See [`kerning`](#spec-glyphs-1-kerning).
- <code><strong>keyboardIncrement</strong>: number = 1</code> (`f32`) – The standard keyboard increment.
- <code><strong>keyboardIncrementBig</strong>: number = 10</code> (`f32`) – The keyboard increment when holding the Shift key.
- <code><strong>keyboardIncrementHuge</strong>: number = 100</code> (`f32`) – The keyboard increment when holding both the Shift and Command key.
- <code><strong>manufacturer</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the manufacturer.
- <code><strong>manufacturerURL</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The URL to the manufacturer.
- <code><strong>unitsPerEm</strong>: integer</code> (`u32`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The number of coordinate units on the em square.
- <code><strong>userData</strong>: object = {}</code> – Custom data associated with the font. See [`userData`](#spec-glyphs-1-userData).
- <code><strong>versionMajor</strong>: integer</code> (`u32`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The major version number of the font.
- <code><strong>versionMinor</strong>: integer</code> (`u32`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The minor version number of the font.
- <code><strong>vertKerning</strong>: object = {}</code> – The vertical kerning of the font. See [`kerning`](#spec-glyphs-1-kerning).
## Definitions

- <code><strong>anchor</strong>: object</code><a name="spec-glyphs-1-anchor"></a> – (`GSAnchor`)
    - <code><strong>name</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the anchor.
    - <code><strong>position</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The position of the anchor. See [`legacyPosition`](#spec-glyphs-1-legacyPosition). Examples: `"{0, 50}"`, `"{-30.5, 600}"`.
- <code><strong>annotation</strong>: object</code><a name="spec-glyphs-1-annotation"></a> – (`GSAnnotation`)
    - <code><strong>angle</strong>: number = 0</code> (`f64`) – The angle of the annotation in degrees clockwise.
    - <code><strong>position</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The position of the annotation. See [`legacyPosition`](#spec-glyphs-1-legacyPosition). Examples: `"{0, 50}"`, `"{-30.5, 600}"`.
    - <code><strong>text</strong>: string = ""</code> – The text of a text-type annotation.
    - <code><strong>type</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The type of the annotation.
        - Possible values: `"Text"`, `"Arrow"`, `"Circle"`, `"Plus"`, `"Minus"`.
    - <code><strong>width</strong>: number = 0</code> (`f64`) – The width of a text- or circle-type annotation.
- <code><strong>attr</strong>: object</code><a name="spec-glyphs-1-attr"></a>
- <code><strong>axis</strong>: object</code><a name="spec-glyphs-1-axis"></a> – (`GSAxis`)
    - <code><strong>default</strong>: number = 0</code> (`f64`) – The default location on the axis.
    - <code><strong>hidden</strong> = false</code> – Whether the axis is considered to be hidden from the font user.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>name</strong>: string = ""</code> – The user-facing name of the axis.
    - <code><strong>tag</strong>: string = ""</code> – The OpenType tag of the axis. Must be unique within the font. The tag may be longer than four characters in which case only the first four characters are considered to be the canonical tag of the axis and the rest is used as a differentiating identifier. On export, the canonical tag is used. Multiple axes with the same canonical tag are useful for higher-order interpolation.
- <code><strong>class</strong>: object</code><a name="spec-glyphs-1-class"></a> – (`GSClass`)
    - <code><strong>automatic</strong> = false</code> – Whether the code of the class is generated automatically.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>code</strong>: string = ""</code> – The code of the class. Note that this code may not just be a whitespace-separated list of glyph names but may also contain comments and other feature code constructs. Examples: `"A B C"`, `"noon-ar noon-ar.fina noon-ar.medi noon-ar.init # noon-ar glyphs"`.
    - <code><strong>disabled</strong> = false</code> – Whether the class is disabled.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>name</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the class. The leading at sign (`@`) is not included. Examples: `"Uppercase"`, `"CombiningTopAccents"`.
    - <code><strong>notes</strong>: string = ""</code> – A string serving as a description or comment about the class.
- <code><strong>color</strong>: array</code><a name="spec-glyphs-1-color"></a> – An RGB color with an alpha channel in the sRGB IEC61966-2.1 color space.
 Tuple with 4 items.
    - <code><strong>#0</strong>: integer</code> (`u8`) – The red color component.
    - <code><strong>#1</strong>: integer</code> (`u8`) – The green color component.
    - <code><strong>#2</strong>: integer</code> (`u8`) – The blue color component.
    - <code><strong>#3</strong>: integer</code> (`u8`) – The alpha color component.
- <code><strong>colorLabel</strong></code><a name="spec-glyphs-1-colorLabel"></a> One of 2 options.
    - Option. `integer` (`u8`) – The index of the color label. See also [the handbook entry on color labels](https://handbook.glyphsapp.com/glyph/#glyph/color-label).
    - Option. `array` – An RGB color with an alpha channel in the sRGB IEC61966-2.1 color space. See [`color`](#spec-glyphs-1-color).
- <code><strong>component</strong>: object</code><a name="spec-glyphs-1-component"></a> – (`GSComponent`)
    - <code><strong>alignment</strong>: integer = 0</code> (`i8`) – (`GSComponentAlignment`) – Controls the automatic alignment of the component. `-1`: disabled (no alignment), `0`: default (alignment is based on context), `1`: force alignment (align regardless of context), `3`: horizontal alignment (align horizontally, but allow for manual vertical placement). One of 4 options.
        - Option. `-1` – Disabled: automatic positioning is disabled.
        - Option. `0` – Default: automatic positioning follows the normal eligibility rules.
        - Option. `1` – Forced: automatic positioning is enabled regardless of normal eligibility.
        - Option. `3` – Horizontal: only the horizontal coordinate is positioned automatically.
    - <code><strong>anchor</strong>: string</code> – The name of the attachment anchor. Set to specify a specific anchor when there are multiple candidates.
    - <code><strong>keepWeight</strong>: number = 0</code> (`f64`) – Unused.
    - <code><strong>locked</strong> = false</code> – Whether the component is locked.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>name</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the component. See `ref` for current format versions.
    - <code><strong>piece</strong>: object = {}</code> – The Smart Component settings of the component, mapping property names to values.
        - <code>string</code> One of 2 options.
            - Option. `number` (`f64`)
            - Option.
                - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the component. See `attr` for current format versions. See [`userData`](#spec-glyphs-1-userData).
    - <code><strong>transform</strong>: string</code> – The transformation matrix of the image (m11, m12, m21, m22, tX, tY). Examples: `"{1, 0, 0, 1, 0, 0}"`, `"{0.5, 0, 0, 0.5, 0, 0}"`.
- <code><strong>customParameter</strong>: object</code><a name="spec-glyphs-1-customParameter"></a> – (`GSCustomParameter`)
    - <code><strong>disabled</strong> = false</code> – Whether the custom parameter is disabled.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>name</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the custom parameter.
    - <code><strong>value</strong></code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The value of the custom parameter.
- <code><strong>displayStrings</strong>: array</code><a name="spec-glyphs-1-displayStrings"></a>
    - <code><strong>#</strong>: string</code>
- <code><strong>featurePrefix</strong>: object</code><a name="spec-glyphs-1-featurePrefix"></a> – (`GSFeaturePrefix`)
    - <code><strong>automatic</strong> = false</code> – Whether the code of the feature prefix is generated automatically.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>code</strong>: string = ""</code> – The code of the feature prefix. Example: `"languagesystem DFLT dflt;"`.
    - <code><strong>disabled</strong> = false</code> – Whether the feature prefix is disabled.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>name</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the feature prefix. Example: `"Languagesystems"`.
    - <code><strong>notes</strong>: string = ""</code> – A string serving as a description or comment about the feature prefix.
- <code><strong>feature</strong>: object</code><a name="spec-glyphs-1-feature"></a> – (`GSFeature`)
    - <code><strong>automatic</strong> = false</code> – Whether the code of the feature is generated automatically.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>code</strong>: string = ""</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The code of the feature. Example: `"sub a by a.alt;"`.
    - <code><strong>disabled</strong> = false</code> – Whether the feature is disabled.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>name</strong>: string</code> – The four-letter tag of the feature. Example: `"calt"`.
    - <code><strong>notes</strong>: string = ""</code> – A string serving as a description or comment about the feature.
- <code><strong>fontMaster</strong>: object</code><a name="spec-glyphs-1-fontMaster"></a> – (`GSFontMaster`)
    - <code><strong>alignmentZones</strong>: array = []</code> – The alignment zones of the master.
        - <code><strong>#</strong>: string</code> Examples: `"{0, -10}"`, `"{700, 16}"`.
    - <code><strong>ascender</strong>: number</code> (`f64`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The ascender metric of the master.
    - <code><strong>capHeight</strong>: number</code> (`f64`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The cap height metric of the master.
    - <code><strong>custom</strong>: string</code> – The custom name of the master.
    - <code><strong>customValue</strong>: number</code> (`f64`) – The location on the custom axis of the master.
    - <code><strong>customValue1</strong>: number</code> (`f64`) – The location on the first custom axis of the master.
    - <code><strong>customValue2</strong>: number</code> (`f64`) – The location on the second custom axis of the master.
    - <code><strong>customValue3</strong>: number</code> (`f64`) – The location on the third custom axis of the master.
    - <code><strong>customParameters</strong>: array = []</code> – The custom parameters of the master.
 See [`customParameter`](#spec-glyphs-1-customParameter) for items.
    - <code><strong>descender</strong>: number</code> (`f64`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The descender metric of the master.
    - <code><strong>guideLines</strong>: array = []</code> – The global guides of the master.
 See [`guide`](#spec-glyphs-1-guide) for items.
    - <code><strong>horizontalStems</strong>: array = []</code> – The horizontal stems of the master.
        - <code><strong>#</strong>: number</code> (`f64`)
    - <code><strong>iconName</strong>: string = "Regular"</code> – The name of the icon that represents the master. Generally omitted when equal to `Regular`, or equal to the default icon name of the master (`GSFontMaster.defaultIconName`). For a list of available names, consult `GSFontMaster.iconNames()`.
    - <code><strong>id</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The unique identifier of the master.
    - <code><strong>italicAngle</strong>: number = 0</code> (`f64`) – The italic angle of the master in degrees clockwise.
    - <code><strong>name</strong>: string</code> – The name of the master. May be omitted in file format version 1 when equal to `Regular` or the default master name.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the master. See [`userData`](#spec-glyphs-1-userData).
    - <code><strong>verticalStems</strong>: array = []</code> – The vertical stems of the master.
        - <code><strong>#</strong>: number</code> (`f64`)
    - <code><strong>visible</strong> = true</code> – Whether the master is visible in the preview.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>weight</strong>: string = "Regular"</code> – The weight name of the master.
    - <code><strong>weightValue</strong>: number</code> (`f64`) – The location on the weight axis of the master.
    - <code><strong>width</strong>: string = "Regular"</code> – The width name of the master.
    - <code><strong>widthValue</strong>: number</code> (`f64`) – The location on the width axis of the master.
    - <code><strong>xHeight</strong>: number</code> (`f64`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The x-height metric of the master.
- <code><strong>glyph</strong>: object</code><a name="spec-glyphs-1-glyph"></a> – (`GSGlyph`)
    - <code><strong>bottomKerningGroup</strong>: string</code> – The bottom kerning group of the glyph.
    - <code><strong>bottomMetricsKey</strong>: string</code> – The bottom metrics key of the glyph.
    - <code><strong>category</strong>: string</code> – The category of the glyph. If unset, then the category is based on a glyph data lookup based on the glyph name.
    - <code><strong>color</strong></code> – The color label of the glyph. See [`colorLabel`](#spec-glyphs-1-colorLabel).
    - <code><strong>export</strong> = true</code> – Whether the glyph is exported.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>glyphname</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the glyph.
    - <code><strong>lastChange</strong>: string</code> – The date and time of the last change of the glyph. Example: `"2023-02-25 14:46:49 +0000"`.
    - <code><strong>layers</strong>: array</code> – The layers of the glyph.
 See [`layer`](#spec-glyphs-1-layer) for items.
    - <code><strong>leftKerningGroup</strong>: string</code> – The left kerning group of the glyph for LTR direction or the right kerning group of the glyph for RTL direction.
    - <code><strong>leftMetricsKey</strong>: string</code> – The left metrics key of the glyph.
    - <code><strong>locked</strong> = false</code> – Whether the glyph is locked.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>note</strong>: string = ""</code> – A string serving as a description or comment about the glyph.
    - <code><strong>partsSettings</strong>: array = []</code> – A list of the Smart Glyph properties and their top/bottom values.
 See [`partProperty`](#spec-glyphs-1-partProperty) for items.
    - <code><strong>production</strong>: string</code> – The production name of the glyph. If unset, then the production name is based on a glyph data lookup based on the glyph name or the Unicode code point.
    - <code><strong>rightKerningGroup</strong>: string</code> – The right kerning group of the glyph for LTR direction or the left kerning group of the glyph for RTL direction.
    - <code><strong>rightMetricsKey</strong>: string</code> – The right metrics key of the glyph.
    - <code><strong>script</strong>: string</code> – The script of the glyph. If unset, then the script is based on a glyph data lookup based on the glyph name.
    - <code><strong>subCategory</strong>: string</code> – The subcategory of the glyph. If unset, then the subcategory is based on a glyph data lookup based on the glyph name.
    - <code><strong>topKerningGroup</strong>: string</code> – The top kerning group of the glyph.
    - <code><strong>topMetricsKey</strong>: string</code> – The top metrics key of the glyph.
    - <code><strong>unicode</strong></code> – The Unicode code points of the glyph. One of 2 options.
        - Option. `string` – A comma-separated list of hexadecimal code point values. Examples: `"0041"`, `"1E900"`, `"0000"`, `"0041,0061"`.
        - Option. `integer` (`u32`) – A code point encoded as a hexadecimal number and decoded as a decimal number. This is a syntax issue in version 1 files where a hexadecimal value encoded as an unquoted string can be ambiguous.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the glyph. See [`userData`](#spec-glyphs-1-userData).
    - <code><strong>vertWidthMetricsKey</strong>: string</code> – The vertical width metrics key of the glyph.
    - <code><strong>widthMetricsKey</strong>: string</code> – The width metrics key of the glyph.
- <code><strong>guide</strong>: object</code><a name="spec-glyphs-1-guide"></a> – (`GSGuide`)
    - <code><strong>alignment</strong>: string = "left"</code> – The alignment of the guide. Renamed to `orientation` in later versions. See [`orientation`](#spec-glyphs-1-orientation).
        - Possible values: `"left"`, `"center"`, `"right"`.
    - <code><strong>angle</strong>: number = 0</code> (`f64`) – The angle at which the guide is drawn in degrees clockwise.
    - <code><strong>filter</strong>: string</code> – The filter of the guide. The syntax is the description of [NSPredicate](https://developer.apple.com/documentation/foundation/nspredicate). Omitted when no filter is defined.
    - <code><strong>grid</strong>: number = 0</code> (`f64`) – The grid of the guide.
    - <code><strong>length</strong>: number = 0</code> (`f64`) – The length of a line-type guide.
    - <code><strong>lockAngle</strong> = false</code> – Whether the angle of the guide is locked.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>locked</strong> = false</code> – Whether the guide is locked.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>name</strong>: string = ""</code> – The name of the guide.
    - <code><strong>position</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The position of the guide. See [`legacyPosition`](#spec-glyphs-1-legacyPosition). Examples: `"{0, 50}"`, `"{-30.5, 600}"`.
    - <code><strong>showMeasurement</strong> = false</code> – Whether the measurement of the guide is shown.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
- <code><strong>hint</strong>: object</code><a name="spec-glyphs-1-hint"></a> – (`GSHint`)
    - <code><strong>horizontal</strong> = false</code> – Whether the hint is horizontal. Not written for path components.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>name</strong>: string</code> – The name of the hint.
    - <code><strong>options</strong>: number = 0</code> (`u32`) – The options of the hint.
    - <code><strong>origin</strong>: string</code> – The origin of the hint. See [`indexPath`](#spec-glyphs-1-indexPath). Examples: `"{0, 1}"`, `"{lsb}"`, `"{rsb}"`.
    - <code><strong>other1</strong>: string</code> – The first other point of the hint, used by TrueType instructions that need more than two nodes. See [`indexPath`](#spec-glyphs-1-indexPath). Examples: `"{0, 1}"`, `"{lsb}"`, `"{rsb}"`.
    - <code><strong>other2</strong>: string</code> – The second other point of the hint, used by TrueType instructions that need more than three nodes. See [`indexPath`](#spec-glyphs-1-indexPath). Examples: `"{0, 1}"`, `"{lsb}"`, `"{rsb}"`.
    - <code><strong>place</strong>: string</code> See [`legacyPosition`](#spec-glyphs-1-legacyPosition). Examples: `"{0, 50}"`, `"{-30.5, 600}"`.
    - <code><strong>scale</strong>: string = "{1, 1}"</code> – The scale of the hint. Examples: `"{2, 2}"`, `"{1.2, 1.2}"`.
    - <code><strong>settings</strong>: object</code> – The settings of the hint.
    - <code><strong>stem</strong>: number</code> (`i32`) – The stem of the hint.
    - <code><strong>target</strong>: string</code> See [`indexPath`](#spec-glyphs-1-indexPath). Examples: `"{0, 1}"`, `"{lsb}"`, `"{rsb}"`.
    - <code><strong>type</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The type of the hint.
        - Possible values: `"TopGhost"`, `"BottomGhost"`, `"Stem"`, `"Flex"`, `"TTStem"`, `"Align"`, `"Anchor"`, `"Interpolate"`, `"Diagonal"`, `"Delta"`, `"Tag"`, `"Corner"`, `"Cap"`, `"Brush"`, `"Segment"`, `"Auto"`, `"Unknown"`.
- <code><strong>image</strong>: object</code><a name="spec-glyphs-1-image"></a> – (`GSImage`)
    - <code><strong>alpha</strong>: number = 50</code> (`f64`) – The alpha value of the image.
    - <code><strong>crop</strong>: string</code> – The cropped frame of the image, specified as the crop origin X/Y and size width/height. Examples: `"{{0, 0}, {100, 100}}"`, `"{{-10, -10}, {90, 90}}"`.
    - <code><strong>imagePath</strong>: string</code> – The file path of the image file relative to the document file.
    - <code><strong>imageURL</strong>: string</code> – The URL bookmark data of the image file path.
    - <code><strong>locked</strong> = false</code> – Whether the image is locked.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>transform</strong>: string</code> – The transformation matrix of the image (m11, m12, m21, m22, tX, tY). Examples: `"{1, 0, 0, 1, 0, 0}"`, `"{0.5, 0, 0, 0.5, 0, 0}"`.
- <code><strong>instance</strong>: object</code><a name="spec-glyphs-1-instance"></a> – (`GSInstance`)
    - <code><strong>axesValues</strong>: array</code> – The internal axis locations of the instance. These values are also used for the external axis locations, if no external axis locations are specified separately.
        - <code><strong>#</strong>: number</code> (`f64`)
    - <code><strong>customParameters</strong>: array = []</code> – The custom parameters of the instance.
 See [`customParameter`](#spec-glyphs-1-customParameter) for items.
    - <code><strong>exports</strong> = true</code> – Whether the instance is exported.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>interpolationCustom</strong>: number</code> (`f64`) – The interpolation value of the third axis.
    - <code><strong>interpolationCustom1</strong>: number</code> (`f64`) – The interpolation value of the fourth axis.
    - <code><strong>interpolationCustom2</strong>: number</code> (`f64`) – The interpolation value of the fifth axis.
    - <code><strong>interpolationCustom3</strong>: number</code> (`f64`) – The interpolation value of the sixth axis.
    - <code><strong>interpolationWeight</strong>: number</code> (`f64`) – The interpolation value of the weight axis (first axis).
    - <code><strong>interpolationWidth</strong>: number</code> (`f64`) – The interpolation value of the width axis (second axis).
    - <code><strong>instanceInterpolations</strong>: object = {}</code> – The interpolation factors where the keys are the master IDs.
        - <code>string</code> One of 2 options.
            - Option. `number` (`f64`) – The X and Y factors are the same.
            - Option. `string` Examples: `"{1, 1}"`, `"{0.5, 0.5}"`.
    - <code><strong>isBold</strong> = false</code> – Whether the instance is bold.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>isItalic</strong> = false</code> – Whether the instance is italic.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>linkStyle</strong>: string</code> – The name of the style-linked instance.
    - <code><strong>manualInterpolation</strong> = false</code> – Whether the `instanceInterpolations` values are used. Otherwise, the values are calculated from the axis values.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>name</strong>: string</code> – The style name of the instance. Examples: `"Regular"`, `"Bold"`, `"Italic"`, `"Bold Italic"`.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the instance. See [`userData`](#spec-glyphs-1-userData).
    - <code><strong>weightClass</strong>: string = "Regular"</code> – The weight class of the instance.
        - Possible values: `"Thin"`, `"ExtraLight"`, `"Light"`, `"Regular"`, `"Medium"`, `"SemiBold"`, `"Bold"`, `"ExtraBold"`, `"Black"`.
    - <code><strong>widthClass</strong>: string = "Medium (normal)"</code> – The width class of the instance.
        - Possible values: `"Ultra Condensed"`, `"Extra Condensed"`, `"Condensed"`, `"SemiCondensed"`, `"Medium (normal)"`, `"Medium"`, `"Semi Expanded"`, `"Expanded"`, `"Extra Expanded"`, `"Ultra Expanded"`.
- <code><strong>indexPath</strong>: string</code><a name="spec-glyphs-1-indexPath"></a> Examples: `"{0, 1}"`, `"{lsb}"`, `"{rsb}"`.
- <code><strong>kerning</strong>: object = {}</code><a name="spec-glyphs-1-kerning"></a> – Maps master IDs to kerning definitions.
    - <code>string: object</code> – Maps glyph names or class names to kerning partners.
        - <code>string: object</code> – Maps glyph names or class names to kerning values.
            - <code>string: number</code> (`f64`)
- <code><strong>layer</strong>: object</code><a name="spec-glyphs-1-layer"></a> – (`GSLayer`)
    - <code><strong>anchors</strong>: array = []</code> – The anchors of the layer.
 See [`anchor`](#spec-glyphs-1-anchor) for items.
    - <code><strong>annotations</strong>: array = []</code> – The annotations of the layer.
 See [`annotation`](#spec-glyphs-1-annotation) for items.
    - <code><strong>associatedMasterId</strong>: string</code> – The unique identifier of the associated master. Omitted when equal to the layer ID.
    - <code><strong>background</strong>: object</code>
        - <code><strong>anchors</strong>: array = []</code> – The anchors of the background layer.
 See [`anchor`](#spec-glyphs-1-anchor) for items.
        - <code><strong>annotations</strong>: array = []</code> – The annotations of the background layer.
 See [`annotation`](#spec-glyphs-1-annotation) for items.
        - <code><strong>backgroundImage</strong>: object</code> – The background image of the layer. See [`image`](#spec-glyphs-1-image).
        - <code><strong>components</strong>: array = []</code> – The components of the background layer.
 See [`component`](#spec-glyphs-1-component) for items.
        - <code><strong>guideLines</strong>: array = []</code> – The guides of the background layer.
 See [`guide`](#spec-glyphs-1-guide) for items.
        - <code><strong>hints</strong>: array = []</code> – The hints of the background layer.
 See [`hint`](#spec-glyphs-1-hint) for items.
        - <code><strong>paths</strong>: array = []</code> – The paths of the background layer.
 See [`path`](#spec-glyphs-1-path) for items.
    - <code><strong>backgroundImage</strong>: object</code> – The background image of the layer. See [`image`](#spec-glyphs-1-image).
    - <code><strong>color</strong></code> – The color label of the layer. See [`colorLabel`](#spec-glyphs-1-colorLabel).
    - <code><strong>components</strong>: array = []</code> – The components of the layer.
 See [`component`](#spec-glyphs-1-component) for items.
    - <code><strong>guideLines</strong>: array = []</code> – The guides of the layer.
 See [`guide`](#spec-glyphs-1-guide) for items.
    - <code><strong>hints</strong>: array = []</code> – The hints of the layer.
 See [`hint`](#spec-glyphs-1-hint) for items.
    - <code><strong>layerId</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The unique ID of the layer. Matches the master ID when the layer is a master layer.
    - <code><strong>leftMetricsKey</strong>: string</code> – The left metrics key of the layer.
    - <code><strong>rightMetricsKey</strong>: string</code> – The right metrics key of the layer.
    - <code><strong>widthMetricsKey</strong>: string</code> – The width metrics key of the layer.
    - <code><strong>name</strong>: string = ""</code> – The name of the layer. Master layers and other special layers display a name in the Glyphs UI that is derived from the layer’s role (for example, the name of the master that the layer belongs to). These derived names are not written to the file. Instead, this name is only displayed in the UI for non-special layers (like backup layers).
    - <code><strong>paths</strong>: array = []</code> – The paths of the layer.
 See [`path`](#spec-glyphs-1-path) for items.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the layer. See [`userData`](#spec-glyphs-1-userData).
    - <code><strong>visible</strong> = false</code> – Whether the layer is visible.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>width</strong>: number</code> (`f64`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The width of the layer.
- <code><strong>legacyPosition</strong>: string</code><a name="spec-glyphs-1-legacyPosition"></a> Examples: `"{0, 50}"`, `"{-30.5, 600}"`.
- <code><strong>metric</strong>: object</code><a name="spec-glyphs-1-metric"></a> – (`GSMetric`)
    - <code><strong>filter</strong>: string</code> – The filter of the metric limiting the scope of the metric to a subset of glyphs.
    - <code><strong>horizontal</strong> = false</code> – Whether the metric is a horizontal metric.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>name</strong>: string</code> – The name of the metric.
    - <code><strong>type</strong>: string</code> – The type of the metric.
        - Possible values: `"ascender"`, `"cap height"`, `"slant height"`, `"x-height"`, `"midHeight"`, `"bodyHeight"`, `"descender"`, `"baseline"`, `"italic angle"`, `"italic slope"`.
- <code><strong>metricStore</strong>: object</code><a name="spec-glyphs-1-metricStore"></a> – (`GSMetricStore`)
    - <code><strong>over</strong>: number = 0</code> (`f64`) – The overshoot of the metric value.
    - <code><strong>pos</strong>: number = 0</code> (`f64`) – The offset from the baseline of the metric value.
- <code><strong>node</strong>: string</code><a name="spec-glyphs-1-node"></a> – (`GSNode`) Examples: `"0 0 MOVE"`, `"-50 100 LINE"`, `"100 100 CURVE SMOOTH"`, `"200 -60 OFFCURVE"`.
- <code><strong>infoProperty</strong></code><a name="spec-glyphs-1-infoProperty"></a> – (`GSInfoProperty`) One of 2 options.
    - Option. `object`
        - <code><strong>key</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The key of the property.
        - <code><strong>value</strong></code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The value of the property.
    - Option. `object`
        - <code><strong>key</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The key of the property.
        - <code><strong>values</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The values of the property.
 See [`infoValue`](#spec-glyphs-1-infoValue) for items.
- <code><strong>infoValue</strong>: object</code><a name="spec-glyphs-1-infoValue"></a> – (`GSInfoValue`)
    - <code><strong>language</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The language tag of the string value. The tag is based on the [OpenType Language System Tags](https://learn.microsoft.com/en-us/typography/opentype/spec/languagetags) but omits trailing whitespace. Examples: `"dflt"`, `"DEU"`.
    - <code><strong>value</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The localized string value.
- <code><strong>orientation</strong>: string</code><a name="spec-glyphs-1-orientation"></a> – (`GSElementOrientation`)
    - Possible values: `"left"`, `"center"`, `"right"`.
- <code><strong>partProperty</strong>: object</code><a name="spec-glyphs-1-partProperty"></a> – (`GSPartProperty`)
    - <code><strong>bottomName</strong>: string</code> – The name of the bottom value of the property. (Unused)
    - <code><strong>bottomValue</strong>: integer</code> (`i32`) – The lower end of the value range of the property.
    - <code><strong>name</strong>: string</code> – The name of the property.
    - <code><strong>topName</strong>: string</code> – The name of the top value of the property. (Unused)
    - <code><strong>topValue</strong>: integer</code> (`i32`) – The upper end of the value range of the property.
- <code><strong>palettes</strong></code><a name="spec-glyphs-1-palettes"></a> – (`GSPalettes`)
- <code><strong>path</strong>: object</code><a name="spec-glyphs-1-path"></a> – (`GSPath`)
    - <code><strong>closed</strong></code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – Whether the path is closed.
        - Possible values: `0`, `"0"`, `1`, `"1"`.
    - <code><strong>nodes</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The on- and off-curve nodes of the path.
 See [`node`](#spec-glyphs-1-node) for items.
- <code><strong>pos</strong>: array</code><a name="spec-glyphs-1-pos"></a>
 Tuple with 2 items.
    - <code><strong>#0</strong>: number</code> (`f64`) – The x-coordinate of the position.
    - <code><strong>#1</strong>: number</code> (`f64`) – The y-coordinate of the position.
- <code><strong>scale</strong>: array</code><a name="spec-glyphs-1-scale"></a>
 Tuple with 2 items.
    - <code><strong>#0</strong>: number</code> (`f64`) – The horizontal scale factor.
    - <code><strong>#1</strong>: number</code> (`f64`) – The vertical scale factor.
- <code><strong>shape</strong></code><a name="spec-glyphs-1-shape"></a> – (`GSShape`) One of 2 options.
    - Option. `object` See [`path`](#spec-glyphs-1-path).
    - Option. `object` See [`component`](#spec-glyphs-1-component).
- <code><strong>size</strong>: array</code><a name="spec-glyphs-1-size"></a>
 Tuple with 2 items.
    - <code><strong>#0</strong>: number</code> (`f64`) – The width.
    - <code><strong>#1</strong>: number</code> (`f64`) – The height.
- <code><strong>slant</strong>: array</code><a name="spec-glyphs-1-slant"></a>
 Tuple with 2 items.
    - <code><strong>#0</strong>: number</code> (`f64`) – The horizontal slant factor.
    - <code><strong>#1</strong>: number</code> (`f64`) – The vertical slant factor.
- <code><strong>userData</strong>: object</code><a name="spec-glyphs-1-userData"></a>

## Changes

### 10. July 2025

- Add descriptions to `GSComponentAlignment`.

### 14. Jan. 2025

- Reworked JSON Schemas and added variants for package and autosave files.
- Expanded descriptions and annotations for most values.

### 1. Oct. 2018:

- Add Notes about special cases
- Better general explanation

### 21. April 2018:

- Add .appVersion, disablesNiceNames, customValue, weight, width, custom
- Fix typos: paths, widthValue

### 4. Feb. 2016:

- added hints
- updated and added a few field in layers
