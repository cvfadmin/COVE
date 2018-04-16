#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask.ext.cors import CORS
from application.views.api.search_api import SearchTextAPI, SearchDatasetAPI, SearchCategoryAPI, SearchAnnotationAPI, SearchAdvancedAPI
from application.views.api.get_api import DownloadAPI
from application.views.api.search_dataset_api import SearchDstNameAPI, SearchDstConferenceAPI, SearchDstAnnotationAPI, SearchDstInstitutionAPI, SearchDstAPI, SearchDstIdAPI
from application.views.api.admin import Administration, ProcessRequest, New_dataset

api = Blueprint('api', __name__)
CORS(api)
api.add_url_rule("/api/search/text", view_func=SearchTextAPI.as_view('api_search'))
api.add_url_rule("/api/search/dataset", view_func=SearchDatasetAPI.as_view('api_dataset'))
#api.add_url_rule("/api/search/problem", view_func=GetProblemAPI.as_view('api_problem'))
api.add_url_rule("/api/search/annotation", view_func=SearchAnnotationAPI.as_view('api_annotation'))
api.add_url_rule("/api/search/category", view_func=SearchCategoryAPI.as_view('api_category'))
api.add_url_rule("/api/search/advanced", view_func=SearchAdvancedAPI.as_view('api_advanced'))
api.add_url_rule("/api/search/download", view_func=DownloadAPI.as_view('api_download'))
api.add_url_rule("/api/search_dataset/name", view_func=SearchDstNameAPI.as_view('dst_name'))
api.add_url_rule("/api/search_dataset/conference", view_func=SearchDstConferenceAPI.as_view('dst_conference'))
api.add_url_rule("/api/search_dataset/annotation", view_func=SearchDstAnnotationAPI.as_view('dst_annotation'))
api.add_url_rule("/api/search_dataset/institution", view_func=SearchDstInstitutionAPI.as_view('dst_institution'))
api.add_url_rule("/api/search_dataset/advanced", view_func=SearchDstAPI.as_view('dst_advanced'))
api.add_url_rule("/api/search_dataset/id", view_func=SearchDstIdAPI.as_view('dst_id'))
admin = Administration.as_view('user_api')
api.add_url_rule("/api/admin", view_func=admin, methods=['POST','GET'])
request = ProcessRequest.as_view('request')
api.add_url_rule("/api/request", view_func=request, methods=['POST'])
api.add_url_rule("/api/request/<int:request_id>", view_func=request, methods=['PUT'])
api.add_url_rule("/api/new_dataset", view_func=New_dataset.as_view('new_dst'), methods=['POST', 'GET'])
