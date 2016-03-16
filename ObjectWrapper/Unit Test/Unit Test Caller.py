#MenuTitle: Glyphs.app Unit Tests
# -*- coding: utf-8 -*-

# To be copied into Glyphs’ script folder.

import sys

# Adjust path
unitTestPath = '/Users/yanone/Library/Application Support/Glyphs/GIT/ObjectWrapper/Unit Test'
if not unitTestPath in sys.path:
	sys.path.append(unitTestPath)

import UnitTest
reload(UnitTest)

UnitTest.unitTest()