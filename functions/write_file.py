import os

def write_file(working_directory, file_path, content):
    actual_file_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(actual_file_path)
    abs_workdir = os.path.abspath(working_directory)
    if not abs_file_path.startswith(abs_workdir):
        return f'Error: Cannot read "{abs_file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        try:
            os.makedirs(abs_file_path, exist_ok=True)
        except OSError as e:
            return f'Error: creating directory "{abs_file_path}": {e}'
    try:
        # Attempt to open the file and overwrite with content
        with open(abs_file_path, "w") as file:
            file.write(content)
            
    except FileNotFoundError:
        # Handle the specific case where the file does not exist
        print("Error: The specified file was not found.")
    except IOError as e:
        # Handle general I/O errors that might occur during file operations
        print(f"Error: An I/O error occurred: {e}")
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"An unexpected error occurred: {e}")
    finally:
        # This block will always execute, regardless of whether an exception occurred
         return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'