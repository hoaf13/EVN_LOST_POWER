from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, rooms, disconnect
from flask import request
from app import app 
import requests
import json
from app.models import Conversation
from app import db

socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('client-start-chat')
def handle_start_chat(msg):
    sender = msg
    Conversation.query.delete()
    db.session.commit()
    message = "Xin chào anh/chị {}, đây là tổng đài tự động của EVN. Xin hỏi anh chị báo mất điện ở khu vực quận, huyện nào vậy.".format(sender)
    start_action = Conversation(
        sender_id = sender,
        action = "action_start",
        intent = "",
        value = "",
        client_message = "",
        bot_message = message
    )
    db.session.add(start_action)
    db.session.commit()
    print("create action start!!!\n\n\n")
    emit("server-start-chat", message, broadcast=False)



@socketio.on('client-send-msg')
def handle_client_send_msg(msg):
    message = msg['message']
    sender = msg['sender']
    url = request.url_root + 'api/evn-conversation/'
    myobj = {
        "sender": sender,
        "message": message
    }
    headers = {'content-type': 'application/json'}
    x = requests.post(url, data = json.dumps(myobj), headers=headers)
    response = json.loads(x.text)
    if response['action'] == 'action_all_field':
        emit('server-send-action-all-field', broadcast=False) 
        emit('server-end', broadcast=False)  

    if response['action'] == 'action_provide_address':
        conversation = Conversation.query.filter_by(sender_id=sender).all()[-2]
        print("action: {}".format(conversation.value))
        if conversation.action == 'action_provide_name':
            emit('server-send-action-provide-address', broadcast=False)
    emit("server-send-msg", response['text'], broadcast=False)
    
        
@socketio.on('client-send-action-all-field')
def handle_client_send_action_all_field(sender):
    conversation = Conversation.query.filter_by(sender_id=sender).all()[-2]
    address = conversation.value 
    print("API ALL FIELD --- address: {}".format(address))
    url = request.url_root + '/api/all-field/'
    myobj = {
        "field": address,
    }
    headers = {'content-type': 'application/json'}
    x = requests.post(url, data = json.dumps(myobj), headers=headers)
    response = json.loads(x.text)
    emit("server-send-msg", response['text'], broadcast=False)
    emit("server-end", broadcast=False)

@socketio.on('client-send-action-provide-address')
def handle_client_send_action_provide_address(sender):
    name = Conversation.query.filter_by(sender_id=sender, intent='intent_provide_name').all()[-1].value
    address = Conversation.query.filter_by(sender_id=sender, intent='intent_provide_address').all()[-1].value
    print("API ONLY HOME --- name: {} - address: {}".format(name, address))
    url = request.url_root + '/api/only-home'
    myobj = {
        "name":name,
        "address": address
    }
    headers = {'content-type': 'application/json'}
    x = requests.post(url, data = json.dumps(myobj), headers=headers)
    response = json.loads(x.text)   
    emit("server-send-msg", response['text'], broadcast=False)
    emit("server-end", broadcast=False)
    