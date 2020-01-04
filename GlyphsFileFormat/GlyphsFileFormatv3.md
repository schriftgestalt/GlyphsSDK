# Glyphs File Format, Version 3
Glyphs saves its files in plaintext format. So the files can be viewed and edited with any text editor. Open an existing `.glyphs` file to see how it works.

- The format is based on Apples old style property list (plist) format.
- It doesn’t use the more common XML-based flavor (that is supported for reading) to save space.
- There are some small deviations from the default format. More about that in Notes.

## Changes
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

## Notes
- It is written without indentation. That is to save file size.
- Each key is on its own line.
- Lists have each element on one line, empty `lists` or `dicts` need to span two lines.
- Some lists (enclosed in normal parenthesis) are put on one line (e.g., `(100,200)`). This is to make it easier to read and save space. We call it *tuple* for now.
    * this is used for colors, points and nodes
- empty elements are always omitted. 
    * except: in `userData` entires. There the structure is preserved.
- Numbers are always written without quotes (negative and float). Strings that look like numbers are written with quotes (mostly important in userData).
- Unicodes are written as int numbers.
- The last element in a list doesn’t get a trailing comma.
- Newlines and tabs in strings (e.g. in feature code or classes) are not escaped.
- Several values have global settings in the font object and values in each master (e.g. metrics > metricValues, axes > axesValues, stems > stemValues, numbers > numberValues). The order and count have to match.

## Element Tree
The property list file contains a dictionary with the following structure.

* .appVersion `string` The build number of the app. (e.g. `"1278"`)
* .formatVersion `int` set to `3` for version 3. If that key is missing assume version 2.
* DisplayStrings `list>string`:
* axes `list>dict`: The interpolation axes
    * hidden `bool`: If the axis should be visible in the UI. Always set to `1`, otherwise omit the key
    * name `string`: The name of the axis (e.g. `Weight`)
    * tag `string`: The axis tag (e.g. `wght`)
* classes `list>dict`: OpenType classes.
    * automatic `bool`: Always set to `1`. If the feature is not set to automatic, the key should be omitted.
    * code `string`: A string containing space separated glyph names.
    * disabled `bool`: The class will not be exported. Always set to `1`, otherwise omit the key
    * name `string`: The OpenType class name.
    * notes `string`: Notes.
* customParameters `list>dict`: Font-wide custom parameters.
    * disabled `bool`: The parameter will be ignored. Always set to `1`, otherwise omit the key
    * name `string`: Property name of the custom parameter.
    * value `string`: Value of the custom parameters.
* date `string`: Format `2014-01-29 14:14:38 +0000`.
* disablesAutomaticAlignment `bool`: Always set to `1`, otherwise omit the key
* disablesNiceNames `bool`: Always set to `1`, otherwise omit the key
* familyName `string`
* featurePrefixes `list>dict`: OpenType feature code before the class definitions.
    * automatic `bool`: Always set to `1`, otherwise omit the key
    * code `string`: A string containing feature code.
    * disabled `bool`: The prefix will not be exported. Always set to `1`, otherwise omit the key
    * name `string`: The name of the prefix
    * notes `string`: Notes.
* features `list>dict`
    * automatic `bool`: Always set to `1`, otherwise omit the key
    * code `string`: A string containing feature code.
    * disabled `bool`: The feature will not be exported. Always set to `1`, otherwise omit the key
    * labels `list>dict`: list of stylistic set labels.
        * language `string`: 'dflt' or three letter ISO language tag ("DEU")
        * value `string`: The name
    * notes `string`: The feature notes.
    * tag `string`: The feature tag.
* fontMaster `list>dict`
    * axesValues `list>float`: a list of float values storing the axis coordinate for each axis, Axis settings are stored in the font object. 
    * customParameters `list>dict`: Master-wide custom parameters.
        * name `string`: Property name of the custom parameter.
        * value `string`: Value of the custom parameter.
    * iconName `string`: stores the selected master icon
    * id `string`: a unique id that connects the layers (associated ID) with the master.
    * metricValues `list>dict`: the metrics values, metrics settings are stored in the font object.
        * over `float`: the overshot
        * pos `float`: the position
    * name `string`: The name of the master
    * numberValues `list>float`: a list of floats, number settings are stored in the font object.
    * properties `list>dict`: see [Properties](#properties)
    * stemValues `list>float`: a list of floats, stem settings are stored in the font object.
    * userData `dict`: to store custom data. Only `string`, `int`, `float`, `array`, `dict` and `date` data is allowed.
    * visible `bool`: Always set to `1`, otherwise omit the key.
* glyphs `list>dict`:
    * case `string`: The 'case' if the glyph when manually set. Possible values: "noCase", "upper", "lower", "smallCaps", "other". This could be used to specify 'height' of default numbers (lining sv old style)
    * category `string`: manually set category
    * color `int` or `tuple`: 
        1. If `int`, it is the index of the internal color list
        2. If `tuple`, two to five numbers in the range of 0–255 denoting a Grey+A, RGBA or CMYKA values
    * direction: The writing direction when manually set. Possible values: "BIDI", "LTR", "RTL", "VTL", "VTR".
    * export `bool`: Always set to `0`, otherwise omit the key.
    * glyphname `string`: Must be unique throughout the font.
    * kernBottom `string`: Bottom kerning group
    * kernLeft `string`: Left kerning group
    * kernRight `string`: Right kerning group
    * kernTop `string`:  Top kerning group
    * lastChange `string`: Format `2014-01-29 14:14:38 +0000`.
    * layers `list>dict`
        * anchors `list>dict`
            * name `string`: The name of the anchor.
            * position `string`: format `{X, Y}`
        * annotations `list>dict`:
        * associatedMasterId `string`: ID of the master the layer is linked to. Not present if it equals layerID, i.e. if the layer is in use as master.
        * background `dict`: Contains the same children as the layer itself, except for background, layerId, associatedMasterId and width.
        * backgroundImage `dict`: a image. 
            * angle `float`: The angle. If not set defaults to 0°
            * imagePath `string`: The file path to the image. It is stored relative if close enough. Otherwise the full path.
            * locked `bool`: Always set to `1`, otherwise omit the key
            * pos `tuple`: the origin
            * scale `tuple`: `(scaleX,scaleY)`
        * color `int` or `tuple`: 
            1. If `int`, it is the index of the internal color list
            2. If `tuple`, two to five numbers in the range of 0–255 denoting a Gray+A, RGBA or CMYKA values
        * guides `list>dict`
            * alignment `string`: If the guide is `right` or `center` aligned. Default: `left`
            * angle `float`: The angle. If not set defaults to 0°
            * locked `int`: Always set to `1`, otherwise omit the key
            * showMeasurement `int`: Always set to `1`, otherwise omit the key
            * pos `tuple`: the origin
        * hints `list>dict`
            * horizontal `int`: If set, the hint is horizontal and vertical otherwise
            * type `string`: The type of the hint. Possible value are: Tag, TopGhost, Stem, BottomGhost, Flex, TTAnchor, TTStem, TTAlign, TTInterpolate, TTDiagonal, TTDelta, Corner, Cap, Brush, Line, Auto
                If there is no type, it defaults to Stem, or Ghost if `target` is not set
            * origin `string`: '(pathIndex,nodeIndex)'
                
                TODO: Explain node indexes
            * target `tuple`: `(pathIndex,nodeIndex)`, `up` or `down`
            * other1 `tuple`: `(pathIndex,nodeIndex)` for TT Institutions that need more than two nodes (Interpolation, Diagonal)
            * other2 `tuple`: `(pathIndex,nodeIndex)` for TT Institutions that need more than three nodes (Diagonal)
            * scale `tuple`: `(scaleX,scaleY)` Only used for caps and corners
            * stem `int`: if a stem is manually set
            * options `int`: a bitfield for options
        * layerId `string`
        * metricBottom `string`:
        * metricLeft `string`:
        * metricRight `string`:
        * metricTop `string`:
        * metricVertWidth `string`:
        * metricWidth `string`:
        * name `string`: The name of the layer. Only stored for none master layers (this is changed in 2.3, before the master names where stored)
        * partSelection `dict`: Keys are property names, values are `1` if the layer is selected for the bottom range, `2` for the top.
        * shapes `list>dict`: Can be paths or components
            * path:
                * attributes: `dict`: see [Attributes](*attributes)
                * closed `bool`: Always set to `1`, otherwise omit the key
                * nodes `tuple`: `(X,Y,TYPE[SMOOTH],{user:data})`, where X and Y are the coordinates as float, and TYPE is either `l`, `c`, `o`, `q`. when the on-curve node is smooth, add an `s`. 
                when the node has usedData store it as fourth element. Remove all newlines and extra spaces.
            * component:
                * alignment `int`: controls the automatic alignment of this component. (-1 disables alignment, 1 forces it for glyph that are usually not aligned)
                * anchor `string`: Should be indicated if connected to an anchor, especially if more than one possibility is available, e.g. in ligatures.
                * anchorTo `string`: TODO
                * angle `float`: the rotation
                * attributes: `dict`: see [Attributes](*attributes)
                * locked `bool`: Always set to `1`, otherwise omit the key.
                * name `string`: The name of the linked glyph (i.e., the glyph the component is pointing to).
                * orientation `int`: if left, center or right aligned
                * piece `dict>string:float`: keys are the name of the smart property, values a position on the axis.
                * pos `tuple`: the position
                * scale `tuple`: `(scaleX,scaleY)`
                * userData `dict`: to store custom data. Only `string`, `int`, `float`, `array`, `dict` and `date` data is allowed.
        * userDate `dict`: A dict with user defined structure
        * vertOrigin `float`: Offset from default (ascender). Defaults to `0` 
        * vertWidth `float`: Only stored if other than the default (ascender+descender)
        * visible `bool`: The visibility setting in the layer panel (the eye symbol). Always set to `1`, otherwise omit the key.
        * width `float`:
    * locked `bool`: Always set to `1`, otherwise omit the key.
    * metricBottom `string`:
    * metricLeft `string`:
    * metricRight `string`:
    * metricTop `string`:
    * metricVertWidth `string`:
    * metricWidth `string`:
    * note `string`:
    * partsSettings `list>dict`: axes of a smart component
        * bottomValue `int`:
        * name `string`:
        * topValue `int`:
    * production `string`: manually set production name
    * tags `list>string`: list of tags
    * script `string`: manually set script
    * subcategory `string`: manually set subcategory
    * unicode `int` or `tuple`: for a single code, use just the int value (e.g. `unicode = 65;`) and for multiple use a tuple of all values (`unicode = (65,97);`).
* gridLength `int`: Only written if not `1`
* gridSubDivision `int`: Only written if bigger then `1`
* instances `list>dict`
    * axesValues `list>float`: A list of float values storing the axis coordinate for each axis, Axis settings are stored in the font object. 
    * customParameters `list>dict`: Instance custom parameters.
        * name `string`: Property name of the custom parameter.
        * value `string`: Value of the custom parameters.
    * exports `bool`: Always set to `0`, otherwise omit the key.
    * instanceInterpolations `dict`: keys are master IDs, values are the factors for that master.
    * isBold `bool`: for style linking. Always set to `1`, otherwise omit the key.
    * isItalic `bool`: for style linking. Always set to `1`, otherwise omit the key.
    * linkStyle `string`: The linked style name
    * manualInterpolation `bool`: If set, use the `instanceInterpolations`, otherwise calculate from `axisValues`. Always set to `1`, otherwise omit the key.
    * name `string`: The style name.
    * properties: `list>dict`: see [Properties](#properties)
    * userData `dict`: to store custom data. Only `string`, `int`, `float`, `array`, `dict` and `date` data is allowed.
    * weightClass `string`:
    * widthClass `string`:
* keepAlternatesTogether: `bool`: Always set to `1`, otherwise omit the key.
* kerningLTR `dict`: three-level `dict` containing a `float` as value.
    * first level key is the master ID.
    * second level is either the left kerning group name or glyph name.
    * third level is either the right kerning group name or glyph name.
* kerningRLT `dict`: see `kerningLTR`
* kerningVertical `dict`: see `kerningLTR`
* keyboardIncrement `float`: Only written if not `1`
* metrics `list>dict`: definition of the (vertical) metrics
    * filter `string`: A predicate format string [(Apple Predicate Programming Guide)](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Predicates/AdditionalChapters/Introduction.html#//apple_ref/doc/uid/TP40001789) (e.g. `"case == 3"` (No Case = 0, Uppercase = 1, Lowercase = 2, Smallcaps = 3, Other = 4))
    * name `string`: the name of the metric. Can be anything but some keys have special meaning: "ascender", "cap height", "slant height", "x-height", "midHeight", "topHeight", "descender", "baseline"
* numbers `list>dict`: definition of the numbers. Used to store interpolating numbers in each master
    * name `string`: name of the number
* properties `list>dict`: see [Properties](#properties)
* unitsPerEm `int`
* userData `dict`: to store custom data. Only `string`, `int`, `float`, `array`, `dict` and `date` data is allowed.
* versionMajor `int`
* versionMinor `int`: must be between 0 and 999.


### Properties
* key `string`: property key. One of the following. Keys ending with "s" are localizable that means the second key is `values`, otherwise `value`.
    * familyNames
    * copyrights
    * designers
    * designerURL
    * manufacturers
    * manufacturerURL
    * licenses
    * licenseURL
    * trademarks
    * descriptions
    * sampleTexts
    * postscriptFullName
    * postscriptFontName
    * WWSFamilyName
    * versionString
* values `list>dict`: a list of localized values
    * language `string`: 'dflt' or three letter ISO language tag ("DEU")
    * value `string`: The value
* value `string`: a single value

### Attributes
uses in paths and components
TODO