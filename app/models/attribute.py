from .. import db

user_tag_associations_table = db.Table(
    'user_tag_associations', db.Model.metadata,
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

resource_tag_associations_table = db.Table(
    'resource_tag_associations', db.Model.metadata,
    db.Column('resource_tag_associations', db.Integer,
              db.ForeignKey('tags.id')),
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

    def __repr__(self):
        return '<Tag \'%s\'>' % self.name
