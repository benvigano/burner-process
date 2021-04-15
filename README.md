# scriptifier
`scriptifier` is a Python package that allows to run a function in a separated script, seamlessly. 

## Install
PyPI: `pip install scriptifier`<br/>
<br/>
*Please notice that the path to the package installation folder should not contain whitespaces. While this would tipically not be the case it's important to point out that it will raise an exception.*

## Usage
```python
import os
from scriptifier import scriptifier

from my_package.my_package_module import func_1

scriptified_func_1 = scriptifier.run_as_script(func_1)
out = scriptified_func_1(in)
```

- Every argument must be pickleable<br/>
- Every return value must be either:
  - pickleable
  - a keras model
  - a list of keras models

## Features
- OS independent<br/>
- Doesn't rely on Multiprocessing package<br/>
- Doesn't rely on Queue for the returns (which would put a limit on the size)<br/>
- Supports functions from imported modules<br/>
- Supports overlapping/parallel calls<br/>

## Possible uses
- Memory leak managemenet (100% of the memory allocated within the function will be freed)<br/>
- Per-function resources usage monitoring<br/>
