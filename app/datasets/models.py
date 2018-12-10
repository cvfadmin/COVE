from app import db, whooshee
import datetime


tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('dataset_id', db.Integer, db.ForeignKey('datasets.id'), primary_key=True)
)


@whooshee.register_model('name', 'description')
class Dataset(db.Model):
    __tablename__ = "datasets"
    id = db.Column(db.Integer, primary_key=True)
    is_approved = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(1000), nullable=False)
    url = db.Column(db.String(1000), nullable=False)
    thumbnail = db.Column(db.String(1000), nullable=True)
    description = db.Column(db.Text, nullable=False)
    license = db.Column(db.String(256), nullable=True)
    citation = db.Column(db.String(1000), nullable=False)
    year_created = db.Column(db.Integer, nullable=True)
    size = db.Column(db.String(256), nullable=True)
    num_cat = db.Column(db.String(256), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'),  nullable=False)
    owner = db.relationship('User', backref='datasets', lazy=True)

    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('datasets', lazy=True))


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
