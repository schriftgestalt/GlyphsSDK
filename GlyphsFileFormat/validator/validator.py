import json
from jsonschema import validate, Draft7Validator
from glyphsLib.parser import Parser

f = open("Glyphs3FileSchema.json",)
schema = json.load(f)

p = Parser()
fp = open("../GlyphsFileFormatv3.glyphs", "r", encoding="utf-8")
data = p.parse(fp.read())

validate(instance=data, schema=schema)

print("----- validate 2")
f = open("Glyphs2FileSchema.json",) 
schema = json.load(f) 

p = Parser()
fp = open("../GlyphsFileFormatv2.glyphs", "r", encoding="utf-8")
data = p.parse(fp.read())
validator = Draft7Validator(schema)
validator.validate(instance=data)
