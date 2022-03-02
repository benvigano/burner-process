# scriptifier
`scriptifier` is a Python wrapper that generates a throw-away script and runs the wrapped function inside of it, seamlessly. 

## Install
PyPI: `pip install scriptifier`<br/>

## Potential uses
- Workaround to memory leaks (the memory allocated within the function will be completely freed once it ends)<br/>
- Function specific resource usage monitoring<br/>

## Usage
```python
from scriptifier import scriptifier

def func_1(in):
    (...)
    return out

scriptified_func_1 = scriptifier.run_as_script(func_1)
out = scriptified_func_1(in)
```

- Each argument must be **pickleable**<br/>
- Each return value must be either:
  - pickleable
  - a `tf.keras.Model` object
  - an iterable whose elements are `tf.keras.Model` objects

## Features
- Tested on Windows and Linux
- Supports overlapping/parallel calls<br/>
- Supports functions from imported packages and modules<br/>
- Doesn't rely on `multiprocessing` package<br/>
- Doesn't rely on a queue for the returns (which would add a limit the size)<br/>
