# Models
from .. import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    email = db.Column(db.Unicode(64))

    def __unicode__(self):
        return self.name


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(64))
    content = db.Column(db.UnicodeText)

    def __unicode__(self):
        return self.name