from google import genai
from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    function_dict = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file}
    
    function_name=function_call_part.name

    if function_name not in function_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = function_call_part.args.copy()
    args['working_directory'] = './calculator'

    if function_call_part.name == 'get_file_content':
        args['file_path'] = args.pop('directory')
    elif function_call_part.name == 'run_python_file':
        args['file_path'] = args.pop('File Path')
        args['args'] = [args.pop('Arguments')]
    elif function_call_part.name == 'write_file':
        args['file_path'] = args.pop('directory')
    # continue for all functions...

    function_result = function_dict[function_call_part.name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


