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


class ResourceReview(db.Model):
    __tablename__ = 'resource_reviews'
    id = db.Column(db.Integer, primary_key=True)
    resource = db.relationship('Resource', backref='resource_review',
                               lazy='joined', uselist=False)
    timestamp = db.Column(db.DateTime)
    user = db.relationship('User', backref='user', lazy='joined',
                           uselist=False)
    content = db.Column(db.Text)
    rating = db.Column(db.Integer)
    count_likes = db.Column(db.Integer, default=0)
    count_dislikes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Resource Review \'%s\' \'%s\'>' % self.resource, self.content
