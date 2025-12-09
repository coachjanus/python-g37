"""
Initialize and configure the Flask application for the payroll system.
This module provides the application factory function that creates and configures
a Flask application instance with database initialization and blueprint registration.
Returns:
    Flask: A configured Flask application instance with the following features:
        - Instance-relative configuration enabled
        - Secret key set for session management
        - SQLite database configured at instance/payroll.db
        - Instance directory created if it doesn't exist
        - Database initialized and connected
        - Pages blueprint registered for routing
"""
from flask import Flask

from . import pages

from . import database
import os

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return '''
#     <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Document</title>
# </head>
# <body>
#     <h1 style="color: crimson;">Hello world</h1>
#     <p>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Natus perferendis tempora laudantium aut saepe veniam cupiditate ex odit pariatur labore molestiae enim ipsum deleniti rerum, dolor quaerat vero dolorem debitis?</p>
# </body>
# </html>
#     '''
    
# def create_app():
#     app = Flask(__name__, instance_relative_config=True)
    
#     app.register_blueprint(pages.bp)
#     return app

'''
Ініціалізація та налаштування програми Flask для системи нарахування заробітної плати.
Цей модуль надає функцію фабрики програм, яка створює та налаштовує екземпляр програми Flask з ініціалізацією бази даних та реєстрацією плану.
Повертає:
Flask: Налаштований екземпляр програми Flask з такими функціями:
- Увімкнено конфігурацію, відносну до екземпляра
- Встановлено секретний ключ для керування сеансом
- База даних SQLite, налаштована за адресою instance/payroll.db
- Створено каталог екземплярів, якщо він не існує
- База даних ініціалізовано та підключено
- План сторінок зареєстровано для маршрутизації

'''
import click



def create_app():
    
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'payroll.db')
    )
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # @app.cli.command('init_db')
    # def initialize_database():
    #     """Initialize the SQLite database."""
    #     click.echo('Initialized the SQLite database!')
        
    database.init_app(app)
    
    app.register_blueprint(pages.bp)
    return app
    