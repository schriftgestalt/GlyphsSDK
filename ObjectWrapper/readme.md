This is a copy of the object wrapper that is shipped with Glyphs. This is just for reference.

### Debugging
To debug the wrapper or play around with it, you can copy or symlink the GlyphsApp folder into `~/Library/Application Support/Glyphs 3/Scripts`

```
cd ~/Library/Application\ Support/Glyphs\ 3/Scripts
ln -s ~/Code/GlyphsSDK/ObjectWrapper/GlyphsApp 
```
(check the path to the GlyphsSDK repo and adjust it)

To check if it is working, add a `print("SDK")` somewhere at the top of `__init__.py`. This will show up the first time the wrapper is imported (so it might be when a plugin is loaded).