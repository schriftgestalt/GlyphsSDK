###############################################################################################
#
#	Reads Sphinx-style docu code from Glyphs and combines it with
#	a Sphinx header file, to bake html docu.
#
#	Author: Yanone
#
#	Requires Sphinx (http://sphinx-doc.org)
#
###############################################################################################


import re, os, codecs

def ReadFromFile(path):
	"""
	Return content of file
	"""
	if os.path.exists(path):
		f = codecs.open(path, encoding='utf-8', mode='r')
		text = f.read()
		f.close()
		return text
	return ''

def WriteToFile(path, string):
	"""
	Write content to file
	"""
	f = codecs.open(path, 'w', "utf-8")
	f.write(string)
	f.close()

def Execute(command):
	"""
	Execute system command, return output.
	"""
	import subprocess
	process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, close_fds=True)
	os.waitpid(process.pid, 0)
	response = process.stdout.read().strip()
	process.stdout.close()
	return response


# local path
path = os.path.dirname(__file__)
scriptPath = os.path.join(os.path.dirname(path), 'GlyphsApp', '__init__.py')
# Read docu code from __init__.py
print("__scriptPath", scriptPath)
code = ReadFromFile(scriptPath)
sphinxoriginal = ReadFromFile(os.path.join(path, 'sphinx folder', 'header.rst.txt'))

# focus on triple comments
r = re.compile(r"'''(.*?)'''", re.DOTALL)
doc = '\n'.join(r.findall(code))

# touch up code
doc = re.sub('((.*?)attribute(.*))', '\n\g<0>\n', doc)
#doc = doc.replace('	:type', '\n	:type')
doc = re.sub('((.*?)code-block(.*))', '\n\g<0>\n', doc)

# Export Sphinx Docu
WriteToFile(os.path.join(path, 'sphinx folder', 'index.rst'), sphinxoriginal + doc)

# bake HTML
Execute('/Library/Frameworks/Python.framework/Versions/3.11/bin/sphinx-build -b html "%s" "%s"' % (os.path.join(path, 'sphinx folder'), os.path.join(path, '_build', 'html')))

html = ReadFromFile(os.path.join(path, '_build', 'html', 'index.html'))

#html = html.replace("        ", "")
html = html.replace('<script id="documentation_options" data-url_root="./" src="_static/documentation_options.js"></script>', "")
html = html.replace('<script src="_static/jquery.js"></script>', "")
html = html.replace('<script src="_static/underscore.js"></script>', "")
html = html.replace('<script src="_static/doctools.js"></script>', "")
html = html.replace('<script src="_static/language_data.js"></script>', "")
html = html.replace('<link rel="index" title="Index" href="genindex.html" />', "")
html = html.replace('<link rel="search" title="Search" href="search.html" />', "")
html = html.replace('\n<!DOCTYPE html>', '<!DOCTYPE html>')
html = re.sub('&amp; <a href="https://github.com/bitprophet/alabaster">Alabaster ([0-9.]*)</a>', '', html)
html = html.replace("<span class=\"colon\">:</span>", ":")
html = html.replace("\r", "\n")
html = html.replace("A collection of string constants.", "")
html = html.replace("<p></p>", "")
# html = html.replace("\n  ", "\n")
# html = html.replace("\n  ", "\n")
# html = html.replace("\n  ", "\n")
# html = html.replace("\n  ", "\n")
# html = html.replace("\n  ", "\n")
# html = html.replace("\n  ", "\n")
# html = html.replace("\n ", "\n")
# html = html.replace("\n\t", "\n")
# html = html.replace("\n\t", "\n")
# html = html.replace("\n\t", "\n")
# html = html.replace("\n\t", "\n")
# html = html.replace("\n\n", "\n")
# html = html.replace("\n\n", "\n")
# html = html.replace("\n\n", "\n")
# html = html.replace("\n\n", "\n")
html = html.replace("\n|\n", " | ")
html = html.replace("<div class=\"toctree-wrapper compound\">\n</div>\n", "")
html = html.replace("()</span></code></a>()</p>", "()</span></code></a></p>")

WriteToFile(os.path.join(path, '_build', 'html', 'index.html'), html)
