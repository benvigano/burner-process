# scriptifier
`scriptifier` is a Python package that allows to run a function in a separated script, seamlessly. 

## Install
PyPI: `pip install scriptifier`<br/>

## Usage
```python
from scriptifier import scriptifier

def func_1(in):
    (...)
    return out

scriptified_func_1 = scriptifier.run_as_script(func_1)
out = scriptified_func_1(in)
```

- Each argument must be pickleable<br/>
- Each return value must be either:
  - pickleable
  - a keras model
  - a list of keras models

## Features
- Tested on Windows and Linux
- Supports overlapping/parallel calls<br/>
- Supports functions from imported packages and modules<br/>
- Doesn't rely on `multiprocessing` package<br/>
- Doesn't rely on a queue for the returns (which would add a limit the size)<br/>


## Possible uses
- Memory leaks managemenet (100% of the memory allocated within the function will be freed once it ends)<br/>
- Function specific resource usage monitoring<br/>
