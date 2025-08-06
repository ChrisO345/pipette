# pipette

`pipette` is a lightweight, expressive Python library designed to enable clean, functional-style data processing pipelines with intuitive syntax and powerful composition.

---

## Features

`pipette` is currently in early development, but it already includes:
- Elegant chaining of iterable transformations using pipe-style syntax.
- Core functional utilities like `select`, `where`, `reduce`, `sort_by`, and more.
- Simple and extensible design to grow with your needs.

---

## Installation

You can install the latest development version of `pipette` directly from GitHub using pip (or other Python package managers):

```bash
pip install git+https://github.com/chriso345/pipette
```

## Usage

`pipette` aims to make functional pipelines clear and concise.
```python
from pipette import where, select, into

data = [
    {"active": True, "value": 10},
    {"active": False, "value": 5},
    {"active": True, "value": 7},
]

result = (
    data
    | where(lambda x: x["active"])
    | select(lambda x: x["value"])
    | into(list)
)

print(result)  # Output: [10, 7]
```

Custom transformations can easily be added to extend functionality:
```python
from pipette import pipette

@pipette
def double(x):
    return builtins.map(lambda n: n * 2, x)

result = (
    [1, 2, 3, 4]
    | double
    | into(list)
)

print(result)  # Output: [2, 4, 6, 8]
```

More detailed usage examples and API docs will be added as development progresses.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
