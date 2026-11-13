import os


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write the content to the new file or replace the content from the existing file in the working directory with the file path. Only use this when the user explicitly requests file creation or modification.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Working directory path to the file",
                },
                "content":{
                     "type":"string",
                     "description":"content to be written in the file"
                }
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
        try:
            abs_path = os.path.abspath(working_directory)
            target_directory = os.path.normpath(os.path.join(abs_path, file_path))
            valid_target_dir = os.path.commonpath([abs_path, target_directory]) == abs_path
            if os.path.isdir(file_path):
                return f'Error: Cannot write to "{file_path}" as it is a directory'
            if not valid_target_dir:
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            else:
                try:
                    current_list = target_directory.split("/")
                    current_path = "/"
                    i = 0
                    while i< len(current_list)-1:
                        current_path = os.path.join(current_path, current_list[i])
                        if not os.path.isdir(current_path):
                            os.makedirs(current_path, exist_ok=True)
                        i+=1
                    with open(target_directory, "w") as f:
                         f.write(content)
                    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
                except Exception as e:
                     return f"Error:{e}"
        except Exception as e:
            return f"Error: {e}"