from .. import db


class ZIPCode(db.Model):
    __tablename__ = 'zip_codes'
    id = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.String(5), unique=True)
    users = db.relationship('User', backref='zip_code', lazy='dynamic')
    addresses = db.relationship('Address', backref='zip_code', lazy='dynamic')

    def __repr__(self):
        return '<ZIPCode \'%s\'>' % self.zip_code


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)         # ABC MOVERS
    street_address = db.Column(db.Text)  # 1500 E MAIN AVE STE 201
    city = db.Column(db.Text)
    state = db.Column(db.String(2))
    zip_code_id = db.Column(db.Integer, db.ForeignKey('zip_codes.id'))
    resources = db.relationship('Resource', backref='address', lazy='dynamic')

    def __repr__(self):
        return '<Address \'%s\'>' % self.name
