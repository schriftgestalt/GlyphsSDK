#!/bin/bash
cd "`dirname "$0"`"
python3 setup.py py2app -A --iconfile Icon.icns
