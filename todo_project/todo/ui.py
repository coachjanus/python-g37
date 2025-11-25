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