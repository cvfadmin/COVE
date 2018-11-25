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
    contact_name = db.Column(db.String(256), nullable=False)
    contact_email = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    delete_requests = db.relationship('DeleteDatasetRequest', backref=db.backref('dataset'), lazy=True)
    edit_requests = db.relationship('EditDatasetRequest', backref=db.backref('dataset'), lazy=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('datasets', lazy=True))


class AddDatasetRequest(db.Model):
    __tablename__ = "add_dataset_request"
    id = db.Column(db.Integer, primary_key=True)
    is_approved = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(256), index=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    dataset_name = db.Column(db.String(1000), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    intro = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(1000), nullable=False)


class EditDatasetRequest(db.Model):
    __tablename__ = "edit_dataset_request"
    id = db.Column(db.Integer, primary_key=True)
    is_approved = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(256), index=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))


class DeleteDatasetRequest(db.Model):
    __tablename__ = "delete_dataset_request"
    id = db.Column(db.Integer, primary_key=True)
    is_approved = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(256), index=False, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
