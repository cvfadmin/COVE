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

class SearchTextAPI(MethodView):
    def get(self):
        search_query = request.args.get("query")
        ret_num = request.args.get("num")
        error = None
        status = None
        value = None
        if not search_query:
            error = "Empty search query."
            status = 404
        else:
            status = 200
            search_query = search_query.lower()
            dataset_query = None
            category_query = None
            annotation_query = None
            conference_query = None
            if search_query in DATASET_LIST:
                dataset_query = DATASET_LIST[search_query]
            elif search_query in CATEGORY_LIST:
                category_query = search_query
            elif search_query in ANNOTATION_LIST:
                annotation_query = search_query
            elif search_query in CONFERENCE_LIST:
                conference_query = search_query
            if dataset_query is not None or category_query is not None or annotation_query is not None or conference_query is not None:
                value = ModelQuery.getQueryResults(dataset_query, category_query, annotation_query, conference_query, ret_num, db.session)
        response = jsonify(error=error, status=status, value=value)
        response.status_code = status 
        return response
        
class SearchDatasetAPI(MethodView):
    def get(self):
        search_query = request.args.get("dataset")
        ret_num = request.args.get("num")
        error = None
        status = None
        value = None
        status = 200
        search_query = search_query.lower()
        query_list = search_query.split(' ')
        dataset_query = None
        for q in query_list:
            if q in DATASET_LIST:
                dataset_query = DATASET_LIST[q]
        if dataset_query is not None:
            value = ModelQuery.getQueryResults(dataset_query, None, None, None, ret_num, db.session)
        response = jsonify(error=error, status=status, value=value)
        response.status_code = status
        return response 

class SearchAnnotationAPI(MethodView):
    def get(self):
        search_query = request.args.get("annotation")
        ret_num = request.args.get("num")
        error = None
        status = None
        value = None
        status = 200
        search_query = search_query.lower()
        query_list = search_query.split(' ')
        annotation_query = None
        for q in query_list:
            if q in ANNOTATION_LIST:
                annotation_query = q
        if annotation_query is not None:
            value = ModelQuery.getQueryResults(None, None, annotation_query, None, ret_num, db.session)
        response = jsonify(error=error, status=status, value=value)
        response.status_code = status
        return response

class SearchCategoryAPI(MethodView):
    def get(self):
        search_query = request.args.get("category")
        ret_num = request.args.get("num")
        error = None
        status = None
        value = None
        status = 200
        search_query = search_query.lower()
        query_list = search_query.split(' ')
        category_query = search_query
        #for q in query_list:
        #    if q in CATEGORY_LIST:
        #        category_query = q
        #if category_query is not None:
        value = ModelQuery.getQueryResults(None, category_query, None, None, ret_num, db.session)
        response = jsonify(error=error, status=status, value=value)
        response.status_code = status
        return response


class SearchAdvancedAPI(MethodView):
    def get(self):
        ret_num = request.args.get("num")
        dataset_query = request.args.get("dataset")
        category_query = request.args.get("category")
        annotation_query = request.args.get("annotation")
        a = "dataset_query is {0} and category is {1} and annotation is {2} \n".format(dataset_query, category_query, annotation_query)
        print a
        if dataset_query == "":
            dataset_query = None
        else:
            if dataset_query in DATASET_LIST:
                dataset_query = DATASET_LIST[dataset_query]
        if category_query == "":
            category_query = None
        if annotation_query == "":
            annotation_query = None
        error = None
        status = None
        value = None
        status = 200
        value = ModelQuery.getQueryResults(dataset_query, category_query, annotation_query, None, ret_num, db.session) 
        response = jsonify(error=error, status=status, value=value)
        response.status_code = status
        return response 

