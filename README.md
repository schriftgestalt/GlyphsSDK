# GlyphsSDK

This is the Plugin SDK for the [Glyphs font editor](http://glyphsapp.com/). There are various kinds of plugins (see below), and there are two ways of writing them, in ObjectiveC or Python. There is extensive documentation in the code. For more details, look into the Readme files inside the Template subfolders.

### .glyphsReporter

These plugins add extra View functionality. They usually draw additional items in the current Edit View. Their titles, preceded by ‘Show’ will appear at the bottom of the *View* menu of the application.

### .glyphsTool

These plugins add a new tool in the toolbar. You can place a small PDF as toolbar icon in the `Contents/Resources/` folder. For measurements, take a look at the placeholder image that is already there.

### .glyphsFilter

This is an ObjectiveC plugin that can add functionality in the *Filter* submenu or anywhere else in the UI of Glyphs.

### .glyphsFileFormat

These add additional file formats for the export dialog.

### .glyphsPalette

Additions to the Palette (Cmd-Opt-P).

### .glyphsPlugin

These are all plugins that do not fit any other category.

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
