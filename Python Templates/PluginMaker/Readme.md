# PluginMaker

A tool for helping you set up your plug-in for Glyphs 3.0 and later.

## Usage instructions

1. After having built the app (see below), you can double click PluginMaker.app. In the dialog that comes up, do the following steps:
2. Choose a *Plugin Type* (see the documentation in the enclosing folders).
3. Choose a (display) *Plugin Name.* It can contain spaces. For Reporter plug-ins, leave out the word ‘Show’ at the beginning.
4. Choose a *Main Class* name, this time without spaces. Typically camel-cased.
5. In *Developer Name,* type in your full name (regular first and last name, with uppercase and lowercase letters and spaces).
6. Press *Make Plugin.*


## Building the app

### Easy

1. Double click the file *Build PluginMaker.command.*
2. The app will be in a subfolder called `dist`. 

### Advanced

Alternatively, if you want to take care of it yourself:

1. Open this directory in Terminal.app (drag the folder onto Terminal.app or `cd` here).
2. Run this command:
  `python3 setup.py py2app -A`
2. The app will be in a subfolder called `dist`. 

The `.command` script does exactly the same, though.

