import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abs_path, directory))
        valid_target_dir = os.path.commonpath([abs_path, target_directory]) == abs_path
        if not os.path.isdir(target_directory):
                    return f'Error: "{directory}" is not a directory'
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        else:
            try:
                contents = os.listdir(target_directory)
                res = ''
                for content in contents:
                    path = target_directory+"/"+content
                    res += "- "+ content + ": file_size="
                    res += str(os.path.getsize(path))+" bytes, is_dir="
                    res += str(os.path.isdir(path))+"\n"
            except Exception as e:
                 return f"Error:{e}"
            return res
            return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f"Error: {e}"