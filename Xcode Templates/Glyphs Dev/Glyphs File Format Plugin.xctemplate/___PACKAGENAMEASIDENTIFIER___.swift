//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//___COPYRIGHT___
//

import Cocoa

@objc class ___FILEBASENAMEASIDENTIFIER___: NSViewController, GlyphsFileFormat {

	@objc var font: GSFont?
	private var _toolbarIcon: NSImage?

	override init(nibName nibNameOrNil: NSNib.Name?, bundle nibBundleOrNil: Bundle?) {
		super.init(nibName: nibNameOrNil, bundle: nibBundleOrNil)
	}

	required init?(coder: NSCoder) {
		super.init(coder: coder)
	}

	convenience init() {
		let bundle = Bundle(for: Self.self)
		self.init(nibName: "___FILEBASENAMEASIDENTIFIER___Dialog", bundle: bundle)

		if let path = bundle.pathForImageResource(NSImage.Name("GenericExportTemplate")) {
			let icon = NSImage(contentsOfFile: path)
			icon?.setName("___FILEBASENAMEASIDENTIFIER___Icon")
			_toolbarIcon = icon
		}
	}

	func interfaceVersion() -> UInt {
		// Distinguishes the API version the plugin was built for. Return 1.
		return 1
	}

	func toolbarTitle() -> String {
		// Return the name of the tool as it will appear in export dialog.
		return "___PACKAGENAME___"
	}

	func toolbarIconName() -> String {
		return "___FILEBASENAMEASIDENTIFIER___Icon"
	}

	func groupID() -> UInt {
		// Position in the export panel. Higher numbers move it to the right.
		return 10
	}

	func exportSettingsView() -> NSView {
		return view
	}

	func font(from URL: URL, ofType typeName: String) throws -> GSFont {
		// Load the font at URL and return a GSFont object.
		throw NSError(domain: "___PACKAGENAME___", code: -1, userInfo: nil)
	}

	func write(_ font: GSFont) throws {
		// Write Font to disk. You have to ask for the path yourself. This is called from the export dialog.
	}

	func write(_ font: GSFont, to destinationURL: URL) throws {
		// Write Font to destinationURL.
	}

	func exportFont(_ font: GSFont) {
		// Exports a Font object.
		// This function should ask the user for the place to save the store the font.
		// Eventually errors have to be presented by the plugin. Use `font.parent?.presentError(error)`.
	}
}
