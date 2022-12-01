from typing import TypeAlias, Union

_PlainJSON: TypeAlias = Union[
    None, bool, int, float, str, list["_PlainJSON"], dict[str, "_PlainJSON"]
]
JSON: TypeAlias = Union[_PlainJSON, list["JSON"], dict[str, "JSON"]]


def key_name(key: str) -> str:
    return key.replace("~1", "/").replace("~0", "~")


def is_valid_number(key: str) -> bool:
    return key == "0" or (not key.startswith("0") and key.isdigit())


def parse_pointer(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise ValueError("Pointer must start with '/'")

    return pointer[1:].split("/")


class JSONPointer:
    def __init__(self, object_: JSON) -> None:
        self._object = object_

    def get(self, pointer: str) -> JSON:
        return get(self._object, pointer)

    def set(self, pointer: str, value: JSON) -> None:
        set(self._object, pointer, value)


def get(object_: JSON, pointer: str) -> JSON:
    if pointer == "":
        return object_

    path = parse_pointer(pointer)

    for key in path:
        key = key_name(key)

        if isinstance(object_, list) and is_valid_number(key):
            key = int(key)

        object_ = object_[key]

    return object_


def set(object_: JSON, pointer: str, value: JSON) -> None:
    if pointer == "":
        raise ValueError("Set pointer must not be empty")

    path = parse_pointer(pointer)
    prev = None

    for i, key in enumerate(path):
        prev = object_

        key = key_name(key)

        if isinstance(object_, list):
            if is_valid_number(key):
                key = int(key)
            elif key == "-":
                break

        try:
            object_ = object_[key]
        except KeyError:
            break

    is_last_key = i == len(path) - 1

    if isinstance(prev, list):
        if key == "-":
            if not is_last_key:
                raise ValueError(f"'-' must be the last item in the pointer")

            prev.append(value)
        else:
            prev[key] = value

    else:  # always dict
        if not is_last_key:
            raise ValueError(f"Pointer to non-existing key must be the last item")

        prev[key] = value
