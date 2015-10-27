from .. import db


class ZIPCode(db.Model):
    __tablename__ = 'ZIPCodes'
    id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.Integer, unique=True)
    users = db.relationship('ZIPCode', backref='user', lazy='dynamic')
    resources = db.relationship('ZIPCode', backref='resource', lazy='dynamic')

    def __repr__(self):
        return '<ZIPCode \' %s \'>' % self.zipcode
