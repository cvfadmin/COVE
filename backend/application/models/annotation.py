#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy_utils.types import TSVectorType

from application.models import db, Base

class Annotation(Base):
    __tablename__ = 'annotation'
    id_ = sa.Column(sa.Integer, nullable=False, primary_key=True, autoincrement=True)
    category_id = sa.Column(sa.Integer, sa.ForeignKey('category.id_'))
    sample_id = sa.Column(sa.Integer, sa.ForeignKey('datasample.id_'))
    type_ = sa.Column(sa.String(128), nullable=False)
    search_vector = sa.Column(TSVectorType('type_'))

    __mapper_args__ = {
                'polymorphic_identity':'annotation',
                'polymorphic_on': type_
            }

    def __init__(self, typename, datasample, category):
        self.type_ = typename
        self.sample_id = datasample
        self.category_id = category
    
    def __repr__(self):
        return "<Annotation %r>" % self.type_

    def serialize(self):
        return {
                "id": self.id_,
                "type": self.type_
               }

class Image_cat(Annotation):
    __tablename__ = 'image_cat'
    id_ = sa.Column(sa.Integer, sa.ForeignKey('annotation.id_'), nullable=False, primary_key=True)
    __mapper_args__ = {
                'polymorphic_identity':'category'
            }
    def __init__(self, datasample, category):
        super(Image_cat, self).__init__("category", datasample, category)

class BoundingBox(Annotation):
    __tablename__ = 'boundingbox'
    id_ = sa.Column(sa.Integer, sa.ForeignKey('annotation.id_'), nullable=False, primary_key=True)
    xywh = sa.Column(sa.String(128), nullable=False)
    __mapper_args__ = {
                'polymorphic_identity':'boundingbox'
            }

    def __init__(self, xywh, datasample, category):
        super(BoundingBox, self).__init__("boundingbox", datasample, category)
        self.xywh = self.list_to_string(xywh)

    def __repr__(self):
        return "<BoundingBox %r>" % self.id_

    def serialize(self):
        return {
                 "id": self.id_,
                 "type": self.type_,
                 "coords": self.string_to_list(self.xywh)
                }

    def list_to_string(self, list_):
        if not list_:
            return
        tmp_str = ""
        for l in list_:
            # tmp_str+=l[0]+","+l[1]+" "
            tmp_str += str(l) + " "
        return tmp_str

    def string_to_list(self, coord_str):
        list_ = []
        temp_list = coord_str.split(' ')
        if temp_list[-1] == '':
            temp_list.pop()
        #for t in temp_list:
        #    res = t.split(',')
        #    if len(res) == 2:
        #        list_.append((int(res[0]), int(res[1])))
        for t in temp_list:
            list_.append(float(t))
        return list_

# class Segmentation(Annotation):
    # __tablename__ = 'segmentation'
