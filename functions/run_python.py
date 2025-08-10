import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    actual_file_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(actual_file_path)
    abs_workdir = os.path.abspath(working_directory)
    if not abs_file_path.startswith(abs_workdir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if abs_file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        script = ["python3", abs_file_path]
        commands = script + args
      
        result = subprocess.run(commands, capture_output=True, text=True, timeout=30, cwd=abs_workdir)

        if result.returncode != 0:
            return f'Process exited with code: {result.returncode} \nSTDERR: {result.stderr}'
        else:
            if result.stdout == "" and result.stderr == "":
                return f"No output produced"
            else:
                return f'STDOUT: {result.stdout} \nSTDERR: {result.stderr}'
    except Exception as e:
        return f"Error: executing Python file: {e}"
