"""
Append module search paths for third-party packages to sys.path.

This is stripped down and customized for use in py2app applications
"""

import sys, os
try:
    basestring
except NameError:
    basestring = str

def makepath(*paths):
    dir = os.path.abspath(os.path.join(*paths))
    return dir, os.path.normcase(dir)

for m in sys.modules.values():
    f = getattr(m, '__file__', None)
    if isinstance(f, basestring) and os.path.exists(f):
        m.__file__ = os.path.abspath(m.__file__)
del m

# This ensures that the initial path provided by the interpreter contains
# only absolute pathnames, even if we're running from the build directory.
L = []
_dirs_in_sys_path = {}
dir = dircase = None  # sys.path may be empty at this point
for dir in sys.path:
    # Filter out duplicate paths (on case-insensitive file systems also
    # if they only differ in case); turn relative paths into absolute
    # paths.
    dir, dircase = makepath(dir)
    if not dircase in _dirs_in_sys_path:
        L.append(dir)
        _dirs_in_sys_path[dircase] = 1
sys.path[:] = L
del dir, dircase, L


# Remove sys.setdefaultencoding() so that users cannot change the
# encoding after initialization.  The test for presence is needed when
# this module is run as a script, because this code is executed twice.
#
if hasattr(sys, "setdefaultencoding"):
    del sys.setdefaultencoding
