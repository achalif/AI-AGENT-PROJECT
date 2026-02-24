import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir, file_path))
        valid_working_dir = os.path.commonpath([working_dir, target_dir]) == working_dir
 
        if not valid_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'    

        directory_path = os.path.dirname(target_dir)
        os.makedirs(directory_path, exist_ok=True)

        with open(target_dir, "w") as f:
            f.write(content)
            return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    except Exception as e:
        return f"Error: {e}"


"""
This is a 'declaration' or 'schema' for our write_file.py. It basically tells the LLM how the function
should be called.
"""

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Allows the LLM to write and overwrite files with limits",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "working_directory": types.Schema(
                type = types.Type.STRING,
                description = "Specifies the working directory that the LLM can access the Python file"
            ),
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "Specifies the relative file path that the LLM will use to execute the Python file"
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "Specifies the content that the LLM will use to write/overwrite a file"
            ),
        },
    ),
)
