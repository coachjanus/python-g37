
import datetime

class Task:

    def __init__(self, title, category,
    added_at=None, completed_at=None,
    status=None, position=None):
        self.title = title
        self.category = category
        self.added_at = added_at if added_at is not None else datetime.datetime.now().isoformat()
        self.completed_at = completed_at if completed_at is not None else None
        self.status = status if status is not None else 0 # 0 = open, 1 = completed
        self.position = position if position is not None else None
    
    def __repr__(self) -> str:
        return f"({self.title}, {self.category}, {self.added_at}, {self.completed_at}, {self.status}, {self.position})"