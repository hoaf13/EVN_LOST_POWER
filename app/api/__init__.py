# ---------------------------------- INTENT CLASSIFICATION ----------------------------------------------
from app.nlp_model.classify import Classifier

classifier = Classifier()
print(classifier)
# classifier.create_model('uploads/classification_weights/bertevn90.hdf5')
# # classifier.summarize()
# print(classifier)


# ----------------------------------- CHOOSING ACTION ----------------------------------------------------
from app.nlp_model.select_action import Selector
selector = Selector()



# ------------------------------------ NAMED ENTITY RECOGNITION ------------------------------------------




# ------------------------------------ CONVERSATION -------------------------------------------------------
from app.models import Conversation
from app import db
Conversation.query.delete()
db.session.commit()
start_action = Conversation(
    sender_id = "13062000",
    action = "action_start",
    value = "",
    client_message = "",
    bot_message = ""
)
db.session.add(start_action)
db.session.commit()
print("add the start action")

