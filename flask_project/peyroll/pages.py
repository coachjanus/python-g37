"""
Blueprint module for rendering static pages in the Flask application.

This module defines a Blueprint that handles routing for the main pages of the application,
including the home page, about page, and contact page. Each route renders a corresponding
HTML template.

Routes:
    /: Renders the home page (pages/index.html)
    /about: Renders the about page (pages/about.html)
    /contact: Renders the contact page (pages/contact.html)
"""
from flask import Blueprint, render_template

'''
Модуль Blueprint для рендерингу статичних сторінок у застосунку Flask.

Цей модуль визначає Blueprint, який обробляє маршрутизацію для головних сторінок застосунку,
включаючи головну сторінку, сторінку «Про нас» та сторінку контактів. Кожен маршрут рендерить відповідний
шаблон HTML.

Маршрути:

/: Рендерить головну сторінку (pages/index.html)

/about: Рендерить сторінку «Про нас» (pages/about.html)

/contact: Рендерить сторінку контактів (pages/contact.html)
'''
bp = Blueprint('pages', __name__)

@bp.route('/')
def home():
    return render_template('pages/index.html')

@bp.route('/about')
def about():
    return render_template('pages/about.html')

@bp.route('/contact')
def contact():
    return render_template('pages/contact.html')

