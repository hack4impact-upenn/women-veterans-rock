from flask.ext.wtf import Form
from wtforms.fields import (
    StringField,
    IntegerField,
    SubmitField
)
from wtforms.validators import InputRequired, Length, URL, Optional,\
    NumberRange


class ResourceForm(Form):
    address_autocomplete = StringField('Enter the address')
    name = StringField('Name', validators=[
        InputRequired(),
        Length(1, 64)
    ])
    description = StringField('Description', validators=[
        InputRequired(),
    ])
    website = StringField('Website', validators=[
        Optional(),
        URL()
    ])

    street_number = IntegerField('Street Number', validators=[
        InputRequired()
    ])
    # Google Place Autocomplete example divs named for Google address schema.
    route = StringField('Street Address', validators=[
        InputRequired()
    ])
    locality = StringField('City', validators=[
        InputRequired()
    ])
    administrative_area_level_1 = StringField('State', validators=[
        InputRequired(),
        Length(2, 2)
    ])
    postal_code = StringField('ZIP Code', validators=[
        InputRequired(),
        Length(5, 5)
    ])
    submit = SubmitField('Add Resource')


class ReviewForm(Form):
    rating = IntegerField('Rating (1-5)', validators=[
        InputRequired(),
        NumberRange(1, 5)
    ])
    content = StringField('Content', validators=[
        InputRequired()
    ])
    submit = SubmitField('Finish Your Review')


class ClosedResourceForm(Form):
    reason = StringField('Why is this resource no longer available?')
    expertise = StringField(
        'How do you know this resource is no longer available? What is your'
        'connection to this resource?')
    submit = SubmitField('Submit')
