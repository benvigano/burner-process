# Burner Process
Burner Process is a wrapper that runs a function inside a newly spawned independent process that is  **not** child to the main process, handling the function's arguments and returns (via `pickle`) as well as all its dependencies.

Other solutions (such as [this one](https://gist.github.com/schlamar/2311116)) rely on `subprocess` and thus spawn a process that is child to the main process, sharing memory and resources with it. Burner Process comes in handy when you need to run a function in an isolated environment, as a 'hard' workaround to memory leaks or inside parallel sub-processes, to monitor a specific worker's resources usage. 

### Limitations
- The function has to be defined in a module different from the main, and the functions's module must not include importing `burner_process` (see example below), which would cause circular imports.
- Both arguments and returns must be  **pickleable**<br/>

### Features
- Supporting overlapping/parallel calls<br/>
- Not relying on `subprocess` nor `multiprocessing`<br/>
- Not relying on a queue for the returns<br/>
- Tested on Windows and Linux

## Usage
### Installation
`pip install burner-process`<br/>

### Example
`my_module.py`
```python
def my_function(x):
    return x * 2
```

`my_script.py`
```python
from burner_process import processify
from my_module import my_function

my_function_p = processify(my_function)
my_function_p(5)
```
```
>> 10
```

### Verbose example
`my_module.py`
```python
def my_function(x):
    return x * 2
```

`my_script.py`
```python
from burner_process import processify
from my_module import my_function

my_function_p = processify(my_function, verbose=True)
my_function_p(5)
```
```
>> Launching from main process (pid: 20124, parent pid: 10568)
>> Serializing arguments to C:\...\io\3
>> Running inside spawned process (pid: 18976, parent pid: 14584)
>> Serializing outputs to C:\...\io\3
>> 10
```
