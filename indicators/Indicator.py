# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *

class Indicator(object):
	# Base class for indicators
	def __init__(self):
		super(Indicator, self).__init__()

	def calculate(self, df=None):
		'''
		# Calcualte method gets df (a python dataframe) as input
		# It calculates the values of the indicator and returns a panda series
		# this panda series must have the same index as the panda dataframe so it could be appendable when being used
		:param: df
		:param: indicator attributes
		:return: panda or dataframe including ONLY the calculated values of the indicator
		'''
		raise NotImplementedError("'calculate' method is not implemented yet")