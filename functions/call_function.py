from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
"""
Include function declaration inside of this list,
"""
available_functions = types.Tool(
    function_declarations = [
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ],
)

"""
Function definition for function that will handle the task of calling one of the 4 functions
and returning the result
"""

def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling the function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    """
    Function map to determine which function names are mapped to which actual function
    """

    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts =[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    """
    Make a shallow copy o function_call.args, an easy way of doing this is 
    using the dict() constructor
    """
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"
         
    #Turn the key-value  
    function_result = function_map[function_name](**args)
        
    """
    Return a types.Content object from function response part describing
    the result of the function call
    """
    result = types.Content(
        role="tool",
        parts = [
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
    return result
