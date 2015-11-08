from .. import db


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    users = db.relationship('User', backref='tag', lazy='dynamic')
    resources = db.relationship('Resource')
    addresses = db.relationship('Address', backref='zip_code', lazy='dynamic')

    def __repr__(self):
        return '<ZIPCode \'%s\'>' % self.zip_code
