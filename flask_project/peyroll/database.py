"""
Database initialization and management module for Flask application.
This module handles SQLite database connections, initialization, and cleanup
for a Flask application. It provides utilities to manage database connections
through Flask's application context and includes CLI commands for database setup.
Functions:
    get_db(): Returns a database connection, creating one if it doesn't exist.
    init_db(): Initializes the database schema from schema.sql file.
    close_db(e=None): Closes the database connection on application teardown.
    init_db_command(): CLI command to initialize the database.
    init_app(app): Registers database functions with the Flask application.
"""

import sqlite3


from flask import current_app, g
# from flask import with_appcontext
import click
import os
from typing import Optional
import logging
logger = logging.getLogger(__name__)


'''
Модуль ініціалізації та керування базою даних для застосунку Flask.
Цей модуль обробляє підключення до бази даних SQLite, ініціалізацію та очищення
для застосунку Flask. Він надає утиліти для керування підключеннями до бази даних
через контекст застосунку Flask та включає команди CLI для налаштування бази даних.
Функції:

get_db(): Повертає підключення до бази даних, створюючи його, якщо воно не існує.

init_db(): Ініціалізує схему бази даних з файлу schema.sql.

close_db(e=None): Закриває підключення до бази даних після завершення роботи застосунку.

init_db_command(): Команда CLI для ініціалізації бази даних.

init_app(app): Реєструє функції бази даних у застосунку Flask.

'''
def get_db() -> sqlite3.Connection:
    """
    Establishes and returns a SQLite database connection for the current Flask application context.
    If a connection does not already exist in the Flask `g` object, a new connection is created using
    the database path specified in the application's configuration. The connection uses `sqlite3.Row`
    as the row factory to allow dictionary-like access to query results.
    Returns:
        sqlite3.Connection: The SQLite database connection associated with the current context.
        
    Встановлює та повертає підключення до бази даних SQLite для поточного контексту програми Flask.
    Якщо підключення ще не існує в об'єкті Flask `g`, створюється нове підключення з використанням шляху до бази даних, зазначеного в конфігурації програми. Підключення використовує `sqlite3.Row`
    як фабрику рядків, щоб забезпечити доступ до результатів запиту, подібний до словника.
    Повертає:
        sqlite3.Connection: Підключення до бази даних SQLite, пов'язане з поточним контекстом.
    """
    
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db
    # if 'db' not in g:
    #     database_path = current_app.config.get(
    #         'DATABASE',
    #         os.path.join(current_app.instance_path, 'peyroll.sqlite')
    #     )
    #     os.makedirs(os.path.dirname(database_path), exist_ok=True)
    #     g.db = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_DECLTYPES)
    #     g.db.row_factory = sqlite3.Row
    # return g.db


def init_db():
    """
    Initializes the database by executing the SQL schema script.
    This function retrieves a database connection, reads the SQL schema from
    the 'schema.sql' file, and executes the script to set up the database
    structure.
    Raises:
        Any exceptions raised by database connection or script execution.
        
    Ініціалізує базу даних, виконуючи скрипт схеми SQL.
    Ця функція отримує підключення до бази даних, зчитує схему SQL з файлу 'schema.sql' та виконує скрипт для налаштування структури бази даних. структури.
    Викликає:
        Будь-які винятки, що виникають під час підключення до бази даних або виконання скрипта.
    """
    
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        sql_script = f.read()
        # print(sql_script)
        db.executescript(sql_script.decode("utf-8"))
    db.commit()
    
    # try:
    #     with current_app.open_resource('schema.sql', mode='r') as f:
    #         db.executescript(f.read())
    #     db.commit()
    # except Exception as exc:
    #     logger.exception("Failed to initialize the database.")
    #     raise
    

def close_db(e: Optional[BaseException] = None) -> None:
    """
    Closes the database connection if it exists in the Flask application context.
    Parameters:
        e (optional): An exception that may have triggered the teardown. Default is None.
    Returns:
        None
    """
    
    db = g.pop('db', None)
    if db is not None:
        db.close()
        
@click.command('init-db')
def init_db_command():
    """
    Initializes the database by calling the init_db function and prints a confirmation message.
    This function is intended to be used as a command-line utility to set up the application's database.
    """
    
    init_db()
    click.echo('Initialized the database.')
    
def init_app(app):
    """
    Initialize the database with the Flask application.
    Registers teardown and CLI commands for database management.
    Args:
        app: The Flask application instance to configure.
    """
    
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)