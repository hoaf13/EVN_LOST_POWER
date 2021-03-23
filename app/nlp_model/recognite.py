from underthesea import ner

def predict(message, label):
		ans = dict()
		tokens = ner(message)
		print("tokens: {}".format(tokens))
		flag = False
		for token in tokens:
			if label in token[3]:
				flag = True
		if flag == False:
			label = 'O'
		start = None
		length = 0
		for i,token in enumerate(tokens):
			if label in token[3]:
				if start == None:
					start = i
					length += len(token[0].split(' ')) 
				if start != None:
					length += len(token[0].split(' '))
		value = [x[0] for x in tokens if label in x[3]]
		value = ' '.join(value)
		if start != None:
			ans['start'] = start + 1
			ans['end'] = start + length
			ans['value'] = value
		return ans
		

class Recognitor:	

	@staticmethod
	def recognize_per(message):
		return predict(message, 'PER')

	@staticmethod
	def recognize_loc(message):
		return predict(message, 'LOC')


	def __str__ (self):
		return "model Ner: {} ".format(self.filename)
		
ner_queue = []
ner_result = dict()