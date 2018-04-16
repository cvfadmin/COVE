#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy_utils.types import TSVectorType

from application.models import db, Base
#from application.models.relation import sample_to_set, DatasetAnnCatAssoc
from application.models.relation import DatasetAnnCatAssoc, Dataset_Institution, Dataset_Task, Dataset_Datatype, Dataset_Topic, Dataset_Annotation, Dataset_Thumbnail


class Dataset(Base):
    __tablename__ = "dataset"
    id_ = sa.Column(sa.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(256), unique=True, nullable=False)
    url = sa.Column(sa.String(256), nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    license = sa.Column(sa.String(256), nullable=True)
    is_local = sa.Column(sa.Boolean, nullable=False)
    creator = sa.Column(sa.String(256), nullable= True)
    year = sa.Column(sa.Integer, nullable= True)
    size = sa.Column(sa.Integer, nullable = True)
    contact_name = sa.Column(sa.String(256), nullable=False)
    contact_email = sa.Column(sa.String(256), nullable=False)
    notes = sa.Column(sa.Text, nullable=False)
    related_paper = sa.Column(sa.Text, nullable=True)
    conference = sa.Column(sa.Text, nullable=True)
    #datasamples = sa.orm.relationship("Datasample", secondary=sample_to_set, \
    #                        backref=sa.orm.backref("dataset", lazy="dynamic"))
    datasamples = sa.orm.relationship("Datasample", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset")) 
    contributers = sa.orm.relationship("Dataset_Institution", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset"))
    tasks = sa.orm.relationship("Dataset_Task", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset"))
    datatypes = sa.orm.relationship("Dataset_Datatype", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset"))
    topics = sa.orm.relationship("Dataset_Topic", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset"))
    annotation_types = sa.orm.relationship("Dataset_Annotation", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset"))
    thumbnails = sa.orm.relationship("Dataset_Thumbnail", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset"))
    # categories = sa.orm.relationship("DatasetAnnCatAssoc", backref="dataset")
    #assoc = sa.orm.relationship("DatasetAnnCatAssoc", backref="dataset", primaryjoin=id_ == DatasetAnnCatAssoc.set_id)
    assoc = sa.orm.relationship("DatasetAnnCatAssoc", backref="dataset")
    search_vector = sa.Column(TSVectorType('name', 'description', 'creator', 'notes', 'conference'))

    def __init__(self, name="", url="", description="", license="", is_local=False, \
            creator="", year=0, size=0, contact_name="", contact_email="", \
            notes="", related_paper="", conference=""):
        self.name = name
        self.url = url
        self.description = description
        self.license = license
        self.is_local = is_local
        self.creator = creator
        self.year = year
        self.size = size
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.notes = notes
        self.related_paper = related_paper
        self.conference = conference
    
    def __repr__(self):
        return "<Dataset %r>" % self.name

    def __hash__(self):
        return self.id_

    def serialize(self, samples):
        return {
                "id": self.id_,
                "name": self.name,
                "url": self.url,
                "description": self.description,
                "license": self.license,
                "is_local": self.is_local,
                "creator": self.creator,
                "year": self.year,
                "contact_name": self.contact_name,
                "contact_email": self.contact_email,
                "notes": self.notes,
                "related_paper": self.related_paper,
                "conference": self.conference,
                "institutions": [s.institution for s in self.contributers],
                "annotation_types": [s.annotation_type for s in self.annotation_types],
                "tasks": [s.task for s in self.tasks],
                "datatypes": [s.data_type for s in self.datatypes],
                "topics": [s.topic for s in self.topics],
                "thumbnails": [s.thumbnail for s in self.thumbnails],
                "datasample_preview": [s.serialize() for s in samples]
                }
