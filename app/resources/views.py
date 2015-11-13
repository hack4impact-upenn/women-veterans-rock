from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user
from . import resources
from .. import db
from ..models import Resource, ZIPCode, Address, User
from .forms import ResourceForm


@resources.route('/', methods=['GET'])
def index():
    return render_template('resources/index.html')


@resources.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ResourceForm()
    if form.validate_on_submit():
        # based on form's zip code, load or create ZIPCode and add to db
        zip_code = ZIPCode.create_zip_code(form.postal_code.data)
        # based on form's address, zip's id, load or create Address, add to db
        street_num_route = str(form.street_number.data) + ' ' + form.route.data
        # should create helper method in models/location.py
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
        # based on form and address id, create a new resource
        # should create helper method in models/resource.py
        resource = Resource(name=form.name.data,
                            description=form.description.data,
                            website=form.website.data,
                            address_id=address.id,
                            user_id=int(current_user.get_id()))
        db.session.add(resource)
        db.session.commit()
        print resource.id
        return redirect(url_for('resources.index'))
    return render_template('resources/add.html', form=form)


@resources.route('/resource/<int:resource_id>')
def show_resource(resource_id):
    # show the resource with the given id, the id is an integer
    resource = Resource.query.filter_by(id=resource_id).first()
    address = Address.query.filter_by(id=resource.address_id).first()
    user = User.query.filter_by(id=resource.user_id).first()
    if resource is None:
        return redirect(url_for('resources.index'))
    return render_template('resources/view.html', resource=resource,
                           address=address, user=user)
