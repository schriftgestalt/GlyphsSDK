#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"
"$PYTHON" -c 'import sys; print("Using", sys.executable, "(Python %s)" % sys.version.split()[0])'

if ! "$PYTHON" -c 'import setuptools, py2app, Cocoa; from PyObjCTools import AppHelper'; then
	printf '\n%s\n' 'Some build dependencies are missing or cannot be imported.'
	printf '%s\n' 'Installation may download PyObjC (Cocoa bindings), which can be large.'
	read -r -p 'Install build dependencies for this Python? [y/N] ' answer
	case "$answer" in
		y|Y|yes|YES) "$PYTHON" -m pip install -r requirements-build.txt ;;
		*) exit 1 ;;
	esac
fi

# Alias mode keeps the small, local helper app used by the original builder.
"$PYTHON" setup.py py2app -A
printf '\nBuilt %s/dist/PluginMaker.app\n' "$PWD"
