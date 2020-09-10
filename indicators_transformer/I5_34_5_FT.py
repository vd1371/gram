# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
import numpy as np
from utils.GlobalVariables import *

class I5_34_5_FT(object):
	# Base class for all of the feature transformers
	def __init__(self):
		super(I5_34_5_FT, self).__init__()

	def transform(self, df, features):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		# We might need to modify this in the future

		# Initializing the column
		df['I5_34_5_FT'] = np.zeros(len(df))

		# Interpreting the values
		df.loc[features > 0, 'I5_34_5_FT'] = LONG
		df.loc[features < 0, 'I5_34_5_FT'] = SHORT

		# make everything clean
		out_series = df['I5_34_5_FT']
		df.drop(columns=['I5_34_5_FT'], inplace = True)

		# For test
		# df['I5_34_5(20)'] = features
		# df['I5_34_5(20)_transformed'] = out_series
		# df.to_csv("../test_reports/I5_34_520_transformed.csv")

		return out_series


if __name__ == "__main__":
	# Loading the data
	from data.FXDataLoader import Pair
	GBPUSD_data = Pair(GBPUSD)

	# Dataframe for test
	df = GBPUSD_data.get_1D()

	# Creating feature
	from indicators.I5_34_5 import I5_34_5
	I5_34_5 = I5_34_5()
	I5_34_5_values = I5_34_5.calculate(df)

	# Transforming the Features
	I5_34_5_transformed = I5_34_5_FT().transform(df, I5_34_5_values)

	print (I5_34_5_transformed)


