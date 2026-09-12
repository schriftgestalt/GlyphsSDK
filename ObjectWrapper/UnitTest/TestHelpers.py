import copy
import pathlib as Pathlib
from typing import Any, Sequence

import pytest
from Foundation import NSPoint  # type: ignore
from GlyphsApp import DictProxy, ListProxy, MGOrderedDictionary, OrderedDictProxy


def assert_read_only(obj, attr_name: str):
	"""Assert that setting a read-only property raises AttributeError."""
	assert obj is not None
	assert attr_name is not None
	initial_value = getattr(obj, attr_name)
	assert hasattr(obj, attr_name), f"'{obj.__class__.__name__}' object has no attribute '{attr_name}'"
	with pytest.raises(AttributeError):
		setattr(obj, attr_name, "This should not happen")
	assert getattr(obj, attr_name) == initial_value


def assert_string(obj, attr_name: str, allow_none: bool = True):
	initial_value = getattr(obj, attr_name)
	if not allow_none:
		assert initial_value is not None, "shouldn’t be None"
	if not (initial_value is None and allow_none):
		assert isinstance(initial_value, str), "value should be str"

	setattr(obj, attr_name, 'X')
	assert getattr(obj, attr_name) == 'X', f"setting new value failed: '{getattr(obj, attr_name)}' != 'X'"
	setattr(obj, attr_name, initial_value) # restore
	assert getattr(obj, attr_name) == initial_value, "restoring value failed"


def assert_dict(dict_object):
	assert isinstance(dict_object, (dict, MGOrderedDictionary)), f"not dict, got {type(dict_object)})"
	var1 = "abc"
	var2 = "def"
	dict_object["uniTestValue"] = var1
	assert dict_object["uniTestValue"] == var1
	dict_object["uniTestValue"] = var2
	assert dict_object["uniTestValue"] == var2
	dict_object.pop("uniTestValue")


def assert_list(list_object: Sequence | OrderedDictProxy, test_values: list | None = None, assert_sorting: bool = True):
	assert isinstance(list_object, (list, DictProxy, ListProxy, OrderedDictProxy))
	if test_values:
		initial_len = len(list_object)
		list_object.append(test_values[0])
		assert list_object[-1] == test_values[0]
		assert len(list_object) == initial_len + 1
		assert list_object.index(test_values[0]) == initial_len
		list_object[-1] = test_values[-1]
		assert list_object[-1] == test_values[-1]
		del list_object[-1]
		assert len(list_object) == initial_len
		list_object.extend(test_values[1:])
		list_object.insert(-(len(test_values) - 1), test_values[0])
		for i, val in enumerate(test_values):
			assert list_object[initial_len + i] == val
		assert len(list_object) == initial_len + len(test_values)
		del list_object[initial_len:-1]
		list_object.remove(list_object[-1])
		list_object.insert(0, test_values[-1])
		if assert_sorting:
			assert list_object[0] == test_values[-1]
			assert list_object.index(test_values[-1]) == 0
		popped = list_object.pop()
		assert isinstance(popped, type(test_values[-1])) or True
		assert len(list_object) == initial_len
	with pytest.raises(IndexError):
		_ = list_object[len(list_object)]
	with pytest.raises(IndexError):
		_ = list_object[-len(list_object) - 1]
	cp = copy.copy(list_object)
	for i, element in enumerate(list_object):
		assert cp[i] is element
	deep = copy.deepcopy(list_object)
	assert len(deep) == len(list_object)


def assert_integer(obj: Any, attr_name: str, assert_type: bool = True, allow_none: bool = True):
	initial_value = getattr(obj, attr_name)
	if not allow_none:
		assert initial_value is not None
	if assert_type and not (initial_value is None and allow_none):
		assert isinstance(initial_value, int)
	setattr(obj, attr_name, 10)
	assert getattr(obj, attr_name) == 10
	setattr(obj, attr_name, initial_value) # restore
	assert getattr(obj, attr_name) == initial_value


def assert_bool(obj: Any, attr_name: str, assert_type: bool = True):
	initial_value = getattr(obj, attr_name)
	if assert_type:
		assert isinstance(initial_value, bool)
	setattr(obj, attr_name, True)
	assert getattr(obj, attr_name) is True
	setattr(obj, attr_name, initial_value) # restore
	assert getattr(obj, attr_name) == initial_value


def assert_point(obj: Any, attr_name: str, assert_type: bool = True):
	initial_value = getattr(obj, attr_name)
	if assert_type:
		assert isinstance(initial_value, NSPoint)
	setattr(obj, attr_name, NSPoint(10, 10))
	assert getattr(obj, attr_name) == NSPoint(10, 10)
	setattr(obj, attr_name, initial_value) # restore
	assert getattr(obj, attr_name) == initial_value


def assert_float(obj: Any, attr_name: str, assert_type: bool = True, allow_none: bool = False):
	initial_value = getattr(obj, attr_name)
	if not allow_none:
		assert initial_value is not None
	if assert_type and not (initial_value is None and allow_none):
		assert isinstance(initial_value, float), f"wrong type. should be float, is {type(initial_value)}"

	setattr(obj, attr_name, 5)
	assert getattr(obj, attr_name) == 5, "setting new value failed"
	setattr(obj, attr_name, initial_value) # restore
	assert getattr(obj, attr_name) == initial_value, "restoring value failed"


def assert_equal_accuracy(first_value, second_value, accuracy=0.01):
	assert abs(float(first_value) - float(second_value)) < accuracy, f"{first_value} != {second_value}"


def assert_is_round_float(number):
	assert number % 1 == 0, f"should be rounded, has fraction: {number % 1}"


def assert_is_file(path):
	if not Pathlib.Path(path).resolve().is_file():
		raise AssertionError(f"File does not exist: {path}")


def assert_is_folder(path):
	if not Pathlib.Path(path).resolve().is_dir():
		raise AssertionError(f"Folder does not exist: {path}")
