from app import db
import datetime


class EditRequest(db.Model):
    __tablename__ = 'edit_requests'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_resolved = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref='edit_requests', lazy=True)

    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'), nullable=False)
    dataset = db.relationship('Dataset', backref='edit_requests', lazy=True)


class EditRequestMessage(db.Model):
    __tablename__ = 'edit_request_messages'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    has_owner_read = db.Column(db.Boolean, default=False)
    has_admin_read = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref='edit_request_messages', lazy=True)

    edit_request_id = db.Column(db.Integer, db.ForeignKey('edit_requests.id'), nullable=False)
    edit_request = db.relationship('EditRequest', backref='messages', lazy=True)
