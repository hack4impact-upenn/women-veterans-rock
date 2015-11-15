from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user
from . import resources
from .. import db
from ..models import Resource, ZIPCode, Address, User, ResourceReview
from .forms import ResourceForm, ReviewForm


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


@resources.route('/resource/<int:resource_id>', methods=['GET'])
def show(resource_id):
    # show the resource with the given id, the id is an integer
    resource = Resource.query.filter_by(id=resource_id).first()
    if resource is None:
        return redirect(url_for('resources.index'))
    address = Address.query.filter_by(id=resource.address_id).first()
    user = User.query.filter_by(id=resource.user_id).first()
    current_user_id = int(current_user.get_id())
    return render_template('resources/view.html', resource=resource,
                           address=address, user=user,
                           current_user_id=current_user_id)


@resources.route('/resource/<int:resource_id>/writeareview',
                 methods=['GET', 'POST'])
@login_required
def review(resource_id):
    resource = Resource.query.filter_by(id=resource_id).first()
    if resource is None:
        return redirect(url_for('resources.index', resource_id=resource.id))
    address = Address.query.filter_by(id=resource.address_id).first()
    user = User.query.filter_by(id=resource.user_id).first()
    form = ReviewForm()
    if form.validate_on_submit():
        review = ResourceReview(content=form.content.data,
                                rating=form.rating.data,
                                resource_id=resource_id,
                                user_id=int(current_user.get_id()))
        db.session.add(review)
        db.session.commit()
        print review.id
        return redirect(url_for('resources.show', resource_id=resource.id))
    return render_template('resources/writeareview.html', resource=resource,
                           address=address, user=user, form=form)


@resources.route('/resource/<int:resource_id>/deleteareview/<int:review_id>')
@login_required
def delete(resource_id, review_id):
    review = ResourceReview.query.filter_by(id=review_id).first()
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('resources.show', resource_id=resource_id))
