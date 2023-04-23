import pickle
import os
import sys


io_directory = "io"


def _save_outputs(outputs, current_call_directory):

    pickle.dumps(outputs)
    with open(os.path.join(current_call_directory, "OUTPUTS.pickle"), 'wb') as f:
        pickle.dump(outputs, f)

# Change the working directory to the directory of the puppet script
puppet_script_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(puppet_script_path)

# Find the subdirectory with the highest identifier (the last that was called)
identifiers = []
for identifier in os.listdir(io_directory):
    identifiers.append(int(identifier))

current_call_directory = os.path.join(io_directory, str(max(list(identifiers))))

# Load the arguments and the function name then delete the file
args, kwargs, function_name, function_module_path, function_module_name, verbose = pickle.load(open(os.path.join(current_call_directory, "INPUT.pickle"), 'rb'))
os.remove(os.path.join(current_call_directory, "INPUT.pickle"))

# Import the namespace of the function's original module
sys.path.append(os.path.dirname(function_module_path))
function_module_name = function_module_name.split(".")[-1]

import importlib
module = importlib.import_module(function_module_name)

# Call the function and save the outputs
func = getattr(module, function_name)

if verbose:
    print(f"Running inside spawned process (pid: {os.getpid()}, parent pid: {os.getppid()})")

outputs = func(*args, **kwargs)

if verbose:
    print(f"Serializing outputs to {os.path.abspath(current_call_directory)}")
_save_outputs(outputs, current_call_directory)
