"""_summary_

    Returns:
        _type_: _description_
"""

from pathlib import Path
import json
from todo import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS
from todo.model import TaskEncoder

class DBHandler:
    def __init__(self, db_path:Path):
        self._db_path = db_path
        
    def write_todos(self, todo_list):
        try:
            with self._db_path.open("w") as db:
                json.dump(todo_list, db, indent=4, cls=TaskEncoder)
            return (todo_list, SUCCESS)
        except OSError:
            return (todo_list, DB_WRITE_ERROR)
    
    def read_todos(self):
        try:
            with self._db_path.open("r") as db:
                try:
                    return (json.load(db), SUCCESS)
                except json.JSONDecodeError:
                    return ([], JSON_ERROR)
        except OSError:
            return ([], DB_READ_ERROR)
    