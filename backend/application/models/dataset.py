#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy_utils.types import TSVectorType

from application.models import db, Base
#from application.models.relation import sample_to_set, DatasetAnnCatAssoc
from application.models.relation import DatasetAnnCatAssoc, Dataset_Institution, Dataset_Task, Dataset_Datatype, Dataset_Topic, Dataset_Annotation, Dataset_Keyword, Dataset_Conference, Dataset_Citation


class Dataset(Base):
    __tablename__ = "dataset"
    id_ = sa.Column(sa.Integer, nullable=False, primary_key=True, autoincrement=True)
    is_approved = sa.Column(sa.Boolean)
    name = sa.Column(sa.String(1000), nullable=False)
    url = sa.Column(sa.String(1000), nullable=False)
    thumbnail = sa.Column(sa.String(1000), nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    license = sa.Column(sa.String(256), nullable=True)
    is_local = sa.Column(sa.Boolean, nullable=False)
    creator = sa.Column(sa.String(1000), nullable= False)
    year = sa.Column(sa.Integer, nullable= True)
    size = sa.Column(sa.String(256), nullable = True)
    num_cat = sa.Column(sa.String(256), nullable = True)
    contact_name = sa.Column(sa.String(256), nullable=False)
    contact_email = sa.Column(sa.String(256), nullable=False)
    notes = sa.Column(sa.Text, nullable=False)
    related_paper = sa.Column(sa.Text, nullable=True)
    #datasamples = sa.orm.relationship("Datasample", secondary=sample_to_set, \
    #                        backref=sa.orm.backref("dataset", lazy="dynamic"))
    datasamples = sa.orm.relationship("Datasample", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset")) 
    institutions = sa.orm.relationship("Dataset_Institution", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset"))
    tasks = sa.orm.relationship("Dataset_Task", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset"))
    datatypes = sa.orm.relationship("Dataset_Datatype", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset"))
    topics = sa.orm.relationship("Dataset_Topic", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset"))
    annotation_types = sa.orm.relationship("Dataset_Annotation", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset"))
    keywords = sa.orm.relationship("Dataset_Keyword", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset"))
    citations = sa.orm.relationship("Dataset_Citation", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset"))
    conferences = sa.orm.relationship("Dataset_Conference", cascade="all, delete-orphan", \
                                        backref=sa.orm.backref("dataset"))
    # categories = sa.orm.relationship("DatasetAnnCatAssoc", backref="dataset")
    #assoc = sa.orm.relationship("DatasetAnnCatAssoc", backref="dataset", primaryjoin=id_ == DatasetAnnCatAssoc.set_id)
    assoc = sa.orm.relationship("DatasetAnnCatAssoc", backref="dataset")
    search_vector = sa.Column(TSVectorType('name', 'description', 'creator', 'notes', 'conference'))


    __mapper_args__ = {
                'polymorphic_identity': True,
                'polymorphic_on': is_approved
    }

    def __init__(self, name="", url="", thumbnail="", description="", license="", \
                 is_local=False, creator="", year="", size="", num_cat='', contact_name="", \
                 contact_email="", notes="", related_paper=""):
        self.name = name
        self.url = url
        self.thumbnail = thumbnail
        self.description = description
        self.license = license
        self.is_local = is_local
        self.creator = creator
        self.year = year
        self.size = size
        self.num_cat = num_cat
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.notes = notes
        self.related_paper = related_paper
    
    def __repr__(self):
        return "<Dataset %r>" % self.name

    def __hash__(self):
        return self.id_

    def serialize(self, samples):
        return {
                "id": self.id_,
                "name": self.name,
                "url": self.url,
                "thumbnail": self.thumbnail,
                "description": self.description,
                "license": self.license,
                "is_local": self.is_local,
                "creator": self.creator,
                "year": self.year,
                "size": self.size,
                "num_cat": self.num_cat,
                "contact_name": self.contact_name,
                "contact_email": self.contact_email,
                "notes": self.notes,
                "related_paper": self.related_paper,
                "institutions": [s.institution for s in self.institutions],
                "annotation_types": [s.annotation_type for s in self.annotation_types],
                "tasks": [s.task for s in self.tasks],
                "datatypes": [s.data_type for s in self.datatypes],
                "topics": [s.topic for s in self.topics],
                "keywords": [s.keyword for s in self.keywords],
                "conferences": [s.conference for s in self.conferences],
                "citations": [s.citation for s in self.citations],                
                "datasample_preview": [s.serialize() for s in samples]
                }
        
class Pending_Dataset(Dataset):
    __tablename__ = "pending_dataset"
    id_ = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'),  primary_key=True)
    edit_id = sa.Column(sa.Integer, nullable = True)
    __mapper_args__ = {
                'polymorphic_identity': False
    }
    def __init__(self, edit_id = None, name="", url="", thumbnail="", description="", license="", \
                 is_local=False, creator="", year="", size="", num_cat='', contact_name="", \
                 contact_email="", notes="", related_paper=""):
        self.name = name
        self.url = url
        self.thumbnail = thumbnail
        self.description = description
        self.license = license
        self.is_local = is_local
        self.creator = creator
        self.year = year
        self.size = size
        self.num_cat = num_cat
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.notes = notes
        self.related_paper = related_paper
        self.edit_id = edit_id

    def serialize(self, samples):
        return {
                "id": self.id_,
                "target_id": self.edit_id,
                "name": self.name,
                "url": self.url,
                "thumbnail": self.thumbnail,
                "description": self.description,
                "license": self.license,
                "is_local": self.is_local,
                "creator": self.creator,
                "year": self.year,
                "size": self.size,
                "num_cat": self.num_cat,
                "contact_name": self.contact_name,
                "contact_email": self.contact_email,
                "notes": self.notes,
                "related_paper": self.related_paper,
                "institutions": [s.institution for s in self.institutions],
                "annotation_types": [s.annotation_type for s in self.annotation_types],
                "tasks": [s.task for s in self.tasks],
                "datatypes": [s.data_type for s in self.datatypes],
                "topics": [s.topic for s in self.topics],
                "keywords": [s.keyword for s in self.keywords],
                "conferences": [s.conference for s in self.conferences],
                "citations": [s.citation for s in self.citations],                
                "datasample_preview": [s.serialize() for s in samples]
                }