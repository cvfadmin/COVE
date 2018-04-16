#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.views import MethodView
from flask import request
from flask.json import jsonify
from flask.ext.mail import Message 
from datetime import datetime
from application.views import mail
from application.models import db
from application.utils.dbmanage.model_query import ModelQuery
from re import sub
import os, shutil

#need to change when deployed
temp_folder_path = "/Users/Sheng/Desktop/cove_local/frontend/download/"
sample_path = "/Users/Sheng/Desktop/cove_local/frontend/samples/"

class GetDatasetAPI(MethodView):
    def get(self):
        dataset_id = request.args.get("dataset_id")
        category_name = request.args.get("category")
        annotation_type = request.args.get("annotation")
        error = None
        status = None
        value = None
        dataset = ModelQuery.getDatasetById(dataset_id, db.session)
        if dataset_id is None or dataset is None:
            status = 404
            error = "Cannot find Dataset"
        else:
            status = 200
            samples = ModelQuery.getDatasample(dataset.id_, category_name, annotation_type, 10, db.session)
            value = dataset.serialize(samples)
        response = jsonify(error=error, status=status, value=value)
        response.status_code = status
        return response

class DownloadAPI(MethodView):
    def post(self):
        id = 0
        data = request.get_json()
        data_list = data['list']
        recipient = data['email_address']
        tmp = sub('[^a-zA-Z0-9 \n\.]', '_', recipient)
        directory = temp_folder_path + tmp + '/'
        #directory = temp_folder_path + "test/"
        if not os.path.exists(directory):
            os.mkdir(directory)
        for q in data_list:
            src_path = sample_path + q[11:]
            ext = src_path.split('.')[-1]
            target = directory + str(id) + '.' + ext
            id += 1
            shutil.copyfile(src_path, target)
        shutil.make_archive(directory, 'zip', directory)
        filename = directory + 'test.zip'
        shutil.rmtree(directory)
        # subject = "Your download request is delivered!" 
        # message = "You can download the dataset you created at this link"
        # msg = Message(subject, sender="haohuan.wang2013@gmail.com", recipients=["liusheng@umich.edu"])
        # msg.body = message
        # msg.attach(filename, "zip")
        # mail.send(msg)
        response = jsonify(error=None, status=200, value=None)
        response.status_code = 200
        return response
