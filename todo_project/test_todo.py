import unittest
from todo.model import Status, Priority


class TestStatus(unittest.TestCase):
    def test_status_values(self):
        self.assertEqual(Status.OPEN, 0)
        self.assertEqual(Status.COMPLETED, 1)


class TestPriority(unittest.TestCase):
    def test_priority_values(self):
        self.assertEqual(Priority.LOW, 0)
        self.assertEqual(Priority.MEDIUM, 1)
        self.assertEqual(Priority.HIGH, 2)


if __name__ == "__main__":
    unittest.main()