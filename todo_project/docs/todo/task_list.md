Module todo.task_list
=====================

Classes
-------

`TaskList(db_path)`
:   

    ### Methods

    `add_task(self, task) ‑> todo.responses.TodoResponse`
    :   Add a task to the DB. Returns (task, error_code).

    `clear_tasks(self) ‑> todo.responses.TodoResponse`
    :   Clear all tasks in the DB. Returns TodoResponse with empty list.

    `find_task_by_id(self, task_id) ‑> todo.responses.TodoResponse`
    :   Find a task by an 'id' field if present.
        
        Returns TodoResponse with task dict or None as data.

    `get_tasks(self) ‑> todo.responses.DBResponse`
    :   Return (tasks_list, error_code).

    `remove_task(self, index: int) ‑> todo.responses.TodoResponse`
    :   Remove task by 1-based index. Returns TodoResponse with removed task.
        
        Errors: DB_READ_ERROR on read failure, ID_ERROR on invalid index,
        DB_WRITE_ERROR on write failure, SUCCESS on success.

    `update_task(self, index: int, updated_task) ‑> todo.responses.TodoResponse`
    :   Replace task at 1-based index with updated_task.
        
        Returns TodoResponse with updated task.