class Recognitor:
	
	def __init__(self):
		self.filename = None
		pass
	
	def create_model(self, path_weights):
		pass

	def preprocessing(self, X_test):
		pass

	def predict(self, X_test):
		# return LOC and Name
		pass 
	
	def recognize_per(self, sentence):
		pass

	def recognize_loc(self, sentence):
		pass

	def __str__ (self):
		return "model Ner: {} ".format(self.filename)
		

