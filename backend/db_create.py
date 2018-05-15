#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm.mapper import configure_mappers

from application import app, db
from application.models import Base
from application.models.dataset import Dataset, Pending_Dataset
from application.models.datasample import Datasample, DatasampleImage
from application.models.category import Category
from application.models.annotation import Annotation, Image_cat, BoundingBox
from application.models.relation import DatasetAnnCatAssoc, Dataset_Institution, Dataset_Task, Dataset_Datatype, Dataset_Topic, Dataset_Annotation,  Dataset_Keyword, Dataset_Conference, Dataset_Citation
from application.models.user import User, Request

# from application.models.relation import DatasetAnnCatAssoc

with app.test_request_context():
    Base.metadata.drop_all(bind=db.engine)
    configure_mappers() 
    Base.metadata.create_all(bind=db.engine)
    user = User(username='cove_admin')
    user.hash_password('coveadmin')
    db.session.add(user)
    db.session.commit()