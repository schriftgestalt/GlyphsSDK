# GlyphsSDK

## Plugin SDK

This is the Plugin SDK for the [Glyphs font editor](http://glyphsapp.com/). There are various kinds of plugins (see below), and there are two ways of writing them, in ObjectiveC (we are still working on the ObjC templates) or in Python. You will find extensive documentation in the code comments. For more details and a step-by-step guide, look into the `README.md` file inside the Templates folder.

### .glyphsFileFormat

These plugins add additional file formats for the export dialog.

### .glyphsFilter

These plugins that add functionality in the *Filter* submenu of Glyphs. A filter can either have a GUI (dialog window) or none. A filter can also be called as an instance custom parameter.

### .glyphsPalette

These plugins add new sections to the Palette (*Window > Palette*, Cmd-Opt-P).

### .glyphsPlugin

These are all plugins that do not fit any other category.

### .glyphsReporter

These plugins add extra View functionality. They usually draw additional items in the current Edit View. Their titles, preceded by ‘Show’ will appear at the bottom of the *View* menu of the application.

### .glyphsTool

These plugins add a new tool in the toolbar. You can place a small PDF as toolbar icon in the `Contents/Resources/` folder. For measurements, take a look at the placeholder image that is already there.

## File Format Description

The file `GlyphsFileFormat.md` contains a description of the Glyphs 1.x file format.

### License

Copyright 2013, 2014 Georg Seifert (@schriftgestalt) and Rainer Erich Scheichelbauer (@mekkablue).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
