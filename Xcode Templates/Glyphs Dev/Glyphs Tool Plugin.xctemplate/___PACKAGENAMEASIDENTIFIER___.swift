//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//  ___COPYRIGHT___
//

import Cocoa

private var _toolBarIcon: NSImage?

@objc class ___FILEBASENAMEASIDENTIFIER___: GlyphsPathPlugin {

	override init() {
		super.init()
		let bundle = Bundle(for: Self.self)
		// The toolbar icon:
		if let path = bundle.pathForImageResource(NSImage.Name("ToolbarIconTemplate")) {
			let icon = NSImage(contentsOfFile: path)
			icon?.isTemplate = true
			_toolBarIcon = icon
		}
	}

	required init?(coder: NSCoder) {
		fatalError("init(coder:) has not been implemented")
	}

	// Distinguishes the API version the plugin was built for. Return 1.
	func interfaceVersion() -> UInt {
		return 1
	}

	func groupID() -> UInt {
		// Return a number between 50 and 1000 to position the icon in the toolbar.
		return 50
	}

	func title() -> String! {
		// Return the name of the tool as it will appear in the tooltip of in the toolbar.
		return "___PACKAGENAME___"
	}

	func trigger() -> String! {
		// Return the key that the user can press to activate the tool.
		// Please make sure to not conflict with other tools.
		return "h"
	}

	func tempTrigger() -> NSEvent.ModifierFlags {
		// Return a modifierMask (e.g. .option, .command ...)
		return []
	}

	override func willSelectTempTool(_ tempTool: Any) -> Bool {
		// This is called when the user presses a modifier key (e.g. the cmd key to switch to the Select Tool).
		// Return false to prevent the tool switching.
		return true
	}

	override func keyDown(with theEvent: NSEvent) {
		// Called when a key is pressed while the tool is active.
		NSLog("keyDown: %@", theEvent)
	}

	override func doCommand(by aSelector: Selector) {
		NSLog("aSelector: %s", sel_getName(aSelector))
	}

	override func defaultContextMenu() -> NSMenu {
		// Adds items to the context menu.
		let theMenu = NSMenu(title: "Contextual Menu")
		theMenu.addItem(withTitle: "Foo", action: #selector(foo(_:)), keyEquivalent: "")
		theMenu.addItem(withTitle: "Bar", action: #selector(bar(_:)), keyEquivalent: "")
		return theMenu
	}

	override func addMenuItems(for theEvent: NSEvent, to theMenu: NSMenu) {
		// Adds an item to theMenu for theEvent.
		theMenu.insertItem(withTitle: "Wail", action: #selector(wail(_:)), keyEquivalent: "", at: theMenu.numberOfItems - 1)
	}

	@objc func foo(_ sender: Any?) {}
	@objc func bar(_ sender: Any?) {}
	@objc func wail(_ sender: Any?) {}

	override func mouseDown(with theEvent: NSEvent) {
		// Called when the mouse button is clicked.
		if let wc = value(forKey: "windowController") as? NSObject,
		   let editViewController = wc.perform(#selector(NSObject.value(forKey:)), with: "activeEditViewController")?.takeUnretainedValue() {
			setValue(editViewController, forKey: "editViewController")
		}
		self.dragStart = theEvent.locationInWindow
	}

	override func mouseDragged(with theEvent: NSEvent) {
		// Called when the mouse is moved with the primary button down.
		let loc = theEvent.locationInWindow
		NSLog("__mouse dragged to : %@", NSStringFromPoint(loc))
	}

	override func mouseUp(with theEvent: NSEvent) {
		// Called when the primary mouse button is released.
	}

	override func drawBackground(in dirtyRect: NSRect) {
		// Draw in the background, concerns the complete view.
	}

	override func drawForeground(in dirtyRect: NSRect) {
		// Draw in the foreground, concerns the complete view.
	}

	func drawLayer(_ layer: GSLayer, at point: NSPoint, asActive active: Bool, attributes: [AnyHashable: Any]) {
		// Draw anything for this particular layer.
		editViewController?.graphicView.draw(layer, at: point, asActive: active, attributes: attributes)
	}

	override func willActivate() {
		// Called when the tool is selected by the user.
	}

	override func willDeactivate() {}
}
