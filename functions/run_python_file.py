import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs the python file from the working directory and print the output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Working directory path with path to the python file ",
                },
            },
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_dir = os.path.commonpath([abs_path, target_directory]) == abs_path
        if not os.path.isfile(target_directory):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
             return f'Error: "{file_path}" is not a Python file'
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        else:
            try:
                command = ["python", target_directory]
                if args:
                    command.extend(args)
                res = subprocess.run(command, cwd = os.path.dirname(target_directory), capture_output=True, text= True, timeout=30)
                if res.returncode != 0:
                   return f"Process exited with code {res.returncode}"
                if not res.stderr and not res.stdout:
                   return "No output produced"
                else:
                    output = ""
                    if res.stdout:
                       output = res.stdout
                       print("STDOUT: ",output)
                    if res.stderr:
                        print("STDERR: ", res.stderr)
                return output
            except Exception as e:
                    return f"Error: executing Python file: {e}"
    except Exception as e:
        return f"Error: {e}"