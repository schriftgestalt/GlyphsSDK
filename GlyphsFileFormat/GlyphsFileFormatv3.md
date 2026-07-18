# Glyphs File Format, Version 3

## File Format Flavors

There are two flavors of the Glyphs file format.

### Single File (.glyphs)

A single file which contains all the data of a font source.

### Package (.glyphspackage)

The package format contains the same data as the single file format, but split into multiple files.
This format uses a bundle structure, where a directory ending in `.glyphspackage` is presented by macOS as a regular file.
Step inside such a bundle by choosing “Show Package Contents” from the context menu in Finder.
Inside this directory, there are the following files:

- `fontinfo.plist` – The main file containing the font data.
- `order.plist` – A file containing the glyph names in their order. An array of strings.
- `UIState.plist` – A file containing the display strings. A dictionary with a `displayStrings` key following the [`displayStrings` schema](#spec-glyphs-3-displayStrings).
- `glyphs/*.glyph` – Individual files for each glyph. The files follow the [`glyph` schema](#spec-glyphs-3-glyph).

Glyphs saves its source files in a plain-text format.
This way, files can be viewed and edited in any text editor.

## File Format Details

- The file format is based on OpenStep Property Lists (also known as NeXTSTEP, ASCII, or old-style Property Lists).
- This format can be converted to JSON for validation against a JSON Schema.
- The file contents are UTF-8 encoded.
- In addition to the four core data types (dictionary, array, string, and data), Glyphs uses unquoted strings to represent numbers (integers, floats, and booleans).
  Booleans are encoded as `1` (true) and `0` (false). 
  Strings that look like numbers are always encoded in quotes.
- Whitespace is restricted to ASCII spaces, line feeds, and horizontal tabs.
- No comments (like `// ...` or `/* .... */`) are present.
- Indentation, while allowed, is generally omitted to reduce file size.
- Dictionaries and arrays are generally broken onto lines such that each key or element starts on a new line.
  When empty, they span two lines, one for the opening and one for the closing bracket.
- Some arrays are encoded on a single line for better readability and to reduce file size.
  These are mostly arrays used as tuples like points with X/Y coordinates.
  The `glyphsCompact` attribute in the JSON Schema indicates that the array is encoded on a single line.
- Dictionary keys are sorted alphabetically.
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

- [glyphs-3.schema.json](https://github.com/schriftgestalt/GlyphsSDK/blob/Glyphs3/GlyphsFileFormat/Schemas/glyphs-3.schema.json)
- [glyphs-autosave-3.schema.json](https://github.com/schriftgestalt/GlyphsSDK/blob/Glyphs3/GlyphsFileFormat/Schemas/glyphs-autosave-3.schema.json)
- [fontinfo-3.schema.json](https://github.com/schriftgestalt/GlyphsSDK/blob/Glyphs3/GlyphsFileFormat/Schemas/fontinfo-3.schema.json)
- [fontinfo-autosave-3.schema.json](https://github.com/schriftgestalt/GlyphsSDK/blob/Glyphs3/GlyphsFileFormat/Schemas/fontinfo-autosave-3.schema.json)

## Document

- <code><strong>.appVersion</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The build number of Glyphs used to save the file. Example: `"4012"`.
- <code><strong>.formatVersion</strong>: integer = 3</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The version of the file format. If unset, the file is considered to be version 1 as used by Glyphs 1 and Glyphs 2.
- <code><strong>DisplayStrings</strong>: array = []</code> – The strings of the Edit View tabs. Omitted when the `Write DisplayStrings` custom parameter is set to false. Omitted and written as `displayStrings` to `UIState.plist` in case of a package file. See [`displayStrings`](#spec-glyphs-3-displayStrings).
- <code><strong>axes</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The designspace variation axes of the font.
 See [`axis`](#spec-glyphs-3-axis) for items.
- <code><strong>classes</strong>: array = []</code> – The OpenType layout classes of the font.
 See [`class`](#spec-glyphs-3-class) for items.
- <code><strong>customParameters</strong>: array = []</code> – The custom parameters of the font.
 See [`customParameter`](#spec-glyphs-3-customParameter) for items.
- <code><strong>date</strong>: string</code> – The moment in time that is used as the creation date of exported font files including date, time, and timezone. Example: `"2026-07-17 03:14:15 +0000"`.
- <code><strong>familyName</strong>: string</code> – The font family name. Corresponds to the default value of the `familyNames` property.
- <code><strong>featurePrefixes</strong>: array = []</code> – The OpenType layout feature prefixes of the font.
 See [`featurePrefix`](#spec-glyphs-3-featurePrefix) for items.
- <code><strong>features</strong>: array = []</code> – The OpenType layout features of the font.
 See [`feature`](#spec-glyphs-3-feature) for items.
- <code><strong>fontMaster</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The masters of the font.
 Min count: 1.
 See [`fontMaster`](#spec-glyphs-3-fontMaster) for items.
- <code><strong>glyphs</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The glyphs of the font. The order is used on export unless the `glyphOrder` custom parameter is set.
 See [`glyph`](#spec-glyphs-3-glyph) for items.
- <code><strong>instances</strong>: array = []</code> – The instances of the font.
 See [`instance`](#spec-glyphs-3-instance) for items.
- <code><strong>kerningLTR</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The left-to-right kerning of the font. See [`kerning`](#spec-glyphs-3-kerning).
- <code><strong>kerningRTL</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The right-to-left kerning of the font. See [`kerning`](#spec-glyphs-3-kerning).
- <code><strong>kerningVertical</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The vertical kerning of the font. See [`kerning`](#spec-glyphs-3-kerning).
- <code><strong>metrics</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The metrics of the font.
 See [`metric`](#spec-glyphs-3-metric) for items.
- <code><strong>note</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The note about the font.
- <code><strong>numbers</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The numbers of the font.
 See [`metric`](#spec-glyphs-3-metric) for items.
- <code><strong>properties</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The properties of the font.
 See [`infoProperty`](#spec-glyphs-3-infoProperty) for items.
- <code><strong>settings</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center">
    - <code><strong>disablesAutomaticAlignment</strong>: boolean = false</code> – Whether automatic alignment of components is disabled.
    - <code><strong>disablesNiceNames</strong>: boolean = false</code> – Whether to use production names instead of nice names.
    - <code><strong>gridLength</strong>: integer = 1</code> (`u32`) – The main grid length.
    - <code><strong>gridSubDivision</strong>: integer = 1</code> (`u32`) – The grid sub-division size.
    - <code><strong>keepAlternatesTogether</strong>: boolean = false</code> – Whether to keep alternates glyphs together in Font View.
    - <code><strong>keyboardIncrement</strong>: number = 1</code> (`f32`) – The standard keyboard increment.
    - <code><strong>keyboardIncrementBig</strong>: number = 10</code> (`f32`) – The keyboard increment when holding the Shift key.
    - <code><strong>keyboardIncrementHuge</strong>: number = 100</code> (`f32`) – The keyboard increment when holding both the Shift and Command key.
    - <code><strong>previewRemoveOverlap</strong>: boolean = false</code> – Whether to preview the effect of the Remove Overlaps filter in Edit View.
    - <code><strong>snapToObjects</strong>: boolean = false</code> – Whether snapping is enabled in Edit View.
    - <code><strong>fontType</strong>: string = "default"</code> – The type of the font.
        - Possible values: `"default"`, `"variable"`, `"layerFont"`, `"iconSet"`.
- <code><strong>stems</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The stems of the font.
 See [`metric`](#spec-glyphs-3-metric) for items.
- <code><strong>unitsPerEm</strong>: integer</code> (`u32`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The number of coordinate units on the em square.
- <code><strong>userData</strong>: object = {}</code> – Custom data associated with the font. See [`userData`](#spec-glyphs-3-userData).
- <code><strong>versionMajor</strong>: integer</code> (`u32`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The major version number of the font.
- <code><strong>versionMinor</strong>: integer</code> (`u32`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The minor version number of the font.
## Definitions

- <code><strong>anchor</strong>: object</code><a name="spec-glyphs-3-anchor"></a> – (`GSAnchor`)
    - <code><strong>locked</strong>: boolean = false</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Whether the anchor is locked.
    - <code><strong>name</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the anchor.
    - <code><strong>orientation</strong>: string = "left"</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The orientation of the anchor. See [`orientation`](#spec-glyphs-3-orientation).
        - Possible values: `"left"`, `"center"`, `"right"`.
    - <code><strong>pos</strong>: array = [0, 0]</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The position of the anchor. See [`pos`](#spec-glyphs-3-pos).
    - <code><strong>userData</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Custom data associated with the anchor. See [`userData`](#spec-glyphs-3-userData).
- <code><strong>annotation</strong>: object</code><a name="spec-glyphs-3-annotation"></a> – (`GSAnnotation`)
    - <code><strong>angle</strong>: number = 0</code> (`f64`) – The angle of the annotation in degrees clockwise.
    - <code><strong>pos</strong>: array = [0, 0]</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The position of the annotation. See [`pos`](#spec-glyphs-3-pos).
    - <code><strong>text</strong>: string = ""</code> – The text of a text-type annotation.
    - <code><strong>type</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The type of the annotation.
        - Possible values: `"Text"`, `"Arrow"`, `"Circle"`, `"Plus"`, `"Minus"`.
    - <code><strong>width</strong>: number = 0</code> (`f64`) – The width of a text- or circle-type annotation.
- <code><strong>attr</strong>: object</code><a name="spec-glyphs-3-attr"></a>
- <code><strong>axis</strong>: object</code><a name="spec-glyphs-3-axis"></a> – (`GSAxis`)
    - <code><strong>default</strong>: number = 0</code> (`f64`) – The default location on the axis.
    - <code><strong>hidden</strong>: boolean = false</code> – Whether the axis is considered to be hidden from the font user.
    - <code><strong>name</strong>: string = ""</code> – The user-facing name of the axis.
    - <code><strong>tag</strong>: string = ""</code> – The OpenType tag of the axis. Must be unique within the font. The tag may be longer than four characters in which case only the first four characters are considered to be the canonical tag of the axis and the rest is used as a differentiating identifier. On export, the canonical tag is used. Multiple axes with the same canonical tag are useful for higher-order interpolation.
- <code><strong>class</strong>: object</code><a name="spec-glyphs-3-class"></a> – (`GSClass`)
    - <code><strong>automatic</strong>: boolean = false</code> – Whether the code of the class is generated automatically.
    - <code><strong>code</strong>: string = ""</code> – The code of the class. Note that this code may not just be a whitespace-separated list of glyph names but may also contain comments and other feature code constructs. Examples: `"A B C"`, `"noon-ar noon-ar.fina noon-ar.medi noon-ar.init # noon-ar glyphs"`.
    - <code><strong>disabled</strong>: boolean = false</code> – Whether the class is disabled.
    - <code><strong>name</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the class. The leading at sign (`@`) is not included. Examples: `"Uppercase"`, `"CombiningTopAccents"`.
    - <code><strong>notes</strong>: string = ""</code> – A string serving as a description or comment about the class.
- <code><strong>color</strong></code><a name="spec-glyphs-3-color"></a> One of 4 options.
    - Option. `array` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – A legacy color reference into the version 3 `Color Palettes` custom parameter, written with an 8-bit alpha factor.
 Tuple with 3 items.
        - <code><strong>#0</strong>: string = "p"</code> – Indicates a palette color reference.
        - <code><strong>#1</strong>: integer</code> (`u16`) – The color palette entry index.
        - <code><strong>#2</strong>: integer = 255</code> (`u8`) – The alpha factor applied to the referenced palette color.
    - Option. `array` – An RGB color with an alpha channel in the sRGB IEC61966-2.1 color space.
 Tuple with 4 items.
        - <code><strong>#0</strong>: integer</code> (`u8`) – The red color component.
        - <code><strong>#1</strong>: integer</code> (`u8`) – The green color component.
        - <code><strong>#2</strong>: integer</code> (`u8`) – The blue color component.
        - <code><strong>#3</strong>: integer</code> (`u8`) – The alpha color component.
    - Option. `array` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – A gray color with an alpha channel in a perceptual generic gray color space with γ = 2.2.
 Tuple with 2 items.
        - <code><strong>#0</strong>: integer</code> (`u8`) – The gray value from `0` (black) to `255` (white).
        - <code><strong>#1</strong>: integer</code> (`u8`) – The alpha color component.
    - Option. `array` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – A CMYK color with an alpha channel. The color space is device-dependent.
 Tuple with 5 items.
        - <code><strong>#0</strong>: integer</code> (`u8`) – The cyan color component.
        - <code><strong>#1</strong>: integer</code> (`u8`) – The magenta color component.
        - <code><strong>#2</strong>: integer</code> (`u8`) – The yellow color component.
        - <code><strong>#3</strong>: integer</code> (`u8`) – The black color component.
        - <code><strong>#4</strong>: integer</code> (`u8`) – The alpha color component.
- <code><strong>colorLabel</strong></code><a name="spec-glyphs-3-colorLabel"></a> One of 2 options.
    - Option. `integer` (`u8`) – The index of the color label. See also [the handbook entry on color labels](https://handbook.glyphsapp.com/glyph/#glyph/color-label).
    - Option. See [`color`](#spec-glyphs-3-color).
- <code><strong>component</strong>: object</code><a name="spec-glyphs-3-component"></a> – (`GSComponent`)
    - <code><strong>alignment</strong>: integer = 0</code> (`i8`) – (`GSComponentAlignment`) – Controls the automatic alignment of the component. `-1`: disabled (no alignment), `0`: default (alignment is based on context), `1`: force alignment (align regardless of context), `3`: horizontal alignment (align horizontally, but allow for manual vertical placement). One of 4 options.
        - Option. `-1` – Disabled: automatic positioning is disabled.
        - Option. `0` – Default: automatic positioning follows the normal eligibility rules.
        - Option. `1` – Forced: automatic positioning is enabled regardless of normal eligibility.
        - Option. `3` – Horizontal: only the horizontal coordinate is positioned automatically.
    - <code><strong>anchor</strong>: string</code> – The name of the attachment anchor. Set to specify a specific anchor when there are multiple candidates.
    - <code><strong>angle</strong>: number = 0</code> (`f64`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The rotation angle of the component in degrees clockwise.
    - <code><strong>attr</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The attributes of the component. See [`shapeAttr`](#spec-glyphs-3-shapeAttr).
    - <code><strong>keepWeight</strong>: number = 0</code> (`f64`) – Unused.
    - <code><strong>locked</strong>: boolean = false</code> – Whether the component is locked.
    - <code><strong>masterId</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The ID of the master from which the component is derived.
    - <code><strong>orientation</strong>: integer = 0</code> (`i8`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – (`GSElementOrientation`) – The orientation of the component. One of 3 options.
        - Option. `0` – Left: x values are relative to the left edge of the layer box.
        - Option. `1` – Right: x values are relative to the right edge of the layer box.
        - Option. `2` – Center: x values are relative to the center of the layer box.
    - <code><strong>piece</strong>: object = {}</code> – The Smart Component settings of the component, mapping property names to values.
        - <code>string</code> One of 2 options.
            - Option. `number` (`f64`)
            - Option. `integer`
    - <code><strong>pos</strong>: array = [0, 0]</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The position (translation transform) of the component. See [`pos`](#spec-glyphs-3-pos).
    - <code><strong>ref</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The name of the referenced glyph.
    - <code><strong>scale</strong>: array = [1, 1]</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The scale transform of the component. See [`scale`](#spec-glyphs-3-scale).
    - <code><strong>slant</strong>: array = [0, 0]</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The slant transform of the component. See [`slant`](#spec-glyphs-3-slant).
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the component. See `attr` for current format versions. See [`userData`](#spec-glyphs-3-userData).
- <code><strong>customParameter</strong>: object</code><a name="spec-glyphs-3-customParameter"></a> – (`GSCustomParameter`)
    - <code><strong>disabled</strong>: boolean = false</code> – Whether the custom parameter is disabled.
    - <code><strong>name</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the custom parameter.
    - <code><strong>value</strong></code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The value of the custom parameter.
- <code><strong>displayStrings</strong>: array</code><a name="spec-glyphs-3-displayStrings"></a>
    - <code><strong>#</strong>: string</code>
- <code><strong>featurePrefix</strong>: object</code><a name="spec-glyphs-3-featurePrefix"></a> – (`GSFeaturePrefix`)
    - <code><strong>automatic</strong>: boolean = false</code> – Whether the code of the feature prefix is generated automatically.
    - <code><strong>code</strong>: string = ""</code> – The code of the feature prefix. Example: `"languagesystem DFLT dflt;"`.
    - <code><strong>disabled</strong>: boolean = false</code> – Whether the feature prefix is disabled.
    - <code><strong>name</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the feature prefix. Example: `"Languagesystems"`.
    - <code><strong>notes</strong>: string = ""</code> – A string serving as a description or comment about the feature prefix.
- <code><strong>feature</strong>: object</code><a name="spec-glyphs-3-feature"></a> – (`GSFeature`)
    - <code><strong>automatic</strong>: boolean = false</code> – Whether the code of the feature is generated automatically.
    - <code><strong>code</strong>: string = ""</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The code of the feature. Example: `"sub a by a.alt;"`.
    - <code><strong>disabled</strong>: boolean = false</code> – Whether the feature is disabled.
    - <code><strong>labels</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The labels of the feature.
 See [`infoValue`](#spec-glyphs-3-infoValue) for items.
    - <code><strong>notes</strong>: string = ""</code> – A string serving as a description or comment about the feature.
    - <code><strong>tag</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The four-letter tag of the feature. Example: `"calt"`.
- <code><strong>fontMaster</strong>: object</code><a name="spec-glyphs-3-fontMaster"></a> – (`GSFontMaster`)
    - <code><strong>axesValues</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The designspace location of the master.
        - <code><strong>#</strong>: number</code> (`f64`)
    - <code><strong>customParameters</strong>: array = []</code> – The custom parameters of the master.
 See [`customParameter`](#spec-glyphs-3-customParameter) for items.
    - <code><strong>guides</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The global guides of the master.
 See [`guide`](#spec-glyphs-3-guide) for items.
    - <code><strong>iconName</strong>: string = "Regular"</code> – The name of the icon that represents the master. Generally omitted when equal to `Regular`, or equal to the default icon name of the master (`GSFontMaster.defaultIconName`). For a list of available names, consult `GSFontMaster.iconNames()`.
    - <code><strong>id</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The unique identifier of the master.
    - <code><strong>metricValues</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The metric values of the master.
 See [`metricStore`](#spec-glyphs-3-metricStore) for items.
    - <code><strong>name</strong>: string</code> – The name of the master. May be omitted in file format version 1 when equal to `Regular` or the default master name.
    - <code><strong>numberValues</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The number values of the master.
        - <code><strong>#</strong>: number</code> (`f64`)
    - <code><strong>properties</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The properties of the master.
 See [`infoProperty`](#spec-glyphs-3-infoProperty) for items.
    - <code><strong>stemValues</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The stem values of the master.
        - <code><strong>#</strong>: number</code> (`f64`)
    - <code><strong>tempData</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Auto-save files only: Temporary data associated with the master. See [`userData`](#spec-glyphs-3-userData).
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the master. See [`userData`](#spec-glyphs-3-userData).
    - <code><strong>visible</strong>: boolean = true</code> – Whether the master is visible in the preview.
- <code><strong>glyph</strong>: object</code><a name="spec-glyphs-3-glyph"></a> – (`GSGlyph`)
    - <code><strong>case</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The case of the glyph. If unset, then the case is based on a glyph data lookup based on the glyph name.
        - Possible values: `"noCase"`, `"upper"`, `"lower"`, `"smallCaps"`, `"minor"`, `"other"`.
    - <code><strong>category</strong>: string</code> – The category of the glyph. If unset, then the category is based on a glyph data lookup based on the glyph name.
    - <code><strong>color</strong></code> – The color label of the glyph. See [`colorLabel`](#spec-glyphs-3-colorLabel).
    - <code><strong>direction</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The writing direction of the glyph. If unset, then the writing direction is based on a glyph data lookup based on the glyph name.
        - Possible values: `"BIDI"`, `"LTR"`, `"RTL"`, `"VTR"`, `"VTL"`.
    - <code><strong>export</strong>: boolean = true</code> – Whether the glyph is exported.
    - <code><strong>glyphname</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the glyph.
    - <code><strong>kernBottom</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The kerning group of the bottom side of the glyph.
    - <code><strong>kernLeft</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The kerning group of the left side of the glyph.
    - <code><strong>kernRight</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The kerning group of the right side of the glyph.
    - <code><strong>kernTop</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The kerning group of the top side of the glyph.
    - <code><strong>lastChange</strong>: string</code> – The date and time of the last change of the glyph. Example: `"2023-02-25 14:46:49 +0000"`.
    - <code><strong>layers</strong>: array</code> – The layers of the glyph.
 See [`layer`](#spec-glyphs-3-layer) for items.
    - <code><strong>locked</strong>: boolean = false</code> – Whether the glyph is locked.
    - <code><strong>metricBottom</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The bottom metrics key of the glyph.
    - <code><strong>metricLeft</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The left metrics key of the glyph.
    - <code><strong>metricRight</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The right metrics key of the glyph.
    - <code><strong>metricTop</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The top metrics key of the glyph.
    - <code><strong>metricVertOrigin</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The vertical origin metrics key of the glyph.
    - <code><strong>metricVertWidth</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The vertical width metrics key of the glyph.
    - <code><strong>metricWidth</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The width metrics key of the glyph.
    - <code><strong>note</strong>: string = ""</code> – A string serving as a description or comment about the glyph.
    - <code><strong>partsSettings</strong>: array = []</code> – A list of the Smart Glyph properties and their top/bottom values.
 See [`partProperty`](#spec-glyphs-3-partProperty) for items.
    - <code><strong>production</strong>: string</code> – The production name of the glyph. If unset, then the production name is based on a glyph data lookup based on the glyph name or the Unicode code point.
    - <code><strong>script</strong>: string</code> – The script of the glyph. If unset, then the script is based on a glyph data lookup based on the glyph name.
    - <code><strong>sortName</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The sort name of the glyph. If unset, then the sort name is based on a glyph data lookup based on the glyph name.
    - <code><strong>sortNameKeep</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The sort name of the glyph used in the *Keep Alternates Next to Base Glyph* display mode. If unset, then the sort name is based on a glyph data lookup based on the glyph name.
    - <code><strong>subCategory</strong>: string</code> – The subcategory of the glyph. If unset, then the subcategory is based on a glyph data lookup based on the glyph name.
    - <code><strong>tags</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The tags of the glyph, sorted lexicographically.
        - <code><strong>#</strong>: string</code>
    - <code><strong>unicode</strong></code> – The Unicode code points of the glyph. One of 2 options.
        - Option. `integer` (`u32`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The code point value. Examples: `65`, `125184`, `0`.
        - Option. `array` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – An ascending list of code point values.
 Min count: 2.
            - <code><strong>#</strong>: integer</code> (`u32`) Examples: `65`, `125184`, `0`.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the glyph. See [`userData`](#spec-glyphs-3-userData).
- <code><strong>guide</strong>: object</code><a name="spec-glyphs-3-guide"></a> – (`GSGuide`)
    - <code><strong>angle</strong>: number = 0</code> (`f64`) – The angle at which the guide is drawn in degrees clockwise.
    - <code><strong>filter</strong>: string</code> – The filter of the guide. The syntax is the description of [NSPredicate](https://developer.apple.com/documentation/foundation/nspredicate). Omitted when no filter is defined.
    - <code><strong>grid</strong>: number = 0</code> (`f64`) – The grid of the guide.
    - <code><strong>length</strong>: number = 0</code> (`f64`) – The length of a line-type guide.
    - <code><strong>lockAngle</strong>: boolean = false</code> – Whether the angle of the guide is locked.
    - <code><strong>locked</strong>: boolean = false</code> – Whether the guide is locked.
    - <code><strong>name</strong>: string = ""</code> – The name of the guide.
    - <code><strong>orientation</strong>: string = "left"</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The orientation of the guide. See [`orientation`](#spec-glyphs-3-orientation).
        - Possible values: `"left"`, `"center"`, `"right"`.
    - <code><strong>pos</strong>: array = [0, 0]</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The position of the guide. See [`pos`](#spec-glyphs-3-pos).
    - <code><strong>showMeasurement</strong>: boolean = false</code> – Whether the measurement of the guide is shown.
    - <code><strong>size</strong>: array = [0, 0]</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The size of the guide. See [`size`](#spec-glyphs-3-size).
    - <code><strong>type</strong>: string = "Line"</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The type of the guide.
        - Possible values: `"Line"`, `"Circle"`, `"Rect"`.
    - <code><strong>userData</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Custom data associated with the guide. See [`userData`](#spec-glyphs-3-userData).
- <code><strong>gradient</strong></code><a name="spec-glyphs-3-gradient"></a> – (`GSGradient`) One of 2 options.
    - Option. `object` – (`GSLinearGradient`) – A linear gradient.
        - <code><strong>colors</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The color stops of the gradient. See [`gradientColors`](#spec-glyphs-3-gradientColors).
        - <code><strong>end</strong>: array</code> – The end point of the linear gradient relative to the shape bounds. See [`pos`](#spec-glyphs-3-pos).
        - <code><strong>start</strong>: array</code> – The start point of the linear gradient relative to the shape bounds. See [`pos`](#spec-glyphs-3-pos).
    - Option. `object` – (`GSRadialGradient`) – A radial gradient.
        - <code><strong>colors</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The color stops of the gradient. See [`gradientColors`](#spec-glyphs-3-gradientColors).
        - <code><strong>end</strong>: array</code> – The end center of the radial gradient relative to the shape bounds. See [`pos`](#spec-glyphs-3-pos).
        - <code><strong>start</strong>: array</code> – The start center of the radial gradient relative to the shape bounds. See [`pos`](#spec-glyphs-3-pos).
        - <code><strong>type</strong>: string = "circle"</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The radial gradient type marker.
- <code><strong>gradientColors</strong>: array</code><a name="spec-glyphs-3-gradientColors"></a>
 See [`gradientColorStop`](#spec-glyphs-3-gradientColorStop) for items.
- <code><strong>gradientColorStop</strong>: array</code><a name="spec-glyphs-3-gradientColorStop"></a> – (`GSColorStop`)
 Tuple with 2 items.
    - <code><strong>#0</strong></code> – The color of the stop. See [`color`](#spec-glyphs-3-color).
    - <code><strong>#1</strong>: number</code> (`f64`) – The offset of the stop.
- <code><strong>hint</strong>: object</code><a name="spec-glyphs-3-hint"></a> – (`GSHint`)
    - <code><strong>horizontal</strong>: boolean = false</code> – Whether the hint is horizontal. Not written for path components.
    - <code><strong>name</strong>: string</code> – The name of the hint.
    - <code><strong>options</strong>: number = 0</code> (`u32`) – The options of the hint.
    - <code><strong>origin</strong></code> – The origin of the hint. See [`indexPath`](#spec-glyphs-3-indexPath).
    - <code><strong>other1</strong></code> – The first other point of the hint, used by TrueType instructions that need more than two nodes. See [`indexPath`](#spec-glyphs-3-indexPath).
    - <code><strong>other2</strong></code> – The second other point of the hint, used by TrueType instructions that need more than three nodes. See [`indexPath`](#spec-glyphs-3-indexPath).
    - <code><strong>place</strong>: array</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center">
 Tuple with 2 items.
        - <code><strong>#0</strong>: number</code> (`f64`) – The origin placement.
        - <code><strong>#1</strong>: number</code> (`f64`) – The width of the hint. `21` for bottom ghost hints and flex hints, `-20` for top ghost hints.
    - <code><strong>scale</strong>: array = [1, 1]</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The scale of the hint. See [`scale`](#spec-glyphs-3-scale).
    - <code><strong>settings</strong>: object</code> – The settings of the hint.
    - <code><strong>stem</strong>: number</code> (`i32`) – The stem of the hint.
    - <code><strong>target</strong></code> One of 2 options.
        - Option. See [`indexPath`](#spec-glyphs-3-indexPath).
        - Option. `string` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The target of a ghost hint.
            - Possible values: `"up"`, `"down"`.
    - <code><strong>type</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The type of the hint.
        - Possible values: `"TopGhost"`, `"BottomGhost"`, `"Stem"`, `"Flex"`, `"TTStem"`, `"TTShift"`, `"TTSnap"`, `"TTInterpolate"`, `"TTDiagonal"`, `"TTDelta"`, `"Tag"`, `"Corner"`, `"Cap"`, `"Brush"`, `"Segment"`, `"Auto"`, `"Unknown"`.
- <code><strong>image</strong>: object</code><a name="spec-glyphs-3-image"></a> – (`GSImage`)
    - <code><strong>alpha</strong>: number = 50</code> (`f64`) – The alpha value of the image.
    - <code><strong>angle</strong>: number = 0</code> (`f64`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The rotation angle of the image in degrees clockwise.
    - <code><strong>crop</strong>: array</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The cropped frame of the image, specified as the crop origin X/Y and size width/height.
 Tuple with 4 items.
        - <code><strong>#0</strong>: number</code> (`f64`) – The X coordinate of the crop origin.
        - <code><strong>#1</strong>: number</code> (`f64`) – The Y coordinate of the crop origin.
        - <code><strong>#2</strong>: number</code> (`f64`) – The width of the crop size.
        - <code><strong>#3</strong>: number</code> (`f64`) – The height of the crop size.
    - <code><strong>imagePath</strong>: string</code> – The file path of the image file relative to the document file.
    - <code><strong>imageURL</strong>: string</code> – The URL bookmark data of the image file path.
    - <code><strong>locked</strong>: boolean = false</code> – Whether the image is locked.
    - <code><strong>pos</strong>: array = [0, 0]</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The position of the image. See [`pos`](#spec-glyphs-3-pos).
    - <code><strong>scale</strong>: array = [1, 1]</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The scale factor of the image. See [`scale`](#spec-glyphs-3-scale).
    - <code><strong>slant</strong>: array = [0, 0]</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The slant factor of the image. See [`slant`](#spec-glyphs-3-slant).
- <code><strong>instance</strong>: object</code><a name="spec-glyphs-3-instance"></a> – (`GSInstance`)
    - <code><strong>axesValues</strong>: array</code> – The internal axis locations of the instance. These values are also used for the external axis locations, if no external axis locations are specified separately.
        - <code><strong>#</strong>: number</code> (`f64`)
    - <code><strong>customParameters</strong>: array = []</code> – The custom parameters of the instance.
 See [`customParameter`](#spec-glyphs-3-customParameter) for items.
    - <code><strong>exports</strong>: boolean = true</code> – Whether the instance is exported.
    - <code><strong>instanceInterpolations</strong>: object = {}</code> – The interpolation factors where the keys are the master IDs.
        - <code>string</code> One of 2 options.
            - Option. `number` (`f64`) – The X and Y factors are the same.
            - Option. `array` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The X and Y factors.
 Tuple with 2 items.
                - <code><strong>#0</strong>: number</code> (`f64`) – The X factor.
                - <code><strong>#1</strong>: number</code> (`f64`) – The Y factor.
    - <code><strong>isBold</strong>: boolean = false</code> – Whether the instance is bold.
    - <code><strong>isItalic</strong>: boolean = false</code> – Whether the instance is italic.
    - <code><strong>linkStyle</strong>: string</code> – The name of the style-linked instance.
    - <code><strong>manualInterpolation</strong>: boolean = false</code> – Whether the `instanceInterpolations` values are used. Otherwise, the values are calculated from the axis values.
    - <code><strong>name</strong>: string</code> – The style name of the instance. Examples: `"Regular"`, `"Bold"`, `"Italic"`, `"Bold Italic"`.
    - <code><strong>properties</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center">
 See [`infoProperty`](#spec-glyphs-3-infoProperty) for items.
    - <code><strong>type</strong>: string = "single"</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The type of the instance.
        - Possible values: `"single"`, `"variable"`, `"static"`, `"icon"`, `"particles"`.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the instance. See [`userData`](#spec-glyphs-3-userData).
    - <code><strong>visible</strong>: boolean = true</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Whether the instance is visible when previewing all instances.
    - <code><strong>weightClass</strong>: integer = 400</code> (`u16`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The weight class of the instance.
    - <code><strong>widthClass</strong>: integer = 5</code> (`u16`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The width class of the instance.
- <code><strong>indexPath</strong></code><a name="spec-glyphs-3-indexPath"></a> One of 4 options.
    - Option. `array` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The index path of a node on a path.
 Tuple with 2 items.
        - <code><strong>#0</strong>: number</code> (`u32`) – The index of a path shape.
        - <code><strong>#1</strong>: number</code> (`u32`) – The index of a node on a path.
    - Option. `array` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The index path of an inflection, where the first two path components point to an on-curve node that finishes a curve segment. The inflection component is most likely `0`.
 Tuple with 3 items.
        - <code><strong>#0</strong>: number</code> (`u32`) – The index of a path shape.
        - <code><strong>#1</strong>: number</code> (`u32`) – The index of a node on a path.
        - <code><strong>#2</strong>: number</code> (`u32`) – The index of an inflection.
    - Option. `array` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Points to the intersection of two path segments. The nodes are the ones finishing the segments.
 Tuple with 4 items.
        - <code><strong>#0</strong>: number</code> (`u32`) – The index of a path shape (P1).
        - <code><strong>#1</strong>: number</code> (`u32`) – The index of a node (N1) on P1.
        - <code><strong>#2</strong>: number</code> (`u32`) – The index of a path shape (P2).
        - <code><strong>#3</strong>: number</code> (`u32`) – The index of a node (N2) on P2.
    - Option. `string` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – An attachment to the left or right side-bearing.
        - Possible values: `"lsb"`, `"rsb"`.
- <code><strong>kerning</strong>: object = {}</code><a name="spec-glyphs-3-kerning"></a> – Maps master IDs to kerning definitions.
    - <code>string: object</code> – Maps glyph names or class names to kerning partners.
        - <code>string: object</code> – Maps glyph names or class names to kerning values.
            - <code>string: number</code> (`f64`)
- <code><strong>layer</strong>: object</code><a name="spec-glyphs-3-layer"></a> – (`GSLayer`)
    - <code><strong>anchors</strong>: array = []</code> – The anchors of the layer.
 See [`anchor`](#spec-glyphs-3-anchor) for items.
    - <code><strong>annotations</strong>: array = []</code> – The annotations of the layer.
 See [`annotation`](#spec-glyphs-3-annotation) for items.
    - <code><strong>associatedMasterId</strong>: string</code> – The unique identifier of the associated master. Omitted when equal to the layer ID.
    - <code><strong>attr</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The attributes of the layer. See [`layerAttr`](#spec-glyphs-3-layerAttr).
    - <code><strong>background</strong>: object</code>
        - <code><strong>anchors</strong>: array = []</code> – The anchors of the background layer.
 See [`anchor`](#spec-glyphs-3-anchor) for items.
        - <code><strong>annotations</strong>: array = []</code> – The annotations of the background layer.
 See [`annotation`](#spec-glyphs-3-annotation) for items.
        - <code><strong>backgroundImage</strong>: object</code> – The background image of the layer. See [`image`](#spec-glyphs-3-image).
        - <code><strong>guides</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The guides of the background layer.
 See [`guide`](#spec-glyphs-3-guide) for items.
        - <code><strong>hints</strong>: array = []</code> – The hints of the background layer.
 See [`hint`](#spec-glyphs-3-hint) for items.
        - <code><strong>shapes</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The shapes of the background layer.
 See [`shape`](#spec-glyphs-3-shape) for items.
    - <code><strong>backgroundImage</strong>: object</code> – The background image of the layer. See [`image`](#spec-glyphs-3-image).
    - <code><strong>color</strong></code> – The color label of the layer. See [`colorLabel`](#spec-glyphs-3-colorLabel).
    - <code><strong>guides</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The guides of the layer.
 See [`guide`](#spec-glyphs-3-guide) for items.
    - <code><strong>hints</strong>: array = []</code> – The hints of the layer.
 See [`hint`](#spec-glyphs-3-hint) for items.
    - <code><strong>layerId</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The unique ID of the layer. Matches the master ID when the layer is a master layer.
    - <code><strong>metricBottom</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The bottom metrics key of the layer.
    - <code><strong>metricLeft</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The left metrics key of the layer.
    - <code><strong>metricRight</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The right metrics key of the layer.
    - <code><strong>metricTop</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The top metrics key of the layer.
    - <code><strong>metricVertOrigin</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The vertical origin metrics key of the layer.
    - <code><strong>metricVertWidth</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The vertical width metrics key of the layer.
    - <code><strong>metricWidth</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The width metrics key of the layer.
    - <code><strong>name</strong>: string = ""</code> – The name of the layer. Master layers and other special layers display a name in the Glyphs UI that is derived from the layer’s role (for example, the name of the master that the layer belongs to). These derived names are not written to the file. Instead, this name is only displayed in the UI for non-special layers (like backup layers).
    - <code><strong>partSelection</strong>: object</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The Smart Glyph setting of the layer. The keys are the property names. The values are either `1` if the layer corresponds to the bottom value of the property or `2` if the layer corresponds to the top value of the property. If a layer is neither the top nor the bottom value, the property is omitted.
        - <code>string: integer</code> One of 2 options.
            - Option. `1` – Bottom: the layer corresponds to the bottom value of the property.
            - Option. `2` – Top: the layer corresponds to the top value of the property.
    - <code><strong>shapes</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The shapes of the layer.
 See [`shape`](#spec-glyphs-3-shape) for items.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the layer. See [`userData`](#spec-glyphs-3-userData).
    - <code><strong>vertOrigin</strong>: number = 0</code> (`f64`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The vertical origin of the layer.
    - <code><strong>vertWidth</strong>: number = 0</code> (`f64`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The vertical width of the layer.
    - <code><strong>visible</strong>: boolean = false</code> – Whether the layer is visible.
    - <code><strong>width</strong>: number</code> (`f64`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The width of the layer.
- <code><strong>layerAttr</strong>: object</code><a name="spec-glyphs-3-layerAttr"></a>
    - <code><strong>axisRules</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Alternative-layer rules, ordered like the font axes.
        - <code><strong>#</strong>: object</code>
            - <code><strong>min</strong>: number</code> (`f64`) – The minimum matching axis value.
            - <code><strong>max</strong>: number</code> (`f64`) – The maximum matching axis value.
    - <code><strong>color</strong>: boolean = false</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Whether the layer is an Apple color layer.
    - <code><strong>colorPalette</strong></code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The color palette index of a color palette layer. One of 2 options.
        - Option. `integer` (`u16`) – The color palette index of a color palette layer.
        - Option. `"*"` – The foreground text color (color index 65535).
    - <code><strong>coordinates</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Intermediate-layer coordinates, ordered like the relevant axes. Starting in version 4, also contains the glyph-local axis coordinates for layers of Smart Glyphs.
        - <code><strong>#</strong>: number</code> (`f64`) – The explicit coordinate value.
    - <code><strong>sbixSize</strong>: integer</code> (`u16`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The Apple sbix image size.
    - <code><strong>svg</strong>: boolean = false</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Whether the layer is an SVG color layer.
- <code><strong>lineCap</strong>: integer</code><a name="spec-glyphs-3-lineCap"></a> (`u8`) One of 4 options.
    - Option. `0` – Butt: ends the stroke at the path endpoint.
    - Option. `1` – Round: extends the stroke with a semicircular cap.
    - Option. `2` – Square: extends the stroke with a square cap.
    - Option. `3` – Round inset: ends the stroke with an inset semicircular cap.
- <code><strong>metric</strong>: object</code><a name="spec-glyphs-3-metric"></a> – (`GSMetric`)
    - <code><strong>filter</strong>: string</code> – The filter of the metric limiting the scope of the metric to a subset of glyphs.
    - <code><strong>horizontal</strong>: boolean = false</code> – Whether the metric is a horizontal metric.
    - <code><strong>name</strong>: string</code> – The name of the metric.
    - <code><strong>type</strong>: string</code> – The type of the metric.
        - Possible values: `"ascender"`, `"cap height"`, `"slant height"`, `"x-height"`, `"midHeight"`, `"bodyHeight"`, `"descender"`, `"baseline"`, `"italic angle"`, `"italic slope"`.
- <code><strong>metricStore</strong>: object</code><a name="spec-glyphs-3-metricStore"></a> – (`GSMetricStore`)
    - <code><strong>over</strong>: number = 0</code> (`f64`) – The overshoot of the metric value.
    - <code><strong>pos</strong>: number = 0</code> (`f64`) – The offset from the baseline of the metric value.
- <code><strong>node</strong>: array</code><a name="spec-glyphs-3-node"></a> – (`GSNode`)
 Tuple with 3–4 items.
    - <code><strong>#0</strong>: number</code> (`f64`) – The x-coordinate of the node.
    - <code><strong>#1</strong>: number</code> (`f64`) – The y-coordinate of the node.
    - <code><strong>#2</strong>: string</code> – The configuration of the node expressed as a sequence of characters. Types: `m`: move, `l`: line, `c`: cubic curve, `q`: quadratic curve, `o`: off-curve. Connection (may follow `l`, `c`, `q`): `s`: smooth. Orientation (left is the default): `R`: right, `C`: center. Locking (not locked is the default): `X`: locked.
    - <code><strong>#3</strong>: object = {}</code> – The attributes of the node. See [`attr`](#spec-glyphs-3-attr).
- <code><strong>infoProperty</strong></code><a name="spec-glyphs-3-infoProperty"></a> – (`GSInfoProperty`) One of 2 options.
    - Option. `object`
        - <code><strong>key</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The key of the property.
        - <code><strong>value</strong></code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The value of the property.
    - Option. `object`
        - <code><strong>key</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The key of the property.
        - <code><strong>values</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The values of the property.
 See [`infoValue`](#spec-glyphs-3-infoValue) for items.
- <code><strong>infoValue</strong>: object</code><a name="spec-glyphs-3-infoValue"></a> – (`GSInfoValue`)
    - <code><strong>language</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The language tag of the string value. The tag is based on the [OpenType Language System Tags](https://learn.microsoft.com/en-us/typography/opentype/spec/languagetags) but omits trailing whitespace. Examples: `"dflt"`, `"DEU"`.
    - <code><strong>value</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The localized string value.
- <code><strong>orientation</strong>: string</code><a name="spec-glyphs-3-orientation"></a> – (`GSElementOrientation`)
    - Possible values: `"left"`, `"center"`, `"right"`.
- <code><strong>partProperty</strong>: object</code><a name="spec-glyphs-3-partProperty"></a> – (`GSPartProperty`)
    - <code><strong>bottomName</strong>: string</code> – The name of the bottom value of the property. (Unused)
    - <code><strong>bottomValue</strong>: integer</code> (`i32`) – The lower end of the value range of the property.
    - <code><strong>name</strong>: string</code> – The name of the property.
    - <code><strong>topName</strong>: string</code> – The name of the top value of the property. (Unused)
    - <code><strong>topValue</strong>: integer</code> (`i32`) – The upper end of the value range of the property.
- <code><strong>palettes</strong>: array</code><a name="spec-glyphs-3-palettes"></a> – (`GSPalettes`) – The version 3 structure of the `Color Palettes` custom parameter.
    - <code><strong>#</strong>: array</code>
 See [`color`](#spec-glyphs-3-color) for items.
- <code><strong>path</strong>: object</code><a name="spec-glyphs-3-path"></a> – (`GSPath`)
    - <code><strong>attr</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The attributes of the path. See [`shapeAttr`](#spec-glyphs-3-shapeAttr).
    - <code><strong>closed</strong>: boolean</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – Whether the path is closed.
    - <code><strong>locked</strong>: boolean = false</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Whether the path is locked.
    - <code><strong>nodes</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The on- and off-curve nodes of the path.
 See [`node`](#spec-glyphs-3-node) for items.
- <code><strong>pos</strong>: array</code><a name="spec-glyphs-3-pos"></a>
 Tuple with 2 items.
    - <code><strong>#0</strong>: number</code> (`f64`) – The x-coordinate of the position.
    - <code><strong>#1</strong>: number</code> (`f64`) – The y-coordinate of the position.
- <code><strong>scale</strong>: array</code><a name="spec-glyphs-3-scale"></a>
 Tuple with 2 items.
    - <code><strong>#0</strong>: number</code> (`f64`) – The horizontal scale factor.
    - <code><strong>#1</strong>: number</code> (`f64`) – The vertical scale factor.
- <code><strong>shape</strong></code><a name="spec-glyphs-3-shape"></a> – (`GSShape`) One of 2 options.
    - Option. `object` See [`path`](#spec-glyphs-3-path).
    - Option. `object` See [`component`](#spec-glyphs-3-component).
- <code><strong>shapeAttr</strong>: object</code><a name="spec-glyphs-3-shapeAttr"></a>
    - <code><strong>color</strong></code> – The color label of the shape. See [`colorLabel`](#spec-glyphs-3-colorLabel).
    - <code><strong>fill</strong>: boolean = false</code> – Whether a stroked path is also filled.
    - <code><strong>fillColor</strong></code> – The fill color of the shape. See [`color`](#spec-glyphs-3-color).
    - <code><strong>gradient</strong></code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The fill gradient of the shape. See [`gradient`](#spec-glyphs-3-gradient).
    - <code><strong>lineCapEnd</strong>: integer = 0</code> (`u8`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The line cap style at the end of the stroke. See [`lineCap`](#spec-glyphs-3-lineCap).
    - <code><strong>lineCapStart</strong>: integer = 0</code> (`u8`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The line cap style at the start of the stroke. See [`lineCap`](#spec-glyphs-3-lineCap).
    - <code><strong>lineJoin</strong>: integer = 0</code> (`u8`) – The line join style of the stroke. One of 3 options.
        - Option. `0` – Miter: extends the segment edges until they intersect.
        - Option. `1` – Round: connects the segment edges with a circular arc.
        - Option. `2` – Bevel: connects the segment edges with a straight edge.
    - <code><strong>mask</strong>: boolean = 0</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – How the shape masks preceding shapes in the same composition unit.
    - <code><strong>reversePaths</strong>: boolean = false</code> – Whether paths from the shape are reversed for drawing/export.
    - <code><strong>shadow</strong>: object</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The outer shadow of the shape. See [`shadow`](#spec-glyphs-3-shadow).
    - <code><strong>shadowIn</strong>: object</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The inner shadow of the shape. See [`shadow`](#spec-glyphs-3-shadow).
    - <code><strong>strokeColor</strong></code> – The stroke color of the shape. See [`color`](#spec-glyphs-3-color).
    - <code><strong>strokeHeight</strong>: number</code> (`f64`) – The vertical stroke size, or an expression resolving to one. Falls back to the value of `strokeWidth` when unset.
    - <code><strong>strokePos</strong>: number = 0.5</code> (`f64`) – The stroke position. In version 4, values range from inside (-1) through centered (0) to outside (1). In version 3, values range from outside (0) through centered (0.5) to inside (1).
    - <code><strong>strokeWidth</strong>: number</code> (`f64`) – The horizontal stroke size, or an expression resolving to one.
- <code><strong>shadow</strong>: object</code><a name="spec-glyphs-3-shadow"></a> – (`GSShadow`)
    - <code><strong>blur</strong>: string = "4"</code> – The shadow blur radius, stored as an expression string.
    - <code><strong>color</strong></code> – The shadow color. See [`color`](#spec-glyphs-3-color).
    - <code><strong>offsetX</strong>: string = "4"</code> – The horizontal shadow offset, stored as an expression string.
    - <code><strong>offsetY</strong>: string = "4"</code> – The vertical shadow offset, stored as an expression string.
- <code><strong>size</strong>: array</code><a name="spec-glyphs-3-size"></a>
 Tuple with 2 items.
    - <code><strong>#0</strong>: number</code> (`f64`) – The width.
    - <code><strong>#1</strong>: number</code> (`f64`) – The height.
- <code><strong>slant</strong>: array</code><a name="spec-glyphs-3-slant"></a>
 Tuple with 2 items.
    - <code><strong>#0</strong>: number</code> (`f64`) – The horizontal slant factor.
    - <code><strong>#1</strong>: number</code> (`f64`) – The vertical slant factor.
- <code><strong>userData</strong>: object</code><a name="spec-glyphs-3-userData"></a>

## Changes

### 10. July 2025

- Add descriptions to `GSComponentAlignment`.

### 14. Jan. 2025

- Reworked JSON Schemas and added variants for package and autosave files.
- Expanded descriptions and annotations for most values.

### 1. March 2021

- add description of .glyphspackage files

### September – December 2020

- several fixes and additions
- add JSON schema for Glyphs 2 and 3 files

### 4. Jan. 2019

- First Draft for version 3

### 1. Oct. 2018:

- Add Notes about special cases
- Better general explanation

### 21. April 2018:

- Add .appVersion, disablesNiceNames, customValue, weight, width, custom
- Fix typos: paths, widthValue

### 4. Feb. 2016:

- added hints
- updated and added a few field in layers
