import json
import os
import collections
from glyphsLib.parser import Parser
from pathlib import Path

f = open(os.path.join(os.path.dirname(__file__), "Glyphs3FileSchema.json"),)
schema = json.load(f)


PathToGlyphsFiles = ""  # add path to a folder that contains .glyphs test files
assert (len(PathToGlyphsFiles) > 10)

# add full file paths of files that you like to exclude
skipFiles = [
]

skipChildren = [
	"kerningLTR",
	"kerningRTL",
	"kerningVertical",
	"kerningContext",
	"userData",
	"instanceInterpolations",
	"customParameters",
	"deltaV",
	"partSelection",
	"piece",
]

ignoreKeys = [
	".storedFormatVersion",
	"changeCount",
	"bottomName",
	"topName",
]


def keysFromObject(obj, parentKey, keyset):
	for key, value in obj.items():
		if key in ignoreKeys:
			continue
		itemKey = parentKey + "/" + key
		if key in skipChildren:
			pass
		elif isinstance(value, (dict, collections.OrderedDict)):
			keysFromObject(value, itemKey, keyset)
			continue
		elif isinstance(value, list):
			hasSubKeys = False
			for item in value:
				if isinstance(item, (dict, collections.OrderedDict)):
					keysFromObject(item, itemKey, keyset)
					hasSubKeys = True
			if hasSubKeys:
				continue
		keyset.add(itemKey)


def keysFromFile(path, keyset):
	p = Parser()
	fp = open(path, "r", encoding="utf-8")
	fileContent = fp.read()
	if ".formatVersion = 3;" not in fileContent[:50]:
		return
	data = p.parse(fileContent)
	keysFromObject(data, "", keyset)


def keysFromAllFiles(folder_path):
	keyset = set()
	pathlist = Path(folder_path).glob('**/*.glyphs')
	for path in pathlist:
		path_in_str = str(path)
		if path_in_str in skipFiles:
			# print("skip done:", path_in_str)
			continue
		keysFromFile(path_in_str, keyset)

	keysFromFile(os.path.join(os.path.dirname(os.path.dirname(__file__)), "GlyphsFileFormatv3.glyphs"), keyset)
	result = list(keyset)
	result.sort()
	for key in result:
		print("\"%s\"," % key)
	print("#found: %s key paths" % len(result))


if __name__ == '__main__':
	keysFromAllFiles(PathToGlyphsFiles)
