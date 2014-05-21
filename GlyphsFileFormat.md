# Glyphs File Format, Version 1
Glyphs stores data using the Apple property list (plist) format. It saves its files in plaintext format, because it saves a lot of space, but the XML-based flavour is also supported. So, the files can be viewed and edited with any text editor. Open an existing `.glyphs` file to see how it works.

## Top Level Elements
The XML file contains a dictionary with the following structure. The elements with child elements are usually a `list` of `dict` elements.

* DisplayStrings `list`
* classes `list`: OpenType classes.
    * automatic `bool`: Always set to `1`. If the feature is not set to automatic, the key should be omitted.
    * code `string`: A string containing space separated glyph names.
    * name `string`: The OpenType class name.
* copyright `string`
* customParameters `list`: Font-wide custom parameters.
    * name `string`: Property name of the custom parameter.
    * value `string`: Value of the custom parameters.
* date `string`: Format `2014-01-29 14:14:38 +0000`.
* designer `string`
* designerURL `string`
* familyName `string`
* featurePrefixes `list`: OpenType feature code before the class definitions.
    * code `string`
    * name `string`
* features `list`
    * automatic `bool` is always set to `1`. If not set the key is not set at all.
    * code `string`: a string containing feature code.
    * name `string`: the feature tag.
* fontMaster `list`
    * alignmentZones `list`
    * ascender `int`
    * capHeight `int`
    * customParameters `list`: Master-wide custom parameters.
        * name `string`: Property name of the custom parameter.
        * value `string`: Value of the custom parameter.
    * descender `int`: is always negative.
    * horizontalStems `list`: a list of `int` values.
    * id `string` a unique id that connects the layers (associated ID) with the master.
    * userData `dict` to store custom data. Only `string`, `int`, `float`, `array`, `dict` and `date` data is allowed.
    * weightValue `int`: The width position for interpolation. Is only present if the value is not `100`.
    * weightValue `int`: The weight position for interpolation. Is only present if the value is not `100`.
    * verticalStems `list`: a list of `int` values.
    * xHeight `int`
* glyphs `list`
    * glyphname `string`: Must be unique throughout the font.
    * lastChange `string`: Format `2014-01-29 14:14:38 +0000`.
    * layers `list`
        * anchors `list`
            * name `string`: The name of the anchor.
            * position `string`: format `{X, Y}`.
        * components `list`
            * anchor `string`: Should be indicated if connected to an anchor, especially if more than one possibility is available, e.g. in ligatures.
            * name `string`: The name of the linked glyph (i.e., the glyph the component is pointing to).
            * transform `string`: An affine transformation matrix, format: `{m11, m12, m21, m22, tX, tY}`.
        * associatedMasterId `string`: ID of the master the layer is linked to. Not present if it equals layerID, i.e. if the layer is in use as master.
        * background `dict`: Contains the same children as the layer itself, except for background, layerId and associatedMasterId. 
        * layerId `string`
        * leftMetricsKey `string`
        * rightMetricsKey `string`
        * name `string`: The name of the layer. Must be unique per glyph, and set to the master name if it is the master layer.
        * path `list`
            * closed `bool`: Always set to `1`. If not set, the key is not present at all.
            * nodes `list`: One entry per node. Format: `X Y TYPE [SMOOTH]`, where X and Y are the coordinates as float, and TYPE is either `LINE`, `CURVE` or `OFFCURVE`. After `LINE` and `CURVE`, you can additionally add a `SMOOTH`.
        * width `float`
    * leftKerningGroup `string`
    * leftMetricsKey `string`
    * rightKerningGroup `string`
    * rightMetricsKey `string`
    * unicode `string`: Hexadecimal Unicode value.
* instances `list`
    * customParameters `list`: Instance custom parameters.
        * name `string`: Property name of the custom parameter.
        * value `string`: Value of the custom parameters.
* kerning `dict`: three-level `dict` containing a `float` as value.
    * first level key is the master ID.
    * second level is either the left kerning group name or glyph name.
    * third level is either the right kerning group name or glyph name.
* manufacturer `string`
* manufacturerURL `string`
* unitsPerEm `int`
* userData `dict`
* versionMajor `int`
* versionMinor `int`: must be between 0 and 999.

