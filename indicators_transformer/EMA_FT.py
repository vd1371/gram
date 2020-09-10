# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
import numpy as np
from utils.GlobalVariables import *

class EMA_FT(object):
	# Base class for all of the feature transformers
	def __init__(self):
		super(EMA_FT, self).__init__()

	def transform(self, df, features):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		# We might need to modify this in the future

		# Initializing the column
		df['EMA_FT'] = np.zeros(len(df))

		# Interpreting the values
		df.loc[df[CLOSE] > features, 'EMA_FT'] = LONG
		df.loc[df[CLOSE] < features, 'EMA_FT'] = SHORT

		# make everything clean
		out_series = df['EMA_FT']
		df.drop(columns=['EMA_FT'], inplace = True)

		# For test
		# df['EMA(20)'] = features
		# df['EMA(20)_transformed'] = out_series
		# df.to_csv("../test_reports/EMA_test/EMA20_transformed.csv")

		return out_series


if __name__ == "__main__":
	# Loading the data
	from data.FXDataLoader import Pair
	GBPUSD_data = Pair(GBPUSD)

	# Dataframe for test
	df = GBPUSD_data.get_1D()

	# Creating feature
	from indicators.EMA import EMA
	EMA = EMA(20, CLOSE)
	ema_values = EMA.calculate(df)

	# Transforming the Features
	ema_transformed = EMA_FT().transform(df, ema_values)

	print (ema_transformed)


