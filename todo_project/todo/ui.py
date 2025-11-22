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

class UI:

    DONE = chr(9989)
    PENDING = chr(10060)
    
    COLORS = {
        'Learn': 'yellow',
        'Work': 'red',
        'Sports': 'cyan',
        'Study': 'green'
    }
    
    PRIORITY = {
        'NEUTRAL': 'green',
        'IMPORTANT': 'blue',
        'CRITICAL': 'red'
    }
       
    keys = ['name', 'style', 'width', 'min_width', 'justify']
    
    values = [
        ["ID", "dim", 6, None, "left"],
        ["Title", None, None, 20, "left"],
        ["Category", None, None, 12, "right"],
        ["Priority", None, None, 12, "right"],
        ["Status", None, None, 12, "right"],
    ]
    
    @staticmethod
    def join_category():
        res = ""
        for k, v in UI.COLORS.items():
            res += f"[bold white on {v}] {k} [/]"
        return res
    
    @staticmethod
    def get_category_color(category):
        key = make_title(category)
        return UI.COLORS.get(key, "white")
    
    
    def choose_category(self):
        return Prompt.ask("[bold green on white] Coose some category: [/]" + UI.join_category(), default="Work")

    # UI methods
    @staticmethod
    def join_priority():
        res = ""
        for k, v in UI.PRIORITY.items():
            res += f"[bold white on {v}] {k} [/]"
        return res
    
    @staticmethod
    def get_priority_color(priority):
        key = make_upper(priority)
        return UI.PRIORITY.get(key, "green")
    

    def choose_priority(self):
        
        return Prompt.ask("[bold grey on white] Coose priority: [/]" + UI.join_priority(), default="NEUTRAL")
    
    def __init__(self):
        
        self.task_list = self.get_tasks()
        self.console = Console()
        
    def get_tasks(self):
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
    
    
    def get_task_details(self) -> dict:
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
        category = make_upper(self.choose_category())
        priority = make_upper(self.choose_priority())
        match priority:
            case 'IMPORTANT':
                task = Task.important(title, category)
            case 'CRITICAL':
                task = Task.critical(title, category)
            case _:
                task = Task(title, category)
        added, write_error = self.task_list.add_task(task)
        if write_error != SUCCESS:
            typer.secho(f"Failed to add task: {ERRORS.get(write_error, 'unknown error')}", fg=typer.colors.RED)
        else:
            # Handle both Task objects and dicts
            title = getattr(added, 'title', None) if hasattr(added, 'title') else added.get('title', '')
            typer.secho(f"Task added: {title}", fg=typer.colors.GREEN)
      
    def get_all_task(self):
        tasks, error = self.task_list.get_tasks()
        if error:
            typer.secho(f"Fetching tasks failed with {ERRORS[error]}", fg=typer.colors.RED)
            raise typer.Exit(1)
        else:
            if len(tasks) == 0:
                typer.secho(f"There are no tasks in the todo list", fg=typer.colors.RED)
                # raise typer.Exit(1)
            self.show(tasks)
        

    def set_done_task(self):
        try:
            idx = self.get_task_id()
        except ValueError as e:
            typer.secho(str(e), fg=typer.colors.RED)
            return

        tasks, read_error = self.task_list.get_tasks()
        if read_error:
            typer.secho(f"Fetching tasks failed with {ERRORS.get(read_error,'read error')}", fg=typer.colors.RED)
            return

        if idx < 1 or idx > len(tasks):
            typer.secho("Invalid task ID", fg=typer.colors.RED)
            return

        task = tasks[idx - 1]
        
        task['status'] = Status.COMPLETED
        task['completed_at'] = datetime.datetime.now().isoformat()

        _, write_error = self.task_list.update_task(idx, task)
        if write_error != SUCCESS:
            typer.secho(f"Failed to mark task done: {ERRORS.get(write_error,'write error')}", fg=typer.colors.RED)
        else:
            typer.secho(f"Task marked done: {task.get('title')}", fg=typer.colors.GREEN)
    def remove_task(self):
        try:
            idx = self.get_task_id()
        except ValueError as e:
            typer.secho(str(e), fg=typer.colors.RED)
            return

        removed, err = self.task_list.remove_task(idx)
        if err != SUCCESS:
            typer.secho(f"Failed to remove task: {ERRORS.get(err,'error')}", fg=typer.colors.RED)
        else:
            typer.secho(f"Removed task: {removed.get('title')}", fg=typer.colors.GREEN)
    
    def make_header(self):
        headers = []
        for v in UI.values:
            d = dict(zip(UI.keys, v))
            headers.append(d)
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