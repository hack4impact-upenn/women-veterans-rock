from flask import request, render_template
from .. import main, db
from ..models import location


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/map', method='[POST]')
def map():
    content = request.get_json(force=True)
    coors = content['zip_codes']
    print coors
    for coor in coors:
        print coor
        db.session.add(location.Zipcode(coor["latitude"], coor["longitude"]))
    db.session.commit()
    return 'OK 12', 200
