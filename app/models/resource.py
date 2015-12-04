from .. import db
from random import randint


class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    website = db.Column(db.Text)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews = db.relationship('ResourceReview', backref='resource',
                              lazy='dynamic')
    closed_resource_explanations = db.relationship(
        'ClosedResourceExplanation',
        backref='closed_resource_explanation')

    def __init__(self, name, description, website):
        self.name = name
        self.description = description
        self.website = website

    @staticmethod
    def get_by_resource(name, description, website):
        """Helper for searching by all resource fields."""
        result = Resource.query.filter_by(name=name,
                                          description=description,
                                          website=website).first()
        return result

    @staticmethod
    def create_resource(name, description, website):
        """
        Helper to create an Resource entry. Returns the newly created Resource
        or the existing entry if all resource fields are already in the table.
        """
        result = Resource.get_by_resource(name,
                                          description,
                                          website)
        if result is None:
            result = Resource(name=name,
                              description=description,
                              website=website)
            db.session.add(result)
            db.session.commit()
        return result

    @staticmethod
    def generate_fake(count=10):
        """Generate count fake Resources for testing."""
        from faker import Faker

        fake = Faker()

        # TODO: make sure fake resources have users and addresses
        for i in range(count):
            r = Resource(
                name=fake.name(),
                description=fake.text(),
                website=fake.url()
            )
            db.session.add(r)
            db.session.commit()

    def __repr__(self):
        return '<Resource \'%s\'>' % self.name


class ResourceReview(db.Model):
    __tablename__ = 'resource_reviews'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    content = db.Column(db.Text)
    rating = db.Column(db.Integer)  # 1 to 5
    count_likes = db.Column(db.Integer, default=0)
    count_dislikes = db.Column(db.Integer, default=0)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, timestamp, content, rating):
        self.timestamp = timestamp
        self.content = content
        self.rating = rating

    @staticmethod
    def generate_fake(count=10):
        """Generate count fake Reviews for testing."""
        from faker import Faker

        fake = Faker()

        # TODO: make sure fake reviews have users and resources
        for i in range(count):
            r = ResourceReview(
                timestamp=fake.date_time(),
                content=fake.text(),
                rating=randint(1, 5),
                count_likes=randint(1, 500),
                count_dislikes=randint(1, 500)
            )
            db.session.add(r)
            db.session.commit()

    def __repr__(self):
        return '<ResourceReview <Resource \'%s\'> \'%s\'>' %\
               (self.resource_id, self.content)


class ClosedResourceExplanation(db.Model):
    __tablename__ = 'closed_resource_explanations'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    connection = db.Column(db.Text)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, content, connection):
        self.content = content
        self.connection = connection

    def __repr__(self):
        return '<ClosedResourceExplanation <Resource \'%s\'> \'%s\'>' %\
               (self.resource_id, self.content)
