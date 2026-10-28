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

1. Install a standard (not free-threaded) Python 3.10 or later for macOS, for example from [python.org](https://www.python.org/downloads/macos/). Python 3.13 and 3.14 are supported by the current build dependencies. Apple's older command-line-tools Python is not sufficient.
2. Double click the file *Build PluginMaker.command.* It uses the installed `python3` and its existing packages. If build dependencies are missing or cannot be imported, it asks before installing them. Press Enter or answer `n` to cancel.
3. The app will be in a subfolder called `dist`.

The dependencies are py2app, setuptools and the Cocoa bindings from PyObjC. Installation requires an internet connection and uses pip for the selected Python, without requesting upgrades of already satisfied requirements.

The app is built in py2app's **alias mode**, as before: keep this source folder and the selected Python installation (including its dependencies) in place. Keep the app inside the enclosing `Python Templates` folder so it can find the templates. Rebuild after moving the project or upgrading Python. This build is for local use; it is not a standalone app for distribution.

### Advanced

To choose a specific Python installation, open this directory in Terminal.app and run:

```sh
PYTHON=/path/to/python3 ./Build\ PluginMaker.command
```

To install the dependencies and build directly:

```sh
python3 -m pip install -r requirements-build.txt
python3 setup.py py2app -A
```

