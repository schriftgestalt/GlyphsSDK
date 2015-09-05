# GlyphsApp.py Sphinx Documentation (http://docu.glyphsapp.com)

Reads Sphinx-style docu code from GlyphsApp.py and combines it with a Sphinx header file, to bake html docu.
Requires Sphinx (http://sphinx-doc.org) and ynlib (https://github.com/yanone/ynlib)

## Update documentation

In `code2sphinx.py` point the code to the path of your version of `GlyphsApp.py`.

Then execute `python code2sphinx.py`. This will combine the sphinx code from the comments in GlyphsApp.py with the headers in index.rst.original, to bake the HTML files found in `sphinx folder/_build/html/`

## Upload to FTP

When ready, upload the new html files to docu.glyphsapp.com. Ask Georg for FTP access.
