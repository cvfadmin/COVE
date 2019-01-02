from app import ma
from app.datasets.schemas import DatasetSchema
from .models import User
import flask_marshmallow.sqla as sqla


class UserSchema(sqla.ModelSchema):
    class Meta:
        model = User

    datasets = ma.Nested(DatasetSchema, many=True)


user_schema = UserSchema()
