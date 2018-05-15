#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import sqlalchemy as sa
from application.models import db, Base

# sample_to_set = sa.Table('sample_to_set', Base.metadata,
#         sa.Column('set_id', sa.Integer, sa.ForeignKey('dataset.id_')),
#         sa.Column('sample_id', sa.Integer, sa.ForeignKey('datasample.id_'))
#         )

class DatasetAnnCatAssoc(Base):
    __tablename__ = 'dataset_ann_cat_assoc'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    cat_id = sa.Column(sa.Integer, sa.ForeignKey('category.id_'), primary_key=True)
    anntype = sa.Column(sa.String(1000), nullable=False)
    # cat = sa.orm.relationship("Category", backref="dataset_assocs")

class Dataset_Task(Base):
    __tablename__ = 'dataset_task'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    task = sa.Column(sa.String(1000), nullable=False, primary_key = True)

class Dataset_Datatype(Base):
    __tablename__ = 'dataset_datatype'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    data_type = sa.Column(sa.String(1000), nullable=False, primary_key = True)

class Dataset_Topic(Base):
    __tablename__ = 'dataset_topic'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    topic = sa.Column(sa.String(1000), nullable=False, primary_key = True)

class Dataset_Annotation(Base):
    __tablename__ = 'dataset_annotation'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    annotation_type = sa.Column(sa.String(1000), nullable=False, primary_key = True)

class Dataset_Keyword(Base):
    __tablename__ = 'dataset_keyword'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    keyword = sa.Column(sa.String(1000), nullable=False, primary_key = True)
    
class Dataset_Citation(Base):
    __tablename__ = 'dataset_citation'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    citation = sa.Column(sa.String(1000), nullable=False, primary_key = True)

class Dataset_Conference(Base):
    __tablename__ = 'dataset_conference'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    conference = sa.Column(sa.String(1000), nullable=False, primary_key = True)

class Dataset_Institution(Base):
    __tablename__ = 'dataset_institution'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    institution = sa.Column(sa.String(1000), nullable=False, primary_key = True)