from flask import render_template

from . import web


@web.route('/')
def home():
    return render_template('home.html')
