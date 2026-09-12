# Type stubs for vanilla
# For more details, see the vanilla documentation:
# https://vanilla.robotools.dev/en/latest/

from typing import Any, Callable, Sequence, TypedDict

from AppKit import NSButton, NSColor, NSFormatter, NSImage, NSScreen

from .vanillaBase import PosSize, Size, VanillaBaseControl, VanillaBaseObject

# Windows and Containers
class Window(VanillaBaseObject):
    def __init__(self, posSize: Size, title: str = "", minSize: tuple[int, int] | None = None, maxSize: tuple[int, int] | None = None, textured: bool = False, autosaveName: str | None = None, closable: bool = True, miniaturizable: bool = True, initiallyVisible: bool = True, fullScreenMode=None, titleVisible: bool = True, fullSizeContentView: bool = False, screen: NSScreen | None = None): ...
    def open(self) -> None: ...
    def show(self) -> None: ...
    def close(self) -> None: ...
    def setContent(self, view: Any) -> None: ...
    def getTitle(self) -> str: ...
    def setTitle(self, title: str) -> None: ...
    def getWindow(self) -> Any: ...
    def setDefaultButton(self, button: "Button") -> None: ...
    def makeKey(self) -> None: ...
    def isVisible(self) -> bool: ...
    def center(self) -> None: ...

class Sheet(Window):
    def __init__(self, posSize: Size, parentWindow: Window): ...
    def close(self, someValue: Any = None) -> None: ...

class FloatingWindow(Window):
    ...

class Drawer(VanillaBaseObject):
    def __init__(self, posSize: PosSize, parentWindow: Window, preferredEdge: str = "left", style: str = "regular"): ...
    def open(self) -> None: ...
    def close(self) -> None: ...
    def toggle(self) -> None: ...
    def isVisible(self) -> bool: ...

class Group(VanillaBaseObject):
    def __init__(self, posSize: PosSize): ...

class ScrollView(VanillaBaseObject):
    def __init__(self, posSize: PosSize, documentView: Any, backgroundColor: Any | None = None, hasHorizontalScroller: bool = True, hasVerticalScroller: bool = True, autohidesScrollers: bool = True): ...
    def setDocumentView(self, view: Any) -> None: ...
    def getDocumentView(self) -> Any: ...
    def scrollToPoint(self, point: tuple[int, int]) -> None: ...
    def getVerticalScroller(self) -> Any: ...
    def getHorizontalScroller(self) -> Any: ...

# Basic Controls
class Button(VanillaBaseControl):
    def __init__(self, posSize: PosSize, title: str, callback: Callable[..., Any] | None = None, style: str = "rounded", sizeStyle: str = "regular"): ...
    def get(self) -> str: ...
    def set(self, title: str) -> None: ...
    def getNSButton(self) -> NSButton: ...


class ImageButton(Button):
    def __init__(self, posSize: PosSize, imagePath: str | None = None, imageNamed: str | None = None, imageObject: NSImage | None = None, title: str | None = None, bordered: bool = True, imagePosition: str = "top", callback: Any | None = None, sizeStyle: str = "regular"): ...

class TextBox(VanillaBaseControl):
    def __init__(self, posSize: PosSize, text: str = "", alignment: str = "left", selectable: bool = False, sizeStyle: str = "regular", readOnly: bool = True): ...
    def get(self) -> str: ...
    def set(self, text: str) -> None: ...

class EditText(VanillaBaseControl):
    def __init__(self, posSize: PosSize, text: str | int = "", callback: Callable[..., Any] | None = None, continuous: bool = True, readOnly: bool = False, formatter: NSFormatter | None = None, placeholder: str | None = None, sizeStyle: str = "regular"): ...
    def get(self) -> str: ...
    def set(self, text: str | int | float) -> None: ...
    def _setCallback(self, Any) -> None: ...

class CheckBox(Button):
    def __init__(self, posSize: PosSize, title: str, callback: Callable[..., Any] | None = None, value: bool = False, sizeStyle: str = "regular"): ...
    def get(self) -> bool: ...
    def set(self, value: bool) -> None: ...

class RadioGroup(VanillaBaseControl):
    def __init__(self, posSize: PosSize, titles: list[str], isVertical: bool = True, callback: Callable[..., Any] | None = None, sizeStyle: str = "regular"): ...
    def get(self) -> int: ...
    def set(self, value: int) -> None: ...

class PopUpButton(VanillaBaseControl):
    def __init__(self, posSize: PosSize, items: Sequence[str], callback: Callable[..., Any] | None = None, sizeStyle: str = "regular", bordered: bool = True): ...
    def get(self) -> int: ...
    def set(self, value: int) -> None: ...
    def getItems(self) -> list[str]: ...
    def setItems(self, items: list[str]) -> None: ...

class Popover(VanillaBaseControl):
    def __init__(self, size: Size, parentView: VanillaBaseControl | None = None, preferredEdge: str = "top", behavior: str = "semitransient"): ...

class ActionButton(PopUpButton):
    def __init__(self, posSize: PosSize, items: list[str | dict[str, Any]], sizeStyle: str = "regular", bordered: bool = True): ...

class ComboBox(VanillaBaseControl):
    def __init__(self, posSize: PosSize, items: Sequence[str | int | float], completes: bool = True, callback: Callable[..., Any] | None = None, continuous: bool = True, sizeStyle: str = "regular"): ...
    def get(self) -> str: ...
    def set(self, value: str) -> None: ...
    def getItems(self) -> list[str]: ...
    def setItems(self, items: list[str]) -> None: ...

class SegmentedButton(VanillaBaseControl):
    def __init__(self, posSize: PosSize, segmentDescriptions: list[dict], callback: Callable[..., Any] | None = None, selectionStyle: str = "one", sizeStyle: str = "small"): ...

class Slider(VanillaBaseControl):
    def __init__(self, posSize: PosSize, minValue: float = 0.0, maxValue: float = 100.0, value: float = 50.0, callback: Callable[..., Any] | None = None, tickMarkCount: float | None = None, stopOnTickMarks: bool = False, continuous: bool = True, sizeStyle: str = "regular", tickMarks: int | None = None): ...
    def get(self) -> float: ...
    def set(self, value: float) -> None: ...

class ProgressSpinner(VanillaBaseObject):
    def __init__(self, posSize: PosSize, displayWhenStopped: bool = True, isIndeterminate: bool = True, sizeStyle: str = "regular"): ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def isIndeterminate(self) -> bool: ...
    def setIndeterminate(self, value: bool) -> None: ...

class ProgressBar(VanillaBaseObject):
    def __init__(self, posSize: PosSize, minValue: float = 0, maxValue: float = 100, isIndeterminate: bool = False, sizeStyle: str = "regular", progressStyle: str = "bar"): ...

# Lists and Tables
class List(VanillaBaseObject):
    def __init__(
        self,
        posSize: PosSize,
        items: list[Any],
        dataSource: Any | None = None,
        columnDescriptions: list[dict] | None = None,
        showColumnTitles: bool = True,
        selectionCallback: Callable[..., Any] | None = None,
        doubleClickCallback: Callable[..., Any] | None = None,
        editCallback: Callable[..., Any] | None = None,
        menuCallback: Callable[..., Any] | None = None,
        enableDelete: bool = False,
        enableTypingSensitivity: bool = False,
        allowsMultipleSelection: bool = False,
        allowsEmptySelection: bool = True,
        allowsSorting: bool = True,
        drawVerticalLines: bool = False,
        drawHorizontalLines: bool = False,
        autohidesScrollers: bool = True,
        drawFocusRing: bool = True,
        rowHeight: float = 17.0,
        selfDropSettings: Any | None = None,
        selfWindowDropSettings: Any | None = None,
        selfDocumentDropSettings: Any | None = None,
        selfApplicationDropSettings: Any | None = None,
        otherApplicationDropSettings: Any | None = None,
        dragSettings: Any | None = None,
        doubleClickcallback: Any = None
    ): ...
    def get(self) -> list[Any]: ...
    def set(self, items: list[Any]) -> None: ...
    def getSelection(self) -> list[int]: ...
    def setSelection(self, selection: list[int]) -> None: ...
    def getSelectedIndexes(self) -> list[int]: ...  # Deprecated
    def setSelectedIndexes(self, selection: list[int]) -> None: ...  # Deprecated
    def refresh(self) -> None: ...



class _ColumnDescriptionRequired(TypedDict):
    identifier: str


class ColumnDescription(_ColumnDescriptionRequired, total=False):
    """Description dict for a single column in List2."""

    title: str
    cellClass: type
    cellClassArguments: dict[str, Any]
    valueToCellConverter: Callable[[Any], Any]
    cellToValueConverter: Callable[[Any], Any]
    editable: bool
    width: float
    minWidth: float
    maxWidth: float
    sortable: bool
    property: str
    getMethod: str
    setMethod: str
    getFunction: Callable[[Any], Any]
    setFunction: Callable[[Any, Any], Any]


class List2GroupRow:
    """A sentinel item that renders as a group-header row inside a List2."""

    value: Any

    def __init__(self, value: Any = None) -> None: ...


class List2:
    """
    A control that shows a list of items in one or more columns,
    backed by an NSTableView inside an NSScrollView.
    """

    def __init__(
        self,
        posSize: PosSize,
        items: Sequence[Any] = ...,
        columnDescriptions: Sequence[ColumnDescription] = ...,
        allowsSelection: bool = True,
        allowsMultipleSelection: bool = True,
        allowsEmptySelection: bool = True,
        allowsSorting: bool = True,
        allowColumnReordering: bool = True,
        enableDelete: bool = False,
        enableTypingSensitivity: bool = False,
        showColumnTitles: bool = True,
        drawFocusRing: bool = True,
        drawVerticalLines: bool = False,
        drawHorizontalLines: bool = False,
        alternatingRowColors: bool = True,
        autohidesScrollers: bool = False,
        selectionCallback: Callable[["List2"], None] | None = None,
        doubleClickCallback: Callable[["List2"], None] | None = None,
        editCallback: Callable[["List2"], None] | None = None,
        deleteCallback: Callable[["List2"], None] | None = None,
        menuCallback: Callable[["List2"], list[Any] | None] | None = None,
        allowsGroupRows: bool = False,
        floatsGroupRows: bool = False,
        groupRowCellClass: type | None = None,
        groupRowCellClassArguments: dict[str, Any] = ...,
        autosaveName: str | None = None,
        dragSettings: dict[str, Any] | None = None,
        dropSettings: dict[str, Any] | None = None,
    ) -> None: ...

    # ----- Columns -----

    def getColumnIdentifiers(self) -> list[str]:
        """Return a list of column identifiers in display order."""
        ...

    def appendColumn(self, columnDescription: ColumnDescription) -> None:
        """Append a column. The identifier must be unique for this table."""
        ...

    def insertColumn(self, index: int, columnDescription: ColumnDescription) -> None:
        """
        Insert a column at *index*. Pass ``-1`` to append.
        The identifier must be unique for this table.
        """
        ...

    def removeColumn(self, identifier: str) -> None:
        """
        Remove the column with *identifier*.
        Fails silently when the column does not exist.
        """
        ...

    # ----- Native views -----

    def getNSTableView(self) -> Any:
        """Return the underlying ``NSTableView``."""
        ...

    def getNSScrollView(self) -> Any:
        """Return the underlying ``NSScrollView``."""
        ...

    # ----- State -----

    def enable(self, onOff: bool) -> None:
        """Enable or disable the control."""
        ...

    def setShowFocusRing(self, value: bool) -> None:
        """Show or hide the focus ring."""
        ...

    # ----- Data -----

    def set(self, items: Sequence[Any]) -> None:
        """Replace the current items with *items*."""
        ...

    def get(self) -> list[Any]:
        """Return all items in their original (unsorted) order."""
        ...

    def getArrangedIndexes(self) -> list[int]:
        """Return item indexes in the order they are currently displayed."""
        ...

    def getArrangedItems(self) -> list[Any]:
        """Return items in the order they are currently displayed."""
        ...

    def reloadData(self, indexes: Sequence[int] | None = None) -> None:
        """
        Refresh the visible cells.  Pass *indexes* to reload only specific
        items; omit (or pass ``None``) to reload everything.
        """
        ...

    # ----- Selection -----

    def getSelectedItems(self) -> list[Any]:
        """Return the currently selected items."""
        ...

    def setSelectedItems(self, items: Sequence[Any]) -> None:
        """
        Select *items* by object identity.
        Prefer ``setSelectedIndexes`` for large lists to avoid O(n) iteration.
        """
        ...

    def getSelectedIndexes(self) -> list[int]:
        """Return the indexes (into the full item list) of selected rows."""
        ...

    def setSelectedIndexes(self, indexes: Sequence[int]) -> None:
        """Select the items at *indexes* (indexes into the full item list)."""
        ...

    def getEditedIndex(self) -> int | None:
        """
        Return the index of the row currently being edited.
        Only valid inside an ``editCallback``.
        """
        ...

    def getEditedItem(self) -> Any:
        """
        Return the item of the row currently being edited.
        Only valid inside an ``editCallback``.
        """
        ...

    def scrollToSelection(self) -> None:
        """Scroll so that the first selected row is visible."""
        ...

    def scrollToIndex(self, row: int) -> None:
        """Scroll so that *row* is visible."""
        ...

    def removeSelection(self) -> None:
        """Delete the selected items from the list."""
        ...

    # ----- Contextual menu -----

    def setMenu(self, items: Sequence[Any]) -> None:
        """
        Attach a static contextual menu built from *items*.
        Use ``menuCallback`` for a dynamic menu instead.
        """
        ...

    # ----- Drag and drop -----

    def setDropSettings(self, settings: dict[str, Any]) -> None:
        """Configure drop behaviour. See the class docstring for valid keys."""
        ...


class CheckBoxList2Cell:
    """A check box cell for use in a List2 column."""

    def __init__(
        self,
        title: str | None = None,
        editable: bool = False,
        callback: Callable[["CheckBoxList2Cell"], None] | None = None,
    ) -> None: ...
    def set(self, value: bool) -> None: ...
    def get(self) -> bool: ...



class Table(List):
    # Inherits from List, has similar API but with columns.
    # The 'items' are typically dictionaries.
    def __init__(self, posSize: PosSize, columnDescriptions: list[dict], items: list[dict] = [], **kwargs): ...


# Other UI Elements
class Box(VanillaBaseObject):
    def __init__(self, posSize: PosSize, title: str = "", fillColor: NSColor | None = None, borderColor: NSColor | None = None, borderWidth: float | None = None, cornerRadius: float | None = None, margins: float | None = None): ...

class HorizontalLine(Box):
    def __init__(self, posSize: PosSize): ...

class VerticalLine(Box):
    def __init__(self, posSize: PosSize): ...

class ColorWell(VanillaBaseObject):
    def __init__(self, posSize: PosSize, color: Any | None = None, callback: Callable[..., Any] | None = None): ...
    def get(self) -> Any: ...  # Returns an NSColor object
    def set(self, color: Any) -> None: ...

class ImageView(VanillaBaseObject):
    def __init__(self, posSize: PosSize, horizontalAlignment: str = "center", verticalAlignment: str = "center", scale: str = "proportional", imageObject: Any | None = None): ...
    def setImage(self, imageObject: Any | None = None, imagePath: str | None = None, imageNamed: str | None = None) -> None: ...
    def getImage(self) -> Any: ...

class LevelIndicator(VanillaBaseObject):
    def __init__(self, posSize: PosSize, minValue: int = 0, maxValue: int = 100, value: int = 0, warningValue: int | None = None, criticalValue: int | None = None, style: str = "relevancy", sizeStyle: str = "regular"): ...
    def get(self) -> int: ...
    def set(self, value: int) -> None: ...

class SplitView(VanillaBaseObject):
    def __init__(self, posSize: PosSize, paneDescriptions: list[dict], isVertical: bool = True, dividerStyle: str = "thick"): ...
    def getPane(self, index: int) -> Any: ...

class Tabs(VanillaBaseObject):
    def __init__(self, posSize: PosSize, tabLabels: list[str], callback: Callable[..., Any] | None = None, sizeStyle: str = "regular"): ...
    def get(self) -> int: ...
    def __getitem__(self, idx: int) -> Any: ...
    def set(self, index: int) -> None: ...
    def getTabs(self) -> list[Any]: ...

class TextEditor(VanillaBaseObject):
    def __init__(self, posSize: PosSize, text: str = "", callback: Callable[..., Any] | None = None, readOnly: bool = False, checksSpelling: bool = False): ...

class CheckBoxListCell(VanillaBaseObject):
    ...
