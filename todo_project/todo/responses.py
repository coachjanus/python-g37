"""
Module: responses
Defines response data structures for the todo application.
Classes:
    DBResponse (NamedTuple):
        Represents the response from the database containing a list of tasks and an error code.
        Attributes:
            tasks_list (TodoListDict): The list of tasks retrieved from the database.
            error (int): Error code indicating the status of the database operation.
    TodoResponse (NamedTuple):
        Represents the response for a single todo item and an error code.
        Attributes:
            todo (DictStr): The todo item data.
            error (int): Error code indicating the status of the operation.
"""
from todo.aliases import TodoListDict, DictStr

from typing import NamedTuple

class DBResponse(NamedTuple):
    tasks_list: TodoListDict
    error: int
    
class TodoResponse(NamedTuple):
    todo: DictStr
    error: int


