# Adding parent directory to the PYTHONPATH
import sys
import os
import pandas as pd
from datetime import datetime
sys.path.insert(0, '..')
from utils.GlobalVariables import *


class Pair(object):
	def __init__(self, name = GBPUSD):
		super(Pair, self).__init__()
		self.name = name

		self._load_data()

	def _load_data(self):
		'''
		Inner method of the class Pair to load the data
		It loads the 1D, 4H, 1H, 5M and assign it to its corresponding attribute
		'''

		# creating the directory to rhe 
		dir = os.path.join('..','data','Forex', self.name, self.name)

		# loading the data
		self._1D = pd.read_csv(dir+'_1D.csv', index_col = 0)
		self._4H = pd.read_csv(dir+'_4H.csv', index_col = 0)
		self._1H = pd.read_csv(dir+'_1H.csv', index_col = 0)
		self._5M = pd.read_csv(dir+'_5M.csv', index_col = 0)

		# Temporarily adding to a list for checking the format
		all_dfs = [self._1D, self._4H, self._1H, self._5M]
		time_frames = ['1D', '4H', '1H', '5M']

		# Parsing the date column from string to timestamp
		def date_parser_1(date_as_str):
			# For the case index: 5/12/1993 0:00
			# There might be other cases so I named it date_parser_1
			return datetime.strptime(date_as_str, "%m/%d/%Y %H:%M")

		# Applying date parser to the indices
		for df in all_dfs:
			df.index = df.index.map(date_parser_1)

		# Checking the columns orders
		for df, tf in zip(all_dfs, time_frames):
			if list(df.columns) != [PAIR, OPEN, HIGH, LOW, CLOSE]:
				raise NameError(f"Columns are not written correctly, please modify"\
								f" Check Pair: {self.pair} - Timeframe : {tf}")

			if df.index.name != DATE:
				raise NameError(f"Index column must be 'Date'"\
								f"Check Pair: {self.pair} - Timeframe : {tf}")

	def get_1D(self):
		return self._1D

	def get_4H(self):
		return self._4H

	def get_1H(self):
		return self._1H

	def get_5M(self):
		return self._5M


if __name__ == '__main__':
	GBPUSD_data = Pair(GBPUSD)
	print (GBPUSD_data.get_1D())
	print (GBPUSD_data.get_4H())
	print (GBPUSD_data.get_1H())
	print (GBPUSD_data.get_5M())
