from .. import db


class Zipcode(db.Model):
    __tablename__ = 'zip_codes'
    id = db.Column(db.Integer, primary_key=True)
    zip_code = db.Column(db.String, unique=True)
    users = db.relationship('User', backref='zipcode', lazy='dynamic')
    resources = db.relationship('Resource', backref='zipcode', lazy='dynamic')

    def __repr__(self):
        return '<ZIPCode \' %s \'>' % self.zip_code


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    # USPS Addressing Standards: http://pe.usps.com/text/pub28/28c2_001.htm
    recipient_line = db.Column(db.Text)         # ABC MOVERS
    delivery_address_line = db.Column(db.Text)  # 1500 E MAIN AVE STE 201
    city = db.Column(db.Text)
    state = db.Column(db.String(2))
    zip_code_id = db.Column(db.Integer, db.ForeignKey('zip_code.id'))

    def __repr__(self):
        return '<Address \'%s\'>' % self.receipt_line
