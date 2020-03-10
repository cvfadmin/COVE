from app import db
import datetime


class OwnershipRequest(db.Model):
    __tablename__ = 'ownership_requests'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_resolved = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref='ownership_requests', lazy=True)

    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'), nullable=False)
    dataset = db.relationship('Dataset', backref='ownership_requests', lazy=True)
