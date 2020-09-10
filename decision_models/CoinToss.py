# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *
from decision_models.BaseDecisionModel import BaseDecisionModel

import numpy as np

class CoinToss(BaseDecisionModel):
	# CoinToss decision maker which opens and closes a position randomly
	def __init__(self, D = 5):
		super(CoinToss, self).__init__()
		self.D = D

	def learn(self, *args):
		pass

	def get_weights(self):
		pass

	def predict_value(self, X):
		return np.random.randn(X.shape[0])

	def decide(self, X):
		return np.random.randint(3, size = X.shape[0]) - 1

	def save(self, *args):
		pass

	def load(self, *args):
		pass

if __name__ == '__main__':
	# Testing the matrix form
	myModel = CoinToss(40)
	X = np.random.randn(100, 40)
	Y = np.random.randn(100, 3)

	myModel.learn(X, Y)
	# print (myModel.get_weights())

	X = np.random.randn(100, 40)
	print (myModel.predict_value(X))
	print (myModel.decide(X))
	myModel.save("", 'Test')
	myModel =CoinToss(40)

