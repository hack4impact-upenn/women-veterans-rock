from flask import render_template
from . import main
from .. import db
from ..models import ZIPCode, User


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/mapusers', method='[POST]')
def mapusers():
    users = User.query('zip_code').all()
    for us in users:
        db.session.add(ZIPCode.latitude, ZIPCode.longitude)
    db.session.commit()
    return render_template('main/mapview.html')
    return 'OK 12', 200
