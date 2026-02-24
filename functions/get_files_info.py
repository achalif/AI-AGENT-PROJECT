from pathlib import Path
from google.genai import types
import os
def get_files_info(working_directory, directory="."):
    try:
        work_dir = os.path.abspath(working_directory)
        targ_dir = os.path.normpath(os.path.join(work_dir, directory))
        valid_targ_dir = os.path.commonpath([work_dir, targ_dir]) == work_dir
	
        if not valid_targ_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(targ_dir):
            return f'Error: "{directory}" is not a directory'
	
        targ_dir_obj = Path(targ_dir)
        results = []

        for item in targ_dir_obj.iterdir():
            name = item.name
            size = item.stat().st_size
            is_dir = item.is_dir()

            info_str = f"  - {name}: file_size={size} bytes, is_dir={is_dir}"
            results.append(info_str)
	
        return "\n".join(results)
    
    except Exception as e:
        return f"Error: {str(e)}"
"""
This is a 'declaration' or 'schema' for our get_files_info.py. This basically tells the LLM
how the function should be called.
"""

schema_get_files_info = types.FunctionDeclaration(
    name = "get_files_info",
    description = "Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "directory": types.Schema(
                type = types.Type.STRING,
                description = "Directory path to list files from, relative to the working directory (default is the working directory itself",   
            ),
        },
    ),
)
