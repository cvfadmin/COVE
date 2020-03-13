from app import db
import datetime
from app.datasets.search import SearchableMixin
from app.lib.ES_docs import ES_DATASET_DOC


# Associative table to hold the many-many relationship between datasets and tags
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('dataset_id', db.Integer, db.ForeignKey('datasets.id'), primary_key=True)
)


class Dataset(SearchableMixin, db.Model):
    __tablename__ = "datasets"
    __searchable__ = ['name', 'description', 'cite_title', 'cite_authors', 'cite_venue', 'cite_year', 'old_citation']
    __doc__ = ES_DATASET_DOC
    id = db.Column(db.Integer, primary_key=True)
    is_approved = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(1000), nullable=False)
    url = db.Column(db.String(1000), nullable=False)
    thumbnail = db.Column(db.String(1000), nullable=True)
    description = db.Column(db.Text, nullable=False)
    license = db.Column(db.String(256), nullable=True)
    year_created = db.Column(db.Integer, nullable=True)
    size = db.Column(db.String(256), nullable=True)
    num_cat = db.Column(db.String(256), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'),  nullable=False)
    owner = db.relationship('User', backref='datasets', lazy=True)

    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('datasets', lazy=True))

    # Citation Fields
    cite_title = db.Column(db.String(1000), nullable=True)
    cite_authors = db.Column(db.String(1000), nullable=True)
    cite_venue = db.Column(db.String(1000), nullable=True)
    cite_year = db.Column(db.Integer, nullable=True)
    open_access_link = db.Column(db.String(1000), nullable=True)

    # Old Citation Field
    old_citation = db.Column(db.String(1000), nullable=True)


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
