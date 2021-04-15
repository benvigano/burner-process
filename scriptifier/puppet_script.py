import pickle
import os


io_directory = "io"


def returns_saver(returns, current_call_directory):

    try:
        # Pickleable object
        pickle.dumps(returns)
        with open(os.path.join(current_call_directory, "RETURNS.pickle"), 'wb') as f:
            pickle.dump(returns, f)

    except TypeError:
        try:
            # Keras model
            returns.save(os.path.join(current_call_directory, "MODEL.h5"))

        except AttributeError:
            # List of Keras models
            for x in range(len(returns)):
                returns[x].save(os.path.join(current_call_directory, f"MODEL_{x + 1}_OF_{len(returns)}.h5"))
        except:
            raise Exception("Scriptifier Error: the object type is not supported.")
    except:
        raise Exception("Scriptifier Error: the object type is not supported.")


# Change the working directory to the directory of the puppet script
puppet_script_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(puppet_script_path)

# Find the subdirectory with the highest identifier (the last that was called)
identifiers = []
for identifier in os.listdir(io_directory):
    identifiers.append(int(identifier))

current_call_directory = os.path.join(io_directory, str(max(list(identifiers))))

# Load the arguments and the function name then delete the file
args, kwargs, function_name = pickle.load(open(os.path.join(current_call_directory, "INPUT.pickle"), 'rb'))
os.remove(os.path.join(current_call_directory, "INPUT.pickle"))

# Import the namespace of the function's original module, then delete the temporary file
import temporary_module
from temporary_module import *

# Call the function and save the returns
func = getattr(temporary_module, function_name)
returns = func(*args, **kwargs)

returns_saver(returns, current_call_directory)
