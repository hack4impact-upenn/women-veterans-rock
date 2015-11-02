from .. import db


class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    website = db.Column(db.Text)

    def __repr__(self):
        return '<Resource \'%s\'>' % self.name
