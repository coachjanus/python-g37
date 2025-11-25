'''

'''
from todo.db_handler import DBHandler
from todo import DB_READ_ERROR, DB_WRITE_ERROR, SUCCESS, ID_ERROR
from todo.responses import TodoResponse, DBResponse


class TaskList:
   
    def __init__(self, db_path) -> None:
        self._db_handler = DBHandler(db_path)
    
    def add_task(self, task) -> TodoResponse:
        """Add a task to the DB. Returns (task, error_code)."""
        # tasks_list, read_error = self._db_handler.read_todos()
        reader = self._db_handler.read_todos()
        # if read_error == DB_READ_ERROR:
        #     return (task, read_error)
        if reader.error == DB_READ_ERROR:
            return TodoResponse(task, reader.error)
        
        # tasks_list.append(task)
        
        reader.tasks_list.append(task)
        
        writer =  self._db_handler.write_todos(reader.tasks_list)
        return TodoResponse(task, writer.error)
        # _, write_error = self._db_handler.write_todos(tasks_list)
        # return (task, write_error)

    
    def get_tasks(self) -> DBResponse:
        """Return (tasks_list, error_code)."""
        reader = self._db_handler.read_todos()
        return DBResponse(reader.tasks_list, reader.error)
        # tasks_list, read_error = self._db_handler.read_todos()
        # return (tasks_list, read_error)
    
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
    
    
    