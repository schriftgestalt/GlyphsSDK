//
//  ___FILENAME___
//  ___PACKAGENAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//___COPYRIGHT___
//

import Cocoa

@objc class ___FILEBASENAMEASIDENTIFIER___: GSFilterPlugin {

	@IBOutlet weak var firstValueField: NSTextField?

	private var _firstValue: CGFloat = 15

	override var title: String! {
		// Return the name of the tool as it will appear in the menu.
		return "___PACKAGENAME___"
	}

	override func actionName() -> String! {
		// The title of the button in the filter dialog.
		return "___PACKAGENAME___"
	}

	override var keyEquivalent: String! {
		// The key together with Cmd+Shift will be the shortcut for the filter.
		// Return nil if you do not want to set a shortcut.
		// Users can set their own shortcuts in System Prefs.
		return nil
	}

	override var view: NSView! {
		get {
			if super.view == nil {
				Bundle(for: Self.self).loadNibNamed("___FILEBASENAMEASIDENTIFIER___Dialog", owner: self, topLevelObjects: nil)
			}
			return super.view
		}
		set { super.view = newValue }
	}

	override func setup() -> Error? {
		_ = super.setup()
		let fontMaster = value(forKey: "fontMaster") as? GSFontMaster
		if let firstValueNumber = fontMaster?.userData(forKey: "theFirstValue") as? NSNumber {
			_firstValue = CGFloat(firstValueNumber.floatValue)
		} else {
			_firstValue = 15
		}
		firstValueField?.floatValue = Float(_firstValue)
		return nil
	}

	func processLayer(_ layer: GSLayer, withFirstValue firstValue: CGFloat) {
		// this is a method specially for your filter. Add/remove arguments as you need.
		// do stuff with the Layer.
	}

	func process(_ font: GSFont, withArguments arguments: [Any]) {
		// Invoked when called as Custom Parameter in an instance at export.
		// The Arguments come from the custom parameter in the instance settings.
		// The first item in Arguments is the class-name. After that, it depends on the filter.
		var firstValue: CGFloat = 15
		if arguments.count > 1, let v = (arguments[1] as? NSNumber)?.floatValue {
			firstValue = CGFloat(v)
		}
		setValue(false, forKey: "checkSelection")
		guard let fontMasterId = font.fontMaster(at: 0)?.id else { return }
		for glyph in font.glyphs {
			guard let layer = glyph.layer(forId: fontMasterId) else { continue }
			processLayer(layer, withFirstValue: firstValue)
		}
	}

	@IBAction func setFirstValue(_ sender: Any) {
		// This is only an example for a setter method.
		// Add methods like this for each option in the dialog.
		guard let floatValue = (sender as AnyObject).floatValue else { return }
		let firstValue = CGFloat(floatValue)
		if abs(firstValue - _firstValue) > 0.01 {
			_firstValue = firstValue
			process(nil)
		}
	}

	override func process(_ sender: Any?) {
		guard let shadowLayers = value(forKey: "shadowLayers") as? [GSLayer] else { return }
		guard let layers = value(forKey: "layers") as? [GSLayer] else { return }
		let checkSelection = value(forKey: "checkSelection") as? Bool ?? false

		for k in 0..<shadowLayers.count {
			let shadowLayer = shadowLayers[k]
			let layer = layers[k]
			layer.shapes = NSMutableArray(array: shadowLayer.shapes, copyItems: true) as? [GSShape]
			layer.selection = NSMutableOrderedSet()
			if shadowLayer.selection.count > 0 && checkSelection {
				for i in 0..<shadowLayer.shapes.count {
					guard let shadowPath = shadowLayer.shapes[i] as? GSPath,
					      let layerPath  = layer.shapes[i]       as? GSPath else { continue }
					for j in 0..<shadowPath.nodes.count {
						let shadowNode = shadowPath.node(at: j)
						if shadowLayer.selection.contains(shadowNode as Any) {
							layer.addSelection(layerPath.nodes[j])
						}
					}
				}
			}
			processLayer(layer, withFirstValue: _firstValue)
			layer.clearSelection()
		}

		// Save the value in the FontMaster. But could be saved in UserDefaults, too.
		let fontMaster = value(forKey: "fontMaster") as? GSFontMaster
		fontMaster?.setUserData(NSNumber(value: Float(_firstValue)), forKey: "____TheFirstValue____")
		super.process(nil)
	}
}
