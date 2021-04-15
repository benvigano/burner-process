import os
import sys
import pickle
from functools import wraps


io_directory = "io"


def file_copier(source, destination):
    try:
        o_binary = os.O_BINARY
    except Exception:
        o_binary = 0

    read_flags = os.O_RDONLY | o_binary
    write_flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | o_binary
    buffer_size = 128 * 1024

    try:
        fin = os.open(source, read_flags)
        stat = os.fstat(fin)
        fout = os.open(destination, write_flags, stat.st_mode)
        for x in iter(lambda: os.read(fin, buffer_size), b""):
            os.write(fout, x)

    finally:

        try:
            os.close(fin)
        except Exception:
            pass

        try:
            os.close(fout)
        except Exception:
            pass


def higher_identifier_generator(io_directory_path):
    used_identifiers = []
    if os.listdir(os.path.join(os.getcwd(), io_directory_path)):
        for folder_name in os.listdir(os.path.join(os.getcwd(), io_directory_path)):
            used_identifiers.append(int(folder_name))
        unused_identifier = max(used_identifiers) + 1
    else:
        unused_identifier = 1

    unused_identifier = str(unused_identifier)

    return unused_identifier


def arguments_saver(io_directory_path, function_name, local_namespace_only, *args, **kwargs):
    # Create a new io subdirectory without overwriting the other subdirectories of previous calls that haven't ended yet (if any)
    unused_identifier = higher_identifier_generator(io_directory_path)

    current_call_directory = os.path.join(io_directory_path, unused_identifier)
    os.makedirs(current_call_directory)

    # Store the arguments and the function name in the current call's directory
    try:
        pickle.dump([args, kwargs, function_name, local_namespace_only], open(os.path.join(current_call_directory, "INPUT.pickle"), 'wb'))

    except Exception:
        raise Exception("Scriptifier Error: The arguments must be pickleable.")

    return current_call_directory


def returns_loader(current_call_directory, tf_exclude_gpu):
    # Load the returns file based on the extension
    if len(os.listdir(current_call_directory)) > 1:

        if tf_exclude_gpu:
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        else:
            pass

        from tensorflow import keras
        returns = []
        for model_file_name in os.listdir(current_call_directory):
            model = keras.models.load_model(os.path.join(current_call_directory, model_file_name), compile=False)
            returns.append(model)
            os.remove(os.path.join(current_call_directory, model_file_name))

    else:

        filename = os.listdir(current_call_directory)
        extension = os.path.splitext(filename[0])[1]

        if extension == ".pickle":
            returns = pickle.load(open(os.path.join(current_call_directory, "RETURNS.pickle"), 'rb'))
            os.remove(os.path.join(current_call_directory, "RETURNS.pickle"))

        elif extension == ".h5":
            from tensorflow import keras
            returns = keras.models.load_model(os.path.join(current_call_directory, "MODEL.h5"), compile=False)
            os.remove(os.path.join(current_call_directory, "MODEL.h5"))

    # Delete the directory
    os.rmdir(current_call_directory)

    return returns


def scriptify(function, tf_exclude_gpu=False, local_namespace_only=False):
    
    # Check if the io folder already exists
    if os.path.isdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), io_directory)):
        pass
    else:
        # If it wasn't created yet, create it
        os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), io_directory))


    @wraps(function)
    def wrapper(*args, **kwargs):
        
        # Temporarily copy the module of the function in the package folder
        if local_namespace_only is False:
            function_module = sys.modules[function.__module__]
            function_module_path = function_module.__file__
            final_module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temporary_module.py")
            file_copier(function_module_path, final_module_path)
        else:
            pass

        # Get the function name
        function_name = function.__name__

        # Save the arguments and the file name in a dedicated directory
        io_directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), io_directory)
        current_call_directory = arguments_saver(io_directory_path, function_name, local_namespace_only, *args, **kwargs)

        # Run the puppet scrit and wait until it ends
        _, path = os.path.splitdrive(os.path.dirname(os.path.abspath(__file__)))
        puppet_script_path = os.path.join(path, "puppet_script.py")
        
        # If the path contains whitespaces, raise an exception
        if ' ' in puppet_script_path:
            raise Exception("Scriptifier Error: The path to the package installation directory can not contain whitespaces. (path=" + str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + ")")
            
        os.system(f"python {puppet_script_path} 1")

        # Load the returns
        returns = returns_loader(current_call_directory, tf_exclude_gpu)

        return returns
    return wrapper
