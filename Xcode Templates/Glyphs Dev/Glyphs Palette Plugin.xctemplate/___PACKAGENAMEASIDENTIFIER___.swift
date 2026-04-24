//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//___COPYRIGHT___
//

import Cocoa

@objc class ___FILEBASENAMEASIDENTIFIER___: NSViewController, GlyphsPalette {

	@MainActor weak var windowController: (NSWindowController & GSWindowControllerProtocol)?

	// Distinguishes the API version the plugin was built for. Return 1.
	let interfaceVersion: UInt = 1

	required init?(coder: NSCoder) {
		super.init(coder: coder)
	}

	override init(nibName nibNameOrNil: NSNib.Name?, bundle nibBundleOrNil: Bundle?) {
		super.init(nibName: nibNameOrNil, bundle: nibBundleOrNil)
	}

	convenience init() {
		self.init(nibName: "___FILEBASENAMEASIDENTIFIER___View", bundle: Bundle(for: Self.self))
		(self.view as? GSPaletteView)?.controller = self
	}

	func loadPlugin() {
		self.title = "___PACKAGENAME___"
	}

	var minHeight: Int {
		return 85
	}

	var maxHeight: Int {
		return 265 // if this is bigger than minHeight, the palette is resizable
	}

	var currentHeight: UInt {
		get {
			return UInt(UserDefaults.standard.integer(forKey: "___FILEBASENAMEASIDENTIFIER___CurrentHeight"))
		}
		set {
			if newValue >= minHeight && newValue <= maxHeight {
				UserDefaults.standard.set(Int(newValue), forKey: "___FILEBASENAMEASIDENTIFIER___CurrentHeight")
			}
		}
	}

	var theView: NSView {
		return view
	}
}
