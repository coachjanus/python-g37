import io
from pathlib import Path
import pytest

import todo.config as cfg


def test_init_config_file_creates_dir_and_file(tmp_path, monkeypatch):
    cfg.CONFIG_DIR_PATH = tmp_path / "cfgdir"
    cfg.CONFIG_FILE_PATH = cfg.CONFIG_DIR_PATH / "config.ini"

    code = cfg._init_config_file()
    assert code == cfg.SUCCESS
    assert cfg.CONFIG_DIR_PATH.exists() and cfg.CONFIG_DIR_PATH.is_dir()
    assert cfg.CONFIG_FILE_PATH.exists() and cfg.CONFIG_FILE_PATH.is_file()


def test_init_config_file_dir_error(monkeypatch):
    class BrokenDir:
        def mkdir(self, exist_ok=False):
            raise OSError("cannot make dir")

    cfg.CONFIG_DIR_PATH = BrokenDir()
    # Ensure CONFIG_FILE_PATH is something harmless (won't be touched when mkdir fails)
    cfg.CONFIG_FILE_PATH = Path("/non/existent/config.ini")

    assert cfg._init_config_file() == cfg.DIR_ERROR


def test_init_config_file_file_error(tmp_path, monkeypatch):
    cfg.CONFIG_DIR_PATH = tmp_path / "cfgdir"
    # Provide a file-like object whose touch() raises
    class BrokenFile:
        def touch(self, exist_ok=False):
            raise OSError("cannot touch file")

    cfg.CONFIG_FILE_PATH = BrokenFile()

    assert cfg._init_config_file() == cfg.FILE_ERROR


def test_create_database_writes_file(tmp_path):
    cfg.CONFIG_FILE_PATH = tmp_path / "config.ini"
    db_path = "/some/db/path.json"

    code = cfg._create_database(db_path)
    assert code == cfg.SUCCESS

    content = cfg.CONFIG_FILE_PATH.read_text()
    assert "[General]" in content
    assert "database" in content
    assert db_path in content


def test_create_database_write_error(monkeypatch):
    class BrokenFile:
        def open(self, mode='w'):
            raise OSError("cannot open for write")

    cfg.CONFIG_FILE_PATH = BrokenFile()
    assert cfg._create_database("/irrelevant") == cfg.DB_WRITE_ERROR


@pytest.mark.parametrize(
    "init_ret, create_ret, expected",
    [
        (cfg.DIR_ERROR, cfg.SUCCESS, cfg.DIR_ERROR),
        (cfg.SUCCESS, cfg.DB_WRITE_ERROR, cfg.DB_WRITE_ERROR),
        (cfg.SUCCESS, cfg.SUCCESS, cfg.SUCCESS),
    ],
)
def test_init_app_propagates_codes(monkeypatch, init_ret, create_ret, expected):
    monkeypatch.setattr(cfg, "_init_config_file", lambda: init_ret)
    monkeypatch.setattr(cfg, "_create_database", lambda db: create_ret)

    assert cfg.init_app("/some/db") == expected
    
# def test_file_operations(tmp_path):
#     # Your test code here
#     pass

# #    The tmp_path fixture returns a pathlib.Path object, which provides a convenient and modern way to interact with file paths. 


# import pytest

# def test_create_and_read_file(tmp_path):
#     file_path = tmp_path / "my_file.txt"
#     file_path.write_text("Hello, Pytest!")

#     assert file_path.read_text() == "Hello, Pytest!"

# monkeypatch.setattr(obj, name, value, raising=True): Встановлює атрибут для об'єкта, класу або модуля.
def test_setattr_example(monkeypatch):
        class MyClass:
            value = 10
        
        monkeypatch.setattr(MyClass, 'value', 20)
        assert MyClass.value == 20
# monkeypatch.delattr(obj, name, raising=True): Видаляє атрибут з об'єкта, класу або модуля.
    def test_delattr_example(monkeypatch):
        class MyClass:
            value = 10
        
        monkeypatch.delattr(MyClass, 'value')
        # Accessing MyClass.value now would raise an AttributeError

# monkeypatch.setitem(dic, name, value): Sets an item in a dictionary-like object. 

    def test_setitem_example(monkeypatch):
        my_dict = {'key1': 'value1'}
        monkeypatch.setitem(my_dict, 'key2', 'value2')
        assert my_dict == {'key1': 'value1', 'key2': 'value2'}
# monkeypatch.delitem(dic, name, raising=True): Deletes an item from a dictionary-like object. 
    def test_delitem_example(monkeypatch):
        my_dict = {'key1': 'value1'}
        monkeypatch.delitem(my_dict, 'key1')
        assert my_dict == {}
