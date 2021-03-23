from . import selector, Recognitor 
from app import db
from app.models import Conversation

def pred_intent(previous2_action, previous1_action, message, model):
    res = model.predict([message])[0]
    pred_label = res['label']
    label = res['label']
    prob = res['probability']
    if (previous2_action == previous1_action and previous2_action != 'action_start')  or label[6:] == previous1_action[6:]:
        label = 'intent_fallback'
        prob = 1.0
    return pred_label, label, prob


def pred_entities(message, label): # label = LOC | PER
    entities = dict()
    entities['start'] = None
    entities['end'] = None
    entities['value'] = None
    if label == 'LOC':
        entities = Recognitor.recognize_loc(message)
    if label == 'PER':
        entities = Recognitor.recognize_per(message)    
    return entities


def generate_action(previous2_action, previous1_action, current_intent):
    action = selector.generate_action(previous2_action, previous1_action, current_intent)
    return action


def generate_text(previous_action, action, provided_entities):
    text = None
    print("generate_text from previous - current: {} {}".format(previous_action, action))

    if action == 'action_start' and previous_action == action:
        name = provided_entities['value']
        text = 'Xin hỏi anh/chị báo mất điện ở khu vực quận, huyện nào vậy.'.format(name)

    elif action == 'action_fallback':
        text = "Dạ Rất xin lỗi anh/chị, em chưa hiểu được phản hồi của anh/chị. Nên em sẽ chuyển máy cho điện thoại viên để hỗ trợ anh/chị. Anh/chị vui lòng đợi trong giây lát." 
    
    elif action == 'action_provide_address' and (previous_action == 'action_start' or previous_action == action):
        district_name = provided_entities['value'] 
        text = "Hệ thống ghi nhận mất điện tại khu vực {}. Anh/chị vui lòng cho em biết là, tình trạng mất điện chỉ ở nhà anh/chị hay trên cả khu vực luôn vậy.".format(district_name)
    
    elif action == 'action_dont_clear':
        text = "Nếu quý khách chưa rõ, quý khách vui lòng kiểm tra lại thông tin dùm em. Nếu cần hỗ trợ quý khách vui lòng liên hệ tổng đài EVN. Chào tạm biệt quý khách"
    
    elif action == 'action_all_field': 
        district_name = provided_entities['value'] 
        text = "Hệ thống ghi nhận mất điện trên cả khu vực. Anh chị vui lòng chờ trong giây lát để em kiểm tra lịch cắt điện tại khu vực của mình.".format(district_name)
    
    elif action == 'action_only_home':
        text = "Hệ thống ghi nhận chỉ có duy nhất nhà anh chị bị mất điện. Anh chị vui lòng cho biết họ và tên người sở hữu."
    
    elif action == 'action_all_field_yes':
        text = "Dạ em đã kiểm tra, thì khu vực của mình hiện tại đang có lịch cắt điện. Thời gian cấp điện trở lại là {}. Mong anh/chị thông cảm và chờ cho đến khi được cấp điện trở lại. Nếu còn cần hỗ trợ gì khác, anh chị vui lòng liên hệ tổng đài EVN. Chào tạm biệt anh chị.".format("9h30")
    
    elif action == 'action_all_field_no':
        text = "Dạ vâng, em đã kiểm tra hiện khu vực của mình đang không có lịch cắt điện. Em sẽ cử người đến để kiểm tra lại tình trạng mất điện ở khu vực của mình. Rất xin lỗi quý khách điều này. Chào tạm biệt quý khách"
    
    elif action == 'action_provide_name':
        person_name = provided_entities['value']
        text = "Hệ thống ghi nhận chủ sở hữu là anh/chị {}. Anh/chị vui lòng cho biết địa chỉ cụ thể của nhà mình.".format(person_name)
    
    elif action == 'action_provide_address' and previous_action == 'action_provide_name':
        address = provided_entities['value']
        text = "Hệ thống ghi nhận địa chỉ của anh chị là {}. Quý khách vui lòng đợi trong giây lát để em kiểm tra thông tin lịch cắt điện.".format(address)
    
    elif action == 'action_provide_address_yes':
        text = "Dạ vâng, em đã ghi nhận tình trạng mất điện của anh chị và sẽ cử nhân viên đến xử lý cho mình sớm nhất có thể. Chào tạm biệt anh/chị."
    
    elif action == 'action_provide_address_no':
        text = "Xin lỗi anh/chị, em tra cứu hệ thông thì không tìm thấy được thông tin đăng ký. Vậy nên em sẽ chuyển máy tới điện thoại viên để hỗ trợ anh/chị. Anh/chị vui lòng đợi trong giây lát để em kết nối."
    
    else:
        text = "Em không hiểu quý khách muốn gì. Mời anh/chị nhập lại."
        
    return text

def save_to_db(sender_id, predicted_intent, action, value, client_message, bot_message):
    conversation = Conversation(sender_id=sender_id, intent=predicted_intent, action=action, value=value, client_message=client_message, bot_message=bot_message)
    db.session.add(conversation)
    db.session.commit()
    print("\n\n\n")
    