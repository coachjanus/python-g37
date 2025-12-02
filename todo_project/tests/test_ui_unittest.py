import sys
import os
import types
import json
import tempfile
import shutil
from pathlib import Path
import builtins
import importlib
import unittest

# Ensure project root is on sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Provide a minimal fake `typer` module so importing `todo.ui` works without typer installed
fake_typer = types.SimpleNamespace()

def _secho(msg, fg=None):
    # no-op for tests
    return None

def _get_app_dir(app_name):
    # Return a temp directory for testing
    return tempfile.mkdtemp()

fake_typer.secho = _secho
fake_typer.get_app_dir = _get_app_dir
fake_typer.Exit = SystemExit
fake_typer.colors = types.SimpleNamespace(RED='red', GREEN='green')

# Inject fake typer before any imports that use it
sys.modules['typer'] = fake_typer


def _import_ui():
    """Import or reload the UI module after ensuring fake typer is present."""
    import todo.ui as ui_mod
    importlib.reload(ui_mod)
    return ui_mod.UI


class UITestCase(unittest.TestCase):
    """Test suite for todo.ui module."""

    def setUp(self):
        """Create a temporary directory for test database files."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_todo_db.json"
        # Initialize DB file with empty list
        self.db_path.write_text(json.dumps([], indent=4))

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_add_todo_persists(self):
        """Test that add_todo persists a task to the database."""
        UI = _import_ui()

        # Create a UI instance without running its __init__ to avoid config checks
        ui = UI.__new__(UI)
        from todo.task_list import TaskList
        from rich.prompt import Prompt
        ui.task_list = TaskList(self.db_path)

        # Monkeypatch Prompt.ask to return category and priority without user input
        original_prompt_ask = Prompt.ask
        prompt_values = iter(['Work', 'NEUTRAL'])
        Prompt.ask = lambda *args, **kwargs: next(prompt_values)

        # Monkeypatch input to provide a title
        original_input = builtins.input
        input_values = iter(['My Test Task'])
        builtins.input = lambda prompt='': next(input_values)

        try:
            # Call add_todo
            ui.add_todo()

            # Verify DB file now contains the task
            data = json.loads(self.db_path.read_text())
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 1)
            task = data[0]
            # Note: add_todo converts title to lowercase, and Task.__init__ adds a trailing period
            self.assertEqual(task.get('title'), 'my test task.')
            self.assertIn(task.get('category'), ('Work', 'work', 'WORK'))
        finally:
            builtins.input = original_input
            Prompt.ask = original_prompt_ask

    def test_set_done_task(self):
        """Test that set_done_task marks a task as completed."""
        UI = _import_ui()

        # Pre-populate db with one task dict; status 0 = open
        initial = [{
            'title': 'Do something',
            'category': 'Work',
            'status': 0,
            'position': 0
        }]
        self.db_path.write_text(json.dumps(initial, indent=4))

        ui = UI.__new__(UI)
        from todo.task_list import TaskList
        ui.task_list = TaskList(self.db_path)

        # Monkeypatch input to provide task ID '1'
        original_input = builtins.input
        inputs = iter(['1'])
        builtins.input = lambda prompt='': next(inputs)

        try:
            ui.set_done_task()

            data = json.loads(self.db_path.read_text())
            self.assertEqual(data[0]['status'], 1)
            self.assertIn('completed_at', data[0])
        finally:
            builtins.input = original_input

    def test_remove_task(self):
        """Test that remove_task deletes a task from the database."""
        UI = _import_ui()

        # Pre-populate db with one task dict
        initial = [{
            'title': 'Do something',
            'category': 'Work',
            'status': 0,
            'position': 0
        }]
        self.db_path.write_text(json.dumps(initial, indent=4))

        ui = UI.__new__(UI)
        from todo.task_list import TaskList
        ui.task_list = TaskList(self.db_path)

        # Monkeypatch input to provide task ID '1'
        original_input = builtins.input
        inputs = iter(['1'])
        builtins.input = lambda prompt='': next(inputs)

        try:
            ui.remove_task()

            data = json.loads(self.db_path.read_text())
            self.assertEqual(data, [])
        finally:
            builtins.input = original_input


if __name__ == '__main__':
    unittest.main()
