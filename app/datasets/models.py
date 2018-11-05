from app import db
import datetime


class Dataset(db.Model):
    __tablename__ = "datasets"
    id = db.Column(db.Integer, primary_key=True)
    is_approved = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(1000), nullable=False)
    url = db.Column(db.String(1000), nullable=False)
    thumbnail = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.Text, nullable=False)
    license = db.Column(db.String(256), nullable=True)
    is_local = db.Column(db.Boolean, nullable=False)
    creator = db.Column(db.String(1000), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    size = db.Column(db.String(256), nullable=True)
    num_cat = db.Column(db.String(256), nullable=True)
    contact_name = db.Column(db.String(256), nullable=False)
    contact_email = db.Column(db.String(256), nullable=False)
    notes = db.Column(db.Text, nullable=False)
    related_paper = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    delete_requests = db.relationship('DeleteDatasetRequest', backref='dataset', lazy=True)


class AddDatasetRequest(db.Model):
    __tablename__ = "add_dataset_request"
    id = db.Column(db.Integer, primary_key=True)
    is_approved = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(256), index=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    dataset_name = db.Column(db.String(1000), nullable=False)
    salt = db.Column(db.String(64), nullable=True)
    year = db.Column(db.Integer, nullable= False)
    intro = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(1000), nullable=False)


class DeleteDatasetRequest(db.Model):
    __tablename__ = "delete_dataset_request"
    id = db.Column(db.Integer, primary_key=True)
    is_approved = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(256), index=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False)
