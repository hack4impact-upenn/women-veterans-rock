from .. import db

user_tag_associations_table = db.Table(
    'user_tag_associations', db.Model.metadata,
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

resource_tag_associations_table = db.Table(
    'resource_tag_associations', db.Model.metadata,
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('resource_id', db.Integer, db.ForeignKey('resources.id'))
)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    users = db.relationship('User', secondary=user_tag_associations_table,
                            backref='tags', lazy='dynamic')
    resources = db.relationship('Resource',
                                secondary=resource_tag_associations_table,
                                backref='tags', lazy='dynamic')
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'tag',
        'polymorphic_on': type
    }

    def __init__(self, name):
        """
        If possible, the helper methods get_by_name and create_tag
        should be used instead of explicitly using this constructor.
        """
        self.name = name

    @staticmethod
    def get_by_name(name):
        """Helper for searching by Tag name."""
        result = Tag.query.filter_by(name=name).first()
        return result

    def __repr__(self):
        return '<Tag \'%s\'>' % self.name


class ResourceCategoryTag(Tag):
    __tablename__ = 'resource_category_tags'
    id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'resource_category_tag',
    }


class AffiliationTag(Tag):
    __tablename__ = 'affiliation_tags'
    id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'affiliation_tag',
    }
