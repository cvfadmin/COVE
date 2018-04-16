#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sets import Set
from sqlalchemy_searchable import search
from application.models.category import Category
from application.models.annotation import Annotation, Image_cat, BoundingBox
from application.models.datasample import Datasample, DatasampleImage
from application.models.dataset import Dataset
from application.models.relation import DatasetAnnCatAssoc, Dataset_Institution, Dataset_Task, Dataset_Datatype, Dataset_Topic, Dataset_Annotation, Dataset_Thumbnail
from application.models.user import Request, User
from application.utils.dbmanage.model_query import ModelQuery
from application.constants import CAT_SUB

class ModelInsert():
    # New features to be added
    # for different datasample format like videos, we need to define
    # def insertDatasampleVideo():


    @staticmethod
    def insertCat(name, supercat, session):
        with session.no_autoflush:
            cat = session.query(Category).filter_by(type_name=name).first()
        if not cat:
            cat = Category(name, supercat)
            session.add(cat)
        return cat


    @staticmethod
    def insertRequest(email, firstname, lastname, session):
        rqst = session.query(Request).filter_by(email = email).first()
        if not rqst:
            rqst = Request(email, firstname, lastname)
            session.add(rqst)
        return rqst

    @staticmethod
    def insertDataset(name, url, description, license, is_local, creator, year, size,\
            contact_name, contact_email, notes, related_paper, conference, tasks,\
            datatypes, topics, annotation_types, thumbnails, institutions, \
            session):
        dst = Dataset(name, url, description, license, is_local, creator, year, size,\
                contact_name, contact_email, notes, related_paper, conference)
        for val in keywords:
            ds_kw = Dataset_Keyword(keyword = val, dataset = dst)
            session.add(ds_kw)
        for val in topics:
            ds_tp = Dataset_Topic(topic = val, dataset = dst)
            session.add(ds_tp)
        for val in tasks:
            ds_tsk = Dataset_Task(task = val, dataset = dst)
            session.add(ds_tsk)
        for val in datatypes:
            ds_dtp = Dataset_Datatype(data_type = val, dataset = dst)
            session.add(ds_dtp)
        for val in annotation_types:
            ds_atp = Dataset_Annotation(annotation_type = val, dataset = dst)
            session.add(ds_atp)
        for val in institutions:
            ds_insti = Dataset_Institution(institution = val, dataset = dst)
            session.add(ds_insti)
        for val in thumbnails:
            ds_thumb = Dataset_Thumbnail(thumbnail = val, dataset = dst)
            session.add(ds_thumb)
        session.add(dst)
        # with session.no_autoflush:
        #     dst = session.query(Dataset).filter_by(name=name).first()
        return dst

    @staticmethod
    def insertDatasampleImage(path, format_, size, comment, width, height, ds, session):
        dsi = DatasampleImage(path, format_, size, comment, width, height)
        ds.datasamples.append(dsi)
        session.add(dsi)
        return dsi

    @staticmethod
    def insertBoundingBox(xywh, datasample_id, category, session):
        ann = BoundingBox(xywh, datasample_id, category.id_)
        session.add(ann)
        return ann

    @staticmethod
    def insertImageCat(datasample_id, category, session):
        ann = Image_cat(datasample_id.id_, category.id_)
        session.add(ann)
        return ann

    @staticmethod
    def insertDatasetAnnCatAssoc(dst, cat, typename, session):
        a = DatasetAnnCatAssoc(set_id=dst.id_, cat_id=cat.id_, anntype=typename)
        with session.no_autoflush:
            dst.assoc.append(a)
            cat.assoc.append(a)
        session.add(a)
        return a

class CategoryManage():

    def __init__(self, session):
        self.to_insert = [] 
        self.session = session
        self.top = ModelQuery.getCategoryByName("", session)

    def addInsertList(self, category_to_insert):
        if isinstance(category_to_insert, list):
            self.to_insert = category_to_insert

    def printTree(self):
        print "==================================="
        print "The Current Category Tree Structure"
        print self.top.print_children()
        print "==================================="

    def keyboardInput(self, catname):
        supercatname = None
        supercat = None
        while True:
            supercatname = raw_input("Please type the supercategory of the inserting category %s." % catname)
            if supercatname  == "x":
                print "Skip this Category"
                return None
            else:
                print "Insert this category to %s" % supercatname
                supercat = ModelQuery.getCategoryByName(supercatname, self.session)
                if supercat is not None:
                    return supercat

    def run(self):
        for c in self.to_insert:
            with self.session.no_autoflush:
                check = ModelQuery.getCategoryByName(c, self.session)
            # check = ModelQuery.getCategoryByName(c, self.session)
            if check is not None:
                continue
            # self.printTree()
            #  Require us to insert supercat previous to the subcats
            # supercat = self.keyboardInput(c)
            supercat = None
            if c not in CAT_SUB:
                supercat = self.keyboardInput(c)
                CAT_SUB[c] = supercat.type_name
            else:
                supercat = ModelQuery.getCategoryByName(CAT_SUB[c], self.session)
            print supercat
            if supercat is not None:
                ModelInsert.insertCat(unicode(c), supercat, self.session)

