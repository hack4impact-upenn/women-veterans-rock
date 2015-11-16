from flask.ext.wtf import Form
from wtforms.fields import (
    StringField,
    IntegerField,
    SubmitField
)
from wtforms.validators import InputRequired, Length


class ResourceForm(Form):
    autocomplete = StringField('Enter the address')

    name = StringField('Name', validators=[
        InputRequired(),
        Length(1, 64)
    ])
    description = StringField('Description', validators=[
        InputRequired(),
    ])
    website = StringField('Website')

    street_number = IntegerField('Street Number', validators=[
        InputRequired()
    ])
    # Google Place Autocomplete example divs named for Google address schema
    route = StringField('Street Address', validators=[
        InputRequired()
    ])
    locality = StringField('City', validators=[
        InputRequired()
    ])
    administrative_area_level_1 = StringField('State', validators=[
        InputRequired()
    ])
    postal_code = StringField('ZIP Code', validators=[
        InputRequired(),
        Length(5)
    ])

    submit = SubmitField('Add Resource')
