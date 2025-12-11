import os
import sqlite3
import tempfile
import pytest

from flask_project.peyroll import create_app
from flask_project.peyroll.database import get_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    try:
        app = create_app()
        # Override config for testing
        app.config.update({
            'TESTING': True,
            'SECRET_KEY': 'test-secret',
            'DATABASE': db_path,
        })

        with app.app_context():
            db = get_db()
            schema_path = os.path.join(os.path.dirname(__file__), '..', 'peyroll', 'schema.sql')
            schema_path = os.path.abspath(schema_path)
            with open(schema_path, 'r', encoding='utf-8') as f:
                db.executescript(f.read())

        yield app
    finally:
        os.close(db_fd)
        os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def register(client, username='testuser', password='Password1'):
    return client.post('/auth/register', data={'username': username, 'password': password}, follow_redirects=True)


def login(client, username='testuser', password='Password1', next_param=None):
    data = {'username': username, 'password': password}
    if next_param:
        data['next'] = next_param
    return client.post('/auth/login', data=data, follow_redirects=False)


def logout(client, method='GET'):
    if method == 'POST':
        return client.post('/auth/logout', follow_redirects=False)
    return client.get('/auth/logout', follow_redirects=False)
