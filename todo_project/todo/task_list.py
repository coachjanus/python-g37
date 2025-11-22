'''

'''
from todo.db_handler import DBHandler
from todo import DB_READ_ERROR, DB_WRITE_ERROR, SUCCESS, ID_ERROR

class TaskList:
    # def __init__(self)  -> None:
    #     self.task_list = []
        
    def __init__(self, db_path) -> None:
        self._db_handler = DBHandler(db_path)
    
    def add_task(self, task):
        # self.task_list.append(task)
        tasks_list, read_error = self._db_handler.read_todos()
        if read_error == DB_READ_ERROR:
            return (task, read_error)
        
        # count = len(tasks_list)
        # task._position = count if count else 0
        
        tasks_list.append(task)

        _, write_error = self._db_handler.write_todos(tasks_list)
        return (task, write_error)
        
    
    def get_tasks(self):
        """Return (tasks_list, error_code)."""
        tasks_list, read_error = self._db_handler.read_todos()
        return (tasks_list, read_error)
    
    def clear_tasks(self):
        """Clear all tasks in the DB. Returns ([], error_code)."""
        _, write_error = self._db_handler.write_todos([])
        return ([], write_error)

    def remove_task(self, index: int):
        """Remove task by 1-based index. Returns (removed_task, error_code).

        Errors: DB_READ_ERROR on read failure, ID_ERROR on invalid index,
        DB_WRITE_ERROR on write failure, SUCCESS on success.
        """
        tasks_list, read_error = self._db_handler.read_todos()
        if read_error == DB_READ_ERROR:
            return (None, DB_READ_ERROR)

        if index < 1 or index > len(tasks_list):
            return (None, ID_ERROR)

        removed = tasks_list.pop(index - 1)
        _, write_error = self._db_handler.write_todos(tasks_list)
        return (removed, write_error)

    def find_task_by_id(self, task_id) -> dict | None:
        """Find a task by an 'id' field if present; returns dict or None."""
        tasks_list, read_error = self._db_handler.read_todos()
        if read_error == DB_READ_ERROR:
            return None
        for task in tasks_list:
            if isinstance(task, dict) and task.get('id') == task_id:
                return task
        return None

    def update_task(self, index: int, updated_task):
        """Replace task at 1-based index with updated_task.

        Returns (updated_task, error_code).
        """
        tasks_list, read_error = self._db_handler.read_todos()
        if read_error == DB_READ_ERROR:
            return (None, DB_READ_ERROR)

        if index < 1 or index > len(tasks_list):
            return (None, ID_ERROR)

        tasks_list[index - 1] = updated_task
        _, write_error = self._db_handler.write_todos(tasks_list)
        return (updated_task, write_error)
    
    
    