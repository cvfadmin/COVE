#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sqlalchemy_searchable import search
from application.models.category import Category
from application.models.annotation import Annotation, Image_cat, BoundingBox
from application.models.datasample import Datasample, DatasampleImage
from application.models.dataset import Dataset, Pending_Dataset
from application.models.relation import DatasetAnnCatAssoc, Dataset_Institution, Dataset_Task, Dataset_Datatype, Dataset_Topic, Dataset_Annotation,  Dataset_Keyword, Dataset_Conference, Dataset_Citation
from application.models.user import Request, AddRequest, EditRequest, DeleteRequest, User
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
    def insertRequest(email, firstname, lastname, r_type, target_id, dataset_name, intro, reason, url, session):
        rqst = None
        message = ""
        err = 0
        if r_type == "add":
            rqst = session.query(AddRequest).filter_by(email = email, dataset_name = dataset_name).first()
            if not rqst:
                rqst = AddRequest(firstname, lastname, email, dataset_name, intro, url)
                session.add(rqst)
                message = "Request sent, we will send a link to your email upon approval. Thank you for your support."
            else:
                message = "You have an existing request to add a dataset. Please wait for our response on the pending request before proceeding."
                err = 1
        elif r_type == "delete":
            rqst = DeleteRequest(firstname, lastname, email, target_id, dataset_name, reason)
            session.add(rqst)
            message = "We will review your request. Thank you for your support."
        elif r_type == "edit":
            rqst = session.query(EditRequest).filter_by(email = email, target_id = target_id).first()
            if not rqst:
                rqst = EditRequest(firstname, lastname, email, target_id, dataset_name)
                session.add(rqst)
                message = "Request sent, we will send a link to your email upon approval. Thank you for your support."
            else:
                message = "You have an existing request to edit a dataset. Please wait for our response on the pending request before proceeding."
                err = 1
        return err, message, rqst

    @staticmethod
    def insertDataset(name, is_approved, edit_id, url, thumbnail, description, license, is_local, creator, year, size,\
            num_cat, contact_name, contact_email, notes, related_paper, citations, conferences, keywords, \
            tasks, datatypes, topics, annotation_types, institutions, \
            session):
        dst = None
        if is_approved:
            dst = Dataset(name, url, thumbnail, description, license, is_local, creator, year, size,\
              num_cat, contact_name, contact_email, notes, related_paper)
        else:
            dst = Pending_Dataset(edit_id, name, url, thumbnail, description, license, is_local, creator, year, size,\
                num_cat, contact_name, contact_email, notes, related_paper)
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
        for val in conferences:
            ds_conf = Dataset_Conference(conference = val, dataset = dst)
            session.add(ds_conf)
        for val in citations:
            ds_cit = Dataset_Citation(citation = val, dataset = dst)
            session.add(ds_cit)
        session.add(dst)
        session.commit()
        return dst