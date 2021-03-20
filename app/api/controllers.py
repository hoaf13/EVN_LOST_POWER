import flask
from flask import jsonify, Blueprint, flash, render_template, request, session, abort, \
                  redirect, url_for
import requests
import os
from app import app
from flask.views import MethodView
from . import selector, classifier
import random 
from app.models import Conversation
from app import db 

from .utils import generate_action, generate_text, pred_entities, pred_intent, save_to_db
api = Blueprint('api', __name__, url_prefix='/api')


endpoint = '/api/evn-conversation/'
flag_request_all_field = False

class EVNannouncer(MethodView):
    
    def get(self):
        
        response = dict()
        url = flask.request.url_root + endpoint
        response['status_code'] = "200_ok"
        return jsonify(response), 200


    def post(self):
        
        sender = request.json.get('sender')
        intent = request.json.get('intent')
        message = request.json.get('message')
        prob = 1.0

        # lay du lieu truoc do
        conversations = Conversation.query.filter_by(sender_id=sender).all()[-2:]
        for c in conversations:
            print(c)
        print("length of conversations: {}".format(len(conversations)))
        sender_id = conversations[-1].sender_id
        

        previous1_action = conversations[-1].action
        previous2_action = None
        if len(conversations) > 1:
            previous2_action = conversations[-2].action  
        print("2 previous: {} - {}".format(previous1_action, str(previous2_action)))
        
        # du doan intent 
        predicted_intent = intent
        # intent = 'intent_provide_address'
        prob = str(1.0)
        # predicted_intent, intent, prob = pred_intent(previous2_action, previous1_action , message, classifier)
        print("predicted intent: {} - intent after: {} - probability: {}".format(predicted_intent, intent, prob))


        # sinh action
        action = generate_action(previous2_action, previous1_action, intent)
        print("Current Action: {}".format(action))


        # du doan entites
        label = None
        if intent == 'intent_provide_address':
            label = 'LOC'
        if intent == 'intent_provide_name':
            label = 'PER'
        entities = pred_entities(message, label=label)

        value = entities['value']
        # print(entities)
        print("Entities: {}".format(value))


        # sinh text 
        text = generate_text(previous1_action, action , entities)
        print(text)

        # luu vao database
        save_to_db(sender_id,action,value,message,text)

        # tra ve ket qua theo yeu cau 
        response = dict()
        response['status_code'] = "200_ok"
        response['intent'] = predicted_intent
        response['action'] = action
        response['entities'] = dict()
        response['entities']['start'] = entities['start']
        response['entities']['end'] = entities['end']
        response['entities']['value'] = entities['value']
        response['text'] = text

        return jsonify(response)

EVNannouncer_view = EVNannouncer.as_view('EVNannouncer_view')
app.add_url_rule(endpoint, view_func=EVNannouncer_view, methods=['GET','POST'])


class AllFieldAPI(MethodView):
    
    def post(self):
        field = request.json.get('field')
        
        # query to database
        res = ['yes', 'no']
        status = random.choice(res)
        times = ['9:30', '10:00', '20:00', '23:15']
        ans = dict()
        ans['status'] = status # Co lich cat dien tren toan khu vuc hay khong. 
        ans['time']  = None
        ans['text'] = None
        if status == 'yes':
            time = random.choice(times)
            ans['text'] = "Dạ em đã kiểm tra, thì khu vực {} hiện tại đang có lịch cắt điện. Thời gian cấp điện trở lại là {}. Mong anh chị thông cảm và chờ cho đến khi được cấp điện trở lại. Nếu còn cần hỗ trợ gì khác, anh chị vui lòng liên hệ tổng đài EVN. Chào tạm biệt anh chị.".format(field, time)
            ans['time'] = time
        else:
            ans['text'] = "Dạ vâng, em đã kiểm tra hiện khu vực của mình đang không có lịch cắt điện. Em sẽ cử người đến để kiểm tra lại tình trạng mất điện ở khu vực của mình. Rất xin lỗi quý khách điều này. Chào tạm biệt quý khách."
        return ans


AllFieldAPI_view = AllFieldAPI.as_view('AllFieldAPI_view')
app.add_url_rule('/api/all-field/', view_func=AllFieldAPI_view, methods=['POST'])
        

class OnlyHomeAPI(MethodView):
    def post(self):
        address = request.json.get('address')
        name = request.json.get('name')
        
        #query to database
        res = ['yes', 'no']
        status = random.choice(res)
        ans = dict()
        ans['text'] = None 
        ans['status'] = status # xac dinh chu so huu nay co dang ky dien tai EVN hay khong.  
        if status == 'yes':
            ans['text'] = 'Dạ vâng, em đã ghi nhận tình trạng mất điện tại hộ đăng kí {} có địa chỉ: {}. Em sẽ cử nhân viên đến xử lý cho mình sớm nhất có thể. Chào tạm biệt anh chị.'.format(name, address)
        else:
            ans['text'] = 'Xin lỗi anh chị, em tra cứu hệ thông thì không tìm thấy được thông tin đăng ký. Vậy nên em sẽ chuyển máy tới điện thoại viên để hỗ trợ anh chị. Anh chị vui lòng đợi trong giây lát để em kết nối.'
        return ans

OnlyHomeAPI_view = OnlyHomeAPI.as_view('OnlyHomeAPI_view')
app.add_url_rule('/api/only-home', view_func=OnlyHomeAPI_view, methods=['POST'])
    