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

def ReadFromFile(path):
	"""\
	Return content of file
	"""
	import codecs
	if os.path.exists(path):
		f = codecs.open(path, encoding='utf-8', mode='r')
		text = f.read()#.decode('utf8')
		f.close()
		return text

	return ''

def WriteToFile(path, string):
	"""\
	Write content to file
	"""
	f = open(path, 'wb')
	f.write(string.encode())
	f.close()
	return True

#from ynlib.system import Execute
def Execute(command):
	"""\
	Execute system command, return output.
	"""

	import sys
	import subprocess

	process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, close_fds=True)
	os.waitpid(process.pid, 0)
	response = process.stdout.read().strip()
	process.stdout.close()
	return response


# local path
path = os.path.dirname(__file__)

# Read docu code from GlyphsApp.py
code = ReadFromFile(os.path.join(path, '..', 'GlyphsApp', '__init__.py'))
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
Execute('/Library/Frameworks/Python.framework/Versions/3.9/bin/sphinx-build -b html "%s" "%s"' % (os.path.join(path, 'sphinx folder'), os.path.join(path, '_build', 'html')))

html = ReadFromFile(os.path.join(path, '_build', 'html', 'index.html'))

html = html.replace("\t", "")
html = html.replace("  ", " ")
html = html.replace("  ", " ")
html = html.replace("  ", " ")
html = html.replace("  ", " ")
html = html.replace("\n\t", "\n")
html = html.replace("\n ", "\n")
html = html.replace("\n ", "\n")
html = html.replace('<script id="documentation_options" data-url_root="./" src="_static/documentation_options.js"></script>', "")
html = html.replace('<script src="_static/jquery.js"></script>', "")
html = html.replace('<script src="_static/underscore.js"></script>', "")
html = html.replace('<script src="_static/doctools.js"></script>', "")
html = html.replace('<script src="_static/language_data.js"></script>', "")
html = html.replace('<link rel="index" title="Index" href="genindex.html" />', "")
html = html.replace('<link rel="search" title="Search" href="search.html" />', "")
html = html.replace('\n<!DOCTYPE html>', '<!DOCTYPE html>')
html = re.sub('&amp; <a href="https://github.com/bitprophet/alabaster">Alabaster ([0-9.]*)</a>', '', html)
html = html.replace("\n\n|\n", "|")

html = html.replace("\n\n", "\n")
html = html.replace("\n\n", "\n")
html = html.replace("\n\n", "\n")
html = html.replace("\n\n", "\n")


WriteToFile(os.path.join(path, '_build', 'html', 'index.html'), html)
