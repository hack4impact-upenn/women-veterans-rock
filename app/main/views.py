from flask import render_template
from flask import Response
from . import main
import json
from ..models import User, Resource
from flask.ext.login import login_required


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/map')
@login_required
def user_map():
    return render_template('main/map.html', users=User.query.all())


@main.route('/search')
def search():
    return render_template('main/search.html')


@main.route('/search/<query>')
def search_query(query):
    looking_for = '%'+query+'%'
    users = User.query.filter((User.first_name.ilike(looking_for)) |
                              User.last_name.ilike(looking_for))\
        .order_by(User.first_name).all()
    data = dict()
    data['results'] = [{'title': u.full_name(),
                        'url': '/account/profile/' + str(u.id)} for u in users]
    json_data = json.dumps(data)
    return Response(response=json_data, status=200,
                    mimetype='application/json')


@main.route('/resource_search')
def search_resources():
    return render_template('main/resource_search.html')


@main.route('/resource_search/<query>')
def search_query_resources(query):
    looking_for = '%'+query+'%'
    resources = Resource.query.filter(Resource.name.ilike(looking_for))\
        .order_by(Resource.name).all()
    data = dict()
    data['results'] = [{'title': r.name,
                        'url': '/resource/' + str(r.id)} for r in resources]
    json_data = json.dumps(data)
    return Response(response=json_data, status=200,
                    mimetype='application/json')
