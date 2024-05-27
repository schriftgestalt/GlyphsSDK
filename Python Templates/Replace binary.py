# this will copy the plugin binary to all plugins in the Glyphs Repository folder

import os
import shutil
rootdir = os.path.expanduser("~/Library/Application Support/Glyphs 3/Repositories")
newBin = os.path.join(os.path.dirname(__file__), "File Format/____PluginName____.glyphsFileFormat/Contents/MacOS/plugin")

for subdir, dirs, files in os.walk(rootdir):
	if ".git" in subdir:
		continue
	for f in files:
		if f == "plugin" and subdir.endswith("/MacOS"):
			print(os.path.join(subdir, f))
			shutil.copyfile(newBin, os.path.join(subdir, f))
