## Description

Module designed for loading and parsing Deal.II parameter files. The main class `prmdict` extends Python's native `dict` class to offer functionality specific to Deal.II parameter files.

## Features

- Load parameters from a file or string input
- Serialize data structure to Deal.II `.prm` file
- Find and set keys using hierarchical paths

## Installation

Place the module in the appropriate directory and import it using Python's `import` statement.

## Class Definitions

### prmdict

Inherits from `dict`. Responsible for parsing and storing Deal.II parameters.

#### Methods

- `__init__ (file=None, file_path=None)`: Initializes the class, accepting a string or a file path as arguments.
  
- `parse(file)`: Reads a `.prm` file or string and populates the dictionary.
  
- `dict2prm(indentation_level=0)`: Converts the dictionary into a `.prm` compatible list of strings.
  
- `save_prm(file_path)`: Saves the current state to a `.prm` file at the specified path.
  
- `find_key_path(key)`: Searches for a given key in the dictionary and returns its hierarchical path.

- `set(path, value)`: Sets a value using a hierarchical path.

## Example Usage

```python
prm = prmdict(file_path="path/to/file.prm")
prm.set("path/to/key", value)
prm.save_prm("path/to/new_file.prm")

current_value = prm.find_key_path("some_key")
```

## Current Limitations

- If more than one subsection has the same key, `find_key_path` will not behave as expected.
