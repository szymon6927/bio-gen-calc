from flask_login import UserMixin
from ..database import db


class Page(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    is_active = db.Column(db.Boolean(), default=True, unique=False)
    breadcrumbs = db.Column(db.String(220))
    seo_title = db.Column(db.String(85))
    seo_desc = db.Column(db.String(180))
    seo_keywords = db.Column(db.String(200))
    text = db.Column(db.UnicodeText)
    desc = db.Column(db.UnicodeText)

    def __unicode__(self):
        return self.name


# Create user model.
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    # Flask-Login integration
    # NOTE: is_authenticated, is_active, and is_anonymous
    # are methods in Flask-Login < 0.3.0
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<User: {}>'.format(self.login)
