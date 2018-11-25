from app.auth.models import User


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

