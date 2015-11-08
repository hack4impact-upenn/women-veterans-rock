from .. import db

users_association_table = db.Table(
    'users_association', db.Model.metadata,
    db.Column('tags_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
)

resources_association_table = db.Table(
    'resources_association', db.Model.metadata,
    db.Column('tags_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('resources_id', db.Integer, db.ForeignKey('resources.id'))
)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    users = db.relationship('User', secondary=users_association_table,
                            backref='tags', lazy='dynamic')
    resources = db.relationship('Resource',
                                secondary=resources_association_table,
                                backref='tags', lazy='dynamic')

    def __repr__(self):
        return '<Tag \'%s\'>' % self.name
