import datetime
"""
todo.model
==========
Module providing simple todo/task data structures and JSON encoding.
Contents
- Status (IntEnum): Task status values.
- Priority (IntEnum): Priority levels for tasks.
- TaskEncoder (json.JSONEncoder): Small custom encoder that serializes objects by returning their __dict__.
- Task: Lightweight task model with basic metadata and convenience constructors.
Status
------
An IntEnum describing the lifecycle state of a task:
- OPEN (0): Task is not completed.
- COMPLETED (1): Task has been completed.
Priority
--------
An IntEnum describing task importance or ordering:
- LOW (0): Default / neutral priority.
- MEDIUM (1): Important.
- HIGH (2): Critical.
TaskEncoder
-----------
A minimal JSON encoder that allows encoding Task instances (and other simple objects)
by returning the object's __dict__. Intended to be passed as the cls argument to
json.dumps(..., cls=TaskEncoder).
Task
----
Represents a todo item with the following attributes:
- title (str): Short title. Trailing whitespace is stripped and a sentence terminator
    ('.') is appended if missing.
- category (str): Category or tag for the task (whitespace trimmed).
- added_at (str): ISO-8601 timestamp when the task was created. Defaults to the
    current time via datetime.datetime.now().isoformat() when not provided.
- completed_at (Optional[str]): Optional ISO-8601 timestamp when the task was completed,
    or None if not completed.
- status (Status): Task status; defaults to Status.OPEN.
- position (Priority): Priority/position of the task; defaults to Priority.LOW.
Constructor
-----------
Task(title, category, added_at=None, completed_at=None, status=None, position=Priority.LOW)
Behavior:
- title and category are coerced to strings and trimmed.
- title is normalized to end with a period ('.') via the endswith_sentence helper.
- If added_at is omitted, it is set to the current time in ISO format.
- If status is omitted, it defaults to Status.OPEN.
- position accepts Priority values; convenience classmethods `important` and
    `critical` construct tasks with MEDIUM and HIGH priority respectively.
Class methods
-------------
- important(title, category) -> Task
    Create a Task with Priority.MEDIUM.
- critical(title, category) -> Task
    Create a Task with Priority.HIGH.
Static methods
--------------
- endswith_sentence(text: str) -> str
    Ensure a non-empty string ends with a '.'; returns the original text unchanged if
    it already ends with a period.
Representation
--------------
- __repr__ produces a compact tuple-like string including title, category, added_at,
    completed_at, status and position, suitable for debugging.
Examples
--------
Create a task and serialize to JSON:
        t = Task("Buy milk", "shopping")
        json_str = json.dumps(t, cls=TaskEncoder)
Notes
-----
- The module stores timestamps as ISO-formatted strings for simplicity; callers may
    prefer to convert them to datetime objects when necessary.
- TaskEncoder is intentionally simple and serializes all attributes present on
    the object via its __dict__. If more control is needed (e.g. to format enums or
    datetimes differently), provide a custom encoder or serialization helper.
"""
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