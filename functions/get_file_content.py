import os
from config import MAX_CHARS
from google.genai import types
def get_file_content(working_directory, file_path):
    try:
        working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir, file_path))  
        valid_target_dir = os.path.commonpath([working_dir, target_dir]) == working_dir

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        with open(target_dir, "r") as f:
            file_contents_str = f.read(MAX_CHARS)
        
            if f.read(1):
                file_contents_str += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_contents_str
    
    except Exception as e:
        return f"Error: {e}"

"""
This is a 'declaration' or 'schema' for our get_file_content.py. This basically
tells the LLM how the function should be called.
"""

schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description = "Reads and returns the text from a file, with truncation if its too long.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "working_directory": types.Schema(
                type = types.Type.STRING,
                description = "The root directory allowed for file access."
            ),
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "File path of the file in which content will be read from, relative to the working directory (default is the working directory itself.)"
            ),
        },
    ),
)
        
 
