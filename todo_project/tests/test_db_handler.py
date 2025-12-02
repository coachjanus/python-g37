import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from todo.db_handler import DBHandler
from todo import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS
from todo.responses import DBResponse

@pytest.fixture
def db_handler(tmp_path):
    """Create a DBHandler instance with a temporary database path."""
    db_path = tmp_path / "test_db.json"
    return DBHandler(db_path)


def test_write_todos_success(db_handler):
    """Test successful writing of todos to the database."""
    todo_list = [{"title": "Test", "done": False}]
    response = db_handler.write_todos(todo_list)
    
    assert response.error_code == SUCCESS
    assert response.todo_list == todo_list


def test_write_todos_oserror(db_handler):
    """Test write_todos handles OSError correctly."""
    todo_list = [{"title": "Test", "done": False}]
    
    with patch.object(db_handler._db_path, "open", side_effect=OSError):
        response = db_handler.write_todos(todo_list)
    
    assert response.error_code == DB_WRITE_ERROR
    assert response.todo_list == todo_list


def test_read_todos_success(db_handler):
    """Test successful reading of todos from the database."""
    todo_list = [{"title": "Test", "done": False}]
    db_handler.write_todos(todo_list)
    
    response = db_handler.read_todos()
    
    assert response.error_code == SUCCESS
    assert response.todo_list == todo_list


def test_read_todos_json_error(db_handler):
    """Test read_todos handles JSONDecodeError correctly."""
    db_handler._db_path.write_text("invalid json")
    
    response = db_handler.read_todos()
    
    assert response.error_code == JSON_ERROR
    assert response.todo_list == []


def test_read_todos_oserror(db_handler):
    """Test read_todos handles OSError correctly."""
    with patch.object(db_handler._db_path, "open", side_effect=OSError):
        response = db_handler.read_todos()
    
    assert response.error_code == DB_READ_ERROR
    assert response.todo_list == []