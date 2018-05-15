#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sets import Set
from sqlalchemy_searchable import search
from application.models.category import Category
from application.models.annotation import Annotation, Image_cat, BoundingBox
from application.models.datasample import Datasample, DatasampleImage
from application.models.dataset import Dataset, Pending_Dataset
from application.models.relation import DatasetAnnCatAssoc
from application.utils.dbmanage.model_query import ModelQuery

class ModelModify():

    @staticmethod
    def changeCatSuperCat(catname, supercat, session):
        cat = ModelQuery.getCategoryByName(catname, session)
        if cat is not None:
            cat.supercategory = supercat
        else:
            print "cannot find %s, skip" % catname
