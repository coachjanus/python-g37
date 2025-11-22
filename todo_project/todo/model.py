import datetime
from enum import IntEnum
import json

class Status(IntEnum):
    OPEN = 0
    COMPLETED = 1

class Priority(IntEnum):
    LOW = 0 # NEUTRAL = 0
    MEDIUM = 1 # IMPORTANT = 1
    HIGH = 2 # CRITICAL = 2
    
class TaskEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class Task:
    def __init__(self, title, category, 
                 added_at=None, completed_at=None,
                 status=None, position=Priority.LOW):
        self.title = self.endswith_sentence(str(title or "").strip())
        self.category = str(category or "").strip()
        self.added_at = added_at if added_at is not None else datetime.datetime.now().isoformat()
        self.completed_at = completed_at  # keep None or ISO string / datetime consistently
        
        self.status = status if status is not None else Status.OPEN
        self.position = position
        
    
    @classmethod
    def important(cls, title, category):
        return cls(title, category, position=Priority.MEDIUM)
    
    @classmethod
    def critical(cls, title, category):
        return cls(title, category, position=Priority.HIGH)
        
    @staticmethod
    def endswith_sentence(text: str) -> str:
        if not text:
            return text
        return text if text.endswith(".") else text + "."

    def __repr__(self) -> str:
        return f"({self.title}, {self.category}, {self.added_at}, {self.completed_at}, {self.status}, {self.position})"