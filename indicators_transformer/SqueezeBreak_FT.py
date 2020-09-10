# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
import numpy as np
from utils.GlobalVariables import *

class SqueezeBreak_FT(object):
	# Base class for all of the feature transformers
	def __init__(self):
		super(SqueezeBreak_FT, self).__init__()

	def transform(self, df, features):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		# We might need to modify this in the future

		# Initializing the column
		df['SqueezeBreak_FT'] = np.zeros(len(df))

		# Interpreting the values
		df.loc[features > 0, 'SqueezeBreak_FT'] = TRADE
		df.loc[features < 0, 'SqueezeBreak_FT'] = WAIT

		# make everything clean
		out_series = df['SqueezeBreak_FT']
		df.drop(columns=['SqueezeBreak_FT'], inplace = True)

		# For test
		# df['SqueezeBreak(14-20)'] = features
		# df['SqueezeBreak(14-20)_transformed'] = out_series
		# df.to_csv("../test_reports/SqueezeBreak_test/SqueezeBreak(14-20)_transformed.csv")

		return out_series


if __name__ == "__main__":
	# Loading the data
	from data.FXDataLoader import Pair
	GBPUSD_data = Pair(GBPUSD)

	# Dataframe for test
	df = GBPUSD_data.get_1D()

	# Creating feature
	from indicators.SqueezeBreak import SqueezeBreak
	squeezebreak = SqueezeBreak(14, 20)
	squeezebreak_values = squeezebreak.calculate(df)

	# Transforming the Features
	squeezebreak_transformed = SqueezeBreak_FT().transform(df, squeezebreak_values)

	print (squeezebreak_transformed)


