#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm.mapper import configure_mappers

from application import application, db
from application.constants import CATEGORY_LIST
from application.models import Base
from application.models.dataset import Dataset
from application.models.datasample import Datasample, DatasampleImage
from application.models.category import Category
from application.models.annotation import Annotation, Image_cat, BoundingBox
from application.models.relation import DatasetAnnCatAssoc, Dataset_Institution
from application.utils.dbmanage.model_insert import ModelInsert, CategoryManage 
from application.utils.dbmanage.model_query import ModelQuery
from application.utils.dbmanage.model_modify import ModelModify
from application.utils.dbmanage.coco_insert import CocoInsert
from application.utils.dbmanage.caltech_insert import CaltechInsert
from datetime import datetime

with application.test_request_context():
    # rootCat = ModelInsert.insertCat("", None, db.session)
    # imageCat = ModelInsert.insertCat("image", rootCat, db.session)
    # videoCat = ModelInsert.insertCat("video", rootCat, db.session)
    # imageCat = db.session.query(Category).filter_by(type_name="image").first()
    # ModelInsert.insertDatasetAnnCatAssoc(testdst, imageCat, "boundingbox", db.session)
    # ret = db.session.query(DatasetAnnCatAssoc).filter_by(cat_id=rootCat.id_, anntype="boundingbox").first()
    # print ret.dataset.serialize([])
    # testsample = ModelInsert.insertDatasampleImage("","img",0,"",10,10,testdst, db.session)
    # testBBox = ModelInsert.insertBoundingBox([20,20,20,20], testsample, imageCat, db.session)
    # cinsert = CocoInsert("coco/", "val2014", -1, -1, db.session)
    # cinsert.insertAll(imageCat)
    calinsert = CaltechInsert("caltech256/", "Caltech 256", db.session)
    calinsert.insertAll()
    calinsert2 = CaltechInsert("caltech101/", "Caltech 101", db.session)
    calinsert2.insertAll()
    db.session.commit()

