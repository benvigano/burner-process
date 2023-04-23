import os
import sys
import pickle
from functools import wraps
import shutil


io_directory = "io"


def _generate_higher_identifier(io_directory_path):
    used_identifiers = []
    if os.listdir(os.path.join(os.getcwd(), io_directory_path)):
        for folder_name in os.listdir(os.path.join(os.getcwd(), io_directory_path)):
            used_identifiers.append(int(folder_name))
        unused_identifier = max(used_identifiers) + 1
    else:
        unused_identifier = 1

    unused_identifier = str(unused_identifier)

    return unused_identifier


def _save_arguments(current_call_directory, function_name, function_module_path, function_module_name, verbose, *args, **kwargs):

    # Store the arguments and the function name in the current call directory
    try:
        pickle.dump([args, kwargs, function_name, function_module_path, function_module_name, verbose], open(os.path.join(current_call_directory, "INPUT.pickle"), 'wb'))

    except Exception:
        raise Exception("The arguments must be pickleable.")

    return current_call_directory


def _load_outputs(current_call_directory):

    # Load the outputs
    filename = os.listdir(current_call_directory)
    extension = os.path.splitext(filename[0])[1]

    outputs = pickle.load(open(os.path.join(current_call_directory, "OUTPUTS.pickle"), 'rb'))
    os.remove(os.path.join(current_call_directory, "OUTPUTS.pickle"))

    # Delete the directory
    os.rmdir(current_call_directory)

    return outputs


def processify(function, verbose=False):

    if verbose:
        print(f"Launching from main process (pid: {os.getpid()}, parent pid: {os.getppid()})")

    # Check if the io folder already exists
    if os.path.isdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), io_directory)):
        pass
    else:
        # If it wasn't created yet, create it
        os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), io_directory))

    @wraps(function)
    def wrapper(*args, **kwargs):

        # Get the fuction module's name and path
        function_module = sys.modules[function.__module__]
        function_module_path = os.path.abspath(function_module.__file__)
        function_module_name = function_module.__name__

        # Get the function's name
        function_name = function.__name__

        # Save the arguments and the file name in a dedicated directory
        io_directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), io_directory)

        # Create a new i/o subdirectory without overwriting any other subdirectories of previous calls that haven't ended yet
        unused_identifier = _generate_higher_identifier(io_directory_path)
        current_call_directory = os.path.join(io_directory_path, unused_identifier)
        os.makedirs(current_call_directory)

        try:
            if verbose:
                print(f"Serializing arguments to {current_call_directory}")

            current_call_directory = _save_arguments(current_call_directory, function_name, function_module_path, function_module_name, verbose, *args, **kwargs)

            # Run the worker (waits until it ends)
            _, path = os.path.splitdrive(os.path.dirname(os.path.abspath(__file__)))
            worker_path = os.path.join(path, "_worker.py")

            os.system(f'python "{worker_path}" 1')

            # Load the outputs
            outputs = _load_outputs(current_call_directory)

        except Exception:

            # In case of error, delete the current call directory
            shutil.rmtree(current_call_directory)
            raise

        return outputs
    return wrapper
