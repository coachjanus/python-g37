import unittest
from unittest.mock import MagicMock, patch
from todo.task_list import TaskList
from todo import DB_READ_ERROR, DB_WRITE_ERROR, SUCCESS, ID_ERROR
from todo.responses import TodoResponse, DBResponse

class TestTaskList(unittest.TestCase):
    def setUp(self):
        self.db_path = "fake_path"
        self.task_list = TaskList(self.db_path)
        self.mock_db_handler = patch('todo.task_list.DBHandler').start()
        self.task_list._db_handler = self.mock_db_handler.return_value

    def tearDown(self):
        patch.stopall()

    def test_add_task_success(self):
        task = {"id": 1, "title": "Test"}
        mock_reader = MagicMock()
        mock_reader.error = SUCCESS
        mock_reader.tasks_list = []
        mock_writer = MagicMock()
        mock_writer.error = SUCCESS

        self.task_list._db_handler.read_todos.return_value = mock_reader
        self.task_list._db_handler.write_todos.return_value = mock_writer

        response = self.task_list.add_task(task)
        self.assertEqual(response.data, task)
        self.assertEqual(response.error, SUCCESS)
        self.task_list._db_handler.write_todos.assert_called_with([task])

    def test_add_task_db_read_error(self):
        task = {"id": 1}
        mock_reader = MagicMock()
        mock_reader.error = DB_READ_ERROR
        self.task_list._db_handler.read_todos.return_value = mock_reader

        response = self.task_list.add_task(task)
        self.assertEqual(response.data, task)
        self.assertEqual(response.error, DB_READ_ERROR)

    def test_get_tasks(self):
        mock_reader = MagicMock()
        mock_reader.error = SUCCESS
        mock_reader.tasks_list = [{"id": 1}]
        self.task_list._db_handler.read_todos.return_value = mock_reader

        response = self.task_list.get_tasks()
        self.assertEqual(response.data, [{"id": 1}])
        self.assertEqual(response.error, SUCCESS)

    def test_clear_tasks(self):
        mock_writer = MagicMock()
        mock_writer.error = SUCCESS
        self.task_list._db_handler.write_todos.return_value = mock_writer

        response = self.task_list.clear_tasks()
        self.assertEqual(response.data, [])
        self.assertEqual(response.error, SUCCESS)
        self.task_list._db_handler.write_todos.assert_called_with([])

    def test_remove_task_success(self):
        mock_reader = MagicMock()
        mock_reader.error = SUCCESS
        mock_reader.tasks_list = [{"id": 1}, {"id": 2}]
        mock_writer = MagicMock()
        mock_writer.error = SUCCESS

        self.task_list._db_handler.read_todos.return_value = mock_reader
        self.task_list._db_handler.write_todos.return_value = mock_writer

        response = self.task_list.remove_task(2)
        self.assertEqual(response.data, {"id": 2})
        self.assertEqual(response.error, SUCCESS)
        self.task_list._db_handler.write_todos.assert_called_with([{"id": 1}])

    def test_remove_task_db_read_error(self):
        mock_reader = MagicMock()
        mock_reader.error = DB_READ_ERROR
        self.task_list._db_handler.read_todos.return_value = mock_reader

        response = self.task_list.remove_task(1)
        self.assertIsNone(response.data)
        self.assertEqual(response.error, DB_READ_ERROR)

    def test_remove_task_id_error(self):
        mock_reader = MagicMock()
        mock_reader.error = SUCCESS
        mock_reader.tasks_list = [{"id": 1}]
        self.task_list._db_handler.read_todos.return_value = mock_reader

        response = self.task_list.remove_task(0)
        self.assertIsNone(response.data)
        self.assertEqual(response.error, ID_ERROR)

        response = self.task_list.remove_task(2)
        self.assertIsNone(response.data)
        self.assertEqual(response.error, ID_ERROR)

    def test_find_task_by_id_found(self):
        mock_reader = MagicMock()
        mock_reader.error = SUCCESS
        mock_reader.tasks_list = [{"id": 1}, {"id": 2}]
        self.task_list._db_handler.read_todos.return_value = mock_reader

        response = self.task_list.find_task_by_id(2)
        self.assertEqual(response.data, {"id": 2})
        self.assertEqual(response.error, SUCCESS)

    def test_find_task_by_id_not_found(self):
        mock_reader = MagicMock()
        mock_reader.error = SUCCESS
        mock_reader.tasks_list = [{"id": 1}]
        self.task_list._db_handler.read_todos.return_value = mock_reader

        response = self.task_list.find_task_by_id(99)
        self.assertIsNone(response.data)
        self.assertEqual(response.error, SUCCESS)

    def test_find_task_by_id_db_read_error(self):
        mock_reader = MagicMock()
        mock_reader.error = DB_READ_ERROR
        self.task_list._db_handler.read_todos.return_value = mock_reader

        response = self.task_list.find_task_by_id(1)
        self.assertIsNone(response.data)
        self.assertEqual(response.error, DB_READ_ERROR)

    def test_update_task_success(self):
        mock_reader = MagicMock()
        mock_reader.error = SUCCESS
        mock_reader.tasks_list = [{"id": 1}, {"id": 2}]
        mock_writer = MagicMock()
        mock_writer.error = SUCCESS

        self.task_list._db_handler.read_todos.return_value = mock_reader
        self.task_list._db_handler.write_todos.return_value = mock_writer

        updated_task = {"id": 2, "title": "Updated"}
        response = self.task_list.update_task(2, updated_task)
        self.assertEqual(response.data, updated_task)
        self.assertEqual(response.error, SUCCESS)
        self.task_list._db_handler.write_todos.assert_called_with([{"id": 1}, updated_task])

    def test_update_task_db_read_error(self):
        mock_reader = MagicMock()
        mock_reader.error = DB_READ_ERROR
        self.task_list._db_handler.read_todos.return_value = mock_reader

        response = self.task_list.update_task(1, {"id": 1})
        self.assertIsNone(response.data)
        self.assertEqual(response.error, DB_READ_ERROR)

    def test_update_task_id_error(self):
        mock_reader = MagicMock()
        mock_reader.error = SUCCESS
        mock_reader.tasks_list = [{"id": 1}]
        self.task_list._db_handler.read_todos.return_value = mock_reader

        response = self.task_list.update_task(0, {"id": 1})
        self.assertIsNone(response.data)
        self.assertEqual(response.error, ID_ERROR)

        response = self.task_list.update_task(2, {"id": 2})
        self.assertIsNone(response.data)
        self.assertEqual(response.error, ID_ERROR)

if __name__ == "__main__":
    unittest.main()