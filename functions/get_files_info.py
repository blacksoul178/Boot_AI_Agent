import os
from pathlib import Path

def get_files_info(working_directory, directory="."):
    files_info = []
    path = Path(os.path.join(working_directory, directory)).resolve()
    working_path = Path(working_directory).resolve()
    if not path.is_relative_to(working_path): 
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(path):
        return(f'Error: "{directory}" is not a directory')

    try: 
        dir_list = os.listdir(path)
    except OSError as e:
        return(f"Error: Failed to list directory '{directory}'. Reason: {e}")
        
        
    for item in dir_list:
        
        try:
            item_size = os.path.getsize(os.path.join(path,item))
        except OSError as e:
            return(f"Error: Failed to retrieve item '{item}' size. Reason: {e}")
        try:
            item_is_dir = os.path.isdir(os.path.join(path,item))
        except OSError as e:
            return(f"Error: Failed to get is_dir for '{item}'. Reason: {e}")
        
        files_info.append(f"- {item}: file_size={item_size} bytes, is_dir={item_is_dir}\n")
        
    
    
    return("\n".join(files_info))

