# ---------------------------------- INTENT CLASSIFICATION ----------------------------------------------
from app.nlp_model.classify import Classifier 
classifier = Classifier()
classifier.create_model('uploads/classification_weights/bertevn90.hdf5')
classifier.predict(["nhà mình mất điện ở Gia Lâm"])

# ----------------------------------- CHOOSING ACTION ----------------------------------------------------
from app.nlp_model.select_action import Selector
selector = Selector()



# ------------------------------------ NAMED ENTITY RECOGNITION ------------------------------------------
from app.nlp_model.recognite import Recognitor


# ------------------------------------ CONVERSATION -------------------------------------------------------
