from app import db
import datetime
import secrets


class CreateDatasetKey(db.Model):
    __tablename__ = "create_dataset_key"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


def create_key():
    return secrets.token_urlsafe(32)
