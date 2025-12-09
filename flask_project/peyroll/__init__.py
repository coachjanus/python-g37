from flask import Flask
from . import pages

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
    
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    app.register_blueprint(pages.bp)
    return app
    
    

