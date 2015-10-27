from .. import db


class ZIPCode(db.Model):
    __tablename__ = 'ZIPCodes'
    id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.Integer, unique=True)
    users = db.relationship('ZIPCode', backref='user', lazy='dynamic')
    resources = db.relationship('ZIPCode', backref='resource', lazy='dynamic')

    def __repr__(self):
        return '<ZIPCode \' %s \'>' % self.zipcode


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    # http://pe.usps.com/text/pub28/28c2_001.htm
    recipient_line = db.Column(db.Text)         # ABC MOVERS
    delivery_address_line = db.Column(db.Text)  # 1500 E MAIN AVE STE 201
    city = db.Column(db.Text)
    state = db.Column(db.String(2))
    zip_code = db.relationship('ZIPCode', backref='address', lazy='dynamic')

    def __repr__(self):
        return '<Address \'%s\'>' % self.receipt_line
