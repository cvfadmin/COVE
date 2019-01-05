from .models import User
from app.datasets.models import Dataset


class AdminOnly:

    @staticmethod
    def has_permission(username):
        if username is None:
            return False

        user = User.query.filter_by(username=username).first()

        # if there is no user by this username
        if user is None:
            return False

        return user.is_admin


class AdminOrDatasetOwner:

    @staticmethod
    def has_permission(username, dataset_id):
        if username is None or dataset_id is None:
            return False

        user = User.query.filter_by(username=username).first()

        if user is None:
            return False
        if user.is_admin:
            return True

        dataset = Dataset.query.filter_by(id=dataset_id, owner=user).first()

        # if there is no user by this username
        if dataset is None:
            return False

        return True

