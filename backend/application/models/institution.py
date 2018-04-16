# from datetime import datetime
# import sqlalchemy as sa
# from sqlalchemy_utils.types import TSVectorType

# from application.models import db, Base
# from application.models.relation import Dataset_Institution

# class Institution(Base):
# 	__tablename__ = "institution"
# 	id_ = sa.Column(sa.Integer, nullable=False, primary_key=True, autoincrement=True)
# 	name = name = sa.Column(sa.String(128), unique=True, nullable=False)

# 	assoc = sa.orm.relationship("Dataset_Institution", backref="institution")

# 	def __init__(self, insti_name):
# 		self.name = insti_name

# 	def __repr__(self):
# 		return "<Institution %r>" % self.name

# 	def serialize(self):
# 		return {
# 			"id" : self.id_,
# 			"name" : self.name
# 		}

