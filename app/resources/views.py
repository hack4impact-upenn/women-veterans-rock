from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user
from flask import Response
from . import resources
from .. import db
from ..models import Resource, ZIPCode, Address, User, ResourceReview
from .forms import ResourceForm
import json


@resources.route('/')
@login_required
def index():
    return render_template('resources/index.html')


@resources.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ResourceForm()
    if form.validate_on_submit():
        # Based on form's zip code, load or create ZIPCode and add to db.
        zip_code = ZIPCode.create_zip_code(form.postal_code.data)
        # Based on form's address, zip's id, load or create Address, add to db.
        street_num_route = str(form.street_number.data) + ' ' + form.route.data
        # TODO: Create helper method in models/location.py.
        address = Address.query.filter_by(
            name=form.name.data,
            street_address=street_num_route,
            city=form.locality.data,
            state=form.administrative_area_level_1.data,
            zip_code_id=zip_code.id).first()
        if address is None:
            address = Address(name=form.name.data,
                              street_address=street_num_route,
                              city=form.locality.data,
                              state=form.administrative_area_level_1.data,
                              zip_code_id=zip_code.id)
            db.session.add(address)
            db.session.commit()
        # Based on form and address id, create a new resource.
        # TODO: Create helper method in models/resource.py.
        resource = Resource(name=form.name.data,
                            description=form.description.data,
                            website=form.website.data,
                            address_id=address.id,
                            user_id=int(current_user.get_id()))
        db.session.add(resource)
        db.session.commit()
        return redirect(url_for('resources.index'))
    return render_template('resources/add_resource.html', form=form)


@resources.route('/resource/<int:resource_id>')
@login_required
def show_resource(resource_id):
    """
    Show the resource with the given id, the id is an integer.
    """
    resource = Resource.query.get_or_404(resource_id)
    address = Address.query.get(resource.address_id)
    user = User.query.get(resource.user_id)
    return render_template('resources/view_resource.html', resource=resource,
                           address=address, user=user)


@resources.route('/resource/<int:resource_id>/<query>')
@login_required
def review_search(query, resource_id):
    looking_for = '%'+query+'%'
    reviews = ResourceReview.query.filter(
        (ResourceReview.content.ilike(looking_for)))\
        .orderby(ResourceReview.content).all()
    data = dict()
    data['results'] = [{'title': r.content()} for r in reviews]
    json_data = json.dumps(data)
    return Response(response=json_data, status=200,
                    mimetype='application/json')
