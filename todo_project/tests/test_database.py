import tempfile
import os
from pathlib import Path
import configparser
import pytest
from todo.database import init_database, get_database_path
from todo import SUCCESS, DB_WRITE_ERROR

def test_init_database_success(tmp_path):
    db_file = tmp_path / "test_db.json"
    result = init_database(db_file)
    assert result == SUCCESS
    assert db_file.read_text() == "[]"

def test_init_database_write_error(monkeypatch, tmp_path):
    db_file = tmp_path / "test_db.json"

    def raise_oserror(*args, **kwargs):
        raise OSError

    monkeypatch.setattr(db_file, "write_text", raise_oserror)
    result = init_database(db_file)
    assert result == DB_WRITE_ERROR

def test_get_database_path(tmp_path):
    config_file = tmp_path / "config.ini"
    db_path = tmp_path / "mydb.json"
    config = configparser.ConfigParser()
    config["General"] = {"database": str(db_path)}
    with open(config_file, "w") as f:
        config.write(f)

    result = get_database_path(config_file)
    assert isinstance(result, Path)
    assert result == db_path