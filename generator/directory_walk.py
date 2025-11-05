from os import scandir
from os.path import isfile, join, exists
import pathlib

# A helper function to read only files from a directory:


def get_files(path):
    path = pathlib.Path(path)
    for entry in path.rglob('*'):
        # entry is a Path; use Path methods directly
        if entry.is_file():
            yield entry
# ...existing code...
# Another helper function to get only the subdirectories:


def get_directories(path):
    path = pathlib.Path(path)
    try:
        entries = path.iterdir()
    except (PermissionError, OSError):
        return
    for entry in entries:
        # use Path methods directly; yield Path objects for consistency
        if entry.is_dir():
            yield entry
# Now use these functions to recursively get all files within a directory and all its subdirectories (using generators):

def get_files_recursive(directory):
    yield from get_files(directory)
    for subdirectory in get_directories(directory):
        yield from get_files_recursive(subdirectory)


    
SKIP_DIRS = ["temp", "temporary_files", "logs"]

def get_all_items(root: pathlib.Path, exclude=SKIP_DIRS):
    for item in root.iterdir():
        if item.name in exclude:
            continue
        yield item
        if item.is_dir():
            yield from get_all_items(item)
            
# Приклад використання:
# large_dir = pathlib.Path("/home/janus/projects/python")
large_dir = pathlib.Path("/home/janus/projects/")
print(large_dir)
print(list(get_all_items(large_dir)))