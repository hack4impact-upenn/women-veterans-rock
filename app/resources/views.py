from flask import render_template, redirect, url_for, flash
from flask.ext.login import login_required, current_user
from . import resources
from .. import db
from ..models import Resource, ZIPCode, Address, ResourceReview
from .forms import ResourceForm, ReviewForm
from datetime import datetime


@resources.route('/')
@login_required
def index():
    return render_template('resources/index.html')


@resources.route('/create', methods=['GET', 'POST'])
@login_required
def create_resource():
    form = ResourceForm()
    if form.validate_on_submit():
        zip_code = ZIPCode.create_zip_code(form.postal_code.data)
        # Google Places API separates the street number and the route.
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
        return redirect(url_for('resources.read_resource',
                                resource_id=resource.id))
    return render_template('resources/create_resource.html', form=form)


@resources.route('/read/<int:resource_id>')
@login_required
def read_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    address = resource.address
    user = resource.user
    # TODO: base template for reviews.
    return render_template('resources/read_resource.html', resource=resource,
                           address=address, user=user,
                           current_user_id=int(current_user.get_id()))


@resources.route('/review/create/<int:resource_id>', methods=['GET', 'POST'])
@login_required
def create_review(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    address = resource.address
    user = resource.user
    form = ReviewForm()
    if form.validate_on_submit():
        review = ResourceReview(timestamp=datetime.now(),
                                content=form.content.data,
                                rating=form.rating.data,
                                resource_id=resource.id,
                                user_id=int(current_user.get_id()))
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('resources.read_resource',
                                resource_id=resource.id))
    return render_template('resources/create_review.html', resource=resource,
                           address=address, user=user, form=form)


@resources.route('/review/update/<int:review_id>', methods=['GET', 'POST'])
@login_required
def update_review(review_id):
    review = ResourceReview.query.get_or_404(review_id)
    resource = review.resource
    if int(current_user.id) != review.user.id:
        flash('You cannot edit a review you did not write.', 'error')
        return redirect(url_for('resources.read_resource',
                                resource_id=resource.id))
    address = resource.address
    user = review.user
    form = ReviewForm()
    if form.validate_on_submit():
        review.timestamp = datetime.now()
        review.content = form.content.data
        review.rating = form.rating.data
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('resources.read_resource',
                                resource_id=resource.id))
    return render_template('resources/update_review.html', resource=resource,
                           address=address, user=user, review=review,
                           form=form)


@resources.route('/review/delete/<int:review_id>')
@login_required
def delete_review(review_id):
    review = ResourceReview.query.get_or_404(review_id)
    resource = review.resource
    if int(current_user.id) != review.user.id:
        flash('You cannot delete a review you did not write.', 'error')
        return redirect(url_for('resources.read_resource',
                                resource_id=resource.id))
    else:
        # TODO: double check user wants to delete.
        db.session.delete(review)
        db.session.commit()
    return redirect(url_for('resources.read_resource',
                            resource_id=resource.id))
