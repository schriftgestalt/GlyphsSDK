import json
import os
import threading
from jsonschema import validate
from glyphsLib.parser import Parser
from pathlib import Path

f = open("Glyphs3FileSchema.json",)
schema = json.load(f)

p = Parser()
fp = open("../GlyphsFileFormatv3.glyphs", "r", encoding="utf-8")
data = p.parse(fp.read())

PathToGlyphsFiles = ""  # add path to a folder that contains .glyphs test files

assert (len(PathToGlyphsFiles) > 10)

pathlist = Path(PathToGlyphsFiles).glob('**/*.glyphs')

# add full file paths of files that you like to exclude
skipFiles = [
]


def validate_file(path_in_str):
	p = Parser()
	fp = open(path_in_str, "r", encoding="utf-8")
	fileContent = fp.read()
	fp.close()
	if ".formatVersion = 3;" not in fileContent[:50]:
		# print("skip v2:", path_in_str)
		return
	print("\"%s\"," % path_in_str)
	data = p.parse(fileContent)
	# print("<<")
	try:
		validate(instance=data, schema=schema)
		result = "OK"
	except:
		import traceback
		result = traceback.format_exc()
	resultFile = open(path_in_str + ".txt", "w")
	resultFile.write(result)
	resultFile.close()


for path in pathlist:
	# because path is object not string
	path_in_str = str(path)
	if path_in_str in skipFiles:
		# print("skip done:", path_in_str)
		continue
	if os.path.isfile(path_in_str + ".txt"):
		continue
	
	x = threading.Thread(target=validate_file, args=(path_in_str,))
	x.start()
	# print(">>")


# print("----- validate 2")
# f = open("Glyphs2FileSchema.json",)
# schema = json.load(f)
#
# p = Parser()
# fp = open("../GlyphsFileFormatv2.glyphs", "r", encoding="utf-8")
# data = p.parse(fp.read())
# validator = Draft7Validator(schema)
# validator.validate(instance=data)
