# JSON Pointer

Implementation of [JSON Pointer](http://tools.ietf.org/html/rfc6901).

## Example

```python
import json_pointer

data = {
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

print(json_pointer.get(data, "/foo"))  # ['bar', 'baz']
print(json_pointer.get(data, "/foo/0"))  # "bar"
print(json_pointer.get(data, "/"))  # 0

json_pointer.set(data, "/foo/1", "replace")
print(json_pointer.get(data, "/foo/1"))  # replace
```
