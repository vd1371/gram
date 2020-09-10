# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *

class FC(object):
	# Base class for all feature constructors
	def __init__(self):
		super(FC, self).__init__()

	def construct(self, df):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		raise NotImplementedError ("'constrcut' feature is not ")