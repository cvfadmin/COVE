from flask.views import MethodView
from flask import request, jsonify, g, abort
from flask.ext.mail import Message 
from datetime import datetime
from application.views import mail
from application.models import db
from application.models.user import User, AddRequest, DeleteRequest, EditRequest
from application.models.dataset import Dataset, Pending_Dataset
from application.models.relation import DatasetAnnCatAssoc, Dataset_Institution, Dataset_Task, Dataset_Datatype, Dataset_Topic, Dataset_Annotation,  Dataset_Keyword, Dataset_Conference, Dataset_Citation
from application.utils.dbmanage.model_insert import ModelInsert
from application.utils.dbmanage.model_query import ModelQuery, getArray
from flask_httpauth import HTTPBasicAuth
import hashlib, uuid
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user_id = User.verify_auth_token(username_or_token)
    user = db.session.query(User).filter_by(id = user_id).first()
    if not user:
        # try to authenticate with username/password
        user = db.session.query(User).filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            False
    g.user = user
    return True

def verify_email(mail, rqst_id, hashed_str):
    if rqst_id:
        rqst_id = int(rqst_id)
    else:
        rqst_id = None
        
    rqst = db.session.query(AddRequest).filter_by(id = rqst_id).first()
    if rqst:
        if rqst.salt is None:
            return False, True, {}
        else:
            m = hashlib.new('sha512')
            m.update((rqst.salt + mail).encode('utf-8'))
            url_suffix = m.hexdigest()
            if url_suffix != hashed_str:
                return False, True, {}
            else:
                data = {
                "id":None,"name":rqst.dataset_name, 
                "url":rqst.url,"thumbnail":"",
                "year":rqst.year,
                "creator":"",
                "description":rqst.intro,
                "size":"", "num_cat":"", "keywords":"",
                "paper":"", "conferences":"", "tasks":"","topics":"","types":"",
                "annotations":"", "citations":"", "institutions":""}
                return True, True, data
    else:
        rqst = db.session.query(EditRequest).filter_by(id = rqst_id).first()
        if rqst is None:
            return False, {}
        if rqst.salt is None:
            return False, False, {}
        else:
            m = hashlib.new('sha512')
            m.update((rqst.salt + mail).encode('utf-8'))
            url_suffix = m.hexdigest()
            if url_suffix != hashed_str:
                return False, False, {}
            else:
                dst_id = rqst.target_id
                data = ModelQuery.getDatasetDetails(db.session, dst_id)
                return True, False, data

class NewRequest(MethodView):
    def post(self):
        email = request.json.get('email')
        firstname = request.json.get('firstname')
        lastname = request.json.get('lastname')
        target_id = request.json.get('target_id')
        dataset_name = request.json.get('dataset_name')
        if target_id:
            target_id = int(target_id)
            dataset_name = ModelQuery.getDatasetById(target_id, db.session).name
        year = request.json.get('year')
        intro = request.json.get('intro')
        reason = request.json.get('reason')
        r_type = request.json.get('r_type')
        url = request.json.get('url')
        err, msg, rqst = ModelInsert.insertRequest(email, firstname, lastname, r_type, target_id, dataset_name, year, intro, reason, url, db.session)
        db.session.commit()
        if err == 1:
            return jsonify({"message":msg}), 400
        else:
            return jsonify({"message":msg}), 200

class NewDataset(MethodView):
    def get(self):
        mail = request.args.get("email")
        rqst_id = request.args.get("rqst_id")
        hashed_str = request.args.get("suffix")
        flag, is_add, val = verify_email(mail, rqst_id, hashed_str)
        if flag:
            return jsonify({"data": val}), 200
        else:
            return jsonify({"error":"Not Authorized"}), 401 
        
    def post(self):
        mail = request.json.get('email')
        hashed_str = request.json.get('suffix')
        r_type = request.json.get('action')
        rqst_id = request.json.get('target_id')
        dst_name = request.json.get('name')
        flag, is_add, val = verify_email(mail, rqst_id, hashed_str)
        if not flag:
            return jsonify({"error":"Not Authorized"}), 401  
        if is_add:
            dst = db.session.query(Dataset).filter_by(name = dst_name, is_approved = True).first()
            if dst:
                return jsonify({"error":"Dataset name already exists in COVE."}), 401

        dst = ModelInsert.insertDataset(
                request.json.get('name'), \
                False,
                request.json.get('dst_id'),
                request.json.get('url'), \
                request.json.get('thumbnail'),\
                request.json.get('description'), \
                "",\
                False,\
                request.json.get('creator'),\
                request.json.get('year'),\
                request.json.get('size'),\
                request.json.get('num_cat'), \
                "",\
                request.json.get('contact_email'), \
                "",\
                request.json.get('related_paper'), \
                request.json.get('citations'), \
                request.json.get('conferences'), \
                request.json.get('keywords'), \
                request.json.get('tasks'),\
                request.json.get('datatypes'), \
                request.json.get('topics'), \
                request.json.get('annotations'), \
                request.json.get('institutions'),\
                db.session)
        if dst:
            rqst = db.session.query(EditRequest).filter_by(id = rqst_id).first()
            if rqst:
                db.session.delete(rqst)
            else:
                rqst = db.session.query(AddRequest).filter_by(id = rqst_id).first()
                db.session.delete(rqst)
            db.session.commit()
            return jsonify({"message":"Succeed"}), 200
        else:
            return jsonify({"error":"Not Valid"}), 401

class ProcessRequest(MethodView):
    @auth.login_required
    def post(self):
        r_type = request.json.get('type')
        rqst_id = int(request.json.get('id'))
        approved = request.json.get('approved')
        if r_type == "add":
            rqst = db.session.query(AddRequest).filter_by(id=rqst_id).first()
            if approved:
                salt = uuid.uuid4().hex
                rqst.salt = salt
                m = hashlib.new('sha512')
                m.update((salt + rqst.email).encode('utf-8'))
                url_suffix = m.hexdigest()
                url = "localhost:8000/#/add_dataset/" + str(rqst_id) + "$" + url_suffix
                subject = "Invitation from COVE"
                message = "You can use the following link to submit your dataset to COVE: \n" + url
                msg = Message(subject, sender="cove@thecvf.com", recipients=[rqst.email])
                msg.body = message
                mail.send(msg)
            else:
                db.session.delete(rqst)
        elif r_type == "edit":
            rqst = db.session.query(EditRequest).filter_by(id=rqst_id).first()
            if approved:
                salt = uuid.uuid4().hex
                rqst.salt = salt
                m = hashlib.new('sha512')
                m.update((salt + rqst.email).encode('utf-8'))
                url_suffix = m.hexdigest()
                url = "localhost:8000/#/edit_dataset/" + str(rqst_id) + "$" + url_suffix
                subject = "Invitation from COVE"
                message = "You can use the following link to edit your dataset: \n" + url
                msg = Message(subject, sender="cove@thecvf.com", recipients=[rqst.email])
                msg.body = message
                mail.send(msg)
            else:
                db.session.delete(rqst)
        elif r_type == "delete":
            rqst = db.session.query(DeleteRequest).filter_by(id=rqst_id).first()
            if approved:
                dst_id = rqst.target_id
                dst = db.session.query(Dataset).filter_by(id_=dst_id).first()
                dst_name = dst.name
                db.session.delete(dst)
                db.session.delete(rqst)
                subject = "Update from COVE"
                message = "Your request to delete the Dataset \"" + dst_name +"\" has been approved. The dataset is now removed from COVE."
                msg = Message(subject, sender="cove@thecvf.com", recipients=[rqst.email])
                msg.body = message
                mail.send(msg)
            else:
                db.session.delete(rqst)
        db.session.commit()
        return jsonify({"message":"Request Processed!"}), 200

class ViewNewDST(MethodView):
    @auth.login_required
    def get(self):
        cur_id = int(request.args.get("cur"))
        target_id = request.args.get("prev")
        data = []
        dst_1 = db.session.query(Pending_Dataset).filter_by(id_ = cur_id).first()
        data.append(dst_1.serialize([]))       
        if target_id:
            target_id = int(target_id)
            dst_1 = db.session.query(Dataset).filter_by(id_ = target_id).first()
            data.append(dst_1.serialize([]))
        else:
            data.append(None)
        response = jsonify({"value":data})
        response.status_code = 200 
        return response
    @auth.login_required
    def post(self):
        cur_id = request.json.get('id')
        target_id = request.json.get('target_id')
        approved = request.json.get('approved')
        if approved:
            if target_id:
                dst = db.session.query(Dataset).filter_by(id_ = target_id).first()
                new_dst = db.session.query(Pending_Dataset).filter_by(id_ = cur_id).first()
                
                # delete old instances 
                db.session.query(Dataset_Task).filter_by(set_id = target_id).delete(synchronize_session='evaluate')
                db.session.query(Dataset_Topic).filter_by(set_id = target_id).delete(synchronize_session='evaluate')
                db.session.query(Dataset_Datatype).filter_by(set_id = target_id).delete(synchronize_session='evaluate')
                db.session.query(Dataset_Annotation).filter_by(set_id = target_id).delete(synchronize_session='evaluate')
                db.session.query(Dataset_Keyword).filter_by(set_id = target_id).delete(synchronize_session='evaluate')
                db.session.query(Dataset_Citation).filter_by(set_id = target_id).delete(synchronize_session='evaluate')
                db.session.query(Dataset_Conference).filter_by(set_id = target_id).delete(synchronize_session='evaluate')
                db.session.query(Dataset_Institution).filter_by(set_id = target_id).delete(synchronize_session='evaluate')
  
                db.session.commit()

                # add new ones
                tasks = getArray(db.session, 'task', 'Dataset_Task', cur_id)
                topics = getArray(db.session, 'topic', 'Dataset_Topic', cur_id)
                datatypes = getArray(db.session, 'data_type', 'Dataset_Datatype', cur_id)
                annotation_types = getArray(db.session, 'annotation_type', 'Dataset_Annotation', cur_id)
                keywords = getArray(db.session, 'keyword', 'Dataset_Keyword', cur_id)
                citations = getArray(db.session, 'citation', 'Dataset_Citation', cur_id)
                conferences = getArray(db.session, 'conference', 'Dataset_Conference', cur_id)
                institutions = getArray(db.session, 'institution', 'Dataset_Institution', cur_id)

                for val in keywords:
                    ds_kw = Dataset_Keyword(keyword = val, dataset = dst)
                    db.session.add(ds_kw)
                for val in topics:
                    ds_tp = Dataset_Topic(topic = val, dataset = dst)
                    db.session.add(ds_tp)
                for val in tasks:
                    ds_tsk = Dataset_Task(task = val, dataset = dst)
                    db.session.add(ds_tsk)
                for val in datatypes:
                    ds_dtp = Dataset_Datatype(data_type = val, dataset = dst)
                    db.session.add(ds_dtp)
                for val in annotation_types:
                    ds_atp = Dataset_Annotation(annotation_type = val, dataset = dst)
                    db.session.add(ds_atp)
                for val in institutions:
                    ds_insti = Dataset_Institution(institution = val, dataset = dst)
                    db.session.add(ds_insti)
                for val in conferences:
                    ds_conf = Dataset_Conference(conference = val, dataset = dst)
                    db.session.add(ds_conf)
                for val in citations:
                    ds_cit = Dataset_Citation(citation = val, dataset = dst)
                    db.session.add(ds_cit)
                db.session.commit()
                
                # delete temp instances
                db.session.query(Dataset_Task).filter_by(set_id = cur_id).delete(synchronize_session='evaluate')
                db.session.query(Dataset_Topic).filter_by(set_id = cur_id).delete(synchronize_session='evaluate')
                db.session.query(Dataset_Datatype).filter_by(set_id = cur_id).delete(synchronize_session='evaluate')
                db.session.query(Dataset_Annotation).filter_by(set_id = cur_id).delete(synchronize_session='evaluate')
                db.session.query(Dataset_Keyword).filter_by(set_id = cur_id).delete(synchronize_session='evaluate')
                db.session.query(Dataset_Citation).filter_by(set_id = cur_id).delete(synchronize_session='evaluate')
                db.session.query(Dataset_Conference).filter_by(set_id = cur_id).delete(synchronize_session='evaluate')
                db.session.query(Dataset_Institution).filter_by(set_id = cur_id).delete(synchronize_session='evaluate')
  
                db.session.commit()

                dst.name = new_dst.name
                dst.url = new_dst.url
                dst.thumbnail = new_dst.thumbnail
                dst.description = new_dst.description
                dst.related_paper = new_dst.related_paper
                dst.creator = new_dst.creator
                dst.year = new_dst.year
                dst.size = new_dst.size
                dst.num_cat = new_dst.num_cat
                dst.contact_name = new_dst.contact_name
                dst.contact_email = new_dst.contact_email
                db.session.delete(new_dst)                
                rqst = db.session.query(EditRequest).filter_by(email = new_dst.contact_email).first()
                if rqst:
                    db.session.delete(rqst)
                db.session.commit()
                
                url = "localhost:8000/#/dataset?id=" + str(dst.id_)
                subject = "View your dataset edits on COVE"
                message = "Your edits to " + dst.name + " were accepted to COVE and can be viewed at the following link: \n" + url + "\n\nThank you for your support!"
                msg = Message(subject, sender="cove@thecvf.com", recipients=[dst.contact_email])
                msg.body = message
                mail.send(msg)
                
            else:
                # add new ones
                dst = db.session.query(Pending_Dataset).filter_by(id_ = cur_id).first()

                tasks = getArray(db.session, 'task', 'Dataset_Task', cur_id)
                topics = getArray(db.session, 'topic', 'Dataset_Topic', cur_id)
                datatypes = getArray(db.session, 'data_type', 'Dataset_Datatype', cur_id)
                annotation_types = getArray(db.session, 'annotation_type', 'Dataset_Annotation', cur_id)
                keywords = getArray(db.session, 'keyword', 'Dataset_Keyword', cur_id)
                citations = getArray(db.session, 'citation', 'Dataset_Citation', cur_id)
                conferences = getArray(db.session, 'conference', 'Dataset_Conference', cur_id)
                institutions = getArray(db.session, 'institution', 'Dataset_Institution', cur_id)
                
                ModelInsert.insertDataset(dst.name, True, None, dst.url, dst.thumbnail, dst.description, dst.license, False, dst.creator, dst.year, dst.size,\
                                dst.num_cat, dst.contact_name, dst.contact_email, dst.notes, dst.related_paper, citations, conferences, keywords, \
                                tasks, datatypes, topics, annotation_types, institutions, db.session)
                rqst = db.session.query(AddRequest).filter_by(email = dst.contact_email).first()
                                
                if rqst:
                    db.session.delete(rqst)
                db.session.delete(dst)
                db.session.commit()

                cur_id = db.session.query(Dataset).filter_by(name = dst.name).first().id_
                url = "localhost:8000/#/dataset?id=" + str(cur_id)
                subject = "View your new dataset on COVE"
                message = "Your dataset " + dst.name + " was accepted to COVE and can be viewed at the following link: \n" + url + "\n\nThank you for your support!"
                msg = Message(subject, sender="cove@thecvf.com", recipients=[dst.contact_email])
                msg.body = message
                mail.send(msg)

        else:
            if target_id:
                new_dst = db.session.query(Pending_Dataset).filter_by(id_ = cur_id).first()
                rqst = db.session.query(EditRequest).filter_by(email = new_dst.contact_email).first()
                if rqst:
                    db.session.delete(rqst)
                db.session.delete(new_dst)
            else:
                new_dst = db.session.query(Pending_Dataset).filter_by(id_ = cur_id).first()
                rqst = db.session.query(AddRequest).filter_by(email = new_dst.contact_email).first()
                if rqst:
                    db.session.delete(rqst)
                db.session.delete(new_dst)
            db.session.commit()
        return jsonify({"message":"Request Processed!"}), 200



class Administration(MethodView):
    @auth.login_required
    def get(self):
        value = []
        add_request = []
        pendings = db.session.query(AddRequest).filter_by(salt=None).all()
        for rqst in pendings:
            add_request.append(rqst.serialize())
        value.append(add_request)
        delete_request = []
        pendings = db.session.query(EditRequest).filter_by(salt=None).all()
        for rqst in pendings:
            delete_request.append(rqst.serialize())
        value.append(delete_request)
        edit_request = []
        pendings = db.session.query(DeleteRequest).filter_by(salt=None).all()
        for rqst in pendings:
            edit_request.append(rqst.serialize())
        value.append(edit_request)
        pending_datasets = []
        pendings = db.session.query(Pending_Dataset).all()
        for rqst in pendings:
            pending_datasets.append([rqst.name, rqst.id_, rqst.edit_id])
        value.append(pending_datasets)
        response = jsonify(pending_requests=value)
        response.status_code = 200 
        return response

    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        message = []
        if verify_password(username, password):
            token = g.user.generate_auth_token(600)
            return jsonify({'token': token.decode('ascii'), 'duration': 600})
        else:
            message.append({"message":"Password is incorrect for the specified username"})
            dic={
                "errors":message
            }
            return jsonify(dic),422

class Logout(MethodView):
    @auth.login_required
    def post(self):
        token = g.user.generate_auth_token()
        return jsonify({'token':token.decode(), 'duration':600})

#        return true