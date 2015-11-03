from flask import request, render_template
from . import main


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/map', method='[POST]')
def map():
    content = request.get_json(force=True)
    coors = content['zip_codes']
    print coors
