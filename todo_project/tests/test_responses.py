import pytest
from todo.responses import DBResponse, TodoResponse

def test_dbresponse_basic():
    tasks = [{"id": 1, "title": "task"}]
    err = 0
    resp = DBResponse(tasks, err)

    assert isinstance(resp, tuple)
    assert len(resp) == 2
    assert resp.tasks_list is tasks
    assert resp.error == err
    assert resp[0] is tasks and resp[1] == err
    assert resp._fields == ("tasks_list", "error")
    assert set(DBResponse.__annotations__.keys()) == {"tasks_list", "error"}


def test_todoresponse_basic():
    todo = {"id": 2, "title": "another"}
    err = 1
    resp = TodoResponse(todo, err)

    assert isinstance(resp, tuple)
    assert len(resp) == 2
    assert resp.todo is todo
    assert resp.error == err
    assert resp[0] is todo and resp[1] == err
    assert resp._fields == ("todo", "error")
    assert set(TodoResponse.__annotations__.keys()) == {"todo", "error"}


def test_namedtuple_immutability_and_indexing():
    db = DBResponse([], 0)
    with pytest.raises(AttributeError):
        db.tasks_list = [1, 2, 3]

    todo = TodoResponse({"id": 3}, 0)
    with pytest.raises(AttributeError):
        todo.error = 5

    # index access remains valid
    assert db[0] == []
    assert db[1] == 0
    assert todo[0] == {"id": 3}
    assert todo[1] == 0