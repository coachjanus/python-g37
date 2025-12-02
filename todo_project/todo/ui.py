"""
User interface module for the todo application.
This module provides a console-oriented UI class (UI) that coordinates
user interaction, formatting and display of tasks, and calls into the
TaskList data layer. It uses 'rich' for table rendering and styling,
and 'typer' for colored error/success output and graceful exits.
Main components
---------------
UI (class)
    A high-level interactive controller that:
    - Loads the task database (via todo.database and todo.config) into a
      TaskList instance at initialization.
    - Presents prompts to the user for creating tasks, choosing category
      and priority, marking tasks done and removing tasks.
    - Renders task lists as a styled table using rich.Table and rich.Console.
    - Normalizes user input for category (Title case) and priority (UPPER).
    - Uses typer.secho for colored success/error messages.
Class attributes
    DONE (str) / PENDING (str)
        Unicode symbols used to indicate task completion status in the table.
    COLORS (dict)
        Mapping of canonical category names (Title case) to background
        colors used for category badges in the table.
    PRIORITY (dict)
        Mapping of priority keys (UPPER) to background colors used to
        display priority badges in prompts and the table.
    keys (list)
        Column spec keys used by make_header to convert UI.values to a
        list of column descriptor dicts.
    values (list of lists)
        Column definitions corresponding to keys. Each inner list must match
        the length of 'keys' and defines the column name, style, width,
        min_width and justification for the rich.Table.
Important instance methods and behavior
    __init__(self)
        - Calls get_tasks to load TaskList and sets up a rich.Console instance.
        - Raises typer.Exit(1) if configuration or database file is missing.
    get_tasks(self) -> TaskList or raises typer.Exit
        - Resolves the configured database path via todo.database and
          returns a TaskList instance pointed at the underlying DB.
        - If the config file or database file is missing, prints a colored
          error and raises typer.Exit(1).
    choice_category(self) -> str
        - Prompts the user to choose a category with a colored set of options
          and returns the canonical Title-cased category string.
    choice_priority(self) -> str
        - Prompts the user to choose a priority and returns the canonical
          UPPER-case priority string.
    add_todo(self)
        - Prompts for a task title, category and priority, normalizes inputs,
          constructs an appropriate Task object (Task, Task.important, or
          Task.critical), and calls TaskList.add_task.
        - Prints a colored success or error message based on the response.
        - Handles returned todo values that may be Task objects or dicts.
    get_all_task(self)
        - Retrieves all tasks via TaskList.get_tasks and displays them
          with show().
        - On failure prints an error and raises typer.Exit(1).
    set_done_task(self)
        - Prompts for a task ID (1-based), validates the ID against the
          current task list and updates the task's status to completed and
          completed_at timestamp.
        - Calls TaskList.update_task to persist changes; displays colored
          success or error messages.
        - If the input ID can't be parsed as int, prints an error and
          returns early (does not raise). If fetching tasks fails, prints
          an error and returns early.
    remove_task(self)
        - Prompts for a task ID and calls TaskList.remove_task.
        - Prints colored success or error messages. If parsing of the ID
          fails, prints an error and returns early.
    get_task_details(self) -> dict
        - Prompts the user for a title and category and returns a dict with
          keys 'title', 'category', and default 'status' == 'pending'.
        - (This helper is provided but add_todo uses a different interactive
          flow that also asks for priority.)
    get_task_id(self) -> int
        - Prompts for a task ID string, strips whitespace and converts to int.
        - Raises ValueError if conversion fails.
    make_header(self) -> list[dict]
        - Validates that each entry in UI.values has the same length as UI.keys,
          zips them into column descriptor dicts and returns the list for use
          when building the rich table.
        - Raises ValueError on mismatch.
    show(self, tasks)
        - Renders the provided iterable/list of task dicts as a rich.Table with
          configured headers and styles. Expects each task to be a mapping
          containing at least: 'title', 'category', 'status' and 'position'.
        - Format details:
            - Index (1-based) is rendered as ID column.
            - Category is shown as a colored badge using UI.COLORS.
            - Priority is derived from the task['position'] index into
              UI.PRIORITY.keys().
            - Status uses DONE/PENDING symbols based on integer status.
        - Uses self.console.print to output the table.
Exceptions, errors and side effects
    - Many UI methods call TaskList and interact with the filesystem/stateful
      database; side effects include writes via TaskList.update_task,
      TaskList.add_task and TaskList.remove_task.
    - get_tasks will raise typer.Exit(1) with an explanatory message if the
      configuration or database is missing.
    - get_task_id raises ValueError for non-integer input.
    - Several methods swallow input/parsing errors and display colored
      messages rather than propagating exceptions to the caller.
Notes and assumptions
    - The module expects other application modules to provide:
        - todo.task_list.TaskList: a class exposing get_tasks, add_task,
          update_task, remove_task methods and response objects with attributes
          like error, tasks_list, todo.
        - todo.model.Task and Status, with helper constructors Task.important
          and Task.critical, and a numeric status scheme where completed
          corresponds to 1.
        - todo.helpers.make_upper and make_title for input normalization.
        - todo.database and todo.config to locate the database file path.
        - SUCCESS and ERRORS constants for standardized response handling.
    - The UI class is designed for interactive console use and does not
      implement automated/non-interactive APIs. It relies on 'rich' and
      'typer' for user-facing formatting and coloring.
Examples
    Typical interactive actions performed by a UI instance (high level):
        ui = UI()               # loads TaskList and prepares console
        ui.add_todo()           # interactively add a task
        ui.get_all_task()       # display all tasks
        ui.set_done_task()      # mark a chosen task done
        ui.remove_task()        # remove a chosen task
"""
from todo import __app_name__
from todo.task_list import TaskList
from todo.model import Task, Status
from todo import SUCCESS
import datetime
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from todo.helpers import make_upper, make_title
from todo import database as db
from todo import config, ERRORS
import typer
from typing import Dict, List, Any, Union

class UI:

    DONE:str = chr(9989)
    PENDING:str = chr(10060)
    
    COLORS:Dict[str, Any] = {
        'Learn': 'yellow',
        'Work': 'red',
        'Sports': 'cyan',
        'Study': 'green'
    }
    
    PRIORITY:Dict[str, Any] = {
        'NEUTRAL': 'green',
        'IMPORTANT': 'blue',
        'CRITICAL': 'red'
    }
       
    keys:List[str] = ['name', 'style', 'width', 'min_width', 'justify']
    
    values:List[List[Union[str, None, int]]] = [
        ["ID", "dim", 6, None, "left"],
        ["Title", None, None, 20, "left"],
        ["Category", None, None, 12, "right"],
        ["Priority", None, None, 12, "right"],
        ["Status", None, None, 12, "right"],
    ]
    
    @staticmethod
    def join_category()->str:
        res = ""
        for k, v in UI.COLORS.items():
            res += f"[bold white on {v}] {k} [/]"
        return res
    
    @staticmethod
    def get_category_color(category:str)->str:
        key = make_title(category)
        return UI.COLORS.get(key, "white")
    
    
    def choice_category(self)-> str:
        # Return a canonical Title-cased category
        choice = Prompt.ask("[bold green on white] Choice some category: [/]" + UI.join_category(), default="Work")
        return make_title(choice)

    # UI methods
    @staticmethod
    def join_priority()->str:
        res = ""
        for k, v in UI.PRIORITY.items():
            res += f"[bold white on {v}] {k} [/]"
        return res
    
    @staticmethod
    def get_priority_color(priority)->str:
        key = make_upper(priority)
        return UI.PRIORITY.get(key, "green")
    

    def choice_priority(self):
        # Return a canonical UPPERCASE priority
        choice = Prompt.ask("[bold grey on white] Choice priority: [/]" + UI.join_priority(), default="NEUTRAL")
        return make_upper(choice)
    
    def __init__(self) -> None:
        
        self.task_list = self.get_tasks()
        self.console = Console()
        
    def get_tasks(self)-> TaskList|typer.Exit:
        if config.CONFIG_FILE_PATH.exists():
            db_path = db.get_database_path(config.CONFIG_FILE_PATH)
        else:
            typer.secho("Config file not found. Please run todo init", fg=typer.colors.RED)
            raise typer.Exit(1)
        if db_path.exists():
            return TaskList(db_path)
        else:
            typer.secho("Database not found. Please run todo init", fg=typer.colors.RED)
            raise typer.Exit(1)
    
    def help_me(self):
        print("""
        All that You can do:
            l: Show all tasks
            a: Add new task
            u: Set done existing task
            d: Delete existing task
            h: Print this help
            q: Exit
        """)
    
    def bye(self):
        print(f"Thanks for using {__app_name__.upper()}")
    
    def hi(self):
        print(f"Hi! It's me, {__app_name__.upper()}")
    
    def your_choice(self):
        return input(f"Please make Your choice (l|a|u|d|h|q) >>> ")
    
    def print_message(self, message: str) -> None:
        print(message)
        
    def print_error(self, error_message: str) -> None:
        print(f"Error: {error_message}")
    
    def print_success(self, success_message: str) -> None:
        print(f"Success: {success_message}")
    
    
    def get_task_details(self) -> Dict[str, Any]:
        title = input("Enter task title: ")
        category = input("Enter task category: ")
        return {
            'title': title,
            'category': category,
            'status': 'pending'
        }   
    def get_task_id(self) -> int:
        task_id = input("Enter task ID: ").strip()
        try:
            return int(task_id)
        except ValueError:
            raise ValueError("Task ID must be an integer")
    
    def add_todo(self):
        title = input("Enter task title: ").strip().lower()
        # Normalize category to Title case and priority to UPPER case
        category = make_title(self.choice_category())
        priority = make_upper(self.choice_priority())
        match priority:
            case 'IMPORTANT':
                task = Task.important(title, category)
            case 'CRITICAL':
                task = Task.critical(title, category)
            case _:
                task = Task(title, category)
        added_response = self.task_list.add_task(task)
        if added_response.error != SUCCESS:
            typer.secho(f"Failed to add task: {ERRORS.get(added_response.error, 'unknown error')}", fg=typer.colors.RED)
        else:
            # Handle both Task objects and dicts
            added = added_response.todo
            title = getattr(added, 'title', None) if hasattr(added, 'title') else added.get('title', '')
            typer.secho(f"Task added: {title}", fg=typer.colors.GREEN)
      
    def get_all_task(self):
        response = self.task_list.get_tasks()
        if response.error:
            typer.secho(f"Fetching tasks failed with {ERRORS[response.error]}", fg=typer.colors.RED)
            raise typer.Exit(1)
        else:
            if len(response.tasks_list) == 0:
                typer.secho(f"There are no tasks in the todo list", fg=typer.colors.RED)
                # raise typer.Exit(1)
            self.show(response.tasks_list)
        

    def set_done_task(self):
        try:
            idx = self.get_task_id()
        except ValueError as e:
            typer.secho(str(e), fg=typer.colors.RED)
            return

        response = self.task_list.get_tasks()
        if response.error:
            typer.secho(f"Fetching tasks failed with {ERRORS.get(response.error,'read error')}", fg=typer.colors.RED)
            return

        if idx < 1 or idx > len(response.tasks_list):
            typer.secho("Invalid task ID", fg=typer.colors.RED)
            return

        task = response.tasks_list[idx - 1]
        
        task['status'] = Status.COMPLETED
        task['completed_at'] = datetime.datetime.now().isoformat()

        update_response = self.task_list.update_task(idx, task)
        if update_response.error != SUCCESS:
            typer.secho(f"Failed to mark task done: {ERRORS.get(update_response.error,'write error')}", fg=typer.colors.RED)
        else:
            typer.secho(f"Task marked done: {task.get('title')}", fg=typer.colors.GREEN)
    def remove_task(self):
        try:
            idx = self.get_task_id()
        except ValueError as e:
            typer.secho(str(e), fg=typer.colors.RED)
            return

        response = self.task_list.remove_task(idx)
        if response.error != SUCCESS:
            typer.secho(f"Failed to remove task: {ERRORS.get(response.error,'error')}", fg=typer.colors.RED)
        else:
            typer.secho(f"Removed task: {response.todo.get('title') if response.todo else 'unknown'}", fg=typer.colors.GREEN)
    
    
    def make_header(self):
        headers = []
        keys = getattr(UI, "keys", [])
        for v in getattr(UI, "values", []):
            if len(v) != len(keys):
                raise ValueError("UI.values item length mismatch with UI.keys")
            headers.append(dict(zip(keys, v)))
        return headers
    
    def show(self, tasks):
        table = Table(show_header=True, header_style="bold blue")
        header = self.make_header()
        
        for item in header:
            table.add_column(item['name'], style=item['style'], width=item['width'], min_width=item['min_width'], justify=item['justify'])
            
                   
        for index, task in enumerate(tasks, start=1):
            c = UI.get_category_color(task['category'])
            status_symbol = UI.DONE if task['status'] == 1 else UI.PENDING
            table.add_row(
                str(index), 
                task['title'], 
                f"[bold {c}] {task['category']} [/]",
                
                str(list(UI.PRIORITY.keys())[task['position']]),
                status_symbol)
            
        self.console.print(table)