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
import pika 
from .utils import generate_action, generate_text, pred_entities, pred_intent, save_to_db
api = Blueprint('api', __name__, url_prefix='/api')


endpoint = '/api/evn-conversation/'
flag_request_all_field = False

import pika
import sys
import time 

print(__package__)

class EVNannouncer(MethodView):
    
    def get(self):
        
        response = dict()
        url = flask.request.url_root + endpoint
        response['status_code'] = "200_ok"
        return jsonify(response), 200


    def post(self):
        sender = request.json.get('sender')
        message = request.json.get('message')
        print("sender: {}".format(sender))
        print("message: {}".format(message))
        print("length of conversations: {}".format(len(Conversation.query.all())))
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
        prob = str(1.0)
        predicted_intent, intent, prob = pred_intent(previous2_action, previous1_action , message, classifier)
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
        entities = pred_entities(message, label)
        print("entities: {}".format(entities))
        value = entities['value']
        
        # sinh text 
        text = generate_text(previous1_action, action , entities)
        print(text)

        # luu vao database
        save_to_db(sender_id,predicted_intent,action,value,message,text)

        # tra ve ket qua theo yeu cau 
        response = dict()
        response['status_code'] = "201_created"
        response['intent'] = predicted_intent
        response['action'] = action
        response['entities'] = dict()
        response['entities']['start'] = entities['start']
        response['entities']['end'] = entities['end']
        response['entities']['value'] = entities['value']
        response['text'] = text
        print(response)
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
            ans['text'] = "D??? em ???? ki???m tra, th?? khu v???c {} hi???n t???i ??ang c?? l???ch c???t ??i???n. Th???i gian c???p ??i???n tr??? l???i l?? {}. Mong anh ch??? th??ng c???m v?? ch??? cho ?????n khi ???????c c???p ??i???n tr??? l???i. N???u c??n c???n h??? tr??? g?? kh??c, anh ch??? vui l??ng li??n h??? t???ng ????i EVN. Ch??o t???m bi???t anh ch???.".format(field, time)
            ans['time'] = time
        else:
            ans['text'] = "D??? v??ng, em ???? ki???m tra hi???n khu v???c c???a m??nh ??ang kh??ng c?? l???ch c???t ??i???n. Em s??? c??? ng?????i ?????n ????? ki???m tra l???i t??nh tr???ng m???t ??i???n ??? khu v???c c???a m??nh. R???t xin l???i qu?? kh??ch ??i???u n??y. Ch??o t???m bi???t qu?? kh??ch."
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
            ans['text'] = 'D??? v??ng, em ???? ghi nh???n t??nh tr???ng m???t ??i???n t???i h??? ????ng k?? {} c?? ?????a ch???: {}. Em s??? c??? nh??n vi??n ?????n x??? l?? cho m??nh s???m nh???t c?? th???. Ch??o t???m bi???t anh ch???.'.format(name, address)
        else:
            ans['text'] = 'Xin l???i anh ch???, em tra c???u h??? th??ng th?? kh??ng t??m th???y ???????c th??ng tin ????ng k??. V???y n??n em s??? chuy???n m??y t???i ??i???n tho???i vi??n ????? h??? tr??? anh ch???. Anh ch??? vui l??ng ?????i trong gi??y l??t ????? em k???t n???i.'
        return ans

OnlyHomeAPI_view = OnlyHomeAPI.as_view('OnlyHomeAPI_view')
app.add_url_rule('/api/only-home', view_func=OnlyHomeAPI_view, methods=['POST'])

