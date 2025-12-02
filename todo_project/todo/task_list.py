'''Module: todo.task_list
TaskList provides CRUD operations for managing tasks stored in a database.
Methods
-------
__init__(db_path)
    Initialize TaskList with the given database path.
add_task(task) -> TodoResponse
    Add a task to the database.
    Returns a TodoResponse containing the task and an error code.
get_tasks() -> DBResponse
    Retrieve all tasks from the database.
    Returns a DBResponse with the list of tasks and an error code.
clear_tasks() -> TodoResponse
    Remove all tasks from the database.
    Returns a TodoResponse with an empty list and an error code.
remove_task(index: int) -> TodoResponse
    Remove a task by its 1-based index.
    Returns a TodoResponse with the removed task and an error code.
    Error codes: DB_READ_ERROR, ID_ERROR, DB_WRITE_ERROR, SUCCESS.
find_task_by_id(task_id) -> TodoResponse
    Find a task by its 'id' field.
    Returns a TodoResponse with the found task (or None) and an error code.
update_task(index: int, updated_task) -> TodoResponse
    Update a task at the given 1-based index with a new value.
    Returns a TodoResponse with the updated task and an error code.
'''
from todo.db_handler import DBHandler

from todo import DB_READ_ERROR, DB_WRITE_ERROR, SUCCESS, ID_ERROR
from todo.responses import TodoResponse, DBResponse


class TaskList:
   
    def __init__(self, db_path) -> None:
        self._db_handler = DBHandler(db_path)
    
    def add_task(self, task) -> TodoResponse:
        """Add a task to the DB. Returns (task, error_code)."""
        
        reader = self._db_handler.read_todos()
        
        if reader.error == DB_READ_ERROR:
            return TodoResponse(task, reader.error)
        
               
        reader.tasks_list.append(task)
        
        writer =  self._db_handler.write_todos(reader.tasks_list)
        return TodoResponse(task, writer.error)
            
    def get_tasks(self) -> DBResponse:
        """Return (tasks_list, error_code)."""
        reader = self._db_handler.read_todos()
        return DBResponse(reader.tasks_list, reader.error)
        
    
    def clear_tasks(self) -> TodoResponse:
        """Clear all tasks in the DB. Returns TodoResponse with empty list."""
        writer = self._db_handler.write_todos([])
        return TodoResponse([], writer.error)

    def remove_task(self, index: int) -> TodoResponse:
        """Remove task by 1-based index. Returns TodoResponse with removed task.

        Errors: DB_READ_ERROR on read failure, ID_ERROR on invalid index,
        DB_WRITE_ERROR on write failure, SUCCESS on success.
        """
        reader = self._db_handler.read_todos()
        if reader.error == DB_READ_ERROR:
            return TodoResponse(None, DB_READ_ERROR)

        if index < 1 or index > len(reader.tasks_list):
            return TodoResponse(None, ID_ERROR)

        removed = reader.tasks_list.pop(index - 1)
        writer = self._db_handler.write_todos(reader.tasks_list)
        return TodoResponse(removed, writer.error)

    def find_task_by_id(self, task_id) -> TodoResponse:
        """Find a task by an 'id' field if present.
        
        Returns TodoResponse with task dict or None as data.
        """
        reader = self._db_handler.read_todos()
        if reader.error == DB_READ_ERROR:
            return TodoResponse(None, DB_READ_ERROR)
        for task in reader.tasks_list:
            if isinstance(task, dict) and task.get('id') == task_id:
                return TodoResponse(task, SUCCESS)
        return TodoResponse(None, SUCCESS)  # not found, but no error

    def update_task(self, index: int, updated_task) -> TodoResponse:
        """Replace task at 1-based index with updated_task.

        Returns TodoResponse with updated task.
        """
        reader = self._db_handler.read_todos()
        if reader.error == DB_READ_ERROR:
            return TodoResponse(None, DB_READ_ERROR)

        if index < 1 or index > len(reader.tasks_list):
            return TodoResponse(None, ID_ERROR)

        reader.tasks_list[index - 1] = updated_task
        writer = self._db_handler.write_todos(reader.tasks_list)
        return TodoResponse(updated_task, writer.error)
    
    
    