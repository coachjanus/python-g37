'''

'''

class TaskList:
    def __init__(self)  -> None:
        self.task_list = []
    
    def add_task(self, task) -> None:
        self.task_list.append(task)
    def get_tasks(self) -> list:
        return self.task_list 
    def clear_tasks(self) -> None:
        self.task_list.clear()
    def remove_task(self, task) -> None:
        self.task_list.remove(task)
        
    def find_task_by_id(self, task_id) -> dict | None:
        for task in self.task_list:
            if task.get('id') == task_id:
                return task
        return None 
    def update_task(self, task_id, updated_task) -> bool:
        for index, task in enumerate(self.task_list):
            if task.get('id') == task_id:
                self.task_list[index] = updated_task
                return True
        return False    
    
    
    