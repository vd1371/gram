# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *
from decision_models.BaseDecisionModel import BaseDecisionModel

import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout
from keras.regularizers import l1, l2

LOSS_FUNC = 'MSE'
OPTIMIZER = 'adam'

class SimpleNN(BaseDecisionModel):
	# Simple neural network for making decision based on input features

	def __init__(self, D, address, name, warm_up=False, n_trained=0):
		super(SimpleNN, self).__init__()
		'''	
		:params: D int : is the dimension of features (i.e., independent variables)
		:params: address str : is the address which model will be saved
		:params: name str : the model will be saved with this name
		:params: warm_up bolean : whether the model should be load in initialization or creadted
				if True, it will be loaded
		:params: n_trained int : number of times that the model has been trained
		'''
		self.D = D
		self.address = address
		self.name = name

		if warm_up:
			self.load(address, name)
		else:
			model = Sequential()
			model.add(Dense(D, input_dim = D, activation="tanh"))
			model.add(Dense(200, activation="relu"))
			model.add(Dense(3, activation="linear"))  # First one is for -1, 0, 1
			model.compile( loss=LOSS_FUNC, optimizer=OPTIMIZER)
			self.model = model

	def learn(self, X, Y):
		self.model.fit(np.atleast_2d(X), Y, epochs = 1, verbose = 0)

	def get_weights(self):
		return self.model.get_weights()

	def set_weights(self, weights):
		self.model.set_weights(weights)

	def predict_value(self, X):
		return self.model.predict(np.atleast_2d(X))

	def decide(self, X):
		return np.argmax(self.model.predict(np.atleast_2d(X)), axis =1)-1

	def save(self, address, name):
		dir = address + name + '.h5'
		self.model.save(dir)

	def load(self, address, name):
		dir = address + name + '.h5'
		self.model = load_model(dir)

if __name__ == '__main__':

	# Test for debugging
	# ----------------------------------------------------------------------------------------------------------#
	# Testing the matrix form
	# myModel = SimpleNN(40, "", 'Test', warm_up = False)
	# X = np.random.randn(100, 40)
	# Y = np.random.randn(100, 3)

	# myModel.learn(X, Y)
	# # print (myModel.get_weights())

	# X = np.random.randn(100, 40)
	# print (myModel.predict_value(X))
	# print (myModel.decide(X))
	# myModel.save("", 'Test')
	# myModel =SimpleNN(40, "", 'Test', warm_up=True)
	# ----------------------------------------------------------------------------------------------------------#


	# Test for functionality
	# ----------------------------------------------------------------------------------------------------------#
	# f(x0, x1, x2, x3, x4) = 2x0 - 6x1 + 3x2 - 4x3 + x4 + NORM.INV(RAND(), 0, 0.1)

	import pandas as pd
	from sklearn.model_selection import train_test_split
	from sklearn.metrics import mean_squared_error

	df = pd.read_csv("RegressionTest.csv", index_col = 0)

	X = df.iloc[:, :-3].to_numpy()
	Y = df.iloc[:, -3:].to_numpy()

	x_train, x_test, y_train, y_test = train_test_split(X, Y, shuffle = True, test_size = 0.2)

	myModel = SimpleNN(5, address = "", name = 'Regression_test', warm_up = False)

	epochs = 5000
	for it in range (epochs):
		if it % 10 == 0:

			y_test_pred = myModel.predict_value(x_test)

			y1_err = round(mean_squared_error(y_test[0], y_test_pred[0]),4)
			y2_err = round(mean_squared_error(y_test[1], y_test_pred[1]),4)
			y3_err = round(mean_squared_error(y_test[2], y_test_pred[2]),4)
			
			print (f"Epoch:{it}. Y1_MSE:{y1_err}, Y2_MSE:{y2_err}, Y3_MSE:{y3_err}")

		# mini batch gradient decent
		sample_size = 50
		for _ in range (int(len(x_train)/sample_size) + 1):
			choices = np.random.choice(len(x_train), sample_size, replace = False)
			x_sample = np.array([x_train[x_idx] for x_idx in choices])
			y_sample = np.array([y_train[y_idx] for y_idx in choices])
			myModel.learn(x_sample, y_sample)