from .. import db


class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    address = db.relationship('Address', backref='resource', lazy='joined',
                              uselist=False)
    description = db.Column(db.Text)
    website = db.Column(db.Text)
    reviews = db.relationship('Review', backref='resource', lazy='dynamic')

    def __repr__(self):
        return '<Resource \'%s\'>' % self.name


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
