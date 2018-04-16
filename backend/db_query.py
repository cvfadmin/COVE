#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.orm.mapper import configure_mappers

from application import application, db
from application.models import Base
from application.models.dataset import Dataset
from application.models.datasample import Datasample, DatasampleImage
from application.models.category import Category
from application.models.annotation import Annotation, Image_cat, BoundingBox
from application.models.relation import DatasetAnnCatAssoc
from application.utils.dbmanage.model_query import ModelQuery 
from application.utils.filters.caltechFilter import CaltechFilter
from application.utils.filters.mscocoFilter import MSCocoFilter
from datetime import datetime

with application.test_request_context():
    #ret = ModelQuery.getLeafCats("vehicle", db.session)
    #print [r.serialize() for r in ret]
    #ret =  ModelQuery.getAnnoteType("boundingbox", db.session)
    #print len(ret)
    #print ret[0].serialize()
    # ret = db.session.query(DatasetAnnCatAssoc).filter_by(cat_id=ret[0].id_, anntype="boundingbox").all()
    # print ret[0].dataset.serialize(sampleret[0:5])
    # print [r.serialize() for r in ret]
    # samples = ModelQuery.getDatasample(ret[0].id_, "person", "boundingbox", 5, db.session)
    #value = ModelQuery.getQueryResults(None, "person", None, 6, db.session)
    #for i in xrange(len(value)):
    #    print value[i]
    #cat = db.session.query(Category).filter(Category.type_name == "image").first()
    #cats = ModelQuery.getLeafCats('elephant', db.session)
    #for c in cats:
    #    print c.serialize()
    #print cat.print_children()
    print ModelQuery.getCategoryByName('animals', db.session)
    #datasample = db.session.query(Datasample).join(Datasample.dataset).join(Annotation).\
    #                    filter(Dataset.id_ == 1, Annotation.category_id == 476).distinct().limit(6).all()
    #print datasample
    #datasample = db.session.query(Datasample).outerjoin(Annotation).\
    #                filter(Datasample.set_id == 6).\
    #                filter(Annotation.category_id == 97).distinct().limit(6).all()
    #print [d.path for d in datasample]
    #print db.session.execute('select * from datasample left outer join annotation on datasample.id_ = annotation.sample_id \
    #                   where datasample.set_id=%d and annotation.category_id=%d' % (6,97))
    #calout = CaltechFilter('outtest1/')
    #calout.outputSamples(datasample, 'bonsai')
    #cocoout = MSCocoFilter('outtest2/','x',0, 0)
    #cocoout.outputSamples(datasample)

    #print datasample
