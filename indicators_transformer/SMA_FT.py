# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
import numpy as np
from utils.GlobalVariables import *

class SMA_FT(object):
	# Base class for all of the feature transformers
	def __init__(self):
		super(SMA_FT, self).__init__()

	def transform(self, df, features):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		# We might need to modify this in the future

		# Initializing the column
		df['SMA_FT'] = np.zeros(len(df))

		# Interpreting the values
		df.loc[df[CLOSE] > features, 'SMA_FT'] = LONG
		df.loc[df[CLOSE] < features, 'SMA_FT'] = SHORT

		# make everything clean
		out_series = df['SMA_FT']
		df.drop(columns=['SMA_FT'], inplace = True)

		# For test
		# df['SMA(20)'] = features
		# df['SMA(20)_transformed'] = out_series
		# df.to_csv("../test_reports/SMA_test/SMA20_transformed.csv")

		return out_series


if __name__ == "__main__":
	# Loading the data
	from data.FXDataLoader import Pair
	GBPUSD_data = Pair(GBPUSD)

	# Dataframe for test
	df = GBPUSD_data.get_1D()

	# Creating feature
	from indicators.SMA import SMA
	sma = SMA(20, CLOSE)
	sma_values = sma.calculate(df)

	# Transforming the Features
	sma_transformed = SMA_FT().transform(df, sma_values)

	print (sma_transformed)


