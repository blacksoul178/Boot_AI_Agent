import os
from pathlib import Path 
from config import max_file_length

def get_file_content(working_directory, file_path):

    path = Path(os.path.join(working_directory,file_path)).resolve()
    working_path = Path(working_directory).resolve()
    if not path.is_relative_to(working_path): 
        return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(path):
        return(f'Error:  File not found or is not a regular file: "{file_path}"')
    
    try:
        
        with open(path, "r") as file:
            file_content = file.read(max_file_length)
            
            if os.path.getsize(path) > max_file_length:
                file_content +=(
                    f'... File {file_path} truncated to {max_file_length} characters'
                )
            return file_content
            
            
            
            
            # this is the workaround i found to not  expand memory for more than 1 unused character and also not say the file is
            #truncated if it has exactly 10 000 characters
                        
            # truncated = ""
            # if len(file_content) > max_file_length:   
            #     file_content = file_content[:max_file_length]
            #     truncated = f""
            # return(file_content+truncated) 

    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
        
            
