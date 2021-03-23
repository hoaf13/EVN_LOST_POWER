from transformers import AutoModel, AutoTokenizer, TFAutoModel, PhobertTokenizer, BertForSequenceClassification
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input, Lambda
import numpy as np
import re
import pandas as pd


class Classifier:
	
	def __init__(self):
		self.model = None
		self.tokenizer = None
		self.intent_labels = ['intent_all_field', 'intent_cant_hear','intent_dont_clear', 
		'intent_only_home', 'intent_provide_address', 'intent_provide_name']
		
	def predict(self, X_test):
		X_embedding = self.preprocessing(X_test)
		y_pred = self.model.predict(X_embedding)
		ans = []
		for y in y_pred:
			tmp = dict()
			index = np.argmax(y)
			tmp['label'] = self.intent_labels[index]
			tmp['probability'] = y[index]
			ans.append(tmp)
		return ans 	

	def __str__(self):
		return "{}".format("BertModel90")

	def create_model(self, path_weights=None):
		phobert = TFAutoModel.from_pretrained("vinai/phobert-base")
		self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)
		MAX_LEN = 25
		ids = tf.keras.layers.Input(shape=(25), dtype=tf.int32)
		mask = tf.keras.layers.Input(shape=(25,), name='attention_mask', dtype='int32')
		# For transformers v4.x+: 

		embeddings = phobert(ids,attention_mask = mask)[0]
		X =( tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128)))(embeddings)
		X = tf.keras.layers.BatchNormalization()(X)
		X = tf.keras.layers.Dense(128, activation='relu')(X)
		X = tf.keras.layers.Dropout(0.1)(X)
		y = tf.keras.layers.Dense(6, activation='softmax', name='outputs')(X)
		self.model = tf.keras.models.Model(inputs=[ids,mask], outputs=[y])
		# model.summary()
		# model.layers[2].trainable = False
		# model.layers[2].roberta.embeddings.trainable = True
		# print()
		# print(model.layers[2])
		# inputs = [inputs]
		# model.compile(optimizer='Adam',loss = 'categorical_crossentropy',metrics='accuracy')
		if path_weights != None:
			self.model.load_weights(path_weights)

	def preprocessing(self, X_train):
		
		def padding(encoded, max_length):
  			return pad_sequences(encoded,max_length,padding = 'post')

		def encoding(sent,max_length = 25):
			all_sent = []
			all_mask_sent = []
			for line in sent:
				tokens = self.tokenizer.encode_plus(line, max_length=max_length,
											truncation=True, padding='max_length',
											add_special_tokens=True, return_attention_mask=True,
											return_token_type_ids=False, return_tensors='tf')
				umk = np.array(tokens['input_ids']).reshape(-1)
				mk = np.array(tokens['attention_mask']).reshape(-1)
				all_sent.append(umk)
				all_mask_sent.append(mk)
			# print(all_sent)
			all_sent = padding(all_sent,max_length=max_length)
			all_mask_sent = padding(all_mask_sent,max_length=max_length)
			return all_sent,all_mask_sent
		X_train = encoding(X_train)
		return X_train
		

	def summarize(self):
		self.model.summary() 
		# pass
	
	
	
