#!/usr/bin/env python
# -*- coding: utf-8 -*- import os
import sqlalchemy as sa
import os
from datetime import datetime
from application.models import db, Base
from application.constants import DATASET_DISPLAY_PATH

# for different datasample format, we need to create more polymorphics,
# class DatasampleVideo(Datasample):

class Datasample(Base):
    __tablename__ = "datasample"
    id_ = sa.Column(sa.Integer, nullable=False, primary_key=True, autoincrement=True)
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'))
    path = sa.Column(sa.String(128), nullable=False)
    type_ = sa.Column(sa.String(128), nullable=False) #img/video
    format_ = sa.Column(sa.String(128), nullable=False) #extension
    size = sa.Column(sa.Integer, nullable=False) #KB
    comment = sa.Column(sa.Text, nullable=False)
    annotations = sa.orm.relationship("Annotation", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("datasample")) 
                                        #collection_class=sa.orm.collections.attribute_mapped_collection('type_'))
    __mapper_args__ = {
                'polymorphic_identity': 'datasample',
                'polymorphic_on': type_
            }

    def __init__(self, path="", type_in="", format_in="", size=0, comment=""):
        self.path = path
        self.type_ = type_in
        self.format_ = format_in
        self.size = size
        self.comment = comment

    def __repr__(self):
        return "<Datasample %r: %r>" % (self.id_, self.path)

    def serialize(self):
        return {
                "id": self.id_,
                "path": os.path.join(DATASET_STORAGE_PATH, self.path),
                "type": self.type_,
                "format": self.format_,
                "size": self.size,
                "comment": self.comment,
                "annotation": list(set([a.type_ if a.type_ != "" else "Category" for a in self.annotations]))
                }

class DatasampleImage(Datasample):
    __tablename__ = "datasampleimage"
    id_ = sa.Column(sa.Integer, sa.ForeignKey('datasample.id_'), nullable=False, primary_key=True)
    width = sa.Column(sa.Integer, nullable=False)
    height = sa.Column(sa.Integer, nullable=False)
    __mapper_args__ = {
                'polymorphic_identity': 'datasampleimage'
            }

    def __init__(self, path="", format_in="", size=0, comment="", width=0, height=0):
        super(DatasampleImage, self).__init__(path, "datasampleimage", format_in, size, comment)
        self.width = width
        self.height = height

    def __repr__(self):
        return "<DatasampleImage %r>" % self.id_

    def serialize(self):
        return {
                "id": self.id_,
                "path": os.path.join(DATASET_DISPLAY_PATH, self.path),
                "type": self.type_,
                "width": self.width,
                "height": self.height,
                "format": self.format_,
                "size": self.size,
                "comment": self.comment,
                "annotation": list(set([a.type_ if a.type_ != "" else "NoAnnotation" for a in self.annotations]))
                }
