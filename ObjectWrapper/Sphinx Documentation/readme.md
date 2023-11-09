# GlyphsApp Sphinx Documentation (http://docu.glyphsapp.com)

Reads Sphinx-style docu code from `GlyphsApp/__init__.py` and combines it with a Sphinx header file, to bake html docu.
Requires Sphinx (http://sphinx-doc.org)

## Update documentation

In `code2sphinx.py` point the code to the path of the `__init__.py`.

Then execute `python code2sphinx.py`. This will combine the sphinx code from the comments in `GlyphsApp/__init__.py` with the headers in index.rst.original, to bake the HTML files found in `sphinx folder/_build/html/`
