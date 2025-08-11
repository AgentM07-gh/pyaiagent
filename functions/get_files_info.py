import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(full_path)
    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    ret_string = ""
    try:
        dir_contents = os.listdir(full_path)
    except FileNotFoundError:
        print(f"Error: The directory '{full_path}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied to access '{full_path}'.")
    except NotADirectoryError:
        print(f"Error: '{full_path}' is not a directory.")
    except OSError as e:
        print(f"An unexpected OS error occurred: {e}")
    if dir_contents == []:
        return f'"{full_path}" is empty'
    else:
        for content in dir_contents:
            try:
               size = os.path.getsize(os.path.join(full_path,content))
            except FileNotFoundError:
                print(f"Error: File '{os.path.join(full_path,content)}' not found.")
            except OSError as e:
                print(f"Error accessing file '{os.path.join(full_path,content)}': {e}")
            
            if os.path.exists(os.path.join(full_path,content)):
               is_dir = os.path.isdir(os.path.join(full_path,content))
            else:
               return f'Error: {os.path.join(full_path,content)} no longer exists'
            
            ret_string += f' - {content}: file_size={size}, is_dir={is_dir} \n'
    return ret_string

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

