# Glyphs File Format, Version 2
Glyphs saves its files in plaintext format. So the files can be viewed and edited with any text editor. Open an existing `.glyphs` file to see how it works.

- The format is based on Apples old style property list (plist) format.
- It doesn’t use the more common XML-based flavor (that is supported for reading) to save space.
- There are some small deviations from the default format. More about that in Notes.

## Changes
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
- Each key needs to be on its own line.
- Lists have each element on one line, empty `lists` or `dicts` need to span two lines.
    * except: color list, they are all on one line.
- empty elements are always omitted.
    * except: in `userData` entires. There the structure is preserved.
- Numbers are always written without quotes (negative and float). Strings that look like numbers are written with quotes (mostly important in userData).
- Unicodes are written as hex string but always without quotes so it might be ambiguous for a general parser ('1234' could be read as int or hex)
- The last element in a list doesn’t get a trailing comma.

## Top Level Elements
The XML file contains a dictionary with the following structure. The elements with child elements are usually a `list` of `dict` elements.

* .appVersion `string`
* DisplayStrings `list`
* classes `list`: OpenType classes.
    * automatic `bool`: Always set to `1`. If the feature is not set to automatic, the key should be omitted.
    * code `string`: A string containing space separated glyph names.
    * disabled `bool`: The class will not be exported. Always set to `1`, otherwise omit the key
    * name `string`: The OpenType class name.
    * notes `string`: Notes.
* copyright `string`
* customParameters `list`: Font-wide custom parameters.
    * name `string`: Property name of the custom parameter.
    * value `string`: Value of the custom parameters.
* date `string`: Format `2014-01-29 14:14:38 +0000`.
* designer `string`
* designerURL `string`
* disablesAutomaticAlignment `bool`: Always set to `1`, otherwise omit the key
* disablesNiceNames `bool` is always set to `1`. If not set the key is not set at all.
* familyName `string`
* featurePrefixes `list`: OpenType feature code before the class definitions.
    * automatic `bool`: Always set to `1`, otherwise omit the key
    * code `string`: A string containing feature code.
    * disabled `bool`: The prefix will not be exported. Always set to `1`, otherwise omit the key
    * name `string`: The name of the prefix
    * notes `string`: Notes.
* features `list`
    * automatic `bool` is always set to `1`. If not set the key is not set at all.
    * code `string`: a string containing feature code.
    * disabled `bool`: The feature will not be exported. Always set to `1`, otherwise omit the key
    * name `string`: the feature tag.
    * notes `string`: The feature notes. For stylistic sets, the note can contain a `featureNames` definition or a `Name:` + feature name
* fontMaster `list`
    * alignmentZones `list`: list of position and overshot in a string with curly braces (e.g. `"{800, 15}"`)
    * ascender `int`
    * capHeight `int`
    * custom `string` : All other parts of the master name that doesn’t fit into `weight` or `width`
    * customValue `int`: axis position for the third axis. Is only present if the value is not `0`.
    * customValue1 `int`: axis position for the forth  axis. Is only present if the value is not `0`.
    * customValue2 `int`: axis position for the fifth  axis. Is only present if the value is not `0`.
    * customValue3 `int`: axis position for the sixth  axis. Is only present if the value is not `0`.
    * customParameters `list`: Master-wide custom parameters.
        * name `string`: Property name of the custom parameter.
        * value `string`: Value of the custom parameter.
    * descender `int`: is always negative.
    * horizontalStems `list`: a list of `int` values.
    * iconName `string`: stores the selected master icon (new in v2.5)
    * id `string` a unique id that connects the layers (associated ID) with the master.
    * userData `dict` to store custom data. Only `string`, `int`, `float`, `array`, `dict` and `date` data is allowed.
    * verticalStems `list`: a list of `int` values.
    * visible `int`: Always set to `1`. If not set, the key is not present at all.
    * weight `string` : The weight part of the master name. Possible values "SemiLight", "Light", "SemiBold", "Bold"
    * weightValue `int`: The weight position for interpolation. Is only present if the value is not `100`.
    * width `string` : The width part of the master name. Possible values "SemiCondensed", "Condensed", "SemiExtended", "Extended"
    * widthValue `int`: The width position for interpolation. Is only present if the value is not `100`.
    * xHeight `int`
* glyphs `list`
    * glyphname `string`: Must be unique throughout the font.
    * production `string`: manually set production name (new in v2.2)
    * script `string`: manually set script (new in v2.2)
    * category `string`: manually set category (new in v2.2)
    * color `int` or `list`:
        1. If `int`, it is the index of the internal color list
        2. If `list`, four numbers in the range of 0–255 denoting a RGBA value
    * subcategory `string`: manually set subcategory (new in v2.2)
    * lastChange `string`: Format `2014-01-29 14:14:38 +0000`.
    * layers `list`
        * anchors `list`
            * name `string`: The name of the anchor.
            * position `string`: format `{X, Y}`
        * annotations `list>dict`
        * associatedMasterId `string`: ID of the master the layer is linked to. Not present if it equals layerID, i.e. if the layer is in use as master.
        * background `dict`: Contains the same children as the layer itself, except for background, layerId and associatedMasterId.
        * backgroundImage `dict`: a image.
            * crop `string`: Portion of the image to show in pixels, format: `{{t,l},{b,r}}`
            * imagePath `string`: The file path to the image. It is stored relative if close enough. Otherwise the full path.
            * locked `bool`: Always set to `1`, otherwise omit the key
            * transform `string`: An affine transformation matrix, format: `{m11, m12, m21, m22, tX, tY}`.
        * components `list`
            * anchor `string`: Should be indicated if connected to an anchor, especially if more than one possibility is available, e.g. in ligatures.
            * name `string`: The name of the linked glyph (i.e., the glyph the component is pointing to).
            * transform `string`: An affine transformation matrix, format: `{m11, m12, m21, m22, tX, tY}`.
            * alignment `int`: controls the automatic alignment of this component. (-1 disables alignment, 1 forces it for glyph that are usually not aligned)
            * disableAlignment `bool`: This component should not be automatically aligned. (not used since version 2.3-826)
        * guideLines `list`
            * alignment `string`: If the guide is `right` or `center` aligned. Default: `left`
            * angle `float`: The angle. If not set defaults to 0°
            * locked `int`: is always `1`, otherwise the field is not there
            * showMeasurement `int`: is always `1`, otherwise the field is not there
            * position `string`: format `{X, Y}`
        * hints `list`
            * horizontal `int`: If set, the hint is horizontal and vertical otherwise
            * type `string`: The type of the hint. Possible value are: TTStem, TopGhost, BottomGhost, Anchor, Align, Interpolate, Diagonal, Tag, Corner, Cap
                If there is no type, it defaults to Stem, of Ghost if `target` is set
            * origin `string`: '{pathIndex, nodeIndex}'
                TODO: Explain node indexes
            * target `string`: `{pathIndex, nodeIndex}`, `up` or `down`
            * other1 `string`: `{pathIndex, nodeIndex}` for TT Institutions that need more than two nodes (Interpolation, Diagonal)
            * other2 `string`: `{pathIndex, nodeIndex}` for TT Institutions that need more than three nodes (Diagonal)
            * scale `string`: `{scaleX, scaleY}` Only used for caps and corners
            * stem `int`: if a stem is manually set
            * options `int`: a bitfield for options
        * layerId `string`
        * leftMetricsKey `string`
        * rightMetricsKey `string`
        * widthMetricsKey `string`
        * name `string`: The name of the layer. Only stored for none master layers (this is changed in 2.3, before the master names where stored)
        * paths `list`
            * closed `bool`: Always set to `0`, otherwise omit the key.
            * nodes `list`: One entry per node. Format: `X Y TYPE [SMOOTH]`, where X and Y are the coordinates as float, and TYPE is either `LINE`, `CURVE` or `OFFCURVE`. After `LINE` and `CURVE`, you can additionally add a `SMOOTH`.
        * userDate `dict`: A dict with user defined structure
        * vertWidth `float`: Only stored if other than the default (ascender+descender)
        * width `float`
        * visible `int`: Always set to `1`. If not set, the key is not present at all.
    * leftKerningGroup `string`
    * leftMetricsKey `string`
    * rightKerningGroup `string`
    * rightMetricsKey `string`
    * unicode `string`: Hexadecimal Unicode value.
* gridLength `int`: Only written if not `1`
* gridSubDivision `int`: Only written if bigger then `1`
* instances `list`
    * customParameters `list`: Instance custom parameters.
        * name `string`: Property name of the custom parameter.
        * value `string`: Value of the custom parameters.
    * exports `bool`: Always set to `0`, otherwise omit the key.
    * interpolationCustom `float`: axis position for the third axis
    * interpolationCustom1 `float`: axis position for the fourth axis
    * interpolationCustom2 `float`: axis position for the fifth axis
    * interpolationCustom3 `float`: axis position for the sixth axis
    * interpolationWeight `float`: axis position for the first axis
    * interpolationWidth `float`: axis position for the second axis
    * instanceInterpolations `dict`: keys are master IDs, values are the factors for that master.
    * isBold `bool`: for style linking. Always set to `1`, otherwise omit the key.
    * isItalic `bool`: for style linking. Always set to `1`, otherwise omit the key.
    * linkStyle `string`: The linked style name
    * manualInterpolation `bool`: If set, use the `instanceInterpolations`, otherwise calculate from `axisValues`. Always set to `1`, otherwise omit the key.
    * name `string`: The style name.
    * userData `dict`: to store custom data. Only `string`, `int`, `float`, `array`, `dict` and `date` data is allowed.
    * weightClass `string`:
    * widthClass `string`:
* keepAlternatesTogether: `bool`: Always set to `1`, otherwise omit the key.
* kerning `dict`: three-level `dict` containing a `float` as value.
    * first level key is the master ID.
    * second level is either the left kerning group name or glyph name.
    * third level is either the right kerning group name or glyph name.
* vertKerning `dict`: see `kerning`
* keyboardIncrement `float`: Only written if not `1`
* manufacturer `string`
* manufacturerURL `string`
* unitsPerEm `int`
* userData `dict`: to store custom data. Only `string`, `int`, `float`, `array`, `dict` and `date` data is allowed.
* versionMajor `int`
* versionMinor `int`: must be between 0 and 999.

