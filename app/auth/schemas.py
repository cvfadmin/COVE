from .models import User
import flask_marshmallow.sqla as sqla


class UserSchema(sqla.ModelSchema):
    class Meta:
        model = User


user_schema = UserSchema()
