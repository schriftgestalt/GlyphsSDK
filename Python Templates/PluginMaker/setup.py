"""Build PluginMaker using the dependencies in the selected Python installation."""
from setuptools import setup

plist = dict(
	NSRequiresAquaSystemAppearance=False
)

setup(
	name="PluginMaker",
	data_files=['MainMenu.nib'],
	app=[dict(script="PluginMaker.py", plist=plist)],
	options={"py2app": {"iconfile": "Icon.icns"}},
)
