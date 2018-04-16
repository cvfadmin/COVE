#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    anntype = sa.Column(sa.String(128), nullable=False)
    # cat = sa.orm.relationship("Category", backref="dataset_assocs")

class Dataset_Task(Base):
    __tablename__ = 'dataset_task'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    task = sa.Column(sa.String(128), nullable=False, primary_key = True)

class Dataset_Datatype(Base):
    __tablename__ = 'dataset_datatype'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    data_type = sa.Column(sa.String(128), nullable=False, primary_key = True)

class Dataset_Topic(Base):
    __tablename__ = 'dataset_topic'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    topic = sa.Column(sa.String(128), nullable=False, primary_key = True)

class Dataset_Annotation(Base):
    __tablename__ = 'dataset_annoataion'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    annotation_type = sa.Column(sa.String(128), nullable=False, primary_key = True)

class Dataset_Thumbnail(Base):
    __tablename__ = 'dataset_thumbnail'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    thumbnail = sa.Column(sa.String(128), nullable=False, primary_key = True)

class Dataset_Institution(Base):
    __tablename__ = 'dataset_institution'
    set_id = sa.Column(sa.Integer, sa.ForeignKey('dataset.id_'), primary_key=True)
    institution = sa.Column(sa.String(128), nullable=False, primary_key = True)
