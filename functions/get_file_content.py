import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    actual_file_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(actual_file_path)
    abs_workdir = os.path.abspath(working_directory)
    if not abs_file_path.startswith(abs_workdir):
        return f'Error: Cannot read "{abs_file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{abs_file_path}"'
    
    try:
        with open(abs_file_path, "r") as f:
            file = f.read()
            if len(file) > MAX_CHARS:
                file = file[:MAX_CHARS]
                file += (f'[...File "{abs_file_path}" truncated at {MAX_CHARS} characters]')
                #print(len(file))
    except FileNotFoundError:
        return "Error: The specified file was not found."
    except PermissionError:
        return "Error: You do not have permission to access this file."
    except IOError as e:
        return f"Error: An I/O error occurred: {e}"
    
    return file