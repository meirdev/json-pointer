from json_pointer import JSONPointer, get, set

import pytest

DATA = {
    "foo": ["bar", "baz"],
    "": 0,
    "a/b": 1,
    "c%d": 2,
    "e^f": 3,
    "g|h": 4,
    "i\\j": 5,
    'k"l': 6,
    " ": 7,
    "m~n": 8,
}


@pytest.mark.parametrize(
    "pointer, expected",
    [
        ("", DATA),
        ("/foo", DATA["foo"]),
        ("/foo/0", DATA["foo"][0]),
        ("/", DATA[""]),
        ("/a~1b", DATA["a/b"]),
        ("/c%d", DATA["c%d"]),
        ("/e^f", DATA["e^f"]),
        ("/g|h", DATA["g|h"]),
        ("/i\\j", DATA["i\\j"]),
        ('/k"l', DATA['k"l']),
        ("/ ", DATA[" "]),
        ("/m~0n", DATA["m~n"]),
    ],
)
def test_get(pointer, expected):
    assert get(DATA, pointer) == expected


def test_get_error_invalid_pointer():
    with pytest.raises(Exception) as excinfo:
        get(["foo", "bar"], "d")

    assert str(excinfo.value) == "Pointer must start with '/'"


def test_get_error_invalid_list_index_zeros_leading():
    with pytest.raises(Exception) as excinfo:
        get(["foo", "bar"], "/01")

    assert "list indices must be integers or slices, not str" in str(excinfo.value)


def test_get_error_invalid_list_index():
    with pytest.raises(Exception) as excinfo:
        get(["foo", "bar"], "/d")

    assert "list indices must be integers or slices, not str" in str(excinfo.value)


def test_get_error_key_of_plain_object():
    with pytest.raises(Exception):
        get({"foo": "bar"}, "/foo/3")


def test_get_error_dict_key_not_found():
    with pytest.raises(Exception) as excinfo:
        get({"foo": "bar"}, "/bar")

    assert repr(excinfo.value) == "KeyError('bar')"


def test_get_error_list_index_not_found():
    with pytest.raises(Exception) as excinfo:
        get(["foo", "bar"], "/2")

    assert "list index out of range" in str(excinfo.value)


def test_set_list_index():
    data = ["bar", "baz"]

    set(data, "/0", "qux")

    assert data == ["qux", "baz"]


def test_set_dict_key():
    data = {"foo": "bar", "baz": "qux"}

    set(data, "/baz", "quux")

    assert data == {"foo": "bar", "baz": "quux"}


def test_set_dict_key_not_last_item():
    data = {
        "foo": {
            "bar": {
                "baz": "qux",
            },
        },
    }

    set(data, "/foo/bar", "qux")

    assert data == {
        "foo": {
            "bar": "qux",
        },
    }


def test_set_dict_new_key():
    data = {"foo": {"bar": "baz"}}

    set(data, "/foo/bar2", "qux")

    assert data == {
        "foo": {
            "bar": "baz",
            "bar2": "qux",
        },
    }


def test_set_error_dict_new_key_not_last_item():
    data = {
        "foo": {
            "bar": "baz",
        }
    }

    with pytest.raises(Exception) as excinfo:
        set(data, "/foo/bar2/4", "qux")

    assert str(excinfo.value) == "Pointer to non-existing key must be the last item"


def test_set_list_new_item():
    data = {"foo": ["bar", "baz"]}

    set(data, "/foo/-", "qux")

    assert data == {"foo": ["bar", "baz", "qux"]}


def test_set_error_root_pointer():
    data = {"foo": ["bar", "baz"]}

    with pytest.raises(Exception) as excinfo:
        set(data, "", "qux")

    assert str(excinfo.value) == "Set pointer must not be empty"


def test_set_error_invalid_path():
    data = {"foo": ["bar", "baz"]}

    with pytest.raises(Exception) as excinfo:
        set(data, "/foo/0/1", "qux")

    assert str(excinfo.value) == "string indices must be integers"


def test_set_error_hypen_not_last_item():
    data = {"foo": ["bar", "baz"]}

    with pytest.raises(Exception) as excinfo:
        set(data, "/foo/-/1", "qux")

    assert str(excinfo.value) == "'-' must be the last item in the pointer"


def test_json_pointer_get():
    data = {"foo": ["bar", "baz"]}

    json_pointer = JSONPointer(data)
    assert json_pointer.get("/foo/0") == "bar"


def test_json_pointer_set():
    data = {"foo": ["bar", "baz"]}

    json_pointer = JSONPointer(data)
    json_pointer.set("/foo/0", "qux")

    assert data == {"foo": ["qux", "baz"]}
