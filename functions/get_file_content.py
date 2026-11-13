import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Print the content of the file in a specified directory relative to the working directory, truncating if the content exceeds 10,000 characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Working directory with path to the file",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_path = os.path.commonpath([abs_path, target_file]) == abs_path
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        if not valid_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        else:
            MAX_CHARS = 10_000
            with open(target_file, "r") as f:
                file_content_string = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
                if f.read(1):
                    file_content_string += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string

    except Exception as e:
        return f"Error: {e}"