#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import 

api_search = Blueprint('search', __name__)

@api_search.route("/api/search/text", methods = "GET", "POST")
def search_by_text():
    if request.method == 'GET':
        query = request.args.get("query")

    if request.method == 'POST':


@api_search.route("/api/search/dataset", methods = "GET", "POST")
def search_by_dataset():


@api_search.route("/api/search/annotation", methods = "GET", "POST")
def search_by_annotation():


@api_search.route("/api/search/category", methods = "GET", "POST")
def search_by_category():


@api_search.route("/api/search/advanced", methods = "GET", "POST")
def search_by_advanced():
