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

#from ynlib.files import ReadFromFile, WriteToFile
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
Execute('/usr/local/bin/sphinx-build -b html "%s" "%s"' % (os.path.join(path, 'sphinx folder'), os.path.join(path, '_build', 'html')))

# Upload to FTP
# not implemented