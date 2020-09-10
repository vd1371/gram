# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *

class FT(object):
	# Base class for all of the feature transformers
	def __init__(self):
		super(FT, self).__init__()

	def transform(self, df):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		# We might need to modify this in the future
		raise NotImplementedError ("'transform' feature is not ")