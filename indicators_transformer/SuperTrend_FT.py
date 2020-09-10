# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
import numpy as np
from utils.GlobalVariables import *

class SuperTrend_FT(object):
	# Base class for all of the feature transformers
	def __init__(self):
		super(SuperTrend_FT, self).__init__()

	def transform(self, df, features):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		# We might need to modify this in the future

		# Initializing the column
		df['SuperTrend_FT'] = np.zeros(len(df))

		# Interpreting the values
		df.loc[df[CLOSE] < features, 'SuperTrend_FT'] = LONG
		df.loc[df[CLOSE] > features, 'SuperTrend_FT'] = SHORT

		# make everything clean
		out_series = df['SuperTrend_FT']
		df.drop(columns=['SuperTrend_FT'], inplace = True)

		# For test
		# df['SuperTrend(20)'] = features
		# df['SuperTrend(20)_transformed'] = out_series
		# df.to_csv("../test_reports/SuperTrend_test/SuperTrend20_transformed.csv")

		return out_series


if __name__ == "__main__":
	# Loading the data
	from data.FXDataLoader import Pair
	GBPUSD_data = Pair(GBPUSD)

	# Dataframe for test
	df = GBPUSD_data.get_1D()

	# Creating feature
	from indicators.SuperTrend import SuperTrend
	SuperTrend = SuperTrend(10, 3)
	SuperTrend_values = SuperTrend.calculate(df)

	# Transforming the Features
	SuperTrend_transformed = SuperTrend_FT().transform(df, SuperTrend_values)

	print (SuperTrend_transformed)


