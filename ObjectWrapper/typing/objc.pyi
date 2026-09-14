
from typing import Any, Callable, Optional, ParamSpec, Tuple, TypeVar

from AppKit import NSBundle, NSObject

def super(super_class: Any, obj: Any) -> NSObject: ...

P = ParamSpec("P")
R = TypeVar("R")

def typedSelector(signature: bytes) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

__version__: str

pyobjc_unicode = str

class selector:
	"""
	Stub for PyObjC's objc.selector factory.
	"""
	def __init__(
		self,
		func: Callable[..., Any],
		selector: Optional[str] = None,
		signature: Optional[bytes] = None,
		isClassMethod: bool = False,
	) -> None:
		...

def addConvenienceForClass(className: str, values: Tuple) -> None: ...

def protocolNamed(name: str) -> Any: ...

def lookUpClass(name: str) -> Any: ...

def createStructType(name: str, typestr: bytes, fieldnames: list[str], doc: str, pack: int | None = ...) -> Any: ...
nil: Any

F = TypeVar("F", bound=Callable[..., Any])

def python_method(func: F) -> F: ...

def IBOutlet() -> Any: ...

F = TypeVar("F", bound=Callable[..., Any])

def IBAction(func: F) -> F: ...

def signature(byte) -> Any: ...

def loadBundleFunctions(bundle: NSBundle, module_globals: dict, functionInfo: list, skip_undefined: bool | None = False) -> None: ...
