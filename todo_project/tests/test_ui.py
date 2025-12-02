import pytest
from unittest.mock import Mock, MagicMock, patch
from rich.console import Console
from todo.ui import UI
from todo.task_list import TaskList
from todo.model import Task, Status
import typer
import datetime

@pytest.fixture
def mock_task_list():
    return Mock(spec=TaskList)


@pytest.fixture
def ui_instance(mock_task_list):
    with patch.object(UI, 'get_tasks', return_value=mock_task_list):
        ui = UI()
        return ui


class TestUIInitialization:
    def test_init_creates_console(self, ui_instance):
        assert isinstance(ui_instance.console, Console)
    
    def test_init_loads_task_list(self, ui_instance, mock_task_list):
        assert ui_instance.task_list == mock_task_list


class TestGetTasks:
    @patch('todo.ui.config.CONFIG_FILE_PATH')
    @patch('todo.ui.db.get_database_path')
    @patch('todo.ui.TaskList')
    def test_get_tasks_success(self, mock_tasklist_class, mock_get_db_path, mock_config_path):
        mock_config_path.exists.return_value = True
        mock_db_path = Mock()
        mock_db_path.exists.return_value = True
        mock_get_db_path.return_value = mock_db_path
        mock_tasklist_instance = Mock()
        mock_tasklist_class.return_value = mock_tasklist_instance
        
        ui = UI.__new__(UI)
        result = ui.get_tasks()
        
        assert result == mock_tasklist_instance
    
    @patch('todo.ui.config.CONFIG_FILE_PATH')
    @patch('todo.ui.typer.secho')
    def test_get_tasks_config_not_found(self, mock_secho, mock_config_path):
        mock_config_path.exists.return_value = False
        
        ui = UI.__new__(UI)
        with pytest.raises(typer.Exit):
            ui.get_tasks()
        
        mock_secho.assert_called_once()
    
    @patch('todo.ui.config.CONFIG_FILE_PATH')
    @patch('todo.ui.db.get_database_path')
    @patch('todo.ui.typer.secho')
    def test_get_tasks_database_not_found(self, mock_secho, mock_get_db_path, mock_config_path):
        mock_config_path.exists.return_value = True
        mock_db_path = Mock()
        mock_db_path.exists.return_value = False
        mock_get_db_path.return_value = mock_db_path
        
        ui = UI.__new__(UI)
        with pytest.raises(typer.Exit):
            ui.get_tasks()


class TestChoiceCategory:
    @patch('todo.ui.Prompt.ask')
    def test_choice_category_returns_title_case(self, mock_prompt, ui_instance):
        mock_prompt.return_value = "work"
        result = ui_instance.choice_category()
        assert result == "Work"


class TestChoicePriority:
    @patch('todo.ui.Prompt.ask')
    def test_choice_priority_returns_uppercase(self, mock_prompt, ui_instance):
        mock_prompt.return_value = "important"
        result = ui_instance.choice_priority()
        assert result == "IMPORTANT"


class TestAddTodo:
    @patch('builtins.input')
    @patch.object(UI, 'choice_category')
    @patch.object(UI, 'choice_priority')
    def test_add_todo_neutral_priority(self, mock_priority, mock_category, mock_input, ui_instance):
        mock_input.return_value = "test task"
        mock_category.return_value = "Work"
        mock_priority.return_value = "NEUTRAL"
        
        mock_response = Mock()
        mock_response.error = 0
        mock_response.todo = Mock(title="test task")
        ui_instance.task_list.add_task.return_value = mock_response
        
        with patch('todo.ui.typer.secho'):
            ui_instance.add_todo()
        
        ui_instance.task_list.add_task.assert_called_once()


class TestGetTaskId:
    def test_get_task_id_valid(self, ui_instance):
        with patch('builtins.input', return_value="5"):
            result = ui_instance.get_task_id()
            assert result == 5
    
    def test_get_task_id_invalid(self, ui_instance):
        with patch('builtins.input', return_value="invalid"):
            with pytest.raises(ValueError):
                ui_instance.get_task_id()


class TestSetDoneTask:
    @patch.object(UI, 'get_task_id')
    def test_set_done_task_valid_id(self, mock_get_id, ui_instance):
        mock_get_id.return_value = 1
        
        mock_response = Mock()
        mock_response.error = None
        mock_response.tasks_list = [{'title': 'task1', 'status': 0}]
        ui_instance.task_list.get_tasks.return_value = mock_response
        
        update_response = Mock()
        update_response.error = 0
        ui_instance.task_list.update_task.return_value = update_response
        
        with patch('todo.ui.typer.secho'):
            ui_instance.set_done_task()
        
        ui_instance.task_list.update_task.assert_called_once()
    
    @patch.object(UI, 'get_task_id')
    def test_set_done_task_invalid_id_range(self, mock_get_id, ui_instance):
        mock_get_id.return_value = 10
        
        mock_response = Mock()
        mock_response.error = None
        mock_response.tasks_list = [{'title': 'task1'}]
        ui_instance.task_list.get_tasks.return_value = mock_response
        
        with patch('todo.ui.typer.secho'):
            ui_instance.set_done_task()
        
        ui_instance.task_list.update_task.assert_not_called()


class TestRemoveTask:
    @patch.object(UI, 'get_task_id')
    def test_remove_task_success(self, mock_get_id, ui_instance):
        mock_get_id.return_value = 1
        
        mock_response = Mock()
        mock_response.error = 0
        mock_response.todo = {'title': 'task1'}
        ui_instance.task_list.remove_task.return_value = mock_response
        
        with patch('todo.ui.typer.secho'):
            ui_instance.remove_task()
        
        ui_instance.task_list.remove_task.assert_called_once_with(1)


class TestMakeHeader:
    def test_make_header_valid(self, ui_instance):
        headers = ui_instance.make_header()
        assert len(headers) == 5
        assert headers[0]['name'] == 'ID'
    
    def test_make_header_mismatch(self, ui_instance):
        UI.values = [["ID", "dim"]]  # Length mismatch
        with pytest.raises(ValueError):
            ui_instance.make_header()


class TestShow:
    def test_show_renders_table(self, ui_instance):
        tasks = [
            {'title': 'task1', 'category': 'Work', 'status': 0, 'position': 0},
            {'title': 'task2', 'category': 'Learn', 'status': 1, 'position': 1}
        ]
        
        with patch.object(ui_instance.console, 'print'):
            ui_instance.show(tasks)
        
        ui_instance.console.print.assert_called_once()


class TestStaticMethods:
    def test_join_category(self):
        result = UI.join_category()
        assert 'Work' in result
        assert 'Learn' in result
    
    def test_join_priority(self):
        result = UI.join_priority()
        assert 'NEUTRAL' in result
        assert 'IMPORTANT' in result
    
    def test_get_category_color(self):
        color = UI.get_category_color("work")
        assert color == "red"
    
    def test_get_priority_color(self):
        color = UI.get_priority_color("important")
        assert color == "blue"