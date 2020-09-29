import json 
from jsonschema import validate
from glyphsLib.parser import Parser

f = open("Glyphs3FileShema.json",) 
schema = json.load(f) 

p = Parser()
fp = open("../GlyphsFileFormatv3.glyphs", "r", encoding="utf-8")
data = p.parse(fp.read())

validate(instance=data, schema=schema)
