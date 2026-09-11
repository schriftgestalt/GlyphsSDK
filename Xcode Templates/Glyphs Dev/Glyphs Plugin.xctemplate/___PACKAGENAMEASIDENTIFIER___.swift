//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//  ___COPYRIGHT___
//

import Cocoa

@objc class ___FILEBASENAMEASIDENTIFIER___: NSObject, GlyphsPlugin {

	// Distinguishes the API version the plugin was built for. Return 1.
	var interfaceVersion: UInt {
		return 1
	}

	override init() {
		super.init()
		// do stuff
	}

	func load() {
		// Set up stuff
	}
}
