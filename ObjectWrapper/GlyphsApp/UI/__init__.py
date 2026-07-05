# encoding: utf-8

from __future__ import absolute_import, annotations

from .GlyphView import GlyphView
from .CanvasView import CanvasView
from .GlyphPreview import GlyphPreview
from typing import Any, List, TYPE_CHECKING

from AppKit import NSWindow, NSPanel, NSButton, NSTextField, NSSearchField, NSComboBox, NSPopUpButton, NSImage, NSScrollView, NSTableView, NSTableColumn, NSArrayController, \
	NSTitledWindowMask, NSClosableWindowMask, NSWindowStyleMaskResizable, NSUtilityWindowMask, NSBackingStoreBuffered, \
	NSTextAlignmentNatural, NSControlSizeRegular, NSControlSizeSmall, NSLayoutConstraintOrientationHorizontal, NSLayoutConstraintOrientationVertical, \
	NSControlStateValueOff, NSLayoutRelationGreaterThanOrEqual, NSLayoutRelationLessThanOrEqual, \
	NSTableColumnUserResizingMask, NSBezelBorder, NSNoBorder, NSValueBinding, NSMenuItem

from Foundation import NSRect, NSMakeRect, NSSelectorFromString, NSClassFromString  # type: ignore
import objc
from objc import python_method

from .. import callbackHelperClass

__all__ = ["GlyphView", "CanvasView", "GlyphPreview", "Window", "Panel", "Button", "Checkbox", "Label", "TextField", "SearchField", "ComboBox", "PopUpButton", "Table", "SteppingEditText", "autoLayout", "NSControlSizeSmall", "MenuItem"]


# stupid hack to allow code that doesn't expect NSButton.state to be a property (and access the value by `button.state()` (e.g. in vanilla)).
class intWrapper (int):
	def __new__(cls, value):
		return super().__new__(cls, value)

	def __call__(self):
		return self

if TYPE_CHECKING:
	from .classes import GSSteppingTextField  # type: ignore
else:
	GSSteppingTextField = NSClassFromString("GSSteppingTextField")


def _setMinimalSizeConstraint(control, compression=1000, hugging=900):
	control.setTranslatesAutoresizingMaskIntoConstraints_(False)
	control.setContentCompressionResistancePriority_forOrientation_(1000, NSLayoutConstraintOrientationVertical)
	control.setContentCompressionResistancePriority_forOrientation_(compression, NSLayoutConstraintOrientationHorizontal)
	control.setContentHuggingPriority_forOrientation_(900, NSLayoutConstraintOrientationVertical)
	control.setContentHuggingPriority_forOrientation_(hugging, NSLayoutConstraintOrientationHorizontal)


def _setCallback(control, action=None, target=None, callback=None):
	if callback:
		callbackHelper = callbackHelperClass(callback, "callback")  # type: ignore
		control.cell().setRepresentedObject_(callbackHelper)  # to keep a reference
		control.setTarget_(callbackHelper)
		control.setAction_(NSSelectorFromString("callback:"))
	else:
		control.setTarget_(target)
		control.setAction_(action)


def autoLayout(anchor1, anchor2=None, distance=0, priority=None, relation=None):
	if anchor2:
		if relation is NSLayoutRelationGreaterThanOrEqual:
			constraint = anchor1.constraintGreaterThanOrEqualToAnchor_constant_(anchor2, distance)
		elif relation is NSLayoutRelationLessThanOrEqual:
			constraint = anchor1.constraintLessThanOrEqualToAnchor_constant_(anchor2, distance)
		else:
			constraint = anchor1.constraintEqualToAnchor_constant_(anchor2, distance)
	else:
		if relation is NSLayoutRelationGreaterThanOrEqual:
			constraint = anchor1.constraintGreaterThanOrEqualToConstant_(distance)
		elif relation is NSLayoutRelationLessThanOrEqual:
			constraint = anchor1.constraintLessThanOrEqualToConstant_(distance)
		else:
			constraint = anchor1.constraintEqualToConstant_(distance)
	if priority:
		constraint.setPriority_(priority)
	constraint.setActive_(True)


def Panel(title="", frame=None, minSize=None, maxSize=None, autosaveName=None):
	mask = NSTitledWindowMask | NSUtilityWindowMask
	return _Window(NSPanel, mask, title, frame, minSize, maxSize, autosaveName=autosaveName)


def Window(title="", frame=None, minSize=None, maxSize=None, textured=False, autosaveName=None, closable=True):
	mask = NSTitledWindowMask
	return _Window(NSWindow, mask, title, frame, minSize, maxSize, textured, autosaveName, closable)


def _Window(windowClass, mask, title="", frame=None, minSize=None, maxSize=None, textured=False, autosaveName=None, closable=True):
	if frame is None:
		frame = NSMakeRect(100, 100, 100, 100)
	if closable:
		mask |= NSClosableWindowMask
	mask |= NSWindowStyleMaskResizable
	window = windowClass.alloc().initWithContentRect_styleMask_backing_defer_(frame, mask, NSBackingStoreBuffered, True)
	window.setReleasedWhenClosed_(False)
	window.setTitle_(title)
	if minSize:
		window.setMinSize_(minSize)
	if maxSize:
		window.setMaxSize_(maxSize)
	if autosaveName:
		window.setFrameAutosaveName_(autosaveName)
	return window


objc.addConvenienceForClass(
	"NSControl",
	(
		(
			"enabled",
			property(
				lambda self: self.isEnabled(),
				lambda self, value: self.setEnabled_(value)
			),
		),
	),
)


def Button(title="", frame=None, image=None, action=None, target=None, callback=None, sizeStyle=NSControlSizeRegular):
	if image and isinstance(image, str):
		image = NSImage.imageNamed_(image)
	if image is not None:
		button = NSButton.buttonWithTitle_image_target_action_(title, image, target, action)
	else:
		button = NSButton.buttonWithTitle_target_action_(title, target, action)
	if frame:
		button.setFrame_(frame)
	_setMinimalSizeConstraint(button)
	_setCallback(button, action, target, callback)
	button.setControlSize_(sizeStyle)
	return button


def Checkbox(title="", frame=None, value=NSControlStateValueOff, action=None, target=None, callback=None, sizeStyle=NSControlSizeRegular):
	button = NSButton.checkboxWithTitle_target_action_(title, None, None)
	if frame:
		button.setFrame_(frame)
	_setMinimalSizeConstraint(button)
	_setCallback(button, action, target, callback)
	button.setControlSize_(sizeStyle)
	return button

objc.addConvenienceForClass(
	"NSButton",
	(
		(
			"state",
			property(
				lambda self: intWrapper(self.pyobjc_instanceMethods.state()),
				lambda self, value: self.setState_(value)
			)
		),
		(
			"keyEquivalent",
			property(
				lambda self: self.pyobjc_instanceMethods.keyEquivalent(),
				lambda self, value: self.setKeyEquivalent_(value)
			)
		),
		(
			"keyEquivalentModifierMask",
			property(
				lambda self: self.pyobjc_instanceMethods.keyEquivalentModifierMask(),
				lambda self, value: self.setKeyEquivalentModifierMask_(value)
			)
		),
	)
)


def Label(text="", frame=None, alignment=NSTextAlignmentNatural, wrapps=False, selectable=False, sizeStyle=NSControlSizeRegular, hugging=750):
	if not wrapps:
		textField = NSTextField.labelWithString_(text)
	else:
		textField = NSTextField.wrappingLabelWithString_(text)
	_setMinimalSizeConstraint(textField, hugging=hugging)
	if frame:
		textField.setFrame_(frame)
	textField.setAlignment_(alignment)
	textField.setSelectable_(selectable)
	textField.setControlSize_(sizeStyle)
	return textField


def TextField(text="", frame=None, alignment=NSTextAlignmentNatural, action=None, target=None, continuous=False, callback=None, formatter=None, sizeStyle=NSControlSizeRegular):
	textField = NSTextField.textFieldWithString_(text)
	_setMinimalSizeConstraint(textField, compression=250, hugging=250)
	if frame:
		textField.setFrame_(frame)
	textField.setAlignment_(alignment)
	textField.setControlSize_(sizeStyle)
	_setCallback(textField, action, target, callback)
	textField.setContinuous_(continuous)
	if formatter is not None:
		TextField.cell().setFormatter_(formatter)
	return textField

objc.addConvenienceForClass(
	"NSButton",
	(
		(
			"stringValue",
			property(
				lambda self: self.pyobjc_instanceMethods.stringValue(),
				lambda self, value: self.setStringValue_(value)
			)
		),
		(
			"placeholder",
			property(
				lambda self: self.placeholderString(),
				lambda self, value: self.setPlaceholderString_(value)
			)
		),
	)
)


def SteppingTextField(text="", frame=None, alignment=NSTextAlignmentNatural, sizeStyle=NSControlSizeRegular):
	textField = GSSteppingTextField.textFieldWithString_(text)
	_setMinimalSizeConstraint(textField, compression=250, hugging=250)
	if frame:
		textField.setFrame_(frame)
	textField.setAlignment_(alignment)
	textField.setControlSize_(sizeStyle)
	return textField


def SearchField(frame=None, action=None, target=None, continuous=False, callback=None, sizeStyle=NSControlSizeRegular):
	textField = NSSearchField.new()
	_setMinimalSizeConstraint(textField, compression=250, hugging=250)
	if frame:
		textField.setFrame_(frame)
	textField.setControlSize_(sizeStyle)
	_setCallback(textField, action, target, callback)
	textField.setContinuous_(continuous)
	return textField


class UIComboBox(NSComboBox):

	@python_method
	def _callVanillaCallback(self, notification):
		target = self.target()
		if target is not None:
			target.performSelector_withObject_(self.action(), self)

	def controlTextDidChange_(self, notification):
		if self.isContinuous():
			self._callVanillaCallback(notification)

	def controlTextDidEndEditing_(self, notification):
		if not self.isContinuous():
			self._callVanillaCallback(notification)

	def comboBoxSelectionDidChange_(self, notification):
		self.setObjectValue_(self.objectValueOfSelectedItem())
		self._callVanillaCallback(notification)


def ComboBox(items=[], frame=None, completes=True, continuous=False, action=None, target=None, callback=None, formatter=None, sizeStyle=NSControlSizeRegular):
	if frame:
		comboBox = UIComboBox.alloc().initWithFrame_(frame)
	else:
		comboBox = UIComboBox.new()
	_setMinimalSizeConstraint(comboBox, hugging=250)
	comboBox.addItemsWithObjectValues_(items)
	comboBox.setContinuous_(continuous)
	comboBox.setCompletes_(completes)
	_setCallback(comboBox, action, target, callback)
	comboBox.setDelegate_(comboBox)
	if formatter is not None:
		TextField.cell().setFormatter_(formatter)

	comboBox.setControlSize_(sizeStyle)
	return comboBox


def PopUpButton(items=[], frame=None, action=None, target=None, callback=None, sizeStyle=NSControlSizeRegular):
	if frame is None:
		frame = NSMakeRect(10, 10, 100, 20)
	popUpButton = NSPopUpButton.alloc().initWithFrame_pullsDown_(frame, False)
	_setMinimalSizeConstraint(popUpButton, hugging=250)
	popUpButton.addItemsWithTitles_(items)
	_setCallback(popUpButton, action, target, callback)
	popUpButton.setControlSize_(sizeStyle)
	return popUpButton


def __NSPopUpButton__setitems__(self, items):
	self.removeAllItems()
	self.addItemsWithTitles_(items)

objc.addConvenienceForClass(
	"NSPopUpButton",
	(
		(
			"selectedIndex",
			property(
				lambda self: self.indexOfSelectedItem(),
				lambda self, value: self.selectItemAtIndex_(int(value))
			)
		),
		(
			"selectedObject",
			property(
				lambda self: self.titleOfSelectedItem(),
				lambda self, value: self.selectItemWithTitle_(value)
			)
		),
		(
			"items",
			property(
				lambda self: self.itemArray(),
				lambda self, value: __NSPopUpButton__setitems__(self, value)
			)
		),
	)
)


NSTableViewDelegate = objc.protocolNamed('NSTableViewDelegate')


class UITableview(NSTableView, protocols=[NSTableViewDelegate]):  # type: ignore

	_arrayController: NSArrayController | None

	def __init__(self):
		self._selectionCallback = None

	def tableViewSelectionDidChange_(self, notification):
		if self._selectionCallback:
			self._selectionCallback(self)

	def doubleClickCallback_(self, sender):
		if self._doubleClickCallback:
			self._doubleClickCallback(self)

	@property
	def selectionCallback(self):
		return self._selectionCallback

	@selectionCallback.setter
	def selectionCallback(self, selectionCallback):
		self._selectionCallback = selectionCallback

	@property
	def doubleClickCallback(self):
		return self._doubleClickCallback

	@doubleClickCallback.setter
	def doubleClickCallback(self, doubleClickCallback):
		if doubleClickCallback is not None:
			self.setDoubleAction_(objc.selector(self.doubleClickCallback_, signature=b"v@:@"))
			self.setTarget_(self)
		else:
			self.setDoubleAction_(None)
			self.setTarget_(None)
		self._doubleClickCallback = doubleClickCallback

	def dealloc(self):
		for column in self.tableColumns():
			contentKey = column.identifier()
			column.unbind_("arrangedObjects." + contentKey)

	@property
	def content(self):
		if self._arrayController:
			return self._arrayController.content()
		else:
			return None

	@content.setter
	def content(self, content):
		# assert(len(content) > 0)
		if self._arrayController:
			self._arrayController.setContent_(content)


def Table(
	columns: List | None = None,
	arrayController: NSArrayController | None = None,
	content: List | None = None,
	frame: NSRect | None = None,
	borderType=NSBezelBorder,
	selectionCallback: Any = None,
	doubleClickCallback: Any = None,
	sizeStyle: int = NSControlSizeRegular,
	rowHeight: float = 22
):
	if frame is None:
		frame = NSMakeRect(10, 10, 100, 20)
	scroller = NSScrollView.alloc().initWithFrame_(frame)
	scroller.setTranslatesAutoresizingMaskIntoConstraints_(False)
	if borderType is None:
		borderType = NSNoBorder
	scroller.setBorderType_(borderType)
	table: UITableview = UITableview.new()
	table.selectionCallback = selectionCallback
	if doubleClickCallback is not None:
		table.doubleClickCallback = doubleClickCallback
	table.setDelegate_(table)
	table.setRowHeight_(rowHeight)
	table.setControlSize_(sizeStyle)
	table.setRowSizeStyle_(sizeStyle)

	if arrayController is None and content is not None:
		arrayController = NSArrayController.new()
		arrayController.setContent_(content)
		columns = [{"title": "-", "width": 100}]
	table._arrayController = arrayController

	for column in columns or []:
		title = column["title"]
		# contentType = column.get("type", "text")
		contentKey = column.get("key", "self")
		width = column.get("width", None)
		minWidth = column.get("minWidth", width)
		maxWidth = column.get("maxWidth", width)
		column = NSTableColumn.alloc().initWithIdentifier_(contentKey)
		column.setTitle_(title)
		if width is not None:
			column.setWidth_(width)
			column.setMinWidth_(minWidth)
			column.setMaxWidth_(maxWidth)
			if maxWidth - minWidth > 1:
				column.setResizingMask_(NSTableColumnUserResizingMask)
		table.addTableColumn_(column)
		column.bind_toObject_withKeyPath_options_(NSValueBinding, arrayController, "arrangedObjects." + contentKey, None)
	scroller.setDocumentView_(table)
	return scroller


def NSWindow__add(self, view):
	self.contentView().addSubview_(view)


def NSWindow__open(self):
	self.orderFront_(None)

def NSWindow__close(self):
	self.orderOut_(None)

objc.addConvenienceForClass(
	"NSWindow",
	(
		(
			"add",
			objc.python_method(NSWindow__add)
		),
		(
			"open",
			objc.python_method(NSWindow__open)
		),
		(
			"close",
			NSWindow.orderOut_
		),
		(
			"makeKey",
			NSWindow.makeKeyWindow
		),
	)
)

# NSWindow.add = objc.python_method(NSWindow__add)
# NSWindow.open = objc.python_method(NSWindow__open)
# NSWindow.close = objc.python_method(NSWindow__close)
# NSWindow.makeKey = objc.python_method(NSWindow.makeKeyWindow)

objc.addConvenienceForClass(
	"NSView",
	(
		(
			"left",
			property(lambda self: self.leadingAnchor()),
		),
		(
			"right",
			property(lambda self: self.trailingAnchor()),
		),
		(
			"top",
			property(lambda self: self.topAnchor()),
		),
		(
			"bottom",
			property(lambda self: self.bottomAnchor()),
		),
		(
			"centerX",
			property(lambda self: self.centerXAnchor()),
		),
		(
			"centerY",
			property(lambda self: self.centerYAnchor()),
		),
		(
			"width",
			property(lambda self: self.widthAnchor()),
		),
		(
			"height",
			property(lambda self: self.heightAnchor()),
		),
		(
			"baseline",
			property(lambda self: self.firstBaselineAnchor()),
		),
		(
			"huggingHorizontal",
			property(
				lambda self: self.contentHuggingPriorityForOrientation_(NSLayoutConstraintOrientationHorizontal),
				lambda self, value: self.setContentHuggingPriority_forOrientation_(value, NSLayoutConstraintOrientationHorizontal)
			),
		),
		(
			"huggingVertical",
			property(
				lambda self: self.contentHuggingPriorityForOrientation_(NSLayoutConstraintOrientationVertical),
				lambda self, value: self.setContentHuggingPriority_forOrientation_(value, NSLayoutConstraintOrientationVertical)
			),
		),
		(
			"compressionHorizontal",
			property(
				lambda self: self.contentCompressionResistancePriorityForOrientation_(NSLayoutConstraintOrientationHorizontal),
				lambda self, value: self.setContentCompressionResistancePriority_forOrientation_(value, NSLayoutConstraintOrientationHorizontal)
			)
		),
		(
			"compressionVertical",
			property(
				lambda self: self.contentCompressionResistancePriorityForOrientation_(NSLayoutConstraintOrientationVertical),
				lambda self, value: self.setContentCompressionResistancePriority_forOrientation_(value, NSLayoutConstraintOrientationVertical)
			)
		),
		(
			"toolTip",
			property(
				lambda self: self.pyobjc_instanceMethods.toolTip(),
				lambda self, value: self.setToolTip_(value)
			)
		),
	)
)

# NSView.left = property(lambda self: self.leadingAnchor())
# NSView.right = property(lambda self: self.trailingAnchor())
# NSView.top = property(lambda self: self.topAnchor())
# NSView.bottom = property(lambda self: self.bottomAnchor())
# NSView.centerX = property(lambda self: self.centerXAnchor())
# NSView.centerY = property(lambda self: self.centerYAnchor())
# NSView.width = property(lambda self: self.widthAnchor())
# NSView.height = property(lambda self: self.heightAnchor())
# NSView.baseline = property(lambda self: self.firstBaselineAnchor())

# NSView.huggingHorizontal = property(
# 	lambda self: self.contentHuggingPriorityForOrientation_(NSLayoutConstraintOrientationHorizontal),
# 	lambda self, value: self.setContentHuggingPriority_forOrientation_(value, NSLayoutConstraintOrientationHorizontal)
# )

# NSView.huggingVertical = property(
# 	lambda self: self.contentHuggingPriorityForOrientation_(NSLayoutConstraintOrientationVertical),
# 	lambda self, value: self.setContentHuggingPriority_forOrientation_(value, NSLayoutConstraintOrientationVertical)
# )

# NSView.compressionHorizontal = property(
# 	lambda self: self.contentCompressionResistancePriorityForOrientation_(NSLayoutConstraintOrientationHorizontal),
# 	lambda self, value: self.setContentCompressionResistancePriority_forOrientation_(value, NSLayoutConstraintOrientationHorizontal)
# )

# NSView.compressionVertical = property(
# 	lambda self: self.contentCompressionResistancePriorityForOrientation_(NSLayoutConstraintOrientationVertical),
# 	lambda self, value: self.setContentCompressionResistancePriority_forOrientation_(value, NSLayoutConstraintOrientationVertical)
# )


objc.addConvenienceForClass(
	"NSWindow",
	(
		(
			"left",
			property(lambda self: self.contentView().leadingAnchor()),
		),
		(
			"right",
			property(lambda self: self.contentView().trailingAnchor()),
		),
		(
			"top",
			property(lambda self: self.contentView().topAnchor()),
		),
		(
			"bottom",
			property(lambda self: self.contentView().bottomAnchor()),
		),
		(
			"centerX",
			property(lambda self: self.contentView().centerXAnchor()),
		),
		(
			"centerY",
			property(lambda self: self.contentView().centerYAnchor()),
		),
	)
)
# NSWindow.left = property(lambda self: self.contentView().leadingAnchor())
# NSWindow.right = property(lambda self: self.contentView().trailingAnchor())
# NSWindow.top = property(lambda self: self.contentView().topAnchor())
# NSWindow.bottom = property(lambda self: self.contentView().bottomAnchor())
# NSWindow.centerX = property(lambda self: self.contentView().centerXAnchor())
# NSWindow.centerY = property(lambda self: self.contentView().centerYAnchor())


def savePreferences(sender):
	print("__savePreferences", sender)


def setAnchorNames(sender):
	print("__setAnchorNames", sender)


def moveAction(sender):
	print("__moveAction", sender)


def AnchorMoverExample():
	w = Panel(title="Anchor Mover")
	text_1 = Label(text="Move anchor", sizeStyle=NSControlSizeSmall)
	w.add(text_1)
	autoLayout(text_1.top, w.top, 20)
	autoLayout(text_1.left, w.left, 20)
	anchor_name = ComboBox(items=("top", "bottom"), sizeStyle=NSControlSizeSmall, callback=savePreferences)
	w.add(anchor_name)
	autoLayout(anchor_name.centerY, text_1.centerY, 0)
	autoLayout(anchor_name.left, text_1.right, 10)
	autoLayout(anchor_name.width, None, 190)
	button = Button(image="NSRefreshTemplate", sizeStyle=NSControlSizeSmall, callback=setAnchorNames)
	w.add(button)
	autoLayout(anchor_name.right, button.left, -10)
	autoLayout(button.centerY, text_1.centerY, 0)
	text_2 = Label(text="in selected glyphs:", sizeStyle=NSControlSizeSmall, hugging=250)
	w.add(text_2)
	autoLayout(text_2.top, w.top, 20)
	autoLayout(text_2.right, w.right, -20)
	autoLayout(button.right, text_2.left, -10)
	items = ("current position", "LSB", "RSB", "center", "bbox left edge", "bbox center", "bbox right edge", "highest node", "lowest node")
	hTarget = PopUpButton(items, sizeStyle=NSControlSizeSmall, callback=savePreferences)
	w.add(hTarget)
	autoLayout(hTarget.top, text_1.bottom, 20)
	autoLayout(hTarget.left, w.left, 20)
	hChange = TextField(sizeStyle=NSControlSizeSmall)
	w.add(hChange)
	autoLayout(hChange.centerY, hTarget.centerY, 0)
	autoLayout(hChange.left, hTarget.right, 20)
	autoLayout(hChange.width, None, 100)
	italic = Checkbox("Respect italic angle", value=True, sizeStyle=NSControlSizeSmall, callback=savePreferences)
	w.add(italic)
	autoLayout(italic.left, hChange.right, 20)
	autoLayout(hChange.centerY, italic.centerY, 0)
	autoLayout(italic.right, w.right, -20)
	button = Button("Move", callback=moveAction)
	button.keyEquivalent = "\r"
	w.add(button)
	autoLayout(button.top, hTarget.bottom, 8)
	autoLayout(button.right, w.right, -20)
	autoLayout(button.bottom, w.bottom, -20)
	w.open()


def TableExample():
	w = Window(title="Table Example")
	label_1 = Label(text="A Label", sizeStyle=NSControlSizeSmall, hugging=249)
	w.add(label_1)
	autoLayout(label_1.top, w.top, 20)
	autoLayout(label_1.left, w.left, 20)
	autoLayout(label_1.right, w.right, -20)
	# autoLayout(label_1.bottom, w.bottom, -20) # don’t add bottom constraint here. The table will do that

	columns = [{
		"title": "First Column",
		"width": 150
	}]

	content = [
		"First",
		"Second",
		"Third",
	]
	arrayController = NSArrayController.new()
	arrayController.setContent_(content)

	def selectionCallback(table):
		print("__selection", table, table.selectedRow())

	def doubleAction(table):
		print("__doubleAction", table, table.clickedRow())

	table = Table(columns, arrayController, selectionCallback=selectionCallback, doubleClickCallback=doubleAction)
	w.add(table)
	autoLayout(table.top, label_1.bottom, 20)
	autoLayout(table.left, w.left, 20)
	autoLayout(table.right, w.right, -20)
	autoLayout(table.bottom, w.bottom, -20)
	autoLayout(table.height, distance=260)

	w.open()


if __name__ == "__main__":
	TableExample()

try:
	from vanilla import EditText
except:
	EditText = object  # type: ignore


class SteppingEditText(EditText):  # type: ignore
	nsTextFieldClass = GSSteppingTextField


# Vanilla compatibility
objc.addConvenienceForClass(
	"NSTextField",
	(
		(
			"get",
			python_method(lambda self: self.stringValue),
		),
		(
			"set",
			python_method(lambda self, value: self.setStringValue_(value))
		),
	)
)

objc.addConvenienceForClass(
	"NSButton",
	(
		(
			"get",
			python_method(lambda self: self.state),
		),
		(
			"set",
			python_method(lambda self, value: self.setState_(value))
		),
	)
)

objc.addConvenienceForClass(
	"NSPopUpButton",
	(
		(
			"get",
			python_method(lambda self: self.indexOfSelectedItem())
		),
		(
			"set",
			python_method(lambda self, value: self.selectItemAtIndex_(value))
		),
	)
)

# NSTextField.get = python_method(lambda self: self.stringValue)
# NSTextField.set = python_method(lambda self, value: self.setStringValue_(value))
# NSButton.get = python_method(lambda self: self.state)
# NSButton.set = python_method(lambda self, value: self.setState_(value))
# NSPopUpButton.get = python_method(lambda self: self.indexOfSelectedItem())
# NSPopUpButton.set = python_method(lambda self, value: self.selectItemAtIndex_(value))


def MenuItem(title, action=None, target=None, keyboard="", modifier=0):
	item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, action, keyboard)
	item.setTarget_(target)
	return item
