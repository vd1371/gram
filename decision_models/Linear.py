# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *
from decision_models.BaseDecisionModel import BaseDecisionModel

import numpy as np
import pandas as pd

class Linear(BaseDecisionModel):
	# Linear model for decision making
	def __init__(self, D, address, name, warm_up = False, n_trained = 0, use_intercept = True):
		super(Linear, self).__init__()
		'''	
		:params: D int : is the dimension of features (i.e., independent variables)
		:params: address str : is the address which model will be saved
		:params: name str : the model will be saved with this name
		:params: warm_up bolean : whether the model should be load in initialization or creadted
				if True, it will be loaded
		:params: n_trained int : number of times that the model has been trained
		'''
		self.use_intercept = use_intercept

		self.D = D
		if self.use_intercept: self.D = self.D + 1

		self.address = address
		self.name = name
		# The model has three vectors, each vector corresponds to a decision namely SHORT, WAIT, LONG
		if warm_up:
			self.load(address, name)
		else:
			self.model = np.random.randn(3, self.D) / np.sqrt(self.D)

	def learn(self, X, Y, action, lr = 0.0002):
		# Gradient descent algorithm
		# action is -1, 0, 1 for decisions, then we only apply gradient decent on the correspongfing model
		# by reaching that model in self.model
		# action+1 is for indexing
		X = np.atleast_2d(X)
		if self.use_intercept:
			intercept = np.ones((X.shape[0], 1))
			X = np.append(X, intercept, axis = 1)

		self.model[action+1] += lr * (Y - X.dot(self.model[action+1])/X.shape[0]).dot(X)

	def get_weights(self):
		return self.model

	def set_weights(self, weights):
		self.model = weights

	def predict_value(self, X):
		if self.use_intercept:
			intercept = np.ones((X.shape[0], 1))
			X = np.append(X, intercept, axis = 1)
			
		return X.dot(np.transpose(self.model))

	def decide(self, X):
		# The "-1" at the end is for indexing
		# ... to convert the index to decision
		return np.argmax(self.predict_value(X), axis = 1) - 1

	def save(self, address, name):
		df = pd.DataFrame(np.transpose(self.model), columns = ['SHORT', 'WAIT', 'LONG'])
		dir = address + name + '.csv'
		df.to_csv(dir)

	def load(self, address, name):
		dir = address + name + '.csv'
		self.model = np.transpose(np.array(pd.read_csv(dir, index_col = 0)))

if __name__ == '__main__':

	# Test for debugging
	# ----------------------------------------------------------------------------------------------------------#
	# Testing the matrix form
	# myModel = Linear(40, "", 'Test', warm_up = False)
	# X = np.random.randn(100, 40)
	# Y = np.random.randn(100)

	# LONG, WAIT, SHORT = 1, 0, -1
	# myModel.learn(X, Y, LONG)
	# # print (myModel.get_weights())

	# X = np.random.randn(100, 40)
	# print (myModel.predict_value(X))
	# print (myModel.decide(X))
	# myModel.save("", 'Test')
	# myModel =Linear(40, "", 'Test', warm_up=True)
	# print (myModel.predict_value(X))
	# print (myModel.decide(X))



	# ----------------------------------------------------------------------------------------------------------#
	# Test for functionality
	# ----------------------------------------------------------------------------------------------------------#
	# Y1 = 2x0 + x1 + NORM.INV(RAND(), 0, 0.1)
	# Y2 = 3x1 + x2 + x3 + NORM.INV(RAND(), 0, 0.1)
	# Y3 = x3 + 3x4 + NORM.INV(RAND(), 0, 0.1)
	# Average of the Y in the Regression test is -2 with range equal to 12. Hence, I created 3 categories
	# Y > 0 : 1, -4 < Y < 0 : 0, Y < -4 : -1

	import pandas as pd
	from sklearn.model_selection import train_test_split
	from sklearn.metrics import mean_squared_error

	df = pd.read_csv("RegressionTest.csv", index_col = 0)

	X = df.iloc[:, :-3].to_numpy()
	Y = df.iloc[:, -3:].to_numpy()

	x_train, x_test, y_train, y_test = train_test_split(X, Y, shuffle = True, test_size = 0.2)


	myModel = Linear(5, address = "", name = 'Regression_test', warm_up = False)
	epochs = 5000
	for it in range (epochs):
		if it % 10 == 0:

			y_test_pred = myModel.predict_value(x_test)

			y1_err = round(mean_squared_error(y_test[0], y_test_pred[0]),4)
			y2_err = round(mean_squared_error(y_test[1], y_test_pred[1]),4)
			y3_err = round(mean_squared_error(y_test[2], y_test_pred[2]),4)
			
			print (f"Epoch:{it}. Y1_MSE:{y1_err}, Y2_MSE:{y2_err}, Y3_MSE:{y3_err}")

		for x, y in zip (x_train, y_train):

			myModel.learn(x, [y[0]], -1)
			myModel.learn(x, [y[1]], 0)
			myModel.learn(x, [y[2]], 1)


