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
        # Converting Google Places API names to our model names.
        name = form.name.data
        street_address = str(form.street_number.data) + ' ' + form.route.data
        city = form.locality.data
        state = form.administrative_area_level_1.data
        zip_code = ZIPCode.create_zip_code(form.postal_code.data)
        address = Address.create_address(name,
                                         street_address,
                                         city,
                                         state)
        address.zip_code = zip_code
        description = form.description.data
        website = form.website.data
        user = current_user
        resource = Resource.create_resource(name,
                                            description,
                                            website)
        resource.address = address
        resource.user = user
        return redirect(url_for('resources.read_resource',
                                resource_id=resource.id))
    return render_template('resources/create_resource.html', form=form)


@resources.route('/read/<int:resource_id>')
@login_required
def read_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    # TODO: check on reviews, which is dynamic?
    return render_template('resources/read_resource.html',
                           resource=resource,
                           reviews=resource.reviews,
                           current_user_id=current_user.id)


@resources.route('/review/create/<int:resource_id>', methods=['GET', 'POST'])
@login_required
def create_review(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    form = ReviewForm()
    if form.validate_on_submit():
        review = ResourceReview(timestamp=datetime.now(),
                                content=form.content.data,
                                rating=form.rating.data)
        review.resource = resource
        review.user = current_user
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('resources.read_resource',
                                resource_id=resource.id))
    return render_template('resources/create_review.html',
                           resource=resource,
                           reviews=resource.reviews,
                           current_user_id=current_user.id,
                           form=form)


@resources.route('/review/update/<int:review_id>', methods=['GET', 'POST'])
@login_required
def update_review(review_id):
    review = ResourceReview.query.get_or_404(review_id)
    resource = review.resource
    # TODO: test this prevents
    if current_user.id != review.user.id:
        flash('You cannot edit a review you did not write.', 'error')
        return redirect(url_for('resources.read_resource',
                                resource_id=resource.id))
    form = ReviewForm()
    if form.validate_on_submit():
        review.timestamp = datetime.now()
        review.content = form.content.data
        review.rating = form.rating.data
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('resources.read_resource',
                                resource_id=resource.id))
    return render_template('resources/update_review.html',
                           resource=resource,
                           reviews=resource.reviews,
                           current_user_id=current_user.id,
                           form=form)


@resources.route('/review/delete/<int:review_id>')
@login_required
def delete_review(review_id):
    review = ResourceReview.query.get_or_404(review_id)
    resource = review.resource
    if current_user.id != review.user.id:
        flash('You cannot delete a review you did not write.', 'error')
    else:
        db.session.delete(review)
        db.session.commit()
    return redirect(url_for('resources.read_resource',
                            resource_id=resource.id))
