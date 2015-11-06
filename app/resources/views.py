from flask import render_template, redirect, url_for, flash  # request
from flask.ext.login import current_user
from . import resources
from .. import db
from ..models import Resource, ZIPCode, Address
from .forms import ResourceForm


@resources.route('/', methods=['GET'])
def index():
    return render_template('resources/index.html')


@resources.route('/add', methods=['GET', 'POST'])
def add():
    form = ResourceForm()
    if form.validate_on_submit():
        # based on the form's zip code, load or create ZIPCode
        zip_code = ZIPCode.filter_by(zip_code=form.zip_code.data).first() or \
            ZIPCode(zip_code=form.zip_code.data)
        # based on the form's address and zip code id, load or create Address
        address = Address.filter_by(name=form.name.data,
                                    street_address=form.street_address.data,
                                    city=form.street_address.data,
                                    state=form.state.data,
                                    zip_code_id=zip_code.id,).first() or \
            Address(name=form.name.data,
                    street_address=form.street_address.data,
                    city=form.city.data,
                    state=form.state.data,
                    zip_code_id=zip_code.id)
        # based on form and address id, create a new resource
        resource = Resource(name=form.name.data,
                            description=form.description.data,
                            website=form.website.data,
                            address_id=address.id,
                            user_id=int(current_user.get_id()))
        db.session.add(resource)
        db.session.commit()
        flash('Resource has been added.')
        return redirect(url_for('resources/index'))
    return render_template('resources/add.html', form=form)


@resources.route('/resource/<int:resource_id>')
def show_resource(resource_id):
    # show the resource with the given id, the id is an integer
    resource = Resource.query.filter_by(id=resource_id).first()
    if resource is None:
        return redirect(url_for('resources/index'))
    return render_template('resources/view.html', resource=resource)
