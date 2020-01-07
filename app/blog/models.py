from app.database import db


class Feed(db.Model):
    __tablename__ = 'feed'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    url = db.Column(db.String(120))


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    link = db.Column(db.String(120))
    pub_date = db.Column(db.DateTime)
    desc = db.Column(db.Text)
