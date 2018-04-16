#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy_utils.types import TSVectorType

from application.models import db, Base
from application.models.relation import DatasetAnnCatAssoc

class Category(Base):
    __tablename__ = 'category'
    # need to modify the supercategory
    id_ = sa.Column(sa.Integer, nullable=False, primary_key=True, autoincrement=True)
    supercategory_id = sa.Column(sa.Integer, sa.ForeignKey(id_))
    type_name = sa.Column(sa.String(128), unique=True, nullable=False)
    search_vector = sa.Column(TSVectorType('type_name'))

    annotations = sa.orm.relationship("Annotation", cascade="all, delete-orphan", \
                                backref=sa.orm.backref("category"))
    subcategory = sa.orm.relationship("Category", cascade="all, delete-orphan",
                                backref=sa.orm.backref("supercategory", remote_side=id_))
                                #collection_class=sa.orm.collections.attribute_mapped_collection('type_name'))
    assoc = sa.orm.relationship("DatasetAnnCatAssoc", backref="category")

    def __init__(self, typename, supercategory=None):
        self.type_name = typename 
        self.supercategory = supercategory

    def __repr__(self):
        return "<Category %r>" % self.type_name

    def print_children(self, level=0):
        ret = "\t"*level+repr(self.type_name)+"\n"
        for child in self.subcategory:
            ret += child.print_children(level+1)
        return ret 

    def serialize(self):
        return {
                "id": self.id_,
                "label": self.type_name,
                }

