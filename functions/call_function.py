from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    function_args["working_directory"] = "./calculator" #append the working directory to the arguments
    
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else :
        print(f" - Calling function: {function_name}")
    
    

    
    callable_functions={
        "get_file_content" : get_file_content, 
        "get_files_info" : get_files_info,
        "write_file" : write_file,
        "run_python_file" : run_python_file,
        }
    

    try:
        function_result = callable_functions[function_name](**function_args)
    except KeyError as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    except Exception as e:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f'Unable to call function, Error: {e}'},
            )
        ],
    )
        
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
        