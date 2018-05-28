#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask.ext.cors import CORS
from flask import request
from flask.json import jsonify
from datetime import datetime
from collections import OrderedDict
import json 
from application.models import db
from application.utils.dbmanage.model_query import ModelQuery
from application.models.dataset import Dataset
from application.models.relation import DatasetAnnCatAssoc, Dataset_Institution, Dataset_Task, Dataset_Datatype, Dataset_Topic, Dataset_Annotation,  Dataset_Keyword, Dataset_Conference, Dataset_Citation
from application.views.api.admin import Administration, ProcessRequest, NewRequest, NewDataset, ViewNewDST, Logout

api = Blueprint('api', __name__)
CORS(api)

def getFilterItems():
    tasks= ModelQuery.getUniqueElems(Dataset_Task, 'task', db.session)
    topics= ModelQuery.getUniqueElems(Dataset_Topic, 'topic', db.session)
    types= ModelQuery.getUniqueElems(Dataset_Datatype, 'data_type', db.session)
    annotations= ModelQuery.getUniqueElems(Dataset_Annotation, 'annotation_type', db.session)
    
    return ({"tasks":tasks,"topics":topics,"types":types,"annotations":annotations})

@api.route('/api')
def home():        
    filterItems = getFilterItems()
    return json.dumps(filterItems)
    

@api.route('/api/results', methods=['GET','POST'])
def searchResults():   
    
    tasks = request.args.getlist('task') if 'task' in request.args else []
    topics = request.args.getlist('topic') if 'topic' in request.args else []
    types = request.args.getlist('type') if 'type' in request.args else []
    minyear = request.args.get('minyear') if 'minyear' in request.args else ''
    maxyear = request.args.get('maxyear') if 'maxyear' in request.args else ''
    publication = request.args.get('publication') if 'publication' in request.args else ''
    search = request.args.get('search') if 'search' in request.args else ''  
    results = ModelQuery.searchDatasets(db.session, tasks, topics, types, minyear, maxyear, publication, search, '', '')
    
    return json.dumps(results)    

@api.route('/api/dataset')
def display():
    id_num = request.args.get('id')
    datasetDetails = ModelQuery.getDatasetDetails(db.session, id_num)
    return json.dumps(datasetDetails)
       


#api.add_url_rule("/api/search/text", view_func=SearchTextAPI.as_view('api_search'))
#api.add_url_rule("/api/search/dataset", view_func=SearchDatasetAPI.as_view('api_dataset'))
##api.add_url_rule("/api/search/problem", view_func=GetProblemAPI.as_view('api_problem'))
#api.add_url_rule("/api/search/annotation", view_func=SearchAnnotationAPI.as_view('api_annotation'))
#api.add_url_rule("/api/search/category", view_func=SearchCategoryAPI.as_view('api_category'))
#api.add_url_rule("/api/search/advanced", view_func=SearchAdvancedAPI.as_view('api_advanced'))
#api.add_url_rule("/api/search/download", view_func=DownloadAPI.as_view('api_download'))
#api.add_url_rule("/api/search_dataset/name", view_func=SearchDstNameAPI.as_view('dst_name'))
#api.add_url_rule("/api/search_dataset/conference", view_func=SearchDstConferenceAPI.as_view('dst_conference'))
#api.add_url_rule("/api/search_dataset/annotation", view_func=SearchDstAnnotationAPI.as_view('dst_annotation'))
#api.add_url_rule("/api/search_dataset/institution", view_func=SearchDstInstitutionAPI.as_view('dst_institution'))
#api.add_url_rule("/api/search_dataset/advanced", view_func=SearchDstAPI.as_view('dst_advanced'))
#api.add_url_rule("/api/search_dataset/id", view_func=SearchDstIdAPI.as_view('dst_id'))
admin = Administration.as_view('user_api')
api.add_url_rule("/api/admin", view_func=admin, methods=['POST','GET'])
api.add_url_rule("/api/process_request", view_func=ProcessRequest.as_view('process_request'), methods=['POST'])
api.add_url_rule("/api/new_request", view_func=NewRequest.as_view('new_request'), methods=['POST'])
api.add_url_rule("/api/new_dataset", view_func=NewDataset.as_view('add_dst'), methods=['POST', 'GET'])
api.add_url_rule("/api/logout", view_func = Logout.as_view('log_out'), methods =['POST'])
api.add_url_rule("/api/view_pending_dst", view_func = ViewNewDST.as_view('view_pending_dst'), methods =['GET','POST']) 
