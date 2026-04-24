//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//___COPYRIGHT___
//

import Cocoa

@objc class ___FILEBASENAMEASIDENTIFIER___: NSObject, GlyphsReporter {

	var controller: (any NSViewController & GSGlyphEditViewControllerProtocol)!
	private var _editViewController: (NSViewController & GSGlyphEditViewControllerProtocol)?

	// Distinguishes the API version the plugin was built for. Return 1.
	func interfaceVersion() -> UInt {
		return 1
	}

	override init() {
		super.init()
		// do stuff
	}

	func title() -> String! {
		// This is the name as it appears in the menu in combination with 'Show'.
		// E.g. `return "Nodes"` will make the menu item read "Show Nodes".
		return NSLocalizedString("___PACKAGENAME___", tableName: nil, bundle: Bundle(for: Self.self), value: "", comment: "DESCRIPTION")
	}

	var keyEquivalent: String! {
		// The key for the keyboard shortcut. Set modifier keys in modifierMask further below.
		// Pretty tricky to find a shortcut that is not taken yet, so be careful.
		// If you are not sure, return nil. Users can set their own shortcuts in System Prefs.
		return nil
	}

	var modifierMask: NSEvent.ModifierFlags {
		// Use any combination of these to determine the modifier keys for your default shortcut:
		// return [.shift, .control, .command, .option]
		// Or:
		// return []
		// ... if you do not want to set a shortcut.
		return []
	}

	func drawForeground(for layer: GSLayer, options: [AnyHashable: Any]) {
		// Whatever you draw here will be displayed IN FRONT OF the paths.
		// To get an NSBezierPath from a GSPath, use the bezierPath method:
		//   myPath.bezierPath().fill()
		// You can apply that to a full layer at once:
		//   layer.bezierPath()      // all closed paths
		//   layer.openBezierPath()  // all open paths

		let rect = layer.bounds()
		NSColor.blue.set()
		NSBezierPath.fill(rect)
	}

	func drawBackground(for layer: GSLayer, options: [AnyHashable: Any]) {
		// Whatever you draw here will be displayed BEHIND the paths.
	}

	func drawBackground(forInactiveLayer layer: GSLayer, options: [AnyHashable: Any]) {
		// Whatever you draw here will be displayed behind the paths, but for inactive masters.
	}

	func needsExtraMainOutlineDrawing(forInactiveLayer layer: GSLayer) -> Bool {
		// Return false to disable the black outline. Otherwise remove the method.
		return false
	}

	func getScale() -> Float {
		// getScale() returns the current scale factor of the Edit View UI.
		// Divide any scalable size by this value in order to keep the same apparent pixel size.
		if let editViewController = _editViewController {
			return Float(editViewController.graphicView.scale)
		}
		return 1.0
	}

	func setController(_ controller: (NSViewController & GSGlyphEditViewControllerProtocol)?) {
		// Use self.controller as object for the current view controller.
		_editViewController = controller
	}
}
