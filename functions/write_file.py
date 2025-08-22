import os
from pathlib import Path 

def write_file(working_directory, file_path, content):
    
    path = Path(os.path.join(working_directory,file_path)).resolve()
    working_path = Path(working_directory).resolve()
    if not path.is_relative_to(working_path): 
        return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        except Exception as e:
            return f'Error creating directory "{os.path.dirname(path)}": {e}'
        
    
    try:
        with open(path, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing in file "{file_path}": {e}'

                

    