# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *

class DataLoader(object):
	# This class load the data of a given pair
	# IMPORTANT Make sure that the type of 'date' column values in the loaded data is panda.TimeStamp
	def __init__(self, pair, 1M = False, 5M = False, 1H = False, 4H = False, 1D = False):
		super(DataLoader, self).__init__()
		# TODO: complete this section
		if 1M: self._load_csv(1M)

	def _load_csv(self, name):
		'''
		Loads the csv from the data folder
		:params: name: name of the csv file
		:return: panda dataframe
		'''
		return

	