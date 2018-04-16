#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.views import MethodView
from flask import request
from flask.json import jsonify
from datetime import datetime
from collections import OrderedDict

from application.models import db
from application.utils.dbmanage.model_query import ModelQuery
from application.constants import CATEGORY_LIST, ANNOTATION_LIST, DATASET_LIST, CONFERENCE_LIST


class SearchDstAPI(MethodView):
    def get(self):
        topic = request.args.get("topic")
        institution = request.args.get("insti")
        year = request.args.get("year")
        task = request.args.get("task")
        conference = request.args.get("conf")
        annotation_type = request.args.get("atype")
        data_type = request.args.get("dtype")
        dataset = ModelQuery.getDst("", institution, year, conference, task, annotation_type, data_type, topic, "", db.session)
        error = None
        status = None
        value = None
        status = 200
        if dataset is not None:
            value = []
            for d in dataset:
                value.append(d.serialize([]))
        response = jsonify(error=error, status=status, value=value)
        response.status_code = status
        return response

class SearchDstNameAPI(MethodView):
    def get(self):
        name = request.args.get("name")
        ret_num = request.args.get("num")
        error = None
        status = None
        value = None
        status = 200
        if name in DATASET_LIST:
            name = DATASET_LIST[name]
        dataset = ModelQuery.getDatasetByName(name, db.session)
        if dataset is not None:
            value = []
            for d in dataset:
                value.append(d.serialize([]))
        response = jsonify(error=error, status=status, value=value)
        response.status_code = status
        return response

class SearchDstAnnotationAPI(MethodView):
    def get(self):
        annotation = request.args.get("annotation")
        ret_num = request.args.get("num")
        error = None
        status = None
        value = None
        status = 200
        dataset = ModelQuery.getDst("", "", "", "", "", annotation, "", "", "", db.session)
        if dataset is not None:
            value = []
            for d in dataset:
                value.append(d.serialize([]))
        response = jsonify(error=error, status=status, value=value)
        response.status_code = status
        return response

class SearchDstIdAPI(MethodView):
    def get(self):
        set_id = request.args.get("dataset_id")
        if set_id != "":
            dst = ModelQuery.getDatasetById(set_id, db.session);
        error = None
        status = None
        value = None
        status = 200
        value = dst.serialize([]);
        response = jsonify(error=error, status=status, value=value)
        response.status_code = status
        return response

class SearchDstConferenceAPI(MethodView):
    def get(self):
        conference = request.args.get("conference")
        ret_num = request.args.get("num")
        error = None
        status = None
        value = None
        status = 200
        dataset = ModelQuery.getDst("", "", "", conference, "", "", "", "", "", db.session)
        if dataset is not None:
            value = []
            for d in dataset:
                value.append(d.serialize([]))
        response = jsonify(error=error, status=status, value=value)
        response.status_code = status
        return response


class SearchDstInstitutionAPI(MethodView):
    def get(self):
        institution = request.args.get("institution")
        ret_num = request.args.get("num")
        error = None
        status = None
        value = None
        status = 200
        dataset = ModelQuery.getDst("", institution, "", "", "", "", "", "", "", db.session)
        if dataset is not None:
            value = []
            for d in dataset:
                value.append(d.serialize([]))
        response = jsonify(error=error, status=status, value=value)
        response.status_code = status
        return response
