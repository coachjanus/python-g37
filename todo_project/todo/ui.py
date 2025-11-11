'''This module contains the UI class for the todo application.
'''
from todo.task_list import TaskList
from todo.model import Task
from rich.table import Table
from rich.console import Console

class UI:
    
    DONE = chr(9989)
    PENDING = chr(10060)
    
    COLORS = {
    'Learn': 'yellow',
    'Work': 'red',
    'Sports': 'cyan',
    'Study': 'green'
    }
    
    
    keys = ['name', 'style', 'width', 'min_width', 'justify']
    values = [
        ["Id", "dim", 6, None, "left"],
        ["Task", None, None, 20, "left"],
        ["Category", None, None, 12, "right"],
        ["Status", None, None, 12, "right"],
    ]
    def make_headers(self):
        headers = []
        for v in UI.values:
            d = dict(zip(UI.keys, v))
            headers.append(d)
        return headers
    #
    
    def __init__(self):
        self.task_list = TaskList()
    def add_todo(self):
        title = input("Enter task title: ").strip().lower()
        category = input("Enter task category: ").strip().upper()
        task = Task(title, category)
        self.task_list.add_task(task)
    
    def display_message(self, message: str) -> None:
        print(message)

    def get_user_input(self, prompt: str) -> str:
        return input(prompt)
    
    def show(self, tasks):
        table = Table(show_header=True, header_style="bold blue")
        header = self.make_header()
        for item in header:
            table.add_column(item['name'], style=item['style'], width=item['width'], min_width=item['min_width'], justify=item['justify'])
        # for idx, task in enumerate(tasks, start=1):
        #     status_symbol = self.DONE if task.status == 2 else self.PENDING
        #     table.add_row(
        #         str(idx),
        #         task.title,
        #         task.category,
        #         status_symbol
        #     )
        self.console.print(table)
