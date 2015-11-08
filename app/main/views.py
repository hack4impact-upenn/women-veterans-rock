from flask import render_template
from . import main
from ..models import User


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/map', methods=['GET', 'POST'])
def mapusers():
    return render_template('main/mapview.html', users=User.query.all())
