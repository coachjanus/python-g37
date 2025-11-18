# from todo import __app_name__
# from todo.task_list import TaskList
# from todo.model import Task
# from rich.table import Table
# from rich.console import Console

# class UI:

#     DONE = chr(9989)
#     PENDING = chr(10060)
    
#     COLORS = {
#         'Learn': 'yellow',
#         'Work': 'red',
#         'Sports': 'cyan',
#         'Study': 'green'
#     }
#     HEADERS = ['ID', 'Title', 'Category', 'Status']
    
#     keys = ['name', 'style', 'width', 'min_width', 'justify']
    
#     values = [
#         ["ID", "dim", 6, None, "left"],
#         ["Title", None, None, 20, "left"],
#         ["Category", None, None, 12, "right"],
#         ["Status", None, None, 12, "right"],
#     ]
    
#     def __init__(self):
#         self.task_list = TaskList()
#         self.console = Console()
    
#     def help_me(self):
#         print("""
#         All that You can do:
#             l: Show all tasks
#             a: Add new task
#             u: Set done existing task
#             d: Delete existing task
#             h: Print this help
#             q: Exit
#         """)
    
#     def bye(self):
#         print(f"Thanks for using {__app_name__.upper()}")
    
#     def hi(self):
#         print(f"Hi! It's me, {__app_name__.upper()}")
    
#     def your_choice(self):
#         return input(f"Please make Your choice (l|a|u|d|h|q) >>> ")
    
#     def print_message(self, message: str) -> None:
#         print(message)
        
#     def print_error(self, error_message: str) -> None:
#         print(f"Error: {error_message}")
    
#     def print_success(self, success_message: str) -> None:
#         print(f"Success: {success_message}")
    
#     def print_tasks_table(self, tasks: list[dict]) -> None:
#         if not tasks:
#             print("No tasks to show.")
#             return
        
#         row_format = "{:<5} {:<20} {:<10} {:<10}"
#         print(row_format.format(*self.HEADERS))
#         print("-" * 50)
        
#         for task in tasks:
#             status_symbol = self.DONE if task.get('status') == 'done' else self.PENDING
#             print(row_format.format(
#                 task.get('id', ''),
#                 task.get('title', ''),
#                 task.get('category', ''),
#                 status_symbol
#             ))
#     def get_task_details(self) -> dict:
#         title = input("Enter task title: ")
#         category = input("Enter task category: ")
#         return {
#             'title': title,
#             'category': category,
#             'status': 'pending'
#         }   
#     def get_task_id(self) -> int:
#         task_id = input("Enter task ID: ")
#         return int(task_id)
    
#     def add_todo(self):
#         title = input("Enter task title: ").strip().lower()
#         category = input("Enter task category: ").strip().upper()
#         task = Task(title, category)
#         self.task_list.add_task(task)
      
#     def get_all_task(self):
#         tasks = self.task_list.get_tasks()
#         if len(tasks) > 0:
#             print(tasks)
#             self.show(tasks)
#         else:
#             self.print_error("No tasks found. Your tasl list is empty. Go back to menu and add new task.")

#     def set_done_task(self):
#         pass
#     def remove_task(self):
#         pass
    
#     def make_header(self):
#         headers = []
#         for v in UI.values:
#             d = dict(zip(UI.keys, v))
#             headers.append(d)
#         return headers
    
    
#     def show(self, tasks):
#         table = Table(show_header=True, header_style="bold blue")
#         header = self.make_header()
        
#         for item in header:
#             table.add_column(item['name'], style=item['style'], width=item['width'], min_width=item['min_width'], justify=item['justify'])
            
#         for idx, task in enumerate(tasks, start=1):
#             status_symbol = self.DONE if task.status == 2 else self.PENDING
#             table.add_row(
#                 str(idx),
#                 task.title,
#                 task.category,
#                 status_symbol
#             )   
            
#         self.console.print(table)
        
        
from todo import __app_name__
from todo.task_list import TaskList
from todo.model import Task
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from todo.helpers import make_upper, make_title

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
        self.task_list = TaskList()
        self.console = Console()
    
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
        self.task_list.add_task(task)
      
    def get_all_task(self):
        tasks = self.task_list.get_tasks()
        if len(tasks) > 0:
            print(tasks)
            self.show(tasks)
        else:
            self.print_error("No tasks found. Your task list is empty. Go back to menu and add new task.")

    
    
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
            c = UI.get_category_color(task.category)
            status_symbol = UI.DONE if task.status == 1 else UI.PENDING
            table.add_row(
                str(index), 
                task.title, 
                f"[bold {c}] {task.category} [/]",
                # position = list(UI.PRIORITY.keys())
                str(list(UI.PRIORITY.keys())[task.position]),
                status_symbol)
            
        self.console.print(table)