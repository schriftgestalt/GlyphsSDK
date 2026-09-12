"""
Type stubs for the runtime globals that GSScriptingHandler injects into
every script's namespace via prepareMacroCallingGlobalDict:.

A short prelude (`from glyphs_runtime import *`) is prepended to the
script when pyright analyses it; this file makes those injected names
visible to the type checker.
"""

from typing import Any

from GlyphsApp import GSApplication, GSFont, GSLayer

Font: GSFont
Layer: GSLayer
Glyphs: GSApplication
