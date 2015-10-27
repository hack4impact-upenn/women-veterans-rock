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
