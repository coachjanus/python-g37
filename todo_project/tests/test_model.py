import unittest
import json
from datetime import datetime
from todo.model import Task, Status, Priority, TaskEncoder

class TestStatus(unittest.TestCase):
    def test_status_values(self):
        self.assertEqual(Status.OPEN, 0)
        self.assertEqual(Status.COMPLETED, 1)


class TestPriority(unittest.TestCase):
    def test_priority_values(self):
        self.assertEqual(Priority.LOW, 0)
        self.assertEqual(Priority.MEDIUM, 1)
        self.assertEqual(Priority.HIGH, 2)


class TestTask(unittest.TestCase):
    def test_task_basic_creation(self):
        task = Task("Buy milk", "shopping")
        self.assertEqual(task.title, "Buy milk.")
        self.assertEqual(task.category, "shopping")
        self.assertEqual(task.status, Status.OPEN)
        self.assertEqual(task.position, Priority.LOW)
        self.assertIsNone(task.completed_at)

    def test_task_title_normalization(self):
        task = Task("Buy milk", "shopping")
        self.assertTrue(task.title.endswith("."))
        
        task2 = Task("Buy milk.", "shopping")
        self.assertEqual(task2.title, "Buy milk.")

    def test_task_category_stripping(self):
        task = Task("Buy milk", "  shopping  ")
        self.assertEqual(task.category, "shopping")

    def test_task_title_stripping(self):
        task = Task("  Buy milk  ", "shopping")
        self.assertEqual(task.title, "Buy milk.")

    def test_task_added_at_default(self):
        task = Task("Buy milk", "shopping")
        self.assertIsNotNone(task.added_at)
        datetime.fromisoformat(task.added_at)  # Should not raise

    def test_task_added_at_custom(self):
        custom_time = "2024-01-01T12:00:00"
        task = Task("Buy milk", "shopping", added_at=custom_time)
        self.assertEqual(task.added_at, custom_time)

    def test_task_completed_at(self):
        completed_time = "2024-01-02T12:00:00"
        task = Task("Buy milk", "shopping", completed_at=completed_time)
        self.assertEqual(task.completed_at, completed_time)

    def test_task_status_custom(self):
        task = Task("Buy milk", "shopping", status=Status.COMPLETED)
        self.assertEqual(task.status, Status.COMPLETED)

    def test_task_important_classmethod(self):
        task = Task.important("Buy milk", "shopping")
        self.assertEqual(task.position, Priority.MEDIUM)
        self.assertEqual(task.title, "Buy milk.")

    def test_task_critical_classmethod(self):
        task = Task.critical("Buy milk", "shopping")
        self.assertEqual(task.position, Priority.HIGH)
        self.assertEqual(task.title, "Buy milk.")

    def test_endswith_sentence(self):
        self.assertEqual(Task.endswith_sentence("test"), "test.")
        self.assertEqual(Task.endswith_sentence("test."), "test.")
        self.assertEqual(Task.endswith_sentence(""), "")

    def test_task_repr(self):
        task = Task("Buy milk", "shopping")
        repr_str = repr(task)
        self.assertIn("Buy milk.", repr_str)
        self.assertIn("shopping", repr_str)


class TestTaskEncoder(unittest.TestCase):
    def test_task_json_encoding(self):
        task = Task("Buy milk", "shopping")
        json_str = json.dumps(task, cls=TaskEncoder)
        decoded = json.loads(json_str)
        
        self.assertEqual(decoded["title"], "Buy milk.")
        self.assertEqual(decoded["category"], "shopping")
        self.assertIn("added_at", decoded)
        self.assertEqual(decoded["status"], Status.OPEN)
        self.assertEqual(decoded["position"], Priority.LOW)


if __name__ == "__main__":
    unittest.main()