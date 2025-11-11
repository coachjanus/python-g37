class TaskList:
    def __init__(self) -> None:
        self.task_list = []
    def add_task(self, task) -> None:
        self.task_list.append(task)
    def get_tasks(self) -> list:
        return self.task_list