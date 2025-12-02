import pytest
from unittest.mock import patch, MagicMock, call
from pathlib import Path
import typer
from todo import cli, config, ERRORS, database as db
from todo.ui import UI

class TestInit:
    """Tests for the init command."""

    @patch("todo.cli.db.init_database")
    @patch("todo.cli.config.init_app")
    def test_init_success(self, mock_init_app, mock_init_db):
        """Test successful initialization."""
        mock_init_app.return_value = None
        mock_init_db.return_value = None

        with patch("typer.secho") as mock_secho:
            cli.init("/path/to/db")
            mock_init_app.assert_called_once_with("/path/to/db")
            mock_init_db.assert_called_once_with(Path("/path/to/db"))
            assert mock_secho.call_count == 1

    @patch("todo.cli.config.init_app")
    def test_init_config_failure(self, mock_init_app):
        """Test initialization fails when config creation fails."""
        mock_init_app.return_value = "error_code"

        with patch("typer.secho") as mock_secho:
            with pytest.raises(typer.Exit) as exc_info:
                cli.init("/path/to/db")
            assert exc_info.value.exit_code == 1
            mock_secho.assert_called_once()

    @patch("todo.cli.db.init_database")
    @patch("todo.cli.config.init_app")
    def test_init_database_failure(self, mock_init_app, mock_init_db):
        """Test initialization fails when database initialization fails."""
        mock_init_app.return_value = None
        mock_init_db.return_value = "error_code"

        with patch("typer.secho") as mock_secho:
            with pytest.raises(typer.Exit) as exc_info:
                cli.init("/path/to/db")
            assert exc_info.value.exit_code == 1


class TestRun:
    """Tests for the run command."""

    @patch("todo.cli.UI")
    def test_run_add_todo(self, mock_ui_class):
        """Test run command with add todo action."""
        mock_ui = MagicMock()
        mock_ui_class.return_value = mock_ui
        mock_ui.your_choice.side_effect = ['a', 'q']

        cli.run()
        mock_ui.add_todo.assert_called_once()
        mock_ui.bye.assert_called_once()

    @patch("todo.cli.UI")
    def test_run_list_tasks(self, mock_ui_class):
        """Test run command with list tasks action."""
        mock_ui = MagicMock()
        mock_ui_class.return_value = mock_ui
        mock_ui.your_choice.side_effect = ['l', 'q']

        cli.run()
        mock_ui.get_all_task.assert_called_once()

    @patch("todo.cli.UI")
    def test_run_mark_done(self, mock_ui_class):
        """Test run command with mark task as done action."""
        mock_ui = MagicMock()
        mock_ui_class.return_value = mock_ui
        mock_ui.your_choice.side_effect = ['u', 'q']

        cli.run()
        mock_ui.set_done_task.assert_called_once()

    @patch("todo.cli.UI")
    def test_run_delete_task(self, mock_ui_class):
        """Test run command with delete task action."""
        mock_ui = MagicMock()
        mock_ui_class.return_value = mock_ui
        mock_ui.your_choice.side_effect = ['d', 'q']

        cli.run()
        mock_ui.remove_task.assert_called_once()

    @patch("todo.cli.UI")
    def test_run_help(self, mock_ui_class):
        """Test run command with help action."""
        mock_ui = MagicMock()
        mock_ui_class.return_value = mock_ui
        mock_ui.your_choice.side_effect = ['h', 'q']

        cli.run()
        mock_ui.help_me.assert_called()

    @patch("todo.cli.UI")
    def test_run_invalid_choice(self, mock_ui_class):
        """Test run command with invalid choice."""
        mock_ui = MagicMock()
        mock_ui_class.return_value = mock_ui
        mock_ui.your_choice.side_effect = ['x', 'q']

        cli.run()
        mock_ui.help_me.assert_called()

    @patch("todo.cli.UI")
    def test_run_quit(self, mock_ui_class):
        """Test run command quit action."""
        mock_ui = MagicMock()
        mock_ui_class.return_value = mock_ui
        mock_ui.your_choice.side_effect = ['q']

        cli.run()
        mock_ui.bye.assert_called_once()