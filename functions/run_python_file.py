import os
import subprocess
from pathlib import Path


def run_python_file(working_directory, file_path, args=[]):
    
    path = Path(os.path.join(working_directory, file_path)).resolve()
    working_path = Path(working_directory).resolve()
    if not path.is_relative_to(working_path): 
        return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.exists(path):
        return(f'Error: File "{file_path}" not found.')
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    command_list = ["python3", file_path]
    if args :
        for arg in args:
            command_list.append(arg)
    
    try:
        completed_process = subprocess.run(command_list, cwd=working_directory, capture_output=True, timeout=30)
        if completed_process.returncode != 0:    
            return (
            f'STDOUT: {completed_process.stdout.decode()}\n' 
            f'STDERR: {completed_process.stderr.decode()}\n'
            f'Process exited with code {completed_process.returncode}')
        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced"
        return (
            f'STDOUT: {completed_process.stdout.decode()}\n' 
            f'STDERR: {completed_process.stderr.decode()}'
                )
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    