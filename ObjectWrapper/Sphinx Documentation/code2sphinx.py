###############################################################################################
#
#	Reads Sphinx-style docu code from GlyphsApp.py and combines it with
#	a Sphinx header file, to bake html docu.
#
#	Author: Yanone
#
#	Requires Sphinx (http://sphinx-doc.org) and ynlib (https://github.com/yanone/ynlib)
#
###############################################################################################


import re, os

from ynlib.files import ReadFromFile, WriteToFile
from ynlib.system import Execute

# local path
path = os.path.dirname(__file__)

# Read docu code from GlyphsApp.py
code = ReadFromFile('/Users/yanone/Library/Application Support/Glyphs/Scripts/GlyphsApp.py SVN/GlyphsApp.py')
sphinxoriginal = ReadFromFile(os.path.join(path, 'sphinx folder', 'index.rst.original'))

# focus on triple comments
r = re.compile(r"'''(.*?)'''", re.DOTALL)
doc = '\n'.join(r.findall(code))

# touch up code
doc = re.sub('((.*?)attribute(.*))', '\n\g<0>\n', doc)
doc = doc.replace('	:type', '\n	:type')
doc = re.sub('((.*?)code-block(.*))', '\n\g<0>\n', doc)

# Export Sphinx Docu
WriteToFile(os.path.join(path, 'sphinx folder', 'index.rst'), sphinxoriginal + doc)

# bake HTML
Execute('/usr/local/bin/sphinx-build "%s" "%s"' % (os.path.join(path, 'sphinx folder'), os.path.join(path, 'sphinx folder', '_build', 'html')))

# Upload to FTP
# not implemented