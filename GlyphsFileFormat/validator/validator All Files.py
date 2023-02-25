import json
from jsonschema import validate, Draft7Validator
from glyphsLib.parser import Parser

f = open("Glyphs3FileShema.json",)
schema = json.load(f)

p = Parser()
fp = open("../GlyphsFileFormatv3.glyphs", "r", encoding="utf-8")
data = p.parse(fp.read())

from pathlib import Path

PathToGlyphsFiles = "/" # add path to a folder that contains .glyphs test files

assert(len(PathToGlyphsFiles) > 10)

pathlist = Path(PathToGlyphsFiles).glob('**/*.glyphs')

# add full file paths of files that you like to exclude
skipFiles = [
]

for path in pathlist:
	# because path is object not string
	path_in_str = str(path)
	if path_in_str in skipFiles:
		# print("skip done:", path_in_str)
		continue
	p = Parser()
	fp = open(path_in_str, "r", encoding="utf-8")
	fileContent = fp.read()
	if ".formatVersion = 3;" not in fileContent[:50]:
		# print("skip v2:", path_in_str)
		continue
	print("\"%s\"," % path_in_str)
	data = p.parse(fileContent)
	#print("<<")
	validate(instance=data, schema=schema)
	#print(">>")
# print("----- validate 2")
# f = open("Glyphs2FileShema.json",)
# schema = json.load(f)
#
# p = Parser()
# fp = open("../GlyphsFileFormatv2.glyphs", "r", encoding="utf-8")
# data = p.parse(fp.read())
# validator = Draft7Validator(schema)
# validator.validate(instance=data)
