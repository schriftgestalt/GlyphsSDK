## Dialogs in contextual menus

You may place `NSView` dialogs in the general or conditional context menus for quick access to settings of your tool.

In fact, we highly encourage you to do so, because we want to keep Glyphs’ user interface as beautiful and uncluttered as it is. Many of Glyphs’ users appreciate that. Now, it’s of course your decision to create a floating tool window, but we ask you to trust and follow our ideas on that and hide dialogs from the view of the user that need not be constantly accessible. A right-click with the mouse will then show that dialog in the context menu.

![](../_Readme_Images/contextmenuview.png)

When creating the menu items in the code, instead of handing over *name* and *action* attributes, you hand over just a *view* that contains a reference to the `NSView` object.

As with other dialogs, we have two choices to create them: Use Xcode’s Xcode or Tal Leming’s [Vanilla](https://vanilla.robotools.dev/en/) library.