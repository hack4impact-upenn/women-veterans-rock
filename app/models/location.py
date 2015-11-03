from .. import db
from geopy.geocoders import Nominatim


class ZIPCode(db.Model):
    __tablename__ = 'zip_codes'
    id = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.String(5), unique=True)
    users = db.relationship('User', backref='zip_code', lazy='dynamic')
    addresses = db.relationship('Address', backref='zip_code', lazy='dynamic')
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __init__(self, *args, **kwargs):
        super(db.Model, self).__init__(*args, **kwargs)
        getcoords = Nominatim()
        loc = getcoords.geocode(ZIPCode.zip_code)
        self.longitude = loc.longitude
        self.latitude = loc.latitude

    def __repr__(self):
        return '<ZIPCode \'%s\'>' % self.zip_code


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    # USPS Addressing Standards: http://pe.usps.com/text/pub28/28c2_001.htm
    recipient_line = db.Column(db.Text)         # ABC MOVERS
    delivery_address_line = db.Column(db.Text)  # 1500 E MAIN AVE STE 201
    city = db.Column(db.Text)
    state = db.Column(db.String(2))
    zip_code_id = db.Column(db.Integer, db.ForeignKey('zip_codes.id'))
    resources = db.relationship('Resource', backref='address', lazy='dynamic')

    def __repr__(self):
        return '<Address \'%s\'>' % self.receipt_line
