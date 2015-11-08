from flask.ext.wtf import Form
from wtforms.fields import (
    StringField,
    SubmitField
)
from wtforms.validators import InputRequired, Length
from wtforms import ValidationError
from urlparse import urlparse


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

    def validate_website(self, field):
        """ https://docs.python.org/2/library/urlparse.html
        urlparse recognizes a netloc only if it is properly introduced by '//'.
        Otherwise the input is presumed to be a relative URL and thus to start
        with a path component.
        """
        print field.data
        if field.data:
            o = urlparse(field.data)
            print o
            if not (o.netloc and o.path):
                raise ValidationError('Website is invalid.')
