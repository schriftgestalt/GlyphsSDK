# GlyphsSDK

This is the Plugin SDK for the [Glyphs font editor](http://glyphsapp.com/). There are three kinds of plugins: `.glyphsReporter`, `.glyphsPlugin` and `.glyphsTool`. And there are two ways of writing them, in ObjectiveC or Python. There is extensive documentation in the code.

### .glyphsReporter

These plugins add extra View functionality. They usually draw additional items in the current Edit View. Their titles, preceded by ‘Show’ will appear at the bottom of the *View* menu of the application.

### .glyphsTool

These plugins add a new tool in the toolbar. You can place a small PDF as toolbar icon in the `Contents/Resources/` folder. For measurements, take a look at the placeholder image that is already there.

### .glyphsPlugin

These are all plugins that do not fit any other category.

### Python plugins

Make a copy of the plugin folder structure. The core code must go into `Contents/Resources/____PluginFileName____.py`. Rename the file and copy the filename into the last line of `__boot__.py`. Give `Contents/MacOS/____PluginFileName____` the same name, except for the `.py` suffix.

Make sure to go through these text files and replace the placeholders with quadruple underscores (`____placeholder____`):
* `Contents/Info.plist`
* `Contents/Resources/____PluginFileName____.py`
* `Contents/Resources/__boot__.py`

Don’t touch these files and folders:
* `Contents/MacOS/python`
* `Contents/PkgInfo`
* `Contents/Resources/lib/`
* `Contents/Resources/site.py`
* `Contents/Resources/__error__.sh`

To install it, move it into the Plugins folder inside the Application Support folder of Glyphs (double click the plugin to let Glyphs do that for you). You can edit your code right there, but you need to restart the application for any changes to take effect.

### ObjectiveC plugins

Still working on those. Stay tuned.

### License

Copyright 2013 Georg Seifert (@schriftgestalt).
Parts of the documentation by Rainer Erich Scheichelbauer (@mekkablue).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
