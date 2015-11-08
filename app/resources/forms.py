from flask.ext.wtf import Form
from wtforms.fields import (
    StringField,
    SubmitField
)
from wtforms.validators import InputRequired, Length


class ResourceForm(Form):
    name = StringField('Name', validators=[
        InputRequired(),
        Length(1, 64)
    ])
    description = StringField('Description', validators=[
        InputRequired(),
    ])
    website = StringField('Website')
    street_address = StringField('Street Address', validators=[
        InputRequired()
    ])
    city = StringField('City', validators=[
        InputRequired()
    ])
    state = StringField('State', validators=[
        InputRequired(),
        Length(2)
    ])
    zip_code = StringField('ZIP Code', validators=[
        InputRequired(),
        Length(5, 10)
    ])
    submit = SubmitField('Add Resource')
