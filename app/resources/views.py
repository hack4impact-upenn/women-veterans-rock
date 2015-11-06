from flask import render_template, redirect, url_for, flash  # request
from flask.ext.login import current_user
from . import resources
from .. import db
from ..models import Resource
from .forms import ResourceForm


@resources.route('/', methods=['GET'])
def index():
    return render_template('resources/index.html')


@resources.route('/add', methods=['GET', 'POST'])
def add():
    form = ResourceForm()
    if form.validate_on_submit():
        print current_user.get_id()
        # zip_code = ZIPCode.filter_by(zip_code=form.zip_code.data).first()
        # address = Address.filter_by()
        resource = Resource(name=form.name.data,
                            description=form.description.data,
                            website=form.website.data)
        # address_id=, # user_id=current_user.get_id())
        db.session.add(resource)
        db.session.commit()
        flash('Resource has been added')
        return redirect(url_for('resources.index'))
    return render_template('resources/add.html', form=form)
