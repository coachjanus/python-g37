Module todo.ui
==============

Classes
-------

`UI()`
:   

    ### Class variables

    `COLORS: Dict[str, Any]`
    :   The type of the None singleton.

    `DONE: str`
    :   The type of the None singleton.

    `PENDING: str`
    :   The type of the None singleton.

    `PRIORITY: Dict[str, Any]`
    :   The type of the None singleton.

    `keys: List[str]`
    :   The type of the None singleton.

    `values: List[List[str | int | None]]`
    :   The type of the None singleton.

    ### Static methods

    `get_category_color(category: str) ‑> str`
    :

    `get_priority_color(priority) ‑> str`
    :

    `join_category() ‑> str`
    :

    `join_priority() ‑> str`
    :

    ### Methods

    `add_todo(self)`
    :

    `bye(self)`
    :

    `choice_category(self) ‑> str`
    :

    `choice_priority(self)`
    :

    `get_all_task(self)`
    :

    `get_task_details(self) ‑> Dict[str, Any]`
    :

    `get_task_id(self) ‑> int`
    :

    `get_tasks(self) ‑> todo.task_list.TaskList | click.exceptions.Exit`
    :

    `help_me(self)`
    :

    `hi(self)`
    :

    `make_header(self)`
    :

    `print_error(self, error_message: str) ‑> None`
    :

    `print_message(self, message: str) ‑> None`
    :

    `print_success(self, success_message: str) ‑> None`
    :

    `remove_task(self)`
    :

    `set_done_task(self)`
    :

    `show(self, tasks)`
    :

    `your_choice(self)`
    :