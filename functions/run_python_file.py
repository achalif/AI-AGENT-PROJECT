import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    working_dir = os.path.abspath(working_directory)
    absolute_file_path = os.path.normpath(os.path.join(working_dir, file_path))
    is_valid_file = os.path.commonpath([working_dir, absolute_file_path]) == working_dir


    if not is_valid_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(absolute_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not absolute_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", absolute_file_path]
    
    if args:
        command.extend(args)

    try:
        result = subprocess.run(
            command,
            cwd = working_dir,
            capture_output = True,
            text = True,
            timeout = 30
        )
        
        output_parts = []

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        
        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")

        else:
            if result.stdout:
                output_parts.append(f"STDOUT: {result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR: {result.stderr}")
        
        output_str = "\n".join(output_parts)
        return output_str

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Allows the LLM to run a Python file in the working directory",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "working_directory": types.Schema(
                type = types.Type.STRING,
                description = "Working directory path in which LLM can run Python files"
            ),
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "Relative file path of Python file to be executed by LLM"    
            ),
            "args": types.Schema(
                type = types.Type.STRING,
                description = "Optional arguments for commands to run on Python files"
            ),
        },
    ),
)
