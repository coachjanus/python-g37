"""Database handler for managing todo list persistence.
This class provides methods to read from and write to a JSON database file,
handling various error cases such as file I/O errors and JSON parsing errors.
Attributes:
    _db_path (Path): The file path to the JSON database file.
Methods:
    write_todos(todo_list): Writes a todo list to the database file.
    read_todos(): Reads a todo list from the database file.

    Returns:
        _type_: _description_
"""

from pathlib import Path
import json
from todo import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS
from todo.model import TaskEncoder
from todo.responses import DBResponse
from todo.aliases import TodoListDict

class DBHandler:
    def __init__(self, db_path:Path) -> None:
        self._db_path = db_path
        
    def write_todos(self, todo_list: TodoListDict) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(todo_list, db, indent=4, cls=TaskEncoder)
            return DBResponse(todo_list, SUCCESS)
        except OSError:
            return DBResponse(todo_list, DB_WRITE_ERROR)
    
    def read_todos(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:
                    return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)
    