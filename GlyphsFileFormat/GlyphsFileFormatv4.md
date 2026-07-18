# Glyphs File Format, Version 4

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
- `UIState.plist` – A file containing the display strings. A dictionary with a `displayStrings` key following the [`displayStrings` schema](#spec-glyphs-4-displayStrings).
- `glyphs/*.glyph` – Individual files for each glyph. The files follow the [`glyph` schema](#spec-glyphs-4-glyph).
- `kerning.plist` – A file containing the `kerningLTR`/`kerningRTL`/`kerningVertical` (following the [`kerning` schema](#spec-glyphs-4-kerning)) and [`kerningContext`](#spec-glyphs-4-kerningContext) dictionaries. Omitted when the font contains no kerning.
- `note.md` – A UTF-8 Markdown text file containing the font note. Omitted when the font note is empty.
- `features/*.fea` – Individual UTF-8 files for feature classes, feature prefixes, and features. Each file contains the layout feature code of the matching object.

Feature file names are derived from the object name:

- Prefixes use their name prefixed with `_`, for example `_Languagesystems.fea`.
- Classes use their name prefixed with `@`, for example `@Uppercase.fea`.
- Features use their tag, for example `calt.fea`.
- If the resulting file name stem conflicts with an earlier file name, `.2`, `.3`, and so on is appended to the stem, for example `calt.fea` and `calt.2.fea`.

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

- [glyphs-4.schema.json](https://github.com/schriftgestalt/GlyphsSDK/blob/Glyphs3/GlyphsFileFormat/Schemas/glyphs-4.schema.json)
- [glyphs-autosave-4.schema.json](https://github.com/schriftgestalt/GlyphsSDK/blob/Glyphs3/GlyphsFileFormat/Schemas/glyphs-autosave-4.schema.json)
- [fontinfo-4.schema.json](https://github.com/schriftgestalt/GlyphsSDK/blob/Glyphs3/GlyphsFileFormat/Schemas/fontinfo-4.schema.json)
- [fontinfo-autosave-4.schema.json](https://github.com/schriftgestalt/GlyphsSDK/blob/Glyphs3/GlyphsFileFormat/Schemas/fontinfo-autosave-4.schema.json)

## Document

- <code><strong>.appVersion</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The build number of Glyphs used to save the file. Example: `"4012"`.
- <code><strong>.formatVersion</strong>: integer</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The version of the file format. If unset, the file is considered to be version 1 as used by Glyphs 1 and Glyphs 2. One of 2 options.
    - Option. `4` – Glyphs file format version 4.
    - Option. `3` – Glyphs file format version 3.
- <code><strong>DisplayStrings</strong>: array = []</code> – The strings of the Edit View tabs. Omitted when the `Write DisplayStrings` custom parameter is set to false. Omitted and written as `displayStrings` to `UIState.plist` in case of a package file. See [`displayStrings`](#spec-glyphs-4-displayStrings).
- <code><strong>axes</strong>: array = []</code> – The designspace variation axes of the font.
 See [`axis`](#spec-glyphs-4-axis) for items.
- <code><strong>classes</strong>: array = []</code> – The OpenType layout classes of the font.
 See [`class`](#spec-glyphs-4-class) for items.
- <code><strong>customParameters</strong>: array = []</code> – The custom parameters of the font.
 See [`customParameter`](#spec-glyphs-4-customParameter) for items.
- <code><strong>date</strong>: string</code> – The moment in time that is used as the creation date of exported font files including date, time, and timezone. Example: `"2026-07-17 03:14:15 +0000"`.
- <code><strong>featurePrefixes</strong>: array = []</code> – The OpenType layout feature prefixes of the font.
 See [`featurePrefix`](#spec-glyphs-4-featurePrefix) for items.
- <code><strong>features</strong>: array = []</code> – The OpenType layout features of the font.
 See [`feature`](#spec-glyphs-4-feature) for items.
- <code><strong>fontMaster</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The masters of the font.
 Min count: 1.
 See [`fontMaster`](#spec-glyphs-4-fontMaster) for items.
- <code><strong>glyphs</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The glyphs of the font. The order is used on export unless the `glyphOrder` custom parameter is set.
 See [`glyph`](#spec-glyphs-4-glyph) for items.
- <code><strong>instances</strong>: array = []</code> – The instances of the font.
 See [`instance`](#spec-glyphs-4-instance) for items.
- <code><strong>kerningContext</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The context kerning of the font. See [`kerningContext`](#spec-glyphs-4-kerningContext).
- <code><strong>kerningLTR</strong>: object = {}</code> – The left-to-right kerning of the font. See [`kerning`](#spec-glyphs-4-kerning).
- <code><strong>kerningRTL</strong>: object = {}</code> – The right-to-left kerning of the font. See [`kerning`](#spec-glyphs-4-kerning).
- <code><strong>kerningVertical</strong>: object = {}</code> – The vertical kerning of the font. See [`kerning`](#spec-glyphs-4-kerning).
- <code><strong>metrics</strong>: array = []</code> – The metrics of the font.
 See [`metric`](#spec-glyphs-4-metric) for items.
- <code><strong>note</strong>: string</code> – The note about the font.
- <code><strong>numbers</strong>: array = []</code> – The numbers of the font.
 See [`metric`](#spec-glyphs-4-metric) for items.
- <code><strong>properties</strong>: array = []</code> – The properties of the font.
 See [`infoProperty`](#spec-glyphs-4-infoProperty) for items.
- <code><strong>settings</strong>: object = {}</code>
    - <code><strong>dependencies</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Maps dependency class names to dependency display names.
        - <code>string: string</code>
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
- <code><strong>stems</strong>: array = []</code> – The stems of the font.
 See [`metric`](#spec-glyphs-4-metric) for items.
- <code><strong>unitsPerEm</strong>: integer</code> (`u32`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The number of coordinate units on the em square.
- <code><strong>userData</strong>: object = {}</code> – Custom data associated with the font. See [`userData`](#spec-glyphs-4-userData).
- <code><strong>versionMajor</strong>: integer</code> (`u32`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The major version number of the font.
- <code><strong>versionMinor</strong>: integer</code> (`u32`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The minor version number of the font.
## Definitions

- <code><strong>anchor</strong>: object</code><a name="spec-glyphs-4-anchor"></a> – (`GSAnchor`)
    - <code><strong>attr</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The attributes of the anchor. See [`attr`](#spec-glyphs-4-attr).
    - <code><strong>locked</strong>: boolean = false</code> – Whether the anchor is locked.
    - <code><strong>name</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the anchor.
    - <code><strong>orientation</strong>: string = "left"</code> – The orientation of the anchor. See [`orientation`](#spec-glyphs-4-orientation).
        - Possible values: `"left"`, `"center"`, `"right"`.
    - <code><strong>pos</strong>: array = [0, 0]</code> – The position of the anchor. See [`pos`](#spec-glyphs-4-pos).
- <code><strong>annotation</strong>: object</code><a name="spec-glyphs-4-annotation"></a> – (`GSAnnotation`)
    - <code><strong>angle</strong>: number = 0</code> (`f64`) – The angle of the annotation in degrees clockwise.
    - <code><strong>pos</strong>: array = [0, 0]</code> – The position of the annotation. See [`pos`](#spec-glyphs-4-pos).
    - <code><strong>text</strong>: string = ""</code> – The text of an text-type annotation.
    - <code><strong>type</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The type of the annotation.
        - Possible values: `"Text"`, `"Arrow"`, `"Circle"`, `"Plus"`, `"Minus"`.
    - <code><strong>width</strong>: number = 0</code> (`f64`) – The width of an text- or circle-type annotation.
- <code><strong>attr</strong>: object</code><a name="spec-glyphs-4-attr"></a>
- <code><strong>axis</strong>: object</code><a name="spec-glyphs-4-axis"></a> – (`GSAxis`)
    - <code><strong>default</strong>: number = 0</code> (`f64`) – The default location on the axis.
    - <code><strong>hidden</strong>: boolean = false</code> – Whether the axis is considered to be hidden from the font user.
    - <code><strong>name</strong>: string = ""</code> – The user-facing name of the axis.
    - <code><strong>names</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The user-facing, localized name of the axis.
 See [`infoValue`](#spec-glyphs-4-infoValue) for items.
    - <code><strong>tag</strong>: string = ""</code> – The OpenType tag of the axis. Must be unique within the font. The tag may be longer than four characters in which case only the first four characters are considered to be the canonical tag of the axis and the rest is used as a differentiating identifier. On export, the canonical tag is used. Multiple axes with the same canonical tag are useful for higher-order interpolation.
    - <code><strong>userData</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Custom data associated with the axis. See [`userData`](#spec-glyphs-4-userData).
- <code><strong>class</strong>: object</code><a name="spec-glyphs-4-class"></a> – (`GSClass`)
    - <code><strong>automatic</strong>: boolean = false</code> – Whether the code of the class is generated automatically.
    - <code><strong>code</strong>: string = ""</code> – The code of the class. Note that this code may not just be a whitespace-separated list of glyph names but may also contain comments and other feature code constructs. Examples: `"A B C"`, `"noon-ar noon-ar.fina noon-ar.medi noon-ar.init # noon-ar glyphs"`.
    - <code><strong>disabled</strong>: boolean = false</code> – Whether the class is disabled.
    - <code><strong>name</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the class. The leading at sign (`@`) is not included. Examples: `"Uppercase"`, `"CombiningTopAccents"`.
    - <code><strong>notes</strong>: string = ""</code> – A string serving as a description or comment about the class.
- <code><strong>color</strong></code><a name="spec-glyphs-4-color"></a> One of 4 options.
    - Option. `array` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – An RGB color with an alpha channel in the font color space. In version 4, color components are normalized to the range 0…1.
 Tuple with 4 items.
        - <code><strong>#0</strong>: number</code> (`f64`) – The red color component.
        - <code><strong>#1</strong>: number</code> (`f64`) – The green color component.
        - <code><strong>#2</strong>: number</code> (`f64`) – The blue color component.
        - <code><strong>#3</strong>: number</code> (`f64`) – The alpha color component.
    - Option. `array` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – A gray color with an alpha channel. In version 4, color components are normalized to the range 0…1.
 Tuple with 2 items.
        - <code><strong>#0</strong>: number</code> (`f64`) – The gray value from `0` (black) to `1` (white).
        - <code><strong>#1</strong>: number</code> (`f64`) – The alpha color component.
    - Option. `array` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – A CMYK color with an alpha channel. In version 4, color components are normalized to the range 0…1.
 Tuple with 5 items.
        - <code><strong>#0</strong>: number</code> (`f64`) – The cyan color component.
        - <code><strong>#1</strong>: number</code> (`f64`) – The magenta color component.
        - <code><strong>#2</strong>: number</code> (`f64`) – The yellow color component.
        - <code><strong>#3</strong>: number</code> (`f64`) – The black color component.
        - <code><strong>#4</strong>: number</code> (`f64`) – The alpha color component.
    - Option. `array` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – A color reference into the `Color Palettes` custom parameter.
 Tuple with 3 items.
        - <code><strong>#0</strong>: string = "p"</code> – Indicates a palette color reference.
        - <code><strong>#1</strong>: integer</code> (`u16`) – The color palette entry index. `65535` indicates the current text color.
        - <code><strong>#2</strong>: number = 1</code> (`f64`) – The alpha factor applied to the referenced palette color.
- <code><strong>colorLabel</strong></code><a name="spec-glyphs-4-colorLabel"></a> One of 2 options.
    - Option. `integer` (`u8`) – The index of the color label. See also [the handbook entry on color labels](https://handbook.glyphsapp.com/glyph/#glyph/color-label).
    - Option. See [`color`](#spec-glyphs-4-color).
- <code><strong>component</strong>: object</code><a name="spec-glyphs-4-component"></a> – (`GSComponent`)
    - <code><strong>alignment</strong>: integer = 0</code> (`i8`) – (`GSComponentAlignment`) – Controls the automatic alignment of the component. `-1`: disabled (no alignment), `0`: default (alignment is based on context), `1`: force alignment (align regardless of context), `3`: horizontal alignment (align horizontally, but allow for manual vertical placement). One of 4 options.
        - Option. `-1` – Disabled: automatic positioning is disabled.
        - Option. `0` – Default: automatic positioning follows the normal eligibility rules.
        - Option. `1` – Forced: automatic positioning is enabled regardless of normal eligibility.
        - Option. `3` – Horizontal: only the horizontal coordinate is positioned automatically.
    - <code><strong>anchor</strong>: string</code> – The name of the attachment anchor. Set to specify a specific anchor when there are multiple candidates.
    - <code><strong>angle</strong>: number = 0</code> (`f64`) – The rotation angle of the component in degrees clockwise.
    - <code><strong>attr</strong>: object = {}</code> – The attributes of the component. See [`shapeAttr`](#spec-glyphs-4-shapeAttr).
    - <code><strong>keepWeight</strong>: number = 0</code> (`f64`) – Unused.
    - <code><strong>locked</strong>: boolean = false</code> – Whether the component is locked.
    - <code><strong>masterId</strong>: string</code> – The ID of the master from which the component is derived.
    - <code><strong>orientation</strong>: integer = 0</code> (`i8`) – (`GSElementOrientation`) – The orientation of the component. One of 3 options.
        - Option. `0` – Left: x values are relative to the left edge of the layer box.
        - Option. `1` – Right: x values are relative to the right edge of the layer box.
        - Option. `2` – Center: x values are relative to the center of the layer box.
    - <code><strong>piece</strong>: object = {}</code> – The Smart Component settings of the component, mapping property names to values.
        - <code>string</code> One of 2 options.
            - Option. `number` (`f64`)
            - Option. `integer`
    - <code><strong>pos</strong>: array = [0, 0]</code> – The position (translation transform) of the component. See [`pos`](#spec-glyphs-4-pos).
    - <code><strong>ref</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the referenced glyph.
    - <code><strong>scale</strong>: array = [1, 1]</code> – The scale transform of the component. See [`scale`](#spec-glyphs-4-scale).
    - <code><strong>slant</strong>: array = [0, 0]</code> – The slant transform of the component. See [`slant`](#spec-glyphs-4-slant).
    - <code><strong>traverseAnchors</strong>: boolean = true</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Whether the component should traverse anchors.
- <code><strong>customParameter</strong>: object</code><a name="spec-glyphs-4-customParameter"></a> – (`GSCustomParameter`)
    - <code><strong>disabled</strong>: boolean = false</code> – Whether the custom parameter is disabled.
    - <code><strong>name</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the custom parameter.
    - <code><strong>value</strong></code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The value of the custom parameter.
- <code><strong>displayStrings</strong>: array</code><a name="spec-glyphs-4-displayStrings"></a>
    - <code><strong>#</strong>: string</code>
- <code><strong>featurePrefix</strong>: object</code><a name="spec-glyphs-4-featurePrefix"></a> – (`GSFeaturePrefix`)
    - <code><strong>automatic</strong>: boolean = false</code> – Whether the code of the feature prefix is generated automatically.
    - <code><strong>code</strong>: string = ""</code> – The code of the feature prefix. Example: `"languagesystem DFLT dflt;"`.
    - <code><strong>disabled</strong>: boolean = false</code> – Whether the feature prefix is disabled.
    - <code><strong>name</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the feature prefix. Example: `"Languagesystems"`.
    - <code><strong>notes</strong>: string = ""</code> – A string serving as a description or comment about the feature prefix.
- <code><strong>feature</strong>: object</code><a name="spec-glyphs-4-feature"></a> – (`GSFeature`)
    - <code><strong>automatic</strong>: boolean = false</code> – Whether the code of the feature is generated automatically.
    - <code><strong>code</strong>: string = ""</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The code of the feature. Example: `"sub a by a.alt;"`.
    - <code><strong>disabled</strong>: boolean = false</code> – Whether the feature is disabled.
    - <code><strong>labels</strong>: array = []</code> – The labels of the feature.
 See [`infoValue`](#spec-glyphs-4-infoValue) for items.
    - <code><strong>notes</strong>: string = ""</code> – A string serving as a description or comment about the feature.
    - <code><strong>tag</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The four-letter tag of the feature. Example: `"calt"`.
- <code><strong>fontMaster</strong>: object</code><a name="spec-glyphs-4-fontMaster"></a> – (`GSFontMaster`)
    - <code><strong>active</strong>: boolean = true</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Whether the master is active.
    - <code><strong>axesValues</strong>: array = []</code> – The designspace location of the master.
        - <code><strong>#</strong>: number</code> (`f64`)
    - <code><strong>customParameters</strong>: array = []</code> – The custom parameters of the master.
 See [`customParameter`](#spec-glyphs-4-customParameter) for items.
    - <code><strong>guides</strong>: array = []</code> – The global guides of the master.
 See [`guide`](#spec-glyphs-4-guide) for items.
    - <code><strong>iconName</strong>: string = "Regular"</code> – The name of the icon that represents the master. Generally omitted when equal to `Regular`, or equal to the default icon name of the master (`GSFontMaster.defaultIconName`). For a list of available names, consult `GSFontMaster.iconNames()`.
    - <code><strong>id</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The unique identifier of the master.
    - <code><strong>metricValues</strong>: array = []</code> – The metric values of the master.
 See [`metricStore`](#spec-glyphs-4-metricStore) for items.
    - <code><strong>name</strong>: string</code> – The name of the master. May be omitted in file format version 1 when equal to `Regular` or the default master name.
    - <code><strong>numberValues</strong>: array = []</code> – The number values of the master.
        - <code><strong>#</strong>: number</code> (`f64`)
    - <code><strong>properties</strong>: array = []</code> – The properties of the master.
 See [`infoProperty`](#spec-glyphs-4-infoProperty) for items.
    - <code><strong>stemValues</strong>: array = []</code> – The stem values of the master.
        - <code><strong>#</strong>: number</code> (`f64`)
    - <code><strong>tempData</strong>: object = {}</code> – Auto-save files only: Temporary data associated with the master. See [`userData`](#spec-glyphs-4-userData).
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the master. See [`userData`](#spec-glyphs-4-userData).
    - <code><strong>visible</strong>: boolean = true</code> – Whether the master is visible in the preview.
- <code><strong>glyph</strong>: object</code><a name="spec-glyphs-4-glyph"></a> – (`GSGlyph`)
    - <code><strong>axes</strong>: array = []</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The Smart Glyph variation axes of the glyph.
 See [`axis`](#spec-glyphs-4-axis) for items.
    - <code><strong>case</strong>: string</code> – The case of the glyph. If unset, then the case is based on a glyph data lookup based on the glyph name.
        - Possible values: `"noCase"`, `"upper"`, `"lower"`, `"smallCaps"`, `"minor"`, `"other"`.
    - <code><strong>category</strong>: string</code> – The category of the glyph. If unset, then the category is based on a glyph data lookup based on the glyph name.
    - <code><strong>color</strong></code> – The color label of the glyph. See [`colorLabel`](#spec-glyphs-4-colorLabel).
    - <code><strong>direction</strong>: string</code> – The writing direction of the glyph. If unset, then the writing direction is based on a glyph data lookup based on the glyph name.
        - Possible values: `"BIDI"`, `"LTR"`, `"RTL"`, `"VTR"`, `"VTL"`.
    - <code><strong>export</strong>: boolean = true</code> – Whether the glyph is exported.
    - <code><strong>glyphname</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The name of the glyph.
    - <code><strong>group</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The glyph group name.
    - <code><strong>groupIdx</strong>: integer = 0</code> (`i32`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The index of the glyph within its group.
    - <code><strong>kernBottom</strong>: string</code> – The kerning group of the bottom side of the glyph.
    - <code><strong>kernLeft</strong>: string</code> – The kerning group of the left side of the glyph.
    - <code><strong>kernRight</strong>: string</code> – The kerning group of the right side of the glyph.
    - <code><strong>kernTop</strong>: string</code> – The kerning group of the top side of the glyph.
    - <code><strong>lastChange</strong>: string</code> – The date and time of the last change of the glyph. Example: `"2023-02-25 14:46:49 +0000"`.
    - <code><strong>layers</strong>: array</code> – The layers of the glyph.
 See [`layer`](#spec-glyphs-4-layer) for items.
    - <code><strong>locked</strong>: boolean = false</code> – Whether the glyph is locked.
    - <code><strong>metricBottom</strong>: string</code> – The bottom metrics key of the glyph.
    - <code><strong>metricLeft</strong>: string</code> – The left metrics key of the glyph.
    - <code><strong>metricRight</strong>: string</code> – The right metrics key of the glyph.
    - <code><strong>metricTop</strong>: string</code> – The top metrics key of the glyph.
    - <code><strong>metricVertOrigin</strong>: string</code> – The vertical origin metrics key of the glyph.
    - <code><strong>metricVertWidth</strong>: string</code> – The vertical width metrics key of the glyph.
    - <code><strong>metricWidth</strong>: string</code> – The width metrics key of the glyph.
    - <code><strong>note</strong>: string = ""</code> – A string serving as a description or comment about the glyph.
    - <code><strong>partsSettings</strong>: array = []</code> – A list of the Smart Glyph properties and their top/bottom values.
 See [`partProperty`](#spec-glyphs-4-partProperty) for items.
    - <code><strong>production</strong>: string</code> – The production name of the glyph. If unset, then the production name is based on a glyph data lookup based on the glyph name or the Unicode code point.
    - <code><strong>script</strong>: string</code> – The script of the glyph. If unset, then the script is based on a glyph data lookup based on the glyph name.
    - <code><strong>sortName</strong>: string</code> – The sort name of the glyph. If unset, then the sort name is based on a glyph data lookup based on the glyph name.
    - <code><strong>sortNameKeep</strong>: string</code> – The sort name of the glyph used in the *Keep Alternates Next to Base Glyph* display mode. If unset, then the sort name is based on a glyph data lookup based on the glyph name.
    - <code><strong>subCategory</strong>: string</code> – The subcategory of the glyph. If unset, then the subcategory is based on a glyph data lookup based on the glyph name.
    - <code><strong>tags</strong>: array = []</code> – The tags of the glyph, sorted lexicographically.
        - <code><strong>#</strong>: string</code>
    - <code><strong>unicode</strong></code> – The Unicode code points of the glyph. One of 2 options.
        - Option. `integer` (`u32`) – The code point value. Examples: `65`, `125184`, `0`.
        - Option. `array` – An ascending list of code point values.
 Min count: 2.
            - <code><strong>#</strong>: integer</code> (`u32`) Examples: `65`, `125184`, `0`.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the glyph. See [`userData`](#spec-glyphs-4-userData).
- <code><strong>guide</strong>: object</code><a name="spec-glyphs-4-guide"></a> – (`GSGuide`)
    - <code><strong>angle</strong>: number = 0</code> (`f64`) – The angle at which the guide is drawn in degrees clockwise.
    - <code><strong>attr</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The attributes of the guide. See [`attr`](#spec-glyphs-4-attr).
    - <code><strong>filter</strong>: string</code> – The filter of the guide. The syntax is the description of [NSPredicate](https://developer.apple.com/documentation/foundation/nspredicate). Omitted when no filter is defined.
    - <code><strong>grid</strong>: number = 0</code> (`f64`) – The grid of the guide.
    - <code><strong>length</strong>: number = 0</code> (`f64`) – The length of a line-type guide.
    - <code><strong>lockAngle</strong>: boolean = false</code> – Whether the angle of the guide is locked.
    - <code><strong>locked</strong>: boolean = false</code> – Whether the guide is locked.
    - <code><strong>name</strong>: string = ""</code> – The name of the guide.
    - <code><strong>orientation</strong>: string = "left"</code> – The orientation of the guide. See [`orientation`](#spec-glyphs-4-orientation).
        - Possible values: `"left"`, `"center"`, `"right"`.
    - <code><strong>pos</strong>: array = [0, 0]</code> – The position of the guide. See [`pos`](#spec-glyphs-4-pos).
    - <code><strong>showMeasurement</strong>: boolean = false</code> – Whether the measurement of the guide is shown.
    - <code><strong>size</strong>: array = [0, 0]</code> – The size of the guide. See [`size`](#spec-glyphs-4-size).
    - <code><strong>slope</strong>: boolean = false</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Whether the guide has a slope.
    - <code><strong>type</strong>: string = "Line"</code> – The type of the guide.
        - Possible values: `"Line"`, `"Circle"`, `"Rect"`.
- <code><strong>gradient</strong></code><a name="spec-glyphs-4-gradient"></a> – (`GSGradient`) One of 3 options.
    - Option. `object` – (`GSLinearGradient`) – A linear gradient.
        - <code><strong>colors</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The color stops of the gradient. See [`gradientColors`](#spec-glyphs-4-gradientColors).
        - <code><strong>end</strong>: array</code> – The end point of the linear gradient relative to the shape bounds. See [`pos`](#spec-glyphs-4-pos).
        - <code><strong>extend</strong>: string = "pad"</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – How the gradient behaves outside the start/end range. Omitted for pad mode. See [`gradientExtend`](#spec-glyphs-4-gradientExtend).
            - Possible values: `"repeat"`, `"reflect"`.
        - <code><strong>start</strong>: array</code> – The start point of the linear gradient relative to the shape bounds. See [`pos`](#spec-glyphs-4-pos).
    - Option. `object` – (`GSRadialGradient`) – A radial gradient.
        - <code><strong>angle</strong>: number = 0</code> (`f64`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The radial gradient angle.
        - <code><strong>colors</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The color stops of the gradient. See [`gradientColors`](#spec-glyphs-4-gradientColors).
        - <code><strong>end</strong>: array</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The end center of the radial gradient relative to the shape bounds. See [`pos`](#spec-glyphs-4-pos).
        - <code><strong>endRadius</strong>: number</code> (`f64`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The end radius of the radial gradient relative to the shape bounds.
        - <code><strong>extend</strong>: string = "pad"</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – How the gradient behaves outside the start/end range. Omitted for pad mode. See [`gradientExtend`](#spec-glyphs-4-gradientExtend).
            - Possible values: `"repeat"`, `"reflect"`.
        - <code><strong>start</strong>: array</code> – The start center of the radial gradient relative to the shape bounds. See [`pos`](#spec-glyphs-4-pos).
        - <code><strong>startRadius</strong>: number = 0</code> (`f64`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The start radius of the radial gradient relative to the shape bounds.
        - <code><strong>type</strong>: string = "radial"</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The radial gradient type marker.
    - Option. `object` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – (`GSConicGradient`) – A conic gradient.
        - <code><strong>angle</strong>: number = 360</code> (`f64`) – The angular extent of the conic gradient.
        - <code><strong>center</strong>: array</code> – The center of the conic gradient relative to the shape bounds. See [`pos`](#spec-glyphs-4-pos).
        - <code><strong>colors</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The color stops of the gradient. See [`gradientColors`](#spec-glyphs-4-gradientColors).
        - <code><strong>controlRadius</strong>: number = 0</code> (`f64`) – The radius used to control the conic gradient.
        - <code><strong>extend</strong>: string = "pad"</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – How the gradient behaves outside the start/end range. Omitted for pad mode. See [`gradientExtend`](#spec-glyphs-4-gradientExtend).
            - Possible values: `"repeat"`, `"reflect"`.
        - <code><strong>startAngle</strong>: number = 0</code> (`f64`) – The start angle of the conic gradient.
        - <code><strong>type</strong>: string = "conic"</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The conic gradient type marker.
- <code><strong>gradientColors</strong>: array</code><a name="spec-glyphs-4-gradientColors"></a>
 See [`gradientColorStop`](#spec-glyphs-4-gradientColorStop) for items.
- <code><strong>gradientExtend</strong>: string = "pad"</code><a name="spec-glyphs-4-gradientExtend"></a>
    - Possible values: `"repeat"`, `"reflect"`.
- <code><strong>gradientColorStop</strong>: array</code><a name="spec-glyphs-4-gradientColorStop"></a> – (`GSColorStop`)
 Tuple with 2 items.
    - <code><strong>#0</strong></code> – The color of the stop. See [`color`](#spec-glyphs-4-color).
    - <code><strong>#1</strong>: number</code> (`f64`) – The offset of the stop.
- <code><strong>hint</strong>: object</code><a name="spec-glyphs-4-hint"></a> – (`GSHint`)
    - <code><strong>horizontal</strong>: boolean = false</code> – Whether the hint is horizontal. Not written for path components.
    - <code><strong>name</strong>: string</code> – The name of the hint.
    - <code><strong>options</strong>: number = 0</code> (`u32`) – The options of the hint.
    - <code><strong>origin</strong></code> – The origin of the hint. See [`indexPath`](#spec-glyphs-4-indexPath).
    - <code><strong>other1</strong></code> – The first other point of the hint, used by TrueType instructions that need more than two nodes. See [`indexPath`](#spec-glyphs-4-indexPath).
    - <code><strong>other2</strong></code> – The second other point of the hint, used by TrueType instructions that need more than three nodes. See [`indexPath`](#spec-glyphs-4-indexPath).
    - <code><strong>place</strong>: array</code>
 Tuple with 2 items.
        - <code><strong>#0</strong>: number</code> (`f64`) – The origin placement.
        - <code><strong>#1</strong>: number</code> (`f64`) – The width of the hint. `21` for bottom ghost hints and flex hints, `-20` for top ghost hints.
    - <code><strong>scale</strong>: array = [1, 1]</code> – The scale of the hint. See [`scale`](#spec-glyphs-4-scale).
    - <code><strong>settings</strong>: object</code> – The settings of the hint.
    - <code><strong>stem</strong>: number</code> (`i32`) – The stem of the hint.
    - <code><strong>target</strong></code> See [`indexPath`](#spec-glyphs-4-indexPath).
    - <code><strong>type</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The type of the hint.
        - Possible values: `"TopGhost"`, `"BottomGhost"`, `"Stem"`, `"Flex"`, `"TTStem"`, `"TTShift"`, `"TTSnap"`, `"TTInterpolate"`, `"TTDiagonal"`, `"TTDelta"`, `"Tag"`, `"Corner"`, `"Cap"`, `"Brush"`, `"Segment"`, `"Head"`, `"Auto"`, `"Unknown"`.
- <code><strong>image</strong>: object</code><a name="spec-glyphs-4-image"></a> – (`GSImage`)
    - <code><strong>alpha</strong>: number = 50</code> (`f64`) – The alpha value of the image.
    - <code><strong>angle</strong>: number = 0</code> (`f64`) – The rotation angle of the image in degrees clockwise.
    - <code><strong>attr</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The attributes of the image. See [`attr`](#spec-glyphs-4-attr).
    - <code><strong>crop</strong>: array</code> – The cropped frame of the image, specified as the crop origin X/Y and size width/height.
 Tuple with 4 items.
        - <code><strong>#0</strong>: number</code> (`f64`) – The X coordinate of the crop origin.
        - <code><strong>#1</strong>: number</code> (`f64`) – The Y coordinate of the crop origin.
        - <code><strong>#2</strong>: number</code> (`f64`) – The width of the crop size.
        - <code><strong>#3</strong>: number</code> (`f64`) – The height of the crop size.
    - <code><strong>imagePath</strong>: string</code> – The file path of the image file relative to the document file.
    - <code><strong>imageURL</strong>: string</code> – The URL bookmark data of the image file path.
    - <code><strong>locked</strong>: boolean = false</code> – Whether the image is locked.
    - <code><strong>pos</strong>: array = [0, 0]</code> – The position of the image. See [`pos`](#spec-glyphs-4-pos).
    - <code><strong>scale</strong>: array = [1, 1]</code> – The scale factor of the image. See [`scale`](#spec-glyphs-4-scale).
    - <code><strong>slant</strong>: array = [0, 0]</code> – The slant factor of the image. See [`slant`](#spec-glyphs-4-slant).
- <code><strong>instance</strong>: object</code><a name="spec-glyphs-4-instance"></a> – (`GSInstance`)
    - <code><strong>axesValues</strong>: array</code> – The internal axis locations of the instance. These values are also used for the external axis locations, if no external axis locations are specified separately.
        - <code><strong>#</strong>: number</code> (`f64`)
    - <code><strong>customParameters</strong>: array = []</code> – The custom parameters of the instance.
 See [`customParameter`](#spec-glyphs-4-customParameter) for items.
    - <code><strong>exports</strong>: boolean = true</code> – Whether the instance is exported.
    - <code><strong>id</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The unique ID of the instance.
    - <code><strong>instanceInterpolations</strong>: object = {}</code> – The interpolation factors where the keys are the master IDs.
        - <code>string</code> One of 2 options.
            - Option. `number` (`f64`) – The X and Y factors are the same.
            - Option. `array` – The X and Y factors.
 Tuple with 2 items.
                - <code><strong>#0</strong>: number</code> (`f64`) – The X factor.
                - <code><strong>#1</strong>: number</code> (`f64`) – The Y factor.
    - <code><strong>isBold</strong>: boolean = false</code> – Whether the instance is bold.
    - <code><strong>isItalic</strong>: boolean = false</code> – Whether the instance is italic.
    - <code><strong>linkStyle</strong>: string</code> – The name of the style-linked instance.
    - <code><strong>manualInterpolation</strong>: boolean = false</code> – Whether the `instanceInterpolations` values are used. Otherwise, the values are calculated from the axis values.
    - <code><strong>properties</strong>: array = []</code>
 See [`infoProperty`](#spec-glyphs-4-infoProperty) for items.
    - <code><strong>type</strong>: string = "single"</code> – The type of the instance.
        - Possible values: `"single"`, `"variable"`, `"static"`, `"icon"`, `"particles"`.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the instance. See [`userData`](#spec-glyphs-4-userData).
    - <code><strong>visible</strong>: boolean = true</code> – Whether the instance is visible when previewing all instances.
    - <code><strong>weightClass</strong>: integer = 400</code> (`u16`) – The weight class of the instance.
    - <code><strong>widthClass</strong>: integer = 5</code> (`u16`) – The width class of the instance.
- <code><strong>indexPath</strong></code><a name="spec-glyphs-4-indexPath"></a> One of 4 options.
    - Option. `array` – The index path of a node on a path.
 Tuple with 2 items.
        - <code><strong>#0</strong>: number</code> (`u32`) – The index of a path shape.
        - <code><strong>#1</strong>: number</code> (`u32`) – The index of a node on a path.
    - Option. `array` – The index path of an inflection, where the first two path components point to an on-curve node that finishes a curve segment. The inflection component is most likely `0`.
 Tuple with 3 items.
        - <code><strong>#0</strong>: number</code> (`u32`) – The index of a path shape.
        - <code><strong>#1</strong>: number</code> (`u32`) – The index of a node on a path.
        - <code><strong>#2</strong>: number</code> (`u32`) – The index of an inflection.
    - Option. `array` – Points to the intersection of two path segments. The nodes are the ones finishing the segments.
 Tuple with 4 items.
        - <code><strong>#0</strong>: number</code> (`u32`) – The index of a path shape (P1).
        - <code><strong>#1</strong>: number</code> (`u32`) – The index of a node (N1) on P1.
        - <code><strong>#2</strong>: number</code> (`u32`) – The index of a path shape (P2).
        - <code><strong>#3</strong>: number</code> (`u32`) – The index of a node (N2) on P2.
    - Option. `string` – An attachment to the left or right side-bearing.
        - Possible values: `"lsb"`, `"rsb"`.
- <code><strong>kerning</strong>: object = {}</code><a name="spec-glyphs-4-kerning"></a> – Maps master IDs to kerning definitions.
    - <code>string: object</code> – Maps glyph names or class names to kerning partners.
        - <code>string: object</code> – Maps glyph names or class names to kerning values.
            - <code>string: number</code> (`f64`)
- <code><strong>kerningContext</strong>: object = {}</code><a name="spec-glyphs-4-kerningContext"></a> – Maps kerning contexts to kerning definitions.
    - <code>string: object</code> – Maps master IDs to kerning values.
        - <code>string: number</code> (`f64`)
- <code><strong>layer</strong>: object</code><a name="spec-glyphs-4-layer"></a> – (`GSLayer`)
    - <code><strong>active</strong>: boolean = true</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Whether the layer is active.
    - <code><strong>anchors</strong>: array = []</code> – The anchors of the layer.
 See [`anchor`](#spec-glyphs-4-anchor) for items.
    - <code><strong>annotations</strong>: array = []</code> – The annotations of the layer.
 See [`annotation`](#spec-glyphs-4-annotation) for items.
    - <code><strong>associatedMasterId</strong>: string</code> – The unique identifier of the associated master. Omitted when equalt to the layer ID.
    - <code><strong>attr</strong>: object = {}</code> – The attributes of the layer. See [`layerAttr`](#spec-glyphs-4-layerAttr).
    - <code><strong>background</strong>: object</code>
        - <code><strong>anchors</strong>: array = []</code> – The anchors of the background layer.
 See [`anchor`](#spec-glyphs-4-anchor) for items.
        - <code><strong>annotations</strong>: array = []</code> – The annotations of the background layer.
 See [`annotation`](#spec-glyphs-4-annotation) for items.
        - <code><strong>backgroundImage</strong>: object</code> – The background image of the layer. See [`image`](#spec-glyphs-4-image).
        - <code><strong>guides</strong>: array = []</code> – The guides of the background layer.
 See [`guide`](#spec-glyphs-4-guide) for items.
        - <code><strong>hints</strong>: array = []</code> – The hints of the background layer.
 See [`hint`](#spec-glyphs-4-hint) for items.
        - <code><strong>shapes</strong>: array = []</code> – The shapes of the background layer.
 See [`shape`](#spec-glyphs-4-shape) for items.
    - <code><strong>backgroundImage</strong>: object</code> – The background image of the layer. See [`image`](#spec-glyphs-4-image).
    - <code><strong>color</strong></code> – The color label of the layer. See [`colorLabel`](#spec-glyphs-4-colorLabel).
    - <code><strong>guides</strong>: array = []</code> – The guides of the layer.
 See [`guide`](#spec-glyphs-4-guide) for items.
    - <code><strong>hints</strong>: array = []</code> – The hints of the layer.
 See [`hint`](#spec-glyphs-4-hint) for items.
    - <code><strong>layerId</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The unique ID of the layer. Matches the master ID when the layer is a master layer.
    - <code><strong>metricBottom</strong>: string</code> – The bottom metrics key of the layer.
    - <code><strong>metricLeft</strong>: string</code> – The left metrics key of the layer.
    - <code><strong>metricRight</strong>: string</code> – The right metrics key of the layer.
    - <code><strong>metricTop</strong>: string</code> – The top metrics key of the layer.
    - <code><strong>metricVertOrigin</strong>: string</code> – The vertical origin metrics key of the layer.
    - <code><strong>metricVertWidth</strong>: string</code> – The vertical width metrics key of the layer.
    - <code><strong>metricWidth</strong>: string</code> – The width metrics key of the layer.
    - <code><strong>name</strong>: string = ""</code> – The name of the layer. Master layers and other special layers display a name in the Glyphs UI that is derived from the layers role (for example, the name of the master that the layer belongs to). These derived names are not written to the file. Instead, this name is only displayed in the UI for non-special layers (like backup layers).
    - <code><strong>partSelection</strong>: object</code> – The Smart Glyph setting of the layer. The keys are the property names. The values are either `1` if the layer corresponds to the bottom value of the property or `2` if the layer corresponds to the top value of the property. If a layer is neither the top nor the bottom value, the property is omitted.
        - <code>string: integer</code> One of 2 options.
            - Option. `1` – Bottom: the layer corresponds to the bottom value of the property.
            - Option. `2` – Top: the layer corresponds to the top value of the property.
    - <code><strong>shapes</strong>: array = []</code> – The shapes of the layer.
 See [`shape`](#spec-glyphs-4-shape) for items.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the layer. See [`userData`](#spec-glyphs-4-userData).
    - <code><strong>vertOrigin</strong>: number = 0</code> (`f64`) – The vertical origin of the layer.
    - <code><strong>vertWidth</strong>: number = 0</code> (`f64`) – The vertical width of the layer.
    - <code><strong>visible</strong>: boolean = false</code> – Whether the layer is visible.
    - <code><strong>width</strong>: number</code> (`f64`) <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The width of the layer.
- <code><strong>layerAttr</strong>: object</code><a name="spec-glyphs-4-layerAttr"></a>
    - <code><strong>axisRules</strong>: array = []</code> – Alternative-layer rules, ordered like the font axes.
        - <code><strong>#</strong>: object</code>
            - <code><strong>min</strong>: number</code> (`f64`) – The minimum matching axis value.
            - <code><strong>max</strong>: number</code> (`f64`) – The maximum matching axis value.
    - <code><strong>color</strong>: boolean = false</code> – Whether the layer is an Apple color layer.
    - <code><strong>colorPalette</strong></code> – The color palette index of a color palette layer. One of 2 options.
        - Option. `integer` (`u16`) – The color palette index of a color palette layer.
        - Option. `"*"` – The foreground text color (color index 65535).
    - <code><strong>coordinates</strong>: array = []</code> – Intermediate-layer coordinates, ordered like the relevant axes. Starting in version 4, also contains the glyph-local axis coordinates for layers of Smart Glyphs.
        - <code><strong>#</strong></code> One of 2 options.
            - Option. `number` (`f64`) – The explicit coordinate value.
            - Option. `"-"` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Use the default value for this axis.
    - <code><strong>sbixSize</strong>: integer</code> (`u16`) – The Apple sbix image size.
    - <code><strong>svg</strong>: boolean = false</code> – Whether the layer is an SVG color layer.
- <code><strong>lineCap</strong>: integer</code><a name="spec-glyphs-4-lineCap"></a> (`u8`) One of 7 options.
    - Option. `0` – Butt: ends the stroke at the path endpoint.
    - Option. `1` – Round: extends the stroke with a semicircular cap.
    - Option. `2` – Square: extends the stroke with a square cap.
    - Option. `3` – Round inset: ends the stroke with an inset semicircular cap.
    - Option. `4` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Align to axis: aligns the cap to the nearest coordinate axis.
    - Option. `5` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Align to x-axis: aligns the cap to the x-axis.
    - Option. `6` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Align to y-axis: aligns the cap to the y-axis.
- <code><strong>metric</strong>: object</code><a name="spec-glyphs-4-metric"></a> – (`GSMetric`)
    - <code><strong>filter</strong>: string</code> – The filter of the metric limiting the scope of the metric to a subset of glyphs.
    - <code><strong>horizontal</strong>: boolean = false</code> – Whether the metric is a horizontal metric.
    - <code><strong>name</strong>: string</code> – The name of the metric.
    - <code><strong>type</strong>: string</code> – The type of the metric.
        - Possible values: `"ascender"`, `"cap height"`, `"slant height"`, `"x-height"`, `"midHeight"`, `"bodyHeight"`, `"descender"`, `"baseline"`, `"italic angle"`, `"italic slope"`.
- <code><strong>metricStore</strong>: object</code><a name="spec-glyphs-4-metricStore"></a> – (`GSMetricStore`)
    - <code><strong>over</strong>: number = 0</code> (`f64`) – The overshoot of the metric value.
    - <code><strong>pos</strong>: number = 0</code> (`f64`) – The offset from the baseline of the metric value.
- <code><strong>node</strong>: array</code><a name="spec-glyphs-4-node"></a> – (`GSNode`)
 Tuple with 3–4 items.
    - <code><strong>#0</strong>: number</code> (`f64`) – The x-coordinate of the node.
    - <code><strong>#1</strong>: number</code> (`f64`) – The y-coordinate of the node.
    - <code><strong>#2</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The configuration of the node expressed as a sequence of characters. Types: `m`: move, `l`: line, `c`: cubic curve, `q`: quadratic curve, `u`: quartic curve, `h`: Hobby curve, `r`: Raph New Spiral, `o`: off-curve. Connections (may follow on-curve types): `s`: smooth, `t`: tangent. Orientation (left is the default): `R`: right, `C`: center. Locking (not locked is the default): `X`: locked.
    - <code><strong>#3</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The attributes of the node. See [`nodeAttr`](#spec-glyphs-4-nodeAttr).
- <code><strong>nodeAttr</strong>: object</code><a name="spec-glyphs-4-nodeAttr"></a>
    - <code><strong>hoi</strong>: object = {}</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Maps axis tags to higher-order interpolation descriptions. The info is stored in the lower node for the HOI span of that axis.
        - <code>string</code> One of 3 options.
            - Option. `object` – HOI intermediate point.
                - <code><strong>ip</strong>: array</code>
 Tuple with 2 items.
                    - <code><strong>#0</strong>: number</code> (`f64`) – The x-coordinate of the intermediate point.
                    - <code><strong>#1</strong>: number</code> (`f64`) – The y-coordinate of the intermediate point.
            - Option. `object` – HOI rotation.
                - <code><strong>rc</strong></code> – HOI rotation center. One of 2 options.
                    - Option. `array`
 Tuple with 2 items.
                        - <code><strong>#0</strong>: number</code> (`f64`) – The x-coordinate of the rotation center.
                        - <code><strong>#1</strong>: number</code> (`f64`) – The y-coordinate of the rotation center.
                    - Option. `"auto"` – The rotation center is automatically determined based on the shared center of the lower HOI shape and upper HOI shape.
                - <code><strong>rd</strong>: string</code> – The rotation direction: clockwise or counter-clockwise. When not set, the direction with the smallest angle is used.
                    - Possible values: `"cw"`, `"ccw"`.
            - Option. `object` – HOI Bézier interpolation. The time is the linear interpolation from the associated node to the other node. The amplitude is the offset orthogonal to the line connecting the associated node and the other node as a percentage of the length of that line.
                - <code><strong>tl</strong>: number = 0.3333333333333333</code> (`f64`) – Lower time.
                - <code><strong>tu</strong>: number = 0.3333333333333333</code> (`f64`) – Upper time.
                - <code><strong>al</strong>: number = 0</code> (`f64`) – Lower amplitude.
                - <code><strong>au</strong>: number = 0</code> (`f64`) – Upper amplitude.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the node. See [`userData`](#spec-glyphs-4-userData).
- <code><strong>infoProperty</strong></code><a name="spec-glyphs-4-infoProperty"></a> – (`GSInfoProperty`) One of 2 options.
    - Option. `object`
        - <code><strong>key</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The key of the property.
        - <code><strong>value</strong></code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The value of the property.
    - Option. `object`
        - <code><strong>key</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The key of the property.
        - <code><strong>values</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The values of the property.
 See [`infoValue`](#spec-glyphs-4-infoValue) for items.
- <code><strong>infoValue</strong>: object</code><a name="spec-glyphs-4-infoValue"></a> – (`GSInfoValue`)
    - <code><strong>language</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The language tag of the string value. The tag is based on the [OpenType Language System Tags](https://learn.microsoft.com/en-us/typography/opentype/spec/languagetags) but omitts trailing whitespace. Examples: `"dflt"`, `"DEU"`.
    - <code><strong>value</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The localized string value.
- <code><strong>orientation</strong>: string</code><a name="spec-glyphs-4-orientation"></a> – (`GSElementOrientation`)
    - Possible values: `"left"`, `"center"`, `"right"`.
- <code><strong>partProperty</strong>: object</code><a name="spec-glyphs-4-partProperty"></a> – (`GSPartProperty`)
    - <code><strong>bottomValue</strong>: integer</code> (`i32`) – The lower end of the value range of the property.
    - <code><strong>name</strong>: string</code> – The name of the property.
    - <code><strong>topValue</strong>: integer</code> (`i32`) – The upper end of the value range of the property.
- <code><strong>palettes</strong>: object</code><a name="spec-glyphs-4-palettes"></a> – (`GSPalettes`) – The version 4 structure of the `Color Palettes` custom parameter.
    - <code><strong>names</strong>: object = {}</code> – Maps color indices to color names.
        - <code>string: string</code>
    - <code><strong>palettes</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The color palettes.
        - <code><strong>#</strong>: object</code>
            - <code><strong>backgroundStyle</strong>: array = []</code> – Which UI background styles the palette is intended for.
                - <code><strong>#</strong>: string</code>
                    - Possible values: `"dark"`, `"light"`.
            - <code><strong>colors</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The colors of the palette.
 See [`color`](#spec-glyphs-4-color) for items.
            - <code><strong>name</strong>: string</code> – The palette name.
- <code><strong>path</strong>: object</code><a name="spec-glyphs-4-path"></a> – (`GSPath`)
    - <code><strong>attr</strong>: object = {}</code> – The attributes of the path. See [`shapeAttr`](#spec-glyphs-4-shapeAttr).
    - <code><strong>closed</strong>: boolean</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – Whether the path is closed.
    - <code><strong>locked</strong>: boolean = false</code> – Whether the path is locked.
    - <code><strong>nodes</strong>: array</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The on- and off-curve nodes of the path.
 See [`node`](#spec-glyphs-4-node) for items.
- <code><strong>pos</strong>: array</code><a name="spec-glyphs-4-pos"></a>
 Tuple with 2 items.
    - <code><strong>#0</strong>: number</code> (`f64`) – The x-coordinate of the position.
    - <code><strong>#1</strong>: number</code> (`f64`) – The y-coordinate of the position.
- <code><strong>scale</strong>: array</code><a name="spec-glyphs-4-scale"></a>
 Tuple with 2 items.
    - <code><strong>#0</strong>: number</code> (`f64`) – The horizontal scale factor.
    - <code><strong>#1</strong>: number</code> (`f64`) – The vertical scale factor.
- <code><strong>shape</strong></code><a name="spec-glyphs-4-shape"></a> – (`GSShape`) One of 4 options.
    - Option. `object` See [`path`](#spec-glyphs-4-path).
    - Option. `object` See [`component`](#spec-glyphs-4-component).
    - Option. `object` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> See [`image`](#spec-glyphs-4-image).
    - Option. `object` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> See [`shapeGroup`](#spec-glyphs-4-shapeGroup).
- <code><strong>shapeAttr</strong>: object</code><a name="spec-glyphs-4-shapeAttr"></a>
    - <code><strong>color</strong></code> – The color label of the shape. See [`colorLabel`](#spec-glyphs-4-colorLabel).
    - <code><strong>compositing</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The compositing operation used to draw the shape. Omitted for the default source-over operation.
    - <code><strong>fill</strong>: boolean = false</code> – Whether a stroked path is also filled.
    - <code><strong>fillColor</strong></code> – The fill color of the shape. See [`color`](#spec-glyphs-4-color).
    - <code><strong>gradient</strong></code> – The fill gradient of the shape. See [`gradient`](#spec-glyphs-4-gradient).
    - <code><strong>group</strong>: string</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The ID of the parent shape group. Omitted for shapes in the root group.
    - <code><strong>hidden</strong>: boolean = false</code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – Whether the shape is hidden.
    - <code><strong>lineCapEnd</strong>: integer = 0</code> (`u8`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The line cap style at the end of the stroke. See [`lineCap`](#spec-glyphs-4-lineCap).
    - <code><strong>lineCapStart</strong>: integer = 0</code> (`u8`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The line cap style at the start of the stroke. See [`lineCap`](#spec-glyphs-4-lineCap).
    - <code><strong>lineJoin</strong>: integer = 0</code> (`u8`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The line join style of the stroke. One of 4 options.
        - Option. `0` – Miter: extends the segment edges until they intersect.
        - Option. `1` – Round: connects the segment edges with a circular arc.
        - Option. `2` – Bevel: connects the segment edges with a straight edge.
        - Option. `3` – Round full: connects the complete segment ends with a circular arc.
    - <code><strong>mask</strong>: integer = 0</code> (`u8`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – How the shape masks preceding shapes in the same composition unit. One of 3 options.
        - Option. `0` – None: does not use the shape as a mask.
        - Option. `1` – Subtract: removes the area covered by the shape.
        - Option. `2` – Intersect: retains only the area covered by the shape.
    - <code><strong>opacity</strong>: number = 1</code> (`f64`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The opacity of the shape.
    - <code><strong>reversePaths</strong>: boolean = false</code> – Whether paths from the shape are reversed for drawing/export.
    - <code><strong>shadow</strong>: object</code> – The outer shadow of the shape. See [`shadow`](#spec-glyphs-4-shadow).
    - <code><strong>shadowIn</strong>: object</code> – The inner shadow of the shape. See [`shadow`](#spec-glyphs-4-shadow).
    - <code><strong>strokeColor</strong></code> – The stroke color of the shape. See [`color`](#spec-glyphs-4-color).
    - <code><strong>strokeGradient</strong></code> <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center"> – The stroke gradient of the shape. See [`gradient`](#spec-glyphs-4-gradient).
    - <code><strong>strokeHeight</strong></code> – The vertical stroke size, or an expression resolving to one. Falls back to the value of `strokeWidth` when unset. One of 2 options.
        - Option. `number` (`f64`)
        - Option. `string` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center">
    - <code><strong>strokePos</strong></code> – The stroke position. In version 4, values range from inside (-1) through centered (0) to outside (1). In version 3, values range from outside (0) through centered (0.5) to inside (1). One of 2 options.
        - Option. `number` (`f64`) <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center">
        - Option. `string` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center">
    - <code><strong>strokeWidth</strong></code> – The horizontal stroke size, or an expression resolving to one. One of 2 options.
        - Option. `number` (`f64`)
        - Option. `string` <img alt="new" src="https://img.shields.io/badge/new-1c6d37" align="center">
- <code><strong>shapeGroup</strong>: object</code><a name="spec-glyphs-4-shapeGroup"></a> – (`GSShapeGroup`)
    - <code><strong>attr</strong>: object = {}</code> – The attributes of the shape group. See [`shapeAttr`](#spec-glyphs-4-shapeAttr).
    - <code><strong>groupId</strong>: string</code> <img alt="required" src="https://img.shields.io/badge/required-204d7e" align="center"> – The unique ID of the shape group. The empty string is reserved for the layer’s root group and is not written as a shape group.
- <code><strong>shadow</strong>: object</code><a name="spec-glyphs-4-shadow"></a> – (`GSShadow`)
    - <code><strong>blur</strong>: string = "4"</code> – The shadow blur radius, stored as an expression string.
    - <code><strong>color</strong></code> – The shadow color. See [`color`](#spec-glyphs-4-color).
    - <code><strong>offsetX</strong>: string = "4"</code> – The horizontal shadow offset, stored as an expression string.
    - <code><strong>offsetY</strong>: string = "4"</code> – The vertical shadow offset, stored as an expression string.
- <code><strong>size</strong>: array</code><a name="spec-glyphs-4-size"></a>
 Tuple with 2 items.
    - <code><strong>#0</strong>: number</code> (`f64`) – The width.
    - <code><strong>#1</strong>: number</code> (`f64`) – The height.
- <code><strong>slant</strong>: array</code><a name="spec-glyphs-4-slant"></a>
 Tuple with 2 items.
    - <code><strong>#0</strong>: number</code> (`f64`) – The horizontal slant factor.
    - <code><strong>#1</strong>: number</code> (`f64`) – The vertical slant factor.
- <code><strong>userData</strong>: object</code><a name="spec-glyphs-4-userData"></a>

## Changes

### 17. July 2026

- Add JSON schemas and documentation for Glyphs file format version 4.
- Add version 4 fields and types based on current save/property-list serialization.
- Update drawing attributes for gradients, colors, caps, joins, masks, shadows, and hidden shapes.
- Update package schema conditions for version 4 package files.
