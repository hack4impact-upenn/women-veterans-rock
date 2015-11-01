from flask import render_template
from . import resources


@resources.route('/')
def index():
    return render_template('resources/index.html')  # DNE
