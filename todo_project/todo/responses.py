
from todo.aliases import TodoListDict, DictStr
from typing import NamedTuple

class DBResponse(NamedTuple):
    tasks_list: TodoListDict
    error: int
    
class TodoResponse(NamedTuple):
    todo: DictStr
    error: int


