#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlalchemy as sa
from sets import Set
from sqlalchemy_searchable import search
from sqlalchemy import func, and_
from application.models.category import Category
from application.models.annotation import Annotation, Image_cat, BoundingBox
from application.models.datasample import Datasample, DatasampleImage
from application.models.dataset import Dataset
from application.models.relation import DatasetAnnCatAssoc, Dataset_Institution, Dataset_Task, Dataset_Datatype, Dataset_Topic, Dataset_Annotation, Dataset_Thumbnail

class ModelQuery():

    @staticmethod
    def getCategoryByName(name, session):
        cat = None
        if name is not None:
            cat =  session.query(Category).filter(Category.type_name == name).first()
        return cat

    @staticmethod
    def getDatasetByName(name, session):
        datasets = None
        if name is not None:
            datasets = session.query(Dataset).filter(Dataset.name == name).all()
        return datasets

    @staticmethod
    def getDatasetById(set_id, session):
        datasets = None
        if set_id is not None:
            datasets = session.query(Dataset).filter(Dataset.id_ == int(set_id)).first()
        return datasets

    @staticmethod
    def getAnnotationByType(type_, session):
        anns = None
        if type_ is not None:
            anns = session.query(Annotation).filter(Annotation.type_ == type_).all()
        return anns

    @staticmethod
    def getLeafCats(category_name, session):
        iterate = []
        ret = []
        #cat = search(session.query(Category), category_name).first()
        cat = session.query(Category).filter(Category.type_name == category_name).first()
        if cat is not None:
            iterate.append(cat)
            while len(iterate) > 0:
                top = iterate[0]
                iterate.pop(0)
                if top.subcategory:
                    ret.append(top)
                    iterate.extend(top.subcategory)
                else:
                    ret.append(top)
            return ret
        return None

    @staticmethod
    def getDataset(dataset_name, category_name, annotation_type, conference, institution, session):
        # given dataset_name
        if dataset_name is not None:
            dataset = session.query(Dataset).filter(Dataset.name == dataset_name).all()
            return dataset

        datasets = None
        # given conference or institution, means only search for one key
        if conference is not None or institution is not None:
            if conference is not None:
                datasets = session.query(Dataset).filter(Dataset.conference == conference).all()
            else:
                datasets = session.query(Dataset).join(Dataset_Institution).filter(func.lower(Dataset_Institution.institution) == institution).all()
            return datasets

        if category_name is not None or annotation_type is not None:
            if category_name is None: #only search at annotation_type
                datasets = session.query(DatasetAnnCatAssoc).filter(DatasetAnnCatAssoc.anntype == annotation_type).all()
            elif annotation_type is None:
                cats = ModelQuery.getLeafCats(category_name, session)
                if cats is not None:
                    datasets = session.query(DatasetAnnCatAssoc).filter(sa.or_(DatasetAnnCatAssoc.cat_id == c.id_ for c in cats)).all()
            else:
                cats = ModelQuery.getLeafCats(category_name, session)
                if cats is not None:
                    datasets = session.query(DatasetAnnCatAssoc).filter(sa.or_(DatasetAnnCatAssoc.cat_id == c.id_ for c in cats),\
                        DatasetAnnCatAssoc.anntype == annotation_type).all()
        
        ret = Set(datasets)
        dataset = [] 
        if len(ret) != 0:
            dataset = session.query(Dataset).filter(sa.or_(Dataset.id_ == r.set_id for r in ret)).all()
        return dataset 

    @staticmethod
    def getDst(name, institution, year, conference, task, annotation_type, data_type, topic, paper, session):
        dst = session.query(Dataset)
        conditions = []
        if name != "":
            dst = dst.filter(Dataset.name == name).first()
            return dst
        print "here"
        if year != "":
            conditions.append(and_(Dataset.year == int(year)))
        if conference != "":
            conditions.append(and_(func.lower(Dataset.conference) == conference))
        if institution != "":
            dst = dst.join(Dataset_Institution)
            conditions.append(and_(func.lower(Dataset_Institution.institution) == institution))
        if topic != "":
            dst = dst.join(Dataset_Topic)
            conditions.append(and_(func.lower(Dataset_Topic.topic) == topic))
        if annotation_type != "":
            dst = dst.join(Dataset_Annotation)
            conditions.append(and_(func.lower(Dataset_Annotation.annotation_type) == annotation_type))
        if data_type != "":
            dst = dst.join(Dataset_Datatype)
            conditions.append(and_(func.lower(Dataset_Datatype.data_type) == data_type))
        if task != "":
            dst = dst.join(Dataset_Task)
            conditions.append(and_(func.lower(Dataset_Task.task) == task))
        if paper != "":
            conditions.append(and_(func.lower(Dataset.related_paper) == paper))
        dst = dst.filter(*conditions).all()
        return dst
        

    @staticmethod
    def getDatasample(set_id, category_name, annotation_type, ret_num, session):
        datasample = []
        if session.query(Dataset).filter(Dataset.id_ == set_id).first().is_local == False:
            return datasample
        if category_name is None and annotation_type is None:
            if ret_num < 0:
                datasample = session.query(Datasample).filter(Datasample.set_id == set_id).all()
            else:
                datasample = session.query(Datasample).filter(Datasample.set_id == set_id).distinct().limit(ret_num).all()
        elif category_name is None: #annotation_type is provided
            if ret_num < 0:
                datasample = session.query(Datasample).outerjoin(Annotation).\
                        filter(Datasample.set_id == set_id, Annotation.type_ == annotation_type).all()
            else:
                datasample = session.query(Datasample).outerjoin(Annotation).\
                        filter(Datasample.set_id == set_id, Annotation.type_ == annotation_type).distinct().limit(ret_num).all()

        else:
            cats = ModelQuery.getLeafCats(category_name, session)
            if cats is not None:
                #d = session.query(Datasample).filter(Datasample.dataset.any(id_ = set_id)).distinct().order_by(sa.asc(Datasample.id_)).all()
                if annotation_type is None: #category is provided
                    if ret_num < 0:
                        #datasample = session.query(Datasample).join(Annotation).\
                        #    filter(sa.and_(Datasample.id_ >= d[0].id_, Datasample.id_ <= d[-1].id_)).\
                        #    filter(sa.or_(Category.id_ == c.id_ for c in cats)).all()
                        datasample = session.query(Datasample).outerjoin(Annotation).\
                            filter(Datasample.set_id == set_id).\
                            filter(sa.or_(Annotation.category_id == c.id_ for c in cats)).all()

                    else:
                        print [c.id_ for c in cats]
                        print annotation_type
                        print set_id

                        #datasample = session.query(Datasample).join(Annotation).\
                        #    filter(sa.and_(Datasample.id_ >= d[0].id_, Datasample.id_ <= d[-1].id_)).\
                        #    filter(sa.or_(Annotation.category_id == c.id_ for c in cats)).distinct().limit(ret_num).all()
                        datasample = session.query(Datasample).outerjoin(Annotation).\
                            filter(Datasample.set_id == set_id).\
                            filter(sa.or_(Annotation.category_id == c.id_ for c in cats)).distinct().limit(ret_num).all()

                else: #both annotation_type and category are provided
                    if ret_num < 0:
                        #datasample = session.query(Datasample).join(Annotation).\
                        #    filter(sa.and_(Datasample.id_ >= d[0].id_, Datasample.id_ <= d[-1].id_)).\
                        #    filter(Annotation.type_ == annotation_type).\
                        #    filter(sa.or_(Category.id_ == c.id_ for c in cats)).all()
                        datasample = session.query(Datasample).outerjoin(Annotation).\
                            filter(Datasample.set_id == set_id, Annotation.type_ == annotation_type).\
                            filter(sa.or_(Annotation.category_id == c.id_ for c in cats)).all()
                    else:
                        #datasample = session.query(Datasample).join(Annotation).\
                        #    filter(sa.and_(Datasample.id_ >= d[0].id_, Datasample.id_ <= d[-1].id_)).\
                        #    filter(Annotation.type_ == annotation_type).\
                        #    filter(sa.or_(Category.id_ == c.id_ for c in cats)).distinct().limit(ret_num).all()
                        print [c.id_ for c in cats]
                        print annotation_type
                        print set_id
                        datasample = session.query(Datasample).outerjoin(Annotation).\
                            filter(Datasample.set_id == set_id, Annotation.type_ == annotation_type).\
                            filter(sa.or_(Annotation.category_id == c.id_ for c in cats)).distinct().limit(ret_num).all()

        return datasample

    @staticmethod
    def getQueryResults(dataset_name, category_name, annotation_type, conference, ret_num, session):
        dataset = ModelQuery.getDataset(dataset_name, category_name, annotation_type, conference, None, session)
        print dataset_name, category_name, annotation_type, conference, ret_num
        value = []
        for d in dataset:
            samples = ModelQuery.getDatasample(d.id_, category_name, annotation_type, ret_num, session)
            value.append(d.serialize(samples))
        return value

    @staticmethod
    def getDatasetResult(dataset_name, annotation, conference, institution, session):
        dataset = ModelQuery.getDataset(dataset_name, None, annotation, conference, institution, session)

