# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *

class FG(object):
	# Base class for all feature constructors
	def __init__(self):
		super(FG, self).__init__()

	def generate_all_features(self, df):
		return NotImplementedError ("'generate' feature is not implemented yet")
		
	def generate(self, idx):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		raise NotImplementedError ("'constrcut' feature is not implemented yet")