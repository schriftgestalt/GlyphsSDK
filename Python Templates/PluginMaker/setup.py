"""
Script for building the example.

Usage:
    python setup.py py2app
"""
from setuptools import setup

plist = dict(
	NSRequiresAquaSystemAppearance=False
)

setup(
    data_files=['MainMenu.nib'],
    app=[
        dict(script="PluginMaker.py", plist=plist),
    ],
    install_requires=["pyobjc-framework-Cocoa"],
    setup_requires=["py2app"],
)
